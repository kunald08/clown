from __future__ import annotations

from pathlib import Path

from clown_tools.base import BaseTool, ToolResult


class GrepSearchTool(BaseTool):
    name = "grep_search"
    description = "Search for text inside utf-8 files."

    def run(self, **kwargs: object) -> ToolResult:
        query = kwargs.get("query")
        root = kwargs.get("root", ".")
        include = kwargs.get("include", "*")

        if not isinstance(query, str) or not query:
            return ToolResult(success=False, output="Missing 'query' argument.")
        if not isinstance(root, str):
            return ToolResult(success=False, output="Invalid 'root' argument.")
        if not isinstance(include, str) or not include:
            return ToolResult(success=False, output="Invalid 'include' argument.")

        root_path = Path(root).expanduser()
        if not root_path.exists():
            return ToolResult(success=False, output=f"Root not found: {root_path}")

        results: list[str] = []
        for path in sorted(root_path.rglob(include)):
            if not path.is_file():
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except UnicodeDecodeError:
                continue

            for lineno, line in enumerate(lines, start=1):
                if query in line:
                    results.append(f"{path}:{lineno}: {line}")

        return ToolResult(
            success=True,
            output="\n".join(results) if results else "No matches found.",
        )
