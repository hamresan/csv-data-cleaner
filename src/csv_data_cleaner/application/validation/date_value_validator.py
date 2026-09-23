"""Validate configured date row values."""

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.domain import DataRow, DateValidationRule, ValidationIssue


class DateValueValidator:
    """Map invalid configured date values to validation issues."""

    def __init__(self, date_parser: DateParser) -> None:
        self.date_parser = date_parser

    def validate(
        self,
        row: DataRow,
        rules: tuple[DateValidationRule, ...],
    ) -> tuple[ValidationIssue, ...]:
        issues: list[ValidationIssue] = []
        for rule in rules:
            value = row.values.get(rule.column)
            if value is None:
                continue
            if not isinstance(value, str) or self.date_parser.parse(value, rule.formats) is None:
                issues.append(
                    ValidationIssue(
                        row_number=row.number,
                        column=rule.column,
                        code="invalid_date",
                        message=f"{rule.column} must contain a valid date.",
                    )
                )
        return tuple(issues)
