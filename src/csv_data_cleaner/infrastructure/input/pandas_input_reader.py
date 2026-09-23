"""Pandas-backed CSV and XLSX input adapter."""

from pathlib import Path

import pandas as pd

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
                frame = pd.read_excel(path, sheet_name=sheet or 0, dtype=object)
            else:
                raise InputDataError(f"Unsupported input format: {suffix}")
        except (OSError, ValueError, pd.errors.ParserError) as error:
            raise InputDataError(f"Could not read input file: {path}") from error

        if frame.columns.empty or any(not str(column).strip() for column in frame.columns):
            raise InputDataError("Input must contain non-empty column headers.")

        columns = tuple(str(column) for column in frame.columns)
        rows = tuple(
            DataRow(
                number=index + 2,
                values={
                    column: None if pd.isna(value) else value
                    for column, value in zip(columns, row, strict=True)
                },
            )
            for index, row in enumerate(frame.itertuples(index=False, name=None))
        )
        return InputData(columns=columns, rows=rows)
