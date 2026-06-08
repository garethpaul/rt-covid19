.PHONY: build check lint test verify

lint:
	python3 scripts/check_notebook_provenance.py

test: lint

build:
	python3 -m json.tool Rt-covid19.ipynb >/dev/null

verify: lint test build

check: verify
