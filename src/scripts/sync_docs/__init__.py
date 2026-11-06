import re
import subprocess
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[3]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .constants import NAME_MAP, TYPE_DISPLAY_NAMES
from .formatters import (
    format_command_value,
    format_type_hint,
    is_compiled_config,
)
from .generators import (
    generate_cli_flags_table,
    generate_command_tables,
    generate_config_ref_table,
    generate_variables_table,
)

DOCS_MD_DIR = PROJECT_ROOT / "docs" / "md"


def sync_cli_docs() -> None:
    CLI_DOCS_FILE = DOCS_MD_DIR / "usage.md"
    cli_flags_md = generate_cli_flags_table()

    if CLI_DOCS_FILE.exists():
        content = CLI_DOCS_FILE.read_text("utf-8")
        content = re.sub(
            r"<!-- DYNAMIC_CLI_FLAGS_START -->.*?<!-- DYNAMIC_CLI_FLAGS_END -->",
            f"<!-- DYNAMIC_CLI_FLAGS_START -->\n\n{cli_flags_md.strip()}\n\n<!-- DYNAMIC_CLI_FLAGS_END -->",
            content,
            flags=re.DOTALL,
        )

        CLI_DOCS_FILE.write_text(content, "utf-8")
        print(f"Synchronized {CLI_DOCS_FILE.name}")
    else:
        print(f"Warning: Could not find {CLI_DOCS_FILE}", file=sys.stderr)


def sync_variables_docs() -> None:
    CUSTOMIZING_CMDS_FILE = DOCS_MD_DIR / "customizing-cmds.md"

    variables_md = generate_variables_table()

    if CUSTOMIZING_CMDS_FILE.exists():
        content = CUSTOMIZING_CMDS_FILE.read_text("utf-8")
        content = re.sub(
            r"<!-- DYNAMIC_VARIABLES_START -->.*?<!-- DYNAMIC_VARIABLES_END -->",
            f"<!-- DYNAMIC_VARIABLES_START -->\n\n{variables_md.strip()}\n\n<!-- DYNAMIC_VARIABLES_END -->",
            content,
            flags=re.DOTALL,
        )

        CUSTOMIZING_CMDS_FILE.write_text(content, "utf-8")
        print(f"Synchronized {CUSTOMIZING_CMDS_FILE.name}")
    else:
        print(f"Warning: Could not find {CUSTOMIZING_CMDS_FILE}", file=sys.stderr)


def sync_commands_docs() -> None:
    interpreted_md, compiled_md = generate_command_tables()

    # Support default-cmds.md (new) or fallback to supported-languages.md (legacy)
    docs_dir = DOCS_MD_DIR

    DEFAULT_CMDS_FILE = docs_dir / "default-cmds.md"

    if not DEFAULT_CMDS_FILE.exists():
        legacy_path = docs_dir / "supported-languages.md"
        if legacy_path.exists():
            DEFAULT_CMDS_FILE = legacy_path

    if DEFAULT_CMDS_FILE.exists():
        content = DEFAULT_CMDS_FILE.read_text("utf-8")
        content = re.sub(
            r"<!-- DYNAMIC_INTERPRETED_START -->.*?<!-- DYNAMIC_INTERPRETED_END -->",
            f"<!-- DYNAMIC_INTERPRETED_START -->\n\n{interpreted_md.strip()}\n\n<!-- DYNAMIC_INTERPRETED_END -->",
            content,
            flags=re.DOTALL,
        )
        content = re.sub(
            r"<!-- DYNAMIC_COMPILED_START -->.*?<!-- DYNAMIC_COMPILED_END -->",
            f"<!-- DYNAMIC_COMPILED_START -->\n\n{compiled_md.strip()}\n\n<!-- DYNAMIC_COMPILED_END -->",
            content,
            flags=re.DOTALL,
        )

        DEFAULT_CMDS_FILE.write_text(content, "utf-8")
        print(f"Synchronized {DEFAULT_CMDS_FILE.name}")

    else:
        print(f"Warning: Could not find {DEFAULT_CMDS_FILE}", file=sys.stderr)


def sync_config_docs() -> None:
    CONFIG_DOCS_FILE = DOCS_MD_DIR / "configuration.md"

    config_ref_md = generate_config_ref_table()

    if CONFIG_DOCS_FILE.exists():
        content = CONFIG_DOCS_FILE.read_text("utf-8")
        content = re.sub(
            r"<!-- DYNAMIC_CONFIG_REF_START -->.*?<!-- DYNAMIC_CONFIG_REF_END -->",
            f"<!-- DYNAMIC_CONFIG_REF_START -->\n\n{config_ref_md.strip()}\n\n<!-- DYNAMIC_CONFIG_REF_END -->",
            content,
            flags=re.DOTALL,
        )

        CONFIG_DOCS_FILE.write_text(content, "utf-8")
        print(f"Synchronized {CONFIG_DOCS_FILE.name}")
    else:
        print(f"Warning: Could not find {CONFIG_DOCS_FILE}", file=sys.stderr)


def main() -> None:
    sync_commands_docs()
    sync_cli_docs()
    sync_config_docs()
    sync_variables_docs()
    subprocess.run(["prettier", "--write", str(DOCS_MD_DIR)], check=True)
    print("Successfully finished documentation synchronization!")


__all__ = [
    "NAME_MAP",
    "TYPE_DISPLAY_NAMES",
    "format_command_value",
    "format_type_hint",
    "generate_cli_flags_table",
    "generate_command_tables",
    "generate_config_ref_table",
    "generate_variables_table",
    "is_compiled_config",
    "main",
    "sync_cli_docs",
    "sync_commands_docs",
    "sync_config_docs",
    "sync_variables_docs",
]
