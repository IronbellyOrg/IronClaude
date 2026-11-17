# Base Selection Scoring, Pass 2 (reverse order: Variant B then Variant A), slot C-09 panel-resolution-and-tier-source

Scorer: pass 2, neutral. Variant A = `variant-1-original.md` (Proposal A). Variant B = `variant-2-original.md` (Proposal B). Both scored as written; the debate (`debate-transcript.md`, `diff-analysis.md`, `invariant-probe.md`) is used only as evidence for correctness verdicts. Method: `sc-adversarial-protocol/refs/scoring-protocol.md` A.1 to A.5, template `artifact-templates.md` Section 3.

## Requirements used (derived from row C-09 of `undecidable-conflicts.md`)

The source has no formal requirement IDs (protocol edge case: topic matching). Row C-09 gives an A-position, a B-position and a tension list. I split them into 13 requirements. A variant "matches" a requirement when its text states or answers that point (fuzzy keyword match, 3+ consecutive words, or the same point in other words). S-numbers below are the section numbers of each variant.

| # | Requirement (source text of C-09) | Variant B match (evidence) | Variant A match (evidence) |
|---|---|---|---|
| R1 | A-claim: one package-owned tier file is the single source | yes: S2 item 1 "Nothing in the packaged file is called the single source of membership" (rejects it, states what the file keeps) | yes: S1 "the package owns the tier data ... the one file" |
| R2 | A-claim: that file carries `classes`, launch map and vendor | yes: S2 item 6 "Class and vendor: the tier file `classes` stays the owner"; S1 keeps `launch` data | yes: S2.1 table (class, vendor via `vendors` map, launch) |
| R3 | A-claim: checked against `ccsession-models.json` slot lists | yes: S2 item 2 "derive-and-compare check replaces the count check" | yes: S3.1 item 4, S5.2 "Extend `_assert_tiers_match_ccsession_slots` to all six tiers" |
| R4 | A-claim: E2 ladder derived from the tier file | NO: no "ladder" anywhere in the text (grep, 0 hits); E10 discusses an E2 panel shape, not the ladder | yes: S2.1 last row, S3.4 "The ladder and the three tier-list copies" |
| R5 | A-claim: strict distinctness default, a shortfall fails loudly | yes: S2 item 4, S3 E4, S7 answer (2) ("fails loudly" needs a new raise rule) | yes: S2.3 (strict default, `expected`, `shortfall`, exit rule) |
| R6 | A-claim: ember is added by a data edit | yes: S2 last bullet, S3 E6, S4 "Cross-repo ordering" | yes: S2.4 "Ember is a data edit" |
| R7 | B-claim: `ccsession-models.json` and the Coder env are the source, the package file derived | yes: S1, S2 item 1 | yes (as the opposing position): S3.1 items 1 to 3, S7 objection answered |
| R8 | B-claim: soft distinctness stays the default for availability | yes: S1, S2 item 4, S3 E4, E5 | yes (as the opposing position): S7 answer 2 and 4 (default may become per-profile soft) |
| R9 | Tension: ownership across the repo and the Coder env (outside the repo) | yes: S3 E1, E2, S4 "Cross-repo ordering" | yes: S2.1 table row "model id behind a slot", S3.1 item 3 |
| R10 | Tension: three class vocabularies | yes: S2 item 6 (test over `classes`, `_vendor_from_model_id`, SKILL.md set; "No vocabulary is merged") | yes: S3.2 "Three class vocabularies exist" |
| R11 | Tension: tests pin soft distinctness as intended | yes: S3 E5 | yes: S3.3 first bullet, S4.2 |
| R12 | Tension: availability versus diversity | yes: S3 E4 table, S7 | yes: S3.3 table, S4.2 "Availability" |
| R13 | Tension: ember's slot and gateway status open | yes: S3 E6 ("slot 02 or slot 04 ... is open"), shim "[UNVERIFIED]" | yes: S2.4, S3.5 ("Whether the gateway serves `muse-ember-1.0` today ... [UNVERIFIED]") |

Matched: Variant B 12 of 13 (misses R4). Variant A 13 of 13.

## Quantitative Scoring (50% weight)

### Computation (re-derivable)

Commands run on the two files (read-only `grep`): tags = `grep -oE '\[(CODE-VERIFIED|OBSERVED-RUNTIME|CODE-CONTRADICTED|UNVERIFIED)[^]]*\]' | wc -l`; H2 = `grep -c '^## '`; vague tokens = `grep -oiE 'appropriate|as needed|properly|adequate|should consider|might|various|etc\.|best practices|industry standard'`; substantive lines = non-blank, non-heading, non-table-separator, non-`Status:` lines; concrete lines = substantive lines that hold a digit or a backticked identifier.

| Quantity | Variant B | Variant A |
|---|---|---|
| Matched requirements / 13 | 12 / 13 | 13 / 13 |
| Scorable claims (each verification-tagged claim is one claim) | 34 | 35 |
| Internal contradictions found | 2 (see below) | 2 (see below) |
| Substantive lines | 61 | 86 |
| Concrete lines (digit or backticked identifier, no vague token) | 56 | 80 |
| Vague tokens | 0 | 0 |
| Internal references (external ones such as `r04`/`R04` sections, `MODEL-TIERS.md section 1`, the experiment "E2 harness" are excluded) | 14 | 18 |
| Internal references that resolve | 14 | 16 |
| H2 sections | 8 | 8 |

Contradictions (opposing claims about one subject, from the text itself):
- B-1: S7 answer (1) says "The repeat is not silent under B: `distinct_models` and `requested_slots` are written into the resolution", but S2 item 5 says the keys are "written only when a profile or flag asks" and S5 item 2 says "the spec profile resolves soft and records neither key", so the one soft consumer repeats silently (diff-analysis X-001; B conceded the text in the debate).
- B-2: S1 calls the packaged `aliases.<tier>.models` "a snapshot" and the file "a consumer", but S2 last bullet makes ember enter by a slot edit plus `classes`/`names` entries and a golden, never naming the edit to the packaged list that `resolve` reads (`panel.py:615-616`, `tiers["aliases"][slot["tier"]]`, checked) and that the check of S2 item 2 needs (X-005; B conceded).
- A-1: S1 says the package file is "the one file" that owns membership ("single source"), but S2.1 row "model id behind a slot" leaves the Coder env as owner, S3.1 item 3 shows the env and the repo already disagree, and S5.1 M3 says A is wrong on "the single-source claim" if the env changes faster than releases (X-006; A conceded "single source" was an overclaim).
- A-2: S2.2 says "its panel does not change by the default flip", but S4.2 says the flip "changes the spec loop's anthropic-only panel from 4 reviewers to as few as 2" and the installed prompt copy can lag; S5.2 names no prompt edit or test (X-007; A conceded).

Reference resolution, A (18 internal refs): 16 resolve. Unresolved, both checked in the file: S2.3 item 4 "(see 3.4)": the scarcest-tier-first order is defined in 3.3 (line 92), 3.4 is the ladder section; S5.2 last bullet "(5.1 above lists why)": the reasons for the golden regeneration are in 4.2, 5.1 does not list them. Reference resolution, B (14): E3, E4 (x5), E6, E8 (x2), E9 (x2), "section 2 item 5" and the two "section 3" pointers all resolve to an existing definition.

### Quantitative table

| Metric | Weight | Variant B (variant-2-original) | Variant A (variant-1-original) |
|---|---|---|---|
| requirement_coverage | 0.30 | 0.923 (12/13) | 1.000 (13/13) |
| internal_consistency | 0.25 | 0.941 (1 - 2/34) | 0.943 (1 - 2/35) |
| specificity_ratio | 0.15 | 0.918 (56/61) | 0.930 (80/86) |
| dependency_completeness | 0.15 | 1.000 (14/14) | 0.889 (16/18) |
| section_coverage | 0.15 | 1.000 (8/8) | 1.000 (8/8) |
| **quant_score** | | **0.9499** (0.2769 + 0.2353 + 0.1377 + 0.1500 + 0.1500) | **0.9586** (0.3000 + 0.2357 + 0.1395 + 0.1333 + 0.1500) |

Note on SR: the table formula of A.1 (concrete / total substantive) is used. The detail formula (concrete / (concrete + vague)) gives 1.000 for both because neither text holds a vague token; it would raise both and change no order.

## Qualitative Scoring (50% weight), additive binary rubric, evaluated B first then A

Each row is one CEV record: CLAIM = the criterion stated as met in that variant; EVIDENCE = quote or section ref (or "No evidence found, searched ..."); VERDICT = MET or NOT MET. Columns are ordered B then A (pass-2 order). Debate verdicts were used only to judge Correctness and Invariant rows (a claim the debate showed wrong or that its author conceded counts against that variant).

### Completeness (5 criteria)

| Criterion | Variant B | Evidence (B) | Variant A | Evidence (A) |
|---|---|---|---|---|
| C1 Covers all explicit requirements | NOT MET | 12 of 13 requirements; R4 (E2 ladder derived from the tier file) has no evidence: searched S1 to S8, 0 hits for "ladder". | MET | 13 of 13 (requirements table); all required common sections present (S1 position, S2 design, S3 evidence, S4 invariants, S5 tests, S6 PR and rf-qa, S7 objection). |
| C2 Addresses edge cases and failure scenarios | MET | S3 E4: "in anthropic-only ... strict leaves two reviewers"; E9 "(a) Locating `ccsession-models.json` from package code ... UNVERIFIED"; E6 "a missing slot fails loudly (`models.py:669`)". | MET | S3.3 table (anthropic-only 40 of 40 strict short, "Max skipped 5"); S4.2 "an installed copy of the prompt that lags the package leaves the old call in place". |
| C3 Includes dependencies and prerequisites | MET | S2 last bullet "after the Coder `defaults.sh` carries the matching slot"; S8 "Dependence on the adjudicated slots C-01, C-02 and C-03". | MET | S0 "Consistency with the three adjudicated slots"; S2.4 "add the env slot in Coder first, because ccsession stops when a listed slot is not set". |
| C4 Defines success or completion criteria | MET | S5 item 1 "B is wrong about the value of this layer if it never fails across the next several tier edits"; item 2 "Pins that must pass unmodified" list. | MET | S5.1 M1 "A is wrong on the default if declared-repeat or soft panels beat strict panels ... it is right if strict is not worse"; S5.2 tests. |
| C5 Specifies what is out of scope | MET | S8 "Not addressed here, by design: the launch mechanism (C-07), served-model capture (C-08), the choice of E2 panels, and any change to the reflect profile ceiling." | MET | S0 "A does not decide clearing ... A does not decide the merge-side half"; S2.1 launch "slot C-07's decision"; S6 "A does not provide [a launcher]". |
| **Subtotal** | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant B | Evidence (B) | Variant A | Evidence (A) |
|---|---|---|---|---|
| K1 No factual errors or hallucinated claims | NOT MET | Debate showed or B conceded: S7 (2) "'fails loudly' requires a new raise rule that makes the default panel unresolvable" overstated (X-003: strict anthropic-only resolves 2 reviewers, 2 is not below `min(2, requested)`); S7 (1) "The repeat is not silent under B" conceded (X-001); packaged file called "a consumer" though `resolve` reads it (X-005, 78% to A). Counts and line cites checked true (`panel.py:700-706`). | NOT MET | A conceded "single source" was an overclaim (X-006) and that the spec loop's panel does change (X-007); S2.3 item 3 exit rule never fires in anthropic-only (X-003); S2.3 item 4 scarcest-first key `len(models)` changes anthropic-only strict picks in 1000 of 1000 runs (INV-012, reproduced); "a re-review expects 1" ignores `apply_to` (INV-010). Counts and line cites checked true. |
| K2 Technical approaches are feasible with stated constraints | MET | S2 item 2 derive-and-compare: probe INV-006 parsed `MODEL-TIERS.md:38-46`, all six tiers equal; S2 item 5 additive keys leave byte-identity golden alone (E5). Caveat: `distinctness` profile field and the overlay are unbuilt (V-5, E9) but marked optional or weakest. | MET | S3.3 scarcest-first measured 0 skipped in 40 of 40 gateway runs, reproduced by diff-analysis V-1; strict flip cost stated (4.2 "rewritten" pins). Caveat: sort key and strict default drawbacks above. |
| K3 Terminology used consistently and accurately | NOT MET | "E2" names both the experiment (S2 "E2 harness", E6, E10 "E2 recommends", S8 "choice of E2 panels", S5.4 "neither E1 nor E2") and B's own evidence item E2 (S3, S5.3 "(E4)"/"E1, E2" pointers) in one document; "consumer" and "snapshot" for the file `resolve` reads. | MET | One vocabulary: "tier file", "strict/soft", `expected`/`shortfall`; "E2" always means the experiment; tags defined in "Citation form". Minor: "single source" vs "owns" is scored under K4, not here. |
| K4 No internal contradictions (cross-validated with IC) | NOT MET | B-1 (S7 (1) vs S2 item 5 / S5 item 2) and B-2 (S1 "snapshot" vs S2 ember path); IC = 0.941. | NOT MET | A-1 (S1 "the one file" vs S2.1 env owner / S5.1 M3) and A-2 (S2.2 vs S4.2); IC = 0.943. |
| K5 Claims supported by evidence or rationale | MET | S3 E1 to E10 with `path:line` cites and tags (34 tagged claims); unverifiable items marked "[UNVERIFIED by me]" (E6, E8, E10). | MET | S3.1 to S3.5 with `path:line` cites and tags (35 tagged claims); S3.5 lists what could not be verified. |
| **Subtotal** | **2/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | Variant B | Evidence (B) | Variant A | Evidence (A) |
|---|---|---|---|---|
| S1 Logical section ordering (prerequisites before dependents) | NOT MET | S8 "Dependence on the adjudicated slots C-01, C-02 and C-03" comes last, but S2 item 1 and the "C-01's adjudicated hybrid keeps it shared" statement depend on it earlier. | MET | S0 "Consistency with the three adjudicated slots" precedes S1 position; then design, evidence, invariants, tests, effects, objection. |
| S2 Consistent hierarchy depth (no orphans) | MET | 8 H2 sections, flat numbered lists, no H3 at all (`grep '^### '` 0 hits). | MET | H3 only under S2 (4), S3 (5), S4 (2), S5 (2); no single-child subsection. |
| S3 Clear separation of concerns | MET | S2 design, S3 pure evidence E1 to E10, S4 invariants, S5 tests; overlay design stays in S2. | NOT MET | Design proposals sit inside the evidence section: S3.3 introduces the scarcest-first order, S3.4 "Under A, detection stays a function of the env but reads a named list of marker variables (design inference)". |
| S4 Navigation aids | MET | Labels E1 to E10 cited from S4/S5/S6/S7 ("(section 3, E9)"); tag legend line 8. | MET | Numbered sections with pointers ("see 2.3", "(3.1 item 4)"), M1 to M3 labels, "Citation form" legend. |
| S5 Follows conventions of the artifact type | MET | All required common sections in order, "Status: Complete" at both ends. | MET | Same required sections plus S0; "Status: Complete" at both ends. |
| **Subtotal** | **4/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | Variant B | Evidence (B) | Variant A | Evidence (A) |
|---|---|---|---|---|
| L1 Unambiguous language | MET | `grep` for appropriate / as needed / properly / adequate / should consider / might / various / etc. / best practices: 0 hits. | MET | Same grep: 0 hits. |
| L2 Concrete rather than abstract | MET | Specific edits named (S2 items 1 to 6), counts "18 of 40", "always 2", line cites. | MET | Specific edits named (S2.1 table, S2.3 items 1 to 4, S2.4 edit list), counts "30 of 40", "0 of 40". |
| L3 Each section has a clear purpose or one-sentence summary | MET | Section titles state purpose ("Strongest objection and the answer"; "Dependence on the adjudicated slots"). | MET | Section titles state purpose; S2.1 to S2.4 each one topic. |
| L4 Acronyms and domain terms defined on first use | NOT MET | Defines `r04`, `r17`, tags; does not define "E2", "INV-A to INV-N", "GQ-046", "CO-14", "DR-014", "FX-15" (header cites "synth-06 6.12.0" only). | NOT MET | Defines `R<NN>` and tags; does not define "INV-I", "GQ-050 / Q-5", "OQ-10", "DATA-11", "CO-13", "VL-23-232" on first use. |
| L5 Actionable next steps or decision points | MET | S5 items 1 to 5 (tests, measurement per template and env that "decides the availability side"). | MET | S5.1 M1 to M3, S5.2 tests, S7 item 5 "who owns the tier file ... is an owner question". |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant B | Evidence (B) | Variant A | Evidence (A) |
|---|---|---|---|---|
| R1 At least 3 risks with probability and impact | NOT MET | S4 "Endangered or conditioned" lists 4 items (derive-check fragility, reproducibility, cross-repo ordering, DR-014) with impact but no probability; only E4 gives frequencies and those concern the strict default B rejects. | MET | S4.2: spec loop 4 to "as few as 2" reviewers (default flip certain, prompt lag window); INV-L parity "not proven" for every existing shadow run; availability "40 of 40" anthropic-only; golden regeneration. |
| R2 Mitigation for each identified risk | MET | Fragility "breaks loudly, which is the intended direction"; overlay records `tiers_source`; cross-repo order: Coder slot first (S2 last bullet); DR-014 visible through `distinct_models`. | NOT MET | S4.2 INV-L: "degrades the parity evidence ... by design of that script", no mitigation; availability loss accepted ("loss of coverage by design"). |
| R3 Failure modes and recovery procedures | MET | E6 "a missing slot fails loudly (`models.py:669`)"; S2 ember: slot, then `classes`/`names`, then regenerate golden; fixed anchor raises (E4). | MET | S2.3 item 3 fixed-anchor exhaustion fatal; S2.4 order of operations; S4.2 "pin ... rewritten with the change". |
| R4 External dependencies and their failure scenarios | MET | E1/E2 live-fetched JSON and Coder env; E9 (b) shim skips by window or cooling; ember gateway status UNVERIFIED. | MET | S3.1 item 2 live fetch stops a workspace lacking the slot; S3.1 item 3 env absent on laptop or CI; S3.5 gateway serving ember UNVERIFIED. |
| R5 Monitoring or validation mechanism for risk detection | MET | S5 item 1 derive-and-compare test with mutation case; `tiers_sha256` and `tiers_source` as detectors; S5 item 3 rerunnable E4 script. | MET | S5.1 M2 shortfall rate over `run1..run1000`; M3 drift measured against live ccsession file and env; S5.2 tests. |
| **Subtotal** | **4/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant B | Evidence (B) | Variant A | Evidence (A) |
|---|---|---|---|---|
| I1 Boundary conditions for collections (empty, single, maximum) | MET | E4 "a non-fixed slot with no candidate is skipped, not failed ... only the fixed anchor raises"; S2 item 2 "Tier0 is not packaged and is skipped"; anthropic-only "always 2". | MET | S2.3 / S0 "exactly one fixed anchor is mandatory (`panel.py:245-246`) ... never empty"; S3.3 "four distinct Anthropic ids for seven slots"; "Re-review is unaffected". |
| I2 State variable interactions across component boundaries | MET | E1/E2 env + ccsession + package; S2 item 3 `select_env` reads `$T3Model01`; E9 (c) per-workspace `tiers_sha256`. | MET | S3.1 item 3 env `T3Model01..06` vs repo two tier-3 models; S4.2 INV-L "`tiers_sha256` ... old run 'not proven'"; "adding an id to `tier4` changes the pool of a random slot". |
| I3 Guard condition gaps | MET | E3 "the existing drift guard is count-only" (tier1a, 1b, 2 unchecked); E4 "a skipped slot is not an error"; S2 item 6 test that every `classes` id maps to a vendor. | MET | S3.1 item 4 "covers 3 of the 6 tiers by count and 2 first-model names"; S3.2 reflect profile refuses a model with no `classes` (`panel.py:124-125`). |
| I4 Count divergence | MET | S2 item 5 `requested_slots` (4 for `default`, 7 for `live7`) vs `len(reviewers)`; S2 item 2 length vs `len(models_env)`. | MET | S2.3 item 2 `expected` and `shortfall = expected - len(reviewers)`; S3.1 item 4 lengths 2, 3, 6, 4, 2, 3 vs `models_env`. (Its "re-review expects 1" is scored under K1.) |
| I5 Interaction effects when components combine | MET | S6 strict default plus lens-per-reviewer rf-qa "cannot resolve all lenses"; E5 CLI default change plus golden pins; soft spec loop plus strict reflect profile. | MET | S4.2 strict flip plus unedited loop prompt lag; S4.1 vendor lookup plus single-vendor degrade (exit 11); S3.3 strict plus slot order. |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant B | Variant A |
|---|---|---|
| Completeness | 4/5 | 5/5 |
| Correctness | 2/5 | 3/5 |
| Structure | 4/5 | 4/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **23/30 = 0.7667** | **25/30 = 0.8333** |

Verdict count over the 30 criteria: Variant B 23 MET and 7 NOT MET; Variant A 25 MET and 5 NOT MET.

## Edge Case Floor Check

Floor: Invariant & Edge Case Coverage must be at least 1/5.

| Variant | Invariant & Edge Case score | Eligible as base |
|---|---|---|
| B | 5/5 | yes |
| A | 5/5 | yes |

## Position-Bias Mitigation

This file is pass 2 only (reverse order, B then A). Pass 1 (input order) is scored independently by another scorer and was not read, so no per-criterion reconciliation is done here. Criteria I judge most likely to differ from an input-order pass, so a reconciliation should look at them first:

| Criterion | Variant | Pass 2 verdict | Why it is close |
|---|---|---|---|
| K1 No factual errors | A, B | NOT MET, NOT MET | Both hold verified counts and line cites; the failures are conceded or debate-refuted design overclaims (A: "single source", spec loop unchanged; B: "unresolvable", "repeat is not silent"). |
| K2 Feasible with stated constraints | A, B | MET, MET | Core moves verified; strict default (A) and `distinctness` field plus overlay (B) are the weak parts. |
| K3 Terminology consistent | B | NOT MET | The "E2" collision between the experiment and B's evidence item E2. |
| S3 Separation of concerns | A | NOT MET | Design inside S3.3 and S3.4; B keeps design in S2. |
| R1 Risks with probability and impact | B | NOT MET | B names impacts, gives probability only for the strict default it rejects. |
| R2 Mitigation for each risk | A | NOT MET | INV-L parity loss and availability loss are accepted with no mitigation. |
| L4 Acronyms defined | A, B | NOT MET, NOT MET | Project codes (INV-x, GQ-x, CO-x) are used undefined by both. |

Disagreements re-evaluated: not applicable (single pass). Final verdicts changed: 0.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate tiebreaker input (pure wins of 25 diff points, `debate-transcript.md` Scoring Matrix) |
|---|---|---|---|---|
| B (variant-2-original) | 0.4750 (0.9499) | 0.3833 (23/30 = 0.7667) | **0.8583** | 6 pure wins (C-002, C-003, C-006, C-009, X-006, X-007) = 24% |
| A (variant-1-original) | 0.4793 (0.9586) | 0.4167 (25/30 = 0.8333) | **0.8960** | 2 pure wins (C-010, X-005; C-007 contested) = 8% |

**Margin**: 0.0377 = 3.8 points, below the 5% threshold. A leads on raw score.
**Tiebreaker applied**: Yes (protocol A.4). Step 1, debate performance: B won 6 pure diff points to A's 2 (9 hybrids, 8 neither or qualify), so under the protocol Variant B is selected as base. Step 2 (Correctness criteria count: A 3, B 2, which would favor A) is not reached because the debate step is not tied.

Reading of the result for the lead: on raw score Variant A is ahead by 0.038 (it covers all 13 requirements and scores 5/5 on Completeness and 3/5 on Correctness, against B's 4/5 and 2/5; B leads only on dependency completeness, 1.000 against A's 0.889 from two mis-pointed section references). The margin sits inside the 5% band, so the protocol tiebreaker, not the raw score, decides the base: Variant B by debate performance. Both variants pass the Edge Case Floor (5/5 each). The 30-criterion verdict counts are B 23 MET, A 25 MET.
