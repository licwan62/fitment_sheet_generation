import json

import httpx

from moto_dimension_crawler.models import InputRecord
from moto_dimension_crawler.normalizer import compact_name, normalize_name, number_tokens, word_tokens
from moto_dimension_crawler.qwen_aliases import QwenAliasGenerator


def record(make: str, model: str) -> InputRecord:
    return InputRecord("000001", make, model, "", normalize_name(make), normalize_name(model), compact_name(model), number_tokens(model), word_tokens(model))


def test_qwen_aliases_are_validated_and_cached(tmp_path, monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        content = json.dumps({
            "decision": "MATCH",
            "selected_candidate": "F 900 GS Adventure",
            "canonical_model_alias": "F900GS ADV",
            "configuration_tokens": ["Adventure"],
            "brand_aliases": ["Bayerische Motoren Werke", "BMW Motorrad"],
            "model_aliases": ["F900 GS Adventure", "F 850 GS", "BMW Motorrad F 900 GS Adventure", "F900GS ADV"],
        })
        return httpx.Response(200, json={"choices": [{"message": {"content": content}}]})

    generator = QwenAliasGenerator(
        {"enabled": True, "model": "qwen-flash", "max_aliases": 10},
        tmp_path,
        transport=httpx.MockTransport(handler),
    )
    item = record("BMW Motorrad", "F 900 GS Adventure")
    first = generator.generate(item, ["F 900 GS Adventure"])
    second = generator.generate(item, ["F 900 GS Adventure"])
    assert first.brand_aliases == ["Bayerische Motoren Werke"]
    assert first.model_aliases == ["F900GS ADV"]
    assert first.status == "SUCCESS"
    assert second.status == "CACHED_SUCCESS"
    assert second.brand_aliases == first.brand_aliases
    assert second.model_aliases == first.model_aliases
    assert first.selected_candidate == "F 900 GS Adventure"
    assert len(calls) == 1
    generator.close()


def test_disabled_qwen_does_not_require_key(tmp_path, monkeypatch):
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    generator = QwenAliasGenerator({"enabled": False}, tmp_path)
    generated = generator.generate(record("BMW", "C 400 GT"))
    assert generated.brand_aliases == []
    assert generated.model_aliases == []
    generator.close()


def test_qwen_timeout_is_cached_temporarily(tmp_path, monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        raise httpx.ReadTimeout("slow", request=request)

    generator = QwenAliasGenerator(
        {"enabled": True, "failure_cache_seconds": 3600}, tmp_path,
        transport=httpx.MockTransport(handler),
    )
    item = record("BMW", "F900XR LWR")
    assert generator.generate(item, ["F 900XR"]).status == "TIMEOUT"
    assert generator.generate(item, ["F 900XR"]).status == "CACHED_TIMEOUT"
    assert len(calls) == 1
    generator.close()


def test_qwen_authentication_failure_is_not_cached(tmp_path, monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "bad-key")
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(401, request=request)

    generator = QwenAliasGenerator(
        {"enabled": True, "failure_cache_seconds": 3600}, tmp_path,
        transport=httpx.MockTransport(handler),
    )
    item = record("Honda", "CR125M")
    for _ in range(2):
        try:
            generator.generate(item, ["CR 125"])
        except RuntimeError as exc:
            assert "HTTP 401" in str(exc)
        else:
            raise AssertionError("authentication failure should stop the run")
    assert len(calls) == 2
    assert not list((tmp_path / "qwen_model_aliases").glob("*.json"))
    generator.close()


def test_selected_candidate_becomes_safe_model_alias(tmp_path, monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")

    def handler(request: httpx.Request) -> httpx.Response:
        content = json.dumps({
            "decision": "MATCH", "selected_candidate": "F 900XR 2020",
            "canonical_model_alias": "", "configuration_tokens": ["LWR"],
            "brand_aliases": [], "model_aliases": [],
        })
        return httpx.Response(200, json={"choices": [{"message": {"content": content}}]})

    generator = QwenAliasGenerator(
        {"enabled": True}, tmp_path, transport=httpx.MockTransport(handler),
    )
    generated = generator.generate(record("BMW", "F900XR LWR"), ["F 900XR 2020"])
    assert generated.decision == "MATCH"
    assert generated.model_aliases == ["F 900XR"]
    assert generated.configuration_tokens == ["LWR"]
    generator.close()


def test_market_alias_decision_is_preserved_and_can_supply_catalog_name(tmp_path, monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")

    def handler(request: httpx.Request) -> httpx.Response:
        request_json = json.loads(request.content)
        assert "regional/market names" in request_json["messages"][0]["content"]
        content = json.dumps({
            "decision": "MATCH", "selected_candidate": "F 650 Funduro",
            "confidence": "MEDIUM", "match_basis": "MARKET_ALIAS",
            "explanation": "The input appears to use an alternate market description.",
            "canonical_model_alias": "F 650 Funduro", "configuration_tokens": [],
            "brand_aliases": [], "model_aliases": [],
        })
        return httpx.Response(200, json={"choices": [{"message": {"content": content}}]})

    generator = QwenAliasGenerator(
        {"enabled": True}, tmp_path, transport=httpx.MockTransport(handler),
    )
    generated = generator.generate(record("BMW", "F650 Enduro"), ["F 650 Funduro"])
    assert generated.decision == "MATCH"
    assert generated.selected_candidate == "F 650 Funduro"
    assert generated.model_aliases == ["F 650 Funduro"]
    assert generated.confidence == "MEDIUM"
    assert generated.match_basis == "MARKET_ALIAS"
    generator.close()


def test_qwen_dimension_inference_is_bounded_marked_and_cached(tmp_path, monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        content = json.dumps({
            "decision": "INFER", "confidence": "HIGH",
            "length_mm": 2029, "width_mm": 739, "height_mm": 1041,
            "wheelbase_mm": 1356, "seat_height_mm": 771,
            "ground_clearance_mm": 138, "explanation": "Representative model dimensions.",
        })
        return httpx.Response(200, json={"choices": [{"message": {"content": content}}]})

    generator = QwenAliasGenerator(
        {"enabled": True, "infer_dimensions_when_missing": True}, tmp_path,
        transport=httpx.MockTransport(handler),
    )
    item = record("Honda", "CB190R")
    first = generator.infer_dimensions(item, {"length_min_mm": 900, "length_max_mm": 3500})
    second = generator.infer_dimensions(item, {"length_min_mm": 900, "length_max_mm": 3500})
    assert first.decision == "INFER"
    assert first.values["length_mm"] == 2029
    assert first.confidence == "LOW"
    assert second.status == "CACHED_SUCCESS"
    assert len(calls) == 1
    generator.close()
