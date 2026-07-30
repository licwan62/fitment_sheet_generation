from __future__ import annotations

import re
import unicodedata


PUNCT_RE = re.compile(r"[-_/.,'\"()\[\]]+")
BOUNDARY_RE = re.compile(r"(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])")


def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKC", str(value or "")).casefold().strip()
    value = PUNCT_RE.sub(" ", value)
    value = BOUNDARY_RE.sub(" ", value)
    return " ".join(value.split())


def compact_name(value: str) -> str:
    return re.sub(r"\s+", "", normalize_name(value))


def number_tokens(value: str) -> list[str]:
    return re.findall(r"\d+(?:\.\d+)?", normalize_name(value))


def word_tokens(value: str) -> list[str]:
    return re.findall(r"[a-z]+", normalize_name(value))


def equivalent(a: str, b: str) -> bool:
    return compact_name(a) == compact_name(b)

