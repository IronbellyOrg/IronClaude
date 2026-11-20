# Round 1: Advocate 2 (variant 2, qa lens, haiku class)

Recorded by the orchestrator from the advocate's returned message. The advocate declined to write the file itself, so only its returned summary exists; the full statement was not saved. Nothing below was added to the advocate's text.

## Position summary

Variant 2 is stronger on the helper's hidden writes, the dropped patch-and-bundle capability and the missing pull-request finish. Variant 1 is stronger on acceptance ordering, the incorrect provenance count and conflicting removal fallbacks. Both support FAIL, but the helper finding needs narrowing: fetch is conditional, temporary-file deletion does not establish data loss, and the spec also requires helper reuse.

## Per-point verdicts

- C-001, acceptance ordering: Variant 1, confidence 0.92. Wider coverage; retain Variant 2's Task 7 dependency.
- C-002, helper writes: Variant 2, 0.94. `branch-landed.sh:99,182,40` establishes child writes hidden by canned helper replies.
- C-003, manual archive: Variant 2, 0.98. Spec line 214 promises patch and bundle; plan lines 25 and 170 explicitly drop it.
- C-004, finish: Variant 2, 0.97. Spec lines 276 and 379 require PR submission; plan ends at line 274.
- C-005, provenance count: Variant 1, 0.99. Spec lines 314-328 contain 15 rows; plan lines 253 and 256 require 14.
- C-006, fallback conflict: Variant 1, 0.98. Spec lines 297-298 prescribe conflicting paths; plan line 33 silently chooses Orca.
- C-007, coverage matrix: Neither, 0.99. Neither visible card supplies it.
- X-001, helper safety: Variant 2, 0.94, as a requirement conflict rather than proven destructive behavior. Silence is not opposition.
- X-002, dependency extent: Variant 1, 0.92, supplemented by Variant 2's Task 7 observation.

## Shared assumptions

- A-001: QUALIFY. Per-task acceptance is implied, but verification timing is not explicitly defined.
- A-002: QUALIFY. Grade each concrete consequence independently; neither card's blanket BLOCKING labels establish equivalence.
