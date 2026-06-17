# Security Policy

## Supported Versions

The supported security scope for `rt-covid19` is the current default branch, `master`. Older commits, tags, branches, forks, demos, and generated artifacts are not actively supported unless the repository explicitly marks them as maintained.

Project summary: This repo contains a notebook to track the progression of COVID19 is the effective repro number (Rt).

## Reporting a Vulnerability

Please report suspected vulnerabilities through GitHub's private vulnerability reporting or by opening a draft GitHub Security Advisory for `garethpaul/rt-covid19` when that option is available. If GitHub does not show a private reporting option for this repository, contact the repository owner through GitHub and avoid posting exploit details publicly until the issue can be assessed.

Do not open a public issue that includes exploit code, secrets, personal data, or detailed reproduction steps for an unpatched vulnerability.

## What to Include

Helpful reports include:

- the affected file, endpoint, permission, dependency, or workflow
- a concise impact statement explaining what an attacker could do
- reproduction steps using test data and accounts you control
- the branch, commit SHA, platform version, device, runtime, or dependency versions used
- logs, screenshots, or proof-of-concept snippets that demonstrate impact without exposing private data

## Project Security Posture

- This repository appears to be a data science notebook project. The active security scope is the code and documentation on the default branch.
- Review found network clients, sockets, web APIs, or service endpoints; changes in those areas should receive security-focused review before merge.
- Review found database, model, query, or persistence-related code; changes in those areas should receive security-focused review before merge.
- No primary dependency manifest was detected in the repository root. If dependencies are added later, include a manifest and prefer reproducible installation instructions.

## Service and API Notes

For web services, APIs, sockets, or scraping workflows, prioritize reports involving authentication bypass, authorization errors, injection, server-side request forgery, unsafe deserialization, credential leakage, data exposure, or denial-of-service conditions. Use test accounts and minimal proof-of-concept traffic only.

## Dependency and Supply Chain Security

Hosted verification uses immutable action commits, a fixed runner image,
exact direct dependency pins, binary-only installation, `pip check`, and
`pip-audit`.

Custom Rt model grids must remain finite, non-negative, and strictly increasing
so malformed numerical inputs fail before posterior calculations.
Model inputs must also keep one-dimensional, non-missing, unique, increasing
case indexes so duplicate or reordered observations cannot create ambiguous
rolling windows or posterior columns.
County ingestion must reject values that are not real numeric, non-boolean
county case totals before coercion can disguise invalid source data.
Case preprocessing must require real numeric, non-boolean cumulative cases and
must require finite cumulative cases and non-negative cumulative cases so
booleans, lossy complex coercions, non-finite values, and impossible negative
totals cannot become plausible model inputs.

Dependency updates should come from trusted package managers and should keep lockfiles in sync when lockfiles exist. Do not commit credentials, private keys, tokens, generated secrets, or machine-local configuration. If a vulnerability depends on a compromised package, typosquatting risk, insecure transitive dependency, or unsafe build step, include the package name, affected version, and the path through which it is used.

Remote county data is pinned to NYT commit
`62ef34cfcb60214be873a38d73619da9ea57d50b` and must be exactly 104,795,654
bytes with SHA-256
`dcb2715a71aaa2c9635f5b44594731bbba708c22fb202247790672e492a07ac0`
before parsing. This identity check complements the existing HTTPS host,
credential, redirect, timeout, and download-size restrictions.

## Safe Research Guidelines

Good-faith research is welcome when it stays within these boundaries:

- use only accounts, devices, data, and infrastructure that you own or have explicit permission to test
- avoid destructive actions, persistence, spam, phishing, social engineering, or denial-of-service testing
- minimize access to personal data and stop testing immediately if private data is exposed
- do not exfiltrate secrets or third-party data; report the minimum evidence needed to verify impact
- keep vulnerability details confidential until the maintainer has assessed the report

## Maintainer Response

The maintainer will review complete reports as availability allows, prioritize issues by exploitability and impact, and coordinate a fix or mitigation when the affected code is still maintained. For sample, archived, or educational repositories, the likely remediation may be documentation, dependency updates, or clearly marking unsupported code rather than a production-style patch release.
