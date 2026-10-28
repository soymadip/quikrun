#!/usr/bin/env python3
from dataclasses import asdict
from pathlib import Path
from tomli_w import dump
import sys


# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from quikrun.config.defaults import DEFAULT_CONF


with open("default_config.toml", "wb" ) as f:
    dump(asdict(DEFAULT_CONF), f)
