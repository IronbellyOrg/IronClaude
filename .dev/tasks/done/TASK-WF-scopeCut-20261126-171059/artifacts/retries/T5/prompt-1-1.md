1aec63c6b8c340fabceb4d511a4753af001cf679
Review one task for spec compliance.

Task brief: ## Task 5: Add the command line and main

Depends on: Task 4

Add `parse_args` and `main(argv=None, env=None, runner=None, now=None)` to `scripts/apply_org_rulesets.py` and the `if __name__ == "__main__"` guard, in the shape of `main` in `scripts/merged_pr_log.py` (line 622), as in source.md section 2. Options: `--org` (required, no default, through `check_org`), `--repo` (required, exactly one), `--out`, `--apply` and `--confirm`. Without `--apply` it builds a read-only runner and prints the dry-run report; with `--apply` it builds a runner that may POST and calls `apply_repo`, then prints the ids, the comment line and one rollback DELETE command per created id (on a failure, what was written before the stop). A runner passed in (tests) is used as given. Exit codes: `EXIT_OK`; `EXIT_USAGE` (64) for usage errors (a missing `--org` or `--repo`, the upstream org name, a list of repos, `--confirm` without `--apply`, `--apply` without `--confirm`); `EXIT_FAILED` (69) for a refusal or a failed step, with the failed check named on stderr.

Create `tests/org_rulesets/test_cli.py`.

Acceptance criteria:
- A missing `--org`, an upstream org name in any letter case, a missing `--repo`, two `--repo` values, `--apply` without `--confirm` and `--confirm` without `--apply` exit with `EXIT_USAGE`.
- A refusal in `--apply` exits with `EXIT_FAILED` and the stderr text names the failed check.
- A successful fake `--apply` prints the comment line and one DELETE command per created id; a read-back failure prints the one written id and exits `EXIT_FAILED`.
- A dry run of a synthetic repo through `main` exits `EXIT_OK`, prints the digest, and records no POST.
- A full fake run of a dry run and then `--apply --confirm <printed digest>` records, across all calls, only the allowed shapes: repo-scoped `gh api` calls name `<org>/<repo>` in full, none contains `SuperClaude-Org` in any letter case, and none writes to the ruleset ids 28081842, 28081844 or 28081845.
- `main` run with the working folder changed to an empty temporary folder finds the rule files and gives the same digest.
- The closing checks of the Constraints pass.

Global constraints: ## Constraints

- No task calls GitHub or touches any IronbellyGroup repo. Every GitHub call in a test goes through `FakeRunner` of `tests/org_rulesets/conftest.py`; no test starts the real `gh`.
- `.github/rulesets/*.json`, the commands in `docs/developer-guide/branch-protection.md` and `tests/docs/test_branch_protection_rulesets.py` stay unchanged. The only edit to the guide is the one link line of Task 7. The existing test must keep passing.
- Python 3.10, standard library only; ruff rules `E,F,I,N,W,TID` at line length 88 as set in `pyproject.toml`.
- No real private repo name and no real org login is written in any tracked file. Tests use synthetic names such as `acme-one`. The script holds no org or repo name, except the upstream org name it refuses.
- Only these paths may change: `scripts/apply_org_rulesets.py`, `tests/org_rulesets/`, `docs/developer-guide/branch-protection-multi-repo.md`, `docs/developer-guide/branch-protection.md` (one link line) and `docs/developer-guide/documentation-index.md`. Nothing under `.claude/` or `.github/` changes.
- "source.md section 2.3" names a heading of `./source.md`.
- Test setup follows `tests/worktree_cleanup/conftest.py` (the session fixture `wc` at lines 26 to 37 loads the script once; `RecordingRunner` at lines 68 to 109 subclasses the real `Runner` and overrides `_execute`). `tests/org_rulesets/conftest.py` defines the session fixture `orr` (the script module) and every shared fixture exactly once; a test module never imports a fixture from another module, because CI lists fixtures with `pytest --fixtures` and a duplicate crashes it.
- Location rule: the repo root is `Path(__file__).resolve().parent.parent`, the rule files are read from `<root>/.github/rulesets/`, and no function reads the current working folder. The before-state file is written into the folder given with `--out`.
- Choices for the owner's review (all are made inside the scope cut and listed in the pull request): one repo per run; the push check excuses no direct push by a named person; the tag ruleset is applied with a printed warning and a manual check of release workflows; rollback is manual.
- Every task ends with the same checks: `uv run pytest tests/org_rulesets/` passes (plus `tests/docs/test_branch_protection_rulesets.py` from Task 6 on), `uv run ruff check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing and `uv run ruff format --check scripts/apply_org_rulesets.py tests/org_rulesets` reports nothing.

Start sha: 1aec63c6b8c340fabceb4d511a4753af001cf679
Diff against the start snapshot: diff --git a/scripts/apply_org_rulesets.py b/scripts/apply_org_rulesets.py
index 6fa1917c7..3a0e24e79 100644
--- a/scripts/apply_org_rulesets.py
+++ b/scripts/apply_org_rulesets.py
@@ -12,11 +12,14 @@ The file holds the pure rendering and comparing functions and the command runner
 
 from __future__ import annotations
 
+import argparse
 import hashlib
 import json
 import os
 import re
 import subprocess
+import sys
+from collections.abc import Mapping
 from dataclasses import dataclass, field
 from datetime import datetime, timedelta, timezone
 from pathlib import Path
@@ -251,6 +254,8 @@ class Runner:
 
     read_only: bool = False
     commands: list[CommandRecord] = field(default_factory=list)
+    # The environment ``gh`` runs in (its token); None means this process's own.
+    env: Mapping[str, str] | None = None
 
     def check_allowed(self, argv: list[str], stdin: str | None = None) -> str | None:
         """Raise RefusedCommand unless ``argv`` is allowed. Return the ``name`` of the
@@ -299,7 +304,7 @@ class Runner:
         return self._execute(argv, stdin)
 
     def _execute(self, argv: list[str], stdin: str | None) -> Result:
-        env = dict(os.environ, GH_PROMPT_DISABLED="1")
+        env = dict(os.environ if self.env is None else self.env, GH_PROMPT_DISABLED="1")
         try:
             proc = subprocess.run(
                 argv,
@@ -804,3 +809,103 @@ def apply_repo(
     )
     result["rollback"] = rollback()
     return result
+
+
+# --- The command line ---------------------------------------------------------------
+
+
+class UsageError(Exception):
+    """A command-line mistake; ``main`` prints it and exits ``EXIT_USAGE``."""
+
+
+class _Parser(argparse.ArgumentParser):
+    def error(self, message):
+        raise UsageError(message)
+
+
+def parse_args(argv: list[str] | None) -> argparse.Namespace:
+    parser = _Parser(
+        prog="apply_org_rulesets",
+        description="Apply the IronClaude rulesets to one repo. Without --apply it is "
+        "a dry run that prints what would change and writes nothing.",
+        allow_abbrev=False,
+    )
+    parser.add_argument("--org", required=True, help="the organisation (no default)")
+    parser.add_argument(
+        "--repo",
+        required=True,
+        action="append",
+        help="the one repo to act on (one repo per run)",
+    )
+    parser.add_argument("--out", type=Path, help="folder for <repo>-before.json")
+    parser.add_argument("--apply", action="store_true", help="create the rulesets")
+    parser.add_argument(
+        "--confirm", metavar="DIGEST", help="the digest the dry run printed"
+    )
+    args = parser.parse_args(argv)
+    if (
+        len(args.repo) != 1
+        or args.repo[0] in (".", "..")
+        or not _SEGMENT.fullmatch(args.repo[0])
+    ):
+        raise UsageError("--repo takes exactly one repo name")
+    args.repo = args.repo[0]
+    try:
+        check_org(args.org)
+    except ValueError as exc:
+        raise UsageError(f"--org: {exc}") from exc
+    if args.confirm is not None and not args.apply:
+        raise UsageError("--confirm needs --apply")
+    if args.apply and not args.confirm:
+        raise UsageError("--apply needs --confirm DIGEST")
+    return args
+
+
+def _print_apply(result: dict) -> int:
+    lines = []
+    if result["before_file"]:
+        lines.append(f"before state saved: {result['before_file']}")
+    lines += [f"created: {n} (id {i})" for n, i in result["ids"].items()]
+    lines += [f"skipped, already present: {n}" for n in result["skipped"]]
+    if result["comment"]:
+        lines.append(f"comment for issue 838: {result['comment']}")
+    if result["rollback"]:
+        lines.append("rollback by hand, only if you need to undo this:")
+        lines += [f"  {command}" for command in result["rollback"]]
+    if lines:
+        print("\n".join(lines))
+    if result["ok"]:
+        return EXIT_OK
+    label = "failed" if result["before_file"] else "refused"
+    print(f"{label}: {result['error']}", file=sys.stderr)
+    return EXIT_FAILED
+
+
+def main(
+    argv: list[str] | None = None,
+    env: Mapping[str, str] | None = None,
+    runner: Runner | None = None,
+    now: datetime | None = None,
+) -> int:
+    try:
+        args = parse_args(argv)
+    except UsageError as exc:
+        print(f"usage error: {exc}", file=sys.stderr)
+        return EXIT_USAGE
+    now = now or datetime.now(timezone.utc)
+    runner = runner or Runner(read_only=not args.apply, env=env)
+    try:
+        if not args.apply:
+            lines = dry_run_report(runner, args.org, args.repo, now)
+            print("\n".join(lines))
+            planned = any(line.startswith("digest: ") for line in lines)
+            return EXIT_OK if planned else EXIT_FAILED
+        result = apply_repo(runner, args.org, args.repo, args.out, args.confirm, now)
+    except RefusedCommand as exc:
+        print(f"refused: {exc}", file=sys.stderr)
+        return EXIT_FAILED
+    return _print_apply(result)
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/tests/org_rulesets/conftest.py b/tests/org_rulesets/conftest.py
index e35c25af7..8c4d7186e 100644
--- a/tests/org_rulesets/conftest.py
+++ b/tests/org_rulesets/conftest.py
@@ -88,3 +88,65 @@ def fake_runner_cls(orr):
             return orr.Result(127, "", f"no canned reply for {argv}")
 
     return FakeRunner
+
+
+_REPO = "repos/acme/acme-one"
+_SERVER = {"source": "acme-one", "source_type": "Repository", "created_at": "2026"}
+
+
+def _activity(branch):
+    return f"{_REPO}/activity?ref=refs/heads/{branch}&time_period=quarter&per_page=100"
+
+
+@pytest.fixture
+def world(fake_runner_cls):
+    """A factory for a fake GitHub holding one repo, ``acme/acme-one``: default branch
+    ``master`` and an ``integration`` branch, no direct pushes, no protection, no
+    rulesets, two v* tags. ``gets`` replaces or adds canned GET answers (by path);
+    ``post`` replaces the POST answer; other keywords change the repo answer. A POST
+    stores the body under ids 101, 102, ... and ``GET rulesets/<id>`` returns it with
+    server keys added, as GitHub does."""
+    ok, http = fake_runner_cls.ok, fake_runner_cls.http
+
+    def build(*, gets=None, post=None, **repo_changes):
+        store = {}
+
+        def default_post(argv, stdin):
+            number = 101 + len(store)
+            store[number] = json.loads(stdin)
+            return ok({"id": number})
+
+        def readback(number):
+            def reply(argv, stdin):
+                return ok({**store[number], "id": number, **_SERVER})
+
+            return reply
+
+        repo = {
+            "owner": {"login": "acme"},
+            "name": "acme-one",
+            "archived": False,
+            "default_branch": "master",
+            "permissions": {"admin": True},
+            **repo_changes,
+        }
+        answers = {
+            _REPO: ok(repo),
+            f"{_REPO}/branches/master": ok({}),
+            f"{_REPO}/branches/integration": ok({}),
+            _activity("master"): ok([]),
+            _activity("integration"): ok([]),
+            f"{_REPO}/branches/master/protection": http(404),
+            f"{_REPO}/branches/integration/protection": http(404),
+            f"{_REPO}/rulesets?per_page=100": ok([]),
+            f"{_REPO}/git/matching-refs/tags/v?per_page=100": ok([{}, {}]),
+            **{f"{_REPO}/rulesets/{n}": readback(n) for n in range(101, 104)},
+            **(gets or {}),
+        }
+        replies = {("GET", path): answer for path, answer in answers.items()}
+        replies[("POST", f"{_REPO}/rulesets")] = post or default_post
+        runner = fake_runner_cls(replies)
+        runner.store = store
+        return runner
+
+    return build
diff --git a/tests/org_rulesets/test_apply.py b/tests/org_rulesets/test_apply.py
index 4dc37ca15..13e6e38bb 100644
--- a/tests/org_rulesets/test_apply.py
+++ b/tests/org_rulesets/test_apply.py
@@ -10,7 +10,6 @@ import pytest
 NOW = datetime(2026, 11, 26, 17, 0, tzinfo=timezone.utc)
 REPO = "repos/acme/acme-one"
 LIST = f"{REPO}/rulesets?per_page=100"
-TAGS = f"{REPO}/git/matching-refs/tags/v?per_page=100"
 SERVER = {"source": "acme-one", "source_type": "Repository", "created_at": "2026"}
 TAG_RULESET = "protect-release-tags"
 PUSH = {"activity_type": "push", "timestamp": "2026-10-01T10:00:00Z"}
@@ -20,57 +19,6 @@ def activity(branch):
     return f"{REPO}/activity?ref=refs/heads/{branch}&time_period=quarter&per_page=100"
 
 
-@pytest.fixture
-def world(fake_runner_cls):
-    """A factory for a fake GitHub holding one repo: default branch ``master`` and an
-    ``integration`` branch, no direct pushes, no protection, no rulesets, two v* tags.
-    ``gets`` replaces or adds canned GET answers; ``post`` replaces the POST answer."""
-    ok, http = fake_runner_cls.ok, fake_runner_cls.http
-
-    def build(*, gets=None, post=None, **repo_changes):
-        store = {}
-
-        def default_post(argv, stdin):
-            number = 101 + len(store)
-            store[number] = json.loads(stdin)
-            return ok({"id": number})
-
-        def readback(number):
-            def reply(argv, stdin):
-                return ok({**store[number], "id": number, **SERVER})
-
-            return reply
-
-        repo = {
-            "owner": {"login": "acme"},
-            "name": "acme-one",
-            "archived": False,
-            "default_branch": "master",
-            "permissions": {"admin": True},
-            **repo_changes,
-        }
-        answers = {
-            REPO: ok(repo),
-            f"{REPO}/branches/master": ok({}),
-            f"{REPO}/branches/integration": ok({}),
-            activity("master"): ok([]),
-            activity("integration"): ok([]),
-            f"{REPO}/branches/master/protection": http(404),
-            f"{REPO}/branches/integration/protection": http(404),
-            LIST: ok([]),
-            TAGS: ok([{}, {}]),
-            **{f"{REPO}/rulesets/{n}": readback(n) for n in range(101, 104)},
-            **(gets or {}),
-        }
-        replies = {("GET", path): answer for path, answer in answers.items()}
-        replies[("POST", f"{REPO}/rulesets")] = post or default_post
-        runner = fake_runner_cls(replies)
-        runner.store = store
-        return runner
-
-    return build
-
-
 def digest_of(orr):
     return orr.payload_digest(orr.plan_bodies(["master", "integration"]))
 
diff --git a/tests/org_rulesets/test_cli.py b/tests/org_rulesets/test_cli.py
new file mode 100644
index 000000000..1a5c5bbee
--- /dev/null
+++ b/tests/org_rulesets/test_cli.py
@@ -0,0 +1,168 @@
+"""parse_args and main: usage errors, exit codes, what is printed, the full fake run."""
+
+from __future__ import annotations
+
+import re
+import subprocess
+from datetime import datetime, timezone
+
+import pytest
+
+NOW = datetime(2026, 11, 26, 17, 0, tzinfo=timezone.utc)
+REPO = "repos/acme/acme-one"
+BASE = ["--org", "acme", "--repo", "acme-one"]
+SHAPE = re.compile(
+    r"^repos/acme/acme-one(/(branches/[\w./-]+|rulesets(/\d+)?|activity|commits"
+    r"|commits/[0-9a-f]+/pulls|git/matching-refs/tags/v))?(\?[\w=&:./-]+)?$"
+)
+
+
+def digest_of(orr):
+    return orr.payload_digest(orr.plan_bodies(["master", "integration"]))
+
+
+def run_main(orr, argv, runner, **kwargs):
+    return orr.main(argv, runner=runner, now=NOW, **kwargs)
+
+
+@pytest.mark.parametrize(
+    "argv",
+    [
+        [],
+        ["--repo", "acme-one"],
+        ["--org", "acme"],
+        ["--org", "SuperClaude-Org", "--repo", "acme-one"],
+        ["--org", "superclaude-org", "--repo", "acme-one"],
+        ["--org", "SUPERCLAUDE-ORG", "--repo", "acme-one"],
+        ["--org", "", "--repo", "acme-one"],
+        ["--org", "acme", "--repo", "a", "--repo", "b"],
+        ["--org", "acme", "--repo", "a,b"],
+        ["--org", "acme", "--repo", "a b"],
+        ["--org", "acme", "--repo", "acme/acme-one"],
+        [*BASE, "--apply"],
+        [*BASE, "--confirm", "abc"],
+        [*BASE, "--apply", "--confirm", ""],
+        [*BASE, "--surprise"],
+        [*BASE, "--app"],
+    ],
+)
+def test_usage_errors_exit_64_and_call_nothing(orr, world, capsys, argv):
+    runner = world()
+    assert run_main(orr, argv, runner) == orr.EXIT_USAGE == 64
+    assert "usage error" in capsys.readouterr().err
+    assert runner.executed == []
+
+
+def test_a_refusal_in_apply_exits_69_and_names_the_check(orr, world, capsys, tmp_path):
+    argv = [*BASE, "--out", str(tmp_path / "out"), "--apply", "--confirm", "0" * 64]
+    runner = world()
+    assert run_main(orr, argv, runner) == orr.EXIT_FAILED == 69
+    captured = capsys.readouterr()
+    assert "refused: confirm digest does not match" in captured.err
+    assert captured.out == ""
+    assert not any(c.stdin_name for c in runner.commands)
+
+
+def test_apply_without_out_is_a_refusal_not_a_usage_error(orr, world, capsys):
+    argv = [*BASE, "--apply", "--confirm", digest_of(orr)]
+    assert run_main(orr, argv, world()) == orr.EXIT_FAILED
+    assert "no --out folder" in capsys.readouterr().err
+
+
+def test_a_successful_apply_prints_the_comment_and_one_delete_per_id(
+    orr, world, capsys, tmp_path
+):
+    out = tmp_path / "out"
+    argv = [*BASE, "--out", str(out), "--apply", "--confirm", digest_of(orr)]
+    assert run_main(orr, argv, world()) == orr.EXIT_OK
+    text = capsys.readouterr().out
+    assert "comment for issue 838: Applied rulesets to acme/acme-one" in text
+    assert "protect-release-tags=101" in text and "protect-master=103" in text
+    deletes = [ln.strip() for ln in text.splitlines() if "--method DELETE" in ln]
+    assert sorted(deletes) == sorted(
+        f"gh api --method DELETE {REPO}/rulesets/{n}" for n in (101, 102, 103)
+    )
+    assert (out / "acme-one-before.json").exists()
+
+
+def test_a_read_back_failure_prints_the_one_written_id_and_exits_69(
+    orr, world, fake_runner_cls, capsys, tmp_path
+):
+    gets = {f"{REPO}/rulesets/101": fake_runner_cls.http(500)}
+    argv = [
+        *BASE,
+        "--out",
+        str(tmp_path / "out"),
+        "--apply",
+        "--confirm",
+        digest_of(orr),
+    ]
+    assert run_main(orr, argv, world(gets=gets)) == orr.EXIT_FAILED
+    captured = capsys.readouterr()
+    assert "created: protect-release-tags (id 101)" in captured.out
+    assert captured.out.count("--method DELETE") == 1
+    assert f"{REPO}/rulesets/101" in captured.out
+    assert "comment for issue 838" not in captured.out
+    assert "failed: read-back of protect-release-tags" in captured.err
+
+
+def test_a_dry_run_exits_0_prints_the_digest_and_never_posts(
+    orr, world, fake_runner_cls, capsys
+):
+    runner = world()
+    runner.read_only = True
+    assert run_main(orr, BASE, runner) == orr.EXIT_OK
+    assert f"digest: {digest_of(orr)}" in capsys.readouterr().out
+    assert all(fake_runner_cls.method_of(c.argv) == "GET" for c in runner.commands)
+
+
+def test_a_dry_run_of_an_unreadable_repo_exits_69(orr, world, fake_runner_cls, capsys):
+    runner = world(gets={REPO: fake_runner_cls.http(404)})
+    assert run_main(orr, BASE, runner) == orr.EXIT_FAILED
+    assert "no plan" in capsys.readouterr().out
+
+
+def test_the_full_fake_run_uses_only_allowed_shapes(
+    orr, world, fake_runner_cls, capsys, tmp_path
+):
+    runner = world()
+    assert run_main(orr, BASE, runner) == orr.EXIT_OK
+    printed = re.search(r"^digest: (\w+)$", capsys.readouterr().out, re.M).group(1)
+    argv = [*BASE, "--out", str(tmp_path / "out"), "--apply", "--confirm", printed]
+    assert run_main(orr, argv, runner) == orr.EXIT_OK
+    assert len(runner.commands) > 10
+    for record in runner.commands:
+        path = fake_runner_cls.path_of(record.argv)
+        assert record.argv[:2] == ["gh", "api"]
+        assert SHAPE.match(path), record.argv
+        text = " ".join(record.argv)
+        assert "superclaude-org" not in text.lower()
+        assert not any(str(i) in text for i in orr.PROTECTED_RULESET_IDS)
+        if fake_runner_cls.method_of(record.argv) != "GET":
+            assert path == f"{REPO}/rulesets" and record.stdin_name
+
+
+def test_main_finds_the_rule_files_from_any_working_folder(
+    orr, world, capsys, tmp_path, monkeypatch
+):
+    monkeypatch.chdir(tmp_path)
+    assert run_main(orr, BASE, world()) == orr.EXIT_OK
+    assert f"digest: {digest_of(orr)}" in capsys.readouterr().out
+    assert list(tmp_path.iterdir()) == []
+
+
+def test_main_builds_a_read_only_runner_for_a_dry_run_and_passes_env(
+    orr, monkeypatch, capsys
+):
+    seen = []
+
+    def stub(argv, **kwargs):
+        seen.append((argv, kwargs["env"]))
+        return subprocess.CompletedProcess(argv, 1, "", "gh: Not Found (HTTP 404)")
+
+    monkeypatch.setattr(subprocess, "run", stub)
+    code = orr.main(BASE, env={"GH_TOKEN": "t"}, now=NOW)
+    assert code == orr.EXIT_FAILED
+    assert seen[0][0] == ["gh", "api", REPO]
+    assert seen[0][1] == {"GH_TOKEN": "t", "GH_PROMPT_DISABLED": "1"}
+    assert "cannot be read" in capsys.readouterr().out

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
