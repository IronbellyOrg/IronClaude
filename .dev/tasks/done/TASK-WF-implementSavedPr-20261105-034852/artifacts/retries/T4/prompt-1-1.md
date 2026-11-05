eb0059840a4f2a70880ff84f062f6067f9558d92
Review one task for spec compliance.

Task brief: T4 (AC ids in order of the "Acceptance criteria:" bullets: T4.AC1,T4.AC2,T4.AC3). Plan file: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md, lines 66-76:
## Task 4: Add the recovery trigger and superseded-prompts notes to refs/managed-workspace.md

Depends on: Task 3

In `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`: in section "## Completion: fresh FINAL, then archive", extend step 6 (the single line that begins "6. `pass` → run the helper in archive mode" and ends "`issues` → STOP `E-ARCHIVE-BLOCKED`; the package stays in `to-do/`; do not reopen completed tasks unless the operator says.") in place, keeping it one line and keeping its first 20 characters and the wording "`issues` → STOP `E-ARCHIVE-BLOCKED`" verbatim: add that when every `issues` item of the FINAL concerns a saved prompt (a template difference, a superseded prompt with no later passing saved prompt, or a missing README), the executor runs "Defective saved prompt (recovery)" from `refs/qa.md` in the same invocation and then repeats the archive gate from step 1, that the recovery is idempotent (it finishes a half-done move, writes a missing README and runs a missing re-review), that the stop applies only if the recovery cannot finish or the new FINAL still returns `issues`, and that "do not reopen completed tasks unless the operator says" gains the exception "except the recovery's own re-review of a saved-prompt task". In section "## Ledger, artifacts, pins", add a bullet that a defective saved prompt moved under that recovery lives at `<pkg>/artifacts/superseded-prompts/` with its `README.md`, is moved with an ordinary file move (the helper rule covers packages only) and is never deleted. In section "## Enforcement map", in the row that begins "| saved reviewer prompt", add that blank-line and trailing-whitespace differences are a note and that `superseded-prompts/` holds history the FINAL checks for a `README.md` and a later passing saved prompt. Keep every new line other than step 6 free of the words listed in the second Constraints bullet. Copy the edited file byte for byte to the `plugins/` twin.

Acceptance criteria:
- `grep -n "6. \`pass\` → run the helper" src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` prints one line, and that same line contains "every `issues` item of the FINAL concerns a saved prompt", "idempotent", "except the recovery's own re-review of a saved-prompt task" and "`issues` → STOP `E-ARCHIVE-BLOCKED`"; `grep -n "superseded-prompts/"` prints at least two lines, one in "## Ledger, artifacts, pins" and one in the "## Enforcement map" saved-prompt row, which also says blank-line and trailing-whitespace differences are a note; the grep output is saved in `./artifacts/t4-grep.txt`.
- The number of lines containing `src/superclaude` in `refs/managed-workspace.md` equals that in `git show HEAD:` of the same file (both counts in `./artifacts/t4-srcpath.txt`).
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills -q -p no:cacheprovider` passes with no failures (`./artifacts/t4-pytest-skills.txt`), `git status --porcelain -- tests` shows no entry for `tests/skills/test_implement_severity_static.py` (`./artifacts/t4-tests-status.txt`), and `cmp` of the `src/` and `plugins/` copies of `refs/managed-workspace.md` exits 0 (`./artifacts/t4-cmp.txt`).


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


Start sha: eb0059840a4f2a70880ff84f062f6067f9558d92
Diff against the start snapshot: (git diff eb0059840a4f2a70880ff84f062f6067f9558d92 -- src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/ listed after the diff)
diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md b/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
index 53390b76..d65eab9e 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
@@ -34,6 +34,7 @@ This runs **before** the missing-file check on the invoked path (SKILL.md "Manag
 - Optional delegates (e.g. `sc:adversarial`, `sc:reflect`) get an explicit root below `<pkg>/artifacts/<name>/`; consume only returned paths whose realpath is inside `<pkg>/artifacts/`, else treat them as missing. `sc:adversarial` writes its own `<root>/adversarial/` child (use its returned `artifacts_dir`). Invoke `sc:reflect` only with `--no-promote`: `/sc:implement` is the sole mover. Give `sc:reflect` a fresh dedicated per-run `--output` directory, e.g. `<pkg>/artifacts/reflect/<mode>-<runid>/`: never `<pkg>`, `<pkg>/artifacts`, or a directory holding a report you pass as input (a prior run's folder). Reflect's own input-snapshot exclusion and overlap guard (sc-reflect-protocol `SKILL.md` §4.0 Step 0.4 `REFLECT_OUTPUT_ROOT`) govern; do not restate or reimplement them here. No mandatory heavy review.
 - Run task checks so they leave no stray byproducts (e.g. `PYTHONDONTWRITEBYTECODE=1`); remove caches/temp files a check created before Q2, because Q0 snapshots sweep all non-ignored untracked files.
 - `.dev/tasks/` is always staged (`git add .dev/tasks`): the package, its `progress.md` ledger and `artifacts/` included. Never gitignore it, never leave it untracked, and never write "do not stage" about it in a ledger note or report. Staging is not committing. After the helper moves a package to `done/`, the new path needs `git add .dev/tasks` again.
+- A defective saved prompt moved by the saved-prompt recovery (`refs/qa.md`, "Defective saved prompt (recovery)") lives at `<pkg>/artifacts/superseded-prompts/` with its `README.md`. It is moved with an ordinary file move (the helper rule below covers packages only) and is never deleted.
 - At ledger creation append, right after the header:
 
 ```
@@ -58,7 +59,7 @@ Archive gate, **every attempt** (N=1, resume, retry; an earlier FINAL never coun
 FINAL: <pass|issues> evidence=<ev-list> state=<sha256>
 ```
 
-6. `pass` → run the helper in archive mode (no extra flag). It appends its own `ARCHIVE: start id=<id> token=<hex>` line after FINAL and moves the package; there is no later "complete" record (location is the archive state). `issues` → STOP `E-ARCHIVE-BLOCKED`; the package stays in `to-do/`; do not reopen completed tasks unless the operator says.
+6. `pass` → run the helper in archive mode (no extra flag). It appends its own `ARCHIVE: start id=<id> token=<hex>` line after FINAL and moves the package; there is no later "complete" record (location is the archive state). `issues` → STOP `E-ARCHIVE-BLOCKED`; the package stays in `to-do/`; do not reopen completed tasks unless the operator says, except the recovery's own re-review of a saved-prompt task. Before that stop, when every `issues` item of the FINAL concerns a saved prompt (a template difference, a superseded prompt with no later passing saved prompt, or a missing README), the executor runs "Defective saved prompt (recovery)" from `refs/qa.md` in the same invocation and then repeats the archive gate from step 1; the recovery is idempotent (it finishes a half-done move, writes a missing README and runs a missing re-review), and the stop applies only if the recovery cannot finish or the new FINAL still returns `issues`.
 
 `<skill base>` is the base directory the loaded skill announces (the directory holding this skill's `SKILL.md`); never hardcode a repository `src/` path. A FINAL pass is not a commit, PR, merge, release or human approval.
 
@@ -84,4 +85,4 @@ An existing `.archiving` marker always stops. If a run was killed mid-archive th
 | real direct package under to-do/done, no symlink escape, schema/slug/contract, pins vs disk, every task complete (matching task Ruling for unchanged non-compliant verdict fields), FINAL pass last and bound to the current state digest, no existing marker, no-replace move, recovery token | **executable** (`scripts/archive_workspace.py`, tested in `tests/skills/test_workflow_archive.py`) |
 | concurrent writers on one package, non-cooperating checkout writers | unsupported; not claimed. The retry ladder reverts a non-cooperating writer's edits to files in the task's revert domain; they are kept only in the sweep refs (`refs/retry.md`) |
 | delivery files missing from every ledger `files=` field, and `./artifacts/*` content | not covered by the state digest; only the FINAL reviewer (protocol) can notice stale evidence |
-| saved reviewer prompt (`<retries>/T<id>/prompt-<k>-<j>.md`) matches the reviewer template outside the slots | **protocol** (the FINAL reviewer compares them; no executable check can prove what a prompt contained) |
+| saved reviewer prompt (`<retries>/T<id>/prompt-<k>-<j>.md`) matches the reviewer template outside the slots | **protocol** (the FINAL reviewer compares them; blank-line and trailing-whitespace differences are a note; `superseded-prompts/` holds history that the FINAL checks for a `README.md` and a later passing saved prompt; no executable check can prove what a prompt contained) |
diff --git a/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md b/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
index 53390b76..d65eab9e 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
@@ -34,6 +34,7 @@ This runs **before** the missing-file check on the invoked path (SKILL.md "Manag
 - Optional delegates (e.g. `sc:adversarial`, `sc:reflect`) get an explicit root below `<pkg>/artifacts/<name>/`; consume only returned paths whose realpath is inside `<pkg>/artifacts/`, else treat them as missing. `sc:adversarial` writes its own `<root>/adversarial/` child (use its returned `artifacts_dir`). Invoke `sc:reflect` only with `--no-promote`: `/sc:implement` is the sole mover. Give `sc:reflect` a fresh dedicated per-run `--output` directory, e.g. `<pkg>/artifacts/reflect/<mode>-<runid>/`: never `<pkg>`, `<pkg>/artifacts`, or a directory holding a report you pass as input (a prior run's folder). Reflect's own input-snapshot exclusion and overlap guard (sc-reflect-protocol `SKILL.md` §4.0 Step 0.4 `REFLECT_OUTPUT_ROOT`) govern; do not restate or reimplement them here. No mandatory heavy review.
 - Run task checks so they leave no stray byproducts (e.g. `PYTHONDONTWRITEBYTECODE=1`); remove caches/temp files a check created before Q2, because Q0 snapshots sweep all non-ignored untracked files.
 - `.dev/tasks/` is always staged (`git add .dev/tasks`): the package, its `progress.md` ledger and `artifacts/` included. Never gitignore it, never leave it untracked, and never write "do not stage" about it in a ledger note or report. Staging is not committing. After the helper moves a package to `done/`, the new path needs `git add .dev/tasks` again.
+- A defective saved prompt moved by the saved-prompt recovery (`refs/qa.md`, "Defective saved prompt (recovery)") lives at `<pkg>/artifacts/superseded-prompts/` with its `README.md`. It is moved with an ordinary file move (the helper rule below covers packages only) and is never deleted.
 - At ledger creation append, right after the header:
 
 ```
@@ -58,7 +59,7 @@ Archive gate, **every attempt** (N=1, resume, retry; an earlier FINAL never coun
 FINAL: <pass|issues> evidence=<ev-list> state=<sha256>
 ```
 
-6. `pass` → run the helper in archive mode (no extra flag). It appends its own `ARCHIVE: start id=<id> token=<hex>` line after FINAL and moves the package; there is no later "complete" record (location is the archive state). `issues` → STOP `E-ARCHIVE-BLOCKED`; the package stays in `to-do/`; do not reopen completed tasks unless the operator says.
+6. `pass` → run the helper in archive mode (no extra flag). It appends its own `ARCHIVE: start id=<id> token=<hex>` line after FINAL and moves the package; there is no later "complete" record (location is the archive state). `issues` → STOP `E-ARCHIVE-BLOCKED`; the package stays in `to-do/`; do not reopen completed tasks unless the operator says, except the recovery's own re-review of a saved-prompt task. Before that stop, when every `issues` item of the FINAL concerns a saved prompt (a template difference, a superseded prompt with no later passing saved prompt, or a missing README), the executor runs "Defective saved prompt (recovery)" from `refs/qa.md` in the same invocation and then repeats the archive gate from step 1; the recovery is idempotent (it finishes a half-done move, writes a missing README and runs a missing re-review), and the stop applies only if the recovery cannot finish or the new FINAL still returns `issues`.
 
 `<skill base>` is the base directory the loaded skill announces (the directory holding this skill's `SKILL.md`); never hardcode a repository `src/` path. A FINAL pass is not a commit, PR, merge, release or human approval.
 
@@ -84,4 +85,4 @@ An existing `.archiving` marker always stops. If a run was killed mid-archive th
 | real direct package under to-do/done, no symlink escape, schema/slug/contract, pins vs disk, every task complete (matching task Ruling for unchanged non-compliant verdict fields), FINAL pass last and bound to the current state digest, no existing marker, no-replace move, recovery token | **executable** (`scripts/archive_workspace.py`, tested in `tests/skills/test_workflow_archive.py`) |
 | concurrent writers on one package, non-cooperating checkout writers | unsupported; not claimed. The retry ladder reverts a non-cooperating writer's edits to files in the task's revert domain; they are kept only in the sweep refs (`refs/retry.md`) |
 | delivery files missing from every ledger `files=` field, and `./artifacts/*` content | not covered by the state digest; only the FINAL reviewer (protocol) can notice stale evidence |
-| saved reviewer prompt (`<retries>/T<id>/prompt-<k>-<j>.md`) matches the reviewer template outside the slots | **protocol** (the FINAL reviewer compares them; no executable check can prove what a prompt contained) |
+| saved reviewer prompt (`<retries>/T<id>/prompt-<k>-<j>.md`) matches the reviewer template outside the slots | **protocol** (the FINAL reviewer compares them; blank-line and trailing-whitespace differences are a note; `superseded-prompts/` holds history that the FINAL checks for a `README.md` and a later passing saved prompt; no executable check can prove what a prompt contained) |

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t4-grep.txt ===
step 6 lines matching: 1
step 6 starts at: 62; first 20 chars: [6. `pass` → run th]
every `issues` item of the FINAL concerns a saved prompt => 1
idempotent => 1
except the recovery's own re-review of a saved-prompt task => 1
`issues` → STOP `E-ARCHIVE-BLOCKED` => 1
--- superseded-prompts/ by section:
37: [## Ledger, artifacts, pins] - A defective saved prompt moved by the saved-prompt recovery (`refs/qa.md`, "De
88: [## Enforcement map] | saved reviewer prompt (`<retries>/T<id>/prompt-<k>-<j>.md`) matches the review
enforcement row has 'blank-line and trailing-whitespace differences are a note': 1

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t4-srcpath.txt ===
src/superclaude lines: now 0 head 0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t4-cmp.txt ===
twin cmp exit=0

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t4-pytest-skills.txt ===
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

============================= 804 passed in 13.11s =============================

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t4-tests-status.txt ===

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
