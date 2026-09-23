"""Behavioral tests for raw configuration value validation."""

import pytest

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.validators.config_value_validator import ConfigValueValidator


def test_validator_accepts_supported_nested_values() -> None:
    result = ConfigValueValidator().parse_object(
        {"required_columns": ["email"], "threshold": 42, "ratio": 1.5, "output": {"format": "csv"}}
    )

    assert result == {\n        "required_columns": ["email"],\n        "threshold": 42,\n        "ratio": 1.5,\n        "output": {"format": "csv"},\n    }


@pytest.mark.parametrize("value", [42, {"value": object()}])
def test_validator_rejects_unsupported_values(value: object) -> None:
    with pytest.raises(ConfigurationError):
        ConfigValueValidator().parse_object(value)
