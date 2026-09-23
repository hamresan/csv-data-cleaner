"""Pandas-backed CSV and XLSX input adapter."""

from pathlib import Path

import pandas as pd
from pandas import DataFrame

from csv_data_cleaner.application.ports import InputReader
from csv_data_cleaner.domain import InputData
from csv_data_cleaner.domain.errors import InputDataError
from csv_data_cleaner.infrastructure.mappers.data_frame_input_mapper import DataFrameInputMapper


class PandasInputReader(InputReader):
    """Read supported tabular files and delegate domain mapping."""

    def __init__(self, mapper: DataFrameInputMapper) -> None:
        self.mapper = mapper

    def read(self, path: Path, *, sheet: str | None = None) -> InputData:
        if not path.is_file():
            raise InputDataError(f"Input file does not exist: {path}")

        suffix = path.suffix.lower()
        try:
            if suffix == ".csv":
                frame = pd.read_csv(path, dtype=object)
            elif suffix == ".xlsx":
                frame: DataFrame = pd.read_excel(  # pyright: ignore[reportUnknownMemberType]
                    path,
                    sheet_name=sheet or 0,
                    dtype=object,
                )
            else:
                raise InputDataError(f"Unsupported input format: {suffix}")
        except (OSError, ValueError, pd.errors.ParserError) as error:
            raise InputDataError(f"Could not read input file: {path}") from error

        return self.mapper.map(frame)
