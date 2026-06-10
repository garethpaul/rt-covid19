.PHONY: build check lint test verify

PYTHON ?= python3

lint:
	$(PYTHON) scripts/check_notebook_provenance.py
	$(PYTHON) -m ruff format --check .
	$(PYTHON) -m ruff check .

test:
	$(PYTHON) -m unittest discover -s tests -p "test*.py"

build:
	$(PYTHON) -m json.tool Rt-covid19.ipynb >/dev/null

verify: lint test build

check: verify
	$(PYTHON) -m pip_audit -r requirements.txt -r requirements-dev.txt
