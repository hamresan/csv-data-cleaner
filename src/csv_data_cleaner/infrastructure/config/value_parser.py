"""Convert untyped parser output into supported configuration values."""

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.config.types import ConfigObject, ConfigValue


class ConfigValueParser:
    """Validate the shape and primitive types of parsed configuration data."""

    def parse_object(self, value: object, field: str = "Configuration root") -> ConfigObject:
        if not isinstance(value, dict):
            raise ConfigurationError(f"{field} must be an object.")

        result: ConfigObject = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ConfigurationError(f"{field} keys must be strings.")
            result[key] = self.parse_value(item, field)
        return result

    def parse_value(self, value: object, field: str) -> ConfigValue:
        if value is None or isinstance(value, str | bool):
            return value
        if isinstance(value, list):
            return [self.parse_value(item, field) for item in value]
        if isinstance(value, dict):
            return self.parse_object(value, field)
        raise ConfigurationError(f"{field} contains an unsupported value.")
