# r5-glm-haiku2 result (t3-1=glm-5.3, t4-1=claude-haiku-5-5, t4-2=claude-haiku-5-5)

No scoring. "Findings" = lines in the reviewer's own findings-v1 block; "blocking" = those marked blocking by the reviewer.
Wall seconds and output tokens are totals over all attempts (from <id>.cost.json; tokens = output_tokens_all). Thin = under 1000 output tokens (none). No category normalisation was needed (no `unpassable-ac` in any report). No reviewer was INVALID.
Reviewer runs: 9 of 9 valid (observed model matched, findings-v1 block present). Max 2 runs at once.

## TASK-WF-designSpec-20261107-075614
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t3-1 | glm-5.3 | glm-5.3 | 2 | 2899 | 183872 | no | 2 | 0 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 390 | 85607 | no | 6 | 0 |
| t4-2 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 159 | 35362 | no | 6 | 1 |

Total wall 3448 s (sum of runs), output tokens 304841. Merged: 8 ledger rows, 1 blocking. Merge OK; all three blocks accepted.
File: combos/r5-glm-haiku2/TASK-WF-designSpec-20261107-075614/merged-1.md

## TASK-WF-makeTheAliasOnly-20261105-051649
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t3-1 | glm-5.3 | glm-5.3 | 2 | 2698 | 180002 | block rejected by merge validator (see note) | 4 | 1 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 213 | 49477 | no | 6 | 1 |
| t4-2 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 161 | 37207 | no | 7 | 2 |

Total wall 3072 s, output tokens 266686. Merged: 7 ledger rows, 1 blocking. Merge OK.
Note: the merge reported "block ok false" for t3-1 (the script's own check saw a findings-v1 block, but the merge validator did not accept it; cause not investigated, not the `unpassable-ac` issue). The round was not refused, so per SPEC no rerun was done (glm already used both attempts). The merged ledger still lists t3-1 in row L1 and L2 as written by the merge tool.
File: combos/r5-glm-haiku2/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md

## TASK-WF-design-20261108-041415
| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking |
|---|---|---|---|---|---|---|---|---|
| t3-1 | glm-5.3 | glm-5.3 | 1 | 1266 | 92737 | no | 3 | 0 |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 273 | 57263 | no | 10 | 2 |
| t4-2 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 287 | 61002 | no | 7 | 1 |

Total wall 1826 s, output tokens 211002. Merged: 4 ledger rows, 2 blocking. Merge OK; all three blocks accepted.
File: combos/r5-glm-haiku2/TASK-WF-design-20261108-041415/merged-1.md

Raw reports, attempts and cost files: <package>/reviews/combos/r5-glm-haiku2/. Resolutions and ledgers: combos/r5-glm-haiku2/<package>/.
