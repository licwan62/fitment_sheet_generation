from __future__ import annotations

import re
from collections import defaultdict

from rapidfuzz.fuzz import ratio

from .models import InputRecord
from .normalizer import compact_name, normalize_name, number_tokens, word_tokens


def targeted_pages(record: InputRecord, index: list[dict], model_aliases: list[str] | None = None,
                   ignored_model_words: list[str] | None = None,
                   brand_aliases: list[str] | None = None) -> list[dict]:
    """Cheap prefilter before the strict matcher; avoids per-record site traversal."""
    make_variants = [compact_name(record.make), *(compact_name(value) for value in (brand_aliases or []))]
    variants = [record.model, *(model_aliases or [])]
    ignored_words = {normalize_name(value) for value in (ignored_model_words or [])}
    variant_tokens = [
        (number_tokens(value), [word for word in word_tokens(value) if word not in ignored_words])
        for value in variants
    ]
    result = []
    for page in index:
        haystack = compact_name(page.get("brand_guess", "") + " " + page.get("page_title", "") + " " + page.get("page_url", ""))
        if not any(make and make in haystack for make in make_variants):
            continue
        brand_words = set(word_tokens(record.make)) | set(word_tokens(page.get("brand_guess", "")))
        for alias in brand_aliases or []:
            brand_words.update(word_tokens(alias))
        page_words = [word for word in word_tokens(page.get("page_title", "")) if word not in brand_words]
        matches_variant = any(
            (not nums or all(n in haystack for n in nums))
            and (not words or all(word in page_words for word in words))
            for nums, words in variant_tokens
        )
        if not matches_variant:
            continue
        result.append(page)
    return result


def fallback_pages(record: InputRecord, index: list[dict], brand_aliases: list[str] | None = None,
                   ignored_model_words: list[str] | None = None) -> list[dict]:
    """Broader local-only discovery for AI review after strict matching failed."""
    make_variants = [compact_name(record.make), *(compact_name(value) for value in (brand_aliases or []))]
    ignored_words = {normalize_name(value) for value in (ignored_model_words or [])}
    input_words = [word for word in word_tokens(record.model) if word not in ignored_words]
    input_numbers = set(record.number_tokens)
    result = []
    for page in index:
        brand_text = page.get("brand_guess", "")
        title = page.get("page_title", "")
        haystack = compact_name(f"{brand_text} {title} {page.get('page_url', '')}")
        if not any(make and make in haystack for make in make_variants):
            continue
        title_without_year = re.sub(r"\b(?:19|20)\d{2}\b", "", title)
        page_numbers = set(number_tokens(title_without_year))
        if input_numbers and input_numbers != page_numbers:
            continue
        brand_words = set(word_tokens(record.make)) | set(word_tokens(brand_text))
        for alias in brand_aliases or []:
            brand_words.update(word_tokens(alias))
        page_words = [word for word in word_tokens(title) if word not in brand_words]
        if input_words and (not page_words or input_words[0] != page_words[0]):
            continue
        result.append(page)
    return result


def cross_source_candidate_pages(record: InputRecord, index: list[dict],
                                 brand_aliases: list[str] | None = None,
                                 ignored_model_words: list[str] | None = None,
                                 max_total: int = 12) -> list[dict]:
    """Return a source-diverse fuzzy pool for AI review.

    Unlike ``fallback_pages``, this intentionally does not require the first
    alphabetic token to match.  It is only an AI review pool, never an
    automatically trusted match, so regional aliases such as CB/CBF can still
    be considered without weakening the deterministic matcher.
    """
    make_variants = [compact_name(record.make), *(compact_name(value) for value in (brand_aliases or []))]
    ignored_words = {normalize_name(value) for value in (ignored_model_words or [])}
    input_words = [word for word in word_tokens(record.model) if word not in ignored_words]
    input_compact = compact_name(" ".join(input_words) + " " + " ".join(record.number_tokens))
    input_numbers = set(record.number_tokens)
    by_source: dict[str, list[tuple[tuple[int, int], dict]]] = defaultdict(list)

    for page in index:
        brand_text = page.get("brand_guess", "")
        title = page.get("page_title", "")
        url = page.get("page_url", "")
        haystack = compact_name(f"{brand_text} {title} {url}")
        if not any(make and make in haystack for make in make_variants):
            continue
        title_without_year = re.sub(r"\b(?:19|20)\d{2}\b", "", title)
        page_numbers = set(number_tokens(title_without_year))
        brand_words = set(word_tokens(record.make)) | set(word_tokens(brand_text))
        page_words = [word for word in word_tokens(title_without_year)
                      if word not in brand_words and word not in ignored_words]
        page_compact = compact_name(" ".join(page_words) + " " + " ".join(sorted(page_numbers)))
        similarity = round(ratio(input_compact, page_compact)) if input_compact and page_compact else 0
        numbers_equal = input_numbers == page_numbers if input_numbers else True
        numbers_overlap = bool(input_numbers & page_numbers)
        if similarity < 25 and not numbers_equal and not numbers_overlap:
            continue
        source = page.get("source_name", "unknown")
        by_source[source].append(((100 if numbers_equal else 30 if numbers_overlap else 0, similarity), page))

    for rows in by_source.values():
        rows.sort(key=lambda item: item[0], reverse=True)

    # Round-robin selection prevents one large catalog from occupying every
    # Qwen candidate slot while smaller configured sources are hidden.
    sources = sorted(
        by_source,
        key=lambda name: min((int(item[1].get("source_priority", 99)) for item in by_source[name]), default=99),
    )
    result: list[dict] = []
    position = 0
    while len(result) < max_total:
        added = False
        for source in sources:
            rows = by_source[source]
            if position < len(rows):
                result.append(rows[position][1])
                added = True
                if len(result) >= max_total:
                    break
        if not added:
            break
        position += 1
    return result
