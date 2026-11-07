aa9d9795cbb4b15e307e4e40316067a5fec757f4
Review one task for spec compliance.

Task brief: ## Task 5: Fold the guard into the run log and export the public names

Depends on: Task 3
Depends on: Task 4

Edit `src/superclaude/pr_submit/run_log.py` `rebuild_state()` so `state["draft_guard"]` is `fold_draft_guard(events)` (default `None`, documented in the method docstring beside the #305 keys), importing from `src/superclaude/pr_submit/merge_guard.py`. Add the public guard names (the enums, dataclasses, the `BRANCH_*` constants, `fix_cycle_id`, `next_cycle_number`, `fold_draft_guard`, `pending_requests`, `held_cycle_published`, `classify_toggles`, `engage_decision`, `release_decision`, `resume_decision`, `guard_status`) to the imports and `__all__` of `src/superclaude/pr_submit/__init__.py`. Update `tests/pr_submit/test_run_log.py`: add `"draft_guard": None` to `_NEW_KEY_DEFAULTS` and add a test that a legacy log rebuilds every old key unchanged with `draft_guard` `None`, and that a log with a request and a confirmed settle rebuilds `phase: held`. Add `src/superclaude/pr_submit/merge_guard.py` to `CORE_PURE_FILES` in `tests/pr_submit/test_static_grep.py`.

Acceptance criteria:
- T5.AC1: `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_idempotency.py -q` passes, including `test_tn50_core_pure_no_gh_git_tokens` over the new file and the exact key-set assertions that use `_NEW_KEY_DEFAULTS`.
- T5.AC2: `uv run python -c "from superclaude.pr_submit import fold_draft_guard, engage_decision, release_decision, resume_decision, held_cycle_published, fix_cycle_id; import superclaude.pr_submit.run_log"` exits 0 in a fresh interpreter (no import cycle).
- T5.AC3: Rebuilding a log that holds `requested(draft)` then `settled(draft, confirmed, changed=True)` returns `state["draft_guard"]["phase"] == "held"` with `owned_draft` true; a log that ends after only the request returns `unsettled == 1` and phase `engage_pending`.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: aa9d9795cbb4b15e307e4e40316067a5fec757f4
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/run_log.py b/src/superclaude/pr_submit/run_log.py
index 7ecedd17..7d551797 100644
--- a/src/superclaude/pr_submit/run_log.py
+++ b/src/superclaude/pr_submit/run_log.py
@@ -21,6 +21,7 @@ import os
 import re
 from pathlib import Path
 
+from .merge_guard import fold_draft_guard
 from .models import EventType
 
 # The 7 idempotency sets (§11.4 + V1.1 addendum §6.3 + INV-S1).
@@ -198,9 +199,18 @@ class RunLog:
         - ``push_rejected``: ``True`` once a ``push_aborted_or_not_landed`` event
           carries ``rejected is True``.
 
-        A log without ``kind`` fields or conflict-cycle events rebuilds every
-        pre-existing key exactly as before, with the four keys at their defaults
-        (``0``, ``[]``, ``None``, ``False``) (NFR-12).
+        Issue #375 (merge guard) adds one key:
+
+        - ``draft_guard``: :func:`~superclaude.pr_submit.merge_guard.fold_draft_guard`
+          over the events, or ``None`` when the log holds no guard record. It is a
+          plain dict (``phase``, ``phase_before_request``, ``cycle_id``,
+          ``original_is_draft``, ``baseline``, ``run_toggles``, ``unsettled``,
+          ``failed_mutations``, ``owned_draft``, ``disabled_cause``).
+
+        A log without ``kind`` fields, conflict-cycle events or guard events
+        rebuilds every pre-existing key exactly as before, with the four #305 keys
+        at their defaults (``0``, ``[]``, ``None``, ``False``) and ``draft_guard``
+        ``None`` (NFR-12).
         """
         state = {
             "pr_number": self.pr_number,
@@ -221,6 +231,8 @@ class RunLog:
             "conflict_cycles": [],
             "open_conflict_cycle": None,
             "push_rejected": False,
+            # Issue #375: the folded merge-guard record (None until a guard event).
+            "draft_guard": None,
         }
         sets = {s: set() for s in IDEMPOTENCY_SETS}
         retriggered_cycles: set = set()
@@ -228,7 +240,8 @@ class RunLog:
         # Open conflict cycles by id; insertion order is sync_started order (a
         # re-opened id is moved to the end), so the last entry is the newest.
         open_cycles: dict = {}
-        for ev in self.read_events():
+        events = self.read_events()
+        for ev in events:
             state["last_event_id"] = ev.get("event_id", state["last_event_id"])
             et = ev.get("event_type")
             if ev.get("state_after"):
@@ -343,6 +356,7 @@ class RunLog:
         state["open_conflict_cycle"] = (
             list(open_cycles.values())[-1] if open_cycles else None
         )
+        state["draft_guard"] = fold_draft_guard(events)
         return state
 
     def materialize_snapshot(self) -> dict:

diff --git a/src/superclaude/pr_submit/__init__.py b/src/superclaude/pr_submit/__init__.py
index 78ded428..d42c1eda 100644
--- a/src/superclaude/pr_submit/__init__.py
+++ b/src/superclaude/pr_submit/__init__.py
@@ -8,7 +8,8 @@ markdown orchestrator and bash glue defer to: the finite state machine
 (:mod:`~superclaude.pr_submit.classifier` / :mod:`~superclaude.pr_submit.detection`),
 the write-ahead JSONL run-log (:mod:`~superclaude.pr_submit.run_log`), the
 crash-window recovery (:mod:`~superclaude.pr_submit.recovery`), the merge-conflict
-core (:mod:`~superclaude.pr_submit.conflicts`, issue #305), and the shared data
+core (:mod:`~superclaude.pr_submit.conflicts`, issue #305), the merge guard
+(:mod:`~superclaude.pr_submit.merge_guard`, issue #375), and the shared data
 models (:mod:`~superclaude.pr_submit.models`).
 
 NFR-6 core purity: the modules in this package contain ZERO ``gh``/``git`` tokens.
@@ -68,6 +69,27 @@ from .fsm import (
     should_retrigger,
     transition,
 )
+from .merge_guard import (
+    BRANCH_AMBIGUOUS,
+    BRANCH_LANDED,
+    BRANCH_NOT_LANDED,
+    Direction,
+    GuardAction,
+    GuardDecision,
+    GuardMode,
+    GuardRead,
+    Phase,
+    classify_toggles,
+    engage_decision,
+    fix_cycle_id,
+    fold_draft_guard,
+    guard_status,
+    held_cycle_published,
+    next_cycle_number,
+    pending_requests,
+    release_decision,
+    resume_decision,
+)
 from .models import (
     EventType,
     Finding,
@@ -148,6 +170,26 @@ __all__ = [
     "resolution_record_ok",
     "should_retrigger",
     "sync_fail_state",
+    # merge guard (issue #375)
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
     # reviewers (Augment + Codex)
     "REVIEWERS",
     "reviewer_identities",

diff --git a/tests/pr_submit/test_run_log.py b/tests/pr_submit/test_run_log.py
index 4c922221..39f91158 100644
--- a/tests/pr_submit/test_run_log.py
+++ b/tests/pr_submit/test_run_log.py
@@ -328,6 +328,7 @@ _NEW_KEY_DEFAULTS = {
     "conflict_cycles": [],
     "open_conflict_cycle": None,
     "push_rejected": False,
+    "draft_guard": None,
 }
 
 
@@ -411,13 +412,79 @@ def _sync_concluded(rl: RunLog, cycle_id: str, outcome: str = "pushed", **extra)
 
 def test_fold_old_log_without_kind_rebuilds_identically(tmp_path):
     """NFR-12: a recorded legacy log rebuilds every pre-existing key unchanged and
-    the four new keys at their defaults; no other key is added."""
+    the new keys at their defaults; no other key is added."""
     state = _legacy_runlog(tmp_path).rebuild_state()
     assert {k: state[k] for k in _LEGACY_EXPECTED} == _LEGACY_EXPECTED
     assert set(state) == set(_LEGACY_EXPECTED) | set(_NEW_KEY_DEFAULTS)
     assert state == {**_LEGACY_EXPECTED, **_NEW_KEY_DEFAULTS}
 
 
+def test_legacy_log_rebuilds_with_draft_guard_none(tmp_path):
+    """A log written before the merge guard existed has no guard record."""
+    state = _legacy_runlog(tmp_path).rebuild_state()
+    assert state["draft_guard"] is None
+    assert {k: state[k] for k in _LEGACY_EXPECTED} == _LEGACY_EXPECTED
+
+
+def _guard_requested(rl: RunLog, to: str, **extra) -> None:
+    rl.append(
+        {
+            "event_type": EventType.DRAFT_GUARD_REQUESTED.value,
+            "run_id": "r1",
+            "cycle_id": "fix-1",
+            "to": to,
+            "idempotency_key": f"guard:r1:fix-1:{to}:a1",
+            **extra,
+        }
+    )
+
+
+def _guard_settled(rl: RunLog, to: str, outcome: str, **extra) -> None:
+    rl.append(
+        {
+            "event_type": EventType.DRAFT_GUARD_SETTLED.value,
+            "run_id": "r1",
+            "cycle_id": "fix-1",
+            "to": to,
+            "idempotency_key": f"guard:r1:fix-1:{to}:a1",
+            "outcome": outcome,
+            "changed": outcome == "confirmed",
+            "cause": None,
+            **extra,
+        }
+    )
+
+
+def test_fold_guard_request_and_confirmed_settle_rebuild_phase_held(tmp_path):
+    rl = RunLog(301, tmp_path)
+    _guard_requested(rl, "draft", timeline_baseline=2, original_is_draft=False)
+    _guard_settled(rl, "draft", "confirmed")
+    guard = rl.rebuild_state()["draft_guard"]
+    assert guard["phase"] == "held"
+    assert guard["owned_draft"] is True
+    assert guard["run_toggles"] == 1
+    assert guard["unsettled"] == 0
+    assert guard["baseline"] == 2
+
+
+def test_fold_guard_request_alone_is_engage_pending_with_one_unsettled(tmp_path):
+    rl = RunLog(302, tmp_path)
+    _guard_requested(rl, "draft", timeline_baseline=0, original_is_draft=False)
+    guard = rl.rebuild_state()["draft_guard"]
+    assert guard["phase"] == "engage_pending"
+    assert guard["unsettled"] == 1
+    assert guard["owned_draft"] is False
+
+
+def test_guard_state_survives_the_snapshot_round_trip(tmp_path):
+    """The folded record is plain data, so the rebuildable snapshot can store it."""
+    rl = RunLog(303, tmp_path)
+    _guard_requested(rl, "draft", timeline_baseline=1, original_is_draft=False)
+    _guard_settled(rl, "draft", "confirmed")
+    state = rl.materialize_snapshot()
+    assert json.loads(rl.snapshot_path.read_text(encoding="utf-8")) == state
+
+
 def test_fold_sync_push_counts_in_sync_push_count_not_push_count(tmp_path):
     """A landed `kind: "sync"` push counts in sync_push_count only (INV-018)."""
     rl = RunLog(201, tmp_path)

diff --git a/tests/pr_submit/test_static_grep.py b/tests/pr_submit/test_static_grep.py
index 2317bde1..fbca9a29 100644
--- a/tests/pr_submit/test_static_grep.py
+++ b/tests/pr_submit/test_static_grep.py
@@ -50,6 +50,8 @@ CORE_PURE_FILES = [
     PR_SUBMIT_PKG / "ci.py",
     # issue #305: the conflict core is pure (no version-control tokens)
     PR_SUBMIT_PKG / "conflicts.py",
+    # issue #375: the merge-guard core is pure (no version-control tokens)
+    PR_SUBMIT_PKG / "merge_guard.py",
 ]
 
 AUGGIE_REVIEW_CMD = REPO_ROOT / "src" / "superclaude" / "commands" / "auggie-review.md"

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
