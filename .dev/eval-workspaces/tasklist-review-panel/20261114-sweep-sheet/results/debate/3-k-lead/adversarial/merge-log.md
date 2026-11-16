# Merge Log

## Metadata
- Base: V3 (sonnet:architect), amended with V1's `no_source` finding and V2's note list and cost-of-fix argument, plus the fault-finder's process gaps.
- Executor: the orchestrating Sonnet session (not the `merge-executor` agent, which prefers Opus; Opus is reserved for blind scoring).
- Merged output: `../VERDICT.md`
- Status: partial (condensed scoring; orchestration and merge by the main session; no Round 3 at standard depth).

## Changes Applied
| # | Change | Source | Applied |
|---|---|---|---|
| 1 | Verdict PASS and the four-test table | V1, V2, V3 Round 2 rulings | yes |
| 2 | Five attack questions answered | V3 section 5, V2 section 3, V1 section 3 | yes |
| 3 | Notes N1 to N12 | V1 to V3 notes, fault-finder INV rows | yes |
| 4 | Reading sentences for the owner | V3 Round 2 item (d), edited to the verified facts | yes |
| 5 | By-hand owner records | fault-finder minimum record, checked on disk (hash, size, untracked state) | yes |

## Post-Merge Validation
- Every file, line and number in VERDICT.md was checked against disk by the orchestrator in this session, except the items marked UNVERIFIED.
- No file outside this output folder changed (find newer than the debate start; only the code-index database files, which a background watcher maintains).

## Summary
Planned 5, applied 5, failed 0, skipped 0.
