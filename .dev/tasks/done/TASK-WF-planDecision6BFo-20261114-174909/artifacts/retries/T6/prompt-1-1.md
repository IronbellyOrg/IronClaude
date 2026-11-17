c170a5270bf0141479d0f900019b474798ce17d5
Review one task for spec compliance.

Task brief: ## Task 6: Add the read-only `stage-status` command

Depends on: Task 3, Task 4, Task 5

Add the `stage-status <issue> --json` verb to src/superclaude/cli/issue_pipeline/cli.py with `tests/issue_pipeline/test_stage_status.py`. It reads GitHub through Task 5, applies Task 4, looks up the row of Task 3, and prints a closed set of keys: the latest plan hash and plan reply id, the approvals found per channel with their reason codes, the row state, and the flags from Task 4. It writes nothing to GitHub, the row store or Orca, and it prints no GitHub text.

Start condition: can start now.

Acceptance criteria:
- A test feeds the recorded events, comments and edits files of Task 4 through the injected runner and shows `stage-status` prints only closed keys for that issue.
- A test table covers: no plan reply yet; plan reply and no approval; label only; comment only; label and comment (one key, one row); plan changed after approval; approval label removed; approver not listed; every case prints only closed keys and values.
- A test, run over the real argv builders of Task 5 and the watcher's `argv_edits`, shows the command never passes a `--method` other than GET, never calls a mutation or a write endpoint (the fixed GraphQL queries are allowed, as tests/issue_watch/test_security_invariants.py:239-241 already allows them), and never calls `orca`, by asserting over the recorded argv of the injected runner.
- `uv run pytest tests/issue_pipeline/test_stage_status.py -v` passes and `uv run superclaude issue-pipeline stage-status --help` exits 0.

AC ids (source order): T6.AC1 = bullet 1 of "Acceptance criteria"; T6.AC2 = bullet 2 of "Acceptance criteria"; T6.AC3 = bullet 3 of "Acceptance criteria"; T6.AC4 = bullet 4 of "Acceptance criteria"
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
Start sha: c170a5270bf0141479d0f900019b474798ce17d5
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/cli.py b/src/superclaude/cli/issue_pipeline/cli.py
--- a/src/superclaude/cli/issue_pipeline/cli.py
+++ b/src/superclaude/cli/issue_pipeline/cli.py
@@ -8,13 +8,20 @@ from __future__ import annotations
 
 import json
 from collections.abc import Callable
+from pathlib import Path
 from typing import Any
 
 import click
 
-from . import approval_line, approval_record, plan_hash
+from superclaude.cli.issue_watch import cycle
+from superclaude.cli.issue_watch import github as gh
+from superclaude.cli.issue_watch.runner import Runner, SubprocessRunner
+
+from . import approval_line, approval_record, plan_hash, reads, stage_predicates
 
 _EXIT_REFUSED = 1
+_EXIT_CONFIG = 2
+_GH_TIMEOUT_S = 60.0
 _EXIT_LOCK_HELD = 75  # the watcher's own code for a held lock
 
 
@@ -138,3 +145,143 @@ def record_show_command(approvals_dir: str, issue: int, stage: str, plan_hash_va
 def record_mark_command(approvals_dir: str, issue: int, stage: str, plan_hash_value: str, state: str) -> None:
     """Move the approval row forward (`instructed`, `acked`) or to `revoked`."""
     _run_record(lambda: approval_record.record_mark(approvals_dir, issue, stage, plan_hash_value, state))
+
+
+# --- stage-status: read-only -------------------------------------------------
+
+
+def _make_runner() -> Runner:
+    """The one place a real ``gh`` runner is made (tests replace it)."""
+    return SubprocessRunner()
+
+
+def _load_stage_inputs(config_path: Path) -> tuple[str, frozenset[int]]:
+    """The approval label and the approver ids of the watcher's configuration."""
+    config = cycle.load_config(config_path)
+    return config.approval_label, cycle.validate_approvers(config.approvers_file)
+
+
+def _timeout() -> float | None:
+    return _GH_TIMEOUT_S
+
+
+def _channel(result: stage_predicates.ChannelResult) -> dict[str, Any]:
+    return {
+        "accepted": result.accepted,
+        "reason": result.reason,
+        "evidence_id": result.evidence_id,
+        "actor_id": result.actor_id,
+        "actor_is_host_login": result.actor_is_host_login,
+    }
+
+
+def _row_facts(approvals_dir: Path | None, issue: int, key: tuple[int, str, str] | None) -> tuple[str | None, int | None, str | None]:
+    """Adoption state, approval-row state and its evidence count, read without writing."""
+    if approvals_dir is None:
+        return None, None, None
+    try:
+        adoption = approval_record.adopt_show(approvals_dir, issue, stage_predicates.STAGE)["state"]
+    except approval_record.ApprovalError:
+        adoption = None
+    if key is None:
+        return adoption, None, None
+    try:
+        row = approval_record.record_show(approvals_dir, issue, key[1], key[2])
+    except approval_record.ApprovalError:
+        return adoption, None, None
+    return adoption, len(row["evidence"]), row["state"]
+
+
+def _stage_status(
+    issue: int,
+    runner: Runner,
+    label: str,
+    approvers: frozenset[int],
+    approvals_dir: Path | None,
+    plan_dir: Path | None,
+    plan_names: list[str],
+) -> dict[str, Any]:
+    budget = gh.CallBudget()
+    login = gh.user(runner, _timeout)
+    if login.value is None:
+        raise _StatusRefused(login.reason)
+    snapshot = gh.reread(runner, budget, issue, _timeout)
+    if snapshot.value is None:
+        raise _StatusRefused(snapshot.reason)
+    evidence = reads.read_stage_evidence(runner, issue, _timeout, budget)
+    if evidence.value is None:
+        raise _StatusRefused(evidence.reason)
+    host = login.value.login
+    checked = plan_dir is not None and bool(plan_names)
+    if checked:
+        try:
+            now: str | None = plan_hash.compute(plan_dir, plan_names)[1]
+        except plan_hash.PlanHashError:
+            now = None  # an unreadable plan counts as changed
+    else:
+        latest = stage_predicates.latest_plan_reply(evidence.value.comments, host)
+        now = latest.plan_marker.plan_hash if latest and latest.plan_marker else None
+    status = stage_predicates.evaluate(
+        issue,
+        evidence.value.comments,
+        evidence.value.events,
+        evidence.value.edits,
+        plan_hash_now=now,
+        host_login=host,
+        assignees=snapshot.value.assignees,
+        approvers=approvers,
+        approval_label=label,
+    )
+    adoption, evidence_count, row_state = _row_facts(approvals_dir, issue, status.key)
+    return {
+        "issue": issue,
+        "state": status.state,
+        "plan_reason": status.plan_reason,
+        "plan_reply_id": status.plan_reply_id,
+        "plan_hash": status.plan_hash,
+        "record_id": status.record_id,
+        "plan_files_checked": checked,
+        "approvals": {"label": _channel(status.label), "comment": _channel(status.comment)},
+        "approved": status.approved,
+        "label_revoked": status.label_revoked,
+        "status_seen": status.status_seen,
+        "assignee_is_host_login": status.assignee_is_host_login,
+        "adoption_state": adoption,
+        "row_state": row_state,
+        "row_evidence_count": evidence_count,
+    }
+
+
+class _StatusRefused(Exception):
+    def __init__(self, reason: str | None) -> None:
+        super().__init__(reason)
+        self.reason = reason or "unreadable"
+
+
+@issue_pipeline_group.command("stage-status")
+@click.argument("issue", type=click.IntRange(min=1))
+@click.option("--json", "as_json", is_flag=True, help="Accepted for symmetry; the output is always JSON.")
+@click.option("--config", "config_path", type=click.Path(path_type=Path), default="~/.config/superclaude/issue-watch.json", show_default=True)
+@click.option("--approvals-dir", type=click.Path(path_type=Path), default=None, help="Read the adoption and approval rows here.")
+@click.option("--plan-dir", type=click.Path(path_type=Path), default=None, help="Report directory holding the plan files.")
+@click.option("--plan-file", "plan_files", multiple=True, help="A plan file name under --plan-dir (repeat).")
+def stage_status_command(
+    issue: int,
+    as_json: bool,
+    config_path: Path,
+    approvals_dir: Path | None,
+    plan_dir: Path | None,
+    plan_files: tuple[str, ...],
+) -> None:
+    """Print the plan-stage status of ISSUE as closed keys; writes nothing, prints no GitHub text."""
+    try:
+        label, approvers = _load_stage_inputs(config_path.expanduser())
+    except cycle.ConfigError as exc:
+        click.echo(f"refused:{exc.reason}")
+        raise SystemExit(_EXIT_CONFIG) from None
+    try:
+        result = _stage_status(issue, _make_runner(), label, approvers, approvals_dir, plan_dir, list(plan_files))
+    except _StatusRefused as exc:
+        click.echo(f"refused:{exc.reason}")
+        raise SystemExit(_EXIT_REFUSED) from None
+    click.echo(json.dumps(result, sort_keys=True))
diff --git a/tests/issue_pipeline/test_stage_status.py b/tests/issue_pipeline/test_stage_status.py
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/test_stage_status.py
@@ -0,0 +1,306 @@
+"""Task 6: the read-only ``stage-status`` verb."""
+
+from __future__ import annotations
+
+import json
+import re
+import shutil
+import subprocess
+from pathlib import Path
+
+import pytest
+from click.testing import CliRunner
+
+from superclaude.cli.issue_pipeline import approval_record, plan_hash, reads
+from superclaude.cli.issue_pipeline import cli as cli_mod
+from superclaude.cli.issue_pipeline.cli import issue_pipeline_group
+from superclaude.cli.issue_watch import github as gh
+from superclaude.cli.issue_watch.runner import CommandResult
+
+pytestmark = pytest.mark.skipif(shutil.which("jq") is None, reason="jq is needed to run the projections")
+
+RECORDED = Path(__file__).parent / "fixtures" / "recorded"
+HOST = "host-login"
+OWNER = "owner-login"
+LABEL = "plan-approved"
+ISSUE = 9
+CANARY = "CANARY-6e1b-NO-LEAK"
+T0 = "2026-11-16T10:00:00Z"
+T1 = "2026-11-16T10:05:00Z"
+T2 = "2026-11-16T10:10:00Z"
+
+EXPECTED_KEYS = {
+    "issue", "state", "plan_reason", "plan_reply_id", "plan_hash", "record_id", "plan_files_checked", "approvals",
+    "approved", "label_revoked", "status_seen", "assignee_is_host_login", "adoption_state", "row_state", "row_evidence_count",
+}
+CHANNEL_KEYS = {"accepted", "reason", "evidence_id", "actor_id", "actor_is_host_login"}
+VOCAB = {
+    "no-plan-reply", "plan-reply-invalid", "plan-changed", "awaiting-approval", "approved", "revoked", "ok",
+    "plan-reply-edited", "plan-reply-edit-unknown", "no-label", "label-before-plan", "label-removed", "actor-not-user",
+    "actor-not-allowed", "no-comment", "author-not-allowed", "comment-before-plan", "edit-unknown", "comment-edited",
+    "hash-mismatch", "reserved", "started", "uncertain", "recorded", "instructed", "acked", "revoked",
+}
+
+
+def jq(program: str, document: object) -> str:
+    done = subprocess.run(["jq", "-c", program], input=json.dumps(document), capture_output=True, text=True, check=True)
+    return done.stdout
+
+
+def ok(stdout: str) -> CommandResult:
+    return CommandResult(("gh",), 0, stdout, "", False, None, 0.0)
+
+
+class World:
+    """Raw GitHub evidence for one issue, served through the injected runner."""
+
+    def __init__(self, *, host: str = HOST, assignees: tuple[str, ...] = (OWNER,)) -> None:
+        self.host, self.assignees = host, assignees
+        self.comments: list[dict] = []
+        self.events: list[dict] = []
+        self.edited: dict[int, str] = {}
+        self.argvs: list[list[str]] = []
+        self._next = 100
+
+    def _id(self) -> int:
+        self._next += 1
+        return self._next
+
+    def plan_reply(self, plan: str, at: str = T0) -> int:
+        cid = self._id()
+        body = f"Plan ready. {CANARY}\n<!-- sc:stage:plan id=ap-{ISSUE}-plan-{plan[:12]} plan={plan} -->"
+        self.comments.append(self._comment(cid, self.host, 1, "User", at, body))
+        return cid
+
+    def comment(self, body: str, at: str, login: str = OWNER, uid: int = 111, kind: str = "User") -> int:
+        cid = self._id()
+        self.comments.append(self._comment(cid, login, uid, kind, at, body))
+        return cid
+
+    @staticmethod
+    def _comment(cid: int, login: str, uid: int, kind: str, at: str, body: str) -> dict:
+        return {"id": cid, "user": {"login": login, "id": uid, "type": kind}, "created_at": at, "updated_at": at, "body": body}
+
+    def label(self, event: str, at: str, login: str = OWNER, uid: int = 111, kind: str = "User") -> None:
+        self.events.append(
+            {"id": self._id(), "event": event, "label": {"name": LABEL}, "actor": {"id": uid, "login": login, "type": kind}, "created_at": at}
+        )
+
+    def status_move(self, at: str) -> None:
+        self.events.append({"id": self._id(), "event": "project_v2_item_status_changed", "actor": {"id": 5, "login": "bot[bot]", "type": "Bot"}, "created_at": at})
+
+    # the injected runner
+    def run(self, argv, timeout, *, cwd=None) -> CommandResult:
+        self.argvs.append(list(argv))
+        if argv == ["gh", "api", "user", "--include"]:
+            return ok("HTTP/2.0 200 OK\ndate: Mon, 16 Nov 2026 10:00:00 GMT\n\n" + json.dumps({"login": self.host, "id": 1}))
+        if argv[:3] == ["gh", "api", "graphql"]:
+            nodes = [
+                {"databaseId": c["id"], "author": {"login": c["user"]["login"]}, "createdAt": c["created_at"], "lastEditedAt": self.edited.get(c["id"])}
+                for c in self.comments
+            ]
+            data = {"data": {"repository": {"issue": {"createdAt": "2026-11-15T00:00:00Z", "lastEditedAt": None,
+                    "comments": {"nodes": nodes, "pageInfo": {"hasNextPage": False, "endCursor": None}}}}}}
+            return ok(json.dumps(data))
+        path = next(a for a in argv if a.startswith("repos/"))
+        if path.endswith("/events"):
+            return ok(jq(gh.EVENTS_JQ, self.events))
+        if path.endswith("/comments"):
+            return ok(jq(reads.COMMENTS_JQ, self.comments))
+        assert path.endswith(f"/issues/{ISSUE}") or re.search(r"/issues/\d+$", path), path
+        return ok(json.dumps({"number": int(path.rsplit("/", 1)[1]), "state": "open", "labels": [], "assignees": list(self.assignees)}))
+
+
+@pytest.fixture
+def plan_dir(tmp_path: Path) -> Path:
+    d = tmp_path / "report"
+    d.mkdir()
+    (d / "plan.md").write_text("the plan")
+    return d
+
+
+def plan_sha(plan_dir: Path) -> str:
+    return plan_hash.compute(plan_dir, ["plan.md"])[1]
+
+
+def invoke(world: World, monkeypatch, *args: str, issue: int = ISSUE, approvers=frozenset({222})):
+    monkeypatch.setattr(cli_mod, "_make_runner", lambda: world)
+    monkeypatch.setattr(cli_mod, "_load_stage_inputs", lambda path: (LABEL, approvers))
+    return CliRunner().invoke(issue_pipeline_group, ["stage-status", str(issue), "--json", *args])
+
+
+def assert_closed(out: dict) -> None:
+    assert set(out) == EXPECTED_KEYS
+    assert set(out["approvals"]) == {"label", "comment"}
+    for channel in out["approvals"].values():
+        assert set(channel) == CHANNEL_KEYS
+    strings = [out["state"], out["plan_reason"], out["adoption_state"], out["row_state"]]
+    strings += [c["reason"] for c in out["approvals"].values()]
+    assert all(s is None or s in VOCAB for s in strings), strings
+    for key in ("plan_hash",):
+        assert out[key] is None or re.fullmatch(r"[0-9a-f]{64}", out[key])
+    assert out["record_id"] is None or re.fullmatch(r"ap-[1-9][0-9]*-plan-[0-9a-f]{12}", out["record_id"])
+    assert CANARY not in json.dumps(out)
+
+
+def status(world: World, monkeypatch, plan_dir: Path, *extra: str, approvers=frozenset({222})) -> dict:
+    result = invoke(world, monkeypatch, "--plan-dir", str(plan_dir), "--plan-file", "plan.md", *extra, approvers=approvers)
+    assert result.exit_code == 0, result.output
+    out = json.loads(result.output)
+    assert_closed(out)
+    return out
+
+
+# --- recorded files -------------------------------------------------------------
+
+
+def test_recorded_files_through_the_injected_runner_print_only_closed_keys(monkeypatch) -> None:
+    world = World(host="ironbelly", assignees=("ironbelly",))
+    world.comments = json.loads((RECORDED / "comments-page1.json").read_text())
+    world.events = json.loads((RECORDED / "events-page1.json").read_text())
+    raw_edits = json.loads((RECORDED / "edits-page1.json").read_text())
+    real_run = world.run
+
+    def run(argv, timeout, *, cwd=None):
+        if argv[:3] == ["gh", "api", "graphql"]:
+            world.argvs.append(list(argv))
+            return ok(json.dumps(raw_edits))
+        return real_run(argv, timeout, cwd=cwd)
+
+    world.run = run  # type: ignore[method-assign]
+    result = invoke(world, monkeypatch, issue=452)
+    assert result.exit_code == 0, result.output
+    out = json.loads(result.output)
+    assert_closed(out)
+    assert out["state"] == "no-plan-reply" and out["issue"] == 452
+
+
+# --- the case table --------------------------------------------------------------
+
+
+def test_no_plan_reply_yet(monkeypatch, plan_dir: Path) -> None:
+    world = World()
+    world.comment("hello", T1)
+    out = status(world, monkeypatch, plan_dir)
+    assert out["state"] == "no-plan-reply" and out["approved"] is False and out["plan_hash"] is None
+
+
+def test_plan_reply_and_no_approval(monkeypatch, plan_dir: Path) -> None:
+    world = World()
+    world.plan_reply(plan_sha(plan_dir))
+    out = status(world, monkeypatch, plan_dir)
+    assert out["state"] == "awaiting-approval" and out["plan_files_checked"] is True
+    assert out["approvals"]["label"]["reason"] == "no-label" and out["approvals"]["comment"]["reason"] == "no-comment"
+
+
+def test_label_only(monkeypatch, plan_dir: Path) -> None:
+    world = World()
+    world.plan_reply(plan_sha(plan_dir))
+    world.label("labeled", T1)
+    out = status(world, monkeypatch, plan_dir)
+    assert out["approved"] and out["approvals"]["label"]["accepted"] and not out["approvals"]["comment"]["accepted"]
+    assert out["status_seen"] is False
+
+
+def test_comment_only(monkeypatch, plan_dir: Path) -> None:
+    world = World()
+    world.plan_reply(plan_sha(plan_dir))
+    world.comment("approved", T1)
+    out = status(world, monkeypatch, plan_dir)
+    assert out["approved"] and out["approvals"]["comment"]["accepted"] and not out["approvals"]["label"]["accepted"]
+
+
+def test_label_and_comment_make_one_key_and_one_row(monkeypatch, plan_dir: Path, tmp_path: Path) -> None:
+    sha = plan_sha(plan_dir)
+    world = World()
+    world.plan_reply(sha)
+    cid = world.comment("approved", T1)
+    world.label("labeled", T1)
+    world.status_move(T2)
+    adir = tmp_path / "approvals"
+    approval_record.init_dir(adir)
+    approval_record.adopt_create(adir, ISSUE, "plan", T0)
+    approval_record.adopt_mark(adir, ISSUE, "plan", "started", "ctx_1", T0)
+    approval_record.record_create(adir, ISSUE, "plan", sha, "label", "evt-1", "u_1", T1)
+    approval_record.record_create(adir, ISSUE, "plan", sha, "comment", f"c{cid}", "u_1", T1)
+    out = status(world, monkeypatch, plan_dir, "--approvals-dir", str(adir))
+    assert out["approved"] and out["approvals"]["label"]["accepted"] and out["approvals"]["comment"]["accepted"]
+    assert (out["adoption_state"], out["row_state"], out["row_evidence_count"]) == ("started", "recorded", 2)
+    assert out["status_seen"] is True
+    assert len(list(adir.glob("approval-*.json"))) == 1
+
+
+def test_plan_changed_after_approval(monkeypatch, plan_dir: Path) -> None:
+    world = World()
+    world.plan_reply(plan_sha(plan_dir))
+    world.comment("approved", T1)
+    (plan_dir / "plan.md").write_text("the plan, edited")
+    out = status(world, monkeypatch, plan_dir)
+    assert out["state"] == "plan-changed" and out["approved"] is False
+
+
+def test_approval_label_removed(monkeypatch, plan_dir: Path) -> None:
+    world = World()
+    world.plan_reply(plan_sha(plan_dir))
+    world.label("labeled", T1)
+    world.label("unlabeled", T2)
+    out = status(world, monkeypatch, plan_dir)
+    assert out["state"] == "revoked" and out["label_revoked"] is True
+
+
+def test_approver_not_listed(monkeypatch, plan_dir: Path) -> None:
+    world = World()
+    world.plan_reply(plan_sha(plan_dir))
+    world.comment("approved", T1, login="stranger", uid=999)
+    world.label("labeled", T1, login="stranger", uid=999)
+    out = status(world, monkeypatch, plan_dir)
+    assert out["approved"] is False
+    assert out["approvals"]["comment"]["reason"] == "author-not-allowed"
+    assert out["approvals"]["label"]["reason"] == "actor-not-allowed"
+    listed = status(world, monkeypatch, plan_dir, approvers=frozenset({999}))
+    assert listed["approved"] is True
+
+
+def test_without_plan_files_the_markers_own_hash_is_used_and_flagged(monkeypatch, plan_dir: Path) -> None:
+    world = World()
+    world.plan_reply(plan_sha(plan_dir))
+    out = json.loads(invoke(world, monkeypatch).output)
+    assert out["plan_files_checked"] is False and out["state"] == "awaiting-approval"
+
+
+def test_a_failed_read_prints_a_closed_refusal_and_nothing_else(monkeypatch) -> None:
+    class Down:
+        def run(self, argv, timeout, *, cwd=None):
+            return CommandResult(tuple(argv), 1, "", f"HTTP 502 {CANARY}", False, None, 0.0)
+
+    result = invoke(Down(), monkeypatch)
+    assert result.exit_code == 1 and result.output.startswith("refused:") and CANARY not in result.output
+
+
+# --- read-only proof -------------------------------------------------------------
+
+
+def test_the_command_only_reads_and_never_calls_orca(monkeypatch, plan_dir: Path, tmp_path: Path) -> None:
+    world = World()
+    world.plan_reply(plan_sha(plan_dir))
+    world.comment("approved", T1)
+    world.label("labeled", T1)
+    before = sorted(p.name for p in tmp_path.rglob("*"))
+    status(world, monkeypatch, plan_dir)
+    assert sorted(p.name for p in tmp_path.rglob("*")) == before  # nothing was written
+    assert world.argvs
+    graphql = [a for a in world.argvs if a[:3] == ["gh", "api", "graphql"]]
+    assert graphql == [gh.argv_edits(ISSUE)]  # the watcher's fixed query, untouched
+    for argv in world.argvs:
+        assert argv[0] == "gh" and "orca" not in " ".join(argv).lower().split()
+        if "--method" in argv:
+            assert argv[argv.index("--method") + 1] == "GET"
+        elif argv[:3] != ["gh", "api", "graphql"]:
+            assert argv == ["gh", "api", "user", "--include"] or "--method" in argv
+        text = " ".join(argv)
+        assert not re.search(r"mutation|--method (POST|PUT|PATCH|DELETE)|-X ", text)
+
+
+def test_stage_status_help_exits_zero() -> None:
+    result = CliRunner().invoke(issue_pipeline_group, ["stage-status", "--help"])
+    assert result.exit_code == 0 and "stage-status" in result.output

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
