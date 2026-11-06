# Diff Analysis: reviewer-card comparison (UC-1 plan review of the P1 static plan)

Variants: V1 = reviewer 1 (analyzer, sonnet, 13 findings, verdict FAIL), V2 = reviewer 2 (qa, haiku, 7 findings, verdict PARTIAL), V3 = reviewer 3 (refactorer, opus, 10 findings, verdict PARTIAL). Plan under review: `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md` (called `plan:N`). Calibrated confidence (Wave 3C): V1 0.81, V2 0.80, V3 0.82.

## Metadata
- Generated: 2026-11-05 (UTC)
- Variants compared: 3
- Total differences found: 22
- Categories: structural (2), content (9), contradictions (6), unique (6), shared assumptions (3)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card verdict | FAIL (one blocking finding) | PARTIAL | PARTIAL | Medium |
| S-002 | `t1_ref` use | maps 5 findings to T1 ids (F-001 to F-005) | maps 4 (F-003, F-006, F-007, one confirm) | marks `null` on every finding except R3-01 although its note says all null | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | graph and impact skills: closed flag tables and contract writing | R1-01 blocking: skills reject or ignore `--unattended` / `--report-dir`, write the contract only with `--output-dir` | not raised | R3-03 should-fix: Tasks 4 and 5 do not say where the worker contract goes under `--report-dir` | High |
| C-002 | init-lite CLI pass-through | R1-02 should-fix: strict click CLI rejects the flags | not raised | R3-02 should-fix: same, plus no Activation pass-through bullets and who writes the contract on `--dry-run` | Medium |
| C-003 | Task 15 path-list criterion vs `git status` | R1-05 should-fix (confirms T1 F-001) | not raised | R3-01 should-fix (confirms F-001) | Medium |
| C-004 | Task 14 nested-propagation test | R1-03 should-fix: workflow also names a nested call | not raised | R3-04 should-fix: same | Medium |
| C-005 | Python regex copy of Check SCAN | R1-04 should-fix: POSIX class never matches | not raised | R3-10 minor: same defect | Low |
| C-006 | Section placement wording | not raised | R2-03 should-fix: skeleton "final boundaries heading" vs tasks "before `## Boundaries`" | R3-08 minor: same | Medium |
| C-007 | `tests/test_cleanup_audit_structure.py` in Task 6 | not raised | R2-04 should-fix: in neither baseline | R3-06 minor: same, plus count error | Low |
| C-008 | D-P1-1 `command` key | R1-07 minor: disclosed and bounded | R2-05 should-fix: ratify D-P1-1 | not raised | Medium |
| C-009 | lint WARN counting | R1-12 minor | not raised | R3-05 minor | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Is the graph and impact skill gap blocking? | R1-01 blocking (claims both skills write the contract only with `--output-dir`; the calibrator showed that is wrong for impact) | silent | R3-03 only should-fix, about placement wording, not skill flag acceptance | High |
| X-002 | Severity of the placement wording defect | silent | R2-03 should-fix | R3-08 minor | Medium |
| X-003 | Severity of the cleanup-audit test baseline gap | silent | R2-04 should-fix | R3-06 minor | Low |
| X-004 | Severity of the regex copy defect | R1-04 should-fix | silent | R3-10 minor | Medium |
| X-005 | Severity of D-P1-1 | R1-07 minor | R2-05 should-fix | silent | Medium |
| X-006 | Does `--report-dir` next to an own flag need an UNVERIFIED entry? | R1-08 refutes (not needed) | silent | silent | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | R1-01 the skills' closed flag tables (the only card to inspect the skill flag validation) | High |
| U-002 | V1 | R1-13 graph `init` refusal timing and who writes the failed contract | Medium |
| U-003 | V1 | R1-10 adversarial `-i` and `-o` aliases | Low |
| U-004 | V1 | R1-11 stale WORKER-CONTRACT.md table (spec observation) | Low |
| U-005 | V3 | R3-09 init-lite "Write anything when `--dry-run` is set" contradiction; R3-07 workflow ref `--output` rule and `E-MISSING-DIR` ban | Medium |
| U-006 | V2 | R2-06 invariant-2 extension missing from decision list; R2-07 stale plugin copies visibility | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | A per-task reviewer judges a task only by its own text plus the Constraints, so a missing statement in a task cannot be recovered by the executor | All three flag "executor must guess" defects | UNSTATED | yes |
| A-002 | The skill files, not the command files, execute graph, impact and init-lite at run time, so command-only edits are insufficient | V1 R1-01/02 and V3 R3-02/03 rely on it; V2 never checks it | UNSTATED | yes |
| A-003 | Any plan edit after the first `/sc:implement` task starts halts the run, so every fix must land before that start | All treat fixes as pre-run edits | STATED (T1 card recommendation) | no |

| # | Assumption | Impact | Status |
|---|---|---|---|
| A-001 | Task text is self-sufficient for the executor | A fix that lives only in a Constraint or report is not enough | open |
| A-002 | Skills are the execution layer | Decides whether the C-001 and C-002 findings are blocking | open |

## Summary
- Total structural differences: 2
- Total content differences: 9
- Total contradictions: 6
- Total unique contributions: 6
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001
