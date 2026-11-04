9c9c70b58911b110e414f5c2d696e67cfaf63669
Review one task for spec compliance.

Task brief: ## Task 8: Create the /sc:issue command file and its test

Depends on: Task 6

Create `src/superclaude/commands/issue.md` (source section 4 and the `issue.md` row of section 15), about 100 to 150 lines: frontmatter `name: issue`, a one-line `description`, `category: workflow`, `complexity: advanced`, `mcp-servers: [auggie, codegraph]`, `personas: [analyzer]`, `argument-hint`; Usage block (the two lines of section 4); Options table listing exactly `--claim`, `--create`, `--depth`, `--mode`, `--type` with the defaults and allowed values of section 4 (`--depth quick|standard|deep`, `--mode feature|bug`, `--type cicd|command|skill|agent|hook|cli|core|docs|tests|install|other`); STOP rules before Activation (exactly one of `--claim` / `--create`; `--depth`/`--mode`/`--type` with `--claim` is `E-CREATE-ONLY-FLAG`; unknown values list the allowed values; empty description); the statement that there is no `--repo`, dry-run or preview flag; Examples; Boundaries; the D26 one-line rule-10 note; `## Activation` reading "Skill sc:issue-protocol" and naming `~/.claude/skills/sc-issue-protocol/SKILL.md`. Follow the shape of an existing thin command such as `src/superclaude/commands/workflow.md`.

Create `tests/commands/test_issue_command.py` (source section 16 row) pinning: the frontmatter fields above; the Options table lists exactly the five flags with the allowed values of section 4; Activation names `Skill sc:issue-protocol`; no `src/superclaude/` path; no `--repo` flag row and no `--dry-run`/`--preview` flag; the command file and `src/superclaude/skills/sc-issue-protocol/SKILL.md` each carry the D26 rule-10 line.

Acceptance criteria:
- `src/superclaude/commands/issue.md` exists with the frontmatter, Options table, STOP rules and Activation above.
- `uv run pytest tests/commands/test_issue_command.py -v` passes.

AC ids: T8.AC1 = first acceptance bullet (command file with frontmatter, Options table, STOP rules and Activation); T8.AC2 = second bullet (pytest passes). Log: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t8-pytest.log.

Coordinator constraint C4 correctness fix applied (round-2 minor F-17, recorded in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/round2-minor-findings.md): the D26 rule-10 sentence is the one fixed wording already in SKILL.md (Task 6), and the test pins that exact line in both files.
Known interim state (not caused by an error in this task): tests/recommend/test_routing_refresh.py::test_command_dispositions_trace_appendix_c_and_inventory and tests/cli/test_issue_body_templates.py::test_no_issue_skill_or_command_added fail now that issue.md exists; Task 9 updates both tests by plan.
Design source: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md sections 4, 15 (issue.md row), 16 (test_issue_command.py row), default D26.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 9c9c70b58911b110e414f5c2d696e67cfaf63669
Diff against the start snapshot: diff --git a/src/superclaude/commands/issue.md b/src/superclaude/commands/issue.md
new file mode 100644
index 00000000..44a1abbb
--- /dev/null
+++ b/src/superclaude/commands/issue.md
@@ -0,0 +1,100 @@
+---
+name: issue
+description: "Claim a GitHub issue on the origin repo (assign it, check its accuracy, write a summary and a next-step prompt, then stop) or create a templated issue with labels from a fixed set"
+category: workflow
+complexity: advanced
+mcp-servers: [auggie, codegraph]
+personas: [analyzer]
+argument-hint: "--claim <number|url> | --create \"<description>\" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]"
+---
+
+# /sc:issue: GitHub Issue Claim and Create
+
+Two modes on the repository that `origin` points at:
+
+- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then stops. It never runs the next-step commands.
+- `--create` turns a description into a GitHub issue built from one of four templates, with labels from a fixed set. GitHub only: no ClickUp task.
+
+Both modes post directly to GitHub; nothing is shown for approval first.
+
+For issues filed through `/sc:issue --create`, its four templates replace the `ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed `CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`.
+
+## Triggers
+
+Explicit only: the user types `/sc:issue --claim ...` or `/sc:issue --create ...`.
+
+## Usage
+
+```text
+/sc:issue --claim <number|url>
+/sc:issue --create "<description>" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]
+```
+
+## Options
+
+| Flag | Mode | Default | Values | Meaning |
+|---|---|---|---|---|
+| `--claim` | claim | - | issue number (`302`, `#302`) or issue URL on the origin repo | Claim this issue |
+| `--create` | create | - | free text, or `@path` to a file holding the description | Description of the feature or bug |
+| `--depth` | create | `quick` | `quick`, `standard`, `deep` | How hard the command checks the flags and fills the body |
+| `--mode` | create | chosen by a worker when omitted | `feature`, `bug` | Picks the feature or bug template and the `enhancement` / `bug` label |
+| `--type` | create | chosen by a worker when omitted | `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install`, `other` | Area of the change; maps to a `type: <value>` label |
+
+There is no repository option (the repo is always `origin`), no dry-run option and no preview option.
+
+## STOP rules (checked before Activation)
+
+- Exactly one of `--claim` / `--create` is required. Both or neither: STOP and print the Usage block.
+- `--depth`, `--mode` or `--type` together with `--claim`: STOP `E-CREATE-ONLY-FLAG` ("--depth, --mode and --type apply to --create only").
+- An unknown value for `--depth`, `--mode` or `--type`: STOP and list the allowed values from the Options table.
+- An empty `--create` description (or an `@path` file that is empty or missing): STOP ("--create needs a description").
+- An empty `--claim` argument: STOP and print the Usage block.
+
+## Examples
+
+```text
+/sc:issue --claim 302
+/sc:issue --claim https://github.com/<owner>/<repo>/issues/302
+/sc:issue --create "The sync check misses deleted skill files" --mode bug --type cli --depth standard
+/sc:issue --create @notes/new-command.md --depth deep
+```
+
+## Outputs
+
+Every file starts from a template of the skill and stays under `.dev/issues/`:
+
+| Mode | Directory | Files |
+|---|---|---|
+| claim | `.dev/issues/<N>/` | `scout.md`, `clickup.json`, `accuracy-check.md` (posted), `summary.md` (effort in hours), `analysis/` (only when the issue is out of date), `recommend.md`, `next-steps.md`, `claim-comment.md` (posted) |
+| create | `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/`, renamed to `.dev/issues/<N>/` once the issue exists | `description.md`, `scout.md`, `flags.md`, `issue-body.md` (posted), `draft-notes.md`, and `create-review.md` (posted only when a standard or deep check disagrees with your flags) |
+
+After a claim, open `.dev/issues/<N>/next-steps.md` and run its commands in your own session, in order, after the `/model` line it starts with.
+
+## Boundaries
+
+**Will:**
+- Resolve the repository from the `origin` remote only.
+- Spawn tier-pinned worker agents for every lookup, accuracy check and draft.
+- Write every artifact under `.dev/issues/` from a template.
+- On claim: assign the issue, assign the ClickUp task when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set, post or update the accuracy-check and claim comments, and stop after writing `next-steps.md`.
+- On create: apply only the labels of the fixed set that already exist in the repo, and list the rest as not applied.
+
+**Will Not:**
+- Run any next-step command (brainstorm, design, workflow, implement, troubleshoot).
+- Create labels, ClickUp tasks, or interact with any repository other than `origin`.
+- Stage or commit `.dev/issues/`.
+
+## Activation
+
+**MANDATORY**: Before executing any protocol steps, invoke:
+> Skill sc:issue-protocol
+
+Do NOT proceed with protocol execution using only this command file.
+The full behavioral specification is in `~/.claude/skills/sc-issue-protocol/SKILL.md`.
+
+## Related Commands
+
+| Command | Difference |
+|---|---|
+| `/sc:recommend` | Picks the next-step chain that a claim writes into `next-steps.md` |
+| `/sc:brainstorm`, `/sc:design`, `/sc:workflow`, `/sc:implement`, `/sc:troubleshoot` | The next-step commands a claim recommends; the user runs them |
diff --git a/tests/commands/test_issue_command.py b/tests/commands/test_issue_command.py
new file mode 100644
index 00000000..da51e291
--- /dev/null
+++ b/tests/commands/test_issue_command.py
@@ -0,0 +1,125 @@
+"""Static tests for the /sc:issue command file (design sections 4 and 16).
+
+Enforcement type: STATIC (command file text).
+"""
+
+import re
+from pathlib import Path
+
+import pytest
+
+ROOT = Path(__file__).resolve().parents[2]
+COMMAND = ROOT / "src/superclaude/commands/issue.md"
+SKILL = ROOT / "src/superclaude/skills/sc-issue-protocol/SKILL.md"
+
+# Default D26, one fixed wording shared by the command file and SKILL.md (F-17).
+RULE_10_LINE = (
+    "For issues filed through `/sc:issue --create`, its four templates replace the "
+    "`ISSUE-HANDOFF.md` / `ISSUE-BACKLOG.md` instruction of rule 10 in the distributed "
+    "`CLAUDE.md`; rule 10 itself is unchanged and still governs issues filed without `/sc:issue`."
+)
+
+ALLOWED = {
+    "--depth": ["quick", "standard", "deep"],
+    "--mode": ["feature", "bug"],
+    "--type": [
+        "cicd",
+        "command",
+        "skill",
+        "agent",
+        "hook",
+        "cli",
+        "core",
+        "docs",
+        "tests",
+        "install",
+        "other",
+    ],
+}
+
+
+def _text() -> str:
+    return COMMAND.read_text(encoding="utf-8")
+
+
+def _frontmatter() -> dict:
+    head = _text().split("\n---\n", 1)[0]
+    assert head.startswith("---\n")
+    fields = {}
+    for line in head[4:].splitlines():
+        key, _, value = line.partition(":")
+        fields[key.strip()] = value.strip()
+    return fields
+
+
+def _options_rows() -> dict[str, list[str]]:
+    section = _text().split("## Options", 1)[1].split("\n## ", 1)[0]
+    rows = {}
+    for line in section.splitlines():
+        if not line.startswith("| `--"):
+            continue
+        cells = [c.strip() for c in line.strip().strip("|").split("|")]
+        rows[cells[0].strip("`")] = cells
+    return rows
+
+
+def test_frontmatter_fields():
+    fields = _frontmatter()
+    assert fields["name"] == "issue"
+    assert fields["description"]
+    assert fields["category"] == "workflow"
+    assert fields["complexity"] == "advanced"
+    assert fields["mcp-servers"] == "[auggie, codegraph]"
+    assert fields["personas"] == "[analyzer]"
+    assert fields["argument-hint"]
+
+
+def test_options_table_lists_exactly_the_five_flags():
+    assert sorted(_options_rows()) == sorted(["--claim", "--create", "--depth", "--mode", "--type"])
+
+
+@pytest.mark.parametrize("flag", sorted(ALLOWED))
+def test_options_table_allowed_values(flag):
+    values_cell = _options_rows()[flag][3]
+    assert re.findall(r"`([a-z]+)`", values_cell) == ALLOWED[flag]
+
+
+def test_option_defaults():
+    rows = _options_rows()
+    assert rows["--depth"][2] == "`quick`"
+    assert rows["--mode"][2] == rows["--type"][2] == "chosen by a worker when omitted"
+    assert rows["--claim"][1] == "claim"
+    assert all(rows[f][1] == "create" for f in ("--create", "--depth", "--mode", "--type"))
+
+
+def test_no_repo_dry_run_or_preview_flag():
+    text = _text()
+    assert "--repo" not in _options_rows()
+    assert "--repo" not in text
+    assert "--dry-run" not in text and "--preview" not in text
+
+
+def test_stop_rules_come_before_activation():
+    text = _text()
+    stops = text.index("## STOP rules")
+    assert stops < text.index("## Activation")
+    rules = text[stops : text.index("\n## ", stops + 1)]
+    assert "Exactly one of `--claim` / `--create`" in rules
+    assert "E-CREATE-ONLY-FLAG" in rules
+    assert "allowed values" in rules
+    assert "empty `--create` description" in rules.lower()
+
+
+def test_activation_names_the_skill():
+    activation = _text().split("## Activation", 1)[1]
+    assert "> Skill sc:issue-protocol" in activation
+    assert "~/.claude/skills/sc-issue-protocol/SKILL.md" in activation
+
+
+def test_no_source_tree_path():
+    assert "src/superclaude/" not in _text()
+
+
+@pytest.mark.parametrize("path", [COMMAND, SKILL], ids=["command", "skill"])
+def test_rule_10_line_is_carried_verbatim(path):
+    assert RULE_10_LINE in path.read_text(encoding="utf-8").splitlines()
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t8-pytest.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t8-pytest.log
new file mode 100644
index 00000000..2512e892
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t8-pytest.log
@@ -0,0 +1,24 @@
+$ uv run pytest tests/commands/test_issue_command.py -v
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.venv/bin/python
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 12 items
+
+tests/commands/test_issue_command.py::test_frontmatter_fields PASSED     [  8%]
+tests/commands/test_issue_command.py::test_options_table_lists_exactly_the_five_flags PASSED [ 16%]
+tests/commands/test_issue_command.py::test_options_table_allowed_values[--depth] PASSED [ 25%]
+tests/commands/test_issue_command.py::test_options_table_allowed_values[--mode] PASSED [ 33%]
+tests/commands/test_issue_command.py::test_options_table_allowed_values[--type] PASSED [ 41%]
+tests/commands/test_issue_command.py::test_option_defaults PASSED        [ 50%]
+tests/commands/test_issue_command.py::test_no_repo_dry_run_or_preview_flag PASSED [ 58%]
+tests/commands/test_issue_command.py::test_stop_rules_come_before_activation PASSED [ 66%]
+tests/commands/test_issue_command.py::test_activation_names_the_skill PASSED [ 75%]
+tests/commands/test_issue_command.py::test_no_source_tree_path PASSED    [ 83%]
+tests/commands/test_issue_command.py::test_rule_10_line_is_carried_verbatim[command] PASSED [ 91%]
+tests/commands/test_issue_command.py::test_rule_10_line_is_carried_verbatim[skill] PASSED [100%]
+
+============================== 12 passed in 0.05s ==============================
+rc=0

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
