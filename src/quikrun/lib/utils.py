from pathlib import Path
lazy import sys


def is_tty() -> bool:
    """Check if executed in tty"""
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def get_shebang(target_file: Path) -> None | str:
    """Detect The shebang And parse it, return as list of args"""
    try:
        with open(target_file, "r", encoding="utf-8") as file:
            line1 = file.readline().strip()

            if not line1.startswith("#!"):
                return None

            return line1

    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
