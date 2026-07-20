import threading

import httpx

from moto_dimension_crawler.cache import PageCache
from moto_dimension_crawler.crawler import Crawler


class _FakeDB:
    def __init__(self):
        self.errors = []

    def cached(self, url):
        return None

    def save_cache(self, meta):
        pass

    def error(self, phase, message, created_at, input_id="", url=""):
        self.errors.append((phase, message, url))


class _AllowAll:
    def allowed(self, url):
        return True


class _ResetThenSuccessClient:
    def __init__(self):
        self.calls = 0

    def get(self, url):
        self.calls += 1
        if self.calls == 1:
            raise httpx.ReadError("connection reset")
        return httpx.Response(200, content=b"<html><title>OK</title></html>")


def _crawler(tmp_path):
    crawler = Crawler.__new__(Crawler)
    crawler.cfg = {
        "request_delay_min_seconds": 0,
        "request_delay_max_seconds": 0,
        "max_retries": 1,
        "retry_delays_seconds": [0],
        "failure_cache_seconds": 60,
        "permanent_failure_cache_seconds": 60,
    }
    crawler.cache = PageCache(tmp_path)
    crawler.db = _FakeDB()
    crawler.client = _ResetThenSuccessClient()
    crawler.robots = {"example.test": _AllowAll()}
    crawler.cache_hits = crawler.failure_cache_hits = crawler.fetched = 0
    crawler._counter_lock = threading.Lock()
    crawler._db_lock = threading.Lock()
    crawler._rate_lock = threading.Lock()
    crawler._next_request_at = {}
    crawler._host_locks = {}
    return crawler


def test_read_error_is_retried_instead_of_escaping_worker(tmp_path):
    crawler = _crawler(tmp_path)

    html, meta, from_cache = crawler.fetch("https://example.test/model")

    assert "<title>OK</title>" in html
    assert meta["status_code"] == 200
    assert from_cache is False
    assert crawler.client.calls == 2
    assert crawler.fetched == 1
