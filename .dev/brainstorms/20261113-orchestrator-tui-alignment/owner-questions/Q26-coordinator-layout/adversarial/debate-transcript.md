# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1
- Convergence achieved: 100 percent (22 of 22 points agreed; 18 unanimous, 4 by 2 of 3)
- Convergence threshold: 80 percent
- Focus areas: all
- Advocate count: 3, spawned in parallel as separate agents (general-purpose type; personas architect, backend, qa); each wrote its own statement file
- Orchestration (diff analysis, this transcript, scoring, plan) was done in-context by the worker that ran the skill; no separate debate-orchestrator agent was spawned

## Round 1: Advocate Statements

Full statements are on disk; they are the record and are not restated here:
- Variant 1 (proposal A) advocate, architect persona: `round1-advocate-V1.md`
- Variant 2 (proposal B) advocate, backend persona: `round1-advocate-V2.md`
- Variant 3 (proposal C) advocate, qa persona: `round1-advocate-V3.md`

### Positions in brief

- **Variant 1 advocate** conceded most points: "In the per-point table below variant 2 wins more points than mine. The design I would defend in Round 2 is variant 2's layout and claims, carrying over variant 1's immutable entry files and an optional single-holder mode." Its strongest remaining claim: one decision authority per epic (two coordinators on one epic can record contradictory epic-wide decisions in two ledgers under variant 2).
- **Variant 2 advocate** claimed the owner's full wording (one branch, developer and scope sub-folders, several developers per epic) and the only git-enforced, project-wide lock keyed on issue, PR and item. It conceded: the lock holds only if an agent never resolves a `claims/` conflict in its own favour; byte-identical bodies raise no conflict; `<dev>-g<NNNN>` grant ids can repeat across one developer's coordinators; ledger row ids lack a same-second rule; push before every dispatch needs the network; `<dev>-2` is under-specified.
- **Variant 3 advocate** claimed the smallest blast radius (no shared write target) and the narrowest push grant, and conceded the largest single failure in the set: cross-developer double dispatch is advisory and racy. Its stated merge: "variant 2's scope-first reading surface and project-wide claim keys with variant 3's per-developer write isolation where it can be kept."

### New facts the advocates verified (read-only, 2026-11-14)

- No branch matching `*coordinators*` exists locally or on `origin`; `.dev/coordinators` does not exist (all three advocates).
- The Orca branch prefix is not universal: worktree `brainstorm-reflect-panel` is on `ironbelly/shadow-runs` and `issue-409-mvp` is on `409-Phase2` (`git worktree list`; confirmed by this worker's own `git worktree list` run earlier). So "observed `<orca-prefix>/<name>`" in all three proposals is a habit, not a rule.
- `merged-requirements.md:954` says a top-level agent's worktree is created with `--base-branch origin/master` (variant 3 advocate), confirming X-003.

### Shared assumption responses

| # | V1 | V2 | V3 | Outcome |
|---|---|---|---|---|
| A-001 handle is the GitHub login | QUALIFY | QUALIFY | QUALIFY | all: read it from `gh api user --jq .login` at session start, refuse when `gh` is unauthenticated, freeze it at creation |
| A-002 one developer per host | QUALIFY | QUALIFY | QUALIFY | all: cheap insurance is the handle in the worktree name |
| A-003 no force push | ACCEPT | QUALIFY | QUALIFY | all: must be a written rule; branch protection on the fork is UNVERIFIED |
| A-004 unmerged base still current | REJECT | QUALIFY | REJECT | all: a coordinator reads code and program documents with `git show origin/master:<path>` (or the owning branch) and records the revision; it never assumes its checkout is current; rebasing the shared branch would break A-003 |
| A-005 Orca launch counts as person-opened | QUALIFY | QUALIFY | ACCEPT | owner confirms in writing |
| A-006 safe to push | QUALIFY | QUALIFY | QUALIFY | all: sanitize; no tokens, no host or contact details |

No omissions: each advocate answered all six.

## Rounds 2, 2.5 and 3

- Round 2 skipped: depth=quick.
- Round 2.5 (invariant probe) skipped: --depth quick. The advocates' concessions above cover the state-mechanics risks the probe would look for (conflict resolution in one's own favour, identical bodies, id repetition, force push, stale base); they are carried into the refactor plan.
- Round 3 skipped: depth=quick.
- Taxonomy coverage: L1, L2 and L3 points were all debated; no forced round.

## Scoring Matrix

Votes are (V1 advocate, V2 advocate, V3 advocate). "tie (x, y)" means those variants are equally good on the point.

| Diff point | Level | Votes | Winner | Confidence | Evidence summary |
|---|---|---|---|---|---|
| S-001 | L1 | tie, tie, tie | tie | 95% | identical section sets |
| S-002 | L2 | 2, 2, 2 | Variant 2 | 95% | scope then developer gives one folder per epic and one glob per developer and allows several developers per epic |
| S-003 | L2 | 1, 1, tie (2, 3) | Variant 1 | 70% | one file per entry cannot lose rows to a rewrite; V2 advocate conceded; V3 advocate argued one writer plus git history is enough |
| C-001 | L2 | tie (1, 2), tie (1, 2), 3 | tie (1, 2) | 70% | one shared branch matches the owner; V3 advocate preferred per-developer branches for blast radius |
| C-002 | L3 | 2, 2, 2 | Variant 2 | 95% | several coordinators per scope kept apart by claims |
| C-003 | L3 | 2, 2, 2 | Variant 2 | 95% | pushed create-once project-wide claims; V1 misses cross-scope writes; V3 is racy (V3 advocate conceded) |
| C-004 | L2 | 2, 2, 2 | Variant 2 | 90% | only explicit release versus epic rule |
| C-005 | L3 | tie (2, 3) x3 | tie (2, 3) | 90% | state row keeps cited paths valid; V1's move breaks them |
| C-006 | L2 | 2, 3, 2 | Variant 2 | 65% | handle in the grant id; V2 advocate itself noted the id can repeat within one developer |
| C-007 | L2 | 2, 2, 2 | Variant 2 | 90% | one branch, known paths, no multi-branch scan |
| C-008 | L2 | 3, 3, 3 | Variant 3 | 90% | own-branch push grant is the narrowest |
| C-009 | L1 | 3, 3, 3 | Variant 3 | 90% | `adhoc` kind covers triage and one-off work |
| C-010 | L2 | tie (2, 3) x3 | tie (2, 3) | 90% | one readable ledger file per coordinator |
| X-001 | L2 | tie (1, 2) x3 | tie (1, 2) | 95% | V3 departs from "a Coordinator branch" (V3 advocate conceded) |
| X-002 | L3 | 2, 3, 2 | Variant 2 | 65% | handle-qualified ids; still needs a per-coordinator qualifier |
| X-003 | L2 | tie x3 | tie | 90% | all three base on a non-master branch against spec 6.2 |
| A-001 | L3 | tie x3 | tie | 90% | same handle source; none stated the unauthenticated case |
| A-002 | L2 | 2, 2, 2 | Variant 2 | 90% | only V2 named the shared-host case |
| A-003 | L3 | 3, 3, 3 | Variant 3 | 90% | no shared lock to void (all three advocates: true only because V3 has no lock) |
| A-004 | L3 | tie x3 | tie | 90% | all equally exposed |
| A-005 | L2 | tie x3 | tie | 90% | same creation path in all three |
| A-006 | L2 | 3, 3, 3 | Variant 3 | 80% | unpushed coordinators keep data local (at the cost of invisible claims) |

Points won outright: Variant 2: 8 (S-002, C-002, C-003, C-004, C-006, C-007, X-002, A-002); Variant 3: 4 (C-008, C-009, A-003, A-006); Variant 1: 1 (S-003). Shared wins: Variant 1 and 2 on C-001, X-001; Variant 2 and 3 on C-005, C-010. Plain ties: S-001, X-003, A-001, A-004, A-005.

Tension to resolve in the plan: S-003 (one file per entry, majority Variant 1) and C-010 (one readable ledger file, unanimous tie of Variants 2 and 3) pull in opposite directions.

## Convergence Assessment
- Points resolved: 22 of 22
- Alignment: 100 percent
- Threshold: 80 percent
- Status: CONVERGED (taxonomy gate passed; invariant gate not applied at depth quick)
- Unresolved points: none. Overall picks: the V2 advocate for Variant 2; the V1 advocate said Variant 2 "wins more points than mine" and proposed Variant 2 plus Variant 1's immutable entries; the V3 advocate proposed Variant 2's reading surface and claims plus Variant 3's write isolation. All three overall positions point at Variant 2 as the base.
