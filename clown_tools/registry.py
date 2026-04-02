from __future__ import annotations

from clown_tools.base import BaseTool
from clown_tools.file.edit import EditFileTool
from clown_tools.file.glob_search import GlobSearchTool
from clown_tools.file.grep_search import GrepSearchTool
from clown_tools.file.read import ReadFileTool
from clown_tools.file.write import WriteFileTool


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
    for tool in (
        ReadFileTool(),
        WriteFileTool(),
        EditFileTool(),
        GlobSearchTool(),
        GrepSearchTool(),
    ):
        registry.register(tool)
    return registry
