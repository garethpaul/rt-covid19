ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

PYTHON ?= python3

.PHONY: build check dependencies lint test verify

lint:
	$(PYTHON) "$(ROOT)/scripts/check_notebook_provenance.py"
	cd "$(ROOT)" && $(PYTHON) -m ruff format --check .
	cd "$(ROOT)" && $(PYTHON) -m ruff check .

test:
	cd "$(ROOT)" && $(PYTHON) -m unittest discover -s tests -p "test*.py"

build:
	$(PYTHON) -m json.tool "$(ROOT)/Rt-covid19.ipynb" >/dev/null

dependencies:
	$(PYTHON) -m pip check
	$(PYTHON) -m pip_audit -r "$(ROOT)/requirements.txt" -r "$(ROOT)/requirements-dev.txt"

verify: lint test build

check: verify dependencies
