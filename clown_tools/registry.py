from __future__ import annotations

from clown_tools.base import BaseTool
from clown_tools.file.read import ReadFileTool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def tool_names(self) -> list[str]:
        return sorted(self._tools)


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(ReadFileTool())
    return registry
