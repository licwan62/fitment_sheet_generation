from __future__ import annotations

from bs4 import BeautifulSoup

from .dimension_parser import parse_dimensions
from .year_parser import parse_year


def visible_text(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "lxml")
    for node in soup(["script", "style", "noscript"]):
        node.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    h1 = soup.find("h1")
    heading = h1.get_text(" ", strip=True) if h1 else ""
    return "\n".join(soup.stripped_strings), heading or title


def parse_page(html: str, url: str) -> dict:
    text, title = visible_text(html)
    dimensions = parse_dimensions(text)
    year, year_start, year_end = parse_year(f"{title} {url} {text[:1000]}")
    return {
        "page_title": title, "year": year, "year_start": year_start, "year_end": year_end,
        "dimensions": dimensions,
    }

