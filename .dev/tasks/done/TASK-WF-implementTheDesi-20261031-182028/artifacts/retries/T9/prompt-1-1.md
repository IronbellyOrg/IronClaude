8fe1a29925986053372788566b05bd1969bf2edc
Review one task for spec compliance.

Task brief: ## Task 9: Add cross-reviewer dedup, pending re-triggers and package exports

Depends on: Task 1, Task 6

Add to src/superclaude/pr_submit/reviewers.py per design sections 9 and 12: `dedup_groups(findings)` (group by path and `line`, falling back to `original_line` when `line` is None, input order kept, every finding kept) and `pending_retriggers(events, cycle_id, present)` (present reviewers without a `rereview_requested` event for that `cycle_id`; an event without `reviewer` counts as augment). Export the public reviewers functions and `has_reviewer_activity` from src/superclaude/pr_submit/__init__.py.

Acceptance criteria:
- Augment and Codex findings on the same path and line form one group of two; different lines form separate groups; a null `line` groups by `original_line`.
- After a log holding only `rereview_requested{cycle_id:"c1", reviewer:"augment"}`, `pending_retriggers(events, "c1", ["augment","codex"]) == ["codex"]`.
- `from superclaude.pr_submit import merge_wait, classify_codex, dedup_groups` works.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 8fe1a29925986053372788566b05bd1969bf2edc
Diff against the start snapshot: --- a/src/superclaude/pr_submit/reviewers.py
+++ b/src/superclaude/pr_submit/reviewers.py
@@ -35,6 +35,7 @@
     has_augment_activity,
     has_reviewer_activity,
 )
+from .models import EventType
 from .severity_router import finding_from_comment, remap_severity
 
 REVIEWERS = ("augment", "codex")
@@ -403,3 +404,36 @@
     else:
         result["outcome"] = "timeout"
     return result
+
+
+# --- cross-reviewer dedup and re-trigger bookkeeping (design sections 9 and 12) ---
+
+
+def dedup_groups(findings: list) -> list[list]:
+    """Group findings by ``(path, line)``, using ``original_line`` when ``line`` is None.
+
+    Input order is kept and every finding is kept: a group of two means Augment and
+    Codex (or two findings) flagged the same place; each keeps its own verdict.
+    """
+    groups: dict[tuple, list] = {}
+    for finding in findings:
+        line = finding.line if finding.line is not None else finding.original_line
+        groups.setdefault((finding.path, line), []).append(finding)
+    return list(groups.values())
+
+
+def pending_retriggers(
+    events: list[dict], cycle_id: Any, present: list[str]
+) -> list[str]:
+    """Present reviewers with no ``rereview_requested`` for ``cycle_id`` yet.
+
+    An event without ``reviewer`` counts as augment (logs written before Codex).
+    """
+    posted = {
+        ev.get("reviewer") or "augment"
+        for ev in events
+        if isinstance(ev, dict)
+        and ev.get("event_type") == EventType.REREVIEW_REQUESTED.value
+        and ev.get("cycle_id") == cycle_id
+    }
+    return [name for name in present if name not in posted]
diff --git a/src/superclaude/pr_submit/__init__.py b/src/superclaude/pr_submit/__init__.py
index f9545afa..2108230d 100644
--- a/src/superclaude/pr_submit/__init__.py
+++ b/src/superclaude/pr_submit/__init__.py
@@ -23,6 +23,7 @@ from .classifier import (
     actionable_finding_comments,
     classify,
     has_augment_activity,
+    has_reviewer_activity,
     is_decline,
     poll_succeeded,
 )
@@ -36,6 +37,23 @@ from .models import (
     Severity,
     SkillResult,
 )
+from .reviewers import (
+    REVIEWERS,
+    augment_wait_outcome,
+    classify_codex,
+    codex_finding_comments,
+    codex_review_state,
+    codex_severity_hint,
+    codex_wait_outcome,
+    dedup_groups,
+    list_review_threads,
+    merge_wait,
+    parse_codex_priority,
+    pending_retriggers,
+    retrigger_phrase,
+    reviewer_activity,
+    reviewer_identities,
+)
 from .severity_router import finding_from_comment, remap_severity, route
 
 # NOTE: ``load_fixture`` lives in ``tests/pr_submit/conftest.py`` (Phase 10) per the
@@ -48,6 +66,7 @@ __all__ = [
     "actionable_finding_comments",
     "is_decline",
     "has_augment_activity",
+    "has_reviewer_activity",
     "poll_succeeded",
     "STATE_DECLINED",
     "poll_augment_review",
@@ -59,6 +78,22 @@ __all__ = [
     "parse_args",
     "evaluate_push_decision",
     "RunConfig",
+    # reviewers (Augment + Codex)
+    "REVIEWERS",
+    "reviewer_identities",
+    "retrigger_phrase",
+    "reviewer_activity",
+    "parse_codex_priority",
+    "codex_severity_hint",
+    "codex_review_state",
+    "classify_codex",
+    "codex_finding_comments",
+    "list_review_threads",
+    "augment_wait_outcome",
+    "codex_wait_outcome",
+    "merge_wait",
+    "dedup_groups",
+    "pending_retriggers",
     # severity routing
     "finding_from_comment",
     "remap_severity",
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t9-check.py b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t9-check.py
new file mode 100644
index 00000000..7ba47fa4
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t9-check.py
@@ -0,0 +1,34 @@
+"""T9 check: dedup_groups, pending_retriggers and package exports."""
+import sys
+
+from superclaude.pr_submit import classify_codex, dedup_groups, merge_wait  # noqa: F401
+from superclaude.pr_submit.models import Finding
+from superclaude.pr_submit.reviewers import pending_retriggers
+
+ok = []
+
+
+def check(name, got, want):
+    ok.append(got == want)
+    print(f"{'PASS' if got == want else 'FAIL'} {name}: got={got!r} want={want!r}")
+
+
+aug = Finding(path="a.md", line=41, body="staged changes", reviewer="augment")
+cdx = Finding(path="a.md", line=41, body="staged changes too", reviewer="codex")
+other = Finding(path="a.md", line=48, body="fallback", reviewer="codex")
+outdated = Finding(path="a.md", line=None, original_line=63, body="edge", reviewer="codex")
+same63 = Finding(path="a.md", line=63, body="edge", reviewer="augment")
+groups = dedup_groups([aug, other, cdx, outdated, same63])
+check("Augment+Codex same path/line -> one group of two", [len(g) for g in groups], [2, 1, 2])
+check("group members keep their reviewers", [f.reviewer for f in groups[0]], ["augment", "codex"])
+check("different lines -> separate groups", groups[1] == [other], True)
+check("null line groups by original_line", groups[2] == [outdated, same63], True)
+check("every finding kept", sum(len(g) for g in groups), 5)
+check("empty input -> no groups", dedup_groups([]), [])
+events = [{"event_type": "rereview_requested", "cycle_id": "c1", "reviewer": "augment"}]
+check("augment posted, codex missing", pending_retriggers(events, "c1", ["augment", "codex"]), ["codex"])
+check("reviewer-less event counts as augment", pending_retriggers([{"event_type": "rereview_requested", "cycle_id": "c1"}], "c1", ["augment", "codex"]), ["codex"])
+check("other cycle does not count", pending_retriggers(events, "c2", ["augment", "codex"]), ["augment", "codex"])
+check("no present reviewers -> nothing to post", pending_retriggers(events, "c1", []), [])
+print("imports ok:", merge_wait.__name__, classify_codex.__name__, dedup_groups.__name__)
+sys.exit(0 if all(ok) else 1)
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t9-check.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t9-check.log
new file mode 100644
index 00000000..a347467e
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t9-check.log
@@ -0,0 +1,12 @@
+PASS Augment+Codex same path/line -> one group of two: got=[2, 1, 2] want=[2, 1, 2]
+PASS group members keep their reviewers: got=['augment', 'codex'] want=['augment', 'codex']
+PASS different lines -> separate groups: got=True want=True
+PASS null line groups by original_line: got=True want=True
+PASS every finding kept: got=5 want=5
+PASS empty input -> no groups: got=[] want=[]
+PASS augment posted, codex missing: got=['codex'] want=['codex']
+PASS reviewer-less event counts as augment: got=['codex'] want=['codex']
+PASS other cycle does not count: got=['augment', 'codex'] want=['augment', 'codex']
+PASS no present reviewers -> nothing to post: got=[] want=[]
+imports ok: merge_wait classify_codex dedup_groups
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t9-test.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t9-test.log
new file mode 100644
index 00000000..6c0c3f09
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t9-test.log
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
+============================= 647 passed in 14.43s =============================
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
