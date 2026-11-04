b5338e12e2042f476b347241e6ef0425b4df03e0
Review one task for spec compliance.

Task brief: ## Task 9: Export the conflict core from the package

Depends on: Task 5, Task 6

Edit `src/superclaude/pr_submit/__init__.py` per source section 6.6: the docstring clause naming `conflicts`, the `from .conflicts import (...)` block with every listed name, `should_retrigger` added to the existing `fsm` import, and an `__all__` group `# merge conflicts (issue #305)` with the same names. `ci.py` exports are not changed by this task.

Acceptance criteria:
- `uv run python -c "from superclaude.pr_submit import conflict_action, should_retrigger, merge_parent_ok, prior_conflict_cycles"` exits 0.
- Every name in the new `__all__` group resolves; no import cycle (`conflicts` imports `fsm` and `models`; `fsm`, `models`, `run_log`, `ci` never import `conflicts`).
- `uv run pytest tests/pr_submit -q` passes; log saved to `./artifacts/t9-tests.log`.
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
Start sha: b5338e12e2042f476b347241e6ef0425b4df03e0
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/__init__.py b/src/superclaude/pr_submit/__init__.py
index 2108230d..81f42438 100644
--- a/src/superclaude/pr_submit/__init__.py
+++ b/src/superclaude/pr_submit/__init__.py
@@ -7,8 +7,9 @@ markdown orchestrator and bash glue defer to: the finite state machine
 (:mod:`~superclaude.pr_submit.loop_guard`), the three-state detection classifier
 (:mod:`~superclaude.pr_submit.classifier` / :mod:`~superclaude.pr_submit.detection`),
 the write-ahead JSONL run-log (:mod:`~superclaude.pr_submit.run_log`), the
-crash-window recovery (:mod:`~superclaude.pr_submit.recovery`), and the shared
-data models (:mod:`~superclaude.pr_submit.models`).
+crash-window recovery (:mod:`~superclaude.pr_submit.recovery`), the merge-conflict
+core (:mod:`~superclaude.pr_submit.conflicts`, issue #305), and the shared data
+models (:mod:`~superclaude.pr_submit.models`).
 
 NFR-6 core purity: the modules in this package contain ZERO ``gh``/``git`` tokens.
 All ``gh``/``git`` I/O lives in the skill's bash scripts and the SKILL.md VAL
@@ -27,8 +28,43 @@ from .classifier import (
     is_decline,
     poll_succeeded,
 )
+from .conflicts import (
+    MECHANICAL_RULES,
+    SYNC_CAP,
+    TIER2_MAX_FILES,
+    ConflictAction,
+    ConflictPlan,
+    MechanicalRule,
+    ResumePlan,
+    SyncDecision,
+    conflict_action,
+    conflict_cycle_id,
+    conflict_plan,
+    conflict_resume_plan,
+    conflict_validation_status,
+    crash_resume_plan,
+    evaluate_sync_decision,
+    finish_manifest,
+    is_conflict_cycle,
+    merge_commit_message,
+    merge_parent_ok,
+    merge_preflight_ok,
+    mergeability_hint,
+    needs_probe,
+    parse_resolution_record,
+    prior_conflict_cycles,
+    resolution_record_ok,
+    sync_fail_state,
+)
 from .detection import DetectionContract, DetectionContractLocked, poll_augment_review
-from .fsm import RunConfig, evaluate_push_decision, parse_args, run_skill, transition
+from .fsm import (
+    RunConfig,
+    evaluate_push_decision,
+    parse_args,
+    run_skill,
+    should_retrigger,
+    transition,
+)
 from .models import (
     EventType,
     Finding,
@@ -78,6 +114,34 @@ __all__ = [
     "parse_args",
     "evaluate_push_decision",
     "RunConfig",
+    # merge conflicts (issue #305)
+    "MECHANICAL_RULES",
+    "SYNC_CAP",
+    "TIER2_MAX_FILES",
+    "ConflictAction",
+    "ConflictPlan",
+    "MechanicalRule",
+    "ResumePlan",
+    "SyncDecision",
+    "conflict_action",
+    "conflict_cycle_id",
+    "conflict_plan",
+    "conflict_resume_plan",
+    "conflict_validation_status",
+    "crash_resume_plan",
+    "evaluate_sync_decision",
+    "finish_manifest",
+    "is_conflict_cycle",
+    "merge_commit_message",
+    "merge_parent_ok",
+    "merge_preflight_ok",
+    "mergeability_hint",
+    "needs_probe",
+    "parse_resolution_record",
+    "prior_conflict_cycles",
+    "resolution_record_ok",
+    "should_retrigger",
+    "sync_fail_state",
     # reviewers (Augment + Codex)
     "REVIEWERS",
     "reviewer_identities",
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-import.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-import.txt
new file mode 100644
index 00000000..d5cdd1bc
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-import.txt
@@ -0,0 +1,2 @@
+$ PYTHONDONTWRITEBYTECODE=1 uv run python -c "from superclaude.pr_submit import conflict_action, should_retrigger, merge_parent_ok, prior_conflict_cycles"
+exit=0
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-exports.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-exports.txt
new file mode 100644
index 00000000..24c81aa7
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-exports.txt
@@ -0,0 +1,16 @@
+## __all__ group 'merge conflicts (issue #305)' resolution
+group_names 27 ['MECHANICAL_RULES', 'SYNC_CAP', 'TIER2_MAX_FILES', 'ConflictAction', 'ConflictPlan', 'MechanicalRule', 'ResumePlan', 'SyncDecision', 'conflict_action', 'conflict_cycle_id', 'conflict_plan', 'conflict_resume_plan', 'conflict_validation_status', 'crash_resume_plan', 'evaluate_sync_decision', 'finish_manifest', 'is_conflict_cycle', 'merge_commit_message', 'merge_parent_ok', 'merge_preflight_ok', 'mergeability_hint', 'needs_probe', 'parse_resolution_record', 'prior_conflict_cycles', 'resolution_record_ok', 'should_retrigger', 'sync_fail_state']
+missing []
+all_names_unique True
+all_resolve True
+exit=0
+
+## no module among fsm, models, run_log, ci imports conflicts (expect no match)
+grep_exit=1 (1 = no import found)
+
+## conflicts.py imports
+24:import base64
+25:import re
+26:from dataclasses import dataclass
+28:from .fsm import run_validation_gates
+29:from .models import MonitorState
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-tests.log
new file mode 100644
index 00000000..0b9fcd63
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t9-tests.log
@@ -0,0 +1,68 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 1566 items
+
+tests/pr_submit/test_auggie_fallback.py ............                     [  0%]
+tests/pr_submit/test_augment_review_remediation.py .......               [  1%]
+tests/pr_submit/test_autonomy_gates.py ........                          [  1%]
+tests/pr_submit/test_ci_classify.py ................................     [  3%]
+tests/pr_submit/test_codex_reviews.py .................................. [  5%]
+..........................                                               [  7%]
+tests/pr_submit/test_conflicts_core.py ................................. [  9%]
+........................................................................ [ 14%]
+........................................................................ [ 18%]
+........................................................................ [ 23%]
+........................................................................ [ 28%]
+........................................................................ [ 32%]
+........................................................................ [ 37%]
+........................................................................ [ 41%]
+........................................................................ [ 46%]
+........................................................................ [ 51%]
+........................................................................ [ 55%]
+..................                                                       [ 56%]
+tests/pr_submit/test_contract_setup_diagnosis.py ..............          [ 57%]
+tests/pr_submit/test_contract_setup_evidence.py .....................    [ 59%]
+tests/pr_submit/test_contract_setup_pr_submit_integration.py ......      [ 59%]
+tests/pr_submit/test_contract_setup_questions.py .........               [ 60%]
+tests/pr_submit/test_contract_setup_validation.py .............          [ 60%]
+tests/pr_submit/test_contract_setup_writer.py ................           [ 61%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 64%]
+...............................................................          [ 68%]
+tests/pr_submit/test_cosmos_protocol.py ...............                  [ 69%]
+tests/pr_submit/test_cosmos_review.py .................................. [ 71%]
+........................................................................ [ 75%]
+....                                                                     [ 76%]
+tests/pr_submit/test_crash_recovery.py ................................. [ 78%]
+.................................                                        [ 80%]
+tests/pr_submit/test_detection_contract.py ............................. [ 82%]
+.....                                                                    [ 82%]
+tests/pr_submit/test_edge_cases.py ...................                   [ 83%]
+tests/pr_submit/test_finding_verify.py ...                               [ 83%]
+tests/pr_submit/test_gate_helper_coverage.py ...........                 [ 84%]
+tests/pr_submit/test_gate_helper_differentials.py ...................... [ 86%]
+                                                                         [ 86%]
+tests/pr_submit/test_idempotency.py ......                               [ 86%]
+tests/pr_submit/test_loop_guard.py ................                      [ 87%]
+tests/pr_submit/test_monitor_arm.py ...                                  [ 87%]
+tests/pr_submit/test_pre_pr_checks.py .................................. [ 89%]
+.....                                                                    [ 90%]
+tests/pr_submit/test_rate_limit.py ....                                  [ 90%]
+tests/pr_submit/test_reply_resolve.py ..........                         [ 91%]
+tests/pr_submit/test_review_retrigger.py .......                         [ 91%]
+tests/pr_submit/test_run_log.py .............................            [ 93%]
+tests/pr_submit/test_setup_questions_resolution.py ....                  [ 93%]
+tests/pr_submit/test_severity_router.py ............................     [ 95%]
+tests/pr_submit/test_silence.py .................                        [ 96%]
+tests/pr_submit/test_skill_parse.py ...............                      [ 97%]
+tests/pr_submit/test_static_grep.py ...................                  [ 98%]
+tests/pr_submit/test_timeout.py .....                                    [ 98%]
+tests/pr_submit/test_troubleshoot_seed.py ....                           [ 99%]
+tests/pr_submit/test_validated_not_verified.py ...                       [ 99%]
+tests/pr_submit/test_validation_gate.py .........                        [100%]
+
+============================ 1566 passed in 17.30s =============================

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
