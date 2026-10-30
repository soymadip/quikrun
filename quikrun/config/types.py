"""Default Config & Command Mappings for Quikrun"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, TypedDict

type CmdCommand = str | list[str] | dict[str, CmdCommand]
type CmdConfig = dict[str, CmdCommand]

type Platform = Literal["auto", "linux", "win", "darwin"]
type Shell = Literal["auto", "posix", "cmd", "pwsh"]
type AutoExit = Literal["always", "never", "on_success"]

type StrOrPath = str | Path


@dataclass(kw_only=True)
class Config:
    """Configuration For Quikrun"""

    # DONT FORGET TO UPDATE ResolvedConf AFTER CHANGE in this
    shell: Shell | None = field(
        default=None,
        metadata={"description": "Which shell to use."},
    )
    platform: Platform | None = field(
        default=None,
        metadata={"description": "Target platform or OS override for execution."},
    )
    clear_terminal: bool | Literal["scroll_up"] | None = field(
        default=None,
        metadata={
            "description": "Whether to clear the terminal or scroll up before running."
        },
    )
    show_time_took: bool | None = field(
        default=None,
        metadata={"description": "Whether to display the execution duration at footer"},
    )
    show_command: bool | None = field(
        default=None,
        metadata={"description": "Whether to display the command in footer."},
    )
    show_divider: bool | None = field(
        default=None,
        metadata={
            "description": "Whether to print the separation line before the footer"
        },
    )
    cache_dir: Path | str | None = field(
        default=None,
        metadata={
            "description": "Custom directory used for cache and compiled build artifacts."
        },
    )
    cd_to_file_dir: bool | None = field(
        default=None,
        metadata={
            "description": "Whether to change the working directory to the target file's folder before running/compiling."
        },
    )
    keep_build_artifacts: bool | None = field(
        default=None,
        metadata={
            "description": "Whether to retain temporary or compiled binaries after execution completes."
        },
    )
    auto_exit: AutoExit | None = field(
        default=None,
        metadata={"description": "Controls automatic process exit behavior."},
    )
    commands: CmdConfig | None = field(
        default=None,
        metadata={"description": "Custom language templates."},
    )


@dataclass(kw_only=True)
class ResolvedConf:
    """Resolved Configuration For Quikrun"""

    shell: Shell
    platform: Platform
    clear_terminal: bool | Literal["scroll_up"]
    show_time_took: bool
    show_command: bool
    show_divider: bool
    cache_dir: Path | str  # related to cwd
    cd_to_file_dir: bool
    keep_build_artifacts: bool
    auto_exit: AutoExit
    commands: CmdConfig


class CmdVars(TypedDict):
    """Template Variables for Command Templates"""

    platform: Platform  #   platform name (e.g., 'linux', 'win', 'darwin')
    shell: Shell  #         shell name (e.g., 'posix', 'cmd', 'pwsh')

    file_path: StrOrPath  # quoted path to the source file as given
    file_dir: StrOrPath  #  quoted absolute path to the source file's directory
    file_name: str  #       quoted filename with extension (e.g., 'main.py')
    file_stem: str  #       quoted filename without extension (e.g., 'main')
    file_slug: str  #       file name without spaces (e.g., 'my file.py' -> 'my_file')
    file_ext: str  #        file extension (e.g., '.py')
    file_shebang: str  #    shebang's command (e.g., '/usr/bin/env python3')

    out_dir: StrOrPath  #   quoted path to the compiled output bin's dir
    out_file: StrOrPath  #  quoted path of out_dir/file_stem
    run_args: str | list[str]  #  arguments to pass to file/bin


UNQUOTED_VARS = frozenset(["file_shebang", "file_ext", "platform", "shell"])
