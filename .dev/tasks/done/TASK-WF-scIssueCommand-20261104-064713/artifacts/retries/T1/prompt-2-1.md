55c06cbabbe4d732e0fac71f24a2ad818d8a7024
Review one task for spec compliance.

Task brief: ## Task 1: Create the origin-repo resolver script and its tests

Create `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` as specified in source section 13 and the `origin_repo.py` row of section 15: Python standard library only; it runs `git remote get-url origin` (reading only the `origin` remote, never `gh repo set-default` or any other remote) and prints `owner/repo`. It accepts `https://github.com/<owner>/<repo>`, `https://github.com/<owner>/<repo>.git`, `git@github.com:<owner>/<repo>` and `git@github.com:<owner>/<repo>.git`, tolerating a trailing `/`. A missing `origin` or a non-GitHub URL exits non-zero and prints `E-NO-ORIGIN`. Factor the URL parsing into a pure function so the tests can call it without a git checkout.

Create `tests/skills/test_issue_repo_resolution.py` (source section 16 row) that loads the script by path (the way `tests/skills/test_workflow_archive.py` loads `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py`) and pins: https, ssh, `.git` suffix and trailing `/` all parse to `owner/repo`; a non-GitHub URL exits non-zero with `E-NO-ORIGIN`; a temporary git repository with no `origin` exits non-zero with `E-NO-ORIGIN`; a temporary repository with an `upstream` remote pointing at another GitHub repo and an `origin` remote still resolves to the `origin` value only.

Acceptance criteria:
- `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` exists and imports only standard-library modules.
- `uv run pytest tests/skills/test_issue_repo_resolution.py -v` passes, with at least one test each for https, ssh, `.git` suffix, trailing `/`, non-GitHub URL, missing `origin`, and origin-only resolution when another remote exists.
- `uv run --no-project python src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` run in this checkout prints `IronbellyOrg/IronClaude`; the output is saved to `./artifacts/t1-origin-repo.txt`.

AC ids: T1.AC1 = first acceptance bullet (script exists, standard library only); T1.AC2 = second bullet (pytest passes with the listed test kinds); T1.AC3 = third bullet (live output saved to ./artifacts/t1-origin-repo.txt, package-relative: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-origin-repo.txt).

Coordinator constraint C2 (binding; overrides the plan text where they conflict; recorded in .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/coordinator-constraints.md):
T1.AC4 = implement the deterministic URL-versus-origin check the design requires (E-FOREIGN-REPO, source.md section 20 item 4: "A claim URL for any repo other than origin stops with `E-FOREIGN-REPO`") in this script, with unit tests for: same repo, foreign owner, same owner with a different repo, a repo-name prefix, a /pull/<N> URL, a trailing slash or fragment, digits in the owner or repo never becoming N. The exit code for E-FOREIGN-REPO must differ from E-NO-ORIGIN. Never run a live /sc:issue claim.
Design source for reference: .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md (sections 13, 15, 16, 20).

Global constraints: ## Constraints

- UV only: run Python and tests with `uv run ...` (`uv run pytest`, `uv run --no-project python ...`); never `python -m`, bare `python script.py` or `pip install`.
- Edit only under `src/superclaude/`, `tests/`, `docs/` and the one plugin guide copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (source section 15 and section 17 item 1). Also allowed: this package's `./artifacts/` folder, the unstaged scratch folder `.dev/issues/smoke/` (Task 15), and one temporary Orca worktree for the master comparison (Task 14), which that task removes. `.claude/` is produced by `make sync-dev`; never edit it by hand and never `git add` any `.claude/` path except `.claude/settings.json` (never `git add -f` on `.claude/`).
- Inside the new primitives (command, skill, refs, templates, agents) every reference to another primitive uses its installed path (`~/.claude/commands/sc/<name>.md`, `~/.claude/skills/<name>/...`, `~/.claude/agents/<name>.md`) plus, for existence checks, the project `.claude/` copy; no `src/superclaude/...` path appears in them (source section 15, "Path rule").
- Never interact with the upstream parent `SuperClaude-Org/SuperClaude_Framework`: every `gh` command passes `--repo IronbellyOrg/IronClaude` (or, inside the shipped skill, `--repo <R>` resolved from `origin`), every `gh api` path spells `repos/<owner>/<repo>/...`, and the only fetch is `git fetch origin` (source section 13).
- Secrets: the executor never asks for, prints, echoes or inlines `CLICKUP_API_TOKEN` (no `echo`, `env`, `printenv` or `set -x` on it). When a live ClickUp run is needed, the user exports the variables in their own shell before starting the session (source section 12, "Never printed, logged or written to disk").
- Do not commit or push unless the user asks. `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included; staging is not committing.
- Out of scope for this plan (source section 1 and section 17 item 5): running any next-step chain, creating GitHub labels, creating ClickUp tasks, editing rule 10 of `src/superclaude/core/CLAUDE.md`, changing the level table, adding `plugins/superclaude/` command, agent or skill mirrors, listing the workers in `docs/user-guide/agents.md`, any `src/superclaude/cli/` code, and opening the pull request (done afterwards with `/sc:pr-submit --monitor 3 --head ironbelly/feat-sc-issue-command --title "..." --body "..."`).
- Live `/sc:issue --claim` or `--create` runs post directly to GitHub (source decision B1). Live checks in this plan are the two the source schedules (Task 15 worker spawns, Task 16 ClickUp smoke claim) and the section 20 acceptance record of Task 17. A run that stops before any GitHub or ClickUp write (section 20 item 4) may run without asking; any run that would assign, comment on or create a real GitHub issue needs the user's explicit approval at that moment.

Start sha: 55c06cbabbe4d732e0fac71f24a2ad818d8a7024
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py b/src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py
new file mode 100644
index 00000000..b4adb69f
--- /dev/null
+++ b/src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py
@@ -0,0 +1,193 @@
+#!/usr/bin/env python3
+"""Resolve the origin GitHub repository and check a /sc:issue claim argument.
+
+Standard library only. Wave 0 of both /sc:issue modes runs this script, so the
+repository rule of the design (section 13) is tested code, not prose.
+
+Usage:
+    origin_repo.py
+        Print ``owner/repo`` parsed from ``git remote get-url origin``.
+    origin_repo.py --claim <number|#number|url>
+        Resolve origin as above, then check the claim argument against it and
+        print ``{"repo": "owner/repo", "number": N}`` as one JSON line.
+
+Only the ``origin`` remote is read. ``gh repo set-default``, gh's fork-parent
+default and every other remote are never consulted.
+
+Accepted origin URLs (a trailing ``/`` is tolerated):
+    https://github.com/<owner>/<repo>
+    https://github.com/<owner>/<repo>.git
+    git@github.com:<owner>/<repo>
+    git@github.com:<owner>/<repo>.git
+
+Claim argument rules (``check_claim``):
+    ``302`` or ``#302``                         -> N = 302
+    ``https://github.com/<origin>/issues/302``  -> N = 302; a trailing ``/``,
+                                                   a ``#fragment`` or a
+                                                   ``?query`` is ignored
+    a GitHub URL naming any other owner or      -> E-FOREIGN-REPO
+    repo, or naming no repo                        (owner and repo compare
+                                                   case-insensitively and as
+                                                   whole path segments, so
+                                                   ``IronClaudeX`` is foreign)
+    a URL (``<scheme>://...`` or               -> E-FOREIGN-REPO
+    ``git@<host>:...``) on any host other
+    than github.com
+    ``https://github.com/<origin>/pull/302``    -> E-NOT-AN-ISSUE
+    a GitHub URL on origin whose path is not    -> E-NOT-AN-ISSUE
+    ``/issues/<N>``
+    anything else (not a number, not a URL)     -> E-NOT-AN-ISSUE
+A GitHub URL may start with ``https://``, ``http://`` or no scheme, may carry
+``www.``, and may be written ``git@github.com:<owner>/<repo>/...``; every form
+is read by the same rules above. N is read only from the path segment right
+after ``/issues/``; digits in the owner or repo name never become N.
+
+Exit codes and messages (the message goes to stderr):
+    0  success
+    1  E-NO-ORIGIN     no origin remote, git failed, or origin is not GitHub
+    2  bad command-line arguments (argparse)
+    3  E-FOREIGN-REPO  the claim URL names a repository other than origin
+    4  E-NOT-AN-ISSUE  the claim argument is not an issue number or issue URL
+"""
+
+from __future__ import annotations
+
+import argparse
+import json
+import re
+import subprocess
+import sys
+
+EXIT_NO_ORIGIN = 1
+EXIT_FOREIGN_REPO = 3
+EXIT_NOT_AN_ISSUE = 4
+
+_NAME = r"[A-Za-z0-9._-]+"
+_ORIGIN_PATTERNS = (
+    re.compile(rf"^https://github\.com/(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
+    re.compile(rf"^git@github\.com:(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
+)
+_GITHUB_URL = re.compile(
+    r"^(?:(?:https?://)?(?:www\.)?github\.com/|git@github\.com:)(?P<path>[^?#]*)",
+    re.IGNORECASE,
+)
+_NUMBER = re.compile(r"^#?(?P<n>[1-9][0-9]*)$")
+
+
+class ClaimError(Exception):
+    """A claim argument that /sc:issue must STOP on."""
+
+    def __init__(self, code: str, exit_code: int, message: str) -> None:
+        super().__init__(message)
+        self.code = code
+        self.exit_code = exit_code
+
+
+def parse_origin_url(url: str) -> str | None:
+    """Return ``owner/repo`` for a GitHub origin URL, else ``None``."""
+    url = url.strip()
+    for pattern in _ORIGIN_PATTERNS:
+        match = pattern.match(url)
+        if match:
+            owner = match.group("owner")
+            repo = match.group("repo")
+            if repo.endswith(".git"):
+                repo = repo[: -len(".git")]
+            if not repo or owner in (".", "..") or repo in (".", ".."):
+                return None
+            return f"{owner}/{repo}"
+    return None
+
+
+def check_claim(arg: str, origin: str) -> int:
+    """Return the issue number a claim argument names on ``origin``.
+
+    Raises ``ClaimError`` with ``E-FOREIGN-REPO`` or ``E-NOT-AN-ISSUE``.
+    """
+    arg = arg.strip()
+    number = _NUMBER.match(arg)
+    if number:
+        return int(number.group("n"))
+
+    url = _GITHUB_URL.match(arg)
+    if not url:
+        if "://" in arg or arg.lower().startswith("git@"):
+            raise ClaimError(
+                "E-FOREIGN-REPO",
+                EXIT_FOREIGN_REPO,
+                f"{arg} is not a GitHub URL, so it is not on the origin repo {origin}",
+            )
+        raise ClaimError(
+            "E-NOT-AN-ISSUE",
+            EXIT_NOT_AN_ISSUE,
+            f"{arg} is not an issue number or an issue URL",
+        )
+
+    segments = [s for s in url.group("path").split("/") if s]
+    if len(segments) < 2:
+        raise ClaimError(
+            "E-FOREIGN-REPO", EXIT_FOREIGN_REPO, f"{arg} names no repository"
+        )
+    owner, repo = segments[0], segments[1]
+    if repo.lower().endswith(".git"):
+        repo = repo[: -len(".git")]
+    origin_owner, origin_repo = origin.split("/", 1)
+    if owner.lower() != origin_owner.lower() or repo.lower() != origin_repo.lower():
+        raise ClaimError(
+            "E-FOREIGN-REPO",
+            EXIT_FOREIGN_REPO,
+            f"{owner}/{repo} is not the origin repo {origin}",
+        )
+
+    rest = segments[2:]
+    if len(rest) == 2 and rest[0] == "issues":
+        number = _NUMBER.match(rest[1])
+        if number and not rest[1].startswith("#"):
+            return int(number.group("n"))
+    if rest and rest[0] == "pull":
+        raise ClaimError(
+            "E-NOT-AN-ISSUE", EXIT_NOT_AN_ISSUE, f"{arg} is a pull request, not an issue"
+        )
+    raise ClaimError(
+        "E-NOT-AN-ISSUE", EXIT_NOT_AN_ISSUE, f"{arg} is not an issue URL"
+    )
+
+
+def read_origin() -> str:
+    """Return ``owner/repo`` of the ``origin`` remote, or raise ``ClaimError``."""
+    try:
+        result = subprocess.run(
+            ["git", "remote", "get-url", "origin"],
+            capture_output=True,
+            text=True,
+            check=False,
+        )
+    except OSError as exc:
+        raise ClaimError("E-NO-ORIGIN", EXIT_NO_ORIGIN, f"git could not run: {exc}") from exc
+    if result.returncode != 0:
+        raise ClaimError("E-NO-ORIGIN", EXIT_NO_ORIGIN, "no origin remote")
+    parsed = parse_origin_url(result.stdout)
+    if parsed is None:
+        raise ClaimError("E-NO-ORIGIN", EXIT_NO_ORIGIN, "origin is not a GitHub URL")
+    return parsed
+
+
+def main(argv: list[str] | None = None) -> int:
+    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
+    parser.add_argument("--claim", metavar="NUMBER_OR_URL")
+    args = parser.parse_args(argv)
+    try:
+        origin = read_origin()
+        if args.claim is None:
+            print(origin)
+            return 0
+        number = check_claim(args.claim, origin)
+    except ClaimError as exc:
+        print(f"{exc.code}: {exc}", file=sys.stderr)
+        return exc.exit_code
+    print(json.dumps({"repo": origin, "number": number}))
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/tests/skills/test_issue_repo_resolution.py b/tests/skills/test_issue_repo_resolution.py
new file mode 100644
index 00000000..7937055b
--- /dev/null
+++ b/tests/skills/test_issue_repo_resolution.py
@@ -0,0 +1,267 @@
+"""Behavior tests for the /sc:issue origin-repo resolver and claim-URL check.
+
+Enforcement type: EXECUTABLE (script behavior). The script is loaded by path,
+the same way test_workflow_archive.py loads archive_workspace.py.
+"""
+
+import importlib.util
+import json
+import subprocess
+import sys
+from pathlib import Path
+
+import pytest
+
+_SCRIPT = (
+    Path(__file__).resolve().parents[2]
+    / "src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py"
+)
+_spec = importlib.util.spec_from_file_location("origin_repo", _SCRIPT)
+orr = importlib.util.module_from_spec(_spec)
+_spec.loader.exec_module(orr)
+
+ORIGIN = "IronbellyOrg/IronClaude"
+
+
+# --- origin URL parsing -------------------------------------------------------
+
+
+@pytest.mark.parametrize(
+    "url",
+    [
+        "https://github.com/IronbellyOrg/IronClaude",  # https
+        "https://github.com/IronbellyOrg/IronClaude.git",  # https + .git suffix
+        "https://github.com/IronbellyOrg/IronClaude/",  # https + trailing /
+        "https://github.com/IronbellyOrg/IronClaude.git/",  # .git + trailing /
+        "git@github.com:IronbellyOrg/IronClaude",  # ssh
+        "git@github.com:IronbellyOrg/IronClaude.git",  # ssh + .git suffix
+        "git@github.com:IronbellyOrg/IronClaude/",  # ssh + trailing /
+        "https://github.com/IronbellyOrg/IronClaude\n",  # git output newline
+    ],
+)
+def test_github_origin_forms_parse_to_owner_repo(url):
+    assert orr.parse_origin_url(url) == ORIGIN
+
+
+@pytest.mark.parametrize(
+    "url",
+    [
+        "https://gitlab.com/IronbellyOrg/IronClaude.git",
+        "git@bitbucket.org:IronbellyOrg/IronClaude.git",
+        "https://github.com/IronbellyOrg",
+        "/srv/git/IronClaude.git",
+        "",
+    ],
+)
+def test_non_github_origin_does_not_parse(url):
+    assert orr.parse_origin_url(url) is None
+
+
+# --- running the script in a real temporary repository ------------------------
+
+
+def _git(repo: Path, *args: str) -> None:
+    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
+
+
+def _repo(tmp_path: Path) -> Path:
+    repo = tmp_path / "repo"
+    repo.mkdir()
+    _git(repo, "init", "-q")
+    return repo
+
+
+def _run(repo: Path, *args: str) -> subprocess.CompletedProcess:
+    return subprocess.run(
+        [sys.executable, str(_SCRIPT), *args],
+        cwd=repo,
+        capture_output=True,
+        text=True,
+        check=False,
+    )
+
+
+def test_non_github_origin_exits_nonzero_with_e_no_origin(tmp_path):
+    repo = _repo(tmp_path)
+    _git(repo, "remote", "add", "origin", "https://gitlab.com/IronbellyOrg/IronClaude.git")
+    result = _run(repo)
+    assert result.returncode == orr.EXIT_NO_ORIGIN != 0
+    assert "E-NO-ORIGIN" in result.stderr
+    assert result.stdout == ""
+
+
+def test_missing_origin_exits_nonzero_with_e_no_origin(tmp_path):
+    repo = _repo(tmp_path)
+    result = _run(repo)
+    assert result.returncode == orr.EXIT_NO_ORIGIN != 0
+    assert "E-NO-ORIGIN" in result.stderr
+
+
+def test_missing_origin_with_other_remote_still_e_no_origin(tmp_path):
+    repo = _repo(tmp_path)
+    _git(repo, "remote", "add", "upstream", "https://github.com/SomeParent/Framework.git")
+    result = _run(repo)
+    assert result.returncode == orr.EXIT_NO_ORIGIN
+    assert "E-NO-ORIGIN" in result.stderr
+
+
+def test_only_origin_is_read_when_another_remote_exists(tmp_path):
+    repo = _repo(tmp_path)
+    _git(repo, "remote", "add", "upstream", "https://github.com/SomeParent/Framework.git")
+    _git(repo, "remote", "add", "origin", "git@github.com:IronbellyOrg/IronClaude.git")
+    result = _run(repo)
+    assert result.returncode == 0, result.stderr
+    assert result.stdout.strip() == ORIGIN
+    assert "SomeParent" not in result.stdout
+
+
+def test_claim_mode_prints_repo_and_number(tmp_path):
+    repo = _repo(tmp_path)
+    _git(repo, "remote", "add", "origin", "https://github.com/IronbellyOrg/IronClaude")
+    result = _run(repo, "--claim", "https://github.com/IronbellyOrg/IronClaude/issues/302")
+    assert result.returncode == 0, result.stderr
+    assert json.loads(result.stdout) == {"repo": ORIGIN, "number": 302}
+
+
+def test_claim_mode_foreign_url_exits_with_distinct_code(tmp_path):
+    repo = _repo(tmp_path)
+    _git(repo, "remote", "add", "origin", "https://github.com/IronbellyOrg/IronClaude")
+    result = _run(repo, "--claim", "https://github.com/octocat/Hello-World/issues/1")
+    assert result.returncode == orr.EXIT_FOREIGN_REPO
+    assert orr.EXIT_FOREIGN_REPO not in (0, orr.EXIT_NO_ORIGIN)
+    assert "E-FOREIGN-REPO" in result.stderr
+    assert result.stdout == ""
+
+
+def test_claim_mode_without_origin_reports_e_no_origin_first(tmp_path):
+    repo = _repo(tmp_path)
+    result = _run(repo, "--claim", "302")
+    assert result.returncode == orr.EXIT_NO_ORIGIN
+    assert "E-NO-ORIGIN" in result.stderr
+
+
+def test_bad_arguments_exit_2(tmp_path):
+    repo = _repo(tmp_path)
+    result = _run(repo, "--no-such-flag")
+    assert result.returncode == 2
+
+
+# --- claim argument versus origin (E-FOREIGN-REPO, design section 20 item 4) --
+
+
+@pytest.mark.parametrize(
+    ("arg", "number"),
+    [
+        ("302", 302),
+        ("#302", 302),
+        ("https://github.com/IronbellyOrg/IronClaude/issues/302", 302),  # same repo
+        ("https://github.com/ironbellyorg/ironclaude/issues/302", 302),  # case-insensitive
+        ("https://github.com/IronbellyOrg/IronClaude/issues/302/", 302),  # trailing /
+        ("https://github.com/IronbellyOrg/IronClaude/issues/302#issuecomment-9", 302),  # fragment
+        ("https://github.com/IronbellyOrg/IronClaude/issues/302?x=1", 302),  # query
+        ("http://github.com/IronbellyOrg/IronClaude/issues/302", 302),  # http scheme
+        ("github.com/IronbellyOrg/IronClaude/issues/302", 302),  # no scheme
+        ("www.github.com/IronbellyOrg/IronClaude/issues/302", 302),  # no scheme, www.
+        ("https://www.github.com/IronbellyOrg/IronClaude/issues/302", 302),  # www.
+        ("git@github.com:IronbellyOrg/IronClaude/issues/302", 302),  # git@ form
+    ],
+)
+def test_claim_on_origin_returns_issue_number(arg, number):
+    assert orr.check_claim(arg, ORIGIN) == number
+
+
+@pytest.mark.parametrize(
+    "arg",
+    [
+        "https://github.com/octocat/IronClaude/issues/1",  # foreign owner
+        "https://github.com/IronbellyOrg/OtherRepo/issues/1",  # same owner, different repo
+        "https://github.com/IronbellyOrg/IronClaudeX/issues/1",  # repo-name prefix
+        "https://github.com/IronbellyOrg/IronClaud/issues/1",  # origin repo is a prefix of it
+        "https://github.com/IronbellyOrgX/IronClaude/issues/1",  # owner-name prefix
+        "https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999",
+        "https://gitlab.com/IronbellyOrg/IronClaude/issues/1",  # not GitHub
+        "https://github.com/IronbellyOrg",  # no repository
+        "github.com/octocat/Hello-World/issues/1",  # no scheme, foreign
+        "www.github.com/IronbellyOrg/IronClaudeX/issues/1",  # no scheme, prefix
+        "git@github.com:octocat/Hello-World.git",  # git@ form, foreign
+        "git@bitbucket.org:IronbellyOrg/IronClaude.git",  # git@ form, not GitHub
+    ],
+)
+def test_claim_url_on_another_repo_is_e_foreign_repo(arg):
+    with pytest.raises(orr.ClaimError) as exc:
+        orr.check_claim(arg, ORIGIN)
+    assert exc.value.code == "E-FOREIGN-REPO"
+    assert exc.value.exit_code == orr.EXIT_FOREIGN_REPO
+
+
+@pytest.mark.parametrize(
+    "arg",
+    [
+        "https://github.com/IronbellyOrg/IronClaude/pull/302",
+        "https://github.com/IronbellyOrg/IronClaude/pull/302/",
+        "https://github.com/IronbellyOrg/IronClaude/pull/302#discussion_r1",
+    ],
+)
+def test_pull_url_on_origin_is_rejected_not_parsed(arg):
+    with pytest.raises(orr.ClaimError) as exc:
+        orr.check_claim(arg, ORIGIN)
+    assert exc.value.code == "E-NOT-AN-ISSUE"
+    assert exc.value.exit_code == orr.EXIT_NOT_AN_ISSUE
+
+
+def test_pull_url_on_foreign_repo_is_e_foreign_repo():
+    with pytest.raises(orr.ClaimError) as exc:
+        orr.check_claim("https://github.com/octocat/Hello-World/pull/302", ORIGIN)
+    assert exc.value.code == "E-FOREIGN-REPO"
+
+
+@pytest.mark.parametrize(
+    ("origin", "arg"),
+    [
+        ("Org302/Repo456", "https://github.com/Org302/Repo456"),
+        ("Org302/Repo456", "https://github.com/Org302/Repo456/"),
+        ("Org302/Repo456", "https://github.com/Org302/Repo456/issues"),
+        ("IronbellyOrg/IronClaude302", "https://github.com/IronbellyOrg/IronClaude302/tree/main"),
+    ],
+)
+def test_digits_in_owner_or_repo_never_become_n(origin, arg):
+    with pytest.raises(orr.ClaimError) as exc:
+        orr.check_claim(arg, origin)
+    assert exc.value.code == "E-NOT-AN-ISSUE"
+
+
+def test_digits_in_owner_and_repo_do_not_replace_the_issue_segment():
+    assert orr.check_claim("https://github.com/Org302/Repo456/issues/7", "Org302/Repo456") == 7
+
+
+@pytest.mark.parametrize(
+    "arg",
+    [
+        "",
+        "abc",
+        "0",
+        "-3",
+        "302abc",
+        "https://github.com/IronbellyOrg/IronClaude/issues/abc",
+        "https://github.com/IronbellyOrg/IronClaude/issues/302/comments",
+        "github.com/IronbellyOrg/IronClaude",  # origin, no scheme, no issue path
+        "git@github.com:IronbellyOrg/IronClaude.git",  # origin remote URL, no issue path
+    ],
+)
+def test_other_arguments_are_not_an_issue(arg):
+    with pytest.raises(orr.ClaimError) as exc:
+        orr.check_claim(arg, ORIGIN)
+    assert exc.value.code == "E-NOT-AN-ISSUE"
+
+
+def test_script_imports_only_standard_library():
+    import ast
+
+    tree = ast.parse(_SCRIPT.read_text(encoding="utf-8"))
+    names = set()
+    for node in ast.walk(tree):
+        if isinstance(node, ast.Import):
+            names.update(alias.name.split(".")[0] for alias in node.names)
+        elif isinstance(node, ast.ImportFrom) and node.module:
+            names.add(node.module.split(".")[0])
+    assert names <= set(sys.stdlib_module_names)
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-origin-repo.txt b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-origin-repo.txt
new file mode 100644
index 00000000..e1c5bbcf
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-origin-repo.txt
@@ -0,0 +1,3 @@
+$ uv run --no-project python src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py
+IronbellyOrg/IronClaude
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-pytest.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-pytest.log
new file mode 100644
index 00000000..95ff319c
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-pytest.log
@@ -0,0 +1,76 @@
+$ uv run pytest tests/skills/test_issue_repo_resolution.py -v
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command/.venv/bin/python
+SuperClaude: 5.0.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, anyio-4.16.0
+collecting ... collected 64 items
+
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude] PASSED [  1%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude.git] PASSED [  3%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude/] PASSED [  4%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude.git/] PASSED [  6%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude] PASSED [  7%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude.git] PASSED [  9%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude/] PASSED [ 10%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude\n] PASSED [ 12%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[https://gitlab.com/IronbellyOrg/IronClaude.git] PASSED [ 14%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[git@bitbucket.org:IronbellyOrg/IronClaude.git] PASSED [ 15%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[https://github.com/IronbellyOrg] PASSED [ 17%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[/srv/git/IronClaude.git] PASSED [ 18%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[] PASSED [ 20%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_exits_nonzero_with_e_no_origin PASSED [ 21%]
+tests/skills/test_issue_repo_resolution.py::test_missing_origin_exits_nonzero_with_e_no_origin PASSED [ 23%]
+tests/skills/test_issue_repo_resolution.py::test_missing_origin_with_other_remote_still_e_no_origin PASSED [ 25%]
+tests/skills/test_issue_repo_resolution.py::test_only_origin_is_read_when_another_remote_exists PASSED [ 26%]
+tests/skills/test_issue_repo_resolution.py::test_claim_mode_prints_repo_and_number PASSED [ 28%]
+tests/skills/test_issue_repo_resolution.py::test_claim_mode_foreign_url_exits_with_distinct_code PASSED [ 29%]
+tests/skills/test_issue_repo_resolution.py::test_claim_mode_without_origin_reports_e_no_origin_first PASSED [ 31%]
+tests/skills/test_issue_repo_resolution.py::test_bad_arguments_exit_2 PASSED [ 32%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[302-302] PASSED [ 34%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[#302-302] PASSED [ 35%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 37%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/ironbellyorg/ironclaude/issues/302-302] PASSED [ 39%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302/-302] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302#issuecomment-9-302] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302?x=1-302] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[http://github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 45%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 46%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[www.github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 48%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://www.github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 50%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[git@github.com:IronbellyOrg/IronClaude/issues/302-302] PASSED [ 51%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/octocat/IronClaude/issues/1] PASSED [ 53%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/OtherRepo/issues/1] PASSED [ 54%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/IronClaudeX/issues/1] PASSED [ 56%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/IronClaud/issues/1] PASSED [ 57%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrgX/IronClaude/issues/1] PASSED [ 59%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999] PASSED [ 60%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://gitlab.com/IronbellyOrg/IronClaude/issues/1] PASSED [ 62%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg] PASSED [ 64%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[github.com/octocat/Hello-World/issues/1] PASSED [ 65%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[www.github.com/IronbellyOrg/IronClaudeX/issues/1] PASSED [ 67%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[git@github.com:octocat/Hello-World.git] PASSED [ 68%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[git@bitbucket.org:IronbellyOrg/IronClaude.git] PASSED [ 70%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302] PASSED [ 71%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302/] PASSED [ 73%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302#discussion_r1] PASSED [ 75%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_foreign_repo_is_e_foreign_repo PASSED [ 76%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[Org302/Repo456-https://github.com/Org302/Repo456] PASSED [ 78%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[Org302/Repo456-https://github.com/Org302/Repo456/] PASSED [ 79%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[Org302/Repo456-https://github.com/Org302/Repo456/issues] PASSED [ 81%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[IronbellyOrg/IronClaude302-https://github.com/IronbellyOrg/IronClaude302/tree/main] PASSED [ 82%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_and_repo_do_not_replace_the_issue_segment PASSED [ 84%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[] PASSED [ 85%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[abc] PASSED [ 87%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[0] PASSED [ 89%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[-3] PASSED [ 90%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[302abc] PASSED [ 92%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[https://github.com/IronbellyOrg/IronClaude/issues/abc] PASSED [ 93%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[https://github.com/IronbellyOrg/IronClaude/issues/302/comments] PASSED [ 95%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[github.com/IronbellyOrg/IronClaude] PASSED [ 96%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[git@github.com:IronbellyOrg/IronClaude.git] PASSED [ 98%]
+tests/skills/test_issue_repo_resolution.py::test_script_imports_only_standard_library PASSED [100%]
+
+============================== 64 passed in 0.38s ==============================
+rc=0

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-pytest.log b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-pytest.log
index 59203017..95ff319c 100644
--- a/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-pytest.log
+++ b/.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/artifacts/t1-pytest.log
@@ -5,61 +5,72 @@ SuperClaude: 5.0.0
 rootdir: /home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command
 configfile: pyproject.toml
 plugins: superclaude-5.0.0, anyio-4.16.0
-collecting ... collected 53 items
+collecting ... collected 64 items
 
 tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude] PASSED [  1%]
 tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude.git] PASSED [  3%]
-tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude/] PASSED [  5%]
-tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude.git/] PASSED [  7%]
-tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude] PASSED [  9%]
-tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude.git] PASSED [ 11%]
-tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude/] PASSED [ 13%]
-tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude\n] PASSED [ 15%]
-tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[https://gitlab.com/IronbellyOrg/IronClaude.git] PASSED [ 16%]
-tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[git@bitbucket.org:IronbellyOrg/IronClaude.git] PASSED [ 18%]
-tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[https://github.com/IronbellyOrg] PASSED [ 20%]
-tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[/srv/git/IronClaude.git] PASSED [ 22%]
-tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[] PASSED [ 24%]
-tests/skills/test_issue_repo_resolution.py::test_non_github_origin_exits_nonzero_with_e_no_origin PASSED [ 26%]
-tests/skills/test_issue_repo_resolution.py::test_missing_origin_exits_nonzero_with_e_no_origin PASSED [ 28%]
-tests/skills/test_issue_repo_resolution.py::test_missing_origin_with_other_remote_still_e_no_origin PASSED [ 30%]
-tests/skills/test_issue_repo_resolution.py::test_only_origin_is_read_when_another_remote_exists PASSED [ 32%]
-tests/skills/test_issue_repo_resolution.py::test_claim_mode_prints_repo_and_number PASSED [ 33%]
-tests/skills/test_issue_repo_resolution.py::test_claim_mode_foreign_url_exits_with_distinct_code PASSED [ 35%]
-tests/skills/test_issue_repo_resolution.py::test_claim_mode_without_origin_reports_e_no_origin_first PASSED [ 37%]
-tests/skills/test_issue_repo_resolution.py::test_bad_arguments_exit_2 PASSED [ 39%]
-tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[302-302] PASSED [ 41%]
-tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[#302-302] PASSED [ 43%]
-tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 45%]
-tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/ironbellyorg/ironclaude/issues/302-302] PASSED [ 47%]
-tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302/-302] PASSED [ 49%]
-tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302#issuecomment-9-302] PASSED [ 50%]
-tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302?x=1-302] PASSED [ 52%]
-tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/octocat/IronClaude/issues/1] PASSED [ 54%]
-tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/OtherRepo/issues/1] PASSED [ 56%]
-tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/IronClaudeX/issues/1] PASSED [ 58%]
-tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/IronClaud/issues/1] PASSED [ 60%]
-tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrgX/IronClaude/issues/1] PASSED [ 62%]
-tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999] PASSED [ 64%]
-tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://gitlab.com/IronbellyOrg/IronClaude/issues/1] PASSED [ 66%]
-tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg] PASSED [ 67%]
-tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302] PASSED [ 69%]
-tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302/] PASSED [ 71%]
-tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302#discussion_r1] PASSED [ 73%]
-tests/skills/test_issue_repo_resolution.py::test_pull_url_on_foreign_repo_is_e_foreign_repo PASSED [ 75%]
-tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[Org302/Repo456-https://github.com/Org302/Repo456] PASSED [ 77%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude/] PASSED [  4%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude.git/] PASSED [  6%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude] PASSED [  7%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude.git] PASSED [  9%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[git@github.com:IronbellyOrg/IronClaude/] PASSED [ 10%]
+tests/skills/test_issue_repo_resolution.py::test_github_origin_forms_parse_to_owner_repo[https://github.com/IronbellyOrg/IronClaude\n] PASSED [ 12%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[https://gitlab.com/IronbellyOrg/IronClaude.git] PASSED [ 14%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[git@bitbucket.org:IronbellyOrg/IronClaude.git] PASSED [ 15%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[https://github.com/IronbellyOrg] PASSED [ 17%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[/srv/git/IronClaude.git] PASSED [ 18%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_does_not_parse[] PASSED [ 20%]
+tests/skills/test_issue_repo_resolution.py::test_non_github_origin_exits_nonzero_with_e_no_origin PASSED [ 21%]
+tests/skills/test_issue_repo_resolution.py::test_missing_origin_exits_nonzero_with_e_no_origin PASSED [ 23%]
+tests/skills/test_issue_repo_resolution.py::test_missing_origin_with_other_remote_still_e_no_origin PASSED [ 25%]
+tests/skills/test_issue_repo_resolution.py::test_only_origin_is_read_when_another_remote_exists PASSED [ 26%]
+tests/skills/test_issue_repo_resolution.py::test_claim_mode_prints_repo_and_number PASSED [ 28%]
+tests/skills/test_issue_repo_resolution.py::test_claim_mode_foreign_url_exits_with_distinct_code PASSED [ 29%]
+tests/skills/test_issue_repo_resolution.py::test_claim_mode_without_origin_reports_e_no_origin_first PASSED [ 31%]
+tests/skills/test_issue_repo_resolution.py::test_bad_arguments_exit_2 PASSED [ 32%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[302-302] PASSED [ 34%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[#302-302] PASSED [ 35%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 37%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/ironbellyorg/ironclaude/issues/302-302] PASSED [ 39%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302/-302] PASSED [ 40%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302#issuecomment-9-302] PASSED [ 42%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://github.com/IronbellyOrg/IronClaude/issues/302?x=1-302] PASSED [ 43%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[http://github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 45%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 46%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[www.github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 48%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[https://www.github.com/IronbellyOrg/IronClaude/issues/302-302] PASSED [ 50%]
+tests/skills/test_issue_repo_resolution.py::test_claim_on_origin_returns_issue_number[git@github.com:IronbellyOrg/IronClaude/issues/302-302] PASSED [ 51%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/octocat/IronClaude/issues/1] PASSED [ 53%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/OtherRepo/issues/1] PASSED [ 54%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/IronClaudeX/issues/1] PASSED [ 56%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/IronClaud/issues/1] PASSED [ 57%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrgX/IronClaude/issues/1] PASSED [ 59%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999] PASSED [ 60%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://gitlab.com/IronbellyOrg/IronClaude/issues/1] PASSED [ 62%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[https://github.com/IronbellyOrg] PASSED [ 64%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[github.com/octocat/Hello-World/issues/1] PASSED [ 65%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[www.github.com/IronbellyOrg/IronClaudeX/issues/1] PASSED [ 67%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[git@github.com:octocat/Hello-World.git] PASSED [ 68%]
+tests/skills/test_issue_repo_resolution.py::test_claim_url_on_another_repo_is_e_foreign_repo[git@bitbucket.org:IronbellyOrg/IronClaude.git] PASSED [ 70%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302] PASSED [ 71%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302/] PASSED [ 73%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_origin_is_rejected_not_parsed[https://github.com/IronbellyOrg/IronClaude/pull/302#discussion_r1] PASSED [ 75%]
+tests/skills/test_issue_repo_resolution.py::test_pull_url_on_foreign_repo_is_e_foreign_repo PASSED [ 76%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[Org302/Repo456-https://github.com/Org302/Repo456] PASSED [ 78%]
 tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[Org302/Repo456-https://github.com/Org302/Repo456/] PASSED [ 79%]
 tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[Org302/Repo456-https://github.com/Org302/Repo456/issues] PASSED [ 81%]
-tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[IronbellyOrg/IronClaude302-https://github.com/IronbellyOrg/IronClaude302/tree/main] PASSED [ 83%]
+tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_or_repo_never_become_n[IronbellyOrg/IronClaude302-https://github.com/IronbellyOrg/IronClaude302/tree/main] PASSED [ 82%]
 tests/skills/test_issue_repo_resolution.py::test_digits_in_owner_and_repo_do_not_replace_the_issue_segment PASSED [ 84%]
-tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[] PASSED [ 86%]
-tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[abc] PASSED [ 88%]
-tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[0] PASSED [ 90%]
-tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[-3] PASSED [ 92%]
-tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[302abc] PASSED [ 94%]
-tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[https://github.com/IronbellyOrg/IronClaude/issues/abc] PASSED [ 96%]
-tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[https://github.com/IronbellyOrg/IronClaude/issues/302/comments] PASSED [ 98%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[] PASSED [ 85%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[abc] PASSED [ 87%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[0] PASSED [ 89%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[-3] PASSED [ 90%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[302abc] PASSED [ 92%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[https://github.com/IronbellyOrg/IronClaude/issues/abc] PASSED [ 93%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[https://github.com/IronbellyOrg/IronClaude/issues/302/comments] PASSED [ 95%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[github.com/IronbellyOrg/IronClaude] PASSED [ 96%]
+tests/skills/test_issue_repo_resolution.py::test_other_arguments_are_not_an_issue[git@github.com:IronbellyOrg/IronClaude.git] PASSED [ 98%]
 tests/skills/test_issue_repo_resolution.py::test_script_imports_only_standard_library PASSED [100%]
 
-============================== 53 passed in 0.36s ==============================
+============================== 64 passed in 0.38s ==============================
 rc=0
diff --git a/src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py b/src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py
index 48712ae4..b4adb69f 100644
--- a/src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py
+++ b/src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py
@@ -25,15 +25,22 @@ Claim argument rules (``check_claim``):
     ``https://github.com/<origin>/issues/302``  -> N = 302; a trailing ``/``,
                                                    a ``#fragment`` or a
                                                    ``?query`` is ignored
-    a URL naming any other owner or repo        -> E-FOREIGN-REPO
-                                                   (owner and repo compare
+    a GitHub URL naming any other owner or      -> E-FOREIGN-REPO
+    repo, or naming no repo                        (owner and repo compare
                                                    case-insensitively and as
                                                    whole path segments, so
                                                    ``IronClaudeX`` is foreign)
+    a URL (``<scheme>://...`` or               -> E-FOREIGN-REPO
+    ``git@<host>:...``) on any host other
+    than github.com
     ``https://github.com/<origin>/pull/302``    -> E-NOT-AN-ISSUE
-    anything else                               -> E-NOT-AN-ISSUE
-N is read only from the path segment right after ``/issues/``; digits in the
-owner or repo name never become N.
+    a GitHub URL on origin whose path is not    -> E-NOT-AN-ISSUE
+    ``/issues/<N>``
+    anything else (not a number, not a URL)     -> E-NOT-AN-ISSUE
+A GitHub URL may start with ``https://``, ``http://`` or no scheme, may carry
+``www.``, and may be written ``git@github.com:<owner>/<repo>/...``; every form
+is read by the same rules above. N is read only from the path segment right
+after ``/issues/``; digits in the owner or repo name never become N.
 
 Exit codes and messages (the message goes to stderr):
     0  success
@@ -60,7 +67,10 @@ _ORIGIN_PATTERNS = (
     re.compile(rf"^https://github\.com/(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
     re.compile(rf"^git@github\.com:(?P<owner>{_NAME})/(?P<repo>{_NAME})/?$"),
 )
-_GITHUB_URL = re.compile(r"^https?://(?:www\.)?github\.com/(?P<path>[^?#]*)", re.IGNORECASE)
+_GITHUB_URL = re.compile(
+    r"^(?:(?:https?://)?(?:www\.)?github\.com/|git@github\.com:)(?P<path>[^?#]*)",
+    re.IGNORECASE,
+)
 _NUMBER = re.compile(r"^#?(?P<n>[1-9][0-9]*)$")
 
 
@@ -101,11 +111,11 @@ def check_claim(arg: str, origin: str) -> int:
 
     url = _GITHUB_URL.match(arg)
     if not url:
-        if "://" in arg or arg.lower().startswith(("git@", "github.com/", "www.github.com/")):
+        if "://" in arg or arg.lower().startswith("git@"):
             raise ClaimError(
                 "E-FOREIGN-REPO",
                 EXIT_FOREIGN_REPO,
-                f"{arg} is not a URL on the origin repo {origin}",
+                f"{arg} is not a GitHub URL, so it is not on the origin repo {origin}",
             )
         raise ClaimError(
             "E-NOT-AN-ISSUE",
diff --git a/tests/skills/test_issue_repo_resolution.py b/tests/skills/test_issue_repo_resolution.py
index e68e0bb7..7937055b 100644
--- a/tests/skills/test_issue_repo_resolution.py
+++ b/tests/skills/test_issue_repo_resolution.py
@@ -159,6 +159,11 @@ def test_bad_arguments_exit_2(tmp_path):
         ("https://github.com/IronbellyOrg/IronClaude/issues/302/", 302),  # trailing /
         ("https://github.com/IronbellyOrg/IronClaude/issues/302#issuecomment-9", 302),  # fragment
         ("https://github.com/IronbellyOrg/IronClaude/issues/302?x=1", 302),  # query
+        ("http://github.com/IronbellyOrg/IronClaude/issues/302", 302),  # http scheme
+        ("github.com/IronbellyOrg/IronClaude/issues/302", 302),  # no scheme
+        ("www.github.com/IronbellyOrg/IronClaude/issues/302", 302),  # no scheme, www.
+        ("https://www.github.com/IronbellyOrg/IronClaude/issues/302", 302),  # www.
+        ("git@github.com:IronbellyOrg/IronClaude/issues/302", 302),  # git@ form
     ],
 )
 def test_claim_on_origin_returns_issue_number(arg, number):
@@ -176,6 +181,10 @@ def test_claim_on_origin_returns_issue_number(arg, number):
         "https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999",
         "https://gitlab.com/IronbellyOrg/IronClaude/issues/1",  # not GitHub
         "https://github.com/IronbellyOrg",  # no repository
+        "github.com/octocat/Hello-World/issues/1",  # no scheme, foreign
+        "www.github.com/IronbellyOrg/IronClaudeX/issues/1",  # no scheme, prefix
+        "git@github.com:octocat/Hello-World.git",  # git@ form, foreign
+        "git@bitbucket.org:IronbellyOrg/IronClaude.git",  # git@ form, not GitHub
     ],
 )
 def test_claim_url_on_another_repo_is_e_foreign_repo(arg):
@@ -235,6 +244,8 @@ def test_digits_in_owner_and_repo_do_not_replace_the_issue_segment():
         "302abc",
         "https://github.com/IronbellyOrg/IronClaude/issues/abc",
         "https://github.com/IronbellyOrg/IronClaude/issues/302/comments",
+        "github.com/IronbellyOrg/IronClaude",  # origin, no scheme, no issue path
+        "git@github.com:IronbellyOrg/IronClaude.git",  # origin remote URL, no issue path
     ],
 )
 def test_other_arguments_are_not_an_issue(arg):

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B2 ac=T1.AC4 at=src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:104 anchor=src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:34 chk=n,y,n,n family=claim-url-schemeless fix=Normalize a scheme-less `github.com/...` or `www.github.com/...` argument to `https://` before the `_GITHUB_URL` match, so an origin URL resolves and a foreign one stays E-FOREIGN-REPO. Otherwise, change the docstring so it says scheme-less and `git@` arguments return E-FOREIGN-REPO, and add a test pinning that. covers="A claim URL for any repo other than origin stops with `E-FOREIGN-REPO`" first=A1 origin=new: I ran `check_claim("github.com/IronbellyOrg/IronClaude/issues/302", "IronbellyOrg/IronClaude")`. It raises E-FOREIGN-REPO with the message "... is not a URL on the origin repo IronbellyOrg/IronClaude", but that argument names the origin repo. The docstring sends such input to "anything else -> E-NOT-AN-ISSUE" (:34) and keeps E-FOREIGN-REPO for "a URL naming any other owner or repo". Both the message and the docstring are false for this input. It still fails closed (the claim stops before any GitHub write), so the harm is a wrong error code and message, not a write to a foreign repo.

Saved-probe re-check hit locations (may be empty): src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:18 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:19 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:20 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:21 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:25 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:28 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:33 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:34 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:36 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:41 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:49 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:68 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:71 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:105 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:114 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:116 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:129 src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:137 tests/skills/test_issue_repo_resolution.py:32 tests/skills/test_issue_repo_resolution.py:33 tests/skills/test_issue_repo_resolution.py:34 tests/skills/test_issue_repo_resolution.py:35 tests/skills/test_issue_repo_resolution.py:36 tests/skills/test_issue_repo_resolution.py:37 tests/skills/test_issue_repo_resolution.py:38 tests/skills/test_issue_repo_resolution.py:39 tests/skills/test_issue_repo_resolution.py:50 tests/skills/test_issue_repo_resolution.py:51 tests/skills/test_issue_repo_resolution.py:102 tests/skills/test_issue_repo_resolution.py:110 tests/skills/test_issue_repo_resolution.py:111 tests/skills/test_issue_repo_resolution.py:120 tests/skills/test_issue_repo_resolution.py:121 tests/skills/test_issue_repo_resolution.py:128 tests/skills/test_issue_repo_resolution.py:129 tests/skills/test_issue_repo_resolution.py:132 tests/skills/test_issue_repo_resolution.py:149 tests/skills/test_issue_repo_resolution.py:157 tests/skills/test_issue_repo_resolution.py:158 tests/skills/test_issue_repo_resolution.py:159 tests/skills/test_issue_repo_resolution.py:160 tests/skills/test_issue_repo_resolution.py:161 tests/skills/test_issue_repo_resolution.py:162 tests/skills/test_issue_repo_resolution.py:163 tests/skills/test_issue_repo_resolution.py:164 tests/skills/test_issue_repo_resolution.py:165 tests/skills/test_issue_repo_resolution.py:166 tests/skills/test_issue_repo_resolution.py:176 tests/skills/test_issue_repo_resolution.py:177 tests/skills/test_issue_repo_resolution.py:178 tests/skills/test_issue_repo_resolution.py:179 tests/skills/test_issue_repo_resolution.py:180 tests/skills/test_issue_repo_resolution.py:181 tests/skills/test_issue_repo_resolution.py:183 tests/skills/test_issue_repo_resolution.py:184 tests/skills/test_issue_repo_resolution.py:185 tests/skills/test_issue_repo_resolution.py:186 tests/skills/test_issue_repo_resolution.py:187 tests/skills/test_issue_repo_resolution.py:193 tests/skills/test_issue_repo_resolution.py:200 tests/skills/test_issue_repo_resolution.py:201 tests/skills/test_issue_repo_resolution.py:202 tests/skills/test_issue_repo_resolution.py:214 tests/skills/test_issue_repo_resolution.py:215 tests/skills/test_issue_repo_resolution.py:221 tests/skills/test_issue_repo_resolution.py:222 tests/skills/test_issue_repo_resolution.py:223 tests/skills/test_issue_repo_resolution.py:224 tests/skills/test_issue_repo_resolution.py:234 tests/skills/test_issue_repo_resolution.py:245 tests/skills/test_issue_repo_resolution.py:246 tests/skills/test_issue_repo_resolution.py:247 tests/skills/test_issue_repo_resolution.py:248 


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
