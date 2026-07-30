from __future__ import annotations

from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import httpx


class RobotsPolicy:
    def __init__(self, base_url: str, user_agent: str, enabled: bool = True):
        self.user_agent, self.enabled = user_agent, enabled
        self.parser = RobotFileParser()
        self.parser.set_url(urljoin(base_url, "/robots.txt"))
        self.loaded = False

    def load(self, client: httpx.Client) -> None:
        if not self.enabled:
            return
        try:
            response = client.get(self.parser.url)
            if response.status_code == 200:
                self.parser.parse(response.text.splitlines())
                self.loaded = True
        except httpx.HTTPError:
            self.loaded = False

    def allowed(self, url: str) -> bool:
        return not self.enabled or not self.loaded or self.parser.can_fetch(self.user_agent, url)

