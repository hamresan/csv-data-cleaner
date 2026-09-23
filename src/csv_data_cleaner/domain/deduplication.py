"""Deduplication result domain models."""

from dataclasses import dataclass

from csv_data_cleaner.domain.input_data import CellValue
from csv_data_cleaner.domain.row_processing import RowProcessingResult


@dataclass(frozen=True, slots=True)
class DuplicateRow:
    """A dropped duplicate row linked to the retained row and duplicate key."""

    row: RowProcessingResult
    retained_row_number: int
    key: tuple[CellValue, ...]


@dataclass(frozen=True, slots=True)
class DeduplicationResult:
    """Partition row results into retained rows and dropped duplicates."""

    retained_rows: tuple[RowProcessingResult, ...]
    duplicate_rows: tuple[DuplicateRow, ...]
