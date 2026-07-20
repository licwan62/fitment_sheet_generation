from __future__ import annotations

import gc
import logging
import json
import re
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

from .cache import PageCache
from .config import load_aliases, load_config, load_manual_pages
from .crawler import Crawler
from .database import StateDB, clear_checkpoint
from .exporter import export_all
from .grouper import group_dimensions
from .index_builder import build_1000ps_index, build_bikedekho_index, build_bikez_index, build_index, load_index, save_index
from .input_reader import read_input
from .matcher import rank_candidates
from .models import Candidate, DimensionResult
from .normalizer import compact_name, normalize_name
from .page_discovery import BrandPageLookup, cross_source_candidate_pages, fallback_pages, targeted_pages
from .parser import parse_page
from .progress import ProgressFiles
from .qwen_aliases import GeneratedAliases, GeneratedDimensions, QwenAliasGenerator
from .reporter import make_report, save_report
from .utils import project_root, utc_now
from .validator import validate


class _TerminalNoiseFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        is_http_transport = record.name == "httpx" or record.name.startswith("httpcore")
        is_qwen_detail = record.name == "moto_dimension_crawler.qwen_aliases"
        return not ((is_http_transport and record.levelno < logging.WARNING) or is_qwen_detail)


def setup_logging(level: str) -> None:
    log_dir = project_root() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level.upper())
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    console_formatter = logging.Formatter("%(message)s")
    console = logging.StreamHandler(); console.setFormatter(console_formatter); console.addFilter(_TerminalNoiseFilter()); root.addHandler(console)
    normal = logging.FileHandler(log_dir / "crawler.log", encoding="utf-8"); normal.setFormatter(formatter); root.addHandler(normal)
    errors = logging.FileHandler(log_dir / "errors.log", encoding="utf-8"); errors.setLevel(logging.ERROR); errors.setFormatter(formatter); root.addHandler(errors)
    # Keep request details in crawler.log, but hide successful transport noise
    # from the terminal. Reset explicit levels in case logging is reconfigured.
    logging.getLogger("httpx").setLevel(logging.NOTSET)
    logging.getLogger("httpcore").setLevel(logging.NOTSET)


def _ai_status_label(generated: GeneratedAliases | None) -> str:
    if generated is None or generated.status in {"DISABLED", "SKIPPED_CONFIDENT"}:
        return ""
    labels = {
        "CACHED_SUCCESS": "cache",
        "CACHED_TIMEOUT": "timeout(cached)",
        "CACHED_API_ERROR": "api-error(cached)",
        "TIMEOUT": "timeout",
        "API_ERROR": "api-error",
    }
    if generated.status in {"SUCCESS", "CACHED_SUCCESS"}:
        source = labels.get(generated.status, "api")
        decision = generated.decision.lower().replace("_", "-")
        detail = ""
        if generated.decision == "MATCH" and generated.match_basis:
            detail = f"({generated.match_basis.lower()},{generated.confidence.lower()})"
        return f"{source}:{decision}{detail}"
    return labels.get(generated.status, generated.status.lower())


def log_match_summary(record, ranked, generated: GeneratedAliases | None = None,
                      position: int | None = None, total: int | None = None,
                      inferred: GeneratedDimensions | None = None) -> None:
    matched = [candidate for candidate in ranked if candidate.status in {"EXACT", "LIKELY", "MULTIPLE"}]
    best = matched[0] if matched else ranked[0] if ranked else None
    ai = _ai_status_label(generated)
    progress = f"[{position}/{total}] " if position is not None and total is not None else ""
    if inferred is not None and inferred.decision == "INFER":
        present = "/".join(key.removesuffix("_mm") for key, value in inferred.values.items() if value is not None)
        message = f"{progress}INFER {record.make} / {record.model} | fields={present or 'none'} | confidence={inferred.confidence.lower()}"
        inference_source = "cache" if inferred.status == "CACHED_SUCCESS" else "api"
        ai = f"{inference_source}:dimension-inference"
    elif matched:
        message = f"{progress}OK   {record.make} / {record.model} -> {best.title} | matches={len(matched)}"
    else:
        closest = best.title if best else "none"
        message = f"{progress}MISS {record.make} / {record.model} | closest={closest}"
    if ai:
        message += f" | ai={ai}"
    logging.getLogger(__name__).info(message)


def input_rows(records) -> list[dict]:
    return [{
        "INPUT_ID": r.input_id, "MAKE": r.make, "MODEL": r.model, "车辆类型": r.vehicle_type,
        "MAKE_NORMALIZED": r.make_normalized, "MODEL_NORMALIZED": r.model_normalized,
        "MODEL_COMPACT": r.model_compact, "MODEL_NUMBER_TOKENS": "|".join(r.number_tokens),
        "MODEL_WORD_TOKENS": "|".join(r.word_tokens),
    } for r in records]


def _confidence(match_status: str, parsed) -> str:
    if match_status == "EXACT" and parsed.parse_status == "COMPLETE" and not parsed.anomaly_flags and parsed.width_scope != "UNKNOWN" and parsed.height_scope != "UNKNOWN":
        return "HIGH"
    if match_status in {"EXACT", "LIKELY"} and parsed.parse_status in {"COMPLETE", "PARTIAL"} and not parsed.anomaly_flags:
        return "MEDIUM"
    return "LOW"


def best_review_candidate(rows: list[dict], input_id: str, review_threshold: int) -> dict:
    return next((row for row in rows
                 if row["INPUT_ID"] == input_id
                 and row.get("MATCH_STATUS") == "REVIEW"
                 and float(row.get("MATCH_SCORE") or 0) >= review_threshold
                 and "primary_alpha=yes" in row.get("MATCH_REASON", "")), {})


def preferred_source_rows(rows: list[dict]) -> list[dict]:
    """Keep the most complete row per input/year, using configured source order as tie-breaker."""
    confidence_rank = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "": 0}
    selected: dict[tuple[str, str], tuple[tuple, dict]] = {}
    for row in rows:
        year_key = str(row.get("YEAR_START") or row.get("YEAR") or row.get("SOURCE_URL", ""))
        key = (row["INPUT_ID"], year_key)
        completeness = sum(row.get(field) not in (None, "") for field in ("L-MM", "W-MM", "H-MM"))
        rank = (
            completeness,
            row.get("PARSE_STATUS") == "COMPLETE",
            confidence_rank.get(row.get("MATCH_CONFIDENCE", ""), 0),
            float(row.get("MATCH_SCORE") or 0),
            -int(row.get("SOURCE_PRIORITY") or 99),
        )
        previous = selected.get(key)
        if previous is None or rank > previous[0]:
            selected[key] = (rank, row)
    return [value[1] for value in selected.values()]


def load_resume_snapshot(output: Path) -> dict[str, list[dict]]:
    """Load the last successful export so a partial resume can preserve untouched rows."""
    path = output / "logs" / "run_details.jsonl"
    datasets: dict[str, list[dict]] = {}
    if not path.exists():
        return datasets
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        record_type, payload = item.get("record_type"), item.get("payload")
        if record_type and isinstance(payload, dict):
            datasets.setdefault(record_type, []).append(payload)
    return datasets


def merge_resumed_rows(previous: list[dict], current: list[dict], replaced_ids: set[str]) -> list[dict]:
    """Replace rows for retried inputs while retaining rows outside the current slice."""
    return [row for row in previous if row.get("INPUT_ID") not in replaced_ids] + current


def checkpoint_ok_rows(record, candidate_rows: list[dict], dimension_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Return restorable rows only when every trusted checkpoint candidate finished parsing."""
    same_input_candidates = [
        row for row in candidate_rows
        if row.get("INPUT_ID") == record.input_id
        and normalize_name(str(row.get("MAKE", ""))) == record.make_normalized
        and compact_name(str(row.get("MODEL", ""))) == record.model_compact
    ]
    credible = [row for row in same_input_candidates
                if row.get("MATCH_STATUS") in {"EXACT", "LIKELY", "MULTIPLE"}]
    if not credible:
        return [], []
    dimensions_by_url = {
        str(row.get("SOURCE_URL") or row.get("url") or ""): row
        for row in dimension_rows
        if row.get("INPUT_ID") == record.input_id
        and normalize_name(str(row.get("MAKE", ""))) == record.make_normalized
        and compact_name(str(row.get("MODEL", ""))) == record.model_compact
    }
    restored_dimensions = []
    for candidate in credible:
        url = str(candidate.get("CANDIDATE_URL") or candidate.get("url") or "")
        parsed = dimensions_by_url.get(url)
        if parsed is None or parsed.get("PARSE_STATUS") not in {"COMPLETE", "PARTIAL"}:
            return [], []
        restored_dimensions.append({
            key: value for key, value in parsed.items()
            if key not in {"input_id", "url", "parsed_at"}
        })
    restored_candidates = [{
        key: value for key, value in row.items() if key not in {"input_id", "url"}
    } for row in same_input_candidates]
    return restored_candidates, restored_dimensions


def checkpoint_match_rows(record, candidate_rows: list[dict]) -> list[dict]:
    """Restore a completed trustworthy match even if page parsing is still pending."""
    same_input = [
        row for row in candidate_rows
        if row.get("INPUT_ID") == record.input_id
        and normalize_name(str(row.get("MAKE", ""))) == record.make_normalized
        and compact_name(str(row.get("MODEL", ""))) == record.model_compact
    ]
    if not any(row.get("MATCH_STATUS") in {"EXACT", "LIKELY", "MULTIPLE"} for row in same_input):
        return []
    return [{key: value for key, value in row.items() if key not in {"input_id", "url"}} for row in same_input]


def candidate_from_checkpoint(row: dict) -> Candidate:
    return Candidate(
        input_id=str(row["INPUT_ID"]), title=str(row.get("CANDIDATE_TITLE", "")),
        url=str(row.get("CANDIDATE_URL", "")), source_make=str(row.get("SOURCE_MAKE", "")),
        source_model=str(row.get("SOURCE_MODEL", "")), source_version=str(row.get("SOURCE_VERSION", "")),
        source_year=str(row.get("SOURCE_YEAR", "")), score=int(float(row.get("MATCH_SCORE") or 0)),
        status=str(row.get("MATCH_STATUS", "REVIEW")), reason=str(row.get("MATCH_REASON", "")),
        discovery_method=str(row.get("DISCOVERY_METHOD", "CHECKPOINT")),
        source_name=str(row.get("DATA_SOURCE", "motorcyclespecs")),
        source_priority=int(row.get("SOURCE_PRIORITY") or 99),
    )


def _candidate_fetch_order(item: tuple) -> tuple:
    """Prefer trustworthy matches and configured sources before weaker fallbacks."""
    _, candidate = item
    status_rank = {"EXACT": 0, "LIKELY": 1, "MULTIPLE": 2}
    year_values = re.findall(r"(?:19|20)\d{2}", candidate.source_year or candidate.url)
    newest_year = max((int(value) for value in year_values), default=0)
    return (
        status_rank.get(candidate.status, 9),
        int(candidate.source_priority or 99),
        -int(candidate.score or 0),
        -newest_year,
        candidate.url,
    )


def adaptive_candidate_plan(selected: list[tuple], max_same_title_pages: int = 3) -> list[tuple]:
    """Bound yearly fan-out while retaining early/middle/late representative pages."""
    grouped: dict[tuple[str, str, str], list[tuple]] = defaultdict(list)
    for item in selected:
        record, candidate = item
        title_key = compact_name(candidate.title) or candidate.url
        grouped[(record.input_id, candidate.source_name, title_key)].append(item)

    kept: list[tuple] = []
    cap = max(1, int(max_same_title_pages))
    for items in grouped.values():
        ordered = sorted(items, key=_candidate_fetch_order)
        if len(ordered) <= cap:
            kept.extend(ordered)
            continue
        chronological = sorted(
            ordered,
            key=lambda item: (
                max((int(value) for value in re.findall(r"(?:19|20)\d{2}", item[1].source_year or item[1].url)), default=0),
                item[1].url,
            ),
        )
        indexes = [round(index * (len(chronological) - 1) / (cap - 1)) for index in range(cap)] if cap > 1 else [len(chronological) - 1]
        kept.extend(chronological[index] for index in dict.fromkeys(indexes))
    return sorted(kept, key=lambda item: (item[0].input_id, *_candidate_fetch_order(item)))


def _is_reliable_complete(candidate: Candidate, dim: DimensionResult) -> bool:
    return (
        candidate.status in {"EXACT", "LIKELY"}
        and dim.parse_status == "COMPLETE"
        and not dim.anomaly_flags
    )


def run_pipeline(*, input_path: Path, output: Path, config_path: Path, sheet: str | None = None,
                 resume: bool = True, force_refetch: bool = False, force_reparse: bool = False,
                 clear_checkpoint_before_run: bool = False,
                 max_concurrency: int | None = None, request_delay_min: float | None = None,
                 request_delay_max: float | None = None, limit: int | None = None, start_row: int = 1,
                 trusted_score_threshold: int | None = None,
                 log_level: str = "INFO", stop_after: str = "export") -> dict:
    setup_logging(log_level)
    started = utc_now(); cfg = load_config(config_path)
    if max_concurrency is not None: cfg["crawler"]["max_concurrency"] = min(2, max(1, max_concurrency))
    if request_delay_min is not None: cfg["crawler"]["request_delay_min_seconds"] = request_delay_min
    if request_delay_max is not None: cfg["crawler"]["request_delay_max_seconds"] = request_delay_max
    if trusted_score_threshold is not None:
        cfg["matching"]["trusted_score_threshold"] = trusted_score_threshold
    threshold = cfg["matching"].get("trusted_score_threshold", cfg["matching"].get("likely_threshold", 85))
    if not 0 <= threshold <= 100:
        raise ValueError("trusted-score-threshold must be between 0 and 100")
    if cfg["crawler"]["request_delay_min_seconds"] > cfg["crawler"]["request_delay_max_seconds"]:
        raise ValueError("request-delay-min cannot exceed request-delay-max")
    records = read_input(input_path, cfg, sheet, start_row, limit)
    root = project_root(); output = output.resolve()
    resume_snapshot = load_resume_snapshot(output) if resume else {}
    current_input_ids = {record.input_id for record in records}
    checkpoint_path = root / "data" / "checkpoints" / "state.sqlite3"
    if clear_checkpoint_before_run:
        removed = clear_checkpoint(checkpoint_path)
        logging.getLogger(__name__).info(
            "CHECKPOINT_CLEARED=%s, FILES_REMOVED=%d", checkpoint_path, len(removed),
        )
    db = StateDB(checkpoint_path)
    for record in records:
        db.upsert_json("input_records", {"input_id": record.input_id}, record.dict(), commit=False)
    db.conn.commit()
    inputs = input_rows(records)
    cache = PageCache(root / "data" / "cache")
    crawler = Crawler(cfg, cache, db)
    progress_files: ProgressFiles | None = None
    try:
        index_path = root / "data" / "index" / "pages.json"
        manifest_path = root / "data" / "index" / "brands.json"
        requested_brands = {r.make for r in records}
        index = load_index(index_path) if resume and index_path.exists() and not force_refetch else []
        for page in index:
            page.setdefault("source_name", "motorcyclespecs")
            page.setdefault("source_priority", 1)
        raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if resume and manifest_path.exists() and not force_refetch else {}
        manifests = ({"motorcyclespecs": raw_manifest} if isinstance(raw_manifest, list) else raw_manifest)
        sources = sorted(
            (source for source in cfg.get("sources", [dict(cfg["site"], name="motorcyclespecs", index_type="motorcyclespecs", priority=1)])
             if source.get("enabled", True)),
            key=lambda source: int(source.get("priority", 99)),
        )
        builders = {
            "motorcyclespecs": build_index,
            "1000ps": build_1000ps_index,
            "bikedekho": build_bikedekho_index,
            "bikez": build_bikez_index,
        }
        for source in sources:
            source_name = source["name"]
            indexed_brands = set(manifests.get(source_name, []))
            indexed_compact = {compact_name(value) for value in indexed_brands}
            missing_brands = {brand for brand in requested_brands if compact_name(brand) not in indexed_compact}
            if not missing_brands:
                continue
            logging.getLogger(__name__).info(
                "INDEXING_SOURCE=%s, BRANDS=%d, INDEX_PAGES=%d", source_name, len(missing_brands), len(index),
            )
            builder = builders[source.get("index_type", source_name)]
            if builder is build_index:
                source_index = builder(crawler, source["base_url"], missing_brands)
            else:
                source_index = builder(crawler, source["base_url"], missing_brands, int(source.get("priority", 99)))
            index = list({page["page_url"]: page for page in [*index, *source_index]}.values())
            for brand in missing_brands:
                if any(compact_name(page.get("brand_guess", "")) == compact_name(brand) for page in source_index):
                    indexed_brands.add(brand)
                else:
                    logging.getLogger(__name__).warning(
                        "INDEXING_SOURCE=%s, BRAND=%s produced no pages; it will be retried", source_name, brand,
                    )
            manifests[source_name] = sorted(indexed_brands)
            save_index(index, index_path)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(json.dumps(manifests, ensure_ascii=False, indent=2), encoding="utf-8")
            logging.getLogger(__name__).info(
                "INDEXED_SOURCE=%s, SOURCE_PAGES=%d, INDEX_PAGES=%d", source_name, len(source_index), len(index),
            )
        manual_pages = load_manual_pages(config_path.parent)
        index = list({page["page_url"]: page for page in [*index, *manual_pages]}.values())
        if stop_after == "build-index":
            return {"index_count": len(index), "index_path": str(index_path)}
        progress_files = ProgressFiles(output)
        brand_aliases, model_aliases = load_aliases(config_path.parent)
        runtime_brand_aliases = {key: list(values) for key, values in brand_aliases.items()}
        runtime_model_aliases = {key: list(values) for key, values in model_aliases.items()}
        page_lookup = BrandPageLookup(index)
        qwen_aliases = QwenAliasGenerator(cfg.get("qwen_aliases", {}), root / "data" / "cache")
        generated_alias_records = []
        candidates_out, selected, inferred_rows, checkpoint_raw_rows = [], [], [], []
        checkpoint_candidates_by_input: dict[str, list[dict]] = {}
        checkpoint_dimensions_by_input: dict[str, list[dict]] = {}
        if resume and not force_refetch and not force_reparse:
            for row in db.rows("candidate_pages"):
                checkpoint_candidates_by_input.setdefault(str(row.get("INPUT_ID") or row.get("input_id") or ""), []).append(row)
            for row in db.rows("dimension_results"):
                checkpoint_dimensions_by_input.setdefault(str(row.get("INPUT_ID") or row.get("input_id") or ""), []).append(row)
        try:
            for match_position, record in enumerate(records, start=1):
                restored_candidates = checkpoint_match_rows(
                    record, checkpoint_candidates_by_input.get(record.input_id, []),
                )
                if restored_candidates:
                    candidates_out.extend(restored_candidates)
                    saved_dimensions = {
                        str(row.get("SOURCE_URL") or row.get("url") or ""): row
                        for row in checkpoint_dimensions_by_input.get(record.input_id, [])
                        if row.get("PARSE_STATUS") in {"COMPLETE", "PARTIAL"}
                    }
                    restored_dimensions, pending_candidates = [], []
                    for row in restored_candidates:
                        if row.get("MATCH_STATUS") not in {"EXACT", "LIKELY", "MULTIPLE"}:
                            continue
                        url = str(row.get("CANDIDATE_URL") or "")
                        if url in saved_dimensions:
                            restored_dimensions.append({
                                key: value for key, value in saved_dimensions[url].items()
                                if key not in {"input_id", "url", "parsed_at"}
                            })
                        else:
                            pending_candidates.append(candidate_from_checkpoint(row))
                    if (
                        cfg["crawler"].get("fetch_strategy", "adaptive") == "adaptive"
                        and any(
                            row.get("PARSE_STATUS") == "COMPLETE"
                            and not row.get("ANOMALY_FLAGS")
                            and row.get("CONFIDENCE") in {"HIGH", "MEDIUM"}
                            for row in saved_dimensions.values()
                        )
                    ):
                        # One reliable completed page satisfies an adaptive task;
                        # do not fetch every remaining year on the next resume.
                        restored_dimensions = [{
                            key: value for key, value in row.items()
                            if key not in {"input_id", "url", "parsed_at"}
                        } for row in saved_dimensions.values()]
                        pending_candidates = []
                    selected.extend((record, candidate) for candidate in pending_candidates)
                    checkpoint_raw_rows.extend(restored_dimensions)
                    input_row = next(item for item in inputs if item["INPUT_ID"] == record.input_id)
                    input_row["QWEN_BRAND_ALIASES"] = ""
                    input_row["QWEN_MODEL_ALIASES"] = ""
                    generated_alias_records.append({
                        "INPUT_ID": record.input_id, "MAKE": record.make, "MODEL": record.model,
                        "PROVIDER": "CHECKPOINT", "API_MODEL": qwen_aliases.model,
                        "API_STATUS": "SKIPPED_CHECKPOINT_MATCH", "DECISION": "MATCH",
                        "REVIEWED_CANDIDATES": [], "SELECTED_CANDIDATE": "",
                        "AI_CONFIDENCE": "", "MATCH_BASIS": "CHECKPOINT",
                        "AI_EXPLANATION": "Trusted candidates and parsed dimensions restored from SQLite checkpoint.",
                        "CONFIGURATION_TOKENS": [], "BRAND_ALIASES": [], "MODEL_ALIASES": [],
                        "INFERENCE_STATUS": "SKIPPED_CHECKPOINT_MATCH", "INFERENCE_DECISION": "",
                        "INFERENCE_CONFIDENCE": "", "INFERENCE_VALUES": {}, "INFERENCE_EXPLANATION": "",
                    })
                    logging.getLogger(__name__).info(
                        "[%d/%d] SKIP %s / %s | checkpoint=%s | candidates=%d | dimensions=%d | fetch_pending=%d",
                        match_position, len(records), record.make, record.model,
                        "OK" if not pending_candidates else "MATCH_OK",
                        len(restored_candidates), len(restored_dimensions), len(pending_candidates),
                    )
                    restored_credible = [
                        row for row in restored_candidates
                        if row.get("MATCH_STATUS") in {"EXACT", "LIKELY", "MULTIPLE"}
                    ]
                    progress_files.match.write({
                        "POSITION": match_position, "TOTAL": len(records), "COMPLETED_AT": utc_now(),
                        "INPUT_ID": record.input_id, "MAKE": record.make, "MODEL": record.model,
                        "STATUS": "SKIP", "BEST_PAGE_TITLE": (
                            restored_credible[0].get("CANDIDATE_TITLE", "") if restored_credible else ""
                        ),
                        "MATCHES": len(restored_credible), "CANDIDATE_COUNT": len(restored_candidates),
                        "CHECKPOINT": "OK" if not pending_candidates else "MATCH_OK", "AI_STATUS": "",
                    })
                    continue
                alias_key = f"{record.make}|{record.model}"
                static_aliases = [
                    alias
                    for key, values in model_aliases.items()
                    for alias in values
                    if normalize_name(key.partition("|")[0]) == record.make_normalized
                    and compact_name(key.partition("|")[2]) == record.model_compact
                ]
                static_brand_aliases = [
                    alias
                    for key, values in brand_aliases.items()
                    for alias in values
                    if normalize_name(key) == record.make_normalized
                ]
                aliases = list(dict.fromkeys(static_aliases))
                brand_values = list(dict.fromkeys(static_brand_aliases))
                runtime_model_aliases[alias_key] = aliases
                runtime_brand_aliases[record.make_normalized] = brand_values
                ignored_words = cfg.get("matching", {}).get("ignored_model_words", [])
                brand_index_pages = page_lookup.pages_for(record.make, brand_values)
                strict_pages = targeted_pages(record, brand_index_pages, aliases, ignored_words, brand_values)
                ranked = rank_candidates(
                    record, strict_pages, cfg, runtime_brand_aliases, runtime_model_aliases,
                )
                credible = [item for item in ranked if item.status in {"EXACT", "LIKELY", "MULTIPLE"}]

                if credible or not qwen_aliases.enabled:
                    generated = GeneratedAliases(
                        [], [], "SKIPPED_CONFIDENT" if credible else "DISABLED",
                        "MATCH" if credible else "AMBIGUOUS",
                        credible[0].title if credible else "", [],
                    )
                    reviewed_titles = []
                else:
                    broad_pages = fallback_pages(record, brand_index_pages, brand_values, ignored_words)
                    cross_source_pages = cross_source_candidate_pages(
                        record, brand_index_pages, brand_values, ignored_words, qwen_aliases.max_candidates,
                    )
                    review_pages = list({
                        page["page_url"]: page
                        for page in [*strict_pages, *broad_pages, *cross_source_pages]
                    }.values())
                    preliminary = rank_candidates(
                        record, review_pages, cfg, runtime_brand_aliases, runtime_model_aliases,
                    )
                    reviewed_titles = [item.title for item in preliminary[:qwen_aliases.max_candidates]]
                    generated = (qwen_aliases.generate(record, reviewed_titles) if reviewed_titles else GeneratedAliases(
                        [], [], "SKIPPED_NO_CANDIDATES", "NO_MATCH", "", [],
                        "LOW", "NONE", "No catalog candidates were available for comparison.",
                    ))
                    aliases = list(dict.fromkeys([*aliases, *generated.model_aliases]))
                    brand_values = list(dict.fromkeys([*brand_values, *generated.brand_aliases]))
                    runtime_model_aliases[alias_key] = aliases
                    runtime_brand_aliases[record.make_normalized] = brand_values
                    brand_index_pages = page_lookup.pages_for(record.make, brand_values)
                    strict_pages = targeted_pages(record, brand_index_pages, aliases, ignored_words, brand_values)
                    broad_pages = fallback_pages(record, brand_index_pages, brand_values, ignored_words)
                    cross_source_pages = cross_source_candidate_pages(
                        record, brand_index_pages, brand_values, ignored_words, qwen_aliases.max_candidates,
                    )
                    final_pages = list({
                        page["page_url"]: page
                        for page in [*strict_pages, *broad_pages, *cross_source_pages]
                    }.values())
                    ranked = rank_candidates(
                        record, final_pages, cfg, runtime_brand_aliases, runtime_model_aliases,
                    )

                credible = [item for item in ranked if item.status in {"EXACT", "LIKELY", "MULTIPLE"}]
                inferred = GeneratedDimensions(status="SKIPPED_CONFIDENT" if credible else "DISABLED")
                if not credible:
                    inferred = qwen_aliases.infer_dimensions(record, cfg.get("validation", {}))
                    if inferred.decision == "INFER":
                        values = inferred.values
                        core_values = [values.get("length_mm"), values.get("width_mm"), values.get("height_mm")]
                        parse_status = "COMPLETE" if all(value is not None for value in core_values) else "PARTIAL"
                        inferred_rows.append({
                            "INPUT_ID": record.input_id, "MAKE": record.make, "MODEL": record.model,
                            "车辆类型": record.vehicle_type, "DATA_SOURCE": "QWEN_INFERENCE", "SOURCE_PRIORITY": 99,
                            "SOURCE_MAKE": record.make, "SOURCE_MODEL": record.model, "SOURCE_VERSION": "",
                            "YEAR": "", "YEAR_START": "", "YEAR_END": "", "PAGE_TITLE": f"{record.make} {record.model}",
                            "SOURCE_URL": "", "L_RAW": "", "W_RAW": "", "H_RAW": "", "UNIT_RAW": "mm",
                            "L-MM-MIN": values.get("length_mm"), "L-MM-MAX": values.get("length_mm"),
                            "W-MM-MIN": values.get("width_mm"), "W-MM-MAX": values.get("width_mm"),
                            "H-MM-MIN": values.get("height_mm"), "H-MM-MAX": values.get("height_mm"),
                            "L-MM": values.get("length_mm"), "W-MM": values.get("width_mm"), "H-MM": values.get("height_mm"),
                            "WHEELBASE-MM": values.get("wheelbase_mm"), "SEAT-HEIGHT-MM": values.get("seat_height_mm"),
                            "GROUND-CLEARANCE-MM": values.get("ground_clearance_mm"), "WIDTH_SCOPE": "UNKNOWN",
                            "HEIGHT_SCOPE": "UNKNOWN", "ACCESSORY_STATUS": "UNKNOWN",
                            "DIMENSION_RAW": json.dumps(values, ensure_ascii=False), "MODEL_SIMILARITY": "",
                            "MATCH_SCORE": 0, "MATCH_CONFIDENCE": "LOW", "MATCH_STATUS": "INFERRED",
                            "PARSE_STATUS": parse_status, "CONFIDENCE": "LOW", "ANOMALY_FLAGS": "AI_INFERRED",
                            "NOTES": f"Unverified Qwen inference: {inferred.explanation}",
                            "FETCHED_AT": utc_now(), "CONTENT_HASH": "",
                        })

                input_row = next(item for item in inputs if item["INPUT_ID"] == record.input_id)
                input_row["QWEN_BRAND_ALIASES"] = "|".join(generated.brand_aliases)
                input_row["QWEN_MODEL_ALIASES"] = "|".join(generated.model_aliases)
                generated_alias_records.append({
                    "INPUT_ID": record.input_id, "MAKE": record.make, "MODEL": record.model,
                    "PROVIDER": "QWEN" if qwen_aliases.enabled else "DISABLED", "API_MODEL": qwen_aliases.model,
                    "API_STATUS": generated.status, "DECISION": generated.decision,
                    "REVIEWED_CANDIDATES": reviewed_titles, "SELECTED_CANDIDATE": generated.selected_candidate,
                    "AI_CONFIDENCE": generated.confidence, "MATCH_BASIS": generated.match_basis,
                    "AI_EXPLANATION": generated.explanation,
                    "INFERENCE_STATUS": inferred.status, "INFERENCE_DECISION": inferred.decision,
                    "INFERENCE_CONFIDENCE": inferred.confidence, "INFERENCE_VALUES": inferred.values,
                    "INFERENCE_EXPLANATION": inferred.explanation,
                    "CONFIGURATION_TOKENS": generated.configuration_tokens,
                    "BRAND_ALIASES": generated.brand_aliases, "MODEL_ALIASES": generated.model_aliases,
                })
                db.clear_input_candidates(record.input_id, commit=False)
                for candidate in ranked:
                    row = {
                        "INPUT_ID": record.input_id, "MAKE": record.make, "MODEL": record.model,
                        "CANDIDATE_TITLE": candidate.title, "CANDIDATE_URL": candidate.url,
                        "DATA_SOURCE": candidate.source_name, "SOURCE_PRIORITY": candidate.source_priority,
                        "SOURCE_MAKE": candidate.source_make, "SOURCE_MODEL": candidate.source_model,
                        "SOURCE_VERSION": candidate.source_version, "SOURCE_YEAR": candidate.source_year,
                        "MATCH_SCORE": candidate.score, "MATCH_STATUS": candidate.status,
                        "MODEL_SIMILARITY": next((part.split("=",1)[1] for part in candidate.reason.split("; ") if part.startswith("model_similarity=")), ""),
                        "MATCH_CONFIDENCE": "HIGH" if candidate.status == "EXACT" else "MEDIUM" if candidate.status == "LIKELY" else "LOW",
                        "MATCH_REASON": candidate.reason, "DISCOVERY_METHOD": "MANUAL_CONFIG" if candidate.url in {p["page_url"] for p in manual_pages} else candidate.discovery_method,
                    }
                    candidates_out.append(row)
                    db.upsert_json("candidate_pages", {"input_id": record.input_id, "url": candidate.url}, row, commit=False)
                    if candidate.status in {"EXACT", "LIKELY", "MULTIPLE"}:
                        selected.append((record, candidate))
                if inferred.decision == "INFER":
                    candidates_out.append({
                        "INPUT_ID": record.input_id, "MAKE": record.make, "MODEL": record.model,
                        "CANDIDATE_TITLE": f"Qwen inference: {record.make} {record.model}", "CANDIDATE_URL": "",
                        "DATA_SOURCE": "QWEN_INFERENCE", "SOURCE_PRIORITY": 99, "SOURCE_MAKE": record.make,
                        "SOURCE_MODEL": record.model, "SOURCE_VERSION": "", "SOURCE_YEAR": "",
                        "MATCH_SCORE": 0, "MATCH_STATUS": "INFERRED", "MODEL_SIMILARITY": "",
                        "MATCH_CONFIDENCE": "LOW", "MATCH_REASON": inferred.explanation,
                        "DISCOVERY_METHOD": "QWEN_INFERENCE",
                    })
                # Persist one input atomically as soon as its match result is
                # known, so an interrupted long run can skip it next time.
                db.conn.commit()
                log_match_summary(record, ranked, generated, match_position, len(records), inferred)
                matched = [
                    candidate for candidate in ranked
                    if candidate.status in {"EXACT", "LIKELY", "MULTIPLE"}
                ]
                best = matched[0] if matched else ranked[0] if ranked else None
                progress_files.match.write({
                    "POSITION": match_position, "TOTAL": len(records), "COMPLETED_AT": utc_now(),
                    "INPUT_ID": record.input_id, "MAKE": record.make, "MODEL": record.model,
                    "STATUS": "INFER" if inferred.decision == "INFER" else "OK" if matched else "MISS",
                    "BEST_PAGE_TITLE": best.title if best else "", "MATCHES": len(matched),
                    "CANDIDATE_COUNT": len(ranked), "CHECKPOINT": "",
                    "AI_STATUS": (
                        "dimension-inference" if inferred.decision == "INFER" else _ai_status_label(generated)
                    ),
                })
        finally:
            qwen_aliases.close()
        generated_alias_path = output / "generated_aliases.json"
        if qwen_aliases.enabled:
            output.mkdir(parents=True, exist_ok=True)
            generated_alias_path.write_text(
                json.dumps(generated_alias_records, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        else:
            generated_alias_path.unlink(missing_ok=True)
        db.conn.commit()
        inferred_candidate_rows = [
            row for row in candidates_out if row.get("MATCH_STATUS") == "INFERRED"
        ]
        if stop_after == "match":
            credible_checkpoint = [row for row in candidates_out if row.get("MATCH_STATUS") in {"EXACT", "LIKELY", "MULTIPLE"}]
            return {"candidate_count": len(candidates_out), "credible_page_count": len(credible_checkpoint),
                    "credible_input_count": len({row["INPUT_ID"] for row in credible_checkpoint}),
                    "inferred_input_count": len(inferred_rows),
                    "progress_file": str((output / "match_progress.csv").resolve())}
        # The remaining stages use selected candidates and checkpoint rows only.
        # Drop the full catalog and matching caches before loading page bodies.
        index = []
        manual_pages = []
        page_lookup = None
        checkpoint_candidates_by_input.clear()
        checkpoint_dimensions_by_input.clear()
        runtime_brand_aliases.clear()
        runtime_model_aliases.clear()
        brand_aliases.clear()
        model_aliases.clear()
        generated_alias_records.clear()
        candidates_out.clear()
        qwen_aliases = None
        generated = None
        inferred = None
        ranked = []
        credible = []
        strict_pages = []
        broad_pages = []
        cross_source_pages = []
        preliminary = []
        final_pages = []
        brand_index_pages = []
        source_index = []
        gc.collect()
        raw_out = [*checkpoint_raw_rows, *inferred_rows]
        fetch_strategy = cfg["crawler"].get("fetch_strategy", "adaptive")
        if fetch_strategy not in {"adaptive", "exhaustive"}:
            raise ValueError("crawler.fetch_strategy must be adaptive or exhaustive")
        planned_selected = (
            adaptive_candidate_plan(
                selected, cfg["crawler"].get("adaptive_max_same_title_pages", 3),
            )
            if fetch_strategy == "adaptive" else sorted(selected, key=_candidate_fetch_order)
        )
        fetch_results: dict[tuple[str, str], tuple[bool, dict | None, str]] = {}
        fetched_by_url: dict[str, tuple[str | None, dict | None, bool]] = {}
        preview_parsed_pages_by_url: dict[str, tuple[dict, DimensionResult]] = {}
        attempted_selected: list[tuple] = []
        fetch_total = len(checkpoint_raw_rows) + len(inferred_rows) + len(planned_selected)
        fetch_position = 0
        for row in checkpoint_raw_rows:
            fetch_position += 1
            progress_files.fetch.write({
                "POSITION": fetch_position, "TOTAL": fetch_total, "COMPLETED_AT": utc_now(),
                "INPUT_ID": row.get("INPUT_ID", ""), "MAKE": row.get("MAKE", ""),
                "MODEL": row.get("MODEL", ""), "STATUS": "SKIPPED_PARSED_CHECKPOINT",
                "PAGE_TITLE": row.get("PAGE_TITLE", ""), "SOURCE_URL": row.get("SOURCE_URL", ""),
                "DATA_SOURCE": row.get("DATA_SOURCE", ""), "FETCHED_AT": row.get("FETCHED_AT", ""),
                "CONTENT_HASH": row.get("CONTENT_HASH", ""),
            })
        for row in inferred_rows:
            fetch_position += 1
            progress_files.fetch.write({
                "POSITION": fetch_position, "TOTAL": fetch_total, "COMPLETED_AT": utc_now(),
                "INPUT_ID": row.get("INPUT_ID", ""), "MAKE": row.get("MAKE", ""),
                "MODEL": row.get("MODEL", ""), "STATUS": "NOT_REQUIRED_INFERENCE",
                "PAGE_TITLE": row.get("PAGE_TITLE", ""), "SOURCE_URL": "",
                "DATA_SOURCE": row.get("DATA_SOURCE", ""), "FETCHED_AT": row.get("FETCHED_AT", ""),
                "CONTENT_HASH": "",
            })
        queues: dict[str, deque] = defaultdict(deque)
        for item in planned_selected:
            queues[item[0].input_id].append(item)
        active_ids = set(queues)
        reported_urls: set[str] = set()
        max_workers = max(1, int(cfg["crawler"].get("max_concurrency", 1)))
        while active_ids:
            round_items = [queues[input_id].popleft() for input_id in sorted(active_ids) if queues[input_id]]
            if not round_items:
                break
            new_urls = {
                candidate.url: candidate
                for _, candidate in round_items
                if candidate.url not in fetched_by_url
            }
            if new_urls:
                with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="page-fetch") as executor:
                    futures = {
                        executor.submit(crawler.fetch, url, force_refetch): url for url in new_urls
                    }
                    for future in as_completed(futures):
                        url = futures[future]
                        try:
                            fetched_by_url[url] = future.result()
                        except Exception as exc:  # keep one worker failure from aborting the run
                            logging.getLogger(__name__).exception("Fetch worker failed for %s", url)
                            fetched_by_url[url] = (None, {"error": str(exc)}, False)

            resolved_this_round: set[str] = set()
            for record, candidate in round_items:
                attempted_selected.append((record, candidate))
                fetch_position += 1
                html, meta, from_cache = fetched_by_url[candidate.url]
                fetch_ok = html is not None
                if candidate.url in reported_urls:
                    fetch_status = "REUSED_URL" if fetch_ok else "REUSED_FETCH_FAILED"
                elif fetch_ok:
                    fetch_status = "CACHE_HIT" if from_cache else "FETCHED"
                elif (meta or {}).get("failure_cached"):
                    fetch_status = "FAILURE_CACHE_HIT"
                else:
                    fetch_status = "FETCH_FAILED"
                reported_urls.add(candidate.url)
                fetch_results[(record.input_id, candidate.url)] = (fetch_ok, meta, fetch_status)
                progress_files.fetch.write({
                    "POSITION": fetch_position, "TOTAL": fetch_total, "COMPLETED_AT": utc_now(),
                    "INPUT_ID": record.input_id, "MAKE": record.make, "MODEL": record.model,
                    "STATUS": fetch_status, "PAGE_TITLE": candidate.title, "SOURCE_URL": candidate.url,
                    "DATA_SOURCE": candidate.source_name, "FETCHED_AT": (meta or {}).get("fetched_at", ""),
                    "CONTENT_HASH": (meta or {}).get("content_hash", ""),
                })
                logging.getLogger(__name__).info(
                    "FETCH_PROGRESS=%d/%d, BRAND=%s, MODEL=%s, PAGE_TITLE=%s, STATUS=%s",
                    fetch_position, fetch_total, record.make, record.model, candidate.title, fetch_status,
                )
                if fetch_strategy == "adaptive" and fetch_ok:
                    if candidate.url not in preview_parsed_pages_by_url:
                        page = parse_page(html, candidate.url)
                        preview_parsed_pages_by_url[candidate.url] = (page, validate(page["dimensions"], cfg))
                    _, dim = preview_parsed_pages_by_url[candidate.url]
                    if _is_reliable_complete(candidate, dim):
                        resolved_this_round.add(record.input_id)

            for input_id in list(active_ids):
                if input_id in resolved_this_round or not queues[input_id]:
                    active_ids.discard(input_id)

        attempted_keys = {(record.input_id, candidate.url) for record, candidate in attempted_selected}
        adaptive_skipped_count = 0
        for record, candidate in planned_selected:
            if (record.input_id, candidate.url) in attempted_keys:
                continue
            adaptive_skipped_count += 1
            fetch_position += 1
            progress_files.fetch.write({
                "POSITION": fetch_position, "TOTAL": fetch_total, "COMPLETED_AT": utc_now(),
                "INPUT_ID": record.input_id, "MAKE": record.make, "MODEL": record.model,
                "STATUS": "SKIPPED_ADAPTIVE", "PAGE_TITLE": candidate.title,
                "SOURCE_URL": candidate.url, "DATA_SOURCE": candidate.source_name,
                "FETCHED_AT": "", "CONTENT_HASH": "",
            })
        selected = attempted_selected
        if stop_after == "fetch":
            return {
                "selected_count": len(selected), "planned_count": len(planned_selected),
                "adaptive_skipped_count": adaptive_skipped_count,
                "fetch_result_count": len(fetch_results),
                "unique_url_count": len(fetched_by_url),
                "fetched": crawler.fetched, "cache_hits": crawler.cache_hits,
                "failure_cache_hits": crawler.failure_cache_hits,
                "progress_file": str((output / "fetch_progress.csv").resolve()),
            }
        unique_fetch_url_count = len(fetched_by_url)
        fetched_by_url.clear()
        gc.collect()

        parse_total = len(checkpoint_raw_rows) + len(inferred_rows) + len(selected)
        parse_position = 0
        for row in checkpoint_raw_rows:
            parse_position += 1
            progress_files.parse.write({
                "POSITION": parse_position, "TOTAL": parse_total, "COMPLETED_AT": utc_now(),
                "STATUS": "RESTORED_FROM_CHECKPOINT", **row,
            })
        for row in inferred_rows:
            parse_position += 1
            progress_files.parse.write({
                "POSITION": parse_position, "TOTAL": parse_total, "COMPLETED_AT": utc_now(),
                "STATUS": "INFERRED", **row,
            })
        parsed_pages_by_url: dict[str, tuple[dict, DimensionResult]] = preview_parsed_pages_by_url
        for record, candidate in selected:
            parse_position += 1
            logging.getLogger(__name__).info(
                "PARSE_PROGRESS=%d/%d, BRAND=%s, MODEL=%s, PAGE_TITLE=%s",
                parse_position, parse_total, record.make, record.model, candidate.title,
            )
            fetch_ok, meta, fetch_status = fetch_results[(record.input_id, candidate.url)]
            if not fetch_ok:
                parse_action = fetch_status
                parsed_row = {
                    "INPUT_ID":record.input_id,"MAKE":record.make,"MODEL":record.model,"车辆类型":record.vehicle_type,
                    "DATA_SOURCE":candidate.source_name,"SOURCE_PRIORITY":candidate.source_priority,
                    "SOURCE_MAKE":candidate.source_make,"SOURCE_MODEL":candidate.source_model,"SOURCE_VERSION":candidate.source_version,
                    "PAGE_TITLE":candidate.title,"SOURCE_URL":candidate.url,"MATCH_SCORE":candidate.score,"MATCH_STATUS":candidate.status,
                    "PARSE_STATUS":"FETCH_FAILED","CONFIDENCE":"LOW","ANOMALY_FLAGS":"","NOTES":"Page fetch failed",
                }
            else:
                if candidate.url in parsed_pages_by_url:
                    page, dim = parsed_pages_by_url[candidate.url]
                    parse_action = "REUSED_PARSED_URL"
                else:
                    html = cache.read(candidate.url)
                    page = parse_page(html, candidate.url); dim = validate(page["dimensions"], cfg)
                    parsed_pages_by_url[candidate.url] = (page, dim)
                    parse_action = "PARSED"
                vals, raws = dim.values, dim.raw
                parsed_row = {
                    "INPUT_ID":record.input_id,"MAKE":record.make,"MODEL":record.model,"车辆类型":record.vehicle_type,
                    "DATA_SOURCE":candidate.source_name,"SOURCE_PRIORITY":candidate.source_priority,
                    "SOURCE_MAKE":candidate.source_make,"SOURCE_MODEL":candidate.source_model,"SOURCE_VERSION":candidate.source_version,
                    "YEAR":page["year"],"YEAR_START":page["year_start"],"YEAR_END":page["year_end"],"PAGE_TITLE":page["page_title"],"SOURCE_URL":candidate.url,
                    "L_RAW":raws.get("l",""),"W_RAW":raws.get("w",""),"H_RAW":raws.get("h",""),"UNIT_RAW":raws.get("unit",""),
                    "L-MM-MIN":vals.get("l_min"),"L-MM-MAX":vals.get("l_max"),"W-MM-MIN":vals.get("w_min"),"W-MM-MAX":vals.get("w_max"),
                    "H-MM-MIN":vals.get("h_min"),"H-MM-MAX":vals.get("h_max"),"L-MM":vals.get("l"),"W-MM":vals.get("w"),"H-MM":vals.get("h"),
                    "WHEELBASE-MM":vals.get("wheelbase"),"SEAT-HEIGHT-MM":vals.get("seat_height"),"GROUND-CLEARANCE-MM":vals.get("ground_clearance"),
                    "WIDTH_SCOPE":dim.width_scope,"HEIGHT_SCOPE":dim.height_scope,"ACCESSORY_STATUS":dim.accessory_status,"DIMENSION_RAW":dim.dimension_raw,
                    "MATCH_SCORE":candidate.score,"MATCH_STATUS":candidate.status,"PARSE_STATUS":dim.parse_status,"CONFIDENCE":_confidence(candidate.status,dim),
                    "MODEL_SIMILARITY":next((part.split("=",1)[1] for part in candidate.reason.split("; ") if part.startswith("model_similarity=")), ""),
                    "MATCH_CONFIDENCE":"HIGH" if candidate.status == "EXACT" else "MEDIUM" if candidate.status == "LIKELY" else "LOW",
                    "ANOMALY_FLAGS":"|".join(dim.anomaly_flags),"NOTES":"","FETCHED_AT":(meta or {}).get("fetched_at",""),"CONTENT_HASH":(meta or {}).get("content_hash",""),
                }
            raw_out.append(parsed_row)
            db.upsert_json("dimension_results", {"input_id":record.input_id,"url":candidate.url}, parsed_row, {"parsed_at":utc_now()})
            progress_files.parse.write({
                "POSITION": parse_position, "TOTAL": parse_total, "COMPLETED_AT": utc_now(),
                "STATUS": parse_action, **parsed_row,
            })
            logging.getLogger(__name__).info(
                "PARSE_PROGRESS=%d/%d, STATUS=%s, PARSE_STATUS=%s",
                parse_position, parse_total, parse_action,
                parsed_row.get("PARSE_STATUS", ""),
            )
        if stop_after == "parse":
            return {
                "selected_count": len(selected), "result_count": len(raw_out),
                "unique_url_count": len(parsed_pages_by_url),
                "fetched": crawler.fetched, "cache_hits": crawler.cache_hits,
                "progress_file": str((output / "parse_progress.csv").resolve()),
            }
        unique_parse_url_count = len(parsed_pages_by_url)
        parsed_pages_by_url.clear()
        fetch_results.clear()
        selected.clear()
        gc.collect()
        candidates_out = [
            {key: value for key, value in row.items() if key not in {"input_id", "url"}}
            for row in db.rows_for_input_ids("candidate_pages", current_input_ids)
        ]
        candidates_out.extend(inferred_candidate_rows)
        input_order = {record.input_id: position for position, record in enumerate(records)}
        candidates_out.sort(key=lambda row: (
            input_order.get(str(row.get("INPUT_ID", "")), len(input_order)),
            -float(row.get("MATCH_SCORE") or 0),
            int(row.get("SOURCE_PRIORITY") or 99),
            str(row.get("CANDIDATE_URL", "")),
        ))
        if resume_snapshot:
            inputs = merge_resumed_rows(resume_snapshot.get("INPUT_NORMALIZED", []), inputs, current_input_ids)
            candidates_out = merge_resumed_rows(
                resume_snapshot.get("CANDIDATE_DIAGNOSTIC", []), candidates_out, current_input_ids,
            )
            raw_out = merge_resumed_rows(resume_snapshot.get("DIMENSIONS_RAW", []), raw_out, current_input_ids)
        effective_raw = preferred_source_rows(raw_out)
        groups = group_dimensions(effective_raw, cfg)
        if stop_after == "summarize":
            return {"dimension_group_count": len(groups)}
        credible_ids = {r["INPUT_ID"] for r in candidates_out if r["MATCH_STATUS"] in {"EXACT","LIKELY","MULTIPLE","INFERRED"}}
        review = []
        for candidate_row in candidates_out:
            if candidate_row.get("MATCH_STATUS") == "REVIEW":
                issue = "VERSION_CONFLICT" if "version=no" in candidate_row.get("MATCH_REASON", "") else "LOW_MATCH_SCORE"
                review.append({"INPUT_ID":candidate_row["INPUT_ID"],"MAKE":candidate_row["MAKE"],"MODEL":candidate_row["MODEL"],
                    "ISSUE_TYPE":issue,"CANDIDATE_URLS":candidate_row["CANDIDATE_URL"],"RAW_VALUE":candidate_row["CANDIDATE_TITLE"],
                    "MATCH_SCORE":candidate_row["MATCH_SCORE"],"ANOMALY_FLAGS":"","RECOMMENDED_ACTION":"Confirm or reject candidate manually",
                    "NOTES":candidate_row.get("MATCH_REASON", "")})
        for row in raw_out:
            issues = []
            if row.get("MATCH_STATUS") == "INFERRED": issues.append("AI_INFERRED_DIMENSION")
            if row.get("PARSE_STATUS") == "FETCH_FAILED": issues.append("FETCH_FAILED")
            elif row.get("PARSE_STATUS") == "NO_DIMENSION": issues.append("DIMENSION_MISSING")
            elif row.get("PARSE_STATUS") == "PARTIAL": issues.append("PARTIAL_DIMENSION")
            elif row.get("PARSE_STATUS") not in {"COMPLETE"}: issues.append(row.get("PARSE_STATUS"))
            if not row.get("YEAR_START"): issues.append("YEAR_UNKNOWN")
            if row.get("MATCH_STATUS") in {"MULTIPLE","REVIEW"}: issues.append(row["MATCH_STATUS"])
            for issue in dict.fromkeys(i for i in issues if i):
                review.append({"INPUT_ID":row["INPUT_ID"],"MAKE":row["MAKE"],"MODEL":row["MODEL"],"ISSUE_TYPE":issue,
                    "CANDIDATE_URLS":row.get("SOURCE_URL",""),"RAW_VALUE":row.get("DIMENSION_RAW",""),"MATCH_SCORE":row.get("MATCH_SCORE",""),
                    "ANOMALY_FLAGS":row.get("ANOMALY_FLAGS",""),"RECOMMENDED_ACTION":"Verify source page manually","NOTES":row.get("NOTES","")})
        not_found = []
        for item in inputs:
            input_id = item["INPUT_ID"]
            if input_id not in credible_ids:
                best = best_review_candidate(candidates_out, input_id, cfg["matching"]["review_threshold"])
                not_found.append({"INPUT_ID":input_id,"MAKE":item["MAKE"],"MODEL":item["MODEL"],"车辆类型":item.get("车辆类型", ""),
                    "SEARCH_TERMS_USED":f"{item['MAKE']} {item['MODEL']}","BEST_CANDIDATE":best.get("CANDIDATE_URL",""),"BEST_SCORE":best.get("MATCH_SCORE",""),"NOTES":"No credible candidate; no automatic fallback selected"})
                review.append({"INPUT_ID":input_id,"MAKE":item["MAKE"],"MODEL":item["MODEL"],"ISSUE_TYPE":"NOT_FOUND","CANDIDATE_URLS":"","RAW_VALUE":"","MATCH_SCORE":best.get("MATCH_SCORE",""),"ANOMALY_FLAGS":"","RECOMMENDED_ACTION":"Search catalog manually","NOTES":""})
        report = make_report(started, inputs, candidates_out, raw_out, groups, db.rows("errors"), crawler.fetched, crawler.cache_hits)
        report["not_found_count"] = len(not_found)
        report["review_count"] = len(review)
        report["performance"] = {
            "candidate_page_relationship_count": parse_total,
            "planned_fetch_relationship_count": len(planned_selected),
            "adaptive_skipped_count": adaptive_skipped_count,
            "unique_fetched_url_count": unique_fetch_url_count,
            "unique_parsed_url_count": unique_parse_url_count,
        }
        report["progress_files"] = {
            "match": str((output / "match_progress.csv").resolve()),
            "fetch": str((output / "fetch_progress.csv").resolve()),
            "parse": str((output / "parse_progress.csv").resolve()),
        }
        save_report(report, output / "logs" / "run_report.json")
        export_all(output, inputs, candidates_out, raw_out, groups, review, not_found, report)
        return report
    finally:
        if progress_files is not None:
            progress_files.close()
        crawler.close(); db.close()
