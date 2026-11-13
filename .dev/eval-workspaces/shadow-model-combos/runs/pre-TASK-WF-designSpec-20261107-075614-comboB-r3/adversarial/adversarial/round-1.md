## Round 1: Advocate Statements

### Variant 1 Advocate (analyzer card)
position_summary: V1 is the most precise on C-001 and the only card that checks T1-F1..F5 against the files and narrows the ones that overreach. Misses: dependency lines (C-008), cycle-id equality (C-002), writer-side event fields (C-007).
steelman: V2 spotted that Task 8 builds the ref from spec sections 3, 4.1, 4.5, 4.6 and 5 (plan 124), leaving out 4.2 (spec 184-185). V3 is right that Tasks 9, 10, 12, 13 consume pre-build-gate.md (plan 137, 148-150, 182, 199) without listing Task 1 (spec 363), and held_cycle_published (spec 108) silently returns false if push cycle ids differ (no criterion at plan 127, 170-171; spec 251).
strengths: C-001 cited line by line (spec 109, 166, 107, 82-85; plan 73, 77); rebuts the "SKILL does the re-entry" reading (spec 280); narrows T1-F5 (already_draft stated at spec 112, 200); only card with C-003 (plan 182 vs 185), C-004 (spec 230, 89 vs plan 111), C-005 (plan 108, 113).
weaknesses: V2 has no per-row evidence and under-rates F2; V3 omits cycle_id from the C-001 signature gap.
concessions: "dependencies consistent" is wrong (spec 363); "missed defects: none" is wrong on the cycle id; V1's own noted quirk (engage rows 2, 5-7 read guard.phase while row 10 admits guard is None, spec 134-142) should have been reported.
verdicts: C-001 V1 70; C-002 V3 78 (MAJOR defensible, but fail-safe); C-003 V1 80; C-004 V1 70; C-005 V1 65; C-006 V1 60; C-007 V2 72; C-008 V3 85; C-009 V3 70; X-001 V3 85; X-002 V3 75.
A-001 QUALIFY (V1 findings are plan-vs-spec, base facts not needed). A-002 QUALIFY (V1/V3 show row-level evidence via overturned labels; V2 none).

### Variant 2 Advocate (qa card)
position_summary: narrow but correct on both findings; found the cycle-id gap V1 missed; coverage is the weakness (missed C-001, C-003, C-004, C-005, C-008).
steelman: V1 tests T1-F1 against the counter-reading (spec 280), finds the heading/grep mismatch (plan 182 vs 185), the boolean conversion (spec 230 vs plan 111) and the conditional _RESOLUTION_SCRIPTS (plan 108 vs 113). V3 reads section 10 best (spec 363; Task 9 reads pre-build-gate.md at plan 137 but lists Tasks 6 and 8) and ties cycle-id equality to held_cycle_published (spec 108, 251).
strengths: F2 correct (plan 127 checks only the minting place, plan 170 only event order; spec 251). MINOR is defensible: a mismatched id leaves the PR draft, the safe direction.
weaknesses: V1 says "none worth raising" while the gap exists, and calls dependencies consistent; V3 rates the gap MAJOR though it fails safe and omits cycle_id from the signature gap.
concessions: missed the row 4 gap (plan 70 lacks applied_edits and target_sha; plan 77 names no action); did not check Task 3 for C-007 (its shakiest finding); coverage claim is bare ids.
verdicts: C-001 V1 62; C-002 V3 58; C-003 V1 78; C-004 V1 80; C-005 V1 68; C-006 V1 60; C-007 V2 55; C-008 V3 80; C-009 V3 65; X-001 V3 75; X-002 V2 55.
A-001 QUALIFY (citing lines does not prove base excerpts were read). A-002 QUALIFY (only V3's four overturned rows are checkable).

### Variant 3 Advocate (refactorer card)
position_summary: only card that checks the plan against the spec's section 10 authoring rules (C-008, C-009). F1 (cycle-id) is real but over-rated; F2 is right on the signature but overstates the consequence.
steelman: V1 is most precise on row 4 (GuardAction has no re-enter member; plan 73 requires every row test to assert action/reason, plan 77 names none for row 4); finds three mechanical defects (plan 182/185, spec 230 vs plan 111, plan 108/113). V2 is right on both points; event-field contract (spec 184-185) has no writer-side check; cycle-id check is minting-place plus event order only; MINOR matches the fail-safe direction.
strengths: F3 (spec 363; Tasks 9, 10, 12, 13 read pre-build-gate.md at plan 134-137, 148, 179-182, 190-199 without listing Task 1); F4 (spec 369 bans file:NNN pointers; plan 128, 143 check only src/superclaude).
weaknesses: V1's "dependencies consistent" and "no missed defects" are wrong; V2 is thin.
concessions: F2's "must invent" overstates (spec 280 has the SKILL do the release; the accurate defect is V1's: row 4 returns nothing assertable); F1 at MAJOR is too high (fail-safe), MINOR is more accurate; missed C-003..C-007.
verdicts: C-001 V1 68; C-002 V3 55 (qualified toward MINOR); C-003 V1 80; C-004 V1 75; C-005 V1 70; C-006 V1 60; C-007 V2 65; C-008 V3 75; C-009 V3 75; X-001 V3 70; X-002 V3 65 (right severity is MINOR, closer to V2).
A-001 QUALIFY. A-002 QUALIFY.
