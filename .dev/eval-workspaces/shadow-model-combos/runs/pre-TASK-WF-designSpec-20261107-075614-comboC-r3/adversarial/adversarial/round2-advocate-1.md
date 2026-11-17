### Variant 1 Advocate rebuttal

**Criticisms and responses**

- **Coverage (V2, V3 advocates): V1 audits only Tasks 1-4 and 9.** Conceded. V1 declared this limit itself. It is a reason to merge V2 and V3 in, not a reason to drop V1's findings.
- **F1 remedy vague (V3 advocate).** Conceded. V3's named sources (`guard.cycle_id`, `push_completed` `target_sha`, `applied_edits >= 1`) and its failing test should replace V1's two alternatives. V1's diagnosis (the vacuous head check, `target_sha=read.head_sha`) stands and both cards agree on it.
- **F2 (Wave 0 contradiction) is overstated.** Partly conceded, after a spot check. Spec line 241 says the bullet "contains no L3 or `draft` condition". The same line says it prints the unprotected line "at L3 with `--merge-guard off`". Plan line 137 repeats both clauses. But plan line 140 narrows the test: the bullet "contains no `L3 only` or `draft` gate wording". Read that way, a bullet that mentions L3 inside a sentence passes, and the test is passable. The defect is ambiguous wording between plan lines 137, 140 and the acceptance bullet ("names an L3 or `draft` condition"). It is not an unpassable check. I downgrade F2 from MAJOR to MINOR. It is still a real wording trap, and V3's F2 (placement only) does not cover it.
- **F3 low value.** Conceded: low severity, but correct.
- **A-001 / A-002.** Unchanged. F1 should be blocking. The spec origin of C-001 argues for recommending a spec amendment too.

**Other variants**

- V2's cycle-id finding (C-007) is stronger than I first allowed. V3's advocate says plan line 124 assigns a mint owner. That is true, but no test asserts equality, so V2's gap remains. MINOR-to-MAJOR is a calibration question, not a validity question.
- V3's whole-line pin (C-009) and same-file ordering (C-005) are the best repo-grounded catches in the set. V3 is the best base for a merge.

**New evidence:** the spot check of spec:241 and plan:137/140 above.

**Changed votes**
- C-002: old V1, new MERGE. Reason: V1's F2 survives only as a MINOR ambiguity, and V3's placement finding is also valid. Keep both as separate MINOR findings.
