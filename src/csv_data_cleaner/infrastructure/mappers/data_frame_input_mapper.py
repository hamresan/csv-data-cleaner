"""Map pandas data frames to canonical input data."""

from pandas import DataFrame

from csv_data_cleaner.domain import DataRow, InputData
from csv_data_cleaner.domain.errors import InputDataError


class DataFrameInputMapper:
    """Convert a raw pandas DataFrame to the canonical domain representation."""

    def map(self, frame: DataFrame) -> InputData:
        if frame.empty:
            raise InputDataError("Input must contain a header row.")

        raw_headers = tuple(frame.iloc[0].tolist())
        if any(self._is_missing(value) or not str(value).strip() for value in raw_headers):
            raise InputDataError("Input must contain non-empty column headers.")

        columns = tuple(str(value) for value in raw_headers)
        rows = tuple(
            DataRow(
                number=index + 2,
                values={
                    column: self.cell_value(value)
                    for column, value in zip(columns, row, strict=True)
                },
            )
            for index, row in enumerate(
                frame.iloc[1:].itertuples(index=False, name=None)
            )
        )
        return InputData(columns=columns, rows=rows)

    def cell_value(self, value: object) -> str | int | float | bool | None:
        if self._is_missing(value):
            return None
        if isinstance(value, str | int | float | bool):
            return value
        return str(value)

    def _is_missing(self, value: object) -> bool:
        return value is None or (isinstance(value, float) and value != value)
