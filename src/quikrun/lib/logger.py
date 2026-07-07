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
_GRAY = "\033[90m"


def _tty() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def fmt(text: str, *codes: str) -> str:
    """Wrap text in ANSI codes if stdout is a TTY."""
    if not _tty():
        return text

    return "".join(codes) + text + _RESET


# ---------------- Public API ---------------


def footer(
    msg: str,
    *,
    succeeded: bool = True,
    elapsed_time: float | None = None,
    exit_code: int | None = None,
    cmd: str | None = None,
    shebang: bool = False,
    shell_cmd: str | None = None,
    show_divider: bool = True,
) -> None:
    """Print the execution footer divider and exit status."""

    if show_divider and _tty():
        print(fmt("-" * 43, _GRAY))

    time_str = (
        fmt(f" [took {elapsed_time:.3f}s]", _GRAY) if elapsed_time is not None else ""
    )
    color = _GREEN if succeeded else _RED

    exit_str = ""

    if exit_code is not None:
        exit_color = _GRAY if exit_code == 0 else _RED
        exit_str = fmt(f" [exit code {exit_code}]", exit_color)

    print(fmt(f"⏵ {msg}", color) + exit_str + time_str)

    if cmd:
        via_str = f" [via {shell_cmd}]" if shell_cmd else ""
        prefix = "⏵ Command [shebang]: " if shebang else "⏵ Command: "
        print(fmt(prefix, _CYAN) + fmt(cmd, _GRAY) + fmt(via_str, _GRAY))
    elif shell_cmd:
        print(fmt("⏵ Shell: ", _CYAN) + fmt(shell_cmd, _GRAY))


def info(msg: str) -> None:
    print(fmt(":: ", _CYAN) + msg)


def success(msg: str) -> None:
    print(fmt("✓ ", _GREEN) + msg)


def warn(msg: str) -> None:
    print(fmt("⚠ ", _YELLOW) + msg, file=sys.stderr)


def error(msg: str) -> None:
    print(fmt("✗ ", _RED) + msg, file=sys.stderr)
