## Round 2: Rebuttals

### Variant 1 Advocate (analyzer), rebuttal
- Concedes "dependencies consistent" and "no missed defects" were wrong (spec 363; cycle-id gap).
- Holds C-001: resume_decision row 4 (spec 166) says "re-enter release_decision"; GuardAction (spec 82-85, 11 members) has no re-enter member; signature (spec 109, plan 70) lacks applied_edits and target_sha needed by release rows 7-8 (spec 155-156); plan 77 asserts no action. Rebuts V3's "must invent" (spec 280 lets the SKILL release).
- Structural points: S-001, S-002 change no verdict; S-003 now sides with MINOR; S-004 neutral.
- Verdicts: C-001 BLOCKING (an implementer must invent row 4's output; row 8 cannot run without target_sha); C-002 MINOR (fail-safe: held_cycle_published false, row 9 NOOP, PR stays draft).
- Engage ordering quirk (rows 2, 5-7 read guard.phase before row 10 handles guard is None, spec 134-142): real, MINOR spec hygiene; plan should state "guard None skips rows 2, 5-7".

### Variant 2 Advocate (qa), rebuttal
- Concedes thin coverage and bare row ids.
- C-007 re-checked against Tasks 3-5: reader side covered (plan 60: original_is_draft from first record or first skip; request/not_applied/request test; plan 62: pending_requests with :a<k> retries); no criterion anywhere checks the written key format guard:<run_id>:<cycle_id>:<to>:a<k> or first-request-only timeline_baseline at the writing point. Half-enforced, MINOR (~60).
- S-002, S-004: V2 weaker; A-002 real for its card.
- C-001: "blocking-leaning, major plan defect rather than a hard block" (spec 280 makes "no returnable action" arguable; plan 77 untestable as written). C-002: MINOR.
- Confirms the engage ordering quirk (Task 4 per-row tests would hit an AttributeError on a None guard), MINOR.

### Variant 3 Advocate (refactorer), rebuttal
- Concedes: "must invent" overstated; C-002 MAJOR too high; missed C-003..C-007.
- C-008: spec 363 violated in letter, transitively met in effect (Task 9 depends on 6 and 8, Task 8 on Task 1, plan 120; Task 12 on 6 and 8; Task 13 on 10, 11, 12); changes no implementation outcome: MINOR, no block.
- C-001: major plan defect, NOT BLOCKING (for: no re-enter GuardAction, signature lacks inputs, plan 73 requires action/reason/cause assertions, plan 77 names none; against: spec 280 "row 4 releases first" lets the SKILL call release_decision, implementer can pick a convention). Underspecified and untestable as written, not unbuildable.
- C-002: MINOR (plan 127 minting place only, plan 170 event order only; fail-safe).
- Agrees C-007 half-enforced; notes plan 124 omits spec 4.2 from Task 8's sources, minor since Tasks 3 and 11 cover the event contract.

## Structural-point coverage (taxonomy gate)
L1 surface: S-001, S-002, S-004 (finding counts, narrative form, row-coverage claims) addressed in Round 2. L2 structural: S-003, C-002, C-007, C-008, C-009 addressed. L3 state mechanics: C-001, X-002, engage ordering quirk, A-001/A-002 addressed. All three levels covered.
