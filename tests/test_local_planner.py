from __future__ import annotations

from clown_agent.engine import AgentEngine
from clown_llm.providers.local_echo import LocalEchoProvider
from clown_tools.registry import build_default_registry


def test_local_planner_creates_read_file_call() -> None:
    provider = LocalEchoProvider(tool_registry=build_default_registry())
    response = provider.generate(messages=[], user_message="read file demo.txt")

    assert response.tool_calls
    assert response.tool_calls[0].tool_name == "read_file"
    assert response.tool_calls[0].arguments == {"path": "demo.txt"}


def test_engine_handles_plain_english_write_request(tmp_path) -> None:
    engine = AgentEngine()
    target = tmp_path / "story.txt"

    response = engine.handle_user_message(
        f"write 'hello planner' to file {target}"
    )

    assert "Planner selected tool: write_file" in response.final_text
    assert target.read_text(encoding="utf-8") == "hello planner"


def test_engine_handles_plain_english_read_request(tmp_path) -> None:
    engine = AgentEngine()
    target = tmp_path / "story.txt"
    target.write_text("read me", encoding="utf-8")

    response = engine.handle_user_message(f"read file {target}")

    assert "Planner selected tool: read_file" in response.final_text
    assert "read me" in response.final_text


def test_engine_flags_plain_english_shell_request_for_approval() -> None:
    engine = AgentEngine()

    response = engine.handle_user_message("run rm sample.txt")

    assert response.pending_approval is not None
    assert response.pending_approval.tool_name == "shell_exec"
