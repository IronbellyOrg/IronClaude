# Diff Analysis: owner-answer proposal comparison (Q26, coordinator home and ledger branch)

## Metadata
- Generated: 2026-11-14T00:05Z
- Variants compared: 3 (V1 = proposal-A, owner-created Orca worktree; V2 = proposal-B, main checkout on a program branch; V3 = proposal-C, no coordinator yet)
- Total differences found: 15
- Categories: structural (1), content (4), contradictions (3), unique (4), shared assumptions (3: UNSTATED 2, STATED 1)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Section set | Answer; What happens next (4 steps); Unlocks; Costs; Unresolved | same five sections (4 steps) | same five sections (4 steps) | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Where the coordinator runs | A new Orca worktree the owner creates from `origin/master` with `--agent`; its agent is the coordinator | The main checkout `/home/coder/workspaces/IronClaude`, owner-opened session | Nowhere yet; XC-09 (stand up the coordinator) held | High |
| C-002 | Where the ledger is staged | The new worktree's own branch | A new program branch from `origin/master` in the main checkout | Not in the repository; owner's own notes | High |
| C-003 | First owner action and its dependency | `orca worktree create ... --agent` (needs Orca reachable) | Owner switches the main checkout's branch (git only), then opens a session | None; re-ask later | Medium |
| C-004 | Effect on the main checkout | Untouched | Branch switched; busy for the program's life | Untouched | Medium |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Is the coordinator "person-opened" as the worker contract and spec require? | Relies on an Orca `--agent` launch counting as person-opened; V1 itself marks this UNVERIFIED | Yes: the owner opens the session by hand | n/a (no coordinator) | High |
| X-002 | Project rule "Session A: Open the main checkout (current branch); it is the orchestrator" (project `CLAUDE.md`) | Treated as an example, not a rule | Followed | Not engaged | Medium |
| X-003 | Where the grant table (spec 6.8; XC-01 (5)) lives | On disk in the worktree | On disk in the main checkout | Owner's notes only; agents cannot read it from disk | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Owner must verify the coordinator's first screen, a launch receipt is not proof (owner memory `orca-worker-resume-verify-screen.md`) | Low |
| U-002 | V2 | Measured state of the docs branch on 2026-11-13: 0 unpushed commits, no modified tracked files, no PR, so "safe to leave" already appears to hold | Medium |
| U-003 | V3 | Re-ask Q26 when the first worker-dispatched item is next, with the then-current Orca and checkout state | Medium |
| U-004 | V2 | Risk that a broad `git add .dev` in the main checkout picks up the 21 untracked entries of other work | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | "The ledger is staged on branch X" holds over time. In git, staged but uncommitted files live in the checkout's index, not on a branch, and travel with a later branch switch (standard `git switch` behaviour when nothing conflicts). In V2, if the owner later switches the main checkout back to a docs branch, the staged ledger goes with it and could be committed there. In V1 the dedicated worktree never switches, so the ledger stays isolated | V1 and V2 both say "staged on that branch"; V3 avoids it | High (state, L3) | UNSTATED, promoted |
| A-002 | Only one live session works in the coordinator home at a time (spec 6.2: one worktree never holds two live agents). V2's main checkout is also the owner's general place of work, so a second session there would break this | V1 and V2 both assume the home is the coordinator's alone | Medium (concurrency, L3) | UNSTATED, promoted |
| A-003 | The Orca app must answer before XC-09 starts (ORCA-AVAILABLE, `merged-requirements.md:604`) | all three | Medium | STATED, not promoted |

## Summary
- Total structural differences: 1
- Total content differences: 4
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001, X-003, A-001
- Taxonomy tags: S-001 L1; C-001, C-002, C-003, C-004, X-002 L2; X-001, X-003, A-001, A-002 L3 (guard, state, concurrency)
