"""Integration tests for the installed command-line entry point."""

import subprocess
import sys

from click.testing import CliRunner

from csv_data_cleaner.presentation.cli import cli


def test_cli_help_succeeds() -> None:
    result = CliRunner().invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Clean, validate, deduplicate" in result.output


def test_package_import_succeeds_in_fresh_python_process() -> None:
    result = subprocess.run(
        [sys.executable, "-c", "import csv_data_cleaner; print(csv_data_cleaner.__version__)"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "0.1.0"
    assert result.stderr == ""
