"""JSON and YAML configuration loader."""

import json
from pathlib import Path
from typing import TypeAlias

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

ConfigValue: TypeAlias = (
    str | bool | None | list["ConfigValue"] | dict[str, "ConfigValue"]
)
ConfigObject: TypeAlias = dict[str, ConfigValue]


class FileConfigLoader(ConfigLoader):
    """Load supported config files and map them to validated domain configuration."""

    def load(self, path: Path) -> ProcessingConfig:
        data = self._read(path)
        return self._map(data)

    def _read(self, path: Path) -> ConfigObject:
        if not path.is_file():
            raise ConfigurationError(f"Configuration file does not exist: {path}")

        try:
            if path.suffix.lower() == ".json":
                data: object = json.loads(path.read_text(encoding="utf-8"))
            elif path.suffix.lower() in {".yaml", ".yml"}:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            else:
                raise ConfigurationError(f"Unsupported configuration format: {path.suffix}")
        except (OSError, json.JSONDecodeError, yaml.YAMLError) as error:
            raise ConfigurationError(f"Could not read configuration: {path}") from error

        return self._config_object(data, "Configuration root")

    def _map(self, data: ConfigObject) -> ProcessingConfig:
        validation = self._optional_object(data.get("validation"), "validation")
        output = self._optional_object(data.get("output"), "output")
        deduplication = self._optional_object(
            data.get("deduplication"), "deduplication", allow_none=True
        )
        sorting = self._objects(data.get("sorting", []), "sorting")

        policy = None
        if deduplication is not None:
            policy = DeduplicationPolicy(
                columns=self._strings(
                    deduplication.get("columns", []),
                    "deduplication.columns",
                ),
                keep=self._deduplication_keep(deduplication.get("keep", "first")),
            )

        return ProcessingConfig(
            required_columns=self._strings(
                data.get("required_columns", []),
                "required_columns",
            ),
            email_columns=self._strings(
                validation.get("email_columns", []),
                "validation.email_columns",
            ),
            date_columns=self._strings(
                validation.get("date_columns", []),
                "validation.date_columns",
            ),
            deduplication=policy,
            sorting=tuple(
                SortRule(
                    column=self._sort_column(item),
                    ascending=self._boolean(item.get("ascending", True), "sorting.ascending"),
                )
                for item in sorting
            ),
            output_format=self._output_format(output.get("format", "csv")),
        )

    @staticmethod
    def _config_object(value: object, field: str) -> ConfigObject:
        if not isinstance(value, dict):
            raise ConfigurationError(f"{field} must be an object.")

        result: ConfigObject = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ConfigurationError(f"{field} keys must be strings.")
            result[key] = FileConfigLoader._config_value(item, field)
        return result

    @staticmethod
    def _config_value(value: object, field: str) -> ConfigValue:
        if value is None or isinstance(value, str | bool):
            return value
        if isinstance(value, list):
            return [FileConfigLoader._config_value(item, field) for item in value]
        if isinstance(value, dict):
            return FileConfigLoader._config_object(value, field)
        raise ConfigurationError(f"{field} contains an unsupported value.")

    @staticmethod
    def _optional_object(
        value: ConfigValue,
        field: str,
        *,
        allow_none: bool = False,
    ) -> ConfigObject | None:
        if value is None:
            if allow_none:
                return None
            return {}
        if not isinstance(value, dict):
            raise ConfigurationError(f"{field} must be an object.")
        return value

    @staticmethod
    def _strings(value: ConfigValue, field: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise ConfigurationError(f"{field} must be a list of non-empty strings.")

        result: list[str] = []
        for item in value:
            if not isinstance(item, str) or not item:
                raise ConfigurationError(f"{field} must be a list of non-empty strings.")
            result.append(item)
        return tuple(result)

    @staticmethod
    def _objects(value: ConfigValue, field: str) -> tuple[ConfigObject, ...]:
        if not isinstance(value, list):
            raise ConfigurationError(f"{field} must be a list.")

        result: list[ConfigObject] = []
        for item in value:
            if not isinstance(item, dict):
                raise ConfigurationError(f"{field} must contain objects.")
            result.append(item)
        return tuple(result)

    @staticmethod
    def _sort_column(value: ConfigObject) -> str:
        column = value.get("column")
        if not isinstance(column, str) or not column:
            raise ConfigurationError("sorting.column must be a non-empty string.")
        return column

    @staticmethod
    def _boolean(value: ConfigValue, field: str) -> bool:
        if not isinstance(value, bool):
            raise ConfigurationError(f"{field} must be a boolean.")
        return value

    @staticmethod
    def _deduplication_keep(value: ConfigValue) -> DeduplicationKeep:
        if not isinstance(value, str):
            raise ConfigurationError("deduplication.keep must be first or last.")
        try:
            return DeduplicationKeep(value)
        except ValueError as error:
            raise ConfigurationError("deduplication.keep must be first or last.") from error

    @staticmethod
    def _output_format(value: ConfigValue) -> OutputFormat:
        if not isinstance(value, str):
            raise ConfigurationError("output.format must be csv or xlsx.")
        try:
            return OutputFormat(value)
        except ValueError as error:
            raise ConfigurationError("output.format must be csv or xlsx.") from error
