"""Behavioral tests for configuration parser selection."""

from pathlib import Path

import pytest

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.factories.config_parser_factory import ConfigParserFactory
from csv_data_cleaner.infrastructure.parsers.json_config_parser import JsonConfigParser
from csv_data_cleaner.infrastructure.parsers.yaml_config_parser import YamlConfigParser


@pytest.mark.parametrize(
    ("path", "parser_type"),
    [
        (Path("config.json"), JsonConfigParser),
        (Path("config.yaml"), YamlConfigParser),
        (Path("config.yml"), YamlConfigParser),
    ],
)
def test_factory_selects_parser_by_extension(path: Path, parser_type: type[object]) -> None:
    assert isinstance(ConfigParserFactory().create(path), parser_type)


def test_factory_rejects_unsupported_extension() -> None:
    with pytest.raises(ConfigurationError):
        ConfigParserFactory().create(Path("config.toml"))
