from __future__ import annotations

from clown_agent.engine import AgentEngine
from clown_agent.tool_invocation import parse_tool_invocation


def test_parse_tool_invocation_with_quotes() -> None:
    invocation = parse_tool_invocation(
        "/tool write_file path=demo.txt content='hello clown'"
    )
    assert invocation is not None
    assert invocation.tool_name == "write_file"
    assert invocation.arguments == {
        "path": "demo.txt",
        "content": "hello clown",
    }


def test_engine_runs_write_file_tool(tmp_path) -> None:
    engine = AgentEngine()
    target = tmp_path / "note.txt"

    response = engine.handle_user_message(
        f"/tool write_file path={target} content='hello from tool'"
    )

    assert "Wrote" in response.final_text
    assert target.read_text(encoding="utf-8") == "hello from tool"


def test_engine_marks_shell_command_for_approval() -> None:
    engine = AgentEngine()

    response = engine.handle_user_message("/tool shell_exec command='rm sample.txt'")

    assert response.pending_approval is not None
    assert response.pending_approval.tool_name == "shell_exec"


def test_engine_can_run_approved_shell_command() -> None:
    engine = AgentEngine()

    response = engine.approve_and_run("shell_exec", {"command": "echo clown-approved"})

    assert response.pending_approval is None
    assert "clown-approved" in response.final_text
