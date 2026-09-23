"""Integration tests for the complete user-facing clean command."""

import json
from pathlib import Path

import pandas as pd
import pytest
from click.testing import CliRunner

from csv_data_cleaner.presentation.cli import cli


def write_config(path: Path, output_format: str) -> None:
    path.write_text(
        f"""required_columns:
  - name
  - email
validation:
  email_columns:
    - email
normalization:
  trim_whitespace: true
  casefold_columns:
    - email
output:
  format: {output_format}
""",
        encoding="utf-8",
    )


def invoke_clean(
    input_path: Path,
    config_path: Path,
    output_dir: Path,
    *extra_args: str,
):
    return CliRunner().invoke(
        cli,
        [
            "clean",
            "--input",
            str(input_path),
            "--config",
            str(config_path),
            "--output-dir",
            str(output_dir),
            *extra_args,
        ],
    )


@pytest.mark.parametrize("output_format", ["csv", "xlsx"])
def test_clean_writes_readable_outputs_and_report(
    tmp_path: Path,
    output_format: str,
) -> None:
    input_path = tmp_path / "input.csv"
    input_path.write_text(
        "name,email\n Ada ,ADA@EXAMPLE.COM\nBob,bob@example.com\n",
        encoding="utf-8",
    )
    config_path = tmp_path / "rules.yaml"
    write_config(config_path, output_format)
    output_dir = tmp_path / "output"

    result = invoke_clean(input_path, config_path, output_dir)

    assert result.exit_code == 0
    cleaned_path = output_dir / f"cleaned.{output_format}"
    if output_format == "csv":
        cleaned = pd.read_csv(cleaned_path)
    else:
        cleaned = pd.read_excel(  # pyright: ignore[reportUnknownMemberType]
            cleaned_path,
            engine="openpyxl",
        )
    assert cleaned.to_dict(orient="records") == [
        {"name": "Ada", "email": "ada@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
    ]
    report = json.loads((output_dir / "report.json").read_text(encoding="utf-8"))
    assert report["processed_records"] == 2
    assert report["valid_records"] == 2
    assert report["invalid_records"] == 0
    assert report["duplicate_records"] == 0
    assert report["exported_records"] == 2
    assert "Processed records: 2" in result.output
    assert f"Output file: {cleaned_path}" in result.output
    assert f"Report file: {output_dir / 'report.json'}" in result.output


def test_clean_dry_run_processes_without_writing_files(tmp_path: Path) -> None:
    input_path = tmp_path / "input.csv"
    input_path.write_text("name,email\nAda,ada@example.com\n", encoding="utf-8")
    config_path = tmp_path / "rules.yaml"
    write_config(config_path, "csv")
    output_dir = tmp_path / "output"

    result = invoke_clean(input_path, config_path, output_dir, "--dry-run")

    assert result.exit_code == 0
    assert not output_dir.exists()
    assert "Processed records: 1" in result.output
    assert "Exported records: 0" in result.output
    assert "Dry run: no output files were written." in result.output


def test_clean_reports_existing_output_directory_without_stack_trace(tmp_path: Path) -> None:
    input_path = tmp_path / "input.csv"
    input_path.write_text("name,email\nAda,ada@example.com\n", encoding="utf-8")
    config_path = tmp_path / "rules.yaml"
    write_config(config_path, "csv")
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    result = invoke_clean(input_path, config_path, output_dir)

    assert result.exit_code == 1
    assert "Error: Output directory already exists:" in result.output
    assert "Traceback" not in result.output


def test_clean_reports_missing_input_without_stack_trace(tmp_path: Path) -> None:
    config_path = tmp_path / "rules.yaml"
    config_path.write_text("{}\n", encoding="utf-8")

    result = invoke_clean(tmp_path / "missing.csv", config_path, tmp_path / "output")

    assert result.exit_code == 1
    assert "Error: Input file does not exist:" in result.output
    assert "Traceback" not in result.output


def test_clean_reports_missing_config_without_stack_trace(tmp_path: Path) -> None:
    input_path = tmp_path / "input.csv"
    input_path.write_text("name\nAda\n", encoding="utf-8")

    result = invoke_clean(input_path, tmp_path / "missing.yaml", tmp_path / "output")

    assert result.exit_code == 1
    assert "Error: Configuration file does not exist:" in result.output
    assert "Traceback" not in result.output
