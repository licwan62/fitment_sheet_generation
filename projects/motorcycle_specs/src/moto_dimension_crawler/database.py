from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable


SCHEMA = """
CREATE TABLE IF NOT EXISTS input_records (input_id TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT DEFAULT 'PENDING');
CREATE TABLE IF NOT EXISTS candidate_pages (input_id TEXT, url TEXT, payload TEXT NOT NULL, PRIMARY KEY(input_id,url));
CREATE TABLE IF NOT EXISTS fetch_tasks (url TEXT PRIMARY KEY, status TEXT, attempts INTEGER DEFAULT 0, error TEXT);
CREATE TABLE IF NOT EXISTS page_cache (url TEXT PRIMARY KEY, cache_path TEXT, content_hash TEXT, fetched_at TEXT, status_code INTEGER, metadata TEXT);
CREATE TABLE IF NOT EXISTS match_results (input_id TEXT, url TEXT, payload TEXT, PRIMARY KEY(input_id,url));
CREATE TABLE IF NOT EXISTS dimension_results (input_id TEXT, url TEXT, payload TEXT, parsed_at TEXT, PRIMARY KEY(input_id,url));
CREATE TABLE IF NOT EXISTS errors (id INTEGER PRIMARY KEY AUTOINCREMENT, phase TEXT, input_id TEXT, url TEXT, message TEXT, created_at TEXT);
"""


class StateDB:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def upsert_json(self, table: str, keys: dict[str, Any], payload: dict[str, Any], extra: dict[str, Any] | None = None, commit: bool = True) -> None:
        allowed = {"input_records", "candidate_pages", "match_results", "dimension_results"}
        if table not in allowed:
            raise ValueError(table)
        data = {**keys, "payload": json.dumps(payload, ensure_ascii=False), **(extra or {})}
        cols = ",".join(data)
        marks = ",".join("?" for _ in data)
        updates = ",".join(f"{c}=excluded.{c}" for c in data if c not in keys)
        self.conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({marks}) ON CONFLICT DO UPDATE SET {updates}", tuple(data.values()))
        if commit:
            self.conn.commit()

    def rows(self, table: str) -> list[dict[str, Any]]:
        allowed = {"input_records", "candidate_pages", "page_cache", "match_results", "dimension_results", "errors"}
        if table not in allowed:
            raise ValueError(table)
        result = []
        for row in self.conn.execute(f"SELECT * FROM {table}"):
            item = dict(row)
            if item.get("payload"):
                item.update(json.loads(item.pop("payload")))
            result.append(item)
        return result

    def cached(self, url: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM page_cache WHERE url=?", (url,)).fetchone()
        return dict(row) if row else None

    def save_cache(self, meta: dict[str, Any]) -> None:
        self.conn.execute("""INSERT INTO page_cache(url,cache_path,content_hash,fetched_at,status_code,metadata)
          VALUES(?,?,?,?,?,?) ON CONFLICT(url) DO UPDATE SET cache_path=excluded.cache_path,content_hash=excluded.content_hash,
          fetched_at=excluded.fetched_at,status_code=excluded.status_code,metadata=excluded.metadata""",
          (meta["url"], meta["cache_path"], meta["content_hash"], meta["fetched_at"], meta["status_code"], json.dumps(meta, ensure_ascii=False)))
        self.conn.commit()

    def parsed(self, input_id: str, url: str) -> bool:
        return self.conn.execute("SELECT 1 FROM dimension_results WHERE input_id=? AND url=?", (input_id, url)).fetchone() is not None

    def error(self, phase: str, message: str, created_at: str, input_id: str = "", url: str = "") -> None:
        self.conn.execute("INSERT INTO errors(phase,input_id,url,message,created_at) VALUES(?,?,?,?,?)", (phase,input_id,url,message,created_at))
        self.conn.commit()
