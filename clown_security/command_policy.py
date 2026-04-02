from __future__ import annotations


DENYLIST = {
    "rm -rf /",
    "mkfs",
    "shutdown",
    "reboot",
}


def command_requires_block(command: str) -> bool:
    normalized = command.strip().lower()
    return any(token in normalized for token in DENYLIST)
