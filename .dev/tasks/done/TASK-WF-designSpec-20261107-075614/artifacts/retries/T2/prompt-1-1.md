9088e6e6aee3f0eae1e07a441ab585cda00204cb
Review one task for spec compliance.

Task brief: ## Task 2: Add the two guard events to the closed event enum and the enumeration texts

Depends on: Task 1

Edit `src/superclaude/pr_submit/models.py`: add `DRAFT_GUARD_REQUESTED = "draft_guard_requested"` and `DRAFT_GUARD_SETTLED = "draft_guard_settled"` to `EventType` (a comment block like the conflict-cycle one), and change the module docstring and the `EventType` class docstring from "exactly 43 members" to 45, naming the new events. Edit the `RunLog.append` docstring in `src/superclaude/pr_submit/run_log.py` that says "43 closed" to 45. Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md`: its heading "The 43 event types" and the sentence that says the enum has EXACTLY 43 members become 45 and name `draft_guard_requested` and `draft_guard_settled`, without the whole words `gh` or `git` (the file is in `CORE_PURE_FILES`). Update `tests/pr_submit/test_run_log.py` (the test `test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events`: rename it to describe 45 members, assert both lengths are 45 and both new values are present) and the `len(EventType)` assertion in `tests/pr_submit/test_codex_reviews.py` to 45. Leave `tests/pr_submit/test_idempotency.py` (7 sets) unchanged. Run `make sync-dev`.

Acceptance criteria:
- T2.AC1: `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_idempotency.py tests/pr_submit/test_static_grep.py -q` passes with `len(EventType) == 45` and the two new values asserted.
- T2.AC2: `RunLog.append` accepts an event with `event_type: "draft_guard_requested"` and still rejects an unknown type, with the updated count in the error message.
- T2.AC3: `grep -rn "43" src/superclaude/pr_submit/models.py src/superclaude/pr_submit/run_log.py src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md` shows no remaining claim that the enum has 43 members, and `refs/loop-guard.md` names both new event values.
- T2.AC4: `make verify-sync` exits 0 after the sync.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: 9088e6e6aee3f0eae1e07a441ab585cda00204cb
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/models.py b/src/superclaude/pr_submit/models.py
index 515b1c3b..15b34c09 100644
--- a/src/superclaude/pr_submit/models.py
+++ b/src/superclaude/pr_submit/models.py
@@ -1,11 +1,12 @@
 """Canonical data models for the ``sc:pr-submit`` deterministic core.
 
-Defines the closed run-log event enum (exactly 43 members — the 32 from spec
+Defines the closed run-log event enum (exactly 45 members — the 32 from spec
 §11.3 plus ``push_aborted_or_not_landed`` from §12.1, plus the 4 V1.1
 re-review/fallback events from addendum §6.1, plus ``silence_rerequested`` and
 ``terminal_augment_no_response``, plus the reviewer events ``reviewer_absent``
 and ``reviewer_incomplete``, plus the two conflict-cycle events
-``sync_started`` and ``sync_concluded``), the severity tiers, the
+``sync_started`` and ``sync_concluded``, plus the two merge-guard events
+``draft_guard_requested`` and ``draft_guard_settled``), the severity tiers, the
 single-FSM state lexicon (spec §5.1; Python identifiers drop the spec's prime, so
 ``S4'_HALT_BEFORE_PUSH`` becomes ``S4_HALT_BEFORE_PUSH``), and the ``Finding`` /
 ``SkillResult`` dataclasses the test bodies assert against.
@@ -21,7 +22,7 @@ from enum import Enum
 
 
 class EventType(str, Enum):
-    """Closed enum of run-log event types — EXACTLY 43 members.
+    """Closed enum of run-log event types — EXACTLY 45 members.
 
     The 32 event types listed in spec §11.3 (merged-spec.md:724-731) PLUS
     ``push_aborted_or_not_landed`` (spec §12.1 line 771 — the crash-window
@@ -32,7 +33,11 @@ class EventType(str, Enum):
     the two reviewer events ``reviewer_absent`` (a reviewer with no activity is
     ignored for the rest of the run) and ``reviewer_incomplete`` (a present
     reviewer did not complete within ``--timeout``) PLUS the two conflict-cycle
-    events ``sync_started`` and ``sync_concluded`` (issue #305, both tiers).
+    events ``sync_started`` and ``sync_concluded`` (issue #305, both tiers) PLUS
+    the two merge-guard events ``draft_guard_requested`` and
+    ``draft_guard_settled`` (issue #375: a PR is held as a draft while a fix
+    cycle runs; a request is written before the change, a settle records its
+    outcome).
     The run-log writer validates every appended event against this closed set;
     an event outside it is a programming error.
     """
@@ -93,6 +98,9 @@ class EventType(str, Enum):
     # --- merge-conflict cycles (issue #305), both tiers - the 42nd-43rd ---
     SYNC_STARTED = "sync_started"
     SYNC_CONCLUDED = "sync_concluded"
+    # --- merge guard (issue #375): hold the PR as a draft during a fix cycle - the 44th-45th ---
+    DRAFT_GUARD_REQUESTED = "draft_guard_requested"
+    DRAFT_GUARD_SETTLED = "draft_guard_settled"
 
 
 class Severity(str, Enum):

diff --git a/src/superclaude/pr_submit/run_log.py b/src/superclaude/pr_submit/run_log.py
index 1e2c1e43..7ecedd17 100644
--- a/src/superclaude/pr_submit/run_log.py
+++ b/src/superclaude/pr_submit/run_log.py
@@ -114,7 +114,7 @@ class RunLog:
     def append(self, event: dict) -> dict:
         """Append a validated, redacted event with a monotonic ``event_id`` and fsync.
 
-        Raises :class:`ValueError` if ``event_type`` is not one of the 43 closed
+        Raises :class:`ValueError` if ``event_type`` is not one of the 45 closed
         enum values (the run-log writer validates against ``models.EventType``).
         """
         event_type = event.get("event_type")

diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
index ddf845e9..83cdfd11 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
@@ -83,14 +83,15 @@ preceded by a **write-ahead** record fsynced BEFORE the side effect.
 Default `<output-dir>` = `<repo-root>/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/` (cwd-relative; the
 repo the operator runs `sc:pr-submit` from) unless `--resume` supplies an existing log dir.
 
-### The 43 event types (§11.3 + §12.1 + V1.1 §6.1 + silence + reviewers + conflict cycles)
+### The 45 event types (§11.3 + §12.1 + V1.1 §6.1 + silence + reviewers + conflict cycles + merge guard)
 
-The closed `EventType` enum has EXACTLY 43 members — the 32 from §11.3 plus
+The closed `EventType` enum has EXACTLY 45 members — the 32 from §11.3 plus
 `push_aborted_or_not_landed` (§12.1, the crash-window not-landed branch) — the 33 prior — plus the 4
 V1.1 re-review/fallback events (`rereview_requested`, `decline_detected`, `auggie_fallback_invoked`,
 `max_rounds_clamped`; addendum §6.1), the 2 silence events (`silence_rerequested`,
 `terminal_augment_no_response`), the 2 reviewer events (`reviewer_absent`,
-`reviewer_incomplete`) and the 2 conflict-cycle events (`sync_started`, `sync_concluded`):
+`reviewer_incomplete`), the 2 conflict-cycle events (`sync_started`, `sync_concluded`) and the 2
+merge-guard events (`draft_guard_requested`, `draft_guard_settled`):
 `run_started`, `environment_check`, `pr_create_attempted`, `pr_created`, `monitor_armed`,
 `baseline_captured`, `poll_attempt`, `poll_result`, `api_backoff`, `classifier_unknown_shape`,
 `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`,
@@ -100,7 +101,8 @@ V1.1 re-review/fallback events (`rereview_requested`, `decline_detected`, `auggi
 `terminal_timeout`, `terminal_max_rounds`, `terminal_halted`, `terminal_failed`,
 `push_aborted_or_not_landed`, `rereview_requested`, `decline_detected`, `auggie_fallback_invoked`,
 `max_rounds_clamped`, `silence_rerequested`, `terminal_augment_no_response`, `reviewer_absent`,
-`reviewer_incomplete`, `sync_started`, `sync_concluded`.
+`reviewer_incomplete`, `sync_started`, `sync_concluded`, `draft_guard_requested`,
+`draft_guard_settled`.
 
 Each line carries `schema_version`, a unique+monotonic `event_id`, `event_type`, `timestamp`,
 `run_id`, `pr{repo,number,url,base,head}`, `state_before`, `state_after`,

diff --git a/tests/pr_submit/test_run_log.py b/tests/pr_submit/test_run_log.py
index 56830364..4c922221 100644
--- a/tests/pr_submit/test_run_log.py
+++ b/tests/pr_submit/test_run_log.py
@@ -168,11 +168,14 @@ def test_rebuild_from_jsonl_is_authoritative(tmp_path):
 # --- V1.1 closed-enum count + new-event folds (addendum §6.1/§6.3) ------------
 
 
-def test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events():
-    """The closed EventType enum has EXACTLY 43 members, including INV-S1, the two
-    reviewer-presence events and the two conflict-cycle events."""
-    assert len(EventType) == 43
-    assert len(list(EventType)) == 43
+def test_eventtype_is_45_members_with_silence_reviewer_conflict_and_guard_events():
+    """The closed EventType enum has EXACTLY 45 members, including INV-S1, the two
+    reviewer-presence events, the two conflict-cycle events and the two merge-guard
+    events."""
+    assert len(EventType) == 45
+    assert len(list(EventType)) == 45
+    assert EventType.DRAFT_GUARD_REQUESTED.value == "draft_guard_requested"
+    assert EventType.DRAFT_GUARD_SETTLED.value == "draft_guard_settled"
     assert EventType.SYNC_STARTED.value == "sync_started"
     assert EventType.SYNC_CONCLUDED.value == "sync_concluded"
     assert EventType.REVIEWER_ABSENT.value == "reviewer_absent"
@@ -205,6 +208,17 @@ def test_new_v11_events_pass_closed_enum_append_validation(tmp_path):
         rl.append({"event_type": "not_a_real_event"})
 
 
+def test_guard_events_pass_closed_enum_append_validation(tmp_path):
+    """The two merge-guard events are valid closed-enum values, and an unknown type
+    is still rejected with the updated member count in the message."""
+    rl = RunLog(32, tmp_path)
+    for member in (EventType.DRAFT_GUARD_REQUESTED, EventType.DRAFT_GUARD_SETTLED):
+        rec = rl.append({"event_type": member.value})
+        assert rec["event_type"] == member.value
+    with pytest.raises(ValueError, match=r"not one of the 45 closed EventType values"):
+        rl.append({"event_type": "not_a_real_event"})
+
+
 def test_max_rounds_clamped_monotone_min_fold_inv_r3(tmp_path):
     """INV-R3: appending two MAX_ROUNDS_CLAMPED events with DIFFERENT
     effective_max_rounds rebuilds to the SMALLER (monotone non-increasing). The

diff --git a/tests/pr_submit/test_codex_reviews.py b/tests/pr_submit/test_codex_reviews.py
index 37cb2ebf..bc76c9b0 100644
--- a/tests/pr_submit/test_codex_reviews.py
+++ b/tests/pr_submit/test_codex_reviews.py
@@ -438,7 +438,7 @@ def test_dedup_groups_same_line_across_reviewers(findings336):
 
 
 def test_event_enum_has_the_two_reviewer_events():
-    assert len(EventType) == 43
+    assert len(EventType) == 45
     assert {EventType.REVIEWER_ABSENT.value, EventType.REVIEWER_INCOMPLETE.value} == {
         "reviewer_absent",
         "reviewer_incomplete",

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
