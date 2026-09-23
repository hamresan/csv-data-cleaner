"""Behavioral tests for transform schema validation."""

import pytest

from csv_data_cleaner.application.transforms import FilterSchemaValidator, SortSchemaValidator
from csv_data_cleaner.domain import FilterOperator, FilterRule, InputData, SortRule
from csv_data_cleaner.domain.errors import InputDataError


def test_filter_schema_rejects_missing_columns() -> None:
    with pytest.raises(InputDataError, match="Missing filter columns: country"):
        FilterSchemaValidator().validate(
            InputData(columns=("name",), rows=()),
            (FilterRule("country", FilterOperator.EQUALS, "OM"),),
        )


def test_sort_schema_rejects_missing_columns() -> None:
    with pytest.raises(InputDataError, match="Missing sorting columns: country"):
        SortSchemaValidator().validate(
            InputData(columns=("name",), rows=()),
            (SortRule("country"),),
        )
