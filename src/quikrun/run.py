import shlex
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

from . import __version__
from .lib.config import default_cmds
from .lib.logger import log
from .lib.utils import get_shebang, is_tty


def quick_run() -> int:
    """Quickly Run a file"""

    # If it's tty, print a newline
    if is_tty():
        print()

    # Parse CLI Arguments
    parser = ArgumentParser(prog="quikrun", description="Run your code hassle free!")

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("file", help="Source file's path to run")

    # If No arguments are given, print help
    if len(sys.argv) == 1:
        log.error("No Arguments are given!\n")
        parser.print_help()
        return 1

    # Check Given Arguments
    args, extra_args = parser.parse_known_args()

    target_file: Path = Path(args.file.strip())

    if not target_file.exists():
        log.error("Given file not found!")
        return 1

    if not target_file.is_file():
        log.error("Given path is not a file!")
        return 1

    cmd_template = get_shebang(target_file)
    file_ext = target_file.suffix

    if cmd_template is None:
        if file_ext:
            try:
                cmd_template = default_cmds[file_ext.lstrip(".")]
            except KeyError:
                log.error(f"Extension {file_ext} is not supported!")
                return 1
        else:
            log.error("Given file has neither shebang nor extension!")
            return 1

    return subprocess.run(
        cmd_template.format_map({"file": shlex.quote(str(target_file))}),
        shell=True,
        check=False,
    ).returncode
