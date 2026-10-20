# Diff Analysis: Tier-2 Reviewer Card Comparison

## Metadata
- Generated: 2026-10-20T06:00:00Z
- Mode: A (--compare), depth: quick, focus: correctness, coverage, deviation-classification
- Variants compared: 2
  - Variant 1 = reviewer-1-card.yaml (sonnet:analyzer, verdict `approve`, self_confidence 0.90, calibrated 0.72)
  - Variant 2 = reviewer-2-card.yaml (haiku:qa, verdict `approve-with-changes`, self_confidence 0.86, calibrated 0.67)
- Ground truth: spec `source.md` (sha256 f108e00f…, matches ledger `source_sha256`) and tasklist `TASK-WF-designSpec-20261020-053703.md`
- Total differences found: 11
- Categories: structural (1), content (4), contradictions (2), unique (2), shared assumptions (2)

## Pre-debate integrity finding (orchestrator, factual)

Both cards declare `target_tasklist_sha256: 9d4d00ed…` (equal to the `PLAN: sha256` in `progress.md`).
The tasklist on disk now hashes to `954add6ccec3866f1ed5e2e20bf453f89bf86836d0474e9b15073e1223a4f4de`.
File times: reviewer-1 card 05:48:45, reviewer-2 card 05:54:38, tasklist last modified 05:54:54 (16 s after card 2).
No copy of the 9d4d00ed revision exists (the task folder is untracked in git). Therefore every finding is
adjudicated against the CURRENT tasklist (954add6c), which is the revision any remediation would act on.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Card sections | `findings` (1) + `prior_findings_resolved` (9) + `baseline_checks`; `coverage_gaps: []` | `findings` (3) + `coverage_gaps` (3); no prior-findings or baseline section | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Task 2 STOP-message placement wording (finding A1) | Low: claims T:50 ("only in Wave 0") contradicts T:56 (Error Handling rows); recommends "only in the Wave 0 step and the two Error Handling rows" | Not raised | Low |
| C-002 | Depth-conditioned WARN + audit-log record (finding QA-1, spec 4.3, RF11) | Not raised; lists `WARN-in-Wave0-conditioned-on-flag-supplied` as resolved (T:51, T:60, T:79) | Medium: unconditional WARN would pass all ACs/tests; wants AC + Wave0-scoped test naming quick/standard (not deep) and the audit log | Medium |
| C-003 | Wave 2 step 5 stays deep-only (finding QA-2, spec section 3) | Not raised | Medium: no AC/test keeps step 5 deep-only; wants assertion that step 5 begins "For `--depth deep` **only**" with `model: <revagent>` | Medium |
| C-004 | RF12 unsupported examples asserted (finding QA-3) | Not raised | Low: only `connect` asserted; wants `Opus`, `claude-sonnet-4-6`, `inherit` asserted in the same bullet | Low |

Current-tasklist evidence per topic:
- C-001: T:50 now reads "the full STOP messages appear only in the Wave 0 step and the two Error Handling rows" — identical to A1's recommended text.
- C-002: T:60 AC requires one Wave 0 sub-bullet "whose condition names both '`--revagent` was supplied' and '`--depth` is `quick` or `standard`', and which says the effect line is recorded in the audit log"; T:80 test requires the bullet "contains both `quick` and `standard`, does not contain `deep`, mentions the audit log, and is conditioned on `--revagent` being supplied".
- C-003: T:61 AC "Wave 2 step 5 still begins `For `--depth deep` **only**` and the `model: <revagent>` rule is inside that step"; T:81 "Deep-only guard" test.
- C-004: T:59 AC and T:77 test both require `connect`, `Opus`, `claude-sonnet-4-6`, `inherit` in the same Wave 0 bullet.

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Overall verdict | `verdict: approve` (only a Low wording finding) | `verdict: approve-with-changes` (two Medium test-contract gaps) | High |
| X-002 | Coverage completeness | `coverage_gaps: []` | 3 gaps: WARN depth-conditioning/audit log (spec 4.3, RF11); step 5 deep-only (spec 4.3); RF12 examples beyond `connect` | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Variant 1 | `prior_findings_resolved` (9 rev-2/rev-3 findings with T: line evidence) and `baseline_checks` against `auggie-review.md` / SKILL.md / `test_static_grep.py` | Medium |
| U-002 | Variant 2 | Behavioral-enforcement lens: asks whether a wrong implementation (unconditional WARN, non-deep step 5) would still pass the ACs | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The tasklist revision each card reviewed (9d4d00ed) is the revision the verdict will be applied to | Both cards declare the same `target_tasklist_sha256` | High — any finding may be stale against the current file (954add6c) | CONTRADICTED (flagged for debate attention; included in convergence denominator) |
| A-002 | Text-literal content-contract tests are an adequate guard for behavioral conditions (WARN only at quick/standard, step 5 deep-only) in a Markdown protocol | Both cards accept the RF5 test style without challenge; V2 asks for more literals, not a different kind of check | Medium — a literal-presence test cannot prove runtime behavior | UNSTATED → promoted [SHARED-ASSUMPTION] |

Taxonomy tags: S-001 L1; C-001 L1; C-002 L3 (guard/condition); C-003 L3 (guard); C-004 L2; X-001 L2; X-002 L2; A-001 L3 (state); A-002 L3 (guard). All three levels covered.

## Summary
- Total structural differences: 1
- Total content differences: 4
- Total contradictions: 2
- Total unique contributions: 2
- Total shared assumptions surfaced: 2 (UNSTATED: 1, STATED: 0, CONTRADICTED: 1)
- Highest-severity items: X-001, A-001
- Debate diff points (convergence denominator): S-001, C-001..C-004, X-001, X-002, A-001, A-002 = 9
- Similarity check: differences well above 10%; debate proceeds.
