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

from .lib import config, logger
from .lib.utils import (
    arg_parser,
    detect_shebang,
    get_out_path,
    resolve_template,
    run_cmd,
)


def main() -> None:

    if sys.stdout.isatty():
        print()

    # No arguments given
    if len(sys.argv) == 1:
        arg_parser().print_help()
        sys.exit(0)

    parser: ArgumentParser = arg_parser()
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
    cmd_templates: dict[str, Any] = cfg.get("commands", {})

    if sys.platform.startswith("win"):
        platform_key = "win"
    elif sys.platform == "darwin":
        platform_key = "darwin"
    else:
        platform_key = "linux"

    # Resolve custom shell
    shell_cmd = cfg.get("shell")
    resolved_shell: str | None = None

    if shell_cmd is not None:
        if isinstance(shell_cmd, dict):
            resolved_shell = shell_cmd.get(platform_key)
        else:
            resolved_shell = str(shell_cmd)

    # Determine shell name
    shell_name: str

    if resolved_shell:
        shell_path = shutil.which(resolved_shell) or resolved_shell
        shell_name = os.path.basename(shell_path).lower()
    elif os.name == "nt":
        shell_path = os.environ.get("COMSPEC", "cmd.exe")
        shell_name = os.path.basename(shell_path).lower()
    else:
        shell_name = "sh"

    # Determine shell family
    if any(shell in shell_name for shell in ["bash", "zsh", "dash", "ash", "sh"]):
        shell_family = "posix"
    elif "cmd" in shell_name:
        shell_family = "cmd"
    elif any(s in shell_name for s in ["pwsh"]):
        shell_family = "pwsh"
    else:
        shell_family = "cmd" if os.name == "nt" else "posix"

    # ---------------- Shebang detected ---------------

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

            if (
                cfg.get("show_time_took")
                or cfg.get("show_command")
                or cfg.get("show_shell")
            ):
                logger.footer(
                    "Ran Successfully" if result.returncode == 0 else "Failed to Run",
                    succeeded=(result.returncode == 0),
                    exit_code=result.returncode,
                    elapsed_time=elapsed if cfg.get("show_time_took") else None,
                    cmd=display_cmd_str if cfg.get("show_command") else None,
                    shebang=True,
                    show_divider=bool(cfg.get("show_divider")),
                )

            sys.exit(result.returncode)

    # ---------------- Extension lookup ---------------

    extension: str = file.suffix.lstrip(".")

    if not extension:
        logger.error(f"'{file}' has no extension nor shebang.")
        sys.exit(1)

    if extension not in cmd_templates:
        logger.error(f"Unsupported extension '.{extension}'.")
        logger.info(
            "Tip: Add a command template for this extension to your user or project quikrun.toml config."
        )
        sys.exit(1)

    raw_template: Any = cmd_templates[extension]

    # Recursively resolve and flatten all aliases, dictionaries, and arrays
    flattened_cmds: list[Any] = resolve_template(
        raw_template, shell_family, platform_key, cmd_templates
    )

    if not flattened_cmds:
        logger.error(f"Invalid configuration for extension '.{extension}'.")
        sys.exit(1)

    # Resolve smart fallbacks by checking which executable is installed
    template: Any = ""
    for cmd_tmpl in flattened_cmds:
        if isinstance(cmd_tmpl, dict):
            cmd_str = cmd_tmpl.get("compile") or cmd_tmpl.get("run", "")
        else:
            cmd_str = cmd_tmpl

        if cmd_str:
            parts = cmd_str.split()
            if parts:
                executable = parts[0]
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

    cwd_arg: str | None = None
    if cfg.get("cd_to_file_dir"):
        cwd_arg = str(file.parent.resolve())

    compile_tmpl = template.get("compile", "") if isinstance(template, dict) else ""
    run_tmpl = template.get("run", "") if isinstance(template, dict) else template

    def format_cmd(tmpl: str, for_display: bool = False) -> str:
        if not tmpl:
            return ""
        return tmpl.format(
            file=file_rel_q if for_display else file_q,
            out=out_q,
            out_stem=out_stem_q,
            file_dir=file_dir_rel_q if for_display else file_dir_q,
            file_name=file_name_q,
            file_stem=file_stem_q,
        )

    if compile_tmpl:
        compile_cmd = format_cmd(compile_tmpl)
        compile_display_cmd = format_cmd(compile_tmpl, for_display=True)

        # Run compile command
        kwargs: dict[str, Any] = {"shell": True}
        if resolved_shell is not None:
            kwargs["executable"] = resolved_shell
        if cwd_arg is not None:
            kwargs["cwd"] = cwd_arg

        compile_start: float = time.perf_counter()
        compile_result = subprocess.run(compile_cmd, **kwargs)
        compile_elapsed: float = time.perf_counter() - compile_start

        if compile_result.returncode != 0:
            if (
                cfg.get("show_time_took")
                or cfg.get("show_command")
                or cfg.get("show_shell")
            ):
                shell_path = None
                if cfg.get("show_shell"):
                    raw_shell = (
                        resolved_shell
                        if resolved_shell is not None
                        else (
                            os.environ.get("COMSPEC", "cmd.exe")
                            if os.name == "nt"
                            else "/bin/sh"
                        )
                    )
                    shell_path = shutil.which(raw_shell) or raw_shell

                logger.footer(
                    "Failed to Compile",
                    succeeded=False,
                    elapsed_time=compile_elapsed if cfg.get("show_time_took") else None,
                    exit_code=compile_result.returncode,
                    cmd=compile_display_cmd if cfg.get("show_command") else None,
                    shell_cmd=shell_path,
                    show_divider=bool(cfg.get("show_divider")),
                )

            sys.exit(compile_result.returncode)

    exit_code = 0
    if run_tmpl:
        run_cmd_str = format_cmd(run_tmpl)
        run_display_cmd = format_cmd(run_tmpl, for_display=True)

        if extra_args:
            run_cmd_str += " " + shlex.join(extra_args)
            run_display_cmd += " " + shlex.join(extra_args)

        if cfg.get("clear_terminal"):
            os.system("cls" if os.name == "nt" else "clear")

        exit_code = run_cmd(
            run_cmd_str,
            shell=resolved_shell,
            show_time=bool(cfg.get("show_time_took")),
            show_command=bool(cfg.get("show_command")),
            display_cmd=run_display_cmd,
            cwd=cwd_arg,
            show_shell=bool(cfg.get("show_shell")),
            show_divider=bool(cfg.get("show_divider")),
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
