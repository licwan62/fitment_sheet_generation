from __future__ import annotations

import json
from pathlib import Path

from .utils import utc_now


FIELDS = ["started_at","finished_at","input_count","processed_count","candidate_page_count","fetched_page_count","cache_hit_count","exact_match_count","likely_match_count","review_count","not_found_count","parsed_complete_count","parsed_partial_count","parse_failed_count","dimension_group_count","error_count"]


def make_report(started_at: str, inputs: list[dict], candidates: list[dict], raw: list[dict], groups: list[dict], errors: list[dict], fetched: int = 0, cache_hits: int = 0) -> dict:
    return {
        "started_at": started_at, "finished_at": utc_now(), "input_count": len(inputs), "processed_count": len(inputs),
        "candidate_page_count": len(candidates), "fetched_page_count": fetched, "cache_hit_count": cache_hits,
        "exact_match_count": sum(x.get("MATCH_STATUS") == "EXACT" for x in candidates),
        "likely_match_count": sum(x.get("MATCH_STATUS") == "LIKELY" for x in candidates),
        "review_count": sum(x.get("MATCH_STATUS") in {"REVIEW", "MULTIPLE"} for x in candidates),
        "not_found_count": len({x["INPUT_ID"] for x in inputs} - {x["INPUT_ID"] for x in candidates if x.get("MATCH_SCORE", 0) >= 70}),
        "parsed_complete_count": sum(x.get("PARSE_STATUS") == "COMPLETE" for x in raw),
        "parsed_partial_count": sum(x.get("PARSE_STATUS") == "PARTIAL" for x in raw),
        "parse_failed_count": sum(x.get("PARSE_STATUS") in {"PARSE_FAILED", "FETCH_FAILED"} for x in raw),
        "dimension_group_count": len(groups), "error_count": len(errors),
    }


def save_report(report: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
