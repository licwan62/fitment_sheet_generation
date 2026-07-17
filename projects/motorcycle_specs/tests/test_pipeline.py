from moto_dimension_crawler.pipeline import best_review_candidate


def test_best_candidate_requires_plausible_primary_model_token():
    rows = [{"INPUT_ID":"003072","MATCH_STATUS":"REVIEW","MATCH_SCORE":78,"MATCH_REASON":"primary_alpha=no","CANDIDATE_URL":"wrong"}]
    assert best_review_candidate(rows, "003072", 70) == {}
