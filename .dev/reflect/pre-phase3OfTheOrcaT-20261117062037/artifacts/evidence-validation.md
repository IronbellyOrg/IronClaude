# Evidence validation (Wave 5 gate)

Validator: evidence-validator agent (sonnet), read-only; it could not write this file, so the orchestrator recorded the result.
Scope: every file:line citation in adversarial/adversarial/merged-review-card.md (98 rows: code, spec and plan lines) plus the 13 Pass 2 inferred rows INF-001 to INF-013 against source.md (13 rows).

| Count | Value |
|---|---|
| total | 111 |
| FOUNDED | 110 |
| UNFOUNDED (dropped) | 1 |
| STALE | 0 |

## Dropped item
- Row 60, finding C-010 (a NOTE), citation "plan line 75": the card said "Task 4 changes five types or functions and two test files". Plan line 75 changes seven types or functions (`QuestionLine`, `_questions_panel`, `DeskView` (new), `View`, `build_view`, `Session`, `apply_key`), one constant (`QUESTIONS_KEYS_LINE`), and two test files. The merged card was corrected in place; the recommendation to split Task 4 is unchanged.

## Notes (left FOUNDED)
- Row 77: the line is built at view.py:678-685; the cited 677-686 runs one line past it.
- Row 71: "acceptance-tests.md ends at T56 (line 62)": the T-rows end at line 62; the file continues with other sections.

## Not checked by the validator
- "No questions-on screen golden exists" (C-002) has no line cited; the orchestrator's Grep in Round 2 (round-2-v3.md) found none.
- Convergence statuses are not file citations.

Sampling: full re-read of all 111 citations (more than 20, but the validator re-read every one, so `citation_budget_policy` is `full_reread`).
