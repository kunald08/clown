from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from clown_agent.session_state import ChatMessage


class PlannedToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, object] = Field(default_factory=dict)


class ProviderResponse(BaseModel):
    text: str
    tool_calls: list[PlannedToolCall] = Field(default_factory=list)


class BaseProvider(ABC):
    @abstractmethod
    def generate(
        self,
        messages: list[ChatMessage],
        user_message: str,
    ) -> ProviderResponse:
        raise NotImplementedError
