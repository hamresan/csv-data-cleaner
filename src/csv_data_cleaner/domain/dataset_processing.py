"""Dataset processing result domain models."""

from dataclasses import dataclass

from csv_data_cleaner.domain.row_processing import RowProcessingResult


@dataclass(frozen=True, slots=True)
class DatasetProcessingResult:
    """Separate processed rows deterministically while preserving row results."""

    rows: tuple[RowProcessingResult, ...]

    @property
    def valid_rows(self) -> tuple[RowProcessingResult, ...]:
        """Return valid row results in source order."""

        return tuple(row for row in self.rows if row.is_valid)

    @property
    def invalid_rows(self) -> tuple[RowProcessingResult, ...]:
        """Return invalid row results in source order."""

        return tuple(row for row in self.rows if not row.is_valid)
