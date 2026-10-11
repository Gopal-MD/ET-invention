from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True)
class RetrievalResult:
    chunk_id: str
    text: str
    source_location: str
    score: int


def lexical_search(chunks: Iterable[dict], query: str, limit: int = 5) -> list[RetrievalResult]:
    terms = {term for term in re.findall(r"[a-z0-9]+", query.lower()) if len(term) > 2}
    if not terms:
        return []
    results: list[RetrievalResult] = []
    for chunk in chunks:
        words = set(re.findall(r"[a-z0-9]+", chunk.get("text", "").lower()))
        score = len(terms & words)
        if score:
            results.append(RetrievalResult(chunk["id"], chunk["text"], chunk.get("source_location", "unknown"), score))
    return sorted(results, key=lambda result: result.score, reverse=True)[:max(1, min(limit, 20))]


def citation_is_supported(chunk_ids: Iterable[str], citation_id: str) -> bool:
    return citation_id in set(chunk_ids)
