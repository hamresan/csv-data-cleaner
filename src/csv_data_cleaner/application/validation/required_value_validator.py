"""Validate configured required row values."""

from csv_data_cleaner.domain import DataRow, ValidationIssue


class RequiredValueValidator:
    """Report missing values for configured required columns."""

    def validate(self, row: DataRow, columns: tuple[str, ...]) -> tuple[ValidationIssue, ...]:
        return tuple(
            ValidationIssue(
                row_number=row.number,
                column=column,
                code="required",
                message=f"{column} is required.",
            )
            for column in columns
            if row.values.get(column) is None
        )
