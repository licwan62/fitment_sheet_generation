"""Abstract interface for LLM backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class LLMResponse:
    """Unified response from any LLM backend."""

    text: str
    round_number: int
    is_complete: bool = False
    truncated: bool = False
    metadata: dict = field(default_factory=dict)


@dataclass
class ConversationState:
    """Current state of an LLM conversation."""

    is_generating: bool = False
    is_ready: bool = True
    error: str | None = None


class LLMBackend(ABC):
    """Abstract interface for LLM interaction.

    Each shard gets its own backend instance (its own conversation context).
    """

    @abstractmethod
    async def start_conversation(self) -> None:
        """Start a new conversation (new chat / new thread)."""

    @abstractmethod
    async def send_message(self, message: str) -> None:
        """Send a message to the LLM."""

    @abstractmethod
    async def wait_for_reply(self, *, timeout: int = 900) -> LLMResponse:
        """Wait for the LLM to finish and return the reply."""

    @abstractmethod
    async def get_state(self) -> ConversationState:
        """Get current conversation state."""

    @abstractmethod
    async def close(self) -> None:
        """Clean up resources."""
