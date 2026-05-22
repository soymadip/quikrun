"""Built-in extension → command mappings for quikrun.

Template placeholders:
  {file}  — shell-quoted absolute path to the source file
  {out}   — shell-quoted path to the compiled output binary
"""

from typing import Any

CMD_TEMPLATES: dict[str, Any] = {
    #
    # ---------------- Interpreted ---------------
    "bash": "bash {file}",
    "dart": "dart run {file}",
    "fish": "fish {file}",
    "java": "java {file}",
    "jl": "julia {file}",
    "js": ["bun run {file}", "deno run {file}", "node {file}"],
    "cjs": "@js",
    "mjs": "@js",
    "lua": "lua {file}",
    "php": "php {file}",
    "pl": "perl {file}",
    "py": {
        "posix": {
            "linux": "python3 {file}",
            "darwin": "python3 {file}",
            "win": "python {file}",
        },
        "cmd": "python {file}",
        "pwsh": {
            "linux": "python3 {file}",
            "darwin": "python3 {file}",
            "win": "python {file}",
        },
    },
    "r": "Rscript {file}",
    "rb": "ruby {file}",
    "sh": "bash {file}",
    "swift": "swift {file}",
    "ts": ["@js", "ts-node {file}"],
    "mts": "@ts",
    "zsh": "zsh {file}",
    #
    # ---------------- Compiled ---------------
    #
    "c": {"compile": "gcc -Wall -Wextra {file} -o {out}", "run": "{out}"},
    "cpp": {
        "compile": "g++ -std=c++23 -Wall -Wextra -Wshadow {file} -o {out}",
        "run": "{out}",
    },
    "c++": "@cpp",
    "cxx": "@cpp",
    "go": {"compile": "go build -o {out} {file}", "run": "{out}"},
    "hs": {"compile": "ghc -o {out} {file}", "run": "{out}"},
    "kt": {
        "compile": "kotlinc {file} -include-runtime -d {out_stem}.jar",
        "run": "java -jar {out_stem}.jar",
    },
    "nim": {"compile": "nim c --out:{out} {file}", "run": "{out}"},
    "rs": {"compile": "rustc {file} -o {out}", "run": "{out}"},
    "v": {"compile": "v -o {out} {file}", "run": "{out}"},
    "zig": {
        "compile": "zig build-exe {file} -femit-bin={out}",
        "run": "{out}",
    },
}
