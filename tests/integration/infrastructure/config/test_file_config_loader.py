"""Integration tests for JSON/YAML configuration loading."""

import json
from pathlib import Path

import pytest
import yaml

from csv_data_cleaner.domain import DeduplicationKeep, OutputFormat
from csv_data_cleaner.domain.errors import ConfigurationError
from csv_data_cleaner.infrastructure.config import FileConfigLoader
from csv_data_cleaner.infrastructure.factories.config_parser_factory import ConfigParserFactory
from csv_data_cleaner.infrastructure.mappers.processing_config_mapper import ProcessingConfigMapper
from csv_data_cleaner.infrastructure.validators.config_value_validator import ConfigValueValidator
from csv_data_cleaner.infrastructure.validators.processing_config_validator import (
    ProcessingConfigValidator,
)

CONFIG = {
    "required_columns": ["name", "email"],
    "validation": {"email_columns": ["email"], "date_columns": []},
    "deduplication": {"columns": ["email"], "keep": "last"},
    "sorting": [{"column": "name", "ascending": True}],
    "output": {"format": "xlsx"},
}


def build_loader() -> FileConfigLoader:
    return FileConfigLoader(
        parser_factory=ConfigParserFactory(),
        value_validator=ConfigValueValidator(),
        config_validator=ProcessingConfigValidator(),
        mapper=ProcessingConfigMapper(),
    )


@pytest.mark.parametrize("suffix", [".json", ".yaml"])
def test_supported_config_formats_map_to_same_domain_config(tmp_path: Path, suffix: str) -> None:
    path = tmp_path / f"rules{suffix}"
    if suffix == ".json":
        path.write_text(json.dumps(CONFIG), encoding="utf-8")
    else:
        path.write_text(yaml.safe_dump(CONFIG), encoding="utf-8")

    config = build_loader().load(path)

    assert config.required_columns == ("name", "email")
    assert config.deduplication is not None
    assert config.deduplication.keep is DeduplicationKeep.LAST
    assert config.output_format is OutputFormat.XLSX


@pytest.mark.parametrize(
    ("filename", "content"),
    [
        ("missing.toml", ""),
        ("rules.txt", "{}"),
        ("rules.json", "[]"),
        ("broken.json", "{"),
    ],
)
def test_invalid_configurations_are_rejected(tmp_path: Path, filename: str, content: str) -> None:
    path = tmp_path / filename
    if filename != "missing.toml":
        path.write_text(content, encoding="utf-8")

    with pytest.raises(ConfigurationError):
        build_loader().load(path)
