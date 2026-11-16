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
| 0 Measurement | `stage0-request.md` | 1 to 10 | `TASK-WF-blockerStage0-20261116-021044` (generated 2026-11-16; its pre-execution review says NEEDS-REVISION, 2 blocking findings, so revise before running it) | not needed (no change under `src/`) |
| 1 Offline scaffold | `stage1-request.md` | 11 to 25 | | |
| 2 Shadow | `stage2-request.md` | 26 to 30 | | |
| 3 Pilot | `stage3-request.md` | 31 to 40 | | |
| 4 Propagation | `stage4-request.md` | 41 to 46 | | |

## Decisions applied to every stage (from the review findings F1 to F15)

- **Gates (F1, F8).** No gate task. The owner's go is a chat message recorded in the ledger above. Each package ends with an owner summary file under its `./artifacts/` that holds the numbers the owner needs for the next go.
- **Cross-package evidence.** A later package reads an earlier package's evidence by package id, found by that folder name under `.dev/tasks/to-do/` or `.dev/tasks/done/` (the package moves when archived). A task never embeds either prefix in an operational link.
- **Merge-rule allow-list staging (F3, F9, F13).** The allow-list in `refs/scale-map.md` lists files by path only and never writes the three merge-rule phrases (`highest severity`, `more severe rating`, `higher severity`) or the old definition sentence. Stage 3's scan test allow-lists only files that exist then. Stage 4 adds the plugin mirror to the allow-list and the registry before it copies the folder, then re-runs the scan.
- **Analysis template (F4).** `agent_template_analysis.md` gets the merge-rule text only. It is not a digest carrier: the registry keeps exactly 11 `digest` rows, and the template count in stage 4 is four digest templates plus the analysis template's merge-rule edit.
- **T3 scope (F5, F12).** The `src/superclaude` path check of T3 applies to `digest` and `canonical` rows only. `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its pointer is present. The existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` (and its plugin twin and the installed variants) is left as it is; it is a read-path note outside this work.
- **Installed files (F15).** No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path; the M, C and E input rule is stated in words.
- **Seeded recall (F2, F10, F11).** Stage 0 defines and sizes the set (with a stated minimum n per gating class, or the set's pass line is called advisory and the interval shown). Stage 3 runs it with fresh agent spawns per pass and alternated order, and Task 33's acceptance line requires the result file to show pass on all three requirements.
- **Classifier evaluation (F7).** Stage 2 evaluates the classifier on the fresh-findings set, the held-out half and the reviewer-called-minor set (all from the stage 0 package) and writes the result for the owner.
- **Superseded acceptance lines (F6).** Resolved by the split: a package's final review covers only its own tasks. Inside a package, a line that a later task of the same package makes false is written with its end point ("until Task N").
- **Unchanged from the revision request.** Three owner gates stay (stage 0 results read before stage 1; stage 1 exit before stage 2; owner go for stages 3 and 4), plus the existing not-built list, the no-authority classifier rule (OD4) and the owner-decision defaults of the first plan.
