"""OpenAI API backend — the recommended LLM backend for production use."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from .protocol import ConversationState, LLMBackend, LLMResponse


@dataclass
class OpenAIBackend(LLMBackend):
    """Drives an LLM conversation via the OpenAI Chat Completions API.

    Parameters
    ----------
    api_key : str
        OpenAI API key (or compatible endpoint key).
    model : str
        Model identifier, e.g. "gpt-4o", "gpt-4-turbo".
    system_prompt : str
        Optional system message prepended to every conversation.
    base_url : str | None
        Override API base URL (for Azure, local proxies, etc.).
    """

    api_key: str
    model: str = "gpt-4o"
    system_prompt: str = ""
    base_url: str | None = None

    _messages: list[dict] = field(default_factory=list, repr=False)
    _round: int = field(default=0, repr=False)
    _client: object | None = field(default=None, repr=False)

    async def start_conversation(self) -> None:
        import openai

        kwargs: dict = {"api_key": self.api_key}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        self._client = openai.AsyncOpenAI(**kwargs)
        self._messages = []
        if self.system_prompt:
            self._messages.append({"role": "system", "content": self.system_prompt})
        self._round = 0

    async def send_message(self, message: str) -> None:
        self._messages.append({"role": "user", "content": message})

    async def wait_for_reply(self, *, timeout: int = 900) -> LLMResponse:
        import openai

        assert isinstance(self._client, openai.AsyncOpenAI)
        response = await asyncio.wait_for(
            self._client.chat.completions.create(
                model=self.model,
                messages=self._messages,
            ),
            timeout=timeout,
        )
        text = response.choices[0].message.content or ""
        self._messages.append({"role": "assistant", "content": text})
        self._round += 1
        return LLMResponse(
            text=text,
            round_number=self._round,
            is_complete=True,
            truncated=response.choices[0].finish_reason == "length",
        )

    async def get_state(self) -> ConversationState:
        return ConversationState(is_generating=False, is_ready=True)

    async def close(self) -> None:
        self._client = None
        self._messages = []
