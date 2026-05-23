"""Leveled config loading for quikrun.

Priority (highest → lowest):
  1. Project-level : quikrun.toml in CWD
                     or pyproject.toml [tool.quikrun] in CWD
  2. User-level    : $XDG_CONFIG_HOME/quikrun/config.toml
  3. Built-in      : templates.COMMAND_TEMPLATES

Each level's [commands] table is merged over the one below it.
"""

import os
import tomllib
from pathlib import Path
from typing import Any

from .templates import CMD_TEMPLATES


def xdg_config_home() -> Path:
    xdg: str = os.environ.get("XDG_CONFIG_HOME", "")

    return Path(xdg) if xdg else Path.home() / ".config"


def _read_toml(file: Path) -> dict[str, Any]:
    """Parse a TOML file, silently returning {} on missing file or parse error."""

    try:
        with file.open("rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        return {}
    except tomllib.TOMLDecodeError as e:
        # Warn but don't crash
        from . import logger

        logger.warn(f"Ignoring malformed config at {file}: {e}")
        return {}


def _read_json(file: Path) -> dict[str, Any]:
    """Parse a JSON file, silently returning {} on missing file or parse error."""
    import json

    try:
        with file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data

            return {}

    except FileNotFoundError:
        return {}
        
    except json.JSONDecodeError as e:
        # Warn but don't crash
        from . import logger

        logger.warn(f"Ignoring malformed config at {file}: {e}")
        return {}


# ---------------- Public API ---------------


def load() -> dict[str, Any]:
    """Return the fully merged configuration (settings + command templates).

    Cascading priority: Built-in < User-level < Project-level
    """
    # Defaults
    default_conf: dict[str, Any] = {
        "shell": None,
        "clear_terminal": True,
        "show_time_took": True,
        "show_command": True,
        "show_shell": True,
        "show_divider": True,
        "temp_dir": None,
        "cd_to_file_dir": False,
        "keep_artifacts": False,
        "commands": CMD_TEMPLATES.copy(),
    }

    # 2. User-level: ~/.config/quikrun/config.toml
    user_conf: dict[str, Any] = _read_toml(
        xdg_config_home() / "quikrun" / "config.toml"
    )

    for key in default_conf:
        if key != "commands" and key in user_conf:
            default_conf[key] = user_conf[key]

    if "commands" in user_conf:
        default_conf["commands"].update(user_conf["commands"])

    # 3. Project-level: quikrun.toml -> pyproject.toml -> Cargo.toml -> package.json in CWD
    cwd: Path = Path.cwd()
    project_conf: dict[str, Any] = {}

    if (cwd / "quikrun.toml").exists():
        project_conf = _read_toml(cwd / "quikrun.toml")
    elif (cwd / "pyproject.toml").exists():
        pyproject: dict[str, Any] = _read_toml(cwd / "pyproject.toml")
        raw_conf = pyproject.get("tool", {}).get("quikrun", {})
        if isinstance(raw_conf, dict):
            project_conf = raw_conf
    elif (cwd / "Cargo.toml").exists():
        cargo: dict[str, Any] = _read_toml(cwd / "Cargo.toml")
        raw_conf = cargo.get("package", {}).get("metadata", {}).get("quikrun", {})
        if isinstance(raw_conf, dict):
            project_conf = raw_conf
    elif (cwd / "package.json").exists():
        raw_conf = _read_json(cwd / "package.json").get("quikrun", {})
        if isinstance(raw_conf, dict):
            project_conf = raw_conf

    for key in default_conf:
        if key != "commands" and key in project_conf:
            default_conf[key] = project_conf[key]

    if "commands" in project_conf:
        default_conf["commands"].update(project_conf["commands"])

    return default_conf
