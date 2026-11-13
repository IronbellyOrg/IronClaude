# RESULT: c2-haiku-grok (t4-1 = claude-haiku-5-5, t4-2 = grok-4.7)

No scoring. "Findings" = lines in the reviewer's own findings-v1 block (blocking in parentheses). Merged = ledger rows in merged-1.md (blocking rows in parentheses). No reviewer was thin (under 1000 output tokens) or invalid. Every run took one attempt. Observed model `grok-4.7-build` is accepted by the script as grok-4.7.

## TASK-WF-designSpec-20261107-075614
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings (blocking) |
|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 246 | 54277 | no | 9 (1) |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 1214 | 77280 | no | 3 (0) |

Totals: wall 1460 s (sum of both runs; two ran at once), output tokens 131557. Merged: verdict FAIL, 6 ledger rows (1 blocking). File: combos/c2-haiku-grok/TASK-WF-designSpec-20261107-075614/merged-1.md

## TASK-WF-makeTheAliasOnly-20261105-051649
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings (blocking) |
|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 273 | 63877 | no (category normalised) | 11 (2) |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 710 | 45925 | no (category normalised) | 5 (2) |

Totals: wall 983 s, output tokens 109802. Merged: verdict FAIL, 7 ledger rows (2 blocking). File: combos/c2-haiku-grok/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md

Category normalised: the first merge refused both reports only because of `unpassable-ac` (2 occurrences in each). Per the SPEC correction, I merged copies (`t4-1.md.catfix.md`, `t4-2.md.catfix.md`, made with `sed 's/unpassable-ac/unpassable-check/g'`) and left the original reports unedited. No reviewer rerun.

## TASK-WF-design-20261108-041415
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings (blocking) |
|---|---|---|---|---|---|---|---|
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 260 | 52477 | no | 7 (1) |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 661 | 42226 | no | 6 (2) |

Totals: wall 921 s, output tokens 94703. Merged: verdict FAIL, 2 ledger rows (1 blocking). File: combos/c2-haiku-grok/TASK-WF-design-20261108-041415/merged-1.md

## Files
Reviews: `<package>/reviews/combos/c2-haiku-grok/`. Resolutions and ledgers: `combos/c2-haiku-grok/<package>/`.
