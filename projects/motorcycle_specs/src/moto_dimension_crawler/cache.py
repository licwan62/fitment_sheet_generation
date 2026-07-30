from __future__ import annotations

import json
import time
from pathlib import Path

from bs4 import BeautifulSoup

from .utils import stable_hash, utc_now


class PageCache:
    def __init__(self, root: Path):
        self.html_dir = root / "html"
        self.meta_dir = root / "metadata"
        self.failure_dir = root / "failures"
        self.html_dir.mkdir(parents=True, exist_ok=True)
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        self.failure_dir.mkdir(parents=True, exist_ok=True)

    def paths(self, url: str) -> tuple[Path, Path]:
        key = stable_hash(url)
        return self.html_dir / f"{key}.html", self.meta_dir / f"{key}.json"

    def valid(self, url: str) -> bool:
        html, meta = self.paths(url)
        return html.is_file() and meta.is_file() and html.stat().st_size > 0

    def read(self, url: str) -> str:
        return self.paths(url)[0].read_text(encoding="utf-8")

    def failure_path(self, url: str) -> Path:
        return self.failure_dir / f"{stable_hash(url)}.json"

    def read_failure(self, url: str) -> dict | None:
        path = self.failure_path(url)
        if not path.is_file():
            return None
        try:
            failure = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
        if float(failure.get("retry_after", 0)) <= time.time():
            path.unlink(missing_ok=True)
            return None
        return failure

    def write_failure(self, url: str, error: str, status_code: int | None, cache_seconds: int) -> dict:
        failure = {
            "url": url,
            "error": error,
            "status_code": status_code,
            "failed_at": utc_now(),
            "retry_after": time.time() + max(0, cache_seconds),
        }
        self.failure_path(url).write_text(
            json.dumps(failure, ensure_ascii=False, indent=2), encoding="utf-8",
        )
        return failure

    def clear_failure(self, url: str) -> None:
        self.failure_path(url).unlink(missing_ok=True)

    def write(self, url: str, content: bytes, status_code: int, encoding: str) -> dict:
        html_path, meta_path = self.paths(url)
        text = content.decode(encoding or "utf-8", errors="replace")
        html_path.write_text(text, encoding="utf-8")
        soup = BeautifulSoup(text, "lxml")
        meta = {
            "url": url, "status_code": status_code, "fetched_at": utc_now(),
            "content_hash": stable_hash(text), "encoding": encoding or "utf-8",
            "page_title": soup.title.get_text(" ", strip=True) if soup.title else "",
            "cache_path": str(html_path.resolve()),
        }
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        self.clear_failure(url)
        return meta

