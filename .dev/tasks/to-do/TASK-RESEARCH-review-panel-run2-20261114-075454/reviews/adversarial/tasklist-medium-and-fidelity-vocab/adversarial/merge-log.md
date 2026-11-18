# Merge Execution Log

## Metadata
- Base: Variant B (Proposal B, `variant-2-original.md`; default model, default persona)
- Executor: merge-executor agent (slot X-15)
- Changes applied: 10 of 10 planned (one with a documented sub-item not carried, see Change 4)
- Status: success
- Timestamp: 2026-11-14T17:44:45Z (merge started 2026-11-14T17:33:35Z)
- Output: `../merged-output.md` (7,511 words including provenance comments; 7,155 excluding them; the base was 3,459; a first draft of 8,211 words was trimmed to meet the "about 7000" limit)
- Inputs read: `variant-2-original.md`, `refactor-plan.md`, `variant-1-original.md` (first 60 lines), `round2-advocate-A.md`, `round2-advocate-B.md`, `debate-transcript.md`, `base-selection.md`, `invariant-probe.md`, templates Section 5 and 6, SKILL.md "Provenance Annotation System (T05.04)". `diff-analysis.md` was grepped for U-004, U-012, U-013, U-015 only.
- Not done: no code, test or artifact outside the two permitted files was read or changed; evidence tags in the merged output are the source texts' own, no claim was re-verified against the repo.

## Changes Applied

### Change 1: Inputs-first dependency table and reordered prerequisites
- **Status**: Applied
- **Source**: Variant A section 0 (C-01, C-02, C-03 table, "Outcome I rely on" column); Variant B section 7
- **Target**: new section 1 "Inputs and dependencies" at the top; old section 7 content moved into it; old section 7 became section 8, a pointer
- **Before**: B's section 7 came after design and evidence (re-evaluator marked ST1 NOT MET)
- **After**: a three-row table (slot, outcome relied on, where the position touches it and the reopening condition). B's three dependency statements and reopening conditions are kept; A's outcome column added; A's note that C-05 was not an input kept. All sections renumbered 1 to 10; the three internal `section N` pointers B had (section 7 below, section 2, section 4) were rewritten to the new numbers.
- **Provenance tag**: `<!-- Source: Variant A, section 0 - merged per Change 1; Base, section 7 (moved here) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS
- **Note**: the plan says "new section 0"; the executor instruction says renumber, so the new section is numbered 1.

### Change 2: Replace B's S4 premise with the consequence test
- **Status**: Applied
- **Source**: C-002, X-001, X-002, X-006; Round 2 of both advocates
- **Target**: base section 1 (now section 2, item 4) and E4 (now section 4); base section 2 S4 bullet (now 3.2)
- **Before**: "the tasklist skill's own model, which pragmatic.md S4 permits"
- **After**: the consequence test of PM:225 and PM:231 applied by analogy; S4 applies only after the skill states a model (X-002, B conceded); S5 not read as covering High/Medium/Low (X-006). E4 rewritten; the `/sc:implement` qa.md:81 and :274 fact added from A R2.
- **Provenance tag**: `<!-- Source: Base (original, modified) - S4 premise replaced per Change 2; two end states per Changes 3 and 9 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: Stage 7 grading block
- **Status**: Applied
- **Source**: Variant A section 2.2; Round 2 A+ block and Round 2 B H+ block; U-001, U-002, C-004, C-013
- **Target**: new subsection 3.3 "Stage 7 grading block"
- **Before**: B had no block (only "the skill states in one place that it applies its own severity model")
- **After**: the elements both advocates adopted; the H+ block and the A+ block carried verbatim as the two end states (each sentence checked with grep against `round2-advocate-B.md` and `round2-advocate-A.md`); a cost table per end state; the Medium definition, the place of "insufficient detail / ambiguity" and the label of SK:1421-1422 marked unresolved. The default is stated as the debate left it (section 2): B's H+ default with A+ only by the registered upgrade rule; A's A+ gated on measurement with fallback to H; INV-017 and INV-020 named.
- **Provenance tag**: `<!-- Source: Variant A, section 2.2 (grading block) - merged per Change 3; both Round 2 blocks carried verbatim -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Measurements F1, F2, F3 with both advocates' decision rules
- **Status**: Applied (with the sub-items below)
- **Source**: A M1, M2 (M-X15-1), M-X15-5; B M-X15-1..4 and Round 2 F1, F2, F3; C-011, S-005, X-004
- **Target**: base section 5 (now section 6)
- **Before**: B's M-X15-1..4
- **After**: static tests (H+: T1 to T4; A+: T1 to T3), a measurement table F1, F2, F3 with B's registered thresholds and A's differing rule side by side, M-X15-4 inside H+ T3, the default rule of each advocate, thresholds marked as design choices.
- **Sub-items**: (a) B's M-X15-2 (label-preserving replay) is not carried as a named measurement because its premise was withdrawn under Change 7; (b) B's M-X15-3 (pins) is carried as H+ T4; (c) A's T4 for Form 2 is dropped with Form 2, per the plan; A's Round 2 replacement T4 (the skill states "keep the highest severity" and tie-break-up) is mentioned as having the same content as H+ T1's clause. The plan names T1, T2, T3 only; (c) goes slightly beyond it and is flagged here.
- **Provenance tag**: `<!-- Source: Base (original, modified) - list replaced per Change 4; Variant A, section 5 (T1-T3, M1, M-X15-5) merged -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Pin inventory correction
- **Status**: Applied
- **Source**: C-005, C-006; Round 2 A W4 and new evidence 1; B Round 2
- **Target**: E3 (section 4) and section 3.3 cost table, section 5.1
- **After**: the pinned HALT phrase lives in CMD:113 (the skill says "this HALT resolves as blocked", SK:1615); both worker-contract pins at `test_worker_contract.py:777` and `:1861` read it through `_unattended_section` (`:893-906`); the byte-equal plan copy `.dev/review-severity-rule/sweep-edits.yaml`. Cost stated per end state: nothing changes under H+; A+ rewrites the SK sites, CMD:113, two pins, 12 fixture rows and the plan copy.
- **Provenance tag**: `<!-- Source: Base (original, modified) - pin sites corrected per Change 5; ... -->` (section 5.1) and the section 4 tag
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Corrected line ranges and counts
- **Status**: Applied (one range chosen by the executor, see note)
- **Source**: X-010
- **Target**: section 3.4 (base section 2), E5, E6, E9, section 5.1, section 6
- **After**: `prompts.py:49-69` (MEDIUM `:58-64`) for the severity definitions in E6; `roadmap/gates.py:195-240`; `test_tasklist_fidelity.py:208-225` everywhere. The "76 lines in 10 files" against "88 lines in 14 files" count is recorded as unresolved (INV-009, LOW) in E8 and section 5.3; neither is stated as settled.
- **Note**: the base cited `prompts.py:28-62` twice, once for the layering guard (section 2) and once for the MEDIUM definition (E6). The plan's replacement `:49-69` fits the severity definitions, not the guard. For the guard the merge used `prompts.py:6-8` and `:43-48`, the cite in Variant A's section 2.3 (tagged CODE-VERIFIED there), and says so in the text. The orchestrator should confirm this reading of the plan.
- **Provenance tag**: `<!-- Source: Base (original, modified) - line ranges corrected per Change 6 (X-010); ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 7: Corrected reading of the archived reports
- **Status**: Applied
- **Source**: C-010, X-004; A Round 1 Strengths 4 confirmed by B Round 2 W4
- **Target**: E6 and E7 (section 4); section 9 answer
- **After**: two omissions (v3.66 M2, test1 M1), two dropped acceptance criteria with Steps/Deliverables present (v3.66 M3, M4), one step contradicting a roadmap target (test1 M2), one expected value asserted as fact (v3.66 M1); one reader, six items, UNVERIFIED as a measurement. E7 keeps the header counts and states that the label-preserving replay ignores a grading block that moves omissions to High.
- **Note**: the plan says "four of six findings at stake under A+"; B Round 2 new evidence 4 says at most about two findings would be in the A+ Medium class. Both are recorded: four findings are not omissions and are classified by block wording; B's estimate is at most about two in the A+ Medium class [INFER; one reader]. No number was added.
- **Provenance tag**: see the section 4 tag
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 8: Hazard notes for later engine hosting
- **Status**: Applied
- **Source**: U-004, U-012, INV-016 (ADDRESSED)
- **Target**: section 3.1, tasklist module bullets
- **After**: a v2 tasklist lens must not set `reflect_category` (`findings_v2.py:161-162`; it is satisfied by the H+ map and contradicted by the A+ Medium row); `card_convert.py` sends `medium` to MINOR and `high` to MAJOR (`:71-83`), so the tasklist map must be its own table. Form 2 stated as withdrawn.
- **Provenance tag**: `<!-- Source: Base (original, modified) - hazard notes added per Change 8 (Variant A section 2.1; Base section 2) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 9: Table of the five unresolved points
- **Status**: Applied
- **Source**: Scoring Matrix rows C-001, C-007, C-012, C-013, C-014; "Remaining disagreements" of both Round 2 files
- **Target**: new section 10 "Points the debate did not resolve (Unresolved)"
- **After**: one row per point with A's final term, B's final term and what would decide it; scoring-matrix confidence recorded; no winner declared; the label of SK:1421-1422 noted as undecided; B's "no longer disputed" list recorded without its default item, because INV-017 contests that item.
- **Provenance tag**: `<!-- Source: Debate scoring matrix and the "Remaining disagreements" of both Round 2 files - merged per Change 9; no winner declared -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Open invariants and conditions from Round 2.5
- **Status**: Applied
- **Source**: `invariant-probe.md` (20 findings, 3 ADDRESSED, 17 UNADDRESSED; HIGH INV-017, INV-018)
- **Target**: new subsection 5.3 "Open Invariants the debate left unaddressed"
- **After**: INV-017 and INV-018 with their falsifying conditions; the 12 MEDIUM items (INV-001, 003, 004, 005, 007, 008, 010, 011, 013, 014, 019, 020) and 3 LOW items (INV-002, 009, 012) by ID with one line each; the ADDRESSED three named. States that none was resolved because standard depth has no Round 3. No resolution added.
- **Provenance tag**: `<!-- Source: Round 2.5 invariant probe (invariant-probe.md) - added per Change 10; record only, no resolution -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Additional content (not a planned change)
- **Status**: Applied, required by the delegation (content rule a)
- **Target**: unnumbered H2 "Debate outcome (as concluded)" before section 1, and a rewritten opening paragraph with an abbreviation key (SK, PR, PM, CMD, FX, RT)
- **After**: base selection and scores (A 0.9138, B 0.8664, margin 4.74%, tiebreaker level 1, B won 12 points against 4); convergence 32 of 37 = 86.5%; BLOCKED_BY_INVARIANTS; the five unresolved points named.
- **Provenance tag**: `<!-- Source: base-selection.md, debate-transcript.md - required content, not a planned change -->`

### Condensing for the word limit (not a planned change)
Base wording was condensed in E1 to E9, 5.1, 5.2, 7, 9 and the provenance comments without changing any claim, except for these removals: the path of the missing B3-10 source file in E2 (the text still says it is absent and the text UNVERIFIED); the grep phrase in 3.2; the sentence "a report with no fixer has nothing to do with a Medium row" in E5 (replaced by the X-007 note that the missing fixer is an inference); the interpretive sentence in E2 that the sweep header puts the mid label on the blocking side (replaced by B Round 2's statement that the header names no middle word).

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. H1 title, then H2 sections 1 to 10 (plus one unnumbered H2, "Debate outcome"), H3 only under sections 3 (3.1 to 3.4) and 5 (5.1 to 5.3); no level gaps, no orphan subsections.
- Section ordering: PASS. Inputs and dependencies come first, then position, design, evidence, invariants, measurement, effects, the consistency pointer, the objection and the unresolved points.
- Document flow: PASS. Status line is `Status: Merged (see Unresolved and Open Invariants)`; the headings "Open Invariants" (5.3) and "Unresolved" (10) match it. Zero `RF_PLACEHOLDER` markers remain. 17 provenance `Source:` tags plus the three header lines.

### Internal References
- Total references: 36 internal (`section N` / `sections N and M` in the body outside HTML comments)
- Resolved: 36 (targets 1, 2, 3, 3.1, 3.3, 5.2, 5.3, 6, 10 all exist)
- Broken: 0
- Excluded: 5 external `research/NN section N` citations (research/11 sections 2, 2.3, 2.4; research/12 sections 3, 4), the quoted finding text "Section 9.7", and `Variant X, section N` references inside HTML provenance comments, which name source variants, not targets in this file.

### Contradiction Re-Scan
- New contradictions introduced: 0
- Details: every statement that Medium blocks or does not block is attributed to an end state (H+ or A+), to an advocate, or to the shipped code; none is stated as a settled position. The five unresolved points (C-001, C-007, C-012, C-013, C-014) appear in sections 2, 3.3 and 10 as unresolved, each with both advocates' final terms. The B-side claims that INV-017 and INV-020 contradict ("no loosening before measurement", "default is a neutral resting point") are attributed to B and flagged as contested where they appear. Base-internal contradiction ST1/CR4 from scoring (sections 1-2 "the skill's own model" against section 8 "the skill states no model") is removed by Change 2.

## Summary
- Total changes planned: 10
- Successfully applied: 10
- Failed: 0
- Skipped: 0 (sub-items not carried: B's M-X15-2 as a named item; A's Form 2 T4)
- Post-merge validation: PASS
- Items for the orchestrator: (1) the Change 6 guard-citation choice; (2) the Change 4 sub-item (c); (3) the Change 7 "four of six" versus "at most about two" wording; (4) total length 7,511 words including provenance comments (7,155 without), about 7 percent over the 7,000 guide.
