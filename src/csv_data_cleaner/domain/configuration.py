"""Processing configuration domain models."""

from dataclasses import dataclass
from enum import StrEnum


class DeduplicationKeep(StrEnum):
    """Record retention strategy for duplicate groups."""

    FIRST = "first"
    LAST = "last"


class OutputFormat(StrEnum):
    """Supported cleaned-data output formats."""

    CSV = "csv"
    XLSX = "xlsx"


@dataclass(frozen=True, slots=True)
class SortRule:
    """A configured output sort rule."""

    column: str
    ascending: bool = True


@dataclass(frozen=True, slots=True)
class DeduplicationPolicy:
    """Columns and retention strategy used to identify duplicates."""

    columns: tuple[str, ...]
    keep: DeduplicationKeep = DeduplicationKeep.FIRST


@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    """Validated configuration consumed by the application pipeline."""

    required_columns: tuple[str, ...]
    email_columns: tuple[str, ...]
    date_columns: tuple[str, ...]
    deduplication: DeduplicationPolicy | None
    sorting: tuple[SortRule, ...]
    output_format: OutputFormat
