c5e10e57d15a4207a73ac41394d9f3d34275defb
Review one task for spec compliance.

Task brief: ## Task 8: Add kind-aware crash recovery to `recovery.py`

Depends on: Task 4, Task 7

Implement step 7 of source section 13 in `src/superclaude/pr_submit/recovery.py` per source section 6.4:

- Add `"kind"` and `"base_sha"` to the copied key tuple (`:98-110`), copied only when present.
- Add `resolve_crash_window_plan(run_log, dangling, *, remote_reachable, observed_remote_sha=None)` exactly as in source section 6.4 item 2, so Branch A and C and halt directives close an open conflict cycle once with `sync_concluded{recovered: true}`; Branch B leaves closing to the SKILL; module docstring paragraph, token-free.
- Tests in `tests/pr_submit/test_crash_recovery.py`: every new function listed for that file in source section 12.2 (by-kind parametrization, recovered record copies, legacy byte-equality, rejected-push record, cycle closing, conflict crash then fix crash, restart row with recorded `review_terminal`, both N1 re-drive tests, row 1 closing, row 4 `expect_checks` default, Branch B landed close, Branch C event order).

Acceptance criteria:
- For kinds `fix` and absent, the returned plan and the appended events are byte-equal to today's `resolve_crash_window` behaviour; existing tests in `test_crash_recovery.py`, `test_augment_review_remediation.py:145` and `test_codex_reviews.py:489` pass unmodified.
- `sync` and `ci` never resume into `S4_PUSHING`, S5a or S5; a second wrapper call appends nothing.
- After a recovered conflict crash, a later fix-push crash window is returned by `detect_crash_window` and `conflict_resume_plan` returns `none`.
- `uv run pytest tests/pr_submit/test_crash_recovery.py tests/pr_submit/test_augment_review_remediation.py tests/pr_submit/test_codex_reviews.py -q` passes; log saved to `./artifacts/t8-tests.log`.
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
Start sha: c5e10e57d15a4207a73ac41394d9f3d34275defb
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/recovery.py b/src/superclaude/pr_submit/recovery.py
index 02e8bec6..c6ee801c 100644
--- a/src/superclaude/pr_submit/recovery.py
+++ b/src/superclaude/pr_submit/recovery.py
@@ -17,10 +17,22 @@ queries the remote for ``target_sha`` and branches three ways:
 Core purity: the LIVE remote query is performed by the SKILL/script; this module
 DECIDES the branch from data, consuming the remote-reachability result as an input.
 It contains no shell or version-control command tokens.
+
+Push kinds (issue #305): a push record may carry ``kind`` (``fix``, ``merge``,
+``sync`` or ``ci``; absent means ``fix``) and ``base_sha``. The recovery events copy
+both only when present, so a legacy record yields byte-equal events.
+``resolve_crash_window_plan`` runs the unchanged three-way resolution and maps its
+result through ``conflicts.crash_resume_plan``: ``fix``, ``merge`` and absent keep
+today's states, while ``sync`` and ``ci`` re-enter the Wave 8 CI wait and never
+resume into ``S4_PUSHING``, ``S5A_RETRIGGER_REVIEW`` or ``S5_AWAITING_REREVIEW``.
+For a conflict cycle that is still open, Branch A, Branch C and every halt
+directive close it once with ``sync_concluded{recovered: true}``; Branch B leaves
+the close to the SKILL after the re-driven push.
 """
 
 from __future__ import annotations
 
+from .conflicts import ResumePlan, crash_resume_plan, is_conflict_cycle
 from .models import EventType, MonitorState
 from .run_log import RunLog
 
@@ -105,6 +117,8 @@ def resolve_crash_window(
             "target_sha",
             "target_branch",
             "target_remote",
+            "kind",
+            "base_sha",
         )
         if k in dangling
     }
@@ -169,3 +183,49 @@ def resolve_crash_window(
         }
     )
     return BRANCH_C_AMBIGUOUS, MonitorState.HALT_HUMAN
+
+
+def resolve_crash_window_plan(
+    run_log: RunLog,
+    dangling: dict,
+    *,
+    remote_reachable: bool | None,
+    observed_remote_sha: str | None = None,
+) -> ResumePlan:
+    """Kind-aware resume: run the unchanged three-way resolution, then map its
+    result through conflicts.crash_resume_plan (fix/merge/absent keep today's
+    state; sync/ci re-enter the Wave 8 CI wait, never S4/S5a/S5)."""
+    branch, state = resolve_crash_window(
+        run_log,
+        dangling,
+        remote_reachable=remote_reachable,
+        observed_remote_sha=observed_remote_sha,
+    )
+    plan = crash_resume_plan(dangling, branch, state)
+    cycle_id = dangling.get("cycle_id")
+    open_cycle = run_log.rebuild_state()["open_conflict_cycle"]
+    if (
+        is_conflict_cycle(cycle_id)
+        and open_cycle is not None
+        and open_cycle.get("cycle_id") == cycle_id
+    ):
+        if plan.directive == "halt":
+            outcome, reason, merge_sha = "halted", plan.reason, None
+        elif branch == BRANCH_A_LANDED:
+            outcome, reason, merge_sha = "pushed", None, dangling.get("target_sha")
+        else:
+            outcome = None  # Branch B: the SKILL closes the cycle after the re-drive
+        if outcome is not None:
+            run_log.append(
+                {
+                    "event_type": EventType.SYNC_CONCLUDED.value,
+                    "cycle_id": cycle_id,
+                    "outcome": outcome,
+                    "merge_sha": merge_sha,
+                    "record_path": None,
+                    "dropped": [],
+                    "reason": reason,
+                    "recovered": True,
+                }
+            )
+    return plan
diff --git a/tests/pr_submit/test_crash_recovery.py b/tests/pr_submit/test_crash_recovery.py
index 4469804c..858858d0 100644
--- a/tests/pr_submit/test_crash_recovery.py
+++ b/tests/pr_submit/test_crash_recovery.py
@@ -7,9 +7,17 @@ Each FM in the catalog has a recovery semantic; plus T-CRASH-WINDOW-NO-DOUBLE-PU
 
 from __future__ import annotations
 
+import json
+
 import pytest
 
 from superclaude.pr_submit.classifier import classify
+from superclaude.pr_submit.conflicts import (
+    ResumePlan,
+    conflict_action,
+    conflict_resume_plan,
+    prior_conflict_cycles,
+)
 from superclaude.pr_submit.detection import DetectionContract
 from superclaude.pr_submit.fsm import (
     RunConfig,
@@ -24,6 +32,7 @@ from superclaude.pr_submit.recovery import (
     BRANCH_C_AMBIGUOUS,
     detect_crash_window,
     resolve_crash_window,
+    resolve_crash_window_plan,
 )
 from superclaude.pr_submit.run_log import RunLog
 
@@ -398,3 +407,688 @@ def test_crash_window_branch_c_ambiguous(tmp_path):
     assert len(halted) == 1
     assert halted[0]["reason"] == "ambiguous_remote_tip"
     assert halted[0]["observed_remote_sha"] == "zzz999"
+
+
+# ---------------------------------------------------------------------------
+# Issue #305: kind-aware crash recovery (design sections 4.8 and 6.4)
+# ---------------------------------------------------------------------------
+
+SHA_PRE = "a" * 40
+SHA_TGT = "b" * 40
+SHA_BASE = "c" * 40
+SHA_OTHER = "d" * 40
+
+# One dangling-push cycle id per kind. Fix and CI cycles never use a reserved
+# conflict prefix; the sync and merge cycles are conflict cycles.
+_CYCLE = {
+    "fix": "c1",
+    "absent": "c1",
+    "ci": "c-ci-1",
+    "sync": "sync-1",
+    "merge": "conflict-1",
+}
+# Branch label -> (remote_reachable, observed_remote_sha).
+_BRANCH_INPUT = {"A": (True, None), "B": (False, None), "C": (None, SHA_OTHER)}
+_BRANCH_NAME = {
+    "A": BRANCH_A_LANDED,
+    "B": BRANCH_B_NOT_LANDED,
+    "C": BRANCH_C_AMBIGUOUS,
+}
+_PUSH_OR_REVIEW_STATES = {
+    MonitorState.S4_PUSHING,
+    MonitorState.S5A_RETRIGGER_REVIEW,
+    MonitorState.S5_AWAITING_REREVIEW,
+}
+
+
+def _sync_started(
+    cycle_id: str, *, kind: str, hook: str, review_terminal, resumed: bool = False
+) -> dict:
+    """A ``sync_started`` payload as design section 4.7 lists it."""
+    return {
+        "event_type": "sync_started",
+        "run_id": "r",
+        "cycle_id": cycle_id,
+        "tier": 1 if kind == "sync" else 2,
+        "kind": kind,
+        "hook": hook,
+        "base_ref": "origin/master",
+        "base_sha": SHA_BASE,
+        "pre_push_sha": SHA_PRE,
+        "merge_tree_oid": "e" * 40,
+        "conflict_max_tier": 1 if kind == "sync" else 2,
+        "review_terminal": review_terminal,
+        "paths": ["uv.lock"],
+        "resumed": resumed,
+    }
+
+
+def _initiated(
+    cycle_id: str,
+    *,
+    kind: str | None = None,
+    base_sha: str | None = None,
+    review_terminal: str | None = None,
+    expect_checks: bool | None = None,
+) -> dict:
+    """A ``push_initiated`` record in the key order ``build_push_triad`` writes."""
+    record: dict = {"event_type": "push_initiated", "remote_ref": "origin/feat"}
+    if review_terminal is not None:
+        record["review_terminal"] = review_terminal
+    if expect_checks is not None:
+        record["expect_checks"] = expect_checks
+    record.update(
+        {
+            "run_id": "r",
+            "cycle_id": cycle_id,
+            "idempotency_key": f"push:r:{cycle_id}:{SHA_PRE}:feat",
+            "pre_push_sha": SHA_PRE,
+            "target_sha": SHA_TGT,
+            "target_branch": "feat",
+            "target_remote": "origin",
+        }
+    )
+    if kind is not None:
+        record["kind"] = kind
+    if base_sha is not None:
+        record["base_sha"] = base_sha
+    return record
+
+
+def _dangling_for(kind: str) -> tuple[dict | None, dict]:
+    """The ``sync_started`` (or ``None``) and the dangling ``push_initiated`` of a kind."""
+    cycle_id = _CYCLE[kind]
+    if kind == "sync":
+        started = _sync_started(
+            cycle_id, kind="sync", hook="wave8a", review_terminal="clean"
+        )
+        return started, _initiated(
+            cycle_id,
+            kind="sync",
+            base_sha=SHA_BASE,
+            review_terminal="clean",
+            expect_checks=True,
+        )
+    if kind == "merge":
+        started = _sync_started(
+            cycle_id, kind="merge", hook="c_initial", review_terminal=None
+        )
+        return started, _initiated(cycle_id, kind="merge", base_sha=SHA_BASE)
+    if kind == "ci":
+        return None, _initiated(
+            cycle_id, kind="ci", review_terminal="clean", expect_checks=True
+        )
+    if kind == "fix":
+        return None, _initiated(cycle_id, kind="fix")
+    return None, _initiated(cycle_id)  # absent: the legacy record shape
+
+
+def _seed(rl: RunLog, kind: str) -> dict:
+    """Append the kind's cycle start (if any) and its dangling push; return the record."""
+    started, record = _dangling_for(kind)
+    if started is not None:
+        rl.append(started)
+    rl.append(record)
+    dangling = detect_crash_window(rl)
+    assert dangling is not None and dangling["cycle_id"] == _CYCLE[kind]
+    return dangling
+
+
+def _plan(rl: RunLog, dangling: dict, branch: str) -> ResumePlan:
+    reachable, observed = _BRANCH_INPUT[branch]
+    return resolve_crash_window_plan(
+        rl, dangling, remote_reachable=reachable, observed_remote_sha=observed
+    )
+
+
+def _of_type(rl: RunLog, event_type: str) -> list[dict]:
+    return [e for e in rl.read_events() if e["event_type"] == event_type]
+
+
+def _skill_close(
+    rl: RunLog,
+    cycle_id: str,
+    *,
+    outcome: str,
+    reason: str | None = None,
+    merge_sha: str | None = None,
+) -> bool:
+    """The SKILL's guarded close: append only while the cycle is still the open one."""
+    open_cycle = rl.rebuild_state()["open_conflict_cycle"]
+    if open_cycle is None or open_cycle.get("cycle_id") != cycle_id:
+        return False
+    rl.append(
+        {
+            "event_type": "sync_concluded",
+            "cycle_id": cycle_id,
+            "outcome": outcome,
+            "merge_sha": merge_sha,
+            "record_path": None,
+            "dropped": [],
+            "reason": reason,
+            "recovered": True,
+        }
+    )
+    return True
+
+
+def _resume(rl: RunLog, **facts) -> ResumePlan:
+    """``conflict_resume_plan`` on the rebuilt state with no foreign operation."""
+    args = {
+        "foreign_op": None,
+        "merge_head_sha": None,
+        "local_head_sha": SHA_TGT,
+        "local_head_parents": [SHA_PRE, SHA_BASE],
+        "dangling": detect_crash_window(rl),
+    }
+    args.update(facts)
+    return conflict_resume_plan(rl.rebuild_state(), **args)
+
+
+# (kind, branch) -> (directive, state, check_merge_parent, rerun_guard, wave8 fields)
+_EXPECTED_PLAN = {
+    ("fix", "A"): ("fsm", MonitorState.S5A_RETRIGGER_REVIEW, False, False, False),
+    ("fix", "B"): ("fsm", MonitorState.S4_PUSHING, False, False, False),
+    ("absent", "A"): ("fsm", MonitorState.S5A_RETRIGGER_REVIEW, False, False, False),
+    ("absent", "B"): ("fsm", MonitorState.S4_PUSHING, False, False, False),
+    ("merge", "A"): ("fsm", MonitorState.S5A_RETRIGGER_REVIEW, False, False, False),
+    ("merge", "B"): ("fsm", MonitorState.S4_PUSHING, True, False, False),
+    ("sync", "A"): ("wave8_ci_wait", None, False, False, True),
+    ("sync", "B"): ("redrive_then_wave8", None, True, True, True),
+    ("ci", "A"): ("wave8_ci_wait", None, False, False, True),
+    ("ci", "B"): ("redrive_then_wave8", None, False, True, True),
+}
+
+
+@pytest.mark.recovery
+@pytest.mark.parametrize("branch", ["A", "B", "C"])
+@pytest.mark.parametrize("kind", ["fix", "merge", "sync", "ci", "absent"])
+def test_resolve_crash_window_plan_by_kind(tmp_path, kind, branch):
+    """Section 4.8 table 2: the exact ``ResumePlan`` for every kind and branch."""
+    rl = RunLog(305, tmp_path)
+    dangling = _seed(rl, kind)
+
+    plan = _plan(rl, dangling, branch)
+
+    plan_kind = "fix" if kind == "absent" else kind
+    common = {
+        "cycle_id": _CYCLE[kind],
+        "kind": plan_kind,
+        "target_sha": SHA_TGT,
+        "base_sha": SHA_BASE if plan_kind in ("sync", "merge") else None,
+    }
+    if branch == "C":
+        expected = ResumePlan(
+            "halt",
+            state=MonitorState.HALT_HUMAN,
+            reason="ambiguous_remote_tip",
+            **common,
+        )
+    else:
+        directive, state, merge_parent, rerun, wave8 = _EXPECTED_PLAN[(kind, branch)]
+        extra = (
+            {"wait_sha": SHA_TGT, "review_terminal": "clean", "expect_checks": True}
+            if wave8
+            else {}
+        )
+        expected = ResumePlan(
+            directive,
+            state=state,
+            check_merge_parent=merge_parent,
+            rerun_guard=rerun,
+            **common,
+            **extra,
+        )
+    assert plan == expected
+    # INV-001: sync and ci never resume into a push or review state.
+    if plan_kind in ("sync", "ci"):
+        assert plan.state not in _PUSH_OR_REVIEW_STATES
+    # Only an open conflict cycle settled by Branch A or C gets a sync_concluded.
+    closes = plan_kind in ("sync", "merge") and branch in ("A", "C")
+    assert len(_of_type(rl, "sync_concluded")) == (1 if closes else 0)
+
+
+@pytest.mark.recovery
+@pytest.mark.parametrize(
+    ("kind", "count_key"), [("sync", "sync_push_count"), ("merge", "push_count")]
+)
+def test_recovered_push_completed_copies_kind_and_base_sha(tmp_path, kind, count_key):
+    """Branch A's recovered ``push_completed`` carries ``kind`` and ``base_sha``.
+
+    So the fold counts a recovered sync push in ``sync_push_count`` and a merge
+    push in ``push_count``.
+    """
+    rl = RunLog(305, tmp_path)
+    dangling = _seed(rl, kind)
+    _plan(rl, dangling, "A")
+
+    [completed] = _of_type(rl, "push_completed")
+    assert completed["recovered"] is True
+    assert completed["kind"] == kind
+    assert completed["base_sha"] == SHA_BASE
+    state = rl.rebuild_state()
+    assert state[count_key] == 1
+    other = "push_count" if count_key == "sync_push_count" else "sync_push_count"
+    assert state[other] == 0
+
+
+# The exact pre-#305 recovery record for a kind-less dangling push, in key order.
+_LEGACY_IDENTITY = {
+    "run_id": "r",
+    "cycle_id": "c1",
+    "idempotency_key": f"push:r:c1:{SHA_PRE}:feat",
+    "pre_push_sha": SHA_PRE,
+    "target_sha": SHA_TGT,
+    "target_branch": "feat",
+    "target_remote": "origin",
+}
+_LEGACY_HEAD = {
+    "A": {"event_type": "push_completed", "recovered": True},
+    "B": {"event_type": "push_aborted_or_not_landed", "recovered": True},
+    "C": {
+        "event_type": "terminal_halted",
+        "recovered": True,
+        "reason": "ambiguous_remote_tip",
+        "observed_remote_sha": SHA_OTHER,
+    },
+}
+_LEGACY_STATE = {
+    "A": MonitorState.S5A_RETRIGGER_REVIEW,
+    "B": MonitorState.S4_PUSHING,
+    "C": MonitorState.HALT_HUMAN,
+}
+
+
+@pytest.mark.recovery
+@pytest.mark.parametrize("branch", ["A", "B", "C"])
+def test_legacy_record_recovery_events_unchanged(tmp_path, branch):
+    """NFR-12: a kind-less record yields byte-equal recovery events and today's state."""
+    rl = RunLog(305, tmp_path)
+    dangling = _seed(rl, "absent")
+
+    plan = _plan(rl, dangling, branch)
+
+    assert plan.state == _LEGACY_STATE[branch]
+    lines = rl.jsonl_path.read_text(encoding="utf-8").splitlines()
+    assert len(lines) == 2  # the dangling push and its one recovery event
+    expected = {
+        "schema_version": "1.0",
+        "event_id": 2,
+        **_LEGACY_HEAD[branch],
+        **_LEGACY_IDENTITY,
+        "timestamp": None,
+    }
+    assert lines[1] == json.dumps(expected)
+
+
+@pytest.mark.recovery
+@pytest.mark.parametrize("branch", ["A", "B", "C"])
+@pytest.mark.parametrize("kind", ["fix", "absent"])
+def test_fix_and_absent_wrapper_matches_resolve_crash_window(tmp_path, kind, branch):
+    """For kinds ``fix`` and absent the wrapper adds nothing to ``resolve_crash_window``.
+
+    Two identical logs: one settled by the wrapper, one by ``resolve_crash_window``.
+    The JSONL bytes are equal and the plan's state is the returned state.
+    """
+    rl_plan = RunLog(305, tmp_path / "plan")
+    rl_today = RunLog(305, tmp_path / "today")
+    dangling_plan = _seed(rl_plan, kind)
+    dangling_today = _seed(rl_today, kind)
+    reachable, observed = _BRANCH_INPUT[branch]
+
+    plan = resolve_crash_window_plan(
+        rl_plan,
+        dangling_plan,
+        remote_reachable=reachable,
+        observed_remote_sha=observed,
+    )
+    branch_today, state_today = resolve_crash_window(
+        rl_today,
+        dangling_today,
+        remote_reachable=reachable,
+        observed_remote_sha=observed,
+    )
+
+    assert branch_today == _BRANCH_NAME[branch]
+    assert plan.state == state_today
+    assert rl_plan.jsonl_path.read_bytes() == rl_today.jsonl_path.read_bytes()
+    assert rl_plan.rebuild_state() == rl_today.rebuild_state()
+
+
+@pytest.mark.recovery
+def test_rejected_push_record_is_not_a_crash_window(tmp_path):
+    """A rejected push is finalized: no crash window, and resume halts ``push_rejected``."""
+    rl = RunLog(305, tmp_path)
+    started, record = _dangling_for("sync")
+    rl.append(started)
+    rl.append(record)
+    rl.append(
+        {
+            "event_type": "push_aborted_or_not_landed",
+            "idempotency_key": record["idempotency_key"],
+            "cycle_id": "sync-1",
+            "rejected": True,
+            "stderr_tail": "rejected: non-fast-forward",
+        }
+    )
+
+    assert detect_crash_window(rl) is None
+    plan = _resume(rl, dangling=None)
+    assert plan == ResumePlan("halt", reason="push_rejected", cycle_id="sync-1")
+
+
+@pytest.mark.recovery
+@pytest.mark.parametrize("case", ["A", "C", "halt"])
+@pytest.mark.parametrize("kind", ["sync", "merge"])
+def test_conflict_crash_recovery_closes_the_cycle(tmp_path, kind, case):
+    """B2: Branch A, Branch C and a halt directive close the open cycle exactly once.
+
+    The halt directive comes from an unusable record: a sync record without
+    ``review_terminal`` (settled through Branch B), or a merge cycle whose record
+    carries an unknown kind (settled through Branch A).
+    """
+    rl = RunLog(305, tmp_path)
+    started, record = _dangling_for(kind)
+    if case == "halt":
+        if kind == "sync":
+            del record["review_terminal"]
+        else:
+            record["kind"] = "merg"
+    rl.append(started)
+    rl.append(record)
+    dangling = detect_crash_window(rl)
+    assert dangling is not None
+    branch = {"A": "A", "C": "C", "halt": "B" if kind == "sync" else "A"}[case]
+
+    plan = _plan(rl, dangling, branch)
+
+    outcome, reason, merge_sha = {
+        "A": ("pushed", None, SHA_TGT),
+        "C": ("halted", "ambiguous_remote_tip", None),
+        "halt": ("halted", "resume_unrepresentable", None),
+    }[case]
+    if case == "halt":
+        assert plan.directive == "halt" and plan.reason == "resume_unrepresentable"
+    concluded = _of_type(rl, "sync_concluded")
+    assert len(concluded) == 1
+    body = {k: v for k, v in concluded[0].items() if k not in ("event_id",)}
+    assert body == {
+        "schema_version": "1.0",
+        "event_type": "sync_concluded",
+        "cycle_id": _CYCLE[kind],
+        "outcome": outcome,
+        "merge_sha": merge_sha,
+        "record_path": None,
+        "dropped": [],
+        "reason": reason,
+        "recovered": True,
+        "timestamp": None,
+    }
+    assert rl.rebuild_state()["open_conflict_cycle"] is None
+    if case == "C":
+        # Today's Branch C record does not finalize the key, so a later resume
+        # can reach the wrapper again; the closed cycle is not closed twice.
+        assert detect_crash_window(rl) is not None
+    else:
+        # The settled key is finalized, so a later resume never reaches the wrapper.
+        assert detect_crash_window(rl) is None
+    # A second wrapper call appends no second sync_concluded (the cycle is closed).
+    _plan(rl, dangling, branch)
+    assert len(_of_type(rl, "sync_concluded")) == 1
+
+
+@pytest.mark.recovery
+@pytest.mark.parametrize("branch", ["A", "B", "C"])
+@pytest.mark.parametrize("kind", ["fix", "ci", "absent"])
+def test_non_conflict_kinds_append_no_sync_concluded(tmp_path, kind, branch):
+    """Kinds ``fix``, ``ci`` and absent have no conflict cycle and close nothing."""
+    rl = RunLog(305, tmp_path)
+    dangling = _seed(rl, kind)
+    _plan(rl, dangling, branch)
+    assert _of_type(rl, "sync_concluded") == []
+    assert rl.rebuild_state()["conflict_cycles"] == []
+
+
+@pytest.mark.recovery
+def test_conflict_crash_then_later_fix_crash_resumes_into_fix_window(tmp_path):
+    """B2: after a recovered sync crash, a later fix crash reaches the fix window."""
+    rl = RunLog(305, tmp_path)
+    dangling = _seed(rl, "sync")
+    _plan(rl, dangling, "A")
+    assert rl.rebuild_state()["open_conflict_cycle"] is None
+
+    fix_record = _initiated("c2")
+    rl.append(fix_record)
+
+    assert _resume(rl) == ResumePlan("none")
+    fix_dangling = detect_crash_window(rl)
+    assert fix_dangling is not None
+    assert fix_dangling["idempotency_key"] == fix_record["idempotency_key"]
+    plan = resolve_crash_window_plan(rl, fix_dangling, remote_reachable=True)
+    assert plan.directive == "fsm"
+    assert plan.state == MonitorState.S5A_RETRIGGER_REVIEW
+    assert len(_of_type(rl, "sync_concluded")) == 1  # only the sync cycle's
+    state = rl.rebuild_state()
+    assert state["sync_push_count"] == 1 and state["push_count"] == 1
+
+
+@pytest.mark.recovery
+def test_restart_row_uses_recorded_review_terminal(tmp_path):
+    """B3, m3: a row 7 restart re-enters with the recorded ``review_terminal``.
+
+    The router then sees ``prior_conflict_cycles == 0`` (the reused id is
+    excluded) and resolves the sync at L3; counting the reused id would hit
+    ``sync_cap``.
+    """
+    rl = RunLog(305, tmp_path)
+    rl.append(
+        _sync_started(
+            "sync-1", kind="sync", hook="wave8a", review_terminal="halt_max_rounds"
+        )
+    )
+    state = rl.rebuild_state()
+    assert state["conflict_cycles"] == ["sync-1"]
+
+    plan = _resume(rl, local_head_sha=SHA_PRE, local_head_parents=[SHA_BASE])
+
+    assert plan.directive == "restart"
+    assert plan.cycle_id == "sync-1"
+    assert plan.hook == "wave8a"
+    assert plan.review_terminal == "halt_max_rounds"
+    assert _skill_close(rl, "sync-1", outcome="aborted") is True
+    rl.append(
+        _sync_started(
+            "sync-1",
+            kind="sync",
+            hook="wave8a",
+            review_terminal=plan.review_terminal,
+            resumed=True,
+        )
+    )
+    state = rl.rebuild_state()
+    assert state["conflict_cycles"] == ["sync-1"]  # the restart counts once
+    assert state["open_conflict_cycle"]["review_terminal"] == "halt_max_rounds"
+
+    prior = prior_conflict_cycles(state["conflict_cycles"], plan.cycle_id)
+    assert prior == 0
+    route = {
+        "hook": plan.hook,
+        "plan_tier": 1,
+        "ordinal": 3,
+        "entering": plan.review_terminal,
+        "conflict_max_tier": 1,
+        "round_counter": 0,
+        "max_rounds": 3,
+        "github_conflicting": True,
+    }
+    action = conflict_action(prior_conflict_cycles=prior, **route)
+    assert (action.action, action.reason) == ("resolve_push", "tier1_sync")
+    not_excluded = conflict_action(
+        prior_conflict_cycles=len(state["conflict_cycles"]), **route
+    )
+    assert not_excluded.reason == "sync_cap"
+
+
+def _branch_b_then_redrive(rl: RunLog) -> dict:
+    """A sync crash settled by Branch B, then the re-drive's ``push_initiated``."""
+    dangling = _seed(rl, "sync")
+    plan = _plan(rl, dangling, "B")
+    assert plan.directive == "redrive_then_wave8"
+    assert _of_type(rl, "sync_concluded") == []  # Branch B: the SKILL closes later
+    _, redrive = _dangling_for("sync")  # same cycle, same key, same target
+    rl.append(redrive)
+    return redrive
+
+
+def _assert_4b_prime_halts_and_closes_once(rl: RunLog) -> None:
+    assert detect_crash_window(rl) is None  # the reused key is already finalized
+    plan = _resume(rl, dangling=None)
+    assert plan == ResumePlan(
+        "halt",
+        reason="resume_unrepresentable",
+        cycle_id="sync-1",
+        target_sha=SHA_TGT,
+    )
+    assert _skill_close(rl, "sync-1", outcome="halted", reason=plan.reason) is True
+    [concluded] = _of_type(rl, "sync_concluded")
+    assert concluded["outcome"] == "halted" and concluded["recovered"] is True
+    assert rl.rebuild_state()["open_conflict_cycle"] is None
+    # A third resume: no open cycle, row 2, and nothing more is appended.
+    assert _resume(rl) == ResumePlan("none")
+    assert _skill_close(rl, "sync-1", outcome="halted", reason=plan.reason) is False
+    assert len(_of_type(rl, "sync_concluded")) == 1
+
+
+@pytest.mark.recovery
+def test_branch_b_crash_during_redrive_halts_and_closes_once(tmp_path):
+    """N1: a crash during the Branch B re-drive reaches row 4b' and closes once."""
+    rl = RunLog(305, tmp_path)
+    _branch_b_then_redrive(rl)
+    # Crash before the re-drive's push_completed.
+    _assert_4b_prime_halts_and_closes_once(rl)
+
+
+@pytest.mark.recovery
+def test_branch_b_redrive_push_failed_then_resume_halts_and_closes_once(tmp_path):
+    """N1: a re-drive ending ``push_failed`` (no record) halts at row 4b' and closes once.
+
+    No directive along the way plans another push.
+    """
+    rl = RunLog(305, tmp_path)
+    _branch_b_then_redrive(rl)
+    rl.append({"event_type": "terminal_halted", "reason": "push_failed"})
+    plans = [_resume(rl, dangling=None)]
+    _assert_4b_prime_halts_and_closes_once(rl)
+    plans.append(_resume(rl))
+    for plan in plans:
+        assert plan.directive in ("halt", "none")
+        assert plan.state != MonitorState.S4_PUSHING
+
+
+@pytest.mark.recovery
+def test_resume_row_1_closes_an_open_cycle(tmp_path):
+    """m2: ``push_rejected`` with a cycle still open closes it once as ``halted``."""
+    rl = RunLog(305, tmp_path)
+    started, record = _dangling_for("sync")
+    rl.append(started)
+    rl.append(record)
+    rl.append(
+        {
+            "event_type": "push_aborted_or_not_landed",
+            "idempotency_key": record["idempotency_key"],
+            "cycle_id": "sync-1",
+            "rejected": True,
+            "stderr_tail": "rejected",
+        }
+    )
+
+    plan = _resume(rl)
+    assert plan.directive == "halt" and plan.reason == "push_rejected"
+    assert plan.cycle_id == "sync-1"
+    assert _skill_close(rl, plan.cycle_id, outcome="halted", reason=plan.reason)
+    [concluded] = _of_type(rl, "sync_concluded")
+    assert (concluded["outcome"], concluded["reason"]) == ("halted", "push_rejected")
+    assert rl.rebuild_state()["open_conflict_cycle"] is None
+    again = _resume(rl)
+    assert again == ResumePlan("halt", reason="push_rejected")  # no cycle to close
+    assert _skill_close(rl, "sync-1", outcome="halted", reason="x") is False
+    assert len(_of_type(rl, "sync_concluded")) == 1
+
+
+@pytest.mark.recovery
+def test_resume_row_4_expect_checks_defaults_true(tmp_path):
+    """m6: row 4 with no ``expect_checks`` on the push record reads it as ``True``."""
+    rl = RunLog(305, tmp_path)
+    rl.append(
+        _sync_started("sync-1", kind="sync", hook="wave8a", review_terminal="clean")
+    )
+    record = _initiated(
+        "sync-1", kind="sync", base_sha=SHA_BASE, review_terminal="clean"
+    )
+    assert "expect_checks" not in record
+    rl.append(record)
+    rl.append(
+        {
+            "event_type": "push_completed",
+            **{k: record[k] for k in _LEGACY_IDENTITY},
+            "cycle_id": "sync-1",
+            "idempotency_key": record["idempotency_key"],
+            "kind": "sync",
+            "base_sha": SHA_BASE,
+        }
+    )
+
+    plan = _resume(rl)
+    assert plan.directive == "complete_after_push"
+    assert plan.expect_checks is True
+    assert plan.wait_sha == SHA_TGT
+    assert plan.state is None  # sync never resumes into S5a or S5
+
+
+@pytest.mark.recovery
+def test_branch_b_redrive_landed_closes_cycle_once(tmp_path):
+    """n4: a landed Branch B re-drive is closed once by the SKILL's guarded close."""
+    rl = RunLog(305, tmp_path)
+    redrive = _branch_b_then_redrive(rl)
+    rl.append(
+        {
+            "event_type": "push_completed",
+            **{k: redrive[k] for k in _LEGACY_IDENTITY},
+            "cycle_id": "sync-1",
+            "idempotency_key": redrive["idempotency_key"],
+            "kind": "sync",
+            "base_sha": SHA_BASE,
+        }
+    )
+    assert _skill_close(rl, "sync-1", outcome="pushed", merge_sha=SHA_TGT) is True
+    [concluded] = _of_type(rl, "sync_concluded")
+    assert concluded["outcome"] == "pushed" and concluded["recovered"] is True
+    assert concluded["merge_sha"] == SHA_TGT
+    assert rl.rebuild_state()["open_conflict_cycle"] is None
+
+    # A later fix-cycle crash window resumes into the fix window through row 2.
+    fix_record = _initiated("c2")
+    rl.append(fix_record)
+    assert _resume(rl) == ResumePlan("none")
+    fix_dangling = detect_crash_window(rl)
+    assert fix_dangling is not None
+    assert fix_dangling["idempotency_key"] == fix_record["idempotency_key"]
+    # A second close attempt for the closed cycle appends nothing.
+    assert _skill_close(rl, "sync-1", outcome="pushed", merge_sha=SHA_TGT) is False
+    assert len(_of_type(rl, "sync_concluded")) == 1
+
+
+@pytest.mark.recovery
+def test_branch_c_event_order(tmp_path):
+    """m5: Branch C writes ``terminal_halted`` and then ``sync_concluded``, each once."""
+    rl = RunLog(305, tmp_path)
+    dangling = _seed(rl, "sync")
+    before = len(rl.read_events())
+
+    _plan(rl, dangling, "C")
+
+    added = rl.read_events()[before:]
+    assert [e["event_type"] for e in added] == ["terminal_halted", "sync_concluded"]
+    assert added[0]["reason"] == "ambiguous_remote_tip"
+    assert added[1]["outcome"] == "halted"
+    assert added[1]["reason"] == "ambiguous_remote_tip"
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t8-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t8-tests.log
new file mode 100644
index 00000000..c0ea4235
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t8-tests.log
@@ -0,0 +1,16 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 133 items
+
+tests/pr_submit/test_crash_recovery.py ................................. [ 24%]
+.................................                                        [ 49%]
+tests/pr_submit/test_augment_review_remediation.py .......               [ 54%]
+tests/pr_submit/test_codex_reviews.py .................................. [ 80%]
+..........................                                               [100%]
+
+============================= 133 passed in 0.94s ==============================

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
