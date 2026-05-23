#!/usr/bin/env python3
import json
import sys
from pathlib import Path

# Add the src/ directory to Python path so we can import quikrun directly
src_dir = str(Path(__file__).parent.parent.resolve())
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import the load function and metadata from your runtime codebase
from quikrun.metadata import CONFIG_METADATA  # noqa: E402


def main() -> None:
    # 1. Build schema properties strictly from the source metadata, bypassing local config files.
    properties = {
        "$schema": {"type": "string", "description": "Path to the JSON schema"}
    }

    for key, meta in CONFIG_METADATA.items():
        val = meta.get("default")
        prop = {}
        prop["description"] = meta.get("description", f"Setting for {key}")

        # If schema is defined explicitly in metadata, use it directly
        if "schema" in meta:
            prop.update(meta["schema"])
        elif isinstance(val, bool):
            prop["type"] = "boolean"
            prop["default"] = val
        elif isinstance(val, str):
            prop["type"] = "string"
            prop["default"] = val
        elif val is None:
            prop["type"] = ["string", "null"]
            prop["default"] = None
        else:
            prop["type"] = "string"
            prop["default"] = str(val)

        # Force insertion order for clean JSON: type first, description second
        ordered_prop = {}
        if "type" in prop:
            ordered_prop["type"] = prop.pop("type")
        if "description" in prop:
            ordered_prop["description"] = prop.pop("description")

        ordered_prop.update(prop)

        properties[key] = ordered_prop

    # 3. Define the full draft-07 SchemaStore structure
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "https://www.schemastore.org/quikrun.json",
        "title": "quikrun",
        "description": "Configuration for quikrun, a CLI tool to run code files instantly without typing complex commands in terminal.",
        "type": "object",
        "properties": properties,
        "additionalProperties": False,
        "definitions": {
            "compileRun": {
                "type": "object",
                "properties": {
                    "compile": {
                        "type": "string",
                        "description": "Command template to compile the file before running (e.g. 'g++ {file} -o {out}')",
                    },
                    "run": {
                        "type": "string",
                        "description": "Command template to execute the compiled binary (e.g. '{out}')",
                    },
                },
                "additionalProperties": False,
            },
            "osSpecific": {
                "type": "object",
                "properties": {
                    "linux": {
                        "$ref": "#/definitions/commandValue",
                        "description": "Command for Linux",
                    },
                    "darwin": {
                        "$ref": "#/definitions/commandValue",
                        "description": "Command for macOS (Darwin)",
                    },
                    "win": {
                        "$ref": "#/definitions/commandValue",
                        "description": "Command for Windows",
                    },
                },
                "additionalProperties": False,
            },
            "shellFamilySpecific": {
                "type": "object",
                "properties": {
                    "posix": {
                        "anyOf": [
                            {"$ref": "#/definitions/commandValue"},
                            {"$ref": "#/definitions/osSpecific"},
                        ],
                        "description": "Command for POSIX shells (bash, zsh, sh, etc.)",
                    },
                    "cmd": {
                        "anyOf": [
                            {"$ref": "#/definitions/commandValue"},
                            {"$ref": "#/definitions/osSpecific"},
                        ],
                        "description": "Command for Windows Command Prompt (cmd.exe)",
                    },
                    "pwsh": {
                        "anyOf": [
                            {"$ref": "#/definitions/commandValue"},
                            {"$ref": "#/definitions/osSpecific"},
                        ],
                        "description": "Command for PowerShell Core (pwsh)",
                    },
                },
                "additionalProperties": False,
            },
            "singleCommand": {
                "anyOf": [
                    {
                        "type": "string",
                        "pattern": "^@.+$",
                        "description": "Inheritance alias starting with @ (e.g., '@js')",
                    },
                    {
                        "type": "string",
                        "description": "The command to execute (e.g., 'python {file}')",
                    },
                    {"$ref": "#/definitions/compileRun"},
                ]
            },
            "commandValue": {
                "description": "Command string, fallback array, or platform-specific object",
                "anyOf": [
                    {"$ref": "#/definitions/singleCommand"},
                    {
                        "type": "array",
                        "items": {"$ref": "#/definitions/commandValue"},
                    },
                    {"$ref": "#/definitions/shellFamilySpecific"},
                ]
            },
        },
    }

    # 4. Save the schema to project root
    output_path = Path(__file__).parent.parent.parent / "quikrun.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
        f.write("\n")

    print(f"Generated schema at {output_path}")


if __name__ == "__main__":
    main()
