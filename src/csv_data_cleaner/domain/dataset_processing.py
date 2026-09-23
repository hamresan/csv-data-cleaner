"""Dataset processing result domain models."""

from dataclasses import dataclass

from csv_data_cleaner.domain.deduplication import DuplicateRow
from csv_data_cleaner.domain.row_processing import RowProcessingResult


@dataclass(frozen=True, slots=True)
class DatasetProcessingResult:
    """Separate retained and duplicate rows while preserving row results."""

    rows: tuple[RowProcessingResult, ...]
    duplicate_rows: tuple[DuplicateRow, ...] = ()

    @property
    def valid_rows(self) -> tuple[RowProcessingResult, ...]:
        """Return retained valid row results in source order."""

        return tuple(row for row in self.rows if row.is_valid)

    @property
    def invalid_rows(self) -> tuple[RowProcessingResult, ...]:
        """Return retained invalid row results in source order."""

        return tuple(row for row in self.rows if not row.is_valid)
