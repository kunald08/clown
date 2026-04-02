from __future__ import annotations

import subprocess
from pathlib import Path

from clown_security.command_policy import evaluate_command
from clown_tools.base import BaseTool, ToolResult, missing_argument


class ShellExecTool(BaseTool):
    name = "shell_exec"
    description = "Execute a shell command with basic safety checks."

    def run(self, **kwargs: object) -> ToolResult:
        command = kwargs.get("command")
        cwd = kwargs.get("cwd")
        timeout = kwargs.get("timeout", 10)
        approved = kwargs.get("approved", False)

        if not isinstance(command, str) or not command.strip():
            return missing_argument("command")
        if cwd is not None and not isinstance(cwd, str):
            return ToolResult(success=False, output="Invalid 'cwd' argument.")
        if not isinstance(timeout, int) or timeout <= 0:
            return ToolResult(success=False, output="Invalid 'timeout' argument.")
        if not isinstance(approved, bool):
            return ToolResult(success=False, output="Invalid 'approved' argument.")

        decision = evaluate_command(command)
        if decision.blocked:
            return ToolResult(success=False, output=decision.reason or "Blocked command.")
        if decision.requires_approval and not approved:
            return ToolResult(
                success=False,
                output=decision.reason or "Command requires approval.",
                requires_approval=True,
                approval_reason=decision.reason or "Command requires approval.",
            )

        working_directory = Path(cwd).expanduser() if cwd else None
        if working_directory and not working_directory.exists():
            return ToolResult(
                success=False,
                output=f"Working directory not found: {working_directory}",
            )

        try:
            completed = subprocess.run(
                ["zsh", "-lc", command],
                cwd=str(working_directory) if working_directory else None,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                output=f"Command timed out after {timeout} seconds.",
            )

        combined_output = (completed.stdout + completed.stderr).strip()
        if not combined_output:
            combined_output = f"Command exited with status {completed.returncode}."

        return ToolResult(
            success=completed.returncode == 0,
            output=combined_output,
        )
