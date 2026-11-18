# Diff Analysis: Reviewer-card Comparison (reflect Wave 4, Mode A)

## Metadata
- Generated: 2026-11-13T02:20:00Z
- Variants compared: 3 (V1 analyzer/sonnet, V2 qa/haiku, V3 refactorer/opus)
- Total differences found: 7
- Categories: structural (1), content (4), contradictions (1), unique (3), shared assumptions (2)

## Structural Differences

| # | Area | V1 (analyzer) | V2 (qa) | V3 (refactorer) | Severity |
|---|------|------|------|------|----------|
| S-001 | Findings count | 3 findings | 0 findings (adherence summary only) | 2 findings | Medium |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Ungated process constraints (staging, no-commit) | F1+F2: two MINOR missing-requirement findings, spec+plan cited | Not raised (constraints acknowledged as "explicit constraints", treated as honored) | Not raised | Medium |
| C-002 | Task 2 AC coherence (force/nonforce paths) | F3: AC2's "including when files already exist" vs AC1's "no Orca calls" nonforce reading — MINOR other | Not raised; summary asserts full adherence | Not raised | Medium |
| C-003 | Copy-matching (core/CLAUDE.md vs README) | Not raised | Not raised | F1: MINOR other — Task 1 criteria check per-copy items, never compare copies; delivered copies already differ on the ccsession-orca sentence | Medium |
| C-004 | Unpassable no-rewrite clause | Not raised | Not raised | F2: MINOR unpassable-check — "edited-guide contents are not rewritten by IronClaude" cannot fail (helper never writes guide files; tests stub Orca); only the no---force check enforces do-not-overwrite | Medium |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Overall verdict on the plan | V1: 3 defects (plan text has ungated constraints, AC-coherence gap) | V2: 9/9 fully adherent, 0 deviations | V3: 2 defects (no copy-compare, unpassable clause) | Medium — no factual conflict over any specific span; V2's zero is an absence of findings, not an assertion that V1/V3 spans are compliant. Under the audit rules a zero-findings card states a stance, not evidence against the others. |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 | F3 AC1/AC2 force-path ambiguity (only the force path can satisfy AC2's "including when files already exist") | Medium |
| U-002 | V3 | F1 no-copy-comparison gap with concrete drift evidence (core:51 vs README:234-235) | Medium |
| U-003 | V3 | F2 unpassable no-rewrite clause (code never writes guides; enforcement is only via no---force) | Medium |

## Shared Assumptions

| # | Assumption | Source Agreement | Impact | Status |
|---|------------|------------------|--------|--------|
| A-001 | All three cards treat the post-hoc (archived package) vantage as ground truth for what the executor did, discounting "no before-state baseline" as audit vantage rather than executor defect. | All three variants audit the plan text against package-internal evidence | Medium | STATED (in briefs) — not promoted |
| A-002 | Findings must name a spec or plan span; code/test-file evidence used to justify a finding is described in prose, not cited as findings-v2 citation roles. | All three variants emit plan/spec citations only | Low | STATED (schema constraint) — not promoted |

## Summary
- Total structural differences: 1
- Total content differences: 4
- Total contradictions: 1
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 0, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: none High; 6 Medium (S-001, C-001..C-004, X-001)
- Similarity check: findings sets are disjoint across V1/V3 and empty in V2; total differences 7 of ~10 comparable items (>10%) — debate proceeds.
