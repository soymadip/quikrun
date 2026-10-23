import sys
from typing import Literal

from .utils import is_tty


class Logger:
    __col = frozendict(
        RESET="\033[0m",
        BOLD="\033[1m",
        DIM="\033[2m",
        RED="\033[31m",
        GREEN="\033[32m",
        YELLOW="\033[33m",
        CYAN="\033[36m",
        GRAY="\033[90m",
    )

    def __fmt(self, text: str, color: str) -> str:
        """Wrap text in ANSI codes if stdout is a TTY."""
        if not is_tty():  # pyright: ignore[reportCallIssue]
            color = ""

        return self.__col.get(color, "") + text + self.__col["RESET"]

    def __log(self, msg: str, level: Literal["info", "success", "warn", "error"]):
        match level:
            case "info":
                prefix: str = "!"
                color: str = " "
            case "success":
                prefix = "✓"
                color = "GREEN"
            case "warn":
                prefix = "⚠"
                color = "YELLOW"
            case "error":
                prefix = "✗"
                color = "RED"

        print(self.__fmt(f"{prefix} {msg}", color), file=sys.stderr)

    def info(self, msg: str) -> None:
        self.__log(msg, "info")

    def success(self, msg: str) -> None:
        self.__log(msg, "success")

    def warn(self, msg: str) -> None:
        self.__log(msg, "warn")

    def error(self, msg: str) -> None:
        self.__log(msg, "error")

    def footer(self) -> None:
        raise NotImplementedError


log = Logger()
