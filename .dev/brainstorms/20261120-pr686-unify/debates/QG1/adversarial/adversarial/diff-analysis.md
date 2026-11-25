# Diff Analysis: debate position papers (QG1 planning and hand-back) Comparison

## Metadata
- Generated: 2026-11-20 (UTC, pipeline run for topic QG1)
- Variants compared: 2 (Variant 1 = OURS, `variant-1-original.md`; Variant 2 = CLAY, `variant-2-original.md`)
- Total differences found: 16 debated points (S 2, C 7, X 3, A 4) plus 7 unique contributions (not debated)
- Categories: structural (2), content (7), contradictions (3), unique (7), shared assumptions (4)
- Taxonomy tags (L1 surface, L2 structural, L3 state-mechanics) are shown in the last column of each table.
- Source of the compared claims: the three open questions OD-1 (default plan depth), OD-2 (how hand-back round 2 starts), OD-13 (a waiting hand-back versus the in-flight count).

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity | Level |
|---|------|------------------|------------------|----------|-------|
| S-001 | Heading set and order | Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right (all H2) | Identical six H2 headings in the same order | Low | L1 |
| S-002 | Kind of evidence cited | 9 facts, mostly second-hand (verdict files D01, D12, D14, D15) plus 3 code lines (`predicates.py:249-259`, `route.py:379-426`, `cycle.py:993-994`) | 9 facts, mostly first-hand design lines (D:60, D:610-620, D:722-724, D:1076-1083) plus 2 verdict references | Medium | L1 |

## Content Differences

| # | Topic | Variant 1 (OURS) Approach | Variant 2 (CLAY) Approach | Severity | Level |
|---|-------|---------------------------|---------------------------|----------|-------|
| C-001 | OD-1 default depth of the plan call | `quick` (the `--plan` default; same as no key). Claim 1 | A stronger default via `plan_tier` = `tier1b` (D:60, D:724), which D15 reads as implying `deep`. Claim 1 | High | L2 |
| C-002 | Shape of the plan setting | One plain key `plan_depth` passed straight to `--depth`; no tier table (merged D15 G-2) | `plan_tier` mapped to `--depth` by a table in `refs/intake.md` of PR P, which is not on master (UNVERIFIED) | Medium | L2 |
| C-003 | OD-2 how hand-back round 2 starts | Re-plan the body, then the person re-applies the approval (option a); no separate chat go per round | No new approval: wave 8 hands the issue back to the orchestrator, wave 2 re-plans via `--plan --remaining --depth` and the same waves run (D:610, D:615, D:618); option (b) named as the alternative if a gate is wanted | High | L3 |
| C-004 | OD-13 a waiting hand-back versus `max_in_flight` | Exclude the waiting step from the count; show a waiting reason; add an expiry later | Keep the issue `in_progress` and counted; the place is never freed between rounds (D:616); no waiting step exists | High | L3 |
| C-005 | What guards plan quality | The person's approval (the check proves presence only) | A stronger planner (goal G6, D:60): a weak plan multiplies cost downstream | Medium | L2 |
| C-006 | Hand-back loop bounds and restart safety | Mentions `HANDBACK_MAX` = 3 as unmeasured; no loop mechanics | Verb `handback` with stop reasons `cap`, `no_progress`, `no_remaining`; old worker must be final; re-plan marker `<!-- sc:issue:replan round=<n> -->` makes a rerun write nothing (D:612-614, D:1078) | Medium | L3 |
| C-007 | What wakes the coordinator after re-approval | Names it as a required condition (C-INV-2): the poll never wakes an acknowledged entry (`cycle.py:993-994`) | Not needed in its design: the orchestrator continues itself, nothing waits | Medium | L3 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact | Level |
|---|-------------------|--------------------|--------------------|--------|-------|
| X-001 | Which depth the plan call runs by default | "`quick` ... the opposite of Clay's goal G6" (V1 Claim 1, costs) | `plan_tier` default `tier1b`, which implies `deep` (V2 Claim 1) | High | L2 |
| X-002 | Is a held place with no worker a defect? | "A waiting issue has no worker running ... only live work holds a place"; three waiting issues block the repo (V1 Mechanism, fact 7) | "Keeping the place counted gives one simple invariant: in flight means someone owns it" (V2 Gets right); concedes the block as a cost (V2 Costs) | Medium | L3 |
| X-003 | Does round 2 pass a start gate again? | Yes, it must: a re-plan voids the approval (`predicates.py:249-259`) so approval comes after the plan (V1 Mechanism, facts 4, 5) | No: hand-back goes "to the orchestrator and not to the owner" (V2 Claim 2, fact 4); V2 fact 9 admits the design text has no round-2 approval | High | L3 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | 1 (OURS) | Invariants C-INV-1 and C-INV-2 (waiting issue must not hold a place; something must wake the coordinator after re-approval) | High |
| U-002 | 1 (OURS) | Code evidence of what counts as in flight (`route.in_flight`, `route.py:379-426`): only `in_progress` files, live poll entries and open plan requests count | Medium |
| U-003 | 1 (OURS) | The dependency on D14: both gates stay only if the owner says so; fit of the restored WC-17 as round-2 gate is UNVERIFIED | Medium |
| U-004 | 2 (CLAY) | Rationale G6 (stronger models plan, cheaper models build) and the cost-cascade argument | High |
| U-005 | 2 (CLAY) | Loop mechanics: `handback` verb stop reasons, old worker final first, idempotent re-plan marker, restart rules (D:612-620) | High |
| U-006 | 2 (CLAY) | `--remaining` rewrites only `## Fix approach` and `## Test plan`, keeps `## Priority`, saves `plan-before-round-<n>.md` (D:1076-1080); fidelity of done items is UNVERIFIED (U60) | Medium |
| U-007 | 2 (CLAY) | Self-found gap: Clay's wave-1 re-check covers only `hold:backlog` and `plan_check`, not the approval (V2 fact 9 citing D01 MR-1) | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | Both accept `--plan --depth quick/standard/deep` with workers t3/t2/t1 (V1 fact 3; V2 fact 3) | A deeper planner produces a materially better plan, or at least one worth its cost; no measurement of plan quality or cost per depth is cited by either paper | UNSTATED | Yes |
| A-002 | Both accept `HANDBACK_MAX` = 3 (V1 fact 9; V2 Claim 3, mechanism) | Hand-backs are rare enough that a pile of waiting or counted issues stays small (the state of the in-flight set stays below `max_in_flight` = 3) | UNSTATED | Yes |
| A-003 | Both accept that a re-plan voids the approval (V1 fact 4; V2 fact 9) | An approval is a guard that proves a person said yes. D01 records that a login-based approval is weak against an agent on the same login (accepted risk L-1; the orchestrator shares Clay's login, `orchestrator.md:111`) | CONTRADICTED (partly) | Yes |
| A-004 | Both quote the in-flight counting rule (V1 fact 8; V2 fact 5) | The counting code (`route.in_flight`) cited from PR 686 (snapshot `pr-a`) is the code that will land; D14 says PR 686 is adapted in place and its `repos.py` does not land | UNSTATED | Yes |

### Promoted shared-assumption diff points ([SHARED-ASSUMPTION])

| # | Assumption | Impact | Level | Status |
|---|-----------|--------|-------|--------|
| A-001 | Depth gives plan quality worth its cost | Decides OD-1 either way; neither default is evidenced | L2 | open for debate |
| A-002 | Hand-backs are rare | Decides whether OD-13 needs an expiry now or later | L3 | open for debate |
| A-003 | Approval proves a person's yes | Decides whether re-approval (OD-2 option a) is a real gate or a label | L3 | open for debate |
| A-004 | Counting code in PR 686 survives | Decides how OD-13's exclusion is implemented | L3 | open for debate |

## Summary
- Total structural differences: 2
- Total content differences: 7
- Total contradictions: 3
- Total unique contributions: 7
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 0, CONTRADICTED: 1)
- Highest-severity items: C-001, C-003, C-004, X-001, X-003
- Taxonomy coverage: L1 = S-001, S-002; L2 = C-001, C-002, C-005, X-001, A-001; L3 = C-003, C-004, C-006, C-007, X-002, X-003, A-002, A-003, A-004
- Total debated diff points for convergence: 16 (S 2 + C 7 + X 3 + A 4)
- Reviewer note (claim validity, not a diff point): V1 fact 2 cites D12 item 6, which defers a higher tier floor at issue creation for medium and complex issues. It is not about the `--plan` default depth. The deferral is a related cost-baseline argument, not a direct source for OD-1.
