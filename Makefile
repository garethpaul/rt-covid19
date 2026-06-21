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
override REPOSITORY_MAKEFILE := $(value MAKEFILE_LIST)
override EXPECTED_MAKEFILE_LIST := $(value MAKEFILE_LIST)
override CURRENT_MAKEFILE_LIST = $(value MAKEFILE_LIST)
export REPOSITORY_MAKEFILE EXPECTED_MAKEFILE_LIST CURRENT_MAKEFILE_LIST
override ROOT :=

override define RUN_IN_REPO
if [ "$$CURRENT_MAKEFILE_LIST" != "$$EXPECTED_MAKEFILE_LIST" ]; then \
	printf '%s\n' 'multiple -f Makefiles are not supported' >&2; \
	exit 1; \
fi; \
makefile=$${REPOSITORY_MAKEFILE# }; \
if [ -z "$$makefile" ] || [ ! -f "$$makefile" ]; then \
	printf '%s\n' 'repository Makefile path could not be resolved' >&2; \
	exit 1; \
fi; \
case "$$makefile" in \
	*/*) repository_directory=$${makefile%/*} ;; \
	*) repository_directory=. ;; \
esac; \
ROOT=$$(CDPATH= cd -- "$$repository_directory" && pwd -P); \
export ROOT; \
cd "$$ROOT" &&
endef

lint:
	$(RUN_IN_REPO) $(PYTHON) scripts/check_notebook_provenance.py
	$(RUN_IN_REPO) $(PYTHON) -m ruff format --check .
	$(RUN_IN_REPO) $(PYTHON) -m ruff check .

test:
	$(RUN_IN_REPO) $(PYTHON) -m unittest discover -s tests -p "test*.py"

build:
	$(RUN_IN_REPO) $(PYTHON) -m json.tool Rt-covid19.ipynb >/dev/null

dependencies:
	$(RUN_IN_REPO) $(PYTHON) -m pip check
	$(RUN_IN_REPO) $(PYTHON) -m pip_audit -r requirements.txt -r requirements-dev.txt

root-test:
	$(RUN_IN_REPO) /bin/sh scripts/test-makefile-root.sh

verify: root-test lint test build

check: verify dependencies
