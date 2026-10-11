from retrieval import citation_is_supported, lexical_search


def test_lexical_retrieval_is_bounded_and_source_aware():
    chunks = [
        {"id": "CHK-1", "text": "Quarterly certification evidence is required.", "source_location": "page:1"},
        {"id": "CHK-2", "text": "Privileged access is reviewed quarterly.", "source_location": "page:4"},
    ]
    results = lexical_search(chunks, "certification evidence", limit=1)
    assert len(results) == 1
    assert results[0].chunk_id == "CHK-1"
    assert results[0].source_location == "page:1"


def test_unsupported_citation_is_not_verified():
    assert citation_is_supported(["CHK-1"], "CHK-1") is True
    assert citation_is_supported(["CHK-1"], "CHK-999") is False