import csv

from moto_dimension_crawler.progress import ProgressFiles, _DurableCsv


def test_progress_files_are_created_with_headers_and_durable_rows(tmp_path):
    progress = ProgressFiles(tmp_path)
    progress.match.write({
        "POSITION": 1, "TOTAL": 2, "INPUT_ID": "000001", "MAKE": "BMW",
        "MODEL": "C evolution", "STATUS": "OK", "MATCHES": 1,
    })

    # The row is visible to a separate reader before the writer is closed.
    with (tmp_path / "match_progress.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["STATUS"] == "OK"
    assert rows[0]["MATCHES"] == "1"
    assert (tmp_path / "fetch_progress.csv").stat().st_size > 0
    assert (tmp_path / "parse_progress.csv").stat().st_size > 0

    progress.close()


def test_progress_csv_flushes_every_row_but_batches_physical_sync(tmp_path, monkeypatch):
    sync_calls = []
    monkeypatch.setattr("moto_dimension_crawler.progress.os.fsync", lambda fileno: sync_calls.append(fileno))
    progress = _DurableCsv(tmp_path / "progress.csv", ["VALUE"], sync_every=3, sync_interval=60)
    assert len(sync_calls) == 1  # header

    progress.write({"VALUE": 1})
    with (tmp_path / "progress.csv").open(encoding="utf-8-sig", newline="") as handle:
        assert list(csv.DictReader(handle))[0]["VALUE"] == "1"
    assert len(sync_calls) == 1

    progress.write({"VALUE": 2})
    progress.write({"VALUE": 3})
    assert len(sync_calls) == 2
    progress.close()
