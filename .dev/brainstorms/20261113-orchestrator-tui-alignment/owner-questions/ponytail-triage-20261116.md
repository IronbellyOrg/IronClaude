# Ponytail triage of the open owner questions (2026-11-16)

Written by the orchestrating session from three read-only review agents (`pt-observer`, `pt-watcher`, `pt-sweep-v2`). The agents could not write files, so their reports came back as chat text and are not saved. **Recommendations only. Nothing here answers a question for the owner, and nothing is a grant.** Read `open-decisions.md` in this folder first for what each Q means.

## Verified by the orchestrating session (2026-11-16)

- The observer snapshot `/home/coder/.local/state/superclaude/observe/snapshot.json` was last written 2026-11-11 19:49 UTC. No code in `src/` reads it (the only other `snapshot.json` hits are the PR tool's own state file).
- `QUESTION_GATE_PASSED = False` at `src/superclaude/cli/observe/commands.py:67` on master.
- Sweep source on master is 3,731 lines in 6 files; its `working` rule is a stub that returns `None` (`src/superclaude/cli/sweep/classify.py:251-257`).
- Issue #423 (Orchestrator v2) is open and untouched since 2026-11-08.
- `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp` (branch `409-Phase2`) still holds two unpushed commits (`1ae72e1a1`, `f104ca51a`) and untracked `owner-decisions-20261108.md`, `live-test-guide.md`, `handoff-mvp-brainstorm.md` and `tuibbs-review/`.
- The fork has no `issue-watch` labels (`gh label list`).
- The route B plan records Q41 as answered on 2026-11-14 (Task 19, line 226 of `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-b/.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909/TASK-WF-planDecision6BFo-20261114-174909.md`).
- `src/superclaude/core/WORKER-CONTRACT.md:288` says person-started sessions "are never messaged". It does not mention sessions the issue watcher starts.

Not verified: the agents' test and line counts other than the sweep's, the 438-row snapshot count, and the watcher and observer sizes. No agent ran any test. Only one agent said it ran the ponytail audit skill by hand; none confirmed a separate audit run.

## The 11 open rows, trimmed

| Q | Verdict | Reason |
|---|---|---|
| Q7 | ANSWER TODAY (shrunk) | A backup, not a decision: the owner's only pass-record copies are unpushed in a side checkout. One word is enough. |
| Q24 | ANSWER TODAY (shrunk) | Two read-only commands pasted into one file replace the three checks (see below). |
| Q41 | BOOKKEEPING | The plan already records answer A. One line in `owner-answers.md` closes it. |
| Q13 | THEATRE | The observer only uses a command that answers `skills list --json` with `orca-cli`, so the screen reader cannot be picked. The risk it accepts cannot occur. |
| Q15 | THEATRE (one caveat) | Person-started sessions are already never messaged. Caveat: that sentence does not cover watcher-started sessions, which the card names as the open case. |
| Q14 | SAFE DEFAULT | #423 already bars building anything before a brainstorm and research. Do not make a code change a start gate. |
| Q8 | DEFER until release 3 is scheduled | Q19 moved the next work to summaries. A record today would describe a changed direction. |
| Q22 | DEFER until a reader of `snapshot.json` exists | No reader exists. The file already carries `generatedAt`. |
| Q30 | DEFER until the questions panel is scheduled | The panel is off and has no audience after Q19 and Q17. |
| Q20 | DEFER until the watcher schedule is installed | No schedule, so no sessions spawn. |
| Q29 | DEFER until the first coordinator is opened | No coordinator exists to run the sweep. Both installed copies predate the sweep merge. |

Q24 shrink: run `orca-ide worktree ps --agent-wait --json` and `orca-ide orchestration worker-show --dispatch <one live id> --json` (both are in the sweep's allow list, `probes.py:52` and `:58-59`), and paste both outputs into one file. The observer snapshot already holds two of the three unknown Orca names; only `agentWait` is missing. The id comparison and the message-write test are not needed now. Each check still needs its own permission row.

## Over-engineering findings (agent recommendations; the owner decides)

1. **Approval flow, 19 tasks to about 9.** One owner on one host needs one approval place (the coordinator), a plan hash the worker checks, and an at-most-once lock. The GitHub label and comment input, its checks and its fixtures (Tasks 2, 4, 5, 6, most of 3) defend an input a single owner does not need, and cost about 4,000 lines by the agent's estimate. Merge Tasks 9 and 10, and 17 and 18. Defer 7 and 13 to 15 (the second-issue guard). Drop 19. **This conflicts with the owner's Decision 3 (approval label, with the exact comment "ideally").** Dropping it would be a change to that decision.
2. **Order.** Plan A (10 tasks) is built before the one event that shows anything works. Split the first live test: FU-1a is one hand-run watcher launch on an owner-written test issue; FU-1b is one throwaway `worker-start`, `ask` and `reply` on a scratch worktree, with no GitHub. FU-1b is the only source of route B facts.
3. **Task 16 (remove plain `approved`).** The agent finds it closes little: a bare `approved` and `/sc:implement x` arrive through the same channel, and the second stays. **The owner answered "remove now" (Q39); this is a challenge to that answer, not a change to it.**
4. **Issue watcher.** 4,795 source lines and 19,709 test lines, never run live, no labels, no config, no schedule, and 13 claims typed by hand in 12 days. Tests pin 19 invented replies. The agent says to freeze it, run FU-1a, and delete the package if it fails or goes unused. One dead helper (`slo_numbers`, about 47 lines plus a 421-line test) has no caller. The agent suggests replacing Q20 with: "Will you apply the trigger label from somewhere you cannot type a claim, in the next 30 days?"
5. **Observer.** The questions panel is switched off and costs about 2,500 source and test lines plus five owner questions. The snapshot export has no reader. Three copies of the Orca finder exist, with one parity test. Freeze all three.
6. **Sweep.** 3,731 source and 9,095 test lines, zero live runs, no coordinator. The classifier's `working: 0` reads as "none working" although the class is off: add a one-line caveat. A possible bug: the parked rule looks for `status` `in_progress` but real data has it under `outcome` (UNVERIFIED for `worker-show`).
7. **Orchestrator v2 (#423).** Nothing built, 14 acceptance boxes unchecked. Do not design it until a person reports duplicate or colliding work.

## What would change these verdicts

A coordinator showing `unknown` for most running workers (restore `working`); two agents editing the same files (start the v2 brainstorm with that case); a sweep report showing fewer workers than the observer (run the id comparison); the owner wanting to start work from a phone by label (the watcher is then justified).
