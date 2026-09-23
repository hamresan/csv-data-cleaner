"""Typed raw configuration values."""

from typing import TypeAlias

ConfigValue: TypeAlias = str | bool | None | list["ConfigValue"] | dict[str, "ConfigValue"]
ConfigObject: TypeAlias = dict[str, ConfigValue]
