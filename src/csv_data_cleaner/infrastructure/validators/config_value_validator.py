"""Convert untyped parser output into supported configuration values."""

from collections.abc import Mapping, Sequence
from typing import cast

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.types.config_value import ConfigObject, ConfigValue


class ConfigValueValidator:
    """Validate the shape and primitive types of parsed configuration data."""

    def parse_object(self, value: object, field: str = "Configuration root") -> ConfigObject:
        if not isinstance(value, Mapping):
            raise ConfigurationError(f"{field} must be an object.")

        mapping = cast(Mapping[object, object], value)
        result: ConfigObject = {}
        for key, item in mapping.items():
            if not isinstance(key, str):
                raise ConfigurationError(f"{field} keys must be strings.")
            result[key] = self.parse_value(item, field)
        return result

    def parse_value(self, value: object, field: str) -> ConfigValue:
        if value is None or isinstance(value, str | bool):
            return value
        if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
            sequence = cast(Sequence[object], value)
            return [self.parse_value(item, field) for item in sequence]
        if isinstance(value, Mapping):
            mapping = cast(Mapping[object, object], value)
            return self.parse_object(mapping, field)
        raise ConfigurationError(f"{field} contains an unsupported value.")
