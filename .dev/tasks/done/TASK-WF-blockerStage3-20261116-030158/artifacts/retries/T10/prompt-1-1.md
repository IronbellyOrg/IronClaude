1dbf6f3fb3ae5d66965413793667c593d0833bb4
Review one task for spec compliance.

Task brief: Task 10 of the plan .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md (AC ids T10.AC1 to T10.AC3 in source order).
## Task 10: Write the stage 3 note for the owner

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9

Write `./artifacts/stage3-summary-for-owner.md`, short, with these parts. First re-run the commands of Tasks 1, 7, 8 and 9 and record each pytest summary line in it.

- RT1, quoted from the RT1 row of spec section 13.2 as stage 0 (its errata task) rewords it: "any real blocker found in a Medium list". Read the live row first; when it does not hold those words, the task fails (the stage 0 edit is missing) and the note is not written. The note says that RT1 is a single event that needs no sample size and acts through the safety rollback below.
- What the owner does after the switch: read the Medium lists of the first five runs (the reviewers' `follow-up candidates` sections and the `notes.md` print at the end of `/sc:implement`) and say in chat whether any real blocker sits in them. Say that the stage 4 go needs that statement and that RT1 did not trip.
- One small planted-defect check, run as part of the live RT1 audit after the switch: plant a few known defects of the Decision, Missing and Safety kinds in one small deliverable, have one fresh review run on it, and confirm each is graded Blocking. It is not a build task and no script is written. State that it covers what the stage 0 regrade cannot (the regrade is a lower bound and cannot measure discovery).
- The safety rollback: restore the listed files from the commit before this package's change, and remove the files this package created (`src/superclaude/cli/review/fixcheck.py`, `fixcheck_cmd.py`, `tests/review/test_review_fixcheck.py` and `tests/skills/test_review_old_rule_scan.py`; also take `"fixcheck_cmd"` out of the tuple in `src/superclaude/cli/review/__init__.py`) (list the files to restore by path: `src/superclaude/output-styles/pragmatic.md`, the ten `S1_S3_FILES` carriers, `src/superclaude/agents/rf-analyst.md`, `src/superclaude/cli/review/__init__.py` with `fixcheck.py` and `fixcheck_cmd.py` and their test, the re-pinned tests under `tests/skills` and `tests/audit`, the two fixtures and their plan tables, and `tests/skills/test_review_old_rule_scan.py`), run `make sync-dev`, then refresh each machine as in the next part.
- The refresh line: `make sync-dev` does not copy output styles, so the installed `~/.claude/output-styles/pragmatic.md` stays old until the owner refreshes it. Name the command, `superclaude install --force` (run from an install that holds this change; `install_output_styles` in `src/superclaude/cli/install_user_setup.py` takes the `force` flag and reports files it keeps), and the check that it worked: `grep -c "asks the user once per run, and again at any escalation halt" ~/.claude/output-styles/pragmatic.md` prints 1. Run that check now, read-only, record what it prints on this machine and say plainly that the new rule is not live on a machine until it prints 1.
- End with the sentence that the owner's go for stage 4 is given in chat and not by this file.

Acceptance criteria:
- `./artifacts/stage3-summary-for-owner.md` quotes RT1 with the words "any real blocker found in a Medium list" (`grep -c` prints 1 or more) and the same words are in the live spec row, lists the tests re-pinned with their observed pytest summary lines, and holds the first-five-runs read, the planted-defect check, the rollback file list and the refresh line.
- The note records the observed output of the `grep -c` on the installed style and states the new rule is live on a machine only when it prints 1.
- The note ends with the sentence that the owner's go for stage 4 is given in chat and not by this file.

Global constraints:
## Constraints

- Spec and cuts: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), revert triggers (RT1 to RT8) and owner decisions (OD1 to OD17) refer to the spec. The cuts that shaped this plan are in `cuts-debate/final-cuts.md` in PF (rows C1 to C14, the S3 table of its section (b), the cross-package facts of its section (c)); where that file and the spec disagree about scope, the cuts file wins. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger `stage-requests/README.md` in PF), found by that folder name in the to-do or done subfolder of the repository task folder. The stage 0 package is `TASK-WF-blockerStage0-20261116-021044` and the stage 1 package `TASK-WF-blockerStage1-20261116-030154`. The stage 2 package is withdrawn: its one survivor, the `/sc:implement` print, is task 2 of the stage 1 package.
- One package, one stage. This is stage 3 of the packages that remain (stage 0, stage 1, this one, stage 4). It changes the live review rule. Entry check, read from files and not from memory: the stage 0 package's `./artifacts/stage0c-regrade.md` exists; the stage 1 package is done (it is in the done subfolder of the repository task folder, or it is in the to-do subfolder with a `complete` line for every task in its `progress.md` and a latest `FINAL:` line that reads `FINAL: pass`); the stage 0 errata task has reworded the spec's RT1 row to read "any real blocker found in a Medium list" (`grep -c -F "any real blocker found in a Medium list"` over the spec prints 1 or more; Task 10 quotes it); the stage 3 row of `stage-requests/README.md` in PF holds the owner's go with a date (the go is a chat message recorded there by the session that received it; no hash and no line ruling are part of it). Task 1 runs this check before it creates any file under `src/` or `tests/`, and Task 2 runs it again before the first rule-file edit. A failed check stops the task before any edit and halts the run for the owner. While the check fails, no fix pass, repair, retry or adviser step edits a file under `src/`, `tests/` or `plugins/`, and the acceptance lines of that task that describe the edit do not apply. No task edits the ledger row. Stage 4 starts only after the owner has read the first five runs' Medium lists after the switch and RT1 did not trip (the stage 3 note says how), and the owner's go in chat.
- Limit of what this package shows. The stage 0 regrade is a lower bound: it regrades findings that were already supplied and cannot measure whether a reviewer would have found a defect. The stage 0 result, as its control test supports it, is only that the new text does not change grades on a table already filed as blocking (310 of 318 stay blocking under both texts, 82 of 82 panel blockers kept); both arms carried the old rule through the same hook, so no task here and no sentence of the Task 10 note cites that regrade as evidence that the new text works. No seeded-defect experiment is run here (the earlier one was confounded: both arms carried the old output style through the SubagentStart hook). What covers discovery is RT1 (spec section 13.2) read by the owner on the first five runs' Medium lists and one small planted-defect check run as part of the live RT1 audit after the switch; both go into the Task 10 note and neither is a build task.
- Owner decisions use the spec's recommendations unless the owner changes them, and none of them is converted into an owner answer here: OD1 no new skill folder, the S1 to S5 bullets of `pragmatic.md` are the one source; OD2 the Medium offer once per run plus at any escalation halt; OD9 reviewer-named consumer; OD11 replace label-max merging, staged (this stage the three agents; the rest is stage 4); OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD16 option (b) for Rule 6 of `rf-qa-qualitative.md`. OD3 (finding text leaving the machine) is open and no task depends on its answer; OD4 stands (no classifier in version 1).
- Retired carriers are not edited. The owner is retiring `/sc:task` and the task-builder: no task here edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`. Tests that exist only to pin those files are not re-pinned here; where one test pins both a retired and an active carrier, only the active carrier's part is re-pinned.
- Follow-up list. The list of minors is the reviewers' own `follow-up candidates` section plus each task's `notes.md`; no list file, codec, sweep or registry is built. The stage 1 package prints that list at the end of `/sc:implement` (one paragraph titled "Follow-up print (record and print only).", command `superclaude review safety-scan`). This package edits no `sc-implement-protocol` file, no plugin file and no `refs/qa.md`. The once-per-run offer question stays with the top-level session through the output style (the Medium rule of `pragmatic.md`, changed from per loop to per run in Task 2), so no command gains a question.
- Plugin surface. IronClaude is installed from the Coder template or from a clone plus `superclaude install`, not as a plugin, so this package edits nothing under `plugins/` and creates no plugin mirror, parity test or plugin registry row. `src/superclaude/commands/spec-panel.md` and its plugin twin keep their "once per loop" wording, pinned by `tests/skills/test_review_severity_mapping.py`, `tests/skills/test_review_loop_extension.py` and `tests/skills/test_spec_panel_review_loop.py`; that wording moves in stage 4.
- Not built here: no classifier (`superclaude review classify` does not exist), no follow-up list file or `follow-ups` command group, no `sc-review-severity` skill folder, scale map, carrier registry, doctor check or registry drift test, no seeded-recall run, hash-bound owner ruling, shadow stage or baseline file, no Jev or other external judge call, no change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), to `src/superclaude/cli/review/ledger.py` or `review-ledger/1`, to the own-scale primitives of spec section 9.3, to code-assigned severity in `src/superclaude/cli/**/*.py`, to the cap of 2 fix cycles, or to the 35 percent target. Stage 4 edits the doubt wording and the merge text of the templates and rule prompts; this package only copies the S1 to S3 and S5 bullets into the ten tuple files (Task 3).
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev` (it copies skills, agents, commands, hooks and templates; it does not copy `output-styles/`, `core/` or `rules/`). The installed `~/.claude/output-styles/pragmatic.md` therefore changes only at a refresh (Task 10 says how). Staging anything under the project `.claude/` folder is forbidden (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Kept mechanical gates (fixed FAIL triggers that stay as named gates) are recorded in the editing task's own `./artifacts/kept-mechanical-gates.md`, one bullet per gate: path relative to `src/superclaude/`, the gate's quoted words, the condition it maps to (the Missing condition of the digest), the reason. No `refs/scale-map.md` exists and none is created.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is left out of staging. Staging is not committing.

Start sha: 1dbf6f3fb3ae5d66965413793667c593d0833bb4

Diff against the start snapshot:
```diff
diff --git a/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/stage3-summary-for-owner.md b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/stage3-summary-for-owner.md
new file mode 100644
index 000000000..7197bb018
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/stage3-summary-for-owner.md
@@ -0,0 +1,48 @@
+# Stage 3 note for the owner (issue #552), written 2026-11-17
+
+## What changed
+
+The review rule in `src/superclaude/output-styles/pragmatic.md` now grades a finding by what changes if the flawed text is corrected (Decision, Missing, Safety are the only things that block). The same text is copied into ten carrier files (`rf-qa.md`, `rf-qa-qualitative.md`, two document templates, two workflow templates, four rule prompts). `rf-qa.md`, `rf-qa-qualitative.md` and `rf-analyst.md` were rewritten so they no longer fail a review by label. A new command `superclaude review fixcheck` runs mechanical checks over the lines a fix pass edited. The Medium offer now happens once per run and again at any escalation halt.
+
+## Tests re-run for this note (observed 2026-11-17)
+
+- Task 1: `uv run pytest tests/review/test_review_fixcheck.py tests/review/test_review_cli.py` gave `25 passed in 0.43s`.
+- Task 7: `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_implement_severity_static.py tests/skills/test_review_loop_extension.py tests/skills/test_review_prompt_overrides.py tests/skills/test_spec_panel_review_loop.py tests/skills/test_task_builder_merge.py tests/review/test_review_rules_text.py` gave `274 passed in 4.34s`. Re-pinned: the Medium pin in `test_review_severity_mapping.py` and the S2 pin in `test_implement_severity_static.py`.
+- Task 8: `uv run pytest tests/audit` gave `1159 passed, 1 skipped, 5 warnings in 3.97s`. Re-pinned: the PASS and FAIL bullets in `test_nfr_conv_9_zero_trust.py`, and the Rule 6 text and block hash in `test_severity_floor_unweakened.py`.
+- Task 9: `uv run pytest tests/skills/test_review_old_rule_scan.py` gave `4 passed in 0.13s`.
+
+## What this package does not show
+
+The stage 0 regrade is a lower bound. It regrades findings that were already filed as blocking, and it cannot show whether a reviewer would have found a defect. Its result, as its control test supports it, is only that the new text does not change grades on a table already filed as blocking (310 of 318 stay blocking under both texts, 82 of 82 panel blockers kept). Both arms carried the old rule through the same hook. Nothing in this note cites that regrade as evidence that the new text works. No seeded-defect experiment was run here.
+
+## RT1 (the revert trigger)
+
+The RT1 row of spec section 13.2 reads "Any real blocker found in a Medium list" (live spec line 988; `grep -c -i -F "any real blocker found in a Medium list"` prints 1). The words are the plan's, with a capital A in the spec. RT1 is a single event. It needs no sample size and acts through the safety rollback below.
+
+## What you do after the switch
+
+1. Let the first five runs finish. In each, read the Medium lists: the reviewers' `follow-up candidates` sections and the `notes.md` print at the end of `/sc:implement`.
+2. Say in chat whether any real blocker sits in them.
+3. The stage 4 go needs that statement and that RT1 did not trip.
+
+## One small planted-defect check (part of the live RT1 audit, not a build task)
+
+After the switch, plant a few known defects of the Decision, Missing and Safety kinds in one small deliverable (for example a wrong number an acceptance check uses, a required section left out, and a command that deletes data), run one fresh review on it, and confirm each is graded Blocking. No script is written. It covers what the stage 0 regrade cannot, because the regrade is a lower bound and cannot measure discovery.
+
+## The safety rollback
+
+Restore these files from the commit before this package's change, remove the files this package created, take `"fixcheck_cmd"` out of the tuple in `src/superclaude/cli/review/__init__.py`, run `make sync-dev`, then refresh each machine as in the next part.
+
+Restore: `src/superclaude/output-styles/pragmatic.md`; the ten carriers `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/templates/documents/agent_template_qa.md`, `src/superclaude/templates/documents/skill_template.md`, `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md`, `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` and the four `src/superclaude/rules/prompts/*_qa_prompt.md` files; `src/superclaude/agents/rf-analyst.md`; `src/superclaude/cli/review/__init__.py`; the re-pinned tests `tests/skills/test_review_severity_mapping.py`, `tests/skills/test_implement_severity_static.py`, `tests/audit/test_nfr_conv_9_zero_trust.py` and `tests/audit/test_severity_floor_unweakened.py` (the two fixtures and their plan tables were not changed).
+
+Remove: `src/superclaude/cli/review/fixcheck.py`, `src/superclaude/cli/review/fixcheck_cmd.py`, `tests/review/test_review_fixcheck.py` and `tests/skills/test_review_old_rule_scan.py`.
+
+## The refresh line
+
+`make sync-dev` does not copy output styles, so the installed `~/.claude/output-styles/pragmatic.md` stays old until you refresh it. Run `superclaude install --force` from an install that holds this change (`install_output_styles` in `src/superclaude/cli/install_user_setup.py` takes the `force` flag and reports files it keeps). The check that it worked: `grep -c "asks the user once per run, and again at any escalation halt" ~/.claude/output-styles/pragmatic.md` prints 1.
+
+Observed on this machine today, before any refresh: that command prints 0. The new rule is not live on a machine until it prints 1. Other installed copies stay old too, for example the package copy under `.venv/lib/python3.11/site-packages/superclaude/_src/` still holds the old sentence.
+
+Also found: one Markdown file outside the scanned roots still holds the old sentence, `docs/developer-guide/review-severity-rule.md` line 24. The reverse scan does not cover `docs/`. It was not edited here (not in the plan).
+
+The owner's go for stage 4 is given in chat and not by this file.
```

Codegraph context
index_state: fresh
checked_at: 2026-11-17T00:49:50Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: none; a single markdown note. It quotes test summary lines that the orchestrator re-ran just before writing it.

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
