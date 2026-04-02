from __future__ import annotations

import shlex
from dataclasses import dataclass


@dataclass(slots=True)
class ToolInvocation:
    tool_name: str
    arguments: dict[str, object]


def parse_tool_invocation(user_message: str) -> ToolInvocation | None:
    if not user_message.startswith("/tool "):
        return None

    parts = shlex.split(user_message)
    if len(parts) < 2:
        return None

    tool_name = parts[1]
    arguments: dict[str, object] = {}
    for token in parts[2:]:
        if "=" not in token:
            continue
        key, raw_value = token.split("=", 1)
        arguments[key] = _coerce_value(raw_value)

    return ToolInvocation(tool_name=tool_name, arguments=arguments)


def _coerce_value(value: str) -> object:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered.isdigit():
        return int(lowered)
    return value
