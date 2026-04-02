from __future__ import annotations

from clown_tools.base import BaseTool, ToolResult, missing_argument
from clown_tools.file.diff_preview import build_diff_preview
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
        approved = kwargs.get("approved", False)
        if not isinstance(approved, bool):
            return ToolResult(success=False, output="Invalid 'approved' argument.")

        path = resolved
        if path.exists() and not approved:
            existing = path.read_text(encoding="utf-8")
            return ToolResult(
                success=False,
                output=f"Overwrite requires approval: {path}",
                requires_approval=True,
                approval_reason=f"Overwrite requires approval: {path}",
                preview=build_diff_preview(
                    existing,
                    content,
                    from_label=str(path),
                    to_label=str(path),
                ),
            )

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return ToolResult(success=True, output=f"Wrote {len(content)} bytes to {path}")
