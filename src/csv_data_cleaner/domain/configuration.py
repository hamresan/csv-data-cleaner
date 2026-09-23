"""Processing configuration domain models."""

from dataclasses import dataclass
from enum import StrEnum

from csv_data_cleaner.domain.input_data import CellValue


class DeduplicationKeep(StrEnum):
    """Record retention strategy for duplicate groups."""

    FIRST = "first"
    LAST = "last"


class OutputFormat(StrEnum):
    """Supported cleaned-data output formats."""

    CSV = "csv"
    XLSX = "xlsx"


class FilterOperator(StrEnum):
    """Supported row-filter comparison operators."""

    EQUALS = "equals"
    NOT_EQUALS = "not_equals"


@dataclass(frozen=True, slots=True)
class FilterRule:
    """A configured inclusion or exclusion filter."""

    column: str
    operator: FilterOperator
    value: CellValue
    include: bool = True


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
class DateValidationRule:
    """Accepted source formats for one configured date column."""

    column: str
    formats: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class NormalizationPolicy:
    """Configured canonicalization behavior for input values."""

    trim_whitespace: bool = True
    empty_strings_as_null: bool = True
    casefold_columns: tuple[str, ...] = ()
    date_output_format: str = "%Y-%m-%d"


@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    """Validated configuration consumed by the application pipeline."""

    required_columns: tuple[str, ...]
    email_columns: tuple[str, ...]
    date_rules: tuple[DateValidationRule, ...]
    normalization: NormalizationPolicy
    deduplication: DeduplicationPolicy | None
    filters: tuple[FilterRule, ...] = ()
    sorting: tuple[SortRule, ...]
    output_format: OutputFormat

    @property
    def date_columns(self) -> tuple[str, ...]:
        """Return configured date columns in deterministic order."""

        return tuple(rule.column for rule in self.date_rules)
