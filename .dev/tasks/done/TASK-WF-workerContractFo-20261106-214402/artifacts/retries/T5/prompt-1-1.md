332077e9a1c3cee5796c3fc8e122dc78176a5c80
Review one task for spec compliance.

Task brief: (Repository root: /home/coder/workspaces/worktrees/IronClaude/WorkerContractFollowups; resolve every repo-relative path against it.)
T5 (Task 5: Tie init-lite's `worker_status` to the tool's exit code

In `src/superclaude/skills/sc-init-lite-protocol/SKILL.md` (Section 3 step 6, line 61), replace "`worker_status` (`succeeded` when the audit finished, else `failed`)" with "`worker_status` (`succeeded` when `superclaude init-lite` exited 0, meaning the audit finished and every requested scaffold write succeeded; otherwise `failed`, with the tool's error in `reason`; the tool's exit code is the only basis for `succeeded`)". In `src/superclaude/commands/init-lite.md` (Unattended mode, Contract bullet, line 92), replace the last sentence "The run is succeeded when the audit finished, and failed otherwise." with "The run is `succeeded` when `superclaude init-lite` exited 0 (the audit finished and every requested scaffold write succeeded), and `failed` otherwise, with the tool's error in `reason`; `artifacts` still lists the `Scaffold:` lines printed before a failure." This follows the decision in ./source.md (Follow-up 3): a WC-9 commit grant commits only on `succeeded`, so a partial scaffold must not be `succeeded`. The init-lite.md status sentence sits inside the `artifacts` clause the tests read, so it must contain neither "failed tool run" nor "on a failed run". Keep the pins "the one write besides the report", "Safety Invariants 2 and 3", `--dry-run`, `Scaffold:`, `[]`, "as it is written". In `tests/skills/test_worker_contract.py`, assert that the SKILL.md line carrying `worker_status` and the init-lite.md Contract line each contain the exact phrase "`succeeded` when `superclaude init-lite` exited 0" and do not contain "when the audit finished".

Acceptance criteria:
- Both init-lite texts carry the exact phrase "`succeeded` when `superclaude init-lite` exited 0", tie `failed` to any other exit with the error in `reason`, keep `artifacts` listing the printed `Scaffold:` lines, and no longer contain "when the audit finished".
- `uv run pytest tests/skills/test_worker_contract.py tests/cli/test_init_lite.py -q` passes, including the new assertions and the existing init-lite pins.
- `uv run pytest tests/skills/test_worker_contract.py tests/commands/test_workflow_command.py tests/skills/test_task_workspace_smoke.py tests/commands/test_routing_plugin_parity.py tests/cli/test_init_lite.py tests/cli/test_how_we_work_install.py -q`, `make lint`, `uv run ruff format --check src/ tests/` and `make verify-sync` (after `make sync-dev`) all pass, with output saved to `./artifacts/t5-checks.txt` (the package's own `artifacts/` folder).
)
AC ids in order of the acceptance-criteria bullets: T5.AC1, T5.AC2, T5.AC3
Global constraints: - Work only in this worktree's branch `ironbelly/WorkerContractFollowups` (based on `origin/master` cb8f2f81).
- Keep every existing test pin in `tests/skills/test_worker_contract.py`: the WC-4 phrase "`artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed"; the `UNATTENDED_EXPECT` flags and phrases for init-lite, build, test and workflow; the `Scaffold:`, `[]`, `--dry-run` and "as each file is written" / "as it is written" pins of the init-lite `artifacts` clause, and its bans on "when `--scaffold` is set", "failed tool run" and "on a failed run".
- No new text in `src/superclaude/commands/` or `src/superclaude/skills/` may contain the literal phrase `git add` (the write-verb classification test scans both); `git check-ignore` is allowed.
- New pointer text in installed files names the installed contract `~/.claude/WORKER-CONTRACT.md` where the file does not already point at it, and contains no `src/superclaude/` path.
- `src/superclaude/commands/workflow.md` and every file under `src/superclaude/skills/sc-workflow-protocol/` must stay byte-identical to their copies under `plugins/superclaude/` (parity tests in `tests/commands/test_workflow_command.py`, `tests/skills/test_task_workspace_smoke.py`, `tests/commands/test_routing_plugin_parity.py`). The plugin copies of `build.md` and `test.md` have no Unattended section and stay unchanged; init-lite has no plugin copy.
- Copies of WC-4 text (decided in review, finding M-4): the live copies are `src/superclaude/core/WORKER-CONTRACT.md`, the pins in `tests/skills/test_worker_contract.py`, and the developer-guide summary `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (around line 1002), which Task 1 updates. The planning spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (header: "Planning only") and its `specs/history/` snapshots stay unchanged, as do frozen records under `.dev/tasks/done/`, `.dev/orca-command-refactor/decisions/` and `.dev/reflect/`.
- Edit `src/superclaude/` (and the developer guide) only; run `make sync-dev` after edits; never stage `.claude/`. `.dev/tasks` is staged with `git add .dev/tasks`.
- Out of scope: the two flaky master tests (ccsession shim-port collision, roadmap thread-ident reuse), any other command's Unattended section (index-repo's fixed list is covered by the new WC-4 sentence without an edit), and `report_path` under an ignored path.
Start sha: 332077e9a1c3cee5796c3fc8e122dc78176a5c80
Diff against the start snapshot: 
diff --git a/src/superclaude/commands/init-lite.md b/src/superclaude/commands/init-lite.md
index cabd3148..a8d0e455 100644
--- a/src/superclaude/commands/init-lite.md
+++ b/src/superclaude/commands/init-lite.md
@@ -89,7 +89,7 @@ The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This sect
 
 - **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
 - **Report directory.** `--report-dir <dir>` only: its `--output <file>` names the report file, not a directory. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
-- **Contract.** `<report-dir>/return-contract.yaml` is the exception to Safety Invariants 2 and 3 of the protocol: it is the one write besides the report and the scaffold, and it is written also on `--dry-run`. `report_path` is the audit report (the `--output` path or `.dev/superclaude/context-audit.md`), null on `--dry-run`; `artifacts` lists only the scaffold files this run wrote, as printed on the tool's `Scaffold:` lines, one per file as it is written (files `--force` overwrote and a file written before a later scaffold write failed included), and is `[]` on `--dry-run` and when no `Scaffold:` line was printed. The run is succeeded when the audit finished, and failed otherwise.
+- **Contract.** `<report-dir>/return-contract.yaml` is the exception to Safety Invariants 2 and 3 of the protocol: it is the one write besides the report and the scaffold, and it is written also on `--dry-run`. `report_path` is the audit report (the `--output` path or `.dev/superclaude/context-audit.md`), null on `--dry-run`; `artifacts` lists only the scaffold files this run wrote, as printed on the tool's `Scaffold:` lines, one per file as it is written (files `--force` overwrote and a file written before a later scaffold write failed included), and is `[]` on `--dry-run` and when no `Scaffold:` line was printed. The run is `succeeded` when `superclaude init-lite` exited 0 (the audit finished and every requested scaffold write succeeded), and `failed` otherwise, with the tool's error in `reason`; `artifacts` still lists the `Scaffold:` lines printed before a failure.
 - **Context inputs.** The command never modifies a context input.
 - **Gates.** None, and no person-mode flag. Nested invocations: none.
 - **Outward actions.** It pushes, commits and stages nothing.
diff --git a/src/superclaude/skills/sc-init-lite-protocol/SKILL.md b/src/superclaude/skills/sc-init-lite-protocol/SKILL.md
index 9121e31f..7005bf5f 100644
--- a/src/superclaude/skills/sc-init-lite-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-init-lite-protocol/SKILL.md
@@ -58,7 +58,7 @@ Under `--unattended` the skill consumes `--unattended` and `--report-dir` itself
    - `--dry-run`: render the report to stdout and write nothing — do NOT create `.dev/superclaude/`.
 4. **Scaffold** (only when `--scaffold`): create advisory `project-guidance/SKILL.md` and `project-guidance/refs/README.md` under `.dev/superclaude/`; idempotent (existing files are left intact unless `--force`).
 5. **Surface** the resulting paths and the token summary to the user.
-6. **Worker contract** (only with `--unattended`; follow the `## Unattended mode` section of the `init-lite` command file, installed copy `~/.claude/commands/sc/init-lite.md` or project copy `.claude/commands/sc/init-lite.md`): after the tool returns, on every outcome including `--dry-run` and a failed tool run, write `<report-dir>/return-contract.yaml` with `worker_contract_version: "1"`, `worker_status` (`succeeded` when the audit finished, else `failed`), `command` (the exact command line), `report_path` (the report path; null on `--dry-run`), `artifacts` (only the scaffold files this run wrote, as printed on the tool's `Scaffold:` lines, which the tool prints as each file is written, including files `--force` overwrote and a file written before a later scaffold write failed; `[]` on `--dry-run` and when no `Scaffold:` line was printed) and `reason` when failed.
+6. **Worker contract** (only with `--unattended`; follow the `## Unattended mode` section of the `init-lite` command file, installed copy `~/.claude/commands/sc/init-lite.md` or project copy `.claude/commands/sc/init-lite.md`): after the tool returns, on every outcome including `--dry-run` and a failed tool run, write `<report-dir>/return-contract.yaml` with `worker_contract_version: "1"`, `worker_status` (`succeeded` when `superclaude init-lite` exited 0, meaning the audit finished and every requested scaffold write succeeded; otherwise `failed`, with the tool's error in `reason`; the tool's exit code is the only basis for `succeeded`), `command` (the exact command line), `report_path` (the report path; null on `--dry-run`), `artifacts` (only the scaffold files this run wrote, as printed on the tool's `Scaffold:` lines, which the tool prints as each file is written, including files `--force` overwrote and a file written before a later scaffold write failed; `[]` on `--dry-run` and when no `Scaffold:` line was printed) and `reason` when failed.
 
 Preferred implementation: shell out to `superclaude init-lite` with the resolved flags via Bash and relay its output.
 
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index e54dafc8..bb01c70c 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -786,6 +786,22 @@ def test_wc4_states_the_ignored_path_exclusion():
         assert phrase in wc4, phrase
 
 
+def test_init_lite_status_follows_the_tool_exit_code():
+    # A partial scaffold exits non-zero, so it must never be `succeeded`.
+    skill = (_REPO / "src/superclaude/skills/sc-init-lite-protocol/SKILL.md").read_text(
+        encoding="utf-8"
+    )
+    status_line = next(ln for ln in skill.splitlines() if "`worker_status`" in ln)
+    contract_line = next(
+        ln
+        for ln in _unattended_section("init-lite").splitlines()
+        if ln.startswith("- **Contract.**")
+    )
+    for line in (status_line, contract_line):
+        assert "`succeeded` when `superclaude init-lite` exited 0" in line, line
+        assert "when the audit finished" not in line, line
+
+
 def test_unattended_artifacts_list_only_files_the_run_wrote():
     # WC-4: `artifacts` is every other file written, so each list follows the run's
     # actual writes (PR #411 review: fixed lists over- and under-listed files).

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
