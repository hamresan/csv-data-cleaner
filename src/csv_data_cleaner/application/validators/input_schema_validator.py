"""Validate input schema requirements before processing."""

from csv_data_cleaner.domain import InputData, ProcessingConfig
from csv_data_cleaner.domain.errors import InputDataError


class InputSchemaValidator:
    """Validate canonical input data against processing configuration."""

    def validate(self, data: InputData, config: ProcessingConfig) -> None:
        missing = tuple(column for column in config.required_columns if column not in data.columns)
        if missing:
            columns = ", ".join(missing)
            raise InputDataError(f"Missing required columns: {columns}")
