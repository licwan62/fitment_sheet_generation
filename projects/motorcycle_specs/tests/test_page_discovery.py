from moto_dimension_crawler.models import InputRecord
from moto_dimension_crawler.normalizer import compact_name, normalize_name, number_tokens, word_tokens
from moto_dimension_crawler.page_discovery import targeted_pages


def record(make, model):
    return InputRecord("003072", make, model, "", normalize_name(make), normalize_name(model), compact_name(model), number_tokens(model), word_tokens(model))


def test_unrelated_brand_page_is_excluded_by_primary_model_token():
    pages = [{"brand_guess":"Indian","page_title":"Chieftain Jack Daniel's L.E.","page_url":"https://example/Indian/chieftain"}]
    assert targeted_pages(record("Indian", "FTR S"), pages) == []


def test_brand_catalog_page_is_not_a_model_candidate():
    pages = [{"brand_guess":"","page_title":"Indian","page_url":"https://example/bikes/Indian.htm"}]
    assert targeted_pages(record("Indian", "FTR S"), pages) == []
