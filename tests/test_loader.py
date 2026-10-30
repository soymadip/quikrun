import json

import pytest

from quikrun.config.loader import (
    CfgLoadError,
    _resolve_references,
    _update_dict,
    load_config,
)
from quikrun.config.types import Config


def test_update_dict_merges_nested_values_and_skips_none() -> None:
    base = {"show_command": True, "commands": {"py": "python3"}}

    result = _update_dict(
        base,
        {
            "show_command": None,
            "commands": {"py": "python", "js": "node"},
            "unknown": True,
        },
    )

    assert result == {
        "show_command": True,
        "commands": {"py": "python", "js": "node"},
        "unknown": True,
    }


def test_resolve_references_handles_strings_lists_and_dicts() -> None:
    commands = {
        "base": "python {file_path}",
        "script": "@base",
        "fallbacks": ["@base", "python3 {file_path}"],
        "compiled": {"run": "@base"},
    }

    assert _resolve_references(commands) == {
        "base": "python {file_path}",
        "script": "python {file_path}",
        "fallbacks": ["python {file_path}", "python3 {file_path}"],
        "compiled": {"run": "python {file_path}"},
    }


def test_resolve_references_rejects_unknown_reference() -> None:
    with pytest.raises(CfgLoadError, match="missing"):
        _resolve_references({"script": "@missing"})


def test_resolve_references_flattens_nested_lists() -> None:
    commands = {
        "base": "python {file_path}",
        "fallbacks": [["@base", "python3 {file_path}"], "pypy {file_path}"],
    }

    assert _resolve_references(commands)["fallbacks"] == [
        "python {file_path}",
        "python3 {file_path}",
        "pypy {file_path}",
    ]


def test_resolve_references_stops_cyclic_references() -> None:
    commands = {"first": "@second", "second": "@first"}

    assert _resolve_references(commands)["first"] == "@first"


def test_load_config_merges_config_objects_and_resolves_commands() -> None:
    config = load_config(
        [
            Config(show_command=False, commands={"py": "python {file_path}"}),
            Config(commands={"py": "@js"}),
        ]
    )

    assert config.show_command is False
    assert config.commands["py"] == ["bun run {file_path}", "node {file_path}"]


def test_load_config_registers_new_command_extension() -> None:
    config = load_config(
        [Config(commands={"zig": "zig run {file_path}"})]
    )

    assert config.commands["zig"] == "zig run {file_path}"


def test_load_config_reads_json_section(tmp_path) -> None:
    config_path = tmp_path / "pyproject.json"
    config_path.write_text(
        json.dumps({"tool": {"quikrun": {"show_command": False}}}),
        encoding="utf-8",
    )

    config = load_config([(config_path, "tool.quikrun")])

    assert config.show_command is False


def test_load_config_skips_missing_file_and_section(tmp_path) -> None:
    missing_path = tmp_path / "missing.toml"
    existing_path = tmp_path / "config.json"
    existing_path.write_text(json.dumps({"tool": {}}), encoding="utf-8")

    config = load_config(
        [missing_path, (existing_path, "tool.quikrun")]
    )

    assert config.show_command is True


def test_load_config_rejects_unknown_keys(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"unknown": True}), encoding="utf-8")

    with pytest.raises(CfgLoadError):
        load_config([config_path])


def test_load_config_rejects_invalid_json(tmp_path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text("{invalid", encoding="utf-8")

    with pytest.raises(CfgLoadError):
        load_config([config_path])