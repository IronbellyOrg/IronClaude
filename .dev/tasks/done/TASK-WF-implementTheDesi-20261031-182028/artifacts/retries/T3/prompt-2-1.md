910485d71f37a7bb7cff4f4b65ffaa9c07e5b3cf
Review one task for spec compliance.

Task brief: ## Task 3: Fold re-trigger count by cycle and rebuild absent reviewers

Depends on: Task 1

Edit src/superclaude/pr_submit/run_log.py `rebuild_state` per design sections 5 and 12: `rereview_request_count` counts distinct `cycle_id` values of `rereview_requested` events (an event without `cycle_id` counts once each), and a new `absent_reviewers` sorted list is folded from `reviewer_absent` events' `reviewer` field.

Acceptance criteria:
- Two `rereview_requested` events with the same `cycle_id` and different `reviewer` rebuild to `rereview_request_count == 1`; two events without `cycle_id` rebuild to 2.
- A `reviewer_absent{reviewer:"codex"}` event rebuilds to `absent_reviewers == ["codex"]`.
- Existing tests in tests/pr_submit/test_run_log.py, test_review_retrigger.py and test_crash_recovery.py pass.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 910485d71f37a7bb7cff4f4b65ffaa9c07e5b3cf
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/run_log.py b/src/superclaude/pr_submit/run_log.py
index e46bef15..8d7208ad 100644
--- a/src/superclaude/pr_submit/run_log.py
+++ b/src/superclaude/pr_submit/run_log.py
@@ -164,6 +164,13 @@ class RunLog:
         Reconstructs the FSM state, ``round_counter``, the 7 idempotency sets, and
         ``push_count``/``reply_count`` from the event stream. This is the source of
         truth on any snapshot/JSONL disagreement.
+
+        ``rereview_request_count`` counts re-triggered push cycles: one cycle may
+        post an Augment and a Codex re-trigger comment, so ``rereview_requested``
+        events are folded by distinct ``cycle_id`` (an event without ``cycle_id``
+        still counts once each, so old logs rebuild to the same number).
+        ``absent_reviewers`` is the sorted set of reviewers named by
+        ``reviewer_absent`` events.
         """
         state = {
             "pr_number": self.pr_number,
@@ -176,10 +183,13 @@ class RunLog:
             "rereview_request_count": 0,
             "effective_max_rounds": None,
             "silence_rerequested_at": None,
+            "absent_reviewers": [],
             "last_event_id": 0,
             **{s: [] for s in IDEMPOTENCY_SETS},
         }
         sets = {s: set() for s in IDEMPOTENCY_SETS}
+        retriggered_cycles: set = set()
+        absent: set = set()
         for ev in self.read_events():
             state["last_event_id"] = ev.get("event_id", state["last_event_id"])
             et = ev.get("event_type")
@@ -188,8 +198,14 @@ class RunLog:
             if et == EventType.ROUND_INCREMENTED.value:
                 state["round_counter"] += 1
             elif et == EventType.REREVIEW_REQUESTED.value:
-                # IDIOM A (count fold) — INV-R1 monotone re-trigger count.
-                state["rereview_request_count"] += 1
+                # IDIOM A (count fold) — INV-R1 monotone re-trigger count, by cycle.
+                cycle_id = ev.get("cycle_id")
+                if cycle_id is None or cycle_id not in retriggered_cycles:
+                    state["rereview_request_count"] += 1
+                if cycle_id is not None:
+                    retriggered_cycles.add(cycle_id)
+            elif et == EventType.REVIEWER_ABSENT.value and ev.get("reviewer"):
+                absent.add(ev["reviewer"])
             elif (
                 et == EventType.AUGGIE_FALLBACK_INVOKED.value
                 and ev.get("pr_number") is not None
@@ -240,6 +256,7 @@ class RunLog:
                 sets["processed_finding_ids"].add(ev["fix_key"])
         for s in IDEMPOTENCY_SETS:
             state[s] = sorted(sets[s], key=str)
+        state["absent_reviewers"] = sorted(absent)
         return state
 
     def materialize_snapshot(self) -> dict:
diff --git a/tests/pr_submit/test_run_log.py b/tests/pr_submit/test_run_log.py
index cee142de..e5271f48 100644
--- a/tests/pr_submit/test_run_log.py
+++ b/tests/pr_submit/test_run_log.py
@@ -225,3 +225,26 @@ def test_rereview_count_and_auggie_set_folds(tmp_path):
     state = rl.rebuild_state()
     assert state["rereview_request_count"] == 2
     assert state["auggie_review_invoked"] == [99]
+
+
+def test_rereview_count_folds_by_distinct_cycle_across_reviewers(tmp_path):
+    """One push cycle that re-triggers Augment and Codex counts once (INV-R1)."""
+    rl = RunLog(100, tmp_path)
+    for reviewer in ("augment", "codex"):
+        rl.append(
+            {
+                "event_type": EventType.REREVIEW_REQUESTED.value,
+                "cycle_id": "c1",
+                "reviewer": reviewer,
+            }
+        )
+    assert rl.rebuild_state()["rereview_request_count"] == 1
+
+
+def test_absent_reviewers_fold_is_a_set_and_seeded_empty(tmp_path):
+    """reviewer_absent folds into a sorted set; a log without it rebuilds to []."""
+    rl = RunLog(101, tmp_path)
+    assert rl.rebuild_state()["absent_reviewers"] == []
+    rl.append({"event_type": EventType.REVIEWER_ABSENT.value, "reviewer": "codex"})
+    rl.append({"event_type": EventType.REVIEWER_ABSENT.value, "reviewer": "codex"})
+    assert rl.rebuild_state()["absent_reviewers"] == ["codex"]
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/src/superclaude/pr_submit/run_log.py b/src/superclaude/pr_submit/run_log.py
index 05664c98..8d7208ad 100644
--- a/src/superclaude/pr_submit/run_log.py
+++ b/src/superclaude/pr_submit/run_log.py
@@ -170,9 +170,7 @@ class RunLog:
         events are folded by distinct ``cycle_id`` (an event without ``cycle_id``
         still counts once each, so old logs rebuild to the same number).
         ``absent_reviewers`` is the sorted set of reviewers named by
-        ``reviewer_absent`` events; ``rereview_watermarks`` maps each reviewer to
-        the ``cycle_id`` and ``watermark`` of its latest ``rereview_requested``
-        event that carried a watermark (a missing ``reviewer`` means augment).
+        ``reviewer_absent`` events.
         """
         state = {
             "pr_number": self.pr_number,
@@ -186,7 +184,6 @@ class RunLog:
             "effective_max_rounds": None,
             "silence_rerequested_at": None,
             "absent_reviewers": [],
-            "rereview_watermarks": {},
             "last_event_id": 0,
             **{s: [] for s in IDEMPOTENCY_SETS},
         }
@@ -207,11 +204,6 @@ class RunLog:
                     state["rereview_request_count"] += 1
                 if cycle_id is not None:
                     retriggered_cycles.add(cycle_id)
-                if ev.get("watermark") is not None:
-                    state["rereview_watermarks"][ev.get("reviewer") or "augment"] = {
-                        "cycle_id": cycle_id,
-                        "watermark": ev["watermark"],
-                    }
             elif et == EventType.REVIEWER_ABSENT.value and ev.get("reviewer"):
                 absent.add(ev["reviewer"])
             elif (
diff --git a/tests/pr_submit/test_run_log.py b/tests/pr_submit/test_run_log.py
index d110ab46..e5271f48 100644
--- a/tests/pr_submit/test_run_log.py
+++ b/tests/pr_submit/test_run_log.py
@@ -230,22 +230,15 @@ def test_rereview_count_and_auggie_set_folds(tmp_path):
 def test_rereview_count_folds_by_distinct_cycle_across_reviewers(tmp_path):
     """One push cycle that re-triggers Augment and Codex counts once (INV-R1)."""
     rl = RunLog(100, tmp_path)
-    for reviewer, watermark in (
-        ("augment", "2026-10-31T10:00:01Z"),
-        ("codex", "2026-10-31T10:00:05Z"),
-    ):
+    for reviewer in ("augment", "codex"):
         rl.append(
             {
                 "event_type": EventType.REREVIEW_REQUESTED.value,
                 "cycle_id": "c1",
                 "reviewer": reviewer,
-                "watermark": watermark,
             }
         )
-    state = rl.rebuild_state()
-    assert state["rereview_request_count"] == 1
-    assert set(state["rereview_watermarks"]) == {"augment", "codex"}
-    assert state["rereview_watermarks"]["codex"]["cycle_id"] == "c1"
+    assert rl.rebuild_state()["rereview_request_count"] == 1
 
 
 def test_absent_reviewers_fold_is_a_set_and_seeded_empty(tmp_path):
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/pr_submit/run_log.py:189 anchor="The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe." chk=n,n,n,y family=unspecified-state-key fix=Remove the rereview_watermarks seed, fold, docstring sentence and test assertions first=A1 origin=new: rebuild_state gains a rereview_watermarks key the design does not describe
Saved-probe re-check hit locations (may be empty): (no hits)

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
