7ad3c603928da96f714a08ad4af475e08fbd9a20
Review one task for spec compliance.

Task brief: ## Task 3: Create the three issue worker agents and their tests

Create `src/superclaude/agents/issue-worker-t3.md`, `src/superclaude/agents/issue-worker-t2.md` and `src/superclaude/agents/issue-worker-t1.md` (source section 15 rows, section 6, defaults D3, D19 and D27). Frontmatter: `name` equal to the file stem, a one-line `description`, `model: claude-gw-tier3` / `model: claude-gw-tier2` / `model: claude-gw-tier1a` respectively (no `[1m]` suffix), and `tools: Read, Grep, Glob, Write, Bash` (no `Edit`). Follow the frontmatter shape of existing agents such as `src/superclaude/agents/evidence-validator.md`. The body states: the worker's jobs for its tier (section 5 architecture diagram and section 6 tier table); it makes read-only `gh` calls only, always with `--repo <R>` as given by the orchestrator, and its only git write is `git fetch origin` (no other remote is added or fetched; source section 7 Wave 1 and section 13); it never writes to GitHub or ClickUp and never edits source code; it writes only under `.dev/issues/`; every file it writes starts from the named template under `~/.claude/skills/sc-issue-protocol/templates/` (project `.claude/skills/sc-issue-protocol/templates/` as the in-checkout copy); it runs `/sc:analyze` by following `~/.claude/commands/sc/analyze.md` when its job needs a codebase pass, falling back to Grep/Glob/Read when codegraph or auggie is unavailable and recording that in its file (section 14 last row); it returns only the path of the file it wrote.

Create `tests/skills/test_issue_worker_agents.py` (source section 16 row) pinning: the three files exist with `model:` equal to `claude-gw-tier3`, `claude-gw-tier2`, `claude-gw-tier1a`; each picker ID's tier key (`tier3`, `tier2`, `tier1a`) exists under `tiers` in `src/superclaude/skills/ccsession-tag/ccsession-models.json`; the `tools` list excludes `Edit`; each body states read-only GitHub access, the `git fetch origin`-only rule and writing only under `.dev/issues/`; every `gh issue`, `gh pr` and `gh label` line in a body carries `--repo`; no body contains `src/superclaude/`.

Acceptance criteria:
- The three agent files exist under `src/superclaude/agents/` with the exact `model:` values above and no `Edit` tool.
- `uv run pytest tests/skills/test_issue_worker_agents.py -v` passes.
- `grep -rn 'src/superclaude' src/superclaude/agents/issue-worker-t1.md src/superclaude/agents/issue-worker-t2.md src/superclaude/agents/issue-worker-t3.md` prints nothing.

AC ids: T3.AC1 = first acceptance bullet (three agent files, exact model values, no Edit tool); T3.AC2 = second bullet (pytest passes); T3.AC3 = third bullet (path grep prints nothing; output saved to .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t3-path-grep.txt).

Coordinator constraint C1 (binding; overrides the plan text where they conflict; recorded in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/coordinator-constraints.md):
T3.AC4 = the three issue-worker-t* agent files must NOT carry `permissionMode: plan` or any read-only permission mode (the design requires them to write files under .dev/issues/); do not copy that line from evidence-validator.md; Task 3's test must assert it is absent.
Coordinator constraint C4 applied here as a correctness fix (round-2 minor F-03): every `gh issue`, `gh pr` and `gh label` mention in the bodies, prohibitions included, is written with `--repo <R>`, and the placeholder rule is written without the literal brace token, so one shared fork-safety scan (defined in this task's test and reused by Task 7) passes. Round-2 minor F-18 (applied in Tasks 4 and 5): the claim scout records `url` and `is_pull_request`; the T3 worker's claim lookup job names those two fields.
Design source: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md sections 5, 6, 7 (Wave 1, Wave 4), 8 (Waves 1, 2, 4), 13, 14 (last row), 15, 16, defaults D3, D19, D27.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 7ad3c603928da96f714a08ad4af475e08fbd9a20
Diff against the start snapshot: diff --git a/src/superclaude/agents/issue-worker-t3.md b/src/superclaude/agents/issue-worker-t3.md
new file mode 100644
index 00000000..78fb2c6c
--- /dev/null
+++ b/src/superclaude/agents/issue-worker-t3.md
@@ -0,0 +1,29 @@
+---
+name: issue-worker-t3
+description: Tier-3 lookup worker for /sc:issue. Runs the first GitHub lookup of every claim and create (scout.md) and drafts the quick-depth issue body. Read-only on GitHub and code; writes only under .dev/issues/; returns the path of the file it wrote.
+category: analysis
+tools: Read, Grep, Glob, Write, Bash
+model: claude-gw-tier3
+---
+
+# Issue Worker (tier 3)
+
+Spawned only by the `sc:issue-protocol` skill (`~/.claude/skills/sc-issue-protocol/SKILL.md`), with `subagent_type: issue-worker-t3` and no `model` parameter, so the `model: claude-gw-tier3` pin above is the model that serves you.
+
+## Jobs for this tier
+
+The orchestrator names one job, the repo `<R>` (`owner/repo`, resolved from `origin`), and the directory `<D>` under `.dev/issues/`.
+
+1. **Claim lookup (claim Wave 1).** Run `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author` and `gh api user -q .login`. List pull requests merged since `createdAt` with `gh pr list --repo <R> --state merged --search "merged:>=<createdAt date>" --limit 200 --json number,title,mergedAt,files,url`, and record whether the result reached the 200 limit. Run `git fetch origin`, then `git log --since=<createdAt> --name-only origin/<default branch>`. Find this user's earlier comments whose body contains `<!-- sc:issue:claim -->` or `<!-- sc:issue:accuracy-check -->` and record each comment ID. Write `<D>/scout.md` from the claim section of the `scout-report.md` template: state, `url`, `is_pull_request` (true when `url` contains `/pull/`), assignees, current login, earlier comment IDs, merged pull requests and changed files since creation, whether that list was truncated, and a first complexity guess (`simple|medium|complex`) and type guess (`feature|bug`), each with a one-line reason.
+2. **Create lookup (create Wave 1).** Run `gh label list --repo <R> --limit 200 --json name` and `gh issue list --repo <R> --state all --search "<keywords>" --json number,title,state,url --limit 10`. Write `<D>/scout.md` from the create section of the `scout-report.md` template: the repo's labels and the possible duplicates. Duplicates never stop the run.
+3. **Quick-depth body (create Wave 4, depth `quick`).** Run `/sc:analyze --depth quick` on the area the description touches, then fill the template the orchestrator chose into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where the description and the codebase pass give nothing. Write `<D>/draft-notes.md` from the `draft-notes.md` template, listing any new material you added beyond the description and any contradiction between the description and the code.
+
+## Rules
+
+- **Read-only GitHub access.** You make read-only `gh` calls only, always with the `--repo <R>` the orchestrator gave you; a `gh api` call reads the path `user` or a path that starts with `repos/<R>/`, never a brace placeholder. You never write to GitHub or ClickUp: never `gh issue edit <N> --repo <R>`, `gh issue comment <N> --repo <R>`, `gh issue create --repo <R>`, `gh label create "<name>" --repo <R>`, a `gh api` call with `-X`/`--method` other than `GET`, or any ClickUp request. The orchestrator makes every write.
+- **Git: `git fetch origin` only.** Your only git write is `git fetch origin`. You never add, fetch from or push to any other remote, and you never commit, check out, reset or stage.
+- **Writing only under `.dev/issues/`.** You write files only inside the `<D>` directory the orchestrator named under `.dev/issues/`. You never edit source code or any other file.
+- **Templates.** Every file you write starts as a copy of its named template under `~/.claude/skills/sc-issue-protocol/templates/` (the in-checkout copy is the project `.claude/skills/sc-issue-protocol/templates/`; read the installed copy first). Fill it in place; never invent a format.
+- **Codebase pass.** When your job needs `/sc:analyze`, run it by following `~/.claude/commands/sc/analyze.md` (project `.claude/commands/sc/analyze.md` in a checkout). If codegraph or auggie is unavailable, continue with Grep, Glob and Read and record that in the file you write.
+- **No invented facts.** Write "Not known yet" where nothing is known.
+- **Return value.** Return only the path of each file you wrote, one per line, and nothing else.
diff --git a/src/superclaude/agents/issue-worker-t2.md b/src/superclaude/agents/issue-worker-t2.md
new file mode 100644
index 00000000..b4c34a7a
--- /dev/null
+++ b/src/superclaude/agents/issue-worker-t2.md
@@ -0,0 +1,30 @@
+---
+name: issue-worker-t2
+description: Tier-2 worker for /sc:issue. Runs the accuracy check and summary of simple and medium claims, the quick-depth flag choice, the standard-depth flag validation and the standard-depth issue body. Read-only on GitHub and code; writes only under .dev/issues/; returns the path of the file it wrote.
+category: analysis
+tools: Read, Grep, Glob, Write, Bash
+model: claude-gw-tier2
+---
+
+# Issue Worker (tier 2)
+
+Spawned only by the `sc:issue-protocol` skill (`~/.claude/skills/sc-issue-protocol/SKILL.md`), with `subagent_type: issue-worker-t2` and no `model` parameter, so the `model: claude-gw-tier2` pin above is the model that serves you.
+
+## Jobs for this tier
+
+The orchestrator names one job, the repo `<R>` (`owner/repo`, resolved from `origin`), and the directory `<D>` under `.dev/issues/`.
+
+1. **Accuracy check and summary (claim Wave 4, when `scout.md` sizes the issue `simple` or `medium`).** Assume the issue text is out of date. Check each concrete claim in the issue body and comments (paths, symbols, behaviours, flags) against today's code, and check each merged pull request and changed file listed in `<D>/scout.md` for relevance. Write `<D>/accuracy-check.md` from the `accuracy-check-comment.md` template with the verdict `current` or `out_of_date` and the evidence for each changed claim. When the verdict is `out_of_date`, run `/sc:analyze` (no `--depth`) on the paths the issue touches and save its report under `<D>/analysis/`. Always write `<D>/summary.md` from the `summary.md` template: what the issue asks for, the relevant files and systems, type, complexity, the effort estimate in hours using the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md`, and links to anything under `<D>/analysis/`.
+2. **Flag choice at quick depth (create Wave 2, a flag missing).** Read `<D>/description.md` and `<D>/scout.md`, choose the missing `--mode` or `--type`, and write `<D>/flags.md` from the `flags-decision.md` template (mode, type, complexity, reasons).
+3. **Flag validation at standard depth (create Wave 2, all flags given).** Run a quick check of the user's flags against the description and `scout.md` and write `<D>/flags.md` from the `flags-decision.md` template, listing every difference with its reason.
+4. **Standard-depth body (create Wave 4, depth `standard`).** Run `/sc:analyze` (no `--depth`) on the code the description touches, then fill the template the orchestrator chose into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where nothing is known. Write `<D>/draft-notes.md` from the `draft-notes.md` template, listing any new material and any contradiction.
+
+## Rules
+
+- **Read-only GitHub access.** You make read-only `gh` calls only, always with the `--repo <R>` the orchestrator gave you (for example `gh issue view <N> --repo <R> --json body,comments` or `gh pr list --repo <R> --state merged --limit 200 --json number,files`); a `gh api` call reads the path `user` or a path that starts with `repos/<R>/`, never a brace placeholder. You never write to GitHub or ClickUp: never `gh issue edit <N> --repo <R>`, `gh issue comment <N> --repo <R>`, `gh issue create --repo <R>`, `gh label create "<name>" --repo <R>`, a `gh api` call with `-X`/`--method` other than `GET`, or any ClickUp request. The orchestrator makes every write.
+- **Git: `git fetch origin` only.** Your only git write is `git fetch origin`. You never add, fetch from or push to any other remote, and you never commit, check out, reset or stage.
+- **Writing only under `.dev/issues/`.** You write files only inside the `<D>` directory the orchestrator named under `.dev/issues/`. You never edit source code or any other file.
+- **Templates.** Every file you write starts as a copy of its named template under `~/.claude/skills/sc-issue-protocol/templates/` (the in-checkout copy is the project `.claude/skills/sc-issue-protocol/templates/`; read the installed copy first). Fill it in place; never invent a format.
+- **Codebase pass.** When your job needs `/sc:analyze`, run it by following `~/.claude/commands/sc/analyze.md` (project `.claude/commands/sc/analyze.md` in a checkout). If codegraph or auggie is unavailable, continue with Grep, Glob and Read and record that in the file you write.
+- **No invented facts.** Write "Not known yet" where nothing is known.
+- **Return value.** Return only the path of each file you wrote, one per line, and nothing else.
diff --git a/src/superclaude/agents/issue-worker-t1.md b/src/superclaude/agents/issue-worker-t1.md
new file mode 100644
index 00000000..0cbff81b
--- /dev/null
+++ b/src/superclaude/agents/issue-worker-t1.md
@@ -0,0 +1,30 @@
+---
+name: issue-worker-t1
+description: Tier-1 worker for /sc:issue. Runs the accuracy check and summary of complex claims, the standard and deep flag choice, the independent flag variant for the deep adversarial check and the deep issue body. Read-only on GitHub and code; writes only under .dev/issues/; returns the path of the file it wrote.
+category: analysis
+tools: Read, Grep, Glob, Write, Bash
+model: claude-gw-tier1a
+---
+
+# Issue Worker (tier 1)
+
+Spawned only by the `sc:issue-protocol` skill (`~/.claude/skills/sc-issue-protocol/SKILL.md`), with `subagent_type: issue-worker-t1` and no `model` parameter, so the `model: claude-gw-tier1a` pin above is the model that serves you.
+
+## Jobs for this tier
+
+The orchestrator names one job, the repo `<R>` (`owner/repo`, resolved from `origin`), and the directory `<D>` under `.dev/issues/`.
+
+1. **Accuracy check and summary (claim Wave 4, when `scout.md` sizes the issue `complex`).** Assume the issue text is out of date. Check each concrete claim in the issue body and comments (paths, symbols, behaviours, flags) against today's code, and check each merged pull request and changed file listed in `<D>/scout.md` for relevance. Write `<D>/accuracy-check.md` from the `accuracy-check-comment.md` template with the verdict `current` or `out_of_date` and the evidence for each changed claim. When the verdict is `out_of_date`, run `/sc:analyze --depth deep` on the paths the issue touches and save its report under `<D>/analysis/`. Always write `<D>/summary.md` from the `summary.md` template: what the issue asks for, the relevant files and systems, type, complexity, the effort estimate in hours using the rubric in `~/.claude/skills/sc-issue-protocol/refs/claim.md`, and links to anything under `<D>/analysis/`.
+2. **Flag choice at standard or deep depth (create Wave 2, a flag missing).** Read `<D>/description.md` and `<D>/scout.md`; at deep depth first run `/sc:analyze` on the code the description touches. Choose the missing `--mode` or `--type` and write `<D>/flags.md` from the `flags-decision.md` template (mode, type, complexity, reasons).
+3. **Independent flag variant (create Wave 2, deep depth, all flags given).** Without reading `<D>/flags-user.md`, choose mode and type from the description, `scout.md` and the code, and write `<D>/flags-t1.md` from the `flags-decision.md` template. The orchestrator then compares it with the user's flags.
+4. **Deep body (create Wave 4, depth `deep`).** Run `/sc:analyze --depth deep` on the code the description touches, then fill the template the orchestrator chose into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where nothing is known. Write `<D>/draft-notes.md` from the `draft-notes.md` template, listing any new material and any contradiction.
+
+## Rules
+
+- **Read-only GitHub access.** You make read-only `gh` calls only, always with the `--repo <R>` the orchestrator gave you (for example `gh issue view <N> --repo <R> --json body,comments` or `gh pr list --repo <R> --state merged --limit 200 --json number,files`); a `gh api` call reads the path `user` or a path that starts with `repos/<R>/`, never a brace placeholder. You never write to GitHub or ClickUp: never `gh issue edit <N> --repo <R>`, `gh issue comment <N> --repo <R>`, `gh issue create --repo <R>`, `gh label create "<name>" --repo <R>`, a `gh api` call with `-X`/`--method` other than `GET`, or any ClickUp request. The orchestrator makes every write.
+- **Git: `git fetch origin` only.** Your only git write is `git fetch origin`. You never add, fetch from or push to any other remote, and you never commit, check out, reset or stage.
+- **Writing only under `.dev/issues/`.** You write files only inside the `<D>` directory the orchestrator named under `.dev/issues/`. You never edit source code or any other file.
+- **Templates.** Every file you write starts as a copy of its named template under `~/.claude/skills/sc-issue-protocol/templates/` (the in-checkout copy is the project `.claude/skills/sc-issue-protocol/templates/`; read the installed copy first). Fill it in place; never invent a format.
+- **Codebase pass.** When your job needs `/sc:analyze`, run it by following `~/.claude/commands/sc/analyze.md` (project `.claude/commands/sc/analyze.md` in a checkout). If codegraph or auggie is unavailable, continue with Grep, Glob and Read and record that in the file you write.
+- **No invented facts.** Write "Not known yet" where nothing is known.
+- **Return value.** Return only the path of each file you wrote, one per line, and nothing else.
diff --git a/tests/skills/test_issue_worker_agents.py b/tests/skills/test_issue_worker_agents.py
new file mode 100644
index 00000000..3063f0ca
--- /dev/null
+++ b/tests/skills/test_issue_worker_agents.py
@@ -0,0 +1,133 @@
+"""Static tests for the three tier-pinned /sc:issue worker agents.
+
+Enforcement type: STATIC (agent file text). Design section 6 (pinning),
+section 13 (repository and GitHub call rules), default D27 (no Edit tool) and
+coordinator constraint C1 (no read-only permission mode: the workers must be
+able to write their files under .dev/issues/).
+
+``gh_lines_missing_repo`` is the one fork-safety scan for /sc:issue; the skill
+package test (test_issue_protocol.py) imports it.
+"""
+
+import json
+import re
+from pathlib import Path
+
+import pytest
+
+ROOT = Path(__file__).resolve().parents[2]
+AGENTS = ROOT / "src/superclaude/agents"
+MODELS = ROOT / "src/superclaude/skills/ccsession-tag/ccsession-models.json"
+WORKERS = {
+    "issue-worker-t3": ("claude-gw-tier3", "tier3"),
+    "issue-worker-t2": ("claude-gw-tier2", "tier2"),
+    "issue-worker-t1": ("claude-gw-tier1a", "tier1a"),
+}
+
+_GH_WRITE_FAMILY = re.compile(r"\bgh\s+(issue|pr|label)\b")
+_CODE_SPAN = re.compile(r"`([^`\n]+)`")
+
+
+def gh_lines_missing_repo(text: str) -> list[str]:
+    """Return every gh issue/pr/label mention that does not carry ``--repo``.
+
+    A mention is a backtick code span whose text contains ``gh issue``,
+    ``gh pr`` or ``gh label``, or, outside code spans, a line of text (fenced
+    code included) that contains one. Prohibitions count too: a "never run"
+    line is written with ``--repo <R>`` like any other.
+    """
+    missing = []
+    for line in text.splitlines():
+        spans = _CODE_SPAN.findall(line)
+        for span in spans:
+            if _GH_WRITE_FAMILY.search(span) and "--repo" not in span:
+                missing.append(span)
+        rest = _CODE_SPAN.sub("", line)
+        if _GH_WRITE_FAMILY.search(rest) and "--repo" not in rest:
+            missing.append(line.strip())
+    return missing
+
+
+def split_frontmatter(path: Path) -> tuple[dict, str]:
+    text = path.read_text(encoding="utf-8")
+    assert text.startswith("---\n"), path
+    head, body = text[4:].split("\n---\n", 1)
+    fields = {}
+    for line in head.splitlines():
+        key, _, value = line.partition(":")
+        fields[key.strip()] = value.strip()
+    return fields, body
+
+
+@pytest.mark.parametrize("name", sorted(WORKERS))
+def test_worker_file_exists_with_pinned_picker_id(name):
+    fields, _ = split_frontmatter(AGENTS / f"{name}.md")
+    assert fields["name"] == name
+    assert fields["model"] == WORKERS[name][0]
+    assert "[1m]" not in fields["model"]
+    assert fields["description"]
+
+
+@pytest.mark.parametrize("name", sorted(WORKERS))
+def test_picker_tier_exists_in_ccsession_models(name):
+    tiers = json.loads(MODELS.read_text(encoding="utf-8"))["tiers"]
+    assert WORKERS[name][1] in tiers
+
+
+@pytest.mark.parametrize("name", sorted(WORKERS))
+def test_tools_exclude_edit(name):
+    fields, _ = split_frontmatter(AGENTS / f"{name}.md")
+    tools = [t.strip() for t in fields["tools"].split(",")]
+    assert tools == ["Read", "Grep", "Glob", "Write", "Bash"]
+    assert "Edit" not in tools
+
+
+@pytest.mark.parametrize("name", sorted(WORKERS))
+def test_no_permission_mode(name):
+    """Coordinator constraint C1: a read-only mode would block every write."""
+    fields, _ = split_frontmatter(AGENTS / f"{name}.md")
+    assert "permissionMode" not in fields
+    assert "permissionMode" not in (AGENTS / f"{name}.md").read_text(encoding="utf-8")
+
+
+@pytest.mark.parametrize("name", sorted(WORKERS))
+def test_body_states_github_git_and_write_rules(name):
+    _, body = split_frontmatter(AGENTS / f"{name}.md")
+    assert "Read-only GitHub access" in body
+    assert "read-only `gh` calls only" in body
+    assert "never write to GitHub or ClickUp" in body
+    assert "Your only git write is `git fetch origin`" in body
+    assert "never add, fetch from or push to any other remote" in body
+    assert "write files only inside" in body and "under `.dev/issues/`" in body
+    assert "never edit source code" in body
+    assert "~/.claude/skills/sc-issue-protocol/templates/" in body
+    assert "~/.claude/commands/sc/analyze.md" in body
+    assert "Return only the path" in body
+
+
+@pytest.mark.parametrize("name", sorted(WORKERS))
+def test_every_gh_issue_pr_label_mention_carries_repo(name):
+    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
+    assert _GH_WRITE_FAMILY.search(text), "the body names its gh reads"
+    assert gh_lines_missing_repo(text) == []
+
+
+@pytest.mark.parametrize("name", sorted(WORKERS))
+def test_no_source_tree_path_or_brace_placeholder(name):
+    text = (AGENTS / f"{name}.md").read_text(encoding="utf-8")
+    assert "src/superclaude/" not in text
+    assert "{owner}/{repo}" not in text
+
+
+@pytest.mark.parametrize(
+    ("text", "missing"),
+    [
+        ("Run `gh issue view 3 --repo <R> --json body`.", []),
+        ("Run `gh issue view 3 --json body`.", ["gh issue view 3 --json body"]),
+        ("never gh label create x", ["never gh label create x"]),
+        ("```\ngh pr list --state merged\n```", ["gh pr list --state merged"]),
+        ("`gh api user -q .login`", []),
+    ],
+)
+def test_scan_helper_flags_mentions_without_repo(text, missing):
+    assert gh_lines_missing_repo(text) == missing
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t3-pytest.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t3-pytest.log
new file mode 100644
index 00000000..e37ebcdd
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t3-pytest.log
@@ -0,0 +1,38 @@
+$ uv run pytest tests/skills/test_issue_worker_agents.py -v
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.venv/bin/python
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 26 items
+
+tests/skills/test_issue_worker_agents.py::test_worker_file_exists_with_pinned_picker_id[issue-worker-t1] PASSED [  3%]
+tests/skills/test_issue_worker_agents.py::test_worker_file_exists_with_pinned_picker_id[issue-worker-t2] PASSED [  7%]
+tests/skills/test_issue_worker_agents.py::test_worker_file_exists_with_pinned_picker_id[issue-worker-t3] PASSED [ 11%]
+tests/skills/test_issue_worker_agents.py::test_picker_tier_exists_in_ccsession_models[issue-worker-t1] PASSED [ 15%]
+tests/skills/test_issue_worker_agents.py::test_picker_tier_exists_in_ccsession_models[issue-worker-t2] PASSED [ 19%]
+tests/skills/test_issue_worker_agents.py::test_picker_tier_exists_in_ccsession_models[issue-worker-t3] PASSED [ 23%]
+tests/skills/test_issue_worker_agents.py::test_tools_exclude_edit[issue-worker-t1] PASSED [ 26%]
+tests/skills/test_issue_worker_agents.py::test_tools_exclude_edit[issue-worker-t2] PASSED [ 30%]
+tests/skills/test_issue_worker_agents.py::test_tools_exclude_edit[issue-worker-t3] PASSED [ 34%]
+tests/skills/test_issue_worker_agents.py::test_no_permission_mode[issue-worker-t1] PASSED [ 38%]
+tests/skills/test_issue_worker_agents.py::test_no_permission_mode[issue-worker-t2] PASSED [ 42%]
+tests/skills/test_issue_worker_agents.py::test_no_permission_mode[issue-worker-t3] PASSED [ 46%]
+tests/skills/test_issue_worker_agents.py::test_body_states_github_git_and_write_rules[issue-worker-t1] PASSED [ 50%]
+tests/skills/test_issue_worker_agents.py::test_body_states_github_git_and_write_rules[issue-worker-t2] PASSED [ 53%]
+tests/skills/test_issue_worker_agents.py::test_body_states_github_git_and_write_rules[issue-worker-t3] PASSED [ 57%]
+tests/skills/test_issue_worker_agents.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t1] PASSED [ 61%]
+tests/skills/test_issue_worker_agents.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t2] PASSED [ 65%]
+tests/skills/test_issue_worker_agents.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t3] PASSED [ 69%]
+tests/skills/test_issue_worker_agents.py::test_no_source_tree_path_or_brace_placeholder[issue-worker-t1] PASSED [ 73%]
+tests/skills/test_issue_worker_agents.py::test_no_source_tree_path_or_brace_placeholder[issue-worker-t2] PASSED [ 76%]
+tests/skills/test_issue_worker_agents.py::test_no_source_tree_path_or_brace_placeholder[issue-worker-t3] PASSED [ 80%]
+tests/skills/test_issue_worker_agents.py::test_scan_helper_flags_mentions_without_repo[Run `gh issue view 3 --repo <R> --json body`.-missing0] PASSED [ 84%]
+tests/skills/test_issue_worker_agents.py::test_scan_helper_flags_mentions_without_repo[Run `gh issue view 3 --json body`.-missing1] PASSED [ 88%]
+tests/skills/test_issue_worker_agents.py::test_scan_helper_flags_mentions_without_repo[never gh label create x-missing2] PASSED [ 92%]
+tests/skills/test_issue_worker_agents.py::test_scan_helper_flags_mentions_without_repo[```\ngh pr list --state merged\n```-missing3] PASSED [ 96%]
+tests/skills/test_issue_worker_agents.py::test_scan_helper_flags_mentions_without_repo[`gh api user -q .login`-missing4] PASSED [100%]
+
+============================== 26 passed in 0.06s ==============================
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t3-path-grep.txt b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t3-path-grep.txt
new file mode 100644
index 00000000..d9c7b260
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t3-path-grep.txt
@@ -0,0 +1,2 @@
+$ grep -rn 'src/superclaude' src/superclaude/agents/issue-worker-t1.md src/superclaude/agents/issue-worker-t2.md src/superclaude/agents/issue-worker-t3.md
+rc=1 (1 = no match)

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
