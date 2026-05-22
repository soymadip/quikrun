"""quikrun — run your code files without hassle."""

import os
import shlex
import shutil
import subprocess
import sys
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any

from . import __version__
from .lib import config, logger
from .lib.utils import detect_shebang, get_out_path, resolve_template, run_cmd


def _build_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="quikrun",
        description="Run your code files without hassle.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument("file", help="Source file to run")

    return parser


def main() -> None:

    if sys.stdout.isatty():
        print()

    # No arguments given
    if len(sys.argv) == 1:
        _build_parser().print_help()
        sys.exit(0)

    parser: ArgumentParser = _build_parser()
    args: Namespace
    extra_args: list[str]
    args, extra_args = parser.parse_known_args()

    file: Path = Path(args.file.strip())

    # ---------------- Validation ---------------

    if not file.exists():
        logger.error(f"File not found: '{file}'")
        sys.exit(1)

    if not file.is_file():
        logger.error(f"'Not a file: '{file}'")
        sys.exit(1)

    # ---------------- Load Configuration ---------------

    cfg: dict[str, Any] = config.load()
    cmd_templates: dict[str, Any] = cfg.get("cmds", {})

    shell_name = "sh"
    platform_key = "linux"

    if sys.platform.startswith("win"):
        platform_key = "win"
    elif sys.platform == "darwin":
        platform_key = "darwin"

    # Resolve custom shell
    shell_cmd = cfg.get("shell")
    resolved_shell: str | None = None

    if shell_cmd is not None:
        if isinstance(shell_cmd, dict):
            resolved_shell = shell_cmd.get(platform_key, next(iter(shell_cmd.values())))
        else:
            resolved_shell = str(shell_cmd)

    # Determine shell family
    if resolved_shell:
        shell_path = shutil.which(resolved_shell) or resolved_shell
        shell_name = os.path.basename(shell_path).lower()
    elif os.name == "nt":
        shell_path = os.environ.get("COMSPEC", "cmd.exe")
        shell_name = os.path.basename(shell_path).lower()

    if any(s in shell_name for s in ["bash", "zsh", "dash", "ash", "sh"]):
        shell_family = "posix"
    elif any(s in shell_name for s in ["cmd"]):
        shell_family = "cmd"
    elif any(s in shell_name for s in ["pwsh"]):
        shell_family = "pwsh"
    else:
        shell_family = "cmd" if os.name == "nt" else "posix"

    # ---------------- Shebang detection ---------------

    if os.name == "posix":
        if shebang := detect_shebang(file):
            if cfg.get("clear_terminal"):
                os.system("cls" if os.name == "nt" else "clear")

            shebang_cmd_list: list[str] = shlex.split(shebang)
            full_cmd = [*shebang_cmd_list, str(file.resolve()), *extra_args]
            display_cmd_str = shlex.join([*shebang_cmd_list, str(file), *extra_args])

            start: float = time.perf_counter()
            result: CompletedProcess = subprocess.run(full_cmd)
            elapsed: float = time.perf_counter() - start

            if cfg.get("show_time_took") or cfg.get("show_command"):
                logger.footer(
                    elapsed,
                    result.returncode,
                    display_cmd_str if cfg.get("show_command") else None,
                    show_time=bool(cfg.get("show_time_took")),
                    is_shebang=True,
                )

            sys.exit(result.returncode)

    # ---------------- Extension lookup ---------------

    extension: str = file.suffix.lstrip(".")

    if not extension:
        logger.error(f"'{file}' has no extension or no shebang.")
        sys.exit(1)

    if extension not in cmd_templates:
        logger.error(f"Unsupported extension '.{extension}'.")
        logger.info(
            "Tip: Add a command template for this extension to your user or project quikrun.toml config."
        )
        sys.exit(1)

    raw_template: Any = cmd_templates[extension]

    # Recursively resolve and flatten all aliases, dictionaries, and arrays
    flattened_cmds: list[str] = resolve_template(
        raw_template, shell_family, platform_key, cmd_templates
    )

    if not flattened_cmds:
        logger.error(f"Invalid configuration for extension '.{extension}'.")
        sys.exit(1)

    # Resolve smart fallbacks by checking which executable is installed
    template: str = ""
    for cmd_tmpl in flattened_cmds:
        executable = cmd_tmpl.split()[0]
        if shutil.which(executable) is not None:
            template = cmd_tmpl
            break

    if not template:
        template = flattened_cmds[-1]

    file_q: str = shlex.quote(str(file.resolve()))  # absolute — for execution
    file_rel_q: str = shlex.quote(str(file))  # relative — for display only
    file_dir_q: str = shlex.quote(str(file.parent.resolve()))
    file_dir_rel_q: str = shlex.quote(str(file.parent))
    file_name_q: str = shlex.quote(file.name)
    file_stem_q: str = shlex.quote(file.stem)

    out_path: Path = get_out_path(file, temp_dir=cfg.get("temp_dir"))
    out_stem_path: Path = out_path.with_suffix("")
    out_q: str = shlex.quote(str(out_path))
    out_stem_q: str = shlex.quote(str(out_stem_path))

    # Fill in templates
    cmd: str = template.format(
        file=file_q,
        out=out_q,
        out_stem=out_stem_q,
        file_dir=file_dir_q,
        file_name=file_name_q,
        file_stem=file_stem_q,
    )
    display_cmd: str = template.format(
        file=file_rel_q,
        out=out_q,
        out_stem=out_stem_q,
        file_dir=file_dir_rel_q,
        file_name=file_name_q,
        file_stem=file_stem_q,
    )

    if extra_args:
        cmd += " " + shlex.join(extra_args)
        display_cmd += " " + shlex.join(extra_args)

    if cfg.get("cd_to_file_dir"):
        if shell_family == "cmd":
            cmd = f'cd /d "{file_dir_q}" && {cmd}'
            display_cmd = f'cd /d "{file_dir_rel_q}" && {display_cmd}'
        elif shell_family == "pwsh":
            cmd = f"cd '{file_dir_q}'; if ($?) {{ {cmd} }}"
            display_cmd = f"cd '{file_dir_rel_q}'; if ($?) {{ {display_cmd} }}"
        else:  # posix
            cmd = f"cd {file_dir_q} && {cmd}"
            display_cmd = f"cd {file_dir_rel_q} && {display_cmd}"

    if cfg.get("clear_terminal"):
        os.system("cls" if os.name == "nt" else "clear")

    exit_code = run_cmd(
        cmd,
        shell=resolved_shell,
        show_time=bool(cfg.get("show_time_took")),
        show_command=bool(cfg.get("show_command")),
        display_cmd=display_cmd,
        cwd=None,
        show_shell=bool(cfg.get("show_shell")),
    )

    # Clean up temporary compiled binary and related artifacts if configured to do so
    if not cfg.get("keep_artifacts"):
        try:
            parent_dir: Path = out_path.parent
            stem = out_path.stem

            if parent_dir.exists() and parent_dir.is_dir():
                for item in parent_dir.iterdir():
                    if item.stem == stem or item.name.startswith(stem + "."):
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)

            # Remove parent directory if it is empty
            if parent_dir.exists() and parent_dir.is_dir():
                if not any(parent_dir.iterdir()):
                    parent_dir.rmdir()

        except Exception:
            pass

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
