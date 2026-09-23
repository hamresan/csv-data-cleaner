"""Behavioral tests for processing configuration mapping."""

import pytest

from csv_data_cleaner.domain import DeduplicationKeep, OutputFormat
from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.mappers.processing_config_mapper import ProcessingConfigMapper


def test_mapper_builds_domain_configuration() -> None:
    result = ProcessingConfigMapper().map(
        {
            "required_columns": ["email"],
            "validation": {"email_columns": ["email"], "date_columns": []},
            "deduplication": {"columns": ["email"], "keep": "last"},
            "sorting": [{"column": "email", "ascending": False}],
            "output": {"format": "xlsx"},
        }
    )

    assert result.required_columns == ("email",)
    assert result.deduplication is not None
    assert result.deduplication.keep is DeduplicationKeep.LAST
    assert result.sorting[0].ascending is False
    assert result.output_format is OutputFormat.XLSX


def test_mapper_rejects_invalid_configuration_shape() -> None:
    with pytest.raises(ConfigurationError):
        ProcessingConfigMapper().map({"required_columns": "email"})
