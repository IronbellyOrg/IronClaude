# Refactoring Plan (merge of reviewer cards into one verdict)

Base: V3. Approval: auto-approved.

## Planned changes
| # | Change | Source | Rationale (debate evidence) | Risk |
|---|---|---|---|---|
| 1 | Add sync-dev gap as medium (M1) | V1 F1, V2 F1, V3 confirm | unanimous | Low |
| 2 | Add baseline-pid gap as medium (M2) with the Tasks 1-3 argument | V3 round 2 | 2 of 3 medium | Low |
| 3 | Keep setsid-reasoning gap as medium, inferred (M3), cite HEAD guard proxy:1012-1019 | V3 F1 | unanimous medium | Low |
| 4 | Add HC5 off-path review as minor (M4) | V2 F2 | 2 of 3 minor; HC5 advisory | Low |
| 5 | Add `contains` vs `ends with` as minor (M5) | V2 F3 | unanimous minor | Low |
| 6 | Keep sleep-check, teardown/pgrep, dependency-chain, pkill-vs-pid, scope wording as minor (M6-M8) | V1 F4/F5, V3 F2-F4 | uncontested | Low |
| 7 | Add rollout caveat (M9), subreaper (M10, inferred), session check only on direct start (M11) as non-blocking | invariant probe | INV-001/002/003 | Low |
| 8 | Correct V3's C-009 citation to test_ccsession_tiers.py:843-882 (fixture), :855, :863 | V3 concession | | Low |

## Changes NOT being made
| Item | Reason |
|---|---|
| Stale line anchors as a plan defect (V1 F3) | anchors matched remediation-source.md and the executor's ledger when the plan ran; kept only as an informational note about HEAD drift |
| Temp-HOME gap (V3 F5) | `_real_launch` sets HOME; withdrawn by V3 |
| V2's FAIL verdict and "Blocking" label | withdrawn by V2 in round 1 |
