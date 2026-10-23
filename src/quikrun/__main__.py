"""Entry point for `python -m quikrun`."""

import sys

from .run import quick_run
lazy from .lib.logger import log


def main() -> None:
    try:
        sys.exit(quick_run())
    except KeyboardInterrupt:
        log.error("\n\nInterrupted by user! (Ctrl+C). Exiting....")
        sys.exit(130)


if __name__ == "__main__":
    main()
