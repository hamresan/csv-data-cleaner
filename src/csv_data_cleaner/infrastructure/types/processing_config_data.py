"""Validated configuration data used at the infrastructure boundary."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeduplicationConfigData:
    """Validated deduplication configuration."""

    columns: tuple[str, ...]
    keep: str


@dataclass(frozen=True, slots=True)
class SortConfigData:
    """Validated sort configuration."""

    column: str
    ascending: bool


@dataclass(frozen=True, slots=True)
class ProcessingConfigData:
    """Validated configuration ready for domain mapping."""

    required_columns: tuple[str, ...]
    email_columns: tuple[str, ...]
    date_columns: tuple[str, ...]
    deduplication: DeduplicationConfigData | None
    sorting: tuple[SortConfigData, ...]
    output_format: str
