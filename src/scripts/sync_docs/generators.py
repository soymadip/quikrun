import dataclasses
from typing import Any

from quikrun.config.defaults import DEFAULT_CONF
from quikrun.config.types import Config

from .formatters import format_command_value, format_type_hint, is_compiled_config


def generate_variables_table() -> str:
    """Dynamically builds the Variables reference table from CmdVars annotations and doc-comments."""
    import inspect
    import re

    from quikrun.config.types import CmdVars

    source = inspect.getsource(CmdVars)
    table_md = "| Placeholder | Value |\n| :--- | :--- |\n"

    for line in source.splitlines():
        # Match lines like: file_path: StrOrPath  # quoted path to the source file as given
        match = re.match(r"^\s*([a-zA-Z0-9_]+)\s*:\s*[^#]+#\s*(.*)$", line)
        if match:
            var_name, desc = match.groups()
            table_md += f"| `{{{var_name}}}` | {desc.strip()} |\n"

    return table_md

def generate_config_ref_table() -> str:
    """Dynamically builds the Configuration Reference table with correct Description and Default columns."""

    table_md = (
        "| Setting | Type | Default | Description |\n| :--- | :--- | :--- | :--- |\n"
    )

    for field in dataclasses.fields(Config):
        if field.name == "commands":
            continue

        setting_name = f"**`{field.name}`**"
        type_str = format_type_hint(field.type)

        # Extract description from field metadata
        description = field.metadata.get("description", "—")

        # Get actual runtime default value from DEFAULT_CONF
        default_val = getattr(DEFAULT_CONF, field.name, None)
        if isinstance(default_val, str):
            default_str = f'`"{default_val}"`'
        else:
            default_str = f"`{default_val}`"

        table_md += f"| {setting_name} | {type_str} | {default_str} | {description} |\n"

    return table_md


def generate_command_tables(commands: dict[str, Any] | None = None) -> tuple[str, str]:
    """Generates markdown tables for interpreted and compiled commands."""

    raw_commands = commands if commands is not None else DEFAULT_CONF.commands
    interpreted = {}
    compiled = {}

    for ext, val in raw_commands.items():
        if is_compiled_config(val):
            compiled[ext] = val
        else:
            interpreted[ext] = val

    interpreted_md = "| Extension | Command |\n| --- | --- |\n"
    for ext in sorted(interpreted.keys()):
        cmd = format_command_value(interpreted[ext])
        interpreted_md += f"| `.{ext}` | {cmd} |\n"

    compiled_md = "| Extension | Compile Command | Run Command |\n| --- | --- | --- |\n"
    for ext in sorted(compiled.keys()):
        val = compiled[ext]
        if isinstance(val, dict) and "compile" in val and "run" in val:
            comp_cmd = format_command_value(val["compile"])
            run_cmd = format_command_value(val["run"])
        else:
            comp_cmd = "—"
            run_cmd = format_command_value(val)
        compiled_md += f"| `.{ext}` | {comp_cmd} | {run_cmd} |\n"

    return interpreted_md, compiled_md

