# Q24: findings of the live Orca captures (2026-11-16)

Written by the orchestrating session from two read-only captures made on 2026-11-16 by a fresh session on master (worktree `q24-orca-capture`, created through Orca with its own agent) after the owner said "Q24 go" and "q24: second capture". **Names and values only.** The raw captures hold the prompt and message text of live sessions, so they stay outside git: `/home/coder/captures/q24-orca-capture-20261116.md` (first) and `/home/coder/captures/q24-orca-capture2-20261116.md` (second, text omitted). Nothing in this note is a grant.

## Commands run (all read-only; the first two in the sweep allow list, `src/superclaude/cli/sweep/probes.py:52` and `:58-59`)
1. `orca-ide worktree ps --agent-wait --json`
2. `orca-ide orchestration worker-show --dispatch ctx_828152156f72 --json` (a worker that finished on 2026-11-11)
3. `orca-ide orchestration worker-list --json` (one read beyond the first two, only to pick a running worker; also in the sweep allow list)
4. `orca-ide orchestration worker-show --dispatch ctx_6c922cf310da --json` (a worker that was running)

## What was seen
| Item | Value seen | Status |
|---|---|---|
| Name of the agent-wait field | `agentWait`, present on all 21 agent entries in `worktree ps` and on both the `terminal` and `observation` blocks of `worker-show` | PROVEN |
| `agentWait` for a working agent | `null` on all 6 agents whose state was `working`, and on the running worker | PROVEN |
| `agentWait` when an agent is waiting | no non-null value appeared anywhere | NOT SEEN |
| Running worker, `dispatch.status` | `dispatched` (worker-list `dispatchStatus` also `dispatched`) | PROVEN |
| Running worker, `projection.outcome` | `in_progress` (underscore) | PROVEN |
| Running worker, `projection.liveness.verdict` | `live` | PROVEN |
| Finished worker | `dispatch.status` `completed`, `projection.outcome` `succeeded`, `projection.liveness.verdict` `unverifiable` (reason `missing_status`) | PROVEN |
| Worker-list tally (100 rows) | `dispatchStatus` values seen: `completed`, `dispatched`, `failed`; one running row (`dispatched`, `in_progress`, `live`) | PROVEN |
| Worktree-level fields in `worktree ps` | `terminalVerdict` `live`; agent `state` `working` or `done`; `workspaceStatus` `in-progress` (hyphen) | PROVEN, separate fields |

## What this means for the sweep (recommendation, no code changed)
- The parked `working` rule at `src/superclaude/cli/sweep/classify.py:251-257` lists the conditions `liveness_verdict "live"`, `status "in_progress"`, `agent_wait_present True`, `agent_wait None`. The sweep sets `status` from `dispatch.status` (`src/superclaude/cli/sweep/probes.py:479`) and `outcome` from `projection.outcome` (line 480). For a running worker `dispatch.status` is `dispatched` and the word `in_progress` is the outcome, so the rule as written could never match. A rule that matches real data would read: liveness `live`, outcome `in_progress`, agent-wait key present and null.
- Not proven: what a non-null `agentWait` looks like, so the "waiting" half of the idea cannot be built from this capture. One running worker is one example; it does not show how often these values hold.
- Worth checking (unverified when written): `classify.py:245` tests `orca.status == "ready"`. No `dispatchStatus` in the 100 list rows was `ready`; `ready` appears as `worker.state`, a different field. **Result (2026-11-17):** not a mismatch; the sweep sets that status itself on rows from `task-list --ready` (finding of the fix session, recorded in `docs/designs/orchestrator-mode.md`).
- This closes the "shared capture" the Q14 answer waits for, except for the non-null `agentWait` value.
- **Outcome (2026-11-17):** the `working` class was restored by PR #579 (merged 2026-11-17 00:29 UTC, commit `b46ecc1bd`), with a fixture copied from the running-worker capture (title and preview text removed) and two follow-up tests. A non-null `agentWait` is still not captured; such a row stays "waiting on a person" and is never classed `working`.
