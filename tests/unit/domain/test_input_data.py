"""Behavioral tests for canonical input data."""

import pytest

from csv_data_cleaner.domain import DataRow, InputData


def test_data_row_copies_and_protects_values() -> None:
    values = {"name": "Ada", "active": True}
    row = DataRow(number=2, values=values)

    values["name"] = "Changed"

    assert row.values == {"name": "Ada", "active": True}
    with pytest.raises(TypeError):
        row.values["name"] = "Grace"  # type: ignore[index]


def test_input_data_preserves_canonical_rows() -> None:
    row = DataRow(number=2, values={"email": "ada@example.com"})

    data = InputData(columns=("email",), rows=(row,))

    assert data.columns == ("email",)
    assert data.rows == (row,)
