from pydantic import TypeAdapter

from quikrun.config.types import Config


def test_shell_schema_includes_literal_and_platform_mapping() -> None:
    schema = TypeAdapter(Config).json_schema()
    shell_config = schema["$defs"]["ShellConfig"]

    assert {"$ref": "#/$defs/Shell"} in shell_config["anyOf"]
    assert {"$ref": "#/$defs/ShellMap"} in shell_config["anyOf"]
    assert set(schema["$defs"]["Shell"]["enum"]) == {"posix", "cmd", "pwsh", "auto"}
    assert set(schema["$defs"]["ShellMap"]["properties"]) == {"linux", "darwin", "win"}


def test_shell_mapping_is_accepted() -> None:
    config = TypeAdapter(Config).validate_python(
        {"shell": {"linux": "/usr/bin/zsh", "win": "pwsh.exe"}}
    )

    assert config.shell == {"linux": "/usr/bin/zsh", "win": "pwsh.exe"}