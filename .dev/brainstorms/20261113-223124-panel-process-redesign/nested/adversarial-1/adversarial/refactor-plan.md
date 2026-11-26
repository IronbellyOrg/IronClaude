# Refactoring Plan: Merge into Base (Variant 2, sonnet:analyzer)

Paths: `ADV` = `.dev/brainstorms/20261113-223124-panel-process-redesign/nested/adversarial-1/adversarial`; variants are `ADV/variant-N-original.md` (V1 architect, V2 analyzer = base, V3 backend). Debate evidence: `ADV/debate/`. Invariant resolutions: `ADV/invariant-probe.md`. The merged output is `nested/adversarial-1/merged-spec.md`.

## Overview
- Base: Variant 2 (sonnet:analyzer), selected by the debate tiebreaker (score margin 0.0482 < 0.05; V2 won 35 of 41 diff points against V1's 19)
- Incorporating strengths from: Variant 1 (cards, extractors, verifier checks, controls, REQ grouping), Variant 3 (parse check, off-path verifier, determinism, bootstrap), the debate (quota, one session, checklist arm K) and the fourteen invariant resolutions
- Planned changes: 16 (changes 1-16), plus 15 changes not being made
- Risk level: Medium (the numbers in Appendix A are recomputed, not copied; the merged text must stay consistent with them)
- Shape fixed by the orchestrator's brief and the debate: the merged specification keeps the same six sections and ends with EXACTLY TWO redesigns: **Redesign 1: Sweep Sheet** (a script extracts at most 12 typed items; each goes to 2 blind reviewers) and **Redesign 2: Recipe Ledger** (instruction only; class recipes by lens). The blind verifier (V3) is NOT a redesign and not on the critical path.

## Planned Changes

### Change 1: Document frame and conventions (from V2 header, V1 conventions block)
- **Source**: V2 header lines 1-9; V1 lines 3-12 (conventions)
- **Target**: Base, top of document (replace)
- **Rationale**: ST4 navigation aid; labels must not clash (CR3 finding). Use `HO-1..HO-6` for hold-out sets (never H1-H6, which are the harness fixes H1-H4) and `RS`/`SS`/`RL` for arm names; `Redesign 1` and `Redesign 2` everywhere (never "A" or "B"); extractor ids `E1-E7`; item ids `S<n>`; class ids `C1-C8`; issue ids `B1..B8, I1..I7` (never GT labels); I7 sits on the control package (scored out of 2) and is outside every "of 14" sum
- **Integration point**: Conventions block of at most 14 lines: path abbreviations, evidence files (seed, IG, EXT, DS, AC, PAT, HO2, MR), the label rules above, "all probabilities are planning values", "per run = one panel run on one package"
- **Risk**: Low - additive

### Change 2: Section 1 Theories (V2 base, V1 numbers)
- **Source**: V2 section 1 (table, issue-to-cause map, rejected rival); V1 section 1 evidence tables and "explains / does not explain"
- **Target**: Section 1 (restructure)
- **Rationale**: C-019, S-005 (V2, 80%); numeric tables from V1 raise CO1 and CR5
- **Integration point**: keep V2's T1, T2 (T2a/T2b), T3 (T3a/T3b) rows; add V1's evidence numbers (unnamed-file rates ember 8%, luna 1%, haiku 0%, sonnet 35%, grok 33%; 0 of 176 cheap control runs; 7 of 8 openers found I7; 16 findings on one sentence all asking the same question) as sub-bullets; keep the rejected reasoning-budget rival (rho 0.64; within-model 0.25 to 0.22 and 0.09 to 0.09); add the issue-to-cause table (V2) and a final table "Mapping of redesigns to theories": Redesign 1 = T1 (the script runs the reverse sweeps) and T2 (one forced item question per anchor) with T3b; Redesign 2 = T2 (forced enumeration, other direction) and T1 partly (named search forms) with T3b; both depend on H1-H4 (T3a)
- **Risk**: Low

### Change 3: Section 2 Defect classes and generality (V2 base, V1 columns)
- **Source**: V2 section 2 table; V1 section 2 (strength column, review targets); V3 section 2
- **Target**: Section 2 (merge)
- **Rationale**: keep "the defect classes with their generality evidence"; C-024
- **Integration point**: one table with columns Class, Definition (target-neutral), Ten-issue instances (B1 B2 -> C1; B5 -> C2; I1 -> C3; I4 -> C4; I5 -> C5; B6 B8 -> C6; I6 -> C7; I7 -> C8), Recurrence outside the three packages (3, 6, 3, 9, 9, 12, 5 broad/1 narrow, 6), Strength (IG section 5), Review targets; then the outside evidence (ISO 29148 map, 59% precision and 82% recall for smell detectors, no catalogue entry for "universal claim unchecked against the corpus"), the seven other recurring classes X1-X7 (the ten are not special), and the limits (one repository, phrase-search lower bounds; records show a class exists, not that cheap panels miss it; C1 and C3 weak, C7 broad only). Add a "Hold-out set labels" key HO-1..HO-6 with the investigation labels in brackets (HO-1 = IG H5 docs-only plan, HO-2 = IG H2, HO-3 = IG H4, HO-4 = IG H3, HO-5 = IG H1 spec ledger, HO-6 = IG H6 sanity)
- **Risk**: Low

### Change 4: Section 3.0 Shared scaffolding (hybrid; new text built from V1 3.0, V2 shared brief changes, V3 3.3 and invariant resolutions)
- **Source**: V1 3.0 (cards, telemetry, graceful degradation, H table); V2 "Shared brief changes" CB-1..CB-3; V3 3.3 (H table with reasons) and coverage-v1 parse rule; invariant-probe.md INV-001, 002, 004, 005, 007, 012, 013, 014
- **Target**: new Section 3.0
- **Rationale**: C-004, C-005, C-006, C-007, C-018, C-024, A-001, A-004, A-006 and the six HIGH invariants
- **Integration point**: subsections in order. (3.0.1) Harness fixes H1-H4 with the gain table from the first brainstorm (`MR` lines 342-350: H3 +0.08, H1 +0.03, H2 +0.03, H4 0, total +0.14, range 0.03-0.34), grading rule and judge held constant (MR:320); V1's CB2 rubric edit is NOT used and may only be its own later arm. (3.0.2) Brief edits CB-1 (source named; rendered only when a source file exists; else log `no_source`, C2 not applicable), CB-2 (every confirmed defect listed; low harm is MINOR not omitted), CB-3 (blocker sentence), CB-4 (merge limits: anchor 12-200, claim at most 300, refs at most 8, one `findings-v1` block only, id of at most 16 characters), CB-5 free-review floor ("keep at least half of your time for your own review of the plan"). (3.0.3) Class cards as data (V1 schema minus adapter code) and the block-kind list used as the re-derive checklist (task, criterion, constraint, dictated text, edit target, gate). (3.0.4) Ledger carrier: a fenced `ledger-v1` JSON-lines block in the FINAL message directly above the findings block (INV-002: the launcher keeps only the final result message, `run-reviewer.sh:50`, and tests only the fence opener, `:57`); fields `item`, `verdict` (OK, PROBLEM, UNSURE), `quote_plan`, `quote_other`, `problem` (at most 300 characters), `ran` (at most 15 words); parsed by a real parser; concatenated assistant text is diagnosis only. (3.0.5) Checks and promotion (INV-005, 007): flattened substring tests (same normalisation as `findings.py` `flat` and `locate`); unsupported PROBLEM rows demoted to non-blocking; a PROBLEM row with no findings line makes the harness copy the reviewer's own `problem` text into a MINOR non-blocking finding, anchor from the plan-side quote, tagged `src=ledger`, validated by the same checks as `findings.py:90-121`, inserted inside the single existing block, logged and skipped on any failure, counted and reported separately. (3.0.6) Telemetry keys `class`, `probe`, `src` (unknown keys are accepted silently, HO2:346; a test must confirm). (3.0.7) Graceful degradation: any failure falls back to the isolated brief with CB-1..CB-5 and records `fallback=true`. (3.0.8) Reach is decomposed into extraction, selection, act, merge survival and judge credit and logged separately (A-001); found-any and found-blocking are reported separately (A-006). (3.0.9) Optional blind claim-only verifier (V3): off the critical path, runs only when measured spare time remains, cannot add claims, unverified or rejected claims go to follow-up candidates, never blockers, excluded from every time figure. (3.0.10) Messaging between reviewers is not used (herding evidence, EXT section 4)
- **Risk**: Medium - largest new block; must match findings.py rules exactly

### Change 5: Section 3.1 Redesign 1 Sweep Sheet - mechanism (V2 R1 base, V1 extractors, V3 determinism)
- **Source**: V2 Redesign 1 (a), question templates; V1 3.1(a) extractors E1-E7 with blind spots and item format; V3 3.1(a) determinism, shuffle seed
- **Target**: Section 3.1 (a)
- **Rationale**: C-001, C-003, U-006, U-011, U-019, U-021; INV-001, 011, 012, 013
- **Integration point**: steps in order S0 (H1-H4 sandbox), S1 (serial pre-pass, non-model, read-only, deterministic: same input and seed give byte-identical output; reads only the candidate, the source if any, and the pre-implementation snapshot; kill at min(15 s, 0.10 x b) then fall back to the isolated brief; grep scope = tests, root documents and named paths, `.dev/` excluded), S2 (selection: extractors E1-E7 emit candidates; quota 1 to 2 items per triggered class, remaining slots by ranked trigger strength, at most 12 items, ALL candidates and dropped items logged with the shuffle seed), S3 (assignment algorithm over 24 slots: each item to 2 of 3 blind reviewers; caps sum to 24; slowest-critical-path reviewer at most 8 on the primary panel, haiku and sonnet at most 6; replica 1 for items without attached tool output; if a reviewer fails, drop to replica 1 and never raise the others' load; order shuffled per reviewer), S4 (reviewers run with the baseline brief plus the sheet block; ledger in the final message), S5 (checks and promotion from 3.0.5), S6 (merge unchanged). Include the extractor table (E1-E7 with class, what it extracts, tool output attached, known blind spot; E6 experimental), the item format, the seven question templates (V2 "Question templates"), the quoted draft sheet block (V2 wording with the `ledger-v1` carrier replacing the table wording and the free-review floor), and the quoted brief additions. State the offline selection-recall gate (INV-001): before any model arm, the share of hold-out and planted defects whose trigger item is inside the 12 must reach a pre-registered floor, and the rank function must beat a random pick on the derivation plans
- **Risk**: Medium

### Change 6: Section 3.1 (b) roles, (c) time, (d) matrix, (e) breadth, (f) gain, (g) overhead, (h) effort, (i) failure modes - Redesign 1
- **Source**: Appendix A below (authoritative numbers); V2 R1 (b), (e); V1 3.1(e) anti-overfitting AO1-AO6; V1 (i) and V2 (i) failure rows
- **Target**: Section 3.1 (b)-(i)
- **Rationale**: C-008..C-013, C-020..C-023; INV-003, 004, 006, 008, 014
- **Integration point**: copy tables A2 (time), A5a (matrix), A6 (gain), A7 (overhead), A8 (effort) verbatim; roles from V2 R1 (b) (ember search items, lunas reading items, haiku at most 6, sonnet at most 6); breadth from V2 R1 (e) plus V1's block kinds and the per-target re-derive list; anti-overfitting AO list from Change 14; failure modes = union of V1, V2 rows plus new rows: selection miss repeats in every run on that document (INV-001), ledger lost when not in the final message (INV-002), promotion line rejected by the parser (INV-005), format-induced demotions (INV-007), kill and retry in the time arm (INV-008), shared item attention displaces free review (INV-014)
- **Risk**: Medium - numbers must match Appendix A

### Change 7: Section 3.2 Redesign 2 Recipe Ledger (V2 R2 base, V1 recipes and search forms)
- **Source**: V2 Redesign 2 (a)-(i); V1 3.0 recipe table (C1..C8 wording), V1 3.2 search-form line; invariant INV-010, 002, 007
- **Target**: Section 3.2
- **Rationale**: C-002, C-006, C-021; Q5 (one session, at most 4 recipes), INV-010
- **Integration point**: steps R0 (H1-H4), R1 (lens assignment table per panel; C2 and C4 duplicated), R2 (reviewers run baseline brief plus CB-1..CB-5 plus lens block; ledger in the final message), R3 (ledger check from 3.0.5; no luna re-ask; ember re-ask only if `now + 30 s <= 1.35 x b`), R4 (merge). Quote the ledger rule (V2 wording with `ledger-v1` JSON lines) and the eight recipes (V2 R-C1..R-C8 wording; V1 C5 recipe's "root-level documents, changelogs, mirrors" kept; V1 search-form line added for search lenses). Row budget per recipe, at most 14 rows per lens (C1 at most 4, C2 at most 6, C3 4, C4 4, C5 4, C6 4, C7 4, C8 4, never more than 14 per lens). Roles per panel from V2 R2 (b). Time and matrix from Appendix A3 and A5b. Failure modes: V2 R2 rows plus single point of failure (C5, C6, C8 live only in ember; C1, C3 only in luna 1; C7 only in luna 2), row cap forces salience choice, compliance (91.4% exact quoting) and `ledger_missing`
- **Risk**: Medium

### Change 8: Section 3 head - distinctness statement and open-question answer (new)
- **Source**: V2 section 3 intro; debate Q1, Q5
- **Target**: first paragraph of Section 3
- **Rationale**: the seed asks whether an instruction change alone is enough or whether a script must do the check; the two redesigns answer from opposite sides; exactly two redesigns are specified
- **Integration point**: one paragraph and a three-row table: what differs (who runs the sweep: script vs model; unit of coverage: typed item vs recipe row; code added: pre-pass vs none), what is shared (3.0), and the explicit statement that the blind verifier, a second ember session, V1's CB2 rubric edit and V3's shared 60-item list are NOT redesigns
- **Risk**: Low

### Change 9: Section 4 Comparison table (V1 and V2 tables, recomputed)
- **Source**: V1 section 4; V2 section 4; Appendix A
- **Target**: Section 4
- **Rationale**: keep "the comparison table"
- **Integration point**: rows from V1 (core mechanism, who finds the trigger, theories addressed, strong and weak classes, share of gain, I7, issues at "consistent", elapsed expected and modelled worst, tokens, effort, deterministic component, portability, maintainability seam, main risk, wrong-blocker risk), values from Appendix A (not the variants'); end with the recommendation: run both in the validation experiment; the shared scaffolding in 3.0 is built first; adopt by the pre-registered rule; if neither passes keep Z0
- **Risk**: Low

### Change 10: Section 5 Validation experiment (V2 base, V1 arms and gates, V3 statistics)
- **Source**: V2 section 5; V1 section 5; V3 section 4; INV-001, 003, 004, 009, 013
- **Target**: Section 5
- **Rationale**: C-015, C-016, C-017, U-004, U-005, U-012, U-013, U-015, U-022
- **Integration point**: Appendix A9 (arms, runs, gates) verbatim; plus the offline pre-experiment gates; hold-out material by HO label; derivation-set check reported but never used for a decision; cautions from V1 and V2 (reflect reports removed; plan sha equals the reviewed plan, UNVERIFIED; ground truth capped at what Tier-2 reviewers found); the pre-registration list; the consistency definition (reached in at least 60 percent of runs, with stable-hit rate and run-to-run Jaccard as secondary)
- **Risk**: Medium

### Change 11: Section 6 Numbered testable requirements (merged)
- **Source**: V1 section 6 (grouped tables with a Test column), V2 section 6, V3 section 5; invariant resolutions
- **Target**: Section 6
- **Rationale**: C-017, S-004; "keep the numbered testable requirements"
- **Integration point**: Appendix A10 list REQ-01..REQ-46 verbatim, grouped under: harness and brief, registry and ledger, Redesign 1, Redesign 2, time, contamination and overfitting, applicability, reporting and validation; each row has a Test column
- **Risk**: Low

### Change 12: Closing "Not checked / UNVERIFIED" note (V1, V2, V3 closings merged)
- **Source**: V1 last paragraph, V2 last paragraph, V3 UNVERIFIED line; INV findings
- **Target**: end of document
- **Rationale**: honesty about estimates (CR5, CO3)
- **Integration point**: list: all probabilities and selection factors are planning values; 48 tokens/s is derived and unconfirmed; the 2 s per item cost, 8 s pre-pass and ledger compliance are unmeasured; the launcher/final-message and `findings.py` facts were read (cited), the telemetry-key acceptance is from the hand-off table and needs a test; the plan sha equality is unchecked; the 348 s figure is a per-run mean summed over three packages (COMBO-REPORT final table) while the gate uses per-package medians of a same-day Z0 arm
- **Risk**: Low

### Change 13: Failure-mode union (V1 + V2 + V3 rows)
- **Source**: V1 (i) both; V2 (i) both; V3 (i) both
- **Target**: 3.1 (i) and 3.2 (i)
- **Rationale**: C-023 (95%, union)
- **Integration point**: each row has Failure, Effect, Probability (low, medium or high, planning value), Mitigation; this adds the probability column that the rubric (RK1) found missing in V1 and V2; recovery path named for each row (RK3)
- **Risk**: Low

### Change 14: Anti-overfitting rules (union)
- **Source**: V1 AO1-AO8; V2 AO-1..AO-8; V3 four rules
- **Target**: 3.0.3 (shared) and referenced from (e) of both redesigns
- **Rationale**: C-014 (unanimous)
- **Integration point**: AO-1 4-word-sequence lint against every `ground-truth.json` description and plan quote plus no package, task or file names; AO-2 swap test (a recipe or question still reads correctly with domain nouns replaced by placeholders) and second-author review who has not seen ground truth; AO-3 every card cites at least 2 instances outside the study packages (3 or "plausible only" for the extractor); AO-4 extractors tested on at least 3 plans not used to write them; AO-5 recipes, extractors, regexes and cards frozen by git tag and hash before hold-out ground truth is written; AO-6 ground truth never in the sandbox, probe reads only candidate, source and snapshot; AO-7 leave-one-class-out ablation (other classes' reach moves at most 15 points); AO-8 a recipe never states an expected outcome and no worked example comes from the three packages
- **Risk**: Low

### Change 15: External-environment and guard rows (new; from INV-013, 012, 008)
- **Source**: invariant-probe.md
- **Target**: 3.0 and the failure tables
- **Rationale**: RK4 (external dependencies), IV1-IV3
- **Integration point**: rows for gateway or model unavailability (reviewer killed or retried counted as zero findings), judge API error audit, repository search time on large trees, missing source or snapshot, empty sheet, single class triggered, all 12 items from one class (quota prevents), only two reviewers left
- **Risk**: Low

### Change 16: Provenance annotations and merge header
- **Source**: skill provenance rules
- **Target**: whole merged document
- **Rationale**: every section carries `<!-- Source: ... -->`
- **Integration point**: header comments (Provenance, Base, Merge date); per-section tags naming base, incorporated variant section, or debate/invariant source; tags are HTML comments
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base or Base Approach | Rationale for Not Merging |
|------------|---------------------------|---------------------------|
| C-007, X-002 | V1 CB2 rewrite of the Medium sentence and a blocking missing-requirement rule | Mixes a rubric change into the design effect; the first brainstorm pins grading and judge (MR:320); 3 of 3 advocates conceded; allowed only as its own later arm |
| C-002 | V1 second fresh ember session | One session isolates the prompt-only effect (Q5, 2 of 3); adds a launcher variable |
| C-001, C-003 | V3 one shared list of up to 60 items for every reviewer | Cost per item breaks +35% (X-003, X-004); class-order truncation lets C6 crowd out C1 and C3; V3 conceded |
| C-002 | V3 Blind Lenses then Verify as a redesign; verifier on the critical path | On a consistent baseline B = 168 s (+37.7%) at b = 122 and 146 s (+46%) at b = 100; kept only as an off-path audit (Q1, unanimous) |
| C-009, X-005 | V1 and V3 kill at D = 1.35 x baseline; V2 1.6 x deadline | A kill discards reports and biases arms; replaced by medians plus a hang guard of 1.5 x (b + expected overhead), intention-to-treat |
| C-011, X-001 | V1 (+0.2 to +0.7) and V3 (+0.4 to +0.9) harness-share estimates | Unsupported; the first brainstorm table gives +0.14 (0.03-0.34) |
| C-020 | V1 target adapter classes and adapter code | Flat extractors and data cards until a second target exists (V1 conceded) |
| C-003 | V2 fixed per-class caps Q2/U2/M2/R2/S2/K1/X1 | Replaced by a quota of 1 to 2 per triggered class with ranked fill and a dropped-item log |
| C-005 | V1 auto-promotion that writes the claim from the reviewer's row | Replaced by copying the reviewer's own `problem` text (V2 and V3 over V1, 2 of 3) |
| A-004, C-008 | V2 option to build the sheet while reviewers read | The brief cannot change after a kill, so the isolated-brief fallback is impossible (INV-012); serial mode only; parallel mode would be a separate later arm |
| INV-010 | V2 resume re-ask for luna | `now + 30 s <= 1.35 x b` can never hold for luna (b + 22 + 30 > 1.35 b) |
| C-013 | Mean of the V1 and V2 per-issue matrices | They describe designs the consensus dropped (INV-006); recomputed from the consensus design only |
| C-012 | V1, V2 and V3 stated totals (3.2-6.1) | Recomputed with the selection factor and displacement 0.1-0.9 (Appendix A6) |
| C-015 | Hold-out labels H1-H6 and arm labels A, B, A0-A4 | Clash with harness fixes H1-H4 and issue labels (rubric finding CR3); renamed HO-1..HO-6, SS, RL, Z0, Z0-raw, K |
| C-010 | V3's time table (luna 102 + 18 against baseline 122) | Mixed per-reviewer and per-package medians; recomputed |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 4 | Medium | Wrong ledger or promotion rules would make the redesigns fail parser checks | Revert 3.0.4-3.0.5 to the V2 ledger text and mark REQ-13 to REQ-17 open |
| 5, 6 | Medium | Time or matrix numbers inconsistent with Appendix A | Re-copy Appendix A tables; merge-review recomputes every sum |
| 7 | Medium | Lens table does not cover all eight classes | Check against the coverage table in 3.2 (b) |
| 10 | Medium | Arm and run counts do not add up | Recompute from Appendix A9 |
| 1-3, 8, 9, 11-16 | Low | Wording or labels drift | Fix in place |

## Review Status
- [x] Auto-approved (default, `--unattended`)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-13T23:47:00Z

---

## Appendix A: Authoritative content for the merge (copy; do not recompute differently)

### A1. Named baseline and cap
- **Z0** = the isolated panel (ember + 2x luna; haiku + 2x luna; sonnet + 2x luna) with H1-H4 and CB-1 to CB-5, run in the same randomised block and on the same day as the redesign arm. **b** = its per-package median of the slowest reviewer. The gate (D1) uses these measured medians. For planning only, the seed's first-study medians stand in: ember + 2x luna b = 100-122 s per package (the 348 s figure is a per-run mean summed over the three packages), haiku + 2x luna 220-238 s, sonnet + 2x luna 259-302 s. Cap = 1.35 b: 135.0 s at b = 100, 164.7 s at b = 122; 297-321 s (haiku); 350-408 s (sonnet).
- Panel elapsed is set by the slowest reviewer; the fast reviewer (ember, about 41 s) idles about 60-90 s on the primary panel; this idle time is where the redesigns put the evidence-heavy items (the only reallocation).
- Per-item cost model (UNVERIFIED): a ledger row of about 75-90 tokens at 48 tokens/s (derived from luna's 4.9k tokens in 102 s) is about 1.6-1.9 s; planning value c = 2 s per row for luna; 4 s for haiku; 3 s for sonnet; ember about 0.4 s.

### A2. Redesign 1 time budget (seconds per package), primary panel
| Step | Actor | Baseline | Redesign 1 | Bound | Critical path |
|---|---|---|---|---|---|
| S0 sandbox build (base commit) | harness | same | same | none | no |
| S1 pre-pass | script | 0 | 8 expected | kill at min(15 s, 0.10 b): 10 s at b = 100, 12.2 s at b = 122 | yes |
| S2-S3 selection, assignment, brief render | script | 0 | 1 | none | yes |
| S4 ember (9 items, search items) | ember | 41 | about 62 (3 s sheet + 9 items x 2 s) | hang guard | no (slack 60-90 s) |
| S4 luna 1 and 2 (8 items each) | luna | b | b + 3 + 8 x 2 = b + 19 | hang guard | yes |
| S5 ledger check and promotion | script | 0 | 1 | none | yes |
Critical path = 8 + 1 + (b + 19) + 1 = b + 29.
| b | Expected (b + 29) | Increase | Pre-pass at its kill limit | Increase | At break-even per item (2.75 s) | Cap |
|---|---|---|---|---|---|---|
| 100 | 129 | +29.0% | 10 + 1 + 119 + 1 = 131 | +31.0% | 8 + 1 + 100 + 3 + 22 + 1 = 135 | 135.0 |
| 122 | 151 | +23.8% | 12.2 + 1 + 141 + 1 = 155.2 | +27.2% | 8 + 1 + 122 + 3 + 3.71 x 8 break-even = 164.7 at 3.71 s per item | 164.7 |
| mean 116 | 145 | +25.0% | | | | 156.6 |
| three-package sum 348 | 348 + 87 = 435 | +25.0% | | | | 469.8 |
Break-evens at b = 100: pre-pass 14 s; 2.75 s per item (8 items). If the timing spike shows more than 2.75 s per item, luna's share drops to 6 items and ember takes the remainder (24 slots: 6 + 6 + 12), critical path b + 25.
Other panels: haiku + 2x luna: critical path haiku, b + 8 + 1 + 3 + 6 x 4 + 1 = b + 37: 257 s (+16.8%) at 220, 275 s (+15.5%) at 238; luna about 121 s stays off the path. sonnet + 2x luna: b + 8 + 1 + 3 + 6 x 3 + 1 = b + 31: 290 s (+12.0%) at 259, 333 s (+10.3%) at 302.
Enforced by structure: pre-pass kill, 12-item cap, hang guard at 1.5 x (b + expected overhead) from launch (kills and retries scored as zero findings, intention-to-treat). Only expected: per-item cost, pre-pass seconds, median elapsed (measured against same-day Z0; one panel clock starts before the pre-pass and reports mean and median).

### A3. Redesign 2 time budget (seconds per package), primary panel
| Step | Actor | Baseline | Redesign 2 | Bound | Critical path |
|---|---|---|---|---|---|
| R1 lens render | script | 0 | 1 | none | yes |
| R2 ember (4 recipes: 4 searches x 3 s + up to 14 rows x 0.4 s + thinking) | ember | 41 | about 81 | hang guard | no |
| R2 luna 1 and luna 2 (3 recipes each, rows at about 2 s) | luna | b | b + 4 + rows x 2: expected 11 rows b + 26, worst 14 rows b + 32 | hang guard | yes |
| R3 ledger check | script | 0 | 1 | none | yes |
Critical path = 1 + (b + 4 + 2 x rows) + 1: expected b + 28, worst b + 34.
| b | Expected (b + 28) | Increase | Worst, 14 rows (b + 34) | Increase | Cap |
|---|---|---|---|---|---|
| 100 | 128 | +28.0% | 134 | +34.0% | 135.0 |
| 122 | 150 | +23.0% | 156 | +27.9% | 164.7 |
| mean 116 | 144 | +24.1% | 150 | +29.3% | 156.6 |
| three-package sum 348 | 348 + 84 = 432 | +24.1% | 348 + 102 = 450 | +29.3% | 469.8 |
Break-even at b = 100: 2.07 s per row at 14 rows (29 / 14). If the spike shows more than 2 s per row, the lens cap drops to 12 rows (break-even 2.42 s). No re-ask for luna; ember re-ask only if `now + 30 s <= 1.35 b`. Other panels: haiku {C5, C6, C8} at most 6 rows x 4 s + 4 + 2 = b + 30: 250 s (+13.6%), 268 s (+12.6%); sonnet {C5, C6, C8, C2} at most 8 rows x 3 s + 4 + 2 = b + 30: 289 s (+11.6%), 332 s (+9.9%).

### A4. Model roles (both redesigns)
Primary (ember + 2x luna): Redesign 1: ember takes search-routed items (E2, E3, E4 and E1 counting items; about 9 items), lunas take reading-routed items (E1 C1 part, E5, E7, E6; 8 items each); every item has 2 reviewers, replica 1 for items without attached tool output. Redesign 2: ember {C4, C5, C6, C8}; luna 1 {C1, C2, C3}; luna 2 {C2, C4, C7}. haiku + 2x luna: haiku is the critical path, so at most 6 items (Redesign 1) or {C5, C6, C8} with at most 6 rows (Redesign 2); lunas take 9 items or {C1, C2, C3} and {C1, C4, C7}. sonnet + 2x luna: sonnet at most 6 items or {C5, C6, C8, C2}; lunas {C1, C3, C7} and {C4, C7, C1}. Only cheap models review; sonnet appears as a comparison panel.

### A5a. Redesign 1 coverage matrix (per run, primary panel). act = V2's act range (extracted and the model acts and the finding survives); s = selection factor (planning; replaced by the measured selection recall); reach = act x s (low x low, high x high)
| Issue | Class | Trigger item (class-level) | act | s | reach | Reviewer slot | Why a cheap model then reaches it / why not |
|---|---|---|---|---|---|---|---|
| B1 | C1 | E1: criterion with a set word beside its task's named scope, asks for the finite check | .10-.35 | .35-.70 | 0.04-0.25 | luna x2 | One-step question; never anchored before (0 anchors in 98 cheap reports). Lexical rank on 34 candidate lines is the weak step |
| B2 | C1 | E1 same item, scope of criterion differs from the instruction's | .15-.40 | .35-.70 | 0.05-0.28 | luna x2 | Two scopes side by side is a read, not a search |
| B5 | C2 | E5: source rule whose identifiers are missing from the citing task | .20-.45 | .40-.70 | 0.08-0.32 | luna x2 | Gives the rule so the 39% source skip no longer matters; misses when identifier overlap is high or the rule is carried in words |
| I1 | C3 | E6 (experimental): read value with no write occurrence | .03-.15 | .25-.50 | 0.01-0.08 | luna | Weak extractor, weak class; not expected to be reached |
| I4 | C4 | E2: pattern vs ordered text, NO MATCH printed | .50-.75 | .80-.95 | 0.40-0.71 | ember + luna | Mechanical; H3 removes the repaired text that gave a false pass |
| I5 | C5 | E4: negative criterion or number phrase with whole-tree hits in an unnamed root document | .35-.60 | .65-.90 | 0.23-0.54 | ember + luna (hits attached) | The hit is handed over; the 16 earlier findings asked the opposite question |
| B6 | C6 | E1: universal sentence plus the task that defines the enforcing test | .05-.20 | .40-.70 | 0.02-0.14 | ember + luna | Contradicting tasks are not scripted; reach depends on the model |
| B8 | C6 | E1: universal sentence over a class of files; asks for one counting search | .10-.30 | .35-.65 | 0.04-0.20 | ember + luna | Ember runs the search it is asked for, but the search form is the model's |
| I6 | C7 | E7: clause with no token overlap in a block that overlaps another clause | .15-.35 | .40-.65 | 0.06-0.23 | luna x2 | Narrow form, weak support |
| **Sum, nine issues in the 14** | | | | | **0.92-2.73** (central 1.83) | | |
| I7 (control, of 1) | C8 | E3: unnamed test file that references an edited path | .40-.65 | .85-.95 | 0.34-0.62 | ember + luna | 7 of 8 runs that opened the file found it; the item makes opening it an instruction |

### A5b. Redesign 2 coverage matrix (per run, primary panel). act = V2's Recipe Ledger range; s = self-selection within the row budget (the model picks which sentences to ledger); reach = act x s
| Issue | Class | Recipe step (class-level) | act | s | reach | Reviewer slot | Why / why not |
|---|---|---|---|---|---|---|---|
| B1 | C1 | R-C1 step 1: write the finite check for each set-word criterion | .10-.30 | .50-.85 | 0.05-0.26 | luna 1 | A written stopping rule is a new move; models may accept a vague rule |
| B2 | C1 | R-C1 step 2: copy the instruction sentence, write both sets | .10-.30 | .50-.85 | 0.05-0.26 | luna 1 | Short comparison, no search |
| B5 | C2 | R-C2: rule by rule carry and one failure-path trace | .15-.35 | .50-.80 | 0.08-0.28 | luna 1, luna 2 | Up to 10 rules, 6 rows; terse luna may leave rules unrecorded |
| I1 | C3 | R-C3: table of read values against writers | .05-.20 | .40-.70 | 0.02-0.14 | luna 1 | Models tabulate when told; weak class |
| I4 | C4 | R-C4: apply the literal pattern to the ordered text | .40-.70 | .60-.90 | 0.24-0.63 | ember, luna 2 | Pure reading and a one-line `printf` test; the model must choose the criteria |
| I5 | C5 | R-C5: whole-tree search for the old literal incl. root documents | .20-.45 | .50-.80 | 0.10-0.36 | ember | Ember greps; the weak step is choosing which changed claim to search |
| B6 | C6 | R-C6 step 3: what does the enforcing test skip, what do other tasks say | .05-.20 | .40-.70 | 0.02-0.14 | ember | Key evidence sits in other tasks |
| B8 | C6 | R-C6 step 2: one count command over the set | .10-.30 | .35-.65 | 0.04-0.20 | ember | Ember has never run an inventory unprompted; the recipe gives the command shape |
| I6 | C7 | R-C7: clause by text tick table | .10-.30 | .40-.70 | 0.04-0.21 | luna 2 | A matrix over many blocks is hard for a terse model |
| **Sum, nine issues in the 14** | | | | | **0.63-2.47** (central 1.55) | | |
| I7 (control, of 1) | C8 | R-C8: `git grep -l` of each edited path over tests, scripts, docs; open unnamed hits | .20-.45 | .55-.85 | 0.11-0.38 | ember | Opening an unnamed test file is the step luna and haiku skip |
Not reached by either (and why): I1 (C3: no reliable trigger shape; extractor experimental), I6 (narrow one-clause form of C7), B6 and B8 (need counting searches whose form the model must invent; the contradicting task is not extractable). "Consistent" (reach at least 0.6 in at least 60% of runs) is expected only for the mechanical classes: I4 and I7 at the high end of Redesign 1 (I4 0.40-0.71, I7 0.34-0.62); not expected for Redesign 2 (I4 0.24-0.63).

### A6. Expected gain, issues found out of 14 per run (ember + 2x luna), harness share and redesign share kept apart
| Block | Low | Central | High | Basis |
|---|---|---|---|---|
| Baseline Z0-raw (isolated ember + 2x luna) | 1.83 | 1.83 | 1.83 | measured (seed) |
| Harness fixes H1-H4 (share H) | +0.03 | +0.14 | +0.34 | MR:342-350 bottom-up table (H3 +0.08, H1 +0.03, H2 +0.03, H4 0); replaced by Z0 minus Z0-raw |
| Redesign 1, gross (nine issues) | +0.92 | +1.83 | +2.73 | A5a sums |
| Displacement of easy finds (shared item attention, ledger time) | -0.90 | -0.50 | -0.10 | planning range (INV-014), measured as non-probe findings per run |
| **Redesign 1 net share** | **+0.02** | **+1.33** | **+2.63** | low pairs the worst of each term |
| **Total found Redesign 1** | **1.9** | **3.3** | **4.8** | |
| Redesign 2, gross | +0.63 | +1.55 | +2.47 | A5b sums |
| **Redesign 2 net share** | **-0.27** | **+1.05** | **+2.37** | |
| **Total found Redesign 2** | **1.6** | **3.0** | **4.5** | |
Control package: I7 +0.34 to +0.62 of 1 (Redesign 1), +0.11 to +0.38 (Redesign 2). The best single panel run recorded is 4 of 14, so both high ends are optimistic. H share and redesign share are reported as separate numbers (R, Z0 minus Z0-raw, and arm minus Z0), never summed in a headline; the 0.1 overlap on I4, I1 and B5 (H3 masks them) is not removed.

### A7. Token overhead per package (baseline output 21.3k for ember + 2x luna; 63.7k haiku; 46.3k sonnet)
Redesign 1: +6k to +9k output (+28% to +42%; ledger about 8 rows x 40-90 tokens per luna plus ember's extra tool use); input +1.2-2.5k per reviewer for the sheet; the pre-pass uses no model tokens. Redesign 2: +5k to +8.5k output (+25% to +40%); recipes about 300 tokens per lens, about 800 for all eight. haiku and sonnet panels: +6k (about +9% and +13%). All unmeasured.

### A8. Implementation effort (lines, unmeasured; adapter code dropped)
Shared scaffolding (cards as data and loader, lint, `ledger-v1` parser and checks, promotion function, H2 truncation, telemetry): about 450. Redesign 1 specific: extractors E1-E7 and item model about 450-600, CLI and assignment about 90, fixtures for non-study plans about 250, tests about 150: about 650-800. Redesign 2 specific: recipes text about 120 lines, launcher lens table and row-budget rule about 70, brief about 40, tests about 80: about 250-310. Totals: Redesign 1 about 1,100-1,250; Redesign 2 about 700-760.

### A9. Validation experiment content
Hold-out material (none from the three study packages): HO-1 docs-only plan (11 items, about 1 hour), HO-2 plan (4-8 items), HO-3 plan (12 items), HO-4 larger plan (9 important findings, about half a day), HO-5 spec with a validated 44-defect ledger (use the 20 blocking rows; tuned on by earlier work, not by these designs), HO-6 sanity (3 items, in no decision); planted set: 6 full-size real plans with at least 8 competing candidates per class, one planted defect per class by an author who has not seen the recipes or extractors, plus their clean twins; documentation arm: about 8 delivered documents with a false universal sentence and a recorded retry finding, reviewed at the commit before the fix (recoverability from git checked first). Cautions: remove `.dev/reflect/`, `artifacts/` and `progress.md` from every sandbox; verify the reviewed plan equals the plan in the package (sha256, UNVERIFIED); Tier-2 ground truth is capped at what those reviewers found; freeze recipes, cards, extractors and regexes by git tag before hold-out ground truth is written.
Arms: **Z0-raw** (current harness, no fixes; HO-1..HO-3 only), **Z0** (H1-H4 + CB-1..CB-5; the control to beat and the named time baseline), **K** (Z0 plus one paragraph naming the eight checks in plain words, no recipes, no sheet, no ledger; merges V1's A4 and V2's placebo), **SS** (Redesign 1 + fixes), **RL** (Redesign 2 + fixes); adaptation arms Zh, SSh, RLh (haiku + 2x luna) and Zs, SSs, RLs (sonnet + 2x luna, comparison only).
Runs. Stage 1 (decision): HO-1..HO-4 x {Z0, K, SS, RL} x 5 = 80; Z0-raw on HO-1..HO-3 x 5 = 15; total 95. Stage 2 (only for arms that pass D1, D2 or D3 on Stage 1): planted 6 x {Z0, SS, RL} x 3 = 54; clean twins 6 x 3 arms x 2 = 36; spec HO-5 x 3 arms x 5 = 15; documentation 8 x 3 arms x 3 = 72; haiku 4 documents x 3 arms x 3 = 36; sonnet 3 documents x 3 arms x 2 = 18; total 231. Grand total 326 panel runs (about 980 reviewer runs). One blind Opus judge per run-package with a frozen rubric, a second judge on a 15% sample. Pre-experiment checks (no arm): 5-run timing spike on luna; 5-run compliance spike per redesign (`ledger_missing` rate, quote validity); offline selection-recall measurement; Z0-raw versus Z0 to replace +0.14.
Consistency: reach rate per item = runs finding it / runs; **consistent** = reached in at least 60% of runs (3 of 5); primary metric = share of hold-out items that are consistent per arm; secondary: found fraction per run, share of runs finding at least half, run-to-run Jaccard, stable-hit rate, wrong blockers per run, found-any versus found-blocking, non-probe findings per run, elapsed, tokens, kills, retries, fallbacks, per-class reach with Wilson intervals; bootstrap resamples packages first, then runs.
Pre-registered gates (versus Z0, pooled over HO-1..HO-4 unless stated): **G0 offline** selection recall at or above the pre-registered floor and the rank beating a random pick on the derivation plans (SS only); `ledger_missing` at most 10% and luna per-item cost below break-even (both); **D1 time**: per-package median elapsed at most 1.35 x Z0's median for the primary and the haiku panel, 90th percentile at most 1.50 x, kills at most 10%, intention-to-treat; **D2 effect**: mean found fraction at least Z0 + 0.12 absolute with the 90% bootstrap lower bound above Z0 + 0.04; **D3 consistency**: consistent items at least Z0's count + 3; **D4 precision**: wrong blockers per run at most Z0 + 1.0 and blocking findings on clean twins at most Z0 + 0.7; **D5 generality**: planted detection at least 0.40 on at least 3 of the 5 general classes (C2, C4, C5, C6, C8) in plans and on at least 2 in specs; documentation arm and HO-5: D2 holds with the lower bound above 0 or the claim is withdrawn to plans only; **D6 non-regression**: items Z0 reaches at 0.5 or more stay within 0.10 of Z0 (blocking gate); **D7 beats the checklist**: gain over K at least 0.04 absolute on D2's metric, otherwise K wins. Outcomes: neither passes: keep Z0 and report per-class results; one passes: adopt it; both pass: adopt the higher found fraction, and if the difference is under 0.05 adopt Recipe Ledger (no script to maintain); K within 0.03 of RL: report that recipe wording adds nothing over plain words and adopt the cheaper form; Z0 minus Z0-raw replaces +0.14; the measured act rate per class replaces every planning probability. Power is low (about 25-30 items, 5 runs per document, 4 packages): a pass is evidence, not proof. The three study packages are re-run once as a derivation-set check, never as evidence for adoption.

### A10. Numbered requirements (REQ-01..REQ-46; each with a Test)
Harness and brief: REQ-01 the brief names the source only when a source file exists; else logs `no_source` and C2 is not applicable (test: render with and without a source). REQ-02 the merge truncates anchor and anchor2 to 200 and claim to 300 characters (a prefix of an exact quote) and validates with the real parser (test: 250-character anchor survives). REQ-03 the sandbox is built at the plan's base commit, or the recorded working tree for documents without a commit (test: a file created by the implementation is absent). REQ-04 the sandbox holds no `.dev/reflect/`, `artifacts/`, `progress.md`, no report about the package and no ground truth (test: `find` and `grep -r`). REQ-05 CB-1..CB-5 present verbatim; grading rule, six findings categories and judge unchanged (test: string match, set equality, sha256).
Registry and ledger: REQ-06 eight cards validate against the schema; recipe at most 120 words; at least 2 instances outside the study packages (test: schema and word count). REQ-07 lint fails on any 4-word sequence from a ground-truth description or plan quote or any package, task or file name (test: real run and a seeded leak). REQ-08 swap test and second-author review recorded per card (test: review record). REQ-09 rendered briefs hold no `src/superclaude/` path (test: grep). REQ-10 a new class is one card plus an optional extractor with no dispatcher change (test: fixture card). REQ-11 findings may carry `class`, `probe`, `src`; existing merge tests pass (test: suite with extra keys). REQ-12 on failure of the pre-pass, lens render or ledger check the harness runs the isolated brief with `fallback=true` (test: forced exception). REQ-13 the ledger is a `ledger-v1` JSON-lines block in the final message directly above the single findings block; both blocks parsed by a real parser, not the fence-opener grep (test: reports with misplaced, duplicated or truncated blocks). REQ-14 substring checks use the same flattening as `findings.py` (test: quote that wraps a plan line). REQ-15 the promotion function copies the reviewer's own `problem`, takes the plan-side anchor, validates with `_check_finding`, inserts inside the single block, tags `src=ledger`, MINOR, non-blocking, and logs and skips on failure (test: ids over 16 characters, short anchors, duplicate ids). REQ-16 unsupported PROBLEM rows are demoted to non-blocking; blocking needs the grading sentence plus two quotes or a search result (test: unit). REQ-17 the `ledger_missing` rate from the compliance spike is at most 10% before any arm (test: spike report).
Redesign 1: REQ-18 the pre-pass is a non-model, read-only, byte-identical-for-same-input-and-seed script, serial, killed at min(15 s, 0.10 b) with fallback (test: run twice and compare bytes; sleeping stub). REQ-19 at most 12 items; quota 1-2 per triggered class, ranked fill; all candidates and dropped items logged with the seed (test: fixture with 200 set-word sentences). REQ-20 assignment over 24 slots with caps summing to 24, replica 1 for items without attached tool output, no growth in survivors' load on failure, order shuffled per reviewer (test: assignment unit test). REQ-21 extractors E1-E4 and E7 reach recall 0.8 or more on at least 3 non-study plans with seeded defects, precision reported; E6 labelled experimental (test: fixture suite). REQ-22 offline selection-recall gate and rank beats a random pick on the derivation plans (test: gate script). REQ-23 an empty sheet leaves the brief equal to Z0's (hash). REQ-24 search scope is tests, root documents and named paths with `.dev/` excluded and a time bound (test: timing on the largest tree).
Redesign 2: REQ-25 the eight recipes live in one file and are quoted verbatim by lens; at most 4 per reviewer; C2 and C4 duplicated (test: parse generated briefs). REQ-26 row budget per recipe, at most 14 rows per lens, `NONE FOUND` allowed (test: ledger check). REQ-27 no luna re-ask; ember re-ask only if `now + 30 s <= 1.35 b` (test: fake clock). REQ-28 the `ran` field is cross-checked against transcript tool calls in the analysis (test: analysis script).
Time: REQ-29 +35% is judged on per-package medians against same-day Z0 in the same randomised block, one panel clock from before the pre-pass, mean and median reported (test: timing log). REQ-30 hang guard 1.5 x (b + expected overhead) from launch; kills and retries per arm; killed or retried reviewers scored as zero findings (test: sleeping stub; analysis). REQ-31 the break-even values (pre-pass 14 s and 2.75 s per item at b = 100; row cost 2.07 s) are in the report with the measured values (test: report check). REQ-32 a 5-run luna timing spike precedes every arm and sets the fallbacks (6 items per luna; 12 rows) (test: spike record).
Contamination and overfitting: REQ-33 recipes, cards, extractors and regexes are frozen by git tag before hold-out ground truth is written (test: tag date earlier than the ground-truth commit). REQ-34 reviewers never receive ground truth; hold-out sandboxes exclude reflect reports (test: grep). REQ-35 leave-one-class-out ablation changes other classes' reach by at most 15 points (test: ablation report). REQ-36 hold-out ground truth is written and hashed before the first arm; planted defects authored by someone who has not seen the recipes or extractors; every planted plan has a clean twin (test: hash times; attestation).
Applicability: REQ-37 spec and documentation fixtures exist: E1, E2 and E5 produce items on a spec fixture; E4 and E1 on a documentation fixture (test: fixtures). REQ-38 the registry README lists, per target type, what must be re-derived (block patterns, command dialect, test and root-document paths, severity guidance, the location of truth) (test: document review).
Reporting and validation: REQ-39 all metrics come from one script over the run folders (test: fixture). REQ-40 gains are reported as H share, prompting share (K minus Z0) and redesign share, never summed in a headline (test: report check). REQ-41 reach is logged per stage (extraction, selection, act, merge survival, judge credit) and the per-class act-rate bands are pre-registered (test: log schema). REQ-42 displacement is measured as non-probe findings per run and D6 is a blocking gate (test: analysis). REQ-43 judge: blind Opus, frozen rubric, second judge on 15%, API-error audit per batch (test: audit log). REQ-44 arms, run counts, consistency definition and gates are committed before the first hold-out run (test: commit order). REQ-45 claims are worded "raises the per-run found fraction; consistency expected only for the mechanical classes C4, C5, C8" (test: report review). REQ-46 the optional verifier never sits on the critical path, cannot add claims, and its time is excluded from every figure (test: timing log).

## Errata found during merge and review (the merged specification is authoritative where it differs from Appendix A)

| Appendix A item | Plan text | Corrected in merged-spec.md | Found by |
|---|---|---|---|
| A8 effort | Redesign 1 specific about 650-800 lines; totals 1,100-1,250 | Specific about 790-1,090 (450-600 + 90 + 250-400); with the shared 450: about 1,240-1,540. Redesign 2 specific about 310; with shared about 760 | merge part B, corrected by part C |
| A4 roles | ember about 9 items | Ember 8 items (caps 8 + 8 + 8 = 24); in the timing-spike fallback only, ember is raised to 12 | merge-review B-1 |
| A7 tokens | Redesign 2 +5k to +8.5k "(+25% to +40%)" | +23% to +40% (5 / 21.3 = 23.5%) | merge-review B-2 |
| A9 D5 | planted detection "on at least 2 [classes] in specs" | clause removed: no planted spec is run; spec generality rests on HO-5 and the REQ-37 fixtures | merge-review B-3 |
| A9 power note | about 25-30 items | about 36-40 items in the Stage 1 decision sets (HO-1 11, HO-2 4-8, HO-3 12, HO-4 9) | merge-review B-4 |
| A10 REQ-45 | "consistency expected only for the mechanical classes C4, C5, C8" | "only for I4 and I7 (classes C4 and C8), and only for Redesign 1 at the high end of its range" | merge-review B-5 |
| A10 REQ-25 | "C2 and C4 are duplicated" | duplicated classes per panel: C2 and C4 (primary), C1 (haiku), C1 and C7 (sonnet) | merge-review B-6 |
| A10 REQ-12 | one rule: failure of pre-pass, lens render or ledger check runs the isolated brief | split: (a) pre-pass or lens render failure gives `fallback=true`; (b) post-run ledger check failure merges as written and records `check_skipped=true` | merge-review B-7 |
| A2 ember step | about 62 s (3 + 9 x 2) | about 60 s (41 + 3 + 8 x 2) | merge-review B-1 |
| A5a and A5b sums | 0.92-2.73 and 0.63-2.47 | unchanged; per-row values rounded to two decimals add to 0.93-2.75 and 0.64-2.48 (a rounding note was added in the document) | merge part B |
