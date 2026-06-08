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
- Keep security and responsible-use metadata available

Next priorities:

- Document data sources, download dates, and preprocessing steps
- Add an environment file for notebook dependencies
- Move reusable calculations into testable Python functions
- Add notes on uncertainty, limitations, and interpretation

Contribution rules:

- One PR = one focused data, notebook, model, visualization, or documentation change.
- Do not commit sensitive health data.
- Keep source dates visible for any dataset refresh.
- Preserve uncertainty intervals and caveats in outputs.

## Security And Responsible Use

Public-health analysis can be misread as operational advice. The notebook
should clearly label assumptions, stale data, and limitations, and should not
replace official public-health guidance.

## What We Will Not Merge (For Now)

- Current-risk claims without fresh sourced data
- Dataset refreshes without provenance
- Model changes without explanation and comparison
- Removal of uncertainty or limitation notes
