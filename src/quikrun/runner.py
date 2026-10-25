import sys
from pathlib import Path
from typing import cast

from .lib.config import CmdVars, Platform, Shell, default_cmds
from .lib.logger import log
from .lib.utils import (
    NA,
    get_shebang,
    is_any_in,
    resolve_cmd,
    run_command,
)


def quick_run(file_path: Path, args: list[str] | None = None) -> int:
    """Quickly Run a file"""

    # Current Environment Info
    cwd = Path.cwd()
    platform: Platform = cast(Platform, sys.platform.removesuffix("32"))
    shell: Shell = "posix"

    file_path = file_path.resolve().relative_to(cwd)

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
    out_dir = cwd / ".quikrun"
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

    #
    # ------------- Start execution --------------

    # Clear the terminal
    run_command("clear" if shell == "posix" else "cls", use_shell=True)

    term_size = shutil.get_terminal_size()
    divider: str = log.fmt(f"{'-' * (term_size.columns - 5)}", "GRAY")


    # Create output directory
    # if compile command is present or run command uses output dir/file
    if compile_cmd or is_any_in(cast(str, run_cmd), ["{out_dir}", "{out_file}"]):
        log.info(f"Creating Output Directory: {out_dir}")
        out_dir.mkdir(exist_ok=True, parents=True)

    # compile if needed
    if compile_cmd:
        log.info(f"Compiling Your File: {file_path}")
        log.info(f"Command: {compile_cmd}")

        compile_result = run_command(cast(str, compile_cmd))

        if compile_result["return_code"] > 0:
            log.error("Failed to compile Your File. Check Logs Above!")
            return compile_result["return_code"]

        log.success("Compilation Done!")
        log.info(f"Took: {round(compile_result['time_taken'], 4)}s")

    #
    # Run the binary/command
    print("\n----------------- Running Your Code  -------------------")

    run_result = run_command(cast(str, run_cmd))

    print("----------------- Run Finished -------------------")

    if run_result["return_code"] > 0:
        log.error("Run Failed")
        return run_result["return_code"]

    log.success("Run Successful!")
    log.info(f"Command: {run_cmd}")
    log.info(f"Took: {round(run_result['time_taken'], 4)}s")
    return 0
