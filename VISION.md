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
- Keep the maintained Python 3.12 runtime pinned and reproducible
- Keep installed dependency consistency and vulnerability checks in CI
- Keep reusable model calculations in the tested Python module
- Keep custom Rt grids non-negative and strictly increasing
- Keep finite, strictly increasing HDI grids behind interval summaries
- Select HDI candidates by numeric endpoint width on nonuniform grids
- Keep one-dimensional, non-missing, unique, increasing case indexes behind
  preprocessing and posterior calculations
- Keep Matplotlib configured for headless reproduction runs
- Keep notebook, provenance, and runtime configuration URL references on HTTPS
- Keep the runtime NYT CSV source named as `DATA_SOURCE_URL`
- Keep the runtime NYT snapshot pinned to commit
  `62ef34cfcb60214be873a38d73619da9ea57d50b`, 104,795,654 bytes, and SHA-256
  `dcb2715a71aaa2c9635f5b44594731bbba708c22fb202247790672e492a07ac0`
  before parsing remote data
- Keep completed maintenance plans under `docs/plans`
- Keep notebook presentation defaults explicit and non-authoritative
- Keep security and responsible-use metadata available

Next priorities:

- Add broader numerical regression fixtures for model changes
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
