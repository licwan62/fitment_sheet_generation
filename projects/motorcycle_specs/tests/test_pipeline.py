import logging

from moto_dimension_crawler.models import Candidate
from moto_dimension_crawler.pipeline import (
    _TerminalNoiseFilter,
    best_review_candidate,
    candidate_from_checkpoint,
    checkpoint_match_rows,
    checkpoint_ok_rows,
    load_resume_snapshot,
    log_match_summary,
    merge_resumed_rows,
    preferred_source_rows,
    setup_logging,
)
from moto_dimension_crawler.qwen_aliases import GeneratedAliases, GeneratedDimensions
from moto_dimension_crawler.models import InputRecord
from moto_dimension_crawler.normalizer import compact_name, normalize_name, number_tokens, word_tokens


def test_best_candidate_requires_plausible_primary_model_token():
    rows = [{"INPUT_ID":"003072","MATCH_STATUS":"REVIEW","MATCH_SCORE":78,"MATCH_REASON":"primary_alpha=no","CANDIDATE_URL":"wrong"}]
    assert best_review_candidate(rows, "003072", 70) == {}


def test_preferred_source_uses_more_complete_fallback_then_priority_for_ties():
    common = {"INPUT_ID": "1", "YEAR": "2025", "MATCH_SCORE": 100, "MATCH_CONFIDENCE": "HIGH"}
    primary = dict(common, **{"DATA_SOURCE": "motorcyclespecs", "SOURCE_PRIORITY": 1, "SOURCE_URL": "primary", "L-MM": 2200, "W-MM": None, "H-MM": None, "PARSE_STATUS": "PARTIAL"})
    bikedekho = dict(common, **{"DATA_SOURCE": "bikedekho", "SOURCE_PRIORITY": 2, "SOURCE_URL": "bikedekho", "L-MM": 2200, "W-MM": 835, "H-MM": 1500, "PARSE_STATUS": "COMPLETE"})
    bikez = dict(common, **{"DATA_SOURCE": "bikez", "SOURCE_PRIORITY": 3, "SOURCE_URL": "bikez", "L-MM": 2200, "W-MM": 835, "H-MM": 1500, "PARSE_STATUS": "COMPLETE"})

    assert preferred_source_rows([primary, bikez, bikedekho])[0]["DATA_SOURCE"] == "bikedekho"


def test_resume_replaces_retried_miss_and_retains_untouched_ok_rows(tmp_path):
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    (log_dir / "run_details.jsonl").write_text(
        '\n'.join([
            '{"record_type":"CANDIDATE_DIAGNOSTIC","payload":{"INPUT_ID":"ok-1","MATCH_STATUS":"EXACT","CANDIDATE_URL":"kept"}}',
            '{"record_type":"CANDIDATE_DIAGNOSTIC","payload":{"INPUT_ID":"miss-1","MATCH_STATUS":"REVIEW","CANDIDATE_URL":"old-miss"}}',
        ]),
        encoding="utf-8",
    )
    snapshot = load_resume_snapshot(tmp_path)
    merged = merge_resumed_rows(
        snapshot["CANDIDATE_DIAGNOSTIC"],
        [{"INPUT_ID": "miss-1", "MATCH_STATUS": "EXACT", "CANDIDATE_URL": "new-hit"}],
        {"miss-1"},
    )

    assert {(row["INPUT_ID"], row["CANDIDATE_URL"]) for row in merged} == {
        ("ok-1", "kept"),
        ("miss-1", "new-hit"),
    }


def test_checkpoint_ok_requires_all_trusted_candidates_to_have_parsed_dimensions():
    record = InputRecord(
        "000290", "Honda", "CB190R", "", normalize_name("Honda"), normalize_name("CB190R"),
        compact_name("CB190R"), number_tokens("CB190R"), word_tokens("CB190R"),
    )
    candidates = [{
        "input_id":"000290", "url":"https://example/one", "INPUT_ID":"000290",
        "MAKE":"Honda", "MODEL":"CB190R", "CANDIDATE_URL":"https://example/one",
        "MATCH_STATUS":"EXACT",
    }]
    complete = [{
        "input_id":"000290", "url":"https://example/one", "INPUT_ID":"000290",
        "MAKE":"Honda", "MODEL":"CB190R", "SOURCE_URL":"https://example/one",
        "PARSE_STATUS":"COMPLETE", "L-MM":2029,
    }]
    restored_candidates, restored_dimensions = checkpoint_ok_rows(record, candidates, complete)
    assert len(restored_candidates) == len(restored_dimensions) == 1
    assert "input_id" not in restored_candidates[0]
    assert "url" not in restored_dimensions[0]

    incomplete = [dict(complete[0], PARSE_STATUS="FETCH_FAILED")]
    assert checkpoint_ok_rows(record, candidates, incomplete) == ([], [])


def test_checkpoint_ok_rejects_rows_when_same_input_id_now_has_another_model():
    record = InputRecord(
        "000290", "Honda", "CB190R", "", normalize_name("Honda"), normalize_name("CB190R"),
        compact_name("CB190R"), number_tokens("CB190R"), word_tokens("CB190R"),
    )
    candidates = [{
        "INPUT_ID":"000290", "MAKE":"Honda", "MODEL":"CBR1000RR",
        "CANDIDATE_URL":"https://example/wrong", "MATCH_STATUS":"EXACT",
    }]
    assert checkpoint_ok_rows(record, candidates, []) == ([], [])


def test_checkpoint_match_can_skip_matching_while_fetch_is_still_pending():
    record = InputRecord(
        "000290", "Honda", "CB190R", "", normalize_name("Honda"), normalize_name("CB190R"),
        compact_name("CB190R"), number_tokens("CB190R"), word_tokens("CB190R"),
    )
    rows = [{
        "input_id":"000290", "url":"https://example/one", "INPUT_ID":"000290",
        "MAKE":"Honda", "MODEL":"CB190R", "CANDIDATE_TITLE":"CB190R",
        "CANDIDATE_URL":"https://example/one", "DATA_SOURCE":"bikez", "SOURCE_PRIORITY":4,
        "MATCH_SCORE":100, "MATCH_STATUS":"EXACT", "MATCH_REASON":"checkpoint",
    }]
    restored = checkpoint_match_rows(record, rows)
    assert len(restored) == 1
    candidate = candidate_from_checkpoint(restored[0])
    assert candidate.status == "EXACT"
    assert candidate.url == "https://example/one"
    assert candidate.source_name == "bikez"


def test_http_request_info_logs_are_suppressed_only_by_terminal_filter():
    setup_logging("INFO")
    noise_filter = _TerminalNoiseFilter()
    info = logging.LogRecord("httpx", logging.INFO, "", 0, "HTTP Request", (), None)
    warning = logging.LogRecord("httpx", logging.WARNING, "", 0, "HTTP warning", (), None)
    pipeline_info = logging.LogRecord("moto_dimension_crawler.pipeline", logging.INFO, "", 0, "summary", (), None)
    assert not noise_filter.filter(info)
    assert noise_filter.filter(warning)
    assert noise_filter.filter(pipeline_info)
    assert logging.getLogger("httpx").getEffectiveLevel() == logging.INFO


def test_match_summary_reports_credible_count_and_best_title(caplog):
    record = type("Record", (), {"make": "BMW", "model": "K1600GT Sport"})()
    ranked = [
        Candidate("1", "K 1600 GT Sport", "one", score=98, status="EXACT"),
        Candidate("1", "K 1600 GT Sport 2018", "two", score=96, status="EXACT"),
        Candidate("1", "K 1600 GT", "three", score=72, status="REVIEW"),
    ]
    with caplog.at_level(logging.INFO, logger="moto_dimension_crawler.pipeline"):
        log_match_summary(record, ranked, position=100, total=4000)
    assert "[100/4000] OK   BMW / K1600GT Sport -> K 1600 GT Sport | matches=2" in caplog.text


def test_match_summary_combines_ai_failure_without_extra_lines(caplog):
    record = type("Record", (), {"make": "Honda", "model": "CR125M"})()
    ranked = [Candidate("1", "CR 125", "one", score=72, status="REVIEW")]
    generated = GeneratedAliases([], [], "CACHED_API_ERROR")
    with caplog.at_level(logging.INFO, logger="moto_dimension_crawler.pipeline"):
        log_match_summary(record, ranked, generated, 101, 4000)
    assert "[101/4000] MISS Honda / CR125M | closest=CR 125 | ai=api-error(cached)" in caplog.text


def test_match_summary_shows_ai_alias_basis_compactly(caplog):
    record = type("Record", (), {"make": "BMW", "model": "F650 Enduro"})()
    ranked = [Candidate("1", "F 650 Funduro", "one", score=95, status="EXACT")]
    generated = GeneratedAliases(
        [], ["F 650 Funduro"], "SUCCESS", "MATCH", "F 650 Funduro", [],
        "MEDIUM", "MARKET_ALIAS", "Alternate market name.",
    )
    with caplog.at_level(logging.INFO, logger="moto_dimension_crawler.pipeline"):
        log_match_summary(record, ranked, generated)
    assert "ai=api:match(market_alias,medium)" in caplog.text


def test_match_summary_marks_dimension_inference_instead_of_miss(caplog):
    record = type("Record", (), {"make": "Honda", "model": "CB190R"})()
    inferred = GeneratedDimensions(
        {"length_mm": 2029, "width_mm": 739, "height_mm": 1041},
        "CACHED_SUCCESS", "INFER", "LOW", "Unverified estimate.",
    )
    with caplog.at_level(logging.INFO, logger="moto_dimension_crawler.pipeline"):
        log_match_summary(record, [], GeneratedAliases([], [], "CACHED_SUCCESS", "NO_MATCH"),
                          290, 3170, inferred)
    assert "[290/3170] INFER Honda / CB190R" in caplog.text
    assert "ai=cache:dimension-inference" in caplog.text
