# Merge Execution Log

## Metadata
- Base: Variant B (sonnet:qa), `variant-2-sonnet-qa.md`
- Executor: merge-executor agent
- Plan: `adversarial/refactor-plan.md` (7 planned changes, auto-approved)
- Output: `final-cut-list.md` (165 lines)
- Changes applied: 7 of 7 planned
- Status: success
- Timestamp: 2026-11-16

## Changes Applied

### Change 1: Row table with the five requested fields
- **Status**: Applied
- **Source**: refactor-plan.md "Target content" / "Final row table" (from debate-transcript.md Scoring Matrix and round1-advocate-1/2/3.md per-point matrices)
- **Target**: Base, verdict table (replaced in full)
- **Before**: Variant B table with columns ID, Verdict, Scope if narrowed, Surviving guard, Confidence %, Evidence; pre-debate verdicts of Variant B only.
- **After**: 39-row table (R1-R10, T1-T10, S1-S6, D1-D13) with columns ID, Final verdict, Exact scope if narrowed, Surviving guard, Conf %, Execution class; copied line for line from the plan. One HTML comment block listing per-row sources placed immediately after the table (no comments inside the table).
- **Provenance tag**: `<!-- Source: Base (original) table skeleton, columns replaced per Change 1; row content from debate-transcript.md Scoring Matrix and round1-advocate-1/2/3.md per-point matrices -->` plus the per-row source block
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 2: Header counts and survival rule
- **Status**: Applied
- **Source**: refactor-plan.md "Counts"; survival rule from "Decision rules applied by the orchestrator" item 3
- **Target**: top of final-cut-list.md (intro paragraph, then section "Counts")
- **Before**: Variant B header paragraph (date, branch, path abbreviations, 39-vs-36 note).
- **After**: intro with date 2026-11-16, branch 409-Phase2, worktree path, read-only quick-depth debate of 3 variants and 3 Round 1 advocates, and the survival rule; then the four Counts bullets verbatim (including the 36-vs-39 note).
- **Provenance tag**: `<!-- Source: Base (original, modified) - intro framing from Variant B header; survival rule from refactor-plan.md "Decision rules" item 3 -->` and `<!-- Source: refactor-plan.md "Counts" (Change 2); figures from debate-transcript.md Convergence Assessment -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: Ordered execution sequence for EXECUTE-NOW items
- **Status**: Applied
- **Source**: refactor-plan.md "Execution sequence (EXECUTE-NOW only)" (round1-advocate-2 Extra 7; round1-advocate-3 A-001)
- **Target**: Base, new section "Execution sequence (EXECUTE-NOW only)"
- **Before**: Section did not exist.
- **After**: gate paragraph, steps 1-5, staging note; verbatim.
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 3; round1-advocate-2 Extra 7 (cut ordering); round1-advocate-3 A-001 (pytest and ruff after each cut); Variant A and Variant C file groupings -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Owner questions
- **Status**: Applied
- **Source**: refactor-plan.md "Questions for the owner" (OWNER-NEEDED rows of all three variants)
- **Target**: Base, new section "Questions for the owner"
- **Before**: Section did not exist (owner questions were spread over Variant B rows and Extra findings).
- **After**: Q1-Q11 verbatim (Q1-Q9 map to the 9 OWNER-NEEDED rows; Q10, Q11 are the two extra questions).
- **Provenance tag**: `<!-- Source: refactor-plan.md Change 4; OWNER-NEEDED rows of Variant A, Variant B and Variant C; Q10 and Q11 are extra questions the debate found (Base (original) Extra-findings idea) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Facts found false or stale in proposed-cuts.md
- **Status**: Applied
- **Source**: refactor-plan.md "Facts found false or stale in proposed-cuts.md" (Variant C Extra 1-25, Variant A Extra, Variant B Extra 2, X-001..X-014)
- **Target**: Base "Extra findings" section, replaced by new section "Facts found false or stale in proposed-cuts.md"
- **Before**: Variant B "Extra findings" list.
- **After**: items 1-31 verbatim.
- **Provenance tag**: `<!-- Source: Variant C (opus:analyzer) false-claims list (Extra 1-25), with Variant A Extra and Variant B Extra 2; refactor-plan.md Change 5; Base (original) Extra-findings idea -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Provenance annotations
- **Status**: Applied
- **Source**: artifact-templates.md Section 6; refactor-plan.md Change 6
- **Target**: whole document
- **Before**: no provenance.
- **After**: 3-line provenance header (`Provenance`, `Base: Variant B (sonnet:qa)`, `Merge date: 2026-11-16`); a `<!-- Source: ... -->` comment before every section; per-row source block after the table (mapping V1/V2/V3 to Variant A/B/C and round1-advocate-1/2/3 per debate-transcript.md Scoring Matrix winner column); `orchestrator override` tag on the closing section. Closing section "Orchestrator overrides and dissent" added as instructed: overrides (a), (b), (c) copied verbatim from plan item 4, plus open dissents R1, T2, T4, T5.
- **Provenance tag**: `<!-- Source: orchestrator override (refactor-plan.md "Decision rules applied by the orchestrator" item 4) -->` and `<!-- Source: debate-transcript.md Scoring Matrix (C-001, C-012, C-014, C-015) and the R1, T2, T4, T5 rows above -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (after deviation 1 below)

### Change 7: Concrete anchors preserved
- **Status**: Applied
- **Source**: refactor-plan.md Change 7
- **Target**: all copied sections
- **Before**: anchors in plan Target content.
- **After**: sections copied mechanically from the plan (plan lines 88-91, 95-135, 138-144, 147-157, 160-190); the only transformation is heading level `###` to `##` so the sections sit directly under the `#` title.
- **Provenance tag**: n/a (covered by section tags)
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## Deviations and fixes
1. T5 dissent wording. The caller's brief described the T5 dissent as "V2 and V3 majority would also cut :148-171". The sources disagree: debate-transcript.md C-015 says "V1 (+V3 concession) ... V2 dissent: independent argv log"; round1-advocate-1.md and round1-advocate-3.md cut :148-171, round1-advocate-2.md keeps it; in the original variants (diff-analysis.md C-015) V1 and V2 cut it and V3 did not. The output states the dissent as "a 2 of 3 majority would also cut ... (in Round 1, advocates 1 and 3; in the original variants, V1 and V2); the round1-advocate-2 position keeps it; kept by override (a)". This matches the plan's T5 row and override (a) ("2 of 3 advocates would cut it"). No verdict, scope, confidence or execution class changed.
2. Heading levels: plan Target content uses `###`; output uses `##` under the `#` title. Text unchanged.

## Post-Merge Validation

All checks are read-only (grep, awk, sed -n over the two files, run from a private /tmp batch directory that was removed afterwards). Batch footer: `BATCH_OK failures=0`.

### (a) Row IDs
- 39 table rows; IDs in order: R1-R10, T1-T10, S1-S6, D1-D13; none missing, none extra. PASS

### (b) Counts match the table
- Final verdict counted from the table: CUT 0, CUT-SMALLER 15, DEFER-OWNER 9, KEEP 15 (matches the Counts bullet).
- Execution class counted from the table: EXECUTE-NOW 11, OWNER-NEEDED 9, NOT-NOW 19 (matches the Counts bullet). PASS

### (c) EXECUTE-NOW rows
- R1 80, R2 80, R3 75, T5 70, T7 75, T8 89, T9 70, S2 77, D1 70, D2 77, D13 70: all CUT-SMALLER, all confidence >= 70.
- None deletes or moves an untracked file (D4, D9, S3 are OWNER-NEEDED or NOT-NOW; D2 explicitly leaves the untracked handoff-mvp-brainstorm.md alone); none weakens a binding rule (sequence states the sanitizer, argv allow-list, process-group kill, terminal restore, snapshot redaction and disclosure label are untouched); none writes an owner record (D1 and D2 cite existing owner-written records; D12 stays OWNER-NEEDED). PASS

### (d) Anchors unchanged
- Verbatim line check: all 94 content lines of the plan's Target content (Counts, table, sequence, questions, facts) appear as exact whole lines in the output; missing 0.
- Spot-check by grep (21 anchors, each present in output): terminal.py:41-53, adapter.py:65-82, parse.py:723-733, view.py:209, test_render.py:182-190, test_question_quiet_scope.py:192-203, test_golden_contract.py:333-365, export.py:165-168, commands.py:177-178, test_view.py:864-869, "5,069 vs 8,271 bytes", "54,129 bytes", "78,427 bytes", 14,438,526, 14,435,766, "660 KB", test_commands.py:743-745, snapshot.schema.json:4, commands.py:369, acceptance-tests.md, "694 passed". PASS

### (e) Contradiction re-scan
- New contradictions introduced: 0. The closing section agrees with the T2, T4, T5, T6, D1 and R1 rows; intro survival rule agrees with decision rule 3 and the Counts. The one brief-vs-source inconsistency (T5 dissent attribution) was resolved toward the sources (deviation 1). PASS

### (f) Dropped-anchor audit
- 106 distinct anchors extracted from the plan's Target content (file:line forms, comma-grouped numbers, "N KB/bytes/files"); dropped from output: none. PASS

### Structural Integrity
- Heading hierarchy: PASS (one `#` title; `##` sections Counts, Final row table, Execution sequence, Questions for the owner, Facts found false or stale, Orchestrator overrides and dissent)
- Section ordering: PASS (as specified by the caller)
- Document flow: PASS; no emojis (grep for emoji ranges: none)

### Internal References
- Total references checked: 106 plan anchors plus Q1-Q9 to OWNER-NEEDED rows plus overrides (a)-(c) referenced from T5, T6, D1
- Resolved: all
- Broken: 0

### Contradiction Re-Scan
- New contradictions introduced: 0
- Details: none

## Summary
- Total changes planned: 7
- Successfully applied: 7
- Failed: 0
- Skipped: 0
- Deviations recorded: 2 (T5 dissent attribution corrected to the sources; heading level `###` to `##`)
- Post-merge validation: PASS (0 failed checks)
