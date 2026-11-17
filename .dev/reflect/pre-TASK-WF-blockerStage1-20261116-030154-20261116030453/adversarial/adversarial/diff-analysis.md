# Diff Analysis: reflect reviewer-card comparison (UC-1 pre-execution audit of plan TASK-WF-blockerStage1-20261116-030154)

## Metadata

- Generated: 2026-11-16T03:40:00Z
- Variants compared: 3 (variant-1 = reviewer 1, analyzer, sonnet class; variant-2 = reviewer 2, qa, haiku class; variant-3 = reviewer 3, refactorer, opus class)
- Total differences found: 17 diff points
- Categories: structural (2), content (10), contradictions (2), unique (8, folded into content rows and tagged), shared assumptions (3)
- Plan under audit (PLAN:<n>): `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`; source request: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md`; program spec (SPEC:<n>): `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`
- Variant findings, as graded by their reviewers: V1 = F1 stoprule file, F2 allow-list, F3 Task 7 grep (all blocking), F4 scale-map layout (MAJOR, non-blocking), F5 `.dev/pr-monitor/` (minor), F6 ledger adapters and Task 10 dependency (minor). V2 = F1 Task 7 grep, F2 stoprule file, F3 review-ledger/1 mapping (all blocking). V3 = F1 stoprule file, F2 Task 7 grep (blocking), F3 T2 scan versus doctor.py (minor), F4 sketch test location (minor).
- Taxonomy level (L1 surface, L2 structural, L3 state-mechanics) is shown per point.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Level | Severity |
|---|------|-----------|-----------|-----------|-------|----------|
| S-001 | Card organization and finding count | 6 findings (3 blocking, 1 MAJOR non-blocking, 2 MINOR), five `Checked` groups, "Not verified" line | 3 findings (all blocking), four `Checked` bullets | 4 findings (2 blocking, 2 MINOR), ten `Checked` bullets plus a closing note | L2 structural | Low |
| S-002 | Citation formatting (path style, range style) | repo-relative paths, `path:N` or `path:N-M` | absolute paths, `path:N-N` ranges | repo-relative paths mostly, one absolute-free; `path:N-N` ranges | L1 surface (formatting) | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Level | Severity |
|---|-------|--------------------|--------------------|--------------------|-------|----------|
| C-001 | Task 7's grep acceptance line (PLAN:115) after Task 10 reuses the reader (PLAN:148); no "until Task N" | blocking (F3); adds that Tasks 12 and 13 "likely" also import it, and a separate half about Task 1's `verify-sync` line | blocking (F1); only Task 10 named | blocking (F2); only Task 10 named; adds `__pycache__` grep noise; cites source.md:17 | L3 state-mechanics (the check is a guard whose state changes after Task 10) | High |
| C-002 | Stoprule/finding-grader family has no defining file in the repository, against Task 3's "exists in the repository" line (PLAN:62) and T4 (PLAN:209) | blocking (F1); says Task 3, Task 5 and T4 cannot all pass because the only repository copies are under `.dev/experiments/` and Task 5 forbids `.dev/` strings (PLAN:87) | blocking (F2); installed path fails the check, an unrelated repository file would misrepresent the scale | blocking (F1); T4 must not read `~/.claude`; OD10 is undecided so the executor cannot bring the files in | L3 state-mechanics (boundary of the checkout versus installed copies) | High |
| C-003 | Task 3's "Merge-rule allow-list" is narrower than the stage 3 scan: `remediate_parser.py:55,301` and `fmea_classifier.py:304` hold the phrases (unique to V1) | blocking (F2) | not raised | not raised | L2 structural (component: allow-list feeding a later test) | High |
| C-004 | Mapping of follow-up rows to `review-ledger/1` rows (SPEC:404) has no task (unique to V2 as a blocker; V1 touches it as "ledger adapters") | minor (F6, "ledger adapters" listed at SPEC:945 with no task) | blocking (F3) | not raised | L2 structural | Medium |
| C-005 | Task 9 and Task 12 read the reviewer label "through the scale map" but Task 3 fixes no table layout or path convention, and no dependency edge links them (unique to V1) | MAJOR non-blocking (F4) | not raised | not raised | L2 structural (interface between a doc file and code) | Medium |
| C-006 | Task 4's location rule (REQ-07) cites `.dev/pr-monitor/` while Task 5's grep bans `.dev/` over the skill folder (unique to V1) | minor (F5) | not raised | not raised | L2 structural | Low |
| C-007 | Task 10 declares `Depends on: Task 9` only while reusing Task 7's reader (unique to V1) | minor (second half of F6) | not raised | not raised | L2 structural (dependency edge) | Low |
| C-008 | T2 reverse scan over `src/` versus fence-opener text in `doctor.py` (unique to V3) | not raised | not raised | minor (F3) | L2 structural (module) | Low |
| C-009 | Where the "agrees with the sketch" test lives; sketch sits under `.dev/tasks/to-do/` and moves on archive (unique to V3) | not raised | not raised | minor (F4) | L2 structural | Low |
| C-010 | Task 1's `make verify-sync` line (PLAN:40) after Tasks 2 to 6 add files; no task re-runs `make sync-dev` (unique to V1, bundled into its F3) | blocking, bundled into F3 | not raised | not raised | L2 structural | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|-------------------|--------------------|--------------------|--------------------|--------|
| X-001 | Does the missing `review-ledger/1` mapping (or "ledger adapters") block stage 1? | Minor: "no task builds or drops them" (V1 F6, quote: "Spec stage 1 lists \"ledger adapters\", and no task builds or drops them") | Blocking: "no task defines that mapping ... those tests can pass without the required result" (V2 F3) | Silent (V3 Checked: "Compared ... command registration"; no finding) | Medium |
| X-002 | Is a Task 7 grep line that becomes false only after a later task a blocking defect when a one-phrase fix exists? V1/V2/V3 all grade blocking, but the calibrators flagged the grade as arguable (V2 calibrator: "a non-blocking grade is also arguable") and V3's calibrator "F3 weak" | Blocking (F3) | Blocking (F1) | Blocking (F2) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | C-003 allow-list incompleteness against the stage 3 scan | High |
| U-002 | V1 | C-005 scale-map layout / dependency gap | Medium |
| U-003 | V1 | C-006 `.dev/pr-monitor/` versus Task 5 grep | Low |
| U-004 | V1 | C-007 and C-010 (dependency edge; verify-sync) | Low |
| U-005 | V2 | C-004 as blocking | Medium |
| U-006 | V3 | C-008 fence text in code versus T2 scan | Low |
| U-007 | V3 | C-009 sketch test location | Low |
| U-008 | V3 | Checked list: `_has_corresponding_command` is false for the new skill; `test_review_cli.py:44-48` checks four names only; banned-phrase scans do not hit the spec text Task 2 copies | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | C-002 (all three) | "Exists in the repository" means a tracked path a test can resolve inside the checkout and a skill file may cite; an installed `~/.claude` copy and a `.dev/experiments` bundle copy do not count (boundary of what the check may read) | UNSTATED (V3 states "without reading `~/.claude`", V1 states the `.dev/` ban; none states the full boundary) | yes |
| A-002 | C-001 (all three) | The final review of the package re-reads every acceptance line as a standing requirement (state after all 16 tasks), not only at the time its own task finishes | STATED in V1 and V2 ("at final review"), UNSTATED in V3 | no (STATED) |
| A-003 | C-001, C-002 (all three) | Invariant: a check that is false at the final review blocks even when an executor could trivially add an end point or reword at execution time (blocking grade independent of fix cost) | UNSTATED | yes |

## Summary

- Total structural differences: 2
- Total content differences: 10
- Total contradictions: 2
- Total unique contributions: 8
- Total shared assumptions surfaced: 3 (UNSTATED: 2 promoted, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003
- total_diff_points for convergence = S (2) + C (10) + X (2) + A promoted (2) = 16. Taxonomy coverage: L1 = 1 point (S-002), L2 = 10, L3 = 5 (C-001, C-002, A-001, A-003, X-002 tagged by their text signals "guard", "boundary", "invariant", "state").
