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

from ..metadata import CONFIG_METADATA


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


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge override into base.

    For keys present in both, if both values are dicts, they are merged recursively.
    Otherwise, the value from override overwrites the value in base.
    """
    result = base.copy()

    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = deep_merge(result[key], val)
        else:
            result[key] = val

    return result


# ---------------- Public API ---------------


def load_conf() -> dict[str, Any]:
    """Return the fully merged configuration (settings + command templates).

    Cascading priority: Built-in < User-level < Project-level
    """
    # Defaults
    default_conf: dict[str, Any] = {}
    for key, meta in CONFIG_METADATA.items():
        val = meta["default"]
        if isinstance(val, dict):
            default_conf[key] = val.copy()
        else:
            default_conf[key] = val

    # 2. User-level: ~/.config/quikrun/config.toml
    user_conf: dict[str, Any] = _read_toml(
        xdg_config_home() / "quikrun" / "config.toml"
    )

    for key in default_conf:
        if key != "commands" and key in user_conf:
            default_conf[key] = user_conf[key]

    if "commands" in user_conf and isinstance(user_conf["commands"], dict):
        default_conf["commands"] = deep_merge(
            default_conf["commands"], user_conf["commands"]
        )

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

    if "commands" in project_conf and isinstance(project_conf["commands"], dict):
        default_conf["commands"] = deep_merge(
            default_conf["commands"], project_conf["commands"]
        )

    return default_conf
