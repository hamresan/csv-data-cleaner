"""Select the parser for a configuration file."""

from pathlib import Path

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.contracts.config_parser import ConfigParser
from csv_data_cleaner.infrastructure.parsers.json_config_parser import JsonConfigParser
from csv_data_cleaner.infrastructure.parsers.yaml_config_parser import YamlConfigParser


class ConfigParserFactory:
    """Resolve supported configuration parsers by file extension."""

    def create(self, path: Path) -> ConfigParser:
        suffix = path.suffix.lower()
        if suffix == ".json":
            return JsonConfigParser()
        if suffix in {".yaml", ".yml"}:
            return YamlConfigParser()
        raise ConfigurationError(f"Unsupported configuration format: {suffix}")
