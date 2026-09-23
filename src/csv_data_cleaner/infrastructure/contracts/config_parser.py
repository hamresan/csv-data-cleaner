"""Configuration file parser contract."""

from pathlib import Path
from typing import Protocol


class ConfigParser(Protocol):
    """Parse one configuration file into an untyped Python value."""

    def parse(self, path: Path) -> object: ...
