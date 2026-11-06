import sys
from argparse import ArgumentParser, BooleanOptionalAction, Namespace
from pathlib import Path
from typing import get_args

from quikrun.config.types import AutoExit, Config, Platform, Shell

from . import __version__
from .lib.logger import is_tty, log
from .runner import quick_run


def create_cli_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="quikrun", description="Run your code hassle free!")

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Print the version and exit.",
    )

    parser.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="Show project information, version, and repository details",
    )

    parser.add_argument("FILE", nargs="?", help="Target file's path to run")

    parser.add_argument(
        "-s",
        "--shell",
        choices=get_args(Shell.__value__),
        default=None,
        help="Which shell to use.",
    )

    parser.add_argument(
        "-p",
        "--platform",
        choices=get_args(Platform.__value__),
        default=None,
        help="Target platform or OS override.",
    )

    clear_term_group = parser.add_mutually_exclusive_group()
    clear_term_group.add_argument(
        "--clear-terminal",
        action=BooleanOptionalAction,
        default=None,
        help="Clear the terminal before running.",
    )
    clear_term_group.add_argument(
        "--scroll-up",
        action="store_const",
        const="scroll_up",
        dest="clear_terminal",
        default=None,
        help="Scroll the terminal up instead of clearing it.",
    )

    show_command_group = parser.add_mutually_exclusive_group()
    show_command_group.add_argument(
        "--show-command",
        action="store_true",
        default=None,
        help="Show the command in the footer.",
    )
    show_command_group.add_argument(
        "--no-show-command",
        dest="show_command",
        action="store_false",
        default=None,
        help="Do not show the command in the footer.",
    )

    parser.add_argument(
        "--show-time-took",
        action=BooleanOptionalAction,
        default=None,
        help="Whether to display the execution duration at footer.",
    )

    parser.add_argument(
        "--show-divider",
        action=BooleanOptionalAction,
        default=None,
        help="Whether to print the separation line before the footer.",
    )

    parser.add_argument(
        "--cd-to-file-dir",
        action=BooleanOptionalAction,
        default=None,
        help="Whether to change the working directory to the target file's folder before running/compiling.",
    )

    parser.add_argument(
        "--keep-build-artifacts",
        action=BooleanOptionalAction,
        default=None,
        help="Whether to retain temporary or compiled binaries after execution completes.",
    )

    parser.add_argument(
        "--cache-dir",
        metavar="path",
        default=None,
        help="Custom directory used for cache and compiled build artifacts.",
    )
    parser.add_argument(
        "--auto-exit",
        choices=get_args(AutoExit.__value__),
        default=None,
        help="Controls automatic process exit behavior.",
    )

    return parser


def run_cli() -> None:
    """CLI wrapper for Quikrun"""
    try:
        if is_tty():
            print()

        parser = create_cli_parser()

        # If No arguments are given, print help
        if len(sys.argv) == 1:
            log.error("No Arguments are given!\n")
            parser.print_help()
            sys.exit(1)

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

        # --------------- Make Config overrides -------------------

        cli_config_kwargs = {
            k: v
            for k, v in vars(args).items()
            if k in Config.__dataclass_fields__ and v is not None
        }

        cli_config: Config | None = (
            Config(**cli_config_kwargs) if cli_config_kwargs else None
        )

        # ---------------- Run the File With Quikrun ----------------#

        return_code = quick_run(
            file_path=target_file,
            file_args=extra_args,
            extra_config=cli_config,
        )

        sys.exit(return_code)

    except KeyboardInterrupt:
        log.error("\n\nInterrupted by user! (Ctrl+C). Exiting....")
        sys.exit(130)


if __name__ == "__main__":
    run_cli()
