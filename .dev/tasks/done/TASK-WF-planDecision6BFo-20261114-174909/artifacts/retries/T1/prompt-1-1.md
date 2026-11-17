346414134dddf640e4873930a41b327ecce19f35
Review one task for spec compliance.

Task brief: ## Task 1: Add the plan-hash function and the `issue-pipeline` command group

Create `src/superclaude/cli/issue_pipeline/__init__.py`, `src/superclaude/cli/issue_pipeline/plan_hash.py` and `src/superclaude/cli/issue_pipeline/cli.py`, register the group as `issue-pipeline` in `src/superclaude/cli/main.py` next to the `issue_watch_group` registration (main.py:563-565), and add `tests/issue_pipeline/test_plan_hash.py`.

`plan_hash.compute(report_dir, names)` returns the SHA-256 over a named list of plan files. Names are relative to the report directory, sorted by their bytes, each file contributing its name, its length and its bytes (so moving bytes between two files changes the hash). It refuses an absolute name, a name with `..`, a symlink, a missing file and a file outside the directory. The `plan-hash <report-dir> <name>...` verb prints the file list and the hash; this is what the coordinator puts in the plan reply and what the worker recomputes.

Start condition: can start now.

Acceptance criteria:
- `uv run superclaude issue-pipeline plan-hash <dir> a.md b.md` prints the ordered file list and a 64-character lowercase hex hash, and the same inputs in a different argument order print the same hash.
- A test shows that changing one byte, renaming a file, swapping bytes between two files, or adding a file each change the hash.
- A test shows that a symlink, an absolute name, a `..` name and a missing file each exit non-zero with a closed reason and print no file text.
- `uv run pytest tests/issue_pipeline/test_plan_hash.py -v` passes, and a test in tests/cli confirms the `issue-pipeline` group is registered without changing any existing registration test.

AC ids (source order): T1.AC1 = bullet 1 of "Acceptance criteria"; T1.AC2 = bullet 2 of "Acceptance criteria"; T1.AC3 = bullet 3 of "Acceptance criteria"; T1.AC4 = bullet 4 of "Acceptance criteria"
Global constraints: ## Constraints

- Plan only. The owner approved this plan with fixes on 2026-11-15 and asked for the review changes on the same day; every owner decision in Task 19 is answered, and what stays open are facts the first live test must measure (Task 8), not decisions. Running `/sc:implement` from this plan still needs the owner's separate go. No push, PR, GitHub write or Orca write verb is authorized by this plan.
- This is Plan A of two. It holds only work that can run now, in this file order: Task 16 first (its own branch from origin/master, its own pull request later), then Tasks 1, 2, 8 (a document only), 3, 4, 5, 6, 7 and 19. Task numbers are stable across both plans, so they are not contiguous here. `/sc:implement` runs items in file order and ignores `Depends on` and `Start condition` text, so the order of the items is the gate. A `Depends on` line names only a task that appears earlier in this file. Plan B lives in its own package folder, `.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909-planB/plan-b-gated-tasks.md` (Tasks 20, 9, 10, 11, 12, 13, 14, 15, 17, 18). It opens with an owner-run gate item, the first live test recorded in docs/designs/issue-pipeline-fu1.md, and is not run from this file.
- Archive. Plan B sits in its own package folder, so archiving this plan's folder when it completes does not move Plan B.
- Owner input O-1 (not chosen by this plan): the number of one GitHub issue that the owner wrote, which Task 4 records real GitHub responses for. It is written by the owner into `tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md` as one line `ISSUE: <number>`. An executor that finds no such line stops at Task 4 and never picks an issue.
- Rebase first. This plan was written on base 0406ef5b0. origin/master is now d4d1662a8 and already holds PR #539 (sweep) and PR #548 (the D2 "claim-only" superseded note in docs/designs/issue-watcher.md). Every task below starts from a worktree based on current origin/master.
- Evidence for every factual claim is in ./artifacts/validation.md (read-only measurements, file and line citations, and what is UNVERIFIED). Real code locations are in ./artifacts/codegraph-grounding.md.
- Chosen claim-side change: B1b, the watcher claims with `--pipeline none` and the coordinator runs the existing `orca_worktree.py worktree` step, then `worker-start --worktree path:<that worktree>`. The owner confirmed it on 2026-11-14 and again on 2026-11-15 (Q35 = B1b; the first reply wrote "Q53 b1b" next to "2. Approved", read as Q35). B2, a new claim level, is not built.
- Owner answers: see Task 19.
- Owner decision Q34 (2026-11-14): the plan-writing worker runs without the launch-level guard (G1) for ONE test issue only. The written acceptance must cover the loss of the guard itself (no block on commit, push, merge, GitHub writes or /sc:implement), the owner writes that issue's text, and it is not stretched from the Decision 1 acceptance of permission checks off. Before any other issue runs through this flow, the guard is changed (G2, Plan B Tasks 13 to 15).
- Accepted earlier and carried here: only the coordinator tells the worker to proceed; one person-opened coordinator owns all watcher-claimed issues on this host with a lock per issue; nothing starts while the coordinator is down; one grant row per pipeline issue; one GitHub login on this host means an agent could apply the approval label or post the approval comment (Decision 4, accepted).
- New code goes in a new package `src/superclaude/cli/issue_pipeline/` and tests in `tests/issue_pipeline/`. The tests in tests/issue_watch/test_module_boundaries.py pin what each issue_watch module may import, and tests/issue_watch/test_no_text.py forbids a gh call that asks for comment text, so issue_pipeline imports from issue_watch and never the reverse.
- Never edit `.claude/` mirrors; edit `src/superclaude/` and run `make sync-dev`. Always stage `.dev/tasks` and the `src/` changes, never `.claude/`; commit only when the owner asks.
- The merged requirements file in the brainstorm folder is not edited by any task; Task 19 writes the change list for it inside this package.
- Every command is run with `uv run`.
Start sha: 346414134dddf640e4873930a41b327ecce19f35
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/__init__.py b/src/superclaude/cli/issue_pipeline/__init__.py
new file mode 100644
--- /dev/null
+++ b/src/superclaude/cli/issue_pipeline/__init__.py
@@ -0,0 +1,5 @@
+"""Issue pipeline: the approval core for a coordinator-started plan-writing worker.
+
+Imports from ``superclaude.cli.issue_watch``, never the reverse (the boundary is
+pinned by tests/issue_watch/test_module_boundaries.py).
+"""
diff --git a/src/superclaude/cli/issue_pipeline/cli.py b/src/superclaude/cli/issue_pipeline/cli.py
new file mode 100644
--- /dev/null
+++ b/src/superclaude/cli/issue_pipeline/cli.py
@@ -0,0 +1,33 @@
+"""The ``superclaude issue-pipeline`` command group.
+
+Verbs only sequence calls into the package and print closed result words; no
+verb prints file or GitHub text.
+"""
+
+from __future__ import annotations
+
+import click
+
+from . import plan_hash
+
+_EXIT_REFUSED = 1
+
+
+@click.group(name="issue-pipeline")
+def issue_pipeline_group() -> None:
+    """Approval core for a coordinator-started plan-writing worker."""
+
+
+@issue_pipeline_group.command("plan-hash")
+@click.argument("report_dir", type=click.Path())
+@click.argument("names", nargs=-1)
+def plan_hash_command(report_dir: str, names: tuple[str, ...]) -> None:
+    """Print the ordered plan file list and the plan hash of REPORT_DIR."""
+    try:
+        ordered, digest = plan_hash.compute(report_dir, list(names))
+    except plan_hash.PlanHashError as exc:
+        click.echo(f"refused:{exc.reason}")
+        raise SystemExit(_EXIT_REFUSED) from None
+    for name in ordered:
+        click.echo(f"file: {name}")
+    click.echo(f"plan-sha256: {digest}")
diff --git a/src/superclaude/cli/issue_pipeline/plan_hash.py b/src/superclaude/cli/issue_pipeline/plan_hash.py
new file mode 100644
--- /dev/null
+++ b/src/superclaude/cli/issue_pipeline/plan_hash.py
@@ -0,0 +1,90 @@
+"""The plan hash: one SHA-256 over a named list of plan files.
+
+The coordinator puts this hash in the plan reply and the worker recomputes it.
+Each file contributes its name, its length and its bytes, in the order of the
+names sorted by their bytes, so moving bytes between two files changes the hash.
+Nothing here ever returns or prints file text.
+"""
+
+from __future__ import annotations
+
+import hashlib
+import os
+from pathlib import Path, PurePosixPath
+
+
+class PlanHashError(Exception):
+    """A closed refusal. ``reason`` is one of ``REASONS``; it never holds file text."""
+
+    def __init__(self, reason: str) -> None:
+        super().__init__(reason)
+        self.reason = reason
+
+
+REASONS = (
+    "no-names",
+    "bad-dir",
+    "absolute-name",
+    "dotdot-name",
+    "bad-name",
+    "duplicate-name",
+    "symlink",
+    "missing",
+    "outside-dir",
+    "not-a-file",
+    "unreadable",
+)
+
+
+def _checked_names(names: list[str]) -> list[str]:
+    if not names:
+        raise PlanHashError("no-names")
+    seen: set[str] = set()
+    for name in names:
+        if not name or "\x00" in name or "\\" in name:
+            raise PlanHashError("bad-name")
+        if name.startswith("/"):
+            raise PlanHashError("absolute-name")
+        parts = PurePosixPath(name).parts
+        if ".." in parts:
+            raise PlanHashError("dotdot-name")
+        if name in seen:
+            raise PlanHashError("duplicate-name")
+        seen.add(name)
+    return sorted(names, key=lambda n: n.encode("utf-8"))
+
+
+def _read_plan_file(root: Path, name: str) -> bytes:
+    path = root / name
+    # Every component below the report directory must be a real one, no links.
+    current = root
+    for part in PurePosixPath(name).parts:
+        current = current / part
+        if current.is_symlink():
+            raise PlanHashError("symlink")
+    if not os.path.lexists(path):
+        raise PlanHashError("missing")
+    if not path.resolve().is_relative_to(root.resolve()):
+        raise PlanHashError("outside-dir")
+    if not path.is_file():
+        raise PlanHashError("not-a-file")
+    try:
+        return path.read_bytes()
+    except OSError:
+        raise PlanHashError("unreadable") from None
+
+
+def compute(report_dir: str | Path, names: list[str]) -> tuple[list[str], str]:
+    """Return the sorted file list and the 64-character lowercase hex hash."""
+    root = Path(report_dir)
+    if root.is_symlink() or not root.is_dir():
+        raise PlanHashError("bad-dir")
+    ordered = _checked_names(list(names))
+    digest = hashlib.sha256()
+    for name in ordered:
+        data = _read_plan_file(root, name)
+        raw = name.encode("utf-8")
+        # Length prefixes make the framing unambiguous.
+        digest.update(len(raw).to_bytes(8, "big") + raw)
+        digest.update(len(data).to_bytes(8, "big") + data)
+    return ordered, digest.hexdigest()
diff --git a/src/superclaude/cli/main.py b/src/superclaude/cli/main.py
--- a/src/superclaude/cli/main.py
+++ b/src/superclaude/cli/main.py
@@ -564,6 +564,10 @@ from superclaude.cli.issue_watch.cli import issue_watch_group  # noqa: E402,I001
 
 main.add_command(issue_watch_group, name="issue-watch")
 
+from superclaude.cli.issue_pipeline.cli import issue_pipeline_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
+
+main.add_command(issue_pipeline_group, name="issue-pipeline")
+
 from superclaude.cli.sweep import sweep_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
 
 main.add_command(sweep_group, name="sweep")
diff --git a/tests/cli/test_issue_pipeline_registered.py b/tests/cli/test_issue_pipeline_registered.py
new file mode 100644
--- /dev/null
+++ b/tests/cli/test_issue_pipeline_registered.py
@@ -0,0 +1,15 @@
+"""Task 1: the ``issue-pipeline`` group is registered on the main CLI."""
+
+from __future__ import annotations
+
+from click.testing import CliRunner
+
+from superclaude.cli.main import main
+
+
+def test_issue_pipeline_group_is_registered() -> None:
+    assert "issue-pipeline" in main.commands
+    assert "issue-watch" in main.commands  # the neighbouring registration is untouched
+    result = CliRunner().invoke(main, ["issue-pipeline", "--help"])
+    assert result.exit_code == 0
+    assert "plan-hash" in result.output
diff --git a/tests/issue_pipeline/__init__.py b/tests/issue_pipeline/__init__.py
new file mode 100644
diff --git a/tests/issue_pipeline/test_plan_hash.py b/tests/issue_pipeline/test_plan_hash.py
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/test_plan_hash.py
@@ -0,0 +1,108 @@
+"""Task 1: the plan hash and the ``issue-pipeline plan-hash`` verb."""
+
+from __future__ import annotations
+
+import re
+from pathlib import Path
+
+import pytest
+from click.testing import CliRunner
+
+from superclaude.cli.issue_pipeline import plan_hash
+from superclaude.cli.issue_pipeline.cli import issue_pipeline_group
+
+
+@pytest.fixture
+def report(tmp_path: Path) -> Path:
+    (tmp_path / "a.md").write_bytes(b"alpha")
+    (tmp_path / "b.md").write_bytes(b"beta")
+    return tmp_path
+
+
+def _hash(report: Path, *names: str) -> str:
+    return plan_hash.compute(report, list(names))[1]
+
+
+def test_cli_prints_ordered_list_and_a_64_hex_hash(report: Path) -> None:
+    result = CliRunner().invoke(issue_pipeline_group, ["plan-hash", str(report), "b.md", "a.md"])
+    assert result.exit_code == 0
+    lines = result.output.splitlines()
+    assert lines[:2] == ["file: a.md", "file: b.md"]
+    assert re.fullmatch(r"plan-sha256: [0-9a-f]{64}", lines[2])
+
+
+def test_argument_order_does_not_change_the_hash(report: Path) -> None:
+    assert _hash(report, "a.md", "b.md") == _hash(report, "b.md", "a.md")
+
+
+def test_one_byte_changes_the_hash(report: Path) -> None:
+    before = _hash(report, "a.md", "b.md")
+    (report / "a.md").write_bytes(b"alphb")
+    assert _hash(report, "a.md", "b.md") != before
+
+
+def test_rename_changes_the_hash(report: Path) -> None:
+    before = _hash(report, "a.md", "b.md")
+    (report / "a.md").rename(report / "c.md")
+    assert _hash(report, "c.md", "b.md") != before
+
+
+def test_swapping_bytes_between_two_files_changes_the_hash(report: Path) -> None:
+    before = _hash(report, "a.md", "b.md")
+    (report / "a.md").write_bytes(b"alphabeta"[:6])  # "alphab"
+    (report / "b.md").write_bytes(b"eta")
+    assert _hash(report, "a.md", "b.md") != before
+
+
+def test_adding_a_file_changes_the_hash(report: Path) -> None:
+    before = _hash(report, "a.md", "b.md")
+    (report / "c.md").write_bytes(b"")
+    assert _hash(report, "a.md", "b.md", "c.md") != before
+
+
+@pytest.mark.parametrize(
+    ("make", "name", "reason"),
+    [
+        ("symlink", "link.md", "symlink"),
+        ("none", "/etc/hostname", "absolute-name"),
+        ("none", "../a.md", "dotdot-name"),
+        ("none", "sub/../a.md", "dotdot-name"),
+        ("none", "missing.md", "missing"),
+        ("none", "a.md", "duplicate-name"),
+    ],
+)
+def test_refusals_exit_non_zero_with_a_closed_reason(report: Path, make: str, name: str, reason: str) -> None:
+    secret = report.parent / "outside-secret.txt"
+    secret.write_text("CANARY-FILE-TEXT")
+    if make == "symlink":
+        (report / "link.md").symlink_to(secret)
+    names = ["a.md", name] if reason == "duplicate-name" else [name]
+    result = CliRunner().invoke(issue_pipeline_group, ["plan-hash", str(report), *names])
+    assert result.exit_code != 0
+    assert result.output.strip() == f"refused:{reason}"
+    assert "CANARY" not in result.output
+
+
+def test_a_symlinked_directory_component_is_refused(report: Path, tmp_path_factory: pytest.TempPathFactory) -> None:
+    other = tmp_path_factory.mktemp("other")
+    (other / "x.md").write_text("x")
+    (report / "sub").symlink_to(other)
+    with pytest.raises(plan_hash.PlanHashError) as err:
+        plan_hash.compute(report, ["sub/x.md"])
+    assert err.value.reason == "symlink"
+
+
+def test_no_names_and_a_bad_directory_are_refused(report: Path) -> None:
+    with pytest.raises(plan_hash.PlanHashError) as err:
+        plan_hash.compute(report, [])
+    assert err.value.reason == "no-names"
+    with pytest.raises(plan_hash.PlanHashError) as err:
+        plan_hash.compute(report / "nope", ["a.md"])
+    assert err.value.reason == "bad-dir"
+
+
+def test_a_directory_is_not_a_plan_file(report: Path) -> None:
+    (report / "d").mkdir()
+    with pytest.raises(plan_hash.PlanHashError) as err:
+        plan_hash.compute(report, ["d"])
+    assert err.value.reason == "not-a-file"

Codegraph context
index_state: fresh
checked_at: 2026-11-16T21:51:31Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: ran on the Grep/Read floor.

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
