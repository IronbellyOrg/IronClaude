# Proposal B: no new package; add SW-02 as a follow-up phase to the sweep task file already in PR #539

## Answer

Do not create a new plan package: plan SW-02 as a new phase appended to the existing sweep task package `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/`, which is already committed in PR #539, and run that phase with its existing executor.

## What happens next if the owner picks it

1. The #539 author reopens the task file (status from Done back to Doing) and appends a phase with SW-02's steps and acceptance criteria.
2. The phase is executed with `/task` (the executor for that task-file format), which also runs its per-phase reviewers.
3. The changed task file and its new phase outputs are committed in #539 by named paths, alongside the fix.
4. The ledger records which phase of the existing package holds SW-02.

## What it unlocks

- One package holds the whole Phase 1 history, from build to the INV-008 fix, in the PR that shipped it.
- No new `.dev/tasks/` package enters #539, so rule A-004's "no new artifact" reading is kept in letter.
- The fix gets the task-file format's per-phase reviewer panels.

## What it costs or risks

- The project's routing guide sends ordinary implementation to `/sc:workflow` and `/sc:implement`; the task-file format is for an explicit choice or exceptional machinery needs (`~/.claude/CLAUDE.md`, workflow levels 3 and 4). Reusing it here is that explicit choice, at higher cost per step.
- Reopening a Done task changes its recorded status and its earlier sign-offs (its frontmatter holds a pre-execution review result for the original scope); a reader could mistake the reopened file for unfinished Phase 1 work.
- The project rule "When an adequate approved plan already exists, use its existing executor directly" fits only if the owner treats the existing package as the plan; it does not plan SW-02 today.
- The package already has 764 files in #539; the new phase adds more.

## What stays unresolved

- Whether the task file's existing reviewers and gates accept a phase added after Done.
