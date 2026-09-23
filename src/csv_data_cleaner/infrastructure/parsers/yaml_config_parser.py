"""YAML configuration parser."""

from pathlib import Path

import yaml

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.contracts.config_parser import ConfigParser


class YamlConfigParser(ConfigParser):
    """Parse YAML configuration files."""

    def parse(self, path: Path) -> object:
        try:
            return yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as error:
            raise ConfigurationError(f"Could not read configuration: {path}") from error
