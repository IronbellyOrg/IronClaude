7114b38229b15731178aa31907f428f3f1345248
Review one task for spec compliance.

Task brief: ## Task 2: Define the approval line and add the `check-approval` verb

Depends on: Task 1

Create `src/superclaude/cli/issue_pipeline/approval_line.py` and add the verb to `src/superclaude/cli/issue_pipeline/cli.py`, with `tests/issue_pipeline/test_approval_line.py`.

One module owns the only two accepted approval texts: the short form `approved` and the long form `approved <record-id> plan-sha256=<64 hex>`, matched as the whole text with no trimming. The record id is `ap-<issue>-plan-<first 12 hex of the plan hash>`, so it is the same for the same (issue, stage, plan version). `check-approval <report-dir> <name>... --line "<text>"` is what the worker runs: it recomputes the hash with Task 1, returns `ok` for the long form only when the id and the hash both match, returns `refused:mismatch` for any other hash, and treats a bare `approved` as acceptable only for the comment channel (the coordinator, not the worker, converts it to the long form before it replies).

Start condition: can start now.

Acceptance criteria:
- A test table accepts `approved` and `approved ap-9-plan-0123456789ab plan-sha256=<64 hex>` and rejects every variant: leading or trailing space, upper case, a second line, a wrong id shape, a 63-character hash, a 65-character hash, and text after the hash.
- `check-approval` against a plan directory returns `ok` for the matching long form, `refused:mismatch` after one byte of a plan file changes, and `refused:bare` for a bare `approved` sent to the worker.
- No function in this module reads or prints anything except the closed result words.
- `uv run pytest tests/issue_pipeline/test_approval_line.py -v` passes.

AC ids (source order): T2.AC1 = bullet 1 of "Acceptance criteria"; T2.AC2 = bullet 2 of "Acceptance criteria"; T2.AC3 = bullet 3 of "Acceptance criteria"; T2.AC4 = bullet 4 of "Acceptance criteria"
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
Start sha: 7114b38229b15731178aa31907f428f3f1345248
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/approval_line.py b/src/superclaude/cli/issue_pipeline/approval_line.py
new file mode 100644
--- /dev/null
+++ b/src/superclaude/cli/issue_pipeline/approval_line.py
@@ -0,0 +1,58 @@
+"""The only two accepted approval texts, and the worker's ``check-approval``.
+
+The short form is ``approved``. The long form is
+``approved <record-id> plan-sha256=<64 hex>``, with the record id
+``ap-<issue>-plan-<first 12 hex of the plan hash>`` so it is the same for the
+same (issue, stage, plan version). Both are matched as the whole text with no
+trimming. This module returns closed result words only; it prints nothing and
+returns no file text.
+"""
+
+from __future__ import annotations
+
+import re
+from pathlib import Path
+
+from .plan_hash import PlanHashError, compute
+
+SHORT = "approved"
+_LONG = re.compile(r"approved (ap-([1-9][0-9]*)-plan-([0-9a-f]{12})) plan-sha256=([0-9a-f]{64})")
+
+OK = "ok"
+REFUSED_BARE = "refused:bare"
+REFUSED_MISMATCH = "refused:mismatch"
+REFUSED_MALFORMED = "refused:malformed"
+
+
+def record_id(issue: int, plan_hash: str) -> str:
+    return f"ap-{issue}-plan-{plan_hash[:12]}"
+
+
+def parse(text: str) -> tuple[str, str | None, str | None]:
+    """Return ``("short", None, None)``, ``("long", record_id, hash)`` or ``("none", None, None)``."""
+    if text == SHORT:
+        return ("short", None, None)
+    match = _LONG.fullmatch(text)
+    if match:
+        return ("long", match.group(1), match.group(4))
+    return ("none", None, None)
+
+
+def check(report_dir: str | Path, names: list[str], line: str, issue: int | None = None) -> str:
+    """Return one closed result word for the worker's approval line."""
+    kind, rid, claimed = parse(line)
+    if kind == "none":
+        return REFUSED_MALFORMED
+    if kind == "short":
+        return REFUSED_BARE  # a bare word is acceptable only for the comment channel
+    try:
+        _, digest = compute(report_dir, names)
+    except PlanHashError as exc:
+        return f"refused:{exc.reason}"
+    assert rid is not None and claimed is not None
+    expected_prefix = rid.rsplit("-", 1)[1]
+    if claimed != digest or expected_prefix != digest[:12]:
+        return REFUSED_MISMATCH
+    if issue is not None and not rid.startswith(f"ap-{issue}-plan-"):
+        return REFUSED_MISMATCH
+    return OK
diff --git a/src/superclaude/cli/issue_pipeline/cli.py b/src/superclaude/cli/issue_pipeline/cli.py
--- a/src/superclaude/cli/issue_pipeline/cli.py
+++ b/src/superclaude/cli/issue_pipeline/cli.py
@@ -8,7 +8,7 @@ from __future__ import annotations
 
 import click
 
-from . import plan_hash
+from . import approval_line, plan_hash
 
 _EXIT_REFUSED = 1
 
@@ -31,3 +31,16 @@ def plan_hash_command(report_dir: str, names: tuple[str, ...]) -> None:
     for name in ordered:
         click.echo(f"file: {name}")
     click.echo(f"plan-sha256: {digest}")
+
+
+@issue_pipeline_group.command("check-approval")
+@click.argument("report_dir", type=click.Path())
+@click.argument("names", nargs=-1)
+@click.option("--line", "line", required=True, help="The approval text, matched whole.")
+@click.option("--issue", type=click.IntRange(min=1), default=None, help="Also require this issue number in the record id.")
+def check_approval_command(report_dir: str, names: tuple[str, ...], line: str, issue: int | None) -> None:
+    """Print ok or a closed refusal for the approval LINE against the plan files."""
+    result = approval_line.check(report_dir, list(names), line, issue)
+    click.echo(result)
+    if result != approval_line.OK:
+        raise SystemExit(_EXIT_REFUSED)
diff --git a/tests/issue_pipeline/test_approval_line.py b/tests/issue_pipeline/test_approval_line.py
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/test_approval_line.py
@@ -0,0 +1,106 @@
+"""Task 2: the approval line and the ``check-approval`` verb."""
+
+from __future__ import annotations
+
+import inspect
+from pathlib import Path
+
+import pytest
+from click.testing import CliRunner
+
+from superclaude.cli.issue_pipeline import approval_line, plan_hash
+from superclaude.cli.issue_pipeline.cli import issue_pipeline_group
+
+H = "0123456789abcdef" * 4  # 64 hex
+RID = f"ap-9-plan-{H[:12]}"
+
+
+def _long(rid: str = RID, h: str = H) -> str:
+    return f"approved {rid} plan-sha256={h}"
+
+
+@pytest.mark.parametrize("text", ["approved", _long()])
+def test_the_two_accepted_texts(text: str) -> None:
+    assert approval_line.parse(text)[0] in ("short", "long")
+
+
+@pytest.mark.parametrize(
+    "text",
+    [
+        " approved",
+        "approved ",
+        "approved\n",
+        "Approved",
+        "APPROVED",
+        "approved\napproved",
+        " " + _long(),
+        _long() + " ",
+        _long() + "\n",
+        _long() + " extra",
+        _long() + "\nsecond line",
+        _long(rid="ap-x-plan-0123456789ab"),  # wrong id shape
+        _long(rid="ap-9-plan-0123456789a"),  # short id hex
+        _long(rid="ap-0-plan-0123456789ab"),  # issue starts with zero
+        _long(h=H[:63]),  # 63-character hash
+        _long(h=H + "0"),  # 65-character hash
+        _long(h=H.upper()),
+        "approved plan-sha256=" + H,
+        "",
+    ],
+)
+def test_every_variant_is_rejected(text: str) -> None:
+    assert approval_line.parse(text) == ("none", None, None)
+
+
+@pytest.fixture
+def plan_dir(tmp_path: Path) -> Path:
+    (tmp_path / "plan.md").write_text("the plan")
+    (tmp_path / "design.md").write_text("the design")
+    return tmp_path
+
+
+def _good_line(plan_dir: Path, issue: int = 9) -> str:
+    digest = plan_hash.compute(plan_dir, ["plan.md", "design.md"])[1]
+    return _long(approval_line.record_id(issue, digest), digest)
+
+
+def test_check_ok_for_the_matching_long_form(plan_dir: Path) -> None:
+    line = _good_line(plan_dir)
+    assert approval_line.check(plan_dir, ["plan.md", "design.md"], line) == "ok"
+    assert approval_line.check(plan_dir, ["plan.md", "design.md"], line, issue=9) == "ok"
+
+
+def test_check_refuses_after_one_byte_changes(plan_dir: Path) -> None:
+    line = _good_line(plan_dir)
+    (plan_dir / "plan.md").write_text("the plaN")
+    assert approval_line.check(plan_dir, ["plan.md", "design.md"], line) == "refused:mismatch"
+
+
+def test_check_refuses_a_bare_approved_from_the_worker(plan_dir: Path) -> None:
+    assert approval_line.check(plan_dir, ["plan.md", "design.md"], "approved") == "refused:bare"
+
+
+def test_check_refuses_a_wrong_issue_and_a_foreign_prefix(plan_dir: Path) -> None:
+    digest = plan_hash.compute(plan_dir, ["plan.md", "design.md"])[1]
+    assert approval_line.check(plan_dir, ["plan.md", "design.md"], _good_line(plan_dir), issue=10) == "refused:mismatch"
+    bad_prefix = _long(rid="ap-9-plan-ffffffffffff", h=digest)
+    assert approval_line.check(plan_dir, ["plan.md", "design.md"], bad_prefix) == "refused:mismatch"
+
+
+def test_check_closed_words_for_malformed_and_plan_errors(plan_dir: Path) -> None:
+    assert approval_line.check(plan_dir, ["plan.md"], "approve") == "refused:malformed"
+    assert approval_line.check(plan_dir, ["missing.md"], _long()) == "refused:missing"
+
+
+def test_cli_exit_codes_and_closed_output(plan_dir: Path) -> None:
+    runner = CliRunner()
+    ok = runner.invoke(issue_pipeline_group, ["check-approval", str(plan_dir), "plan.md", "design.md", "--line", _good_line(plan_dir)])
+    assert (ok.exit_code, ok.output.strip()) == (0, "ok")
+    bare = runner.invoke(issue_pipeline_group, ["check-approval", str(plan_dir), "plan.md", "design.md", "--line", "approved"])
+    assert (bare.exit_code, bare.output.strip()) == (1, "refused:bare")
+
+
+def test_the_module_prints_and_reads_nothing_itself() -> None:
+    source = inspect.getsource(approval_line)
+    for banned in ("print(", "open(", "read_text", "read_bytes", "stdout", "stderr"):
+        assert banned not in source, banned

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
