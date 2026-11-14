# Base Selection Report

Variants: V1 = sonnet:architect, V2 = sonnet:analyzer, V3 = haiku:backend. Scoring files: `scoring/quant.py` (deterministic; rerun gives identical output, checked), `scoring/qual-pass1.md`, `scoring/qual-pass2.md`, `scoring/resolved.json`, `scoring/final-qual-table.md`, `scoring/convergence-output.txt`. A first quant run had two regex bugs (a case error that hid the three-theories match in all variants, and a harness-share pattern too narrow for V3's gain table); both were fixed before scoring and the first output is kept as `scoring/quant-run1-regex-bug.json`.

## Quantitative Scoring (50% weight)

The quant layer is a heuristic of regex counts over the artifact text (limits: the metrics reward presence of sections, not correctness; the V1-V2 gap of 0.0036 is within noise, while V3's lower score reflects a missing theory mapping and 8 unresolved references).

| Metric | Weight | V1 (sonnet:architect) | V2 (sonnet:analyzer) | V3 (haiku:backend) |
|--------|--------|-----------------------|----------------------|--------------------|
| requirement_coverage | 0.30 | 1.0000 (28 of 28 seed-brief requirement patterns) | 1.0000 (28 of 28) | 0.9643 (27 of 28; no redesign-to-theory mapping) |
| internal_consistency | 0.25 | 0.9878 (4 contradictions / 327 claims) | 0.9923 (2 / 259) | 0.9713 (6 / 209) |
| specificity_ratio | 0.15 | 0.9968 (310 concrete / 1 vague) | 1.0000 (218 / 0) | 0.9947 (188 / 1) |
| dependency_completeness | 0.15 | 0.9872 (77 of 78 references resolve) | 1.0000 (42 of 42) | 0.8367 (41 of 49) |
| section_coverage | 0.15 | 1.0000 (6 H2 of max 6) | 1.0000 (6 of 6) | 1.0000 (6 of 6) |
| **quant_score** | | **0.9945** | **0.9981** | **0.9568** |

Contradiction counts (the contradictions where the variant sat on the wrong side of a checked fact, from `diff-analysis.md`): V1 X-001, X-002, X-005, X-008; V2 its 1.6 x deadline (X-005) and its own sum of harness and redesign shares in 3(f); V3 X-001, X-003, X-004, X-005, X-006, X-007.

## Qualitative Scoring (50% weight) - Additive Binary Rubric (30 criteria)

Two independent passes (order V1, V2, V3 and reverse order V3, V2, V1) with Claim-Evidence-Verdict tables are in `scoring/qual-pass1.md` and `scoring/qual-pass2.md`. The final table below uses the agreed verdicts and the re-evaluation of the 9 disagreements.

### Completeness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| CO1 covers all seed requirements | MET | Sec 1 theory mapping; (a)-(i) per redesign; sections 5-6 | MET | Sec 4 "Theories answered" row; (a)-(i) per redesign | NOT MET | No redesign-to-theory mapping; idle-time reallocation not assigned |
| CO2 edge cases and failure scenarios | MET | REQ-11 fallback; abort on missing source; NONE FOUND | MET | Empty sheet equals baseline; pre-pass kill at 15 s | MET | Reverse-dependency flood cap 12; verifier kill marks unverified |
| CO3 dependencies and prerequisites | MET | H1-H4 prerequisites; plan sha check flagged UNVERIFIED | MET | H3 is a precondition (R-04); sha comparison first | MET | "Both redesigns depend on harness fixes H1 to H4" |
| CO4 success/completion criteria | MET | Pre-registered gates G1-G7 | MET | Decision rule D1-D6 with outcomes table | MET | Section 4 decision rule, five checks |
| CO5 out of scope stated | MET | Claims-only exchange "out of scope for the first test" | MET | "Out of scope" line; messaging not used; docs set not gated | NOT MET | No out-of-scope statement anywhere |
| **Subtotal** | **5/5** | | **5/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| CR1 no factual errors (arithmetic) | MET | Recomputed 402, 474, 393, 453, 3.4-6.1, 2.8-5.5 correct | NOT MET | RE-EVALUATED (pass1 NOT MET: Stated 128-150 s; table sums to 129-151; 24 vs 25 assignments / pass2 MET: Recomputed: 1.63/3.55, 1.25/3.10, 254 runs, +23%, +18% correct) | NOT MET | Coverage sums 3.6-6.6 recompute to 3.5-6.05; +6% vs +21% |
| CR2 feasible within +35% | MET | Expected +15%/+13%; timeout D; fallback on failure | MET | Expected +23-28%; tightest 128 s vs cap 135 s, mitigation given | NOT MET | +18 s for 60 items vs +30% tokens; timeout 165+6+3 exceeds cap |
| CR3 terminology consistent | NOT MET | RE-EVALUATED (pass1 NOT MET: Hold-out H2/H5 collide with harness H1-H4; arm A3 tests Redesign B / pass2 MET: Class IDs C1-C8, cards, probe, lens used consistently) | NOT MET | RE-EVALUATED (pass1 NOT MET: Hold-out H5/H2 vs fixes H1-H4; step S1 vs extractor S / pass2 MET: Conventions block; C1-C8, ledger, sheet used consistently) | NOT MET | "H4" names two fixes; GT, I and B labels mixed |
| CR4 no internal contradictions | NOT MET | RE-EVALUATED (pass1 MET: None found; worst-case overrun of D acknowledged / pass2 NOT MET: Luna +1.5k tokens at 48 tok/s conflicts with stated +12 s) | NOT MET | R-12 caps critical-path model at 6 items; primary luna gets 8 | NOT MET | Per-package +6% vs aggregate +21% from same table |
| CR5 claims supported | MET | Theory tables cite PAT, DS, AC sections with counts | MET | Theory rows cite PAT sec 1, DS sec 2c counts | MET | Theory table cites investigation sections with run counts |
| **Subtotal** | **3/5** | | **2/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| ST1 logical section ordering | MET | 3.0 scaffolding precedes both redesigns | MET | Shared brief changes precede both redesigns | MET | Order follows seed; shared 3.3 placed after redesigns |
| ST2 consistent hierarchy depth | MET | Identical (a)-(i) headings in 3.1 and 3.2 | MET | Identical bold (a)-(i) in both redesigns | MET | Identical (a)-(i) in 3.1 and 3.2 |
| ST3 separation of concerns | MET | Shared scaffolding 3.0 separate from redesigns | MET | Shared brief changes separate from redesigns | MET | Harness fixes 3.3 separate from A and B |
| ST4 navigation aids | MET | Conventions block; REQ-nn and section cross-references | MET | Conventions block; R-04, R-14, D2 references resolve | NOT MET | No conventions block; "validation run (section 5)" points at requirements |
| ST5 six-section artifact conventions | MET | Six numbered sections matching the seed | MET | Six sections including comparison section 4 | MET | All six parts present; comparison nested as 3.4 |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| CL1 unambiguous language | MET | Exact item JSON, ledger row syntax, testable REQs | MET | Ledger line syntax and numeric caps stated | NOT MET | "Every reviewer answers all" vs "ember takes mechanical items" |
| CL2 concrete not abstract | MET | Quoted CB1-CB4 and eight recipe texts | MET | Quoted recipes R-C1 to R-C8 | MET | Quoted brief and per-class item templates |
| CL3 one purpose per section | MET | Each of six sections has one purpose | MET | Each of six sections has one purpose | MET | Sections 1-5 each single purpose |
| CL4 terms defined on first use | MET | Conventions defines BR, EVAL, HO2, IG, RE, DS, AC, PAT | MET | Conventions defines EVAL, BR, GEN, EXT, DS, AC, PAT | NOT MET | GT, "DE runs", "terra" never defined |
| CL5 actionable next steps | MET | Sec 4 recommendation; build 3.0 first; outcomes list | MET | Outcomes table with adopt, stop, report actions | MET | Adopt CRS if difference under 0.3 |
| **Subtotal** | **5/5** | | **5/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| RK1 at least 3 risks with probability and impact | NOT MET | RE-EVALUATED (pass1 MET: Kill rate 5% or less; luna files 31% surface blockers / pass2 NOT MET: Failure tables list effect, no probability per risk) | NOT MET | RE-EVALUATED (pass1 MET: Rubber-stamp 41% non-defects; compliance 91.4%; 2.75-3.25 wrong blockers / pass2 NOT MET: Failure tables list effect, no probability per risk) | NOT MET | Only false-positive growth quantified (+2 to +4); no likelihoods |
| RK2 mitigation for each risk | MET | Every failure-table row has a mitigation | MET | Every failure row has a control | MET | Every failure bullet has a mitigation |
| RK3 failure modes and recovery | MET | Graceful degradation to isolated panel; fallback recorded | MET | Pre-pass kill falls back; re-ask only if time fits | NOT MET | RE-EVALUATED (pass1 NOT MET: Killed CRS reviewer lost; helper failure unhandled / pass2 MET: Verifier timeout leaves claims unverified, listed in follow-up) |
| RK4 external dependencies and failure | MET | REQ-35 judge API error audited per batch | NOT MET | RE-EVALUATED (pass1 MET: Block-randomised order cancels gateway load drift / pass2 NOT MET: Only gateway-load randomisation; no dependency failure handling) | NOT MET | No judge, gateway or API failure handling |
| RK5 monitoring or validation mechanism | MET | Per-class yield telemetry; REQ-33 displacement and wrong blockers | MET | R-10 meta fields; ledger audit metrics | MET | Coverage audit counts unchecked; req 20 wrong blockers |
| **Subtotal** | **4/5** | | **3/5** | | **2/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| IV1 collection boundaries | MET | NONE FOUND for empty check; cap 12 items | MET | Empty sheet; 12-item cap; R-17 | MET | 200-sentence fixture capped at 60; 12 hits per path |
| IV2 cross-boundary state interactions | MET | Ledger quote vs 200-char anchor; promotion via anchor_text | MET | Ledger outside block; R-03 merge unchanged | MET | Coverage block ignored by merge; req 7 |
| IV3 guard-condition gaps | MET | Unknown-key acceptance and plan sha flagged UNVERIFIED | MET | Plan sha equality UNVERIFIED, must be checked first | MET | BLOCK_OK checks fence opener only; parse gap noted |
| IV4 count divergence | MET | D=floor(1.35b); run counts 120, 96, 48 reproduce | NOT MET | RE-EVALUATED (pass1 NOT MET: 128 vs 129 critical path; 25 vs 24 item assignments / pass2 MET: I7 excluded from sums; 254-run total recomputes) | NOT MET | Coverage sums off by 0.1 to 0.55 |
| IV5 combined-component interactions | MET | Harness overlap may double-count 0.1; displacement | MET | H and redesign shares never summed; placebo arm | MET | "Shares are not additive" |
| **Subtotal** | **5/5** | | **4/5** | | **4/5** | |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 5/5 | 5/5 | 3/5 |
| Correctness | 3/5 | 2/5 | 1/5 |
| Structure | 5/5 | 5/5 | 4/5 |
| Clarity | 5/5 | 5/5 | 3/5 |
| Risk Coverage | 4/5 | 3/5 | 2/5 |
| Invariant & Edge Case Coverage | 5/5 | 4/5 | 4/5 |
| **qual_score** | **27/30 = 0.9000** | **24/30 = 0.8000** | **17/30 = 0.5667** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Eligible as base (floor 1/5) |
|---------|-----------------------------|------------------------------|
| V1 | 5/5 | yes |
| V2 | 4/5 | yes |
| V3 | 4/5 | yes |

## Position-Bias Mitigation

Raw totals: pass 1 (V1, V2, V3) = 29, 26, 17; pass 2 (reverse) = 28, 27, 18. Disagreements: 9 of 90 criterion-variant pairs. Each was re-evaluated by a third agent with both pieces of evidence (`scoring/resolved-evidence.md`); all nine finals are NOT MET.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| CR1 no factual errors (recomputed) | V2 | NOT MET | MET | DISAGREE | NOT MET (critical-path table sums to 129-151, not the stated 128-150; 25 vs 24 assignments) |
| CR3 terminology consistent | V1 | NOT MET | MET | DISAGREE | NOT MET (H1-H4 means both harness fixes and hold-out sets; "A" overloaded) |
| CR3 terminology consistent | V2 | NOT MET | MET | DISAGREE | NOT MET (same H-label clash; S used for step and extractor) |
| CR4 no internal contradictions | V1 | MET | NOT MET | DISAGREE | NOT MET (luna +1.5k tokens at 48 tokens/s is about 31 s against the stated +12 s) |
| IV4 count divergence | V2 | NOT MET | MET | DISAGREE | NOT MET (24 vs 25 assignments; 128 vs 129 s) |
| RK1 risks with probability and impact | V1 | MET | NOT MET | DISAGREE | NOT MET (failure tables give effect and mitigation, no probability per risk) |
| RK1 risks with probability and impact | V2 | MET | NOT MET | DISAGREE | NOT MET (same) |
| RK3 failure modes and recovery | V3 | NOT MET | MET | DISAGREE | NOT MET (killed reviewer lost; helper failure has no fallback) |
| RK4 external dependencies | V2 | MET | NOT MET | DISAGREE | NOT MET (only gateway-load randomisation) |

Disagreements re-evaluated: 9
Final verdicts changed from either pass: 9 (4 changed pass 1, 5 changed pass 2)

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker (diff points won, Step 2) |
|---------|---------------|--------------|-----------------|--------------------------------------------|
| V1 (sonnet:architect) | 0.4973 | 0.4500 | **0.9473** | 19 of 41 (46%) |
| V2 (sonnet:analyzer) | 0.4991 | 0.4000 | **0.8991** | 35 of 41 (85%) |
| V3 (haiku:backend) | 0.4784 | 0.2833 | **0.7617** | 5 of 41 (12%) |

Points won are counted from the scoring matrix in `debate-transcript.md`: a variant counts when it is the winner or a named part of a combined winner (the three variants are not exclusive, so shares sum above 41).

**Margin**: V1 over V2 = 0.0482 (4.8 points of score; below the 0.05 threshold of `refs/scoring-protocol.md` A.4: |score_A - score_B| < 0.05)
**Tiebreaker applied**: Yes (level 1, debate performance: V2 won or shared 35 points against V1's 19)

## Selected Base: Variant 2 (sonnet:analyzer)

### Selection Rationale

The raw score ranks V1 first (0.9473 against 0.8991), but the margin of 0.0482 is inside the 0.05 tiebreak band, and the protocol's first tiebreaker (diff points won in the debate) gives V2 35 of 41 against V1's 19. The debate evidence agrees with that ordering: all three advocates conceded to V2 on the sourced harness share (X-001, +0.14), the unchanged grading rule (X-002), median-based time judgement (X-005, X-008) and the arithmetic points (X-003, X-004, X-006), and V2's two redesigns (script-built sheet, prompt-only recipe ledger) were the pair the other two advocates also proposed. The base is marginal: V1 scored higher on completeness of risk and edge-case coverage, so the refactoring plan takes V1's strengths wholesale where the debate sided with V1.

### Strengths to Preserve from Base (V2)

1. Sourced harness share (+0.14, range 0.03-0.34) and the three-share reporting (harness, prompting, redesign), never summed in a headline.
2. Grading rule and judge held constant; CB-1 to CB-3 wording including the blocker sentence.
3. The two redesigns as opposite answers to the open question (script does the sweep; instruction only), with per-package arithmetic and the tightest cell shown.
4. Issue-to-cause map (main and secondary theory per issue), T2a/T2b and T3a/T3b splits.
5. Planted defects with clean twins, placebo and Z0-raw arms, pre-registered gates D1-D6, act-rate readout.
6. Swap test and second-author review of every template.

### Strengths to Incorporate from Non-Base Variants

1. From V1 (3.0, 3.1, 5): class cards as data (definition, recipe, question template, extractor, route, replicas, instances, known weakness), block-kind list as the re-derive checklist, extractor blind spots, quote verifier, the tagged ledger promotion (as amended by INV-005), generic-checklist arm and gate G5, documentation arm, stage 2 on the other two panels, telemetry keys, REQ grouping with a Test column.
2. From V3 (3.1(a), 3.2(a), 3.3, 5): blind claim-only verifier as an off-path audit only, real-parser check of the ledger block, byte-identical determinism test, logged shuffle seed and dropped-item count, package-level bootstrap and stable-hit rate, arm manifest with sandbox hash.
3. From the debate: quota of 1-2 items per triggered class with ranked fill (Q3), one session per reviewer (Q5), one checklist arm K, hang guard 1.5 x (b + overhead), pre-pass kill min(15 s, 0.10 x b).
4. From Round 2.5 and 3: the fourteen invariant resolutions INV-001..INV-014 (selection-recall gate, final-message `ledger-v1` JSON-lines block, break-even values, narrowed claim, promotion function, recomputed matrices, assignment algorithm, no_source rule, displacement 0.1-0.9, intention-to-treat).
