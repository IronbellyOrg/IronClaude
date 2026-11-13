# Diff Analysis: Reviewer Card Comparison (reflect-pre Tier 2)

## Metadata
- Generated: 2026-11-13T00:16:00Z
- Variants compared: 3 (reviewer-1 analyzer/sonnet, reviewer-2 qa/haiku, reviewer-3 refactorer/opus)
- Total differences found: 10 (structural 1, content 3, contradictions 2, unique 4)
- Calibrated card scores: reviewer-1 0.66, reviewer-2 0.55, reviewer-3 0.82 (blind per-card calibration)
- Panel pre-check: 10/10 findings calibrated, cluster_agreement 1.0, 19 citations checked 0 flagged

## Structural Differences

| # | Area | Reviewer 1 | Reviewer 2 | Reviewer 3 | Severity |
|----|------|-----------|-----------|-----------|----------|
| S-001 | Finding count / lens coverage | 3 findings (root-cause lens) | 3 findings (coverage lens) | 4 findings (structural lens) | Low |

## Content Differences

| # | Topic | Reviewer 1 | Reviewer 2 | Reviewer 3 | Severity |
|----|-------|-----------|-----------|-----------|----------|
| C-001 | Stale tasklist text (summary.md vs issue-summary.md) | F1, MINOR, "documentation-level staleness only" | not surfaced directly (adjacent via F2 row-bundling) | F1 MAJOR + F2 "AC cannot be met by on-disk tests" | Medium |
| C-002 | Scope expansion beyond spec's 4-file list | F2 INFO authorized expansion | F1 MINOR "matrix hides expansion with no spec row" | F3 INFO authorized expansion | Low |
| C-003 | Test-design / gate coherence | F3 "Task 2 gate silent on SKILL.md test" (calibrator flagged: criteria say 'pre-existing' + 'Task 1 agent tests', so gate is coherent) | F2 "INF-001 bundling overstates per-span verification" | F4 five-copy duplication rename hazard | Medium |

## Contradictions

| # | Point of Conflict | Position A | Position B | Impact |
|----|-------------------|-----------|-----------|--------|
| X-001 | Severity of the stale-text finding | R1: MINOR (archived package; documentation-level only; blocking: false) | R3: MAJOR (would fail pinned tests if executed; blocking: false) | Medium: severity label only; both agree on the fact and on non-blocking |
| X-002 | Task 2 gate coherence | R1 F3: gate "silent"/incoherent unless read narrowly | R1's own calibrator: criteria text names "pre-existing" and "Task 1 agent tests", so the gate is coherent as written | Low: single-card internal tension, not cross-card |

## Unique Contributions

| # | Variant | Contribution | Value |
|----|---------|-------------|-------|
| U-001 | R2 | INF-001 bundles rationale/consumers/failure-marker into one row; no AC asserts them individually — one-row mapping overstates per-span verification | Medium |
| U-002 | R2 | Evidence citations (t1-red.log tail only) don't expose per-file red failures or the SKILL.md negative test | Low |
| U-003 | R3 | Five byte-identical copies of the early-section paragraph (3 agents + test constants) — any rename must touch all five; already bit once | Medium |
| U-004 | R1 | Task 2 AC wording depends on reading "Task 1 agent tests" as excluding the SKILL.md test | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|----|-----------------|-----------|----------------|----------|
| A-001 | All three cards mark findings non-blocking | The package's archived (done/) status means the stale text will never be re-executed | UNSTATED | YES — [SHARED-ASSUMPTION] diff point |
| A-002 | All three cards treat on-disk agents+tests as authoritative over tasklist text | Source-precedence (code > docs) applies to the archived tasklist | STATED (implicit in every finding's evidence direction) | no |

## Summary
- Total structural: 1, content: 3, contradictions: 2, unique: 4, shared assumptions surfaced: 2 (UNSTATED: 1 promoted, STATED: 1)
- Total diff points for convergence denominator (S+C+X+A): 8
- Highest severity items: X-001, C-001, C-003 (Medium)
