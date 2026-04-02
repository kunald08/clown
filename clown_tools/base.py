from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class ToolResult(BaseModel):
    success: bool
    output: str


class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError
