.PHONY: lint format-check type-check test check

lint:
	uv run ruff check src tests

format-check:
	uv run ruff format --check src tests

type-check:
	uv run pyright src tests

test:
	uv run pytest --cov=csv_data_cleaner --cov-branch --cov-report=term-missing

check: lint format-check type-check test
