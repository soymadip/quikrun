import shlex
import sys
from pathlib import Path
from typing import cast

from .lib.config import default_cmds
from .lib.logger import log
from .lib.utils import (
    NA,
    get_shebang,
    resolve_cmd,
    run_command,
)


def quick_run(file: Path, args: list[str] | None = None) -> int:
    """Quickly Run a file"""

    if not file.exists():
        log.error("Given file doesn't exist!")
        return 1

    if not file.is_file():
        log.error("Given path is not a file!")
        return 1

    file_shebang: str = get_shebang(file)
    file_ext: str = file.suffix.strip()
    file_quoted: str = shlex.quote(str(file))

    compile_cmd: str | NA = ""
    run_cmd: str | NA = ""

    if file_shebang:
        run_cmd = f"{file_shebang} {file_quoted}"

    elif file_ext:
        try:
            resolved_cmd = resolve_cmd(
                config_obj=default_cmds[file_ext.removeprefix(".")],
                file_ext=file_ext,
                shell="posix",
                platform=sys.platform.removesuffix(
                    "32"
                ),  # can be darwin, linux, win32,
                placeholders={
                    "file_ext": file_ext,
                    "file": file.name,
                },
            )

        except KeyError:
            log.error(f"Extension `{file_ext}` is not supported Yet")
            log.info("Please Report in Project Repository. (Tip: run quikrun --info)")
            return 1

        compile_cmd = resolved_cmd["compile"]
        run_cmd = resolved_cmd["run"]

        if (compile_cmd is NA) or (run_cmd is NA):
            return 1

    else:
        log.error("Given file has neither shebang nor Extension")
        return 1

    #
    # ------------- Start execution --------------

    # compile if needed
    if compile_cmd:
        print("----------------- Compiling Your Code -------------------")

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
    log.info(f"Took: {round(run_result['time_taken'], 4)}s")
    return 0
