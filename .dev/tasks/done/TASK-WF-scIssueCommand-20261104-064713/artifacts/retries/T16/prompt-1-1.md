1f31901043bb550325a7e5270f34565aaf4a137e
Review one task for spec compliance.

Task brief: Depends on: Task 14

The source schedules one manual smoke claim against a ClickUp test task (source section 12, last paragraph; section 20 item 5). It needs a ClickUp test task whose description links a test GitHub issue URL on `IronbellyOrg/IronClaude`, and `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` exported by the user in their own shell before the session started. Ask the user only for the test issue URL and task ID; never ask for, print, echo or inline the token or workspace values. If the variables are not exported, record the task as pending and stop. Otherwise run `uv run --no-project python src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py --issue-url <test issue url> --issue-number <N> --repo IronbellyOrg/IronClaude` twice (the second run should report `already_assigned`). Compare the live response shapes with the fixtures in `tests/skills/test_clickup_claim.py` by key paths only, without printing or copying live values; never copy live values into fixtures. If the shapes differ, update the fixtures with made-up values and the script, then re-run `uv run pytest tests/skills/test_clickup_claim.py -v`, `make sync-dev`, `make verify-sync` and `make lint`.

Acceptance criteria:
- `./artifacts/t16-clickup-smoke.md` records either both runs' status fields (first `assigned` with `rule: github_link`, second `already_assigned`), the test task ID and whether the live key paths matched the fixtures, or "pending" with the reason (variables not exported, or no test task). The token and workspace values appear nowhere in it.
- If the script or fixtures changed: `uv run pytest tests/skills/test_clickup_claim.py -v` passes and `make verify-sync` and `make lint` exit 0, with outputs saved under `./artifacts/t16-*.log`.
- `git add .dev/tasks` has been run after writing the artifact.

AC ids: T16.AC1 = first acceptance bullet (artifact records both runs' status fields or "pending" with the reason; no token or workspace value in it); T16.AC2 = second bullet (only if the script or fixtures changed; they did not); T16.AC3 = third bullet (`git add .dev/tasks` run after writing the artifact).

Coordinator constraint C3 (binding; overrides the plan text; recorded in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/coordinator-constraints.md): /sc:implement cannot ask the user mid-run and the CLICKUP_* variables are not set in this environment, so the ClickUp smoke claim is recorded as pending with the reason and listed in Task 17's post-restart runbook. The plan's "Ask the user ... for the test issue URL and task ID" step is replaced by that record. Round-2 minor F-04 is not applied (no live comparison happens in this run).
Presence check used (prints no value): for each of CLICKUP_API_TOKEN, CLICKUP_WORKSPACE_ID, CLICKUP_LIST_IDS, CLICKUP_MAX_PAGES, `test -n "${VAR:-}"`; at 2026-11-04T14:05:14Z all four were not set.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 1f31901043bb550325a7e5270f34565aaf4a137e
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t16-clickup-smoke.md b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t16-clickup-smoke.md
new file mode 100644
index 00000000..ac9585ae
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t16-clickup-smoke.md
@@ -0,0 +1,23 @@
+# Task 16: ClickUp smoke claim against a test task
+
+Result: **pending**. The script was not run against ClickUp in this run, and no ClickUp request was made.
+
+| Item | Value |
+|---|---|
+| First run status | pending (not run) |
+| Second run status | pending (not run) |
+| Test task ID | not supplied |
+| Live key paths matched the fixtures | not checked |
+| Script or fixtures changed | no |
+
+## Why pending
+
+1. The environment has none of the ClickUp variables. Checked at 2026-11-04T14:05:14Z with presence tests that print no value (`test -n "${VAR:-}"`): `CLICKUP_API_TOKEN` not set, `CLICKUP_WORKSPACE_ID` not set, `CLICKUP_LIST_IDS` not set, `CLICKUP_MAX_PAGES` not set.
+2. No test GitHub issue URL or ClickUp test task ID was supplied before the run.
+3. Coordinator constraint C3 (`./coordinator-constraints.md`): `/sc:implement` cannot ask the user mid-run, so the plan's "ask the user for the test issue URL and task ID" step is replaced by this pending record and runbook step 3 in `./t17-acceptance.md`.
+
+No token or workspace value appears in this file.
+
+## What covers the script today
+
+`tests/skills/test_clickup_claim.py` (Task 2) pins every outcome with patched `urllib` and recorded response shapes (made-up values): see `./t2-pytest.log`.

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
