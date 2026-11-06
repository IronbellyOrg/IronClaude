09efe9b16bb9e0dd9e9fcd6b6414c684668e0c6b
Review one task for spec compliance.

Task brief: (Repository root: /home/coder/workspaces/worktrees/IronClaude/WorkerContractFollowups; resolve every repo-relative path against it.)
T4 (Task 4: Add an `artifacts` rule to the /sc:test Unattended section

Depends on: Task 1

In `src/superclaude/commands/test.md` (Unattended mode, Contract bullet, line 103), add after the `report_path` sentence: "`artifacts` lists every other file the run wrote; paths git ignores are left out (WC-4; typically coverage output such as `htmlcov/`, `.coverage`, `coverage.xml` and `.pytest_cache/`), and the test report names where they were written; it is `[]` when nothing else listable was written." This must be the first backticked `artifacts` in the test Unattended section (no earlier bullet mentions it). Keep the existing pins (`--watch`, `--output`, "test-report.md", "verdict", "destructive"). In `tests/skills/test_worker_contract.py`, add "left out" to `UNATTENDED_EXPECT["test"]["phrases"]` (so the token-removal test covers it), and in `test_unattended_artifacts_list_only_files_the_run_wrote` assert that the test section's `artifacts` clause contains the exact phrase "paths git ignores are left out", "WC-4" and "`[]`", and has no write-verb match.

Acceptance criteria:
- The `src/superclaude/commands/test.md` Contract bullet has the `artifacts` clause above: ignored coverage output is left out with a WC-4 pointer, the report names where it went, and `[]` applies when nothing else listable was written.
- A clause that lists `htmlcov/` while naming WC-4 and `[]` but lacking "paths git ignores are left out" would fail the new assertion.
- `uv run pytest tests/skills/test_worker_contract.py -q` passes, including the new pins and the existing test.md `UNATTENDED_EXPECT` row.
)
AC ids in order of the acceptance-criteria bullets: T4.AC1, T4.AC2, T4.AC3
Global constraints: - Work only in this worktree's branch `ironbelly/WorkerContractFollowups` (based on `origin/master` cb8f2f81).
- Keep every existing test pin in `tests/skills/test_worker_contract.py`: the WC-4 phrase "`artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed"; the `UNATTENDED_EXPECT` flags and phrases for init-lite, build, test and workflow; the `Scaffold:`, `[]`, `--dry-run` and "as each file is written" / "as it is written" pins of the init-lite `artifacts` clause, and its bans on "when `--scaffold` is set", "failed tool run" and "on a failed run".
- No new text in `src/superclaude/commands/` or `src/superclaude/skills/` may contain the literal phrase `git add` (the write-verb classification test scans both); `git check-ignore` is allowed.
- New pointer text in installed files names the installed contract `~/.claude/WORKER-CONTRACT.md` where the file does not already point at it, and contains no `src/superclaude/` path.
- `src/superclaude/commands/workflow.md` and every file under `src/superclaude/skills/sc-workflow-protocol/` must stay byte-identical to their copies under `plugins/superclaude/` (parity tests in `tests/commands/test_workflow_command.py`, `tests/skills/test_task_workspace_smoke.py`, `tests/commands/test_routing_plugin_parity.py`). The plugin copies of `build.md` and `test.md` have no Unattended section and stay unchanged; init-lite has no plugin copy.
- Copies of WC-4 text (decided in review, finding M-4): the live copies are `src/superclaude/core/WORKER-CONTRACT.md`, the pins in `tests/skills/test_worker_contract.py`, and the developer-guide summary `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (around line 1002), which Task 1 updates. The planning spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (header: "Planning only") and its `specs/history/` snapshots stay unchanged, as do frozen records under `.dev/tasks/done/`, `.dev/orca-command-refactor/decisions/` and `.dev/reflect/`.
- Edit `src/superclaude/` (and the developer guide) only; run `make sync-dev` after edits; never stage `.claude/`. `.dev/tasks` is staged with `git add .dev/tasks`.
- Out of scope: the two flaky master tests (ccsession shim-port collision, roadmap thread-ident reuse), any other command's Unattended section (index-repo's fixed list is covered by the new WC-4 sentence without an edit), and `report_path` under an ignored path.
Start sha: 09efe9b16bb9e0dd9e9fcd6b6414c684668e0c6b
Diff against the start snapshot: 
diff --git a/src/superclaude/commands/test.md b/src/superclaude/commands/test.md
index cd4fd66e..fc0b53da 100644
--- a/src/superclaude/commands/test.md
+++ b/src/superclaude/commands/test.md
@@ -100,7 +100,7 @@ The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This sect
 
 - **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
 - **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
-- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/test-report.md`, holding the coverage and test summary. A failing suite is a verdict in that report and the run still ends succeeded; it ends failed only when no test runner could run.
+- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/test-report.md`, holding the coverage and test summary. `artifacts` lists every other file the run wrote; paths git ignores are left out (WC-4; typically coverage output such as `htmlcov/`, `.coverage`, `coverage.xml` and `.pytest_cache/`), and the test report names where they were written; it is `[]` when nothing else listable was written. A failing suite is a verdict in that report and the run still ends succeeded; it ends failed only when no test runner could run.
 - **Person-mode flags.** `--watch` is refused before any work, because it never ends (contract `worker_status: failed`, the flag in `reason`).
 - **Gates.** There is no other gate. `--fix` is the caller's consent for non-destructive fixes only; a destructive change to a test file (the rule "without explicit permission") is never made under `--unattended`.
 - **Nested invocations.** None.
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 96fba990..e54dafc8 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -349,7 +349,7 @@ UNATTENDED_EXPECT: dict = {
     },
     "test": {
         "flags": ["--watch", "--output"],
-        "phrases": ["test-report.md", "verdict", "destructive"],
+        "phrases": ["test-report.md", "verdict", "destructive", "left out"],
         "nested": [],
     },
     "explain": {
@@ -813,6 +813,9 @@ def test_unattended_artifacts_list_only_files_the_run_wrote():
     )
     assert "WC-4" in build and "git refuses" not in build, build
     assert not WRITE_VERB_RE.search(build), build
+    test = _artifacts_clause(_unattended_section("test"))
+    assert "paths git ignores are left out" in test and "WC-4" in test, test
+    assert "`[]`" in test and not WRITE_VERB_RE.search(test), test
     cleanup = _artifacts_clause(_unattended_section("cleanup-audit"))
     assert "pass<N>-summary.md" in cleanup and "progress.json" in cleanup, cleanup
     for clause in (

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
