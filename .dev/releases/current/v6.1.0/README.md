# v6.1.0 release records

These files record the IronClaude 6.1.0 release (the task and documentation bundle, Part B of plan issue 571, tracked by issue 647), run by the `ic6-orchestrator` session on Clay's approval relayed by GeneralIronFlow on 2026-11-18 20:57 UTC. They live on branch `clayphi/release-6.0.0` (the same records branch as 6.0.0, so nothing new needs to be created; never merge a pull request from it with `--delete-branch`) and are committed and pushed after every merge.

| File | What it holds |
|---|---|
| `RELEASE-READINESS.md` | What the release depends on (owner for every item), the pull requests with state and links, the gate G1 to G9, tag and release, finished worktrees. |
| `DECISIONS.md` | Each decision, who made it and when. |
| `PROCESS-LOG.md` | One entry per step, with times and what should change. |
| `prompts/` | Prompts sent to agents by the orchestrator (none yet). |

The lessons of 6.0.0 that apply here are in `../v6.0.0/RETROSPECTIVE.md` (proposals only). The first one is applied: `RELEASE-READINESS.md` section 1 lists every item the release depends on with an owner, or marks it "not in this release", before the release pull request is opened.
