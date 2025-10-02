PYTHON ?= python3
VENV := .venv
ACTIVATE := . $(VENV)/bin/activate

.PHONY: bootstrap lint format mypy test run

bootstrap:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install -r requirements.txt

lint:
	$(ACTIVATE) && ruff check src

format:
	$(ACTIVATE) && ruff format src

mypy:
	$(ACTIVATE) && mypy src

test:
	$(ACTIVATE) && pytest

run:
	$(ACTIVATE) && $(PYTHON) -m src.app
