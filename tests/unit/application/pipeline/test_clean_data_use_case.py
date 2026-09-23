"""Tests for top-level pipeline orchestration."""

from pathlib import Path

from tests.unit.application.pipeline.fakes import (
    FakeConfigLoader,
    FakeExporter,
    FakeInputReader,
    FakeReportCalculator,
)

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.application.deduplication import (
    DeduplicationSchemaValidator,
    RowDeduplicator,
)
from csv_data_cleaner.application.mappers import RowResultMapper
from csv_data_cleaner.application.normalization import (
    DateRowNormalizer,
    DateValueNormalizer,
    StringRowNormalizer,
    StringValueNormalizer,
)
from csv_data_cleaner.application.pipeline import CleanDataRequest, CleanDataUseCase
from csv_data_cleaner.application.processing import DatasetProcessor, RowProcessor
from csv_data_cleaner.application.transforms import (
    FilterRuleEvaluator,
    FilterSchemaValidator,
    FilterSortProcessor,
    RowFilter,
    RowSorter,
    SortValueKeyBuilder,
    SortSchemaValidator,
)
from csv_data_cleaner.application.validation import (
    DateValueValidator,
    EmailValueValidator,
    RequiredValueValidator,
    RowValidator,
)
from csv_data_cleaner.domain import (
    DataRow,
    FilterOperator,
    FilterRule,
    InputData,
    NormalizationPolicy,
    OutputFormat,
    ProcessingConfig,
    ProcessingSummary,
    SortRule,
)
from tests.unit.application.validation.fakes import FakeEmailSyntaxChecker


def processor() -> DatasetProcessor:
    parser = DateParser()
    return DatasetProcessor(
        row_processor=RowProcessor(
            string_normalizer=StringRowNormalizer(StringValueNormalizer()),
            date_normalizer=DateRowNormalizer(DateValueNormalizer(parser)),
            validator=RowValidator(
                RequiredValueValidator(),
                EmailValueValidator(FakeEmailSyntaxChecker(set())),
                DateValueValidator(parser),
            ),
            result_mapper=RowResultMapper(),
        ),
        row_deduplicator=RowDeduplicator(),
        deduplication_schema_validator=DeduplicationSchemaValidator(),
        filter_sort_processor=FilterSortProcessor(RowFilter(FilterRuleEvaluator()), RowSorter(SortValueKeyBuilder())),
        filter_schema_validator=FilterSchemaValidator(),
        sort_schema_validator=SortSchemaValidator(),
    )


def test_use_case_coordinates_pipeline_boundaries() -> None:
    config = ProcessingConfig(
        required_columns=(),
        email_columns=(),
        date_rules=(),
        normalization=NormalizationPolicy(),
        deduplication=None,
        filters=(FilterRule("country", FilterOperator.EQUALS, "OM"),),
        sorting=(SortRule("name"),),
        output_format=OutputFormat.CSV,
    )
    data = InputData(
        columns=("name", "country"),
        rows=(
            DataRow(2, {"name": "B", "country": "OM"}),
            DataRow(3, {"name": "A", "country": "US"}),
            DataRow(4, {"name": "A", "country": "OM"}),
        ),
    )
    summary = ProcessingSummary("input.csv", 3, 2, 0, 0, None)
    config_loader = FakeConfigLoader(config)
    input_reader = FakeInputReader(data)
    exporter = FakeExporter()
    report_calculator = FakeReportCalculator(summary)
    use_case = CleanDataUseCase(
        config_loader,
        input_reader,
        processor(),
        exporter,
        report_calculator,
    )
    request = CleanDataRequest(
        Path("input.csv"),
        Path("rules.yaml"),
        Path("output"),
        sheet="Customers",
    )

    result = use_case.execute(request)

    assert tuple(row.source_row.number for row in result.processing_result.rows) == (4, 2)
    assert tuple(row.source_row.number for row in result.processing_result.filtered_rows) == (3,)
    assert config_loader.calls == [Path("rules.yaml")]
    assert input_reader.calls == [(Path("input.csv"), "Customers")]
    assert exporter.calls == [(result.processing_result, config, Path("output"))]
    assert report_calculator.calls == [(Path("input.csv"), result.processing_result)]
    assert result.summary == summary
