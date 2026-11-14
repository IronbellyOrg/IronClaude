# Refactoring Plan: Q14

## Overview
- Base: Variant 3 (proposal-C)
- Changes planned: 2. Overall risk: Low

## Planned Changes
1. **Sufficiency check at the gate.** Source: Variant 2 U-002; advocate V2's unassigned pick. Target: "What happens next" (V2-02 bullet). Approach: append: the dated gate entry states whether the recorded values are enough to build Rule 5's four conditions (classify.py:251-257); if not, that is recorded as a known v2 limit and a #534 row. Risk: Low.
2. **Optional fallback.** Source: Variant 1 U-001; advocates V1 and V3. Target: "What happens next" and "What stays unresolved". Approach: append: only if the owner sets a date and the capture still cannot run by then, the gate drops to #539 merged with live-value fields marked pending in the v2 design. Risk: Low (it applies only if the owner adds a date).

## Changes NOT Being Made
- Variant 2's SW-14 on the gate: rejected (X-003, 80 percent; W5).
- Variant 1's per-feature gate as the main gate: rejected (needs a field list that does not exist; C-001).

## Review Status
Auto-approved, 2026-11-14.
