# Post-review fixes to the plan (one fix cycle, applied in place before the plan's first task)

The reflect run's Tier-2 reviewers returned three findings lists (raw text is in the session transcript; the cards are summarised in `reviewer-cards/summary.md`). The plan was revised in place once. Nothing here was run through the adversarial merge (see REPORT.md, "What did not run").

| # | Finding (reviewer) | Severity | Fix in the plan |
|---|---|---|---|
| 1 | Plan pins HEAD and the base ref to `7127c247`, but the branch tip moved (merge `185f8349`, then `f0e307eb`) (R1 correctness gap, R3 #1 Regression) | HIGH | No literal tip. Task 1 saves `git rev-parse HEAD` to `./artifacts/branch-tip.txt`, requires `7127c247` as an ancestor, a clean tracked tree; every later check compares to that file |
| 2 | Install line compares only changed command files; spec says every file (R1 #2, R2 #1, R3 #2) | MEDIUM | Task 1 compares every file under `src/superclaude/commands/`, changed skill files that still exist, and `WORKER-CONTRACT.md` |
| 3 | AC-1.8 uses `worker-start --setup run` without the user naming it and without a pre-dispatch sync (R3 #3, #4; R1 note) | MEDIUM | Task 24 creates the child with `orca worktree create --parent-worktree active`, runs `make sync-dev` and the section check, then starts the worker with `--worktree path:` and no `--setup` flag |
| 4 | Task 24 skips the Worktree step outputs that later steps need (R1 #1) | MEDIUM | Task 24 now saves `lc22-worktree.json`, `lc22-branch.txt`, `lc22-status-before.txt`, checks HEAD and path |
| 5 | Step 5 conditions 2 and 3 do not fit guard refusals (R3 correctness gap) | MEDIUM | Constraints step 5: condition 2 is `not applicable` and replaced by "command not invoked" for Tasks 20 to 22; result rule says steps 3 and 4 as replaced |
| 6 | Orca help list omits `status`, `repo list`, `--version`; Task 25 version source unclear (R2 #3, R2 gap, R3 #6) | LOW | Help list extended; `orca --version` saved to `orca-version.txt`; Task 25 reads that file |
| 7 | lc12 forbids `codegraph sync`, stricter than the spec's "init/index" (R2 #2) | LOW | `sync` is a note, not a failure |
| 8 | Section-check mismatch has no rule; step 2 vs step 3 re-wait ambiguity (R1 notes) | LOW | Both rules added to the procedure |
| 9 | Wrong task numbers in the section-check and refusal lines (found while fixing) | LOW | Troubleshoot is Task 21, help is Task 22; refusal replacement applies to Tasks 18, 20, 21, 22 |
| 10 | "Nothing pushed" no longer true (R3 note) | LOW | Constraints bullet states the fork push of `185f8349` |

Not changed: the 3 INF rows that map only to the Constraints block (INF-006, 008, 011); coverage-matrix omissions R2 #5 to #11 are trace debt of the reflect matrix, not plan defects (the plan covers each span, checked by R2 against the plan lines).

Gate re-check of the revised plan: 25 tasks, six phases, no checkbox or numbered lines, every task has acceptance criteria, `7127c247` appears only as the ancestor requirement.
