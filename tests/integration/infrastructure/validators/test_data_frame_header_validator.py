"""Behavioral tests for physical DataFrame header validation."""

import pandas as pd
import pytest

from csv_data_cleaner.domain.errors import InputDataError
from csv_data_cleaner.infrastructure.validators.data_frame_header_validator import (
    DataFrameHeaderValidator,
)


def test_validator_returns_canonical_headers() -> None:
    frame = pd.DataFrame([["name", "email"], ["Ada", "ada@example.com"]])

    assert DataFrameHeaderValidator().validate(frame) == ("name", "email")


@pytest.mark.parametrize("header", [[None], [""], ["   "]])
def test_validator_rejects_empty_headers(header: list[object]) -> None:
    frame = pd.DataFrame([header, ["value"]])

    with pytest.raises(InputDataError, match="non-empty column headers"):
        DataFrameHeaderValidator().validate(frame)


def test_validator_rejects_duplicate_headers() -> None:
    frame = pd.DataFrame([["email", "email"], ["first@example.com", "second@example.com"]])

    with pytest.raises(InputDataError, match="duplicate column headers: email"):
        DataFrameHeaderValidator().validate(frame)
