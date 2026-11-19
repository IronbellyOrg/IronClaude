# Coverage matrix (UC-1, Step 1B.0)

Spec: .dev/tasks/to-do/TASK-WF-refactorTheScIss-20261118-054817/source.md (one prose line, so every citation is `source.md:1`).
Plan: .dev/tasks/to-do/TASK-WF-refactorTheScIss-20261118-054817/TASK-WF-refactorTheScIss-20261118-054817.md

Pass 1 (labeled IDs by `ID_REGEX`): 0 parsed requirements. Pass 2 (inference): 16 inferred rows. `inferred_count 16 > parsed_count 0`, so `coverage_degraded: parsed-sparse` and `coverage_undefined: true` (no parsed ID). The matching below is by judgment against the plan text (the deterministic content-word rule is not run), so every row is marked `inferred`.

| Id | Source | Verbatim quote (source.md:1) | Mapped task(s) | Match |
|---|---|---|---|---|
| INF-001 | inferred | "resolve the level in refs/claim.md Wave 5 from the Type, Complexity and Effort-estimate lines of <D>/issue-summary.md" | Task 1 | covered |
| INF-002 | inferred | "bug -> full (all bugs, including complex)" | Task 1 | covered |
| INF-003 | inferred | "feature with complexity simple or medium and no more than 16 hours -> full" | Task 1 | covered |
| INF-004 | inferred | "feature with complexity complex or over 16 hours -> worktree" | Task 1 | covered |
| INF-005 | inferred | "if type, complexity or hours cannot be read -> worktree" | Task 1 (Constraints repeat it) | covered |
| INF-006 | inferred | "An explicit --pipeline always wins" | Task 1, Task 3, Task 4 | covered |
| INF-007 | inferred | "--submit still needs an explicit --pipeline full" | Constraints, Task 3 | covered |
| INF-008 | inferred | "the issue watcher keeps passing explicit --pipeline none and never reaches the rule" | Constraints, Task 3, Task 4 | covered |
| INF-009 | inferred | "add one new Wave 5 step after step 2 (before the plan-boundary step) that sets <L> and prints one line such as 'Level: worktree (default: complex feature)', also in the final output" | Task 1 | covered |
| INF-010 | inferred | "Wave 5 step 4 and Wave 8 then use that <L>" | Task 1 (Wave 8 kept unchanged on purpose) | covered |
| INF-011 | inferred | "No new return-contract field (tests pin ten fields); pipeline_level carries the resolved level" | Constraints, Task 2, Task 5 | covered |
| INF-012 | inferred | "the already_launched re-claim path still reports the stored level" | Constraints, Task 2 | covered |
| INF-013 | inferred | "Files: src/superclaude/commands/issue.md ... plus the byte-for-byte copy plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md" | Task 1 (claim.md), Task 2 (SKILL.md lines 17, 138, next-steps.md; plan names line 89 where the source names line 92), Task 3, Task 4, Task 5, Task 6, Task 7, Task 8 | covered, one line-number difference |
| INF-014 | inferred | "Do not touch tests/issue_watch/, src/superclaude/cli/issue_watch/launch.py, or the guard and ship-gate text." | Constraints | covered |
| INF-015 | inferred | "Finish with make sync-dev, make verify-sync, and git add of the changed paths plus .dev/tasks; never stage .claude/." | Task 9 | covered |
| INF-016 | inferred | "Note claim-handoff-planb edits the same files." | Constraints (rebase before any PR) | covered |

coverage_pct (parsed-only): null. coverage_pct_union: 16/16 = 1.00. unmapped_requirements: []. unmapped_requirements_union: [].
