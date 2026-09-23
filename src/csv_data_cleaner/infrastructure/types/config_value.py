"""Typed raw configuration values."""

type ConfigValue = str | int | float | bool | list["ConfigValue"] | dict[str, "ConfigValue"] | None
type ConfigObject = dict[str, ConfigValue]
