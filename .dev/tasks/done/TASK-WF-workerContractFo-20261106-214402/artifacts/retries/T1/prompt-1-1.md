f7d0bad783074199e4d422e5a5a33a5b7c7b1622
Review one task for spec compliance.

Task brief: (Repository root: /home/coder/workspaces/worktrees/IronClaude/WorkerContractFollowups; resolve every repo-relative path against it.)
T1 (Task 1: Add the gitignored-path exclusion to WC-4 in WORKER-CONTRACT.md

In `src/superclaude/core/WORKER-CONTRACT.md`, WC-4 (the `- **WC-4.` bullet at line 31 and its sub-bullets up to the `- **WC-8.` bullet), add a new sub-bullet directly after the worker-fields sub-bullet (line 32) reading exactly: "`artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path and git refuses them. This applies to every command's `artifacts` list, including a fixed list in the command's own section." Do not change the pinned phrase on line 32. Do not add a report-naming duty to WC-4 (owner decision, Revision note). In `tests/skills/test_worker_contract.py`, add the phrase "`artifacts` leaves out paths git ignores and paths outside the repository" to `RULE_PHRASES["WC-4"]` (so `test_rule_check_fails_when_rule_removed` covers it), and add one assertion that the WC-4 span alone (the text from "- **WC-4." up to "\n- **WC-8.") contains "git ignores", "outside the repository" and "every command's `artifacts` list". In the developer guide (`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, the "WC-4, the worker contract." bullet around line 1002), add one sentence with the same rule: `artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path and git refuses them.

Acceptance criteria:
- WC-4 in `src/superclaude/core/WORKER-CONTRACT.md` holds the new sub-bullet with the exact text above, inside the WC-4 span; the line-32 pin is unchanged; no new WC-4 text contains the literal `git add`.
- The new `RULE_PHRASES["WC-4"]` entry and the WC-4-span assertion exist; the span assertion fails if the sentence is moved into WC-9 (check by reasoning over the slice bounds, or with the existing `_patched_copy` helper).
- The developer-guide WC-4 bullet carries the rule.
- `uv run pytest tests/skills/test_worker_contract.py -q` passes.
)
AC ids in order of the acceptance-criteria bullets: T1.AC1, T1.AC2, T1.AC3, T1.AC4
Global constraints: - Work only in this worktree's branch `ironbelly/WorkerContractFollowups` (based on `origin/master` cb8f2f81).
- Keep every existing test pin in `tests/skills/test_worker_contract.py`: the WC-4 phrase "`artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed"; the `UNATTENDED_EXPECT` flags and phrases for init-lite, build, test and workflow; the `Scaffold:`, `[]`, `--dry-run` and "as each file is written" / "as it is written" pins of the init-lite `artifacts` clause, and its bans on "when `--scaffold` is set", "failed tool run" and "on a failed run".
- No new text in `src/superclaude/commands/` or `src/superclaude/skills/` may contain the literal phrase `git add` (the write-verb classification test scans both); `git check-ignore` is allowed.
- New pointer text in installed files names the installed contract `~/.claude/WORKER-CONTRACT.md` where the file does not already point at it, and contains no `src/superclaude/` path.
- `src/superclaude/commands/workflow.md` and every file under `src/superclaude/skills/sc-workflow-protocol/` must stay byte-identical to their copies under `plugins/superclaude/` (parity tests in `tests/commands/test_workflow_command.py`, `tests/skills/test_task_workspace_smoke.py`, `tests/commands/test_routing_plugin_parity.py`). The plugin copies of `build.md` and `test.md` have no Unattended section and stay unchanged; init-lite has no plugin copy.
- Copies of WC-4 text (decided in review, finding M-4): the live copies are `src/superclaude/core/WORKER-CONTRACT.md`, the pins in `tests/skills/test_worker_contract.py`, and the developer-guide summary `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (around line 1002), which Task 1 updates. The planning spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (header: "Planning only") and its `specs/history/` snapshots stay unchanged, as do frozen records under `.dev/tasks/done/`, `.dev/orca-command-refactor/decisions/` and `.dev/reflect/`.
- Edit `src/superclaude/` (and the developer guide) only; run `make sync-dev` after edits; never stage `.claude/`. `.dev/tasks` is staged with `git add .dev/tasks`.
- Out of scope: the two flaky master tests (ccsession shim-port collision, roadmap thread-ident reuse), any other command's Unattended section (index-repo's fixed list is covered by the new WC-4 sentence without an edit), and `report_path` under an ignored path.
Start sha: f7d0bad783074199e4d422e5a5a33a5b7c7b1622
Diff against the start snapshot: 
diff --git a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
index c17772b9..0b4d3ec2 100644
--- a/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
+++ b/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
@@ -999,7 +999,7 @@ Orca can run IronClaude commands as workers under an Orca coordinator (the `/orc
 - **Person-mode refusal.** Under `--unattended` every command refuses the flags that exist to involve a human: `--interactive`, `--format interactive` (explain), `--mode socratic` (business-panel), `--watch` (test) and `--monitor 1` (pr-submit). The refusal is a stop before any work: the command writes its worker contract with `worker_status: failed` and the refused flag in `reason`, or, when no report directory is known, prints the refusal in chat only (WC-4).
 - **WC-2, no waiting for a human.** Under `--unattended` nothing asks the person: the command never calls `AskUserQuestion`, never ends its turn on a chat question or a `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed in the command's `## Unattended mode` section: a documented default, a value the caller passed as a flag, or blocked, where the command writes its contract with `worker_status: blocked` and the exact question in `blocked_question`, then stops.
 - **WC-4, the report directory.** The brief passes exactly one report directory. A command uses its own directory-valued `--output` or `--output-dir` as the report directory; `--report-dir <dir>` is for a command without such a flag, or for a brief that does not pass that flag. Passing both, or neither, is refused before any work (WC-4): the command does no work, writes nothing, and prints one fixed error message in chat that names both ways to pass a report directory. With no contract written, the worker reports the run as failed (WC-5).
-- **WC-4, the worker contract.** The command writes `<report-dir>/return-contract.yaml` on every outcome (succeeded, failed, blocked and partial), including stops before any other output exists. Its top-level fields are `worker_contract_version` (`"1"`), `worker_status`, `command` (the exact command line), `report_path` (the main human-readable deliverable, if any) and `artifacts` (every other file written), plus `blocked_question` when blocked and `reason` when failed (for `/sc:implement`, also when blocked, carrying the STOP code). `worker_status` is one of `succeeded`, `partial`, `failed` or `blocked`. It is not named `status`, because existing contracts already use `status` with other values.
+- **WC-4, the worker contract.** The command writes `<report-dir>/return-contract.yaml` on every outcome (succeeded, failed, blocked and partial), including stops before any other output exists. Its top-level fields are `worker_contract_version` (`"1"`), `worker_status`, `command` (the exact command line), `report_path` (the main human-readable deliverable, if any) and `artifacts` (every other file written), plus `blocked_question` when blocked and `reason` when failed (for `/sc:implement`, also when blocked, carrying the STOP code). `artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path and git refuses them. `worker_status` is one of `succeeded`, `partial`, `failed` or `blocked`. It is not named `status`, because existing contracts already use `status` with other values.
 - **WC-4, the two-case rule.** A command that already writes `return-contract.yaml` in the report directory itself keeps every existing field, including its own `status`, and adds the worker fields beside them. A command whose own contract lives elsewhere leaves that file unchanged, and the worker contract at `<report-dir>/return-contract.yaml` lists it in `artifacts`.
 - **WC-4, the status mapping.** A command's own status maps to `worker_status` in five cases: `success` to `succeeded`, `partial` to `partial`, `failed` to `failed`, `stopped-precondition` to `failed` with the precondition in `reason`, and the flag-STOP `blocked` of impact and graph to `failed` with the STOP in `reason`.
 - **WC-8, no dispatch from a command.** A command never calls `worker-start`, `dispatch` or `task-create`. Fan-out that needs Orca records is split into separate Tasks by the coordinator.
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 589ec391..d0e76010 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -30,6 +30,7 @@ These rules bind a command run with `--unattended`. Without the flag a command b
 - **WC-2. No person-blocking step in unattended mode.** Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed in the command's `## Unattended mode` section: (a) a documented default; (b) a value the caller supplied as a flag; (c) **blocked**: the command writes its contract with `worker_status: blocked` and the exact question in `blocked_question` (WC-4), and stops. What the worker does next is fixed by the brief (WC-3).
 - **WC-4. One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<report-dir>/return-contract.yaml`, where `<report-dir>` is the one report directory the brief passes (section 1): either the command's own directory-valued `--output` / `--output-dir`, or `--report-dir`. The coordinator therefore knows the path before dispatch even when the command's own deliverable lands at a generated or fixed location (for example workflow's `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>` package, cleanup-audit's `.claude-audit/`, implement's ledger, research's `claudedocs/research_[topic]_[timestamp].md`); the contract then points at that deliverable.
   - The worker fields are top-level keys: `worker_contract_version` (`"1"`), `worker_status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed (for `/sc:implement`, also when blocked, carrying the STOP code).
+  - `artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path and git refuses them. This applies to every command's `artifacts` list, including a fixed list in the command's own section.
   - The status field is named `worker_status`, not `status`, because existing contracts already use `status` with other values (`success | partial | failed` in workflow's and adversarial's contracts; reflect's `stopped-precondition`). A command that already writes `return-contract.yaml` in the report directory itself (brainstorm and reflect, `<output>/return-contract.yaml`) keeps every existing field, including its own `status`, and adds the worker fields beside them. Where its own contract lives elsewhere (workflow's package; adversarial's `<output>/adversarial/return-contract.yaml`, whose fields sit in a nested `return_contract:` block), the worker contract at `<report-dir>/return-contract.yaml` lists that file in `artifacts` and the command's own file is left unchanged.
   - Mapping from a command's own status: `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`, `stopped-precondition` → `failed` (precondition in `reason`), and the flag-STOP `blocked` of impact and graph → `failed` (the STOP in `reason`).
   - The contract is written on success, failure, blocked and partial outcomes, including stops before any other output exists.
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index bda71d67..eb99657e 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -105,6 +105,7 @@ RULE_PHRASES = {
             "One report file, known before dispatch, written on every outcome",
             '`worker_contract_version` (`"1"`), `worker_status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path`',
             "`artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed",
+            "`artifacts` leaves out paths git ignores and paths outside the repository",
         ],
     ),
     "WC-4-mapping": (
@@ -774,6 +775,17 @@ def _artifacts_clause(text: str) -> str:
     return re.split(r"`artifacts`|^artifacts:", line, maxsplit=1)[1]
 
 
+def test_wc4_states_the_ignored_path_exclusion():
+    # The exclusion lives once in WC-4; command sections point at it.
+    wc4 = _contract().split("- **WC-4.", 1)[1].split("\n- **WC-8.", 1)[0]
+    for phrase in (
+        "git ignores",
+        "outside the repository",
+        "every command's `artifacts` list",
+    ):
+        assert phrase in wc4, phrase
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
