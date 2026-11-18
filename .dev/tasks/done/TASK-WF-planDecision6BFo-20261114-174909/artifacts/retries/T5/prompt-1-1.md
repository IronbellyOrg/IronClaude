b607a62e841407c0ab8839c28b7cf84bb1c051f3
Review one task for spec compliance.

Task brief: ## Task 5: Add the GitHub reads that turn comment text into booleans

Depends on: Task 4

Create `src/superclaude/cli/issue_pipeline/reads.py` and `tests/issue_pipeline/test_reads.py`. The reads reuse `argv_events`, `argv_edits` (a fixed GraphQL query that `gh api graphql` sends as a POST, github.py:106-108 and :228-244) and the call budget of src/superclaude/cli/issue_watch/github.py (:218, :242, :437), build the comments argv with `_argv_rest_page(n, "comments", page, <new jq>)` as `argv_comments` does (:201-225), and add one comments projection in jq, in the same manner as `MARKER_JQ` (github.py:61): the body never leaves jq. The projection returns per comment the id, author login, author id, author type, created time, and three values computed inside jq: whether the whole body matches the short or long approval line, the record id and hash captured from a long line, and whether the body carries the plan-reply marker with its hash. Python re-validates every captured value against a fixed hex or id pattern before it is used.

Start condition: can start now; field names are pinned by the real recorded fixtures of Task 4 and re-checked in FU-1 (Task 8).

Acceptance criteria:
- A test runs the jq projection over the recorded comments file of Task 4 and shows every projected field is present with the expected type.
- A test with a hostile comment body (a canary string, markup, a very long line) shows the canary appears in no output, no argv and no file, in the same way as tests/issue_watch/test_no_text.py, and a second test shows the new gh argv asks for no body field.
- A test shows the jq projection returns `matches_approval_line: true` only for the two exact forms, and returns false for trailing newline, trailing space, a quoted line and a reply that merely contains the word approved.
- A test shows the call cap and page cap of `CallBudget` are respected across the events, comments and edits reads, and a transient gh failure returns a closed reason instead of a partial approval.
- `uv run pytest tests/issue_pipeline/test_reads.py -v` passes.

AC ids (source order): T5.AC1 = bullet 1 of "Acceptance criteria"; T5.AC2 = bullet 2 of "Acceptance criteria"; T5.AC3 = bullet 3 of "Acceptance criteria"; T5.AC4 = bullet 4 of "Acceptance criteria"; T5.AC5 = bullet 5 of "Acceptance criteria"
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
Start sha: b607a62e841407c0ab8839c28b7cf84bb1c051f3
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/reads.py b/src/superclaude/cli/issue_pipeline/reads.py
new file mode 100644
--- /dev/null
+++ b/src/superclaude/cli/issue_pipeline/reads.py
@@ -0,0 +1,159 @@
+"""GitHub reads that turn comment text into booleans and ids (plan Task 5).
+
+The reads reuse ``argv_events``, ``argv_edits`` (a fixed GraphQL query that ``gh api
+graphql`` sends as a POST) and the call budget and page cap of
+``superclaude.cli.issue_watch.github``. The comments argv is built with
+``_argv_rest_page(n, "comments", page, COMMENTS_JQ)`` as ``argv_comments`` does, with one
+new jq projection in the manner of ``MARKER_JQ``: the body never leaves jq. Per comment it
+returns the id, author login, author id, author type, created time and values computed
+inside jq (whether the whole body matches an approval form, the record id and hash of a long
+form, and the plan-reply marker with its hash). Python re-validates every captured value
+against a fixed pattern before it is used.
+
+Portability note: ``gh --jq`` runs gojq, not jq. The projection uses only ``test``, ``scan``,
+``split``, ``ltrimstr``, ``\\A`` and ``\\z`` with no named groups, which both accept; FU-1
+(precondition j) re-checks it against a live reply.
+"""
+
+from __future__ import annotations
+
+import re
+from collections.abc import Callable
+from dataclasses import dataclass
+
+from superclaude.cli.issue_watch import github as gh
+from superclaude.cli.issue_watch.github import (
+    CallBudget,
+    Read,
+    _argv_rest_page,
+    _check,
+    _pos_int,
+    _rest_read,
+    _text,
+    _time,
+)
+from superclaude.cli.issue_watch.predicates import EditEvidence, LabelEvent
+from superclaude.cli.issue_watch.runner import Runner
+
+from .stage_predicates import CommentFact, PlanMarker
+
+_RECORD_ID = r"ap-[1-9][0-9]*-plan-[0-9a-f]{12}"
+_LONG_LINE = rf"\\Aapproved {_RECORD_ID} plan-sha256=[0-9a-f]{{64}}\\z"
+_MARKER = rf"<!-- sc:stage:plan id={_RECORD_ID} plan=[0-9a-f]{{64}} -->"
+
+COMMENTS_JQ = (
+    '[.[] | (.body // "") as $b'
+    f' | ($b | test("{_LONG_LINE}")) as $long'
+    f' | ([$b | scan("{_MARKER}")] | first) as $m'
+    " | {id, login: .user.login, user_id: .user.id, user_type: .user.type, created_at,"
+    ' matches_approval_line: ($b == "approved" or $long),'
+    ' approval_form: (if $b == "approved" then "short" elif $long then "long" else null end),'
+    ' approval_record_id: (if $long then ($b | split(" ")[1]) else null end),'
+    ' approval_hash: (if $long then ($b | split("=")[1]) else null end),'
+    ' plan_marker_record_id: (if $m then ($m | split(" ")[2] | ltrimstr("id=")) else null end),'
+    ' plan_marker_hash: (if $m then ($m | split(" ")[3] | ltrimstr("plan=")) else null end)}]'
+)
+"""The comments projection: the body becomes booleans and fixed-pattern ids."""
+
+_RECORD_ID_RE = re.compile(_RECORD_ID)
+_HASH_RE = re.compile(r"[0-9a-f]{64}")
+_LOGIN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}(\[bot\])?")
+_TYPE_RE = re.compile(r"[A-Za-z]{1,20}")
+COMMENTS_UNREADABLE = "comments_unreadable"
+
+
+def argv_comments_projected(n: int, page: int) -> list[str]:
+    """One REST page of the issue's comments, reduced by ``COMMENTS_JQ``."""
+    return _argv_rest_page(n, "comments", page, COMMENTS_JQ)
+
+
+def _pattern_or_none(value: object, pattern: re.Pattern[str]) -> str | None:
+    if value is None:
+        return None
+    text = _text(value)
+    _check(pattern.fullmatch(text) is not None)
+    return text
+
+
+def _comment_fact(item: dict) -> CommentFact:
+    """One projected comment, every captured value re-validated (a bad shape is malformed)."""
+    form = item.get("approval_form")
+    _check(form in (None, "short", "long"))
+    _check(type(item.get("matches_approval_line")) is bool)
+    _check(item["matches_approval_line"] == (form is not None))
+    record_id = _pattern_or_none(item.get("approval_record_id"), _RECORD_ID_RE)
+    digest = _pattern_or_none(item.get("approval_hash"), _HASH_RE)
+    _check((form == "long") == (record_id is not None and digest is not None))
+    marker_id = _pattern_or_none(item.get("plan_marker_record_id"), _RECORD_ID_RE)
+    marker_hash = _pattern_or_none(item.get("plan_marker_hash"), _HASH_RE)
+    _check((marker_id is None) == (marker_hash is None))
+    user_id = item.get("user_id")
+    _check(user_id is None or (type(user_id) is int and user_id > 0))
+    return CommentFact(
+        id=_pos_int(item.get("id")),
+        author_login=_pattern_or_none(item.get("login"), _LOGIN_RE),
+        author_id=user_id,
+        author_type=_pattern_or_none(item.get("user_type"), _TYPE_RE),
+        created_at=_time(item.get("created_at")),
+        approval_form=form,
+        approval_record_id=record_id,
+        approval_hash=digest,
+        plan_marker=PlanMarker(marker_id, marker_hash) if marker_id and marker_hash else None,
+    )
+
+
+def comments(
+    runner: Runner, budget: CallBudget, n: int, timeout_for: Callable[[], float | None]
+) -> Read:
+    """A tuple of ``CommentFact`` for the issue's comments; every failure is ``comments_unreadable``."""
+    return _rest_read(
+        runner,
+        budget,
+        timeout_for,
+        lambda page: argv_comments_projected(n, page),
+        _comment_fact,
+        COMMENTS_UNREADABLE,
+        COMMENTS_UNREADABLE,
+        False,
+    )
+
+
+@dataclass(frozen=True)
+class StageEvidence:
+    comments: tuple[CommentFact, ...]
+    events: tuple[LabelEvent, ...]
+    edits: EditEvidence
+
+
+def read_stage_evidence(
+    runner: Runner,
+    n: int,
+    timeout_for: Callable[[], float | None],
+    budget: CallBudget | None = None,
+) -> Read:
+    """Read events, comments and edits under one ``CallBudget``.
+
+    Returns ``Read(StageEvidence)``, or the first failed ``Read`` (value None, a closed
+    reason): a partial read never yields an approval.
+    """
+    budget = budget or CallBudget()
+    events = gh.events(runner, budget, n, timeout_for)
+    if events.value is None:
+        return events
+    found = comments(runner, budget, n, timeout_for)
+    if found.value is None:
+        return found
+    edits = gh.edits(runner, budget, n, timeout_for)
+    if edits.value is None:
+        return edits
+    return Read(StageEvidence(found.value, events.value, edits.value))  # type: ignore[arg-type]
+
+
+__all__ = [
+    "COMMENTS_JQ",
+    "COMMENTS_UNREADABLE",
+    "StageEvidence",
+    "argv_comments_projected",
+    "comments",
+    "read_stage_evidence",
+]
diff --git a/tests/issue_pipeline/test_reads.py b/tests/issue_pipeline/test_reads.py
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/test_reads.py
@@ -0,0 +1,215 @@
+"""Task 5: the GitHub reads that turn comment text into booleans."""
+
+from __future__ import annotations
+
+import json
+import shutil
+import subprocess
+from pathlib import Path
+
+import pytest
+
+from superclaude.cli.issue_pipeline import reads
+from superclaude.cli.issue_watch import github as gh
+from superclaude.cli.issue_watch.runner import CommandResult
+
+RECORDED = Path(__file__).parent / "fixtures" / "recorded"
+CANARY = "CANARY-9f3a-DO-NOT-LEAK"
+H = "a" * 64
+RID = "ap-9-plan-" + H[:12]
+LONG = f"approved {RID} plan-sha256={H}"
+
+pytestmark = pytest.mark.skipif(shutil.which("jq") is None, reason="jq is needed to run the projection")
+
+
+def jq(program: str, document: object) -> str:
+    done = subprocess.run(["jq", "-c", program], input=json.dumps(document), capture_output=True, text=True, check=True)
+    return done.stdout
+
+
+def project(bodies: list[str | None]) -> list[dict]:
+    raw = [
+        {"id": i + 1, "user": {"login": "u", "id": 5, "type": "User"}, "created_at": "2026-11-16T10:00:00Z", "body": b}
+        for i, b in enumerate(bodies)
+    ]
+    return json.loads(jq(reads.COMMENTS_JQ, raw))
+
+
+def ok(stdout: str) -> CommandResult:
+    return CommandResult(("gh",), 0, stdout, "", False, None, 0.0)
+
+
+def failed(stderr: str = "HTTP 502: Bad Gateway") -> CommandResult:
+    return CommandResult(("gh",), 1, "", stderr, False, None, 0.0)
+
+
+class Served:
+    """A runner that answers each call from ``answer(argv)`` and keeps every argv and reply."""
+
+    def __init__(self, answer) -> None:
+        self.answer = answer
+        self.argvs: list[list[str]] = []
+        self.replies: list[CommandResult] = []
+
+    def run(self, argv, timeout, *, cwd=None) -> CommandResult:
+        self.argvs.append(list(argv))
+        reply = self.answer(list(argv))
+        self.replies.append(reply)
+        return reply
+
+
+def never_expires() -> float:
+    return 30.0
+
+
+# --- the projection over the recorded file -------------------------------------
+
+
+def test_projection_over_the_recorded_comments_has_every_field_with_its_type() -> None:
+    raw = json.loads((RECORDED / "comments-page1.json").read_text())
+    rows = json.loads(jq(reads.COMMENTS_JQ, raw))
+    assert len(rows) == len(raw) > 0
+    for row in rows:
+        assert isinstance(row["id"], int) and isinstance(row["user_id"], int)
+        assert isinstance(row["login"], str) and isinstance(row["user_type"], str)
+        assert isinstance(row["created_at"], str) and isinstance(row["matches_approval_line"], bool)
+        assert row["approval_form"] is None and row["approval_record_id"] is None and row["approval_hash"] is None
+        assert row["plan_marker_record_id"] is None and row["plan_marker_hash"] is None
+    facts = [reads._comment_fact(row) for row in rows]  # Python re-validates every row
+    assert [f.id for f in facts] == [c["id"] for c in raw]
+
+
+# --- the exact forms -----------------------------------------------------------
+
+
+def test_matches_approval_line_only_for_the_two_exact_forms() -> None:
+    bodies = ["approved", LONG, "approved\n", "approved ", " approved", "> approved", f"> {LONG}", "I approved this", LONG + "\n", LONG + " x", "Approved", None]
+    rows = project(bodies)
+    assert [r["matches_approval_line"] for r in rows] == [True, True] + [False] * 10
+    assert rows[0]["approval_form"] == "short" and rows[1]["approval_form"] == "long"
+    assert rows[1]["approval_record_id"] == RID and rows[1]["approval_hash"] == H
+    assert all(r["approval_record_id"] is None for i, r in enumerate(rows) if i != 1)
+
+
+def test_the_plan_marker_is_read_with_its_hash() -> None:
+    rows = project([f"intro\n<!-- sc:stage:plan id={RID} plan={H} -->\nmore", "<!-- sc:stage:plan id=bad plan=x -->"])
+    assert (rows[0]["plan_marker_record_id"], rows[0]["plan_marker_hash"]) == (RID, H)
+    assert rows[1]["plan_marker_record_id"] is None
+
+
+# --- no text ------------------------------------------------------------------
+
+
+def test_the_new_argv_asks_for_no_body_field() -> None:
+    argv = reads.argv_comments_projected(452, 1)
+    assert argv[:5] == ["gh", "api", "--method", "GET", "repos/IronbellyOrg/IronClaude/issues/452/comments"]
+    for banned in ("--json", "--template", "-t", "bodyText", "bodyHTML"):
+        assert banned not in argv
+    assert "body:" not in reads.COMMENTS_JQ.replace(" ", "")  # no output key named body
+    keys = set(project(["x"])[0])
+    assert not keys & {"body", "title", "text", "message"}
+
+
+def test_a_hostile_body_never_reaches_output_argv_result_or_a_file(tmp_path: Path, monkeypatch) -> None:
+    monkeypatch.chdir(tmp_path)
+    hostile = [
+        f"{CANARY} <script>alert(1)</script> [x](javascript:y)",
+        CANARY * 5000 + "\n" + LONG,
+        f"<!-- sc:stage:plan id={RID} plan={H} -->{CANARY}",
+        "‮" + CANARY,
+    ]
+    raw = [
+        {"id": i + 1, "user": {"login": "u", "id": 5, "type": "User"}, "created_at": "2026-11-16T10:00:00Z", "body": b}
+        for i, b in enumerate(hostile)
+    ]
+    projected = jq(reads.COMMENTS_JQ, raw)
+    assert CANARY not in projected
+    runner = Served(lambda argv: ok(projected))
+    out = reads.comments(runner, gh.CallBudget(), 452, never_expires)
+    assert out.reason is None and len(out.value) == 4
+    assert CANARY not in repr(out) and CANARY not in " ".join(" ".join(a) for a in runner.argvs)
+    assert all(CANARY not in r.stdout + r.stderr for r in runner.replies)
+    assert list(tmp_path.iterdir()) == []  # nothing was written
+
+
+@pytest.mark.parametrize("field", ["approval_hash", "approval_record_id", "plan_marker_hash", "login", "user_type"])
+def test_python_rejects_a_captured_value_that_breaks_its_pattern(field: str) -> None:
+    row = project([LONG])[0]
+    row[field] = "not valid\n" if field in ("login", "user_type") else "ZZ" + CANARY
+    if field == "plan_marker_hash":
+        row["plan_marker_record_id"] = RID
+    with pytest.raises(gh._Malformed):
+        reads._comment_fact(row)
+    served = Served(lambda argv: ok(json.dumps([row])))
+    result = reads.comments(served, gh.CallBudget(), 9, never_expires)
+    assert result.value is None and result.reason == "comments_unreadable"
+
+
+# --- budget, page cap, failure --------------------------------------------------
+
+
+def _page(n_items: int, offset: int = 0) -> str:
+    return json.dumps([{"id": offset + i + 1, "login": "u", "user_id": 5, "user_type": "User", "created_at": "2026-11-16T10:00:00Z",
+                        "matches_approval_line": False, "approval_form": None, "approval_record_id": None, "approval_hash": None,
+                        "plan_marker_record_id": None, "plan_marker_hash": None} for i in range(n_items)])
+
+
+def test_page_cap_stops_a_comment_read_that_never_ends() -> None:
+    # every page is full with fresh ids, so only the page cap ends the read: incomplete, never partial
+    def answer(argv: list[str]) -> CommandResult:
+        page = int(next(a for a in argv if a.startswith("page=")).split("=")[1])
+        return ok(_page(gh.PAGE_SIZE, offset=page * 1000))
+
+    runner = Served(answer)
+    result = reads.comments(runner, gh.CallBudget(), 9, never_expires)
+    assert result.value is None and result.reason == "comments_unreadable"
+    assert len(runner.argvs) == gh.PAGE_CAP
+
+
+def test_call_cap_is_shared_across_events_comments_and_edits() -> None:
+    budget = gh.CallBudget()
+    budget.calls = gh.CALL_CAP - gh.RESERVED_CALLS - 2  # room for two per-issue calls only
+    recorded = {"events": _recorded_events(), "comments": _page(1)}
+
+    def answer(argv: list[str]) -> CommandResult:
+        return ok(recorded["events"] if argv[4].endswith("/events") else recorded["comments"])
+
+    runner = Served(answer)
+    out = reads.read_stage_evidence(runner, 452, never_expires, budget)
+    assert out.value is None and out.reason == "budget_exhausted"
+    assert budget.calls <= gh.CALL_CAP - gh.RESERVED_CALLS
+    assert len(runner.argvs) == 2  # the third read never ran
+
+
+def _recorded_events() -> str:
+    return jq(gh.EVENTS_JQ, json.loads((RECORDED / "events-page1.json").read_text()))
+
+
+def test_a_transient_gh_failure_returns_a_closed_reason_not_a_partial_approval() -> None:
+    def answer(argv: list[str]) -> CommandResult:
+        if argv[4].endswith("/events"):
+            return ok(_recorded_events())
+        return failed()
+
+    out = reads.read_stage_evidence(Served(answer), 452, never_expires)
+    assert out.value is None and out.reason == "comments_unreadable"
+    first = reads.read_stage_evidence(Served(lambda argv: failed()), 452, never_expires)
+    assert first.value is None and first.reason == "events_unreadable"
+
+
+def test_the_whole_read_over_the_recorded_files_succeeds() -> None:
+    raw_comments = json.loads((RECORDED / "comments-page1.json").read_text())
+    edits = (RECORDED / "edits-page1.json").read_text()
+
+    def answer(argv: list[str]) -> CommandResult:
+        if argv[:3] == ["gh", "api", "graphql"]:
+            return ok(edits)
+        if argv[4].endswith("/events"):
+            return ok(_recorded_events())
+        assert argv[4].endswith("/comments")
+        return ok(jq(reads.COMMENTS_JQ, raw_comments))
+
+    out = reads.read_stage_evidence(Served(answer), 452, never_expires)
+    assert out.reason is None
+    evidence = out.value
+    assert len(evidence.comments) == len(raw_comments) and evidence.events and evidence.edits.comments

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
