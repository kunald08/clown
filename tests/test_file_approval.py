from __future__ import annotations

from pathlib import Path

from clown_agent.engine import AgentEngine
from clown_tools.file.edit import EditFileTool
from clown_tools.file.write import WriteFileTool


def test_write_file_requires_approval_for_overwrite(tmp_path: Path) -> None:
    path = tmp_path / "demo.txt"
    path.write_text("old value\n", encoding="utf-8")

    result = WriteFileTool().run(path=str(path), content="new value\n")

    assert result.success is False
    assert result.requires_approval is True
    assert "Overwrite requires approval" in result.output
    assert result.preview is not None
    assert "-old value" in result.preview
    assert "+new value" in result.preview


def test_edit_file_requires_approval_with_diff_preview(tmp_path: Path) -> None:
    path = tmp_path / "demo.txt"
    path.write_text("alpha\nbeta\n", encoding="utf-8")

    result = EditFileTool().run(
        path=str(path),
        old_text="beta",
        new_text="gamma",
    )

    assert result.success is False
    assert result.requires_approval is True
    assert "Edit requires approval" in result.output
    assert result.preview is not None
    assert "-beta" in result.preview
    assert "+gamma" in result.preview


def test_engine_can_apply_approved_overwrite(tmp_path: Path) -> None:
    engine = AgentEngine()
    target = tmp_path / "story.txt"
    target.write_text("before", encoding="utf-8")

    first = engine.handle_user_message(
        f"write 'after' to file {target}"
    )
    assert first.pending_approval is not None

    second = engine.approve_and_run(
        first.pending_approval.tool_name,
        first.pending_approval.arguments,
    )

    assert second.pending_approval is None
    assert target.read_text(encoding="utf-8") == "after"
