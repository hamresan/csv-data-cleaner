"""Configuration loading orchestration."""

from pathlib import Path

from csv_data_cleaner.application.ports import ConfigLoader
from csv_data_cleaner.domain import ProcessingConfig
from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.factories.config_parser_factory import ConfigParserFactory
from csv_data_cleaner.infrastructure.mappers.processing_config_mapper import ProcessingConfigMapper
from csv_data_cleaner.infrastructure.validators.config_value_validator import ConfigValueValidator
from csv_data_cleaner.infrastructure.validators.processing_config_validator import (
    ProcessingConfigValidator,
)


class FileConfigLoader(ConfigLoader):
    """Coordinate parsing, validation, and domain mapping."""

    def __init__(
        self,
        parser_factory: ConfigParserFactory,
        value_validator: ConfigValueValidator,
        config_validator: ProcessingConfigValidator,
        mapper: ProcessingConfigMapper,
    ) -> None:
        self.parser_factory = parser_factory
        self.value_validator = value_validator
        self.config_validator = config_validator
        self.mapper = mapper

    def load(self, path: Path) -> ProcessingConfig:
        if not path.is_file():
            raise ConfigurationError(f"Configuration file does not exist: {path}")

        parser = self.parser_factory.create(path)
        parsed = parser.parse(path)
        raw_config = self.value_validator.parse_object(parsed)
        validated_config = self.config_validator.validate(raw_config)
        return self.mapper.map(validated_config)
