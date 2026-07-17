from __future__ import annotations

import logging
import json
from dataclasses import asdict
from pathlib import Path

from .cache import PageCache
from .config import load_aliases, load_config, load_manual_pages
from .crawler import Crawler
from .database import StateDB
from .exporter import export_all
from .grouper import group_dimensions
from .index_builder import build_index, load_index, save_index
from .input_reader import read_input
from .matcher import rank_candidates
from .normalizer import compact_name
from .page_discovery import targeted_pages
from .parser import parse_page
from .reporter import make_report, save_report
from .utils import project_root, utc_now
from .validator import validate


def setup_logging(level: str) -> None:
    log_dir = project_root() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level.upper())
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    console = logging.StreamHandler(); console.setFormatter(formatter); root.addHandler(console)
    normal = logging.FileHandler(log_dir / "crawler.log", encoding="utf-8"); normal.setFormatter(formatter); root.addHandler(normal)
    errors = logging.FileHandler(log_dir / "errors.log", encoding="utf-8"); errors.setLevel(logging.ERROR); errors.setFormatter(formatter); root.addHandler(errors)


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


def run_pipeline(*, input_path: Path, output: Path, config_path: Path, sheet: str | None = None,
                 resume: bool = True, force_refetch: bool = False, force_reparse: bool = False,
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
    db = StateDB(root / "data" / "checkpoints" / "state.sqlite3")
    for record in records:
        db.upsert_json("input_records", {"input_id": record.input_id}, record.dict(), commit=False)
    db.conn.commit()
    inputs = input_rows(records)
    cache = PageCache(root / "data" / "cache")
    crawler = Crawler(cfg, cache, db)
    try:
        index_path = root / "data" / "index" / "pages.json"
        manifest_path = root / "data" / "index" / "brands.json"
        requested_brands = {r.make for r in records}
        indexed_brands = set(json.loads(manifest_path.read_text(encoding="utf-8"))) if resume and manifest_path.exists() and not force_refetch else set()
        index = load_index(index_path) if resume and index_path.exists() and not force_refetch else []
        if not index or not {compact_name(x) for x in requested_brands} <= {compact_name(x) for x in indexed_brands}:
            index = build_index(crawler, cfg["site"]["base_url"], requested_brands)
            save_index(index, index_path)
            manifest_path.write_text(json.dumps(sorted(requested_brands), ensure_ascii=False, indent=2), encoding="utf-8")
        manual_pages = load_manual_pages(config_path.parent)
        index = list({page["page_url"]: page for page in [*index, *manual_pages]}.values())
        if stop_after == "build-index":
            return {"index_count": len(index), "index_path": str(index_path)}
        brand_aliases, model_aliases = load_aliases(config_path.parent)
        candidates_out, selected = [], []
        for record in records:
            ranked = rank_candidates(record, targeted_pages(record, index), cfg, brand_aliases, model_aliases)
            for candidate in ranked:
                row = {
                    "INPUT_ID": record.input_id, "MAKE": record.make, "MODEL": record.model,
                    "CANDIDATE_TITLE": candidate.title, "CANDIDATE_URL": candidate.url,
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
        db.conn.commit()
        if stop_after == "match":
            return {"candidate_count": len(candidates_out), "credible_page_count": len(selected),
                    "credible_input_count": len({record.input_id for record, _ in selected})}
        raw_out = []
        for record, candidate in selected:
            if resume and not force_reparse and db.parsed(record.input_id, candidate.url):
                previous = next((x for x in db.rows("dimension_results") if x["input_id"] == record.input_id and x["url"] == candidate.url), None)
                if previous:
                    restored = {k:v for k,v in previous.items() if k not in {"input_id","url","parsed_at"}}
                    restored.update({
                        "SOURCE_MAKE": candidate.source_make, "SOURCE_MODEL": candidate.source_model,
                        "MODEL_SIMILARITY": next((part.split("=",1)[1] for part in candidate.reason.split("; ") if part.startswith("model_similarity=")), ""),
                        "MATCH_SCORE": candidate.score, "MATCH_CONFIDENCE": "HIGH" if candidate.status == "EXACT" else "MEDIUM" if candidate.status == "LIKELY" else "LOW",
                        "MATCH_STATUS": candidate.status,
                    })
                    raw_out.append(restored)
                    continue
            html, meta, _ = crawler.fetch(candidate.url, force_refetch)
            if html is None:
                parsed_row = {
                    "INPUT_ID":record.input_id,"MAKE":record.make,"MODEL":record.model,"车辆类型":record.vehicle_type,
                    "SOURCE_MAKE":candidate.source_make,"SOURCE_MODEL":candidate.source_model,"SOURCE_VERSION":candidate.source_version,
                    "PAGE_TITLE":candidate.title,"SOURCE_URL":candidate.url,"MATCH_SCORE":candidate.score,"MATCH_STATUS":candidate.status,
                    "PARSE_STATUS":"FETCH_FAILED","CONFIDENCE":"LOW","ANOMALY_FLAGS":"","NOTES":"Page fetch failed",
                }
            else:
                page = parse_page(html, candidate.url); dim = validate(page["dimensions"], cfg)
                vals, raws = dim.values, dim.raw
                parsed_row = {
                    "INPUT_ID":record.input_id,"MAKE":record.make,"MODEL":record.model,"车辆类型":record.vehicle_type,
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
        if stop_after in {"fetch", "parse"}:
            return {"selected_count":len(selected),"result_count":len(raw_out),"fetched":crawler.fetched,"cache_hits":crawler.cache_hits}
        groups = group_dimensions(raw_out, cfg)
        if stop_after == "summarize":
            return {"dimension_group_count": len(groups)}
        credible_ids = {r["INPUT_ID"] for r in candidates_out if r["MATCH_STATUS"] in {"EXACT","LIKELY","MULTIPLE"}}
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
        for record in records:
            if record.input_id not in credible_ids:
                best = best_review_candidate(candidates_out, record.input_id, cfg["matching"]["review_threshold"])
                not_found.append({"INPUT_ID":record.input_id,"MAKE":record.make,"MODEL":record.model,"车辆类型":record.vehicle_type,
                    "SEARCH_TERMS_USED":f"{record.make} {record.model}","BEST_CANDIDATE":best.get("CANDIDATE_URL",""),"BEST_SCORE":best.get("MATCH_SCORE",""),"NOTES":"No credible candidate; no automatic fallback selected"})
                review.append({"INPUT_ID":record.input_id,"MAKE":record.make,"MODEL":record.model,"ISSUE_TYPE":"NOT_FOUND","CANDIDATE_URLS":"","RAW_VALUE":"","MATCH_SCORE":best.get("MATCH_SCORE",""),"ANOMALY_FLAGS":"","RECOMMENDED_ACTION":"Search catalog manually","NOTES":""})
        report = make_report(started, inputs, candidates_out, raw_out, groups, db.rows("errors"), crawler.fetched, crawler.cache_hits)
        report["not_found_count"] = len(not_found)
        report["review_count"] = len(review)
        save_report(report, output / "run_report.json")
        export_all(output, inputs, candidates_out, raw_out, groups, review, not_found, report)
        return report
    finally:
        crawler.close(); db.close()
