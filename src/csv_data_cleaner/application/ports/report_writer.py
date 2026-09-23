"""Processing report persistence boundary."""

from pathlib import Path
from typing import Protocol

from csv_data_cleaner.domain import ProcessingSummary


class ReportWriter(Protocol):
    """Persist a processing summary without exposing serialization details."""

    def write(self, summary: ProcessingSummary, output_dir: Path) -> Path: ...
