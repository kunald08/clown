from __future__ import annotations

import json
from pathlib import Path


class TranscriptStore:
    def __init__(self, clown_home: Path) -> None:
        self._dir = clown_home / "transcripts"
        self._dir.mkdir(parents=True, exist_ok=True)
        self._path = self._dir / "latest.jsonl"

    def append_turn(self, role: str, content: str) -> None:
        record = {"role": role, "content": content}
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")
