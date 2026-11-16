# Stage 1 plan request: offline scaffold for the blocker classification work (issue #552)

Second of five plan packages (see `stage-requests/README.md` for the one-plan-per-stage decision and the decisions that apply to every stage). Generate it only after the owner has read the stage 0 package's `./artifacts/stage0-summary-for-owner.md` and said go in chat, and after the stage ledger row for stage 0 has the package id. This stage creates new files only (the skill folder, new CLI modules, new tests, one doctor check); it edits no review-loop carrier.

## Base text

Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 2, stage 1; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward. Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owner-decision defaults, the not-built list, the classifier facts (M, C and E run only with code-supplied inputs; the "M or C is Y gives BLOCKING" row is never enabled; confidence is an ordinal band), pins by content, `src/superclaude/` as source of truth with `make sync-dev`, UV only. The stage 0 package's evidence (inventory freeze, availability counts, spec reconciliation) is read by package id.

## Changes to apply

- **Constraints.** State this package is stage 1: new files only, no carrier edited, every registry `digest` row stays `legacy`. The next package (stage 2) starts only after the owner's go in chat. Drop the base plan's Phase 3 to 5 gate prose.
- **Task 13 (scale map).** The "Merge-rule allow-list" section lists files by path and never writes the three merge-rule phrases or the old definition sentence. At stage 1 it lists the auggie file, `refs/rule.md` and the six stage 4 files. Say in the task that the plugin mirror is added in stage 4, not here.
- **Task 12 (rule).** `refs/rule.md` holds the GR5 sentence with the phrase `highest severity` (allow-listed) but never quotes the old definition sentence "Grade every review finding as blocking or minor" outside the digest's own fence history; state this as an acceptance line (`grep` of the old sentence over the skill folder prints nothing).
- **Task 15 (classifier questions) and all refs.** No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path (acceptance: `grep -rn "\.dev/\|artifacts/" src/superclaude/skills/sc-review-severity` prints nothing). State the M, C and E input rule in words.
- **Task 16 (registry).** Keep exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). Say the analysis template is not a carrier row (merge-rule text only in stage 4).
- **Task 25 (registry drift tests).** T3's `src/superclaude` check applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its pointer is present; the test never reads `~/.claude`. T2 is non-strict (strict only in stage 4). Acceptance includes a temporary-tree test of each exemption.
- **Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N").
- **New final task: stage 1 exit summary for the owner.** Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and its observed test result (the commands run and their pass counts), the list of files created, a statement that no carrier was edited (`git diff --stat` over carriers is empty), the open items, and the sentence that the owner's go for stage 2 is given in chat and not by this file. This is the stage 1 exit the spec requires.

## Not to be done by the plan

No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT) and no stage 2 to 4 task. Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.
