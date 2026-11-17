96bd45a9a5ce08ca1b338f2a3f3ff657c9e87bac
Review one task for spec compliance.

Task brief: Task 2 of the plan .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md (AC ids T2.AC1 to T2.AC7 in source order).
## Task 2: Add the print-only follow-up paragraph to the final review step

Depends on: Task 1

Before editing, record the SHA-256 of `src/superclaude/skills/sc-implement-protocol/refs/qa.md` and of its plugin twin `plugins/superclaude/skills/sc-implement-protocol/refs/qa.md` in `./artifacts/qa-md-sha256-before.txt` (two lines; equal today). Then read `src/superclaude/skills/sc-implement-protocol/SKILL.md` (the "Done" section and the "Whole-list review" section), `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (the archive gate, steps 1 to 6) and `refs/qa.md` (the notes-file definition: line 1 holds the `start` sha, lines 2 to m are the live lines, lines after m begin with `superseded `; and the closed list of interrupts), and edit only the first two files.

In `SKILL.md` "Done", add one paragraph that begins with the bold title **Follow-up print (record and print only).** (the word "sweep" is not used). The paragraph says that at the final review step the executor prints every non-superseded minor line of every task's `<retries>/T<id>/notes.md` (lines 2 to m, the lines the Done section already counts) and runs the safety scan over each notes file, holding the call as a fenced code block of exactly one line, so the call sits on its own physical line apart from the prose: `superclaude review safety-scan <notes file>`. A scan hit prints first, before the minor lines, and stays blocking; it is not turned into a follow-up. A task whose notes file is missing prints the line "no notes file for T<id>" (a clean task writes no notes file, so the line says only that no file exists, never that nothing was found). A legacy run adds the scan to the printing the Done section already does for it; a managed package prints and scans in the archive gate of `refs/managed-workspace.md`, so each run prints once. The paragraph states that the step asks the user nothing ("It asks the user nothing"), makes no offer (the offer is the top-level session's), changes no verdict, no final-review result and no archive outcome, adds no stop code, and that a missing `superclaude` command or a non-zero exit is printed as one line and the run continues.

In `refs/managed-workspace.md`, add one paragraph with the same bold title and the same one-line code block (so each file holds the call once) between the closing fence of the code block that holds the line `FINAL: <pass|issues> evidence=<ev-list> state=<sha256>` and the line that begins "6. `pass`": it says that on a final review that appended `FINAL: pass` the executor prints the follow-up lines and runs the scan before the helper moves the package, and on `FINAL: issues` it does neither; what is printed and the "no notes file" line are the ones of `SKILL.md`. Do not renumber the steps and do not change any existing line. Then run `make sync-dev` and copy the two edited files byte for byte to `plugins/superclaude/skills/sc-implement-protocol/SKILL.md` and `plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` with `cp`.

The existing tests that pin this text and must stay green: `tests/skills/test_implement_severity_static.py` (its site scan flags any new line that holds the words halt, Ruling, `E-HALT-QA` or `E-ARCHIVE-BLOCKED`, and its allow-list pins the step 2, step 3 and step 6 lines of the archive gate), `tests/skills/test_review_severity_rule.py` (the byte-equal twin test, the old cap wording scan and the sweep-phrase patterns), `tests/skills/test_task_workspace_lifecycle.py` (no cross-file line pointers, the location-resolution rows), `tests/skills/test_task_workspace_smoke.py`, `tests/skills/test_workflow_archive.py`, `tests/skills/test_implement_saved_prompt_rule.py`, `tests/skills/test_reflect_input_snapshot.py` (the managed-workspace mirror), `tests/skills/test_codegraph_adoption.py` and `tests/commands/test_impact_command.py` (both read `SKILL.md`), `tests/skills/test_worker_contract.py` (the git-word scan of these files), `tests/unit/test_cli_install.py` (the installed file lists), and three more tests that name the skill: `tests/skills/test_implement_retry_revert.py`, `tests/skills/test_implement_retry_citation.py` and `tests/skills/test_implement_adviser_family.py`. All fourteen files were found with `test -e` when this plan was generated; re-check before running.

Acceptance criteria:
- `sha256sum` of `refs/qa.md` in both trees equals the two lines of `./artifacts/qa-md-sha256-before.txt`, and `git diff --stat HEAD -- src/superclaude/skills/sc-implement-protocol/refs/qa.md plugins/superclaude/skills/sc-implement-protocol/refs/qa.md` prints nothing.
- In `refs/managed-workspace.md` the new paragraph sits after the closing fence of the code block that holds the line `FINAL: <pass|issues> evidence=<ev-list> state=<sha256>` and before the line that begins "6. `pass` → run the helper in archive mode"; the line that begins "5. Re-run step 3.", the step 6 line and the line "2. `--skip-final-review` → no FINAL and no archive" are unchanged.
- Both files carry the bold title "Follow-up print (record and print only)." on the first line of the new paragraph. `grep -c "superclaude review safety-scan" src/superclaude/skills/sc-implement-protocol/SKILL.md src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` prints 1 for each file, the matching line in each file is a line of a fenced code block, and the sentence "It asks the user nothing" appears in `SKILL.md`. The word "sweep" appears in no added line.
- Both files hold the printed line "no notes file for T<id>", tied to a missing notes file, and `SKILL.md` states that a scan hit prints first and stays blocking.
- `git diff -U0 HEAD -- src/superclaude/skills/sc-implement-protocol | grep '^+' | grep -E "\bhalt(s|ed|ing)?\b|E-HALT-QA|E-ARCHIVE-BLOCKED|\bRuling\b"` prints nothing, and the same added lines contain no question mark.
- Active-flow smoke check, recorded in `./artifacts/print-smoke.txt`: in a temporary folder with two task folders, `T1/notes.md` (line 1 a sha, one live minor line holding the word `delete`, one line beginning `superseded `) and no notes file for `T2`, following the added paragraph step by step yields a non-empty printed list for T1 that holds the live line and not the `superseded ` line, one `SAFETY HIT` line printed before that list, and the line `no notes file for T2`.
- `uv run pytest tests/skills/test_implement_severity_static.py tests/skills/test_review_severity_rule.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_task_workspace_smoke.py tests/skills/test_workflow_archive.py tests/skills/test_implement_saved_prompt_rule.py tests/skills/test_reflect_input_snapshot.py tests/skills/test_codegraph_adoption.py tests/commands/test_impact_command.py tests/skills/test_worker_contract.py tests/unit/test_cli_install.py tests/skills/test_implement_retry_revert.py tests/skills/test_implement_retry_citation.py tests/skills/test_implement_adviser_family.py -v` passes, and `make verify-sync` reports no difference.
- `cmp` shows the two plugin twin files equal to their sources, and `git diff --stat HEAD -- plugins` lists only those two plugin files.

Global constraints:
## Constraints

- Spec and cuts: the merged spec `02-brainstorm/merged-requirements.md` and the cuts list `cuts-debate/final-cuts.md` both sit inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF. The cuts list is authoritative where it differs from the earlier stage requests (revision 4 of the source says so); the rows C1 to C4, C7 and C10 of its section (a) decide what this package builds. Section numbers, requirement ids (REQ-nn) and guardrails (GR1, GR12) refer to the spec.
- One package, two tasks. This is stage 1 of four packages (stages 0, 1, 3 and 4); stage 2 is withdrawn into this package and has no package of its own. The package adds new files only (the scan module, its command module and their tests) and edits exactly three existing files: `src/superclaude/cli/review/__init__.py` (one name added to the tuple of subcommand modules, Task 1) and `SKILL.md` and `refs/managed-workspace.md` of the `sc-implement-protocol` skill (Task 2), plus the two plugin twins of those skill files. It edits no other review-loop carrier. It runs only after the owner has said go for stage 1 in chat and the go is recorded in the stage ledger `stage-requests/README.md` in PF (Task 1 checks that). Stage 3 starts only after this package is done, as its own entry check reads.
- Depth. The source's revision 4 says this package has two tasks in two phases and `depth: quick`; the program gate checker that requires `depth: standard` and 4 to 8 phases fails it for that reason only. The owner chose `quick` in chat on 2026-11-16.
- Not built (cuts rows C1, C2, C3, C4 and C10): the follow-up ledger and its codec, the classifier and its inputs supplier, the carrier registry and scale map, the new skill folder and its references, the install check for digest versions, the registry drift tests, the owner summary file, the sweep and the shadow stage. Nothing here reads, writes or names any of them, and no stored tag for a safety hit exists: the scan only prints.
- Also not built: any Jev or other external judge call, key or account (owner decision OD3 stays open; no finding text leaves the machine); any edit of `src/superclaude/skills/sc-implement-protocol/refs/qa.md` or its plugin twin (it keeps its own scale, and its final summary "never asks the user anything"); any edit of `src/superclaude/cli/review/ledger.py`, `WORKER-CONTRACT.md` or the own-scale primitives; code-assigned severity in `src/superclaude/cli/**/*.py`, with one exception: the safety-only raise function of the new `src/superclaude/cli/review/safety_route.py` (the GR12 raise-only rule of Task 1, which promotes a row with a safety hit to Blocking and never lowers an outcome) is built; any change to the cap of 2 fix cycles.
- Retired carriers stay unedited. `/sc:task` and task-builder are being retired (owner, 2026-11-16): no task edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`.
- Plugin surface. IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin, so this package creates no plugin surface. The one existing hand-kept twin it touches is `plugins/superclaude/skills/sc-implement-protocol/`, and only its two files `SKILL.md` and `refs/managed-workspace.md`, because `test_h_implement_protocol_plugin_twins_byte_equal` in `tests/skills/test_review_severity_rule.py` pins them byte for byte to their sources. The owner has not confirmed removing plugin parity (the program's open-questions file, section 3.4); this plan does not decide it.
- Carrier choice. The owner approved the final review step of `/sc:implement` as the follow-up carrier, "record and print only". The once-per-run offer question stays with the top-level session through the output style, so the added paragraph asks the user nothing, makes no offer and adds no stop code.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. New text added to installed primitives avoids the words the static scans pin (the halt, stop and ruling words of `tests/skills/test_implement_severity_static.py`, the old cap wording and the sweep-phrase patterns of `tests/skills/test_review_severity_rule.py`) and cites no `SKILL.md:<number>` style pointer.
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; keep everything under the project `.claude/` folder out of `git add` (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...` and `uv run python ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes tells a reader to keep `.dev/tasks/` out of `git add`. Staging is not committing.

Start sha: 96bd45a9a5ce08ca1b338f2a3f3ff657c9e87bac

Diff against the start snapshot:
```diff
diff --git a/plugins/superclaude/skills/sc-implement-protocol/SKILL.md b/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
index 7dbbefaa6..b421ba0df 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
@@ -191,6 +191,14 @@ Extra `fail` does not change the spec verdict. A task MUST NOT be marked `compli
 
 Every enumerable task has a `complete` ledger line (verdict `compliant`, or non-compliant plus operator Ruling). Print the ledger path. A `compliant` line may carry a `notes@` token (complete with notes, `refs/qa.md`). When no FINAL that can block ran (any legacy run, including N=1 and `--skip-final-review`), the final summary also prints lines 2 to m of each task's notes file with their checklist answers, informational only, asking the user nothing. The final summary also prints every `family-fallback:` header line of an `advice-3-b.md` (`refs/retry.md`, Model ladder). Suggest `/sc:test` and `/sc:git` only as optional next steps, not gates.
 
+**Follow-up print (record and print only).** At the final review step the executor prints every non-superseded minor line of every task's `<retries>/T<id>/notes.md` (lines 2 to m, the lines counted above) and runs the safety scan over each notes file with this call:
+
+```
+superclaude review safety-scan <notes file>
+```
+
+A scan hit prints first, before the minor lines, and stays blocking; it is not turned into a follow-up. A task whose notes file is missing prints the line "no notes file for T<id>" (a clean task writes no notes file, so that line says only that no file exists, never that nothing was found). A legacy run adds the scan to the printing described above; a managed package prints and scans in its archive gate, so each run prints once. It asks the user nothing, makes no offer (the offer belongs to the top-level session), and changes no verdict, no final-review result and no archive outcome. It adds no stop code: a missing `superclaude` command or a non-zero exit is printed as one line and the run continues.
+
 Legacy: if all tasks already `complete` on invoke: STOP `already complete: <ledger path>`.
 
 Managed: done means the helper reported `archived` (print its actual `done/` path) or `already-archived`. All tasks complete but not archived is **archive-blocked**, not complete.
diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md b/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
index 4454b7268..d970bdf7d 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
@@ -59,6 +59,14 @@ Archive gate, **every attempt** (N=1, resume, retry; an earlier FINAL never coun
 FINAL: <pass|issues> evidence=<ev-list> state=<sha256>
 ```
 
+**Follow-up print (record and print only).** When the final review appended `FINAL: pass`, the executor prints the follow-up lines and runs the safety scan before the helper moves the package, with this call:
+
+```
+superclaude review safety-scan <notes file>
+```
+
+On `FINAL: issues` it does neither. What is printed, and the "no notes file for T<id>" line, are the ones the Done section of the skill describes.
+
 6. `pass` → run the helper in archive mode (no extra flag). It appends its own `ARCHIVE: start id=<id> token=<hex>` line after FINAL and moves the package; there is no later "complete" record (location is the archive state). `issues` → STOP `E-ARCHIVE-BLOCKED`; the package stays in `to-do/`; do not reopen completed tasks unless the operator says, except the recovery's own re-review of a saved-prompt task. Before that stop, when every `issues` item of the FINAL concerns a saved prompt (a template difference, a superseded prompt with no later passing saved prompt, or a missing README), the executor runs "Defective saved prompt (recovery)" from `refs/qa.md` in the same invocation and then repeats the archive gate from step 1; the recovery is idempotent (it finishes a half-done move, writes a missing README and runs a missing re-review), and the stop applies only if the recovery cannot finish or the new FINAL still returns `issues`.
 
 `<skill base>` is the base directory the loaded skill announces (the directory holding this skill's `SKILL.md`); never hardcode a repository `src/` path. A FINAL pass is not a commit, PR, merge, release or human approval.
diff --git a/src/superclaude/skills/sc-implement-protocol/SKILL.md b/src/superclaude/skills/sc-implement-protocol/SKILL.md
index 7dbbefaa6..b421ba0df 100644
--- a/src/superclaude/skills/sc-implement-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-implement-protocol/SKILL.md
@@ -191,6 +191,14 @@ Extra `fail` does not change the spec verdict. A task MUST NOT be marked `compli
 
 Every enumerable task has a `complete` ledger line (verdict `compliant`, or non-compliant plus operator Ruling). Print the ledger path. A `compliant` line may carry a `notes@` token (complete with notes, `refs/qa.md`). When no FINAL that can block ran (any legacy run, including N=1 and `--skip-final-review`), the final summary also prints lines 2 to m of each task's notes file with their checklist answers, informational only, asking the user nothing. The final summary also prints every `family-fallback:` header line of an `advice-3-b.md` (`refs/retry.md`, Model ladder). Suggest `/sc:test` and `/sc:git` only as optional next steps, not gates.
 
+**Follow-up print (record and print only).** At the final review step the executor prints every non-superseded minor line of every task's `<retries>/T<id>/notes.md` (lines 2 to m, the lines counted above) and runs the safety scan over each notes file with this call:
+
+```
+superclaude review safety-scan <notes file>
+```
+
+A scan hit prints first, before the minor lines, and stays blocking; it is not turned into a follow-up. A task whose notes file is missing prints the line "no notes file for T<id>" (a clean task writes no notes file, so that line says only that no file exists, never that nothing was found). A legacy run adds the scan to the printing described above; a managed package prints and scans in its archive gate, so each run prints once. It asks the user nothing, makes no offer (the offer belongs to the top-level session), and changes no verdict, no final-review result and no archive outcome. It adds no stop code: a missing `superclaude` command or a non-zero exit is printed as one line and the run continues.
+
 Legacy: if all tasks already `complete` on invoke: STOP `already complete: <ledger path>`.
 
 Managed: done means the helper reported `archived` (print its actual `done/` path) or `already-archived`. All tasks complete but not archived is **archive-blocked**, not complete.
diff --git a/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md b/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
index 4454b7268..d970bdf7d 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md
@@ -59,6 +59,14 @@ Archive gate, **every attempt** (N=1, resume, retry; an earlier FINAL never coun
 FINAL: <pass|issues> evidence=<ev-list> state=<sha256>
 ```
 
+**Follow-up print (record and print only).** When the final review appended `FINAL: pass`, the executor prints the follow-up lines and runs the safety scan before the helper moves the package, with this call:
+
+```
+superclaude review safety-scan <notes file>
+```
+
+On `FINAL: issues` it does neither. What is printed, and the "no notes file for T<id>" line, are the ones the Done section of the skill describes.
+
 6. `pass` → run the helper in archive mode (no extra flag). It appends its own `ARCHIVE: start id=<id> token=<hex>` line after FINAL and moves the package; there is no later "complete" record (location is the archive state). `issues` → STOP `E-ARCHIVE-BLOCKED`; the package stays in `to-do/`; do not reopen completed tasks unless the operator says, except the recovery's own re-review of a saved-prompt task. Before that stop, when every `issues` item of the FINAL concerns a saved prompt (a template difference, a superseded prompt with no later passing saved prompt, or a missing README), the executor runs "Defective saved prompt (recovery)" from `refs/qa.md` in the same invocation and then repeats the archive gate from step 1; the recovery is idempotent (it finishes a half-done move, writes a missing README and runs a missing re-review), and the stop applies only if the recovery cannot finish or the new FINAL still returns `issues`.
 
 `<skill base>` is the base directory the loaded skill announces (the directory holding this skill's `SKILL.md`); never hardcode a repository `src/` path. A FINAL pass is not a commit, PR, merge, release or human approval.
diff --git a/.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/artifacts/qa-md-sha256-before.txt b/.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/artifacts/qa-md-sha256-before.txt
new file mode 100644
index 000000000..2411decfc
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/artifacts/qa-md-sha256-before.txt
@@ -0,0 +1,2 @@
+93e232f5d49207624c24da25bc6f2e9a0686b4f7f7ca99a38e4b95f56edaf004
+93e232f5d49207624c24da25bc6f2e9a0686b4f7f7ca99a38e4b95f56edaf004
diff --git a/.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/artifacts/print-smoke.txt b/.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/artifacts/print-smoke.txt
new file mode 100644
index 000000000..a3a13350e
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/artifacts/print-smoke.txt
@@ -0,0 +1,20 @@
+## Task 1 smoke: clean file
+$ superclaude review safety-scan <clean file>
+safety-scan: 2 rows read, 0 skipped, 0 hits
+exit=0
+
+## Task 1 smoke: missing path
+$ superclaude review safety-scan <missing file>
+safety-scan: cannot read <tmp>/missing.md: no such file
+exit=2
+
+## Task 2 smoke: follow-up print over a temporary folder (T1 has notes.md, T2 has none)
+--- T1
+$ superclaude review safety-scan <T1 notes file>
+SAFETY HIT line 2 (delete), graded blocking: A1 r1-1 F1.1 minor src/x.py:3 ac=T1.AC1 n,n,n,n the recipe will delete the cache folder
+safety-scan: 2 rows read, 1 skipped, 1 hits
+Show these rows to the person before they are treated as follow-ups.
+printed minor lines (lines 2 to m, non-superseded):
+A1 r1-1 F1.1 minor src/x.py:3 ac=T1.AC1 n,n,n,n the recipe will delete the cache folder
+--- T2
+no notes file for T2
```

Codegraph context
index_state: fresh
checked_at: 2026-11-17T00:06:11Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: none; the change is added prose in two skill files and their plugin copies. The test run of the 14 files named in the task passed (1503 passed), make verify-sync reported all components in sync, and cmp shows the plugin copies equal to their sources (recorded by the orchestrator, not evidence you must trust; re-check from the live files).

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
