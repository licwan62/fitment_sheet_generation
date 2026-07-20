from __future__ import annotations

import logging
import random
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

import httpx

from .cache import PageCache
from .database import StateDB
from .robots import RobotsPolicy
from .utils import utc_now


class Crawler:
    def __init__(self, cfg: dict, cache: PageCache, db: StateDB):
        site, crawl = cfg["site"], cfg["crawler"]
        self.cfg, self.cache, self.db = crawl, cache, db
        timeout = httpx.Timeout(crawl["read_timeout_seconds"], connect=crawl["connect_timeout_seconds"])
        self.client = httpx.Client(headers={"User-Agent": site["user_agent"]}, timeout=timeout, follow_redirects=True)
        configured_sites = cfg.get("sources") or [site]
        self.robots: dict[str, RobotsPolicy] = {}
        for configured in configured_sites:
            host = urlparse(configured["base_url"]).netloc.casefold()
            policy = RobotsPolicy(
                configured["base_url"], site["user_agent"],
                configured.get("obey_robots_txt", site.get("obey_robots_txt", True)),
            )
            policy.load(self.client)
            self.robots[host] = policy
        self.cache_hits = self.failure_cache_hits = self.fetched = 0
        self._counter_lock = threading.Lock()
        self._db_lock = threading.Lock()
        self._rate_lock = threading.Lock()
        self._next_request_at: dict[str, float] = {}
        self._host_locks: dict[str, threading.Lock] = {}

    def close(self) -> None:
        self.client.close()

    def _increment(self, name: str) -> None:
        with self._counter_lock:
            setattr(self, name, getattr(self, name) + 1)

    def _wait_for_request_slot(self, url: str) -> None:
        """Reserve a request start time while preserving a per-host crawl delay."""
        host = urlparse(url).netloc.casefold()
        low = float(self.cfg["request_delay_min_seconds"])
        high = float(self.cfg["request_delay_max_seconds"])
        with self._rate_lock:
            now = time.monotonic()
            scheduled = max(now, self._next_request_at.get(host, now))
            self._next_request_at[host] = scheduled + random.uniform(low, high)
        wait = scheduled - time.monotonic()
        if wait > 0:
            time.sleep(wait)

    def _host_lock(self, url: str) -> threading.Lock:
        """Keep requests to one host sequential while allowing cross-host concurrency."""
        host = urlparse(url).netloc.casefold()
        with self._rate_lock:
            return self._host_locks.setdefault(host, threading.Lock())

    def fetch(self, url: str, force: bool = False) -> tuple[str | None, dict | None, bool]:
        if not force and self.cache.valid(url):
            self._increment("cache_hits")
            with self._db_lock:
                meta = self.db.cached(url)
            return self.cache.read(url), meta, True
        if not force:
            failure = self.cache.read_failure(url)
            if failure is not None:
                self._increment("failure_cache_hits")
                return None, {**failure, "failure_cached": True}, True
        policy = self.robots.get(urlparse(url).netloc.casefold())
        if policy is None or not policy.allowed(url):
            with self._db_lock:
                self.db.error("FETCH", "Blocked by robots.txt", utc_now(), url=url)
            return None, None, False
        delays = self.cfg.get("retry_delays_seconds", [5, 15, 45])
        last = ""
        status_code = None
        for attempt in range(self.cfg.get("max_retries", 3) + 1):
            if attempt:
                time.sleep(delays[min(attempt - 1, len(delays) - 1)])
            try:
                with self._host_lock(url):
                    self._wait_for_request_slot(url)
                    response = self.client.get(url)
                status_code = response.status_code
                if response.status_code == 200:
                    meta = self.cache.write(url, response.content, response.status_code, response.encoding or "utf-8")
                    with self._db_lock:
                        self.db.save_cache(meta)
                    self._increment("fetched")
                    return response.text, meta, False
                last = f"HTTP {response.status_code}"
                if response.status_code not in {429, 500, 502, 503, 504}:
                    break
            except httpx.TransportError as exc:
                # Includes timeouts, connect failures, connection resets while
                # reading, and malformed/closed remote protocol streams.
                last = str(exc)
        permanent = status_code is not None and status_code not in {408, 429, 500, 502, 503, 504}
        cache_seconds = int(self.cfg.get(
            "permanent_failure_cache_seconds" if permanent else "failure_cache_seconds",
            604800 if permanent else 21600,
        ))
        failure = self.cache.write_failure(url, last or "Fetch failed", status_code, cache_seconds)
        with self._db_lock:
            self.db.error("FETCH", last or "Fetch failed", utc_now(), url=url)
        logging.getLogger(__name__).error("Fetch failed %s: %s", url, last)
        return None, failure, False
