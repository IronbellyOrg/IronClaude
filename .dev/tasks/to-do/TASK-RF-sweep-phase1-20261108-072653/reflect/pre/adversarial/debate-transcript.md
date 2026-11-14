# Adversarial Debate Transcript

Abbreviations: TL is the tasklist `TASK-RF-sweep-phase1-20261108-072653.md`. DESIGN is `docs/designs/orchestrator-mode.md`. DA is `diff-analysis.md`. INV is `invariant-probe.md`. CAL is a card's Part 2 blind calibration (its `holds` and `calibrated_severity` outrank the card's own rating).

## Metadata

- Depth: standard
- Rounds completed: 2, plus the Round 2.5 invariant probe (no Round 3 at standard depth)
- Convergence achieved: 100% (39 of 39 points agreed by at least 2 of 3 advocates); strict reading with ties excluded: 89.7% (35 of 39)
- Convergence threshold: 80%
- Status: BLOCKED_BY_INVARIANTS (3 HIGH UNADDRESSED probe items: INV-001, INV-002, INV-009)
- Focus areas: all (S, C, X and the promoted A points from DA)
- Advocate count: 3 (V1 analyzer card, V2 qa card, V3 refactorer card)
- Subject: sc-reflect UC-1 pre-execution review of TL against DESIGN. The merged output is the single merged reflect verdict.
- Orchestrator role: coordinate and score only; no side argued.

## Round 1: Advocate Statements

Full statements: `debate/round1-v1.md`, `debate/round1-v2.md`, `debate/round1-v3.md`. Summaries only below.

### Variant 1 Advocate (analyzer card, 76 rows)

- Position: V1 is the only card on the FR, NFR and step spine (S-001), so the merged ledger needs its 76 rows.
- Steelman of others: V2 found every calibrated HIGH; V3 has the cleanest citations (40 checked, 0 failed).
- Strengths claimed: R1-G3 (the 14.11 lens searches the wrong folders, CAL MEDIUM, holds); full repo paths; traceability re-mapping (C-015).
- Weaknesses identified in others: V2 inflates severity (7 self HIGH, 3 calibrated); V3 files confirmations as findings (R3-G9, R3-G10).
- Concessions: V1 missed all three HIGHs; three factual errors (2.16 called an edit, X-003; "installs nothing", X-006; open item 2 instead of 3, X-005); 4 CAL citation failures (R1-G1, R1-G2, R1-G4, R1-G6).

### Variant 2 Advocate (qa card, 51 rows)

- Position: V2 holds every calibrated HIGH (R2-G7 deadlock, R2-G5 `grep -c`, R2-G3 echo) and the highest calibrated confidence (0.85), so it is the merge core.
- Steelman of others: V1's ledger is the widest; V3's design-fix slice (phases 2 to 6) is not covered by V2 at all.
- Strengths claimed: only card with `recommended_action` and `not_checked` (S-005); no confirmation filed as a finding (S-007); line-range citations (S-003).
- Weaknesses identified in others: V1 and V3 both miss the 6.2 deadlock; V3 R3-G10 calls the owner gate sound (X-001).
- Concessions: severity inflation (7 to 3 HIGH, X-008); the `gate-bypass` class on R2-G2 is contradicted by its own CAL; the INF-013 row conflicts with R2-G8 (X-007); one cite off by two lines (R2-G4: TL:1634, not TL:1635-1636).

### Variant 3 Advocate (refactorer card, 24 rows)

- Position: V3 is the only card on the design-fix phases and reuse, and its citations are the best grounded (S-006).
- Steelman of others: V2's three HIGHs hold under literal execution; V1's R1-G3 holds.
- Strengths claimed: R3-G4 (the owner is asked only for the rule id, CAL MEDIUM, holds); R3-G3 (dead `:545` greps); smallest self-to-calibrated gap (S-004).
- Weaknesses identified in others: V1's 2.16 misdescription (X-003); V2's INF-005 and INF-014 verdicts (X-010).
- Concessions: R3-G10 is wrong on the owner gate (refuted by TL:989); R3-G9 and R3-G10 are confirmations, not findings; R3-G1 was rated above what the text supports.

## Round 2: Rebuttals

Full rebuttals: `debate/round2-v1.md`, `debate/round2-v2.md`, `debate/round2-v3.md`.

### Variant 1 Rebuttal

- Response to criticisms: accepts the missed HIGHs and the three factual errors.
- Updated assessment: a higher view of V2, with the reservation that its HIGH fixes must name every site.
- New evidence: (1) R2-G5 is wider than any card says: `ClassifiedRow` and `SessionRow` each appear at least twice in a correct `models.py` (TL:1431, TL:1434, DESIGN:466). (2) 6.2 and 7.4 have two missing links: no step writes the owner's answer into the decision file, and Branch 1 fires on PENDING before Branch 2 can set RESOLVED; the HALT rule has no resume clause (TL:982, TL:989, TL:1165, TL:192). (3) The A-007 guard is TL:224, not TL:2508; item 1.3 does not HALT and does not cover the master pins. (4) R1-G3 is confirmed against DESIGN:777-778 and TL:2509. (5) X-004: DESIGN:216 asserts enforcement; the `pathlib` residue (TL:1432) is a design question.

### Variant 2 Rebuttal

- Response to criticisms: concedes D6 (R3-G4 is a separate MEDIUM) and A-007.
- Updated assessment: the INF-013 row should read "construction assigned; verification partial, see R2-G8".
- New evidence: (1) the 8.3 fix is to count declarations, not whole-name occurrences. (3) 7.16 needs an explicit narrow permission for the discovery commands, plus verification of command records instead of arbitrary captured output.

### Variant 3 Rebuttal

- Response to criticisms: accepts the R3-G10 refutation.
- Updated assessment: D6 should be relabelled `partial`; the FR-010 note should read "ambiguous after edit 4".
- New evidence: (1) a grep of "PENDING or" gives 9 lines (TL:989, 1140, 1151, 1165, 1179, 1193, 1207, 1221, 2481); proposes fix (a), a transcription step, and fix (b), Branch 1 only when `Chosen:` is empty. (2) In item 2.2, "Several matching rows" becomes "One or more matching rows". (3) A third missing link: TL:192 has no resume clause.

### Shared assumptions (all three advocates, Round 2)

| ID | V1 | V2 | V3 | Result |
|---|---|---|---|---|
| A-001 delegation counts as coverage | QUALIFY | QUALIFY | QUALIFY | Holds only if the delegated row survives the Phase 2 to 6 DESIGN edits (FR-010 is the tested case) |
| A-002 literal execution | QUALIFY | QUALIFY | QUALIFY | A literal reading decides whether a check passes; recovery awareness decides its severity |
| A-007 master anchors stable | QUALIFY | QUALIFY | QUALIFY | No item guards it (TL:224 is a note, not a HALT) |

### Merge direction (unanimous)

V2's three HIGHs as the core; V1's 76-row ledger plus R1-G3; V3's design-fix slice plus R3-G4.

## Round 2.5: Invariant Probe

Full results: `invariant-probe.md`. 21 items: 6 ADDRESSED, 15 UNADDRESSED (3 HIGH, 7 MEDIUM, 5 LOW).

- HIGH UNADDRESSED:
  - INV-001: applying the deadlock fix "once, in 6.2 and TL:1140" misses the six inline copies in 7.2, 7.4, 7.6, 7.8, 7.10 and 7.12 (TL:1151, TL:1165, TL:1179, TL:1193, TL:1207, TL:1221). 7.13 needs seven RESOLVED rows, so everything after it stays blocked.
  - INV-002: 7.15 does deadlock. 7.14 writes `Run id:` empty and no step copies the Run id, so 7.15 re-HALTs and 7.16 never runs (TL:1242).
  - INV-009: an echo allowance in 7.16 alone fails, because TL:1248, TL:1260 and the 7.24 lens (TL:1314, each breach BLOCKING) still forbid it; DESIGN:894 says "read the files only".
- MEDIUM UNADDRESSED (warnings): INV-003 (no else branch after narrowing Branch 1), INV-004 (session rollover and a self-attested quote), INV-005 (no resume clause, TL:192, TL:978), INV-010 (the TL:1260 grep runs over captured output, and no step writes the forbidden-list sentence), INV-013 (declaration pattern), INV-015 (nine scope notes in 2.8 to 2.16, and research/04:90), INV-017 (the TL:224 guard is a note).
- LOW UNADDRESSED: INV-006, INV-008, INV-011, INV-014, INV-016.
- Every HIGH and MEDIUM probe item is folded into a planned change in `refactor-plan.md` (Changes 1, 2, 3, 10 and 12).

## Scoring Matrix

Winner = Round 2 majority of the three advocate positions. Confidence: unanimous 90 to 99, majority 60 to 89, never 100.

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | V1 | 97% | V1 alone covers FR-001 to FR-026, NFR-001 to NFR-015 and the step rows (76 rows); V2 and V3 cover other row families. |
| S-002 | tie | 94% | Disjoint item lists reflect different scopes (delivery items against design-fix items); neither is wrong. |
| S-003 | V2 | 94% | V2 line ranges (for example TL:1784-1788) are the most checkable notation; the V3 `TL:` shorthand is the least portable. |
| S-004 | V3 | 96% | V3 self 0H/2M/8L to calibrated 0H/1M/9L, delta -0.02; V2 lost 4 HIGHs. |
| S-005 | V2 | 97% | Only V2 has `recommended_action` and `not_checked`. |
| S-006 | V3 | 97% | V3 CAL: 40 citations checked, 0 failed; V1 had 4 failed, V2 had 1. |
| S-007 | V2 | 96% | V2 files no confirmation as a finding; V1 R1-G5, V3 R3-G9 and R3-G10 do. |
| S-008 | tie | 98% | All three omit the Aligned/Refinement/Drift/Regression category; only V1's calibrator penalised it, so the scores are not comparable. |
| S-009 | V2 | 93% | V2 engages T1 F1, F2, F3 and F7, including the only Tier-2 confirmation of F3. |
| C-001 | V2 | 97% | R2-G3 holds (CAL HIGH): TL:1258 step (6) runs `echo` and `ls -la`; TL:1260 accepts only the eight templates or a file read. |
| C-002 | V2 | 98% | R2-G7 holds (CAL HIGH): TL:989 Branch 1 fires on PENDING, so Branch 2 never sets RESOLVED; R2-G2 holds (CAL MEDIUM). |
| C-003 | V3 | 94% | R3-G1 partly (CAL LOW): edit 4 drops the single-row clause (research/04:90); the R3-B2 closing clause at research/04:148 covers one row. |
| C-004 | V1 | 65% | 2 of 3 (V2 and V3 for V1; V1 called a tie). R1-G2 (ID labels on delivery items) and R2-G9 (B2 matrix row) do not overlap; V1's point is the more general traceability gap. |
| C-005 | V2 | 97% | R2-G1 (CAL MEDIUM, partly); DA greps for `GAPS line 138`, `113 rows` and `never edit the REPORT` return 0 hits against DESIGN:78-80. |
| C-006 | V1 | 99% | R1-G3 holds (CAL MEDIUM): TL:2509 searches only `tests/sweep/` or `tests/commands/test_sweep_command.py`; DESIGN:777-778 send FR-023 and FR-024 elsewhere. |
| C-007 | V2 | 98% | R2-G5 holds (CAL HIGH): TL:1434 "appears once (`grep -c` per name)" against TL:1431 `row: SessionRow`; wider per DESIGN:447-468. |
| C-008 | V2 | 96% | R2-G8 holds (CAL MEDIUM): 8.9 adds no negative guard test (TL:1467-1476); V3 R3-G7 is a narrower preference. |
| C-009 | V2 | 92% | R2-G10 partly (CAL MEDIUM): the DESIGN:987 rationale has no deliverable (TL:1535-1539); R1-G6 is LOW and has a false clause. |
| C-010 | V1 | 91% | R1-G4 partly (CAL LOW): only V1 asks for the 14.46 handoff line on grouping 13.1, 13.2 and 13.4. |
| C-011 | tie | 94% | V1 R1-G5 and V3 R3-G10 both confirm ordering; neither is a defect. |
| C-012 | V3 | 95% | R3-G5 holds (CAL LOW): TL:1952 lacks "at most once every 5 minutes", which TL:773 and TL:2258 carry. |
| C-013 | V3 | 96% | R3-G6 holds (CAL LOW): 13.6 adds a CHANGELOG test bullet beyond R8 (TL:2293; DESIGN:701). |
| C-014 | V3 | 96% | R3-G8 holds (CAL LOW): lint-architecture guards B5 (contracts `__init__.py:1-6`, `:302-313`). |
| C-015 | V2 | 95% | V2 turns the INF-001 false match into R2-G1; V1 re-maps; V3 records and stops (CAL criticism). |
| X-001 | V2 | 99% | TL:982 and TL:989 confirm V2 R2-G7; V3 conceded R3-G10. |
| X-002 | V3 | 94% | The calibrated reading (wording ambiguity, LOW) outranks the V3 card and the V1 `covered` verdict. |
| X-003 | V3 | 98% | TL:347: 2.16 is a SPEC-fidelity QA lens, not an edit. |
| X-004 | V1 | 95% | DESIGN:216 asserts that the NFR-004 import test enforces B2; V2 critiques the design, not TL. |
| X-005 | V1 | 73% | 2 of 3 (V2 and V3 for V1; V1 called a tie). `M2` has 0 TL hits, but DESIGN:971 is open item 3 and its behaviour-until-closed already routes to the owner. |
| X-006 | V1 | 98% | CAL correction of V1, accepted by V1: TL:2488 shows `pipx run --spec` installs runtime dependencies. |
| X-007 | V3 | 92% | V2 INF-013 `covered` against R2-G8 on the same guard; V2 conceded the row text. |
| X-008 | tie | 95% | CAL outranks V2's self severity; G1, G2, G6 and G8 drop to MEDIUM; agreed by all. |
| X-009 | V2 | 92% | V2's grade 2 tracks the calibrated HIGHs; V1 and V3 grade 4 while missing them. |
| X-010 | V2 | 95% | V2 finds real delivery for INF-005 and INF-014; V3 stops at false-match with no gap entry. |
| X-011 | V1 | 92% | Same row id, different subjects (TL:263 is a DESIGN edit); V1's `partial` judges the capture run. |
| X-012 | V3 | 96% | CAL correction of V3, accepted by V3: conftest.py:59-74 also replaces the whole `_git`; R3-G7 is a preference. |
| A-001 | V3 | 94% | QUALIFY; V3 R3-G1 is the tested case (FR-010). |
| A-002 | V2 | 94% | QUALIFY; a literal reading decides pass or fail, recovery decides severity. |
| A-007 | V3 | 91% | QUALIFY; TL:224 records the base sha only, with no HALT; V3 R3-G3 shows a stale anchor. |

Winner totals: V1 8, V2 15, V3 12, tie 4.

## Taxonomy Coverage

| Level | Points | Count | Covered |
|---|---|---|---|
| L1 (surface) | S-003, S-005, S-006, C-013 | 4 | yes |
| L2 (structural) | S-001, S-002, S-004, S-007, S-008, S-009, C-004, C-010, C-011, C-012, C-014, C-015, X-003, X-006, X-007, X-008, X-009, X-010, X-011, X-012, A-001, A-007 | 22 | yes |
| L3 (state mechanics) | C-001, C-002, C-003, C-005, C-006, C-007, C-008, C-009, X-001, X-002, X-004, X-005, A-002 | 13 | yes |

Taxonomy gate: passed (all three levels above 0).

## Convergence Assessment

- Points resolved: 39 of 39 (37 unanimous, 2 by a 2 of 3 majority: C-004 and X-005). Of the 37 unanimous points, 4 are unanimous ties (S-002, S-008, C-011, X-008).
- Alignment: 100% (89.7% on the strict reading that excludes ties). Both are at or above the 80% threshold.
- Threshold: 80%
- Invariant gate: 3 HIGH UNADDRESSED items (INV-001, INV-002, INV-009) block convergence. MEDIUM warnings: INV-003, INV-004, INV-005, INV-010, INV-013, INV-015, INV-017.
- Status: BLOCKED_BY_INVARIANTS
- Unresolved points: none at the debate level. The block is on fix sufficiency, not on any disputed point. Every blocking item is folded into a planned change in `refactor-plan.md`, so the merged verdict carries complete fixes.
