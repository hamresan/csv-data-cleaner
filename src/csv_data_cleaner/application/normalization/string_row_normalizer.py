"""Normalize string values in canonical input rows."""

from csv_data_cleaner.application.normalization.string_value_normalizer import StringValueNormalizer
from csv_data_cleaner.domain import DataRow, NormalizationPolicy


class StringRowNormalizer:
    """Apply string normalization to every value while preserving row identity."""

    def __init__(self, value_normalizer: StringValueNormalizer) -> None:
        self.value_normalizer = value_normalizer

    def normalize(self, row: DataRow, policy: NormalizationPolicy) -> DataRow:
        return DataRow(
            number=row.number,
            values={
                column: self.value_normalizer.normalize(value, policy)
                for column, value in row.values.items()
            },
        )
