from __future__ import annotations

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class SessionState(BaseModel):
    messages: list[ChatMessage] = Field(default_factory=list)
