"""Centralized terminal output for quikrun.

All user-facing messages go through this module — no bare print() elsewhere.
"""

import sys

# ---------------- ANSI escape codes ---------------
_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"
_RED = "\033[31m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_CYAN = "\033[36m"


def _tty() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def fmt(text: str, *codes: str) -> str:
    """Wrap text in ANSI codes if stdout is a TTY."""
    if not _tty():
        return text

    return "".join(codes) + text + _RESET


# ---------------- Public API ---------------


def footer(
    elapsed: float,
    exit_code: int,
    cmd: str | None = None,
    show_time: bool = True,
    is_shebang: bool = False,
    shell_path: str | None = None,
) -> None:
    """Print the execution footer divider and exit status."""
    if _tty():
        print(fmt("-" * 43, _DIM))

    time_str = fmt(f" (in {elapsed:.1f}s)", _DIM) if show_time else ""

    if exit_code == 0:
        print(fmt("⏵ Ran successfully", _GREEN) + time_str)
    else:
        print(fmt(f"⏵ Failed with exit code {exit_code}", _RED) + time_str)

    if shell_path:
        print(fmt("⏵ Shell: ", _CYAN) + fmt(shell_path, _DIM))

    if cmd:
        prefix = "⏵ Command (shebang): " if is_shebang else "⏵ Command: "
        print(fmt(prefix, _CYAN) + fmt(cmd, _DIM))


def info(msg: str) -> None:
    print(fmt(":: ", _CYAN) + msg)


def success(msg: str) -> None:
    print(fmt("✓ ", _GREEN) + msg)


def warn(msg: str) -> None:
    print(fmt("⚠ ", _YELLOW) + msg, file=sys.stderr)


def error(msg: str) -> None:
    print(fmt("✗ ", _RED) + msg, file=sys.stderr)
