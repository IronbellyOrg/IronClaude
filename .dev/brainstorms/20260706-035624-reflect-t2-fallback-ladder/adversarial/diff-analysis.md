# Diff Analysis: Reflect T2 Fallback Ladder Variants

## Metadata

- Variants compared: 3
- Variant 1: architect — append-only fallback attempt ledger at reflect/swarm seam
- Variant 2: analyzer — quorum top-up controller with auditable attempt ledger
- Variant 3: backend/refactorer — post-normalization top-up ladder with minimal-risk helper extraction
- Total substantive differences: 7

## Structural Differences

| ID | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Helper location | Prefers new `reflect/fallbacks.py` early | Prefers new `reflect/fallback.py` | Prefers keeping first pass in `ensemble.py`, extract later | Medium |
| S-002 | Metadata naming | `tier2_reviewer_attempts` / `fallback_certification` | `t2_fallback` / `reviewer_attempts` / `final_reviewer_set` | `fallback_ladder` / `contributing_reviewer_attempt_ids` | Low |
| S-003 | Swarm generalization | Extract slot-family resolver in swarm | Expose model-slot descriptors in swarm | Keep reflect-local first, widen transport resolver only as needed | Medium |

## Content Differences

| ID | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Dispatch timing | Full-primary fan-out then fallback | Full-primary fan-out then fallback | Full-primary fan-out then fallback | Low |
| C-002 | Fallback 2 trigger | Multiple primary failures or T1Model01 fails | Multiple primary failures, T1Model01 fails, or T1Model01 succeeds but does not repair diversity | Multiple primary failures or T1Model01 failure; also quorum/diversity still invalid | Medium |
| C-003 | Reduction inputs | Reduce over primary + fallback attempts, derive final set | Final reviewer set selection before reduce/contract | Reduce all attempts for audit visibility, scorer on contributors | Medium |
| C-004 | Contract semantics | Add descriptive metadata, keep verdict unchanged | Add explicit terminal reason enum | Add non-breaking metadata and contributor IDs | Low |

## Contradictions

| ID | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | Whether to immediately extract a new module | New helper module is recommended up front | New helper module is recommended | First pass may stay in `ensemble.py`, extract if large | Implementation sequencing only; merge can choose minimal initial extraction with a clean extraction boundary. |
| X-002 | Whether successful non-contributing attempts feed reduction/scorer | Says reduce over primary + fallback attempts but final facts from final reviewer set | Says final reviewer set before reduce/contract | Says reduce all attempts for audit visibility but adversarial scorer only on contributors | Needs explicit merged rule: audit ledger contains all attempts; semantic merge/scorer and verdict use contributing reviewers only. |

## Shared Assumptions

| ID | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | Existing retry and normalization must finish before fallback engages | All variants | Preserves retry matrix and parse salvage behavior | Accepted |
| A-002 | Fallback must be bounded to `T1Model01` and `T1Model02` for v1 | All variants | Prevents unbounded model calls | Accepted |
| A-003 | Existing verdict derivation must remain fail-closed | All variants | Avoids false green from relabeling | Accepted |
| A-004 | Diversity must be computed from resolved successful reviewer metadata | All variants | Prevents slot-name diversity from masking same vendor/model | Accepted |

## Unique Contributions

| ID | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | Variant 2 | Explicit terminal-reason enum for fallback outcomes | High |
| U-002 | Variant 3 | Phased rollout from pure helper tests to stub-only integration to real transport | High |
| U-003 | Variant 1 | Strong slot-family resolver boundary for swarm config | Medium |

## Summary

The variants converge strongly on a post-primary, post-normalization fallback top-up design with append-only audit metadata and unchanged verdict semantics. The main merge decision is implementation altitude: start with a small reflect-owned helper boundary, keep verdict logic unchanged, and widen swarm config only enough to resolve T1 slots safely.