"""Input-reading boundary."""

from pathlib import Path
from typing import Protocol

from csv_data_cleaner.domain import InputData


class InputReader(Protocol):
    """Read one supported tabular input into the canonical domain model."""

    def read(self, path: Path, *, sheet: str | None = None) -> InputData: ...
