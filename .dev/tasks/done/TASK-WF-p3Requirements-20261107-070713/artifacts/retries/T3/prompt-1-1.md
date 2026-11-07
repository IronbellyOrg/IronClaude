157b784ddbdae5736756fa94b2d3c61e84c9cc82
Review one task for spec compliance.

Task brief: ## Task 3: Add `late_conflict_trigger` to `conflicts.py` and export it

Satisfies: R-002, R-012 (part b).

In `src/superclaude/pr_submit/conflicts.py`, directly after `needs_probe`, add `late_conflict_trigger(payload: object, wait_sha: object = None) -> bool` exactly as R-002 of `./source.md` describes: true only for a dict payload whose `merge_state` dict yields `mergeability_hint(mergeable, status) == "conflicting"`; false for every other input, including a `wait_sha` that is a non-empty string different from a non-empty `payload["head_sha"]` (an empty or non-string `head_sha` or `wait_sha` gives no mismatch information, as in `classify_checks`); it never raises. The docstring is two sentences, cites FR-24 and FR-25, and contains no standalone `gh` or `git` word. Re-export the function in `src/superclaude/pr_submit/__init__.py` the way `mergeability_hint` and `needs_probe` are (import list and `__all__`).

Add table-driven tests to `tests/pr_submit/test_conflicts_core.py` beside the `mergeability_hint` tests: conflicting payload with checks, conflicting payload with `state: polling` and `checks: []`, conflicting payload that is otherwise `clean`, `DIRTY` status with `MERGEABLE`, lowercase values, `BEHIND`, `BLOCKED`, `CLEAN`, `UNKNOWN`, empty strings, no `merge_state` key, `merge_state` not a dict, payload `None`, a list, junk values, and `wait_sha` equal, different, empty and absent, plus a non-string `head_sha` and a non-string `wait_sha`.

Acceptance criteria (ids):
T3.AC1: `late_conflict_trigger({"head_sha": "a", "state": "polling", "checks": [], "merge_state": {"mergeable": "CONFLICTING", "status": "DIRTY"}}, wait_sha="a")` is `True`; the same call with `wait_sha="b"` is `False`; the same payload with `"MERGEABLE"`/`"CLEAN"` is `False`; a payload without `merge_state` is `False`.
T3.AC2: `uv run pytest tests/pr_submit/test_conflicts_core.py tests/pr_submit/test_static_grep.py -q` passes, including `test_tn50_core_pure_no_gh_git_tokens` and the existing router tables unchanged.
T3.AC3: `uv run ruff check src/superclaude/pr_submit/conflicts.py src/superclaude/pr_submit/__init__.py tests/pr_submit/test_conflicts_core.py` reports no findings.
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
Start sha: 157b784ddbdae5736756fa94b2d3c61e84c9cc82
Diff against the start snapshot: 
diff --git a/src/superclaude/pr_submit/__init__.py b/src/superclaude/pr_submit/__init__.py
index 78ded428..513f8be2 100644
--- a/src/superclaude/pr_submit/__init__.py
+++ b/src/superclaude/pr_submit/__init__.py
@@ -48,6 +48,7 @@ from .conflicts import (
     evaluate_sync_decision,
     finish_manifest,
     is_conflict_cycle,
+    late_conflict_trigger,
     lock_trust_findings,
     merge_commit_message,
     merge_parent_ok,
@@ -137,6 +138,7 @@ __all__ = [
     "evaluate_sync_decision",
     "finish_manifest",
     "is_conflict_cycle",
+    "late_conflict_trigger",
     "lock_trust_findings",
     "merge_commit_message",
     "merge_parent_ok",
diff --git a/src/superclaude/pr_submit/conflicts.py b/src/superclaude/pr_submit/conflicts.py
index c471f601..5849c07f 100644
--- a/src/superclaude/pr_submit/conflicts.py
+++ b/src/superclaude/pr_submit/conflicts.py
@@ -461,6 +461,30 @@ def needs_probe(hint: str) -> bool:
     return hint in ("conflicting", "unknown")
 
 
+def late_conflict_trigger(payload: object, wait_sha: object = None) -> bool:
+    """True when a CI poll payload's ``merge_state`` object reads ``"conflicting"``
+    through ``mergeability_hint``, whatever its checks say (FR-24, FR-25). A payload
+    for another head than ``wait_sha``, a missing or malformed ``merge_state`` and
+    every other hint give False; it never raises.
+    """
+    if not isinstance(payload, dict):
+        return False
+    head = payload.get("head_sha")
+    if (
+        isinstance(wait_sha, str)
+        and wait_sha
+        and isinstance(head, str)
+        and head
+        and head != wait_sha
+    ):
+        return False
+    state = payload.get("merge_state")
+    if not isinstance(state, dict):
+        return False
+    hint = mergeability_hint(state.get("mergeable"), state.get("status"))
+    return hint == "conflicting"
+
+
 # ---------------------------------------------------------------------------
 # Parsing (design section 5.3)
 # ---------------------------------------------------------------------------
diff --git a/tests/pr_submit/test_conflicts_core.py b/tests/pr_submit/test_conflicts_core.py
index 7141a73b..8f2c617b 100644
--- a/tests/pr_submit/test_conflicts_core.py
+++ b/tests/pr_submit/test_conflicts_core.py
@@ -50,6 +50,7 @@ from superclaude.pr_submit.conflicts import (
     classify_path,
     conflict_plan,
     group_entries,
+    late_conflict_trigger,
     mergeability_hint,
     needs_probe,
     parse_numstat_binary,
@@ -161,6 +162,85 @@ def test_needs_probe(hint, expected):
     assert needs_probe(hint) is expected
 
 
+# --- late_conflict_trigger (issue #361, FR-24 / FR-25) ---------------------------
+
+
+def _poll(mergeable, status, *, checks=None, state="polling", head=SHA_A):
+    return {
+        "pr": 7,
+        "head_sha": head,
+        "source": "ci",
+        "state": state,
+        "checks": [] if checks is None else checks,
+        "merge_state": {"mergeable": mergeable, "status": status},
+    }
+
+
+_PENDING_CHECK = [{"name": "ci", "state": "PENDING", "bucket": "pending"}]
+
+
+@pytest.mark.parametrize(
+    "payload, expected",
+    [
+        # conflicting, whatever the checks say
+        (_poll("CONFLICTING", "DIRTY", checks=_PENDING_CHECK), True),
+        (_poll("CONFLICTING", "DIRTY", checks=[], state="polling"), True),
+        (_poll("CONFLICTING", "DIRTY", state="clean"), True),
+        (_poll("MERGEABLE", "DIRTY"), True),
+        (_poll("conflicting", "dirty"), True),
+        # every other hint
+        (_poll("MERGEABLE", "BEHIND"), False),
+        (_poll("MERGEABLE", "BLOCKED"), False),
+        (_poll("MERGEABLE", "CLEAN"), False),
+        (_poll("UNKNOWN", "UNKNOWN"), False),
+        (_poll("", ""), False),
+        (_poll(None, None), False),
+        (_poll(7, ["DIRTY"]), False),
+        (_poll("junk", "junk"), False),
+        # malformed payloads
+        ({"state": "polling", "checks": []}, False),
+        ({"merge_state": "CONFLICTING"}, False),
+        ({"merge_state": None}, False),
+        ({"merge_state": ["CONFLICTING", "DIRTY"]}, False),
+        ({"merge_state": {}}, False),
+        (None, False),
+        ([], False),
+        ("CONFLICTING", False),
+        (7, False),
+    ],
+)
+def test_late_conflict_trigger_reads_the_merge_state_object(payload, expected):
+    assert late_conflict_trigger(payload) is expected
+
+
+@pytest.mark.parametrize(
+    "head, wait_sha, expected",
+    [
+        (SHA_A, SHA_A, True),  # same head
+        (SHA_A, SHA_B, False),  # a payload for another head is not evidence
+        (SHA_A, None, True),  # no wait sha: no mismatch information
+        (SHA_A, "", True),
+        ("", SHA_B, True),  # empty head_sha: no mismatch information
+        (None, SHA_B, True),
+        (7, SHA_B, True),  # non-string head_sha
+        (SHA_A, 7, True),  # non-string wait_sha
+        (SHA_A, ["x"], True),
+    ],
+)
+def test_late_conflict_trigger_ignores_a_payload_for_another_head(
+    head, wait_sha, expected
+):
+    payload = _poll("CONFLICTING", "DIRTY", head=head)
+    assert late_conflict_trigger(payload, wait_sha=wait_sha) is expected
+    assert late_conflict_trigger(payload, wait_sha) is expected
+
+
+def test_late_conflict_trigger_polling_with_no_checks_and_clean_merge_state():
+    """A wait stuck at polling with no checks only fires on a conflicting reading."""
+    assert late_conflict_trigger(_poll("MERGEABLE", "CLEAN", checks=[])) is False
+    assert late_conflict_trigger(_poll("CONFLICTING", "DIRTY", checks=[])) is True
+
+
 # ---------------------------------------------------------------------------
 # Parse: merge-tree stage records
 # ---------------------------------------------------------------------------

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
