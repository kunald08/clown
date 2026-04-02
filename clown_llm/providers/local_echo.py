from __future__ import annotations

import re

from clown_agent.session_state import ChatMessage
from clown_llm.base import BaseProvider, PlannedToolCall, ProviderResponse
from clown_tools.registry import ToolRegistry


class LocalEchoProvider(BaseProvider):
    """A lightweight local planner used to validate Clown end-to-end."""

    def __init__(self, tool_registry: ToolRegistry) -> None:
        self._tool_registry = tool_registry

    def generate(
        self,
        messages: list[ChatMessage],
        user_message: str,
    ) -> ProviderResponse:
        planned_call = self._plan_tool_call(user_message)
        if planned_call is not None:
            return ProviderResponse(
                text=f"Planner selected tool: {planned_call.tool_name}",
                tool_calls=[planned_call],
            )

        tool_names = ", ".join(self._tool_registry.tool_names()) or "no tools yet"
        return ProviderResponse(
            text=(
                "Local provider is wired up. "
                f"You said: {user_message!r}. "
                f"Available tools: {tool_names}."
            )
        )

    def _plan_tool_call(self, user_message: str) -> PlannedToolCall | None:
        text = user_message.strip()
        lowered = text.lower()

        if lowered.startswith("read file ") or lowered.startswith("show file "):
            path = text.split("file ", 1)[1].strip()
            if path:
                return PlannedToolCall(
                    tool_name="read_file",
                    arguments={"path": path},
                )

        write_match = re.match(
            r"write\s+(?P<content>.+?)\s+to\s+(?:file\s+)?(?P<path>.+)$",
            text,
            re.IGNORECASE,
        )
        if write_match:
            return PlannedToolCall(
                tool_name="write_file",
                arguments={
                    "path": write_match.group("path").strip(),
                    "content": write_match.group("content").strip().strip("'\""),
                },
            )

        edit_match = re.match(
            r"replace\s+(?P<old>.+?)\s+with\s+(?P<new>.+?)\s+in\s+(?:file\s+)?(?P<path>.+)$",
            text,
            re.IGNORECASE,
        )
        if edit_match:
            return PlannedToolCall(
                tool_name="edit_file",
                arguments={
                    "path": edit_match.group("path").strip(),
                    "old_text": edit_match.group("old").strip().strip("'\""),
                    "new_text": edit_match.group("new").strip().strip("'\""),
                },
            )

        search_match = re.match(
            r"search\s+for\s+(?P<query>.+?)\s+in\s+(?P<root>.+)$",
            text,
            re.IGNORECASE,
        )
        if search_match:
            return PlannedToolCall(
                tool_name="grep_search",
                arguments={
                    "query": search_match.group("query").strip().strip("'\""),
                    "root": search_match.group("root").strip(),
                },
            )

        glob_match = re.match(
            r"(?:find|list)\s+files\s+matching\s+(?P<pattern>.+?)\s+in\s+(?P<root>.+)$",
            text,
            re.IGNORECASE,
        )
        if glob_match:
            return PlannedToolCall(
                tool_name="glob_search",
                arguments={
                    "pattern": glob_match.group("pattern").strip().strip("'\""),
                    "root": glob_match.group("root").strip(),
                },
            )

        if lowered.startswith("run "):
            return PlannedToolCall(
                tool_name="shell_exec",
                arguments={"command": text[4:].strip()},
            )

        if lowered.startswith("execute "):
            return PlannedToolCall(
                tool_name="shell_exec",
                arguments={"command": text[8:].strip()},
            )

        return None
