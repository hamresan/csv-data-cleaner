"""Configuration loading orchestration."""

from pathlib import Path

from csv_data_cleaner.application.ports import ConfigLoader
from csv_data_cleaner.domain import ProcessingConfig
from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.mappers.processing_config_mapper import ProcessingConfigMapper
from csv_data_cleaner.infrastructure.factories.config_parser_factory import ConfigParserFactory
from csv_data_cleaner.infrastructure.validators.config_value_validator import ConfigValueValidator


class FileConfigLoader(ConfigLoader):
    """Coordinate parsing, boundary validation, and domain mapping."""

    def __init__(
        self,
        parser_factory: ConfigParserFactory,
        value_validator: ConfigValueValidator,
        mapper: ProcessingConfigMapper,
    ) -> None:
        self.parser_factory = parser_factory
        self.value_validator = value_validator
        self.mapper = mapper

    def load(self, path: Path) -> ProcessingConfig:
        if not path.is_file():
            raise ConfigurationError(f"Configuration file does not exist: {path}")

        parser = self.parser_factory.create(path)
        parsed = parser.parse(path)
        config = self.value_validator.parse_object(parsed)
        return self.mapper.map(config)
