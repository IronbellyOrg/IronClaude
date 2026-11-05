9115b66dfa9e61580068f1b5da9cb7ea01de4150
Review one task for spec compliance.

Task brief: ## Task 4: Generalise thread selection and activity over an identity set

Edit src/superclaude/pr_submit/classifier.py per design section 14: `_thread_findings(threads, contract, completed, identities=None)` uses the given identity set (default: the Augment identities, so Augment behaviour is unchanged), and a new `has_reviewer_activity(payload, identities)` returns whether any review or comment, or any thread root, is authored by those identities. `has_augment_activity` keeps its current result.

Acceptance criteria:
- With no `identities` argument every existing classifier test passes unchanged (`uv run pytest tests/pr_submit/test_cosmos_review.py tests/pr_submit/test_cosmos_protocol.py tests/pr_submit/test_silence.py -q -p no:cacheprovider`).
- An Augment payload that also contains Codex-rooted unresolved threads yields the same `actionable_finding_comments` result as without them.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 9115b66dfa9e61580068f1b5da9cb7ea01de4150
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/classifier.py b/src/superclaude/pr_submit/classifier.py
index 717b8abd..c551c2d5 100644
--- a/src/superclaude/pr_submit/classifier.py
+++ b/src/superclaude/pr_submit/classifier.py
@@ -52,6 +52,28 @@ def _augment_entries(entries: Any, identities: set[str]) -> list[dict]:
     return [e for e in entries if isinstance(e, dict) and _login_of(e) in identities]
 
 
+def has_reviewer_activity(payload: dict, identities: set[str]) -> bool:
+    """Whether any review, comment or review-thread root is authored by ``identities``.
+
+    Used for reviewer presence; Augment's silence path keeps
+    :func:`has_augment_activity` (reviews and comments only), unchanged.
+    """
+    if not isinstance(payload, dict) or not identities:
+        return False
+    if _augment_entries(payload.get("reviews"), identities) or _augment_entries(
+        payload.get("comments"), identities
+    ):
+        return True
+    threads = payload.get("threads")
+    for thread in threads if isinstance(threads, list) else []:
+        connection = thread.get("comments") if isinstance(thread, dict) else None
+        nodes = connection.get("nodes") if isinstance(connection, dict) else None
+        if isinstance(nodes, list) and nodes and isinstance(nodes[0], dict):
+            if _login_of(nodes[0]) in identities:
+                return True
+    return False
+
+
 def has_augment_activity(payload: dict, contract: Any) -> bool:
     """Raw review/comment activity for silence handling, independent of completion."""
     if not isinstance(payload, dict):
@@ -256,17 +278,32 @@ def _stable_id(entry: dict) -> str | int | None:
     return None
 
 
-def _thread_findings(threads: Any, contract: Any, completed: dict) -> list[dict] | None:
+def _thread_findings(
+    threads: Any,
+    contract: Any,
+    completed: dict | None,
+    identities: set[str] | None = None,
+    *,
+    completed_at: Any = None,
+) -> list[dict] | None:
     """Return roots only, or None if an unresolved source cannot be safely selected.
 
     Current-null/original-only locations stay hints. Resolution is authoritative;
     neither outdated state nor the re-trigger watermark discards an open root.
+    ``identities`` selects whose roots count (default: the Augment identities).
+    ``completed_at`` overrides the completion time otherwise read from the
+    ``completed`` review's submission time (Codex passes its marker-derived time).
     """
     if not isinstance(threads, list):
         return None
-    identities = _augment_identities(contract)
+    if identities is None:
+        identities = _augment_identities(contract)
     selected, seen_threads, seen_roots = [], set(), set()
-    completed_at = _timestamp(_submission_ts(completed))
+    if completed_at is None:
+        completed_at = (
+            _submission_ts(completed) if isinstance(completed, dict) else None
+        )
+    completed_at = _timestamp(completed_at)
     for thread in threads:
         if not isinstance(thread, dict) or type(thread.get("isResolved")) is not bool:
             return None
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t4-check.py b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t4-check.py
new file mode 100644
index 00000000..0babe3c2
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t4-check.py
@@ -0,0 +1,20 @@
+import copy, json, sys
+from superclaude.pr_submit import DetectionContract, actionable_finding_comments, classify
+from superclaude.pr_submit.classifier import has_augment_activity, has_reviewer_activity
+snap = json.load(open("tests/pr_submit/fixtures/cosmos-pr266.json"))
+c = DetectionContract(augment_bot_login="augmentcode[bot]", augment_app_slug="augmentcode")
+W = "2026-10-16T19:30:00Z"
+snap["threads"][0]["isResolved"] = False
+base = actionable_finding_comments(snap, c, watermark=W)
+cx = copy.deepcopy(snap["threads"][0]); cx["id"] = "PRRT_codex_example"
+root = cx["comments"]["nodes"][0]; root["id"] = "PRRC_codex"; root["databaseId"] = 9999999
+root["author"] = {"login": "chatgpt-codex-connector"}
+snap2 = copy.deepcopy(snap); snap2["threads"].append(cx)
+mixed = actionable_finding_comments(snap2, c, watermark=W)
+print("augment-only roots:", [r["comment_id"] for r in base], classify(snap, c, watermark=W))
+print("with codex root   :", [r["comment_id"] for r in mixed], classify(snap2, c, watermark=W))
+print("same selection    :", base == mixed)
+codex = {"chatgpt-codex-connector", "chatgpt-codex-connector[bot]"}
+print("has_reviewer_activity(codex) on mixed:", has_reviewer_activity(snap2, codex), "on augment-only:", has_reviewer_activity(snap, codex))
+print("has_augment_activity unchanged:", has_augment_activity(snap2, c) == has_augment_activity(snap, c))
+sys.exit(0 if base == mixed else 1)
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t4-check.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t4-check.log
new file mode 100644
index 00000000..661c1b96
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t4-check.log
@@ -0,0 +1,6 @@
+augment-only roots: [4296483537] findings
+with codex root   : [4296483537] findings
+same selection    : True
+has_reviewer_activity(codex) on mixed: True on augment-only: False
+has_augment_activity unchanged: True
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t4-test.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t4-test.log
new file mode 100644
index 00000000..5a6999e9
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t4-test.log
@@ -0,0 +1,54 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 647 items
+
+tests/pr_submit/test_auggie_fallback.py ............                     [  1%]
+tests/pr_submit/test_augment_review_remediation.py .......               [  2%]
+tests/pr_submit/test_autonomy_gates.py .......                           [  4%]
+tests/pr_submit/test_ci_classify.py ....................                 [  7%]
+tests/pr_submit/test_contract_setup_diagnosis.py ..............          [  9%]
+tests/pr_submit/test_contract_setup_evidence.py .....................    [ 12%]
+tests/pr_submit/test_contract_setup_pr_submit_integration.py ......      [ 13%]
+tests/pr_submit/test_contract_setup_questions.py .........               [ 14%]
+tests/pr_submit/test_contract_setup_validation.py .............          [ 16%]
+tests/pr_submit/test_contract_setup_writer.py ................           [ 19%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 24%]
+...............................................................          [ 34%]
+tests/pr_submit/test_cosmos_protocol.py ...............                  [ 36%]
+tests/pr_submit/test_cosmos_review.py .................................. [ 42%]
+........................................................................ [ 53%]
+                                                                         [ 53%]
+tests/pr_submit/test_crash_recovery.py ................                  [ 55%]
+tests/pr_submit/test_detection_contract.py ............................. [ 60%]
+.....                                                                    [ 61%]
+tests/pr_submit/test_edge_cases.py ...................                   [ 63%]
+tests/pr_submit/test_finding_verify.py ...                               [ 64%]
+tests/pr_submit/test_gate_helper_coverage.py ...........                 [ 66%]
+tests/pr_submit/test_gate_helper_differentials.py ...................... [ 69%]
+                                                                         [ 69%]
+tests/pr_submit/test_idempotency.py ......                               [ 70%]
+tests/pr_submit/test_loop_guard.py .............                         [ 72%]
+tests/pr_submit/test_monitor_arm.py ...                                  [ 72%]
+tests/pr_submit/test_pre_pr_checks.py .................................. [ 78%]
+.....                                                                    [ 78%]
+tests/pr_submit/test_rate_limit.py ....                                  [ 79%]
+tests/pr_submit/test_reply_resolve.py ..........                         [ 81%]
+tests/pr_submit/test_review_retrigger.py .......                         [ 82%]
+tests/pr_submit/test_run_log.py ............                             [ 84%]
+tests/pr_submit/test_setup_questions_resolution.py ....                  [ 84%]
+tests/pr_submit/test_severity_router.py ............................     [ 89%]
+tests/pr_submit/test_silence.py .................                        [ 91%]
+tests/pr_submit/test_skill_parse.py ..............                       [ 93%]
+tests/pr_submit/test_static_grep.py ...................                  [ 96%]
+tests/pr_submit/test_timeout.py .....                                    [ 97%]
+tests/pr_submit/test_troubleshoot_seed.py ....                           [ 98%]
+tests/pr_submit/test_validated_not_verified.py ...                       [ 98%]
+tests/pr_submit/test_validation_gate.py .........                        [100%]
+
+============================= 647 passed in 14.32s =============================
+rc=0
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
