"""Pipeline export boundary."""

from pathlib import Path
from typing import Protocol

from csv_data_cleaner.domain import DatasetProcessingResult, ProcessingConfig


class Exporter(Protocol):
    """Export pipeline results without exposing infrastructure details."""

    def export(
        self,
        result: DatasetProcessingResult,
        config: ProcessingConfig,
        output_dir: Path,
    ) -> None: ...
