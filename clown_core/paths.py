from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    return Path.cwd()


def clown_home() -> Path:
    override = os.environ.get("CLOWN_HOME")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".clown"


def ensure_clown_home() -> Path:
    home = clown_home()
    home.mkdir(parents=True, exist_ok=True)
    return home
