import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from . import __version__
from .lib.logger import is_tty, log
from .runner import quick_run


def run_cli() -> None:
    """CLI wrapper for Quikrun"""
    try:
        if is_tty():
            print()

        parser: ArgumentParser = ArgumentParser(
            prog="quikrun", description="Run your code hassle free!"
        )

        parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s {__version__}"
        )

        parser.add_argument(
            "-i",
            "--info",
            action="store_true",
            help="Show project information, version, and repository details",
        )

        parser.add_argument("FILE", nargs="?", help="Target file's path to run")

        # If No arguments are given, print help
        if len(sys.argv) == 1:
            log.error("No Arguments are given!\n")
            parser.print_help()
            sys.exit(1)

        # Parse Given Arguments
        args: Namespace
        extra_args: list[str]

        args, extra_args = parser.parse_known_args()

        # --info flag
        if args.info:
            print(f"quikrun v{__version__}")
            print("Homepage: https://soymadip.github.io/quikrun")
            print("Project Repo: https://github.com/soymadip/quikrun")
            sys.exit(0)

        # Ensure a target file was provided if --info wasn't used
        if not args.FILE:
            log.error("Error: No target file specified!\n")
            parser.print_help()
            sys.exit(1)

        target_file: Path = Path(args.FILE.strip())

        # Run the file
        return_code: int = quick_run(target_file, extra_args if extra_args else None)

        sys.exit(return_code)

    except KeyboardInterrupt:
        log.error("\n\nInterrupted by user! (Ctrl+C). Exiting....")
        sys.exit(130)


if __name__ == "__main__":
    run_cli()
