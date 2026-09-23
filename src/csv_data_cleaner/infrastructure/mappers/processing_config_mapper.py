"""Map validated configuration data to domain configuration."""

from csv_data_cleaner.domain import (
    DeduplicationKeep,
    DeduplicationPolicy,
    OutputFormat,
    ProcessingConfig,
    SortRule,
)
from csv_data_cleaner.infrastructure.types.processing_config_data import ProcessingConfigData


class ProcessingConfigMapper:
    """Map validated infrastructure data to domain models."""

    def map(self, data: ProcessingConfigData) -> ProcessingConfig:
        deduplication = None
        if data.deduplication is not None:
            deduplication = DeduplicationPolicy(
                columns=data.deduplication.columns,
                keep=DeduplicationKeep(data.deduplication.keep),
            )

        return ProcessingConfig(
            required_columns=data.required_columns,
            email_columns=data.email_columns,
            date_columns=data.date_columns,
            deduplication=deduplication,
            sorting=tuple(
                SortRule(column=item.column, ascending=item.ascending)
                for item in data.sorting
            ),
            output_format=OutputFormat(data.output_format),
        )
