6306c0a7658751c80c75e062e737fca48b58c5fd
Review one task for spec compliance.

Task brief: ## Task 3: Rewrite rule 5 (_rule_working) with the real names and update the classify tests

Depends on: Task 2

In `src/superclaude/cli/sweep/classify.py`, replace the body and comment of `_rule_working` (registered as `Rule("working", _rule_working)` in `RULES`, the only reference besides the module itself) so it returns a `working` classification with rule name `working` only when all four hold on `row.orca`: `liveness_verdict == "live"`, `outcome == "in_progress"` (the `projection.outcome` field; not `status`, which holds `dispatch.status` and is `dispatched` for a running worker), `agent_wait_present is True`, `agent_wait is None`. Use the same `_classification(...)` helper the neighbouring rules use; its evidence text states the four observed values in the style of the other rules (for example "liveness_verdict live, outcome in_progress, agentWait present and null"). A row with a non-null `agent_wait` never reaches here as working because `_rule_waiting_signal` (rule 4) runs first and returns waiting on a person; keep that order. The comment must state that a non-null `agentWait` was never captured and its meaning is UNVERIFIED. Do not change `orca.status == "ready"` in `_rule_waiting_signal`. Class name constant: `C_WORKING` if it exists in `classify.py` or `models.py`; otherwise use the string `working` the way the other rules use their constants (Read the file first). In `tests/sweep/test_classify.py`: in `_rule_cases` (near line 278) change `live_unwaiting` to `outcome="in_progress"` with `status="dispatched"` and make the `working` case expect class `working`, rule `working`, no waiting kind; in `test_rule_case_per_rule_1_to_9` delete the `matched = "fallback" if rule == "working"` special case; in `test_every_class_name_but_working_is_reached` (near line 376) expect every name in `CLASSES` and rename the test; replace `test_rule_5_never_matches_while_the_agent_wait_names_are_uncaptured` (near line 436) with tests that the four-condition row is `working` and that breaking each condition one at a time is not `working` (liveness `unverifiable` and `exited`, outcome `succeeded` and `None`, `agent_wait_present` False, a non-null `agent_wait` gives rule `waiting_signal`); add a test that `status="in_progress"` with `outcome=None` is not `working` (this pins the correction of the old field name). Check every other test in the file that builds `liveness_verdict="live"` with `status="in_progress"` or `outcome="in_progress"` (near lines 524, 537, 642, 660, 1065) and fix those whose expected class changes because rule 5 now matches. Dependents of `classify` to keep working: `src/superclaude/cli/sweep/report.py` (reads the class and `agent_wait` through `_age`), `tests/sweep/test_report.py` (builds classified rows directly, so it is expected to need no change) and `tests/sweep/test_cli_contract.py`.

Acceptance criteria:
T3.AC1: `classify` returns class `working`, rule `working` for an observation with `liveness_verdict="live"`, `outcome="in_progress"`, `agent_wait_present=True`, `agent_wait=None`, and returns something else for each single broken condition; a non-null `agent_wait` with the other three true gives rule `waiting_signal`.
T3.AC2: `git diff` shows `if orca is not None and orca.status == "ready":` in `src/superclaude/cli/sweep/classify.py` unchanged.
T3.AC3: `uv run pytest tests/sweep/test_classify.py tests/sweep/test_report.py -q` passes, and no test in `tests/sweep/test_classify.py` still says rule 5 is inert, open item 6 or "no row is working in Phase 1".
Global constraints: 
- The sweep stays read-only: add no Orca command to `ALLOWED_ORCA` in `src/superclaude/cli/sweep/probes.py`, change nothing about what the sweep may run, and leave the git protections for INV-008 (fsmonitor off on every git call, submodules ignored, `unscanned` for a worktree where a selected filter could run) untouched.
- Edit `src/superclaude/` and `tests/` and `docs/` only; never the `.claude/` mirrors. No skill, agent, command or hook is changed, so `make sync-dev` is not needed; run `make verify-sync` once at the end of Task 5.
- What a non-null `agentWait` looks like was never captured. Code comments and docs must label its meaning UNVERIFIED and must not invent its shape. A non-null `agentWait` stays with rule 4 (`waiting_signal`, class waiting on a person) exactly as today, and is never `working`.
- `orca.status == "ready"` at `src/superclaude/cli/sweep/classify.py` (rule 4, inside `_rule_waiting_signal`) is not a mismatch: the sweep itself sets `status="ready"` on the rows it builds from `task-list --ready` in `_run_rows` (`src/superclaude/cli/sweep/probes.py`). Leave it as it is.
- The report footnote constant `SP24` ("Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred.") in `src/superclaude/cli/sweep/report.py` and `tests/sweep/test_report.py` is a wording contract pinned by tests and it is about stalled and fenced, which stay unobserved. Do not change its wording. If the evidence shows a report wording change is needed, stop and report it as an owner decision.
- Real values the code must match, from the 2026-11-16 capture of a running worker (`/home/coder/captures/q24-orca-capture2-20261116.md`): `result.dispatch.status` is `dispatched`; `result.projection.outcome` is `in_progress`; `result.projection.liveness.verdict` is `live`; `agentWait` is present with value null at `result.observation.agentWait` and at `result.terminal.agentWait`. A finished worker shows `completed`, `succeeded`, `unverifiable`.
- Do not open `/home/coder/captures/q24-orca-capture-20261116.md` (it holds other sessions' private prompt text).
- Use `uv run` for every Python command.
Start sha: 6306c0a7658751c80c75e062e737fca48b58c5fd
Diff against the start snapshot: diff --git a/src/superclaude/cli/sweep/classify.py b/src/superclaude/cli/sweep/classify.py
index 960faa562..a470eddaa 100644
--- a/src/superclaude/cli/sweep/classify.py
+++ b/src/superclaude/cli/sweep/classify.py
@@ -249,11 +249,23 @@ def _rule_waiting_signal(row: SessionRow, ctx: SweepContext) -> Classification |
 
 
 def _rule_working(row: SessionRow, ctx: SweepContext) -> Classification | None:
-    # Rule 5 cannot match in Phase 1 (DESIGN open item 6): the live names of the
-    # ``agentWait`` field and of the ``live`` and ``in_progress`` values were never
-    # captured, so a row that would reach it falls to the fallback. Once a read-only
-    # capture records them, restore the four conditions of DESIGN 7.2 (SP-24):
-    # liveness_verdict "live", status "in_progress", agent_wait_present True, agent_wait None.
+    # The four conditions of DESIGN 7.2 (SP-24), with the names captured from a running
+    # worker on 2026-11-16: projection.liveness.verdict "live", projection.outcome
+    # "in_progress" (dispatch.status is "dispatched", so ``status`` is not tested), and
+    # agentWait present with value null. A non-null agentWait never gets here: rule 4
+    # takes it first. What a non-null agentWait means is UNVERIFIED (never captured).
+    orca = row.orca
+    if (
+        orca is not None
+        and orca.liveness_verdict == "live"
+        and orca.outcome == "in_progress"
+        and orca.agent_wait_present is True
+        and orca.agent_wait is None
+    ):
+        evidence = (
+            "liveness_verdict live, outcome in_progress, agentWait present and null"
+        )
+        return _classification(C_WORKING, "working", evidence)
     return None
 
 
diff --git a/tests/sweep/test_classify.py b/tests/sweep/test_classify.py
index b5abc9f78..f5a7bd07a 100644
--- a/tests/sweep/test_classify.py
+++ b/tests/sweep/test_classify.py
@@ -275,12 +275,12 @@ def assert_no_sp16(result) -> None:
 
 
 def _rule_cases(now: datetime) -> dict[str, tuple[SessionRow, str, str | None]]:
-    # Rule 5 (working) cannot match while the live agentWait, `live` and `in_progress`
-    # names are uncaptured (DESIGN open item 6): its case holds all four conditions and
-    # is expected to fall to the fallback rule.
+    # Rule 5 (working) holds the four conditions captured from a running worker on
+    # 2026-11-16: liveness `live`, outcome `in_progress`, agentWait present and null.
     live_unwaiting = orca(
         liveness_verdict="live",
-        status="in_progress",
+        status="dispatched",
+        outcome="in_progress",
         agent_wait_present=True,
         agent_wait=None,
     )
@@ -317,7 +317,7 @@ def _rule_cases(now: datetime) -> dict[str, tuple[SessionRow, str, str | None]]:
             WAITING,
             "a",
         ),
-        "working": (row(orca=live_unwaiting), UNKNOWN, None),
+        "working": (row(orca=live_unwaiting), WORKING, None),
         "finished": (
             row(
                 orca=orca(outcome="succeeded"),
@@ -365,15 +365,14 @@ RULE_NAMES = [
 def test_rule_case_per_rule_1_to_9(now, rule):
     case_row, class_name, kind = _rule_cases(now)[rule]
     cls = classify(case_row, make_ctx(now))
-    matched = "fallback" if rule == "working" else rule  # rule 5 cannot match (item 6)
-    assert (cls.rule, cls.class_name, cls.waiting_kind) == (matched, class_name, kind)
+    assert (cls.rule, cls.class_name, cls.waiting_kind) == (rule, class_name, kind)
 
 
-def test_every_class_name_but_working_is_reached(now):
+def test_every_class_name_is_reached(now):
     reached = {
         classify(r, make_ctx(now)).class_name for r, _, _ in _rule_cases(now).values()
     }
-    assert reached == set(CLASSES) - {WORKING}  # no row is working in Phase 1
+    assert reached == set(CLASSES)
 
 
 def test_rules_order_pin():
@@ -433,25 +432,57 @@ def test_policy_of_is_independent_of_the_class(case_row, expected):
     assert policy_of(case_row) == expected
 
 
-def test_rule_5_never_matches_while_the_agent_wait_names_are_uncaptured(now):
-    full = dict(
-        liveness_verdict="live",
-        status="in_progress",
-        agent_wait_present=True,
-        agent_wait=None,
-    )
-    ctx = make_ctx(now)
-    # All four conditions of DESIGN 7.2 hold, and the row still falls to the fallback.
-    cls = classify(row(orca=orca(**full)), ctx)
-    assert (cls.rule, cls.class_name) == ("fallback", UNKNOWN)  # open item 6
-    for broken in (
+FULL_WORKING = dict(
+    liveness_verdict="live",
+    status="dispatched",
+    outcome="in_progress",
+    agent_wait_present=True,
+    agent_wait=None,
+)
+
+
+def test_rule_5_matches_a_live_in_progress_row_with_a_null_agent_wait(now):
+    cls = classify(row(orca=orca(**FULL_WORKING)), make_ctx(now))
+    assert (cls.rule, cls.class_name, cls.waiting_kind) == ("working", WORKING, None)
+    assert "outcome in_progress" in cls.evidence
+
+
+@pytest.mark.parametrize(
+    "broken",
+    [
         {"liveness_verdict": "unverifiable"},
-        {"status": "pending"},
+        {"liveness_verdict": "exited"},
+        {"liveness_verdict": None},
+        {"outcome": "succeeded"},
+        {"outcome": None},
         {"agent_wait_present": False},
-        {"agent_wait": {"since": "x"}},  # a non-null wait is rule 4, not working
-    ):
-        cls = classify(row(orca=orca(**{**full, **broken})), ctx)
-        assert cls.class_name != WORKING, broken
+    ],
+)
+def test_rule_5_needs_every_condition(now, broken):
+    cls = classify(row(orca=orca(**{**FULL_WORKING, **broken})), make_ctx(now))
+    assert cls.class_name != WORKING
+
+
+def test_rule_5_does_not_test_dispatch_status(now):
+    # dispatch.status is `dispatched` for a running worker; the word in_progress is the
+    # outcome. A row with status in_progress but no outcome is therefore not working.
+    only_status = {**FULL_WORKING, "status": "in_progress", "outcome": None}
+    cls = classify(row(orca=orca(**only_status)), make_ctx(now))
+    assert (cls.rule, cls.class_name) == ("fallback", UNKNOWN)
+    other_status = {**FULL_WORKING, "status": "pending"}
+    assert classify(row(orca=orca(**other_status)), make_ctx(now)).class_name == WORKING
+
+
+def test_a_non_null_agent_wait_is_waiting_never_working(now):
+    # What a non-null agentWait looks like is UNVERIFIED (never captured); this stand-in
+    # only shows that any non-null value stops rule 5 and reaches rule 4.
+    waiting = {**FULL_WORKING, "agent_wait": {"since": "x"}}
+    cls = classify(row(orca=orca(**waiting)), make_ctx(now))
+    assert (cls.rule, cls.class_name, cls.waiting_kind) == (
+        "waiting_signal",
+        WAITING,
+        "a",
+    )
 
 
 # ===========================================================================================
@@ -520,7 +551,8 @@ def test_future_transcript_gets_no_age(now):
         pytest.param(
             orca(
                 liveness_verdict="unverifiable",
-                status="in_progress",
+                status="dispatched",
+                outcome="in_progress",
                 agent_wait_present=True,
             ),
             id="unverifiable",
@@ -528,13 +560,19 @@ def test_future_transcript_gets_no_age(now):
         pytest.param(
             orca(
                 liveness_verdict="live",
-                status="in_progress",
+                status="dispatched",
+                outcome="in_progress",
                 agent_wait_present=False,
             ),
             id="late-heartbeat",
         ),
         pytest.param(
-            orca(liveness_verdict=None, status="in_progress", agent_wait_present=True),
+            orca(
+                liveness_verdict=None,
+                status="dispatched",
+                outcome="in_progress",
+                agent_wait_present=True,
+            ),
             id="stale-liveStatus",
         ),
         pytest.param(orca(), id="missing-worker-show-row"),
@@ -638,7 +676,8 @@ def test_no_contract_note_is_only_for_a_settled_row_with_no_contract(now, case_r
 def _live(**kw) -> OrcaObservation:
     base = dict(
         liveness_verdict="live",
-        status="in_progress",
+        status="dispatched",
+        outcome="in_progress",
         agent_wait_present=True,
         agent_wait=None,
     )

Codegraph context: index_state fresh (checked 2026-11-16T22:34:54Z); call codegraph only when index_state: fresh, never to widen scope. Dependents not in the diff: _rule_waiting_signal (rule 4, unchanged, runs before rule 5), src/superclaude/cli/sweep/report.py (reads class names and agent_wait through _age; unchanged), tests/sweep/test_report.py and tests/sweep/test_cli_contract.py (unchanged, still passing). Test run after the change: uv run pytest tests/sweep -q gives 647 passed; uv run ruff check src/superclaude/cli/sweep tests/sweep passes. The line if orca is not None and orca.status == "ready": in classify.py is not in the diff.
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
