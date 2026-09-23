"""Row processing result domain models."""

from dataclasses import dataclass

from csv_data_cleaner.domain.input_data import DataRow
from csv_data_cleaner.domain.validation import ValidationIssue


@dataclass(frozen=True, slots=True)
class RowProcessingResult:
    """Preserve source and normalized row data together with validation issues."""

    source_row: DataRow
    normalized_row: DataRow
    issues: tuple[ValidationIssue, ...]

    @property
    def is_valid(self) -> bool:
        """Return whether the row has no validation failures."""

        return not self.issues
