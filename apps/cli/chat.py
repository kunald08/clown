from __future__ import annotations

from rich.console import Console

from clown_agent.engine import AgentEngine


def chat_command() -> None:
    """Start a minimal local chat session."""
    console = Console()
    engine = AgentEngine()

    console.print("[bold magenta]Clown[/bold magenta] local chat")
    console.print("Type a prompt. Type 'exit' or 'quit' to leave.\n")

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
        console.print(f"\n[bold green]Clown:[/bold green] {response.final_text}\n")
