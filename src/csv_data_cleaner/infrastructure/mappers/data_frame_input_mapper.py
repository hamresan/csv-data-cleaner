"""Map pandas data frames to canonical input data."""

from pandas import DataFrame

from csv_data_cleaner.domain import DataRow, InputData
from csv_data_cleaner.infrastructure.mappers.cell_value_mapper import CellValueMapper
from csv_data_cleaner.infrastructure.validators.data_frame_header_validator import (
    DataFrameHeaderValidator,
)


class DataFrameInputMapper:
    """Convert a raw pandas DataFrame to the canonical domain representation."""

    def __init__(
        self,
        header_validator: DataFrameHeaderValidator,
        cell_value_mapper: CellValueMapper,
    ) -> None:
        self.header_validator = header_validator
        self.cell_value_mapper = cell_value_mapper

    def map(self, frame: DataFrame) -> InputData:
        columns = self.header_validator.validate(frame)
        rows = tuple(
            DataRow(
                number=index + 2,
                values={
                    column: self.cell_value_mapper.map(value)
                    for column, value in zip(columns, row, strict=True)
                },
            )
            for index, row in enumerate(
                frame.iloc[1:].itertuples(index=False, name=None)
            )
        )
        return InputData(columns=columns, rows=rows)
