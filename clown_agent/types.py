from __future__ import annotations

from pydantic import BaseModel, Field


class PendingApproval(BaseModel):
    tool_name: str
    arguments: dict[str, object]
    reason: str


class AgentResponse(BaseModel):
    final_text: str
    tool_events: list[str] = Field(default_factory=list)
    pending_approval: PendingApproval | None = None
