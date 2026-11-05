4f36aedd1a2f82d7887bd0354a30a14831a26323
Review one task for spec compliance.

Task brief: ## Task 7: Make the run-log fold kind-aware and conflict-cycle aware in `run_log.py`

Depends on: Task 2

Implement step 6 of source section 13 in `src/superclaude/pr_submit/run_log.py` `rebuild_state` per source section 6.3 items 1 to 6:

- New state keys `sync_push_count`, `conflict_cycles`, `open_conflict_cycle`, `push_rejected`; fold branches for `sync_started`, `sync_concluded`, `push_initiated` (open-cycle flags, `target_sha`, `expect_checks` stored as `True` when missing or non-bool, `superseded` for other open cycles), the kind-aware `push_completed`, and `push_aborted_or_not_landed` with `rejected is True`; `IDEMPOTENCY_SETS` unchanged; docstring updated.
- Tests in `tests/pr_submit/test_run_log.py`: every new function listed for that file in source section 12.2, including the recorded legacy-log fixture test and the redaction test.

Acceptance criteria:
- A legacy log without `kind` or conflict events rebuilds with every pre-existing key equal and the new keys at their defaults.
- A `sync` push increments `sync_push_count` and not `push_count`; `fix`, `ci`, `merge` and kind-less pushes increment `push_count`.
- `conflict_cycles` keeps first-seen order and counts a resume restart's reused id once; `open_conflict_cycle` carries `hook` and `review_terminal`; a later push of another cycle marks the open cycle `superseded`.
- `len(IDEMPOTENCY_SETS) == 7` (`tests/pr_submit/test_idempotency.py:89`) still passes.
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_idempotency.py -q` passes; log saved to `./artifacts/t7-tests.log`.
Global constraints: 
- The design in `./source.md` is the specification. Every section reference below (for example "source section 5.3") points into it. Where a task and the source disagree, the source wins; record the disagreement in the task's evidence.
- Never force-push, and never write a force flag after the words "git push" on any line of a `.md` or `.sh` file in `src/superclaude/skills/sc-pr-submit-protocol/` (the force-push scan in `tests/pr_submit/test_static_grep.py:758-776` covers every such file). The only push text is `git push origin <target_sha>:<HEAD_BRANCH>`; prohibitions are written in words.
- `push_parent_ok`, `evaluate_push_decision`, `push_fail_state`, `push_idempotency_key`, `needs_rebase` and every existing `transition()` edge in `src/superclaude/pr_submit/fsm.py` stay byte-identical (source section 6.1). `resolve_crash_window` in `recovery.py` keeps its signature and return value.
- T-N50: no `git` or `gh` token (regex `\bgh\b|\bgit\b`), docstrings and comments included, in `conflicts.py`, `fsm.py`, `ci.py`, `refs/state-machine.md`, `refs/loop-guard.md` and every other file in `CORE_PURE_FILES` (`tests/pr_submit/test_static_grep.py:37-51`).
- Installed primitives (`SKILL.md`, refs, scripts, `commands/pr-submit.md`) never name a `src/superclaude/` path in new text.
- Every `gh` call in new text carries `--repo "$REPO"` or a `repos/<owner/repo>/` path. Nothing contacts `SuperClaude-Org/SuperClaude_Framework`.
- Never stash, never use a hook-skipping flag, never amend, never stage everything; stage exact paths only.
- `SKILL.md` keeps exactly one python code block (`tests/pr_submit/test_cosmos_protocol.py:36`, `tests/pr_submit/test_codex_reviews.py:688`) and grows by at most 15 lines (source section 8.1).
- Edit `src/superclaude/`, then run `make sync-dev`; never stage `.claude/` paths except `.claude/settings.json`. `.dev/tasks/` is always staged (`git add .dev/tasks`), including this package and its `artifacts/`.
- Python through UV only (`uv run pytest ...`, `uv run python ...`). Run the tests each task names plus `tests/pr_submit/`, `tests/unit/test_cli_install.py` and `tests/commands/`; do not run the full suite (`make test`) or `tests/cli/eval/` as a directory (orchestrator brief; this overrides the `make test` step of source section 12.5).
- Real-git tests run only inside pytest temporary directories with a local bare repository as `origin`, a `gh` stub on `PATH`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, and for real `uv` `UV_OFFLINE=1`, `UV_NO_CONFIG=1`, `UV_CACHE_DIR=<tmp>` (source section 12 preamble). No test touches the network or `~/.claude`.
- Out of scope: P3 late re-sync (#361) and the post-release verification follow-ups V1 to V8 of source section 14; they are not implemented by this plan.
- Task evidence (test logs, grep output) goes under `./artifacts/` in this package.
Start sha: 4f36aedd1a2f82d7887bd0354a30a14831a26323
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/run_log.py b/src/superclaude/pr_submit/run_log.py
index 5f143c44..1e2c1e43 100644
--- a/src/superclaude/pr_submit/run_log.py
+++ b/src/superclaude/pr_submit/run_log.py
@@ -57,6 +57,12 @@ def fix_key(path: str, line: int | str, body: str) -> str:
     return hashlib.sha256(f"{path}\n{line}\n{body}".encode("utf-8")).hexdigest()
 
 
+def _cycle_key(event: dict) -> str | None:
+    """The event's ``cycle_id`` when it is a string, else ``None`` (never unhashable)."""
+    cycle_id = event.get("cycle_id")
+    return cycle_id if isinstance(cycle_id, str) else None
+
+
 def _redact(value):
     """Recursively scrub credential/token patterns from a value (NFR-7)."""
     if isinstance(value, str):
@@ -171,6 +177,30 @@ class RunLog:
         still counts once each, so old logs rebuild to the same number).
         ``absent_reviewers`` is the sorted set of reviewers named by
         ``reviewer_absent`` events.
+
+        Issue #305 (conflict cycles and push kinds) adds four keys:
+
+        - ``sync_push_count``: landed ``push_completed`` events with ``kind ==
+          "sync"``. Such pushes do NOT count in ``push_count``; every other kind
+          (``fix``, ``merge``, ``ci``, or absent, which means ``fix``) does.
+        - ``conflict_cycles``: the distinct ``cycle_id`` values of ``sync_started``
+          events in first-seen order (not sorted); a resume restart that re-opens
+          the same id is counted once.
+        - ``open_conflict_cycle``: the open cycle whose ``sync_started`` came last,
+          or ``None``. A cycle opens on ``sync_started`` (the entry is the event's
+          payload, so it carries ``hook``, ``review_terminal``, ``kind``,
+          ``base_sha`` and ``pre_push_sha``, plus the flags ``push_initiated``,
+          ``push_completed`` and ``superseded`` and the ``target_sha`` and
+          ``expect_checks`` copied from its ``push_initiated``) and closes on
+          ``sync_concluded``. A missing or non-bool ``expect_checks`` is stored as
+          ``True`` (fail closed). A ``push_initiated`` of any other cycle marks
+          every still-open cycle ``superseded``.
+        - ``push_rejected``: ``True`` once a ``push_aborted_or_not_landed`` event
+          carries ``rejected is True``.
+
+        A log without ``kind`` fields or conflict-cycle events rebuilds every
+        pre-existing key exactly as before, with the four keys at their defaults
+        (``0``, ``[]``, ``None``, ``False``) (NFR-12).
         """
         state = {
             "pr_number": self.pr_number,
@@ -186,10 +216,18 @@ class RunLog:
             "absent_reviewers": [],
             "last_event_id": 0,
             **{s: [] for s in IDEMPOTENCY_SETS},
+            # Issue #305 (design section 6.3): push kinds and conflict cycles.
+            "sync_push_count": 0,
+            "conflict_cycles": [],
+            "open_conflict_cycle": None,
+            "push_rejected": False,
         }
         sets = {s: set() for s in IDEMPOTENCY_SETS}
         retriggered_cycles: set = set()
         absent: set = set()
+        # Open conflict cycles by id; insertion order is sync_started order (a
+        # re-opened id is moved to the end), so the last entry is the newest.
+        open_cycles: dict = {}
         for ev in self.read_events():
             state["last_event_id"] = ev.get("event_id", state["last_event_id"])
             et = ev.get("event_type")
@@ -235,10 +273,55 @@ class RunLog:
                 state["effective_max_rounds"] = (
                     clamp if prev is None else min(prev, clamp)
                 )
+            elif et == EventType.SYNC_STARTED.value:
+                cycle_id = _cycle_key(ev)
+                if cycle_id is not None:
+                    if cycle_id not in state["conflict_cycles"]:
+                        state["conflict_cycles"].append(cycle_id)
+                    # A resume restart re-opens the same id; it becomes the newest.
+                    open_cycles.pop(cycle_id, None)
+                    open_cycles[cycle_id] = {
+                        **ev,
+                        "push_initiated": False,
+                        "push_completed": False,
+                        "target_sha": None,
+                        "expect_checks": None,
+                        "superseded": False,
+                    }
+            elif et == EventType.SYNC_CONCLUDED.value:
+                cycle_id = _cycle_key(ev)
+                if cycle_id is not None:
+                    open_cycles.pop(cycle_id, None)
+            elif et == EventType.PUSH_INITIATED.value:
+                cycle_id = _cycle_key(ev)
+                for open_id, entry in open_cycles.items():
+                    if open_id == cycle_id:
+                        expect = ev.get("expect_checks")
+                        entry["push_initiated"] = True
+                        entry["target_sha"] = ev.get("target_sha")
+                        # Fail closed: never a None or defaulted False here.
+                        entry["expect_checks"] = (
+                            expect if isinstance(expect, bool) else True
+                        )
+                    else:
+                        # A push of another cycle: this one was never closed.
+                        entry["superseded"] = True
             elif et == EventType.PUSH_COMPLETED.value:
-                state["push_count"] += 1
+                # Kind-aware count: absent means "fix"; only "sync" is excluded.
+                if (ev.get("kind") or "fix") == "sync":
+                    state["sync_push_count"] += 1
+                else:
+                    state["push_count"] += 1
                 if ev.get("target_sha"):
                     sets["pushed_commit_shas"].add(ev["target_sha"])
+                cycle_id = _cycle_key(ev)
+                if cycle_id is not None and cycle_id in open_cycles:
+                    open_cycles[cycle_id]["push_completed"] = True
+            elif (
+                et == EventType.PUSH_ABORTED_OR_NOT_LANDED.value
+                and ev.get("rejected") is True
+            ):
+                state["push_rejected"] = True
             elif et == EventType.REPLY_POSTED.value:
                 state["reply_count"] += 1
                 if ev.get("comment_id") is not None:
@@ -257,6 +340,9 @@ class RunLog:
         for s in IDEMPOTENCY_SETS:
             state[s] = sorted(sets[s], key=str)
         state["absent_reviewers"] = sorted(absent)
+        state["open_conflict_cycle"] = (
+            list(open_cycles.values())[-1] if open_cycles else None
+        )
         return state
 
     def materialize_snapshot(self) -> dict:
diff --git a/tests/pr_submit/test_run_log.py b/tests/pr_submit/test_run_log.py
index 022bbf42..56830364 100644
--- a/tests/pr_submit/test_run_log.py
+++ b/tests/pr_submit/test_run_log.py
@@ -12,7 +12,13 @@ import json
 
 import pytest
 
-from superclaude.pr_submit.fsm import RunConfig, run_skill
+from superclaude.pr_submit.conflicts import conflict_resume_plan
+from superclaude.pr_submit.fsm import (
+    RunConfig,
+    build_push_triad,
+    evaluate_push_decision,
+    run_skill,
+)
 from superclaude.pr_submit.models import EventType, Finding
 from superclaude.pr_submit.run_log import RunLog, fix_key
 
@@ -250,3 +256,407 @@ def test_absent_reviewers_fold_is_a_set_and_seeded_empty(tmp_path):
     rl.append({"event_type": EventType.REVIEWER_ABSENT.value, "reviewer": "codex"})
     rl.append({"event_type": EventType.REVIEWER_ABSENT.value, "reviewer": "codex"})
     assert rl.rebuild_state()["absent_reviewers"] == ["codex"]
+
+
+# --- issue #305: kind-aware, conflict-cycle-aware fold (design section 6.3) ----
+
+_SHA_A = "a" * 40
+_SHA_B = "b" * 40
+_SHA_C = "c" * 40
+_SHA_D = "d" * 40
+_SHA_E = "e" * 40
+
+# A recorded legacy run-log (pre-#305 shape: no `kind`, no conflict-cycle events),
+# written verbatim as JSONL lines. Its pre-change fold, captured from the
+# unmodified `rebuild_state` before the #305 edit, is `_LEGACY_EXPECTED`.
+_LEGACY_JSONL = (
+    '{"schema_version": "1.0", "event_id": 1, "event_type": "run_started", "state_after": "S0_IDLE", "timestamp": "2026-06-11T00:00:01Z"}',
+    '{"schema_version": "1.0", "event_id": 2, "event_type": "monitor_armed", "state_after": "S2_CLASSIFY", "timestamp": "2026-06-11T00:00:02Z"}',
+    '{"schema_version": "1.0", "event_id": 3, "event_type": "findings_normalized", "review_id": 101, "timestamp": "2026-06-11T00:00:03Z"}',
+    '{"schema_version": "1.0", "event_id": 4, "event_type": "fix_applied", "fix_key": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "state_after": "S3_FIXING", "timestamp": "2026-06-11T00:00:04Z"}',
+    '{"schema_version": "1.0", "event_id": 5, "event_type": "validation_completed", "state_after": "S7_VALIDATING", "timestamp": "2026-06-11T00:00:05Z"}',
+    '{"schema_version": "1.0", "event_id": 6, "event_type": "push_decision", "run_id": "r1", "cycle_id": "c1", "idempotency_key": "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", "pre_push_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "target_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "timestamp": "2026-06-11T00:00:06Z"}',
+    '{"schema_version": "1.0", "event_id": 7, "event_type": "push_initiated", "run_id": "r1", "cycle_id": "c1", "idempotency_key": "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", "pre_push_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "target_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "state_after": "S4_PUSHING", "timestamp": "2026-06-11T00:00:07Z"}',
+    '{"schema_version": "1.0", "event_id": 8, "event_type": "push_completed", "run_id": "r1", "cycle_id": "c1", "idempotency_key": "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", "pre_push_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "target_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "timestamp": "2026-06-11T00:00:08Z"}',
+    '{"schema_version": "1.0", "event_id": 9, "event_type": "reply_posted", "comment_id": 55, "state_after": "S6_REPLYING", "timestamp": "2026-06-11T00:00:09Z"}',
+    '{"schema_version": "1.0", "event_id": 10, "event_type": "thread_resolved", "thread_id": "PRRT_1", "state_after": "RESOLVING", "timestamp": "2026-06-11T00:00:10Z"}',
+    '{"schema_version": "1.0", "event_id": 11, "event_type": "rereview_requested", "cycle_id": "c1", "reviewer": "augment", "state_after": "S5a_RETRIGGER_REVIEW", "timestamp": "2026-06-11T00:00:11Z"}',
+    '{"schema_version": "1.0", "event_id": 12, "event_type": "rereview_requested", "cycle_id": "c1", "reviewer": "codex", "timestamp": "2026-06-11T00:00:12Z"}',
+    '{"schema_version": "1.0", "event_id": 13, "event_type": "round_incremented", "state_after": "S5_AWAITING_REREVIEW", "timestamp": "2026-06-11T00:00:13Z"}',
+    '{"schema_version": "1.0", "event_id": 14, "event_type": "reviewer_absent", "reviewer": "codex", "timestamp": "2026-06-11T00:00:14Z"}',
+    '{"schema_version": "1.0", "event_id": 15, "event_type": "silence_rerequested", "pr_number": 77, "elapsed": 600, "timestamp": "2026-06-11T00:00:15Z"}',
+    '{"schema_version": "1.0", "event_id": 16, "event_type": "auggie_fallback_invoked", "pr_number": 77, "timestamp": "2026-06-11T00:00:16Z"}',
+    '{"schema_version": "1.0", "event_id": 17, "event_type": "max_rounds_clamped", "effective_max_rounds": 2, "timestamp": "2026-06-11T00:00:17Z"}',
+    '{"schema_version": "1.0", "event_id": 18, "event_type": "push_aborted_or_not_landed", "cycle_id": "c2", "idempotency_key": "jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj", "timestamp": "2026-06-11T00:00:18Z"}',
+    '{"schema_version": "1.0", "event_id": 19, "event_type": "terminal_clean", "state_after": "TERMINAL_CLEAN", "timestamp": "2026-06-11T00:00:19Z"}',
+)
+_LEGACY_EXPECTED = {
+    "pr_number": 77,
+    "state": "TERMINAL_CLEAN",
+    "round_counter": 1,
+    "push_count": 1,
+    "reply_count": 1,
+    "rereview_request_count": 1,
+    "effective_max_rounds": 2,
+    "silence_rerequested_at": 600,
+    "absent_reviewers": ["codex"],
+    "last_event_id": 19,
+    "processed_review_ids": [101],
+    "processed_finding_ids": ["f" * 64],
+    "replied_comment_ids": [55],
+    "resolved_thread_ids": ["PRRT_1"],
+    "pushed_commit_shas": [_SHA_A],
+    "auggie_review_invoked": [77],
+    "silence_rerequest_invoked": [77],
+}
+_NEW_KEY_DEFAULTS = {
+    "sync_push_count": 0,
+    "conflict_cycles": [],
+    "open_conflict_cycle": None,
+    "push_rejected": False,
+}
+
+
+def _legacy_runlog(tmp_path) -> RunLog:
+    """Write the recorded legacy JSONL verbatim, then open it as a resumed RunLog."""
+    path = tmp_path / "monitor-run-77.jsonl"
+    path.write_text("\n".join(_LEGACY_JSONL) + "\n", encoding="utf-8")
+    return RunLog(77, tmp_path)
+
+
+def _push(
+    rl: RunLog,
+    cycle_id: str,
+    pre_push_sha: str,
+    target_sha: str,
+    *,
+    land: bool = True,
+    **extras,
+) -> None:
+    """Append a push triad built by the real builder (the completed record only if ``land``)."""
+    decision = evaluate_push_decision(
+        monitor_ordinal=3,
+        validation_status="validated",
+        needs_human_decision=False,
+        round_counter=0,
+        max_rounds=3,
+        applied_edits=1,
+    )
+    triad = build_push_triad(
+        run_id="r1",
+        cycle_id=cycle_id,
+        round_counter=0,
+        pre_push_sha=pre_push_sha,
+        target_sha=target_sha,
+        target_branch="feature",
+        target_remote="origin",
+        decision=decision,
+        **extras,
+    )
+    for record in triad if land else triad[:2]:
+        rl.append(record)
+
+
+def _sync_started(rl: RunLog, cycle_id: str, **overrides) -> None:
+    tier = 2 if cycle_id.startswith("conflict-") else 1
+    event = {
+        "event_type": EventType.SYNC_STARTED.value,
+        "run_id": "r1",
+        "cycle_id": cycle_id,
+        "tier": tier,
+        "kind": "merge" if tier == 2 else "sync",
+        "hook": "c_initial" if tier == 2 else "wave8a",
+        "base_ref": "origin/master",
+        "base_sha": _SHA_C,
+        "pre_push_sha": _SHA_B,
+        "merge_tree_oid": _SHA_E,
+        "conflict_max_tier": tier,
+        "review_terminal": None if tier == 2 else "clean",
+        "paths": ["uv.lock"],
+        "resumed": False,
+    }
+    event.update(overrides)
+    rl.append(event)
+
+
+def _sync_concluded(rl: RunLog, cycle_id: str, outcome: str = "pushed", **extra):
+    rl.append(
+        {
+            "event_type": EventType.SYNC_CONCLUDED.value,
+            "cycle_id": cycle_id,
+            "outcome": outcome,
+            "merge_sha": _SHA_D if outcome == "pushed" else None,
+            "record_path": None,
+            "dropped": [],
+            "reason": None,
+            "recovered": False,
+            **extra,
+        }
+    )
+
+
+def test_fold_old_log_without_kind_rebuilds_identically(tmp_path):
+    """NFR-12: a recorded legacy log rebuilds every pre-existing key unchanged and
+    the four new keys at their defaults; no other key is added."""
+    state = _legacy_runlog(tmp_path).rebuild_state()
+    assert {k: state[k] for k in _LEGACY_EXPECTED} == _LEGACY_EXPECTED
+    assert set(state) == set(_LEGACY_EXPECTED) | set(_NEW_KEY_DEFAULTS)
+    assert state == {**_LEGACY_EXPECTED, **_NEW_KEY_DEFAULTS}
+
+
+def test_fold_sync_push_counts_in_sync_push_count_not_push_count(tmp_path):
+    """A landed `kind: "sync"` push counts in sync_push_count only (INV-018)."""
+    rl = RunLog(201, tmp_path)
+    _push(rl, "sync-1", _SHA_B, _SHA_D, push_kind="sync", base_sha=_SHA_C)
+    state = rl.rebuild_state()
+    assert state["sync_push_count"] == 1
+    assert state["push_count"] == 0
+    assert state["pushed_commit_shas"] == [_SHA_D]
+
+
+@pytest.mark.parametrize("push_kind", ["fix", "ci", "merge", None])
+def test_fold_fix_ci_merge_and_kindless_pushes_count_in_push_count(tmp_path, push_kind):
+    """`fix`, `ci`, `merge` and kind-less landed pushes count in push_count."""
+    rl = RunLog(202, tmp_path)
+    _push(rl, "c1", _SHA_B, _SHA_A, push_kind=push_kind)
+    # A falsy `kind` reads as `fix` too (absent means fix).
+    rl.append(
+        {
+            "event_type": EventType.PUSH_COMPLETED.value,
+            "kind": "",
+            "target_sha": _SHA_E,
+        }
+    )
+    state = rl.rebuild_state()
+    assert state["push_count"] == 2
+    assert state["sync_push_count"] == 0
+    assert state["pushed_commit_shas"] == [_SHA_A, _SHA_E]
+
+
+def test_fold_conflict_cycles_first_seen_order_and_open_cycle(tmp_path):
+    """conflict_cycles keeps first-seen order (not sorted) and counts a resume
+    restart's reused id once; the open cycle tracks push_initiated / push_completed."""
+    rl = RunLog(203, tmp_path)
+    _sync_started(rl, "sync-2")
+    _sync_concluded(rl, "sync-2", "aborted")
+    _sync_started(rl, "conflict-1")
+    state = rl.rebuild_state()
+    assert state["conflict_cycles"] == ["sync-2", "conflict-1"]
+    assert state["open_conflict_cycle"]["cycle_id"] == "conflict-1"
+    # A resume restart: close the open attempt, re-open the same id.
+    _sync_concluded(rl, "conflict-1", "aborted", recovered=True)
+    _sync_started(rl, "conflict-1", resumed=True)
+    state = rl.rebuild_state()
+    assert state["conflict_cycles"] == ["sync-2", "conflict-1"]
+    open_cycle = state["open_conflict_cycle"]
+    assert open_cycle["cycle_id"] == "conflict-1"
+    assert open_cycle["resumed"] is True
+    assert (open_cycle["push_initiated"], open_cycle["push_completed"]) == (
+        False,
+        False,
+    )
+    assert open_cycle["target_sha"] is None
+    assert open_cycle["expect_checks"] is None
+    assert open_cycle["superseded"] is False
+    # push_initiated sets its flag, target_sha and a bool expect_checks.
+    _push(
+        rl,
+        "conflict-1",
+        _SHA_B,
+        _SHA_D,
+        land=False,
+        push_kind="merge",
+        base_sha=_SHA_C,
+        expect_checks=False,
+    )
+    open_cycle = rl.rebuild_state()["open_conflict_cycle"]
+    assert (open_cycle["push_initiated"], open_cycle["push_completed"]) == (
+        True,
+        False,
+    )
+    assert open_cycle["target_sha"] == _SHA_D
+    assert open_cycle["expect_checks"] is False
+    # push_completed sets its flag; the cycle stays open until sync_concluded.
+    rl.append(
+        {
+            "event_type": EventType.PUSH_COMPLETED.value,
+            "cycle_id": "conflict-1",
+            "kind": "merge",
+            "target_sha": _SHA_D,
+        }
+    )
+    state = rl.rebuild_state()
+    assert state["open_conflict_cycle"]["push_completed"] is True
+    assert state["push_count"] == 1
+    _sync_concluded(rl, "conflict-1")
+    state = rl.rebuild_state()
+    assert state["open_conflict_cycle"] is None
+    assert state["conflict_cycles"] == ["sync-2", "conflict-1"]
+
+
+@pytest.mark.parametrize("raw", ["absent", None, "yes", 1, 0])
+def test_fold_push_initiated_expect_checks_fails_closed_to_true(tmp_path, raw):
+    """A missing or non-bool expect_checks on the cycle's push_initiated is stored
+    as True, so conflict_resume_plan row 4 never reads None or a defaulted False."""
+    rl = RunLog(204, tmp_path)
+    _sync_started(rl, "sync-1")
+    record = {
+        "event_type": EventType.PUSH_INITIATED.value,
+        "cycle_id": "sync-1",
+        "kind": "sync",
+        "target_sha": _SHA_D,
+    }
+    if raw != "absent":
+        record["expect_checks"] = raw
+    rl.append(record)
+    assert rl.rebuild_state()["open_conflict_cycle"]["expect_checks"] is True
+
+
+def test_fold_push_rejected(tmp_path):
+    """push_aborted_or_not_landed with `rejected is True` sets push_rejected; a
+    Branch B record without it, or with a truthy non-True value, does not."""
+    rl = RunLog(205, tmp_path)
+    for rejected in ("absent", False, "true", 1):
+        record = {
+            "event_type": EventType.PUSH_ABORTED_OR_NOT_LANDED.value,
+            "cycle_id": "c1",
+        }
+        if rejected != "absent":
+            record["rejected"] = rejected
+        rl.append(record)
+    assert rl.rebuild_state()["push_rejected"] is False
+    rl.append(
+        {
+            "event_type": EventType.PUSH_ABORTED_OR_NOT_LANDED.value,
+            "cycle_id": "sync-1",
+            "rejected": True,
+            "stderr_tail": "! [rejected] (fetch first)",
+        }
+    )
+    assert rl.rebuild_state()["push_rejected"] is True
+
+
+def test_fold_open_cycle_carries_hook_and_review_terminal(tmp_path):
+    """B3: the open-cycle entry carries `hook` and `review_terminal` from its
+    sync_started, which conflict_resume_plan rows 4c, 5 and 7 read."""
+    rl = RunLog(206, tmp_path)
+    _sync_started(rl, "sync-1", review_terminal="halt_max_rounds")
+    open_cycle = rl.rebuild_state()["open_conflict_cycle"]
+    assert open_cycle["hook"] == "wave8a"
+    assert open_cycle["review_terminal"] == "halt_max_rounds"
+    assert open_cycle["kind"] == "sync"
+    assert open_cycle["base_sha"] == _SHA_C
+    assert open_cycle["pre_push_sha"] == _SHA_B
+    _sync_concluded(rl, "sync-1", "aborted")
+    _sync_started(rl, "conflict-1")
+    open_cycle = rl.rebuild_state()["open_conflict_cycle"]
+    assert open_cycle["hook"] == "c_initial"
+    assert open_cycle["review_terminal"] is None
+    # The fold's output is exactly what the resume planner reads (row 4: a landed
+    # sync push with no expect_checks on its push_initiated reads as True).
+    rl2 = RunLog(207, tmp_path / "row4")
+    _sync_started(rl2, "sync-1")
+    _push(rl2, "sync-1", _SHA_B, _SHA_D, push_kind="sync", base_sha=_SHA_C)
+    plan = conflict_resume_plan(
+        rl2.rebuild_state(),
+        foreign_op=None,
+        merge_head_sha=None,
+        local_head_sha=_SHA_D,
+        local_head_parents=[_SHA_B, _SHA_C],
+        dangling=None,
+    )
+    assert plan.directive == "complete_after_push"
+    assert (plan.cycle_id, plan.hook, plan.review_terminal) == (
+        "sync-1",
+        "wave8a",
+        "clean",
+    )
+    assert plan.wait_sha == _SHA_D
+    assert plan.expect_checks is True
+
+
+def test_fold_push_of_another_cycle_marks_open_cycle_superseded(tmp_path):
+    """B2 belt: a push_initiated of a different cycle marks the still-open cycle
+    superseded (conflict_resume_plan row 3b halts on it); its own push does not."""
+    rl = RunLog(208, tmp_path)
+    _sync_started(rl, "sync-1")
+    _push(rl, "sync-1", _SHA_B, _SHA_D, land=False, push_kind="sync", base_sha=_SHA_C)
+    assert rl.rebuild_state()["open_conflict_cycle"]["superseded"] is False
+    _push(rl, "fix-cycle-2", _SHA_D, _SHA_A)
+    state = rl.rebuild_state()
+    open_cycle = state["open_conflict_cycle"]
+    assert open_cycle["cycle_id"] == "sync-1"
+    assert open_cycle["superseded"] is True
+    assert open_cycle["push_completed"] is False  # another cycle's completion
+    plan = conflict_resume_plan(
+        state,
+        foreign_op=None,
+        merge_head_sha=None,
+        local_head_sha=_SHA_A,
+        local_head_parents=[_SHA_D],
+        dangling=None,
+    )
+    assert (plan.directive, plan.reason, plan.cycle_id) == (
+        "halt",
+        "resume_unrepresentable",
+        "sync-1",
+    )
+
+
+def test_rebuild_state_with_a_conflict_push_in_the_fixture(tmp_path):
+    """QA-1: the legacy fixture (one fix push, one round tick, one re-triggered
+    cycle) plus a Tier 1 sync push and a Tier 2 merge push with its re-review and
+    round tick folds to exact counters."""
+    rl = _legacy_runlog(tmp_path)
+    # Tier 1 sync cycle (Wave 8a): never ticks a round, never counts in push_count.
+    _sync_started(rl, "sync-1")
+    _push(
+        rl,
+        "sync-1",
+        _SHA_B,
+        _SHA_D,
+        push_kind="sync",
+        base_sha=_SHA_C,
+        review_terminal="clean",
+        expect_checks=True,
+    )
+    _sync_concluded(rl, "sync-1")
+    # Tier 2 merge cycle (C-initial): counts in push_count, re-review, round tick.
+    _sync_started(rl, "conflict-2", pre_push_sha=_SHA_D)
+    _push(rl, "conflict-2", _SHA_D, _SHA_E, push_kind="merge", base_sha=_SHA_C)
+    _sync_concluded(rl, "conflict-2", merge_sha=_SHA_E)
+    for reviewer in ("augment", "codex"):
+        rl.append(
+            {
+                "event_type": EventType.REREVIEW_REQUESTED.value,
+                "cycle_id": "conflict-2",
+                "reviewer": reviewer,
+            }
+        )
+    rl.append({"event_type": EventType.ROUND_INCREMENTED.value})
+    state = rl.rebuild_state()
+    assert state["push_count"] == 2  # the legacy fix push + the merge push
+    assert state["sync_push_count"] == 1
+    assert state["round_counter"] == 2  # the legacy tick + the merge cycle's tick
+    assert state["rereview_request_count"] == 2  # cycles c1 and conflict-2
+    assert state["conflict_cycles"] == ["sync-1", "conflict-2"]
+    assert state["open_conflict_cycle"] is None
+    assert state["push_rejected"] is False
+    assert state["pushed_commit_shas"] == [_SHA_A, _SHA_D, _SHA_E]
+
+
+def test_sync_concluded_payload_is_redacted(tmp_path):
+    """NFR-7: a token-shaped string in a sync_concluded `dropped` list reaches the
+    JSONL as [REDACTED]."""
+    rl = RunLog(209, tmp_path)
+    token = "ghp_ABCDEFGHIJKLMNOP0123456789"
+    _sync_concluded(
+        rl,
+        "conflict-1",
+        dropped=[f"removed the line export GH_TOKEN={token}", token],
+    )
+    raw = rl.jsonl_path.read_text(encoding="utf-8")
+    assert "ghp_ABCDEFGHIJKLMNOP" not in raw
+    dropped = json.loads(raw.splitlines()[-1])["dropped"]
+    assert dropped[1] == "[REDACTED]"
+    assert "[REDACTED]" in dropped[0]
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t7-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t7-tests.log
new file mode 100644
index 00000000..df7d1cdf
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t7-tests.log
@@ -0,0 +1,13 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 35 items
+
+tests/pr_submit/test_run_log.py .............................            [ 82%]
+tests/pr_submit/test_idempotency.py ......                               [100%]
+
+============================== 35 passed in 0.19s ==============================

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
