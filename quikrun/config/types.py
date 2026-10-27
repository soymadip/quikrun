"""Default Config & Command Mappings for Quikrun"""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict

type CmdCommand = str | list[str] | dict[str, CmdCommand]
type CmdConfig = dict[str, CmdCommand]

type Platform = Literal["linux", "win", "darwin", 'auto']
type Shell = Literal["posix", "cmd", "pwsh", "auto"]

type StrOrPath = str | Path


@dataclass(kw_only=True)
class Config:
    """Configuration For Quikrun"""

    # DONT FORGET TO UPDATE ResolvedConf AFTER CHANGE in this
    shell: Shell | None = None
    platform: Platform | None = None
    clear_terminal: bool | Literal["scroll_up"] | None = None 
    show_time_took: bool | None = None
    show_command: bool | None = None
    show_shell: bool | None = None
    show_divider: bool | None = None
    cache_dir: Path | str | None = None
    cd_to_file_dir: bool | None = None
    keep_build_artifacts: bool | None = None
    auto_exit: Literal["always", "never", "on_success"] | None = None
    commands: CmdConfig | None = None


@dataclass(kw_only=True)
class ResolvedConf:
    """Resolved Configuration For Quikrun"""

    shell: Shell
    platform: Platform
    clear_terminal: bool | Literal["scroll_up"]
    show_time_took: bool
    show_command: bool
    show_shell: bool
    show_divider: bool
    cache_dir: Path | str  # related to cwd
    cd_to_file_dir: bool
    keep_build_artifacts: bool
    auto_exit: Literal["always", "never", "on_success"]
    commands: CmdConfig


class CmdVars(TypedDict):
    """Template Variables for Command Templates"""

    file_path: StrOrPath  # quoted path to the source file as given
    file_dir: StrOrPath  #  quoted absolute path to the source file's directory
    file_name: str  #       quoted filename with extension (e.g., 'main.py')
    file_stem: str  #       quoted filename without extension (e.g., 'main')
    file_slug: str  #       file name without spaces (e.g., 'my file.py' -> 'my_file')
    file_ext: str  #        file extension (e.g., '.py')
    file_shebang: str  #    shebang's command (e.g., '/usr/bin/env python3')

    out_dir: StrOrPath  #   quoted path to the compiled output bin's dir
    out_file: StrOrPath  #  quoted path of out_dir/file_stem
    platform: Platform  #   platform name (e.g., 'linux', 'win', 'darwin')
    shell: Shell  #         shell name (e.g., 'posix', 'cmd', 'pwsh')


UNQUOTED_VARS = frozenset(["file_shebang", "file_ext", "platform", "shell"])
