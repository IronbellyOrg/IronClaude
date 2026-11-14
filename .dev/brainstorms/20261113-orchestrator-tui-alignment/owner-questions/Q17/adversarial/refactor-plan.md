# Refactoring Plan: Merge into Base (Variant 2, proposal-B)

## Overview
- Base: Variant 2 (proposal-B, not now)
- Incorporating strengths from: Variant 1 (proposal-A), Variant 3 (proposal-C), advocate suggestions
- Planned changes: 4
- Risk level: Low (all additive)

## Planned Changes

### Change 1: Written re-ask trigger (from all three advocates)
- **Source**: round1-advocate-1.md "Suggested merge"; round1-advocate-2.md "Concessions" 1; round1-advocate-3.md "Overall"
- **Target**: Base, "What happens next if the owner picks it" (append)
- **Rationale**: base weakness U-002 ("not now" has no trigger) named by all three advocates.
- **Integration point**: bullet: the ledger records a re-ask trigger: ask Q17 again when Q19 (which reviewer ask comes first) picks Decision Desk or OB-09 is scheduled, and only after PR #539 has merged.
- **Risk**: Low.

### Change 2: Freshness gap recorded for any later yes (from Variant 1)
- **Source**: Variant 1 "What it costs or risks" bullet 4; diff points U-001, C-005
- **Target**: Base, "What happens next" (append, next to the contract-note bullet)
- **Rationale**: C-005 and U-001 won by Variant 1 unanimously (75 to 85 percent).
- **Integration point**: bullet: the contract note also records that sweep facts are always older than live Orca rows (the coordinator sweep is capped at once per 5 minutes, a cap and not a schedule, ADJ line 81), so any later panel must show the report age prominently.
- **Risk**: Low.

### Change 3: Leave room in Decision Desk (from Variant 1 advocate)
- **Source**: round1-advocate-1.md "Steelman of Variant 2" critique and "Suggested merge"
- **Target**: Base, "What it costs or risks", layout-rework bullet (append a mitigation)
- **Rationale**: reduces the base's own layout-rework risk at the cost of one sentence.
- **Integration point**: after "adding them later may mean reworking its layout".
- **Risk**: Low.

### Change 4: Possible home for a joined view (from Variant 3)
- **Source**: Variant 3 "What happens next" bullet 4 and "What stays unresolved"; diff point C-004 (advocate 3)
- **Target**: Base, "What stays unresolved" (append)
- **Rationale**: base leaves the joined view homeless; v2 is linked to sweep facts through SW-11 (MR line 200) but is unbuilt.
- **Integration point**: new bullet.
- **Risk**: Low; must say v2 is unbuilt.

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| X-001 | Yes now (V1) or never (V3) | All three advocates judged "not now" best; V1 needs unmerged and unscheduled work; V3 exceeds the evidence (ADJ line 361 is about "now") |
| C-002 | Make Q9 a requirement now (V1) | Q9's own recommendation is "Not now" (ADJ line 779) |
| C-003 | Demote the verbatim-words rule to history (V3) | Keeping it live costs nothing |
| C-001 | Remove the SW-11 to OB-09 soft edge (V3) | The soft edge costs nothing while inactive |
| (V3 clause) | "The sweep reads no observer output" | Outside the question; no source asks for it |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 to 4 | Low | None beyond the base | Remove the added text |

## Review Status
- Approved by: auto (non-interactive)
- Approval timestamp: 2026-11-14
