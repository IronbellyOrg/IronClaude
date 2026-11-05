98470602dc2b12406c7066aa84da4ba13bf724f4
Review one task for spec compliance.

Task brief: T3 (AC ids in order of the "Acceptance criteria:" bullets: T3.AC1,T3.AC2,T3.AC3). Plan file: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md, lines 55-65:
## Task 3: Allow the re-review complete line in refs/ledger.md

Depends on: Task 2

In `src/superclaude/skills/sc-implement-protocol/refs/ledger.md`, after the section "## Post-ruling complete line", add a section "## Re-review complete line" stating that after a FINAL flags a saved prompt (`refs/qa.md`, "Defective saved prompt (recovery)"), a re-review with no blocking finding appends the task's `complete` line again with the same verdict fields as its latest `complete` line and no new `start` line, except that a re-review which writes new notes lines replaces the `notes@` token; it uses the existing verdict grammar and regex, the latest record of the task counts, it is legal only after a `FINAL:` line, and for a task completed after a user-accepted gap it repeats the non-compliant verdict fields unchanged so the accepted gap stays valid (see "Post-ruling complete line"). In section "## Managed-package extension", add one bullet saying the re-review `complete` lines and the later move to `superseded-prompts/` come before the fresh FINAL of the next archive attempt. Keep every new line free of the words listed in the second Constraints bullet. Copy the edited file byte for byte to the `plugins/` twin.

Acceptance criteria:
- `grep -n "## Re-review complete line" src/superclaude/skills/sc-implement-protocol/refs/ledger.md` prints one line, that section contains "no new `start` line", "same verdict fields", "replaces the `notes@` token" and "legal only after a `FINAL:` line", and the Managed-package extension bullet names `superseded-prompts/`; the grep output is saved in `./artifacts/t3-grep.txt`.
- The `extract-blocks.py ledger` output on the edited file is `cmp`-equal to its output on `git show HEAD:src/superclaude/skills/sc-implement-protocol/refs/ledger.md` (`./artifacts/t3-grammar-cmp.txt`, exit 0), and the number of lines containing `src/superclaude` equals that in `git show HEAD:` (`./artifacts/t3-srcpath.txt`).
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills -q -p no:cacheprovider` passes with no failures (`./artifacts/t3-pytest-skills.txt`), `git status --porcelain -- tests` shows no entry for `tests/skills/test_implement_severity_static.py` (`./artifacts/t3-tests-status.txt`), and `cmp` of the `src/` and `plugins/` copies of `refs/ledger.md` exits 0 (`./artifacts/t3-cmp.txt`).


Global constraints: (plan ## Constraints, .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md lines 17-27)
## Constraints

- Rule changes go only in `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`, each with a byte-identical copy at the same relative path under `plugins/superclaude/skills/sc-implement-protocol/`. No other skill, command, agent or core file changes, and the reviewer template block (the fenced block that begins "Review one task for spec compliance." under "## Subagent prompt (when not inline)" in `refs/qa.md`) and the `ledger-grammar-block` fenced blocks in `refs/ledger.md` do not change.
- `tests/skills/test_implement_severity_static.py` is not modified. Its classification test fails on any line in the protocol files that matches the words `Ruling` (capital R), `halt`, `halts`, `halted`, `halting`, `E-HALT-QA` or `E-ARCHIVE-BLOCKED` and is not already listed there, so every new or rewritten line in the three refs avoids those words (say "a user-accepted gap" and "stop"), and additions to step 6 of `refs/managed-workspace.md` stay inside the existing single step-6 line. The existing wording "`issues` → STOP `E-ARCHIVE-BLOCKED`" stays verbatim.
- A prompt-builder script, any other lesson in `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`, and the globally installed copy of this skill (it changes when the user runs `superclaude install`) are out of scope.
- Never stage `.claude/` contents. `make sync-dev` copies `src/superclaude/` into `.claude/` only and does not touch `plugins/`, so each task copies its edited ref into the `plugins/` twin by hand, and Task 5 runs `make sync-dev` once after all edits to `src/superclaude/`.
- Installed primitives (the three refs above) must not tell an agent to read anything through a `src/superclaude/...` path.
- In `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/`, only the new file `artifacts/prompt-template-check.md` is added; its prompts, ledger and every other file stay byte-unchanged.
- Scripts and evidence for this plan go under this package's `./artifacts/`.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.


Start sha: 98470602dc2b12406c7066aa84da4ba13bf724f4
Diff against the start snapshot: (git diff 98470602dc2b12406c7066aa84da4ba13bf724f4 -- src/superclaude/skills/sc-implement-protocol/refs/ledger.md plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/ listed after the diff)
diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md b/plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md
index 11998722..a29b85a0 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md
@@ -81,6 +81,10 @@ T<id>: complete verdict=<unchanged-non-compliant-verdict> ac=... evidence=... ex
 
 Legal **only** when a matching `T<id>: Ruling:` line exists above it, after the latest blocked record. Preserve all verdict fields, not only the verdict label. A later blocked record or new start invalidates prior acceptance. A changed accepted finding/outcome requires new user confirmation; do not reuse the old Ruling. Legacy records with a Ruling before the first verdict remain readable; that first complete verdict binds its scope.
 
+## Re-review complete line
+
+After a FINAL flags a saved prompt (`refs/qa.md`, "Defective saved prompt (recovery)"), a re-review with no blocking finding appends the task's `complete` line again with the same verdict fields as its latest `complete` line and no new `start` line. It uses the verdict grammar above by reference, the latest record of the task counts, and it is legal only after a `FINAL:` line. For a compliant task whose re-review wrote new notes lines, the line replaces the `notes@` token. For a task completed after a user-accepted gap (see "Post-ruling complete line"), the line is byte-identical to its latest `complete` line, notes token included, so the accepted gap stays valid; a re-review finding whose unmet check is that accepted gap is not a confirmed blocker (`refs/qa.md`).
+
 ## Retry and halt records
 
 Two kinds for the escalating retry ladder (`refs/retry.md`): one `retry` kind with three steps, and `halt`. They are part of this main grammar, legacy and managed alike.
@@ -234,6 +238,7 @@ Managed ledgers (`<package>/progress.md`) reuse every record above unchanged and
 - A managed `FINAL:` carries the helper's `state=` digest and must be the last record before the helper's own `ARCHIVE: start id=<id> token=<hex>` line. Any later `PLAN`/`T`/`ARCHIVE` record makes it stale: run a new FINAL on every archive attempt. `ARCHIVE: failed id=<id> token=<hex> reason=<code>` records a refused attempt.
 - Legacy `ARCHIVE: Ruling: <what naming T-ids> — <why> — <cost-if-wrong>` records remain readable but are optional. A matching task Ruling is sufficient for ordinary archiving of unchanged accepted work; never demand duplicate approval. Neither form waives FINAL or authorizes commit, PR, merge or release.
 - Resume dispatch for managed packages: location check → pin check → first non-complete task → the per-task resume table (Resume) → all complete = active all-complete → archive gate. "Already complete" is reported only after the helper answers `already-archived`.
+- The re-review `complete` lines of the saved-prompt recovery ("Re-review complete line" above) and the later move of a defective saved prompt to `superseded-prompts/` (`refs/qa.md`, "Defective saved prompt (recovery)") come before the fresh FINAL of the next archive attempt.
 
 ```
 # implement ledger — source: ./TASK-WF-authLogin-20261001-063000.md — created: 2026-10-01T06:30:00Z
diff --git a/src/superclaude/skills/sc-implement-protocol/refs/ledger.md b/src/superclaude/skills/sc-implement-protocol/refs/ledger.md
index 11998722..a29b85a0 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/ledger.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/ledger.md
@@ -81,6 +81,10 @@ T<id>: complete verdict=<unchanged-non-compliant-verdict> ac=... evidence=... ex
 
 Legal **only** when a matching `T<id>: Ruling:` line exists above it, after the latest blocked record. Preserve all verdict fields, not only the verdict label. A later blocked record or new start invalidates prior acceptance. A changed accepted finding/outcome requires new user confirmation; do not reuse the old Ruling. Legacy records with a Ruling before the first verdict remain readable; that first complete verdict binds its scope.
 
+## Re-review complete line
+
+After a FINAL flags a saved prompt (`refs/qa.md`, "Defective saved prompt (recovery)"), a re-review with no blocking finding appends the task's `complete` line again with the same verdict fields as its latest `complete` line and no new `start` line. It uses the verdict grammar above by reference, the latest record of the task counts, and it is legal only after a `FINAL:` line. For a compliant task whose re-review wrote new notes lines, the line replaces the `notes@` token. For a task completed after a user-accepted gap (see "Post-ruling complete line"), the line is byte-identical to its latest `complete` line, notes token included, so the accepted gap stays valid; a re-review finding whose unmet check is that accepted gap is not a confirmed blocker (`refs/qa.md`).
+
 ## Retry and halt records
 
 Two kinds for the escalating retry ladder (`refs/retry.md`): one `retry` kind with three steps, and `halt`. They are part of this main grammar, legacy and managed alike.
@@ -234,6 +238,7 @@ Managed ledgers (`<package>/progress.md`) reuse every record above unchanged and
 - A managed `FINAL:` carries the helper's `state=` digest and must be the last record before the helper's own `ARCHIVE: start id=<id> token=<hex>` line. Any later `PLAN`/`T`/`ARCHIVE` record makes it stale: run a new FINAL on every archive attempt. `ARCHIVE: failed id=<id> token=<hex> reason=<code>` records a refused attempt.
 - Legacy `ARCHIVE: Ruling: <what naming T-ids> — <why> — <cost-if-wrong>` records remain readable but are optional. A matching task Ruling is sufficient for ordinary archiving of unchanged accepted work; never demand duplicate approval. Neither form waives FINAL or authorizes commit, PR, merge or release.
 - Resume dispatch for managed packages: location check → pin check → first non-complete task → the per-task resume table (Resume) → all complete = active all-complete → archive gate. "Already complete" is reported only after the helper answers `already-archived`.
+- The re-review `complete` lines of the saved-prompt recovery ("Re-review complete line" above) and the later move of a defective saved prompt to `superseded-prompts/` (`refs/qa.md`, "Defective saved prompt (recovery)") come before the fresh FINAL of the next archive attempt.
 
 ```
 # implement ledger — source: ./TASK-WF-authLogin-20261001-063000.md — created: 2026-10-01T06:30:00Z

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t3-grep.txt ===
heading lines: 1
no new `start` line => 1
same verdict fields => 1
replaces the `notes@` token => 1
legal only after a `FINAL:` line => 1
--- superseded-prompts/ in the Managed-package extension:
241: [## Managed-package extension (`refs/managed-workspace.md`)] - The re-review `complete` lines of the saved-prompt recovery ("Re-review complete line" a

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t3-grammar-cmp.txt ===
grammar cmp exit=0 lines=12

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t3-srcpath.txt ===
src/superclaude lines: now 0 head 0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t3-cmp.txt ===
twin cmp exit=0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t3-pytest-skills.txt ===
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
SuperClaude: 4.3.5
rootdir: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs
configfile: pyproject.toml
plugins: superclaude-4.3.5, anyio-4.16.0
collected 804 items

tests/skills/test_brainstorm_protocol.py .                               [  0%]
tests/skills/test_codegraph_adoption.py ................................ [  4%]
..................                                                       [  6%]
tests/skills/test_implement_adviser_family.py ...                        [  6%]
tests/skills/test_implement_retry_citation.py .....................      [  9%]
tests/skills/test_implement_retry_revert.py ............................ [ 12%]
..........................                                               [ 16%]
tests/skills/test_implement_severity_replay.py ............              [ 17%]
tests/skills/test_implement_severity_static.py ......................... [ 20%]
...                                                                      [ 21%]
tests/skills/test_primitive_dual_surface_lookup.py ...                   [ 21%]
tests/skills/test_reflect_input_snapshot.py ...............              [ 23%]
tests/skills/test_repo_inventory_nongit.py .....                         [ 23%]
tests/skills/test_review_severity_rule.py .............................. [ 27%]
................................                                         [ 31%]
tests/skills/test_sc_recommend_routing_contract.py ..................... [ 34%]
......                                                                   [ 34%]
tests/skills/test_task_builder_merge.py ................................ [ 38%]
....................................                                     [ 43%]
tests/skills/test_task_workspace_lifecycle.py .......................... [ 46%]
...............................................                          [ 52%]
tests/skills/test_task_workspace_smoke.py ....                           [ 52%]
tests/skills/test_tier2_tavily_consistency.py .....                      [ 53%]
tests/skills/test_worker_contract.py ................................... [ 57%]
........................................................................ [ 66%]
........................................................................ [ 75%]
.................                                                        [ 77%]
tests/skills/test_workflow_archive.py .................................. [ 82%]
........................................................................ [ 91%]
.......................................................................  [100%]

============================= 804 passed in 13.00s =============================

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t3-tests-status.txt ===

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
