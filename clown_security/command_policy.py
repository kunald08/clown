from __future__ import annotations

from pydantic import BaseModel


BLOCK_PATTERNS = {
    "rm -rf /",
    "mkfs",
    "shutdown",
    "reboot",
    "dd if=",
    ":(){:|:&};:",
}

APPROVAL_PATTERNS = {
    "rm ",
    "mv ",
    "cp ",
    "chmod ",
    "chown ",
    "sudo ",
    "git reset --hard",
    "git clean -fd",
    ">",
    ">>",
    "curl |",
    "wget |",
}


class CommandPolicyDecision(BaseModel):
    blocked: bool
    requires_approval: bool
    reason: str | None = None


def evaluate_command(command: str) -> CommandPolicyDecision:
    normalized = command.strip().lower()

    for pattern in BLOCK_PATTERNS:
        if pattern in normalized:
            return CommandPolicyDecision(
                blocked=True,
                requires_approval=False,
                reason=f"Blocked by command policy: {pattern}",
            )

    for pattern in APPROVAL_PATTERNS:
        if pattern in normalized:
            return CommandPolicyDecision(
                blocked=False,
                requires_approval=True,
                reason=f"Command requires approval: {pattern}",
            )

    return CommandPolicyDecision(
        blocked=False,
        requires_approval=False,
        reason=None,
    )
