"""Processing report calculation boundary."""

from pathlib import Path
from typing import Protocol

from csv_data_cleaner.domain import DatasetProcessingResult, ProcessingSummary


class ReportCalculator(Protocol):
    """Calculate a processing summary from final pipeline results."""

    def calculate(
        self,
        input_path: Path,
        result: DatasetProcessingResult,
        output_file: Path,
    ) -> ProcessingSummary: ...
