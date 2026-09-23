"""Validate the processing configuration schema."""

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.types.config_value import ConfigObject, ConfigValue
from csv_data_cleaner.infrastructure.types.processing_config_data import (
    DeduplicationConfigData,
    ProcessingConfigData,
    SortConfigData,
)


class ProcessingConfigValidator:
    """Validate raw configuration fields and build validated configuration data."""

    def validate(self, data: ConfigObject) -> ProcessingConfigData:
        validation = self._object_or_empty(data.get("validation"), "validation")
        output = self._object_or_empty(data.get("output"), "output")
        deduplication = self._optional_object(data.get("deduplication"), "deduplication")
        sorting = self._objects(data.get("sorting", []), "sorting")

        deduplication_data = None
        if deduplication is not None:
            deduplication_data = DeduplicationConfigData(
                columns=self._strings(
                    deduplication.get("columns", []),
                    "deduplication.columns",
                ),
                keep=self._choice(
                    deduplication.get("keep", "first"),
                    "deduplication.keep",
                    {"first", "last"},
                ),
            )

        return ProcessingConfigData(
            required_columns=self._strings(
                data.get("required_columns", []),
                "required_columns",
            ),
            email_columns=self._strings(
                validation.get("email_columns", []),
                "validation.email_columns",
            ),
            date_columns=self._strings(
                validation.get("date_columns", []),
                "validation.date_columns",
            ),
            deduplication=deduplication_data,
            sorting=tuple(
                SortConfigData(
                    column=self._required_string(item.get("column"), "sorting.column"),
                    ascending=self._boolean(
                        item.get("ascending", True),
                        "sorting.ascending",
                    ),
                )
                for item in sorting
            ),
            output_format=self._choice(
                output.get("format", "csv"),
                "output.format",
                {"csv", "xlsx"},
            ),
        )

    def _object_or_empty(self, value: ConfigValue, field: str) -> ConfigObject:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ConfigurationError(f"{field} must be an object.")
        return value

    def _optional_object(self, value: ConfigValue, field: str) -> ConfigObject | None:
        if value is None:
            return None
        if not isinstance(value, dict):
            raise ConfigurationError(f"{field} must be an object.")
        return value

    def _strings(self, value: ConfigValue, field: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise ConfigurationError(f"{field} must be a list of non-empty strings.")
        if any(not isinstance(item, str) or not item for item in value):
            raise ConfigurationError(f"{field} must be a list of non-empty strings.")
        return tuple(item for item in value if isinstance(item, str))

    def _objects(self, value: ConfigValue, field: str) -> tuple[ConfigObject, ...]:
        if not isinstance(value, list):
            raise ConfigurationError(f"{field} must be a list.")
        if any(not isinstance(item, dict) for item in value):
            raise ConfigurationError(f"{field} must contain objects.")
        return tuple(item for item in value if isinstance(item, dict))

    def _required_string(self, value: ConfigValue, field: str) -> str:
        if not isinstance(value, str) or not value:
            raise ConfigurationError(f"{field} must be a non-empty string.")
        return value

    def _boolean(self, value: ConfigValue, field: str) -> bool:
        if not isinstance(value, bool):
            raise ConfigurationError(f"{field} must be a boolean.")
        return value

    def _choice(
        self,
        value: ConfigValue,
        field: str,
        choices: set[str],
    ) -> str:
        if not isinstance(value, str) or value not in choices:
            options = " or ".join(sorted(choices))
            raise ConfigurationError(f"{field} must be {options}.")
        return value
