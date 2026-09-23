"""Integration tests for concrete configuration parsers."""

import json
from pathlib import Path

import pytest
import yaml

from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.parsers.json_config_parser import JsonConfigParser
from csv_data_cleaner.infrastructure.parsers.yaml_config_parser import YamlConfigParser


def test_json_parser_reads_real_file(tmp_path: Path) -> None:
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"required_columns": ["email"]}), encoding="utf-8")

    assert JsonConfigParser().parse(path) == {"required_columns": ["email"]}


def test_yaml_parser_reads_real_file(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump({"required_columns": ["email"]}), encoding="utf-8")

    assert YamlConfigParser().parse(path) == {"required_columns": ["email"]}


@pytest.mark.parametrize("parser", [JsonConfigParser(), YamlConfigParser()])
def test_parser_rejects_malformed_real_file(tmp_path: Path, parser: object) -> None:
    path = tmp_path / ("config.json" if isinstance(parser, JsonConfigParser) else "config.yaml")
    path.write_text("{", encoding="utf-8")

    with pytest.raises(ConfigurationError):
        parser.parse(path)  # type: ignore[attr-defined]
