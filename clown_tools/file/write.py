from __future__ import annotations

from clown_tools.base import BaseTool, ToolResult, missing_argument
from clown_tools.file.common import resolve_input_path


class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Write utf-8 text to a file on disk."

    def run(self, **kwargs: object) -> ToolResult:
        resolved = resolve_input_path(kwargs.get("path"))
        if isinstance(resolved, ToolResult):
            return resolved

        content = kwargs.get("content")
        if not isinstance(content, str):
            return missing_argument("content")

        path = resolved
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return ToolResult(success=True, output=f"Wrote {len(content)} bytes to {path}")
