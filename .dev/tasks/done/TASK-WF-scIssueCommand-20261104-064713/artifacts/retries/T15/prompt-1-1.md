373e0665eaf03f5a9c74119e151859b30555d515
Review one task for spec compliance.

Task brief: Depends on: Task 14

The source schedules one manual smoke spawn per worker to confirm that the pinned picker ID is served (source section 6, section 20 item 7, default D19). Agent definitions load when a Claude Code session starts, so this check needs a session started after Task 13. If the current session started before Task 13, stop here and ask the user to start a new session in this checkout and re-run the same `/sc:implement` command; it resumes at this task. In that session, spawn `issue-worker-t3`, `issue-worker-t2` and `issue-worker-t1` once each with the Agent tool using only `subagent_type` and never the `model` parameter, with a harmless prompt that writes one file under `.dev/issues/smoke/`. Served-model evidence must come from a source outside the worker: the gateway or proxy request log entry for the call, or the model field of the subagent's transcript; the worker's own statement of its model is recorded but is not accepted as evidence. A spawn that fails because the picker ID is not served is recorded as `E-TIER-UNAVAILABLE` with the agent file and picker ID, not worked around with an alias. `.dev/issues/smoke/` is never staged; delete it afterwards only with the user's approval.

Acceptance criteria:
- `./artifacts/t15-tier-smoke.md` exists with one row per worker giving the spawn outcome and one of: served (with the external evidence source and the picker ID it shows), `E-TIER-UNAVAILABLE` (with the reason), or pending (with the reason the session could not run it). The row states the truth; a pending or unavailable row is a valid result of this task.
- `git add .dev/tasks` has been run after writing the artifact.

AC ids: T15.AC1 = first acceptance bullet (artifact with one row per worker: served, E-TIER-UNAVAILABLE, or pending with the reason; a pending row is a valid result); T15.AC2 = second bullet (`git add .dev/tasks` run after writing it; check with `git status --short .dev/tasks`).

Coordinator constraint C3 (binding; overrides the plan text where they conflict; recorded in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/coordinator-constraints.md): /sc:implement cannot ask the user mid-run, so the worker smoke spawns are recorded as pending with the reason, and the post-restart runbook at the end of Task 17's artifact lists them. The plan's "stop here and ask the user to start a new session" exit is replaced by that pending row. Round-2 minor F-15 (evidence definition) is not applied as a change, only restated in the runbook text.
Facts for checking: this session started at 2026-11-04T13:25 UTC (ledger header line 1 of .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/progress.md); .claude/agents/issue-worker-t3.md was written at 13:51:22 UTC by Task 13's make sync-dev.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 373e0665eaf03f5a9c74119e151859b30555d515
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t15-tier-smoke.md b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t15-tier-smoke.md
new file mode 100644
index 00000000..a52b21e1
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t15-tier-smoke.md
@@ -0,0 +1,19 @@
+# Task 15: worker smoke spawns on their pinned tiers
+
+Result: **pending** for all three workers. No spawn was attempted in this run.
+
+| Worker | Agent file | Picker ID pinned | Spawn outcome | Status | Reason |
+|---|---|---|---|---|---|
+| `issue-worker-t3` | `src/superclaude/agents/issue-worker-t3.md` (dev copy `.claude/agents/issue-worker-t3.md`) | `claude-gw-tier3` | not attempted | pending | see below |
+| `issue-worker-t2` | `src/superclaude/agents/issue-worker-t2.md` (dev copy `.claude/agents/issue-worker-t2.md`) | `claude-gw-tier2` | not attempted | pending | see below |
+| `issue-worker-t1` | `src/superclaude/agents/issue-worker-t1.md` (dev copy `.claude/agents/issue-worker-t1.md`) | `claude-gw-tier1a` | not attempted | pending | see below |
+
+## Why pending
+
+1. Agent definitions load when a Claude Code session starts. This session started at 2026-11-04T13:25 UTC; Task 13's `make sync-dev`, which wrote the three `.claude/agents/issue-worker-t*.md` dev copies, ran at about 13:51 UTC. This session's agent list does not contain the three workers, so a spawn by `subagent_type` cannot reach them here. (Whether a newly synced agent becomes available mid-session was not tested; the plan treats it as needing a new session.)
+2. Coordinator constraint C3 (`./coordinator-constraints.md`): `/sc:implement` cannot ask the user mid-run, so the plan's "stop and ask the user to start a new session" exit is replaced by a pending row and a post-restart runbook step.
+3. The installed copies under `~/.claude/agents/` do not exist yet (`superclaude install` has not been run for this branch); the in-checkout copies under `.claude/agents/` do.
+
+## How it will be checked (runbook step 2 in `./t17-acceptance.md`)
+
+In a new Claude Code session started in this checkout, spawn each worker once with the Agent tool using only `subagent_type` (never the `model` parameter) and a harmless prompt that writes one file under `.dev/issues/smoke/`. Served-model evidence must come from outside the worker: the gateway or proxy request log entry for the call, or the model field of the subagent's transcript. The picker ID itself, or a model from that tier's mapping in `ccsession-models.json`, counts as served. The worker's own statement of its model is recorded but is not evidence. A spawn that fails because the picker ID is not served is recorded as `E-TIER-UNAVAILABLE` with the agent file and picker ID; no alias fallback. `.dev/issues/smoke/` is never staged; delete it afterwards only with the user's approval.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
