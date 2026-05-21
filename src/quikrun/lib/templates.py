"""Built-in extension → command mappings for quikrun.

Template placeholders:
  {file}  — shell-quoted absolute path to the source file
  {out}   — shell-quoted path to the compiled output binary
"""

from typing import Any

CMD_TEMPLATES: dict[str, Any] = {
    #
    # ---------------- Interpreted ---------------
    "js": ["bun run {file}", "deno run {file}", "node {file}"],
    "mjs": "@js",
    "cjs": "@js",
    "ts": ["@js", "ts-node {file}"],
    "mts": "@ts",
    "lua": "lua {file}",
    "rb": "ruby {file}",
    "go": "go run {file}",
    "sh": "bash {file}",
    "bash": "bash {file}",
    "zsh": "zsh {file}",
    "fish": "fish {file}",
    "php": "php {file}",
    "pl": "perl {file}",
    "r": "Rscript {file}",
    "java": "java {file}",
    "swift": "swift {file}",
    "dart": "dart run {file}",
    "jl": "julia {file}",
    "py": {
        "posix": {
            "linux": "python3 {file}",
            "darwin": "python3 {file}",
            "win": "python {file}",
        },
        "cmd": "python {file}",
        "pwsh": "python {file}",
    },
    #
    # ---------------- Compiled ---------------
    "rs": "rustc {file} -o {out} && {out}",
    "c": "gcc {file} -o {out} && {out}",
    "cpp": "g++ {file} -o {out} && {out}",
    "cxx": "@cpp",
    "c++": "@cpp",
    "nim": "nim c --out:{out} {file} && {out}",
    "zig": "zig build-exe {file} -femit-bin={out} && {out}",
    "v": "v -o {out} {file} && {out}",
    "hs": "ghc -o {out} {file} && {out}",
    "kt": "kotlinc {file} -include-runtime -d {out}.jar && java -jar {out}.jar",
}
