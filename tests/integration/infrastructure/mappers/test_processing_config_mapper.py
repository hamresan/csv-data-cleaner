"""Behavioral tests for processing configuration mapping."""

from csv_data_cleaner.domain import DeduplicationKeep, OutputFormat
from csv_data_cleaner.infrastructure.mappers.processing_config_mapper import ProcessingConfigMapper
from csv_data_cleaner.infrastructure.types.processing_config_data import (
    DeduplicationConfigData,
    ProcessingConfigData,
    SortConfigData,
)


def test_mapper_builds_domain_configuration() -> None:
    data = ProcessingConfigData(
        required_columns=("email",),
        email_columns=("email",),
        date_columns=(),
        deduplication=DeduplicationConfigData(
            columns=("email",),
            keep="last",
        ),
        sorting=(SortConfigData(column="email", ascending=False),),
        output_format="xlsx",
    )

    result = ProcessingConfigMapper().map(data)

    assert result.required_columns == ("email",)
    assert result.deduplication is not None
    assert result.deduplication.keep is DeduplicationKeep.LAST
    assert result.sorting[0].ascending is False
    assert result.output_format is OutputFormat.XLSX
