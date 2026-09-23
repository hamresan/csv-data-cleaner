"""Behavioral tests for processing configuration mapping."""

from csv_data_cleaner.domain import DeduplicationKeep, OutputFormat
from csv_data_cleaner.infrastructure.mappers.processing_config_mapper import ProcessingConfigMapper
from csv_data_cleaner.infrastructure.types.processing_config_data import (
    DateValidationConfigData,
    DeduplicationConfigData,
    NormalizationConfigData,
    ProcessingConfigData,
    SortConfigData,
)


def test_mapper_builds_domain_configuration() -> None:
    data = ProcessingConfigData(
        required_columns=("email",),
        email_columns=("email",),
        date_rules=(
            DateValidationConfigData(
                column="signup_date",
                formats=("%Y-%m-%d", "%d/%m/%Y"),
            ),
        ),
        normalization=NormalizationConfigData(
            trim_whitespace=True,
            empty_strings_as_null=True,
            casefold_columns=("email",),
            date_output_format="%Y-%m-%d",
        ),
        deduplication=DeduplicationConfigData(
            columns=("email",),
            keep="last",
        ),
        sorting=(SortConfigData(column="email", ascending=False),),
        output_format="xlsx",
    )

    result = ProcessingConfigMapper().map(data)

    assert result.required_columns == ("email",)
    assert result.date_columns == ("signup_date",)
    assert result.date_rules[0].formats == ("%Y-%m-%d", "%d/%m/%Y")
    assert result.normalization.empty_strings_as_null is True
    assert result.normalization.casefold_columns == ("email",)
    assert result.deduplication is not None
    assert result.deduplication.keep is DeduplicationKeep.LAST
    assert result.sorting[0].ascending is False
    assert result.output_format is OutputFormat.XLSX
