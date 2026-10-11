import json
import os
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("DATABASE_PATH", Path(__file__).with_name("regulaai.db")))


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize() -> None:
    with connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS assessment_runs (
                id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def list_records(table: str) -> list[dict[str, Any]]:
    if table not in {"documents", "audit_events", "assessment_runs"}:
        raise ValueError("Unsupported table")
    initialize()
    with connect() as connection:
        rows = connection.execute(f"SELECT payload FROM {table} ORDER BY created_at DESC").fetchall()
    return [json.loads(row["payload"]) for row in rows]


def save_record(table: str, record: dict[str, Any]) -> None:
    if table not in {"documents", "audit_events", "assessment_runs"}:
        raise ValueError("Unsupported table")
    initialize()
    with connect() as connection:
        connection.execute(
            f"INSERT OR REPLACE INTO {table} (id, payload, created_at) VALUES (?, ?, ?)",
            (record["id"], json.dumps(record), record.get("uploaded_at") or record.get("timestamp", "")),
        )
        connection.commit()


def seed_records(table: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    existing = list_records(table)
    if existing:
        return existing
    for record in records:
        save_record(table, record)
    return list_records(table)
