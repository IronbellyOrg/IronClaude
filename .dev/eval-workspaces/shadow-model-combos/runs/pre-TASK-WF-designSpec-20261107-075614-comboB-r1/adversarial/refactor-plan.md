# Refactoring Plan

## Overview
- Base: Variant 3 (reviewer-3 card). Incorporated: Variant 2 (F1, F2), Variant 1 (F2 same as V3 F3; rows-checked statement), invariant probe (INV-001, INV-002, INV-006).
- Output: a merged findings document and a merged verdict (`merged-verdict.yaml`) with severity settled by the debate.

## Planned Changes
| # | Change | Source | Target in base | Rationale | Risk |
|---|--------|--------|----------------|-----------|------|
| 1 | Set F1 (GuardRead adapter) severity MAJOR to MEDIUM; merge V1 F1 | V1 F1, Round 2 consensus | V3 F1 | all three advocates end at MEDIUM; malformed read falls into the unreadable path (source.md:117) | Low |
| 2 | Set F2 (stale held-guard cycle_id) MAJOR to MEDIUM; reframe as spec defect copied by the plan; add that spec never says which target_sha resume passes; mark HEAD REBIND as HEAD-only evidence | Round 2 (V1, V2, V3), INV-006 | V3 F2 | evidence source.md:107-109, :139, :156, :166 | Low |
| 3 | Add finding: zero-edit release (row 7) can release a guard still holding an earlier cycle's unpublished fix | INV-001 | new | source.md:155-156, :69; plan:75, :166 | Medium (probe-only, one agent) |
| 4 | Add finding: engage row 8 before row 10 halts an originally-draft PR on an unreadable timeline | INV-002 | new | source.md:140, :142; plan:70, :73-74 | Low |
| 5 | Merge V1 F2 into V3 F3 (Task 7 criterion versus conditional list) | V1 F2 | V3 F3 | same defect, 2 of 3 advocates | Low |
| 6 | Add finding: Tasks 9, 10, 12, 13 omit Task 1 dependency edges; withdraw V3 "all complete" | V2 F1, Round 2 | new | source.md:363; plan:134-137, :148-154, :179-182, :190-199 | Low |
| 7 | Add finding: Task 13 gives flags.md only a row | V2 F2 | new | source.md:245; plan:195-198 | Low |
| 8 | Keep F4, F5, F6, F7 at MINOR | V3 | V3 | conceded to LOW by V3 itself; F5 advisory | Low |
| 9 | Drop V2 F3 (coverage-matrix note) | Round 2 | none | not a plan defect | Low |

## Changes NOT Being Made
- V3 claim "Dependency lines checked against spec:363; all complete": rejected (false for Tasks 9, 10, 12, 13).
- V1 and V2 severity MINOR for C-001: superseded by MEDIUM consensus.
- Probe INV-003, INV-004, INV-005: recorded in invariant-probe.md only (LOW, weak or addressed).

## Review Status
auto-approved
