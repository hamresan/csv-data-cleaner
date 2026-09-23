"""Integration tests for DataFrame input mapping."""

import pandas as pd
import pytest

from csv_data_cleaner.domain.errors import InputDataError
from csv_data_cleaner.infrastructure.mappers.cell_value_mapper import CellValueMapper
from csv_data_cleaner.infrastructure.mappers.data_frame_input_mapper import DataFrameInputMapper
from csv_data_cleaner.infrastructure.validators.data_frame_header_validator import (
    DataFrameHeaderValidator,
)


def build_mapper() -> DataFrameInputMapper:
    return DataFrameInputMapper(
        header_validator=DataFrameHeaderValidator(),
        cell_value_mapper=CellValueMapper(),
    )


def test_mapper_converts_dataframe_to_canonical_input_data() -> None:
    frame = pd.DataFrame([{"name": "Ada", "email": "ada@example.com"}, {"name": "Grace"}])

    result = build_mapper().map(frame)

    assert result.columns == ("name", "email")
    assert result.rows[0].number == 2
    assert result.rows[0].values == {"name": "Ada", "email": "ada@example.com"}
    assert result.rows[1].number == 3
    assert result.rows[1].values == {"name": "Grace", "email": None}


def test_mapper_rejects_empty_headers() -> None:
    frame = pd.DataFrame([["Ada"]], columns=[""])

    with pytest.raises(InputDataError):
        build_mapper().map(frame)
