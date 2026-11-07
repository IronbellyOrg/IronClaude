# Reviewer 1 card (analyzer, sonnet class) - 12 deviations (Regression 1, Drift 6, Necessary 3, Authorized 2)

Plan = `.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/TASK-WF-p1LivePlanBrief-20261105-164506.md`; brief = `source.md` in the same folder.

| # | Class | Location | Finding | Evidence | Sev |
|---|---|---|---|---|---|
| 1 | Regression | plan:58 (Task 1 install line) | `cmp` of "every file under src/superclaude/commands/" includes README.md and __init__.py, which the installer never copies, so the install line can never pass and every live task records `not run: install precondition failed` | src/superclaude/cli/install_commands.py:11 (_EXCLUDE_FILES = {"README.md"}), :40 (glob("*.md")) | HIGH |
| 2 | Drift | plan:58, :61, :65 | Task 1 requires `git status --porcelain` to show no modified tracked file; the tree already had tracked changes (APPROVED.md, plan file); plan:65 tolerates baseline-modified files, so the checks conflict | plan:58,61,65 | MEDIUM |
| 3 | Drift | plan:52, :556 (Task 24 brief substitution) | `<OWNER INSTRUCTION>` is replaced by the whole Constraints bullet "as it stands", which also holds plan prose, so the brief would not quote the owner's instruction word for word; "still reads NOT YET GIVEN" is a fuzzy test | spec WC-9 (spec line 77); WORKER-CONTRACT.md:183 | MEDIUM |
| 4 | Necessary | plan:14, :52, :552 | owner grant file replaced by a Constraints bullet; documented | source.md:79 | LOW |
| 5 | Drift | plan:584 (Task 25 acceptance) | still says AC-1.8 "not run for lack of the owner grant file", contradicting plan:52, :552, :580 | plan:584 | LOW |
| 6 | Necessary | plan:554 | child worktree created with `orca worktree create --parent-worktree active`, then sync, then `worker-start --worktree path:`; justified by spec 7.2 step 1 and the slot rule | spec 7.2 step 1; WORKER-CONTRACT.md:174 | LOW |
| 7 | Drift | plan:541, :544 (Task 23) | pass rule "find output is empty" cannot hold: the branch tracks many return-contract.yaml files under .dev/tasks; no pre-run baseline is saved | plan:541,544; spec AC-1.3 (spec line 319, "no return-contract.yaml appears") | MEDIUM |
| 8 | Drift | plan:19, :22, :580 | static report covers 7127c247, not the tested tip; Task 25 does not require stating that | plan:19,22,580 | LOW |
| 9 | Necessary | plan:19, :33, :58 | tip pin replaced by branch-tip.txt plus ancestor check; justified | source.md:30 | LOW |
| 10 | Authorized | plan:36, :38 | Gate line and Section check added | spec 7.2 step 1 | LOW |
| 11 | Authorized | plan:44, :473, :495 | "command not invoked" check extended to guard cases 1 and 2 | spec AC-1.7 | LOW |
| 12 | Drift | plan:405 | extra cites D-P1-5 for "worker did not stage .dev/tasks"; D-P1-5 is about skipping --handoff implement; the staging rule is WC-9 | .dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md:29 | LOW |

Advisory correctness gaps: (1) `--parent-worktree active` may resolve to the Orca UI's active worktree, not the coordinator's (plan:554; .dev/orca-command-refactor/review/p0-live-orca-help.txt:36,49,69). (2) Live tasks depend only on Task 1; a concurrent run would pollute `check --run` and the machine-wide `pgrep` (plan:41, :451).
