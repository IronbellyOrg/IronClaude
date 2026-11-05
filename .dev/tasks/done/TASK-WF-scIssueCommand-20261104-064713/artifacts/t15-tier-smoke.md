# Task 15: worker smoke spawns on their pinned tiers

Result: **pending** for all three workers. No spawn was attempted in this run.

| Worker | Agent file | Picker ID pinned | Spawn outcome | Status | Reason |
|---|---|---|---|---|---|
| `issue-worker-t3` | `src/superclaude/agents/issue-worker-t3.md` (dev copy `.claude/agents/issue-worker-t3.md`) | `claude-gw-tier3` | not attempted | pending | see below |
| `issue-worker-t2` | `src/superclaude/agents/issue-worker-t2.md` (dev copy `.claude/agents/issue-worker-t2.md`) | `claude-gw-tier2` | not attempted | pending | see below |
| `issue-worker-t1` | `src/superclaude/agents/issue-worker-t1.md` (dev copy `.claude/agents/issue-worker-t1.md`) | `claude-gw-tier1a` | not attempted | pending | see below |

## Why pending

1. Agent definitions load when a Claude Code session starts. This session started at 2026-11-04T13:25 UTC; Task 13's `make sync-dev`, which wrote the three `.claude/agents/issue-worker-t*.md` dev copies, ran at about 13:51 UTC. This session's agent list does not contain the three workers, so a spawn by `subagent_type` cannot reach them here. (Whether a newly synced agent becomes available mid-session was not tested; the plan treats it as needing a new session.)
2. Coordinator constraint C3 (`./coordinator-constraints.md`): `/sc:implement` cannot ask the user mid-run, so the plan's "stop and ask the user to start a new session" exit is replaced by a pending row and a post-restart runbook step.
3. The installed copies under `~/.claude/agents/` do not exist yet (`superclaude install` has not been run for this branch); the in-checkout copies under `.claude/agents/` do.

## How it will be checked (runbook step 2 in `./t17-acceptance.md`)

In a new Claude Code session started in this checkout, spawn each worker once with the Agent tool using only `subagent_type` (never the `model` parameter) and a harmless prompt that writes one file under `.dev/issues/smoke/`. Served-model evidence must come from outside the worker: the gateway or proxy request log entry for the call, or the model field of the subagent's transcript. The picker ID itself, or a model from that tier's mapping in `ccsession-models.json`, counts as served. The worker's own statement of its model is recorded but is not evidence. A spawn that fails because the picker ID is not served is recorded as `E-TIER-UNAVAILABLE` with the agent file and picker ID; no alias fallback. `.dev/issues/smoke/` is never staged; delete it afterwards only with the user's approval.
