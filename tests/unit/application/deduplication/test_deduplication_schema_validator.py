"""Tests for deduplication input-schema validation."""

import pytest

from csv_data_cleaner.application.deduplication import DeduplicationSchemaValidator
from csv_data_cleaner.domain import DeduplicationPolicy, InputData
from csv_data_cleaner.domain.errors import InputDataError


def test_accepts_existing_deduplication_columns() -> None:
    validator = DeduplicationSchemaValidator()
    input_data = InputData(columns=("email", "country"), rows=())

    validator.validate(
        input_data,
        DeduplicationPolicy(columns=("email", "country")),
    )


def test_rejects_missing_deduplication_columns() -> None:
    validator = DeduplicationSchemaValidator()
    input_data = InputData(columns=("email", "country"), rows=())

    with pytest.raises(
        InputDataError,
        match="^Missing deduplication columns: customer_id, tenant_id$",
    ):
        validator.validate(
            input_data,
            DeduplicationPolicy(columns=("email", "customer_id", "tenant_id")),
        )
