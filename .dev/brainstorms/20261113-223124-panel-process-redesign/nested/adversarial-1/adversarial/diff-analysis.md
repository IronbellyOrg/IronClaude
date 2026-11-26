# Diff Analysis: requirements specification (panel process redesign) comparison

Variants: V1 = sonnet:architect (`variant-1-original.md`), V2 = sonnet:analyzer (`variant-2-original.md`), V3 = haiku:backend (`variant-3-original.md`). Seed brief: `.dev/brainstorms/20261113-223124-panel-process-redesign/seed-brief.md`.
Taxonomy tag per point (L1 surface, L2 structural, L3 state-mechanics) is shown in brackets after the ID title where it is not L2.

## Metadata
- Generated: 2026-11-13T23:12:00Z
- Variants compared: 3
- Total differences found: 41 (promoted points counted in the denominator: S 5, C 24, X 8, A 4)
- Categories: structural (5), content (24), contradictions (8), unique (22), shared assumptions (9; 4 promoted, 4 documented, 1 contradicted)

## Structural Differences

| # | Area | V1 (architect) | V2 (analyzer) | V3 (backend) | Severity |
|---|------|----------------|---------------|--------------|----------|
| S-001 | Section layout | Six sections: theories, classes, redesigns (3.0 shared scaffolding + two), comparison, validation, requirements | Same six sections; "shared brief changes" opens section 3 | Five sections: comparison is 3.4 inside section 3; harness fixes are 3.3 after the redesigns | Medium |
| S-002 | Placement of shared material (harness fixes H1-H4, brief edits) | 3.0 first: registry, adapter interface, H1-H4 table, CB1-CB4, recipes, telemetry, fallback | "Shared brief changes" CB-1..CB-3 before redesigns; H1-H4 by reference to the first brainstorm | 3.3 at the end; H1-H4 table with "why needed" | Medium |
| S-003 | Redesign sub-structure | (a)-(i) lettered blocks, identical for both | (a)-(i) lettered, identical for both | (a)-(i) lettered, identical for both | Low |
| S-004 | Requirements numbering and form | REQ-01..37 in 8 grouped tables with a Test column | R-01..32 in 3 grouped tables with a Test column | 20 numbered items each ending "Test:" | Medium |
| S-005 | Theory presentation | Per-theory evidence table + "explains / does not explain" + redesign-to-theory map + rejected rival | One table (theory, evidence, implied change) + issue-to-cause map (main and secondary cause) + rejected rival | One table + rejected paragraph, no per-issue map | Low |

## Content Differences

| # | Topic | V1 approach | V2 approach | V3 approach | Severity |
|---|-------|-------------|-------------|-------------|----------|
| C-001 | Redesign A shape (what the helper emits) | "Probe Sheet": 7 extractors E1-E7 emit typed items with evidence; at most 12 items per reviewer; deterministic `probe.json` | "Sweep Sheet": 6 extractors Q,U,M,R,S,K/X; at most 12 items in total, shuffled per reviewer | "Class Recipe Sweep": one shared list of up to 60 items (10 KB) for every reviewer | High |
| C-002 | Redesign B shape | "Lens Ledger": class recipes by lens, forced ledger, ember runs a second lens in idle time | "Recipe Ledger": recipes by lens (at most 4 per reviewer), ledger, one resume re-ask if time allows | "Blind Lenses then Verify": 3 blind lenses, deterministic union, one blind verifier stage | High |
| C-003 | Item routing and replication | Routed by card `route` (search or read) and `replicas`; data in the panel template | Each item goes to exactly two of three reviewers, about 8 per reviewer, at most 6 for the slow model | Every reviewer gets all items (A); packets S and R split by search or read (B) | High |
| C-004 | Where answers are written | Table `Probe responses` in the report body; findings lines carry optional `class` and `probe` keys | `## Check ledger` above the findings block; merge reads only the block | Separate fenced `coverage-v1` block; merge ignores it; parse check closes the fence-opener-only gap | Medium |
| C-005 | Verifying and promoting answers | Quote-substring check; unsupported PROBLEM demoted to non-blocking; PROBLEM with no finding promoted to a MINOR finding | `ledger-check.py`: line per item, finding per DEFECT, substring quotes; flags only (no promotion) | Audit of coverage verdicts; B adds blind verifier that cannot add claims | Medium |
| C-006 | Recipe and question granularity | 8 registry cards: recipe text at most 120 words plus a question template and extractor name | 8 recipes (with named steps) used as lens text; 7 printed question templates for the sheet | Five per-class item templates shown; recipe = "one detection move" per class | Medium |
| C-007 | Brief edits | CB1-CB4: source named, missing-requirement category and blocking rule, "list every mismatch", merge limits | CB-1..CB-3: source named, list every defect, blocker sentence; grading rule unchanged | One paragraph for the list, one for the lens, one for the verifier; no rubric change | High |
| C-008 | Pre-pass on the timeline | Serial before reviewers: 6 s expected, `timeout 12` | Serial 8 s (kill 15 s); fallback idea: build the sheet while reviewers do first reads | Serial 6 s, cap 15 s | Medium |
| C-009 | Time enforcement | Per-reviewer `timeout D`, D = floor(1.35 b); kill loses the report | Pre-pass kill, 12-item cap, panel deadline 1.6 x baseline; +35% judged on medians | `timeout 165` (A) or 150 plus verifier 45 (B) | Medium |
| C-010 | Baseline used in the arithmetic | b = 100 or 122 per package (slowest reviewer median) with a b + overhead table | Same b = 100-122; tightest cell shown (128 vs cap 135) | 122 for every package; critical path built from luna's own median 102 | High |
| C-011 | Harness-fix (H1-H4) gain | +0.2 to +0.7 of 14 (estimate) | +0.03 to +0.34, central +0.14, from the first brainstorm bottom-up table | +0.4 to +0.9 (estimate) | High |
| C-012 | Redesign gain ranges (total found of 14, ember + 2x luna) | A 3.4-6.1; B 2.8-5.5 | R1 3.2-5.7; R2 2.7-5.2 | A 3.4-5.0; B 3.3-4.8 | Medium |
| C-013 | Per-issue reach probabilities (examples) | A: I4 .45-.80, I5 .40-.75, B5 .10-.30, B1 .25-.45, I7 .55-.85. B: I4 .25-.60, I5 .15-.40, I7 .20-.50 | R1: I4 .50-.75, I5 .35-.60, B5 .20-.45, B1 .10-.35, I7 .40-.65. R2: I4 .40-.70, I5 .20-.45, I7 .20-.45 | A: I4 .60-.85, I5 .50-.75, B5 .30-.60, B1 .25-.55, I7 .55-.80 (labels GT1..) | Medium |
| C-014 | Anti-overfitting rules | AO1-AO8: 4-word n-gram lint, at least 2 outside instances per card, extractors tested on 3 plans, git-tag freeze, leave-one-class-out ablation | AO-1..AO-8: swap test, 3 outside instances, hashed freeze, second author reviews recipes, 8-word shingles | Four rules: no quotes, frozen regexes, no repo names hard-coded, never give the answer | Medium |
| C-015 | Hold-out material | H5, H2, H4, H3 plans, H1 spec, documentation arm (about 8 delivered docs), H6 sanity | Real-1/2 (H5,H2,H4,H3), spec H1, H6 sanity, planted defects (6 docs x 8 classes), clean twins | H5, H2, H4 only (about 25 items), H1 optional | High |
| C-016 | Arms and controls | A0, A1 (fixes + CB), A2, A3, A4 generic-checklist control, Stage 2 haiku and sonnet | Z0, Z0-raw, P placebo (class names only), A, B, haiku and sonnet versions | A0, A1, A2, A3 (sonnet comparison); no placebo or checklist control | High |
| C-017 | Consistency measure and decision rule | consistent = reached in 4 of 6 runs; G1-G7 incl. beats the checklist (G5) | consistent = reach at least 0.6 (3 of 5); D1-D6 incl. planted-class gate | stable = found in 6 of 8 runs; five-point rule; bootstrap resamples packages | High |
| C-018 | Wrong-blocker control | Blocking only with grading sentence plus two quotes; gate on wrong blockers; auto-promoted rows MINOR | CB-3 sentence; UNSURE non-blocking; limit +1.0 wrong blockers per run; clean-twin gate | Blind verifier filters; defect without command result becomes a note; limit +1.0 | Medium |
| C-019 | Theory refinements | Numeric evidence tables; rejects reasoning budget; maps A and B to T1-T3 | Splits T2 into T2a/T2b and T3 into T3a/T3b; maps each issue to main and secondary cause | Redefines T2 as "one-axis questions"; rejects reasoning budget | Medium |
| C-020 | Implementation effort | A about 1,300-1,500 lines; B about 700-950 (registry shared) | R1 about 800 lines incl. tests (400+250+30+90+25); R2 about 370 | A about 240 lines; B about 350 | Medium |
| C-021 | Model roles on the three panels | Primary: ember search items, lunas read items; haiku capped at 4 free findings; sonnet takes search items | Primary: ember R,S,U,M; lunas Q,K,X,M; haiku 6 items; sonnet 6 items | Primary: ember mechanical items, lunas reading items; haiku/sonnet replace ember | Medium |
| C-022 | Output-token overhead (ember + 2x luna) | A +26%; B +42% | R1 +28-42%; R2 +25-40% | A about +30%; B about +25% | Low |
| C-023 | Failure-mode coverage | 7 rows A, 7 rows B incl. kills, anchoring on items, dictation-blind classes | 7 rows R1, 6 rows R2 incl. rubber-stamp, lens blind spot | 5 rows A, 5 rows B incl. verifier rejects a true defect, flood | Low |
| C-024 | Broad applicability mechanism | Registry plus target adapters (plan v1, spec and doc v2) and class cards | Extractors keyed to sentence shapes; re-derive section map and edited-object detector | Same helper on any markdown plan; re-derive quantifier words and path rules | Medium |

## Contradictions

Evidence for every row cites the variant text; X-001 and X-002 were also checked against the first brainstorm file `.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` (lines 311-352) and X-004 was recomputed from the variants' own numbers.

| # | Point of Conflict | V1 position | V2 position | V3 position | Impact |
|---|-------------------|-------------|-------------|-------------|--------|
| X-001 | Size of the gain from harness fixes H1-H4 alone (ember + 2x luna, of 14) | "+0.2 to +0.7 ... estimate" (3.0, 3(f)) | "+0.03 to +0.34, central +0.14" citing the first brainstorm bottom-up table | "+0.4 to +0.9 ... Estimate, not measured" (3.1(f)) | High. The source table (merged-requirements.md:342-350) gives total +0.14 (0.03-0.34); H4 contributes 0 on cheap panels. V1 and V3 are unsupported guesses and overstate the harness share by 1.5x to 6x |
| X-002 | Whether the grading rule is changed by the redesign | CB2 rewrites the Medium sentence and adds a missing-requirement rule that can be blocking | "The grading rule itself is unchanged"; CB-3 only restricts when a tool line may become blocking | No rubric change | High. The first brainstorm pins the grading rule and the judge so a rubric change is never mixed with a design effect (merged-requirements.md:320); V1's CB2 mixes them and cannot be separated from the redesign in the arms |
| X-003 | Critical-path cost per item the model must answer | about 1.5-2 s per item (8 items about +12 s; 0.65k tokens about 14 s) | 2 s per item (+3 s start; 8 items = +19 s) | +18 s for 40-60 items per reviewer ("about 40 short lines") | High. 40 lines at about 35 tokens is 1.4k tokens, about 29 s at the 48 tokens/s that V1 derives; V3's +18 s is below even V1's per-item rate for 8 items |
| X-004 | Baseline used for the +35% comparison | b + overhead with b = per-package slowest-reviewer median (100 or 122) | same | Critical path built on luna's own median 102 plus overhead, compared with 122 | High. On a consistent b = 122: A = 6+122+18+3 = 149 s (+22%, not +6%); B = 6+132+2+25+3 = 168 s (+38%, above the 165 s ceiling). On b = 100: B = 146 s (+46%) |
| X-005 | Whether killing a reviewer at 1.35 x baseline is acceptable | Kill at D = floor(1.35 b); a killed reviewer's findings are lost; kill rate must stay at 10% or less | Rejects it: run-to-run spread of one reviewer exceeds 35%, so a kill at 1.35 x median discards 25-40% of reports; uses a 1.6 x deadline and judges +35% on medians | Kill at 165 s (A) or 150 s plus 45 s verifier (B); a killed lens contributes nothing | Medium. The seed brief asks for elapsed arithmetic from medians, not for a kill |
| X-006 | Internal arithmetic of V3's coverage sum and gain | n/a | n/a | Matrix rows sum to 3.5-6.05 (ten issues incl. the control one) but text says 3.6-6.6; "+1.2 to +2.3" gain is a 60% haircut of a nine-issue sum of 2.95-5.25 with no derivation | Medium |
| X-007 | Rate at which ember skips source.md | 39% (81 of 209 valid runs) | 39% | 36% (14 of 39 runs in one package); other places 39% | Low. Different denominators (all valid runs vs one package); the 39% figure is the seed's |
| X-008 | Whether V1 meets +35% by design or by kill | Expected +15%; modelled worst +36% (A) and +42% on b = 100, "kill-limited" | Tightest cell 128 s vs cap 135 s (+28%), no kill needed for the stated cell | n/a | Medium. V1's own worst case exceeds the cap and relies on a kill that discards findings |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Class registry (card schema: definition, recipe, question template, extractor, route, replicas, instances, known weakness) and target adapter interface (task, criterion, constraint, dictated text, edit target, gate); new class = one card | High |
| U-002 | V1 | Telemetry keys `class` and `probe` on findings lines (unknown keys are accepted silently per the hand-off table, HO2:346) and a per-class yield table | Medium |
| U-003 | V1 | Deterministic quote verifier: demote PROBLEM rows whose quotes are not substrings; promote PROBLEM rows with no findings line to a MINOR non-blocking finding | High |
| U-004 | V1 | Arm A4: one-paragraph generic checklist control, and gate G5 (must beat the checklist or the machinery is not justified) | High |
| U-005 | V1 | Documentation arm: delivered documents reviewed at the commit before the fix; ground truth from recorded retry findings | Medium |
| U-006 | V1 | Extractors E1-E7 with a named blind spot each; E6 labelled experimental | High |
| U-007 | V1 | Second ember session in idle time, launched only if the first ended before 0.45 x D | Medium |
| U-008 | V1 | Stage 2: winning redesign on haiku + 2x luna and sonnet + 2x luna | Medium |
| U-009 | V2 | Issue-to-cause map (main and secondary theory per issue; T2a/T2b, T3a/T3b split) | Medium |
| U-010 | V2 | Option to build the sheet while reviewers do their first reads, taking the pre-pass off the critical path | High |
| U-011 | V2 | Items shuffled per reviewer and each item judged by two blind reviewers; cap 12 | Medium |
| U-012 | V2 | Planted-defect documents (one defect per class, written by an author who has not seen the recipes) and clean twins for the false-positive rate | High |
| U-013 | V2 | Placebo arm P: class names only, no recipe, no sheet | Medium |
| U-014 | V2 | Swap test for every template (still correct after domain nouns are replaced), second-author review, 8-word shingle check | Medium |
| U-015 | V2 | Z0-raw arm to measure the harness share and replace the +0.14 estimate; act-rate readout replaces planning probabilities | Medium |
| U-016 | V2 | Ledger audit: the "what you ran" field cross-checked against transcript tool calls; empty sheet equals baseline brief (hash test) | Medium |
| U-017 | V2 | Resume re-ask only when `now + 30 s <= 1.35 x baseline`, once per reviewer | Low |
| U-018 | V3 | Blind verifier stage: only the claim, anchor and evidence; cannot add claims; unverified claims go to follow-up candidates, never blockers | High |
| U-019 | V3 | Deterministic union of claims by anchor overlap (12 characters after whitespace flattening) and seeded item-order shuffle with the seed logged | Medium |
| U-020 | V3 | Parse the coverage block with a real parser (the current block-OK check only tests the fence opener, HO2:209) | Medium |
| U-021 | V3 | Byte-identical determinism test, item cap with dropped count, arm manifest with sandbox hash | Medium |
| U-022 | V3 | Stable-hit rate and a bootstrap that resamples packages, not runs | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | "Reach probability" is the chance that a reviewer writes a finding that survives the merge (anchor and claim limits) and that the blind judge credits as that issue. The three coverage matrices multiply a trigger by a model act rate but never separate the judge-credit and merge-survival factors | All three coverage matrices (C-013) | UNSTATED | High (all gain ranges depend on it) | Promoted |
| A-002 | Per-issue probabilities can be added into an expected issues-found figure (no interference between items competing for one reviewer's attention beyond a flat displacement of 0.1-0.4) | C-012 totals in all three variants | UNSTATED | High | Promoted |
| A-003 | Harness-share and redesign-share gains are additive or nearly so (V1 notes 0.1 overlap; V3 says not additive) | C-011, C-012 | STATED | Medium | Documented |
| A-004 | A pre-implementation sandbox exists for each target and a whole-tree text search over it finishes inside the 6-8 s pre-pass budget (the repository holds thousands of files under `.dev/`) | C-001, C-008, C-009 | UNSTATED | High (state/guard: a missing snapshot or a slow search silently changes which items exist) | Promoted |
| A-005 | Cheap reviewers will complete the item list or ledger honestly instead of rubber-stamping OK, at the stated token cost | C-001, C-002 | STATED (failure-mode rows in all three) | High | Documented |
| A-006 | A finding graded MINOR or non-blocking still counts as "found" for the study's score and for the 1.83 baseline | C-005, C-007 | UNSTATED | Medium (the study credits I7 finds that were all non-blocking, but the loop verdict depends on blocking) | Promoted |
| A-007 | Per-package baseline medians (100-122 s) are stable enough over the experiment to judge +35%; arms run in randomised blocks | C-009, C-010 | STATED (V2 block randomisation) | Medium | Documented |
| A-008 | The eight classes are representative of defects other review targets contain, although all material is one repository | C-014, C-024 | STATED (caveat in all three) | Medium | Documented |
| A-009 | Each extra item costs about 2 s or less of critical-path time | C-010, X-003 | CONTRADICTED by V3's own token counts and V1/V2's per-item rate | High | Flagged for debate |

## Summary
- Total structural differences: 5
- Total content differences: 24
- Total contradictions: 8
- Total unique contributions: 22
- Total shared assumptions surfaced: 9 (UNSTATED: 4, STATED: 4, CONTRADICTED: 1)
- Highest-severity items: C-001, C-002, C-003, C-007, C-010, C-011, C-015, C-016, C-017, X-001, X-002, X-003, X-004, A-001, A-002, A-004, A-009
- Similarity check: differences far exceed 10% of comparable items; debate proceeds.
