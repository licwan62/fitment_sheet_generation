from __future__ import annotations

import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx

from .models import InputRecord
from .normalizer import compact_name, normalize_name, number_tokens
from .utils import stable_hash


PROMPT_VERSION = "motorcycle-candidate-resolution-v4"
DIMENSION_PROMPT_VERSION = "motorcycle-dimension-inference-v1"


@dataclass(slots=True)
class GeneratedAliases:
    brand_aliases: list[str]
    model_aliases: list[str]
    status: str = "DISABLED"
    decision: str = "AMBIGUOUS"
    selected_candidate: str = ""
    configuration_tokens: list[str] = field(default_factory=list)
    confidence: str = "UNKNOWN"
    match_basis: str = ""
    explanation: str = ""


@dataclass(slots=True)
class GeneratedDimensions:
    values: dict[str, float | None] = field(default_factory=dict)
    status: str = "DISABLED"
    decision: str = "UNKNOWN"
    confidence: str = "LOW"
    explanation: str = ""


class QwenAliasGenerator:
    def __init__(self, config: dict, cache_root: Path, transport: httpx.BaseTransport | None = None):
        self.config = config
        self.enabled = bool(config.get("enabled", False))
        self.model = str(config.get("model", "qwen-flash"))
        self.base_url = str(config.get("base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1")).rstrip("/")
        self.max_aliases = max(1, min(int(config.get("max_aliases", 12)), 30))
        self.max_candidates = max(1, min(int(config.get("max_candidates", 8)), 20))
        self.failure_cache_seconds = max(0, int(config.get("failure_cache_seconds", 3600)))
        self.cache_enabled = bool(config.get("cache_enabled", True))
        self.cache_dir = cache_root / "qwen_model_aliases"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.dimension_cache_dir = cache_root / "qwen_dimension_inference"
        self.dimension_cache_dir.mkdir(parents=True, exist_ok=True)
        key_env = str(config.get("api_key_env", "DASHSCOPE_API_KEY"))
        self.api_key = os.environ.get(key_env, "")
        if self.enabled and not self.api_key:
            raise ValueError(f"Qwen alias generation is enabled but environment variable {key_env} is not set")
        self.client = httpx.Client(
            timeout=float(config.get("timeout_seconds", 30)),
            transport=transport,
        )

    def close(self) -> None:
        self.client.close()

    def _cache_path(self, record: InputRecord, candidate_titles: list[str]) -> Path:
        identity = json.dumps({
            "prompt_version": PROMPT_VERSION,
            "model": self.model,
            "make": record.make,
            "model_name": record.model,
            "max_aliases": self.max_aliases,
            "candidate_titles": candidate_titles[:self.max_candidates],
        }, ensure_ascii=False, sort_keys=True)
        return self.cache_dir / f"{stable_hash(identity)}.json"

    def _messages(self, record: InputRecord, candidate_titles: list[str]) -> list[dict]:
        return [
            {
                "role": "system",
                "content": (
                    "You resolve a noisy motorcycle input name against a closed list of real catalog candidate titles, "
                    "including vintage and discontinued motorcycles. Use your motorcycle knowledge, not only string "
                    "similarity. Recognize regional/market names, historical marketing names, abbreviations, "
                    "transliterations, and plausible input typos. A title may MATCH even when alphabetic words differ "
                    "if both names identify the same underlying motorcycle model. Return JSON only. "
                    "Never match a merely related model, successor, predecessor, or different displacement. "
                    "A parent company, acquired marque, sibling marque, distributor, and engine maker are not brand aliases. "
                    "Preserve displacement and other identity-bearing numeric model tokens exactly, except a four-digit "
                    "catalog year. Treat letter suffixes as identity-bearing by default, but allow a difference when you "
                    "know it is a market label, configuration label, abbreviation, or clear typo for the same model. "
                    "Treat equipment, market, ride-height, anniversary, and homologation suffixes as configuration tokens "
                    "only when the base motorcycle identity is unchanged. Do not reject a candidate solely because the "
                    "catalog title is not a literal spelling match. Do not reveal chain-of-thought; give one short factual explanation."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Manufacturer: {record.make}\nModel: {record.model}\n"
                    f"Catalog candidates: {json.dumps(candidate_titles[:self.max_candidates], ensure_ascii=False)}\n"
                    f"Generate at most {self.max_aliases} aliases per field. Select only a title from Catalog candidates. "
                    "If one candidate is the same underlying motorcycle, including a known market name or plausible typo, "
                    "return MATCH and provide its catalog expression as canonical_model_alias, excluding manufacturer and year. "
                    "Use NO_MATCH only when the candidates are genuinely different models; use AMBIGUOUS when evidence is insufficient. "
                    'Output: {"decision":"MATCH|NO_MATCH|AMBIGUOUS","selected_candidate":"",'
                    '"confidence":"HIGH|MEDIUM|LOW","match_basis":"SAME_NAME|MARKET_ALIAS|HISTORICAL_ALIAS|'
                    'ABBREVIATION|TYPO|CONFIGURATION|NONE","explanation":"",'
                    '"canonical_model_alias":"","configuration_tokens":[],"brand_aliases":[],"model_aliases":[]}'
                ),
            },
        ]

    def _validated_brand_aliases(self, record: InputRecord, values: object) -> list[str]:
        if not isinstance(values, list):
            return []
        seen = {compact_name(record.make)}
        aliases = []
        for value in values:
            if not isinstance(value, str):
                continue
            alias = " ".join(value.strip().split())
            alias_compact = compact_name(alias)
            if not alias or len(alias) > 80 or alias_compact in seen:
                continue
            seen.add(alias_compact)
            aliases.append(alias)
            if len(aliases) >= self.max_aliases:
                break
        return aliases

    def _validated_model_aliases(self, record: InputRecord, values: object) -> list[str]:
        if not isinstance(values, list):
            return []
        expected_numbers = set(record.number_tokens)
        make_norm = normalize_name(record.make)
        seen = {compact_name(record.model)}
        aliases = []
        for value in values:
            if not isinstance(value, str):
                continue
            alias = " ".join(value.strip().split())
            alias_norm = normalize_name(alias)
            if make_norm and alias_norm.startswith(make_norm + " "):
                alias = " ".join(alias.split()[len(make_norm.split()):])
                alias_norm = normalize_name(alias)
            alias_numbers = set(number_tokens(alias))
            alias_compact = compact_name(alias)
            if (not alias or len(alias) > 80 or alias_compact in seen
                    or alias_numbers != expected_numbers):
                continue
            seen.add(alias_compact)
            aliases.append(alias)
            if len(aliases) >= self.max_aliases:
                break
        return aliases

    def _from_payload(self, record: InputRecord, payload: dict, candidate_titles: list[str], status: str) -> GeneratedAliases:
        decision = str(payload.get("decision", "AMBIGUOUS")).upper()
        if decision not in {"MATCH", "NO_MATCH", "AMBIGUOUS"}:
            decision = "AMBIGUOUS"
        selected_text = " ".join(str(payload.get("selected_candidate", "")).split())
        candidate_lookup = {" ".join(title.split()): title for title in candidate_titles}
        selected = candidate_lookup.get(selected_text, "")
        if not selected:
            selected = ""
            if decision == "MATCH":
                decision = "AMBIGUOUS"
        model_values = payload.get("model_aliases") if isinstance(payload.get("model_aliases"), list) else []
        canonical = payload.get("canonical_model_alias")
        if isinstance(canonical, str) and canonical.strip():
            model_values = [canonical, *model_values]
        if decision == "MATCH" and selected:
            selected_without_year = re.sub(r"\b(?:19|20)\d{2}\b", "", selected)
            model_values = [selected_without_year, *model_values]
        configuration_tokens = [
            str(value).strip() for value in payload.get("configuration_tokens", [])
            if isinstance(value, str) and value.strip()
        ] if isinstance(payload.get("configuration_tokens"), list) else []
        confidence = str(payload.get("confidence", "UNKNOWN")).upper()
        if confidence not in {"HIGH", "MEDIUM", "LOW"}:
            confidence = "UNKNOWN"
        match_basis = str(payload.get("match_basis", "")).upper()
        allowed_bases = {
            "SAME_NAME", "MARKET_ALIAS", "HISTORICAL_ALIAS", "ABBREVIATION",
            "TYPO", "CONFIGURATION", "NONE",
        }
        if match_basis not in allowed_bases:
            match_basis = ""
        explanation = " ".join(str(payload.get("explanation", "")).split())[:300]
        return GeneratedAliases(
            self._validated_brand_aliases(record, payload.get("brand_aliases")),
            self._validated_model_aliases(record, model_values),
            status, decision, selected, configuration_tokens,
            confidence, match_basis, explanation,
        )

    def generate(self, record: InputRecord, candidate_titles: list[str] | None = None) -> GeneratedAliases:
        candidate_titles = list(dict.fromkeys(candidate_titles or []))[:self.max_candidates]
        if not self.enabled:
            return GeneratedAliases([], [], "DISABLED")
        cache_path = self._cache_path(record, candidate_titles)
        if self.cache_enabled and cache_path.exists():
            try:
                cached = json.loads(cache_path.read_text(encoding="utf-8"))
                if cached.get("status") == "SUCCESS":
                    return self._from_payload(record, cached, candidate_titles, "CACHED_SUCCESS")
                age = time.time() - cache_path.stat().st_mtime
                if (cached.get("status") in {"TIMEOUT", "API_ERROR"}
                        and cached.get("retryable") is True
                        and age < self.failure_cache_seconds):
                    return GeneratedAliases([], [], f"CACHED_{cached['status']}")
            except (OSError, json.JSONDecodeError):
                logging.getLogger(__name__).warning("Ignoring invalid Qwen alias cache %s", cache_path)
        try:
            response = self.client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": self._messages(record, candidate_titles),
                    "response_format": {"type": "json_object"},
                    "temperature": 0,
                },
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            payload = json.loads(content)
            aliases = self._from_payload(record, payload, candidate_titles, "SUCCESS")
            if self.cache_enabled:
                cache_path.write_text(json.dumps({
                    **payload, "status": "SUCCESS", "prompt_version": PROMPT_VERSION, "model": self.model,
                    "make": record.make, "model_name": record.model,
                    "brand_aliases": aliases.brand_aliases, "model_aliases": aliases.model_aliases,
                }, ensure_ascii=False, indent=2), encoding="utf-8")
            return aliases
        except (httpx.HTTPError, KeyError, TypeError, json.JSONDecodeError) as exc:
            status_code = exc.response.status_code if isinstance(exc, httpx.HTTPStatusError) else None
            if status_code in {401, 403}:
                raise RuntimeError(
                    f"Qwen API 鉴权失败（HTTP {status_code}）。请检查 QWEN_API_KEY、Key 所属地域和 base_url。"
                ) from exc
            failure_status = "TIMEOUT" if isinstance(exc, httpx.TimeoutException) else "API_ERROR"
            retryable = (
                isinstance(exc, (httpx.TimeoutException, httpx.NetworkError))
                or status_code == 429
                or (status_code is not None and status_code >= 500)
            )
            if self.cache_enabled and retryable:
                cache_path.write_text(json.dumps({
                    "status": failure_status, "prompt_version": PROMPT_VERSION, "model": self.model,
                    "make": record.make, "model_name": record.model,
                    "candidate_titles": candidate_titles, "error_type": type(exc).__name__,
                    "status_code": status_code, "retryable": True,
                }, ensure_ascii=False, indent=2), encoding="utf-8")
            logging.getLogger(__name__).warning(
                "Qwen alias generation failed for %s %s: %s; using deterministic matching",
                record.make, record.model, exc,
            )
            return GeneratedAliases([], [], failure_status)

    def _dimension_cache_path(self, record: InputRecord) -> Path:
        identity = json.dumps({
            "prompt_version": DIMENSION_PROMPT_VERSION,
            "model": self.model,
            "make": record.make,
            "model_name": record.model,
        }, ensure_ascii=False, sort_keys=True)
        return self.dimension_cache_dir / f"{stable_hash(identity)}.json"

    @staticmethod
    def _dimension_values(payload: dict, validation: dict) -> dict[str, float | None]:
        bounds = {
            "length_mm": (validation.get("length_min_mm", 900), validation.get("length_max_mm", 3500)),
            "width_mm": (validation.get("width_min_mm", 300), validation.get("width_max_mm", 2000)),
            "height_mm": (validation.get("height_min_mm", 400), validation.get("height_max_mm", 2500)),
            "wheelbase_mm": (700, 2500),
            "seat_height_mm": (300, 1500),
            "ground_clearance_mm": (30, 600),
        }
        values: dict[str, float | None] = {}
        for key, (minimum, maximum) in bounds.items():
            raw = payload.get(key)
            try:
                value = float(raw) if raw is not None and raw != "" else None
            except (TypeError, ValueError):
                value = None
            values[key] = value if value is not None and minimum <= value <= maximum else None
        return values

    def _dimensions_from_payload(self, payload: dict, validation: dict, status: str) -> GeneratedDimensions:
        decision = str(payload.get("decision", "UNKNOWN")).upper()
        if decision not in {"INFER", "UNKNOWN"}:
            decision = "UNKNOWN"
        values = self._dimension_values(payload, validation)
        if decision != "INFER" or not any(value is not None for value in values.values()):
            decision = "UNKNOWN"
            values = {key: None for key in values}
        confidence = str(payload.get("confidence", "LOW")).upper()
        # An answer without a verifiable page can never be exported as HIGH.
        if confidence not in {"LOW", "MEDIUM"}:
            confidence = "LOW"
        explanation = " ".join(str(payload.get("explanation", "")).split())[:500]
        return GeneratedDimensions(values, status, decision, confidence, explanation)

    def infer_dimensions(self, record: InputRecord, validation: dict | None = None) -> GeneratedDimensions:
        """Infer dimensions only after every configured catalog has no credible candidate."""
        if not self.enabled or not self.config.get("infer_dimensions_when_missing", False):
            return GeneratedDimensions(status="DISABLED")
        validation = validation or {}
        cache_path = self._dimension_cache_path(record)
        if self.cache_enabled and cache_path.exists():
            try:
                cached = json.loads(cache_path.read_text(encoding="utf-8"))
                if cached.get("status") == "SUCCESS":
                    return self._dimensions_from_payload(cached, validation, "CACHED_SUCCESS")
                age = time.time() - cache_path.stat().st_mtime
                if (cached.get("status") in {"TIMEOUT", "API_ERROR"}
                        and cached.get("retryable") is True and age < self.failure_cache_seconds):
                    return GeneratedDimensions(status=f"CACHED_{cached['status']}")
            except (OSError, json.JSONDecodeError):
                logging.getLogger(__name__).warning("Ignoring invalid Qwen dimension cache %s", cache_path)

        messages = [
            {
                "role": "system",
                "content": (
                    "You estimate factory motorcycle overall dimensions from model knowledge only when no catalog page was found. "
                    "Return UNKNOWN when the model identity is uncertain or dimensions vary materially by year/market. "
                    "Do not copy dimensions from a related model. Use millimetres, null for unknown fields, and avoid false precision. "
                    "This is explicitly unverified inference, not sourced evidence. Return JSON only."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Manufacturer: {record.make}\nModel: {record.model}\n"
                    'Output: {"decision":"INFER|UNKNOWN","confidence":"MEDIUM|LOW",'
                    '"length_mm":null,"width_mm":null,"height_mm":null,"wheelbase_mm":null,'
                    '"seat_height_mm":null,"ground_clearance_mm":null,"explanation":""}'
                ),
            },
        ]
        try:
            response = self.client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": self.model, "messages": messages,
                      "response_format": {"type": "json_object"}, "temperature": 0},
            )
            response.raise_for_status()
            payload = json.loads(response.json()["choices"][0]["message"]["content"])
            result = self._dimensions_from_payload(payload, validation, "SUCCESS")
            if self.cache_enabled:
                cache_path.write_text(json.dumps({
                    **payload, "status": "SUCCESS", "prompt_version": DIMENSION_PROMPT_VERSION,
                    "model": self.model, "make": record.make, "model_name": record.model,
                }, ensure_ascii=False, indent=2), encoding="utf-8")
            return result
        except (httpx.HTTPError, KeyError, TypeError, json.JSONDecodeError) as exc:
            status_code = exc.response.status_code if isinstance(exc, httpx.HTTPStatusError) else None
            if status_code in {401, 403}:
                raise RuntimeError(
                    f"Qwen API 鉴权失败（HTTP {status_code}）。请检查 QWEN_API_KEY、Key 所属地域和 base_url。"
                ) from exc
            failure_status = "TIMEOUT" if isinstance(exc, httpx.TimeoutException) else "API_ERROR"
            retryable = (isinstance(exc, (httpx.TimeoutException, httpx.NetworkError))
                         or status_code == 429 or (status_code is not None and status_code >= 500))
            if self.cache_enabled and retryable:
                cache_path.write_text(json.dumps({
                    "status": failure_status, "prompt_version": DIMENSION_PROMPT_VERSION,
                    "model": self.model, "make": record.make, "model_name": record.model,
                    "retryable": True, "error_type": type(exc).__name__, "status_code": status_code,
                }, ensure_ascii=False, indent=2), encoding="utf-8")
            logging.getLogger(__name__).warning(
                "Qwen dimension inference failed for %s %s: %s", record.make, record.model, exc,
            )
            return GeneratedDimensions(status=failure_status)
