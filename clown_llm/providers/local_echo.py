from __future__ import annotations

from clown_agent.session_state import ChatMessage
from clown_llm.base import BaseProvider, ProviderResponse
from clown_tools.registry import ToolRegistry


class LocalEchoProvider(BaseProvider):
    """Temporary local provider used to validate the app loop."""

    def __init__(self, tool_registry: ToolRegistry) -> None:
        self._tool_registry = tool_registry

    def generate(
        self,
        messages: list[ChatMessage],
        user_message: str,
    ) -> ProviderResponse:
        tool_names = ", ".join(self._tool_registry.tool_names()) or "no tools yet"
        return ProviderResponse(
            text=(
                "Local provider is wired up. "
                f"You said: {user_message!r}. "
                f"Available tools: {tool_names}."
            )
        )
