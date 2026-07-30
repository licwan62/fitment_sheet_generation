from __future__ import annotations

from urllib.parse import parse_qs, urljoin, urlparse
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


def _bikez_links(html: str, base_url: str, discovered_from: str, brand: str) -> list[dict]:
    """Extract Bikez model pages from one brand catalog page."""
    soup = BeautifulSoup(html, "lxml")
    rows, seen = [], set()
    for anchor in soup.select("a[href]"):
        url = urljoin(base_url, anchor.get("href", "")).split("#", 1)[0]
        parsed = urlparse(url)
        if parsed.netloc.casefold() not in {"bikez.com", "www.bikez.com"}:
            continue
        if not re.fullmatch(r"/motorcycles/[^/]+\.php", parsed.path, re.I) or url in seen:
            continue
        seen.add(url)
        title = anchor.get_text(" ", strip=True)
        if not title:
            title = Path(parsed.path).stem.replace("_", " ")
        year, _, _ = parse_year(f"{title} {url}")
        rows.append({
            "page_url": url,
            "page_title": title,
            "brand_guess": brand,
            "model_guess": title,
            "year_guess": year,
            "version_guess": "",
            "discovered_from": discovered_from,
            "source_name": "bikez",
            "source_priority": 2,
        })
    return rows


def build_bikez_index(crawler: Crawler, base_url: str, brands: set[str] | None = None,
                      priority: int = 2) -> list[dict]:
    """Build a targeted Bikez index by following only requested brand catalogs."""
    brands_url = urljoin(base_url, "/brands/index.php")
    html, _, _ = crawler.fetch(brands_url)
    if not html:
        return []
    wanted = {compact_name(brand): brand for brand in (brands or set())}
    soup = BeautifulSoup(html, "lxml")
    catalogs: list[tuple[str, str]] = []
    for anchor in soup.select("a[href]"):
        url = urljoin(brands_url, anchor.get("href", ""))
        if not re.fullmatch(r"/brand/[^/]+_motorcycles\.php", urlparse(url).path, re.I):
            continue
        label = re.sub(r"\s+motorcycles.*$", "", anchor.get_text(" ", strip=True), flags=re.I)
        compact = compact_name(label)
        if not wanted or compact in wanted:
            catalogs.append((url, wanted.get(compact, label)))

    index: list[dict] = []
    for seed_url, brand in dict(catalogs).items():
        pending, visited = [seed_url], set()
        seed_path = urlparse(seed_url).path
        while pending and len(visited) < 50:
            catalog_url = pending.pop(0)
            if catalog_url in visited:
                continue
            visited.add(catalog_url)
            page_html, _, _ = crawler.fetch(catalog_url)
            if not page_html:
                continue
            rows = _bikez_links(page_html, catalog_url, catalog_url, brand)
            for row in rows:
                row["source_priority"] = priority
            index.extend(rows)
            page_soup = BeautifulSoup(page_html, "lxml")
            for anchor in page_soup.select("a[href]"):
                page_url = urljoin(catalog_url, anchor.get("href", "")).split("#", 1)[0]
                parsed = urlparse(page_url)
                page_values = parse_qs(parsed.query).get("page", [])
                if parsed.path == seed_path and page_values and page_values[0].isdigit() and page_url not in visited:
                    pending.append(page_url)
    return list({row["page_url"]: row for row in index}.values())


def build_bikedekho_index(crawler: Crawler, base_url: str, brands: set[str] | None = None,
                          priority: int = 2) -> list[dict]:
    """Build BikeDekho candidates from its compact, robots-advertised specs sitemap."""
    sitemap_url = urljoin(base_url, "/ModelSpecifications.xml")
    xml, _, _ = crawler.fetch(sitemap_url)
    if not xml:
        return []
    wanted = {compact_name(brand): brand for brand in (brands or set())}
    soup = BeautifulSoup(xml, "xml")
    rows = []
    for loc in soup.find_all("loc"):
        url = loc.get_text(strip=True)
        parsed = urlparse(url)
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) != 3 or parts[-1].casefold() != "specifications" or parts[0].casefold() == "hi":
            continue
        brand_slug, model_slug = parts[0], parts[1]
        brand_compact = compact_name(re.sub(r"-(?:bikes|scooters)$", "", brand_slug, flags=re.I))
        matched_brand = next(
            (display for compact, display in wanted.items()
             if brand_compact == compact or compact_name(brand_slug).startswith(compact)),
            "" if wanted else brand_slug.replace("-", " ").title(),
        )
        if wanted and not matched_brand:
            continue
        model = model_slug.replace("-", " ")
        title = f"{matched_brand} {model}".strip()
        year, _, _ = parse_year(f"{title} {url}")
        rows.append({
            "page_url": url,
            "page_title": title,
            "brand_guess": matched_brand,
            "model_guess": model,
            "year_guess": year,
            "version_guess": "",
            "discovered_from": sitemap_url,
            "source_name": "bikedekho",
            "source_priority": priority,
        })
    return list({row["page_url"]: row for row in rows}.values())


def build_1000ps_index(crawler: Crawler, base_url: str, brands: set[str] | None = None,
                       priority: int = 2) -> list[dict]:
    """Build a targeted 1000PS model index from its public brand directory."""
    brands_url = urljoin(base_url, "/en-gb/brands")
    html, _, _ = crawler.fetch(brands_url)
    if not html:
        return []
    wanted = {compact_name(brand): brand for brand in (brands or set())}
    soup = BeautifulSoup(html, "lxml")
    catalogs: dict[str, str] = {}
    for anchor in soup.select("a[href]"):
        url = urljoin(brands_url, anchor.get("href", "")).split("#", 1)[0]
        match = re.fullmatch(r"/en-gb/brand/\d+/([^/?#]+)", urlparse(url).path, re.I)
        if not match:
            continue
        compact = compact_name(match.group(1).replace("-", " "))
        if not wanted or compact in wanted:
            catalogs[url] = wanted.get(compact, match.group(1).replace("-", " ").title())

    rows = []
    for catalog_url, brand in catalogs.items():
        page_html, _, _ = crawler.fetch(catalog_url)
        if not page_html:
            continue
        page_soup = BeautifulSoup(page_html, "lxml")
        for anchor in page_soup.select("a[href]"):
            url = urljoin(catalog_url, anchor.get("href", "")).split("#", 1)[0]
            match = re.fullmatch(r"/en-gb/model/\d+/([^/?#]+)", urlparse(url).path, re.I)
            if not match:
                continue
            model_slug = match.group(1)
            title = model_slug.replace("-", " ")
            rows.append({
                "page_url": url,
                "page_title": title,
                "brand_guess": brand,
                "model_guess": title,
                "year_guess": "",
                "version_guess": "",
                "discovered_from": catalog_url,
                "source_name": "1000ps",
                "source_priority": priority,
            })
    return list({row["page_url"]: row for row in rows}.values())


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
                child["source_name"] = "motorcyclespecs"
                child["source_priority"] = 1
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
