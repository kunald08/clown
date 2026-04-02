from __future__ import annotations

from difflib import unified_diff


def build_diff_preview(
    before: str,
    after: str,
    *,
    from_label: str = "before",
    to_label: str = "after",
) -> str:
    diff = unified_diff(
        before.splitlines(),
        after.splitlines(),
        fromfile=from_label,
        tofile=to_label,
        lineterm="",
    )
    return "\n".join(diff)
