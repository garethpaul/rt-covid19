#!/usr/bin/env python3
"""Validate notebook dependency and data-source documentation."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "Rt-covid19.ipynb"
README = ROOT / "README.md"
REQUIREMENTS = ROOT / "requirements.txt"
DEV_REQUIREMENTS = ROOT / "requirements-dev.txt"
PROVENANCE = ROOT / "DATA_PROVENANCE.md"
MATPLOTLIBRC = ROOT / "matplotlibrc"
MODEL = ROOT / "rt_covid19.py"
MODEL_TESTS = ROOT / "tests" / "test_rt_covid19.py"
WORKFLOW = ROOT / ".github" / "workflows" / "check.yml"
MAKEFILE = ROOT / "Makefile"
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-rt-covid19-baseline.md"
KERNEL_VERSION_PLAN = DOCS_PLANS / "2026-06-09-kernel-version-provenance.md"
MATPLOTLIBRC_HTTPS_PLAN = DOCS_PLANS / "2026-06-09-matplotlibrc-https-urls.md"
MODERN_RUNTIME_PLAN = DOCS_PLANS / "2026-06-10-modern-runtime-and-ci.md"
HOSTED_VALIDATION_PLAN = DOCS_PLANS / "2026-06-10-hosted-validation-hardening.md"
HDI_GRID_PLAN = DOCS_PLANS / "2026-06-12-hdi-grid-validation.md"
DATASET_INTEGRITY_PLAN = DOCS_PLANS / "2026-06-12-dataset-snapshot-integrity.md"

DATA_SOURCE_COMMIT = "62ef34cfcb60214be873a38d73619da9ea57d50b"
DATA_SOURCE_URL = (
    f"https://raw.githubusercontent.com/nytimes/covid-19-data/{DATA_SOURCE_COMMIT}/us-counties.csv"
)
DATA_SOURCE_BYTES = "104,795,654"
DATA_SOURCE_SHA256 = "dcb2715a71aaa2c9635f5b44594731bbba708c22fb202247790672e492a07ac0"

EXPECTED_WORKFLOW = """name: Check

on:
  pull_request:
  push:
    branches:
      - master
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  verify:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
        with:
          persist-credentials: false
      - name: Set up Python
        uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6.2.0
        with:
          python-version: "3.12"
          cache: pip
      - name: Install dependencies
        run: "python -m pip install --only-binary=:all: -r requirements.txt -r requirements-dev.txt"
      - name: Run full verification
        run: make check
"""

IMPORT_TO_REQUIREMENT = {
    "IPython": "ipython",
    "matplotlib": "matplotlib",
    "numpy": "numpy",
    "pandas": "pandas",
    "scipy": "scipy",
}

REQUIRED_NOTEBOOK_ASSIGNMENTS = [
    "FILTERED_REGIONS",
    "no_lockdown",
    "partial_lockdown",
    "FULL_COLOR",
    "NONE_COLOR",
    "PARTIAL_COLOR",
    "ERROR_BAR_COLOR",
]


def requirement_lines():
    if not REQUIREMENTS.exists():
        return []

    lines = []
    for raw_line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def requirement_names():
    names = set()
    for line in requirement_lines():
        name = re.split(r"[<>=!~\[]", line, maxsplit=1)[0].strip().lower()
        if name:
            names.add(name)
    return names


def main():
    failures = []

    if not CANONICAL_PLAN.exists():
        failures.append("docs/plans/2026-06-08-rt-covid19-baseline.md is missing")
    if not KERNEL_VERSION_PLAN.exists():
        failures.append("docs/plans/2026-06-09-kernel-version-provenance.md is missing")
    if not MATPLOTLIBRC_HTTPS_PLAN.exists():
        failures.append("docs/plans/2026-06-09-matplotlibrc-https-urls.md is missing")
    if not MODERN_RUNTIME_PLAN.exists():
        failures.append("docs/plans/2026-06-10-modern-runtime-and-ci.md is missing")
    if not HOSTED_VALIDATION_PLAN.exists():
        failures.append("docs/plans/2026-06-10-hosted-validation-hardening.md is missing")
    if not HDI_GRID_PLAN.exists():
        failures.append("docs/plans/2026-06-12-hdi-grid-validation.md is missing")
    if not DATASET_INTEGRITY_PLAN.exists():
        failures.append("docs/plans/2026-06-12-dataset-snapshot-integrity.md is missing")

    docs_plans = sorted(DOCS_PLANS.glob("*.md")) if DOCS_PLANS.exists() else []
    if not docs_plans:
        failures.append("docs/plans must contain at least one completed plan")
    for plan_path in docs_plans:
        plan = plan_path.read_text(encoding="utf-8")
        if "Status: Completed" not in plan or "make check" not in plan:
            failures.append(
                f"{plan_path.relative_to(ROOT)} must record completed status and make check verification"
            )

    if not NOTEBOOK.exists():
        failures.append("Rt-covid19.ipynb is missing")
        notebook = None
    else:
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        if notebook.get("nbformat") != 4:
            failures.append("Rt-covid19.ipynb must use nbformat 4")

    readme_text = README.read_text(encoding="utf-8") if README.exists() else ""
    if not readme_text:
        failures.append("README.md is missing or empty")

    provenance_text = PROVENANCE.read_text(encoding="utf-8") if PROVENANCE.exists() else ""
    if not provenance_text:
        failures.append("DATA_PROVENANCE.md is missing or empty")

    matplotlibrc_text = MATPLOTLIBRC.read_text(encoding="utf-8") if MATPLOTLIBRC.exists() else ""
    if not matplotlibrc_text:
        failures.append("matplotlibrc is missing or empty")

    docs_with_urls = {
        "README.md": readme_text,
        "DATA_PROVENANCE.md": provenance_text,
        "matplotlibrc": matplotlibrc_text,
    }
    for doc_name, doc_text in docs_with_urls.items():
        insecure_urls = sorted(set(re.findall(r"http://[^\s)\]\"']+", doc_text)))
        for url in insecure_urls:
            failures.append(f"{doc_name} must use HTTPS URLs, found {url}")

    if matplotlibrc_text and not re.search(
        r"^backend\s*:\s*Agg\s*$", matplotlibrc_text, flags=re.MULTILINE
    ):
        failures.append("matplotlibrc must set backend : Agg for headless notebook reproduction")

    requirement_specs = requirement_lines()
    requirements = requirement_names()
    if not requirements:
        failures.append("requirements.txt is missing or empty")

    expected_requirements = {
        "ipython==9.14.0",
        "matplotlib==3.10.9",
        "numpy==2.4.6",
        "pandas==3.0.3",
        "scipy==1.17.1",
    }
    if set(requirement_specs) != expected_requirements:
        failures.append("requirements.txt must keep the verified Python 3.12 runtime pins")

    dev_requirements = (
        {
            line.strip()
            for line in DEV_REQUIREMENTS.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        if DEV_REQUIREMENTS.exists()
        else set()
    )
    if dev_requirements != {"pip-audit==2.10.0", "ruff==0.15.16"}:
        failures.append("requirements-dev.txt must keep the verified quality-tool pins")

    model_text = MODEL.read_text(encoding="utf-8") if MODEL.exists() else ""
    if not model_text:
        failures.append("rt_covid19.py is missing or empty")
    else:
        for contract in (
            "DATA_SOURCE_URL =",
            f'DATA_SOURCE_COMMIT = "{DATA_SOURCE_COMMIT}"',
            "DATA_SOURCE_BYTES = 104_795_654",
            f'DATA_SOURCE_SHA256 = "{DATA_SOURCE_SHA256}"',
            "digest = hashlib.sha256()",
            "digest.update(chunk)",
            "declared_size != DATA_SOURCE_BYTES",
            "downloaded_bytes != DATA_SOURCE_BYTES",
            "digest.hexdigest() != DATA_SOURCE_SHA256",
            "County data SHA-256 does not match the reviewed snapshot.",
            "def load_counties(",
            "def _validate_case_index(series, label):",
            "index.nlevels != 1",
            "index.hasnans",
            "not index.is_unique",
            "not index.is_monotonic_increasing",
            'f"{label} index must be one-dimensional, non-missing, unique, and increasing."',
            "DEFAULT_DOWNLOAD_TIMEOUT =",
            "DEFAULT_MAX_DOWNLOAD_BYTES =",
            "urllib.request.urlopen(request, timeout=timeout)",
            "response.geturl() != url",
            "def prepare_cases(",
            "def get_posteriors(",
            "def highest_density_interval(",
            "pmf.index.nlevels != 1",
            "pd.api.types.is_numeric_dtype(pmf.index.dtype)",
            "pd.api.types.is_bool_dtype(",
            "(np.diff(grid) <= 0).any()",
            "grid[candidate[1]] - grid[candidate[0]]",
            "grid[best[1]] - grid[best[0]]",
            "grid[candidate[1]] - grid[candidate[0]] < grid[best[1]] - grid[best[0]]",
            'raise ValueError("HDI grid must be numeric, finite, and strictly increasing.")',
            "if r_t_range.ndim != 1 or r_t_range.size == 0 or not np.isfinite(r_t_range).all():",
            "if (r_t_range < 0).any() or (np.diff(r_t_range) <= 0).any():",
            'raise ValueError("Rt range must be non-negative and strictly increasing.")',
            ').squeeze("columns")',
        ):
            if contract not in model_text:
                failures.append(f"rt_covid19.py must keep model contract: {contract}")
        model_imports = set(
            re.findall(r"^(?:import|from)\s+([A-Za-z_][\w]*)", model_text, flags=re.MULTILINE)
        )
        for module in sorted(model_imports):
            expected = IMPORT_TO_REQUIREMENT.get(module)
            if expected and expected not in requirements:
                failures.append(
                    f"requirements.txt must include {expected} for model import {module}"
                )

    model_tests_text = MODEL_TESTS.read_text(encoding="utf-8") if MODEL_TESTS.exists() else ""
    for contract in (
        "def test_get_posteriors_rejects_invalid_rt_range(self):",
        "def test_prepare_cases_rejects_ambiguous_indexes(self):",
        "def test_get_posteriors_rejects_ambiguous_indexes(self):",
        "def invalid_case_indexes():",
        "pd.Index([0, 0, 1])",
        "pd.Index([2, 1, 0])",
        'pd.DatetimeIndex(["2020-01-01", None, "2020-01-03"])',
        "np.array([])",
        "np.array([[0.0, 1.0]])",
        "np.array([0.0, np.nan])",
        "np.array([0.0, np.inf])",
        "np.array([-0.1, 0.0, 0.1])",
        "np.array([0.0, 0.5, 0.5, 1.0])",
        "with self.assertRaisesRegex(ValueError, message):",
        "def test_highest_density_interval_rejects_invalid_grid(self):",
        "def test_highest_density_interval_uses_numeric_grid_width(self):",
        "def test_highest_density_interval_preserves_earliest_equal_width(self):",
        "[0, 100, 101, 102]",
        "self.assertEqual([100, 101], interval.tolist())",
        "self.assertEqual([0, 1], interval.tolist())",
        '["0", "1", "2"]',
        "[False, True, True]",
        "pd.MultiIndex.from_tuples([(0, 0), (1, 1), (2, 2)])",
        'ValueError, "HDI grid must be numeric, finite, and strictly increasing"',
        "isinstance(value, (int, np.integer))",
        "def test_load_counties_verifies_remote_snapshot_before_parsing(self):",
        "def test_load_counties_rejects_remote_snapshot_size_mismatch_before_parsing(self):",
        "def test_load_counties_rejects_remote_snapshot_digest_mismatch_before_parsing(self):",
        "read_counties.assert_not_called()",
    ):
        if contract not in model_tests_text:
            failures.append(f"tests/test_rt_covid19.py must keep model test contract: {contract}")

    hdi_docs = {
        "README.md": readme_text,
        "VISION.md": (ROOT / "VISION.md").read_text(encoding="utf-8"),
        "CHANGES.md": (ROOT / "CHANGES.md").read_text(encoding="utf-8"),
        "DATA_PROVENANCE.md": provenance_text,
    }
    for doc_name, doc_text in hdi_docs.items():
        if "finite, strictly increasing HDI grids" not in " ".join(doc_text.split()):
            failures.append(f"{doc_name} must document finite, strictly increasing HDI grids")

    numeric_width_docs = {
        "README.md": readme_text,
        "VISION.md": hdi_docs["VISION.md"],
        "CHANGES.md": hdi_docs["CHANGES.md"],
    }
    for doc_name, doc_text in numeric_width_docs.items():
        if "numeric endpoint width" not in " ".join(doc_text.split()):
            failures.append(f"{doc_name} must document numeric endpoint width for HDIs")

    case_index_docs = dict(hdi_docs)
    case_index_docs["SECURITY.md"] = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    for doc_name, doc_text in case_index_docs.items():
        normalized = " ".join(doc_text.split())
        if "one-dimensional, non-missing, unique, increasing case indexes" not in normalized:
            failures.append(f"{doc_name} must document ordered case indexes")

    snapshot_docs = dict(hdi_docs)
    snapshot_docs["SECURITY.md"] = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    for doc_name, doc_text in snapshot_docs.items():
        normalized = " ".join(doc_text.split())
        for identity in (DATA_SOURCE_COMMIT, DATA_SOURCE_BYTES, DATA_SOURCE_SHA256):
            if identity not in normalized:
                failures.append(f"{doc_name} must document dataset identity {identity}")

    if DATA_SOURCE_URL not in model_text:
        failures.append("rt_covid19.py must pin the exact reviewed NYT dataset URL")
    if "/master/us-counties.csv" in model_text:
        failures.append("rt_covid19.py must not restore the mutable NYT master dataset URL")
    if model_text:
        digest_check = model_text.find("digest.hexdigest() != DATA_SOURCE_SHA256")
        parse_call = model_text.find("return _read_counties(handle)")
        if digest_check < 0 or parse_call < 0 or digest_check > parse_call:
            failures.append("rt_covid19.py must verify the dataset digest before CSV parsing")

    workflow_text = WORKFLOW.read_text(encoding="utf-8") if WORKFLOW.exists() else ""
    for contract in (
        "permissions:",
        "contents: read",
        "runs-on: ubuntu-24.04",
        "timeout-minutes: 10",
        "concurrency:",
        "cancel-in-progress: true",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        "persist-credentials: false",
        'python-version: "3.12"',
        "python -m pip install --only-binary=:all:",
        "run: make check",
    ):
        if contract not in workflow_text:
            failures.append(f"GitHub Actions workflow must keep contract: {contract}")

    for action, revision in re.findall(
        r"^\s*uses:\s*([^@\s]+)@([^\s#]+)", workflow_text, re.MULTILINE
    ):
        if not re.fullmatch(r"[a-f0-9]{40}", revision):
            failures.append(f"GitHub Actions action {action} must be pinned to a full commit SHA")

    workflow_files = sorted(
        path
        for path in WORKFLOW.parent.glob("*")
        if path.is_file() and path.suffix in {".yml", ".yaml"}
    )
    if workflow_files != [WORKFLOW]:
        failures.append(".github/workflows/check.yml must remain the only approved workflow")
    if workflow_text != EXPECTED_WORKFLOW:
        failures.append(".github/workflows/check.yml must match the approved verification policy")

    makefile_text = MAKEFILE.read_text(encoding="utf-8") if MAKEFILE.exists() else ""
    for contract in (
        "ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))",
        "dependencies:",
        "$(PYTHON) -m pip check",
        '$(PYTHON) -m pip_audit -r "$(ROOT)/requirements.txt"',
        "check: verify dependencies",
    ):
        if contract not in makefile_text:
            failures.append(f"Makefile must keep contract: {contract}")

    if notebook:
        language_info = notebook.get("metadata", {}).get("language_info", {})
        kernel_version = language_info.get("version", "")
        documented_kernel_version = kernel_version.split("-", 1)[0]
        if not documented_kernel_version:
            failures.append("Rt-covid19.ipynb must record language_info.version")
        else:
            kernel_phrase = f"Python {documented_kernel_version}"
            if kernel_phrase not in readme_text:
                failures.append(f"README.md must document notebook kernel version {kernel_phrase}")
            if kernel_phrase not in provenance_text:
                failures.append(
                    f"DATA_PROVENANCE.md must document notebook kernel version {kernel_phrase}"
                )

        for index, cell in enumerate(notebook.get("cells", []), start=1):
            if cell.get("cell_type") != "code":
                continue
            if cell.get("execution_count") is not None:
                failures.append(
                    f"Rt-covid19.ipynb code cell {index} must not store an execution_count"
                )
            if cell.get("outputs"):
                failures.append(
                    f"Rt-covid19.ipynb code cell {index} must not store execution outputs"
                )
            if not "".join(cell.get("source", [])).strip():
                failures.append(f"Rt-covid19.ipynb code cell {index} must not be empty")

        sources = "\n".join("".join(cell.get("source", [])) for cell in notebook.get("cells", []))
        insecure_notebook_urls = sorted(set(re.findall(r"http://[^\s)\]\"']+", sources)))
        for url in insecure_notebook_urls:
            failures.append(f"Rt-covid19.ipynb must use HTTPS URLs, found {url}")

        code_sources = "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook.get("cells", [])
            if cell.get("cell_type") == "code"
        )
        for name in REQUIRED_NOTEBOOK_ASSIGNMENTS:
            if not re.search(rf"^{re.escape(name)}\s*=", code_sources, flags=re.MULTILINE):
                failures.append(f"Rt-covid19.ipynb must define {name} before plotting summaries")

        imported_modules = set(
            re.findall(r"^(?:import|from)\s+([A-Za-z_][\w]*)", code_sources, flags=re.MULTILINE)
        )
        for module in sorted(imported_modules):
            expected = IMPORT_TO_REQUIREMENT.get(module)
            if expected and expected not in requirements:
                failures.append(
                    f"requirements.txt must include {expected} for notebook import {module}"
                )

        if "squeeze=True" in code_sources or "squeeze=True" in model_text:
            failures.append("Runtime code must not use removed read_csv(squeeze=True) behavior")

        urls = sorted(set(re.findall(r"""https?://[^\s)\]"']+""", code_sources + model_text)))
        data_urls = [url for url in urls if "nytimes/covid-19-data" in url]
        if not data_urls:
            failures.append("Runtime code must keep the NYT COVID-19 data URL visible")
        for url in data_urls:
            if url not in readme_text:
                failures.append(f"README.md must document notebook data source {url}")
            if url not in provenance_text:
                failures.append(f"DATA_PROVENANCE.md must document notebook data source {url}")

        if "from rt_covid19 import (" not in code_sources:
            failures.append("Rt-covid19.ipynb must import the tested model helpers")
        if "counties = load_counties()" not in code_sources:
            failures.append("Rt-covid19.ipynb must load county data through load_counties")

    if "not current public-health guidance" not in readme_text.lower():
        failures.append(
            "README.md must state that the notebook is not current public-health guidance"
        )
    if "not current public-health guidance" not in provenance_text.lower():
        failures.append(
            "DATA_PROVENANCE.md must state that the notebook is not current public-health guidance"
        )
    if "no data refresh was performed on 2026-06-08" not in provenance_text.lower():
        failures.append("DATA_PROVENANCE.md must document the 2026-06-08 refresh status")
    if "gaussian smoothing" not in provenance_text.lower():
        failures.append("DATA_PROVENANCE.md must document notebook preprocessing assumptions")

    if failures:
        print("Notebook provenance checks failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("Notebook provenance checks passed")


if __name__ == "__main__":
    main()
