#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from pydantic import TypeAdapter

# Resolve project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from quikrun.config.types import Config


def main() -> None:
    adapter = TypeAdapter(Config)
    config_schema_dict = adapter.json_schema()
    config_schema_dict["$id"] = "https://www.schemastore.org/quikrun.json"

    output_path = PROJECT_ROOT / "quikrun.json"
    output_path.write_text(
        json.dumps(config_schema_dict, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Generated schema at {output_path}")


if __name__ == "__main__":
    main()
