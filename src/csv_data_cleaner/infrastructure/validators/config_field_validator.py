"""Validate typed fields within a processing configuration."""

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.types.config_value import ConfigObject, ConfigValue


class ConfigFieldValidator:
    """Validate individual configuration field shapes and scalar values."""

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
        if any(not isinstance(item, str) or not item for item in value):
            raise ConfigurationError(f"{field} must be a list of non-empty strings.")
        return tuple(item for item in value if isinstance(item, str))

    def non_empty_strings(self, value: ConfigValue, field: str) -> tuple[str, ...]:
        values = self.strings(value, field)
        if not values:
            raise ConfigurationError(f"{field} must contain at least one value.")
        return values

    def objects(self, value: ConfigValue, field: str) -> tuple[ConfigObject, ...]:
        if not isinstance(value, list):
            raise ConfigurationError(f"{field} must be a list.")
        if any(not isinstance(item, dict) for item in value):
            raise ConfigurationError(f"{field} must contain objects.")
        return tuple(item for item in value if isinstance(item, dict))

    def required_string(self, value: ConfigValue, field: str) -> str:
        if not isinstance(value, str) or not value:
            raise ConfigurationError(f"{field} must be a non-empty string.")
        return value

    def boolean(self, value: ConfigValue, field: str) -> bool:
        if not isinstance(value, bool):
            raise ConfigurationError(f"{field} must be a boolean.")
        return value

    def choice(self, value: ConfigValue, field: str, choices: set[str]) -> str:
        if not isinstance(value, str) or value not in choices:
            options = " or ".join(sorted(choices))
            raise ConfigurationError(f"{field} must be {options}.")
        return value
