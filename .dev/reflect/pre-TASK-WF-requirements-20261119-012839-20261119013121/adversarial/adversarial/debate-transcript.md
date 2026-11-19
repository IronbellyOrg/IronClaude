# Adversarial Debate Transcript (v3 plan)
Depth quick (Round 1 only; no Round 2, invariant probe, Round 3 or position-bias pass). Advocates: 3 sonnet, read-only, each read cited code.
## Round 1 summary
V1 advocate: conceded its card is narrow and missed C-001, C-002, C-006; defended C-004, C-005, C-008, C-009; leaned toward blocking on the updatedAt fail-open half. V2 advocate: withdrew blanket Blocking labels; defended QA-1 (guard at Full Submit) and QA-3 (Project id); agreed adding tests alone does not close the gap. V3 advocate: defended F-1 (self-approval chain), F-2 (ship gate), the fail-open half of F-3; conceded F-5 and F-6 are overstated and that the "every approval voided" half of F-3 is probably wrong (a label bumps the issue, not the Project item).
## Scoring matrix
| Point | Winner | Confidence | Severity agreed |
|---|---|---|---|
| C-001 guard allows issue writes at Full Submit; self-approval chain | V3 (V2 found the gap) | 85% | blocking |
| C-002 ship gate claim.md:133 unchecked | V3 | 75% | blocking |
| C-003 updatedAt behaviour untested (fail-open half) | V3 | 70% | blocking |
| C-004 reason precedence Task 4 vs 6 | V1, V2 | 85% | blocking |
| C-005 guard pattern unnamed | V1, V3 | 75% | medium |
| C-006 Task 9 lacks Project id | V2 | 75% | medium |
| C-007 level-None claim session | V3 (downgraded) | 55% | note |
| C-008 Task 6 acceptance order | V1 | 70% | medium |
| C-009 String! assertion | V1 | 60% | note |
| C-010 ordering notes | V1, V3 | 60% | note |
| X-001 | V3 on fail-open half | 70% | |
| X-002 | V3 plus V1 and V2 additions | 75% | |
| A-001 | ACCEPT (all three) | 80% | |
| A-002 | ACCEPT/QUALIFY/QUALIFY | 60% | qualify |
## Convergence
Resolved 14 of 16 points (S-001, S-002 not debated) = 0.875, threshold 0.80, CONVERGED.
