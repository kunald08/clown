from __future__ import annotations

from pathlib import Path

from clown_tools.base import ToolResult


def resolve_input_path(raw_path: object) -> Path | ToolResult:
    if not isinstance(raw_path, str) or not raw_path.strip():
        return ToolResult(success=False, output="Missing 'path' argument.")
    return Path(raw_path).expanduser()


def ensure_text_file(path: Path) -> ToolResult | None:
    if not path.exists():
        return ToolResult(success=False, output=f"File not found: {path}")
    if path.is_dir():
        return ToolResult(success=False, output=f"Path is a directory: {path}")
    return None


def read_utf8_text(path: Path) -> str | ToolResult:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ToolResult(success=False, output=f"File is not utf-8 text: {path}")
