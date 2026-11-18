# Round 1 summary (advocate statements, parallel; digest by the orchestrator, per-point tables verbatim in substance)

Advocates: A1 = Variant 1 (analyzer card, 14 findings), A2 = Variant 2 (qa card, 3 findings), A3 = Variant 3 (refactorer card, 2 findings). All three steelmanned the others and verified claims against source.md and the plan.

## A1 (for Variant 1)
- Claims: V1 is the only card that tests spec tables 4.1 and 4.2 against the plan. Real gaps: resume row 4 and RETRY_RELEASE re-enter release_decision whose inputs (applied_edits, target_sha) the resume_decision signature lacks (F2/F13, source.md:107, 109, 137, 166, 169); `not_applied` of a ready request may restore RELEASE_PENDING, the requested rows never set phase_before_request, plan:60 tests only HELD (F3, source.md:196-201); Wave 0 reconcile promise vs resume row 2 (F5, source.md:58, 164; plan:76); Phase enum values undefined while plan:90 asserts `engage_pending` (F10).
- Concessions: F1 should be MINOR (plan:124 states the reuse; V3 is right), blocking withdrawn. F4, F5, F6, F7 are spec-level ambiguities the plan copies faithfully: MINOR. F3 partly covered by plan:60 (general phase_before_request rule), downgrade to MINOR/MEDIUM. F13 duplicates F2. V1's blocking set realistically shrinks to F2/F13 at most.
- A-001 QUALIFY (AC weaker than prose is a defect only if a wrong implementation could still pass). A-003 QUALIFY leaning REJECT (tables not complete for a literal implementer; holes belong to the spec).
- Table: C-001 V3 0.7; C-002 V1 0.65 (severity debatable); C-003 V1 0.6; C-004 V1 0.6; C-005 V1 0.55; C-006 V1 0.55; C-007 V2 0.7; C-008 V2 0.5; C-009 V2 0.6; C-010 V3 0.7; C-011 V1 0.6; X-001 V3 0.7; X-002 no real conflict 0.8; X-003 V1 on existence of real gaps, V3's "no defect" wrong 0.65.

## A2 (for Variant 2)
- Claims: V2 is best calibrated on severity and blocking. F1 verified: Task 11 AC (plan:169) names twelve tests; prose (plan:166) omits release-failure retry, unreadable timeline and moved head (source.md:315, 317, 319); "one retry" has no check anywhere. F3 verified (plan:23, source.md:369 vs AC plan:126-129). MINOR is correct: no wrong runtime outcome follows.
- Concessions: V2's F1 has a garbled third citation path; F2 cites plan 517-518 (plan has 200 lines; real line is 111); refs empty; F2 is trivial and source.md:230 shows `false` where gh returns object or null; V2 missed cycle-id, V1's seams and `_RESOLUTION_SCRIPTS`.
- Against V1: F2/F13 are one gap filed twice and an orchestration detail the spec leaves open; F5/F7 spec-internal; F4 overcalled; six blockers not credible.
- A-001 QUALIFY. A-003 QUALIFY (accept for the pure tables, reject for SKILL orchestration inputs, which are spec gaps).
- Table: C-001 V3 70; C-002 V1 55 (MINOR, not blocking); C-003 V1 55 (MINOR); C-004 V1 55 (F6 MINOR right, F4 overcalled); C-005 V1 50 (spec-level, MINOR); C-006 V1 50 (spec-level, MINOR); C-007 V2 70; C-008 V2 55; C-009 V2 65; C-010 V3 60; C-011 V1 65; X-001 V3 70; X-002 V3's phrasing 60; X-003 V2 and V3 65.

## A3 (for Variant 3)
- Claims: V3's two findings are real, correctly cited and correctly MINOR. Verified plan:124 (reuse stated in prose), plan:127 (AC names only the mint place), plan:129 (phrases the protocol test asserts: no id reuse), plan:170 (trace asserts event order). `_RESOLUTION_SCRIPTS`: plan:108 conditional vs plan:113 assumed, source.md:299.
- Against V1: F3 overstated (plan:56 lists phase_before_request; first fold AC tests "restores phase_before_request"; Task 11 covers a ready `not_applied` that stays HELD); F2/F13 probably over-rated (the SKILL caller holds target_sha and the edit count; Task 8 says release uses "this cycle's applied-edit count"); only F5 is a plausible blocker; X-003 "any blocking defect" is a stretch.
- Concessions: V3 has two findings and ignores tables 4.1/4.2; "covers the reviewed requirements" is unearned; V1's F5 and F7 valid; V2's F1 and F3 legitimate.
- A-001 QUALIFY (MINOR unless a wrong outcome follows). A-003 QUALIFY (seams are caller wiring, not the tables).
- Table: C-001 V3 75; C-002 V1 on existence, closer to MINOR 55; C-003 neither, V1 overstated 60; C-004 V1 MINOR 55; C-005 V1 strongest finding but plan's own deliberate ordering 60; C-006 V1 55; C-007 V2 70; C-008 V2 65; C-009 V2 75; C-010 V3 70; C-011 V1 60; X-001 V3 (MINOR) ; X-002 V3 80; X-003 V3 on "no six blockers", V1 right that at least F5 is serious 55.

## Convergence after Round 1
Winners agree on 14 of 14 addressed C/X points and on A-001 and A-003 (QUALIFY from all three); S-001 and S-002 (volume and citation hygiene, L1) were not addressed by anyone. Severity of V1's findings F2, F3, F5, F7, F13 is the open question: all three advocates say MINOR except A1 keeps F2/F13 as "debatable, at most blocking" and A3 keeps F5 as "plausible blocker".
Taxonomy coverage: L1 (C-009), L2 (C-001, C-004, C-006, C-007, C-008, C-010), L3 (C-002, C-003, C-005, C-011, A-003) all covered.
