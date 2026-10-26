"""Default Config & Command Mappings for Quikrun"""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict

type CmdCommand = str | list[str] | dict[str, CmdCommand]
type CmdConfig = dict[str, CmdCommand]

type Platform = Literal["linux", "win", "darwin"]
type Shell = Literal["posix", "cmd", "pwsh"]

type StrOrPath = str | Path


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


@dataclass(frozen=True)
class Config:
    commands: CmdConfig
