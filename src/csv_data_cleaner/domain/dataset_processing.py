"""Dataset processing result domain models."""

from dataclasses import dataclass

from csv_data_cleaner.domain.deduplication import DuplicateRow
from csv_data_cleaner.domain.row_processing import RowProcessingResult


@dataclass(frozen=True, slots=True)
class DatasetProcessingResult:
    """Separate retained, duplicate, and filtered rows."""

    rows: tuple[RowProcessingResult, ...]
    duplicate_rows: tuple[DuplicateRow, ...] = ()
    filtered_rows: tuple[RowProcessingResult, ...] = ()
    columns: tuple[str, ...] = ()

    @property
    def valid_rows(self) -> tuple[RowProcessingResult, ...]:
        """Return retained valid row results in pipeline order."""

        return tuple(row for row in self.rows if row.is_valid)

    @property
    def invalid_rows(self) -> tuple[RowProcessingResult, ...]:
        """Return retained invalid row results in pipeline order."""

        return tuple(row for row in self.rows if not row.is_valid)

    @property
    def all_invalid_rows(self) -> tuple[RowProcessingResult, ...]:
        """Return every non-duplicate invalid row, including filtered rows."""

        filtered_invalid = tuple(row for row in self.filtered_rows if not row.is_valid)
        return self.invalid_rows + filtered_invalid

    @property
    def all_valid_rows(self) -> tuple[RowProcessingResult, ...]:
        """Return every non-duplicate valid row, including filtered rows."""

        filtered_valid = tuple(row for row in self.filtered_rows if row.is_valid)
        return self.valid_rows + filtered_valid
