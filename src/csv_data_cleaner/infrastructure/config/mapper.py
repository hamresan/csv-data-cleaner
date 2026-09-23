"""Map validated raw configuration values to domain configuration."""

from csv_data_cleaner.domain import (
    DeduplicationKeep,
    DeduplicationPolicy,
    OutputFormat,
    ProcessingConfig,
    SortRule,
)
from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.config.types import ConfigObject, ConfigValue


class ProcessingConfigMapper:
    """Map supported configuration values to domain models."""

    def map(self, data: ConfigObject) -> ProcessingConfig:
        validation = self.object_or_empty(data.get("validation"), "validation")
        output = self.object_or_empty(data.get("output"), "output")
        deduplication = self.optional_object(data.get("deduplication"), "deduplication")
        sorting = self.objects(data.get("sorting", []), "sorting")

        policy = None
        if deduplication is not None:
            policy = DeduplicationPolicy(
                columns=self.strings(deduplication.get("columns", []), "deduplication.columns"),
                keep=self.deduplication_keep(deduplication.get("keep", "first")),
            )

        return ProcessingConfig(
            required_columns=self.strings(data.get("required_columns", []), "required_columns"),
            email_columns=self.strings(
                validation.get("email_columns", []), "validation.email_columns"
            ),
            date_columns=self.strings(
                validation.get("date_columns", []), "validation.date_columns"
            ),
            deduplication=policy,
            sorting=tuple(
                SortRule(
                    column=self.sort_column(item),
                    ascending=self.boolean(item.get("ascending", True), "sorting.ascending"),
                )
                for item in sorting
            ),
            output_format=self.output_format(output.get("format", "csv")),
        )

    def object_or_empty(self, value: ConfigValue, field: str) -> ConfigObject:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ConfigurationError(f"{field} must be an object.")
        return value

    def optional_object(self, value: ConfigValue, field: str) -> ConfigObject | None:
        if value is None:
            return None
        if not isinstance(value, dict):
            raise ConfigurationError(f"{field} must be an object.")
        return value

    def strings(self, value: ConfigValue, field: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise ConfigurationError(f"{field} must be a list of non-empty strings.")
        result: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item:
                raise ConfigurationError(f"{field} must be a list of non-empty strings.")
            result.append(item)
        return tuple(result)

    def objects(self, value: ConfigValue, field: str) -> tuple[ConfigObject, ...]:
        if not isinstance(value, list):
            raise ConfigurationError(f"{field} must be a list.")
        result: list[ConfigObject] = []
        for item in value:
            if not isinstance(item, dict):
                raise ConfigurationError(f"{field} must contain objects.")
            result.append(item)
        return tuple(result)

    def sort_column(self, value: ConfigObject) -> str:
        column = value.get("column")
        if not isinstance(column, str) or not column:
            raise ConfigurationError("sorting.column must be a non-empty string.")
        return column

    def boolean(self, value: ConfigValue, field: str) -> bool:
        if not isinstance(value, bool):
            raise ConfigurationError(f"{field} must be a boolean.")
        return value

    def deduplication_keep(self, value: ConfigValue) -> DeduplicationKeep:
        if not isinstance(value, str):
            raise ConfigurationError("deduplication.keep must be first or last.")
        try:
            return DeduplicationKeep(value)
        except ValueError as error:
            raise ConfigurationError("deduplication.keep must be first or last.") from error

    def output_format(self, value: ConfigValue) -> OutputFormat:
        if not isinstance(value, str):
            raise ConfigurationError("output.format must be csv or xlsx.")
        try:
            return OutputFormat(value)
        except ValueError as error:
            raise ConfigurationError("output.format must be csv or xlsx.") from error
