# Refactor plan (verdict PASS: no file is changed)

## Overview
- Base: V3 (sonnet:architect). Incorporated: V1 (requirement points, text versus runs), V2 (routes R-E to R-I, the "descriptive only" sentence).
- Changes planned to files of the study: 0. A PASS changes no file (owner's rule). The only writes of this debate are inside `results/debate/2-cb2-verbatim/`.
- Risk: none for the experiment; the notes below are advice for the owner.

## Planned changes
None.

## Advice carried into VERDICT.md section 4 (not applied; each needs the owner)
| # | Advice | Source | Where it would go if the owner wants it | Cost |
|---|---|---|---|---|
| 1 | Add the count rule (n of N, exact upper bound, never "harmless") and the post-freeze limit to the DD-7 row and 15.1 row 3 (VERDICT N9, wording corrected for corrections item 5) | V3 option (d), V2 smallest edit, V1 concession | `DESIGN.md` DD-7 and 15.1; `results/owner-decisions.md` | text only; no hash, test or RL change |
| 2 | Widen `ledger_headings` (other spellings, `ledger-v1` blocks, per panel, N = 0), print `invalid` in the arm table, add a test beside `tests/test_report.py` 326, update `TESTING.md` 187 | V3, probe INV-007, INV-008, INV-009 | `analysis/analyze.py`, `tests/`, `TESTING.md` (all outside what this task may edit) | a follow-up change; until then the rule is applied by hand, as in debate 1 |
| 3 | Decide the K lead-in with CB-2 at step 14.3 | probe INV-006 | `results/owner-decisions.md` | none |
| 4 | If a real look at Z0 is wanted before the owner decides, order the timing spike before 14.3 (`run-panel.sh` accepts a null freeze tag) | V3 | the owner's schedule | about 5 Z0 panel runs; needs the owner's go-ahead |

## Changes NOT being made
| Diff point | Alternative | Why the default was kept (debate evidence) |
|---|---|---|
| C-003, C-008 | reword CB-2 for all arms (option b) | breaks REQ-05 as written (`test_cb_verbatim_against_mr`, MR 1124); removes the only PROBLEM-row-to-findings instruction (`DESIGN.md` 511-519); leaves CB-3 and CB-5 dangling; needs the Recipe Ledger copy changed |
| C-008 | per-arm variant with two hashes (option c) | breaks REQ-05 for Z0 and K and the Recipe Ledger rule that its brief starts with the Z0 brief (RL DR-2); adds an SS-versus-Z0 text difference no model has seen; new part, registry entry, 4+ test changes |
| C-004 | a new 5 Z0 + 5 K pilot on HO-6 (V2) | 10 panel runs, needs go-ahead; 15 reports with zero seen bound the rate only at 18.1%; the planned spike is cheaper |
| C-002 | the contingent reword of V2 (clause moved to an SS-only `ledger-link.txt`) | untested order change; only needed if a heading is seen; any change after 14.5 is a new freeze (`check-order.sh` 81 and 88) |

## Risk summary
Residual risk of the default: the clause's effect on found fraction, time and format failures is unmeasured and its direction unknown (UNVERIFIED). Rollback: before step 14.5 a reword costs edits and a test exception; after 14.5 it costs a new freeze.

## Review status
Auto-approved (non-interactive run; no `--interactive`). The owner has not confirmed decision 3.
