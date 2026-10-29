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


def main() -> None:
    adapter = TypeAdapter(Config)
    auto_schema = adapter.json_schema()
    
    remove_nonstandard_formats(auto_schema)

    # Remove Pre Existing entries from auto generated schema
    auto_schema.pop("title", None)
    auto_schema.pop("description", None)
    auto_schema.pop("$schema", None)
    auto_schema.pop("$id", None)

    config_schema_dict = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "https://www.schemastore.org/quikrun.json",
        "title": "quikrun",
        "description": "Configuration for quikrun, a CLI tool to run code files instantly without typing complex commands in terminal.",
        **auto_schema
    }

    output_path = PROJECT_ROOT / "quikrun.json"
    output_path.write_text(
        json.dumps(config_schema_dict, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Generated schema at {output_path}")


if __name__ == "__main__":
    main()