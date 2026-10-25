"""Utility Methods for quikrun."""

from collections.abc import Iterable
from typing import Any, TypedDict, cast
lazy import shutil
lazy import subprocess
lazy from pathlib import Path
lazy from shlex import quote
lazy from time import perf_counter

from .config import UNQUOTED_VARS, CmdCommand, CmdVars
from .logger import log

# sentinel Types
INVALID_KEY = sentinel("INVALID_KEY")
INVALID_DATA_TYPE = sentinel("INVALID_DATA_TYPE")
NO_BIN_AVAIL = sentinel("NO_BIN_AVAIL")


type NA = None | NO_BIN_AVAIL | INVALID_KEY | INVALID_DATA_TYPE


class ResolvedCmd(TypedDict):
    """
    A Resolved Command Return Type
    Format: {run:.., compile:.. }
    """

    run: str | NA
    compile: str | NA


class RunResult(TypedDict):
    """
    Result of a cmd run.
    Format: {return_code:.., time_taken:..}
    """

    return_code: int
    time_taken: float


def get_shebang(file_path: Path) -> str:
    """Detect the shebang if present & return the interpreter path, else return empty str."""
    shebang_prefix = "#!"

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            line1 = file.readline().strip()

            if not line1.startswith(shebang_prefix):
                return ""

            return line1.removeprefix(shebang_prefix).strip()

    except (OSError, UnicodeDecodeError) as e:
        log.error(f"Error reading {file_path}: {e}")
        return ""


def is_all_in(iterator: Iterable[Any], items: Iterable[Any]) -> bool:
    """Check if all of the given items are present in the given iterable."""
    return all(item in iterator for item in items)


def is_any_in(iterator: Iterable[Any], items: Iterable[Any]) -> bool:
    """Check if any of the given items are present in the given iterable."""
    return any(item in iterator for item in items)


def get_avail_cmd(cfg_list: list[str]) -> str | NO_BIN_AVAIL:
    """Return the command which's binary is available"""

    bins: str = ""

    for cmd in cfg_list:
        binary: str = cmd.split(maxsplit=1)[0].strip()
        bins += f"{'' if not bins else ','} {binary}"

        if shutil.which(binary):
            return cmd

    # None of the List is found in PATH
    log.error("No suitable interpreter is not installed or not in PATH!")
    log.info(f"Please install one of: {bins}")
    return NO_BIN_AVAIL


def resolve_cmd(
    config_obj: CmdCommand,
    file_ext: str,
    shell: str,
    platform: str,
    variables: CmdVars | None = None,
    _is_recursing: bool = False,
) -> ResolvedCmd:
    """Resolve command From a extension's value"""

    def _recurse(current_obj) -> ResolvedCmd:
        return resolve_cmd(
            current_obj,
            file_ext,
            shell,
            platform,
            variables,
            _is_recursing=True,
        )

    # Strip leading dot
    if file_ext.startswith(".") or not _is_recursing:
        file_ext = file_ext.removeprefix(".")

    # Quote placeholders
    if variables and not _is_recursing:
        quoted = {}
        for k, v in variables.items():
            v = str(v)
            quoted[k] = quote(v) if k not in UNQUOTED_VARS else v
        variables = cast(CmdVars, quoted)

    # Pick only config of given file extension
    if not _is_recursing and isinstance(config_obj, dict):
        try:
            config_obj = config_obj[file_ext]
        except KeyError:
            log.error(f"Extension `{file_ext}` is not supported Yet")
            log.info("Please Report in Project Repository. (Tip: run quikrun --info)")

            return {"run": INVALID_KEY, "compile": INVALID_KEY}
    #
    # ----------------- Resolve Command -----------------

    if isinstance(config_obj, str):
        if variables:
            config_obj = config_obj.format_map(variables)

        return {"run": config_obj, "compile": None}

    if isinstance(config_obj, list):
        return {"run": get_avail_cmd(config_obj), "compile": None}

    if isinstance(config_obj, dict):
        if is_all_in(config_obj, ["posix", "cmd", "pwsh"]):
            config_obj = config_obj[shell]

        elif is_all_in(config_obj, ["linux", "win", "darwin"]):
            config_obj = config_obj[platform]

        elif is_all_in(config_obj, ["compile", "run"]):
            # only run key is real value
            compile_obj = _recurse(config_obj["compile"])["run"]
            run_obj = _recurse(config_obj["run"])["run"]

            return {"run": run_obj, "compile": compile_obj}

        else:
            log.error(
                f"There are invalid/incomplete keys in {file_ext}'s configuration..."
            )
            return {"run": INVALID_KEY, "compile": INVALID_KEY}

        return _recurse(config_obj)

    log.error(f"Unexpected configuration type for {file_ext}: {type(config_obj)}")
    return {"run": INVALID_DATA_TYPE, "compile": INVALID_DATA_TYPE}


def run_command(cmd_str: str, use_shell: bool = True) -> RunResult:
    """Run a given command with or without shell"""

    start = perf_counter()
    return_code = subprocess.run(cmd_str, shell=use_shell, check=False).returncode
    stop = perf_counter()

    return {"return_code": return_code, "time_taken": stop - start}
