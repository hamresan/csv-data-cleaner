# CSV Data Cleaner

A configurable command-line tool for cleaning, validating, deduplicating, and reporting on CSV and Excel data.

> **Status:** Under active development. This README defines the planned public interface for the first release. The project foundation and CLI entry point are implemented. Feature commands remain under active development until version `0.1.0` is complete.

## Why this project?

Business data often arrives as a spreadsheet that contains missing values, invalid emails or dates, inconsistent records, and duplicates. Cleaning it manually is repetitive and hard to reproduce.

CSV Data Cleaner turns that work into a repeatable command:

```text
input CSV/XLSX → validate → clean → deduplicate → filter/sort → export → report
```

It is designed for developers, analysts, and small teams that need a local, scriptable data-cleaning workflow without a database, web server, or UI.

## Planned features

- Read `.csv` and `.xlsx` input files
- Validate required fields, email addresses, dates, and configurable custom rules
- Remove duplicate records using one or more columns
- Separate invalid and duplicate rows for review
- Apply configurable filtering and sorting
- Export cleaned data as CSV or Excel
- Produce a JSON summary of total, valid, invalid, and duplicate records
- Return clear command-line errors for invalid files and configurations
- Keep rules in a YAML or JSON file instead of hard-coding them

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Installation

Clone the repository and install the development environment:

```bash
git clone https://github.com/hamresan/csv-data-cleaner.git
cd csv-data-cleaner
uv sync
```

## Quick start

Create a rules file:

```yaml
# rules.yaml
required_columns:
  - name
  - email
  - signup_date

validation:
  email_columns:
    - email
  date_columns:
    - signup_date
  date_formats:
    signup_date:
      - "%Y-%m-%d"
      - "%d/%m/%Y"

normalization:
  trim_whitespace: true
  empty_strings_as_null: true
  casefold_columns:
    - email
  date_output_format: "%Y-%m-%d"

deduplication:
  columns:
    - email
  keep: first

sorting:
  - column: name
    ascending: true

output:
  format: xlsx
```

Run the cleaner:

```bash
uv run csv-data-cleaner clean \
  --input examples/customers.xlsx \
  --config rules.yaml \
  --output-dir output
```

The command will create:

```text
output/
├── cleaned.xlsx       # valid, cleaned, deduplicated records
├── invalid_rows.csv   # rows that did not pass validation
├── duplicate_rows.csv # rows removed as duplicates
└── report.json        # processing summary
```

Example `report.json`:

```json
{
  "input_file": "customers.xlsx",
  "processed_records": 1200,
  "valid_records": 1087,
  "invalid_records": 73,
  "duplicate_records": 40,
  "output_file": "output/cleaned.xlsx"
}
```

## Configuration

Rules are intentionally configurable, so the same tool can support different datasets.

| Setting | Purpose |
| --- | --- |
| `required_columns` | Columns that must exist in the input file |
| `validation.email_columns` | Columns that must contain valid email addresses |
| `validation.date_columns` | Columns that must contain valid dates |
| `validation.date_formats` | Accepted input formats for configured date columns; defaults to `%Y-%m-%d` |
| `normalization.trim_whitespace` | Trim leading/trailing whitespace from strings; defaults to `true` |
| `normalization.empty_strings_as_null` | Convert empty normalized strings to null; defaults to `true` |
| `normalization.casefold_columns` | Columns whose string values are case-normalized with Unicode-aware case folding; defaults to an empty list |
| `normalization.date_output_format` | Canonical date representation; defaults to `%Y-%m-%d` |
| `deduplication.columns` | One or more columns used to identify duplicates |
| `deduplication.keep` | Which duplicate to keep: `first` or `last` |
| `sorting` | Ordered list of output sorting rules |
| `output.format` | Output format: `csv` or `xlsx` |

A missing required **value** makes a row invalid. A missing required **column** stops processing with a clear configuration error.

### Deduplication behavior

Deduplication runs after normalization and validation and compares the normalized values of all configured key columns. Composite keys require every configured key value to match. `keep: first` retains the first matching row in source order, while `keep: last` retains the last.

Missing key values participate in the duplicate key. This means two rows with the same normalized key, including `null` in the same key positions, are duplicates. For example, when `email` is the only duplicate key, two rows whose normalized `email` is `null` belong to the same duplicate group.

Validation status does not exclude a row from duplicate detection. If duplicate rows are also validation-invalid, dropped rows are classified as duplicates and kept separately for duplicate review rather than being counted again among retained invalid rows. Their original source values and validation issues remain available in the processing result.

## Command reference

```text
csv-data-cleaner clean
  --input PATH
  --config PATH
  --output-dir PATH
  [--sheet NAME]
  [--dry-run]
```

- `--input`: Source CSV or XLSX file.
- `--config`: YAML or JSON rule file.
- `--output-dir`: Directory for generated files.
- `--sheet`: Optional Excel worksheet name.
- `--dry-run`: Validate and show the summary without writing output files.

## Development

```bash
uv sync --all-groups
make check
```

The project will use Python 3.12, `pandas`, and `openpyxl` for tabular and Excel handling. Its implementation will keep parsing, validation, deduplication, export, and reporting as separate testable components.

## Roadmap

- [x] Project scaffolding and CLI entry point
- [ ] CSV and XLSX readers
- [ ] Configurable validation and deduplication rules
- [ ] CSV/XLSX exports and JSON report
- [ ] Example datasets and end-to-end tests
- [ ] Docker image and GitHub Actions checks

## Contributing

Issues and pull requests are welcome. Before opening a pull request, run the checks in the [Development](#development) section.

## License

This project will be released under the MIT License.
