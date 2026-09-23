"""Behavioral tests for processing configuration models."""

from csv_data_cleaner.domain import (
    DeduplicationKeep,
    DeduplicationPolicy,
    OutputFormat,
    ProcessingConfig,
    SortRule,
)


def test_processing_config_preserves_domain_values() -> None:
    config = ProcessingConfig(
        required_columns=("email",),
        email_columns=("email",),
        date_columns=(),
        deduplication=DeduplicationPolicy(("email",), DeduplicationKeep.LAST),
        sorting=(SortRule("email", ascending=False),),
        output_format=OutputFormat.CSV,
    )

    assert config.deduplication == DeduplicationPolicy(("email",), DeduplicationKeep.LAST)
    assert config.sorting == (SortRule("email", ascending=False),)
