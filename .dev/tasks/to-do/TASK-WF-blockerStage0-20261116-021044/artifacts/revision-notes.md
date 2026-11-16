# Revision notes: stage 0 plan

Revision 1, 2026-11-16, made in place after the pre-execution review (status NEEDS-REVISION, 2 blocking and 9 non-blocking findings).

| Review item | Findings | Where the plan changed |
|---|---|---|
| R-001 | F1 | Constraints (new bullet: PF files read-only except the spec; evaluate.py only on a real copy); Task 3 body and two acceptance lines (copy under `./artifacts/results-check/`, hash and blob id before and after) |
| R-002 | F2 | Task 4 body (old-rule injection confound, grader instructions, lower-bound reporting) and one acceptance line; Task 10 body and acceptance line carry the confound |
| R-003 | F3, F5 | Task 9 body (adds spec lines 1011 and 1108) and widened grep acceptance line; Task 10 acceptance lines (OD3 and OD4, five findings, package id in the ledger section) |
| R-004 | F4, F6, F7, F10 | Task 2 body and acceptance line (frame rules); Task 5 body and acceptance line (keywords, all 318 rows, repeat groups, sample listed once); Task 6 body and acceptance lines (sample scored in its own section, disjointness by source path) |
| R-005 | F8, F9, F11 | Constraints (always-staged bullet); Task 7 body (compute n at recall 0.90 and 0.95; advisory fallback expected); Task 8 body and acceptance line (`Source path and line or heading` column, `@E2` rows through `git show`) |

Not changed: the task order, the phase structure and the 10-task count. The review's report describes the plan as it stood before this revision; the plan has not been re-reviewed.
`source.md` was refreshed from `stage-requests/stage0-request.md` (which now carries a "Revision 1" section) so the plan and its source agree.
