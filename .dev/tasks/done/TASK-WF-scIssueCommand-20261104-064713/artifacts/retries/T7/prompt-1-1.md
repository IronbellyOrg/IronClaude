c743438dcf8acea23d231f2543aef009efb185dd
Review one task for spec compliance.

Task brief: Depends on: Task 6

Create `tests/skills/test_issue_protocol.py` (source section 16 row) pinning:
- `SKILL.md` frontmatter (`name: sc:issue-protocol`, the `allowed-tools` list) and size: fewer than 500 lines by `len(text.splitlines())`.
- Every ref, template and script named in `SKILL.md` exists, and every file in `refs/`, `templates/` and `scripts/` is named in `SKILL.md`.
- The text "never pass the `model` parameter" is present in `SKILL.md` and in every `refs/*.md` file.
- Every posted template ends with its marker (`accuracy-check-comment.md`, `claim-comment.md`, `create-review-comment.md`, and `<!-- sc:issue:create template=<stem> -->` on the four issue templates).
- The four issue templates carry the source section 10 headings in order and contain no `ClickUp` text (case-insensitive).
- Every `/sc:*` flag in `refs/chains.md` exists in the command file it names, read from `src/superclaude/commands/<name>.md` (the `_command_text` source used by `test_every_notes_flag_exists_in_its_command` in `tests/core/test_how_we_work_routing_table.py`), and `/task` is checked against `src/superclaude/skills/task/SKILL.md`. Reading only the source copies is a deliberate narrowing of source section 16's "installed-or-source" wording so the test does not depend on the machine's `~/.claude` install; say so in the test's docstring.
- `refs/chains.md` contains no `--handoff tasklist` and no `--handoff design` on a `/sc:brainstorm` step, and every `/sc:brainstorm` step passes `--models opus,sonnet`.
- Fork safety (source section 13 and section 20 item 4): every line in `SKILL.md`, `refs/*.md` and the three `src/superclaude/agents/issue-worker-t*.md` bodies that runs `gh issue`, `gh pr` or `gh label` carries `--repo`, and no file in the skill or the three agents contains the `{owner}/{repo}` placeholder.
- No text file under `src/superclaude/skills/sc-issue-protocol/` contains `src/superclaude/`; the scan skips `__pycache__/` and files that do not decode as UTF-8.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_protocol.py -v` passes.
- Deleting the marker line from a copy of `templates/claim-comment.md` in a temporary directory makes the marker test fail, and a temporary copy of a ref with a `gh issue view` line lacking `--repo` makes the fork-safety test fail (shown by parametrised negative cases or helper unit tests inside the same file).

AC ids: T7.AC1 = first acceptance bullet (pytest passes); T7.AC2 = second bullet (negative cases for the marker test and the fork-safety test inside the same file). Logs: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t7-pytest.log and t7-t1-rerun.log.

Coordinator constraint C4 correctness fixes applied here (recorded in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/round2-minor-findings.md): F-16 (the inventory covers refs/*.md, templates/*.md and scripts/*.py only, so scripts/__pycache__/ cannot fail it); F-03 (the fork-safety scan is the one shared helper `gh_lines_missing_repo` defined in tests/skills/test_issue_worker_agents.py, imported here).
Disclosed executor change outside the new test file: the brace-placeholder test scans every file of the skill, and src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py held the literal text `{owner}/{repo}` inside two Python f-strings (not a gh placeholder). The two f-strings were rewritten as `"/".join((owner, repo))` with the same output; tests/skills/test_issue_repo_resolution.py still passes (t7-t1-rerun.log). The flag check skips a command span that carries no flag (chains.md mentions the bare `/sc:issue`, whose command file is created by Task 8).
Design source: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md sections 10, 13, 16 (test_issue_protocol.py row), 19, 20 item 4.

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: c743438dcf8acea23d231f2543aef009efb185dd
Diff against the start snapshot: diff --git a/tests/skills/test_issue_protocol.py b/tests/skills/test_issue_protocol.py
new file mode 100644
index 00000000..ce940ce2
--- /dev/null
+++ b/tests/skills/test_issue_protocol.py
@@ -0,0 +1,261 @@
+"""Static tests for the sc-issue-protocol skill package (design section 16).
+
+Enforcement type: STATIC (skill package text). Pins the SKILL.md frontmatter
+and size, the two-way inventory of refs/templates/scripts, the spawn rule,
+the posted-template markers, the issue-template headings, the next-step chain
+flags and the fork-safety rule of design section 13.
+
+Flag check source: every ``/sc:*`` flag in ``refs/chains.md`` is checked only
+against the source command file ``src/superclaude/commands/<name>.md`` (and
+``/task`` against ``src/superclaude/skills/task/SKILL.md``), the same source
+``_command_text`` in tests/core/test_how_we_work_routing_table.py reads. This
+deliberately narrows design section 16's "installed-or-source" wording so the
+test never depends on the machine's ``~/.claude`` install.
+
+The fork-safety scan is the one shared helper ``gh_lines_missing_repo`` from
+test_issue_worker_agents.py.
+"""
+
+import re
+from pathlib import Path
+
+import pytest
+
+from tests.skills.test_issue_worker_agents import gh_lines_missing_repo
+
+ROOT = Path(__file__).resolve().parents[2]
+SKILL_DIR = ROOT / "src/superclaude/skills/sc-issue-protocol"
+SKILL = SKILL_DIR / "SKILL.md"
+REFS = SKILL_DIR / "refs"
+TEMPLATES = SKILL_DIR / "templates"
+COMMANDS = ROOT / "src/superclaude/commands"
+TASK_SKILL = ROOT / "src/superclaude/skills/task/SKILL.md"
+AGENTS = [ROOT / f"src/superclaude/agents/issue-worker-t{n}.md" for n in (3, 2, 1)]
+
+SPAWN_RULE = "never pass the `model` parameter"
+ALLOWED_TOOLS = "Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion"
+
+BUG_SIMPLE = [
+    "Bug Summary",
+    "Environment (OS, version)",
+    "Current Behavior",
+    "Expected Behavior",
+    "Steps to Reproduce",
+    "Impact Assessment (Severity, Blast Radius)",
+    "Error Messages",
+    "Codebase Context (from `/sc:analyze`)",
+    "Related Issues",
+    "Testing Notes",
+]
+BUG_COMPLEX = BUG_SIMPLE + [
+    "Frequency",
+    "User Impact",
+    "Business Impact",
+    "Cascading Effects",
+    "Logs and Stack Trace",
+    "Attempted Solutions",
+    "Proposed Solution",
+    "For Development Team (Root Cause Analysis, Fix Approach, Verification Plan)",
+]
+FEATURE_SIMPLE = [
+    "Feature Summary",
+    "Problem Statement",
+    "User Story",
+    "Proposed Solution",
+    "Acceptance Criteria",
+    "Out of Scope",
+    "Components Affected (from `/sc:analyze`)",
+    "Related Issues/PRs",
+]
+FEATURE_COMPLEX = FEATURE_SIMPLE + [
+    "Success Metrics",
+    "Architecture Impact",
+    "Dependencies",
+    "Testing Strategy",
+    "Documentation Needs",
+    "Alternatives Considered",
+    "Impact Analysis (Blast Radius, Integration Impact)",
+    "Risks & Mitigation",
+    "Effort Estimate (hours) and Complexity",
+]
+ISSUE_TEMPLATES = {
+    "issue-bug-simple": BUG_SIMPLE,
+    "issue-bug-complex": BUG_COMPLEX,
+    "issue-feature-simple": FEATURE_SIMPLE,
+    "issue-feature-complex": FEATURE_COMPLEX,
+}
+POSTED_MARKERS = {
+    "accuracy-check-comment": "<!-- sc:issue:accuracy-check -->",
+    "claim-comment": "<!-- sc:issue:claim -->",
+    "create-review-comment": "<!-- sc:issue:create-review -->",
+    **{stem: f"<!-- sc:issue:create template={stem} -->" for stem in ISSUE_TEMPLATES},
+}
+
+_SKILL_PATH = re.compile(r"(?:refs|templates|scripts)/[A-Za-z0-9_.-]+\.(?:md|py)")
+_COMMAND_SPAN = re.compile(r"`(/(?:sc:[a-z][a-z0-9-]*|task)\b[^`]*)`")
+_FLAG = re.compile(r"--[a-z][a-z0-9-]*")
+
+
+def _text(path: Path) -> str:
+    return path.read_text(encoding="utf-8")
+
+
+def last_nonempty_line(text: str) -> str:
+    return [line for line in text.splitlines() if line.strip()][-1].strip()
+
+
+def headings(text: str) -> list[str]:
+    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]
+
+
+def chain_rows(text: str) -> list[str]:
+    """The data rows of the chain table (one row per type and complexity)."""
+    return [line for line in text.splitlines() if re.match(r"^\| (Feature|Bug), ", line)]
+
+
+# --- SKILL.md frontmatter, size and inventory ------------------------------------
+
+
+def test_skill_frontmatter_and_size():
+    text = _text(SKILL)
+    head = text.split("\n---\n", 1)[0]
+    assert head.startswith("---\n")
+    assert "\nname: sc:issue-protocol\n" in head + "\n"
+    assert f"\nallowed-tools: {ALLOWED_TOOLS}" in head
+    assert "\ndescription: " in head
+    assert len(text.splitlines()) < 500
+
+
+def test_every_named_path_exists_and_every_file_is_named():
+    text = _text(SKILL)
+    named = set(_SKILL_PATH.findall(text))
+    on_disk = {
+        str(p.relative_to(SKILL_DIR))
+        for pattern in ("refs/*.md", "templates/*.md", "scripts/*.py")
+        for p in SKILL_DIR.glob(pattern)
+    }
+    assert on_disk, "the skill package has files"
+    assert sorted(n for n in named if not (SKILL_DIR / n).is_file()) == []
+    assert sorted(on_disk - named) == []
+
+
+@pytest.mark.parametrize("path", [SKILL, *sorted(REFS.glob("*.md"))], ids=lambda p: p.name)
+def test_spawn_rule_text_present(path):
+    assert SPAWN_RULE in _text(path)
+
+
+def test_all_five_refs_exist():
+    assert sorted(p.name for p in REFS.glob("*.md")) == [
+        "chains.md",
+        "claim.md",
+        "create.md",
+        "labels.md",
+        "tiers.md",
+    ]
+
+
+# --- templates ------------------------------------------------------------------
+
+
+@pytest.mark.parametrize(("stem", "marker"), sorted(POSTED_MARKERS.items()))
+def test_posted_template_ends_with_marker(stem, marker):
+    assert last_nonempty_line(_text(TEMPLATES / f"{stem}.md")) == marker
+
+
+def test_marker_check_fails_when_marker_is_removed(tmp_path):
+    copy = tmp_path / "claim-comment.md"
+    lines = _text(TEMPLATES / "claim-comment.md").splitlines()
+    copy.write_text("\n".join(line for line in lines if "sc:issue:claim" not in line) + "\n")
+    assert last_nonempty_line(copy.read_text()) != POSTED_MARKERS["claim-comment"]
+
+
+@pytest.mark.parametrize(("stem", "expected"), sorted(ISSUE_TEMPLATES.items()))
+def test_issue_template_headings_in_order(stem, expected):
+    assert headings(_text(TEMPLATES / f"{stem}.md")) == expected
+
+
+@pytest.mark.parametrize("stem", sorted(ISSUE_TEMPLATES))
+def test_issue_template_has_no_clickup_text(stem):
+    assert "clickup" not in _text(TEMPLATES / f"{stem}.md").lower()
+
+
+# --- next-step chains -------------------------------------------------------------
+
+
+def _command_source(token: str) -> str:
+    if token == "task":
+        return _text(TASK_SKILL)
+    return _text(COMMANDS / f"{token[3:]}.md")
+
+
+def test_every_chain_flag_exists_in_its_command():
+    spans = _COMMAND_SPAN.findall(_text(REFS / "chains.md"))
+    assert spans, "chains.md names commands in code spans"
+    missing = []
+    for span in spans:
+        flags = _FLAG.findall(span)
+        if not flags:  # a bare command name, e.g. the `/sc:issue` mention
+            continue
+        token = span[1:].split()[0]
+        source = _command_source(token)
+        missing.extend(f"{token} {flag}" for flag in flags if flag not in source)
+    assert missing == []
+
+
+def test_brainstorm_steps_have_no_handoff_and_pin_models():
+    rows = chain_rows(_text(REFS / "chains.md"))
+    assert len(rows) == 6
+    steps = [s for row in rows for s in _COMMAND_SPAN.findall(row) if s.startswith("/sc:brainstorm")]
+    assert len(steps) == 3
+    for step in steps:
+        assert "--handoff tasklist" not in step and "--handoff design" not in step
+        assert "--models opus,sonnet" in step
+    text = _text(REFS / "chains.md")
+    assert "--handoff tasklist" not in text and "--handoff design" not in text
+
+
+# --- fork safety (design section 13, section 20 item 4) ---------------------------
+
+
+_FORK_FILES = [SKILL, *sorted(REFS.glob("*.md")), *AGENTS]
+
+
+@pytest.mark.parametrize("path", _FORK_FILES, ids=lambda p: p.name)
+def test_every_gh_issue_pr_label_mention_carries_repo(path):
+    assert gh_lines_missing_repo(_text(path)) == []
+
+
+@pytest.mark.parametrize(
+    "path",
+    [*sorted(p for p in SKILL_DIR.rglob("*") if p.is_file() and "__pycache__" not in p.parts), *AGENTS],
+    ids=lambda p: p.name,
+)
+def test_no_brace_placeholder(path):
+    try:
+        text = _text(path)
+    except UnicodeDecodeError:
+        pytest.skip("not UTF-8 text")
+    assert "{owner}/{repo}" not in text
+
+
+def test_fork_safety_scan_fails_on_a_ref_without_repo(tmp_path):
+    ref = tmp_path / "claim.md"
+    ref.write_text(_text(REFS / "claim.md") + "\nRun `gh issue view 302 --json state`.\n")
+    assert gh_lines_missing_repo(ref.read_text()) == ["gh issue view 302 --json state"]
+
+
+# --- installed-path rule ------------------------------------------------------------
+
+
+def test_no_source_tree_path_in_skill_files():
+    hits = []
+    for path in sorted(SKILL_DIR.rglob("*")):
+        if not path.is_file() or "__pycache__" in path.parts:
+            continue
+        try:
+            text = path.read_text(encoding="utf-8")
+        except UnicodeDecodeError:
+            continue
+        if "src/superclaude/" in text:
+            hits.append(str(path.relative_to(ROOT)))
+    assert hits == []
diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py b/src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py
deleted file mode 100644
index b4adb69f..00000000
--- a/src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py
+++ /dev/null
@@ -1,193 +0,0 @@
-#!/usr/bin/env python3
-"""Resolve the origin GitHub repository and check a /sc:issue claim argument.
-
-Standard library only. Wave 0 of both /sc:issue modes runs this script, so the
-repository rule of the design (section 13) is tested code, not prose.
-
-Usage:
-    origin_repo.py
-        Print ``owner/repo`` parsed from ``git remote get-url origin``.
-    origin_repo.py --claim <number|#number|url>
-        Resolve origin as above, then check the claim argument against it and
-        print ``{"repo": "owner/repo", "number": N}`` as one JSON line.
-
-Only the ``origin`` remote is read. ``gh repo set-default``, gh's fork-parent
-default and every other remote are never consulted.
-
-Accepted origin URLs (a trailing ``/`` is tolerated):
-    https://github.com/<owner>/<repo>
-    https://github.com/<owner>/<repo>.git
-    git@github.com:<owner>/<repo>
-    git@github.com:<owner>/<repo>.git
-
-Claim argument rules (``check_claim``):
-    ``302`` or ``#302``                         -> N = 302
-    ``https://github.com/<origin>/issues/302``  -> N = 302; a trailing ``/``,
-                                                   a ``#fragment`` or a
-                                                   ``?query`` is ignored
-    a GitHub URL naming any other owner or      -> E-FOREIGN-REPO
-    repo, or naming no repo                        (owner and repo compare
-                                                   case-insensitively and as
-                                                   whole path segments, so
-                                                   ``IronClaudeX`` is foreign)
-    a URL (``<scheme>://...`` or               -> E-FOREIGN-REPO
-    ``git@<host>:...``) on any host other
-    than github.com
-    ``https://github.com/<origin>/pull/302``    -> E-NOT-AN-ISSUE
-    a GitHub URL on origin whose path is not    -> E-NOT-AN-ISSUE
-    ``/issues/<N>``
-    anything else (not a number, not a URL)     -> E-NOT-AN-ISSUE
-A GitHub URL may start with ``https://``, ``http://`` or no scheme, may carry
-``www.``, and may be written ``git@github.com:<owner>/<repo>/...``; every form
-is read by the same rules above. N is read only from the path segment right
-after ``/issues/``; digits in the owner or repo name never become N.
-
-Exit codes and messages (the message goes to stderr):
-    0  success
-    1  E-NO-ORIGIN     no origin remote, git failed, or origin is not GitHub
-    2  bad command-line arguments (argparse)
-    3  E-FOREIGN-REPO  the claim URL names a repository other than origin
-    4  E-NOT-AN-ISSUE  the claim argument is not an issue number or issue URL
-"""
-
-from __future__ import annotations
-
-import argparse
-import json
-import re
-import subprocess
-import sys
-
-EXIT_NO_ORIGIN = 1
-EXIT_FOREIGN_REPO = 3
-EXIT_NOT_AN_ISSUE = 4
-
-_NAME = r"[A-Za-z0-9._-]+"
-_ORIGIN_PATTERNS = (
-    re.compile(rf"^https://github\.com/(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
-    re.compile(rf"^git@github\.com:(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
-)
-_GITHUB_URL = re.compile(
-    r"^(?:(?:https?://)?(?:www\.)?github\.com/|git@github\.com:)(?P<path>[^?#]*)",
-    re.IGNORECASE,
-)
-_NUMBER = re.compile(r"^#?(?P<n>[1-9][0-9]*)$")
-
-
-class ClaimError(Exception):
-    """A claim argument that /sc:issue must STOP on."""
-
-    def __init__(self, code: str, exit_code: int, message: str) -> None:
-        super().__init__(message)
-        self.code = code
-        self.exit_code = exit_code
-
-
-def parse_origin_url(url: str) -> str | None:
-    """Return ``owner/repo`` for a GitHub origin URL, else ``None``."""
-    url = url.strip()
-    for pattern in _ORIGIN_PATTERNS:
-        match = pattern.match(url)
-        if match:
-            owner = match.group("owner")
-            repo = match.group("repo")
-            if repo.endswith(".git"):
-                repo = repo[: -len(".git")]
-            if not repo or owner in (".", "..") or repo in (".", ".."):
-                return None
-            return f"{owner}/{repo}"
-    return None
-
-
-def check_claim(arg: str, origin: str) -> int:
-    """Return the issue number a claim argument names on ``origin``.
-
-    Raises ``ClaimError`` with ``E-FOREIGN-REPO`` or ``E-NOT-AN-ISSUE``.
-    """
-    arg = arg.strip()
-    number = _NUMBER.match(arg)
-    if number:
-        return int(number.group("n"))
-
-    url = _GITHUB_URL.match(arg)
-    if not url:
-        if "://" in arg or arg.lower().startswith("git@"):
-            raise ClaimError(
-                "E-FOREIGN-REPO",
-                EXIT_FOREIGN_REPO,
-                f"{arg} is not a GitHub URL, so it is not on the origin repo {origin}",
-            )
-        raise ClaimError(
-            "E-NOT-AN-ISSUE",
-            EXIT_NOT_AN_ISSUE,
-            f"{arg} is not an issue number or an issue URL",
-        )
-
-    segments = [s for s in url.group("path").split("/") if s]
-    if len(segments) < 2:
-        raise ClaimError(
-            "E-FOREIGN-REPO", EXIT_FOREIGN_REPO, f"{arg} names no repository"
-        )
-    owner, repo = segments[0], segments[1]
-    if repo.lower().endswith(".git"):
-        repo = repo[: -len(".git")]
-    origin_owner, origin_repo = origin.split("/", 1)
-    if owner.lower() != origin_owner.lower() or repo.lower() != origin_repo.lower():
-        raise ClaimError(
-            "E-FOREIGN-REPO",
-            EXIT_FOREIGN_REPO,
-            f"{owner}/{repo} is not the origin repo {origin}",
-        )
-
-    rest = segments[2:]
-    if len(rest) == 2 and rest[0] == "issues":
-        number = _NUMBER.match(rest[1])
-        if number and not rest[1].startswith("#"):
-            return int(number.group("n"))
-    if rest and rest[0] == "pull":
-        raise ClaimError(
-            "E-NOT-AN-ISSUE", EXIT_NOT_AN_ISSUE, f"{arg} is a pull request, not an issue"
-        )
-    raise ClaimError(
-        "E-NOT-AN-ISSUE", EXIT_NOT_AN_ISSUE, f"{arg} is not an issue URL"
-    )
-
-
-def read_origin() -> str:
-    """Return ``owner/repo`` of the ``origin`` remote, or raise ``ClaimError``."""
-    try:
-        result = subprocess.run(
-            ["git", "remote", "get-url", "origin"],
-            capture_output=True,
-            text=True,
-            check=False,
-        )
-    except OSError as exc:
-        raise ClaimError("E-NO-ORIGIN", EXIT_NO_ORIGIN, f"git could not run: {exc}") from exc
-    if result.returncode != 0:
-        raise ClaimError("E-NO-ORIGIN", EXIT_NO_ORIGIN, "no origin remote")
-    parsed = parse_origin_url(result.stdout)
-    if parsed is None:
-        raise ClaimError("E-NO-ORIGIN", EXIT_NO_ORIGIN, "origin is not a GitHub URL")
-    return parsed
-
-
-def main(argv: list[str] | None = None) -> int:
-    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
-    parser.add_argument("--claim", metavar="NUMBER_OR_URL")
-    args = parser.parse_args(argv)
-    try:
-        origin = read_origin()
-        if args.claim is None:
-            print(origin)
-            return 0
-        number = check_claim(args.claim, origin)
-    except ClaimError as exc:
-        print(f"{exc.code}: {exc}", file=sys.stderr)
-        return exc.exit_code
-    print(json.dumps({"repo": origin, "number": number}))
-    return 0
-
-
-if __name__ == "__main__":
-    sys.exit(main())
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t7-pytest.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t7-pytest.log
new file mode 100644
index 00000000..ee86d0dd
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t7-pytest.log
@@ -0,0 +1,75 @@
+$ uv run pytest tests/skills/test_issue_protocol.py -v
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.venv/bin/python
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 63 items
+
+tests/skills/test_issue_protocol.py::test_skill_frontmatter_and_size PASSED [  1%]
+tests/skills/test_issue_protocol.py::test_every_named_path_exists_and_every_file_is_named PASSED [  3%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[SKILL.md] PASSED [  4%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[chains.md] PASSED [  6%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[claim.md] PASSED [  7%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[create.md] PASSED [  9%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[labels.md] PASSED [ 11%]
+tests/skills/test_issue_protocol.py::test_spawn_rule_text_present[tiers.md] PASSED [ 12%]
+tests/skills/test_issue_protocol.py::test_all_five_refs_exist PASSED     [ 14%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[accuracy-check-comment-<!-- sc:issue:accuracy-check -->] PASSED [ 15%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[claim-comment-<!-- sc:issue:claim -->] PASSED [ 17%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[create-review-comment-<!-- sc:issue:create-review -->] PASSED [ 19%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[issue-bug-complex-<!-- sc:issue:create template=issue-bug-complex -->] PASSED [ 20%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[issue-bug-simple-<!-- sc:issue:create template=issue-bug-simple -->] PASSED [ 22%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[issue-feature-complex-<!-- sc:issue:create template=issue-feature-complex -->] PASSED [ 23%]
+tests/skills/test_issue_protocol.py::test_posted_template_ends_with_marker[issue-feature-simple-<!-- sc:issue:create template=issue-feature-simple -->] PASSED [ 25%]
+tests/skills/test_issue_protocol.py::test_marker_check_fails_when_marker_is_removed PASSED [ 26%]
+tests/skills/test_issue_protocol.py::test_issue_template_headings_in_order[issue-bug-complex-expected0] PASSED [ 28%]
+tests/skills/test_issue_protocol.py::test_issue_template_headings_in_order[issue-bug-simple-expected1] PASSED [ 30%]
+tests/skills/test_issue_protocol.py::test_issue_template_headings_in_order[issue-feature-complex-expected2] PASSED [ 31%]
+tests/skills/test_issue_protocol.py::test_issue_template_headings_in_order[issue-feature-simple-expected3] PASSED [ 33%]
+tests/skills/test_issue_protocol.py::test_issue_template_has_no_clickup_text[issue-bug-complex] PASSED [ 34%]
+tests/skills/test_issue_protocol.py::test_issue_template_has_no_clickup_text[issue-bug-simple] PASSED [ 36%]
+tests/skills/test_issue_protocol.py::test_issue_template_has_no_clickup_text[issue-feature-complex] PASSED [ 38%]
+tests/skills/test_issue_protocol.py::test_issue_template_has_no_clickup_text[issue-feature-simple] PASSED [ 39%]
+tests/skills/test_issue_protocol.py::test_every_chain_flag_exists_in_its_command PASSED [ 41%]
+tests/skills/test_issue_protocol.py::test_brainstorm_steps_have_no_handoff_and_pin_models PASSED [ 42%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[SKILL.md] PASSED [ 44%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[chains.md] PASSED [ 46%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[claim.md] PASSED [ 47%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[create.md] PASSED [ 49%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[labels.md] PASSED [ 50%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[tiers.md] PASSED [ 52%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t3.md] PASSED [ 53%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t2.md] PASSED [ 55%]
+tests/skills/test_issue_protocol.py::test_every_gh_issue_pr_label_mention_carries_repo[issue-worker-t1.md] PASSED [ 57%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[SKILL.md] PASSED [ 58%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[chains.md] PASSED [ 60%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[claim.md] PASSED [ 61%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[create.md] PASSED [ 63%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[labels.md] PASSED [ 65%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[tiers.md] PASSED [ 66%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[clickup_claim.py] PASSED [ 68%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[origin_repo.py] PASSED [ 69%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[accuracy-check-comment.md] PASSED [ 71%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[claim-comment.md] PASSED [ 73%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[create-review-comment.md] PASSED [ 74%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[description.md] PASSED [ 76%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[draft-notes.md] PASSED [ 77%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[flags-decision.md] PASSED [ 79%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-bug-complex.md] PASSED [ 80%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-bug-simple.md] PASSED [ 82%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-feature-complex.md] PASSED [ 84%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-feature-simple.md] PASSED [ 85%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[next-steps.md] PASSED [ 87%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[recommend-record.md] PASSED [ 88%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[scout-report.md] PASSED [ 90%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[summary.md] PASSED [ 92%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-worker-t3.md] PASSED [ 93%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-worker-t2.md] PASSED [ 95%]
+tests/skills/test_issue_protocol.py::test_no_brace_placeholder[issue-worker-t1.md] PASSED [ 96%]
+tests/skills/test_issue_protocol.py::test_fork_safety_scan_fails_on_a_ref_without_repo PASSED [ 98%]
+tests/skills/test_issue_protocol.py::test_no_source_tree_path_in_skill_files PASSED [100%]
+
+============================== 63 passed in 0.10s ==============================
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t7-t1-rerun.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t7-t1-rerun.log
new file mode 100644
index 00000000..294cf535
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t7-t1-rerun.log
@@ -0,0 +1,14 @@
+$ uv run pytest tests/skills/test_issue_repo_resolution.py -q (re-run after the Task 7 edit to origin_repo.py)
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collected 64 items
+
+tests/skills/test_issue_repo_resolution.py ............................. [ 45%]
+...................................                                      [100%]
+
+============================== 64 passed in 0.36s ==============================
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
