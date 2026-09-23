"""Map validated configuration data to domain configuration."""

from csv_data_cleaner.domain import (
    DateValidationRule,
    DeduplicationKeep,
    DeduplicationPolicy,
    FilterOperator,
    FilterRule,
    NormalizationPolicy,
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
            date_rules=tuple(
                DateValidationRule(column=item.column, formats=item.formats)
                for item in data.date_rules
            ),
            normalization=NormalizationPolicy(
                trim_whitespace=data.normalization.trim_whitespace,
                empty_strings_as_null=data.normalization.empty_strings_as_null,
                casefold_columns=data.normalization.casefold_columns,
                date_output_format=data.normalization.date_output_format,
            ),
            deduplication=deduplication,
            filters=tuple(
                FilterRule(
                    column=item.column,
                    operator=FilterOperator(item.operator),
                    value=item.value,
                    include=item.include,
                )
                for item in data.filters
            ),
            sorting=tuple(
                SortRule(column=item.column, ascending=item.ascending) for item in data.sorting
            ),
            output_format=OutputFormat(data.output_format),
        )
