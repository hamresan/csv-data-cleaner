"""Contract-shape tests for the input reader port."""

from pathlib import Path

from csv_data_cleaner.application.ports import InputReader
from csv_data_cleaner.domain import InputData


class StubInputReader(InputReader):
    """Minimal implementation proving the port can be implemented explicitly."""

    def read(self, path: Path, *, sheet: str | None = None) -> InputData:
        del path, sheet
        return InputData(columns=(), rows=())


def test_input_reader_contract_supports_explicit_implementation() -> None:
    reader: InputReader = StubInputReader()

    assert reader.read(Path("input.csv")) == InputData(columns=(), rows=())
