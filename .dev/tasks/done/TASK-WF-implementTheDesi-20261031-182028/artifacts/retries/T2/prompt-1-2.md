642270fb4c3b0a3d3d6d757fca5aeb06c50b6197
Review one task for spec compliance.

Task brief: ## Task 2: Add the Codex fields to the detection contract

Edit src/superclaude/pr_submit/detection.py and the YAML block in src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md per design section 14: `codex_bot_login` (shipped "chatgpt-codex-connector[bot]"), `codex_app_slug` (shipped "chatgpt-codex-connector"), `codex_retrigger_phrase` (default "@codex review"). `from_yaml` trims the identities like the Augment ones. Direct `DetectionContract()` construction keeps both Codex identities empty (fail-safe, same as Augment), while the shipped ref supplies the real values.

Acceptance criteria:
- `DetectionContract.load()` returns the two Codex identities and the "@codex review" phrase; `DetectionContract()` has empty Codex identities.
- A local override YAML without Codex fields still loads (Codex identities empty, so Codex is disabled for that override) and existing tests in tests/pr_submit/test_detection_contract.py pass.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 642270fb4c3b0a3d3d6d757fca5aeb06c50b6197
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/detection.py b/src/superclaude/pr_submit/detection.py
index 3f1ae628..5a923b93 100644
--- a/src/superclaude/pr_submit/detection.py
+++ b/src/superclaude/pr_submit/detection.py
@@ -43,7 +43,9 @@ _LOCAL_OVERRIDE_PATH: Path | None = None
 # Shipped Codex (ChatGPT Codex Connector) identity and re-trigger phrase. A YAML
 # contract that OMITS a Codex key falls back to these values (an override written
 # by contract setup has no Codex keys and must not switch Codex off); an explicit
-# empty or null value disables Codex. Direct ``DetectionContract()`` construction
+# empty or null value blanks that one identity. Codex is disabled only when both
+# Codex identities are blank; it stays on while either remains. Direct
+# ``DetectionContract()`` construction
 # keeps both identities empty (fail-safe, like Augment).
 _SHIPPED_CODEX_BOT_LOGIN = "chatgpt-codex-connector[bot]"
 _SHIPPED_CODEX_APP_SLUG = "chatgpt-codex-connector"
@@ -146,7 +148,9 @@ class DetectionContract:
         """Build a contract from YAML, trimming identity padding (no lock enforcement).
 
         Codex keys use key-presence semantics: an absent key falls back to the
-        shipped Codex value; a present empty or null value disables Codex.
+        shipped Codex value; a present empty or null value blanks that identity.
+        Codex is disabled only when both Codex identities are blank; it stays on
+        while either remains.
         """
         data = data.copy()
         for key, shipped in (
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t2r-lint.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t2r-lint.log
new file mode 100644
index 00000000..632ad637
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t2r-lint.log
@@ -0,0 +1,3 @@
+All checks passed!
+1 file already formatted
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t2r-test.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t2r-test.log
new file mode 100644
index 00000000..83455d33
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t2r-test.log
@@ -0,0 +1,56 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 705 items
+
+tests/pr_submit/test_auggie_fallback.py ............                     [  1%]
+tests/pr_submit/test_augment_review_remediation.py .......               [  2%]
+tests/pr_submit/test_autonomy_gates.py .......                           [  3%]
+tests/pr_submit/test_ci_classify.py ....................                 [  6%]
+tests/pr_submit/test_codex_reviews.py .................................. [ 11%]
+........................                                                 [ 14%]
+tests/pr_submit/test_contract_setup_diagnosis.py ..............          [ 16%]
+tests/pr_submit/test_contract_setup_evidence.py .....................    [ 19%]
+tests/pr_submit/test_contract_setup_pr_submit_integration.py ......      [ 20%]
+tests/pr_submit/test_contract_setup_questions.py .........               [ 21%]
+tests/pr_submit/test_contract_setup_validation.py .............          [ 23%]
+tests/pr_submit/test_contract_setup_writer.py ................           [ 25%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 31%]
+...............................................................          [ 40%]
+tests/pr_submit/test_cosmos_protocol.py ...............                  [ 42%]
+tests/pr_submit/test_cosmos_review.py .................................. [ 46%]
+........................................................................ [ 57%]
+                                                                         [ 57%]
+tests/pr_submit/test_crash_recovery.py ................                  [ 59%]
+tests/pr_submit/test_detection_contract.py ............................. [ 63%]
+.....                                                                    [ 64%]
+tests/pr_submit/test_edge_cases.py ...................                   [ 66%]
+tests/pr_submit/test_finding_verify.py ...                               [ 67%]
+tests/pr_submit/test_gate_helper_coverage.py ...........                 [ 68%]
+tests/pr_submit/test_gate_helper_differentials.py ...................... [ 72%]
+                                                                         [ 72%]
+tests/pr_submit/test_idempotency.py ......                               [ 72%]
+tests/pr_submit/test_loop_guard.py .............                         [ 74%]
+tests/pr_submit/test_monitor_arm.py ...                                  [ 75%]
+tests/pr_submit/test_pre_pr_checks.py .................................. [ 80%]
+.....                                                                    [ 80%]
+tests/pr_submit/test_rate_limit.py ....                                  [ 81%]
+tests/pr_submit/test_reply_resolve.py ..........                         [ 82%]
+tests/pr_submit/test_review_retrigger.py .......                         [ 83%]
+tests/pr_submit/test_run_log.py ............                             [ 85%]
+tests/pr_submit/test_setup_questions_resolution.py ....                  [ 85%]
+tests/pr_submit/test_severity_router.py ............................     [ 89%]
+tests/pr_submit/test_silence.py .................                        [ 92%]
+tests/pr_submit/test_skill_parse.py ..............                       [ 94%]
+tests/pr_submit/test_static_grep.py ...................                  [ 97%]
+tests/pr_submit/test_timeout.py .....                                    [ 97%]
+tests/pr_submit/test_troubleshoot_seed.py ....                           [ 98%]
+tests/pr_submit/test_validated_not_verified.py ...                       [ 98%]
+tests/pr_submit/test_validation_gate.py .........                        [100%]
+
+============================= 705 passed in 14.72s =============================
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t2r-grep.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t2r-grep.log
new file mode 100644
index 00000000..906ec40b
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t2r-grep.log
@@ -0,0 +1,4 @@
+$ grep -n -i "disable" src/superclaude/pr_submit/detection.py
+46:# empty or null value blanks that one identity. Codex is disabled only when both
+141:    # from_yaml supply the real values. An empty identity set disables Codex.
+152:        Codex is disabled only when both Codex identities are blank; it stays on
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
