"""Behavioral tests for processing configuration schema validation."""

import pytest

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.validators.processing_config_validator import (
    ProcessingConfigValidator,
)


def test_validator_builds_typed_configuration_data() -> None:
    result = ProcessingConfigValidator().validate(
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
    assert result.deduplication.keep == "last"
    assert result.sorting[0].ascending is False
    assert result.output_format == "xlsx"


@pytest.mark.parametrize(
    "config",
    [
        {"required_columns": "email"},
        {"validation": []},
        {"deduplication": {"columns": "email"}},
        {"deduplication": {"keep": "middle"}},
        {"sorting": ["email"]},
        {"sorting": [{"column": ""}]},
        {"sorting": [{"column": "email", "ascending": "yes"}]},
        {"output": {"format": "json"}},
    ],
)
def test_validator_rejects_invalid_schema(config: dict[str, object]) -> None:
    with pytest.raises(ConfigurationError):
        ProcessingConfigValidator().validate(config)  # type: ignore[arg-type]
