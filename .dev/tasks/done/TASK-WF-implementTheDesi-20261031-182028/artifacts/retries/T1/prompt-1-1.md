34f8e91ca1982a8ede10bc4c6db99d8f11675b04
Review one task for spec compliance.

Task brief: ## Task 1: Add the reviewer field and the two reviewer events to the models

Edit src/superclaude/pr_submit/models.py per design sections 7 and 13: add `reviewer: str = "augment"` to `Finding`, add `EventType.REVIEWER_ABSENT = "reviewer_absent"` and `EventType.REVIEWER_INCOMPLETE = "reviewer_incomplete"`, and update the class docstrings that state the member count (39 → 41). Update tests/pr_submit/test_run_log.py test_eventtype_is_39_members_with_silence_events to assert 41 members including the two new values.

Acceptance criteria:
- `len(EventType) == 41` and both new values exist; `Finding(path="a", line=1, body="b").reviewer == "augment"`.
- `uv run pytest tests/pr_submit/test_run_log.py -q -p no:cacheprovider` passes.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 34f8e91ca1982a8ede10bc4c6db99d8f11675b04
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/models.py b/src/superclaude/pr_submit/models.py
index 53a239dc..358d5f12 100644
--- a/src/superclaude/pr_submit/models.py
+++ b/src/superclaude/pr_submit/models.py
@@ -1,9 +1,10 @@
 """Canonical data models for the ``sc:pr-submit`` deterministic core.
 
-Defines the closed run-log event enum (exactly 39 members — the 32 from spec
+Defines the closed run-log event enum (exactly 41 members — the 32 from spec
 §11.3 plus ``push_aborted_or_not_landed`` from §12.1, plus the 4 V1.1
 re-review/fallback events from addendum §6.1, plus ``silence_rerequested`` and
-``terminal_augment_no_response``), the severity tiers, the
+``terminal_augment_no_response``, plus the reviewer events ``reviewer_absent``
+and ``reviewer_incomplete``), the severity tiers, the
 single-FSM state lexicon (spec §5.1; Python identifiers drop the spec's prime, so
 ``S4'_HALT_BEFORE_PUSH`` becomes ``S4_HALT_BEFORE_PUSH``), and the ``Finding`` /
 ``SkillResult`` dataclasses the test bodies assert against.
@@ -19,14 +20,17 @@ from enum import Enum
 
 
 class EventType(str, Enum):
-    """Closed enum of run-log event types — EXACTLY 39 members.
+    """Closed enum of run-log event types — EXACTLY 41 members.
 
     The 32 event types listed in spec §11.3 (merged-spec.md:724-731) PLUS
     ``push_aborted_or_not_landed`` (spec §12.1 line 771 — the crash-window
     not-landed branch) — the 33 prior members — PLUS the 4 V1.1
     re-review/fallback events (``rereview_requested``, ``decline_detected``,
     ``auggie_fallback_invoked``, ``max_rounds_clamped``; addendum §6.1) PLUS
-    ``silence_rerequested`` (INV-S1) and ``terminal_augment_no_response``.
+    ``silence_rerequested`` (INV-S1) and ``terminal_augment_no_response`` PLUS
+    the two reviewer events ``reviewer_absent`` (a reviewer with no activity is
+    ignored for the rest of the run) and ``reviewer_incomplete`` (a present
+    reviewer did not complete within ``--timeout``).
     The run-log writer validates every appended event against this closed set;
     an event outside it is a programming error.
     """
@@ -81,6 +85,9 @@ class EventType(str, Enum):
     MAX_ROUNDS_CLAMPED = "max_rounds_clamped"
     SILENCE_REREQUESTED = "silence_rerequested"
     TERMINAL_AUGMENT_NO_RESPONSE = "terminal_augment_no_response"
+    # --- reviewer presence (Augment + Codex) — the 40th-41st ---
+    REVIEWER_ABSENT = "reviewer_absent"
+    REVIEWER_INCOMPLETE = "reviewer_incomplete"
 
 
 class Severity(str, Enum):
@@ -147,12 +154,13 @@ TERMINAL_STATES = frozenset(
 
 @dataclass
 class Finding:
-    """A normalized Augment review finding.
+    """A normalized review finding from Augment or Codex.
 
-    ``severity_hint``/``category``/``confidence``/``in_diff`` are the raw Augment
+    ``severity_hint``/``category``/``confidence``/``in_diff`` are the raw reviewer
     inputs; ``remapped_severity`` is filled by the severity router (FR-3.1) and
     ``verification_status`` by the verify-before-remediate wave (FR-3.5,
-    one of ``"unverified"`` / ``"verified"`` / ``"report_only"``).
+    one of ``"unverified"`` / ``"verified"`` / ``"report_only"``). ``reviewer``
+    names the bot whose thread this is (``"augment"`` or ``"codex"``).
     """
 
     path: str
@@ -170,6 +178,7 @@ class Finding:
     review_id: int | str | None = None
     original_line: int | None = None
     is_outdated: bool = False
+    reviewer: str = "augment"
 
     @property
     def fix_key(self) -> str:
@@ -209,7 +218,8 @@ class SkillResult:
     # ends in PROPOSED (the L1 ceiling proposes but applies no edits, T-402).
     proposal: str | None = None
     # --- V1.1 re-trigger / fallback fields (addendum §6.1) ---
-    # ``rereview_request_count`` counts S5a re-trigger comments (INV-R1, monotone,
+    # ``rereview_request_count`` counts re-triggered push cycles (one cycle may post
+    # an Augment and a Codex re-trigger comment; INV-R1, monotone,
     # <= max_rounds); ``fallback_engaged``/``auggie_review_invoked`` flag the R2
     # single-shot /sc:auggie-review fallback (INV-R2 strict-once);
     # ``decline_detected`` flags an Augment "abnormally large" decline (FR-9.1);
diff --git a/src/superclaude/pr_submit/run_log.py b/src/superclaude/pr_submit/run_log.py
index 84b18b66..e46bef15 100644
--- a/src/superclaude/pr_submit/run_log.py
+++ b/src/superclaude/pr_submit/run_log.py
@@ -108,13 +108,14 @@ class RunLog:
     def append(self, event: dict) -> dict:
         """Append a validated, redacted event with a monotonic ``event_id`` and fsync.
 
-        Raises :class:`ValueError` if ``event_type`` is not one of the 37 closed
+        Raises :class:`ValueError` if ``event_type`` is not one of the 41 closed
         enum values (the run-log writer validates against ``models.EventType``).
         """
         event_type = event.get("event_type")
         if event_type not in _VALID_EVENT_VALUES:
             raise ValueError(
-                f"unknown event_type: {event_type!r} (not one of the 37 §11.3 events)"
+                f"unknown event_type: {event_type!r} "
+                f"(not one of the {len(_VALID_EVENT_VALUES)} closed EventType values)"
             )
         self._event_id += 1
         record = {
diff --git a/tests/pr_submit/test_run_log.py b/tests/pr_submit/test_run_log.py
index c112cd62..cee142de 100644
--- a/tests/pr_submit/test_run_log.py
+++ b/tests/pr_submit/test_run_log.py
@@ -162,10 +162,13 @@ def test_rebuild_from_jsonl_is_authoritative(tmp_path):
 # --- V1.1 closed-enum count + new-event folds (addendum §6.1/§6.3) ------------
 
 
-def test_eventtype_is_39_members_with_silence_events():
-    """The closed EventType enum has EXACTLY 39 members, including INV-S1."""
-    assert len(EventType) == 39
-    assert len(list(EventType)) == 39
+def test_eventtype_is_41_members_with_silence_and_reviewer_events():
+    """The closed EventType enum has EXACTLY 41 members, including INV-S1 and the
+    two reviewer-presence events."""
+    assert len(EventType) == 41
+    assert len(list(EventType)) == 41
+    assert EventType.REVIEWER_ABSENT.value == "reviewer_absent"
+    assert EventType.REVIEWER_INCOMPLETE.value == "reviewer_incomplete"
     assert EventType.REREVIEW_REQUESTED.value == "rereview_requested"
     assert EventType.DECLINE_DETECTED.value == "decline_detected"
     assert EventType.AUGGIE_FALLBACK_INVOKED.value == "auggie_fallback_invoked"
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
