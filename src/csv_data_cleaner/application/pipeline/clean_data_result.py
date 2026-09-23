"""Pipeline output result."""

from dataclasses import dataclass

from csv_data_cleaner.domain import DatasetProcessingResult, ProcessingSummary


@dataclass(frozen=True, slots=True)
class CleanDataResult:
    """Return both detailed processing data and calculated summary."""

    processing_result: DatasetProcessingResult
    summary: ProcessingSummary
