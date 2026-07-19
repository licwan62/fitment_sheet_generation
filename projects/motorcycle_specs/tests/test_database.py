from moto_dimension_crawler.database import StateDB, clear_checkpoint


def test_clear_checkpoint_removes_sqlite_files_only(tmp_path):
    checkpoint = tmp_path / "state.sqlite3"
    sidecars = [tmp_path / "state.sqlite3-wal", tmp_path / "state.sqlite3-shm"]
    preserved = tmp_path / "cached-page.html"
    for path in [checkpoint, *sidecars, preserved]:
        path.write_text("test", encoding="utf-8")

    removed = clear_checkpoint(checkpoint)

    assert removed == [checkpoint, *sidecars]
    assert not checkpoint.exists()
    assert all(not path.exists() for path in sidecars)
    assert preserved.exists()


def test_clear_checkpoint_is_idempotent(tmp_path):
    checkpoint = tmp_path / "state.sqlite3"

    assert clear_checkpoint(checkpoint) == []


def test_clear_input_candidates_replaces_stale_match_rows(tmp_path):
    db = StateDB(tmp_path / "state.sqlite3")
    db.upsert_json("candidate_pages", {"input_id":"1", "url":"old"}, {"INPUT_ID":"1"})
    db.upsert_json("candidate_pages", {"input_id":"2", "url":"kept"}, {"INPUT_ID":"2"})
    db.clear_input_candidates("1")
    assert {(row["input_id"], row["url"]) for row in db.rows("candidate_pages")} == {("2", "kept")}
    db.close()
