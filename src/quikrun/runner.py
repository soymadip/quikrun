import shutil
import sys
from pathlib import Path
from typing import Literal, cast

from .lib.config import CmdVars, Platform, Shell, default_cmds
from .lib.logger import log
from .lib.utils import (
    NA,
    get_shebang,
    is_any_in,
    resolve_cmd,
    run_command,
    scroll_to_top,
)


def quick_run(file_path: Path, run_args: list[str] | None = None) -> int:
    """Quickly Run a file"""

    # Current Environment Info
    cwd = Path.cwd()
    platform: Platform = cast(Platform, sys.platform.removesuffix("32"))
    shell: Shell = "posix"

    file_path = file_path.resolve().relative_to(cwd)

    if not run_args:
        run_args = []

    # ------------- Validate Input --------------

    if not file_path.exists():
        log.error(f"Given file doesn't exist! ({file_path})")
        return 1

    if not file_path.is_file():
        log.error("Given path is not a file!")
        return 1

    # ----------- Construct Commands --------------

    # Commands
    compile_cmd: str | NA = ""
    run_cmd: str | NA = ""

    # Output Dir, Path
    out_dir = Path(".quikrun")
    out_file = out_dir / file_path.stem

    # File Related Info
    file: CmdVars = {
        "file_path": file_path,
        "file_shebang": get_shebang(file_path),
        "file_dir": file_path.parent,
        "file_name": file_path.name,
        "file_stem": file_path.stem,
        "file_slug": file_path.stem.replace(" ", "_"),
        "file_ext": file_path.suffix.strip().strip("."),
        "out_dir": out_dir,
        "out_file": out_file,
        "platform": platform,
        "shell": shell,
    }

    # Error if file has neither shebang nor extension
    if not file["file_shebang"] and not file["file_ext"]:
        log.error("Given file has neither shebang nor Extension")
        return 1

    # Found shebang in file
    if file["file_shebang"]:
        run_cmd = f"{file['file_shebang']} {file['file_path']}"

    # Else use extension
    elif file["file_ext"]:
        # Resolve which command based on platform, shell.
        resolved_cmd = resolve_cmd(
            config_obj=default_cmds,
            file_ext=file["file_ext"],
            shell=shell,
            platform=platform,
            variables=file,
        )

        compile_cmd = resolved_cmd["compile"]
        run_cmd = resolved_cmd["run"]

        # apparently walrus operator makes type checker useless!
        if (compile_cmd is NA) or (run_cmd is NA):
            return 1

    term_size = shutil.get_terminal_size()
    clear_term: bool | Literal["scroll_up"] = "scroll_up"

    # Clear the terminal
    if clear_term == "scroll_up":
        scroll_to_top()
    elif clear_term:
        run_command("clear" if shell == "posix" else "cls")

    # Create output directory
    # if compile command is present or run command uses output dir/file
    if compile_cmd or is_any_in(cast(str, run_cmd), ["{out_dir}", "{out_file}"]):
        try:
            out_dir.mkdir(exist_ok=True, parents=True)
        except OSError as e:
            log.error(f"Failed to create output directory: {e}")
            return 1

    #
    # -------------- compile if needed ----------------

    if compile_cmd:
        log.info("Compiling Your Code....")
        log.info(f"Command: {log.fmt(cast(str, compile_cmd), 'GRAY')}")

        compile_result = run_command(cast(str, compile_cmd))

        if compile_result["return_code"] > 0:
            log.error("Failed to compile Your File. Check Logs Above!")
            return compile_result["return_code"]

        cmp_time = f"[took {round(compile_result['time_taken'], 3)}s]"

        log.success(f"Compilation Done. {log.fmt(cmp_time, 'GRAY')}")
        log.info("Executing Compiled Binary.")

    #
    # ------------- Code/Binary Execution --------------

    scroll_to_top()
    print(log.fmt(" Output ".center(term_size.columns, "-"), "GRAY"))

    run_cmd = f"{cast(str, run_cmd)} {' '.join(arg for arg in run_args)}"

    run_result = run_command(run_cmd)

    #
    # ------------------ Print Footer ------------------

    print(log.fmt("".center(term_size.columns, "-"), "GRAY"))

    run_status = log.fmt(
        f"[exit code {run_result['return_code']}] [took {round(run_result['time_taken'], 3)}s]",
        "GRAY",
    )

    if run_result["return_code"] > 0:
        log.error(f"Run Failed. Check Above. {run_status}")
    else:
        log.success(f"Ran Successfully {run_status}")

    compile_cmd = f"{compile_cmd} && " if compile_cmd else ""

    log.info(f"Command: {log.fmt(compile_cmd + cast(str, run_cmd), 'GRAY')}")

    input(log.fmt("⏵ Press Enter to Exit...", "GRAY"))

    return run_result["return_code"]
