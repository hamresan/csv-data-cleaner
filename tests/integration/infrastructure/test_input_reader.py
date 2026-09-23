"""Integration tests for real CSV/XLSX input files."""

from pathlib import Path

import pandas as pd
import pytest

from csv_data_cleaner.domain.errors import InputDataError
from csv_data_cleaner.infrastructure.input import PandasInputReader


def test_csv_and_xlsx_produce_same_canonical_rows(tmp_path: Path) -> None:
    frame = pd.DataFrame(
        [{"name": "Ada", "email": "ada@example.com"}, {"name": "Grace", "email": None}]
    )
    csv_path = tmp_path / "customers.csv"
    xlsx_path = tmp_path / "customers.xlsx"
    frame.to_csv(csv_path, index=False)
    frame.to_excel(xlsx_path, index=False)

    reader = PandasInputReader()

    assert reader.read(csv_path) == reader.read(xlsx_path)


def test_xlsx_reads_requested_sheet(tmp_path: Path) -> None:
    path = tmp_path / "customers.xlsx"
    with pd.ExcelWriter(path) as writer:
        pd.DataFrame([{"name": "Wrong"}]).to_excel(writer, sheet_name="First", index=False)
        pd.DataFrame([{"name": "Ada"}]).to_excel(writer, sheet_name="Customers", index=False)

    result = PandasInputReader().read(path, sheet="Customers")

    assert result.rows[0].values["name"] == "Ada"


@pytest.mark.parametrize("filename", ["missing.csv", "input.txt"])
def test_reader_rejects_unreadable_or_unsupported_input(tmp_path: Path, filename: str) -> None:
    path = tmp_path / filename
    if path.suffix == ".txt":
        path.write_text("name\nAda\n", encoding="utf-8")

    with pytest.raises(InputDataError):
        PandasInputReader().read(path)
