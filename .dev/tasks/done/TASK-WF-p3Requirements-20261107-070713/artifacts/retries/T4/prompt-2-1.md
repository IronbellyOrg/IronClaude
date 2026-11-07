bc1400fa3ea604d9a68598157baf459e648ad1ff
Review one task for spec compliance.

Task brief: ## Task 4: Guard the classifier against the new payload key

Depends on: Task 3

Satisfies: R-003, R-005 (no router change), R-012 (part c).

Add tests only; no source change, and no router row (`_WAVE8A_ROWS` at lines 929 to 1044 of `tests/pr_submit/test_conflicts_core.py` already pins every outcome of R-005).

- In `tests/pr_submit/test_ci_classify.py` add the R-003 payload-shape tests: a payload that carries `merge_state` classifies exactly like the same payload without it for pending, all-pass, fail, empty with `expect_checks` true and false, and a stale head, and `state: polling` with no checks stays `polling` when `merge_state` is conflicting. Say in a docstring that these are regression guards (they pass on today's code).

Acceptance criteria (ids):
T4.AC1: `uv run pytest tests/pr_submit/test_ci_classify.py tests/pr_submit/test_conflicts_core.py -q` passes with every pre-existing test in both files unchanged and no tuple added to `_WAVE8A_ROWS`.
T4.AC2: Mutation check by hand: in a scratch copy where `classify_checks` returns `polling` whenever the payload's `merge_state` is conflicting, at least one of the new tests fails (the copy is not kept).
Global constraints: 
- Edit canonical sources under `src/superclaude/` only, then run `make sync-dev`; the `.claude/` mirrors are generated and are never staged.
- Use `uv run ...` for every Python and pytest call; no bare `python` or `pip`.
- `src/superclaude/pr_submit/fsm.py`, `run_log.py`, `models.py` and `ci.py` are not edited, no new `EventType` is added and every existing push-safety rule stays as it is (R-003, R-004).
- `src/superclaude/pr_submit/conflicts.py` and `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` are in the core-pure file set of `tests/pr_submit/test_static_grep.py`: neither may contain the standalone words `gh` or `git` on any line, comments and docstrings included.
- Several tests pin exact lines of the files this plan edits: `tests/skills/test_worker_contract.py` (an inventory keyed by exact file line, with a stale-entry check), `tests/pr_submit/test_conflict_sync_protocol.py` (fragments E1 to E13, order pins) and `tests/pr_submit/test_static_grep.py`. Each task that changes a pinned line updates the pin in the same task. The router outcomes any prose describes are the table in R-005 of `./source.md`, which `_WAVE8A_ROWS` in `tests/pr_submit/test_conflicts_core.py` already pins, so no router row is added anywhere in this plan.
- Every new prose deliverable gets its own positive assertion scoped to that text (R-012 part d), so that removing only that text fails exactly that assertion.
- Non-goal: the go/no-go gate of the issue (one real run where the base moved, or a maintainer waiver) is a release sign-off item and stays open (R-014). Nothing in this plan runs against a real PR.
- Non-goal: `.dev/brainstorms/issue-305-pr-submit-conflict-resolution/merged-requirements.md` and `.dev/designs/issue-305-pr-submit-conflict-resolution/DESIGN.md` are historical records and are not edited.
- Owner authorization (2026-11-07, relayed by the coordinator): after the third advisory review left two word-level blocking findings (the "unconditional" end-of-wait re-read in R-010 and Task 7, and the over-general status bullet in R-005), the owner allowed word edits to `./source.md` and this plan, with the listed minor guardrails, and no fourth review. The corrections are in R-005, R-010, Task 7 and the guardrails of Tasks 1, 2, 6, 7, 9 and 10; the report is `.dev/reflect/pre-TASK-WF-p3Requirements-20261107-070713-20261107070932/REPORT.md`.
Start sha: bc1400fa3ea604d9a68598157baf459e648ad1ff
Diff against the start snapshot: 
diff --git a/tests/pr_submit/test_ci_classify.py b/tests/pr_submit/test_ci_classify.py
index 0fdc6935..6645ac09 100644
--- a/tests/pr_submit/test_ci_classify.py
+++ b/tests/pr_submit/test_ci_classify.py
@@ -2,6 +2,8 @@
 
 from __future__ import annotations
 
+import pytest
+
 from superclaude.pr_submit.ci import (
     ci_wait_autofix,
     classify_checks,
@@ -329,3 +331,65 @@ def test_expect_checks_after_push_non_int_evidence_fails_closed():
             )
             is True
         )
+
+
+# issue #361 (FR-25): the CI poll payload also carries ``merge_state``. These tests
+# are regression guards: they pass on today's code because ``classify_checks`` never
+# reads that key, and they fail if a later change makes it read it.
+
+_CONFLICTING_STATE = {"mergeable": "CONFLICTING", "status": "DIRTY"}
+_PASS_CHECK = {"name": "t", "bucket": "pass", "state": "COMPLETED"}
+_PENDING_CHECK = {"name": "t", "bucket": "pending", "state": "PENDING"}
+_FAIL_CHECK = {"name": "t", "bucket": "fail", "state": "COMPLETED"}
+
+_PAYLOAD_SHAPES = {
+    "pending": {"head_sha": _HEAD, "checks": [_PENDING_CHECK]},
+    "all-pass": {"head_sha": _HEAD, "checks": [_PASS_CHECK]},
+    "fail": {"head_sha": _HEAD, "checks": [_FAIL_CHECK]},
+    "empty": {"head_sha": _HEAD, "checks": []},
+    "empty-polling": {"head_sha": _HEAD, "state": "polling", "checks": []},
+}
+_CLASSIFY_KWARGS = {
+    "default": {},
+    "expect-checks-true": {"expect_checks": True},
+    "expect-checks-false": {"expect_checks": False},
+    "matching-wait-sha": {"wait_sha": _HEAD},
+    "stale-head": {"wait_sha": "b" * 40},
+}
+_MERGE_STATES = [
+    _CONFLICTING_STATE,
+    {"mergeable": "MERGEABLE", "status": "CLEAN"},
+    {"mergeable": "", "status": ""},
+    "junk",
+    None,
+]
+
+
+@pytest.mark.parametrize("merge_state", _MERGE_STATES)
+@pytest.mark.parametrize("kwargs", _CLASSIFY_KWARGS.values(), ids=_CLASSIFY_KWARGS)
+@pytest.mark.parametrize("payload", _PAYLOAD_SHAPES.values(), ids=_PAYLOAD_SHAPES)
+def test_classify_ignores_the_merge_state_key(payload, kwargs, merge_state):
+    """Regression guard (passes on today's code): ``merge_state`` never changes the
+    classification of a payload."""
+    assert classify_checks(
+        {**payload, "merge_state": merge_state}, **kwargs
+    ) == classify_checks(payload, **kwargs)
+
+
+def test_classify_polling_with_no_checks_stays_polling_when_conflicting():
+    """Regression guard (passes on today's code): the late trigger is not the
+    classifier's job, so a conflicting wait with no checks stays ``polling``."""
+    payload = {"state": "polling", "checks": [], "merge_state": _CONFLICTING_STATE}
+    assert classify_checks(payload) == STATE_POLLING
+    assert classify_checks(payload, expect_checks=True) == STATE_POLLING
+
+
+def test_classify_merge_state_conflicting_does_not_turn_clean_checks_into_findings():
+    """Regression guard (passes on today's code): clean checks stay clean."""
+    payload = {
+        "head_sha": _HEAD,
+        "checks": [_PASS_CHECK],
+        "merge_state": _CONFLICTING_STATE,
+    }
+    assert classify_checks(payload, wait_sha=_HEAD) == STATE_CLEAN
+

Delta diff from the previous reviewed tree (empty on the first review): 
diff --git a/tests/pr_submit/test_ci_classify.py b/tests/pr_submit/test_ci_classify.py
index ff10c8b0..6645ac09 100644
--- a/tests/pr_submit/test_ci_classify.py
+++ b/tests/pr_submit/test_ci_classify.py
@@ -369,18 +369,23 @@ _MERGE_STATES = [
 @pytest.mark.parametrize("kwargs", _CLASSIFY_KWARGS.values(), ids=_CLASSIFY_KWARGS)
 @pytest.mark.parametrize("payload", _PAYLOAD_SHAPES.values(), ids=_PAYLOAD_SHAPES)
 def test_classify_ignores_the_merge_state_key(payload, kwargs, merge_state):
+    """Regression guard (passes on today's code): ``merge_state`` never changes the
+    classification of a payload."""
     assert classify_checks(
         {**payload, "merge_state": merge_state}, **kwargs
     ) == classify_checks(payload, **kwargs)
 
 
 def test_classify_polling_with_no_checks_stays_polling_when_conflicting():
+    """Regression guard (passes on today's code): the late trigger is not the
+    classifier's job, so a conflicting wait with no checks stays ``polling``."""
     payload = {"state": "polling", "checks": [], "merge_state": _CONFLICTING_STATE}
     assert classify_checks(payload) == STATE_POLLING
     assert classify_checks(payload, expect_checks=True) == STATE_POLLING
 
 
 def test_classify_merge_state_conflicting_does_not_turn_clean_checks_into_findings():
+    """Regression guard (passes on today's code): clean checks stay clean."""
     payload = {
         "head_sha": _HEAD,
         "checks": [_PASS_CHECK],

Earlier blocking findings of this start (empty on the first review): 
F1.1 sev=blocking trigger=B4 ac=T4.AC1 at=tests/pr_submit/test_ci_classify.py:336 anchor="Say in a docstring that these are regression guards (they pass on today's code)." chk=amiss:n,false:n,harm:n,constraint:y family=T4-guard-docstring fix=move the regression-guard sentence into a docstring covers="Say in a docstring that these are regression guards" first=A1 origin=new: the regression-guard statement is a comment block at lines 336-338, not a docstring
Saved-probe re-check hit locations (may be empty): 
337:# are regression guards: they pass on today's code because ``classify_checks`` never

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
