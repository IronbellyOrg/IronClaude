# c3-luna-grok RESULT (no scoring)

Row: t4-1 = gpt-6-luna, t4-2 = grok-4.7. Max 2 reviewers at once. Every reviewer was valid on attempt 1 (no retries). Thin = under 1000 output tokens: none were thin.
"Findings (own)" = findings in the reviewer's own findings-v1 block; "blocking (own)" = those marked blocking by that reviewer.
Merged = rows in merged-1.md (after de-duplication across the two reviewers). Every merge returned verdict FAIL, decision REVISE.

## TASK-WF-designSpec-20261107-075614
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings (own) | Blocking (own) |
|---|---|---|---|---|---|---|---|---|
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 37 | 1380 | no | 0 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 928 | 59959 | no | 2 | 1 |

Merged report: combos/c3-luna-grok/TASK-WF-designSpec-20261107-075614/merged-1.md. Findings in merged report: 2 (L1, L2); blocking: 1 (L1).
Totals: wall 965 s (sequential sum; luna and grok ran concurrently), output tokens 61339.

## TASK-WF-makeTheAliasOnly-20261105-051649
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings (own) | Blocking (own) |
|---|---|---|---|---|---|---|---|---|
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 100 | 4876 | no (category normalised) | 1 | 1 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 682 | 43957 | no (category normalised) | 5 | 2 |

The first merge was refused only because both reports used the category `unpassable-ac`. Per the SPEC correction, I merged `.catfix.md` copies (sed `unpassable-ac` to `unpassable-check`) in reviews/combos/c3-luna-grok/; the original reports are unedited. No reviewer rerun.
Merged report: combos/c3-luna-grok/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md. Findings in merged report: 4 (L1-L4); blocking: 2 (L1, L2).
Totals: wall 782 s (sequential sum), output tokens 48833.

## TASK-WF-design-20261108-041415
| Reviewer | Model | Observed model | Attempts | Wall s | Output tokens | Invalid/thin | Findings (own) | Blocking (own) |
|---|---|---|---|---|---|---|---|---|
| t4-1 | gpt-6-luna | gpt-6-luna | 1 | 44 | 1817 | no | 0 | 0 |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 844 | 53827 | no | 2 | 1 |

Merged report: combos/c3-luna-grok/TASK-WF-design-20261108-041415/merged-1.md. Findings in merged report: 2 (L1, L2); blocking: 1 (L1).
Totals: wall 888 s (sequential sum), output tokens 55644.

## Overall
Wall (sum of per-reviewer wall) 2635 s; output tokens 165816. Merged ledgers and resolutions are in combos/c3-luna-grok/<package>/.
