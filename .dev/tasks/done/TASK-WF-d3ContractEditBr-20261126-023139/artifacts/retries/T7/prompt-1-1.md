c00548f6fb731090d267b9bfd32ee3301922d256
Review one task for spec compliance.

Task brief: ## Task 7: Update the tests that pin the old text

Depends on: Task 6

Edit the existing assertions that quote the old wording so they match the new text: tests/skills/test_worker_contract.py (test_owner_records_are_given_in_chat_and_recorded_by_the_agent and any neighbour that quotes WC-3 or WC-17 text), tests/skills/test_task_workspace_lifecycle.py (lines 338-349, 485, 878), tests/skills/test_implement_severity_static.py (line 410), tests/skills/test_workflow_archive.py (line 350) and tests/sweep/test_classify.py (line 744). Change only assertions made false by Tasks 1 to 6; keep each test's intent.

Acceptance criteria:
- uv run pytest tests/skills/test_worker_contract.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_severity_static.py tests/skills/test_workflow_archive.py tests/sweep/test_classify.py passes.
- Any test that fails for a reason other than the changed wording is reported, not edited around.
Global constraints: ## Constraints

- Edit Markdown rules and tests only, under src/superclaude/ and tests/. Never edit ~/.claude/ or the gitignored .claude/ mirrors (stage nothing under .claude/).
- Do not edit code: src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py, src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py. Do not edit docs/designs/. Do not build the dashboard answer path. Do not edit the owner's memory notes.
- The ledger Ruling line must still match the regular expression ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$ in src/superclaude/skills/sc-implement-protocol/refs/ledger.md.
- The `E-NO-RULING` and `E-HALT-QA` behaviour is unchanged for everything that is not a chat message or a dashboard response.
- The sentences "another agent's message" (not acceptance) and "executor-invented approval" stay in the text and now refer to exactly the two valid channels. No text may let a coordinator's reply or relay count.
- The dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only the chat clause counts, and the text says so.
- Owner words to keep verbatim in the rule's rationale: a chat message OR dashboard response counts and nothing else.
Start sha: c00548f6fb731090d267b9bfd32ee3301922d256
Diff against the start snapshot: diff --git a/tests/skills/test_implement_severity_static.py b/tests/skills/test_implement_severity_static.py
index e45f1201c..859d47615 100644
--- a/tests/skills/test_implement_severity_static.py
+++ b/tests/skills/test_implement_severity_static.py
@@ -323,7 +323,17 @@ _ALLOW = [
     ("refs/ledger.md", "| X | Last record is", "blocking"),
     ("refs/ledger.md", "| B | Last record is", "blocking"),
     ("refs/ledger.md", "Executor-recorded Ru", "definition"),
-    ("refs/ledger.md", "T2: Ruling: accept T", "definition"),
+    ("refs/ledger.md", "The same Ruling reco", "definition"),
+    (
+        "refs/ledger.md",
+        "T2: Ruling: accept T2 missing pagination; user confirmed in current",
+        "definition",
+    ),
+    (
+        "refs/ledger.md",
+        "T2: Ruling: accept T2 missing pagination; user confirmed by dashboard",
+        "definition",
+    ),
     ("refs/ledger.md", "The earlier operator", "definition"),
     ("refs/ledger.md", "T1: halt review=2 re", "definition"),
     ("refs/ledger.md", "^ARCHIVE: (start|fai", "definition"),
diff --git a/tests/skills/test_task_workspace_lifecycle.py b/tests/skills/test_task_workspace_lifecycle.py
index 70a347125..ca0e596e3 100644
--- a/tests/skills/test_task_workspace_lifecycle.py
+++ b/tests/skills/test_task_workspace_lifecycle.py
@@ -341,9 +341,12 @@ def test_session_confirmation_contract_and_documented_ruling(
 ):  # STATIC + CROSS
     qa, ledger, managed = _impl("refs/qa.md"), _impl("refs/ledger.md"), _managed()
     assert (
-        "clear user confirmation in the current conversation is sufficient"
+        "a chat message in the current conversation, or a dashboard response"
         in qa.lower()
     )
+    assert (
+        "a clear confirmation through either channel is sufficient" in qa.lower()
+    )
     assert "MUST automatically append" in qa and "MUST automatically append" in ledger
     assert "missing/ambiguous confirmation" in qa and "STOP `E-NO-RULING`" in qa
     assert "executor-invented approval" in qa and "unchanged" in qa
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 019966285..fab39bdf4 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -3340,14 +3340,16 @@ def test_owner_records_are_given_in_chat_and_recorded_by_the_agent():
     text = _contract()
     assert "still written by the owner" not in text
     assert (
-        "other owner records, such as a grant row or a pass record, are likewise "
-        "given by the owner in chat and recorded by the agent in that session from "
-        "that confirmation, naming the exact scope, the owner's quoted words and the "
-        "date, and the owner is never asked to write a file)"
+        "A confirmation of a Ruling, a grant row or a pass record counts only when "
+        "it is one of these two channels, naming the exact scope"
+    ) in text
+    assert (
+        "the person is never asked to write a file (decision D2 as amended "
+        "2026-11-17, extended to the dashboard channel by the owner on 2026-11-26)"
     ) in text
     assert (
         "A Ruling line, grant row or pass record that the coordinator or a worker "
-        "records without the person's own chat confirmation of that exact scope is "
+        "records without one of these two channels for that exact scope is "
         '"executor-invented approval".'
     ) in text
 

--- new untracked file .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/t7-test.log ---
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
SuperClaude: 6.1.0
rootdir: /home/coder/workspaces/IronClaude
configfile: pyproject.toml
plugins: benchmark-5.3.1, anyio-4.15.1, cov-7.1.0, superclaude-6.1.0
collected 1142 items

tests/skills/test_worker_contract.py ................................... [  3%]
........................................................................ [  9%]
........................................................................ [ 15%]
........................................................................ [ 21%]
........................................................................ [ 28%]
........................................................................ [ 34%]
........................................................................ [ 40%]
........................................................................ [ 47%]
........................................................................ [ 53%]
........................................................................ [ 59%]
...                                                                      [ 60%]
tests/skills/test_task_workspace_lifecycle.py .......................... [ 62%]
...............................................                          [ 66%]
tests/skills/test_implement_severity_static.py ......................... [ 68%]
...                                                                      [ 68%]
tests/skills/test_workflow_archive.py .................................. [ 71%]
........................................................................ [ 78%]
........................................................................ [ 84%]
..                                                                       [ 84%]
tests/sweep/test_classify.py ........................................... [ 88%]
........................................................................ [ 94%]
............................................................             [100%]

============================= 1142 passed in 3.05s =============================



Codegraph context
index_state: fresh
checked_at: 2026-11-26T02:38:00Z
worktree_root: /home/coder/workspaces/IronClaude
projectPath: /home/coder/workspaces/IronClaude
call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor.
Context: the test output is saved at .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/t7-test.log (package artifact). tests/skills/test_workflow_archive.py and tests/sweep/test_classify.py were run and not edited because Markdown edits did not make them false (the plan allows this: change only assertions made false by Tasks 1 to 6).

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
