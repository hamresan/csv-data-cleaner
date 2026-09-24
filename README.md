# CSV Data Cleaner

[![Checks](https://github.com/hamresan/csv-data-cleaner/actions/workflows/checks.yml/badge.svg)](https://github.com/hamresan/csv-data-cleaner/actions/workflows/checks.yml)

A configurable local command-line tool for cleaning, validating, deduplicating, filtering, sorting, exporting, and reporting on CSV and Excel data.

## Features

- Read `.csv` and `.xlsx` input files.
- Validate required values, email addresses, and configurable date formats.
- Normalize whitespace, empty strings, selected string columns, and dates.
- Remove duplicates using one or more columns with `first` or `last` retention.
- Preserve original invalid and duplicate rows in review exports.
- Apply ordered inclusion/exclusion filters and stable multi-column sorting.
- Export cleaned data as CSV or XLSX.
- Produce a deterministic JSON processing report.
- Preview processing with `--dry-run` without writing output files.
- Return concise CLI errors for expected input, configuration, and output failures.

The processing pipeline is:

```text
read -> normalize/validate -> deduplicate -> filter -> sort -> export/report
```

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
git clone https://github.com/hamresan/csv-data-cleaner.git
cd csv-data-cleaner
uv sync --locked
```

## Quick start

The repository includes a complete runnable example:

```bash
uv run csv-data-cleaner clean \
  --input examples/customers.csv \
  --config examples/rules.yaml \
  --output-dir output
```

Expected terminal output:

```text
Processed records: 5
Valid records: 3
Invalid records: 1
Duplicate records: 1
Exported records: 2
Output file: output/cleaned.csv
Report file: output/report.json
```

The command creates:

```text
output/
├── cleaned.csv
├── invalid_rows.csv
├── duplicate_rows.csv
└── report.json
```

Reference outputs are committed under `examples/expected/` so the example result can be inspected without running the command.

## Configuration

Configuration files may be YAML or JSON. The supported configuration surface is:

| Setting | Accepted value | Default |
| --- | --- | --- |
| `required_columns` | List of column names | `[]` |
| `validation.email_columns` | List of column names | `[]` |
| `validation.date_columns` | List of column names | `[]` |
| `validation.date_formats.<column>` | Non-empty list of `strptime` formats | `["%Y-%m-%d"]` |
| `normalization.trim_whitespace` | Boolean | `true` |
| `normalization.empty_strings_as_null` | Boolean | `true` |
| `normalization.casefold_columns` | List of column names | `[]` |
| `normalization.date_output_format` | Non-empty `strftime` format string | `"%Y-%m-%d"` |
| `deduplication.columns` | Non-empty list of column names | Deduplication disabled when section is omitted |
| `deduplication.keep` | `first` or `last` | `first` |
| `filters[].column` | Column name | Required per filter |
| `filters[].operator` | `equals` or `not_equals` | `equals` |
| `filters[].value` | Scalar: string, number, boolean, or null | `null` when omitted |
| `filters[].include` | Boolean | `true` |
| `sorting[].column` | Column name | Required per sort rule |
| `sorting[].ascending` | Boolean | `true` |
| `output.format` | `csv` or `xlsx` | `csv` |

A complete configuration is available at `examples/rules.yaml`.

A missing required value makes a row invalid. A missing required column stops processing with a configuration error. Date formats may only be declared for columns listed in `validation.date_columns`.

### Deduplication

Deduplication runs after normalization and validation. Composite keys require every configured key value to match. Missing key values participate in duplicate keys.

Validation-invalid rows still participate in duplicate detection. A dropped duplicate that is also invalid is classified as a duplicate rather than counted again among retained invalid rows. Review exports preserve original source values.

### Filtering and sorting

Filters and sorting operate on normalized retained rows after deduplication. Filters use AND semantics. `include: true` retains matches; `include: false` excludes matches.

Sort rules are applied in declared priority order, source order is stable for ties, and null values sort after non-null values in ascending order. Referencing a missing filter or sorting column stops processing.

### Export and reporting

`output.format` controls the cleaned artifact only. Review files are always written as `invalid_rows.csv` and `duplicate_rows.csv`; the processing report is always `report.json`.

Existing output directories are rejected rather than overwritten.

## Command reference

```text
csv-data-cleaner clean
  --input PATH
  --config PATH
  --output-dir PATH
  [--sheet NAME]
  [--dry-run]
```

- `--input`: CSV or XLSX source file.
- `--config`: YAML or JSON configuration file.
- `--output-dir`: New directory for generated artifacts.
- `--sheet`: XLSX worksheet name. The first worksheet is used when omitted.
- `--dry-run`: Execute processing and print counts without creating output files.

Example dry run:

```bash
uv run csv-data-cleaner clean \
  --input examples/customers.csv \
  --config examples/rules.yaml \
  --output-dir output \
  --dry-run
```

## Known limitations

- Input formats are limited to CSV and XLSX.
- Configuration formats are limited to YAML and JSON.
- XLSX processing targets worksheet cell data; spreadsheet presentation features are not part of the cleaning model.
- The tool runs locally and does not provide a server, database, web UI, or background service.
- Output directories must not already exist.
- CSV/XLSX formula neutralization is not currently performed. See Security before opening generated files in spreadsheet software.

## Security

Treat CSV and XLSX files from untrusted sources as untrusted data.

CSV and spreadsheet applications may interpret cell values beginning with formula-triggering characters as formulas. CSV Data Cleaner currently preserves such cell content rather than neutralizing it, so generated CSV/XLSX files should not be treated as safe merely because they were processed by this tool. Inspect untrusted output before opening it in spreadsheet software, and avoid enabling active content or external links.

The application does not execute spreadsheet formulas itself; its supported workflow reads tabular values through pandas/openpyxl and writes tabular output.

## Development

Install all development dependencies and run the same quality gate used by CI:

```bash
uv sync --locked --all-groups
make check
```

`make check` runs Ruff linting, Ruff formatting checks, strict Pyright type checking, and pytest with branch coverage.

The codebase uses a `src/` layout and separates domain, application, infrastructure, presentation, and composition-root responsibilities.

## Continuous integration

GitHub Actions runs `make check` on pushes to `main` and `stage-*` branches and on pull requests targeting `main`.

## License

Licensed under the MIT License. See `LICENSE`.
