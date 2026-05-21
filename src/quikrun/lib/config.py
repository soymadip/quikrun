"""Leveled config loading for quikrun.

Priority (highest → lowest):
  1. Project-level : quikrun.toml in CWD
                     or pyproject.toml [tool.quikrun] in CWD
  2. User-level    : $XDG_CONFIG_HOME/quikrun/config.toml
  3. Built-in      : templates.COMMAND_TEMPLATES

Each level's [cmds] table is merged over the one below it.
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
        "temp_dir": None,
        "cd_to_file_dir": False,
        "keep_artifacts": False,
        "cmds": CMD_TEMPLATES.copy(),
    }

    # 2. User-level: ~/.config/quikrun/config.toml
    user_conf: dict[str, Any] = _read_toml(
        xdg_config_home() / "quikrun" / "config.toml"
    )

    for key in default_conf:
        if key != "cmds" and key in user_conf:
            default_conf[key] = user_conf[key]

    if "cmds" in user_conf:
        default_conf["cmds"].update(user_conf["cmds"])

    # 3. Project-level: quikrun.toml in CWD, falling back to pyproject.toml [tool.quikrun]
    cwd: Path = Path.cwd()
    project_conf: dict[str, Any] = {}

    if (cwd / "quikrun.toml").exists():
        project_conf = _read_toml(cwd / "quikrun.toml")
    else:
        pyproject: dict[str, Any] = _read_toml(cwd / "pyproject.toml")
        project_conf = pyproject.get("tool", {}).get("quikrun", {})

    for key in default_conf:
        if key != "cmds" and key in project_conf:
            default_conf[key] = project_conf[key]

    if "cmds" in project_conf:
        default_conf["cmds"].update(project_conf["cmds"])

    return default_conf
