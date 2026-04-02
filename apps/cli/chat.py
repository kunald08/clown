from __future__ import annotations

from rich.console import Console

from clown_agent.engine import AgentEngine
from clown_agent.types import AgentResponse, PendingApproval


def chat_command() -> None:
    """Start a minimal local chat session."""
    console = Console()
    engine = AgentEngine()

    console.print("[bold magenta]Clown[/bold magenta] local chat")
    console.print("Type a prompt. Type 'exit' or 'quit' to leave.\n")
    console.print("Tool mode: /tool <name> key=value key='quoted value'\n")

    while True:
        try:
            prompt = console.input("[bold cyan]> [/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nBye.")
            break

        if not prompt:
            continue
        if prompt.lower() in {"exit", "quit"}:
            console.print("Bye.")
            break

        response = engine.handle_user_message(prompt)
        response = maybe_handle_approval(console, engine, response)
        console.print(f"\n[bold green]Clown:[/bold green] {response.final_text}\n")


def maybe_handle_approval(
    console: Console,
    engine: AgentEngine,
    response: AgentResponse,
) -> AgentResponse:
    approval = response.pending_approval
    if approval is None:
        return response

    console.print(f"[bold yellow]Approval needed:[/bold yellow] {approval.reason}")
    if approval.preview:
        console.print("[dim]Preview:[/dim]")
        console.print(approval.preview)
    if not ask_for_approval(console, approval):
        return AgentResponse(final_text="Command cancelled by user.")

    return engine.approve_and_run(approval.tool_name, approval.arguments)


def ask_for_approval(console: Console, approval: PendingApproval) -> bool:
    answer = console.input(
        f"Approve {approval.tool_name}? [y/N]: "
    ).strip()
    return answer.lower() in {"y", "yes"}
