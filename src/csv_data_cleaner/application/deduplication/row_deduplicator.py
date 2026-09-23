"""Deduplicate processed rows by configured normalized key values."""

from csv_data_cleaner.domain.configuration import DeduplicationKeep, DeduplicationPolicy
from csv_data_cleaner.domain.deduplication import DeduplicationResult, DuplicateRow
from csv_data_cleaner.domain.input_data import CellValue
from csv_data_cleaner.domain.row_processing import RowProcessingResult

type DuplicateKey = tuple[CellValue, ...]


class RowDeduplicator:
    """Partition processed rows into retained rows and dropped duplicates."""

    def deduplicate(
        self,
        rows: tuple[RowProcessingResult, ...],
        policy: DeduplicationPolicy,
    ) -> DeduplicationResult:
        keys = tuple(
            tuple(row.normalized_row.values[column] for column in policy.columns)
            for row in rows
        )
        retained_index_by_key: dict[DuplicateKey, int] = {}

        indices = range(len(rows))
        if policy.keep is DeduplicationKeep.LAST:
            indices = reversed(range(len(rows)))

        for index in indices:
            retained_index_by_key.setdefault(keys[index], index)

        retained_indices = set(retained_index_by_key.values())
        retained_rows = tuple(
            row for index, row in enumerate(rows) if index in retained_indices
        )
        duplicate_rows = tuple(
            DuplicateRow(
                row=row,
                retained_row_number=rows[retained_index_by_key[keys[index]]].source_row.number,
                key=keys[index],
            )
            for index, row in enumerate(rows)
            if index not in retained_indices
        )

        return DeduplicationResult(
            retained_rows=retained_rows,
            duplicate_rows=duplicate_rows,
        )
