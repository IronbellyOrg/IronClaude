# Base Selection Report

Variant A = Variant 1 = Proposal A (`variant-1-original.md`). Variant B = Variant 2 = Proposal B (`variant-2-original.md`). Both are position papers scored AS WRITTEN (not the debate's hybrid). The "requirements" are those of conflict row C-09 of `undecidable-conflicts.md` (no formal requirement IDs exist, so the protocol's edge case applies: topic matching). Scoring passes: `scorer-pass1.md` (input order A, B), `scorer-pass2.md` (reverse order B, A), `scorer-reeval.md` (re-evaluation of the 6 disagreements; its verdicts are final). The full 30-row CEV tables per pass are in the two pass files; the table below carries the final verdict and the decisive evidence per criterion.

## Quantitative Scoring (50% weight)

The two scorers counted claim units, contradictions, specificity lines and internal references independently by reading, with different unit definitions (pass 1: 20 derived requirements, 75 / 53 claim units; pass 2: 13 derived requirements, 35 / 34 tagged claims). The protocol asks for deterministic metrics; the two passes agree on every ranking and differ by at most 0.0068 on any score, so the reported `quant_score` is the mean of the two passes, with both shown.

| Metric | Weight | Variant A (Proposal A) pass 1 / pass 2 | Variant B (Proposal B) pass 1 / pass 2 |
|--------|--------|------------------------------------------|------------------------------------------|
| requirement_coverage | 0.30 | 1.0000 (20/20) / 1.0000 (13/13) | 0.9500 (19/20) / 0.9231 (12/13); both passes: the E2 fallback ladder is absent from B |
| internal_consistency | 0.25 | 0.9600 (1 - 3/75) / 0.9429 (1 - 2/35) | 0.9434 (1 - 3/53) / 0.9412 (1 - 2/34) |
| specificity_ratio | 0.15 | 0.9333 (70/75) / 0.9302 (80/86) | 0.9057 (48/53) / 0.9180 (56/61) |
| dependency_completeness | 0.15 | 0.8824 (15/17) / 0.8889 (16/18); two mis-pointed references: A 2.3 item 4 "(see 3.4)" and 5.2 "(5.1 above lists why)" | 1.0000 (12/12) / 1.0000 (14/14) |
| section_coverage | 0.15 | 1.0000 (8/8) / 1.0000 (8/8) | 1.0000 (8/8) / 1.0000 (8/8) |
| quant_score per pass | | 0.9624 / 0.9586 | 0.9567 / 0.9499 |
| **quant_score (mean of passes)** | | **0.9605** | **0.9533** |

Intra-variant contradictions found by both scorers (each also conceded in the debate): A: "single source" versus env as owner of the served model (X-006), "spec loop panel does not change" versus "changes from 4 to 2" (X-007), and a loud exit that never fires in anthropic-only (X-003). B: "the repeat is not silent" versus keys written only on request (X-001), "snapshot" versus an ember path that omits the packaged-list edit (X-005), and "unresolvable" versus its own "always 2 reviewers" table (X-003).

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts after position-bias re-evaluation. Evidence is the decisive CEV evidence; the complete CLAIM / EVIDENCE / VERDICT rows are in the pass files.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| C1 Covers all explicit requirements | MET | All derived requirements matched, including A 2.1 last row "E2 fallback ladder ... a pure function of the tier lists" | NOT MET | The A-claim "E2 ladder derived from the tier file" has no passage in B (both passes: 0 hits for ladder/FALLBACK) |
| C2 Edge cases and failure scenarios | MET | 3.3 table "Max skipped 5"; 2.3 item 3 fixed-anchor exhaustion stays fatal | MET | E4 "strict leaves two reviewers"; E6 "a missing slot fails loudly (`models.py:669`)" |
| C3 Dependencies and prerequisites | MET | Section 0 on C-01..C-03; 2.4 "add the env slot in Coder first" | MET | Section 8 dependence on C-01..C-03; E6 "after the Coder `defaults.sh` carries the matching slot" |
| C4 Success / completion criteria | MET | 5.1 M1 "A is wrong on the default if ... it is right if strict is not worse" | MET | Section 5 item 1 red/green conditions; item 4 "B is wrong if distinct-served panels find materially more blocking items" |
| C5 Out of scope | MET | Section 0 "A does not decide clearing"; section 6 launcher; 7.5 | MET | Section 8 "Not addressed here, by design: the launch mechanism (C-07), served-model capture (C-08) ..." |
| **Subtotal** | **5/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| K1 No factual errors or hallucinated claims | NOT MET | Conceded or refuted in the debate: "its panel does not change" (2.2), "data edit ... not a code change" with `test_ccsession_tiers.py:222` omitted, "single source", `len(models)` sort key changes anthropic-only strict picks in 1000 of 1000 runs (INV-012), "a re-review expects 1" ignores `apply_to` (INV-010) | NOT MET | Conceded or refuted: "The repeat is not silent under B" (X-001), "unresolvable" (X-003), packaged file "a consumer" though `resolve` reads it (`panel.py:615`, X-005) |
| K2 Technical approaches feasible with stated constraints | MET (re-eval; pass 1 NOT MET, pass 2 MET) | Strict default, vendor lookup and scarcest-first are buildable and A prices the cost (4.2 "I do not call that 'pins unmodified'"; 3.3 "0 skipped slots in 40 of 40"); the contradiction belongs to K4 | MET | Derive-and-compare green today for six tiers; additive keys keep the byte-identity golden |
| K3 Terminology consistent and accurate | MET (re-eval; pass 1 NOT MET, pass 2 MET) | Terms scoped explicitly ("the Coder env stays the runtime owner of which model each slot serves"); "single source" is an overclaim (K1/K4), not a term with two meanings | NOT MET (re-eval; pass 1 MET, pass 2 NOT MET) | "E2" names both B's own evidence item ("E2. `ccsession-models.json` reaches workspaces") and the E2 experiment ("neither E1 nor E2 used", section 5 item 4) |
| K4 No internal contradictions | NOT MET | IC found X-006, X-007, X-003 inside A | NOT MET | IC found X-001, X-005, X-003 inside B |
| K5 Claims supported by evidence or rationale | MET | Tagged evidence throughout; counts reproduced (diff V-1) | MET | E1-E10 with line cites; unverified items tagged |
| **Subtotal** | **3/5** | | **2/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| S1 Logical section ordering | MET | Section 0 (adjudicated-slot consistency) precedes position, design, evidence | NOT MET | Adjudicated-slot dependence is section 8, after section 2 items 4-5 already build on C-02/C-03 (diff S-001) |
| S2 Consistent hierarchy depth | MET | H3 only under sections 2-5, each with 2+ siblings | MET | 8 H2 sections, flat numbered lists |
| S3 Separation of concerns | NOT MET (re-eval; pass 1 MET, pass 2 NOT MET) | Scarcest-first order is first introduced inside evidence (3.3) and the marker-variable list inside 3.4; section 2 never states them | MET | Overlay, derive-and-compare, additive keys defined in section 2 and only evaluated in section 3/E9 |
| S4 Navigation aids | MET | Citation-form legend, numbered cross-references | MET | Legend line 8, E1-E10 cross-referenced |
| S5 Artifact-type conventions | MET | All required common sections, Status markers | MET | All required common sections, Status markers |
| **Subtotal** | **4/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| L1 Unambiguous language | MET | No vague-word hits; design statements labelled "design inference" | MET | No vague-word hits; uncertainty tagged [UNVERIFIED] |
| L2 Concrete rather than abstract | MET | 2.3 items 1-4 name flags, keys, exit behaviour | MET | 2 item 2 names the exact check |
| L3 Section purpose clear | MET | Headings state purpose | MET | Headings state purpose |
| L4 Acronyms defined on first use | NOT MET | "E2", "T1", "GQ-050", "OQ-10", "DATA-11" not expanded | NOT MET | "E2", "CO-14", "GQ-046", "DR-014", "INV-C..INV-N" not expanded |
| L5 Actionable next steps / decision points | MET | M1-M3 each end in an "A is wrong if" rule; 7.5 open owner question | MET | Section 5 red/green conditions; section 8 names C-03 open point 4 |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| RK1 At least 3 risks with probability and impact | MET | 4.2: loop panel "from 4 reviewers to as few as 2", INV-L parity, availability "40 of 40" | MET (re-eval; pass 1 MET, pass 2 NOT MET) | Section 4: four risks with impact and a likelihood handle (E4 rates, per-workspace hash, ordering failure, parser fragility); ruling B NOT MET would require ruling A NOT MET |
| RK2 Mitigation for each identified risk | NOT MET | INV-L "degrades the parity evidence ... by design of that script", nothing else | MET (re-eval; pass 1 NOT MET, pass 2 MET) | Each B risk has a named limiter ("breaks it loudly", `tiers_source`, Coder-slot-first rule, `distinct_models`); none left accepted-with-nothing |
| RK3 Failure modes and recovery | MET | 2.4 Coder slot first; 3.1 item 2 | MET | E6 `models.py:669`; section 4 cross-repo ordering |
| RK4 External dependencies | MET | 3.1 items 1-2; 3.5 | MET | E2, E9 (wheel, shim skipping) |
| RK5 Monitoring / validation mechanism | MET | 5.1 M3 drift measurement; 5.2 tests | MET | Section 5 items 1, 3, 5 |
| **Subtotal** | **4/5** | | **5/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| IE1 Collection boundaries | MET | "A hand-edited empty list stays C-02's open item"; "re-admits the only candidate" pin; four Anthropic ids for seven slots | MET | "Tier0 is not packaged and is skipped"; E4 "strict leaves two reviewers" |
| IE2 State interactions across components | MET | 3.1 item 3 env vs repo; INV-L `tiers_sha256`; tier4 random-slot pool change | MET | `select_env` reads `$T3Model01`; E9(c) per-workspace hash |
| IE3 Guard condition gaps | MET | 3.4 closed key set; `panel.py:124-125` classes guard | MET | E4 skipped slot "is not an error"; FX-14 single-variable detection |
| IE4 Count divergence | MET | `expected`/`shortfall`; list lengths 2,3,6,4,2,3 vs `models_env` | MET | `requested_slots` 4/7 vs `len(reviewers)` 2; length vs `len(models_env)` |
| IE5 Interaction effects | MET | Strict flip + unedited loop prompt lag; vendor lookup + single-vendor degrade | MET | Additive keys + byte-identity golden; strict + C-03 floor; overlay + hash goldens |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 4/5 |
| Correctness | 3/5 | 2/5 |
| Structure | 4/5 | 4/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 5/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.8333** | **24/30 = 0.8000** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case Coverage | Floor (>= 1/5) | Eligible as base |
|---------|-------------------------------|----------------|------------------|
| A | 5/5 | Pass | Yes |
| B | 5/5 | Pass | Yes |

## Position-Bias Mitigation

Pass 1 (input order) scored A 24/30, B 24/30; pass 2 (reverse order) scored A 25/30, B 23/30. They disagreed on 6 of 60 criterion-variant pairs; the other 54 agree.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| K2 Technical approaches feasible | A | NOT MET | MET | DISAGREE | MET |
| K3 Terminology consistent | A | NOT MET | MET | DISAGREE | MET |
| K3 Terminology consistent | B | MET | NOT MET | DISAGREE | NOT MET |
| S3 Separation of concerns | A | MET | NOT MET | DISAGREE | NOT MET |
| RK1 Risks with probability and impact | B | MET | NOT MET | DISAGREE | MET |
| RK2 Mitigation for each risk | B | NOT MET | MET | DISAGREE | MET |

Disagreements re-evaluated: 6 (`scorer-reeval.md`, same standard applied to both variants). Final verdicts equal pass 2 in 5 pairs and pass 1 in 1 pair (B, RK1); relative to pass 1, 5 verdicts changed (A: K2, K3, S3; B: K3, RK2); relative to pass 2, 1 verdict changed (B: RK1).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (Proposal A) | 0.4803 (0.9605 x 0.5) | 0.4167 (0.8333 x 0.5) | **0.8969** | 2 pure wins of 25 points = 8% (C-010, X-005; C-007 contested) |
| B (Proposal B) | 0.4767 (0.9533 x 0.5) | 0.4000 (0.8000 x 0.5) | **0.8767** | 6 pure wins of 25 points = 24% (C-002, C-003, C-006, C-009, X-006, X-007) |

Cross-check of the two raw passes: pass 1 A 0.8812 / B 0.8783 (margin 0.0028); pass 2 A 0.8960 / B 0.8583 (margin 0.0377). The re-evaluated total is A 0.8969 / B 0.8767.

**Margin**: 0.0202 (2.0 points; A ahead on raw score), below the 5% threshold.
**Tiebreaker applied**: Yes, level 1 (debate performance). Variant B won 6 pure diff points to Variant A's 2 (9 points went to the hybrid, 8 to neither or qualify, 1 contested); 24% against 8% is not within 5%, so level 2 (Correctness count: A 3, B 2, which would favour A) is not reached. Even if the contested C-007 is credited to A, B keeps the lead 6 to 3.

## Selected Base: Variant B (Proposal B; `variant-2-original.md`)

### Selection Rationale

The raw score margin (0.0202) is inside the 5% band, so the protocol tiebreaker decides: debate performance, Variant B 6 pure wins against Variant A's 2. Variant A's lead on the raw score comes from the quantitative layer (full requirement coverage, because only A carries the E2 ladder) and from Completeness, partly offset by A's two mis-pointed internal references and by a Structure fault (design elements introduced in its evidence section). The debate shows where the lead of B came from: the ordered derive-and-compare guard (C-002, 90%), soft as the default (C-003, 83%, after A withdrew its strict default), the class and vendor treatment with no `vendors` map (C-006, 80%), the unedited spec loop prompt (C-009, 88%) and A's concessions on "single source" (X-006) and on the loop panel (X-007). A's own advocate withdrew the strict default, `--allow-repeat`, the `vendors` map, the env marker list, the stderr line, the resolve-time exit rule and the loop-prompt edit, so the base text as written carries more to remove than B's does. Both advocates converged on one hybrid (24 of 25 points agreed); Variant B is the base onto which that hybrid is merged.

### Strengths to Preserve from Base (Variant B)

1. The ordered derive-and-compare guard for all six tiers against the `MODEL-TIERS.md` section 1 table and `len(models_env)` (B section 2 item 2, section 5 item 1); adopted by A in Round 2.
2. Soft distinctness stays the default in the resolver and the CLI; `--strict-distinct` stays the opt-in that reflect already passes (`SKILL.md:340`); the shipped soft pins stay green (B section 2 item 4, E5).
3. Additive `requested_slots` and `distinct_models` keys that leave the byte-identity golden alone (B section 2 item 5), now placed in the CLI layer (0 pins; 17 pins if written in the library).
4. No vocabulary merge: one parity test for class and vendor; classes cannot be derived from `ccsession-models.json` (B section 2 item 6).
5. The named weakest layer (the env overlay, E9), dropped by both advocates; the dependence section on C-01..C-03 (B section 8); the served-versus-requested identity caveat (E8).

### Strengths to Incorporate from Non-Base Variants (Variant A)

1. Scarcest-tier-first slot order as the CLI's order, library keyword defaulting to today's order, `reviewers` and `skipped_slots` emitted in emission order, `template_sha256` unchanged (A 3.3, 2.3 item 4, as repaired in A Round 2 item 4); the sort key is the one unresolved point (C-007): A's `len(aliases[tier].models)` against B's servable-candidate count.
2. A's "today versus under A" ownership table as the presentation of the ownership statement (A 2.1), and the merged wording "the reviewed copy `panel resolve` reads, held in step by the guard" (both Round 2 section 6 item 1).
3. The E2 fallback ladder as a pure function of (tier, model) (A 2.1 last row, 3.4): B's one missing requirement; deferred in the debate (concerns the harness, not `panel resolve`).
4. Measurement M1 (soft versus strict versus declared repeat on ground truth) and M3 (drift between sources), and the concession that the strictness default can be judged apart from the ownership claim (A 5.1, 7.4).
5. The ember edit list union (A: packaged `aliases.tier4.models` entry, `classes`, `names`, `T4Model04`; B: `test_ccsession_tiers.py:222`, Coder slot first), plus the Round 2.5 and Round 2 additions: `make sync-dev` and `make verify-sync`, `classes` and `names` in the same change, the `MODEL-TIERS.md` tier 4 row.
6. A's candour items (A 4.2 "I do not call that 'pins unmodified'"; section 0's one exact difference from C-01) and its accounting sentence for INV-L.
