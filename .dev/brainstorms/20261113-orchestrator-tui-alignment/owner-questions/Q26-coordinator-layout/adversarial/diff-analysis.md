# Diff Analysis: coordinator layout proposals (Q26 follow-up)

## Metadata
- Generated: 2026-11-14T15:05Z
- Variants compared: 3 (variant 1 = `proposal-A.md`, scope folders with a lease; variant 2 = `proposal-B.md`, shared branch, scope then developer, claim files; variant 3 = `proposal-C.md`, developer folders on developer branches)
- Total differences found: 22 debatable points
- Categories: structural (3), content (10), contradictions (3), unique (6, not counted in the denominator), shared assumptions (6)
- Depth: quick (Round 1 only; Round 2 and the Round 2.5 invariant probe are skipped by the protocol at this depth)

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity | Level |
|---|---|---|---|---|---|---|
| S-001 | Section set | the same 8 sections | the same 8 sections | the same 8 sections | Low | L1 |
| S-002 | First directory level under `.dev/coordinators/` | scope only (`<kind>-<scope>/`); developer is a field | scope, then developer (`<kind>-<scope>/<dev>/`) | developer, then coordinator (`<dev>/<kind>-<scope>/`) | High | L2 |
| S-003 | Shape of ledger and grant storage | one file per entry in `ledger/` and `grants/` folders | one append-only file per coordinator (`ledger.md`, `grants.md`) | one append-only file per coordinator | Medium | L2 |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity | Level |
|---|---|---|---|---|---|---|
| C-001 | Branch model | one shared `coordinators` branch per project | one shared `coordinators` branch per project | one `<dev>/coordinators` branch per developer; no shared write branch | High | L2 |
| C-002 | How many live coordinators per scope | at most one (lease in `holder.md`) | one per developer, more with `-2` | unlimited, unaware of each other | High | L3 (state) |
| C-003 | Stopping two coordinators dispatching one item | lease within a scope; each item listed in exactly one `scope.md` | pushed create-once `claims/<key>.md`; git add/add conflict is the lock; no pushed claim, no dispatch | advisory scan of every `origin/*/coordinators` `claims.md`; racy | High | L3 (concurrency, guard) |
| C-004 | Release versus epic | release scope lists epics, never their items | release claims only release-only items; reads epic items | no rule | Medium | L2 |
| C-005 | Archive | move the folder to `archive/` (owner only) | state row; folder stays | state row; folder stays | Medium | L3 (transition) |
| C-006 | Grant scoping | per scope; approver handle in the entry | per coordinator folder; grant id carries the handle | per coordinator on the developer's own branch | Medium | L2 |
| C-007 | How developer B reads A's state | `git show origin/coordinators:<path>` | `git show origin/coordinators:<path>`; one glob per developer | fetch and scan every `origin/<dev>/coordinators` | Medium | L2 |
| C-008 | Push permission needed | standing grant to push one shared branch | standing grant to push one shared branch | per-developer grant to push the developer's own branch | Medium | L2 |
| C-009 | Kinds of coordinator | `epic`, `release` | `epic`, `release` | `epic`, `release`, `adhoc` | Low | L1 |
| C-010 | Readability of the ledger | needs `ls` or a reader script to build the table | one file per coordinator | one file per coordinator | Medium | L2 |

## Contradictions

| # | Point of conflict | Positions | Impact |
|---|---|---|---|
| X-001 | The owner's wording "a Coordinator branch" (one per project) | A and B keep one shared branch; C gives one per developer and says so ("departs from that wording") | Medium |
| X-002 | Grant ids inside A (intra-variant) | A: "`g` plus 4 digits, counted per scope ... two holders never mint the same file even if both pick `g0001`": file names stay unique, but two grants can carry the same id, so a ledger entry or graph edge that cites `g0001` is ambiguous | Medium (L3 guard) |
| X-003 | Base branch of a coordinator worktree versus the merged spec | all three base the coordinator worktree on a non-master branch (`origin/coordinators` or `origin/<dev>/coordinators`); merged spec 6.2 says a top-level agent's worktree is created with `--base-branch origin/master`; all three mark Orca's support for another base UNVERIFIED | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | A | Lease and handover: one ledger per epic survives a change of developer | Medium |
| U-002 | A | One file per ledger or grant entry: zero edit conflicts even for a careless writer | Medium |
| U-003 | B | Project-wide `claims/` keyed by `issue-<N>`, `pr-<N>`, `item-<scope>-<id>`: catches two scopes (for example an epic and a release) both writing to the same issue or PR, which A's per-scope lease does not | High |
| U-004 | B | Release coordinator claims only release-only items and reads epic items | Medium |
| U-005 | C | `adhoc` kind and private (unpushed) coordinators allowed | Low |
| U-006 | C | Matches the existing developer-prefixed branch habit (`ironbelly/...`, `origin/clayphi/...`) | Low |

## Shared Assumptions

Agreement points: all three use the GitHub login as the developer handle; all give each coordinator its own Orca worktree; all keep `.dev/coordinators/` unmerged and pushed only to the fork; all rely on git's own conflict detection or fetch-then-act; all move the ledger out of `.dev/tasks/<program-package>/`.

| # | Assumption | Source agreement | Classification | Promoted | Level |
|---|---|---|---|---|---|
| A-001 | One human has exactly one GitHub login, and every session can read it (`gh` authenticated). The git log shows one person under three author names (`Ironbelly`, `Ryan wiancko`, `coder`) and the host's `user.name` is the shared default `coder`, so commit metadata cannot identify a developer | handle grammar | UNSTATED | yes | L3 (guard) |
| A-002 | Each developer has their own host and Orca; two developers never share one worktree folder namespace (B states it UNVERIFIED; A and C rely on it silently) | worktree naming | UNSTATED | yes | L2 |
| A-003 | Nobody force-pushes or rewrites the shared branch; every writer does fetch, rebase, push. The lock of A (`holder.md`) and B (`claims/`) is void after a `push --force` | git conflicts as locks | UNSTATED | yes | L3 (concurrency) |
| A-004 | A coordinator on an unmerged branch still sees current code and current program documents. Its worktree holds the branch base plus `.dev/coordinators/` only, so master code and documents committed after the base (and files on other unmerged branches, such as this spec on the #539 branch) are absent unless the branch is kept current or read from elsewhere | unmerged branch | UNSTATED | yes | L3 (state) |
| A-005 | A session the developer launches with `orca worktree create --agent` counts as "person-opened" (the original Q26 split, `Q26/final.md`); the owner's 2026-11-14 answer ("create and maintain a Coordinator branch and worktree") points that way but does not say it | coordinator creation | UNSTATED | yes | L2 |
| A-006 | Everything written under `.dev/coordinators/` is safe to push to the fork (owner wording in grants, sanitized captures); the fork is described as private in project `CLAUDE.md` | push for visibility | UNSTATED | yes | L2 |

## Summary
- Structural differences: 3; content differences: 10; contradictions: 3; unique contributions: 6; shared assumptions surfaced: 6 (UNSTATED 6, STATED 0, CONTRADICTED 0)
- Debatable points (denominator): 3 + 10 + 3 + 6 = 22
- Highest-severity items: S-002, C-001, C-002, C-003
- Taxonomy coverage: L1 (S-001, C-009), L2 (S-002, S-003, C-001, C-004, C-006 to C-008, C-010, A-002, A-005, A-006, X-001, X-003), L3 (C-002, C-003, C-005, X-002, A-001, A-003, A-004): all three levels covered
- Similarity check: the variants differ on most topics; debate not skipped.
