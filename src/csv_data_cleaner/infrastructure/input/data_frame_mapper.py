"""Map pandas data frames to canonical input data."""

import pandas as pd
from pandas import DataFrame

from csv_data_cleaner.domain import DataRow, InputData
from csv_data_cleaner.domain.errors import InputDataError


class DataFrameInputMapper:
    """Convert a pandas DataFrame to the canonical domain representation."""

    def map(self, frame: DataFrame) -> InputData:
        columns = tuple(str(column) for column in frame.columns)
        if not columns or any(not column.strip() for column in columns):
            raise InputDataError("Input must contain non-empty column headers.")

        rows = tuple(
            DataRow(
                number=index + 2,
                values={
                    column: self.cell_value(value)
                    for column, value in zip(columns, row, strict=True)
                },
            )
            for index, row in enumerate(frame.itertuples(index=False, name=None))
        )
        return InputData(columns=columns, rows=rows)

    def cell_value(self, value: object) -> str | int | float | bool | None:
        if pd.isna(value):
            return None
        if isinstance(value, str | int | float | bool):
            return value
        return str(value)
