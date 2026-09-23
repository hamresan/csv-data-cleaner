"""Validate deduplication columns against the input schema."""

from csv_data_cleaner.domain import InputData
from csv_data_cleaner.domain.configuration import DeduplicationPolicy
from csv_data_cleaner.domain.errors import InputDataError


class DeduplicationSchemaValidator:
    """Ensure configured duplicate-key columns exist in the input data."""

    def validate(self, input_data: InputData, policy: DeduplicationPolicy) -> None:
        missing_columns = tuple(
            column for column in policy.columns if column not in input_data.columns
        )
        if missing_columns:
            columns = ", ".join(missing_columns)
            raise InputDataError(f"Missing deduplication columns: {columns}")
