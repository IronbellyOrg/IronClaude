# Refactor Plan for Merged Design Artifact

## Overview

Base variant: Variant 2 — Quorum Top-Up Fallback Ladder with an Auditable Attempt Ledger.

Planned merge changes:

1. Add Variant 1’s reflect/swarm boundary language.
2. Add Variant 3’s minimal-risk implementation sequencing.
3. Resolve reduction/scorer ambiguity by defining separate views: attempt ledger, contributing reviewer set, semantic reviewer merge/scorer inputs, and metadata audit trail.
4. Add explicit accepted/rejected alternatives section.
5. Add implementation file surface and source-of-truth/sync notes.

## Planned Changes

| Change | Source | Target | Approach | Risk |
|---|---|---|---|---|
| C1 | Variant 1 | Architecture section | Append boundary responsibilities | Low |
| C2 | Variant 2 | State machine | Preserve as base | Low |
| C3 | Variant 3 | Implementation plan | Append phased rollout and tests | Low |
| C4 | Hybrid | Contract section | Normalize field names and terminal reasons | Medium |
| C5 | Hybrid | Alternatives section | Merge cheaper alternatives and rejected designs | Low |

## Changes Not Being Made

- No immediate fallback dispatch design: rejected for determinism and auditability.
- No verdict-layer special case: rejected because contract must remain fact-based.
- No global swarm fallback behavior in v1: rejected due blast radius.
- No quorum weakening or degraded relabeling.

## Review Status

Auto-approved for merged design artifact generation.