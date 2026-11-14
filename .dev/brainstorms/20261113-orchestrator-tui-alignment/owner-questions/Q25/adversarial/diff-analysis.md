# Diff Analysis: owner-answer proposal comparison (Q25, who runs `/sc:pr-submit --monitor 3`)

## Metadata
- Generated: 2026-11-14
- Mode: A (compare), depth quick (Round 1 only)
- Variants compared: 3 (variant-1 = proposal-A worker then coordinator-launched PR session, variant-2 = proposal-B owner-opened PR session, variant-3 = proposal-C one top-level agent per PR item, no worker)
- Total differences found: 13
- Categories: structural (1), content (5), contradictions (4), unique (2), shared assumptions (1)
- Prerequisites validated: output path under `.dev/`; all three inputs exist.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Section layout | Same five sections | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Who starts the PR session | Coordinator, `orca agent launch` | The owner, by hand | Coordinator, `orca worktree create --agent` (one agent does both build and PR) | High |
| C-002 | Who builds the change | Supervised worker | Supervised worker | The same top-level agent | High |
| C-003 | Agents per PR item | 2 (sequential) | 1 worker plus 1 person-opened session | 1 | Medium |
| C-004 | Point where the person sees the diff before push | Coordinator shows it after `worker_done` | Owner sees it in the session they open | The agent stops and shows it before pushing | Medium |
| C-005 | Spec rows to reword | None | None (runs-in cells say "PR session") | Nine work-item rows | Low |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | Does the answer rest on an unverified Orca behaviour? | Yes: a second `agent launch` in a `worker-start` worktree | No | No | High |
| X-002 | Are supervised-worker controls (brief guard, heartbeats, admitted `worker_done`) kept for code? | Yes | Yes | No | High |
| X-003 | Is owner time spent per PR? | No (one confirmation) | Yes, every PR | No | High |
| X-004 | Who answers review findings: the author or a cold reader? | Cold reader | Cold reader (the owner's session) | Author | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 1 | A one-time check of the Orca behaviour before the first PR item, with a named fallback | High |
| U-002 | 2 | Person sees every change before publishing by construction, the literal reading of `WORKER-CONTRACT.md:244` | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | [SHARED-ASSUMPTION] A PR session (any of the three kinds) may commit and push in the item's worktree. The worker contract says "The coordinator performs every git and GitHub outward action ... in its own conversation" and "The coordinator commits or merges in a worktree only when no worker runs there" (`WORKER-CONTRACT.md:240,245`), while the spec gives the commit to the PR session (merged-requirements.md line 987, 6.4 rule 14) and forbids the coordinator from running pr-submit (line 962). No variant reconciles these | All three let the PR session commit and push | If the contract's "coordinator performs every outward action" governs, none of the three is compliant without a contract amendment or an explicit owner instruction per action | UNSTATED, promoted |

## Summary
- Structural 1, content 5, contradictions 4, unique 2, shared assumptions 1.
- Highest-severity items: C-001, C-002, X-001, X-002, X-003, A-001.
- Taxonomy tags: L1 S-001; L2 C-001, C-002, C-003, C-005, X-004; L3 C-004, X-001, X-002, X-003, A-001 (guards: who may publish, what is verified first, contract boundary).
