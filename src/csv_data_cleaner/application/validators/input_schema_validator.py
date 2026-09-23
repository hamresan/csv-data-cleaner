"""Validate input schema requirements before processing."""

from csv_data_cleaner.domain import InputData, ProcessingConfig
from csv_data_cleaner.domain.errors import InputDataError


class InputSchemaValidator:
    """Validate canonical input data against configured column requirements."""

    def validate(self, data: InputData, config: ProcessingConfig) -> None:
        configured_columns = dict.fromkeys(
            (*config.required_columns, *config.email_columns, *config.date_columns)
        )
        missing = tuple(column for column in configured_columns if column not in data.columns)
        if missing:
            columns = ", ".join(missing)
            raise InputDataError(f"Missing configured columns: {columns}")
