from __future__ import annotations

from pathlib import Path

from clown_tools.base import BaseTool, ToolResult


class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Read a text file from disk."

    def run(self, **kwargs: object) -> ToolResult:
        raw_path = kwargs.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            return ToolResult(success=False, output="Missing 'path' argument.")

        path = Path(raw_path).expanduser()
        if not path.exists():
            return ToolResult(success=False, output=f"File not found: {path}")
        if path.is_dir():
            return ToolResult(success=False, output=f"Path is a directory: {path}")

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return ToolResult(success=False, output=f"File is not utf-8 text: {path}")

        return ToolResult(success=True, output=content)
