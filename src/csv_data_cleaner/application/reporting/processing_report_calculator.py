"""Calculate deterministic processing summaries."""

from pathlib import Path

from csv_data_cleaner.application.ports import ReportCalculator
from csv_data_cleaner.domain import DatasetProcessingResult, ProcessingSummary


class ProcessingReportCalculator(ReportCalculator):
    """Derive report counters exclusively from the pipeline result."""

    def calculate(
        self,
        input_path: Path,
        result: DatasetProcessingResult,
        output_file: Path,
    ) -> ProcessingSummary:
        return ProcessingSummary(
            input_file=input_path.name,
            processed_records=len(result.rows)
            + len(result.filtered_rows)
            + len(result.duplicate_rows),
            valid_records=len(result.all_valid_rows),
            invalid_records=len(result.all_invalid_rows),
            duplicate_records=len(result.duplicate_rows),
            exported_records=len(result.valid_rows),
            output_file=str(output_file),
        )
