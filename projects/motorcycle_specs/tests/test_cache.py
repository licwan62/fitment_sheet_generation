import time

from moto_dimension_crawler.cache import PageCache


def test_failure_cache_observes_cooldown_and_can_be_cleared(tmp_path):
    cache = PageCache(tmp_path)
    cached = cache.write_failure("https://example.test/page", "HTTP 503", 503, 60)

    assert cached["retry_after"] > time.time()
    assert cache.read_failure("https://example.test/page")["status_code"] == 503

    cache.clear_failure("https://example.test/page")
    assert cache.read_failure("https://example.test/page") is None


def test_expired_failure_cache_is_ignored(tmp_path):
    cache = PageCache(tmp_path)
    cache.write_failure("https://example.test/page", "timeout", None, 0)

    assert cache.read_failure("https://example.test/page") is None
