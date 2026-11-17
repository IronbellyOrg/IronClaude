# Diff Analysis: reviewer-card Comparison

## Metadata

- Generated: 2026-11-15T21:25:00Z
- Variants compared: 2 (variant 1 = reviewer-1 card, analyzer, haiku class; variant 2 = reviewer-2 card, qa, opus class)
- Both cards review the same plan: `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md` (PLAN below). Both return NEEDS-REVISION.
- Total differences found: 12 diff points
- Categories: structural (1), content (9), contradictions (0), unique contributions (6, listed as content points C-003 to C-006, C-008 and C-009), shared assumptions (2)
- Debate focus: correctness, coverage, deviation-classification

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Card shape | 4 findings (3 blocking, 1 minor), 4 Checked bullets | 6 findings (4 blocking, 2 minor), 7 Checked bullets, longer who/wrong-result prose | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Severity |
|---|-------|-----------|-----------|----------|
| C-001 | Task 40 allow-list names the plugin mirror of `rule.md`; the existence check fails until Task 46 creates it | V1 F1 (blocking, MAJOR): "its plugin mirror path" PLAN:477, "does not exist" PLAN:482, Task 46 PLAN:546 | V2 F3, second half (blocking, MAJOR): same three lines | Medium (agreed) |
| C-002 | Task 46 copies the skill folder, then edits the source registry, so the T15 parity check fails | V1 F4 (MINOR, non-blocking) | V2 F5 (MINOR, non-blocking) | Low (agreed) |
| C-003 | Task 41 gives `agent_template_analysis.md` a digest and a `v2` registry row, but the registry has no row for it (exactly 11 `digest` rows) and the file holds no definition sentence, only a merge-rule line | V1 F2 (blocking, MAJOR) | absent (V2 Checked says only "exactly 11 files hold the definition sentence") | High (unique to V1) |
| C-004 | Task 6 says the fresh-findings classifier evaluation "is run at stage 2, not here"; no stage 2 task consumes `./artifacts/fresh-findings.md` | V1 F3 (blocking, MAJOR, missing-requirement) | absent | Medium (unique to V1) |
| C-005 | Plan says "Run `/sc:implement` on one phase at a time and stop at each gate"; `/sc:implement` runs a whole plan file and fails with `E-PLAN-CHANGED` if the plan changes after the first task, so Tasks 11 to 46 run straight through; no task requires a recorded owner go | absent | V2 F1 (blocking, MAJOR) | High (unique to V2) |
| C-006 | Task 31 only reports the seeded-recall result; Task 33 depends on Task 31 being finished, not on it passing | absent | V2 F2 (blocking, MAJOR, safety) | High (unique to V2) |
| C-007 | Task 13 requires `refs/scale-map.md` to hold a section naming the three merge-rule phrases; Task 40's scan covers that file and its allow-list does not list it | absent | V2 F3, first half (blocking, MAJOR) | Medium (unique to V2; also in the T1 card as O1) |
| C-008 | Task 25's T3 check fails on `commands/spec-panel.md:220`, which holds a `src/superclaude/` path, in a pointer-only row | absent | V2 F4 (blocking, MAJOR) | Medium (unique to V2) |
| C-009 | The coverage matrix omits four source lines and maps four rows to the Constraints block | absent | V2 F6 (MINOR, non-blocking) | Low (unique to V2) |

## Contradictions

None. No claim in one card is opposed by a claim in the other.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | C-003 analysis-template digest vs registry count | High |
| U-002 | 1 | C-004 fresh-findings evaluation has no task | Medium |
| U-003 | 2 | C-005 `/sc:implement` cannot stop at phase gates | High |
| U-004 | 2 | C-006 Task 31 gates nothing | High |
| U-005 | 2 | C-007 scale-map self-trip | Medium |
| U-006 | 2 | C-008 T3 fails on `spec-panel.md:220` | Medium |
| U-007 | 2 | C-009 coverage-matrix omissions | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The executor follows the plan's acceptance checks literally and runs the plan through `/sc:implement` as one file (so any check that cannot pass, or any gate that is only prose, is a real defect) | Both cards classify unpassable checks as blocking | High | UNSTATED, promoted |
| A-002 | The severity rule "blocking = an unmeetable requirement whose fix needs a decision the plan does not make, or a silent wrong or missing result; wording and mechanical coordinate errors with stated intent are minor" is applied the same way by both reviewers | Both cards grade Task 46 order MINOR and the rest MAJOR | Medium | STATED in the brief, promoted for debate |

## Summary

- Total structural differences: 1
- Total content differences: 9 (agreed: 2; unique to V1: 2; unique to V2: 5)
- Total contradictions: 0
- Total unique contributions: 7
- Total shared assumptions surfaced: 2 (UNSTATED: 1, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-003, C-005, C-006
- total_diff_points for convergence = S (1) + C (9) + X (0) + A (2) = 12
