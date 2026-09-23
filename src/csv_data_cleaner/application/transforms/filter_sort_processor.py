"""Apply Stage 4 filtering and sorting to retained processed rows."""

from csv_data_cleaner.application.transforms.row_filter import RowFilter
from csv_data_cleaner.application.transforms.row_sorter import RowSorter
from csv_data_cleaner.domain import FilterRule, RowProcessingResult, SortRule


class FilterSortProcessor:
    """Coordinate filtering first, then ordered sorting."""

    def __init__(self, row_filter: RowFilter, row_sorter: RowSorter) -> None:
        self.row_filter = row_filter
        self.row_sorter = row_sorter

    def process(
        self,
        rows: tuple[RowProcessingResult, ...],
        filters: tuple[FilterRule, ...],
        sorting: tuple[SortRule, ...],
    ) -> tuple[tuple[RowProcessingResult, ...], tuple[RowProcessingResult, ...]]:
        retained, filtered = self.row_filter.apply(rows, filters)
        return self.row_sorter.sort(retained, sorting), filtered
