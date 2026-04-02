from __future__ import annotations

import typer

from apps.cli.chat import chat_command

app = typer.Typer(help="Clown terminal coding assistant.")
app.command("chat")(chat_command)


if __name__ == "__main__":
    app()
