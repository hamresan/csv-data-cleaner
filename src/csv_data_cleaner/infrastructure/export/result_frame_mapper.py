"""Map processing results to exportable pandas data frames."""

from pandas import DataFrame

from csv_data_cleaner.domain import DatasetProcessingResult


class ResultFrameMapper:
    """Build deterministic data frames while preserving required row representations."""

    def cleaned(self, result: DatasetProcessingResult) -> DataFrame:
        records = [dict(row.normalized_row.values) for row in result.valid_rows]
        return DataFrame.from_records(records, columns=result.columns)

    def invalid(self, result: DatasetProcessingResult) -> DataFrame:
        rows = sorted(result.all_invalid_rows, key=lambda row: row.source_row.number)
        records = [dict(row.source_row.values) for row in rows]
        return DataFrame.from_records(records, columns=result.columns)

    def duplicates(self, result: DatasetProcessingResult) -> DataFrame:
        duplicates = sorted(
            result.duplicate_rows,
            key=lambda duplicate: duplicate.row.source_row.number,
        )
        records = [dict(duplicate.row.source_row.values) for duplicate in duplicates]
        return DataFrame.from_records(records, columns=result.columns)
