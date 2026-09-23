"""Immutable domain models used by the cleaning pipeline."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType

type CellValue = str | int | float | bool | None


class DeduplicationKeep(StrEnum):
    """Record retention strategy for duplicate groups."""

    FIRST = "first"
    LAST = "last"


class OutputFormat(StrEnum):
    """Supported cleaned-data output formats."""

    CSV = "csv"
    XLSX = "xlsx"


@dataclass(frozen=True, slots=True)
class DataRow:
    """A canonical input row with its original source position."""

    number: int
    values: Mapping[str, CellValue]

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", MappingProxyType(dict(self.values)))


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A validation failure associated with one source row."""

    row_number: int
    column: str
    code: str
    message: str


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


@dataclass(frozen=True, slots=True)
class InputData:
    """Canonical tabular input independent of its physical file format."""

    columns: tuple[str, ...]
    rows: tuple[DataRow, ...]


@dataclass(frozen=True, slots=True)
class ProcessingSummary:
    """Machine-readable processing counters and output location."""

    input_file: str
    processed_records: int
    valid_records: int
    invalid_records: int
    duplicate_records: int
    output_file: str | None
