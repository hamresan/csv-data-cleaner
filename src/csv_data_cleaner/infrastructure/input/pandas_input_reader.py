"""Pandas-backed CSV and XLSX input adapter."""

from pathlib import Path
from typing import cast

import pandas as pd
from pandas import DataFrame

from csv_data_cleaner.application.ports import InputReader
from csv_data_cleaner.domain import DataRow, InputData
from csv_data_cleaner.domain.errors import InputDataError


class PandasInputReader(InputReader):
    """Read CSV/XLSX files into the canonical input representation."""

    def read(self, path: Path, *, sheet: str | None = None) -> InputData:
        if not path.is_file():
            raise InputDataError(f"Input file does not exist: {path}")

        suffix = path.suffix.lower()
        try:
            if suffix == ".csv":
                frame = pd.read_csv(path, dtype=object)
            elif suffix == ".xlsx":
                frame = cast(
                    DataFrame,
                    pd.read_excel(path, sheet_name=sheet or 0, dtype=object),
                )
            else:
                raise InputDataError(f"Unsupported input format: {suffix}")
        except (OSError, ValueError, pd.errors.ParserError) as error:
            raise InputDataError(f"Could not read input file: {path}") from error

        columns = tuple(str(column) for column in frame.columns)
        if not columns or any(not column.strip() for column in columns):
            raise InputDataError("Input must contain non-empty column headers.")

        rows = tuple(
            DataRow(
                number=index + 2,
                values={
                    column: self._cell_value(value)
                    for column, value in zip(columns, row, strict=True)
                },
            )
            for index, row in enumerate(frame.itertuples(index=False, name=None))
        )
        return InputData(columns=columns, rows=rows)

    @staticmethod
    def _cell_value(value: object) -> str | int | float | bool | None:
        if pd.isna(value):
            return None
        if isinstance(value, str | int | float | bool):
            return value
        return str(value)
