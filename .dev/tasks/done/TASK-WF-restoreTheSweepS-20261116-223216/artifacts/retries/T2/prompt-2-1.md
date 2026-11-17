759e68baad72de784500e78afaaffe7f42fd21ee
Review one task for spec compliance.

Task brief: ## Task 2: Make parse_worker_show read agentWait presence and value, and replace the test that pinned it off

Depends on: Task 1

In `src/superclaude/cli/sweep/probes.py`, change `parse_worker_show` (the only production caller is `_run_rows`, same file; the other callers are tests in `tests/sweep/test_probes_allowlist.py`) so it sets `agent_wait` and `agent_wait_present` on the returned `OrcaObservation`. Read the key from `result.observation.agentWait` first (`_get(show, "observation")`), and fall back to `result.terminal.agentWait` (`_get(show, "terminal")`) only when the `observation` object has no `agentWait` key. `agent_wait_present` is True when the key exists in that object, even when its value is null (the existing `_get` returns None for both a missing key and a null value, so write a small helper that tests key membership in the dict). `agent_wait` is the value found (None for null). When there is no show, or neither object has the key, `agent_wait_present` stays False and `agent_wait` None. `agent_wait_since` stays unset (no captured field names a wait time); keep a short comment saying so and that the meaning of a non-null `agentWait` is UNVERIFIED. Replace the stale comment above the `return OrcaObservation(` call. In `src/superclaude/cli/sweep/models.py`, rewrite the three "Reserved: no code sets these ... DESIGN open item 6" comments on `agent_wait`, `agent_wait_present` and `agent_wait_since` (class `OrcaObservation`) to say that `agent_wait` and `agent_wait_present` are set by `parse_worker_show` from `observation.agentWait` then `terminal.agentWait`, and `agent_wait_since` is still set by nothing. In `tests/sweep/test_probes_allowlist.py`, replace `test_parse_worker_show_reads_no_agent_wait_field_until_its_names_are_captured` (near line 1639) with tests that use `_captured("captured-worker-show-running.json")["result"]`: present and null gives `agent_wait_present` True and `agent_wait` None; also `liveness_verdict` `live`, `status` `dispatched`, `outcome` `in_progress`; an observation-only key, a terminal-only key (fallback), a non-null value in `observation` (`agent_wait` equals that value and `agent_wait_present` True; build it inline and call the meaning UNVERIFIED in a comment), a show with neither key, and a non-dict `observation` all behave as described and raise nothing. Update the assertion `obs.agent_wait_present is False` in `test_a_list_row_with_no_show_keeps_the_show_only_fields_unknown` only if it no longer holds (it should still hold). Dependents that must keep working: `_run_rows` in `src/superclaude/cli/sweep/probes.py` (builds rows through `dataclasses.replace` on the result), `test_list_and_show_disagree_and_the_show_value_is_used`, `test_a_show_of_the_wrong_shape_raises_nothing`, `test_one_missing_and_one_extra_worker_show_key_raise_nothing` and the three `test_worker_show_dispatch_times_*` tests, all in `tests/sweep/test_probes_allowlist.py`.

Acceptance criteria:
T2.AC1: `parse_worker_show` on the running-worker fixture result returns `agent_wait_present` True, `agent_wait` None, `liveness_verdict` `live`, `status` `dispatched`, `outcome` `in_progress`; on `captured-worker-show-1.json` (a finished worker without an `agentWait` key) it returns `agent_wait_present` False.
T2.AC2: The fallback, non-null, missing and wrong-shape cases listed above each have a test that passes, and no call to `parse_worker_show` raises on any shape.
T2.AC3: `ALLOWED_ORCA` in `src/superclaude/cli/sweep/probes.py` is unchanged (`git diff` shows no change to that tuple) and `uv run pytest tests/sweep/test_probes_allowlist.py -q` passes.
Global constraints: 
- The sweep stays read-only: add no Orca command to `ALLOWED_ORCA` in `src/superclaude/cli/sweep/probes.py`, change nothing about what the sweep may run, and leave the git protections for INV-008 (fsmonitor off on every git call, submodules ignored, `unscanned` for a worktree where a selected filter could run) untouched.
- Edit `src/superclaude/` and `tests/` and `docs/` only; never the `.claude/` mirrors. No skill, agent, command or hook is changed, so `make sync-dev` is not needed; run `make verify-sync` once at the end of Task 5.
- What a non-null `agentWait` looks like was never captured. Code comments and docs must label its meaning UNVERIFIED and must not invent its shape. A non-null `agentWait` stays with rule 4 (`waiting_signal`, class waiting on a person) exactly as today, and is never `working`.
- `orca.status == "ready"` at `src/superclaude/cli/sweep/classify.py` (rule 4, inside `_rule_waiting_signal`) is not a mismatch: the sweep itself sets `status="ready"` on the rows it builds from `task-list --ready` in `_run_rows` (`src/superclaude/cli/sweep/probes.py`). Leave it as it is.
- The report footnote constant `SP24` ("Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred.") in `src/superclaude/cli/sweep/report.py` and `tests/sweep/test_report.py` is a wording contract pinned by tests and it is about stalled and fenced, which stay unobserved. Do not change its wording. If the evidence shows a report wording change is needed, stop and report it as an owner decision.
- Real values the code must match, from the 2026-11-16 capture of a running worker (`/home/coder/captures/q24-orca-capture2-20261116.md`): `result.dispatch.status` is `dispatched`; `result.projection.outcome` is `in_progress`; `result.projection.liveness.verdict` is `live`; `agentWait` is present with value null at `result.observation.agentWait` and at `result.terminal.agentWait`. A finished worker shows `completed`, `succeeded`, `unverifiable`.
- Do not open `/home/coder/captures/q24-orca-capture-20261116.md` (it holds other sessions' private prompt text).
- Use `uv run` for every Python command.
Start sha: 759e68baad72de784500e78afaaffe7f42fd21ee
Diff against the start snapshot: diff --git a/src/superclaude/cli/sweep/models.py b/src/superclaude/cli/sweep/models.py
index 5fb8dad94..fdab7926b 100644
--- a/src/superclaude/cli/sweep/models.py
+++ b/src/superclaude/cli/sweep/models.py
@@ -94,7 +94,9 @@ class OrcaObservation:
     liveness_verdict: str | None = None  # live, unverifiable, exited or None
     status: str | None = None
     outcome: str | None = None
-    # Reserved: no code sets these two while the agentWait lookup is off (DESIGN open item 6).
+    # Set by parse_worker_show from worker-show ``observation.agentWait``, else
+    # ``terminal.agentWait``. Captured: present and null for a running worker. A non-null
+    # value was never captured, so its meaning is UNVERIFIED (DESIGN open item 6).
     agent_wait: object | None = None
     agent_wait_present: bool = False  # null versus absent (GQ-58)
     parent: str | None = None
@@ -106,7 +108,7 @@ class OrcaObservation:
     worker_done_seen: bool | None = None
     fenced_evidence: str = "unreadable"  # present, absent or unreadable
     task_spec_text: str | None = None
-    # Reserved: the agentWait time. No code sets it while the lookup is off (DESIGN open item 6).
+    # Reserved: the agentWait time. No code sets it: no captured field names a wait time.
     agent_wait_since: datetime | None = None
 
 
diff --git a/src/superclaude/cli/sweep/probes.py b/src/superclaude/cli/sweep/probes.py
index e2c895f6f..8875b67a1 100644
--- a/src/superclaude/cli/sweep/probes.py
+++ b/src/superclaude/cli/sweep/probes.py
@@ -455,6 +455,19 @@ def _first(*values: object) -> object | None:
     return next((v for v in values if v is not None), None)
 
 
+def _agent_wait(show: object | None) -> tuple[bool, object | None]:
+    """(key present, value) of ``agentWait`` in ``observation``, else in ``terminal``.
+
+    Captured 2026-11-16 (a running worker): the key is present with value null in both
+    places. A non-null value was never captured, so its meaning is UNVERIFIED.
+    """
+    for place in ("observation", "terminal"):
+        block = _get(show, place)
+        if isinstance(block, dict) and "agentWait" in block:
+            return True, block["agentWait"]
+    return False, None
+
+
 def parse_worker_show(
     run: str, list_row: object, show: object | None
 ) -> OrcaObservation:
@@ -465,9 +478,8 @@ def parse_worker_show(
     determine (WC-10) and counts toward ``bound_reached``.
     """
     dispatch = _text(_first(_get(list_row, "dispatchId"), _get(show, "dispatch", "id")))
-    # No agentWait field is read: its live name was not captured (step 1.0a, open item 6),
-    # so ``agent_wait``, ``agent_wait_present`` and ``agent_wait_since`` keep their model
-    # defaults until a read-only capture records the names.
+    # ``agent_wait_since`` stays unset: no captured field names a wait time.
+    wait_present, wait = _agent_wait(show)
     return OrcaObservation(
         dispatch=dispatch or "",
         run=run,
@@ -478,6 +490,8 @@ def parse_worker_show(
         liveness_verdict=_text(_get(show, "projection", "liveness", "verdict")),
         status=_text(_get(show, "dispatch", "status")),
         outcome=_text(_get(show, "projection", "outcome")),
+        agent_wait=wait,
+        agent_wait_present=wait_present,
         parent=_text(
             _first(
                 _get(show, "projection", "parent"),
diff --git a/tests/sweep/test_probes_allowlist.py b/tests/sweep/test_probes_allowlist.py
index 8752c5256..c35fd59cb 100644
--- a/tests/sweep/test_probes_allowlist.py
+++ b/tests/sweep/test_probes_allowlist.py
@@ -1636,23 +1636,68 @@ def test_a_list_row_with_no_show_keeps_the_show_only_fields_unknown():
     assert obs.agent_wait_present is False
 
 
-def test_parse_worker_show_reads_no_agent_wait_field_until_its_names_are_captured():
-    # Open item 6: no live ``agentWait`` name was captured, so nothing is read from either
-    # place it might sit, and no wait time is guessed from any key (FIN-F1).
-    wait = {"since": "2026-11-08T10:00:00Z", "kind": "question"}
-    show = {
-        "dispatch": {"id": DISPATCH, "status": "dispatched"},
-        "projection": {"agentWait": wait},
-        "agentWait": wait,
-    }
+def test_a_captured_running_worker_reads_live_in_progress_and_a_null_agent_wait():
+    result = _captured("captured-worker-show-running.json")["result"]
 
-    obs = probes.parse_worker_show(RUN, {"dispatchId": DISPATCH}, show)
+    obs = probes.parse_worker_show(RUN, {"dispatchId": "ctx_6c922cf310da"}, result)
 
+    assert obs.liveness_verdict == "live"
+    assert (
+        obs.status == "dispatched"
+    )  # dispatch.status; the word in_progress is outcome
+    assert obs.outcome == "in_progress"
+    assert obs.agent_wait_present is True
     assert obs.agent_wait is None
-    assert obs.agent_wait_present is False
     assert obs.agent_wait_since is None
 
 
+def test_a_captured_finished_worker_has_no_agent_wait_key():
+    result = _captured("captured-worker-show-1.json")["result"]
+
+    obs = probes.parse_worker_show(RUN, {"dispatchId": DISPATCH}, result)
+
+    assert obs.agent_wait_present is False and obs.agent_wait is None
+
+
+def test_agent_wait_is_read_from_observation_then_terminal():
+    base = {"dispatch": {"id": DISPATCH}}
+    from_terminal = {**base, "terminal": {"agentWait": None}}
+    both = {
+        **base,
+        "observation": {"agentWait": "obs-value"},
+        "terminal": {"agentWait": "term-value"},
+    }
+    # An observation block without the key falls through to the terminal block.
+    fall_through = {
+        **base,
+        "observation": {"status": "live"},
+        "terminal": {"agentWait": None},
+    }
+
+    for show, present, value in (
+        (from_terminal, True, None),
+        (both, True, "obs-value"),  # observation wins
+        (fall_through, True, None),
+        (base, False, None),  # neither block has the key
+        ({**base, "observation": [], "terminal": "x"}, False, None),  # wrong shapes
+        ({**base, "projection": {"agentWait": "x"}, "agentWait": "x"}, False, None),
+    ):
+        obs = probes.parse_worker_show(RUN, {"dispatchId": DISPATCH}, show)
+        assert (obs.agent_wait_present, obs.agent_wait) == (present, value), show
+        assert obs.agent_wait_since is None  # no captured field names a wait time
+
+
+def test_a_non_null_agent_wait_is_kept_as_found():
+    # What a waiting worker really shows was never captured (UNVERIFIED): this dict is a
+    # made-up stand-in that only proves the value is passed through, not its meaning.
+    wait = {"since": "2026-11-08T10:00:00Z", "kind": "question"}
+    show = {"dispatch": {"id": DISPATCH}, "observation": {"agentWait": wait}}
+
+    obs = probes.parse_worker_show(RUN, {"dispatchId": DISPATCH}, show)
+
+    assert obs.agent_wait == wait and obs.agent_wait_present is True
+
+
 def test_one_missing_and_one_extra_worker_show_key_raise_nothing():
     list_row = {"dispatchId": DISPATCH}
     result = _captured("captured-worker-show-1.json")["result"]

Codegraph context: index_state fresh (checked 2026-11-16T22:34:54Z); call codegraph only when index_state: fresh, never to widen scope. Dependents not in the diff: _run_rows (src/superclaude/cli/sweep/probes.py) calls parse_worker_show and then uses dataclasses.replace on the result; it is unchanged. Test run after the change: uv run pytest tests/sweep -q gives 639 passed; uv run ruff check src/superclaude/cli/sweep tests/sweep passes. ALLOWED_ORCA in probes.py is not in the diff.
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
