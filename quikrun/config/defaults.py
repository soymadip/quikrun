from . import Config

DEFAULT_CONF: Config = Config(
    commands={
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
)
