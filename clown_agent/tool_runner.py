from __future__ import annotations

from clown_tools.base import ToolResult
from clown_tools.registry import ToolRegistry


class ToolRunner:
    def __init__(self, registry: ToolRegistry) -> None:
        self._registry = registry

    def run_tool(self, tool_name: str, arguments: dict[str, object]) -> ToolResult:
        tool = self._registry.get(tool_name)
        if tool is None:
            return ToolResult(success=False, output=f"Unknown tool: {tool_name}")
        return tool.run(**arguments)
