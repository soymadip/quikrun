import pytest
from pydantic import TypeAdapter

from quikrun.config.types import Config

config_adapter = TypeAdapter(Config)


def test_config_schema_describes_all_fields() -> None:
    schema = config_adapter.json_schema()

    assert set(schema["properties"]) == {
        "shell",
        "platform",
        "clear_terminal",
        "show_time_took",
        "show_command",
        "show_divider",
        "cache_dir",
        "cd_to_file_dir",
        "keep_build_artifacts",
        "auto_exit",
        "commands",
    }
    assert schema["properties"]["shell"]["description"] == "Which shell to use."
    assert (
        schema["properties"]["commands"]["description"]
        == "Custom language templates."
    )


@pytest.mark.parametrize(
    ("definition", "values"),
    [
        ("Shell", ["posix", "cmd", "pwsh", "auto"]),
        ("Platform", ["linux", "win", "darwin", "auto"]),
        ("AutoExit", ["always", "never", "on_success"]),
    ],
)
def test_schema_lists_enum_values(definition: str, values: list[str]) -> None:
    schema = config_adapter.json_schema()

    assert set(schema["$defs"][definition]["enum"]) == set(values)

