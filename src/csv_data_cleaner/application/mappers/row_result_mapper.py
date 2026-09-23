"""Map row processing outputs to a domain result."""

from csv_data_cleaner.domain import DataRow, RowProcessingResult, ValidationIssue


class RowResultMapper:
    """Build immutable row processing results without changing source data."""

    def map(
        self,
        source_row: DataRow,
        normalized_row: DataRow,
        issues: tuple[ValidationIssue, ...],
    ) -> RowProcessingResult:
        return RowProcessingResult(
            source_row=source_row,
            normalized_row=normalized_row,
            issues=issues,
        )
