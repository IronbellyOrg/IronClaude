# Proposal B: the main checkout, switched by the owner to a dedicated program branch from origin/master

## Answer

The coordinator runs in the main checkout `/home/coder/workspaces/IronClaude`, which the owner first switches from `docs/409-orca-dashboard-designs` to a new program branch made from `origin/master`, once the docs work there is safe; the ledger package is staged on that program branch.

## What happens next if the owner picks it

1. The owner confirms the docs branch is safe to leave. Observed 2026-11-13: `docs/409-orca-dashboard-designs` at `495eb96d1` has 0 unpushed commits, no modified tracked files and no PR; 21 untracked entries (under `.claude-audit/` and `.dev/`, none under `.dev/tasks/`) stay in the folder across a branch switch.
2. The owner, not the coordinator, creates and switches to the program branch (the coordinator never switches a branch on its own, `merged-requirements.md:900`).
3. The owner opens a Claude session there. That session is the coordinator (XC-09): person-opened, and in the place the project names for the orchestrator ("Session A: Open the main checkout ... it is the orchestrator", project `CLAUDE.md`).
4. The coordinator writes the ledger package `.dev/tasks/<program-package>/`, staged on the program branch, committed only when the owner asks. XC-10 part (3) records the path and branch.

## What it unlocks

- XC-09 and every item it dispatches (edge 119), on the only existing home that conforms to every project rule (`invariant-probe.md:10`).
- No new worktree, and no open question about whether the coordinator counts as person-opened.

## What it costs or risks

- The main checkout is busy with the program for weeks; other work the owner does there (docs, issue drafting) must move or share the branch, and the 21 untracked entries from other work sit beside the ledger (they are not staged by the `.dev/tasks/` rule, but a careless `git add .dev` would pick them up).
- The owner must do the branch switch by hand at the right moment; a switch with uncommitted tracked changes would be refused by git or would carry them over.
- Orca must still be reachable before XC-09 starts (ORCA-AVAILABLE, `merged-requirements.md:604`).

## What stays unresolved

- The program branch's name (the owner names it).
- When the docs branch work is "safe" is the owner's judgment; the observed state suggests it already is.
