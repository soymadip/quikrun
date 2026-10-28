#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import Any, Literal, Union, get_origin, get_args
import dataclasses
import re

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from quikrun.config.defaults import DEFAULT_CONF
from quikrun.config.types import Config

NAME_MAP = {
    "linux": "Linux",
    "darwin": "macOS",
    "win": "Windows",
    "posix": "POSIX",
    "cmd": "CMD",
    "pwsh": "PowerShell 7",
}


def format_command_value(val: Any) -> str:
    """Formats command values for documentation, keeping @notations intact as code tags."""
    if isinstance(val, str):
        return f"`{val}`"
    elif isinstance(val, list):
        return " → ".join(format_command_value(v) for v in val)
    elif isinstance(val, dict):
        parts = []
        for k, v in val.items():
            label = NAME_MAP.get(k, k)
            formatted_v = format_command_value(v)
            parts.append(f"{label}: {formatted_v}")
        return "<br>".join(parts)
    return f"`{val}`"


def is_compiled_config(val: Any) -> bool:
    """Determines whether a command configuration represents a compiled language."""
    if isinstance(val, dict):
        if "compile" in val and "run" in val:
            return True
        for sub_val in val.values():
            if is_compiled_config(sub_val):
                return True
    return False


def format_type_hint(tp: Any) -> str:
    """Recursively resolves type aliases, unwraps unions, and cleans up type hints into a single backtick block."""
    if hasattr(tp, "__value__"):
        return format_type_hint(tp.__value__)[1:-1]

    origin = get_origin(tp)
    if origin is Union or type(tp).__name__ == "UnionType":
        args = get_args(tp)
        parts = []
        for arg in args:
            if arg is type(None) or arg is None:
                parts.append("None")
            else:
                parts.append(format_type_hint(arg).strip("`"))
        return f"`{' | '.join(parts)}`"

    if origin is Literal or getattr(tp, "__name__", "") == "Literal":
        args = get_args(tp)
        formatted_args = ", ".join(repr(arg) for arg in args)
        return f"`Literal[{formatted_args}]`"

    if tp is type(None) or tp is None:
        return "`None`"

    tp_str = str(tp)
    prefixes_to_strip = [
        "quikrun.config.types.",
        "typing.",
        "pathlib.",
        "<class '",
        "'>",
    ]
    for prefix in prefixes_to_strip:
        tp_str = tp_str.replace(prefix, "")

    return f"`{tp_str}`"


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

        table_md += f"| {setting_name} | {type_str} | {description} | {default_str} |\n"

    return table_md


def main() -> None:
    # 1. Generate Languages Tables
    raw_commands = DEFAULT_CONF.commands
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

    # Sync supported-languages.md
    lang_docs_path = PROJECT_ROOT / "docs" / "md" / "supported-languages.md"
    if lang_docs_path.exists():
        content = lang_docs_path.read_text("utf-8")
        content = re.sub(
            r"<!-- DYNAMIC_INTERPRETED_START -->.*?<!-- DYNAMIC_INTERPRETED_END -->",
            f"<!-- DYNAMIC_INTERPRETED_START -->\n\n{interpreted_md.strip()}\n\n<!-- DYNAMIC_INTERPRETED_END -->",
            content,
            flags=re.DOTALL,
        )
        content = re.sub(
            r"<!-- DYNAMIC_COMPILED_START -->.*?<!-- DYNAMIC_COMPILED_END -->",
            f"<!-- DYNAMIC_COMPILED_START -->\n\n{compiled_md.strip()}\n\n<!-- DYNAMIC_COMPILED_END -->",
            content,
            flags=re.DOTALL,
        )
        lang_docs_path.write_text(content, "utf-8")
        print(f"Synchronized {lang_docs_path.name}")
    else:
        print(f"Warning: Could not find {lang_docs_path}", file=sys.stderr)

    # 2. Generate and Sync Configuration Reference Table
    config_ref_md = generate_config_ref_table()
    config_docs_path = PROJECT_ROOT / "docs" / "md" / "configuration.md"

    if config_docs_path.exists():
        content = config_docs_path.read_text("utf-8")
        content = re.sub(
            r"<!-- DYNAMIC_CONFIG_REF_START -->.*?<!-- DYNAMIC_CONFIG_REF_END -->",
            f"<!-- DYNAMIC_CONFIG_REF_START -->\n\n{config_ref_md.strip()}\n\n<!-- DYNAMIC_CONFIG_REF_END -->",
            content,
            flags=re.DOTALL,
        )
        config_docs_path.write_text(content, "utf-8")
        print(f"Synchronized {config_docs_path.name}")
    else:
        print(f"Warning: Could not find {config_docs_path}", file=sys.stderr)

    print("Successfully finished documentation synchronization!")


if __name__ == "__main__":
    main()
