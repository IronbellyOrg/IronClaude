# Merge Execution Log

## Metadata

- Base: variant-2 (qa, claude-gw-tier2)
- Executor: merge-executor (sc:adversarial Step 5, Mode A)
- Plan: refactor-plan.md (revised), PASS in refactor-plan-review-2.md
- Output: merged-verdict.yaml (same folder)
- Changes applied: 25 of 25
- Status: COMPLETE
- Timestamp: 2026-11-08

Abbreviations: TL is the tasklist `TASK-RF-sweep-phase1-20261108-072653.md`; DESIGN is `docs/designs/orchestrator-mode.md`. The YAML holds the full alias map under `path_aliases`.

Minor review notes applied because they cost nothing: M-1 (F-21 notes TL:2677 is a 14.x QA item), M-2 (F-21 id mapping), M-3 (F-12 stays LOW, scope grew), M-4 (F-09 "QA edge-case lens", F-23 full matrix path), M-6 (F-01 line-count wording), M-7 (R3-G9 evidence in not_carried), m-1 (F-03 single option), m-2 (F-03 anchored grep), m-3 (F-03 `$ ` format on TL:1258 and the 7.24 lens note). M-5 is recorded in not_carried (S-008).

## Changes

Each change below targets the merged verdict, not the tasklist. "Before" is the base (variant-2) state; "After" is the merged entry.

### Change 1: F-01 owner-gate deadlock (HIGH)

- Status: Applied
- Source: R2-G7 (base), R2-G2 merged in, V1 R2 New Evidence 2, V3 R2 New Evidence 1 and 3, C-002, X-001
- Target: findings F-01
- Before: base R2-G7 named fewer sites and R2-G2 was a separate gate-bypass HIGH.
- After: one HIGH finding over 6.2, TL:1140, the six inline items, 7.15, 7.16 and 14.7, with the seven-part fix and the "PENDING or" check.
- Provenance tag: `# Source: Change 1`; provenance.invariants INV-001 to INV-008
- Validation: TL:989, TL:1140, TL:1151, TL:1165, TL:1242, TL:2481, TL:192 read; all match.

### Change 2: F-02 8.3 grep -c (HIGH)

- Status: Applied
- Source: R2-G5 (base), V1 R2 NE1, V2 R2 NE1, C-007
- Target: findings F-02
- Before: base gave an either-or pattern fix.
- After: single anchored pattern, exactly 1 per name, name set includes the four DESIGN 7.2 constants plus ClassifiedRow.
- Provenance tag: `# Source: Change 2`; INV-012 to INV-014
- Validation: TL:1434 and DESIGN:447, DESIGN:466 read; match.

### Change 3: F-03 7.16 command allowance (HIGH)

- Status: Applied (with m-1, m-2, m-3)
- Source: R2-G3 (base), T1 F3, V2 R2 NE3, C-001
- Target: findings F-03
- Before: base offered an either-or and named fewer texts.
- After: two allowed step (6) commands, four texts edited together (TL:1248, TL:1257-1258, TL:1260, TL:1314), `check` added to the grep, anchored check `^\$ (ls|echo)\b`.
- Provenance tag: `# Source: Change 3`; INV-009 to INV-011
- Validation: TL:1248, TL:1257, TL:1258, TL:1260, TL:1314, DESIGN:894 read; match.

### Change 4: F-04 14.11 lens folders (MEDIUM)

- Status: Applied
- Source: V1 R1-G3, V1 R2 NE4, C-006
- Target: findings F-04 (new; missing from base)
- Before: absent.
- After: MEDIUM finding naming the test folders; NFR-012 has no test by design.
- Provenance tag: `# Source: Change 4`
- Validation: TL:2509, DESIGN:777, DESIGN:778 read; match.

### Change 5: F-05 GAPS line 138 rule (MEDIUM)

- Status: Applied
- Source: R2-G1 (base, self HIGH), C-005, C-015, X-008
- Target: findings F-05; row_coverage missing and false_match lists
- Before: HIGH.
- After: MEDIUM; INF-001 marked false match; GQ-111, GQ-112 missing; GQ-113 partial.
- Provenance tag: `# Source: Change 5`
- Validation: DESIGN:78 and DESIGN:80 read; match.

### Change 6: F-06 WC-16 text approval (MEDIUM)

- Status: Applied
- Source: V3 R3-G4, INV-021
- Target: findings F-06 (new); row_coverage D6 to partial
- Before: absent; D6 covered.
- After: separate MEDIUM finding paired with the F-01 edit at 7.4.
- Provenance tag: `# Source: Change 6`
- Validation: WORKER-CONTRACT.md:110 read; match.

### Change 7: F-07 8.1 per-file PASS (MEDIUM)

- Status: Applied
- Source: R2-G6 (base, self HIGH), X-008
- Target: findings F-07
- Before: HIGH.
- After: MEDIUM, per-file PASS.
- Provenance tag: `# Source: Change 7`
- Validation: TL:1417 read; lists the six gate files.

### Change 8: F-08 8.9 negative guard test (MEDIUM)

- Status: Applied
- Source: R2-G8 (base, self HIGH), X-007, X-008
- Target: findings F-08; row_coverage INF-013 to partial
- Before: HIGH; INF-013 covered.
- After: MEDIUM; INF-013 relabelled "construction assigned; verification partial, see F-08".
- Provenance tag: `# Source: Change 8`
- Validation: TL:1467 read; match.

### Change 9: F-09 SP-28 rationale (MEDIUM)

- Status: Applied (with M-4)
- Source: R2-G10 (base), C-009
- Target: findings F-09; row_coverage SP-28 partial
- After: rationale deliverable in 14.9; 8.18 called a "QA edge-case lens".
- Provenance tag: `# Source: Change 9`
- Validation: DESIGN:987 read; item 19 is SP-28.

### Change 10: F-10 HALT on a CHANGED anchor (LOW)

- Status: Applied
- Source: invariant probe INV-017, debate A-007, V1 R2 NE3; no card holds it
- Target: findings F-10 (new)
- After: LOW, tagged [INFERRED], one HALT sentence at TL:233. Not INV-017's MEDIUM, per the plan.
- Provenance tag: `# Source: Change 10`
- Validation: TL:224 and TL:233 read; TL:224 is a note, TL:233 handles only MOVED and a missing file.

### Changes 11 to 23: LOW findings F-11 to F-23

All Applied. Each adds or edits one LOW finding exactly as the register row states.

| Change | Finding | Source | Note | Validation |
|---|---|---|---|---|
| 11 | F-11 5.5 pin greps | R3-G3 | Card TL:792 corrected to TL:796 | TL:796 read, holds the :545 greps |
| 12 | F-12 FR-010 wording | R3-G1, V3 R2 NE2, C-003, X-002, A-001, INV-015, INV-016 | Stays LOW, scope grew (M-3) | research/04:90 read, edit 4 |
| 13 | F-13 3.1 fallback pointer | R3-G2 | Card TL:423 corrected to TL:425 | TL:425 read |
| 14 | F-14 11.1 cadence | R3-G5, C-012 | | TL:1952 read |
| 15 | F-15 13.6 CHANGELOG bullet | R3-G6, C-013 | | TL:2293, DESIGN:701 read |
| 16 | F-16 lint-architecture | R3-G8, C-014 | Paired with F-02 on 8.3 | contracts/__init__.py:35 read |
| 17 | F-17 8.8 fake seam | R3-G7, X-012 | Class is test-design preference | conftest.py:59 read |
| 18 | F-18 14.5 count | R1-G6 count part | pipx clause not carried | TL:2470, DESIGN:939 read |
| 19 | F-19 M2 route | R1-G1 naming part, X-005, INV-020 | Target is open item 3 | DESIGN:971, TL:1265 read |
| 20 | F-20 8.6 and 9.2 counts | R2-G4 part | Card TL:1635-1636 corrected to TL:1634 | TL:1634 read |
| 21 | F-21 FR/NFR ids | R1-G2 part, C-004 | M-1 and M-2 applied | DESIGN:777 read |
| 22 | F-22 commit grouping | R1-G4 part, C-010 | | TL:2754 read |
| 23 | F-23 B2 matrix row | R2-G9 matrix part, X-004 | Full matrix path (M-4) | DESIGN:216, coverage-matrix:232 read |

Provenance tag for each: `# Source: Change N` comment above the finding plus `provenance.change: N`.

### Change 24: V1 ledger corrections

- Status: Applied
- Source: X-003, X-006, X-011
- Target: row_coverage (comment block and counts)
- After: 2.16 is a QA lens (TL:347), fixing V1's NFR-003 note; no "pipx run installs nothing" (TL:2488), fixing V1's step-1.29 note; V1 partial on step-1.0a kept.
- Validation: TL:2488 read; pipx run --spec installs dependencies.

### Change 25: V3 row corrections

- Status: Applied
- Source: X-010, A-001, F-06, F-12
- Target: row_coverage
- After: V2's INF-005 and INF-014 verdicts kept over V3's false-match; FR-010 to covered-in-substance with "ambiguous after edit 4, see F-12"; D6 to partial; delegated rows carry the A-001 caveat.
- Validation: union count 76 + 51 + 24 minus 9 (V1 and V3) minus 7 (V2 and V3) = 135; merged counts 62 + 65 + 5 + 2 + 1 = 135.

## Interpretations (not deviations)

- `path_aliases` was added as a top-level field so the short file:line citations (TL, DESIGN, research/04, coverage-matrix and others) resolve. The plan uses these aliases; the field adds no finding content.
- `severity_counts` was added as a convenience total; it repeats the register counts.
- Overlap rule for row_coverage: where V1 and V3 share a row, the V1 verdict is kept except FR-010 (Change 25); where V2 and V3 share a row, the V2 verdict is kept (X-010). The plan implies this rule but does not state it as one sentence.
- F-10 is tagged [INFERRED] because no card holds it; all other findings are Grounded.

## Post-Merge Validation

### Structural Integrity

PASS. `merged-verdict.yaml` parsed with yaml.safe_load: 23 findings, ids F-01 to F-23 in order, severities HIGH 3, MEDIUM 6, LOW 14; row_coverage merged counts sum to 135, equal to unique_rows; all required top-level fields present (schema, merge_method, base_variant, sources, convergence_score, convergence_status, unaddressed_invariants_high, findings, row_coverage, not_carried, best_practice_grade, calibrated_confidence). No em dash characters (grep count 0).

### Internal References

- Total spot-checked: 43 file:line citations, read directly (TL:192, 224, 233, 425, 796, 989, 1140, 1151, 1165, 1242, 1248, 1257, 1258, 1260, 1265, 1314, 1417, 1434, 1467, 1634, 1952, 2293, 2470, 2481, 2488, 2509, 2754; DESIGN:78, 216, 447, 466, 701, 777, 894, 939, 971, 987; research/04:90; coverage-matrix:232; WORKER-CONTRACT.md:110; conftest.py:59; contracts/__init__.py:35; test_worker_contract.py:25)
- Resolved: 43
- Broken: 0
- Three card citations were corrected per the plan before inclusion (F-11, F-13, F-20).

### Contradiction Re-Scan

PASS. 0 contradictions.

- F-10 is LOW while INV-017 is MEDIUM; the plan sets LOW and the finding says it is not calibrated. Not a contradiction.
- F-19 carries only the naming of open item 3; not_carried drops the "open item 2" target and "no owner step" claim. Consistent.
- F-23 carries only the matrix row; not_carried drops the import-check part. Consistent.
- F-18 carries only the count part; not_carried drops the pipx clause. Consistent.
- F-01 absorbs R2-G2; not_carried drops only its label and HIGH severity. No duplicate finding.
- F-06 stays separate from F-01 (INV-021); they edit 7.4 together but claim different gaps.
- F-02 and F-16 both touch 8.3 with different fixes (pattern versus lint); they do not conflict.
- F-12 is LOW and not_carried drops the MEDIUM "rule lost" claim. Consistent.
- row_coverage keeps V2's INF-005 and INF-014 verdicts, matching not_carried.

## Summary

- Planned: 25
- Applied: 25
- Failed: 0
- Skipped: 0
- Deviated: 0 (four interpretations recorded above)
- Post-merge validation: PASS
