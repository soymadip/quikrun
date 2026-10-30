"""quikrun — run your code files without hassle."""

import sys
from importlib import metadata
from importlib.metadata import PackageNotFoundError

from .config.types import Config
from .runner import quick_run

__all__ = ["Config", "quick_run"]

__version__ = "3.1.2"

if sys.version_info < (3, 14):  # noqa: UP036
    sys.stderr.write("Error: quikrun requires Python 3.14 or newer.\n")
    sys.exit(1)

try:
    __version__ = metadata.version("quikrun")
except PackageNotFoundError:
    pass