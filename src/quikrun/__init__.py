"""quikrun — run your code files without hassle."""

import importlib.metadata
import sys

version = sys.version_info


if version < (3, 15):
    sys.stderr.write("Error: quikrun requires Python 3.14 or newer.\n")
    sys.exit(1)

try:
    __version__ = importlib.metadata.version("quikrun")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
