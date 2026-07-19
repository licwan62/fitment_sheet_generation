from moto_dimension_crawler.models import InputRecord
from moto_dimension_crawler.normalizer import compact_name, normalize_name, number_tokens, word_tokens
from moto_dimension_crawler.page_discovery import cross_source_candidate_pages, fallback_pages, targeted_pages


def record(make, model):
    return InputRecord("003072", make, model, "", normalize_name(make), normalize_name(model), compact_name(model), number_tokens(model), word_tokens(model))


def test_unrelated_brand_page_is_excluded_by_primary_model_token():
    pages = [{"brand_guess":"Indian","page_title":"Chieftain Jack Daniel's L.E.","page_url":"https://example/Indian/chieftain"}]
    assert targeted_pages(record("Indian", "FTR S"), pages) == []


def test_brand_catalog_page_is_not_a_model_candidate():
    pages = [{"brand_guess":"","page_title":"Indian","page_url":"https://example/bikes/Indian.htm"}]
    assert targeted_pages(record("Indian", "FTR S"), pages) == []


def test_generated_alias_participates_in_candidate_prefilter():
    pages = [{"page_title": "Honda VFR 800 F 2018", "page_url": "https://example.invalid/vfr800f", "brand_guess": "Honda"}]
    assert targeted_pages(record("Honda", "VFR 800 Interceptor"), pages, ["VFR 800 F"]) == pages


def test_word_specific_prefilter_excludes_other_same_prefix_models():
    pages = [
        {"page_title": "BMW C Evolution", "page_url": "https://example.invalid/c-evolution", "brand_guess": "BMW"},
        {"page_title": "BMW C 650 Sport", "page_url": "https://example.invalid/c650-sport", "brand_guess": "BMW"},
        {"page_title": "BMW C 400 GT", "page_url": "https://example.invalid/c400-gt", "brand_guess": "BMW"},
    ]
    assert targeted_pages(record("BMW", "C evolution"), pages) == pages[:1]


def test_ignored_market_word_does_not_block_prefilter():
    pages = [{"page_title": "BMW F 900 GS Adventure 2024", "page_url": "https://example.invalid/f900gs", "brand_guess": "BMW"}]
    assert targeted_pages(record("BMW", "F900GS Adventure Equipada"), pages, ignored_model_words=["equipada"]) == pages


def test_generated_brand_alias_participates_in_brand_prefilter():
    pages = [{"page_title": "BMW C Evolution", "page_url": "https://example.invalid/c-evolution", "brand_guess": "BMW"}]
    assert targeted_pages(record("BMW Motorrad", "C Evolution"), pages, brand_aliases=["BMW"]) == pages


def test_fallback_discovery_finds_base_model_behind_unknown_suffix():
    pages = [
        {"page_title": "BMW F 900XR 2020", "page_url": "https://example.invalid/f900xr", "brand_guess": "BMW"},
        {"page_title": "BMW F 850GS 2020", "page_url": "https://example.invalid/f850gs", "brand_guess": "BMW"},
    ]
    assert fallback_pages(record("BMW", "F900XR LWR"), pages) == pages[:1]


def test_cross_source_pool_keeps_nearby_models_from_each_catalog():
    pages = [
        {"page_title": "Honda CBF 190TR", "page_url": "https://one/cbf190tr", "brand_guess": "Honda", "source_name": "one", "source_priority": 1},
        {"page_title": "Honda CB 190X", "page_url": "https://two/cb190x", "brand_guess": "Honda", "source_name": "two", "source_priority": 2},
        {"page_title": "Honda CBR 1000RR", "page_url": "https://one/cbr1000rr", "brand_guess": "Honda", "source_name": "one", "source_priority": 1},
    ]
    found = cross_source_candidate_pages(record("Honda", "CB190R"), pages, max_total=2)
    assert [page["source_name"] for page in found] == ["one", "two"]
    assert {page["page_title"] for page in found} == {"Honda CBF 190TR", "Honda CB 190X"}
