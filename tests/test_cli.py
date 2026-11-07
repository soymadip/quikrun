from pathlib import Path
from unittest.mock import patch

import pytest

from quikrun.cli import create_cli_parser, run_cli
from quikrun.config.types import Config


def test_cli_help(capsys: pytest.CaptureFixture[str]) -> None:
    with patch("sys.argv", ["quikrun", "--help"]):
        with pytest.raises(SystemExit) as exc:
            run_cli()
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "usage: quikrun" in captured.out
        assert "-h, --help" in captured.out
        assert "-v, --version" in captured.out
        assert "--clear-terminal" in captured.out
        assert "--scroll-up" in captured.out
        assert "--no-show-command" in captured.out
        assert "--show-time-took" in captured.out
        assert "{auto,posix,cmd,pwsh}" in captured.out
        assert "{auto,linux,win,darwin}" in captured.out
        assert "{always,never,on_success}" in captured.out


def test_cli_defines_only_expected_short_options() -> None:
    parser = create_cli_parser()
    short_options = {
        option
        for action in parser._actions
        for option in action.option_strings
        if option.startswith("-") and not option.startswith("--")
    }

    assert short_options == {"-h", "-v", "-i", "-s", "-p"}


def test_cli_info(capsys: pytest.CaptureFixture[str]) -> None:
    with patch("sys.argv", ["quikrun", "--info"]):
        with pytest.raises(SystemExit) as exc:
            run_cli()
        assert exc.value.code == 0
        captured = capsys.readouterr()
        assert "quikrun v" in captured.out


def test_cli_no_args_exits_with_error(capsys: pytest.CaptureFixture[str]) -> None:
    with patch("sys.argv", ["quikrun"]):
        with pytest.raises(SystemExit) as exc:
            run_cli()
        assert exc.value.code == 1


def test_cli_passes_extra_config_flags() -> None:
    with (
        patch(
            "sys.argv",
            [
                "quikrun",
                "test.py",
                "-s",
                "posix",
                "-p",
                "linux",
                "--no-show-command",
                "--no-show-time-took",
                "--show-divider",
                "--scroll-up",
                "--cd-to-file-dir",
                "--cache-dir",
                "/tmp/cache",
                "--auto-exit",
                "always",
                "--",
                "--arg1",
                "val1",
            ],
        ),
        patch("quikrun.cli.quick_run", return_value=0) as mock_quick_run,
    ):
        with pytest.raises(SystemExit) as exc:
            run_cli()

        assert exc.value.code == 0
        mock_quick_run.assert_called_once()
        call_kwargs = mock_quick_run.call_args.kwargs
        target_path = call_kwargs["file_path"]
        extra_args = call_kwargs["file_args"]
        extra_config = call_kwargs["extra_config"]

        assert target_path == Path("test.py")
        assert extra_args == ["--", "--arg1", "val1"]
        assert isinstance(extra_config, Config)
        assert extra_config.shell == "posix"
        assert extra_config.platform == "linux"
        assert extra_config.show_command is False
        assert extra_config.show_time_took is False
        assert extra_config.show_divider is True
        assert extra_config.clear_terminal == "scroll_up"
        assert extra_config.cd_to_file_dir is True
        assert extra_config.cache_dir == "/tmp/cache"
        assert extra_config.auto_exit == "always"


def test_cli_accepts_long_config_flags() -> None:
    with (
        patch(
            "sys.argv",
            [
                "quikrun",
                "test.py",
                "--clear-terminal",
                "--show-time-took",
                "--keep-build-artifacts",
            ],
        ),
        patch("quikrun.cli.quick_run", return_value=0) as mock_quick_run,
    ):
        with pytest.raises(SystemExit) as exc:
            run_cli()

        assert exc.value.code == 0
        extra_config = mock_quick_run.call_args[1].get("extra_config")
        assert isinstance(extra_config, Config)
        assert extra_config.clear_terminal is True
        assert extra_config.show_command is None
        assert extra_config.show_time_took is True
        assert extra_config.keep_build_artifacts is True


def test_cli_no_show_command_hides_command() -> None:
    with (
        patch("sys.argv", ["quikrun", "test.py", "--no-show-command"]),
        patch("quikrun.cli.quick_run", return_value=0) as mock_quick_run,
    ):
        with pytest.raises(SystemExit) as exc:
            run_cli()

        assert exc.value.code == 0
        extra_config = mock_quick_run.call_args[1].get("extra_config")
        assert isinstance(extra_config, Config)
        assert extra_config.show_command is False


def test_cli_show_command_override() -> None:
    with (
        patch("sys.argv", ["quikrun", "test.py", "--show-command"]),
        patch("quikrun.cli.quick_run", return_value=0) as mock_quick_run,
    ):
        with pytest.raises(SystemExit) as exc:
            run_cli()

        assert exc.value.code == 0
        extra_config = mock_quick_run.call_args[1].get("extra_config")
        assert isinstance(extra_config, Config)
        assert extra_config.show_command is True


def test_cli_show_command_flags_are_mutually_exclusive() -> None:
    with patch(
        "sys.argv",
        ["quikrun", "test.py", "--no-show-command", "--show-command"],
    ):
        with pytest.raises(SystemExit) as exc:
            run_cli()

        assert exc.value.code == 2


def test_cli_without_flags_passes_none_extra_config() -> None:
    with (
        patch("sys.argv", ["quikrun", "main.py"]),
        patch("quikrun.cli.quick_run", return_value=0) as mock_quick_run,
    ):
        with pytest.raises(SystemExit) as exc:
            run_cli()

        assert exc.value.code == 0
        mock_quick_run.assert_called_once_with(
            file_path=Path("main.py"),
            file_args=[],
            extra_config=None,
        )