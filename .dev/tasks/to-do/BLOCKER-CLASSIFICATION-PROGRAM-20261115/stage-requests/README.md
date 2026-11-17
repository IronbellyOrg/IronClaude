# Stage requests for the blocker-classification work (issue #552): one plan per stage

Decision (owner, 2026-11-16): one managed plan package per stage, each generated with `/sc:workflow` and run with `/sc:implement`. `/sc:implement` cannot pause for an owner go, ignores `Depends on:` lines between packages and fails on a plan changed after its first task, so each owner gate sits between two packages and is a chat message from the owner, not a task.

This replaces the single 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (its pre-execution review, `.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md`, found 8 blocking defects). That plan stays on disk as the base text for the task bodies; each stage request below names the base tasks it reuses and the changes the review required.

## How to use

1. Generate a stage's package only after the owner's go for it: `/sc:workflow @<request file> --depth standard --handoff none`.
2. Read the plan and its reflect report; run `/sc:implement <printed plan path>` only when execution is wanted.
3. When the package is done, the owner reads its owner summary file and says go for the next stage in chat. Record the go and the package id in the table below (the owner or the session that receives the go writes the row).

## Stage ledger

| Stage | Request file | Base tasks (revised plan) | Package id | Owner go (date, where) |
|---|---|---|---|---|
| 0 Measurement | `stage0-request.md` | 1 to 10 | `TASK-WF-blockerStage0-20261116-021044` (trimmed to 3 tasks by the cuts debate 2026-11-16; reviewer pass owed) | not needed (no change under `src/`) |
| 1 Offline scaffold | `stage1-request.md` | 11 to 25 | `TASK-WF-stage1Request-20261116-221852` (regenerated 2026-11-16 with `/sc:workflow --depth quick`; 2 tasks; absorbs stage 2's print step; pre-execution review done, verdict revise: one blocking finding, see its `return-contract.yaml` for the report path; replaces `TASK-WF-blockerStage1-20261116-030154`, which has no contract and is not to be run) | 2026-11-16, owner in chat (stage 0 worker session), after reading `stage0c-regrade.md` with `stage0c-control/RESULT.md`: the regrade is read as "the new text does not change grades on a table of findings already filed as blocking", a limit of the table that RT1 and the owner's read of the first five runs' Medium lists cover. The go covers the regenerated package named in the previous cell. It is not to be run until the blocking review finding is resolved or the owner accepts it |
| 2 Shadow | `stage2-request.md` | 26 to 30 | `TASK-WF-blockerStage2-20261116-030156` (WITHDRAWN 2026-11-16 by the cuts debate; its one surviving task, the `/sc:implement` print step, is stage 1 task 2; package archived) | |
| 3 Pilot | `stage3-request.md` | 31 to 40 | `TASK-WF-blockerStage3-20261116-030158` (trimmed to 10 tasks by the cuts debate 2026-11-16; reviewer pass owed) | 2026-11-17, owner in chat ("Start stage 3"), received by the stage 0 and 1 worker session after PR #581 was merged. Stage 1 is the package `TASK-WF-stage1Request-20261116-221852` (done), not `TASK-WF-blockerStage1-20261116-030154` (archived, superseded) that the plan text names. |
| 4 Propagation | `stage4-request.md` | 41 to 46 | `TASK-WF-blockerStage4-20261116-030206` (trimmed to 4 tasks by the cuts debate 2026-11-16; reviewer pass owed) | |

## Decisions applied to every stage (from the review findings F1 to F15)

- **Gates (F1, F8).** No gate task. The owner's go is a chat message recorded in the ledger above. Each package ends with an owner summary file under its `./artifacts/` that holds the numbers the owner needs for the next go.
- **Cross-package evidence.** A later package reads an earlier package's evidence by package id, found by that folder name under `.dev/tasks/to-do/` or `.dev/tasks/done/` (the package moves when archived). A task never embeds either prefix in an operational link.
- **Merge-rule allow-list staging (F3, F9, F13).** The allow-list in `refs/scale-map.md` lists files by path only and never writes the three merge-rule phrases (`highest severity`, `more severe rating`, `higher severity`) or the old definition sentence. Stage 3's scan test allow-lists only files that exist then. Revision 2 (2026-11-16): there is no plugin mirror folder and no plugin parity test (IronClaude is not installed as a plugin); stage 4 narrows the allow-list and runs the scan strict for `src/` only. The retired `/sc:task` and task-builder files are listed `exempt-by-retirement` and are not edited.
- **Analysis template (F4).** `agent_template_analysis.md` gets the merge-rule text only. It is not a digest carrier: the registry keeps exactly 11 `digest` rows, and the template count in stage 4 is four digest templates plus the analysis template's merge-rule edit.
- **T3 scope (F5, F12).** The `src/superclaude` path check of T3 applies to `digest` and `canonical` rows only. `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its pointer is present. The existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` (and its plugin twin and the installed variants) is left as it is; it is a read-path note outside this work.
- **Installed files (F15).** No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path; the M, C and E input rule is stated in words.
- **Seeded recall (F2, F10, F11).** Stage 0 defines and sizes the set (with a stated minimum n per gating class, or the set's pass line is called advisory and the interval shown). Stage 3 runs it with fresh agent spawns per pass and alternated order, and Task 33's acceptance line requires the result file to show pass on all three requirements.
- **Classifier evaluation (F7).** Stage 2 evaluates the classifier on the fresh-findings set, the held-out half and the reviewer-called-minor set (all from the stage 0 package) and writes the result for the owner.
- **Superseded acceptance lines (F6).** Resolved by the split: a package's final review covers only its own tasks. Inside a package, a line that a later task of the same package makes false is written with its end point ("until Task N").
- **Unchanged from the revision request.** Three owner gates stay (stage 0 results read before stage 1; stage 1 exit before stage 2; owner go for stages 3 and 4), plus the existing not-built list, the no-authority classifier rule (OD4) and the owner-decision defaults of the first plan.

## Revision 2 decisions (2026-11-16, see `revision2-brief.md` and `../OPEN-QUESTIONS.md`)

- `/sc:task` and task-builder are being retired: no stage edits them; the scan allow-list lists them `exempt-by-retirement`.
- The follow-up carrier is `/sc:implement`'s final review step (owner approved 2026-11-16): record and print only, `refs/qa.md` unedited; the once-per-run offer question stays with the top-level session through the output style.
- No plugin mirror, parity test or plugin registry row; existing plugin twins are edited only where an existing test pins them.
- `follow-ups.md` stays a separate file; no mapping to `review-ledger/1` in these plans.

## Fields the stage 3 ledger row must hold (from the stage 3 plan, Task 1 and Task 4)

Owner go with its date; the list of shadow-run folders; the observed run count; the path of the safety-miss confirmation file (`reviewed: <date> by <name>` line plus `<run_id>:<row id>` entries). The row later also holds any owner ruling with its line id, date and SHA-256.

## Revision 4 decisions (2026-11-16, cuts debate; `../cuts-debate/final-cuts.md` is authoritative and overrides the revision 2 decisions above where they conflict)

- Result: 19 tasks in 4 packages (stage 0: 3, stage 1: 2, stage 3: 10, stage 4: 4); the stage 2 package is withdrawn.
- No ledger, classifier, registry, skill folder, scale map, doctor check, allow-list, seeded-recall experiment, five-shadow-run gate or per-stage owner summaries (except the stage 3 note that stage 4 reads).
- The `/sc:implement` final step is print-only (prints `notes.md` minors and runs `superclaude review safety-scan`); `refs/qa.md` stays unedited.
- The new rule text is copied atomically into all ten pinned files in stage 3; stages 3 and 4 stay separate packages with separate owner gos.
- The merge-rule scan, plugin mirror, `exempt-by-retirement` and strict-switch decisions of the revision 2 section above no longer apply.

## Archived plans (2026-11-16)

Moved with `git mv` to `.dev/tasks/archive/to-do/` (nothing deleted; the folder names are unchanged):

| Plan | Why archived |
|---|---|
| `TASK-WF-loosenBlockerCla-20261115-133045` (39 tasks) | superseded by the 46-task plan |
| `TASK-WF-loosenBlockerRev-20261115-210254` (46 tasks) | superseded by the per-stage packages; its task bodies were the base text |
| `TASK-WF-blockerStage2-20261116-030156` (8 tasks) | withdrawn by the cuts debate; its one surviving task moved to stage 1 |

Text above that says these packages are "found under `.dev/tasks/to-do/`" describes where they were when written.
