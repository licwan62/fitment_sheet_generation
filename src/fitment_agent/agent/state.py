"""Shard processing state machine."""

from __future__ import annotations

from enum import Enum, auto


class ShardState(Enum):
    """States a single shard passes through during processing."""

    INIT = auto()
    SENDING_INITIAL = auto()
    WAITING_REPLY = auto()
    EVALUATING_REPLY = auto()

    # Action states (send a message, then go back to WAITING_REPLY)
    SENDING_CONTINUE = auto()
    SENDING_FULL_TABLE_REQUEST = auto()
    SENDING_FIX_REQUEST = auto()
    SENDING_MISSING_SIGNALS = auto()

    # Terminal states
    COMPLETE = auto()
    REPEATED = auto()
    DEVIATED = auto()
    MAX_ROUNDS = auto()
    ERROR = auto()

    @property
    def is_terminal(self) -> bool:
        return self in {
            self.COMPLETE,
            self.REPEATED,
            self.DEVIATED,
            self.MAX_ROUNDS,
            self.ERROR,
        }

    @property
    def is_sending(self) -> bool:
        return self in {
            self.SENDING_INITIAL,
            self.SENDING_CONTINUE,
            self.SENDING_FULL_TABLE_REQUEST,
            self.SENDING_FIX_REQUEST,
            self.SENDING_MISSING_SIGNALS,
        }

    def to_status_string(self) -> str:
        """Human-readable status for logs."""
        return {
            self.COMPLETE: "成功",
            self.REPEATED: "重复终止",
            self.DEVIATED: "偏离终止",
            self.MAX_ROUNDS: "次数上限终止",
            self.ERROR: "错误终止",
        }.get(self, "进行中")
