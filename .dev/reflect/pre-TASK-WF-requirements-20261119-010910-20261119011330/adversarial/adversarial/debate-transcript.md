# Adversarial Debate Transcript (v2 plan)
Depth quick (Round 1 only; Round 2, invariant probe, Round 3 and position-bias pass skipped). Advocates: 3 sonnet, read-only, each read cited code.
## Round 1 summary
V1 advocate: defended N-2 (test_security_invariants.py:915, :918) and N-1 (guard has no prompt allow-list), conceded it missed C-005 and C-008 and treated the self-call as open. V2 advocate: defended QA-1 and QA-2 (cycle.py:1099-1109), conceded over-labelling and no guard lines; called the self-call a conflict, not an open choice. V3 advocate: defended B-1, B-2, M-a, M-b; conceded it missed C-002, C-003, C-004, C-008, C-009; said B-2 may partly be an owner decision.
## Scoring matrix
| Point | Winner | Confidence | Severity agreed |
|---|---|---|---|
| C-001 self-call bypasses guard and coordinator-only writes | all three | 90% | blocking |
| C-002 Task 10 breaks test_security_invariants.py:911-919 | V1 | 85% | blocking |
| C-003 guard has no prompt allow-list; Task 6 edits wrong place | V1 | 75% | medium |
| C-004 missing Depends-on edges, item-id read | V1 | 75% | medium |
| C-005 Pipeline provenance unproven | V3 | 70% | blocking, owner decision |
| C-006 marker author and Status retry | V3 | 70% | medium |
| C-007 Status command vs launch level, end Status | V3 | 70% | medium |
| C-008 killed child leaves no launched line | V2 | 80% | blocking |
| C-009 Spec judgment lacks acceptance test | V2 | 65% | medium |
| C-010 NG-2 header and scan | V3 | 60% | note |
| X-001 | V2+V3 | 75% | conflict, not design choice |
| X-002 | V2 on C-008; C-009 medium | 70% | |
| A-001 | QUALIFY/ACCEPT | 65% | |
| A-002 | split (REJECT, ACCEPT, QUALIFY) | 40% | unresolved |
## Convergence
Resolved 13 of 16 points (S-001, S-002 not debated; A-002 split) = 0.8125, threshold 0.80, CONVERGED at the margin. Unresolved: A-002.
