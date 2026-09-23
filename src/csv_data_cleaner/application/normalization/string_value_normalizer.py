"""Normalize string cell values."""

from csv_data_cleaner.domain import CellValue, NormalizationPolicy


class StringValueNormalizer:
    """Apply configured canonical string normalization."""

    def normalize(
        self,
        value: CellValue,
        policy: NormalizationPolicy,
        *,
        casefold: bool = False,
    ) -> CellValue:
        if not isinstance(value, str):
            return value

        normalized = value.strip() if policy.trim_whitespace else value
        if policy.empty_strings_as_null and normalized == "":
            return None
        return normalized.casefold() if casefold else normalized
