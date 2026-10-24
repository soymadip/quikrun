"""quikrun — run your code files without hassle."""

import sys
from importlib import metadata
from importlib.metadata import PackageNotFoundError

from .runner import quick_run

__all__ = ["quick_run"]

if sys.version_info < (3, 15):  # noqa: UP036
    sys.stderr.write("Error: quikrun requires Python 3.15 or newer.\n")
    sys.exit(1)

try:
    __version__ = metadata.version("quikrun")
except PackageNotFoundError:
    __version__ = "unknown"
