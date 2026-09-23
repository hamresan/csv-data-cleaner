"""Tests for canonical input schema validation."""

import pytest

from csv_data_cleaner.application.validators import InputSchemaValidator
from csv_data_cleaner.domain import InputData, OutputFormat, ProcessingConfig
from csv_data_cleaner.domain.errors import InputDataError


def config_with_required_columns(*columns: str) -> ProcessingConfig:
    return ProcessingConfig(
        required_columns=columns,
        email_columns=(),
        date_columns=(),
        deduplication=None,
        sorting=(),
        output_format=OutputFormat.CSV,
    )


def test_validator_accepts_present_required_columns() -> None:
    data = InputData(columns=("name", "email"), rows=())

    InputSchemaValidator().validate(
        data,
        config_with_required_columns("name", "email"),
    )


def test_validator_reports_all_missing_required_columns() -> None:
    data = InputData(columns=("name",), rows=())

    with pytest.raises(
        InputDataError,
        match="Missing required columns: email, created_at",
    ):
        InputSchemaValidator().validate(
            data,
            config_with_required_columns("email", "created_at"),
        )
