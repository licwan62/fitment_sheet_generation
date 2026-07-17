from __future__ import annotations
import re

from rapidfuzz.fuzz import ratio

from .models import Candidate, InputRecord
from .normalizer import compact_name, normalize_name, number_tokens, word_tokens


VERSION_WORDS = {"gt", "x", "r", "rr", "s", "sport", "sports", "adventure", "touring", "rally", "abs", "concept"}


def score_candidate(record: InputRecord, title: str, url: str, cfg: dict, brand_aliases: dict | None = None, model_aliases: dict | None = None, source_make: str = "") -> Candidate:
    brand_aliases = brand_aliases or {}
    model_aliases = model_aliases or {}
    title_norm = normalize_name(title)
    title_without_year = re.sub(r"\b(?:19|20)\d{2}\b", "", title)
    title_compact = compact_name(title_without_year)
    brand_haystack_norm = normalize_name(f"{source_make} {title} {url}")
    brand_haystack_compact = compact_name(f"{source_make} {title} {url}")
    make_variants = {record.make_normalized, *(normalize_name(v) for v in brand_aliases.get(record.make_normalized, []))}
    brand_ok = any(v and (v in brand_haystack_norm or compact_name(v) in brand_haystack_compact) for v in make_variants)
    ignored_words = {normalize_name(word) for word in cfg.get("matching", {}).get("ignored_model_words", [])}
    # Remove market/configuration suffixes without changing the original
    # alpha/numeric token order (for example F 900 GS must stay F 900 GS).
    record_core_tokens = [token for token in record.model_normalized.split() if token not in ignored_words]
    record_core_normalized = " ".join(record_core_tokens)
    record_core_words = word_tokens(record_core_normalized)
    model_compact = compact_name(record_core_normalized)
    candidate_model_compact = title_compact
    for brand_text in (source_make, record.make, *brand_aliases.get(record.make_normalized, [])):
        brand_compact = compact_name(brand_text)
        if brand_compact and candidate_model_compact.startswith(brand_compact):
            candidate_model_compact = candidate_model_compact[len(brand_compact):]
            break
    alias_values = []
    for key, values in model_aliases.items():
        make_key, _, model_key = key.partition("|")
        if normalize_name(make_key) == record.make_normalized and compact_name(model_key) == model_compact:
            alias_values.extend(values)
    model_variants = {model_compact, *(compact_name(v) for v in alias_values)}
    model_exact = any(v and v == candidate_model_compact for v in model_variants)
    input_nums = set(record.number_tokens)
    candidate_nums = {n for n in number_tokens(title) if not (len(n) == 4 and 1900 <= int(float(n)) <= 2099)}
    number_ok = input_nums == candidate_nums if input_nums else True
    input_words = set(record_core_words)
    make_words = set(word_tokens(record.make)) | set(word_tokens(source_make))
    candidate_word_list = [word for word in word_tokens(title) if word not in make_words]
    candidate_words = set(candidate_word_list)
    primary_alpha_ok = not record_core_words or bool(candidate_word_list and record_core_words[0] == candidate_word_list[0])
    alpha_tokens_ok = record_core_words == candidate_word_list
    version_input = input_words & VERSION_WORDS
    version_candidate = candidate_words & VERSION_WORDS
    version_ok = version_input == version_candidate
    keyword_ratio = ratio(" ".join(record_core_words), " ".join(sorted(candidate_words))) / 100
    similarity = round(ratio(model_compact, candidate_model_compact))
    score = (30 if brand_ok else 0) + (35 if model_exact else int(35 * similarity / 100))
    score += 10 if number_ok else 0
    score += 15 if model_exact else int(15 * keyword_ratio)
    score += 5 if version_ok else 0
    if not brand_ok:
        score = min(score, 40)
    if input_nums and not number_ok:
        score = min(score, 65)
    if not primary_alpha_ok:
        score = min(score, 84)
    exact = brand_ok and model_exact and number_ok and version_ok
    thresholds = cfg["matching"]
    if not brand_ok:
        status = "BRAND_MISMATCH"
    elif input_nums and not number_ok:
        status = "NUMBER_MISMATCH"
    elif not primary_alpha_ok:
        status = "MODEL_MISMATCH"
    elif exact and score >= thresholds["exact_threshold"]:
        status = "EXACT"
    elif (score > thresholds.get("trusted_score_threshold", thresholds.get("likely_threshold", 85))
          and version_ok and primary_alpha_ok and alpha_tokens_ok and number_ok):
        status = "LIKELY"
    elif score >= thresholds["review_threshold"]:
        status = "REVIEW"
    else:
        status = "MODEL_MISMATCH"
    confidence = "HIGH" if status == "EXACT" else "MEDIUM" if status == "LIKELY" else "LOW"
    reason = f"brand={'yes' if brand_ok else 'no'}; model_exact={'yes' if model_exact else 'no'}; model_similarity={similarity}; primary_alpha={'yes' if primary_alpha_ok else 'no'}; alpha_tokens={'yes' if alpha_tokens_ok else 'no'}; numbers={'yes' if number_ok else 'no'}; version={'yes' if version_ok else 'no'}; match_confidence={confidence}"
    return Candidate(record.input_id, title, url, source_make if brand_ok else "", title, score=score, status=status, reason=reason)


def rank_candidates(record: InputRecord, pages: list[dict], cfg: dict, brand_aliases: dict | None = None, model_aliases: dict | None = None) -> list[Candidate]:
    ranked = [score_candidate(record, p["page_title"], p["page_url"], cfg, brand_aliases, model_aliases, p.get("brand_guess", "")) for p in pages]
    ranked.sort(key=lambda x: (-x.score, x.url))
    credible = [x for x in ranked if x.status in {"EXACT", "LIKELY"}]
    if len(credible) > 1:
        close = [item for item in credible
                 if credible[0].score - item.score < cfg["matching"]["multiple_score_gap"]]
        identities = {
            compact_name(re.sub(r"\b(?:19|20)\d{2}\b", "", item.title))
            for item in close
        }
        # Several year pages for one model are valid sources, not an ambiguous match.
        if len(identities) > 1:
            for item in close:
                item.status = "MULTIPLE"
    return ranked
