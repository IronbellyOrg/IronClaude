<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (haiku:qa) -->
<!-- Merge date: 2026-11-06T12:25:00Z -->

# Merge Execution Log

## Metadata
- Base: Variant 2 (haiku:qa), `variant-2-original.md`, combined score 0.897
- Executor: merge-executor agent
- Plan: `refactor-plan.md` (14 changes, M-01..M-14; auto-approved 2026-11-06T12:24:00Z)
- Output: `merged-verdict.yaml`
- Changes applied: 14 of 14 planned
- Status: success
- Timestamp: 2026-11-06T12:25:00Z

## Changes Applied

Each change became one finding in `merged-verdict.yaml`. "Before" is the base card (Variant 2); "After" is the merged finding. Every `exact_change` is copied verbatim from the plan (checked line by line against `refactor-plan.md`).

### Change 1: M-01 (P2) whole-text acceptance checks for Tasks 1, 2, 3 and 6
- **Status**: Applied
- **Source**: Variant 3 R3-2 (mechanism, corrected in Round 2), Variant 1 R1-F1, Variant 2 R2-01; orchestrator INV-001, INV-002, INV-003, INV-014
- **Target**: Base R2-01 (`variant-2-original.md:6-30`)
- **Before**: R2-01 asked for exact-equality ACs with no runnable mechanism and an [INFERRED] verifier
- **After**: four exact AC texts plus the Task 6 body sentence, one path base, non-empty and plan self-checks, `.grep` regex; evidence re-run by the executor (lengths 412, 261, 361, 450, 1210; plan `-cxF` = 1 each; targets 0)
- **Provenance tag**: `<!-- Source: Base (original, modified) + Variant 3 R3-2 + Variant 1 R1-F1 + orchestrator INV-001/002/003/014 — merged per Change #1 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 2: M-02 (P3) copy residual risks 1, 2 and 4 verbatim
- **Status**: Applied
- **Source**: Variant 2 R2-05
- **Target**: Base R2-05 (`variant-2-original.md:92-110`)
- **Before**: "copy the five texts verbatim" without exact text
- **After**: plan's exact replacement for plan:134, :135, :137 and its verifier (lines 240, 241, 243)
- **Provenance tag**: `<!-- Source: Base (original, modified) — narrowed per Change #2 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 3: M-03 (P3) record the extra negative pin as a deviation, keep it
- **Status**: Applied
- **Source**: Variant 2 R2-02 (detection); Variant 1 and Variant 3 (keep it)
- **Target**: Base R2-02 (`variant-2-original.md:32-48`)
- **Before**: move the negative pin to a note or get authorization
- **After**: keep plan:144 unchanged and append the deviation sentence to plan:131
- **Provenance tag**: `<!-- Source: Base (original, modified) — action from Variants 1 and 3 per Change #3 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 4: M-04 (P3) F-14 absence check without the literal
- **Status**: Applied
- **Source**: Variant 2 R2-04 (detection); Variant 1 Round 2 fix
- **Target**: Base R2-04 (`variant-2-original.md:72-90`)
- **Before**: rephrase the negative AC without the literal (no exact text)
- **After**: regex class `r[a]n` replacement at plan:45; executor confirmed plan still holds the literal once today (the change is needed)
- **Provenance tag**: `<!-- Source: Base (original, modified) — fix from Variant 1 Round 2 per Change #4 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 5: M-05 (P3) Task 3 diff-shape AC
- **Status**: Applied
- **Source**: Variant 3 R3-3
- **Target**: Base, new finding
- **Before**: [Finding did not exist in the base]
- **After**: `git diff --stat` AC for Task 3
- **Provenance tag**: `<!-- Source: Variant 3 R3-3 — merged per Change #5 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 6: M-06 (P3) Task 5 HEAD guard and Task 4 claim
- **Status**: Applied
- **Source**: Variant 3 R3-4
- **Target**: Base, new finding
- **Before**: [Finding did not exist in the base]
- **After**: `git cat-file -e` guard at plan:111; narrowed wording at plan:95
- **Provenance tag**: `<!-- Source: Variant 3 R3-4 — merged per Change #6 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 7: M-07 (P3) exit status in the Task 7 logs
- **Status**: Applied
- **Source**: Variant 3 R3-5, narrowed
- **Target**: Base, new finding
- **Before**: [Finding did not exist in the base]
- **After**: `exit=<status>` line at plan:153; lint-baseline half dropped (E-2)
- **Provenance tag**: `<!-- Source: Variant 3 R3-5 (narrowed) — merged per Change #7 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 8: M-08 (P3, review artifact) verifier rows in the coverage matrix
- **Status**: Applied
- **Source**: Variant 2 R2-06 and its per_correction table
- **Target**: Base R2-06 (`variant-2-original.md:112-140`), priority P2 to P3 per the plan
- **Before**: P2 finding listing 17 verifier spans to add as rows
- **After**: P3 review-artifact record: the report carries the F-1..F-17 table (14 pass, 3 fail explained by M-03, M-04, M-12)
- **Provenance tag**: `<!-- Source: Base (original, modified) — re-scoped per Change #8 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9: M-09 (P3, owner item) step 5 condition 2 scope
- **Status**: Applied
- **Source**: Variant 1 R1-F6 (citations re-mapped: spec:296, lc10-result.md:13)
- **Target**: Base, new finding (top of the owner list)
- **Before**: [Finding did not exist in the base]
- **After**: owner note, tag INFERRED (conditional path, debate X-003)
- **Provenance tag**: `<!-- Source: Variant 1 R1-F6 — merged per Change #9 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 10: M-10 (P3, owner item) refusal has no recorded marker
- **Status**: Applied
- **Source**: Variant 1 R1-F3
- **Target**: Base, new finding
- **Before**: [Finding did not exist in the base]
- **After**: owner note on residual risks 6 and 7, tag INFERRED (debate C-008)
- **Provenance tag**: `<!-- Source: Variant 1 R1-F3 — merged per Change #10 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 11: M-11 (P3, owner item) "only when" reads as a necessary condition
- **Status**: Applied
- **Source**: Variant 1 R1-F2
- **Target**: Base, new finding
- **Before**: [Finding did not exist in the base]
- **After**: optional owner wording change ("exactly when")
- **Provenance tag**: `<!-- Source: Variant 1 R1-F2 — merged per Change #11 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 12: M-12 (P3, owner item) F-12 verifier contradicts F-3
- **Status**: Applied
- **Source**: Variant 2 R2-03
- **Target**: Base R2-03 (`variant-2-original.md:50-70`), priority P2 to P3 per the plan
- **Before**: P2, record the contradiction in the plan and request clarification
- **After**: P3 owner note, no plan change
- **Provenance tag**: `<!-- Source: Base (original, modified) — re-prioritized per Change #12 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 13: M-13 (P3) hardening notes on M-01
- **Status**: Applied
- **Source**: orchestrator invariant probe INV-006, INV-014
- **Target**: Base, new finding
- **Before**: [Finding did not exist in the base]
- **After**: line-count limit and no hard-coded `to-do/` path, recorded as notes
- **Provenance tag**: `<!-- Source: orchestrator INV-006, INV-014 — merged per Change #13 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 14: M-14 (P3) carried owner items from the previous review
- **Status**: Applied
- **Source**: previous review (Tier 1 card F-4; previous report M-12, M-13, M-14, INV-020, INV-021)
- **Target**: Base, new finding
- **Before**: [Finding did not exist in the base]
- **After**: four carried owner items, copied verbatim; marked "not re-verified in this merge"
- **Provenance tag**: `<!-- Source: previous review — carried per Change #14 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Changes NOT Being Made
Copied from the plan into `changes_not_made` (6 rows: C-009, C-010 half, C-012, C-013, C-016, A-001). Base findings not carried as findings: none dropped; R2-01..R2-06 all map to M-01, M-02, M-03, M-04, M-08, M-12.

## Post-Merge Validation

### Structural Integrity
- Status: PASS
- `merged-verdict.yaml` parsed on read-back (`yaml.safe_load`, 2026-11-06T12:29Z): 22 top-level keys, status `success`, 14 findings (P1 0, P2 1, P3 13), 6 confirmations, 15 `invariant_disposition` rows (INV-001..INV-015), 6 `changes_not_made` rows, `unresolved_conflicts: []`.
- Every finding has non-empty `evidence` and `verifier` (programmatic check: 0 missing).
- Every `exact_change` matches the plan verbatim; one mismatch (missing bold on M-01's header line) was found and fixed before this check.
- Issues found: none open.

### Internal References
- Total references: findings M-01..M-14, confirmations OK-1..OK-6, INV-001..INV-015, debate points C-/X-/A-/S-
- Resolved: all; each `provenance` entry names a "Change #N" in `refactor-plan.md` or an orchestrator item (E-1..E-4, INV-*)
- Broken: none
- M-01 evidence re-run read-only at 2026-11-06T12:24:50Z: extraction lengths 412, 261, 361, 450, 1210; plan `grep -cxF` = 1 each; target counts 0

### Contradiction Re-scan
- New contradictions introduced: 0
- Every finding position matches the debate scoring matrix winner and the plan; dropped points (C-009, C-013, C-016, A-001 premise) stay dropped; MEDIUM invariants INV-001, INV-002, INV-015 are addressed by M-01's AC text; INV-006 is recorded in M-13
- Unresolved conflicts: 0

## Summary
- Planned: 14
- Applied: 14
- Failed: 0
- Skipped: 0
- Validation: PASS
- Final status: success
