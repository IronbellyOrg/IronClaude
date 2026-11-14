# Diff Analysis: owner-answer proposal comparison (Q24, who runs the live reads)

## Metadata
- Generated: 2026-11-14
- Mode: A (compare), depth quick (Round 1 only)
- Variants compared: 3 (variant-1 = proposal-A fresh master-based capture session, variant-2 = proposal-B owner by hand, variant-3 = proposal-C the 409 session)
- Total differences found: 12
- Categories: structural (1), content (5), contradictions (3), unique (2), shared assumptions (1)
- Prerequisites validated: output path under `.dev/`; all three inputs exist.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Section layout | Same five sections | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Runner of XC-03 and XC-04 | New top-level agent in a master-based Orca worktree | The owner | The 409 session | High |
| C-002 | Runner of OB-03 (seeded writes) | Owner or a session the owner names | The owner | The 409 session, under a separate row | Medium |
| C-003 | Fit with XC-04's "master code" requirement | Native (master-based worktree, rebased after #539 merges) | Owner's environment, unspecified | Must use installed CLI or switch code; worktree on unmerged branch | Medium |
| C-004 | Risk to `issue-409-mvp` unpushed commits and records | None | None | Present; must not disturb before OB-01 | Medium |
| C-005 | Owner time cost | Low | High (three live sittings) | Low | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | Should an agent hold live-read permission rows at all? | Yes | No | Yes | High |
| X-002 | Does familiarity with the observer outweigh a clean runner? | No | n/a | Yes | Medium |
| X-003 | Is "one sitting" still achievable? | No (two sittings) | No | No, stated explicitly | Low |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 1 | The D-A risk applies to any newly launched agent: its terminal may be bound to a Run, so "holds no Run" must be read back, not assumed | High |
| U-002 | 2 | Removes delegated live-read authority entirely: every live Orca call made by a person | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | [SHARED-ASSUMPTION] A terminal that "holds no Run" can still read the Runs XC-03 and XC-04 need. Q-1 failed on 2026-11-11: a terminal not bound to a Run cannot read another terminal's Run (ADJ line 87). XC-04 compares ids "on one real Run"; whether a Run-less terminal can list that Run's workers with `worker-list --run <id>` is not stated by any variant | All three require a terminal that holds no Run | If a Run-less terminal cannot read another Run's workers, XC-04 (and parts of XC-03) cannot run as written by anyone | UNSTATED, promoted |

## Summary
- Structural 1, content 5, contradictions 3, unique 2, shared assumptions 1.
- Highest-severity items: C-001, X-001, A-001.
- Taxonomy tags: L1 S-001; L2 C-001, C-002, C-005, X-002; L3 C-003, C-004, X-001, X-003, A-001 (guard and boundary: who may call live Orca, terminal binding, master code).
