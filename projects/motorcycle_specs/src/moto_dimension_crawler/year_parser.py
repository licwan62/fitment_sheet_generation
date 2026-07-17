from __future__ import annotations

import re


YEAR_RE = re.compile(r"\b((?:19|20)\d{2})(?:\s*[-–—/]\s*((?:19|20)\d{2}))?\b")


def parse_year(text: str) -> tuple[str, str, str]:
    match = YEAR_RE.search(text or "")
    if not match:
        return "", "", ""
    start, end = match.group(1), match.group(2) or match.group(1)
    return start if start == end else "", start, end

