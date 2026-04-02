from __future__ import annotations

from clown_tools.base import BaseTool, ToolResult
from clown_tools.file.common import ensure_text_file, read_utf8_text, resolve_input_path


class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Read a text file from disk."

    def run(self, **kwargs: object) -> ToolResult:
        resolved = resolve_input_path(kwargs.get("path"))
        if isinstance(resolved, ToolResult):
            return resolved

        path = resolved
        error = ensure_text_file(path)
        if error:
            return error

        content = read_utf8_text(path)
        if isinstance(content, ToolResult):
            return content

        return ToolResult(success=True, output=content)
