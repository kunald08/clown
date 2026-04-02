from __future__ import annotations

from clown_tools.base import BaseTool, ToolResult, missing_argument
from clown_tools.file.common import (
    ensure_text_file,
    read_utf8_text,
    resolve_input_path,
)
from clown_tools.file.diff_preview import build_diff_preview


class EditFileTool(BaseTool):
    name = "edit_file"
    description = "Replace text in an existing utf-8 file."

    def run(self, **kwargs: object) -> ToolResult:
        resolved = resolve_input_path(kwargs.get("path"))
        if isinstance(resolved, ToolResult):
            return resolved

        old_text = kwargs.get("old_text")
        new_text = kwargs.get("new_text")
        if not isinstance(old_text, str):
            return missing_argument("old_text")
        if not isinstance(new_text, str):
            return missing_argument("new_text")
        approved = kwargs.get("approved", False)
        if not isinstance(approved, bool):
            return ToolResult(success=False, output="Invalid 'approved' argument.")

        path = resolved
        error = ensure_text_file(path)
        if error:
            return error

        existing = read_utf8_text(path)
        if isinstance(existing, ToolResult):
            return existing
        if old_text not in existing:
            return ToolResult(
                success=False,
                output=f"Target text not found in {path}",
            )

        updated = existing.replace(old_text, new_text, 1)
        if not approved:
            return ToolResult(
                success=False,
                output=f"Edit requires approval: {path}",
                requires_approval=True,
                approval_reason=f"Edit requires approval: {path}",
                preview=build_diff_preview(
                    existing,
                    updated,
                    from_label=str(path),
                    to_label=str(path),
                ),
            )

        path.write_text(updated, encoding="utf-8")
        return ToolResult(success=True, output=f"Edited {path}")
