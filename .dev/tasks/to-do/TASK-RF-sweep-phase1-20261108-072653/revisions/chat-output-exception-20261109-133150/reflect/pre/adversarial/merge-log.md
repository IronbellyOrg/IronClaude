# Merge log: merged reviewer verdict (sc:adversarial step 5, Mode A, depth standard)

## Metadata

- Base variant: variant-2 (reviewer 2, qa, haiku slot, calibrated C 0.86), `variant-2-original.md`.
- Executor: merge-executor (step 5). It applied the plan and made no strategic decision.
- Plan: `refactor-plan.md` (12 changes), reviewed PASS with minor notes in `refactor-plan-review.md`. The plan text was not edited; the review corrections (a) to (f) are recorded as notes on the affected findings.
- Output: `merged-verdict.yaml` (schema `sc-reflect-merged-verdict/v1`, 547 lines).
- Changes applied: 12 of 12. Failed: 0. Skipped: 0.
- Status: complete. No file other than `merged-verdict.yaml` and this log was written.
- Timestamp date: 2026-11-10.
- All paths in this file are relative to the `reflect/pre/adversarial/` folder unless stated. TL, DESIGN, ADD, DM, BR, STYLE and coverage-matrix are the aliases defined in the `path_aliases` block of the YAML.

## Per-change log

| Change | Status | What became what | Provenance tag |
|---|---|---|---|
| 1 | applied | Finding F-01 (HIGH, unsound-check, inside the 82 bodies). Locations TL:1293, 1363, 1391 and the twelve lens lines plus TL:2572. Correction (b) applied: the lens rewording is REQUIRED; the row for an OQ-17 or OQ-18 decision cannot be added by editing 7.17 (no 7.17 row in DM), so the 7.22 and 7.25 wording must read seven plus one per resolved optional decision and the 7.30 and 7.34 fixers may correct owner-decisions.md (TL:1363, TL:1391). Correction (f) applied (DM:21-117). Review minors carried: F-R4 (at least 1, not exactly 1, for OQ-17 and OQ-18), F-R10 (apply with F-06 in one pass), F-R3 (the word optional is dropped). | R2-F1 base; R1-F3; T1 F3; M-01; INV-013, 015, 019, 020, 021 |
| 2 | applied | Finding F-02 (HIGH, unsound-check, needs new bounded authorization). INV-005 folded in and also listed under `unaddressed_invariants_high`. Corrections (c) (label pre-existing, outside the 82 revised bodies) and (d) (command-form verifier: `grep -nF` of the DESIGN:716 sentence expects line 404; a second command on TL expects only line 776) applied. Review minor F-R7 carried. | R2-F2 base; T1 F1; M-02; INV-005, 007, 022 |
| 3 | applied | Finding F-03 (MEDIUM, partial, inside the 82 bodies). Embed the missing ADD:15, 17, 19, 21 clauses on the same physical line, no whole-block copy, no new 11.4 substring assertion. INV-016 (presence pins only) and INV-023 (ADD:19 sentence 1) carried. | R3-F2; R1-F4; T1 F5; M-03; INV-014, 016, 023 |
| 4 | applied | Finding F-04 (MEDIUM, missing, inside the 82 bodies). The step-7.10 result file is the carrier and is written before the style edit (INV-001); the PRE path is as supplied with the authorization (INV-024 falsifier 2); a quote by the same executor is a record, not independent evidence (falsifier 1); 7.20 gets a command and expected value (falsifier 3). | R1-F2; T1 F4; M-04; INV-001, 018, 024 |
| 5 | applied | Finding F-05 (LOW, partial, inside the 82 bodies). Correction (e): I read TL:1295 and TL:1210 myself. The STOP-and-escalate sentence is the penultimate sentence of TL:1210 and the final sentence is "On failure log negative evidence ... remain incomplete". TL:1295 means fix the owning item and then re-run THIS (checking) item, so the plan phrase about re-running 11.1 or 11.3 in place is reworded; the style-defect route is a HALT with a named blocker. The "fresh authorization only if ..." rule is dropped. | R1-F1; T1 F2; M-05; INV-003 |
| 6 | applied with a recorded severity departure | Finding F-06 (LOW, stale-text, inside the 82 bodies). The plan said MEDIUM; correction (a) sets LOW (the debate value). Reason: TL:1307 and TL:1370 pass agents "the input list in Context" or "the inputs in Context", so the claim that the stale sentence reaches spawned agents is conditional and unverified. INV-025 is kept as a note. The in-place reword of the 58 Context lines is recommended as the cheap form. The note-only alternative (verifier 59) is dropped (review minor F-R2). | R3-F1; U-005; M-06; INV-010, 012, 025 |
| 7 | applied | Finding F-07 (LOW, authority, optional, inside the 82 bodies). Sums recorded before the spawn sentence, OQ-6 file only (INV-026). | R3-F3; M-07; INV-026 |
| 8 | applied | Finding F-08 (LOW, missing, inside the 82 bodies). Correction (d): added a command-form verifier. The expected value 6 holds only after 7.10 has run (0 before), per review minor F-R6. | U-001; M-08; INV-014, 017 |
| 9 | applied | Finding F-09 (LOW, ordering, optional, inside the 82 bodies). Correction (d): added the verifier `grep -n 'Phase 7 preamble Branches'` (prints nothing today). INV-002 recorded as a note (state during the Action is unresolved and UNVERIFIED). | R1-F5; T1 F7; M-09; INV-002 |
| 10 | applied | Finding F-10 (LOW, stale-text, optional, needs new bounded authorization). Correction (d): added a verifier that covers both TL:1551 and TL:1812. TL:1501 was checked and needs no change. | T1 F6; M-10; INV-006 |
| 11 | applied | Header fields and invariant blocks: `convergence_score` 0.947, `convergence_detail`, `convergence_status: BLOCKED_BY_INVARIANTS` (comment explains INV-005), `unaddressed_invariants_high`, `unaddressed_invariants_medium` (11 items), `unaddressed_invariants_low` (4 items; INV-023 moved here from the plan's MEDIUM grouping, review minor F-R9), `invariants_addressed` (10 items). | CONS convergence assessment; invariant-probe.md |
| 12 | applied | `consequence_note` (INV-008: re-run structural, alignment, qualitative and PRE after any edit; single physical line), `residual_notes` (INV-011, the 14.46 three-versus-four residual, needs the same new authorization as F-02), `not_carried` (all dropped candidates with reasons), `tier1_verdicts`, `departures_from_consensus`, `row_coverage`, `best_practice_grade`, `confidence_calibrated`, `verdict_recommendation`. | CONS disposition table; invariant-probe.md |

## Post-merge validation

### YAML loads

I had no interpreter available (the brief allows Read, Grep and Glob only), so I did not run a parser. I checked the structure in three ways:

1. Re-read the whole file in three Read calls (lines 1-80, 80-250, 250-547). Indentation is two spaces per level, every list item under `findings`, `evidence`, `notes` and the invariant blocks starts with `- `, and no key is repeated inside a mapping.
2. Used regex searches on the file. Every `key: '...'` line either ends with a closing single quote or is a flow mapping that ends with `}`; no tab character and no em dash or en dash exists in the file.
3. Checked the escaping by eye on every line that holds an apostrophe or a backtick pair: embedded apostrophes are doubled (`''`), and no double-quoted scalar is used.

Result: no structural defect found. This is a manual check, not a parser run, so I report it as "expected to load", not "loaded".

### Evidence references

- Refs checked: 95 (87 in the ten findings: F-01 18, F-02 10, F-03 11, F-04 7, F-05 7, F-06 6, F-07 8, F-08 10, F-09 4, F-10 6; plus 6 in `row_coverage` and 2 in `residual_notes`).
- Broken: 0.
- Method: before writing, I Read the source lines (TL 772-779, 1139-1144, 1205-1234, 1266-1297, 1305-1307, 1326-1328, 1360-1365, 1369-1370, 1382-1393, 1549-1551, 1811-1813, 1970-1983, 2046-2051, 2262-2270, 2341-2342, 2570-2572, 2612-2614, 2759-2764, 2996-2999, 3008-3021; DESIGN 714-717 and 758-761; DM 1-30, 30-59, 60-119; ADD 10-49; BR 45-60; OQ6 8-15; STYLE 58 plus a grep of lines 22-90; coverage-matrix 1-70, 256 and 279). After writing, I ran one combined Grep over TL for every quoted fragment and matched each reported hit to its cited line number. The fragments that appear in the YAML in doubled-apostrophe form match the source's single apostrophes.
- Not re-read: the YAML note for INV-021 (the 7.37 to 8.1 leg, TL:1424-1427) comes from `invariant-probe.md` and says so; I did not Read TL:1424-1427 in this pass, and no evidence entry depends on it.

### Severity counts

`severity_counts` says HIGH 2, MEDIUM 2, LOW 6, total 10. Counted from the findings: HIGH F-01, F-02; MEDIUM F-03, F-04; LOW F-05, F-06, F-07, F-08, F-09, F-10. They match. The plan's own tally would have been MEDIUM 3 and LOW 5 because it raised F-06 to MEDIUM; correction (a) removes that difference.

### Contradictions between findings

I looked for contradictions and found none:

- F-01 (part b, the twelve lens lines) and F-06 (the same lines) edit the same physical lines. They do not contradict each other. A note on each says to apply both in one pass.
- F-01 and F-08 both edit TL:1293, 1363 and 1391. The F-08 note says it is part of the same edit.
- F-04 (the 7.10 result file carries the authorization quote) and F-05 (no fresh-authorization clause) agree. F-05 states that it drops the clause because it clashes with F-04.
- F-06 and F-10 have the same consequence class and both stay LOW.
- F-02 and F-10 both need a new bounded authorization, and F-10 names F-02 as the same authorization.
- The F-02 verifier uses `grep -nF` on HOW-WE-WORK.md and a plain `grep -n` on TL. Their expected values do not overlap.

### Row coverage

I checked the numbers against the matrix summary (coverage-matrix lines 42-62): parsed 127, `matched_parsed` 127, `coverage_pct` 1.0, `coverage_pct_union` 0.985, `unmapped_count` 0, `unmapped_count_union` 3, union list `INF-017`, `INF-A06`, `INF-A29`. The YAML gives INF-A06 as carried in F-03 (the matrix marks it partial because 7.10 lacks the same-message case), and INF-017 and INF-A29 as not carried. The INF-017 reason is that the matrix calls it a wording question about whether the task executor counts as the coordinator, item 7.16 is not among the 82 revised bodies, and no card, debate row or probe item raised it. The INF-A29 reason is that the matrix marks it benign (a future-only rollback rule with no build item expected) and the debate dropped it as U-009.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 12 | 12 | 0 | 0 |

Deviations from the plan, all driven by the instructions for this step: F-06 severity LOW instead of MEDIUM (correction a); the F-01 lens rewording is required and the owner-decisions carrier is the 7.22/7.25 wording plus the 7.30/7.34 fixers (correction b); F-02 keeps the label "pre-existing (outside the 82 revised bodies)" (correction c); F-02, F-08, F-09 and F-10 carry command-form verifiers (correction d); F-05 quotes TL:1295 and TL:1210 as I read them (correction e); the manifest range is DM:21-117 (correction f). One extra alias `OQ6` was added because the F-10 evidence needs the OQ-6 record.

What I could not do: run a YAML parser (no interpreter in my tool set), and re-verify the split of the 59 label lines by phase (I recounted the total 59 only; the split 15, 14, 13, 16 for the 58 later items is cited from `refactor-plan-review.md`). No fix has been applied to any task file, design, addendum, ledger or source.
