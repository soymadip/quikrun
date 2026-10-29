#!/usr/bin/env python3
import argparse
from dataclasses import asdict
from pathlib import Path
from tomli_w import dump
import sys

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from quikrun.config.defaults import DEFAULT_CONF

def main():
    parser = argparse.ArgumentParser(description="Generate default quikrun configuration TOML.")
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=Path("default_config.toml"),
        help="Path where the default config TOML file should be written",
    )
    args = parser.parse_args()

    # Ensure parent directories exist if a nested path is passed
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with open(args.output, "wb") as f:
        dump(asdict(DEFAULT_CONF), f)
    
    print(f"Generated default config at: {args.output}")

if __name__ == "__main__":
    main()