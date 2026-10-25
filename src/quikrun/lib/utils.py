from typing import TypedDict
lazy import shutil
lazy import subprocess
lazy import sys
lazy from pathlib import Path
lazy from time import perf_counter

from .logger import log

# sentinel Types
INVALID_KEY_PRESENT = sentinel("INVALID_KEY_PRESENT")
INVALID_DATA_TYPE = sentinel("INVALID_DATA_TYPE")
NO_BIN_AVAIL = sentinel("NO_BIN_AVAIL")


type NA = None | NO_BIN_AVAIL | INVALID_KEY_PRESENT | INVALID_DATA_TYPE


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


def get_shebang(target_file: Path) -> str:
    """Detect the shebang if present & return the interpreter path, else return empty str."""
    shebang_prefix = "#!"

    try:
        with open(target_file, "r", encoding="utf-8", errors="ignore") as file:
            line1 = file.readline().strip()

            if not line1.startswith(shebang_prefix):
                return ""

            return line1.removeprefix(shebang_prefix).strip()

    except (OSError, UnicodeDecodeError) as e:
        log.error(f"Error reading {target_file}: {e}")
        return ""


def is_all_in(iterator: list | dict, items: list) -> bool:
    """Check if given items all are in a list"""
    for item in items:
        if item not in iterator:
            return False

    return True


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
    config_obj: str | list | dict,
    file_ext: str,
    shell: str,
    platform: str,
    placeholders: dict | None = None,
) -> ResolvedCmd:
    """Resolve command From a extension's value"""

    if file_ext.startswith("."):
        file_ext = file_ext.removeprefix(".")

    def _recurse(current_obj) -> ResolvedCmd:
        return resolve_cmd(
            current_obj,
            file_ext,
            shell,
            platform,
            placeholders,
        )

    # Strip leading dot
    if file_ext.startswith("."):
        file_ext = file_ext.removeprefix(".")

    # Quote placeholders
    if placeholders:
        quoted = {}
        for k, v in placeholders.items():
            if k not in UNQUOTED_KEYS:
                v = quote(cast(str, v))

            quoted[k] = v

        placeholders = cast(CmdPlaceholders, quoted)

    #
    # ----------------- Resolve Command -----------------

    if isinstance(config_obj, str):
        if placeholders:
            config_obj = config_obj.format_map(placeholders)

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
            return {"run": INVALID_KEY_PRESENT, "compile": INVALID_KEY_PRESENT}

        return _recurse(config_obj)

    log.error(f"Unexpected configuration type for {file_ext}: {type(config_obj)}")
    return {"run": INVALID_DATA_TYPE, "compile": INVALID_DATA_TYPE}


def run_command(cmd_str: str, use_shell: bool = True) -> RunResult:
    """Run a given command with or without shell"""

    start = perf_counter()
    return_code = subprocess.run(cmd_str, shell=use_shell, check=False).returncode
    stop = perf_counter()

    return {"return_code": return_code, "time_taken": stop - start}
