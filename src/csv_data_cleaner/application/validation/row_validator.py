"""Orchestrate validation of one canonical row."""

from csv_data_cleaner.application.validation.date_value_validator import DateValueValidator
from csv_data_cleaner.application.validation.email_value_validator import EmailValueValidator
from csv_data_cleaner.application.validation.required_value_validator import RequiredValueValidator
from csv_data_cleaner.domain import DataRow, ProcessingConfig, ValidationIssue


class RowValidator:
    """Run row validators in a stable order and accumulate every issue."""

    def __init__(
        self,
        required_validator: RequiredValueValidator,
        email_validator: EmailValueValidator,
        date_validator: DateValueValidator,
    ) -> None:
        self.required_validator = required_validator
        self.email_validator = email_validator
        self.date_validator = date_validator

    def validate(self, row: DataRow, config: ProcessingConfig) -> tuple[ValidationIssue, ...]:
        return (
            *self.required_validator.validate(row, config.required_columns),
            *self.email_validator.validate(row, config.email_columns),
            *self.date_validator.validate(row, config.date_rules),
        )
