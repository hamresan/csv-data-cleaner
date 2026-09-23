"""Behavioral tests for processing configuration schema validation."""

import pytest

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.validators.config_field_validator import ConfigFieldValidator
from csv_data_cleaner.infrastructure.validators.processing_config_validator import (
    ProcessingConfigValidator,
)


def build_validator() -> ProcessingConfigValidator:
    return ProcessingConfigValidator(field_validator=ConfigFieldValidator())


def test_validator_builds_typed_configuration_data() -> None:
    result = build_validator().validate(
        {
            "required_columns": ["email"],
            "validation": {
                "email_columns": ["email"],
                "date_columns": ["signup_date"],
                "date_formats": {
                    "signup_date": ["%Y-%m-%d", "%d/%m/%Y"],
                },
            },
            "normalization": {
                "trim_whitespace": True,
                "empty_strings_as_null": True,
                "casefold_columns": ["email"],
                "date_output_format": "%Y-%m-%d",
            },
            "deduplication": {"columns": ["email"], "keep": "last"},
            "filters": [{"column": "email", "operator": "not_equals", "value": None}],
            "sorting": [{"column": "email", "ascending": False}],
            "output": {"format": "xlsx"},
        }
    )

    assert result.required_columns == ("email",)
    assert result.date_rules[0].column == "signup_date"
    assert result.date_rules[0].formats == ("%Y-%m-%d", "%d/%m/%Y")
    assert result.normalization.trim_whitespace is True
    assert result.normalization.empty_strings_as_null is True
    assert result.normalization.casefold_columns == ("email",)
    assert result.normalization.date_output_format == "%Y-%m-%d"
    assert result.deduplication is not None
    assert result.deduplication.keep == "last"
    assert result.filters[0].operator == "not_equals"
    assert result.sorting[0].ascending is False
    assert result.output_format == "xlsx"


def test_validator_uses_deterministic_stage_2_defaults() -> None:
    result = build_validator().validate(
        {
            "validation": {"date_columns": ["created_at"]},
        }
    )

    assert result.date_rules[0].formats == ("%Y-%m-%d",)
    assert result.normalization.trim_whitespace is True
    assert result.normalization.empty_strings_as_null is True
    assert result.normalization.casefold_columns == ()
    assert result.normalization.date_output_format == "%Y-%m-%d"


@pytest.mark.parametrize(
    "config",
    [
        {"required_columns": "email"},
        {"validation": []},
        {"validation": {"date_formats": []}},
        {
            "validation": {
                "date_columns": ["created_at"],
                "date_formats": {"created_at": []},
            }
        },
        {
            "validation": {
                "date_columns": ["created_at"],
                "date_formats": {"other_date": ["%Y-%m-%d"]},
            }
        },
        {"normalization": []},
        {"normalization": {"trim_whitespace": "yes"}},
        {"normalization": {"empty_strings_as_null": "yes"}},
        {"normalization": {"casefold_columns": "email"}},
        {"normalization": {"casefold_columns": [""]}},
        {"normalization": {"date_output_format": ""}},
        {"deduplication": {"columns": "email"}},
        {"deduplication": {"columns": []}},
        {"deduplication": {"keep": "middle"}},
        {"filters": ["email"]},
        {"filters": [{"column": "", "value": "x"}]},
        {"filters": [{"column": "email", "operator": "contains", "value": "x"}]},
        {"filters": [{"column": "email", "value": [], "include": True}]},
        {"filters": [{"column": "email", "value": "x", "include": "yes"}]},
        {"sorting": ["email"]},
        {"sorting": [{"column": ""}]},
        {"sorting": [{"column": "email", "ascending": "yes"}]},
        {"output": {"format": "json"}},
    ],
)
def test_validator_rejects_invalid_schema(config: dict[str, object]) -> None:
    with pytest.raises(ConfigurationError):
        build_validator().validate(config)  # type: ignore[arg-type]
