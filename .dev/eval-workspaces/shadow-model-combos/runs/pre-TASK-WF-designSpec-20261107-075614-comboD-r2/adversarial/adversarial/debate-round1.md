## Round 1: Advocate Statements

### Variant 1 Advocate (analyzer card, sonnet class)

**Position summary.** V1 is the only card that audits the spec's decision tables for internal defects. It found five real table or plan defects (C-001 to C-005), each verified against the spec and plan lines. V2 is the best card on acceptance-criteria gaps, and V1 largely omits those. V3 found one weak item. V1 plus V2's unique findings should drive the merge, and V2's blocking flag on F1 is overstated.

**Steelman.** V2: a plan fails when its acceptance criteria cannot catch a wrong implementation. Task 4's body says `applied_edits` is "THIS cycle" (plan 70), but the AC at plan 75 only feeds `release_decision` a zero. The byte-identical pin compares against a start-text constant (plan 154). Task 9 AC (plan 139-144) omits the flag-row and wave-line tests the body requires (plan 137). V3: precise, zero-noise; its one finding is real because spec 175 itself writes "43 to 45".

**Strengths claimed.** F4 verified (spec 199, 138, 170; plan 70). F5 verified (spec 166 before 168; plan 77). F2 verified (spec 240 vs plan 124). F3 verified (spec 112, 135, 140; plan 61). F7 verified (spec 168 has no phase condition, row 5 has one).

**Weaknesses identified.** V2 F1 is blocking, but plan 70 says "THIS cycle", plan 124 says "this cycle's applied-edit count", plan 166 adds the zero-edit-after-fixing-cycle scenario: the gap is AC wording only, MAJOR at most. V2 F2 faults the plan for a method the spec mandates (spec 377). V3 coverage is thin: "assigned rows covered" for 16 rows is unevidenced.

**Concessions.** V1 F1 has a gap: a release request for the later cycle may refresh `cycle_id` in the fold; the effect table is silent, so this is a spec ambiguity, not a proven bug. V1 never checked AC gaps and treated INF-021 as covered. V1 marked all seven findings non-blocking; F4 and F5 plausibly warrant blocking. F6 and F7 are low value.

**Shared assumptions.** A-001 ACCEPT (tables are the intended behaviour). A-002 ACCEPT. A-003 QUALIFY (body text is an instruction to the executor, so body-only requirements are weakly gated, not ungated).

**Point verdicts.**

| point | verdict | confidence |
|---|---|---|
| S-001 | V3 cleaner, V1's prose useful and harmless | 60 |
| S-002 | all-zero blocking too lax, V2's F1 blocking too strong; F4 and F5 are the better blockers | 65 |
| S-003 | V1 better (its quotes survive the pre-check) | 80 |
| C-001 | real defect, V1 superior (release request may refresh the id) | 65 |
| C-002 | real defect, V1 superior | 90 |
| C-003 | real, minor | 80 |
| C-004 | real defect, V1 superior | 85 |
| C-005 | real defect | 80 |
| C-006 | F6 real ambiguity; F7 real but low impact | 70 |
| C-007 | V2 right on the AC gap, "blocking" overstated | 70 |
| C-008 | V2 real, minor | 70 |
| C-009 | real, shares a root with C-001 | 75 |
| C-010 | real but low | 60 |
| C-011 | mostly real; Task 9 AC omission verified (plan 137 vs 139-144) | 70 |
| C-012 | weak, spec mandates constants | 70 |
| C-013 | real but low (spec 175 uses "43 to 45") | 65 |
| X-001 | V2 partly right: gap in the AC, body covers it | 70 |
| X-002 | no real conflict | 85 |

### Variant 2 Advocate (qa card, haiku class)

**Position summary.** V2 is strongest where the plan's ACs are weakest, but its one blocking finding is overstated, and it misses the two largest spec defects V1 found.

**Steelman.** V1: decision tables are where a shipped guard fails by leaving a PR ready or releasing it wrongly. Spec 190 lists `cycle_id` in the fold, but no effect row (194-206) sets it, and engage row 7 (139) returns NOOP without a request, so a reused held draft is judged against the old id. Spec 240 says "sections 3 and 4.1 to 4.4", plan 124 builds from 3, 4.1, 4.5, 4.6, 5. V3: narrow, does not overclaim; its "covered" claim for INF-048..063 has no per-row evidence.

**Strengths claimed.** Per-cycle `applied_edits`: spec 107 and 366 require an AC; Task 4 (plan 75) tests only the function with an input count; Task 8 ACs (127-130) never check the ref uses this cycle's count although its body (124) says so; a run-wide caller passes every test. Byte-identical pins compare start text (plan 154). Task 9 body (137) requires flag and wave-line tests, its criteria (139-144) omit them. Task 10 consumes Task 8's file but declares only Task 9 (148).

**Weaknesses identified.** Overstated blocking: plan 75 and 166 do name the zero-edit-after-fixing case; the real gap is only the caller side. Inconsistent severity: F2 is MAJOR "unpassable-check" yet non-blocking, and its rationale contradicts its own claim. Missed defects: `cycle_id` non-rebinding, Task 8 source narrowing, resume row ordering. Untraceable restatement of T1-F4/F5/F6. Not verified: the 8 quote-not-found flags and what the pins literally match.

**Concessions.** F1 should be MAJOR and non-blocking unless the owner requires a call-site test. F2's blocking label contradicts its own reasoning. V1 found the spec-level defects V2 missed.

**Shared assumptions.** A-001 QUALIFY (a table gap is a spec defect the plan inherits). A-002 QUALIFY (HEAD is simply not evidence against the plan). A-003 ACCEPT (spec 366 makes ACs the gate).

**Point verdicts.**

| point | verdict | confidence |
|---|---|---|
| S-001 | layout only | 90 |
| S-002 | V2's blocking overstated; defect real at MAJOR, non-blocking | 65 |
| S-003 | cosmetic | 60 |
| C-001 | V1 superior; real | 85 |
| C-002 | V1 superior; real | 85 |
| C-003 | real but minor | 65 |
| C-004 | real; engage row 6 has no live-draft check | 65 |
| C-005 | real but overstated; release row 8 limits harm | 60 |
| C-006 | real, low; F7 overreads plan 77 | 55 |
| C-007 | V2 superior on the call-site gap; V1's "carried" overstated | 65 |
| C-008 | real, minor | 60 |
| C-009 | real | 60 |
| C-010 | real | 55 |
| C-011 | V2 superior; real | 75 |
| C-012 | real; start-text comparison | 75 |
| C-013 | real, low | 50 |
| X-001 | V2 superior at the call site | 65 |
| X-002 | not a contradiction | 60 |

### Variant 3 Advocate (refactorer card, opus class)

**Position summary.** V3's finding is real but minor: Task 2's grep criterion leaves room for judgment (plan 49-50). The other cards identify more consequential issues; V3 missed them.

**Steelman.** V1: the tables contain edge cases the plan's tests do not pin (stale `cycle_id`, failed-engage recovery; spec 138-140, 190-201; plan 60-62, 70-77); Task 8 omits spec sections 4.2-4.4 (spec 240; plan 124). V2: an AC must fail for a wrong implementation; missing per-cycle assertion (spec 107, 366; plan 70-77); Task 10 dependency list (spec 363; plan 146-150).

**Strengths claimed.** Narrow and directly actionable: make the "no remaining 43" grep check unambiguous (plan 49).

**Weaknesses identified.** Missed higher-impact gaps: per-cycle `applied_edits`, Task 8 omission, decision-table edge cases, Task 10 not declaring Task 8. Did not inspect the dependency structure closely: Task 8 depends on Tasks 4 and 7, Task 11 on 3, 4, 5, 7; the missing direct Task 8 dependency for Task 10 is the clearest structural concern (plan 118-124, 146-150, 159-165).

**Concessions.** V3's finding is low severity. V1's table findings and V2's AC/dependency findings deserve more attention. Not every spec-table inconsistency is solely a plan defect.

**Shared assumptions.** A-001 QUALIFY (an inconsistent table may need a spec clarification). A-002 ACCEPT. A-003 ACCEPT.

**Point verdicts.**

| point | verdict | confidence |
|---|---|---|
| S-001 | V1's organization aids review | 80 |
| S-002 | V2's single blocking finding better justified than all-zero | 80 |
| S-003 | V1 clearest | 75 |
| C-001 | V1 real ambiguity; require a decision on rebinding | 75 |
| C-002 | V1 superior | 95 |
| C-003 | V1 real mismatch | 70 |
| C-004 | V1 merits a test or spec correction | 75 |
| C-005 | V1 real row-precedence concern | 70 |
| C-006 | V1 stronger | 70 |
| C-007 | V2 superior | 90 |
| C-008 | V2 right | 80 |
| C-009 | V2 real | 75 |
| C-010 | V2 right | 85 |
| C-011 | V2 superior | 85 |
| C-012 | V2 valid | 70 |
| C-013 | V3 valid, minor | 90 |
| X-001 | V2 superior | 90 |
| X-002 | V2 identifies more uncovered requirements | 85 |
