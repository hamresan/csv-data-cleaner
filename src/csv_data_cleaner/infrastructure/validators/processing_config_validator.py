"""Validate the processing configuration schema."""

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.types.config_value import ConfigObject
from csv_data_cleaner.infrastructure.types.processing_config_data import (
    DateValidationConfigData,
    DeduplicationConfigData,
    NormalizationConfigData,
    ProcessingConfigData,
    SortConfigData,
)
from csv_data_cleaner.infrastructure.validators.config_field_validator import ConfigFieldValidator


class ProcessingConfigValidator:
    """Validate raw processing configuration and build typed configuration data."""

    def __init__(self, field_validator: ConfigFieldValidator) -> None:
        self.field_validator = field_validator

    def validate(self, data: ConfigObject) -> ProcessingConfigData:
        fields = self.field_validator
        validation = fields.object_or_empty(data.get("validation"), "validation")
        normalization = fields.object_or_empty(data.get("normalization"), "normalization")
        output = fields.object_or_empty(data.get("output"), "output")
        deduplication = fields.optional_object(data.get("deduplication"), "deduplication")
        sorting = fields.objects(data.get("sorting", []), "sorting")

        date_columns = fields.strings(
            validation.get("date_columns", []),
            "validation.date_columns",
        )
        date_formats = fields.object_or_empty(
            validation.get("date_formats"),
            "validation.date_formats",
        )
        unknown_date_format_columns = tuple(
            column for column in date_formats if column not in date_columns
        )
        if unknown_date_format_columns:
            columns = ", ".join(unknown_date_format_columns)
            raise ConfigurationError(
                f"validation.date_formats contains unconfigured date columns: {columns}"
            )

        date_rules = tuple(
            DateValidationConfigData(
                column=column,
                formats=fields.non_empty_strings(
                    date_formats.get(column, ["%Y-%m-%d"]),
                    f"validation.date_formats.{column}",
                ),
            )
            for column in date_columns
        )

        deduplication_data = None
        if deduplication is not None:
            deduplication_data = DeduplicationConfigData(
                columns=fields.non_empty_strings(
                    deduplication.get("columns", []),
                    "deduplication.columns",
                ),
                keep=fields.choice(
                    deduplication.get("keep", "first"),
                    "deduplication.keep",
                    {"first", "last"},
                ),
            )

        return ProcessingConfigData(
            required_columns=fields.strings(
                data.get("required_columns", []),
                "required_columns",
            ),
            email_columns=fields.strings(
                validation.get("email_columns", []),
                "validation.email_columns",
            ),
            date_rules=date_rules,
            normalization=NormalizationConfigData(
                trim_whitespace=fields.boolean(
                    normalization.get("trim_whitespace", True),
                    "normalization.trim_whitespace",
                ),
                empty_strings_as_null=fields.boolean(
                    normalization.get("empty_strings_as_null", True),
                    "normalization.empty_strings_as_null",
                ),
                casefold_columns=fields.strings(
                    normalization.get("casefold_columns", []),
                    "normalization.casefold_columns",
                ),
                date_output_format=fields.required_string(
                    normalization.get("date_output_format", "%Y-%m-%d"),
                    "normalization.date_output_format",
                ),
            ),
            deduplication=deduplication_data,
            sorting=tuple(
                SortConfigData(
                    column=fields.required_string(item.get("column"), "sorting.column"),
                    ascending=fields.boolean(
                        item.get("ascending", True),
                        "sorting.ascending",
                    ),
                )
                for item in sorting
            ),
            output_format=fields.choice(
                output.get("format", "csv"),
                "output.format",
                {"csv", "xlsx"},
            ),
        )
