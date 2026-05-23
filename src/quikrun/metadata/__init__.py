"""Metadata for quikrun configuration."""

from typing import Any
from .cmd_templates import cmd_templates

CONFIG_METADATA: dict[str, dict[str, Any]] = {
    "shell": {
        "default": None,
        "description": "Custom shell to run commands in",
        "schema": {
            "anyOf": [
                {
                    "type": "string",
                    "description": "Cross-platform custom shell to run commands",
                },
                {
                    "type": "object",
                    "description": "Platform-specific custom shells",
                    "properties": {
                        "win": {
                            "type": "string",
                            "description": "Custom shell for Windows",
                        },
                        "linux": {
                            "type": "string",
                            "description": "Custom shell for Linux",
                        },
                        "darwin": {
                            "type": "string",
                            "description": "Custom shell for macOS (Darwin)",
                        },
                    },
                    "additionalProperties": False,
                },
            ]
        },
    },
    "clear_terminal": {
        "default": True,
        "description": "Clear the terminal before executing commands",
    },
    "show_time_took": {
        "default": True,
        "description": "Show time taken to execute the script",
    },
    "show_command": {
        "default": True,
        "description": "Show the actual command that is being run",
    },
    "show_shell": {
        "default": True,
        "description": "Show the shell being used for execution",
    },
    "show_divider": {
        "default": True,
        "description": "Show the divider line before command stdout/stderr",
    },
    "temp_dir": {
        "default": None,
        "description": "Directory to store temporary execution files",
    },
    "cd_to_file_dir": {
        "default": False,
        "description": "Change directory to the folder containing the file before execution",
    },
    "keep_artifacts": {
        "default": False,
        "description": "Keep generated binaries or temporary files after execution",
    },
    "commands": {
        "default": cmd_templates,
        "description": "Command Templates by file extension",
        "schema": {
            "type": "object",
            "description": "Command Templates by file extension",
            "additionalProperties": {"$ref": "#/definitions/commandValue"},
        },
    },
}
