from __future__ import annotations

from pathlib import Path

from clown_tools.file.edit import EditFileTool
from clown_tools.file.glob_search import GlobSearchTool
from clown_tools.file.grep_search import GrepSearchTool
from clown_tools.file.read import ReadFileTool
from clown_tools.file.write import WriteFileTool
from clown_tools.registry import build_default_registry


def test_registry_contains_new_file_tools() -> None:
    registry = build_default_registry()
    assert registry.tool_names() == [
        "edit_file",
        "glob_search",
        "grep_search",
        "read_file",
        "shell_exec",
        "write_file",
    ]


def test_write_and_read_file(tmp_path: Path) -> None:
    path = tmp_path / "demo.txt"

    write_result = WriteFileTool().run(path=str(path), content="hello clown")
    read_result = ReadFileTool().run(path=str(path))

    assert write_result.success is True
    assert read_result.success is True
    assert read_result.output == "hello clown"


def test_edit_file_replaces_first_match(tmp_path: Path) -> None:
    path = tmp_path / "demo.txt"
    path.write_text("hello clown\nhello clown\n", encoding="utf-8")

    result = EditFileTool().run(
        path=str(path),
        old_text="hello clown",
        new_text="hello world",
    )

    assert result.success is True
    assert path.read_text(encoding="utf-8") == "hello world\nhello clown\n"


def test_glob_search_finds_files(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("print('a')", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")

    result = GlobSearchTool().run(root=str(tmp_path), pattern="*.py")

    assert result.success is True
    assert str(tmp_path / "a.py") in result.output


def test_grep_search_finds_matching_lines(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "sample.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("alpha\nbeta clown\ngamma\n", encoding="utf-8")

    result = GrepSearchTool().run(root=str(tmp_path), include="*.py", query="clown")

    assert result.success is True
    assert f"{target}:2: beta clown" in result.output
