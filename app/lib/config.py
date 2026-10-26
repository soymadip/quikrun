"""Built-in Config & command mappings for quikrun."""

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


UNQUOTED_VARS = frozenset(
    [
        "file_shebang",
        "file_ext",
        "platform",
        "shell",
    ]
)


default_cmds: CmdConfig = {
    #
    # ---------------- Interpreted ---------------
    "bash": "bash {file_path}",
    "dart": "dart run {file_path}",
    "fish": "fish {file_path}",
    "java": "java {file_path}",
    "jl": "julia {file_path}",
    "js": ["bun run {file_path}", "node {file_path}"],
    "cjs": "@js",
    "mjs": "@js",
    "lua": "lua {file_path}",
    "php": "php {file_path}",
    "pl": "perl {file_path}",
    "py": {
        "posix": {
            "linux": "python3 {file_path}",
            "darwin": "python3 {file_path}",
            "win": "python {file_path}",
        },
        "cmd": "python {file_path}",
        "pwsh": {
            "linux": "python3 {file_path}",
            "darwin": "python3 {file_path}",
            "win": "python {file_path}",
        },
    },
    "r": "Rscript {file_path}",
    "rb": "ruby {file_path}",
    "sh": "bash {file_path}",
    "swift": "swift {file_path}",
    "ts": ["@js", "ts-node {file_path}"],
    "mts": "@ts",
    "zsh": "zsh {file_path}",
    #
    # ---------------- Compiled ---------------
    #
    "c": {
        "compile": "gcc -Wall -Wextra {file_path} -o {out_file}",
        "run": "{out_file}",
    },
    "cpp": {
        "compile": "g++ -std=c++23 -Wall -Wextra -Wshadow {file_path} -o {out_file}",
        "run": "{out_file}",
    },
    "c++": "@cpp",
    "cxx": "@cpp",
    "go": {"compile": "go build -o {out_file} {file_path}", "run": "{out_file}"},
    "hs": {"compile": "ghc -o {out_file} {file_path}", "run": "{out_file}"},
    "kt": {
        "compile": "kotlinc {file_path} -include-runtime -d {out_stem}.jar",
        "run": "java -jar {out_stem}.jar",
    },
    "nim": {"compile": "nim c --out:{out_file} {file_path}", "run": "{out_file}"},
    "rs": {"compile": "rustc {file_path} -o {out_file}", "run": "{out_file}"},
    "v": {"compile": "v -o {out_file} {file_path}", "run": "{out_file}"},
    "zig": {
        "compile": "zig build-exe {file_path} -femit-bin={out_file}",
        "run": "{out_file}",
    },
}
