"""JSON and YAML configuration loader."""

import json
from pathlib import Path
from typing import Any

import yaml

from csv_data_cleaner.application.ports import ConfigLoader
from csv_data_cleaner.domain import (
    DeduplicationKeep,
    DeduplicationPolicy,
    OutputFormat,
    ProcessingConfig,
    SortRule,
)
from csv_data_cleaner.domain.errors import ConfigurationError


class FileConfigLoader(ConfigLoader):
    """Load supported config files and map them to validated domain configuration."""

    def load(self, path: Path) -> ProcessingConfig:
        raw = self._read(path)
        return self._map(raw)

    def _read(self, path: Path) -> dict[str, Any]:
        if not path.is_file():
            raise ConfigurationError(f"Configuration file does not exist: {path}")

        try:
            if path.suffix.lower() == ".json":
                data = json.loads(path.read_text(encoding="utf-8"))
            elif path.suffix.lower() in {".yaml", ".yml"}:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            else:
                raise ConfigurationError(f"Unsupported configuration format: {path.suffix}")
        except (OSError, json.JSONDecodeError, yaml.YAMLError) as error:
            raise ConfigurationError(f"Could not read configuration: {path}") from error

        if not isinstance(data, dict):
            raise ConfigurationError("Configuration root must be an object.")
        return data

    def _map(self, data: dict[str, Any]) -> ProcessingConfig:
        try:
            validation = data.get("validation", {})
            output = data.get("output", {})
            deduplication = data.get("deduplication")
            sorting = data.get("sorting", [])

            if not isinstance(validation, dict) or not isinstance(output, dict):
                raise TypeError
            if not isinstance(sorting, list):
                raise TypeError

            deduplication_policy = None
            if deduplication is not None:
                if not isinstance(deduplication, dict):
                    raise TypeError
                deduplication_policy = DeduplicationPolicy(
                    columns=self._strings(deduplication.get("columns", []), "deduplication.columns"),
                    keep=DeduplicationKeep(deduplication.get("keep", "first")),
                )

            sort_rules = tuple(
                SortRule(
                    column=self._required_string(item, "sorting.column"),
                    ascending=self._boolean(item.get("ascending", True), "sorting.ascending"),
                )
                for item in self._objects(sorting, "sorting")
            )

            return ProcessingConfig(
                required_columns=self._strings(data.get("required_columns", []), "required_columns"),
                email_columns=self._strings(
                    validation.get("email_columns", []), "validation.email_columns"
                ),
                date_columns=self._strings(
                    validation.get("date_columns", []), "validation.date_columns"
                ),
                deduplication=deduplication_policy,
                sorting=sort_rules,
                output_format=OutputFormat(output.get("format", "csv")),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ConfigurationError("Configuration contains invalid values.") from error

    @staticmethod
    def _strings(value: Any, field: str) -> tuple[str, ...]:
        if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
            raise ConfigurationError(f"{field} must be a list of non-empty strings.")
        return tuple(value)

    @staticmethod
    def _objects(value: list[Any], field: str) -> tuple[dict[str, Any], ...]:
        if any(not isinstance(item, dict) for item in value):
            raise ConfigurationError(f"{field} must contain objects.")
        return tuple(value)

    @staticmethod
    def _required_string(value: dict[str, Any], field: str) -> str:
        item = value.get("column")
        if not isinstance(item, str) or not item:
            raise ConfigurationError(f"{field} must be a non-empty string.")
        return item

    @staticmethod
    def _boolean(value: Any, field: str) -> bool:
        if not isinstance(value, bool):
            raise ConfigurationError(f"{field} must be a boolean.")
        return value
