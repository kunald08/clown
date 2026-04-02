from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class ToolResult(BaseModel):
    success: bool
    output: str
    requires_approval: bool = False
    approval_reason: str | None = None
    preview: str | None = None


class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError


def missing_argument(name: str) -> ToolResult:
    return ToolResult(success=False, output=f"Missing {name!r} argument.")
