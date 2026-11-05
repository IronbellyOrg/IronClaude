e8571b3e2f3c899687413d38acf2445b8e8aca00
Review one task for spec compliance.

Task brief: ## Task 2: Add the two conflict-cycle run-log events (41 to 43)

Implement step 2 of source section 13 per source sections 6.5 and 12.2:

- `src/superclaude/pr_submit/models.py`: add `SYNC_STARTED = "sync_started"` and `SYNC_CONCLUDED = "sync_concluded"` after `REVIEWER_INCOMPLETE` with the comment line from source section 6.5; update the module docstring (`:3-7`) and the class docstring (`:23-33`) from 41 to 43 members.
- `src/superclaude/pr_submit/run_log.py:111`: docstring "one of the 41 closed" becomes "one of the 43 closed".
- `src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md:86-99`: heading, "EXACTLY 43 members" sentence and the event list per source section 8.6 items 1 and 2 (token-free).
- `tests/pr_submit/test_run_log.py:165-169`: rename the test, update its docstring and both asserts to 43, add the two value asserts (source section 12.2).
- `tests/pr_submit/test_codex_reviews.py:441`: `== 41` becomes `== 43`.

Acceptance criteria:
- `len(EventType) == 43` and `EventType.SYNC_STARTED.value == "sync_started"`, `EventType.SYNC_CONCLUDED.value == "sync_concluded"`.
- `grep -rn '\b41\b' src/superclaude/pr_submit tests/pr_submit src/superclaude/skills/sc-pr-submit-protocol` shows no event-count hit (the PR-number literal in `test_run_log.py` `RunLog(41, ...)` excepted); output saved to `./artifacts/t2-grep.txt`.
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_static_grep.py -q` passes.
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
Start sha: e8571b3e2f3c899687413d38acf2445b8e8aca00
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/models.py b/src/superclaude/pr_submit/models.py
index 358d5f12..515b1c3b 100644
--- a/src/superclaude/pr_submit/models.py
+++ b/src/superclaude/pr_submit/models.py
@@ -1,10 +1,11 @@
 """Canonical data models for the ``sc:pr-submit`` deterministic core.
 
-Defines the closed run-log event enum (exactly 41 members — the 32 from spec
+Defines the closed run-log event enum (exactly 43 members — the 32 from spec
 §11.3 plus ``push_aborted_or_not_landed`` from §12.1, plus the 4 V1.1
 re-review/fallback events from addendum §6.1, plus ``silence_rerequested`` and
 ``terminal_augment_no_response``, plus the reviewer events ``reviewer_absent``
-and ``reviewer_incomplete``), the severity tiers, the
+and ``reviewer_incomplete``, plus the two conflict-cycle events
+``sync_started`` and ``sync_concluded``), the severity tiers, the
 single-FSM state lexicon (spec §5.1; Python identifiers drop the spec's prime, so
 ``S4'_HALT_BEFORE_PUSH`` becomes ``S4_HALT_BEFORE_PUSH``), and the ``Finding`` /
 ``SkillResult`` dataclasses the test bodies assert against.
@@ -20,7 +21,7 @@ from enum import Enum
 
 
 class EventType(str, Enum):
-    """Closed enum of run-log event types — EXACTLY 41 members.
+    """Closed enum of run-log event types — EXACTLY 43 members.
 
     The 32 event types listed in spec §11.3 (merged-spec.md:724-731) PLUS
     ``push_aborted_or_not_landed`` (spec §12.1 line 771 — the crash-window
@@ -30,7 +31,8 @@ class EventType(str, Enum):
     ``silence_rerequested`` (INV-S1) and ``terminal_augment_no_response`` PLUS
     the two reviewer events ``reviewer_absent`` (a reviewer with no activity is
     ignored for the rest of the run) and ``reviewer_incomplete`` (a present
-    reviewer did not complete within ``--timeout``).
+    reviewer did not complete within ``--timeout``) PLUS the two conflict-cycle
+    events ``sync_started`` and ``sync_concluded`` (issue #305, both tiers).
     The run-log writer validates every appended event against this closed set;
     an event outside it is a programming error.
     """
@@ -88,6 +90,9 @@ class EventType(str, Enum):
     # --- reviewer presence (Augment + Codex) — the 40th-41st ---
     REVIEWER_ABSENT = "reviewer_absent"
     REVIEWER_INCOMPLETE = "reviewer_incomplete"
+    # --- merge-conflict cycles (issue #305), both tiers - the 42nd-43rd ---
+    SYNC_STARTED = "sync_started"
+    SYNC_CONCLUDED = "sync_concluded"
 
 
 class Severity(str, Enum):
diff --git a/src/superclaude/pr_submit/run_log.py b/src/superclaude/pr_submit/run_log.py
index 8d7208ad..5f143c44 100644
--- a/src/superclaude/pr_submit/run_log.py
+++ b/src/superclaude/pr_submit/run_log.py
@@ -108,7 +108,7 @@ class RunLog:
     def append(self, event: dict) -> dict:
         """Append a validated, redacted event with a monotonic ``event_id`` and fsync.
 
-        Raises :class:`ValueError` if ``event_type`` is not one of the 41 closed
+        Raises :class:`ValueError` if ``event_type`` is not one of the 43 closed
         enum values (the run-log writer validates against ``models.EventType``).
         """
         event_type = event.get("event_type")
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
index 28ca23a1..8d5759d8 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md
@@ -83,14 +83,14 @@ preceded by a **write-ahead** record fsynced BEFORE the side effect.
 Default `<output-dir>` = `<repo-root>/.dev/pr-monitor/pr-<N>-<YYYYMMDDHHMMSS>/` (cwd-relative; the
 repo the operator runs `sc:pr-submit` from) unless `--resume` supplies an existing log dir.
 
-### The 41 event types (§11.3 + §12.1 + V1.1 §6.1 + silence + reviewers)
+### The 43 event types (§11.3 + §12.1 + V1.1 §6.1 + silence + reviewers + conflict cycles)
 
-The closed `EventType` enum has EXACTLY 41 members — the 32 from §11.3 plus
+The closed `EventType` enum has EXACTLY 43 members — the 32 from §11.3 plus
 `push_aborted_or_not_landed` (§12.1, the crash-window not-landed branch) — the 33 prior — plus the 4
 V1.1 re-review/fallback events (`rereview_requested`, `decline_detected`, `auggie_fallback_invoked`,
 `max_rounds_clamped`; addendum §6.1), the 2 silence events (`silence_rerequested`,
-`terminal_augment_no_response`) and the 2 reviewer events (`reviewer_absent`,
-`reviewer_incomplete`):
+`terminal_augment_no_response`), the 2 reviewer events (`reviewer_absent`,
+`reviewer_incomplete`) and the 2 conflict-cycle events (`sync_started`, `sync_concluded`):
 `run_started`, `environment_check`, `pr_create_attempted`, `pr_created`, `monitor_armed`,
 `baseline_captured`, `poll_attempt`, `poll_result`, `api_backoff`, `classifier_unknown_shape`,
 `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`,
@@ -100,7 +100,7 @@ V1.1 re-review/fallback events (`rereview_requested`, `decline_detected`, `auggi
 `terminal_timeout`, `terminal_max_rounds`, `terminal_halted`, `terminal_failed`,
 `push_aborted_or_not_landed`, `rereview_requested`, `decline_detected`, `auggie_fallback_invoked`,
 `max_rounds_clamped`, `silence_rerequested`, `terminal_augment_no_response`, `reviewer_absent`,
-`reviewer_incomplete`.
+`reviewer_incomplete`, `sync_started`, `sync_concluded`.
 
 Each line carries `schema_version`, a unique+monotonic `event_id`, `event_type`, `timestamp`,
 `run_id`, `pr{repo,number,url,base,head}`, `state_before`, `state_after`,
diff --git a/tests/pr_submit/test_run_log.py b/tests/pr_submit/test_run_log.py
index e5271f48..022bbf42 100644
--- a/tests/pr_submit/test_run_log.py
+++ b/tests/pr_submit/test_run_log.py
@@ -162,11 +162,13 @@ def test_rebuild_from_jsonl_is_authoritative(tmp_path):
 # --- V1.1 closed-enum count + new-event folds (addendum §6.1/§6.3) ------------
 
 
-def test_eventtype_is_41_members_with_silence_and_reviewer_events():
-    """The closed EventType enum has EXACTLY 41 members, including INV-S1 and the
-    two reviewer-presence events."""
-    assert len(EventType) == 41
-    assert len(list(EventType)) == 41
+def test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events():
+    """The closed EventType enum has EXACTLY 43 members, including INV-S1, the two
+    reviewer-presence events and the two conflict-cycle events."""
+    assert len(EventType) == 43
+    assert len(list(EventType)) == 43
+    assert EventType.SYNC_STARTED.value == "sync_started"
+    assert EventType.SYNC_CONCLUDED.value == "sync_concluded"
     assert EventType.REVIEWER_ABSENT.value == "reviewer_absent"
     assert EventType.REVIEWER_INCOMPLETE.value == "reviewer_incomplete"
     assert EventType.REREVIEW_REQUESTED.value == "rereview_requested"
diff --git a/tests/pr_submit/test_codex_reviews.py b/tests/pr_submit/test_codex_reviews.py
index 0c94973d..37cb2ebf 100644
--- a/tests/pr_submit/test_codex_reviews.py
+++ b/tests/pr_submit/test_codex_reviews.py
@@ -438,7 +438,7 @@ def test_dedup_groups_same_line_across_reviewers(findings336):
 
 
 def test_event_enum_has_the_two_reviewer_events():
-    assert len(EventType) == 41
+    assert len(EventType) == 43
     assert {EventType.REVIEWER_ABSENT.value, EventType.REVIEWER_INCOMPLETE.value} == {
         "reviewer_absent",
         "reviewer_incomplete",
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t2-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t2-tests.log
new file mode 100644
index 00000000..db6c4e45
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t2-tests.log
@@ -0,0 +1,15 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 91 items
+
+tests/pr_submit/test_run_log.py ............                             [ 13%]
+tests/pr_submit/test_codex_reviews.py .................................. [ 50%]
+..........................                                               [ 79%]
+tests/pr_submit/test_static_grep.py ...................                  [100%]
+
+============================== 91 passed in 0.86s ==============================
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t2-grep.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t2-grep.txt
new file mode 100644
index 00000000..12d4b278
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t2-grep.txt
@@ -0,0 +1,9 @@
+tests/pr_submit/fixtures/codex-findings-pr336.json:438:      "originalLine": 41,
+tests/pr_submit/fixtures/codex-findings-pr336.json:449:            "originalLine": 41,
+tests/pr_submit/fixtures/codex-findings-pr336.json:534:      "originalLine": 41,
+tests/pr_submit/fixtures/codex-findings-pr336.json:545:            "originalLine": 41,
+tests/pr_submit/fixtures/codex-findings-pr336.json:825:      "original_line": 41,
+tests/pr_submit/fixtures/codex-findings-pr336.json:828:      "original_position": 41,
+tests/pr_submit/fixtures/finding-max.json:405:      "line": 41,
+tests/pr_submit/fixtures/finding-max.json:416:      "body": "Issue 41 in module 41.",
+tests/pr_submit/test_run_log.py:206:    rl = RunLog(41, tmp_path)

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
