## Rt Covid19 Vision

Rt Covid19 is a notebook-based analysis of county-level COVID-19 effective
reproduction number estimates using the Bettencourt and Ribeiro Bayesian
approach.

The repository is useful as an explanatory notebook: it walks through Poisson
likelihoods, priors, serial-interval assumptions, and iterative estimation of
Rt from observed case counts.

The goal is to preserve the educational analysis while making data provenance,
statistical assumptions, and reproducibility explicit.

The current focus is:

Priority:

- Preserve the notebook narrative and formulas
- Keep assumptions about likelihoods, priors, and serial interval visible
- Avoid presenting historical estimates as current public-health guidance
- Keep committed notebooks free of stale execution outputs and counts
- Keep committed notebooks free of empty placeholder code cells
- Keep the notebook's recorded Python kernel version visible in provenance docs
- Keep legacy pandas compatibility constraints explicit while notebook source
  depends on them
- Keep Matplotlib configured for headless reproduction runs
- Keep completed maintenance plans under `docs/plans`
- Keep notebook presentation defaults explicit and non-authoritative
- Keep security and responsible-use metadata available

Next priorities:

- Document Python environment constraints beyond `requirements.txt`
- Move reusable calculations into testable Python functions
- Add notes on uncertainty, limitations, and interpretation

Contribution rules:

- One PR = one focused data, notebook, model, visualization, or documentation change.
- Do not commit sensitive health data.
- Keep source dates visible for any dataset refresh.
- Preserve uncertainty intervals and caveats in outputs.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Public-health analysis can be misread as operational advice. The notebook
should clearly label assumptions, stale data, and limitations, and should not
replace official public-health guidance.

## What We Will Not Merge (For Now)

- Current-risk claims without fresh sourced data
- Dataset refreshes without provenance
- Model changes without explanation and comparison
- Removal of uncertainty or limitation notes

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
