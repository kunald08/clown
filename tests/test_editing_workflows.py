from __future__ import annotations

from pathlib import Path

from clown_agent.engine import AgentEngine
from clown_llm.providers.local_echo import LocalEchoProvider
from clown_tools.file.append import AppendFileTool
from clown_tools.registry import build_default_registry


def test_append_file_requires_approval(tmp_path: Path) -> None:
    path = tmp_path / "notes.txt"
    path.write_text("alpha", encoding="utf-8")

    result = AppendFileTool().run(path=str(path), content="\nbeta")

    assert result.success is False
    assert result.requires_approval is True
    assert "Append requires approval" in result.output
    assert result.preview is not None


def test_planner_creates_verified_append_chain() -> None:
    provider = LocalEchoProvider(tool_registry=build_default_registry())
    response = provider.generate(
        messages=[],
        user_message="append 'beta' to file demo.txt and verify",
    )

    assert [call.tool_name for call in response.tool_calls] == [
        "append_file",
        "read_file",
    ]


def test_engine_can_run_approved_verified_append_chain(tmp_path: Path) -> None:
    engine = AgentEngine()
    target = tmp_path / "notes.txt"
    target.write_text("alpha", encoding="utf-8")

    first = engine.handle_user_message(
        f"append 'beta' to file {target} and verify"
    )
    assert first.pending_approval is not None
    assert first.pending_approval.tool_name == "append_file"

    second = engine.approve_and_run(
        first.pending_approval.tool_name,
        first.pending_approval.arguments,
    )
    assert "Appended" in second.final_text

    verified = engine.handle_user_message(f"read file {target}")
    assert "alphabeta" in verified.final_text


def test_engine_runs_verified_edit_chain(tmp_path: Path) -> None:
    engine = AgentEngine()
    target = tmp_path / "story.txt"
    target.write_text("old value", encoding="utf-8")

    first = engine.handle_user_message(
        f"replace 'old value' with 'new value' in file {target} and verify"
    )
    assert first.pending_approval is not None

    second = engine.approve_and_run(
        first.pending_approval.tool_name,
        first.pending_approval.arguments,
    )
    assert "Edited" in second.final_text

    verified = engine.handle_user_message(f"read file {target}")
    assert "new value" in verified.final_text
