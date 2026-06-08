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
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-rt-covid19-baseline.md"

IMPORT_TO_REQUIREMENT = {
    "IPython": "ipython",
    "matplotlib": "matplotlib",
    "numpy": "numpy",
    "pandas": "pandas",
    "scipy": "scipy",
}


def requirement_names():
    if not REQUIREMENTS.exists():
        return set()

    names = set()
    for raw_line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[<>=!~\[]", line, maxsplit=1)[0].strip().lower()
        if name:
            names.add(name)
    return names


def main():
    failures = []

    if not CANONICAL_PLAN.exists():
        failures.append("docs/plans/2026-06-08-rt-covid19-baseline.md is missing")

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

    requirements = requirement_names()
    if not requirements:
        failures.append("requirements.txt is missing or empty")

    if notebook:
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

        sources = "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook.get("cells", [])
            if cell.get("cell_type") == "code"
        )
        imported_modules = set(re.findall(r"^(?:import|from)\s+([A-Za-z_][\w]*)", sources, flags=re.MULTILINE))
        for module in sorted(imported_modules):
            expected = IMPORT_TO_REQUIREMENT.get(module)
            if expected and expected not in requirements:
                failures.append(f"requirements.txt must include {expected} for notebook import {module}")

        urls = sorted(set(re.findall(r"""https?://[^\s)\]"']+""", sources)))
        data_urls = [url for url in urls if "nytimes/covid-19-data" in url]
        if not data_urls:
            failures.append("Rt-covid19.ipynb must keep the NYT COVID-19 data URL visible")
        for url in data_urls:
            if url not in readme_text:
                failures.append(f"README.md must document notebook data source {url}")
            if url not in provenance_text:
                failures.append(f"DATA_PROVENANCE.md must document notebook data source {url}")

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
