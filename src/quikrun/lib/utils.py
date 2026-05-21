"""Utility helpers utilities for quikrun."""

import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from . import logger


def get_out_path(file: Path, temp_dir: str | None = None) -> Path:
    """Get the output path for the compiled binary.

    If temp_dir is provided, compiles to a hashed name inside that directory.
    Otherwise, compiles to a local '.quikrun' directory next to the source file.
    """
    file = file.resolve()
    
    if temp_dir:
        expanded = os.path.expandvars(temp_dir)
        custom_dir = Path(expanded).expanduser().resolve()
        custom_dir.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha1(str(file.resolve()).encode()).hexdigest()[:10]
        out_path = custom_dir / f"quikrun_{digest}"
    else:
        out_dir = file.parent / ".quikrun"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / file.stem

    if os.name == "nt":
        out_path = out_path.with_suffix(".exe")

    return out_path


def detect_shebang(file: Path) -> str | None:
    """Return the interpreter from the shebang line, or None."""
    try:
        with file.open("rb") as f:
            if f.read(2) != b"#!":
                return None
            return f.readline().decode("utf-8", errors="replace").strip()
    except OSError:
        return None


def run_cmd(
    cmd: str,
    shell: str | None = None,
    show_time: bool = False,
    show_command: bool = False,
    display_cmd: str | None = None,
    cwd: str | None = None,
    show_shell: bool = False,
) -> int:
    """Execute a fully-resolved runner command through the shell."""

    kwargs: dict[str, Any] = {"shell": True}
    start: float = time.perf_counter()

    if shell is not None:
        kwargs["executable"] = shell

    if cwd is not None:
        kwargs["cwd"] = cwd

    return_code: int = subprocess.run(cmd, **kwargs).returncode
    elapsed_time: float = time.perf_counter() - start

    if show_time or show_command or show_shell:
        shell_path = None
        if show_shell:
            import shutil

            raw_shell = (
                shell
                if shell is not None
                else (
                    os.environ.get("COMSPEC", "cmd.exe")
                    if os.name == "nt"
                    else "/bin/sh"
                )
            )

            shell_path = shutil.which(raw_shell) or raw_shell

        logger.footer(
            elapsed_time,
            return_code,
            (display_cmd or cmd) if show_command else None,
            show_time=show_time,
            shell_path=shell_path,
        )

    return return_code


def resolve_template(
    tmpl: Any, shell_family: str, platform_key: str, command_templates: dict[str, Any], depth: int = 0
) -> list[str]:
    """Recursively flatten aliases, platform dicts, and arrays into a flat list of commands."""

    if depth > 10:
        logger.error(
            "Alias resolution error: Maximum recursion depth exceeded (circular alias?)."
        )
        sys.exit(1)

    if isinstance(tmpl, str):
        if tmpl.startswith("@"):
            alias_key = tmpl[1:]
            if alias_key not in command_templates:
                logger.error(f"Alias error: '{alias_key}' is not a valid command template.")
                sys.exit(1)
            return resolve_template(
                command_templates[alias_key], shell_family, platform_key, command_templates, depth + 1
            )
        return [tmpl]

    if isinstance(tmpl, dict):
        # 1. Resolve Shell Family
        if shell_family in tmpl:
            val = tmpl[shell_family]
        else:
            logger.error(
                f"Config error: Command template is missing a configuration for shell family '{shell_family}'."
            )
            sys.exit(1)
            
        # 2. Resolve OS Platform (if nested dict)
        if isinstance(val, dict):
            if platform_key in val:
                val = val[platform_key]
            else:
                logger.error(
                    f"Config error: Command template is missing a configuration for OS platform '{platform_key}'."
                )
                sys.exit(1)

        return resolve_template(val, shell_family, platform_key, command_templates, depth + 1)

    if isinstance(tmpl, list):
        result: list[str] = []

        for item in tmpl:
            result.extend(
                resolve_template(item, shell_family, platform_key, command_templates, depth + 1)
            )
        return result

    return []
