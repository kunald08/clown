from __future__ import annotations

from pathlib import Path

from clown_tools.base import BaseTool, ToolResult


class GlobSearchTool(BaseTool):
    name = "glob_search"
    description = "Find files matching a glob pattern."

    def run(self, **kwargs: object) -> ToolResult:
        pattern = kwargs.get("pattern")
        root = kwargs.get("root", ".")

        if not isinstance(pattern, str) or not pattern.strip():
            return ToolResult(success=False, output="Missing 'pattern' argument.")
        if not isinstance(root, str):
            return ToolResult(success=False, output="Invalid 'root' argument.")

        root_path = Path(root).expanduser()
        if not root_path.exists():
            return ToolResult(success=False, output=f"Root not found: {root_path}")

        matches = sorted(
            str(path)
            for path in root_path.glob(pattern)
            if path.is_file()
        )
        return ToolResult(
            success=True,
            output="\n".join(matches) if matches else "No matches found.",
        )
