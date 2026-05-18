import os
import sys
import stat
import subprocess

EXT_MAP = {
    "py": ["python3"],
    "js": ["node"],
    "ts": ["ts-node"],
    "lua": ["lua"],
    "rb": ["ruby"],
    "go": ["go", "run"],
    "sh": ["bash"],
    "bash": ["bash"],
    "zsh": ["zsh"],
}

def has_shebang(filepath: str) -> bool:
    with open(filepath, "rb") as f:
        return f.read(2) == b"#!"

def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] == "-h":
        print("Usage: run-code <filename> [-c <command>]")
        return

    filepath = args[0]

    if not os.path.isfile(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    print("\n\n")

    if has_shebang(filepath):
        print(":: Executing via shebang...")
        os.chmod(filepath, os.stat(filepath).st_mode | stat.S_IEXEC)
        os.execv(filepath, [filepath])

    ext = filepath.rsplit(".", 1)[-1]

    if ext in EXT_MAP:
        subprocess.run(EXT_MAP[ext] + [filepath])
    else:
        print(f"Error: Extension '.{ext}' is unsupported.")
        print(f"Try: run-code {filepath} -c <command>")
        sys.exit(1)

if __name__ == "__main__":
    main()
