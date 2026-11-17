a0631eddb02483330971ea8b8975b77010ddb517
Review one task for spec compliance.

Task brief: ## Task 4: Add an end-to-end sweep test that a captured running worker is reported as working

Depends on: Task 1, Task 2, Task 3

In `tests/sweep/test_cli_contract.py`, add a test next to `test_waiting_lists_hold_row_ids_only` (near line 1085) that uses the same `env` fixture and `_canned(env, RUN, workers=[...], shows={dispatch: <running fixture result>}, ...)` helper and `_ps(env)` the neighbouring tests use (Read them first for exact signatures) to run the sweep over one worker whose `worker-show` is `_captured("captured-worker-show-running.json")["result"]` (its `dispatch.id` is `ctx_6c922cf310da`; set the worker-list row's `dispatchId` and `dispatchStatus` `dispatched` to match). Assert from the JSON output that the row's class is `working` and the Working section of the Markdown report lists it, and add the same run with a finished worker fixture (`captured-worker-show-1.json`) to show it is not `working`. Update the comment near line 1095 ("the live agentWait field is not read in Phase 1 (open item 6)") because it is no longer true. If the running fixture's `terminal.worktreePath` or other joined fields make the row land under `could not determine` for an unrelated reason (for example the join to a transcript), assert only what the sweep reports for the Orca row and say why in a comment; do not weaken any existing assertion. The worker-show command stays the one already in the allow list: assert the recorded argv list contains no template outside `ALLOWED_ORCA`.

Acceptance criteria:
T4.AC1: The new test passes and fails if `_rule_working` is changed back to `return None` (confirm once by temporarily reverting locally, then restore; do not commit the revert).
T4.AC2: `uv run pytest tests/sweep/test_cli_contract.py tests/sweep/test_readonly.py tests/sweep/test_probes_allowlist.py -q` passes.
T4.AC3: No existing assertion in the three files is removed or loosened except the stale comment.
Global constraints: 
- The sweep stays read-only: add no Orca command to `ALLOWED_ORCA` in `src/superclaude/cli/sweep/probes.py`, change nothing about what the sweep may run, and leave the git protections for INV-008 (fsmonitor off on every git call, submodules ignored, `unscanned` for a worktree where a selected filter could run) untouched.
- Edit `src/superclaude/` and `tests/` and `docs/` only; never the `.claude/` mirrors. No skill, agent, command or hook is changed, so `make sync-dev` is not needed; run `make verify-sync` once at the end of Task 5.
- What a non-null `agentWait` looks like was never captured. Code comments and docs must label its meaning UNVERIFIED and must not invent its shape. A non-null `agentWait` stays with rule 4 (`waiting_signal`, class waiting on a person) exactly as today, and is never `working`.
- `orca.status == "ready"` at `src/superclaude/cli/sweep/classify.py` (rule 4, inside `_rule_waiting_signal`) is not a mismatch: the sweep itself sets `status="ready"` on the rows it builds from `task-list --ready` in `_run_rows` (`src/superclaude/cli/sweep/probes.py`). Leave it as it is.
- The report footnote constant `SP24` ("Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred.") in `src/superclaude/cli/sweep/report.py` and `tests/sweep/test_report.py` is a wording contract pinned by tests and it is about stalled and fenced, which stay unobserved. Do not change its wording. If the evidence shows a report wording change is needed, stop and report it as an owner decision.
- Real values the code must match, from the 2026-11-16 capture of a running worker (`/home/coder/captures/q24-orca-capture2-20261116.md`): `result.dispatch.status` is `dispatched`; `result.projection.outcome` is `in_progress`; `result.projection.liveness.verdict` is `live`; `agentWait` is present with value null at `result.observation.agentWait` and at `result.terminal.agentWait`. A finished worker shows `completed`, `succeeded`, `unverifiable`.
- Do not open `/home/coder/captures/q24-orca-capture-20261116.md` (it holds other sessions' private prompt text).
- Use `uv run` for every Python command.
Start sha: a0631eddb02483330971ea8b8975b77010ddb517
Diff against the start snapshot: diff --git a/tests/sweep/test_cli_contract.py b/tests/sweep/test_cli_contract.py
index b564aa78d..4d6960ef2 100644
--- a/tests/sweep/test_cli_contract.py
+++ b/tests/sweep/test_cli_contract.py
@@ -1091,8 +1091,8 @@ def test_waiting_lists_hold_row_ids_only(env):
         "workerState": "running",
         "dispatchStatus": "dispatched",
     }
-    # Waiting (a) comes from a blocked contract the Task names (rule 1): the live
-    # agentWait field is not read in Phase 1 (open item 6).
+    # Waiting (a) comes from a blocked contract the Task names (rule 1). This worker's
+    # show has no agentWait key, so rule 4's agentWait signal does not apply.
     contract = env.sweep_root.contract(worker_status="blocked", reason="needs a person")
     _canned(
         env,
@@ -1115,6 +1115,48 @@ def test_waiting_lists_hold_row_ids_only(env):
     assert payload["summary"]["counts"]["waiting on a person"] == 2
 
 
+def _single_worker_world(env, show_name: str) -> str:
+    """One captured worker (its real worker-show) in an otherwise empty Run."""
+    show = _captured(show_name)["result"]
+    dispatch = show["dispatch"]["id"]
+    worker = {
+        "dispatchId": dispatch,
+        "taskId": show["dispatch"]["taskId"],
+        "runId": RUN,
+        "dispatchStatus": show["dispatch"]["status"],
+    }
+    _canned(env, RUN, workers=[worker], shows={dispatch: show})
+    _ps(env)
+    return f"orca:{dispatch}"
+
+
+def test_a_captured_running_worker_is_reported_as_working(env):
+    row_id = _single_worker_world(env, "captured-worker-show-running.json")
+
+    payload = _payload(_run(env, "--run", RUN))
+
+    row = _row(payload, row_id)
+    assert (row["class"], row["rule"]) == ("working", "working")
+    assert payload["summary"]["counts"]["working"] == 1
+    text = Path(payload["report_path"]).read_text("utf-8")
+    assert row_id in _section(text, "## Sessions (1/1)")
+    # The sweep read the worker through the allowed worker-show call; nothing new was run.
+    asked = [c["args"] for c in env.orca.calls]
+    assert _worker_show(row_id.removeprefix("orca:")) in asked
+    # check_orca_argv raises ValueError unless the argv matches an ALLOWED_ORCA template.
+    for args in asked:
+        probes.check_orca_argv(args)
+
+
+def test_a_captured_finished_worker_is_not_reported_as_working(env):
+    row_id = _single_worker_world(env, "captured-worker-show-1.json")
+
+    payload = _payload(_run(env, "--run", RUN))
+
+    assert _row(payload, row_id)["class"] != "working"
+    assert payload["summary"]["counts"]["working"] == 0
+
+
 # =========================================================================================
 # FR-017: report names, two runs with one injected now, earlier reports untouched
 # =========================================================================================

Codegraph context: index_state fresh (checked 2026-11-16T22:34:54Z); call codegraph only when index_state: fresh, never to widen scope. No production file changed in this task. Test run after the change: uv run pytest tests/sweep -q gives 649 passed; uv run ruff check src/superclaude/cli/sweep tests/sweep passes. With _rule_working's code replaced by a function returning None (in-process patch, no file edit), test_a_captured_running_worker_is_reported_as_working fails; with probes.check_orca_argv patched to raise, the same test fails too.
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/tests/sweep/test_cli_contract.py b/tests/sweep/test_cli_contract.py
index 2177d2206..4d6960ef2 100644
--- a/tests/sweep/test_cli_contract.py
+++ b/tests/sweep/test_cli_contract.py
@@ -1143,12 +1143,9 @@ def test_a_captured_running_worker_is_reported_as_working(env):
     # The sweep read the worker through the allowed worker-show call; nothing new was run.
     asked = [c["args"] for c in env.orca.calls]
     assert _worker_show(row_id.removeprefix("orca:")) in asked
-    assert {a[:2] for a in asked} <= {
-        ("orchestration", "worker-list"),
-        ("orchestration", "worker-show"),
-        ("orchestration", "task-list"),
-        ("worktree", "ps"),
-    }
+    # check_orca_argv raises ValueError unless the argv matches an ALLOWED_ORCA template.
+    for args in asked:
+        probes.check_orca_argv(args)
 
 
 def test_a_captured_finished_worker_is_not_reported_as_working(env):
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=tests/sweep/test_cli_contract.py:1142-1148 anchor="assert the recorded argv list contains no template outside ALLOWED_ORCA" chk=n,n,n,y family=allowlist-assert fix=check each recorded argv with probes.check_orca_argv first=start origin=new: the test checks only that the first two tokens are one of four verbs; a worktree ps --agent-wait call would still pass
Saved-probe re-check hit locations (may be empty): tests/sweep/test_cli_contract.py:328:    lists = [a for a in _orca_calls(env) if a[:2] == ("orchestration", "worker-list")]
tests/sweep/test_cli_contract.py:350:    lists = [a for a in proc.argv() if a[:2] == ("orchestration", "worker-list")]

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
