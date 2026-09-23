"""Tests for top-level pipeline orchestration."""

from pathlib import Path

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
    SortSchemaValidator,
    SortValueKeyBuilder,
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

from ..validation.fakes import FakeEmailSyntaxChecker
from .fakes import (
    FakeConfigLoader,
    FakeExporter,
    FakeInputReader,
    FakeReportCalculator,
    FakeReportWriter,
)


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
        filter_sort_processor=FilterSortProcessor(
            RowFilter(FilterRuleEvaluator()),
            RowSorter(SortValueKeyBuilder()),
        ),
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
    output_file = Path("output/cleaned.csv")
    summary = ProcessingSummary(
        input_file="input.csv",
        processed_records=3,
        valid_records=3,
        invalid_records=0,
        duplicate_records=0,
        exported_records=2,
        output_file=str(output_file),
    )
    config_loader = FakeConfigLoader(config)
    input_reader = FakeInputReader(data)
    exporter = FakeExporter(output_file)
    report_calculator = FakeReportCalculator(summary)
    report_writer = FakeReportWriter()
    use_case = CleanDataUseCase(
        config_loader,
        input_reader,
        processor(),
        exporter,
        report_calculator,
        report_writer,
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
    assert result.processing_result.columns == ("name", "country")
    assert config_loader.calls == [Path("rules.yaml")]
    assert input_reader.calls == [(Path("input.csv"), "Customers")]
    assert exporter.calls == [(result.processing_result, config, Path("output"))]
    assert report_calculator.calls == [
        (Path("input.csv"), result.processing_result, output_file)
    ]
    assert report_writer.calls == [(summary, Path("output"))]
    assert result.summary == summary
