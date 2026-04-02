from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from clown_core.paths import ensure_clown_home, project_root


class ClownSettings(BaseModel):
    model_name: str = "local-echo"
    project_root: Path = Field(default_factory=project_root)
    clown_home: Path = Field(default_factory=ensure_clown_home)


def load_settings() -> ClownSettings:
    return ClownSettings()
