import shutil
import sys
from pathlib import Path
from typing import cast

from .config.loader import CfgList, CfgLoadError, load_config
from .config.types import CmdVars, Config, Platform
from .lib.logger import log
from .lib.utils import (
    NA,
    get_shebang,
    get_usr_conf_home,
    is_any_in,
    resolve_cmd,
    run_command,
    scroll_to_top,
)

type ExitCode = int


def quick_run(
    file_path: str | Path,
    run_args: list[str] | None = None,
    extra_config: Config | None = None,
    dry_run: bool = False,  # TODO
) -> ExitCode:
    """
    Quickly Run a file
    Returns Return Code of the code file
    """

    # -------------- Transform Arguments ----------------

    cwd = Path.cwd()
    file_path = Path(file_path).resolve().relative_to(cwd)

    if not run_args:
        run_args = []

    # ------------- Validate Input --------------

    log.info("Checking given path:", log.fmt(str(file_path), "GRAY"))

    if not file_path.exists():
        log.error("Given path doesn't exist!")
        return 1

    if not file_path.is_file():
        log.error("Given path is not a file!")
        return 1

    # --------------- Config Resolution ---------------

    config_files: CfgList = [
        extra_config,  # This Takes most priority, wlill be passed by CLI flags or method caller
        Path("quikrun.toml"),
        (Path("pyproject.toml"), "tool.quikrun"),
        (Path("Cargo.toml"), "package.metadata.quikrun"),
        (Path("package.json"), "quikrun"),
        get_usr_conf_home() / "quikrun" / "config.toml",  # User Config
        Path("/etc/quikrun/config.toml"),  # Global Config
    ]

    try:
        config = load_config(config_files)
    except CfgLoadError:
        return 1

    # Current Environment Info
    if config.platform == "auto":
        config.platform = cast(Platform, sys.platform.removesuffix("32"))

    if config.shell == "auto":
        config.shell = "cmd" if config.platform == "win" else "posix"

    # Commands
    compile_cmd: str | NA = ""
    run_cmd: str | NA = ""

    # Output Dir, Path
    out_dir = Path(config.cache_dir)
    out_file = out_dir / file_path.stem

    # File Related Info
    file: CmdVars = {
        "file_path": file_path,
        "file_shebang": get_shebang(file_path),
        "file_dir": file_path.parent,
        "file_name": file_path.name,
        "file_stem": file_path.stem,
        "file_slug": file_path.stem.replace(" ", "_"),
        "file_ext": file_path.suffix.strip().removeprefix("."),
        "out_dir": out_dir,
        "out_file": out_file,
        "platform": config.platform,
        "shell": config.shell,
        "run_args": run_args,
    }

    # ----------- Construct Commands --------------

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
            file_ext=file["file_ext"],
            config_obj=config.commands,
            shell=config.shell,
            platform=config.platform,
            variables=file,
        )

        compile_cmd = resolved_cmd["compile"]
        run_cmd = resolved_cmd["run"]
        display_cmd = resolved_cmd["display_cmd"]

        # apparently walrus operator makes type checker useless!
        if (compile_cmd is NA) or (run_cmd is NA):
            return 1

    term_size = shutil.get_terminal_size()

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
        log.info("Command:", log.fmt(cast(str, compile_cmd), "GRAY"))

        compile_result = run_command(cast(str, compile_cmd))

        if compile_result["return_code"] > 0:
            print()
            log.error("Failed to compile Your File. Check Logs Above!")
            return compile_result["return_code"]

        log.success(
            "Compilation Done.",
            log.fmt(f"[took {round(compile_result['time_taken'], 3)}s]", "GRAY"),
            log.fmt(f"[exit code {round(compile_result['return_code'], 3)}]", "GRAY"),
        )
        log.info("Executing Compiled Binary...")

    #
    # ------------- Code/Binary Execution --------------

    # Clear the terminal
    if config.clear_terminal == "scroll_up":
        scroll_to_top()
    elif config.clear_terminal:
        run_command("clear" if config.shell == "posix" else "cls")

    print(log.fmt(" Output ".center(term_size.columns, "-"), "GRAY"))

    run_result = run_command(cast(str, run_cmd))

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

    log.info(f"Command: {log.fmt(cast(str, display_cmd), 'GRAY')}")

    _ = input(log.fmt("⏵ Press Enter to Exit...", "GRAY"))

    return run_result["return_code"]
