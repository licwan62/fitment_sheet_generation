from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup

from .utils import stable_hash, utc_now


class PageCache:
    def __init__(self, root: Path):
        self.html_dir = root / "html"
        self.meta_dir = root / "metadata"
        self.html_dir.mkdir(parents=True, exist_ok=True)
        self.meta_dir.mkdir(parents=True, exist_ok=True)

    def paths(self, url: str) -> tuple[Path, Path]:
        key = stable_hash(url)
        return self.html_dir / f"{key}.html", self.meta_dir / f"{key}.json"

    def valid(self, url: str) -> bool:
        html, meta = self.paths(url)
        return html.is_file() and meta.is_file() and html.stat().st_size > 0

    def read(self, url: str) -> str:
        return self.paths(url)[0].read_text(encoding="utf-8")

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
        return meta

