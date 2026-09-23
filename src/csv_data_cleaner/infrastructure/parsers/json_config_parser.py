"""JSON configuration parser."""

import json
from pathlib import Path

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.contracts.config_parser import ConfigParser


class JsonConfigParser(ConfigParser):
    """Parse JSON configuration files."""

    def parse(self, path: Path) -> object:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ConfigurationError(f"Could not read configuration: {path}") from error
