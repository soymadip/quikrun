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
    "c": "gcc -Wall -Wextra {file} -o {out} && {out}",
    "cpp": "g++ -std=c++23 -Wall -Wextra -Wshadow {file} -o {out} && {out}",
    "c++": "@cpp",
    "cxx": "@cpp",
    "go": "go build {file} -o {out} && {out}",
    "hs": "ghc -o {out} {file} && {out}",
    "kt": "kotlinc {file} -include-runtime -d {out_stem}.jar && java -jar {out_stem}.jar",
    "nim": "nim c --out:{out} {file} && {out}",
    "rs": "rustc {file} -o {out} && {out}",
    "v": "v -o {out} {file} && {out}",
    "zig": "zig build-exe {file} -femit-bin={out} && {out}",
}
