from __future__ import annotations

from clown_agent.loop import AgentLoop
from clown_agent.session_state import SessionState
from clown_agent.tool_invocation import parse_tool_invocation
from clown_agent.tool_runner import ToolRunner
from clown_agent.types import AgentResponse, PendingApproval
from clown_core.settings import load_settings
from clown_llm.base import ToolExecution
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
            return self._handle_planned_invocations(
                provider_response.tool_calls,
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

    def _handle_planned_invocations(
        self,
        planned_calls,
        original_user_message: str,
        preamble: str | None,
    ) -> AgentResponse:
        executions: list[ToolExecution] = []

        for planned_call in planned_calls:
            resolved_arguments = self._resolve_arguments(
                planned_call.arguments,
                executions,
            )
            response = self._handle_tool_invocation(
                planned_call.tool_name,
                resolved_arguments,
                original_user_message=original_user_message,
                preamble=None,
                record_transcript=False,
            )

            executions.append(
                ToolExecution(
                    tool_name=planned_call.tool_name,
                    arguments=resolved_arguments,
                    success=response.pending_approval is None
                    and "error" not in response.tool_events[-1],
                    output=response.final_text,
                )
            )

            if response.pending_approval is not None:
                response.final_text = self.provider.summarize_tool_results(
                    user_message=original_user_message,
                    executions=executions,
                    preamble=preamble,
                )
                self.transcript_store.append_turn("user", original_user_message)
                self.transcript_store.append_turn("assistant", response.final_text)
                return response

        final_text = self.provider.summarize_tool_results(
            user_message=original_user_message,
            executions=executions,
            preamble=preamble,
        )
        self.transcript_store.append_turn("user", original_user_message)
        self.transcript_store.append_turn("assistant", final_text)
        return AgentResponse(
            final_text=final_text,
            tool_events=[
                f"{execution.tool_name}: {'ok' if execution.success else 'error'}"
                for execution in executions
            ],
        )

    def _resolve_arguments(
        self,
        arguments: dict[str, object],
        executions: list[ToolExecution],
    ) -> dict[str, object]:
        if not executions:
            return dict(arguments)

        last_output = executions[-1].output
        first_line = last_output.splitlines()[0] if last_output else ""
        resolved: dict[str, object] = {}
        for key, value in arguments.items():
            if value == "$LAST_OUTPUT":
                resolved[key] = last_output
            elif value == "$FIRST_LINE":
                resolved[key] = first_line
            else:
                resolved[key] = value
        return resolved

    def _handle_tool_invocation(
        self,
        tool_name: str,
        arguments: dict[str, object],
        original_user_message: str,
        preamble: str | None = None,
        record_transcript: bool = True,
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

        if record_transcript:
            self.transcript_store.append_turn("user", original_user_message)
            self.transcript_store.append_turn("assistant", final_text)
        return AgentResponse(
            final_text=final_text,
            tool_events=[f"{tool_name}: {'ok' if result.success else 'error'}"],
            pending_approval=pending_approval,
        )
