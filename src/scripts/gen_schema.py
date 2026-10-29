#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from pydantic import TypeAdapter

# Resolve project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from quikrun.config.types import Config


def remove_nonstandard_formats(schema: object) -> None:
    if isinstance(schema, dict):
        if schema.get("format") == "path":
            schema.pop("format")
        for value in schema.values():
            remove_nonstandard_formats(value)
    elif isinstance(schema, list):
        for value in schema:
            remove_nonstandard_formats(value)


def add_platform_shell_mapping(schema: dict[str, object]) -> None:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return

    shell = properties.get("shell")
    if not isinstance(shell, dict):
        return

    alternatives = shell.get("anyOf")
    if not isinstance(alternatives, list):
        return

    alternatives.insert(
        1,
        {
            "type": "object",
            "properties": {
                "linux": {"type": "string"},
                "darwin": {"type": "string"},
                "win": {"type": "string"},
            },
            "additionalProperties": False,
        },
    )


def main() -> None:
    adapter = TypeAdapter(Config)
    config_schema_dict = adapter.json_schema()
    remove_nonstandard_formats(config_schema_dict)
    add_platform_shell_mapping(config_schema_dict)
    config_schema_dict["$schema"] = "http://json-schema.org/draft-07/schema#"
    config_schema_dict["$id"] = "https://www.schemastore.org/quikrun.json"

    output_path = PROJECT_ROOT / "quikrun.json"
    output_path.write_text(
        json.dumps(config_schema_dict, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Generated schema at {output_path}")


if __name__ == "__main__":
    main()
