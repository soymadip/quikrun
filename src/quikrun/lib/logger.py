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


def _c(text: str, *codes: str) -> str:
    """Wrap text in ANSI codes if stdout is a TTY."""
    if not _tty():
        return text
    return "".join(codes) + text + _RESET


# ---------------- Public API ---------------


def header(file: str, runner: str, cmd: str | None = None) -> None:
    """Print the execution banner before running the file."""
    print(
        _c("⚡ quikrun", _BOLD, _CYAN)
        + " → "
        + _c(file, _BOLD)
        + "  "
        + _c(f"[{runner}]", _DIM)
    )
    if cmd:
        print(_c(f"$ {cmd}", _DIM))
    print(_c("─" * 44, _DIM))


def footer(elapsed: float, exit_code: int) -> None:
    """Print the execution footer divider and exit status."""
    if _tty():
        print(_c("─" * 44, _DIM))
    if exit_code == 0:
        print(_c(":: ", _GREEN) + f"Execution succeeded in {elapsed:.3f}s")
    else:
        print(
            _c(":: ", _RED)
            + f"Execution failed in {elapsed:.3f}s (exit code: {exit_code})"
        )


def info(msg: str) -> None:
    print(_c(":: ", _CYAN) + msg)


def success(msg: str) -> None:
    print(_c("✓ ", _GREEN) + msg)


def warn(msg: str) -> None:
    print(_c("⚠ ", _YELLOW) + msg, file=sys.stderr)


def error(msg: str) -> None:
    print(_c("✗ ", _RED) + msg, file=sys.stderr)
