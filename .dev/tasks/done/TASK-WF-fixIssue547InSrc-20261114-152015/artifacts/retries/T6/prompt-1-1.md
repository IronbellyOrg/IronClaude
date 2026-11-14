2b4765e4baf07f0b9e3915cc14dcbf9b4d6d4e69
Review one task for spec compliance.

Task brief: ## Task 6: Count raw worker rows for the 100-row truncation rule and commit T1

Depends on: Task 5

Add the regression test first, in `tests/sweep/test_probes_allowlist.py` next to `test_collect_worker_list_source_rows_and_truncated` (line 1175): ninety-nine valid worker rows from `_rows([did(i) for i in range(99)])` plus the string `"not-an-object"`, delivered through `patch_orca.respond(wl(RUN1), {"workers": <those 100>, "page": {"limit": 100, "hasMore": False}})` after `_stock_run(patch_orca, RUN1, <the 99 rows>)`; assert `inp.truncated is True`. Run it on the unchanged code and save the failing output to `./artifacts/t6-red.log`. Then fix `_orca_reads` in `src/superclaude/cli/sweep/probes.py` (the `worker-list` block around lines 1049 to 1056): compute the raw count as `len(raw) if isinstance(raw, list) else 0` and use it in `if raw_count >= WORKER_LIST_PAGE or more:`; the `workers` list keeps filtering to objects for later use. Run `uv run pytest tests/sweep -q`, `uv run ruff format`, `uv run ruff check`, stage the two Python files by name and commit locally with the subject `fix(sweep): count raw worker rows for the full-page truncation rule (issue 547)` and the Co-Authored-By line. Do not close the issue and do not push.

Acceptance criteria:
- The new test fails before the fix (./artifacts/t6-red.log) and passes after; the existing 100-row and 99-row cases in `test_collect_worker_list_source_rows_and_truncated` still pass.
- `_orca_reads` callers (`collect`) are unchanged and `uv run pytest tests/sweep -q` passes.
- `git log --oneline -3` shows the T1 commit after the T2 commit, each touching only its own files.

Global constraints: 
- Owner design A (2026-11-14): `--ignore-submodules=all` goes into the status template; a submodule's own changes are no longer reported. No new JSON key and no new file other than this package and tests; the refusal reuses the existing `unscanned` source row (`SourceCoverage(name, "unscanned", None, reason)` built by `_failed_worktree` in `src/superclaude/cli/sweep/probes.py`).
- The owner-signed git allow-list (`ALLOWED_GIT`) may change only by the three read-only entries named in Task 2; any other allow-list change is not authorized. `ALLOWED_ORCA` and `FORBIDDEN_TOKENS` stay untouched.
- The git-status scope stays separate from the contract allow-list and the transcript scans: `_worktree_paths` and the shared `paths` list in `collect` are not filtered.
- Out of scope: `CLAUDE.md`, `tests/core/test_claude_md_worktree_rule.py`, anything under `.claude/`, wording or alignment edits, new JSON keys, sidecar files.
- Python only through UV: `uv run pytest tests/sweep -q`, `uv run ruff check`, `uv run ruff format`. Never `python -m`, bare `python`, or `pip`.
- Stage named paths only (`git add -- <paths>`, never `git add -A` or `git add .`); the plan package under `.dev/tasks/` is staged with the T2 commit. Commit locally on the current branch with conventional messages ending with the line `Co-Authored-By: Claude Code <noreply@anthropic.com>`. The executor commits only; it never pushes, opens a PR or writes to GitHub (the owner's session pushes afterwards).
- T2 (Tasks 1 to 5) and T1 (Task 6) are two separate commits. The sweep tests forbid a real subprocess unless a test carries the `integration` mark (`tests/sweep/conftest.py` autouse guard); real-git tests must carry that mark.


Start sha: 2b4765e4baf07f0b9e3915cc14dcbf9b4d6d4e69
Diff against the start snapshot: diff --git a/src/superclaude/cli/sweep/probes.py b/src/superclaude/cli/sweep/probes.py
index 4d58ce33d..e2c895f6f 100644
--- a/src/superclaude/cli/sweep/probes.py
+++ b/src/superclaude/cli/sweep/probes.py
@@ -1141,7 +1141,9 @@ def _orca_reads(
                 [w for w in raw if isinstance(w, dict)] if isinstance(raw, list) else []
             )
             more = _get(listing.data, "page", "hasMore") is True
-            if len(workers) >= WORKER_LIST_PAGE or more:
+            # The raw row count: a malformed entry dropped above must not hide a full page.
+            raw_count = len(raw) if isinstance(raw, list) else 0
+            if raw_count >= WORKER_LIST_PAGE or more:
                 state.truncated = True
         tasks_by_id: dict[str, dict] = {}
         ready_tasks: list[dict] = []
diff --git a/tests/sweep/test_probes_allowlist.py b/tests/sweep/test_probes_allowlist.py
index dd1f10175..8752c5256 100644
--- a/tests/sweep/test_probes_allowlist.py
+++ b/tests/sweep/test_probes_allowlist.py
@@ -1283,6 +1283,23 @@ def test_collect_worker_list_source_rows_and_truncated(
         assert inp.truncated is expected, count
 
 
+def test_full_worker_page_with_a_malformed_entry_still_sets_truncated(
+    sweep_root, patch_orca, patch_git, clock
+):
+    # Issue 547 (review thread on PR 539): 99 valid rows plus one non-object entry is a
+    # full page of 100 raw rows; dropping the bad entry must not hide the full page.
+    good = _rows([did(i) for i in range(99)])
+    _stock_run(patch_orca, RUN1, good)
+    patch_orca.respond(
+        wl(RUN1),
+        {"workers": [*good, "not-an-object"], "page": {"limit": 100, "hasMore": False}},
+    )
+
+    inp = _collect(sweep_root, clock)
+
+    assert inp.truncated is True
+
+
 def test_collect_worker_list_source_rows_budget_spent_before_r2(
     sweep_root, patch_orca, patch_git, clock, monkeypatch
 ):

=== evidence ./artifacts/t6-red.log (the new test on the unchanged code) ===
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/sweep-git-fix
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collected 279 items / 278 deselected / 1 selected

tests/sweep/test_probes_allowlist.py F                                   [100%]

=================================== FAILURES ===================================
______ test_full_worker_page_with_a_malformed_entry_still_sets_truncated _______
tests/sweep/test_probes_allowlist.py:1300: in test_full_worker_page_with_a_malformed_entry_still_sets_truncated
    assert inp.truncated is True
E   AssertionError: assert False is True
E    +  where False = SweepInput(orca_rows=(OrcaObservation(dispatch='ctx_000000000000', run='run_000000000001', session_join='term_ctx_0000...atetime.timezone.utc), collected_end=datetime.datetime(20
=========================== short test summary info ============================
FAILED tests/sweep/test_probes_allowlist.py::test_full_worker_page_with_a_malformed_entry_still_sets_truncated
====================== 1 failed, 278 deselected in 0.67s =======================

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
