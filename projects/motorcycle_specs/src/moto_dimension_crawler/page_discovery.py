from __future__ import annotations

from .models import InputRecord
from .normalizer import compact_name, word_tokens


def targeted_pages(record: InputRecord, index: list[dict]) -> list[dict]:
    """Cheap prefilter before the strict matcher; avoids per-record site traversal."""
    make = compact_name(record.make)
    nums = record.number_tokens
    result = []
    for page in index:
        haystack = compact_name(page.get("brand_guess", "") + " " + page.get("page_title", "") + " " + page.get("page_url", ""))
        if make and make not in haystack:
            continue
        if nums and not all(n in haystack for n in nums):
            continue
        record_words = record.word_tokens
        brand_words = set(word_tokens(record.make)) | set(word_tokens(page.get("brand_guess", "")))
        page_words = [word for word in word_tokens(page.get("page_title", "")) if word not in brand_words]
        if record_words and (not page_words or record_words[0] != page_words[0]):
            continue
        result.append(page)
    return result
