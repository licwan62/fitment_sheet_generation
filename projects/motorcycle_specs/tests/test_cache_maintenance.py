import json

from moto_dimension_crawler.cache import PageCache
from moto_dimension_crawler.cache_maintenance import reconcile_cache
from moto_dimension_crawler.database import StateDB


def test_reconcile_registers_page_files_and_refreshes_cache_path(tmp_path):
    cache = PageCache(tmp_path / "cache")
    metadata = cache.write(
        "https://example.test/model", b"<html><title>Model</title></html>", 200, "utf-8",
    )
    metadata_path = cache.paths(metadata["url"])[1]
    stored = json.loads(metadata_path.read_text(encoding="utf-8"))
    stored["cache_path"] = "D:/old/cache.html"
    metadata_path.write_text(json.dumps(stored), encoding="utf-8")
    checkpoint = tmp_path / "state.sqlite3"
    StateDB(checkpoint).close()

    result = reconcile_cache(tmp_path / "cache", checkpoint)

    db = StateDB(checkpoint)
    row = db.cached(metadata["url"])
    db.close()
    assert result["valid_pairs"] == result["registered"] == result["path_updates"] == 1
    assert row["cache_path"] == str(cache.paths(metadata["url"])[0].resolve())
