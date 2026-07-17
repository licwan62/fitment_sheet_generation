from __future__ import annotations

from urllib.parse import urljoin, urlparse
from pathlib import Path
import json
import re

from bs4 import BeautifulSoup

from .crawler import Crawler
from .year_parser import parse_year
from .normalizer import compact_name


def links_from_html(html: str, base_url: str, discovered_from: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    rows, seen = [], set()
    for anchor in soup.select("a[href]"):
        url = urljoin(base_url, anchor.get("href", ""))
        image = anchor.find("img")
        title = anchor.get_text(" ", strip=True) or anchor.get("title", "") or (image.get("alt", "") if image else "")
        if not title:
            title = Path(urlparse(url).path).stem.replace("-", " ").replace("_", " ")
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or "motorcyclespecs.co.za" not in parsed.netloc.lower() or not title:
            continue
        key = url.split("#", 1)[0]
        if key in seen:
            continue
        seen.add(key)
        year, _, _ = parse_year(title + " " + url)
        rows.append({"page_url": key, "page_title": title, "brand_guess": "", "model_guess": title,
                     "year_guess": year, "version_guess": "", "discovered_from": discovered_from})
    return rows


def build_index(crawler: Crawler, base_url: str, brands: set[str] | None = None) -> list[dict]:
    html, _, _ = crawler.fetch(base_url)
    if not html:
        return []
    index = links_from_html(html, base_url, base_url)
    # This is deliberately targeted: only catalog pages linked by the site's home page.
    brands = {compact_name(b) for b in (brands or set())}
    catalog = [r for r in index if "/bikes/" in r["page_url"].lower() and (not brands or compact_name(r["page_title"]) in brands)]
    for row in catalog[:80]:
        # Brand catalogs can be split into bmw.html, bmw2.html, bmw3.html, etc.
        # Follow only that catalog family, never unrelated brands or model pages.
        seed_path = Path(urlparse(row["page_url"]).path)
        seed_stem = seed_path.stem.casefold()
        pending = [row["page_url"]]
        visited_catalogs = set()
        while pending and len(visited_catalogs) < 30:
            catalog_url = pending.pop(0)
            if catalog_url in visited_catalogs:
                continue
            visited_catalogs.add(catalog_url)
            sub_html, _, _ = crawler.fetch(catalog_url)
            if not sub_html:
                continue
            children = links_from_html(sub_html, catalog_url, catalog_url)
            for child in children:
                child["brand_guess"] = row["page_title"]
                child_path = Path(urlparse(child["page_url"]).path)
                same_dir = child_path.parent == seed_path.parent
                is_catalog_page = bool(re.fullmatch(re.escape(seed_stem) + r"\d*", child_path.stem.casefold()))
                if same_dir and is_catalog_page and child["page_url"] not in visited_catalogs:
                    pending.append(child["page_url"])
            index.extend(children)
    dedup = {r["page_url"]: r for r in index}
    return list(dedup.values())


def save_index(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def load_index(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
