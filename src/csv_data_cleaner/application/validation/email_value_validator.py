"""Validate configured email row values."""

from csv_data_cleaner.application.contracts import EmailSyntaxChecker
from csv_data_cleaner.domain import DataRow, ValidationIssue


class EmailValueValidator:
    """Map invalid configured email values to validation issues."""

    def __init__(self, syntax_checker: EmailSyntaxChecker) -> None:
        self.syntax_checker = syntax_checker

    def validate(self, row: DataRow, columns: tuple[str, ...]) -> tuple[ValidationIssue, ...]:
        issues: list[ValidationIssue] = []
        for column in columns:
            value = row.values.get(column)
            if value is None:
                continue
            if not isinstance(value, str) or not self.syntax_checker.is_valid(value):
                issues.append(
                    ValidationIssue(
                        row_number=row.number,
                        column=column,
                        code="invalid_email",
                        message=f"{column} must contain a valid email address.",
                    )
                )
        return tuple(issues)
