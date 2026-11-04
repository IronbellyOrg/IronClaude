6dd29242d4d7a33f1026c8a527fa1d431dd4fb65
Review one task for spec compliance.

Task brief: Depends on: Task 8

In `docs/user-guide/commands.md` (source section 15 row):
- Add a row to the "8. UTILITIES" table: `/sc:issue`, purpose "Claim a GitHub issue (assign, accuracy check, summary, next-step prompt) or create a templated issue", file `issue.md`, "Changes files?" = "Yes (posts to GitHub; writes `.dev/issues/`)". Link it to the new section anchor the way `/sc:graph` is linked.
- Add a `### /sc:issue - GitHub Issue Claim and Create` section under "Detailed Description of Each Command", in the same shape as the neighbouring command sections: what it does, the usage lines of source section 4, the Options table, two or three examples (`/sc:issue --claim 302`, `/sc:issue --create "..." --mode bug --type cli --depth standard`), and the facts that it posts directly to GitHub, never creates labels, assigns the ClickUp task only on claim when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set, and stops after writing `next-steps.md`.

Acceptance criteria:
- `docs/user-guide/commands.md` has the UTILITIES row and the `/sc:issue` section; the row's anchor link resolves to that section's heading.
- Every flag named in the new section exists in `src/superclaude/commands/issue.md`'s Options table.

AC ids: T12.AC1 = first acceptance bullet (UTILITIES row and /sc:issue section; the row's anchor resolves to that section's heading); T12.AC2 = second bullet (every flag named in the new section exists in src/superclaude/commands/issue.md's Options table). Check output saved at .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t12-docs-checks.txt.
Note: the heading is written with backticks around `/sc:issue`, the same as every neighbouring section heading (for example "### `/sc:graph` - Code-Graph Index Status"); GitHub drops backticks from anchors, so the anchor is the same as for the plan's backtick-free spelling (round-2 report notes this difference as cosmetic).
Design source: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md sections 4, 11, 12, 15 (docs/user-guide/commands.md row).

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 6dd29242d4d7a33f1026c8a527fa1d431dd4fb65
Diff against the start snapshot: diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index 822696b5..36bc0a75 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -112,6 +112,7 @@ This page is the per-command reference: exact syntax, options, and what each com
 | `/sc:save` | Save project memory to `.superclaude/memory/` (not a resume method) | `save.md` | Report only |
 | `/sc:help` | List installed commands, skills, process levels | `help.md` | No |
 | [`/sc:graph`](#scgraph---code-graph-index-status) | Code-graph index status; builds the index only on `init` | `graph.md` | Only with `init` |
+| [`/sc:issue`](#scissue---github-issue-claim-and-create) | Claim a GitHub issue (assign, accuracy check, summary, next-step prompt) or create a templated issue | `issue.md` | Yes (posts to GitHub; writes `.dev/issues/`) |
 | `/sc:recommend` | Paste-ready prompt for the right command | `recommend.md` | Report only (inside an IronClaude checkout it writes its cache and telemetry under `.claude/cache/`) |
 | `/sc:init-lite` | Safe audit of project-local context surfaces | `init-lite.md` | Report only |
 | `/sc:pr-submit` | Open fork PR and monitor review fixes | `pr-submit.md` | Yes |
@@ -343,6 +344,43 @@ When codegraph, the index or its lookup tools are not usable, it falls back to G
 
 ---
 
+### `/sc:issue` - GitHub Issue Claim and Create
+
+**When to use:** Take an existing GitHub issue on the repository `origin` points at, or file a new one. `--claim` assigns the issue to you, checks whether its text is still accurate against today's code and the pull requests merged since it was opened, writes a summary (with an effort estimate in hours) and a next-step prompt under `.dev/issues/<N>/`, posts an accuracy-check comment and a claim comment, then stops. `--create` turns a description into an issue built from one of four templates (feature or bug, simple or complex) with labels from a fixed set.
+
+**Syntax:**
+
+```
+/sc:issue --claim <number|url>
+/sc:issue --create "<description>" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]
+```
+
+**Options:**
+
+| Flag | Mode | Default | What it does |
+|------|------|---------|--------------|
+| `--claim <number\|url>` | claim | - | The issue to claim: a number (`302`, `#302`) or an issue URL on the origin repo |
+| `--create "<description>"` | create | - | The feature or bug description, as text or `@path` to a file |
+| `--depth quick\|standard\|deep` | create | `quick` | How hard the command checks your flags and fills the body; `deep` uses the complex template |
+| `--mode feature\|bug` | create | chosen by a worker | Picks the feature or bug template and the `enhancement` or `bug` label |
+| `--type <type>` | create | chosen by a worker | Area of the change: `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install` or `other`; maps to a `type: <value>` label |
+
+`--depth`, `--mode` and `--type` work with `--create` only. There is no repository option: the repository is always `origin`.
+
+**Examples:**
+
+```bash
+/sc:issue --claim 302
+/sc:issue --create "The sync check misses deleted skill files" --mode bug --type cli --depth standard
+/sc:issue --create @notes/new-command.md --depth deep
+```
+
+It posts directly to GitHub, without showing the comment or the issue body for approval first. It never creates labels: a label from the fixed set that the repository does not have is skipped and listed. On claim it also assigns the matching ClickUp task, only when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set; `--create` never touches ClickUp. A claim stops after writing `.dev/issues/<N>/next-steps.md`; you run those commands yourself, in your own session.
+
+**MCP servers:** auggie, codegraph
+
+---
+
 ### `/sc:load` - Project Context Loading
 
 **When to use:** Load project memory from the `.superclaude/memory/` files (project context, memories and checkpoints) at the start of a session. It is not a way to resume work: to continue a task, rerun `/task <task file>` or `/sc:implement <plan path>`, or reopen a tagged session with `ccsession <name>` (see [How We Work](how-we-work.md), section 3.12). It does not modify project structure or configuration, or override existing session context without a checkpoint.
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t12-docs-checks.txt b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t12-docs-checks.txt
new file mode 100644
index 00000000..1d162d93
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t12-docs-checks.txt
@@ -0,0 +1,5 @@
+$ anchor and flag checks for docs/user-guide/commands.md (uv run python)
+row anchor: scissue---github-issue-claim-and-create -> heading line 347
+flags in the new section: ['--claim', '--create', '--depth', '--mode', '--type']
+flags in issue.md Options table: ['--claim', '--create', '--depth', '--mode', '--type']
+section flags missing from the Options table: []

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
