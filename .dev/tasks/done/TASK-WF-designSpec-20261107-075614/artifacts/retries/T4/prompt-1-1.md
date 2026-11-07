5964432d497cff3032b17f322a817022f4b705ad
Review one task for spec compliance.

Task brief: ## Task 4: Add the toggle classifier and the three decision functions

Depends on: Task 3

In `src/superclaude/pr_submit/merge_guard.py` add `classify_toggles(guard, read)` (the exact rule of ./source.md section 4.1: `unreadable` for a failed, incomplete or short timeline, `foreign` when observed transitions exceed `run_toggles + unsettled + failed_mutations` or the live draft flag contradicts a `HELD` or `RELEASED` phase, `ok` otherwise), `engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows, first match wins, `notes` carries `auto_merge_armed`), `release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)` (all 9 rows; `applied_edits` is the count of edits applied in THIS cycle, not the run-wide output field) and `resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)` (all 9 rows, with the row 2 precedence, the three `RECONCILE` reasons `resume_reconciled`, `not_applied`, `ambiguous` of section 4.1, and `dangling_branch` limited to `None` or the `BRANCH_*` constants of Task 3). Extend `tests/pr_submit/test_merge_guard.py` with one parametrized case per table row, the ready-then-draft round trip, and a failed-on-client-but-landed mutation that must not classify as foreign.

Acceptance criteria:
- T4.AC1: Each row of the three decision tables has a test that names the row number and asserts the returned `action`, `reason` and `cause`; the engage test at ordinal 2, with `mode=OFF`, and with cycle id `sync-1` and `conflict-1` all return `NOOP`.
- T4.AC2: `classify_toggles` returns `unreadable` for `complete=False`, `transitions=None` and for observed below `run_toggles`, `foreign` for one extra transition and for a `HELD` phase with a ready PR, and `ok` when observed equals `run_toggles + failed_mutations`.
- T4.AC3: `release_decision` called with `applied_edits=0` for a new cycle while the guard record already holds an earlier fixing cycle returns `RELEASE` with cause `no_edits`; it returns `HOLD` for a head different from `target_sha`, and `HALT_PR_NOT_OPEN` for a merged state; a guard in phase `DISABLED` (originally draft) never yields `RELEASE` or `ENGAGE`.
- T4.AC4: `resume_decision` tests prove the precedence: ordinal 2 with phase `ENGAGE_PENDING` and a non-empty `pending` returns `REPORT_HELD` (row 2 wins over row 3); mode `OFF` at ordinal 3 with phase `HELD` returns `REPORT_HELD`; phases `RELEASED` and `DISABLED` skip row 2; ordinal 3 with `pending` non-empty returns `RECONCILE` with a distinct test for each of `resume_reconciled` (live state matches the request and observed equals `run_toggles + 1`), `not_applied` (live state does not match) and `ambiguous` (anything else, which holds).
- T4.AC5: `resume_decision` row 4 is tested for both entries: phase `HELD` with `dangling_branch == "landed"` and phase `HELD` with `dangling_branch is None` and `published=True` each re-enter `release_decision` with `push_completed=True`; phase `HELD` with `dangling_branch is None` and `published=False` returns `NOOP` (row 9); `"not_landed"` returns `NOOP(held_through_redrive)`; `"ambiguous"` returns `HOLD(ambiguous_remote_tip)`; a test passes the real `BRANCH_A_LANDED` string of `recovery.py` and gets the row 4 result.
- T4.AC6: `uv run pytest tests/pr_submit/test_merge_guard.py -q` passes with ruff clean.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: 5964432d497cff3032b17f322a817022f4b705ad
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/merge_guard.py b/src/superclaude/pr_submit/merge_guard.py
index b2c5e291..bd87f489 100644
--- a/src/superclaude/pr_submit/merge_guard.py
+++ b/src/superclaude/pr_submit/merge_guard.py
@@ -9,8 +9,9 @@ This module only DECIDES. It does no I/O: the protocol (``SKILL.md`` and
 calls these functions, appends the run-log events and performs the mutation.
 That is the same split as the push triad and the re-trigger (NFR-6).
 
-Core-purity (NFR-6 / AC-9): this module imports only the standard library and
-contains no version-control or hosting command word on any line.
+Core-purity (NFR-6 / AC-9): this module imports only ``enum``, ``dataclasses``,
+``re`` and ``is_conflict_cycle`` from ``.conflicts``, and contains no
+version-control or hosting command word on any line.
 
 Guard state is the plain dict returned by :func:`fold_draft_guard` (or ``None``
 when the run log holds no guard record); decisions read it with ``.get`` so a
@@ -23,6 +24,8 @@ import re
 from dataclasses import dataclass
 from enum import Enum
 
+from .conflicts import is_conflict_cycle
+
 # Event names of the two guard events (the members of ``EventType`` carry the
 # same values; a test pins the equality because this module cannot import them).
 REQUESTED = "draft_guard_requested"
@@ -341,3 +344,235 @@ def guard_status(guard: dict | None, mode: object, ordinal: object) -> str:
     if phase == Phase.RELEASED.value:
         return "released"
     return "unavailable"
+
+
+# ---------------------------------------------------------------------------
+# Toggle classification
+# ---------------------------------------------------------------------------
+
+
+def classify_toggles(guard: dict | None, read: GuardRead) -> str:
+    """``"ok"``, ``"foreign"`` or ``"unreadable"``: the only foreign-toggle test.
+
+    No actor identity is used (one login serves the human and the agent): the
+    count of draft/ready transitions on the timeline is compared with the count
+    the guard itself made, with slack for calls that failed or were never settled.
+    """
+    if (
+        not read.ok
+        or not read.complete
+        or read.transitions is None
+        or read.is_draft is None
+        or not guard
+        or not _is_int(guard.get("baseline"))
+    ):
+        return "unreadable"
+    observed = read.transitions - guard["baseline"]
+    run_toggles = guard.get("run_toggles", 0)
+    slack = guard.get("unsettled", 0) + guard.get("failed_mutations", 0)
+    if observed < run_toggles:
+        return "unreadable"  # events are missing from the timeline
+    if observed > run_toggles + slack:
+        return "foreign"
+    expected = {Phase.HELD.value: True, Phase.RELEASED.value: False}.get(_phase(guard))
+    if expected is not None and read.is_draft != expected:
+        return "foreign"
+    return "ok"
+
+
+# ---------------------------------------------------------------------------
+# Decisions
+# ---------------------------------------------------------------------------
+
+
+def _inert(mode: object, ordinal: object, cycle_id: object) -> str | None:
+    if mode == GuardMode.OFF:
+        return "mode_off"
+    if not (_is_int(ordinal) and ordinal >= _MIN_ORDINAL):
+        return "ordinal"
+    if is_conflict_cycle(cycle_id):
+        return "conflict_cycle"
+    return None
+
+
+def engage_decision(
+    *,
+    mode: object,
+    ordinal: object,
+    cycle_id: object,
+    guard: dict | None,
+    read: GuardRead,
+) -> GuardDecision:
+    """Decide whether to make the PR a draft: first matching row wins."""
+    inert = _inert(mode, ordinal, cycle_id)
+    if inert:  # row 1
+        return GuardDecision(GuardAction.NOOP, inert)
+    phase = _phase(guard)
+    if phase == Phase.DISABLED.value:  # row 2
+        return GuardDecision(GuardAction.NOOP, "disabled")
+    if not read.ok:  # row 3
+        return GuardDecision(GuardAction.HALT_UNAVAILABLE, "read_failed")
+    if read.state != "OPEN":  # row 4
+        return GuardDecision(GuardAction.HALT_PR_NOT_OPEN, "pr_not_open")
+    if phase == Phase.RELEASE_PENDING.value:
+        if guard.get("owned_draft"):  # row 5
+            return GuardDecision(GuardAction.RETRY_RELEASE, "release_pending")
+        return GuardDecision(GuardAction.HOLD, "ownership_unproven")  # row 6
+    if phase == Phase.HELD.value:  # row 7
+        return GuardDecision(GuardAction.NOOP, "already_held")
+    if not read.complete or read.transitions is None:  # row 8
+        return GuardDecision(GuardAction.HALT_UNAVAILABLE, "timeline_unreadable")
+    if guard and classify_toggles(guard, read) == "foreign":  # row 9
+        return GuardDecision(
+            GuardAction.SKIP_USER_OVERRIDE, "user_override", cause="user_override"
+        )
+    if guard is None and read.is_draft:  # row 10
+        return GuardDecision(
+            GuardAction.SKIP_ALREADY_DRAFT, "already_draft", cause="already_draft"
+        )
+    notes = ("auto_merge_armed",) if read.auto_merge_armed else ()  # row 11
+    return GuardDecision(GuardAction.ENGAGE, "engage", notes=notes)
+
+
+def release_decision(
+    *,
+    mode: object,
+    ordinal: object,
+    cycle_id: object,
+    guard: dict | None,
+    read: GuardRead,
+    applied_edits: int,
+    target_sha: str | None,
+    push_completed: bool,
+) -> GuardDecision:
+    """Decide whether to mark the PR ready again: first matching row wins.
+
+    ``applied_edits`` is THIS cycle's count of applied edits, not the run-wide
+    output field, so a zero-edit cycle after a fixing cycle still releases with
+    cause ``no_edits``.
+    """
+    inert = _inert(mode, ordinal, cycle_id)
+    if inert:  # row 1
+        return GuardDecision(GuardAction.NOOP, inert)
+    phase = _phase(guard)
+    if phase not in (Phase.HELD.value, Phase.RELEASE_PENDING.value):  # row 2
+        return GuardDecision(GuardAction.NOOP, "not_held")
+    if not read.ok:  # row 3
+        return GuardDecision(GuardAction.HOLD, "read_failed")
+    if read.state != "OPEN":  # row 4
+        return GuardDecision(GuardAction.HALT_PR_NOT_OPEN, "pr_not_open")
+    verdict = classify_toggles(guard, read)
+    if verdict == "unreadable":  # row 5
+        return GuardDecision(GuardAction.HOLD, "timeline_unreadable")
+    if verdict == "foreign":  # row 6
+        return GuardDecision(
+            GuardAction.SKIP_USER_OVERRIDE, "user_override", cause="user_override"
+        )
+    if applied_edits == 0:  # row 7
+        return GuardDecision(GuardAction.RELEASE, "no_edits", cause="no_edits")
+    if push_completed and target_sha is not None and read.head_sha == target_sha:
+        return GuardDecision(GuardAction.RELEASE, "pushed", cause="pushed")  # row 8
+    reason = "head_mismatch" if push_completed else "push_not_completed"
+    return GuardDecision(GuardAction.HOLD, reason)  # row 9
+
+
+def _reconcile(guard: dict, read: GuardRead | None, pending: list) -> GuardDecision:
+    """Resume row 3: settle the last unsettled request from the live state."""
+    request = pending[-1]
+    if (
+        read is None
+        or classify_toggles(guard, read) in ("unreadable", "foreign")
+        or read.transitions is None
+    ):
+        return GuardDecision(GuardAction.RECONCILE, "ambiguous")
+    observed = read.transitions - guard["baseline"]
+    run_toggles = guard.get("run_toggles", 0)
+    wants_draft = request.get("to") == Direction.DRAFT.value
+    matches = read.is_draft is wants_draft
+    if matches and observed == run_toggles + 1:
+        return GuardDecision(
+            GuardAction.RECONCILE, "resume_reconciled", cause="resume_reconciled"
+        )
+    if not matches and observed == run_toggles:
+        return GuardDecision(GuardAction.RECONCILE, "not_applied", cause="not_applied")
+    return GuardDecision(GuardAction.RECONCILE, "ambiguous")
+
+
+def resume_decision(
+    *,
+    mode: object,
+    ordinal: object,
+    guard: dict | None,
+    read: GuardRead | None,
+    pending: list,
+    dangling_branch: str | None,
+    published: bool,
+    applied_edits: int = 1,
+    target_sha: str | None = None,
+    cycle_id: object = None,
+) -> GuardDecision:
+    """Decide what ``--resume`` does about the guard: first matching row wins.
+
+    ``dangling_branch`` is ``None`` or a ``BRANCH_*`` constant; ``published`` is
+    :func:`held_cycle_published` (a push that completed normally before the
+    crash leaves no dangling window). Row 4 re-enters :func:`release_decision`
+    with ``push_completed=True``; the held cycle has pushed, so at least one edit
+    counts, and with no ``target_sha`` the head proof cannot succeed and the
+    guard holds.
+    """
+    if not guard:  # row 1
+        return GuardDecision(GuardAction.NOOP, "no_guard")
+    phase = _phase(guard)
+    settled_phases = (Phase.RELEASED.value, Phase.DISABLED.value)
+    if (not _is_int(ordinal) or ordinal < _MIN_ORDINAL or mode == GuardMode.OFF) and (
+        phase not in settled_phases
+    ):  # row 2
+        return GuardDecision(GuardAction.REPORT_HELD, "held_report")
+    if pending:  # row 3
+        return _reconcile(guard, read, pending)
+    if phase == Phase.HELD.value and (dangling_branch == BRANCH_LANDED or published):
+        if read is None:  # row 4
+            return GuardDecision(GuardAction.HOLD, "read_failed")
+        return release_decision(
+            mode=mode,
+            ordinal=ordinal,
+            cycle_id=cycle_id if cycle_id is not None else guard.get("cycle_id"),
+            guard=guard,
+            read=read,
+            applied_edits=max(1, applied_edits),
+            target_sha=target_sha,
+            push_completed=True,
+        )
+    if dangling_branch == BRANCH_NOT_LANDED and phase == Phase.HELD.value:  # row 5
+        return GuardDecision(GuardAction.NOOP, "held_through_redrive")
+    if dangling_branch == BRANCH_AMBIGUOUS:  # row 6
+        return GuardDecision(GuardAction.HOLD, "ambiguous_remote_tip")
+    if phase == Phase.RELEASE_PENDING.value:
+        if guard.get("owned_draft"):  # row 7
+            return GuardDecision(GuardAction.RETRY_RELEASE, "release_pending")
+        if read is not None and read.is_draft:  # row 8
+            return GuardDecision(GuardAction.HOLD, "ownership_unproven")
+    return GuardDecision(GuardAction.NOOP, "nothing_to_do")  # row 9
+
+
+__all__ = [
+    "BRANCH_AMBIGUOUS",
+    "BRANCH_LANDED",
+    "BRANCH_NOT_LANDED",
+    "Direction",
+    "GuardAction",
+    "GuardDecision",
+    "GuardMode",
+    "GuardRead",
+    "Phase",
+    "classify_toggles",
+    "engage_decision",
+    "fix_cycle_id",
+    "fold_draft_guard",
+    "guard_status",
+    "held_cycle_published",
+    "next_cycle_number",
+    "pending_requests",
+    "release_decision",
+    "resume_decision",
+]

diff --git a/tests/pr_submit/test_merge_guard.py b/tests/pr_submit/test_merge_guard.py
index 79898493..404c3569 100644
--- a/tests/pr_submit/test_merge_guard.py
+++ b/tests/pr_submit/test_merge_guard.py
@@ -225,9 +225,74 @@ FOLD_CASES = {
             "unsettled": 0,
             "owned_draft": True,
             "run_toggles": 1,
+            "failed_mutations": 0,
+            "disabled_cause": None,
+        },
+    ),
+    # A ready-direction not_applied returns to the phase before the request, so
+    # after a failed release it is RELEASE_PENDING again, and it leaves the failure
+    # count and ownership alone whether or not the draft was owned.
+    "ready_not_applied_after_failed_release": (
+        ENGAGED
+        + [
+            req("ready"),
+            settled("ready", "failed"),
+            req("ready", attempt=2),
+            settled("ready", "skipped", cause="not_applied", attempt=2),
+        ],
+        {
+            "phase": "release_pending",
+            "unsettled": 0,
+            "failed_mutations": 1,
+            "owned_draft": True,
+            "run_toggles": 1,
+            "disabled_cause": None,
+        },
+    ),
+    "ready_not_applied_after_failed_engage": (
+        [
+            req("draft", baseline=1, original=False),
+            settled("draft", "failed"),
+            req("ready"),
+            settled("ready", "skipped", cause="not_applied"),
+        ],
+        {
+            "phase": "release_pending",
+            "unsettled": 0,
+            "failed_mutations": 1,
+            "owned_draft": False,
+            "run_toggles": 0,
             "disabled_cause": None,
         },
     ),
+    # A failed draft call leaves ownership as it was: still owned after an earlier
+    # confirmed engage.
+    "draft_failed_keeps_ownership": (
+        ENGAGED
+        + [req("draft", cycle="fix-2"), settled("draft", "failed", cycle="fix-2")],
+        {
+            "phase": "release_pending",
+            "unsettled": 0,
+            "failed_mutations": 1,
+            "owned_draft": True,
+            "run_toggles": 1,
+        },
+    ),
+    # original_is_draft comes only from the first guard record, never from a later
+    # skip settle either.
+    "later_skip_does_not_overwrite_original_is_draft": (
+        ENGAGED
+        + [
+            settled(
+                "ready",
+                "skipped",
+                cause="user_override",
+                with_key=False,
+                original=True,
+            )
+        ],
+        {"phase": "disabled", "original_is_draft": False, "owned_draft": False},
+    ),
     "draft_not_applied_after_failed_engage_returns_to_release_pending": (
         [
             req("draft", baseline=1, original=False),
@@ -433,6 +498,18 @@ def test_pending_requests_pairs_by_idempotency_key():
     assert mg.pending_requests([]) == []
 
 
+def test_pending_requests_tell_retries_apart_by_the_attempt_suffix():
+    """Settling the a2 retry leaves the unsettled a1 request pending."""
+    events = [
+        req("draft", baseline=1, original=False),
+        req("draft", attempt=2),
+        settled("draft", "failed", attempt=2),
+    ]
+    assert [e["idempotency_key"] for e in mg.pending_requests(events)] == [
+        "guard:r1:fix-1:draft:a1"
+    ]
+
+
 def test_held_cycle_published_normal_recovered_and_other_cycle():
     guard = mg.fold_draft_guard(ENGAGED)
     assert mg.held_cycle_published(ENGAGED + [push_completed("fix-1")], guard) is True
@@ -483,3 +560,497 @@ def test_module_imports_only_the_allowed_modules():
     assert set(imports) <= {"__future__", "re", "dataclasses", "enum", ".conflicts"}, (
         imports
     )
+
+
+# =============================================================================
+# classify_toggles, engage_decision, release_decision, resume_decision
+# =============================================================================
+
+H = "a" * 40  # head sha
+T = "b" * 40  # another sha
+
+
+def rd(**overrides):
+    fields = {
+        "ok": True,
+        "state": "OPEN",
+        "is_draft": True,
+        "head_sha": H,
+        "auto_merge_armed": False,
+        "transitions": 3,
+        "complete": True,
+    }
+    fields.update(overrides)
+    return mg.GuardRead(**fields)
+
+
+def guard(phase="held", **overrides):
+    fields = {
+        "phase": phase,
+        "phase_before_request": None,
+        "cycle_id": "fix-1",
+        "original_is_draft": False,
+        "baseline": 2,
+        "run_toggles": 1,
+        "unsettled": 0,
+        "failed_mutations": 0,
+        "owned_draft": True,
+        "disabled_cause": None,
+    }
+    fields.update(overrides)
+    return fields
+
+
+A = mg.GuardAction
+
+
+def check(decision, action, reason, cause=None, notes=()):
+    assert decision.action == action, decision
+    assert decision.reason == reason, decision
+    assert decision.cause == cause, decision
+    assert decision.notes == notes, decision
+
+
+# --- classify_toggles -----------------------------------------------------------
+
+CLASSIFY_CASES = {
+    "incomplete_timeline": (guard(), rd(complete=False), "unreadable"),
+    "transitions_missing": (guard(), rd(transitions=None), "unreadable"),
+    "read_failed": (guard(), rd(ok=False), "unreadable"),
+    "draft_flag_missing": (guard(), rd(is_draft=None), "unreadable"),
+    "no_guard": (None, rd(), "unreadable"),
+    "baseline_missing": (guard(baseline=None), rd(), "unreadable"),
+    "observed_below_run_toggles": (guard(), rd(transitions=2), "unreadable"),
+    "one_extra_transition": (guard(), rd(transitions=4), "foreign"),
+    "held_but_pr_is_ready": (guard(), rd(is_draft=False), "foreign"),
+    "released_but_pr_is_draft": (
+        guard("released", run_toggles=2),
+        rd(transitions=4, is_draft=True),
+        "foreign",
+    ),
+    "held_matches": (guard(), rd(), "ok"),
+    "released_matches": (
+        guard("released", run_toggles=2),
+        rd(transitions=4, is_draft=False),
+        "ok",
+    ),
+    "equals_run_toggles_plus_failed": (
+        guard(failed_mutations=1),
+        rd(transitions=4),
+        "ok",
+    ),
+    "failed_call_did_not_land": (guard(failed_mutations=1), rd(transitions=3), "ok"),
+    "two_over_with_one_failed": (
+        guard(failed_mutations=1),
+        rd(transitions=5),
+        "foreign",
+    ),
+    "pending_engage_accepts_draft": (
+        guard("engage_pending", run_toggles=0, unsettled=1, owned_draft=False),
+        rd(transitions=3, is_draft=True),
+        "ok",
+    ),
+    "pending_engage_accepts_ready": (
+        guard("engage_pending", run_toggles=0, unsettled=1, owned_draft=False),
+        rd(transitions=2, is_draft=False),
+        "ok",
+    ),
+    "pending_release_accepts_draft": (
+        guard("release_pending", unsettled=1),
+        rd(transitions=3, is_draft=True),
+        "ok",
+    ),
+    "pending_release_accepts_ready": (
+        guard("release_pending", unsettled=1),
+        rd(transitions=4, is_draft=False),
+        "ok",
+    ),
+    "failed_on_client_but_landed": (
+        guard("release_pending", run_toggles=0, failed_mutations=1, owned_draft=False),
+        rd(transitions=3, is_draft=True),
+        "ok",
+    ),
+    "ready_then_user_redrafts": (
+        guard("released", run_toggles=2),
+        rd(transitions=5, is_draft=True),
+        "foreign",
+    ),
+}
+
+
+@pytest.mark.parametrize("name", sorted(CLASSIFY_CASES))
+def test_classify_toggles(name):
+    state, read, expected = CLASSIFY_CASES[name]
+    assert mg.classify_toggles(state, read) == expected
+
+
+# --- engage_decision ------------------------------------------------------------
+
+
+def engage(**overrides):
+    kwargs = {
+        "mode": "draft",
+        "ordinal": 3,
+        "cycle_id": "fix-1",
+        "guard": None,
+        "read": rd(is_draft=False, transitions=2),
+    }
+    kwargs.update(overrides)
+    return mg.engage_decision(**kwargs)
+
+
+@pytest.mark.parametrize(
+    ("overrides", "reason"),
+    [
+        ({"mode": "off"}, "mode_off"),
+        ({"mode": mg.GuardMode.OFF}, "mode_off"),
+        ({"ordinal": 2}, "ordinal"),
+        ({"ordinal": 0}, "ordinal"),
+        ({"cycle_id": "sync-1"}, "conflict_cycle"),
+        ({"cycle_id": "conflict-1"}, "conflict_cycle"),
+    ],
+)
+def test_engage_row_1_inert(overrides, reason):
+    check(engage(**overrides), A.NOOP, reason)
+
+
+def test_engage_row_2_disabled():
+    check(
+        engage(guard=guard("disabled", disabled_cause="user_override")),
+        A.NOOP,
+        "disabled",
+    )
+
+
+def test_engage_row_3_read_failed():
+    check(engage(read=rd(ok=False, state=None)), A.HALT_UNAVAILABLE, "read_failed")
+
+
+@pytest.mark.parametrize("state", ["MERGED", "CLOSED"])
+def test_engage_row_4_pr_not_open(state):
+    check(engage(read=rd(state=state)), A.HALT_PR_NOT_OPEN, "pr_not_open")
+
+
+def test_engage_row_5_retry_release_when_owned():
+    check(engage(guard=guard("release_pending")), A.RETRY_RELEASE, "release_pending")
+
+
+def test_engage_row_6_hold_when_ownership_unproven():
+    check(
+        engage(guard=guard("release_pending", owned_draft=False)),
+        A.HOLD,
+        "ownership_unproven",
+    )
+
+
+def test_engage_row_7_already_held():
+    check(engage(guard=guard("held")), A.NOOP, "already_held")
+
+
+@pytest.mark.parametrize(
+    "read", [rd(complete=False, is_draft=False), rd(transitions=None, is_draft=False)]
+)
+def test_engage_row_8_timeline_unreadable(read):
+    check(engage(read=read), A.HALT_UNAVAILABLE, "timeline_unreadable")
+
+
+def test_engage_row_9_foreign_toggle_skips_engage():
+    state = guard("released", run_toggles=2)
+    check(
+        engage(guard=state, read=rd(transitions=5, is_draft=False)),
+        A.SKIP_USER_OVERRIDE,
+        "user_override",
+        cause="user_override",
+    )
+
+
+def test_engage_row_10_already_draft_without_guard():
+    check(
+        engage(read=rd(is_draft=True)),
+        A.SKIP_ALREADY_DRAFT,
+        "already_draft",
+        cause="already_draft",
+    )
+
+
+def test_engage_row_11_engage_and_auto_merge_note():
+    check(engage(), A.ENGAGE, "engage")
+    check(
+        engage(read=rd(is_draft=False, auto_merge_armed=True)),
+        A.ENGAGE,
+        "engage",
+        notes=("auto_merge_armed",),
+    )
+
+
+def test_engage_second_cycle_after_a_release_engages_again():
+    state = guard("released", run_toggles=2)
+    check(
+        engage(guard=state, cycle_id="fix-2", read=rd(transitions=4, is_draft=False)),
+        A.ENGAGE,
+        "engage",
+    )
+
+
+# --- release_decision -----------------------------------------------------------
+
+
+def release(**overrides):
+    kwargs = {
+        "mode": "draft",
+        "ordinal": 3,
+        "cycle_id": "fix-1",
+        "guard": guard(),
+        "read": rd(),
+        "applied_edits": 2,
+        "target_sha": H,
+        "push_completed": True,
+    }
+    kwargs.update(overrides)
+    return mg.release_decision(**kwargs)
+
+
+@pytest.mark.parametrize(
+    ("overrides", "reason"),
+    [
+        ({"mode": "off"}, "mode_off"),
+        ({"ordinal": 1}, "ordinal"),
+        ({"cycle_id": "sync-2"}, "conflict_cycle"),
+    ],
+)
+def test_release_row_1_inert(overrides, reason):
+    check(release(**overrides), A.NOOP, reason)
+
+
+@pytest.mark.parametrize(
+    "state",
+    [
+        None,
+        guard("released"),
+        guard("disabled", disabled_cause="already_draft"),
+        guard("engage_pending"),
+    ],
+)
+def test_release_row_2_not_held(state):
+    check(release(guard=state), A.NOOP, "not_held")
+
+
+def test_release_row_3_read_failed():
+    check(release(read=rd(ok=False)), A.HOLD, "read_failed")
+
+
+def test_release_row_4_pr_not_open():
+    check(release(read=rd(state="MERGED")), A.HALT_PR_NOT_OPEN, "pr_not_open")
+
+
+def test_release_row_5_timeline_unreadable():
+    check(release(read=rd(transitions=None)), A.HOLD, "timeline_unreadable")
+
+
+def test_release_row_6_foreign_toggle():
+    check(
+        release(read=rd(is_draft=False)),
+        A.SKIP_USER_OVERRIDE,
+        "user_override",
+        cause="user_override",
+    )
+
+
+def test_release_row_7_zero_edits_releases_without_a_push():
+    check(
+        release(applied_edits=0, push_completed=False, target_sha=None),
+        A.RELEASE,
+        "no_edits",
+        cause="no_edits",
+    )
+
+
+def test_release_row_7_applies_to_a_zero_edit_cycle_after_a_fixing_cycle():
+    earlier = guard(cycle_id="fix-2", run_toggles=3, baseline=2)
+    read = rd(transitions=5)
+    check(
+        release(
+            guard=earlier,
+            cycle_id="fix-2",
+            read=read,
+            applied_edits=0,
+            push_completed=False,
+        ),
+        A.RELEASE,
+        "no_edits",
+        cause="no_edits",
+    )
+
+
+def test_release_row_8_published_head_releases():
+    check(release(), A.RELEASE, "pushed", cause="pushed")
+    check(
+        release(guard=guard("release_pending", unsettled=0, failed_mutations=1)),
+        A.RELEASE,
+        "pushed",
+        cause="pushed",
+    )
+
+
+def test_release_row_9_holds_on_moved_head_or_missing_push():
+    check(release(read=rd(head_sha=T)), A.HOLD, "head_mismatch")
+    check(release(push_completed=False), A.HOLD, "push_not_completed")
+    check(release(target_sha=None), A.HOLD, "head_mismatch")
+
+
+def test_disabled_guard_never_engages_or_releases():
+    state = guard("disabled", disabled_cause="already_draft")
+    assert engage(guard=state).action == A.NOOP
+    assert release(guard=state).action == A.NOOP
+
+
+# --- resume_decision ------------------------------------------------------------
+
+
+def resume(**overrides):
+    kwargs = {
+        "mode": "draft",
+        "ordinal": 3,
+        "guard": guard(),
+        "read": rd(),
+        "pending": [],
+        "dangling_branch": None,
+        "published": False,
+        "applied_edits": 1,
+        "target_sha": H,
+    }
+    kwargs.update(overrides)
+    return mg.resume_decision(**kwargs)
+
+
+def pending_request(to):
+    return req(to)
+
+
+def test_resume_row_1_no_guard():
+    check(resume(guard=None), A.NOOP, "no_guard")
+
+
+def test_resume_row_2_report_held_wins_over_reconcile():
+    pending_guard = guard(
+        "engage_pending", run_toggles=0, unsettled=1, owned_draft=False
+    )
+    check(
+        resume(ordinal=2, guard=pending_guard, pending=[pending_request("draft")]),
+        A.REPORT_HELD,
+        "held_report",
+    )
+    check(resume(mode="off"), A.REPORT_HELD, "held_report")
+    check(
+        resume(mode=mg.GuardMode.OFF, guard=guard("release_pending")),
+        A.REPORT_HELD,
+        "held_report",
+    )
+
+
+@pytest.mark.parametrize("phase", ["released", "disabled"])
+def test_resume_row_2_skips_settled_phases(phase):
+    check(resume(ordinal=2, guard=guard(phase)), A.NOOP, "nothing_to_do")
+    check(resume(mode="off", guard=guard(phase)), A.NOOP, "nothing_to_do")
+
+
+ENGAGE_PENDING = guard("engage_pending", run_toggles=0, unsettled=1, owned_draft=False)
+RELEASE_PENDING = guard("release_pending", phase_before_request="held", unsettled=1)
+
+
+@pytest.mark.parametrize(
+    ("state", "to", "read", "reason", "cause"),
+    [
+        (
+            ENGAGE_PENDING,
+            "draft",
+            rd(is_draft=True, transitions=3),
+            "resume_reconciled",
+            "resume_reconciled",
+        ),
+        (
+            RELEASE_PENDING,
+            "ready",
+            rd(is_draft=False, transitions=4),
+            "resume_reconciled",
+            "resume_reconciled",
+        ),
+        (
+            ENGAGE_PENDING,
+            "draft",
+            rd(is_draft=False, transitions=2),
+            "not_applied",
+            "not_applied",
+        ),
+        (
+            RELEASE_PENDING,
+            "ready",
+            rd(is_draft=True, transitions=3),
+            "not_applied",
+            "not_applied",
+        ),
+        (ENGAGE_PENDING, "draft", rd(is_draft=True, transitions=2), "ambiguous", None),
+        (ENGAGE_PENDING, "draft", rd(is_draft=False, transitions=3), "ambiguous", None),
+        (ENGAGE_PENDING, "draft", rd(transitions=None), "ambiguous", None),
+        (ENGAGE_PENDING, "draft", rd(ok=False), "ambiguous", None),
+        (ENGAGE_PENDING, "draft", None, "ambiguous", None),
+    ],
+)
+def test_resume_row_3_reconcile_reasons(state, to, read, reason, cause):
+    check(
+        resume(guard=state, pending=[pending_request(to)], read=read),
+        A.RECONCILE,
+        reason,
+        cause=cause,
+    )
+
+
+def test_resume_row_4_release_after_a_landed_recovered_push():
+    check(resume(dangling_branch="landed"), A.RELEASE, "pushed", cause="pushed")
+    check(
+        resume(dangling_branch=recovery.BRANCH_A_LANDED),
+        A.RELEASE,
+        "pushed",
+        cause="pushed",
+    )
+
+
+def test_resume_row_4_release_after_a_normal_completed_push():
+    check(resume(published=True), A.RELEASE, "pushed", cause="pushed")
+
+
+def test_resume_row_4_holds_on_a_moved_head_or_unknown_target():
+    check(resume(published=True, read=rd(head_sha=T)), A.HOLD, "head_mismatch")
+    check(resume(published=True, target_sha=None), A.HOLD, "head_mismatch")
+    check(resume(published=True, read=None), A.HOLD, "read_failed")
+
+
+def test_resume_row_4_published_with_zero_counter_still_counts_one_edit():
+    check(resume(published=True, applied_edits=0), A.RELEASE, "pushed", cause="pushed")
+
+
+def test_resume_held_without_publication_is_a_noop():
+    check(resume(), A.NOOP, "nothing_to_do")
+
+
+def test_resume_row_5_not_landed_stays_held():
+    check(resume(dangling_branch="not_landed"), A.NOOP, "held_through_redrive")
+
+
+@pytest.mark.parametrize("phase", ["held", "release_pending", "released"])
+def test_resume_row_6_ambiguous_tip_holds(phase):
+    check(
+        resume(guard=guard(phase), dangling_branch="ambiguous"),
+        A.HOLD,
+        "ambiguous_remote_tip",
+    )
+
+
+def test_resume_row_7_retry_release_when_owned():
+    check(resume(guard=guard("release_pending")), A.RETRY_RELEASE, "release_pending")
+
+
+def test_resume_row_8_ownership_unproven_when_live_draft():
+    unowned = guard("release_pending", owned_draft=False)
+    check(resume(guard=unowned, read=rd(is_draft=True)), A.HOLD, "ownership_unproven")
+    check(resume(guard=unowned, read=rd(is_draft=False)), A.NOOP, "nothing_to_do")

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
