7260014dfc131f97cdcc90be88ef72b2819976f3
Review one task for spec compliance.

Task brief: ## Task 11: Document picker-ID pinning in the developer guide

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (source section 15 row, section 6):
- Section 4.1 "Anatomy of an Agent File": state that the optional `model:` field takes an alias, a full model ID or picker ID (for example `claude-gw-tier3`), or `inherit`; that the Agent call's `model` parameter accepts aliases only and overrides the frontmatter; so a skill that needs a pinned tier spawns the agent by `subagent_type` and must not pass `model`.
- Section 4.3 "Agent Spec Format (Dynamic Instantiation)": add one line saying the `<model>` in agent specs is an alias.

Acceptance criteria:
- Section 4.1 of the developer guide contains the picker-ID sentence and the "must not pass `model`" rule; section 4.3 contains the alias line.
- `git diff -U0 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` shows hunks only between the `### 4.1` heading and the `### 4.4` heading.

AC ids: T11.AC1 = first acceptance bullet (section 4.1 picker-ID sentence and "must not pass `model`" rule; section 4.3 alias line); T11.AC2 = second bullet (hunks only between the ### 4.1 and ### 4.4 headings). Diff saved at .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t11-devguide-diff.txt.
Design source: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md section 6 (pinning facts, lines 122-135) and section 15 (developer guide row).

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 7260014dfc131f97cdcc90be88ef72b2819976f3
Diff against the start snapshot: diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index 8bb6a990..b0f8784d 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -408,6 +408,8 @@ maxTurns: 10                   # Maximum conversation turns
 permissionMode: restricted     # Permission level
 ```
 
+The optional `model:` field takes an alias (`sonnet`, `opus`, `haiku`, `fable`), a full model ID or picker ID (for example `claude-gw-tier3`), or `inherit`. The Agent call's `model` parameter accepts aliases only and overrides the frontmatter. So a skill that needs a pinned tier spawns the agent by `subagent_type` and must not pass `model`.
+
 **Markdown Body** (standard sections):
 
 | Section | Purpose | Required |
@@ -468,6 +470,8 @@ Skills can dynamically create agents using the agent spec mini-language:
 <model>[:persona[:"instruction"]]
 ```
 
+The `<model>` in an agent spec is an alias (for example `opus`, `sonnet` or `haiku`), not a full model ID or picker ID.
+
 **Examples**:
 
 | Spec | Meaning |
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t11-devguide-diff.txt b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t11-devguide-diff.txt
new file mode 100644
index 00000000..eb4f8c08
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t11-devguide-diff.txt
@@ -0,0 +1,16 @@
+$ grep -n '^### 4\.' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+388:### 4.1 Anatomy of an Agent File
+428:### 4.2 Agent Patterns
+465:### 4.3 Agent Spec Format (Dynamic Instantiation)
+486:### 4.4 Agent Activation Methods
+$ git diff -U0 -- docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+index 8bb6a990..b0f8784d 100644
+--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
++++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+@@ -410,0 +411,2 @@ permissionMode: restricted     # Permission level
++The optional `model:` field takes an alias (`sonnet`, `opus`, `haiku`, `fable`), a full model ID or picker ID (for example `claude-gw-tier3`), or `inherit`. The Agent call's `model` parameter accepts aliases only and overrides the frontmatter. So a skill that needs a pinned tier spawns the agent by `subagent_type` and must not pass `model`.
++
+@@ -470,0 +473,2 @@ Skills can dynamically create agents using the agent spec mini-language:
++The `<model>` in an agent spec is an alias (for example `opus`, `sonnet` or `haiku`), not a full model ID or picker ID.
++

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
