"""Typed raw configuration values."""

type ConfigValue = str | bool | list["ConfigValue"] | dict[str, "ConfigValue"] | None
type ConfigObject = dict[str, ConfigValue]
