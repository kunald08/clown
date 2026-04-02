from __future__ import annotations

from clown_agent.session_state import ChatMessage, SessionState
from clown_agent.types import AgentResponse
from clown_llm.base import ProviderResponse
from clown_storage.local.transcript_store import TranscriptStore


class AgentLoop:
    def __init__(self, transcript_store: TranscriptStore) -> None:
        self._transcript_store = transcript_store

    def run_turn(
        self,
        session: SessionState,
        user_message: str,
        provider_response: ProviderResponse,
    ) -> AgentResponse:
        session.messages.append(ChatMessage(role="user", content=user_message))
        session.messages.append(
            ChatMessage(role="assistant", content=provider_response.text)
        )
        self._transcript_store.append_turn("user", user_message)
        self._transcript_store.append_turn("assistant", provider_response.text)
        return AgentResponse(final_text=provider_response.text)
