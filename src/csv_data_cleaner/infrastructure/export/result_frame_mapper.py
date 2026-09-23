"""Map processing results to exportable pandas data frames."""

from pandas import DataFrame

from csv_data_cleaner.domain import DatasetProcessingResult


class ResultFrameMapper:
    """Build deterministic data frames while preserving required row representations."""

    def cleaned(self, result: DatasetProcessingResult) -> DataFrame:
        records = [dict(row.normalized_row.values) for row in result.valid_rows]
        return DataFrame.from_records(records, columns=result.columns)

    def invalid(self, result: DatasetProcessingResult) -> DataFrame:
        records = [dict(row.source_row.values) for row in result.all_invalid_rows]
        return DataFrame.from_records(records, columns=result.columns)

    def duplicates(self, result: DatasetProcessingResult) -> DataFrame:
        records = [dict(duplicate.row.source_row.values) for duplicate in result.duplicate_rows]
        return DataFrame.from_records(records, columns=result.columns)
