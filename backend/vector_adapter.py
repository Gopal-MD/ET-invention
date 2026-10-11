import os
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass
class VectorRecord:
    id: str
    text: str
    score: float
    source: str


class VectorAdapter:
    def __init__(self, connection_string: str | None = None):
        self.connection_string = connection_string or os.getenv("POSTGRES_DSN")

    def is_available(self) -> bool:
        return bool(self.connection_string)

    def search(self, query: str, limit: int = 5, chunks: Iterable[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        if not chunks:
            return []
        normalized = query.lower().strip()
        matches: list[dict[str, Any]] = []
        for chunk in chunks:
            text = str(chunk.get("text", "")).lower()
            if normalized and normalized not in text:
                continue
            matches.append(
                {
                    "id": chunk.get("id", "chunk-unknown"),
                    "text": chunk.get("text", ""),
                    "score": round(0.90 if normalized in text else 0.50, 4),
                    "source": chunk.get("source_location", "document"),
                }
            )
        return matches[:limit]
