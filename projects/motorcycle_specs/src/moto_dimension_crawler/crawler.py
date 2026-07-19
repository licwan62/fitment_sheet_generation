from __future__ import annotations

import logging
import random
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
        self.cache_hits = self.fetched = 0

    def close(self) -> None:
        self.client.close()

    def fetch(self, url: str, force: bool = False) -> tuple[str | None, dict | None, bool]:
        if not force and self.cache.valid(url):
            self.cache_hits += 1
            return self.cache.read(url), self.db.cached(url), True
        policy = self.robots.get(urlparse(url).netloc.casefold())
        if policy is None or not policy.allowed(url):
            self.db.error("FETCH", "Blocked by robots.txt", utc_now(), url=url)
            return None, None, False
        delays = self.cfg.get("retry_delays_seconds", [5, 15, 45])
        last = ""
        for attempt in range(self.cfg.get("max_retries", 3) + 1):
            if attempt:
                time.sleep(delays[min(attempt - 1, len(delays) - 1)])
            time.sleep(random.uniform(self.cfg["request_delay_min_seconds"], self.cfg["request_delay_max_seconds"]))
            try:
                response = self.client.get(url)
                if response.status_code == 200:
                    meta = self.cache.write(url, response.content, response.status_code, response.encoding or "utf-8")
                    self.db.save_cache(meta)
                    self.fetched += 1
                    return response.text, meta, False
                last = f"HTTP {response.status_code}"
                if response.status_code not in {429, 500, 502, 503, 504}:
                    break
            except (httpx.TimeoutException, httpx.ConnectError) as exc:
                last = str(exc)
        self.db.error("FETCH", last or "Fetch failed", utc_now(), url=url)
        logging.getLogger(__name__).error("Fetch failed %s: %s", url, last)
        return None, None, False
