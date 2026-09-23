"""Validate and normalize physical DataFrame headers."""

from pandas import DataFrame

from csv_data_cleaner.domain.errors import InputDataError


class DataFrameHeaderValidator:
    """Validate the physical header row and return canonical column names."""

    def validate(self, frame: DataFrame) -> tuple[str, ...]:
        if frame.empty:
            raise InputDataError("Input must contain a header row.")

        headers = tuple(frame.iloc[0].tolist())
        if any(
            value is None
            or (isinstance(value, float) and value != value)
            or not str(value).strip()
            for value in headers
        ):
            raise InputDataError("Input must contain non-empty column headers.")

        return tuple(str(value) for value in headers)
