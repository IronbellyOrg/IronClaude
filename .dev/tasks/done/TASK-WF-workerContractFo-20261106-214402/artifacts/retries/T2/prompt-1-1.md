b50d8260627dfdc01bc23c642d43bff15098fa7d
Review one task for spec compliance.

Task brief: (Repository root: /home/coder/workspaces/worktrees/IronClaude/WorkerContractFollowups; resolve every repo-relative path against it.)
T2 (Task 2: Shorten the workflow copies of the rule to a WC-4 pointer

Depends on: Task 1

In `src/superclaude/commands/workflow.md` (Unattended mode, Contract bullet, line 72), replace "are left out because WC-9 stages every `artifacts` path and git refuses ignored paths" with "are left out (WC-4)". In `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md` (the `artifacts:` YAML line 52), replace the comment tail "are left out (WC-9 stages every listed path, and git refuses ignored paths)" with "are left out (WC-4 in ~/.claude/WORKER-CONTRACT.md)". Keep everything else on both lines (package `return-contract.yaml`, `source.md` when written, reflect's run-directory files, the deviation-patterns file, "pre-creation", `[]` before a package exists). Add no line with a backticked `artifacts` or a leading `artifacts:` above line 52 of return-contract.md, so the test helper `_artifacts_clause` keeps reading line 52. Byte-copy both files to `plugins/superclaude/commands/workflow.md` and `plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`. In `test_unattended_artifacts_list_only_files_the_run_wrote` (`tests/skills/test_worker_contract.py`), make the workflow assertions require "runs.jsonl", "left out" and "WC-4" in both the command clause and the ref line.

Acceptance criteria:
- Both workflow texts name the ignored files they leave out and point at WC-4; neither contains "git refuses", "stages every" or the literal `git add`; return-contract.md names `~/.claude/WORKER-CONTRACT.md` and no `src/superclaude/` path.
- The plugin copies are byte-identical (`uv run pytest tests/commands/test_workflow_command.py tests/skills/test_task_workspace_smoke.py tests/commands/test_routing_plugin_parity.py -q` passes).
- `uv run pytest tests/skills/test_worker_contract.py -q` passes with the updated workflow assertions.
)
AC ids in order of the acceptance-criteria bullets: T2.AC1, T2.AC2, T2.AC3
Global constraints: - Work only in this worktree's branch `ironbelly/WorkerContractFollowups` (based on `origin/master` cb8f2f81).
- Keep every existing test pin in `tests/skills/test_worker_contract.py`: the WC-4 phrase "`artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed"; the `UNATTENDED_EXPECT` flags and phrases for init-lite, build, test and workflow; the `Scaffold:`, `[]`, `--dry-run` and "as each file is written" / "as it is written" pins of the init-lite `artifacts` clause, and its bans on "when `--scaffold` is set", "failed tool run" and "on a failed run".
- No new text in `src/superclaude/commands/` or `src/superclaude/skills/` may contain the literal phrase `git add` (the write-verb classification test scans both); `git check-ignore` is allowed.
- New pointer text in installed files names the installed contract `~/.claude/WORKER-CONTRACT.md` where the file does not already point at it, and contains no `src/superclaude/` path.
- `src/superclaude/commands/workflow.md` and every file under `src/superclaude/skills/sc-workflow-protocol/` must stay byte-identical to their copies under `plugins/superclaude/` (parity tests in `tests/commands/test_workflow_command.py`, `tests/skills/test_task_workspace_smoke.py`, `tests/commands/test_routing_plugin_parity.py`). The plugin copies of `build.md` and `test.md` have no Unattended section and stay unchanged; init-lite has no plugin copy.
- Copies of WC-4 text (decided in review, finding M-4): the live copies are `src/superclaude/core/WORKER-CONTRACT.md`, the pins in `tests/skills/test_worker_contract.py`, and the developer-guide summary `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (around line 1002), which Task 1 updates. The planning spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (header: "Planning only") and its `specs/history/` snapshots stay unchanged, as do frozen records under `.dev/tasks/done/`, `.dev/orca-command-refactor/decisions/` and `.dev/reflect/`.
- Edit `src/superclaude/` (and the developer guide) only; run `make sync-dev` after edits; never stage `.claude/`. `.dev/tasks` is staged with `git add .dev/tasks`.
- Out of scope: the two flaky master tests (ccsession shim-port collision, roadmap thread-ident reuse), any other command's Unattended section (index-repo's fixed list is covered by the new WC-4 sentence without an edit), and `report_path` under an ignored path.
Start sha: b50d8260627dfdc01bc23c642d43bff15098fa7d
Diff against the start snapshot: 
diff --git a/plugins/superclaude/commands/workflow.md b/plugins/superclaude/commands/workflow.md
index 854a478f..1890089e 100644
--- a/plugins/superclaude/commands/workflow.md
+++ b/plugins/superclaude/commands/workflow.md
@@ -69,7 +69,7 @@ The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This sect
 
 - **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (an inline prompt is a quoted argument); otherwise nothing here applies and no worker contract is written.
 - **Report directory.** `--report-dir <dir>` only; the retired `--output` stays `E-LEGACY`. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
-- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, including each pre-creation STOP (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-BAD-FLAG`, `E-LEGACY`, `E-PACKAGE-COLLISION`), with the STOP code in `reason`. The package's own rule for those STOPs (no package, no yaml) is unchanged. Once a package exists, `artifacts` lists every other file the run wrote: the package's `return-contract.yaml`, its `source.md` when the snapshot was written, each file the reflect step wrote in its `.dev/reflect/` run directory (also when reflect failed), and `docs/memory/reflect/deviation-patterns-<slug>.md` when reflect wrote it; reflect's gitignored per-machine files (`.dev/reflect/runs.jsonl`, `.superclaude/memory/`) are left out because WC-9 stages every `artifacts` path and git refuses ignored paths. `report_path` is the plan `<id>.md`. The package statuses success, partial and failed map to succeeded, partial and failed.
+- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, including each pre-creation STOP (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-BAD-FLAG`, `E-LEGACY`, `E-PACKAGE-COLLISION`), with the STOP code in `reason`. The package's own rule for those STOPs (no package, no yaml) is unchanged. Once a package exists, `artifacts` lists every other file the run wrote: the package's `return-contract.yaml`, its `source.md` when the snapshot was written, each file the reflect step wrote in its `.dev/reflect/` run directory (also when reflect failed), and `docs/memory/reflect/deviation-patterns-<slug>.md` when reflect wrote it; reflect's gitignored per-machine files (`.dev/reflect/runs.jsonl`, `.superclaude/memory/`) are left out (WC-4). `report_path` is the plan `<id>.md`. The package statuses success, partial and failed map to succeeded, partial and failed.
 - **Handoff.** A `--handoff implement` is skipped (the implement executor accepts the flag only in a later phase) and recorded in the package contract as `partial` with one `unresolved` line. The `design` and `tasklist` handoffs are text and unchanged.
 - **Gates.** None else, and no person-mode flag.
 - **Nested invocations.** The reflect step runs as today, without `--unattended` and without `--remediate`; in that form it has no gate.
diff --git a/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md b/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
index 8d6ebd26..ba015c72 100644
--- a/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
+++ b/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
@@ -49,7 +49,7 @@ worker_contract_version: "1"
 worker_status: succeeded | partial | failed
 command: <the exact command line>
 report_path: <repo path of the plan <id>.md, in to-do/ or, after an archive, done/> | null
-artifacts: [<package return-contract.yaml>, <package source.md if written>, <each file reflect wrote in its .dev/reflect/ run directory, whatever reflect_status is>, <docs/memory/reflect/deviation-patterns-<slug>.md if reflect wrote it>]   # [] before a package exists; gitignored .dev/reflect/runs.jsonl and .superclaude/memory/ are left out (WC-9 stages every listed path, and git refuses ignored paths)
+artifacts: [<package return-contract.yaml>, <package source.md if written>, <each file reflect wrote in its .dev/reflect/ run directory, whatever reflect_status is>, <docs/memory/reflect/deviation-patterns-<slug>.md if reflect wrote it>]   # [] before a package exists; gitignored .dev/reflect/runs.jsonl and .superclaude/memory/ are left out (WC-4 in ~/.claude/WORKER-CONTRACT.md)
 reason: <the STOP code or the failure>                              # only when failed
 ```
 
diff --git a/src/superclaude/commands/workflow.md b/src/superclaude/commands/workflow.md
index 854a478f..1890089e 100644
--- a/src/superclaude/commands/workflow.md
+++ b/src/superclaude/commands/workflow.md
@@ -69,7 +69,7 @@ The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This sect
 
 - **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (an inline prompt is a quoted argument); otherwise nothing here applies and no worker contract is written.
 - **Report directory.** `--report-dir <dir>` only; the retired `--output` stays `E-LEGACY`. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
-- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, including each pre-creation STOP (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-BAD-FLAG`, `E-LEGACY`, `E-PACKAGE-COLLISION`), with the STOP code in `reason`. The package's own rule for those STOPs (no package, no yaml) is unchanged. Once a package exists, `artifacts` lists every other file the run wrote: the package's `return-contract.yaml`, its `source.md` when the snapshot was written, each file the reflect step wrote in its `.dev/reflect/` run directory (also when reflect failed), and `docs/memory/reflect/deviation-patterns-<slug>.md` when reflect wrote it; reflect's gitignored per-machine files (`.dev/reflect/runs.jsonl`, `.superclaude/memory/`) are left out because WC-9 stages every `artifacts` path and git refuses ignored paths. `report_path` is the plan `<id>.md`. The package statuses success, partial and failed map to succeeded, partial and failed.
+- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, including each pre-creation STOP (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-BAD-FLAG`, `E-LEGACY`, `E-PACKAGE-COLLISION`), with the STOP code in `reason`. The package's own rule for those STOPs (no package, no yaml) is unchanged. Once a package exists, `artifacts` lists every other file the run wrote: the package's `return-contract.yaml`, its `source.md` when the snapshot was written, each file the reflect step wrote in its `.dev/reflect/` run directory (also when reflect failed), and `docs/memory/reflect/deviation-patterns-<slug>.md` when reflect wrote it; reflect's gitignored per-machine files (`.dev/reflect/runs.jsonl`, `.superclaude/memory/`) are left out (WC-4). `report_path` is the plan `<id>.md`. The package statuses success, partial and failed map to succeeded, partial and failed.
 - **Handoff.** A `--handoff implement` is skipped (the implement executor accepts the flag only in a later phase) and recorded in the package contract as `partial` with one `unresolved` line. The `design` and `tasklist` handoffs are text and unchanged.
 - **Gates.** None else, and no person-mode flag.
 - **Nested invocations.** The reflect step runs as today, without `--unattended` and without `--remediate`; in that form it has no gate.
diff --git a/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md b/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
index 8d6ebd26..ba015c72 100644
--- a/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
+++ b/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
@@ -49,7 +49,7 @@ worker_contract_version: "1"
 worker_status: succeeded | partial | failed
 command: <the exact command line>
 report_path: <repo path of the plan <id>.md, in to-do/ or, after an archive, done/> | null
-artifacts: [<package return-contract.yaml>, <package source.md if written>, <each file reflect wrote in its .dev/reflect/ run directory, whatever reflect_status is>, <docs/memory/reflect/deviation-patterns-<slug>.md if reflect wrote it>]   # [] before a package exists; gitignored .dev/reflect/runs.jsonl and .superclaude/memory/ are left out (WC-9 stages every listed path, and git refuses ignored paths)
+artifacts: [<package return-contract.yaml>, <package source.md if written>, <each file reflect wrote in its .dev/reflect/ run directory, whatever reflect_status is>, <docs/memory/reflect/deviation-patterns-<slug>.md if reflect wrote it>]   # [] before a package exists; gitignored .dev/reflect/runs.jsonl and .superclaude/memory/ are left out (WC-4 in ~/.claude/WORKER-CONTRACT.md)
 reason: <the STOP code or the failure>                              # only when failed
 ```
 
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index eb99657e..0cd1925f 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -818,6 +818,8 @@ def test_unattended_artifacts_list_only_files_the_run_wrote():
     ):
         assert "reflect" in clause and "deviation-patterns" in clause, clause
         assert "runs.jsonl" in clause and "left out" in clause, clause
+        # The reason lives in WC-4; the clause only points at it.
+        assert "WC-4" in clause and "git refuses" not in clause, clause
 
 
 def test_explain_declares_write_under_tool_coordination():

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
