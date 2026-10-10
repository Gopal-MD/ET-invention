from io import BytesIO

import pytest

from document_parser import DocumentParseError, parse_document


def test_txt_parser_creates_stable_source_chunk():
    first = parse_document("policy.txt", b"Maintain quarterly evidence for regulatory reports.")
    second = parse_document("policy.txt", b"Maintain quarterly evidence for regulatory reports.")
    assert first.parser == "utf8-text"
    assert first.chunks[0].id == second.chunks[0].id
    assert first.chunks[0].source_location == "text:1"


def test_empty_text_is_rejected():
    with pytest.raises(DocumentParseError, match="no extractable text"):
        parse_document("empty.txt", b"\n")


def test_pdf_parser_preserves_page_reference():
    fitz = pytest.importorskip("fitz")
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Quarterly certification is required.")
    parsed = parse_document("sample.pdf", document.tobytes())
    assert parsed.parser == "pymupdf"
    assert parsed.chunks[0].page == 1
    assert parsed.chunks[0].source_location == "page:1"


def test_docx_parser_extracts_paragraph_text():
    docx = pytest.importorskip("docx")
    document = docx.Document()
    document.add_paragraph("Evidence must be retained.")
    stream = BytesIO()
    document.save(stream)
    parsed = parse_document("sample.docx", stream.getvalue())
    assert parsed.parser == "python-docx"
    assert "Evidence must be retained" in parsed.text