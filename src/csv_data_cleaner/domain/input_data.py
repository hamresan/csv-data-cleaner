"""Canonical input data models."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

type CellValue = str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class DataRow:
    """A canonical input row with its original source position."""

    number: int
    values: Mapping[str, CellValue]

    def __post_init__(self) -> None:
        object.__setattr__(self, "values", MappingProxyType(dict(self.values)))


@dataclass(frozen=True, slots=True)
class InputData:
    """Canonical tabular input independent of its physical file format."""

    columns: tuple[str, ...]
    rows: tuple[DataRow, ...]
