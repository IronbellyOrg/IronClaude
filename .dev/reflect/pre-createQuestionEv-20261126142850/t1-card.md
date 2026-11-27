# Tier 1 reflection card (UC-1, pre-execution, second review of the regenerated plan)

Spec: .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-142533/source.md
Plan: .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-142533/TASK-WF-createQuestionEv-20261126-142533.md
Author of the plan (executor): the orchestrating session, model claude-gw-tier1b (the `sonnet` alias class).
hypothesis_source: inline-fallback (the orchestrator wrote this card; no separate Tier 1 agent was spawned).
Prior review: the first plan (now archived) had blocking 3, medium 10, note 5; this plan was regenerated from a source that carries 24 labelled requirements R-001 to R-024 for those findings.

## Root-cause / deviation findings

- C1 (Grounded). The three blocking findings of the first review each have a covering task or constraint in the new plan. M-01 (tests of a test-local rule): the Constraints call the Phase 1 tests notes-contract tests (plan line 21), and Task 9 caps criteria 2 and 5 at "partly evidenced" for scenarios no run exercises (plan line 205). M-02 (no stop when the harness cannot observe questions): Task 4 ends in a stop report and "Task 5 does not start until the lead's reply is written into this file" (plan line 104, acceptance at line 108). M-03 (GitHub write paths and unscanned logs): the Constraints list the extra write paths to block (plan line 22), Task 5 builds the fake `gh`, the run script and the secret scan (plan line 116), and Task 9 runs the scan before anything is staged (plan line 191).
- C2 (Grounded). The matrix-wide stop that the first plan kept only in the last run task is now in the Constraints (plan line 23) and in a preamble before Task 6 (plan line 134).
- C3 (Grounded). The plan states that the installed copy of the skill and workers differs from `src/` and that runs must load `src/` (plan line 24), and Task 5 asks for `read-files.txt` per run, built from the run's own event log (plan line 120), instead of relying on the self-test hash list alone.
- C4 (Grounded). The closing keyword rule is `Refs #834` unless every criterion is delivered with run evidence (plan lines 25 and 234), with AC2 and AC5 capped by Task 9 (plan line 205), so the expected outcome is `Refs #834`, as the lead's scope change requires (source.md:43).
- C5 (Grounded). Mechanical coverage: parsed 24 of 24 requirements matched by exact id, union 0.8421 over 38 rows, `S_dev_density` 0.1579, no `coverage_degraded` (artifacts/coverage-matrix.json). The six unmapped inferred rows (INF-001, 002, 003, 004, 007, 009) are each covered by hand: INF-001 and INF-009 across Tasks 5 to 9, INF-002 by the Constraints and Task 9, INF-003 by the issue-state read in Task 9 (plan line 191) and the Constraints (plan line 25), INF-004 by Tasks 1 to 3, INF-007 by Task 4 (plan line 104).
- C6 (INFERRED). When Task 4's stop report triggers, the plan cannot finish without a reply from the lead; an unattended executor would stop at Task 4. That is intended by the spec (source.md:35), but the plan does not say who writes the reply into the file or how the executor waits.
- C7 (INFERRED). The plan still sets no time or cost ceiling on the nine controlled runs; only stop conditions end the matrix early.
- C8 (INFERRED). Task 5 builds three scripts and a self-test in one task (plan lines 116 to 127), which is large for one task, although each file is named.

## Coverage / acceptance findings

- C9 (Grounded). Each of the six acceptance criteria is now quoted in full in Task 9 (plan lines 191 to 205), so the verdicts are graded against the real criterion text, and AC4 requires reading the three claim-boundary files and showing an empty diff for them (plan line 205).
- C10 (Grounded). AC6 is "pending" in Task 9 and refreshed from the gate results in Task 11 (plan lines 207 and 234), so it is not graded before its evidence exists. The gates run in Task 10 (`make test` at plan line 222) and Task 10 also carries R-024 (plan line 219).
- C11 (INFERRED). The two preserved-flag descriptions drop the "Feature:" word, so the run no longer pairs a description that states a mode with a contradicting flag; whether the rule then asks zero questions is what the run measures, and the plan records any difference as a finding rather than a failure.
