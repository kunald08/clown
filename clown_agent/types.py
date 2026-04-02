from __future__ import annotations

from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    final_text: str
    tool_events: list[str] = Field(default_factory=list)
