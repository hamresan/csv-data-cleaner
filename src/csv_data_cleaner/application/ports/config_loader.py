"""Configuration-loading boundary."""

from pathlib import Path
from typing import Protocol

from csv_data_cleaner.domain import ProcessingConfig


class ConfigLoader(Protocol):
    """Load and validate one supported configuration file."""

    def load(self, path: Path) -> ProcessingConfig: ...
