from __future__ import annotations

from pathlib import Path
import os

import pandas as pd


INPUT_COLUMNS = ["INPUT_ID","MAKE","MODEL","车辆类型","MAKE_NORMALIZED","MODEL_NORMALIZED","MODEL_COMPACT","MODEL_NUMBER_TOKENS","MODEL_WORD_TOKENS"]
CANDIDATE_COLUMNS = ["INPUT_ID","MAKE","MODEL","CANDIDATE_TITLE","CANDIDATE_URL","SOURCE_MAKE","SOURCE_MODEL","SOURCE_VERSION","SOURCE_YEAR","MODEL_SIMILARITY","MATCH_SCORE","MATCH_CONFIDENCE","MATCH_STATUS","MATCH_REASON","DISCOVERY_METHOD"]
RAW_COLUMNS = ["INPUT_ID","MAKE","MODEL","车辆类型","SOURCE_MAKE","SOURCE_MODEL","SOURCE_VERSION","YEAR","YEAR_START","YEAR_END","PAGE_TITLE","SOURCE_URL","L_RAW","W_RAW","H_RAW","UNIT_RAW","L-MM-MIN","L-MM-MAX","W-MM-MIN","W-MM-MAX","H-MM-MIN","H-MM-MAX","L-MM","W-MM","H-MM","WHEELBASE-MM","SEAT-HEIGHT-MM","GROUND-CLEARANCE-MM","WIDTH_SCOPE","HEIGHT_SCOPE","ACCESSORY_STATUS","DIMENSION_RAW","MODEL_SIMILARITY","MATCH_SCORE","MATCH_CONFIDENCE","MATCH_STATUS","PARSE_STATUS","CONFIDENCE","ANOMALY_FLAGS","NOTES","FETCHED_AT","CONTENT_HASH"]
SUMMARY_COLUMNS = ["DIMENSION_GROUP_ID","MAKE","MODEL","VERSION","YEARS","YEAR_START","YEAR_END","L-MM","W-MM","H-MM-MIN","H-MM-MAX","WIDTH_SCOPE","HEIGHT_SCOPE","ACCESSORY_STATUS","SOURCE_COUNT","SOURCE_URLS","CONFIDENCE","REVIEW_STATUS"]
REVIEW_COLUMNS = ["INPUT_ID","MAKE","MODEL","ISSUE_TYPE","CANDIDATE_URLS","RAW_VALUE","MATCH_SCORE","ANOMALY_FLAGS","RECOMMENDED_ACTION","NOTES"]
NOT_FOUND_COLUMNS = ["INPUT_ID","MAKE","MODEL","车辆类型","SEARCH_TERMS_USED","BEST_CANDIDATE","BEST_SCORE","NOTES"]
FITMENT_COLUMNS = ["INPUT_ID","MAKE","MODEL","车辆类型","DIMENSION_STATUS","L-MM","W-MM","H-MM","H-MM-MIN","H-MM-MAX","YEAR","MODEL_SIMILARITY","MATCH_SCORE","MATCH_CONFIDENCE","MATCH_STATUS","PARSE_STATUS","SOURCE_PAGE_COUNT","SOURCE_URL","NOTES"]


def build_fitment_rows(inputs: list[dict], raw: list[dict]) -> list[dict]:
    by_input: dict[str, list[dict]] = {}
    for row in raw:
        by_input.setdefault(row["INPUT_ID"], []).append(row)
    result = []
    confidence_rank = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "": 0}
    for item in inputs:
        sources = by_input.get(item["INPUT_ID"], [])
        if sources:
            def rank(row: dict) -> tuple:
                completeness = sum(row.get(key) not in (None, "") for key in ("L-MM", "W-MM", "H-MM"))
                return (completeness, row.get("PARSE_STATUS") == "COMPLETE", confidence_rank.get(row.get("MATCH_CONFIDENCE", ""), 0), float(row.get("MATCH_SCORE") or 0))
            best = max(sources, key=rank)
            present = sum(best.get(key) not in (None, "") for key in ("L-MM", "W-MM", "H-MM"))
            status = "FOUND_COMPLETE" if present == 3 else "FOUND_PARTIAL" if present else "SOURCE_NO_DIMENSION"
        else:
            best, status = {}, "NOT_FOUND"
        result.append({
            "INPUT_ID": item["INPUT_ID"], "MAKE": item["MAKE"], "MODEL": item["MODEL"], "车辆类型": item.get("车辆类型", ""),
            "DIMENSION_STATUS": status, "L-MM": best.get("L-MM"), "W-MM": best.get("W-MM"), "H-MM": best.get("H-MM"),
            "H-MM-MIN": best.get("H-MM-MIN"), "H-MM-MAX": best.get("H-MM-MAX"), "YEAR": best.get("YEAR", ""),
            "MODEL_SIMILARITY": best.get("MODEL_SIMILARITY", ""), "MATCH_SCORE": best.get("MATCH_SCORE", ""),
            "MATCH_CONFIDENCE": best.get("MATCH_CONFIDENCE", ""), "MATCH_STATUS": best.get("MATCH_STATUS", ""),
            "PARSE_STATUS": best.get("PARSE_STATUS", ""), "SOURCE_PAGE_COUNT": len(sources), "SOURCE_URL": best.get("SOURCE_URL", ""),
            "NOTES": "Best available source; see DIMENSIONS_RAW for all years." if sources else "No automatically trusted source page.",
        })
    return result


def export_all(output: Path, inputs: list[dict], candidates: list[dict], raw: list[dict], groups: list[dict], review: list[dict], not_found: list[dict], report: dict) -> None:
    output.mkdir(parents=True, exist_ok=True)
    datasets = {
        "INPUT_NORMALIZED": (inputs, INPUT_COLUMNS, "input_normalized.csv"),
        "FITMENT_DIMENSIONS": (build_fitment_rows(inputs, raw), FITMENT_COLUMNS, "fitment_dimensions.csv"),
        "CANDIDATE_PAGES": (candidates, CANDIDATE_COLUMNS, "candidate_pages.csv"),
        "DIMENSIONS_RAW": (raw, RAW_COLUMNS, "dimensions_raw.csv"),
        "DIMENSIONS_SUMMARY": (groups, SUMMARY_COLUMNS, "dimensions_summary.csv"),
        "REVIEW_NEEDED": (review, REVIEW_COLUMNS, "review_needed.csv"),
        "NOT_FOUND": (not_found, NOT_FOUND_COLUMNS, "not_found.csv"),
    }
    frames = {}
    for sheet, (rows, columns, filename) in datasets.items():
        frames[sheet] = pd.DataFrame(rows).reindex(columns=columns)
        frames[sheet].to_csv(output / filename, index=False, encoding="utf-8-sig")
    frames["RUN_REPORT"] = pd.DataFrame([report])
    if os.environ.get("MOTO_EXPORT_XLSX") != "1":
        return
    from openpyxl import load_workbook
    excel = output / "motorcycle_dimensions.xlsx"
    with pd.ExcelWriter(excel, engine="openpyxl") as writer:
        for sheet, frame in frames.items():
            frame.to_excel(writer, sheet_name=sheet, index=False)
    workbook = load_workbook(excel)
    for sheet in workbook:
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions
    workbook.save(excel)
