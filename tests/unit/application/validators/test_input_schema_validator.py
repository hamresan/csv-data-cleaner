"""Tests for canonical input schema validation."""

import pytest

from csv_data_cleaner.application.validators import InputSchemaValidator
from csv_data_cleaner.domain import (
    DateValidationRule,
    InputData,
    NormalizationPolicy,
    OutputFormat,
    ProcessingConfig,
)
from csv_data_cleaner.domain.errors import InputDataError


def build_config(
    *,
    required_columns: tuple[str, ...] = (),
    email_columns: tuple[str, ...] = (),
    date_columns: tuple[str, ...] = (),
) -> ProcessingConfig:
    return ProcessingConfig(
        required_columns=required_columns,
        email_columns=email_columns,
        date_rules=tuple(
            DateValidationRule(column=column, formats=("%Y-%m-%d",)) for column in date_columns
        ),
        normalization=NormalizationPolicy(),
        deduplication=None,
        filters=(),
        sorting=(),
        output_format=OutputFormat.CSV,
    )


def test_validator_accepts_all_present_configured_columns() -> None:
    data = InputData(columns=("name", "email", "created_at"), rows=())

    InputSchemaValidator().validate(
        data,
        build_config(
            required_columns=("name",),
            email_columns=("email",),
            date_columns=("created_at",),
        ),
    )


def test_validator_reports_missing_columns_from_all_validation_rules() -> None:
    data = InputData(columns=("name",), rows=())

    with pytest.raises(
        InputDataError,
        match="Missing configured columns: email, created_at",
    ):
        InputSchemaValidator().validate(
            data,
            build_config(
                email_columns=("email",),
                date_columns=("created_at",),
            ),
        )


def test_validator_reports_missing_columns_once_in_deterministic_order() -> None:
    data = InputData(columns=("name",), rows=())

    with pytest.raises(
        InputDataError,
        match="Missing configured columns: email, created_at",
    ):
        InputSchemaValidator().validate(
            data,
            build_config(
                required_columns=("email",),
                email_columns=("email",),
                date_columns=("created_at",),
            ),
        )
