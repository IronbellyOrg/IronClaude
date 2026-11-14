# Diff Analysis: owner-answer proposal Comparison (Q32)

## Metadata
- Generated: 2026-11-14T00:30:00Z
- Variants compared: 3 (Variant 1 = proposal-A.md, Variant 2 = proposal-B.md, Variant 3 = proposal-C.md)
- Total differences found: 15
- Categories: structural (2), content (7), contradictions (2), unique (4), shared assumptions (2 promoted)
- Context file (not a variant): `Q32/question.md`

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|------|---------------|---------------|---------------|----------|
| S-001 | Section set | Five brief sections | Same five | Same five | Low |
| S-002 | Concrete wording offered | An example per-Task question | None needed | The full standing sentence to quote | Low |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|-------|---------------|---------------|---------------|----------|
| C-001 | Do workers commit | Only Tasks the owner approves at dispatch | Never | Every code-changing Task | High |
| C-002 | Owner wording collected | One answer per Task at dispatch (up to nine questions) | None | One sentence now, Task id filled in by the coordinator | High |
| C-003 | Fit with WC-9 "quotes, word for word, the user's instruction naming a local commit for that Task" | Strict fit: owner's own words per Task | Not applicable | Fit UNVERIFIED for a filled-in template | High |
| C-004 | Protection of the change between `worker_done` and the PR session's commit | Only for approved Tasks | None: uncommitted files in the worktree | Commit checkpoint for every Task | Medium |
| C-005 | Where the person reviews | Mixed | Once, before the PR session commits | Worker commits shown before push (`WORKER-CONTRACT.md:244`) | Medium |
| C-006 | Where a pre-commit hook failure lands | Mixed | PR session | Worker that wrote the change | Low |
| C-007 | Number of commit paths in the program | Two (worker or PR session, per Task) | One (PR session) | One for the change (worker) plus PR-session fix commits | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 (A) Position | Variant 2 (B) Position | Variant 3 (C) Position | Impact |
|---|-------------------|------------------------|------------------------|------------------------|--------|
| X-001 | Can one standing sentence satisfy WC-9 for every Task | Implicitly no: asks per Task to meet it strictly | Not needed | Yes in practice, flagged UNVERIFIED | Medium |
| X-002 | Is the uncommitted gap a material risk | Material enough to allow commits case by case | Names it, size UNVERIFIED, accepts it | Treats it as a main reason to commit | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | 1 (A) | Commits only where the owner judges a checkpoint worth it | Medium |
| U-002 | 3 (C) | Commit id in `worker_done` gives a fixed revision to review and push | Medium |
| U-003 | 2 (B) | One review before commit; what is pushed equals what the pushing session committed | Medium |
| U-004 | 3 (C) | Hook failures surface in the session that wrote the change | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | All three hand the change to a PR session in the same worktree | The Q25 model holds: a PR session is launched later in the worker's own worktree (spec 6.3 says Orca permitting a second, sequential launch in a `worker-start` worktree is UNVERIFIED) | UNSTATED | Yes |
| A-002 | All three rely on the worktree staying as the worker left it | Nothing writes, cleans or switches the worktree between the worker's end and the PR session (single live agent per worktree, spec 6.2), and the shared git stash stack is not used there | UNSTATED | Yes |
| A-003 | All | The person is available to review before any push (`WORKER-CONTRACT.md:244`) | STATED (B, C) | No |

Promoted shared-assumption points:

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | PR session runs in the same worktree after the worker (Q25 model) | All variants | Medium: if Q25 is answered with the alternative (a top-level agent per PR item and no worker), Q32 has no workers to govern | Open for debate |
| A-002 | The worktree is stable between worker end and PR session | All variants | Medium: state guard (L3); decides how much the uncommitted gap matters | Open for debate |

## Summary
- Total structural differences: 2
- Total content differences: 7
- Total contradictions: 2
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003
- Diff points counted for convergence (S + C + X + A): 13
