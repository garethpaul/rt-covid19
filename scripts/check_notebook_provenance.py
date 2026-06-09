#!/usr/bin/env python3
"""Validate notebook dependency and data-source documentation."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "Rt-covid19.ipynb"
README = ROOT / "README.md"
REQUIREMENTS = ROOT / "requirements.txt"
PROVENANCE = ROOT / "DATA_PROVENANCE.md"
MATPLOTLIBRC = ROOT / "matplotlibrc"
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-rt-covid19-baseline.md"
KERNEL_VERSION_PLAN = DOCS_PLANS / "2026-06-09-kernel-version-provenance.md"

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

    docs_with_urls = {
        "README.md": readme_text,
        "DATA_PROVENANCE.md": provenance_text,
    }
    for doc_name, doc_text in docs_with_urls.items():
        insecure_urls = sorted(set(re.findall(r"http://[^\s)\]\"']+", doc_text)))
        for url in insecure_urls:
            failures.append(f"{doc_name} must use HTTPS URLs, found {url}")

    matplotlibrc_text = MATPLOTLIBRC.read_text(encoding="utf-8") if MATPLOTLIBRC.exists() else ""
    if not matplotlibrc_text:
        failures.append("matplotlibrc is missing or empty")
    elif not re.search(r"^backend\s*:\s*Agg\s*$", matplotlibrc_text, flags=re.MULTILINE):
        failures.append("matplotlibrc must set backend : Agg for headless notebook reproduction")

    requirement_specs = requirement_lines()
    requirements = requirement_names()
    if not requirements:
        failures.append("requirements.txt is missing or empty")

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
                failures.append(f"DATA_PROVENANCE.md must document notebook kernel version {kernel_phrase}")

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

        sources = "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook.get("cells", [])
        )
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

        imported_modules = set(re.findall(r"^(?:import|from)\s+([A-Za-z_][\w]*)", code_sources, flags=re.MULTILINE))
        for module in sorted(imported_modules):
            expected = IMPORT_TO_REQUIREMENT.get(module)
            if expected and expected not in requirements:
                failures.append(f"requirements.txt must include {expected} for notebook import {module}")

        if "squeeze=True" in code_sources:
            pandas_upper_bound = any(
                re.match(r"^pandas\s*<\s*2(?:\b|$)", spec, flags=re.IGNORECASE)
                for spec in requirement_specs
            )
            if not pandas_upper_bound:
                failures.append("requirements.txt must keep pandas<2 for read_csv(..., squeeze=True) compatibility")
            if "pandas<2" not in readme_text:
                failures.append("README.md must document the pandas<2 compatibility constraint")
            if "pandas<2" not in provenance_text:
                failures.append("DATA_PROVENANCE.md must document the pandas<2 compatibility constraint")

        urls = sorted(set(re.findall(r"""https?://[^\s)\]"']+""", code_sources)))
        data_urls = [url for url in urls if "nytimes/covid-19-data" in url]
        if not data_urls:
            failures.append("Rt-covid19.ipynb must keep the NYT COVID-19 data URL visible")
        for url in data_urls:
            if url not in readme_text:
                failures.append(f"README.md must document notebook data source {url}")
            if url not in provenance_text:
                failures.append(f"DATA_PROVENANCE.md must document notebook data source {url}")

        if not re.search(
            r"^DATA_SOURCE_URL\s*=\s*['\"]https://raw\.githubusercontent\.com/nytimes/covid-19-data/master/us-counties\.csv['\"]",
            code_sources,
            flags=re.MULTILINE,
        ):
            failures.append("Rt-covid19.ipynb must define DATA_SOURCE_URL for the NYT county data source")
        if not re.search(r"pd\.read_csv\(\s*DATA_SOURCE_URL\b", code_sources):
            failures.append("Rt-covid19.ipynb must read county data from DATA_SOURCE_URL")

    if "not current public-health guidance" not in readme_text.lower():
        failures.append("README.md must state that the notebook is not current public-health guidance")
    if "not current public-health guidance" not in provenance_text.lower():
        failures.append("DATA_PROVENANCE.md must state that the notebook is not current public-health guidance")
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
