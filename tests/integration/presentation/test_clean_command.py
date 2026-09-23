"""Integration tests for user-facing clean command errors."""

from pathlib import Path

from click.testing import CliRunner

from csv_data_cleaner.presentation.cli import cli


def test_clean_reports_missing_input_without_stack_trace(tmp_path: Path) -> None:
    config_path = tmp_path / "rules.yaml"
    config_path.write_text("{}\n", encoding="utf-8")

    result = CliRunner().invoke(
        cli,
        [
            "clean",
            "--input",
            str(tmp_path / "missing.csv"),
            "--config",
            str(config_path),
            "--output-dir",
            str(tmp_path / "output"),
        ],
    )

    assert result.exit_code == 1
    assert "Error: Input file does not exist:" in result.output
    assert "Traceback" not in result.output


def test_clean_reports_missing_config_without_stack_trace(tmp_path: Path) -> None:
    input_path = tmp_path / "input.csv"
    input_path.write_text("name\nAda\n", encoding="utf-8")

    result = CliRunner().invoke(
        cli,
        [
            "clean",
            "--input",
            str(input_path),
            "--config",
            str(tmp_path / "missing.yaml"),
            "--output-dir",
            str(tmp_path / "output"),
        ],
    )

    assert result.exit_code == 1
    assert "Error: Configuration file does not exist:" in result.output
    assert "Traceback" not in result.output
