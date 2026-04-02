from __future__ import annotations

from clown_security.command_policy import evaluate_command
from clown_tools.shell.exec import ShellExecTool


def test_command_policy_blocks_dangerous_command() -> None:
    decision = evaluate_command("rm -rf /tmp && rm -rf /")
    assert decision.blocked is True
    assert decision.requires_approval is False


def test_command_policy_requires_approval_for_write_like_command() -> None:
    decision = evaluate_command("rm sample.txt")
    assert decision.blocked is False
    assert decision.requires_approval is True


def test_shell_exec_runs_safe_command() -> None:
    result = ShellExecTool().run(command="echo clown-shell")
    assert result.success is True
    assert "clown-shell" in result.output


def test_shell_exec_rejects_unapproved_command() -> None:
    result = ShellExecTool().run(command="rm sample.txt")
    assert result.success is False
    assert "requires approval" in result.output.lower()


def test_shell_exec_hard_blocks_dangerous_command() -> None:
    result = ShellExecTool().run(command="shutdown now")
    assert result.success is False
    assert "blocked" in result.output.lower()


def test_shell_exec_honors_timeout() -> None:
    result = ShellExecTool().run(command="sleep 2", timeout=1)
    assert result.success is False
    assert "timed out" in result.output.lower()
