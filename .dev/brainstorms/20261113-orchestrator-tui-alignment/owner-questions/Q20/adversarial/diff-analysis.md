# Diff Analysis: owner-answer proposals for Q20 (owner of the watcher worktree's agent; up to 6 coordinator-less sessions a day)

## Metadata
- Generated: 2026-11-14
- Variants compared: 3 (variant-1 = proposal-A "name no owner yet; hold FU-1"; variant-2 = proposal-B "a named person owns the agent; sessions stay person-reviewed top-level sessions"; variant-3 = proposal-C "the program's coordinator session creates and owns the agent and reviews watcher sessions")
- Total differences found: 13
- Categories: structural (1), content (5), contradictions (3), unique (3), shared assumptions (2)
- Step 1 performed by: the orchestrating session (group 4 worker), not a separate analytical agent.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section layout | Five fixed sections | Same five | Same five | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Who owns the watcher worktree's agent | Nobody yet | A named person | The program's coordinator session | High |
| C-002 | Up to 6 sessions a day in one worktree | Not accepted yet | Accepted | Accepted, reviewed by the coordinator | High |
| C-003 | Effect on WA-03 (runbook step), WA-02 edit 4, WA-04 (FU-1) | All held (default) | All proceed | All proceed, runbook names the coordinator | High |
| C-004 | Cleanup of open watcher sessions | Decided together with ownership before FU-1 | Closed by hand by the named person | Reported by the coordinator; closing stays a person's action | Medium |
| C-005 | Visibility of watcher sessions | Not raised | Observer cannot see them; sweep shows transcript rows "could not determine" | Same limit, named as the main weakness of coordinator review | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | May a coordinator own watcher sessions? | Undecided | Never | Yes (owner and reviewer, not Orca adoption) | High |
| X-002 | Is a person or a session the right owner? | Undecided | A person (Orca's creator rule) | A session (project rule: "the eligible session that creates a worktree owns its agent(s)") | Medium |
| X-003 | Should FU-1 wait for a cleanup rule? | Yes | No; cleanup by hand | No; coordinator reports, person closes | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | Variant 1 | Pairs the ownership answer with a decision on closing or reaping sessions, which nothing does today | Medium |
| U-002 | Variant 2 | Adds the runbook note that every watcher session writes `.dev/issues/<N>/`, so the sweep shows the worktree as uncommitted | Medium |
| U-003 | Variant 3 | One already-watching session as accountable reviewer, folded into the owner's recurring check (Q31) | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The day cap of 6 per 24 hours is fixed by the watcher's design and is not itself a choice in this answer | All three treat "6 a day" as given | If the cap is configurable (UNVERIFIED), a lower cap is a cheaper control than any ownership rule | UNSTATED, promoted |
| A-002 | The watcher keeps starting every session in one shared configured worktree, whatever Q2 (claim level) answers | All three accept one shared worktree | At the default claim level each claim also creates `issue-<N>` with a second, governed agent, so ownership questions multiply | UNSTATED, promoted |

## Summary
- Total structural differences: 1
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, X-001
- Taxonomy tags: L1 S-001; L2 C-001, X-002, U-001 to U-003; L3 C-002 (boundary: session count), C-003 (guard: gated items), C-004 (state: open sessions), C-005 (state visibility), X-001 (boundary: coordinator ownership), X-003 (guard), A-001, A-002
