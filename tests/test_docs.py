from pathlib import Path
from typing import Literal

from src.scripts.sync_docs import format_type_hint


def test_format_type_hint_renders_literal_values() -> None:
    assert format_type_hint(Literal["posix", "cmd"]) == '`"posix"` / `"cmd"`'


def test_format_type_hint_renders_union_members_individually() -> None:
    assert format_type_hint(bool | None) == "`bool`"


def test_format_type_hint_maps_path() -> None:
    assert format_type_hint(Path | str | None) == "`string` / `str`"


def test_format_type_hint_maps_lists_to_arrays() -> None:
    assert format_type_hint(list[str]) == "`array`"