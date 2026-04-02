from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from clown_agent.session_state import ChatMessage


class ProviderResponse(BaseModel):
    text: str
    tool_calls: list[str] = Field(default_factory=list)


class BaseProvider(ABC):
    @abstractmethod
    def generate(
        self,
        messages: list[ChatMessage],
        user_message: str,
    ) -> ProviderResponse:
        raise NotImplementedError
