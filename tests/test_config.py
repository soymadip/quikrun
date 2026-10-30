import pytest
from pydantic import TypeAdapter, ValidationError

from quikrun.config.types import Config

config_adapter = TypeAdapter(Config)


@pytest.mark.parametrize(
    ("field", "values"),
    [
        ("shell", ["posix", "cmd", "pwsh", "auto"]),
        ("platform", ["linux", "win", "darwin", "auto"]),
        ("auto_exit", ["always", "never", "on_success"]),
    ],
)
def test_config_accepts_enum_values(field: str, values: list[str]) -> None:
    for value in values:
        config = config_adapter.validate_python({field: value})

        assert getattr(config, field) == value


@pytest.mark.parametrize(
    "config_data",
    [
        {"shell": "fish"},
        {"platform": "android"},
        {"clear_terminal": "always"},
        {"auto_exit": "on_error"},
        {"commands": {"py": 42}},
    ],
)
def test_config_rejects_invalid_values(config_data: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        config_adapter.validate_python(config_data)


def test_config_accepts_all_scalar_options() -> None:
    config = config_adapter.validate_python(
        {
            "shell": "posix",
            "platform": "linux",
            "clear_terminal": "scroll_up",
            "show_time_took": True,
            "show_command": False,
            "show_divider": True,
            "cache_dir": ".cache",
            "cd_to_file_dir": True,
            "keep_build_artifacts": False,
            "auto_exit": "on_success",
        }
    )

    assert config.clear_terminal == "scroll_up"
    assert config.cache_dir == ".cache"
    assert config.cd_to_file_dir is True
    assert config.keep_build_artifacts is False


def test_config_accepts_recursive_command_templates() -> None:
    commands = {
        "py": "python {file_path}",
        "js": ["bun {file_path}", "node {file_path}"],
        "c": {
            "compile": "gcc {file_path} -o {out_file}",
            "run": "{out_file}",
        },
    }

    config = config_adapter.validate_python({"commands": commands})

    assert config.commands == commands


def test_config_defaults_optional_fields_to_none() -> None:
    config = config_adapter.validate_python({})

    assert config.shell is None
    assert config.platform is None
    assert config.commands is None