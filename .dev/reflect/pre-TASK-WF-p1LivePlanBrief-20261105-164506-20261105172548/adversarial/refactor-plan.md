# Refactoring plan (base: Variant 1, reviewer-1 card)

## Overview
- Base: `variant-1-original.md` (combined score 0.7511; V3 0.7441, V2 0.5829; tiebreaker level 1, debate points V1 10 of 17 decided).
- Output: `merged-review-card.md` in this folder, plus `merge-log.md`.
- Inputs for the merge: `base-selection.md` "Strengths to incorporate", `invariant-probe.md`, `round2-advocate-*.md`.
- Planned changes: 11. Rejected: 4. Overall risk: Low (the merged card is a review record; the plan itself was already fixed separately, see `../post-fix-rechecks.md`).

## Planned Changes

| # | Change | Source | Target in base | Approach | Rationale | Risk |
|---|---|---|---|---|---|---|
| 1 | Correct C-002 (V1 #2): drop "the tree already had tracked changes" and "the checks conflict"; restate as: the clean-tree check fails for any uncommitted edit to a tracked file (probe INV-001); fix = scope to `src plugins tests` | V1 base, V3 #3 (no-commit rule), invariant-probe INV-001 | row 2 | replace | Round 2 advocates 1 to 3 conceded the stale parts; the probe showed it fires for any plan edit | Low |
| 2 | Raise C-001 evidence: add "reproduced by three advocates: `cmp` rc=2 on README.md and `__init__.py`; introduced by revision 1 of the plan" | round1 advocates 1 to 3, round2 advocate 3 | row 1 | append | the cause matters for the record | Low |
| 3 | C-003 severity LOW; add the baseline-diff fix | V1 base, V2/V3 rebuttals | row 7 | replace | conceded to LOW; the spec says "no return-contract.yaml appears" | Low |
| 4 | Split C-004: swap Necessary (cite APPROVED.md G1, lines 66 to 71), quoting Drift LOW (fix: markers) | V1 base, V2 #1 | rows 3 and 4 | merge | X-002 resolved: not Drift for the swap | Low |
| 5 | Demote C-013 to a note | V1 base | row 8 | move to notes | spec line 238 has no "same tree" clause | Low |
| 6 | Add U-003 (watcher listing self-match) scoped to lc18 only | V3 advisory 1 | new advisory | insert | reproduced by advocates 1 and 3; lc08 wording says "started by the worker" | Low |
| 7 | Add U-004 (report-path comparison) | V3 advisory 2, INV-011 | new advisory | insert | real; fix is `realpath -m` | Low |
| 8 | Add INV-012 (Task 1 retry creates a second Orca run) | invariant-probe | new advisory | insert | probe finding | Low |
| 9 | Add C-009, U-006 and C-010 (as a process note) | V2 | rows 4 to 6 and notes | insert | complete the coverage | Low |
| 10 | Add a scope note: not checked (the `--parent-worktree active` effect at run time, `coordinator_handle` field name, `/sc:implement` behaviour on a failed Task 1 acceptance) | V3 notes, advocate 3 | notes | insert | honesty about limits | Low |
| 11 | Reclassify with the debate result: Regression 1 (C-001), Drift 5, Necessary 3, Authorized 2; counts in the title | all | title | replace | counts must match the rows | Low |

## Changes NOT being made
- U-005 (skills install exclusion): not a defect; three advocates ran the check.
- V2's "No Regression found": refuted (X-001).
- V3's Drift label for the grant swap (X-002): withdrawn by V3 in round 2.
- V1's C-002 "checks conflict at plan:58 and plan:65" as a stand-alone Drift: merged into row 1 above.

## Review Status
auto-approved (non-interactive).
