import shlex
import subprocess
from pathlib import Path

from .lib.config import default_cmds
from .lib.logger import log
from .lib.utils import get_shebang


def quick_run(target_file: Path, args: list[str] | None = None) -> int:
    """Quickly Run a file"""

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
