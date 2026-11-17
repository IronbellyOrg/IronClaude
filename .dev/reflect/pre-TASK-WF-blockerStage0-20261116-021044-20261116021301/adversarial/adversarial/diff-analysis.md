# Diff Analysis: reviewer-card Comparison (stage 0 plan)

## Metadata

- Generated: 2026-11-16T02:25:00Z
- Variants compared: 2 (variant 1 = reviewer-1 card, analyzer, haiku class, NEEDS-REVISION; variant 2 = reviewer-2 card, qa, opus class, PASS-with-notes)
- Both review `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md` (PLAN below).
- Total differences found: 9 diff points
- Categories: structural (1), content (5), contradictions (1), unique contributions (5, listed as C-001 to C-005), shared assumptions (2)
- Debate focus: correctness, coverage, deviation-classification

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Card shape | 1 finding (blocking), 2 Checked bullets, citations as a list | 3 findings (0 blocking, one MAJOR), 4 Checked bullets, run-on citations | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Severity |
|---|-------|-----------|-----------|----------|
| C-001 | Task 3's instruction to re-run `08-test/evaluate.py` overwrites `08-test/results.md` (`evaluate.py:110`), which holds hand-added sections (Diagnosis at line 54, kappa and per-kind tables at lines 83 to 89), and edits a file outside the allowed set | F1 (blocking, MAJOR, data-loss) | absent (V2's Checked bullet says only that the Task 3 figures were not re-derived) | High (unique to V1) |
| C-002 | The request says to keep the constraint that `.dev/tasks/` is always staged; the plan's Constraints omit it | absent | F1 (MINOR, non-blocking; also found by the T1 calibrator) | Low (unique to V2) |
| C-003 | Task 2 leaves the frame (how minor findings are identified and de-duplicated across the run-2 QA files, and how "appears uncorrected" is decided) to the executor, with no acceptance line that records the choice | absent | F2 (MAJOR, blocking false) | Medium (unique to V2) |
| C-004 | Task 7's recall sizing will almost certainly fall back to an advisory pass line for every gating class (about 70 to 140 planted defects per class needed) | V1 Checked: the fallback is explicit, "not an unpassable sizing check" (PLAN:104) | F3(a) (MINOR): a short spec cannot hold that many | Low |
| C-005 | Tasks 5 and 6 both include the Task 2 sample, so a stage 2 task that pools the fresh-findings set and the reviewer-called-minor set counts the same findings twice | absent | F3(b) (MINOR) | Low (unique to V2) |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Verdict | NEEDS-REVISION: a blocking data-loss defect in Task 3 | PASS-with-notes: no blocking defect found; "every live path I checked exists" | High (decides the merged verdict) |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | C-001 Task 3 overwrites its own evidence source | High |
| U-002 | 2 | C-002 dropped always-staged constraint | Low |
| U-003 | 2 | C-003 Task 2 frame unspecified | Medium |
| U-004 | 2 | C-005 double counting of the Task 2 sample | Low |
| U-005 | 2 | Detailed Task 9 anchor checks (spec lines 572, 609, 944, 946 to 947, 974, 985 to 986) | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The executor runs each command a task names exactly as written (so a command that overwrites a file is a real risk, and a frame the plan leaves open is decided silently by the executor) | Both cards grade by what the executor would do | High | UNSTATED, promoted |
| A-002 | The severity rule in the brief (blocking = an unmeetable requirement whose fix needs a decision the plan does not make, or a silent wrong or missing result, including data loss) is applied the same way by both | Both cite it | Medium | STATED, promoted for debate |

## Summary

- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 1
- Total unique contributions: 5
- Total shared assumptions surfaced: 2 (UNSTATED: 1, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001
- total_diff_points for convergence = S (1) + C (5) + X (1) + A (2) = 9
- PLAN = `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md`. The T1 calibrator and the card-2 calibrator also noted that Task 10's acceptance lines (PLAN:139 to 142) do not require items its body asks for; neither reviewer card has it (probe input).
