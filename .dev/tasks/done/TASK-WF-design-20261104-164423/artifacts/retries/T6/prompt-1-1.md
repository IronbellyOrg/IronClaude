cdc15f9d313648ac167eafc0c76add00a95575f2
Review one task for spec compliance.

Task brief: ## Task 6: Add `expect_checks` to CI classification in `ci.py`

Implement step 5 of source section 13 in `src/superclaude/pr_submit/ci.py` per source section 6.2:

- `classify_checks(payload, *, wait_sha=None, expect_checks=False)`: unchanged body when false; when true a non-dict payload and an empty or missing chosen list return `polling`.
- `expect_checks_after_push(*, checks_seen_this_run, pre_push_evidence, base_evidence)` with the fail-closed rule of source section 6.2 item 2; module docstring sentence, token-free.
- Tests in `tests/pr_submit/test_ci_classify.py`: every new function listed in source section 12.2; existing tests at `:20-70` unmodified.

Acceptance criteria:
- Empty list with `expect_checks=True` and a matching head is `polling`; a nonempty all-pass list is `clean`; `expect_checks=False` keeps empty as `clean`; head mismatch is `polling`; non-dict payload with `expect_checks=True` is `polling`.
- `expect_checks_after_push` is false only when `checks_seen_this_run` is false and both evidence values are 0; `-1` and `None` give true.
- `uv run pytest tests/pr_submit/test_ci_classify.py tests/pr_submit/test_static_grep.py -q` passes; log saved to `./artifacts/t6-tests.log`.
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
Start sha: cdc15f9d313648ac167eafc0c76add00a95575f2
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/ci.py b/src/superclaude/pr_submit/ci.py
index 0fc23751..9f729ac4 100644
--- a/src/superclaude/pr_submit/ci.py
+++ b/src/superclaude/pr_submit/ci.py
@@ -2,6 +2,9 @@
 
 Pure: consumes an already-fetched checks payload and (optionally) failed-job
 logs. Does not import or name any version-control command tokens (NFR-6).
+With ``expect_checks`` true (set by ``expect_checks_after_push`` for a wait
+that must see at least one check), an empty, missing or unreadable check list
+stays ``polling`` instead of ``clean`` (issue #305, INV-034).
 """
 
 from __future__ import annotations
@@ -19,14 +22,20 @@ _RUN_ID = re.compile(r"/actions/runs/(\d+)")
 _HUMAN_NAME = "boundary"
 
 
-def classify_checks(payload: dict, *, wait_sha: str | None = None) -> str:
+def classify_checks(
+    payload: dict, *, wait_sha: str | None = None, expect_checks: bool = False
+) -> str:
     """Return ``polling`` / ``clean`` / ``findings``. Pure. No DetectionContract.
 
     If ``wait_sha`` is set and ``payload['head_sha']`` differs, return
     ``polling`` (PR head has not caught up to this wait).
+
+    If ``expect_checks`` is true, a non-dict payload and an empty or missing
+    check list return ``polling`` (never an early ``clean``). A nonempty list
+    classifies the same either way.
     """
     if not isinstance(payload, dict):
-        return STATE_CLEAN
+        return STATE_POLLING if expect_checks else STATE_CLEAN
     head = payload.get("head_sha")
     if wait_sha and head and head != wait_sha:
         return STATE_POLLING
@@ -34,7 +43,7 @@ def classify_checks(payload: dict, *, wait_sha: str | None = None) -> str:
     if payload.get("state") == STATE_POLLING and not checks:
         return STATE_POLLING
     if not isinstance(checks, list) or not checks:
-        return STATE_CLEAN
+        return STATE_POLLING if expect_checks else STATE_CLEAN
     buckets = {str(c.get("bucket", "")).lower() for c in checks if isinstance(c, dict)}
     states = {str(c.get("state", "")).lower() for c in checks if isinstance(c, dict)}
     if "pending" in buckets:
@@ -46,6 +55,27 @@ def classify_checks(payload: dict, *, wait_sha: str | None = None) -> str:
     return STATE_CLEAN
 
 
+def _evidence_is_zero(value: object) -> bool:
+    """True only for an int (not bool) equal to 0; anything else fails closed."""
+    return isinstance(value, int) and not isinstance(value, bool) and value == 0
+
+
+def expect_checks_after_push(
+    *,
+    checks_seen_this_run: bool,
+    pre_push_evidence: int | None,
+    base_evidence: int | None,
+) -> bool:
+    """True when the push's CI wait must see at least one check before clean.
+    Evidence values are check counts from the commit-scoped evidence read;
+    -1 (failed or unparsable read) and None count as "had checks" (fail closed)."""
+    return (
+        checks_seen_this_run is True
+        or not _evidence_is_zero(pre_push_evidence)
+        or not _evidence_is_zero(base_evidence)
+    )
+
+
 def should_arm_ci_wait(state: object) -> bool:
     """True when Wave 8 should wait on checks after this Augment terminal."""
     name = getattr(state, "value", state)
diff --git a/tests/pr_submit/test_ci_classify.py b/tests/pr_submit/test_ci_classify.py
index 3506884d..0fdc6935 100644
--- a/tests/pr_submit/test_ci_classify.py
+++ b/tests/pr_submit/test_ci_classify.py
@@ -5,6 +5,7 @@ from __future__ import annotations
 from superclaude.pr_submit.ci import (
     ci_wait_autofix,
     classify_checks,
+    expect_checks_after_push,
     findings_from_logs,
     is_human_gate,
     should_arm_ci_wait,
@@ -199,3 +200,132 @@ def test_missing_run_link_does_not_borrow_other_log():
         {"1": "tests/foo.py:12: in test_x\n"},
     )
     assert findings == []
+
+
+# issue #305 (source section 6.2): ``expect_checks`` and its setter.
+
+_HEAD = "a" * 40
+
+
+def test_expect_checks_empty_matching_head_is_polling():
+    payload = {"head_sha": _HEAD, "checks": []}
+    assert classify_checks(payload, wait_sha=_HEAD, expect_checks=True) == STATE_POLLING
+    assert classify_checks({"head_sha": _HEAD}, expect_checks=True) == STATE_POLLING
+    assert classify_checks({}, expect_checks=True) == STATE_POLLING
+
+
+def test_expect_checks_nonempty_all_pass_is_clean(load_fixture):
+    payload = {
+        "head_sha": _HEAD,
+        "checks": [{"name": "t", "bucket": "pass", "state": "COMPLETED"}],
+    }
+    assert classify_checks(payload, wait_sha=_HEAD, expect_checks=True) == STATE_CLEAN
+    fixture = load_fixture("checks-pass.json")
+    assert classify_checks(fixture, expect_checks=True) == STATE_CLEAN
+    fail = load_fixture("checks-fail.json")
+    assert classify_checks(fail, expect_checks=True) == STATE_FINDINGS
+
+
+def test_expect_checks_false_keeps_empty_clean():
+    assert classify_checks({"checks": []}, expect_checks=False) == STATE_CLEAN
+    assert classify_checks({}, expect_checks=False) == STATE_CLEAN
+    assert (
+        classify_checks(
+            {"head_sha": _HEAD, "checks": []}, wait_sha=_HEAD, expect_checks=False
+        )
+        == STATE_CLEAN
+    )
+    assert classify_checks("not a dict", expect_checks=False) == STATE_CLEAN
+
+
+def test_expect_checks_head_mismatch_is_polling():
+    payload = {
+        "head_sha": "b" * 40,
+        "checks": [{"name": "t", "bucket": "pass", "state": "COMPLETED"}],
+    }
+    assert classify_checks(payload, wait_sha=_HEAD, expect_checks=True) == STATE_POLLING
+    assert (
+        classify_checks(payload, wait_sha=_HEAD, expect_checks=False) == STATE_POLLING
+    )
+
+
+def test_expect_checks_non_dict_payload_is_polling():
+    for payload in (None, [], "x", 0):
+        assert classify_checks(payload, expect_checks=True) == STATE_POLLING
+        assert classify_checks(payload) == STATE_CLEAN
+
+
+def test_expect_checks_after_push_pre_push_evidence_one_is_true():
+    assert (
+        expect_checks_after_push(
+            checks_seen_this_run=False, pre_push_evidence=1, base_evidence=0
+        )
+        is True
+    )
+
+
+def test_expect_checks_after_push_all_zero_is_false():
+    assert (
+        expect_checks_after_push(
+            checks_seen_this_run=False, pre_push_evidence=0, base_evidence=0
+        )
+        is False
+    )
+
+
+def test_expect_checks_after_push_failed_read_is_true():
+    assert (
+        expect_checks_after_push(
+            checks_seen_this_run=False, pre_push_evidence=-1, base_evidence=0
+        )
+        is True
+    )
+    assert (
+        expect_checks_after_push(
+            checks_seen_this_run=False, pre_push_evidence=0, base_evidence=-1
+        )
+        is True
+    )
+
+
+def test_expect_checks_after_push_none_is_true():
+    assert (
+        expect_checks_after_push(
+            checks_seen_this_run=False, pre_push_evidence=None, base_evidence=0
+        )
+        is True
+    )
+    assert (
+        expect_checks_after_push(
+            checks_seen_this_run=False, pre_push_evidence=0, base_evidence=None
+        )
+        is True
+    )
+
+
+def test_expect_checks_after_push_base_evidence_two_is_true():
+    assert (
+        expect_checks_after_push(
+            checks_seen_this_run=False, pre_push_evidence=0, base_evidence=2
+        )
+        is True
+    )
+
+
+def test_expect_checks_after_push_checks_seen_this_run_is_true():
+    assert (
+        expect_checks_after_push(
+            checks_seen_this_run=True, pre_push_evidence=0, base_evidence=0
+        )
+        is True
+    )
+
+
+def test_expect_checks_after_push_non_int_evidence_fails_closed():
+    for bad in ("0", 0.0, False, True):
+        assert (
+            expect_checks_after_push(
+                checks_seen_this_run=False, pre_push_evidence=bad, base_evidence=0
+            )
+            is True
+        )
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t6-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t6-tests.log
new file mode 100644
index 00000000..d1258aa4
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t6-tests.log
@@ -0,0 +1,13 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 51 items
+
+tests/pr_submit/test_ci_classify.py ................................     [ 62%]
+tests/pr_submit/test_static_grep.py ...................                  [100%]
+
+============================== 51 passed in 0.76s ==============================

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
