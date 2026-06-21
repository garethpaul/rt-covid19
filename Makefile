.DEFAULT_GOAL := check

.PHONY: build check dependencies lint root-test test verify

override SHELL := /bin/sh
override .SHELLFLAGS := -c
override PYTHON := python3
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; path=$$(printf '%s' "$$path" | /bin/sed 's/^ //'); [ -f "$$path" ] || exit 1; directory=$$(/usr/bin/dirname -- "$$path"); CDPATH= cd -- "$$directory" && /bin/pwd -P)
export ROOT
ifeq ($(strip $(ROOT)),)
$(error repository Makefile path could not be resolved)
endif

lint:
	$(PYTHON) "$$ROOT/scripts/check_notebook_provenance.py"
	cd "$$ROOT" && $(PYTHON) -m ruff format --check .
	cd "$$ROOT" && $(PYTHON) -m ruff check .

test:
	cd "$$ROOT" && $(PYTHON) -m unittest discover -s tests -p "test*.py"

build:
	$(PYTHON) -m json.tool "$$ROOT/Rt-covid19.ipynb" >/dev/null

dependencies:
	$(PYTHON) -m pip check
	$(PYTHON) -m pip_audit -r "$$ROOT/requirements.txt" -r "$$ROOT/requirements-dev.txt"

root-test:
	"$$ROOT/scripts/test-makefile-root.sh"

verify: root-test lint test build

check: verify dependencies
