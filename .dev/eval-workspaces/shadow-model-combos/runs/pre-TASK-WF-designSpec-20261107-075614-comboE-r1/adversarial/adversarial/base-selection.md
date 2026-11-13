# Base Selection
Method: orchestrator (judge) assessment, single pass. The 30-criterion dual-pass rubric was not run (cost); counts below are findings-level, not rubric scores. Documented deviation.

| Variant | Findings | Survived the debate (full or reduced) | Unique survivors | Citation defects |
|---|---|---|---|---|
| V1 (analyzer) | 11 | 9 (F7 dropped as refuted, F4 re-cited) | 5 (C-006..C-009, C-011) | 1 (F4 line) |
| V2 (qa) | 5 | 5 | 0 | 1 (F4 line 420) |
| V3 (refactorer) | 7 | 7 | 3 (C-012..C-014) | 1 (F7 path) |

## Selected Base: Variant 1 (analyzer)
Rationale: widest verified coverage and the only variant that found spec-internal contradictions; V1 loses F7 (refuted) and carries one wrong citation. Strengths to incorporate from V3: C-012, C-013, C-014 (Low). From V2: tighter wording of C-001..C-004.
Tie-breaker: not needed (V1 leads V3 by more than 5% on survivors).
