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
| `deduplication.columns` | One or more columns used to identify duplicates |
| `deduplication.keep` | Which duplicate to keep: `first` or `last` |
| `sorting` | Ordered list of output sorting rules |
| `output.format` | Output format: `csv` or `xlsx` |

A missing required **value** makes a row invalid. A missing required **column** stops processing with a clear configuration error.

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