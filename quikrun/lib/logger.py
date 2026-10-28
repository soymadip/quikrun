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
        self, level: Literal["info", "success", "warn", "error", "dim"], *msgs: str
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

        to_print = log.fmt(prefix, color)

        for msg in msgs:
            to_print += " "
            to_print += self.fmt(msg, color)

        print(to_print, file=sys.stderr)

    def info(self, *msg: str) -> None:
        self.__log("info", *msg)

    def success(self, *msg: str) -> None:
        self.__log("success", *msg)

    def warn(self, *msg: str) -> None:
        self.__log("warn", *msg)

    def error(self, *msg: str) -> None:
        self.__log("error", *msg)

    def dim(self, *msg: str) -> None:
        self.__log("dim", *msg)


# Make a Logger object
log = Logger()
