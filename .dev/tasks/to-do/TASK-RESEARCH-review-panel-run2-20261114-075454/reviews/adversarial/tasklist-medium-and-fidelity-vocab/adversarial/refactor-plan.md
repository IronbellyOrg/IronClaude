# Refactoring Plan: slot X-15 (tasklist-medium-and-fidelity-vocab)

## Overview

- Base variant: Variant B (Proposal B, `variant-2-original.md`), selected by the debate's own base selection: "Selected Base: Variant B (Proposal B; default model, default persona)". Combined scores A 0.9138, B 0.8664, margin 4.74% (below 5%), tiebreaker level 1 (debate performance): B won 12 points against 4 for A (`base-selection.md`).
- Non-base variant: Variant A (Proposal A, `variant-1-original.md`).
- Total planned changes: 10 (additions and one restructure). Changes not being made: 12 (below).
- Overall risk: Medium. The merge restructures B's section order (Change 1) and adds text; it changes no code and no pinned sentence. Where the debate left a point unresolved (C-001, C-007, C-012, C-013, C-014) the merged text states both advocates' final terms side by side and does not choose.
- Rule for this plan: it adds nothing the debate did not conclude. Every change cites the diff point, the round and the advocate position it comes from. Debate confidence values are in `debate-transcript.md`, Scoring Matrix.
- Output of Step 5: `merged-output.md` in the folder above this one (`../merged-output.md`).

## Planned Changes

### Change 1: Inputs-first dependency table and reordered prerequisites (from Variant A, section 0)

- Source: Variant A section 0 "Inputs and dependencies" (the C-01, C-02, C-03 table); Variant B section 7 "Consistency with the adjudicated slots".
- Target: a new section 0 at the top of the base, before B's section 1; B's section 7 content moves into it and the old section 7 becomes a pointer.
- Approach: restructure (move) plus insert.
- Rationale: S-001 won by A, 85% (both advocates); the re-evaluator marked B's ST1 NOT MET because the adjudicated outcomes B relies on appear only in section 7, after design and evidence (`score-reeval.md`).
- Risk: Medium (restructures). Keep B's three dependency statements (C-01 "if reopened, B is reopened with it"; C-02 typed `blocking` as the authority; C-03 per-profile policy) and add A's "Outcome I rely on" column. A states no reopening condition; B does, so B's wording is kept.

### Change 2: Replace B's S4 premise with the consequence test (from Variant A section 7 and Round 2 of both advocates)

- Source: Diff points C-002 (Hybrid, 85%), X-001 (Neither, 85%), X-002 (A, 95%: B conceded the skill states no model before B's own edit), X-006 (B, 90%: `pragmatic.md:229` and `:231` name no High/Medium/Low scale).
- Target: B section 1 (the position) and section 3 evidence E4.
- Approach: replace the sentence "the tasklist skill's own model, which pragmatic.md S4 permits" with the basis both advocates ended on: the consequence test of `pragmatic.md:225` and `:231` applied by analogy; S4 applies only after the skill states a model; S5 is not read as covering High/Medium/Low.
- Risk: Low.

### Change 3: Stage 7 grading block (from Variant A section 2.2, as adopted by both advocates in Round 2)

- Source: Variant A section 2.2 (grading block), Round 2 A+ block and Round 2 B H+ block; diff points U-001, U-002, C-004, C-013.
- Target: new subsection "Stage 7 grading block" in the design section of the base.
- Approach: insert. Carry the elements both advocates adopted: grade by consequence (PM:225/PM:231); omission of a roadmap item, deliverable, ID, dependency, exit criterion or validation step is High; "when torn between two grades, grade higher"; same-task duplicates at the dedup step (SK:1410) keep the highest severity. Carry the two final blocks verbatim as the two end states (A+ and H+) and mark the Medium definition, the place of "insufficient detail / ambiguity" and the label of SK:1421-1422 as unresolved (C-004 label, C-013).
- Rationale: C-004 Hybrid 80%; C-013 unresolved 55%.
- Risk: Medium (the block lands as new skill text; INV-017 applies to H+).

### Change 4: Measurements F1, F2, F3 with the decision rules of both advocates (from Variant A section 5 and Round 2)

- Source: Variant A M1, M2 and M-X15-5 (Round 2); Variant B M-X15-1..4 and its Round 2 F1, F2, F3; diff points C-011 (Hybrid, 85%), S-005 (Hybrid, 85%), X-004 (Hybrid, 82%).
- Target: B section 5.
- Approach: replace B's list with the merged list: F1 (blind grade of the six archived Medium findings), F2 (seeded defects under both blocks, FC and FB), F3 (flip rate at both boundaries), M-X15-4 (no `Medium` token in core files), plus A's static tests T1, T2, T3 (T4 is dropped with Form 2). Keep B's registered thresholds and default rule; record A's differing rule (adopt A+ if all three measurements pass; fall back to H if any fails) beside it; mark thresholds as design choices, not evidence.
- Risk: Low.

### Change 5: Pin inventory correction (from Variant A Round 2 W4, new evidence 1)

- Source: Diff points C-005, C-006; Round 2 A and B both [READ] `src/superclaude/commands/tasklist.md:113` and `tests/skills/test_worker_contract.py:777`, `:1861` via `_unattended_section` (`:893-906`).
- Target: B section 3 E3 and section 4.
- Approach: add the missing pin sites: the phrase "the unresolved High or Medium HALT resolves as blocked" lives in the command file, not in the skill (the skill says "this HALT resolves as blocked", SK:1615); the byte-equal plan copy `.dev/review-severity-rule/sweep-edits.yaml`. State the cost under each end state: nothing changes under H+; A+ rewrites SK sites, `commands/tasklist.md:113`, two pins, 12 fixture rows and the plan copy.
- Risk: Low.

### Change 6: Corrected line ranges and counts (from Variant A, X-010)

- Source: X-010 (A, 95%: B conceded). Correct ranges: `prompts.py:49-69` (MEDIUM `:58-64`), `roadmap/gates.py:195-240`, test `tests/tasklist/test_tasklist_fidelity.py:208-225`.
- Target: B sections 2, 3 (E5, E6, E9).
- Approach: replace the three ranges. Keep the "76 lines in 10 files" against "88 lines in 14 files" count as unresolved (invariant INV-009, LOW); do not state either number as settled.
- Risk: Low.

### Change 7: Corrected reading of the archived reports (from Variant A Round 1 Strengths 4, confirmed by B Round 2 W4)

- Source: C-010 (B with A's correction, 82%), X-004 (Hybrid, 82%).
- Target: B section 3 E6 and E7.
- Approach: replace "mostly an omitted or unmatched roadmap requirement" with the reading both advocates ended on (two omissions: v3.66 M2, test1 M1; two dropped acceptance criteria with Steps/Deliverables still present: v3.66 M3, M4; one step contradicting a roadmap target: test1 M2; one expected value asserted as fact: v3.66 M1; one reader, six items, [UNVERIFIED] as a measurement). Replace E7's label-preserving replay with the statement that it ignores a grading block that moves omissions to High, so what remains at stake is four of six findings under A+ (or whatever the blocks classify).
- Risk: Low.

### Change 8: Hazard notes for later engine hosting (from Variant A section 2.1 and Variant B section 2)

- Source: U-004 (a v2 tasklist lens must not set `reflect_category`), U-012 (`card_convert.py` maps `medium` to MINOR and `high` to MAJOR), invariant INV-016 (ADDRESSED, LOW).
- Target: B section 2, tasklist module bullets.
- Approach: insert both notes; state that Form 2 (a parse-edge severity-to-blocking table) is withdrawn.
- Risk: Low.

### Change 9: Table of the five unresolved points with both advocates' final terms

- Source: Scoring Matrix rows C-001, C-007, C-012, C-013, C-014 (Unresolved) and the "Remaining disagreements" sections of both Round 2 files.
- Target: new section "Points the debate did not resolve".
- Approach: insert. One row per point: A's final term, B's final term, what would decide it (F1, F2, F3, the PR:62 owner decision). No winner is declared for these five.
- Risk: Low.

### Change 10: Open invariants and conditions from Round 2.5

- Source: `invariant-probe.md`: 20 findings, 17 UNADDRESSED; HIGH: INV-017, INV-018.
- Target: B section 4 (invariants).
- Approach: append a subsection "Invariants the debate left unaddressed" listing INV-017 and INV-018 (HIGH) with their falsifying conditions, and the MEDIUM and LOW items by ID and one line. State that none was resolved because standard depth has no Round 3. Do not add a resolution the debate did not reach.
- Risk: Low (record only).

## Changes NOT Being Made (with rationale)

| Diff point | Non-base approach (Variant A) | Why the base approach stands |
|------------|-------------------------------|------------------------------|
| C-003 | Form 2: a module-declared severity-to-blocking table enforced at the parse edge | A withdrew it in Round 2 (W5): `findings_v2.py:155-162` forces `category` into a closed set and ties blocking to `severity != MINOR`; C-02 ruled out a core predicate. B 95%. |
| S-004, C-008 | The fidelity prompt becomes a tasklist-module vocabulary under the core | A moved to B's placement in Round 2: no core code consumes the vocabulary, and moving it would touch the six-field frontmatter shared with `SPEC_FIDELITY_GATE`. B 88% / Hybrid 85% (B's placement, A's parity test). |
| X-005 | A role table (roadmap as `source`, tasklist directory as `plan`, no `spec` role) | No module-declared role or pair table exists; `ROLES` is a closed set (`findings_v2.py:35`). B 90%. |
| X-009 | The any-reviewer union of C-03 as the mitigation for High/Medium misgrades | Each task slice has one grader (SK:1351-1368); A conceded fully. B 95%. |
| X-006 | "On a three-label scale grade by the definition" (S5 read as covering High/Medium/Low) | `pragmatic.md:229` and `:231` name no High/Medium/Low scale; A conceded. B 90%. |
| X-008 | "One product should not have a gate that passes a report and a skill that halts on the same row" | A conceded: one product family and one readiness question, not one code path. B 90%. |
| C-005, C-006 | Rewrite of about ten skill sites, `commands/tasklist.md:113`, two pins, 12 sweep rows and the plan copy now | A+ pays this only after F2 and F3 pass; the base keeps zero churn by default. B 90% each. A states it as a cost. |
| C-001 (default) | A+ as the end state now (Medium non-blocking) | Unresolved. The base keeps H+ as default per B's final position; A's own position is "adoption gated on measurement, fallback to H". Recorded in Change 9, not decided. |
| C-013 (CLI side) | Split of `prompts.py:62` so the CLI and the skill agree | Unresolved; B: the prompt has one caller (`executor.py:173`) and the edit changes the exit-1 rate of `tasklist validate`, an owner decision. A accepts it only with a measurement gate. Not adopted in the base; recorded in Change 9. |
| C-004 (label of SK:1421-1422) | Regrade the two TDD checks from MEDIUM to High | Both keep them blocking until measurement; the label is part of the C-001 split. Not decided here. |
| X-010 count | A's "76 lines in 10 files" | Both counts (76/10, 88/14) are unreconciled (INV-009); neither is stated as fact. |
| U-007 history reading (A) | #343 shows a bucket mapping, not a Medium decision | X-003 went to B (82%): the fixture header at `review_severity_sweep_edits.yaml:29` records "open High/Medium findings HALT"; both quotes are true; only the framing is disputed. The base keeps B's text with A's framing noted. |

## Risk Summary

| Change | Risk | Note |
|--------|------|------|
| 1 | Medium | Moves B's section 7 to the front; no content removed. |
| 2 | Low | Replaces one sentence and one evidence item. |
| 3 | Medium | New skill text is described, not applied; INV-017 and INV-018 are open for it. |
| 4 | Low | Both advocates' decision rules recorded. |
| 5 | Low | Adds pin sites. |
| 6 | Low | Range corrections only. |
| 7 | Low | Corrected reading, flagged as one reader, six items. |
| 8 | Low | Notes only. |
| 9 | Low | No winner declared for the five points. |
| 10 | Low | Record only; no resolution added. |

Overall: Medium, because of Changes 1 and 3. The risk that the merged text overstates the debate is handled by Changes 9 and 10: both name what stays open.

## Review Status

- Approval: auto-approved (non-interactive run; `--interactive` not set).
- Timestamp: 2026-11-14T17:33:00Z. The plan was drafted by the orchestrator from `base-selection.md` and the debate; no separate analytical-agent review of the draft was run.
