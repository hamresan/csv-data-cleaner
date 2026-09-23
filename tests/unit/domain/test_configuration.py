"""Behavioral tests for processing configuration models."""

from csv_data_cleaner.domain import (
    DateValidationRule,
    DeduplicationKeep,
    DeduplicationPolicy,
    NormalizationPolicy,
    OutputFormat,
    ProcessingConfig,
    SortRule,
)


def test_processing_config_preserves_domain_values() -> None:
    config = ProcessingConfig(
        required_columns=("email",),
        email_columns=("email",),
        date_rules=(
            DateValidationRule(
                column="signup_date",
                formats=("%Y-%m-%d", "%d/%m/%Y"),
            ),
        ),
        normalization=NormalizationPolicy(
            trim_whitespace=True,
            empty_strings_as_null=True,
            date_output_format="%Y-%m-%d",
        ),
        deduplication=DeduplicationPolicy(("email",), DeduplicationKeep.LAST),
        sorting=(SortRule("email", ascending=False),),
        output_format=OutputFormat.CSV,
    )

    assert config.date_columns == ("signup_date",)
    assert config.date_rules[0].formats == ("%Y-%m-%d", "%d/%m/%Y")
    assert config.normalization.date_output_format == "%Y-%m-%d"
    assert config.deduplication == DeduplicationPolicy(("email",), DeduplicationKeep.LAST)
    assert config.sorting == (SortRule("email", ascending=False),)
