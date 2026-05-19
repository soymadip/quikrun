"""Built-in extension → command mappings for quikrun.

Template placeholders:
  {file}  — shell-quoted absolute path to the source file
  {out}   — shell-quoted path to the compiled output binary
"""

RUNNERS: dict[str, str | list[str] | dict[str, str | list[str]]] = {
    #
    # ---------------- Interpreted ---------------
    "js": ["bun run {file}", "deno run {file}", "node {file}"],
    "ts": ["@js", "ts-node {file}"],
    "lua": "lua {file}",
    "rb": "ruby {file}",
    "go": "go run {file}",
    "sh": "bash {file}",
    "bash": "bash {file}",
    "zsh": "zsh {file}",
    "py": {
        "posix": "python3 {file}",
        "win": "python {file}",
    },
    #
    # ---------------- Compiled ---------------
    "rs": "rustc {file} -o {out} && {out}",
    "c": "gcc {file} -o {out} && {out}",
    "cpp": "g++ {file} -o {out} && {out}",
    "cxx": "@cpp",
    "c++": "@cpp",
}
