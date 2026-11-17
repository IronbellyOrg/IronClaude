8c23180f9930bac120e6843c9b73895d87b60826
Review one task for spec compliance.

Task brief: ## Task 3: Build the locked, write-ahead approval record helper

Depends on: Task 1, Task 2

Create `src/superclaude/cli/issue_pipeline/approval_record.py` and its verbs (`init`, `adopt-create`, `adopt-mark`, `record-create`, `record-show`, `record-mark`) in `src/superclaude/cli/issue_pipeline/cli.py`, with `tests/issue_pipeline/test_approval_record.py`, `tests/issue_pipeline/test_approval_concurrency.py` and `tests/issue_pipeline/test_approval_crash.py`.

The helper keeps two kinds of row in an approvals directory of its own, never inside the watcher's state directory and never touching `dispatch.json`. An adoption row is keyed (issue, stage) and is created before any plan exists, so no plan hash is needed: it is the per-issue reservation that stops a second start (state `reserved`, then `started` with the Dispatch id, or `uncertain` when `worker-start` did not report ready; an `uncertain` row is settled by a person or by reading `worker-list`, never by starting again). An approval row is keyed (issue, stage, plan hash) and hangs under the adoption row. `init <dir>` creates the directory (0700) and its `lock` file (0600), because `FileStore.lock()` opens an existing file with no create flag and raises `lock_missing` otherwise (record.py:391-397). It takes the lock with `FileStore(<approvals dir>).lock()` from src/superclaude/cli/issue_watch/record.py:381 (an exclusive non-blocking `flock`, so a second concurrent caller gets `LockHeld` at once and the verbs say "retry the append", never "lost"; the lock is held only for one call, so it is not what spans adoption: the adoption row is), and writes with `write_prepared_bytes` from `superclaude.cli.swarm.atomic` followed by a directory sync, the same way `FileStore.save` does (record.py:370 and `_fsync_dir` at record.py:310). `record.py` itself is not edited. Row fields: record id, issue, stage, plan hash, evidence list (channel, event or comment or message id, actor id, time), state (`recorded`, `instructed`, `acked`, `revoked`), times. A second approval for the same key, from any channel, appends evidence to the existing row and returns the existing row, so a label plus a comment can never produce two rows. A re-approval of the same plan after `revoked` reopens the same row.

Start condition: can start now.

Acceptance criteria:
- A test with two processes calling `record-create` for the same key at once shows exactly one row and one winner; the loser gets the existing row or a lock-held result, never a second row.
- A test shows that a label approval followed by a comment approval for the same key leaves one row with two evidence entries, and that a different plan hash for the same issue makes a different row.
- A crash test (kill after the write, before the caller proceeds) shows the row is on disk and `record-show` returns state `recorded`, mirroring tests/issue_watch/test_crash_injection.py.
- `record-create` in a directory that `init` never ran in fails with a closed reason (not a traceback), and after `init` the first call succeeds; a concurrent second call reports `lock-held, retry` and the evidence is appended on the retry.
- Adoption tests: two callers of `adopt-create` for one issue get one row and one `reserved` winner; a kill between `worker-start` and `adopt-mark started` leaves the row `reserved`, and the next `adopt-create` refuses a second start with the reason `uncertain-launch`; a duplicate approval, sequential or concurrent, and a crash between the row write and the `reply` each yield at most one start and at most one continuation instruction, asserted on the adoption and approval row states, not on a row count.
- `record-mark` accepts only the forward moves `recorded` to `instructed` to `acked`, and `revoked` from any of them, and refuses every other move with a closed reason.
- `git diff --stat` shows no change to src/superclaude/cli/issue_watch/record.py, and `uv run pytest tests/issue_pipeline/ tests/issue_watch/test_record.py tests/issue_watch/test_module_boundaries.py -v` passes.

AC ids (source order): T3.AC1 = bullet 1 of "Acceptance criteria"; T3.AC2 = bullet 2 of "Acceptance criteria"; T3.AC3 = bullet 3 of "Acceptance criteria"; T3.AC4 = bullet 4 of "Acceptance criteria"; T3.AC5 = bullet 5 of "Acceptance criteria"; T3.AC6 = bullet 6 of "Acceptance criteria"; T3.AC7 = bullet 7 of "Acceptance criteria"
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
Start sha: 8c23180f9930bac120e6843c9b73895d87b60826
Diff against the start snapshot: diff --git a/src/superclaude/cli/issue_pipeline/approval_record.py b/src/superclaude/cli/issue_pipeline/approval_record.py
new file mode 100644
--- /dev/null
+++ b/src/superclaude/cli/issue_pipeline/approval_record.py
@@ -0,0 +1,308 @@
+"""The locked, write-ahead approval record helper (plan Task 3).
+
+Two kinds of row live in an approvals directory of their own, never inside the
+watcher's state directory and never touching ``dispatch.json``:
+
+* An **adoption row** is keyed (issue, stage). It is created before any plan
+  exists, so it needs no plan hash. It is the per-issue reservation that stops a
+  second start: state ``reserved``, then ``started`` (with the Dispatch id) or
+  ``uncertain`` when ``worker-start`` did not report ready. An ``uncertain`` row is
+  settled by a person or by reading ``worker-list``, never by starting again.
+* An **approval row** is keyed (issue, stage, plan hash) and hangs under the
+  adoption row. States: ``recorded``, ``instructed``, ``acked``, ``revoked``.
+
+Every mutation holds ``FileStore(<dir>).lock()``: an exclusive non-blocking
+``flock`` on ``<dir>/lock``, so a second concurrent caller gets ``lock-held`` at
+once and the verbs say "retry", never "lost". ``record.py`` of the watcher is not
+edited; only its ``FileStore.lock`` is used. Rows are written with
+``write_prepared_bytes`` followed by a directory sync, as ``FileStore.save`` does.
+Nothing here keeps or prints GitHub text: every stored value matches a fixed pattern.
+"""
+
+from __future__ import annotations
+
+import json
+import os
+import re
+import stat
+from datetime import datetime, timezone
+from pathlib import Path
+from typing import Any
+
+from superclaude.cli.issue_watch.record import FileStore, LockError, LockHeld
+from superclaude.cli.swarm.atomic import write_prepared_bytes
+
+from .approval_line import record_id
+
+LOCK_FILE = "lock"
+
+_STAGE = re.compile(r"[a-z][a-z0-9-]{0,31}")
+_HASH = re.compile(r"[0-9a-f]{64}")
+_ID = re.compile(r"[0-9A-Za-z_:.=-]{1,80}")
+_TIME = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
+CHANNELS = ("label", "comment", "reply")
+ADOPTION_STATES = ("reserved", "started", "uncertain")
+APPROVAL_STATES = ("recorded", "instructed", "acked", "revoked")
+_FORWARD = {"recorded": "instructed", "instructed": "acked"}
+
+
+class ApprovalError(Exception):
+    """A closed refusal; ``reason`` never holds file or GitHub text."""
+
+    def __init__(self, reason: str) -> None:
+        super().__init__(reason)
+        self.reason = reason
+
+
+def _now() -> str:
+    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
+
+
+def _need(pattern: re.Pattern[str], value: str, reason: str) -> str:
+    if not isinstance(value, str) or not pattern.fullmatch(value):
+        raise ApprovalError(reason)
+    return value
+
+
+def _issue(issue: int) -> int:
+    if isinstance(issue, bool) or not isinstance(issue, int) or issue < 1:
+        raise ApprovalError("bad-issue")
+    return issue
+
+
+def _fsync_dir(path: Path) -> None:
+    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
+    try:
+        os.fsync(fd)
+    finally:
+        os.close(fd)
+
+
+def init_dir(directory: str | Path) -> None:
+    """Create the approvals directory (0700) and its ``lock`` file (0600).
+
+    ``FileStore.lock()`` opens an existing file with no create flag and raises
+    ``lock_missing`` otherwise, so ``init`` is the only creator. Safe to repeat.
+    """
+    path = Path(directory)
+    if path.is_symlink() or (path.exists() and not path.is_dir()):
+        raise ApprovalError("bad-dir")
+    path.mkdir(mode=0o700, parents=True, exist_ok=True)
+    lock = path / LOCK_FILE
+    if lock.is_symlink():
+        raise ApprovalError("bad-dir")
+    fd = os.open(lock, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
+    os.close(fd)
+    os.chmod(path, 0o700)
+    os.chmod(lock, 0o600)
+    _fsync_dir(path)
+
+
+def _locked(directory: Path):
+    """The lock context, with the closed refusals mapped."""
+    if directory.is_symlink() or not directory.is_dir():
+        raise ApprovalError("not-initialized")
+    return FileStore(directory).lock()
+
+
+class _Guard:
+    def __init__(self, directory: Path) -> None:
+        self._cm = _locked(directory)
+
+    def __enter__(self) -> None:
+        try:
+            self._cm.__enter__()
+        except LockHeld:
+            raise ApprovalError("lock-held") from None
+        except LockError as exc:
+            raise ApprovalError("not-initialized" if exc.reason == "lock_missing" else "lock-invalid") from None
+
+    def __exit__(self, *exc_info: Any) -> bool | None:
+        return self._cm.__exit__(*exc_info)
+
+
+def _adoption_path(directory: Path, issue: int, stage: str) -> Path:
+    return directory / f"adoption-{_issue(issue)}-{_need(_STAGE, stage, 'bad-stage')}.json"
+
+
+def _approval_path(directory: Path, issue: int, stage: str, plan_hash: str) -> Path:
+    name = f"approval-{_issue(issue)}-{_need(_STAGE, stage, 'bad-stage')}-{_need(_HASH, plan_hash, 'bad-hash')}.json"
+    return directory / name
+
+
+def _read_row(path: Path) -> dict[str, Any] | None:
+    try:
+        st = os.lstat(path)
+    except FileNotFoundError:
+        return None
+    if not stat.S_ISREG(st.st_mode):
+        raise ApprovalError("row-invalid")
+    try:
+        row = json.loads(path.read_bytes())
+    except (OSError, ValueError):
+        raise ApprovalError("row-invalid") from None
+    if not isinstance(row, dict) or row.get("state") not in (*ADOPTION_STATES, *APPROVAL_STATES):
+        raise ApprovalError("row-invalid")
+    return row
+
+
+def _write_row(path: Path, row: dict[str, Any]) -> None:
+    text = json.dumps(row, sort_keys=True, indent=2, ensure_ascii=True)
+    write_prepared_bytes(path, text.encode() + b"\n")
+    os.chmod(path, 0o600)
+    _fsync_dir(path.parent)
+
+
+# --- adoption rows ------------------------------------------------------------
+
+
+def adopt_create(directory: str | Path, issue: int, stage: str, now: str | None = None) -> dict[str, Any]:
+    """Reserve (issue, stage). Only the caller that gets ``created`` may start a worker.
+
+    An existing ``reserved`` or ``uncertain`` row refuses with ``uncertain-launch``
+    (a start may or may not have happened; never start again), a ``started`` row
+    with ``already-started``.
+    """
+    d = Path(directory)
+    path = _adoption_path(d, issue, stage)
+    with _Guard(d):
+        existing = _read_row(path)
+        if existing is not None:
+            raise ApprovalError("already-started" if existing["state"] == "started" else "uncertain-launch")
+        stamp = _need(_TIME, now or _now(), "bad-time")
+        row = {
+            "kind": "adoption",
+            "issue": issue,
+            "stage": stage,
+            "state": "reserved",
+            "dispatch_id": None,
+            "created_at": stamp,
+            "updated_at": stamp,
+        }
+        _write_row(path, row)
+        return {"result": "created", "row": row}
+
+
+def adopt_mark(
+    directory: str | Path,
+    issue: int,
+    stage: str,
+    state: str,
+    dispatch_id: str | None = None,
+    now: str | None = None,
+) -> dict[str, Any]:
+    """``reserved`` to ``started`` (needs a Dispatch id) or ``uncertain``; ``uncertain`` to ``started``."""
+    d = Path(directory)
+    path = _adoption_path(d, issue, stage)
+    if state not in ("started", "uncertain"):
+        raise ApprovalError("bad-move")
+    if state == "started":
+        _need(_ID, dispatch_id or "", "bad-dispatch-id")
+    with _Guard(d):
+        row = _read_row(path)
+        if row is None or row.get("kind") != "adoption":
+            raise ApprovalError("no-row")
+        if (row["state"], state) not in (("reserved", "started"), ("reserved", "uncertain"), ("uncertain", "started")):
+            raise ApprovalError("bad-move")
+        row["state"] = state
+        if state == "started":
+            row["dispatch_id"] = dispatch_id
+        row["updated_at"] = _need(_TIME, now or _now(), "bad-time")
+        _write_row(path, row)
+        return {"result": "marked", "row": row}
+
+
+def adopt_show(directory: str | Path, issue: int, stage: str) -> dict[str, Any]:
+    row = _read_row(_adoption_path(Path(directory), issue, stage))
+    if row is None:
+        raise ApprovalError("no-row")
+    return row
+
+
+# --- approval rows ------------------------------------------------------------
+
+
+def record_create(
+    directory: str | Path,
+    issue: int,
+    stage: str,
+    plan_hash: str,
+    channel: str,
+    evidence_id: str,
+    actor: str,
+    now: str | None = None,
+) -> dict[str, Any]:
+    """Create the row for (issue, stage, plan hash), or append evidence to the existing one.
+
+    A second approval for the same key, from any channel, appends evidence and
+    returns the existing row, so a label plus a comment never produce two rows.
+    A re-approval of the same plan after ``revoked`` reopens the same row.
+    """
+    d = Path(directory)
+    path = _approval_path(d, issue, stage, plan_hash)
+    if channel not in CHANNELS:
+        raise ApprovalError("bad-channel")
+    _need(_ID, evidence_id, "bad-evidence-id")
+    _need(_ID, actor, "bad-actor")
+    stamp = _need(_TIME, now or _now(), "bad-time")
+    with _Guard(d):
+        if _read_row(_adoption_path(d, issue, stage)) is None:
+            raise ApprovalError("no-adoption")
+        evidence = {"channel": channel, "id": evidence_id, "actor": actor, "time": stamp}
+        row = _read_row(path)
+        if row is None:
+            row = {
+                "kind": "approval",
+                "record_id": record_id(issue, plan_hash),
+                "issue": issue,
+                "stage": stage,
+                "plan_hash": plan_hash,
+                "state": "recorded",
+                "evidence": [evidence],
+                "created_at": stamp,
+                "updated_at": stamp,
+            }
+            _write_row(path, row)
+            return {"result": "created", "row": row}
+        if evidence not in row["evidence"]:
+            row["evidence"].append(evidence)
+        if row["state"] == "revoked":
+            row["state"] = "recorded"
+        row["updated_at"] = stamp
+        _write_row(path, row)
+        return {"result": "exists", "row": row}
+
+
+def record_show(directory: str | Path, issue: int, stage: str, plan_hash: str) -> dict[str, Any]:
+    row = _read_row(_approval_path(Path(directory), issue, stage, plan_hash))
+    if row is None:
+        raise ApprovalError("no-row")
+    return row
+
+
+def record_mark(
+    directory: str | Path,
+    issue: int,
+    stage: str,
+    plan_hash: str,
+    state: str,
+    now: str | None = None,
+) -> dict[str, Any]:
+    """Only ``recorded`` to ``instructed`` to ``acked``, and ``revoked`` from any of them."""
+    d = Path(directory)
+    path = _approval_path(d, issue, stage, plan_hash)
+    if state not in APPROVAL_STATES[1:]:
+        raise ApprovalError("bad-move")
+    stamp = _need(_TIME, now or _now(), "bad-time")
+    with _Guard(d):
+        row = _read_row(path)
+        if row is None or row.get("kind") != "approval":
+            raise ApprovalError("no-row")
+        current = row["state"]
+        allowed = (state == "revoked" and current != "revoked") or _FORWARD.get(current) == state
+        if not allowed:
+            raise ApprovalError("bad-move")
+        row["state"] = state
+        row["updated_at"] = stamp
+        _write_row(path, row)
+        return {"result": "marked", "row": row}
diff --git a/src/superclaude/cli/issue_pipeline/cli.py b/src/superclaude/cli/issue_pipeline/cli.py
--- a/src/superclaude/cli/issue_pipeline/cli.py
+++ b/src/superclaude/cli/issue_pipeline/cli.py
@@ -6,11 +6,35 @@ verb prints file or GitHub text.
 
 from __future__ import annotations
 
+import json
+from collections.abc import Callable
+from typing import Any
+
 import click
 
-from . import approval_line, plan_hash
+from . import approval_line, approval_record, plan_hash
 
 _EXIT_REFUSED = 1
+_EXIT_LOCK_HELD = 75  # the watcher's own code for a held lock
+
+
+def _run_record(action: Callable[[], dict[str, Any]]) -> None:
+    """Print the closed JSON result of one record verb, or one closed refusal."""
+    try:
+        result = action()
+    except approval_record.ApprovalError as exc:
+        if exc.reason == "lock-held":
+            click.echo("lock-held, retry")
+            raise SystemExit(_EXIT_LOCK_HELD) from None
+        click.echo(f"refused:{exc.reason}")
+        raise SystemExit(_EXIT_REFUSED) from None
+    click.echo(json.dumps(result, sort_keys=True))
+
+
+_DIR = click.argument("approvals_dir", type=click.Path())
+_ISSUE = click.option("--issue", type=click.IntRange(min=1), required=True)
+_STAGE = click.option("--stage", default="plan", show_default=True)
+_PLAN_HASH = click.option("--plan-hash", "plan_hash_value", required=True, help="64 lowercase hex.")
 
 
 @click.group(name="issue-pipeline")
@@ -44,3 +68,73 @@ def check_approval_command(report_dir: str, names: tuple[str, ...], line: str, i
     click.echo(result)
     if result != approval_line.OK:
         raise SystemExit(_EXIT_REFUSED)
+
+
+@issue_pipeline_group.command("init")
+@_DIR
+def init_command(approvals_dir: str) -> None:
+    """Create the approvals directory (0700) and its lock file (0600)."""
+    try:
+        approval_record.init_dir(approvals_dir)
+    except approval_record.ApprovalError as exc:
+        click.echo(f"refused:{exc.reason}")
+        raise SystemExit(_EXIT_REFUSED) from None
+    click.echo("ok")
+
+
+@issue_pipeline_group.command("adopt-create")
+@_DIR
+@_ISSUE
+@_STAGE
+def adopt_create_command(approvals_dir: str, issue: int, stage: str) -> None:
+    """Reserve (issue, stage); only a `created` result may start a worker."""
+    _run_record(lambda: approval_record.adopt_create(approvals_dir, issue, stage))
+
+
+@issue_pipeline_group.command("adopt-mark")
+@_DIR
+@_ISSUE
+@_STAGE
+@click.option("--state", type=click.Choice(["started", "uncertain"]), required=True)
+@click.option("--dispatch-id", default=None, help="Required for `started`.")
+def adopt_mark_command(approvals_dir: str, issue: int, stage: str, state: str, dispatch_id: str | None) -> None:
+    """Mark the adoption row `started` (with the Dispatch id) or `uncertain`."""
+    _run_record(lambda: approval_record.adopt_mark(approvals_dir, issue, stage, state, dispatch_id))
+
+
+@issue_pipeline_group.command("record-create")
+@_DIR
+@_ISSUE
+@_STAGE
+@_PLAN_HASH
+@click.option("--channel", type=click.Choice(list(approval_record.CHANNELS)), required=True)
+@click.option("--evidence-id", required=True, help="Event, comment or message id.")
+@click.option("--actor", required=True, help="Actor id.")
+def record_create_command(
+    approvals_dir: str, issue: int, stage: str, plan_hash_value: str, channel: str, evidence_id: str, actor: str
+) -> None:
+    """Create the approval row, or append evidence to the existing one."""
+    _run_record(
+        lambda: approval_record.record_create(approvals_dir, issue, stage, plan_hash_value, channel, evidence_id, actor)
+    )
+
+
+@issue_pipeline_group.command("record-show")
+@_DIR
+@_ISSUE
+@_STAGE
+@_PLAN_HASH
+def record_show_command(approvals_dir: str, issue: int, stage: str, plan_hash_value: str) -> None:
+    """Print the approval row."""
+    _run_record(lambda: {"row": approval_record.record_show(approvals_dir, issue, stage, plan_hash_value)})
+
+
+@issue_pipeline_group.command("record-mark")
+@_DIR
+@_ISSUE
+@_STAGE
+@_PLAN_HASH
+@click.option("--state", type=click.Choice(list(approval_record.APPROVAL_STATES[1:])), required=True)
+def record_mark_command(approvals_dir: str, issue: int, stage: str, plan_hash_value: str, state: str) -> None:
+    """Move the approval row forward (`instructed`, `acked`) or to `revoked`."""
+    _run_record(lambda: approval_record.record_mark(approvals_dir, issue, stage, plan_hash_value, state))
diff --git a/tests/issue_pipeline/test_approval_concurrency.py b/tests/issue_pipeline/test_approval_concurrency.py
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/test_approval_concurrency.py
@@ -0,0 +1,72 @@
+"""Task 3: two processes at once never make a second row."""
+
+from __future__ import annotations
+
+import multiprocessing as mp
+import time
+from pathlib import Path
+
+from superclaude.cli.issue_pipeline import approval_record as ar
+
+H = "0123456789abcdef" * 4
+T = "2026-11-16T10:00:00Z"
+
+
+def _retry(fn):
+    """Call ``fn`` until it is not lock-held, as the verbs tell a caller to."""
+    for _ in range(2000):
+        try:
+            return fn()
+        except ar.ApprovalError as exc:
+            if exc.reason != "lock-held":
+                return ("refused", exc.reason)
+            time.sleep(0.002)
+    raise AssertionError("lock never freed")
+
+
+def _create_worker(directory: str, n: int, start, out) -> None:
+    start.wait()
+    out.put(_retry(lambda: ar.record_create(directory, 9, "plan", H, "comment", f"c{n}", f"u{n}", T))["result"])
+
+
+def _adopt_worker(directory: str, start, out) -> None:
+    start.wait()
+    try:
+        out.put(ar.adopt_create(directory, 9, "plan", T)["result"])
+    except ar.ApprovalError as exc:
+        out.put(exc.reason)
+
+
+def _run(target, args_for) -> list:
+    ctx = mp.get_context("fork")
+    start, out = ctx.Event(), ctx.Queue()
+    procs = [ctx.Process(target=target, args=args_for(n, start, out)) for n in range(6)]
+    for p in procs:
+        p.start()
+    start.set()
+    results = [out.get(timeout=30) for _ in procs]
+    for p in procs:
+        p.join(timeout=30)
+        assert p.exitcode == 0
+    return results
+
+
+def test_concurrent_record_create_makes_one_row_and_one_winner(tmp_path: Path) -> None:
+    d = tmp_path / "a"
+    ar.init_dir(d)
+    ar.adopt_create(d, 9, "plan", T)
+    ar.adopt_mark(d, 9, "plan", "started", "ctx_1", T)
+    results = _run(_create_worker, lambda n, s, o: (str(d), n, s, o))
+    assert sorted(results) == ["created"] + ["exists"] * 5
+    assert len(list(d.glob("approval-*.json"))) == 1
+    assert len(ar.record_show(d, 9, "plan", H)["evidence"]) == 6  # every retry appended
+
+
+def test_concurrent_adopt_create_has_one_reserved_winner(tmp_path: Path) -> None:
+    d = tmp_path / "b"
+    ar.init_dir(d)
+    results = _run(_adopt_worker, lambda n, s, o: (str(d), s, o))
+    assert results.count("created") == 1
+    assert all(r in ("created", "uncertain-launch", "lock-held") for r in results)
+    assert len(list(d.glob("adoption-*.json"))) == 1
+    assert ar.adopt_show(d, 9, "plan")["state"] == "reserved"
diff --git a/tests/issue_pipeline/test_approval_crash.py b/tests/issue_pipeline/test_approval_crash.py
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/test_approval_crash.py
@@ -0,0 +1,73 @@
+"""Task 3: a kill at the worst moment leaves rows that stop a second start.
+
+Mirrors tests/issue_watch/test_crash_injection.py: a child process does the write
+and is killed before its caller can proceed; the parent then reads the disk.
+"""
+
+from __future__ import annotations
+
+import subprocess
+import sys
+from pathlib import Path
+
+from superclaude.cli.issue_pipeline import approval_record as ar
+
+H = "0123456789abcdef" * 4
+T = "2026-11-16T10:00:00Z"
+
+
+def _killed_after(code: str, directory: Path) -> None:
+    """Run ``code`` (with ``ar`` and ``d`` bound) in a child that then SIGKILLs itself."""
+    script = (
+        "import os, signal\n"
+        "from superclaude.cli.issue_pipeline import approval_record as ar\n"
+        f"d = {str(directory)!r}\n"
+        f"{code}\n"
+        "os.kill(os.getpid(), signal.SIGKILL)\n"
+    )
+    proc = subprocess.run([sys.executable, "-c", script], capture_output=True, timeout=60)
+    assert proc.returncode == -9, proc.stderr.decode()[-300:]
+
+
+def test_a_killed_record_create_is_on_disk_as_recorded(tmp_path: Path) -> None:
+    d = tmp_path / "a"
+    ar.init_dir(d)
+    ar.adopt_create(d, 9, "plan", T)
+    ar.adopt_mark(d, 9, "plan", "started", "ctx_1", T)
+    _killed_after(f"ar.record_create(d, 9, 'plan', {H!r}, 'label', 'e1', 'u1', {T!r})", d)
+    assert ar.record_show(d, 9, "plan", H)["state"] == "recorded"
+
+
+def test_a_kill_between_worker_start_and_adopt_mark_blocks_a_second_start(tmp_path: Path) -> None:
+    d = tmp_path / "b"
+    ar.init_dir(d)
+    _killed_after(f"ar.adopt_create(d, 9, 'plan', {T!r})", d)  # worker-start ran, adopt-mark never did
+    assert ar.adopt_show(d, 9, "plan")["state"] == "reserved"
+    try:
+        ar.adopt_create(d, 9, "plan", T)
+    except ar.ApprovalError as exc:
+        assert exc.reason == "uncertain-launch"
+    else:
+        raise AssertionError("a second start was allowed")
+
+
+def test_duplicate_approval_and_a_crash_before_the_reply_give_at_most_one_instruction(tmp_path: Path) -> None:
+    d = tmp_path / "c"
+    ar.init_dir(d)
+    ar.adopt_create(d, 9, "plan", T)
+    ar.adopt_mark(d, 9, "plan", "started", "ctx_1", T)
+    ar.record_create(d, 9, "plan", H, "label", "e1", "u1", T)
+    ar.record_create(d, 9, "plan", H, "comment", "c1", "u1", T)  # duplicate approval, other channel
+    # the coordinator records the instruction first (write-ahead), then replies; it dies before the reply
+    _killed_after(f"ar.record_mark(d, 9, 'plan', {H!r}, 'instructed', {T!r})", d)
+    assert ar.record_show(d, 9, "plan", H)["state"] == "instructed"
+    # the next coordinator pass cannot record a second instruction, so it sends none
+    try:
+        ar.record_mark(d, 9, "plan", H, "instructed", T)
+    except ar.ApprovalError as exc:
+        assert exc.reason == "bad-move"
+    else:
+        raise AssertionError("a second continuation instruction was allowed")
+    # the adoption row still holds exactly one start
+    assert ar.adopt_show(d, 9, "plan")["state"] == "started"
+    assert len(list(d.glob("adoption-*.json"))) == 1 and len(list(d.glob("approval-*.json"))) == 1
diff --git a/tests/issue_pipeline/test_approval_record.py b/tests/issue_pipeline/test_approval_record.py
new file mode 100644
--- /dev/null
+++ b/tests/issue_pipeline/test_approval_record.py
@@ -0,0 +1,242 @@
+"""Task 3: the approval record helper, rows and verbs."""
+
+from __future__ import annotations
+
+import json
+import os
+import stat
+from pathlib import Path
+
+import pytest
+from click.testing import CliRunner
+
+from superclaude.cli.issue_pipeline import approval_record as ar
+from superclaude.cli.issue_pipeline.cli import issue_pipeline_group
+
+H1 = "0123456789abcdef" * 4
+H2 = "fedcba9876543210" * 4
+T = "2026-11-16T10:00:00Z"
+
+
+@pytest.fixture
+def adir(tmp_path: Path) -> Path:
+    d = tmp_path / "approvals"
+    ar.init_dir(d)
+    return d
+
+
+def _adopt_started(d: Path, issue: int = 9) -> None:
+    ar.adopt_create(d, issue, "plan", T)
+    ar.adopt_mark(d, issue, "plan", "started", "ctx_abc123", T)
+
+
+def _create(d: Path, channel: str, ev: str, h: str = H1, issue: int = 9) -> dict:
+    return ar.record_create(d, issue, "plan", h, channel, ev, "u_1", T)
+
+
+def test_init_makes_a_private_directory_and_lock(tmp_path: Path) -> None:
+    d = tmp_path / "x"
+    ar.init_dir(d)
+    ar.init_dir(d)  # safe to repeat
+    assert stat.S_IMODE(d.stat().st_mode) == 0o700
+    assert stat.S_IMODE((d / "lock").stat().st_mode) == 0o600
+
+
+def test_record_create_before_init_fails_with_a_closed_reason(tmp_path: Path) -> None:
+    d = tmp_path / "no-init"
+    d.mkdir()
+    result = CliRunner().invoke(
+        issue_pipeline_group,
+        ["record-create", str(d), "--issue", "9", "--plan-hash", H1, "--channel", "label", "--evidence-id", "e1", "--actor", "u1"],
+    )
+    assert result.exit_code == 1 and result.output.strip() == "refused:not-initialized"
+    assert "Traceback" not in result.output
+    missing = CliRunner().invoke(
+        issue_pipeline_group,
+        ["record-show", str(tmp_path / "absent"), "--issue", "9", "--plan-hash", H1],
+    )
+    assert missing.output.strip() == "refused:no-row"
+
+
+def test_after_init_the_first_call_succeeds(adir: Path) -> None:
+    _adopt_started(adir)
+    assert _create(adir, "label", "e1")["result"] == "created"
+
+
+def test_label_then_comment_leave_one_row_with_two_evidence_entries(adir: Path) -> None:
+    _adopt_started(adir)
+    first = _create(adir, "label", "evt-1")
+    second = _create(adir, "comment", "cmt-2")
+    assert (first["result"], second["result"]) == ("created", "exists")
+    row = ar.record_show(adir, 9, "plan", H1)
+    assert [e["channel"] for e in row["evidence"]] == ["label", "comment"]
+    assert len(list(adir.glob("approval-*.json"))) == 1
+    assert row["record_id"] == "ap-9-plan-" + H1[:12]
+
+
+def test_the_same_evidence_twice_is_not_appended_twice(adir: Path) -> None:
+    _adopt_started(adir)
+    _create(adir, "label", "evt-1")
+    _create(adir, "label", "evt-1")
+    assert len(ar.record_show(adir, 9, "plan", H1)["evidence"]) == 1
+
+
+def test_a_different_plan_hash_makes_a_different_row(adir: Path) -> None:
+    _adopt_started(adir)
+    _create(adir, "label", "evt-1", H1)
+    _create(adir, "label", "evt-1", H2)
+    assert len(list(adir.glob("approval-*.json"))) == 2
+
+
+def test_record_create_needs_an_adoption_row(adir: Path) -> None:
+    with pytest.raises(ar.ApprovalError) as err:
+        _create(adir, "label", "e1")
+    assert err.value.reason == "no-adoption"
+
+
+def test_record_mark_allows_only_forward_moves_and_revoke(adir: Path) -> None:
+    _adopt_started(adir)
+    _create(adir, "label", "e1")
+
+    def mark(state: str) -> str:
+        return ar.record_mark(adir, 9, "plan", H1, state, T)["row"]["state"]
+
+    for bad in ("acked", "recorded", "bogus"):
+        with pytest.raises(ar.ApprovalError) as err:
+            mark(bad)
+        assert err.value.reason == "bad-move"
+    assert mark("instructed") == "instructed"
+    with pytest.raises(ar.ApprovalError):
+        mark("instructed")  # a second continuation instruction is refused
+    assert mark("acked") == "acked"
+    with pytest.raises(ar.ApprovalError):
+        mark("instructed")  # no way back
+    assert mark("revoked") == "revoked"
+    with pytest.raises(ar.ApprovalError):
+        mark("revoked")
+
+
+@pytest.mark.parametrize("prefix", [[], ["instructed"], ["instructed", "acked"]])
+def test_revoke_from_every_state_and_re_approval_reopens_the_same_row(adir: Path, prefix: list[str]) -> None:
+    _adopt_started(adir)
+    _create(adir, "label", "e1")
+    for state in prefix:
+        ar.record_mark(adir, 9, "plan", H1, state, T)
+    assert ar.record_mark(adir, 9, "plan", H1, "revoked", T)["row"]["state"] == "revoked"
+    again = _create(adir, "comment", "c9")
+    assert again["result"] == "exists" and again["row"]["state"] == "recorded"
+    assert len(list(adir.glob("approval-*.json"))) == 1
+
+
+def test_adoption_reserve_start_and_uncertain_paths(adir: Path) -> None:
+    assert ar.adopt_create(adir, 5, "plan", T)["row"]["state"] == "reserved"
+    with pytest.raises(ar.ApprovalError) as err:
+        ar.adopt_create(adir, 5, "plan", T)
+    assert err.value.reason == "uncertain-launch"
+    ar.adopt_mark(adir, 5, "plan", "uncertain", None, T)
+    with pytest.raises(ar.ApprovalError) as err:
+        ar.adopt_create(adir, 5, "plan", T)
+    assert err.value.reason == "uncertain-launch"
+    # a person settles an uncertain row after reading worker-list
+    assert ar.adopt_mark(adir, 5, "plan", "started", "ctx_1", T)["row"]["dispatch_id"] == "ctx_1"
+    with pytest.raises(ar.ApprovalError) as err:
+        ar.adopt_create(adir, 5, "plan", T)
+    assert err.value.reason == "already-started"
+    with pytest.raises(ar.ApprovalError):
+        ar.adopt_mark(adir, 5, "plan", "uncertain", None, T)
+
+
+def test_started_needs_a_valid_dispatch_id(adir: Path) -> None:
+    ar.adopt_create(adir, 5, "plan", T)
+    for bad in (None, "", "has space", "x" * 81):
+        with pytest.raises(ar.ApprovalError) as err:
+            ar.adopt_mark(adir, 5, "plan", "started", bad, T)
+        assert err.value.reason == "bad-dispatch-id"
+
+
+@pytest.mark.parametrize(
+    "kwargs",
+    [
+        {"channel": "email"},
+        {"evidence_id": "has space"},
+        {"evidence_id": "x" * 81},
+        {"actor": "<b>"},
+        {"plan_hash": "ABC"},
+        {"stage": "Plan"},
+        {"issue": 0},
+    ],
+)
+def test_stored_values_must_match_fixed_patterns(adir: Path, kwargs: dict) -> None:
+    _adopt_started(adir)
+    args = {"issue": 9, "stage": "plan", "plan_hash": H1, "channel": "label", "evidence_id": "e1", "actor": "u1", "now": T}
+    args.update(kwargs)
+    with pytest.raises(ar.ApprovalError):
+        ar.record_create(adir, **args)
+
+
+def test_a_corrupt_row_is_a_closed_refusal_and_files_are_private(adir: Path) -> None:
+    _adopt_started(adir)
+    _create(adir, "label", "e1")
+    row_file = next(adir.glob("approval-*.json"))
+    assert stat.S_IMODE(row_file.stat().st_mode) == 0o600
+    row_file.write_text("{not json")
+    with pytest.raises(ar.ApprovalError) as err:
+        ar.record_show(adir, 9, "plan", H1)
+    assert err.value.reason == "row-invalid"
+
+
+def test_a_symlinked_row_is_refused(adir: Path, tmp_path: Path) -> None:
+    target = tmp_path / "elsewhere.json"
+    target.write_text(json.dumps({"state": "recorded"}))
+    (adir / "adoption-9-plan.json").symlink_to(target)
+    with pytest.raises(ar.ApprovalError) as err:
+        ar.adopt_create(adir, 9, "plan", T)
+    assert err.value.reason == "row-invalid"
+
+
+def test_cli_round_trip_prints_closed_json(adir: Path) -> None:
+    run = CliRunner()
+    base = [str(adir), "--issue", "9"]
+    assert json.loads(run.invoke(issue_pipeline_group, ["adopt-create", *base]).output)["result"] == "created"
+    run.invoke(issue_pipeline_group, ["adopt-mark", *base, "--state", "started", "--dispatch-id", "ctx_1"])
+    made = run.invoke(
+        issue_pipeline_group,
+        ["record-create", *base, "--plan-hash", H1, "--channel", "label", "--evidence-id", "e1", "--actor", "u1"],
+    )
+    assert json.loads(made.output)["row"]["state"] == "recorded"
+    marked = run.invoke(issue_pipeline_group, ["record-mark", *base, "--plan-hash", H1, "--state", "instructed"])
+    assert json.loads(marked.output)["row"]["state"] == "instructed"
+    shown = run.invoke(issue_pipeline_group, ["record-show", *base, "--plan-hash", H1])
+    assert json.loads(shown.output)["row"]["state"] == "instructed"
+    again = run.invoke(issue_pipeline_group, ["record-mark", *base, "--plan-hash", H1, "--state", "instructed"])
+    assert (again.exit_code, again.output.strip()) == (1, "refused:bad-move")
+
+
+def test_lock_held_reports_retry_with_exit_75(adir: Path) -> None:
+    import fcntl
+
+    _adopt_started(adir)
+    fd = os.open(adir / "lock", os.O_RDWR)
+    try:
+        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
+        result = CliRunner().invoke(
+            issue_pipeline_group,
+            ["record-create", str(adir), "--issue", "9", "--plan-hash", H1, "--channel", "label", "--evidence-id", "e1", "--actor", "u1"],
+        )
+    finally:
+        os.close(fd)
+    assert (result.exit_code, result.output.strip()) == (75, "lock-held, retry")
+    # the retry appends the evidence
+    assert _create(adir, "label", "e1")["result"] == "created"
+
+
+def test_the_watcher_record_module_is_not_edited() -> None:
+    import subprocess
+
+    out = subprocess.run(
+        ["git", "diff", "--stat", "HEAD", "--", "src/superclaude/cli/issue_watch/record.py"],
+        capture_output=True,
+        text=True,
+        check=True,
+    ).stdout
+    assert out.strip() == ""

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
