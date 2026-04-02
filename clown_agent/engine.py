from __future__ import annotations

from clown_agent.loop import AgentLoop
from clown_agent.session_state import SessionState
from clown_agent.types import AgentResponse
from clown_core.settings import load_settings
from clown_llm.providers.local_echo import LocalEchoProvider
from clown_storage.local.transcript_store import TranscriptStore
from clown_tools.registry import build_default_registry


class AgentEngine:
    def __init__(self) -> None:
        self.settings = load_settings()
        self.session = SessionState()
        self.transcript_store = TranscriptStore(self.settings.clown_home)
        self.provider = LocalEchoProvider(tool_registry=build_default_registry())
        self.loop = AgentLoop(self.transcript_store)

    def handle_user_message(self, user_message: str) -> AgentResponse:
        provider_response = self.provider.generate(
            messages=self.session.messages,
            user_message=user_message,
        )
        return self.loop.run_turn(self.session, user_message, provider_response)
