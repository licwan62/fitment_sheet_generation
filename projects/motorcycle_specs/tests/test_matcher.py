import pytest

from moto_dimension_crawler.matcher import score_candidate
from moto_dimension_crawler.models import InputRecord
from moto_dimension_crawler.normalizer import compact_name, normalize_name, number_tokens, word_tokens


CFG = {"matching":{"exact_threshold":95,"likely_threshold":85,"review_threshold":70,"multiple_score_gap":5}}


def record(make, model):
    return InputRecord("000001", make, model, "", normalize_name(make), normalize_name(model), compact_name(model), number_tokens(model), word_tokens(model))


@pytest.mark.parametrize("model,title", [
    ("C 400 GT", "BMW C 400 X 2021"), ("C 400 GT", "BMW C 650 GT 2021"),
    ("R 1200 GS", "BMW R 1250 GS 2020"), ("MT-07", "Yamaha MT-09 2020"),
    ("Africa Twin", "Honda Africa Twin Adventure Sports 2022"),
])
def test_different_models_are_not_exact(model, title):
    make = "Yamaha" if model.startswith("MT") else "Honda" if model.startswith("Africa") else "BMW"
    assert score_candidate(record(make, model), title, "https://example.invalid", CFG).status != "EXACT"


def test_compact_model_is_exact():
    result = score_candidate(record("BMW", "C400GT"), "BMW C 400 GT 2019", "https://example.invalid", CFG)
    assert result.status == "EXACT"
    assert result.score >= 95
    assert "model_similarity=" in result.reason
    assert "match_confidence=HIGH" in result.reason


def test_same_number_different_model_prefix_is_not_automatic():
    result = score_candidate(record("Honda", "CBR125R"), "Honda CB 125R 2024", "https://example.invalid", CFG)
    assert result.status not in {"EXACT", "LIKELY", "MULTIPLE"}


def test_review_candidates_are_not_promoted_to_multiple():
    from moto_dimension_crawler.matcher import rank_candidates
    pages = [
        {"page_title":"BMW C 650 GT 2018", "page_url":"https://example.invalid/bmw-c650gt-18", "brand_guess":"BMW"},
        {"page_title":"BMW C 650 Sport 2018", "page_url":"https://example.invalid/bmw-c650sport-18", "brand_guess":"BMW"},
    ]
    assert all(x.status != "MULTIPLE" for x in rank_candidates(record("BMW", "F650"), pages, CFG))


def test_same_model_year_pages_are_not_marked_multiple():
    from moto_dimension_crawler.matcher import rank_candidates
    pages = [
        {"page_title": "BMW F 750 GS 2021", "page_url": "https://example.invalid/f750gs-21", "brand_guess": "BMW"},
        {"page_title": "BMW F 750 GS 2022", "page_url": "https://example.invalid/f750gs-22", "brand_guess": "BMW"},
    ]
    results = rank_candidates(record("BMW", "F750GS"), pages, CFG)
    assert [item.status for item in results] == ["EXACT", "EXACT"]


def test_base_model_is_not_automatic_match_for_suffixed_model():
    result = score_candidate(record("BMW", "R100"), "BMW R100GS", "https://example.invalid", CFG)
    assert result.status not in {"EXACT", "LIKELY", "MULTIPLE"}


def test_short_model_does_not_match_unrelated_title_containing_s():
    result = score_candidate(record("Indian", "FTR S"), "Chieftain Jack Daniel's L.E.", "https://example.invalid", CFG, source_make="Indian")
    assert result.status == "MODEL_MISMATCH"
    assert "primary_alpha=no" in result.reason
    assert result.score < 70


def test_ignored_market_suffix_matches_core_model():
    cfg = {"matching":{**CFG["matching"], "ignored_model_words":["equipada"]}}
    result = score_candidate(record("BMW", "F900GS Adventure Equipada"), "BMW F 900 GS Adventure 2024", "https://example.invalid", cfg, source_make="BMW")
    assert result.status == "EXACT"
    assert result.score == 95


def test_trusted_score_threshold_promotes_safe_candidate():
    high_threshold = {"matching": {**CFG["matching"], "trusted_score_threshold": 95}}
    usable_threshold = {"matching": {**CFG["matching"], "trusted_score_threshold": 80}}
    equal_threshold = {"matching": {**CFG["matching"], "trusted_score_threshold": 84}}
    item = record("BMW", "F 900 GS Adventure")
    title = "BMW F GS 900 Adventure"
    assert score_candidate(item, title, "https://example.invalid", high_threshold).status == "REVIEW"
    assert score_candidate(item, title, "https://example.invalid", equal_threshold).status == "REVIEW"
    assert score_candidate(item, title, "https://example.invalid", usable_threshold).status == "LIKELY"


def test_trusted_threshold_does_not_bypass_primary_model_constraint():
    cfg = {"matching": {**CFG["matching"], "trusted_score_threshold": 0}}
    result = score_candidate(record("Indian", "FTR S"), "Chieftain Jack Daniel's L.E.",
                             "https://example.invalid", cfg, source_make="Indian")
    assert result.status == "MODEL_MISMATCH"
