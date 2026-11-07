# T1 reflection card (UC-1, pre-execution), round 2

Spec: `.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/source.md` (the brief, 20906 bytes). Tasklist: `.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-20261105-164506/TASK-WF-p1LivePlanBrief-20261105-164506.md` (586 lines, 25 tasks, 6 phases, depth standard). Round 1 of this review found a stale tip pin and 9 other issues; the plan was revised once (`.dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105165021/post-fix-rechecks.md`) and the owner-instruction file requirement was then removed (plan line 52). This round audits the revised plan.

## Root-cause / deviation (analyzer slice)

- Pass 1 found 0 parsed requirement ids (the brief uses AC-x.y, lcNN and D-P1-n labels). Pass 2 enumerated 39 quote-pinned rows (`artifacts/coverage-matrix.yaml`).
- Candidate deviation (a), Drift: plan line 52 and Task 24 (line 552) replace the brief's owner grant file (`source.md:79`) with a Constraints bullet. The brief still names the file; the plan supersedes it on purpose, because the file is in no spec or decision. Candidate label: Necessary deviation, documented at plan line 19 and line 52.
- Candidate deviation (b), Authorized expansion: the plan adds a Gate line (line 36) and a Section check (line 38) the brief states only in prose (`source.md:30`).
- Candidate deviation (c), Necessary deviation: Task 24 (line 552) creates the child worktree with `orca worktree create --parent-worktree active` and syncs it before dispatch, instead of the brief's `worker-start --worktree new-child --setup run` (`source.md:79`), because spec 7.2 step 1 requires the sync before dispatch (`orca-worker-contract-spec.md:283`) and WORKER-CONTRACT.md slot rules allow `--setup run` only when the user names it (`WORKER-CONTRACT.md:174`).
- Verified-open risk: whether `orca worktree create --parent-worktree active` accepts `active` from this terminal is UNVERIFIED; Task 1 saves the help text (plan line 58) and a usage error is recorded as FAIL (plan line 29).

## Coverage / acceptance (qa slice)

- 39 inferred rows. 36 map to a task item by the 0.6 containment rule; INF-006, INF-008, INF-011 map to the Constraints block. Union coverage 1.0 with Constraints, 0.9231 task-only.
- lc01 to lc22 each have their own task (Tasks 2 to 22 and 24), AC-1.3 is Task 23, the phase report is Task 25. Command lines match `source.md:51-79` exactly (checked by round-1 reviewer 3).
- Refusal checks: Tasks 18, 20, 21, 22 replace steps 3 and 4 and, for Tasks 20 to 22, condition 2 of step 5 is `not applicable` (plan line 44).
- Tip pin: Task 1 (line 58) records `git rev-parse HEAD` to `./artifacts/branch-tip.txt` and requires `7127c247` as an ancestor; the live tip is `f0e307eb` (git log, grounding hunk G9).

## Structural / tech-debt (refactorer slice)

- The live-check procedure is written once in Constraints (lines 35-49) and each task repeats a four-bullet acceptance block. Intentional, for reviewer isolation; any edit after the first task halts the run (E-PLAN-CHANGED, plan line 29).
- Tasks run strictly in order; no parallelism marker. A long run is expected (P0 workflow check took 87 minutes).
- Task 24 (line 552) depends on one sentence from the owner copied into plan line 52 before the run; until then it is a recorded `not run`.

## Recommendations (each with a target and a check)

1. Before `/sc:implement`, copy the owner's AC-1.8 sentence into plan line 52. Check: `grep -c 'NOT YET GIVEN'` on the plan prints 0.
2. Run `uv run superclaude install --force` is already done; Task 1's install line (plan line 58) must therefore print PASS. Check: `./artifacts/preflight.md` install line PASS.
3. Run `/sc:implement <plan path>` from an Orca terminal session (depth 0). Check: Task 1 saves `./artifacts/live-run.json` with `result.run.coordinator_handle` equal to `$ORCA_TERMINAL_HANDLE`.

## Self-reported confidence

0.80 (open risks: the `--parent-worktree active` selector, and the unverified behaviour of `claude -p` under `acceptEdits`).
