from __future__ import annotations

from clown_agent.loop import AgentLoop
from clown_agent.session_state import SessionState
from clown_agent.tool_invocation import parse_tool_invocation
from clown_agent.tool_runner import ToolRunner
from clown_agent.types import AgentResponse, PendingApproval
from clown_core.settings import load_settings
from clown_llm.providers.local_echo import LocalEchoProvider
from clown_storage.local.transcript_store import TranscriptStore
from clown_tools.registry import build_default_registry


class AgentEngine:
    def __init__(self) -> None:
        self.settings = load_settings()
        self.session = SessionState()
        self.transcript_store = TranscriptStore(self.settings.clown_home)
        self.registry = build_default_registry()
        self.provider = LocalEchoProvider(tool_registry=self.registry)
        self.loop = AgentLoop(self.transcript_store)
        self.tool_runner = ToolRunner(self.registry)

    def handle_user_message(self, user_message: str) -> AgentResponse:
        invocation = parse_tool_invocation(user_message)
        if invocation is not None:
            return self._handle_tool_invocation(
                invocation.tool_name,
                invocation.arguments,
                original_user_message=user_message,
            )

        provider_response = self.provider.generate(
            messages=self.session.messages,
            user_message=user_message,
        )
        if provider_response.tool_calls:
            planned_call = provider_response.tool_calls[0]
            return self._handle_tool_invocation(
                planned_call.tool_name,
                planned_call.arguments,
                original_user_message=user_message,
                preamble=provider_response.text,
            )
        return self.loop.run_turn(self.session, user_message, provider_response)

    def approve_and_run(
        self,
        tool_name: str,
        arguments: dict[str, object],
    ) -> AgentResponse:
        approved_arguments = dict(arguments)
        approved_arguments["approved"] = True
        return self._handle_tool_invocation(
            tool_name,
            approved_arguments,
            original_user_message=f"/tool {tool_name}",
        )

    def _handle_tool_invocation(
        self,
        tool_name: str,
        arguments: dict[str, object],
        original_user_message: str,
        preamble: str | None = None,
    ) -> AgentResponse:
        result = self.tool_runner.run_tool(tool_name, arguments)
        final_text = result.output if preamble is None else f"{preamble}\n{result.output}"
        pending_approval: PendingApproval | None = None

        requires_approval = (
            tool_name == "shell_exec"
            and not arguments.get("approved", False)
            and "requires approval" in result.output.lower()
        )
        if requires_approval:
            pending_approval = PendingApproval(
                tool_name=tool_name,
                arguments=arguments,
                reason=result.output,
            )

        self.transcript_store.append_turn("user", original_user_message)
        self.transcript_store.append_turn("assistant", final_text)
        return AgentResponse(
            final_text=final_text,
            tool_events=[f"{tool_name}: {'ok' if result.success else 'error'}"],
            pending_approval=pending_approval,
        )
