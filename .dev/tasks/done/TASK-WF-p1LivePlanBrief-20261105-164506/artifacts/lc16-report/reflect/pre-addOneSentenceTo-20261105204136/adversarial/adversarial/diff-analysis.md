# Diff Analysis: reviewer-card comparison (UC-1 pre-execution plan audit)

## Metadata

- Generated: 2026-11-05T20:46:00Z
- Variants compared: 3 (V1 sonnet/analyzer, V2 haiku/qa, V3 opus/refactorer)
- Calibrated confidence (blind): V1 0.82, V2 0.59, V3 0.78
- Total differences found: 11 (structural 1, content 3, contradictions 2, unique 4, shared assumptions 2 promoted)
- Focus: correctness, coverage, deviation-classification

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity | Level |
|---|------|----|----|----|----------|-------|
| S-001 | Card shape and severity labelling | 4 findings; two "none"-class findings still labelled `minor` | 2 findings, both "none"-class labelled `minor`, no actionable recommendation | 5 findings; three "none"-class labelled `minor` | Low | L1 |

## Content Differences

| # | Topic | V1 approach | V2 approach | V3 approach | Severity | Level |
|---|-------|-------------|-------------|-------------|----------|-------|
| C-001 | Accuracy of the sentence the spec asks for ("overwrites files that already exist in ~/.claude") | gap: scope it to what the installer copies; cites install_hooks.py:89-95 | not checked | gap: say "framework files"; cites upgrading.md:85-87 | Medium | L2 |
| C-002 | Acceptance criterion 2 (`git diff --stat` lists no file other than README.md) | gap: can mis-fire (staged `.dev/tasks`, one removed + one added line); wants a README-scoped command | calls it checkable and falsifiable | silent | Medium | L3 |
| C-003 | Evidence that `--force` really overwrites | read main.py:178-236 and install_core.py:69-75; upgrades the [INFERRED] tag | none | relies on docs (upgrading.md, installation.md), did not read the merge code | Medium | L2 |

## Contradictions

| # | Point of Conflict | Position A | Position B | Impact | Level |
|---|-------------------|-----------|-----------|--------|-------|
| X-001 | Is acceptance criterion 2 sound? | V1 F3: it can fail or pass wrongly (`git diff --stat` ignores staged and untracked files; whole-line change shows as -/+) | V2 F2: both criteria are checkable and falsifiable | Medium | L3 |
| X-002 | What `--force` leaves alone | V3 F1: "leaves user-created files in ~/.claude alone"; V1 F1: "files the installer does not manage are never touched" | docs/getting-started/installation.md:593 (Warning): `--force` deletes and re-copies each shipped skill folder, so files a user added inside one are lost | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V3 | Checks other install docs (installation.md:283, :591, upgrading.md:56-60) and tests that read README (tests/docs/test_retired_docs_absent.py:39) for fallout | High |
| U-002 | V1 | Traces the `force` flag from main.py through core and hooks installers; notes seed data file is never overwritten (install_hooks.py:89-95) and `--force` is not forwarded to codegraph (main.py:52) | High |
| U-003 | V2 | Audits the coverage matrix against the spec body (qa lens): no requirement-bearing span missing | Medium |
| U-004 | V1 | Suggests `git diff --word-diff -- README.md` as the check for "only the sentence changed" | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source agreement | Classification | Impact | Status |
|-------|-----------|------------------|----------------|--------|--------|
| A-001 | At execution time the `git diff` used to check criterion 2 is read on a tree where README.md is the only tracked change and nothing is staged | All three treat the diff-based criterion as usable (V1 F3 doubts it, V2 F2 relies on it, V3 F5 accepts it) | UNSTATED | Medium | Promoted [SHARED-ASSUMPTION], L3 (guard/boundary of the check) |
| A-002 | Adding one sentence cannot break any test or doc check, so no test run is needed in the plan | V3 F4 says no test pins README.md:64; V1 notes it did not open the tests; V2 silent | UNSTATED | Low | Promoted [SHARED-ASSUMPTION], L2 |

STATED assumptions (documented, not promoted): README.md:64 is the single-line target paragraph (V1 F4, V3 F2 both cite it).

## Summary

- Total structural differences: 1
- Total content differences: 3
- Total contradictions: 2
- Total unique contributions: 4
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: none High; Medium: C-001, C-002, C-003, X-001, X-002, A-001
- Taxonomy coverage: L1 = S-001; L2 = C-001, C-003, X-002, A-002; L3 = C-002, X-001, A-001
- total_diff_points for convergence = S(1) + C(3) + X(2) + A(2) = 8
