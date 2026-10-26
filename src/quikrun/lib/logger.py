import sys
from typing import Literal


def is_tty() -> bool:
    """Check if executed in tty"""
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


type Color = Literal[
    "RESET",
    "BOLD",
    "DIM",
    "RED",
    "GREEN",
    "YELLOW",
    "CYAN",
    "GRAY",
    "BLUE",
]


class Logger:
    def __init__(self) -> None:
        self.__col: dict[Color, str] = {
            "RESET": "\033[0m",
            "BOLD": "\033[1m",
            "DIM": "\033[2m",
            "RED": "\033[31m",
            "GREEN": "\033[32m",
            "YELLOW": "\033[33m",
            "CYAN": "\033[36m",
            "GRAY": "\033[90m",
            "BLUE": "\033[34m",
        }

    def fmt(self, text: str, color: Color) -> str:
        """Wrap text in ANSI color codes if stdout is a TTY."""
        if not is_tty():
            color = "RESET"

        return self.__col.get(color, "") + text + self.__col["RESET"]

    def __log(
        self, msg: str, level: Literal["info", "success", "warn", "error", "dim"]
    ):
        """Internal Central Logging Function"""
        match level:
            case "info":
                prefix: str = "i"
                color: Color = "BLUE"
            case "success":
                prefix = "✓"
                color = "GREEN"
            case "warn":
                prefix = "⚠"
                color = "YELLOW"
            case "error":
                prefix = "✗"
                color = "RED"
            case "dim":
                prefix = "⏵"
                color = "GRAY"

        print(self.fmt(f"{prefix} {msg}", color), file=sys.stderr)

    def info(self, msg: str) -> None:
        self.__log(msg, "info")

    def success(self, msg: str) -> None:
        self.__log(msg, "success")

    def warn(self, msg: str) -> None:
        self.__log(msg, "warn")

    def error(self, msg: str) -> None:
        self.__log(msg, "error")

    def dim(self, msg: str) -> None:
        self.__log(msg, "dim")


# Make a Logger object
log = Logger()
