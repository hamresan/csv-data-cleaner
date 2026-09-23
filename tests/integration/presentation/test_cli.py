"""Integration tests for the command-line entry point."""

import subprocess
import sys

from click.testing import CliRunner
from pytest import MonkeyPatch

from csv_data_cleaner.presentation.cli import cli, main


def test_cli_help_succeeds() -> None:
    result = CliRunner().invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Clean, validate, deduplicate" in result.output


def test_main_runs_cli_help(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["csv-data-cleaner", "--help"])

    try:
        main()
    except SystemExit as error:
        assert error.code == 0


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
