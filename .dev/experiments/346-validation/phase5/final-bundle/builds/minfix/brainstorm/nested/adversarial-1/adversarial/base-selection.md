# Base Selection Report

Step 3 of `/sc:adversarial` (hybrid scoring and base selection). Rules: `sc-adversarial-protocol/refs/scoring-protocol.md` A.1-A.5. Template: `refs/artifact-templates.md` section 3.

Variants: **A** = `variant-1-opus-architect.md` (opus:architect), **B** = `variant-2-sonnet-analyzer.md` (sonnet:analyzer), **C** = `variant-3-haiku-backend.md` (haiku:backend). Source: `seed-brief.md`. Inputs: `scoring/qual-pass-1.md` (order A,B,C), `scoring/qual-pass-2.md` (order C,B,A), `debate-transcript.md` (Scoring Matrix, Convergence Assessment, forced L1 round), `invariant-probe.md`. Citations `X:n` are line numbers in variant X.

Debate status carried in: **BLOCKED_BY_INVARIANTS** (55 of 55 points resolved after the forced L1 round; 10 HIGH UNADDRESSED invariants). Depth standard has no Round 3, so under the `no_convergence` rule this step force-selects the base by combined score and documents the non-convergence for user review.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (opus:architect) | Variant B (sonnet:analyzer) | Variant C (haiku:backend) |
|--------|--------|-------------------|-------------------|-------------------|
| requirement_coverage | 0.30 | 1.000 (12/12) | 1.000 (12/12) | 1.000 (12/12) |
| internal_consistency | 0.25 | 0.994 (1 - 1/160) | 0.989 (1 - 2/189) | 0.980 (1 - 2/102) |
| specificity_ratio | 0.15 | 0.894 (160/179) | 0.922 (189/205) | 0.797 (102/128) |
| dependency_completeness | 0.15 | 1.000 (18/18) | 1.000 (23/23) | 1.000 (2/2) |
| section_coverage | 0.15 | 1.000 (8/8) | 1.000 (8/8) | 1.000 (8/8) |
| **quant_score** | | **0.9825** | **0.9856** | **0.9646** |

### Computation

All counts come from one stdlib script (`uv run --no-project python -`, read-only) over the three variant files. Fenced code blocks are tracked by fence character and length, so the `## L1`, `## L2`, `## deferred` lines inside B's four-backtick example (B:136-157) are not headings. "Substantive line" = a non-blank line outside fences that is not a heading, a `---` rule or a table separator row (variant paragraphs are one line each).

**RC (requirement coverage).** The source has no requirement IDs, so the list is the seed brief's 8 Constraints bullets (K1-K8) and 4 Success Criteria bullets (S1-S4); the six required constraints restated in the variant prompts are the same items and are not counted twice. A requirement is matched when every keyword regex of its row matches the variant text (case-insensitive):

| ID | Seed requirement | Keyword regexes (all must match) | A | B | C |
|---|---|---|---|---|---|
| K1 | Build on 427's `## Review Loop`; keep its 7 bullets, cap text and test pins | `review loop`; `(seven\|7)\b[^.\n]{0,20}bullets`; `test_spec_panel_review_loop\|test_review_severity_rule` | Y | Y | Y |
| K2 | Mechanical enforcement first; prose-only rules named with residual risk | `prose`; `residual` | Y | Y | Y |
| K3 | Additive variant `spec-panel-minfix` | `spec-panel-minfix`; `additive` | Y | Y | Y |
| K4 | Installed primitives never cite `src/superclaude/`; package via `superclaude` CLI | `src/superclaude`; `install` | Y | Y | Y |
| K5 | UV only; no new dependency | `uv run`; `stdlib\|no (new )?(package )?dependenc` | Y | Y | Y |
| K6 | Explicit, logged override with a reason | `override`; `reason` | Y | Y | Y |
| K7 | Escalate, never expand | `escalat`; `never (be )?expand\|never expanded\|not expand\|without expanding` | Y | Y | Y |
| K8 | 3-review cap unchanged | `(3\|three)-review cap` | Y | Y | Y |
| S1 | S1 bars (R3 mean <=3 vs control 6.0; growth <=44.4% vs 63.5%) | `44\.4`; `63\.5`; `6\.0` | Y | Y | Y |
| S2 | Every changed sentence attributed; zero unapproved over-budget fixes | `attribut`; `over[- ]budget` | Y | Y | Y |
| S3 | `origin=changed` share stays measurable | `origin=changed` | Y | Y | Y |
| S4 | Stated falsification result | `falsif` | Y | Y | Y |

First-run note: with the narrower patterns `(seven|7) bullets` and `never expand|not expand`, A missed K1 (A:163 says "still seven one-line bullets") and C missed K7 (C:167 says "escalate the remaining blockers without expanding scope"). Both patterns were widened once, equally for all variants, to the forms above. RC is topic coverage only; whether a variant honours a requirement is judged in the qualitative layer (Completeness 1).

**IC (internal consistency).** Scorable claims = substantive lines that contain a number or a backticked named entity (the A.1 concrete indicators): A 160, B 189, C 102. Contradictions = the verified internal contradictions cited by either qualitative pass or confirmed in the re-evaluation below, each counted once:

| Variant | Contradiction (opposing claims about the same subject) | Count |
|---|---|---|
| A | A:82 "13 blocking findings (2 `C`, 11 `B`, 1 `L`): 160 + 440 + 150 = 750": the breakdown and the sum describe 14 findings | 1 |
| B | B:331 M2 (variant equals `src/superclaude/commands/spec-panel.md` line for line, and that file cites `src/superclaude/examples/release-spec-template.md` at line 220) versus B:334 M5 ("no `src/superclaude` in the command"); minor budget "12 words, net 0" (B:133, B:223, B:233) versus "fixcheck budget 0" / "minor budget 0" (B:133, B:226) | 2 |
| C | C:88 "`fix` requires at least one real edit" versus, in the same paragraph, `fix` "instead of its own edit" (a third form, "owned edit or incoming link", at C:195); gate folder `cycle-1/` (C:47, C:68) versus `minfix-cycle-N/` for the same `state.json` and `ledger.json` (C:126) | 2 |

A:314 (growth row labelled "bytes", ceiling computed in words against an 8,148-word draft) is a unit error, not two opposing claims, so it is scored under Correctness 1, not here. The unit is a paragraph-line, which holds several claims, so IC is an upper bound for all three variants alike.

**SR (specificity ratio).** A.1 gives two definitions: the metrics table ("concrete statements / total substantive statements") and the YAML formula `concrete / (concrete + vague)`. The vague-term regex (`appropriate(ly)?|as needed|properly|adequate(ly)?|should consider|might|various|etc.|best practices?|industry standard`) matched **0** lines in every variant, so the YAML formula gives 1.000 to all three and separates nothing. The table definition is used: concrete lines (containing a digit or a backticked token) / substantive lines = A 160/179, B 189/205, C 102/128. Sensitivity: with the YAML formula the quant scores are A 0.9984, B 0.9974, C 0.9951 and the selected base does not change (see Combined Scoring).

**DC (dependency completeness).** References matched: `sections? N(.M)` in substantive lines. Each match was read and classified; references to another document are external and excluded per A.1.

| Variant | Internal references (all resolve to a heading of that number with the cited content) | External, excluded |
|---|---|---|
| A | 18: A:82, 125, 134, 136, 144-148, 153, 225 (x2: class table in 2.4, exit codes in 2.5), 266 ("Why a skill folder" at A:151), 294, 303, 345, 349, 370 ("What would mean the idea failed" at A:324) | 3: A:30 and A:126 (S1 spec section 2.4), A:262 (design doc section 5) |
| B | 23: B:87, 98 (7.2 lists under-fixing first, B:446), 110, 111, 112, 218, 222 (x2), 228, 244, 245, 376, 384 (x2), 389, 397, 446 (x2), 467, 471 (x2), 479, 480 | 7: B:24, B:47 (x2), B:391 (S1 spec sections 2.4 and 3), B:33 (x2, `disposition.md` sections 0 and 1), B:73 ("section 7 of the spec") |
| C | 2: C:151, C:285 (section 2) | 1: C:16 (design doc section 5) |

Every internal reference resolves, so DC = 1.000 for all three. C makes far fewer cross-references (2), which the metric does not penalise.

**SC (section coverage).** H2 headings outside fences: A 8, B 8, C 8 (the same eight seed sections in the same order). Max 8, so SC = 1.000 for all.

**Formula.** `quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC`:
- A = 0.300 + 0.25 x 0.99375 + 0.15 x 0.89385 + 0.150 + 0.150 = **0.9825**
- B = 0.300 + 0.25 x 0.98942 + 0.15 x 0.92195 + 0.150 + 0.150 = **0.9856**
- C = 0.300 + 0.25 x 0.98039 + 0.15 x 0.79688 + 0.150 + 0.150 = **0.9646**

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts after position-bias resolution (A.5). Where both passes agreed, the agreed verdict and its evidence are used; where they disagreed, the re-evaluation verdict (marked **R**) is final. The protocol has six dimensions (30 criteria); the template's five-dimension tables are extended with the Invariant & Edge Case dimension, and qual_score is out of 30.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| Covers all explicit requirements | NOT MET | Both passes: A:157 keeps the file byte-identical outside five regions, so the installed variant carries `src/superclaude/examples/...` (spec-panel.md:220); pass 2 adds A:365, an over-budget fix can reach a review | NOT MET **R** | Installed copy keeps the `src/superclaude/` citation (B:241, B:331; spec-panel.md:220) | MET | C:160 replaces the inherited source-path lookup; C:182 no eighth bullet; C:98 escalate, never a larger fix |
| Addresses edge cases/failures | MET | A:347-355; A:105-110 | MET | B:444-456; B:327 tests 1-19 | MET | C:329-343; C:275 |
| Includes dependencies/prerequisites | MET | A:278; A:185 stdlib list | MET | B:104-106 `E-FIXCHECK-MISSING`; B:360 | MET | C:289 |
| Defines success/completion criteria | MET | A:322; A:324-330 | MET | B:378 bar (a)-(c) | MET | C:313-314; C:345 |
| Specifies out-of-scope items | MET | A:140; A:256 | MET | B:246-247; B:340 | MET | C:158; C:347 |
| **Subtotal** | **4/5** | | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| No factual errors | NOT MET **R** | A:82 count error (2+11+1 = 14, stated 13); A:314 growth row labelled bytes, computed in words | MET | B:9, B:241 (486/472 lines verified), B:242 | MET | C:12, C:319, C:317 (12,288/57,763 = 21.3%) |
| Feasible with stated constraints | MET | A:162 drops `## Unattended mode` with the test reason; A:151 avoids the `sc-` install strip; A:37 no coordinator duty | NOT MET **R** | B:241 copy keeps `## Unattended mode`, which fails `test_worker_contract.py:831-839`; B:331 pins it; B:248 omits that test | NOT MET | Both passes: C:47, C:49 coordinator freeze/hash duties no brief carries; C:149 keeps `## Unattended mode` |
| Terminology consistent | MET | A:80 term definitions used in A:73-78, A:189-196 | MET | Classes identical at B:174-176, B:273-275, B:296-298 | NOT MET **R** | Gate folder `cycle-1/` (C:47, C:68) versus `minfix-cycle-N/` (C:126) |
| No internal contradictions | MET | Both passes: A:76-78 = A:189-191; A:109 = A:174 | NOT MET | Pass 1: B:331 M2 versus B:334 M5; pass 2: minor budget 12 (B:223, B:233) versus 0 (B:133, B:226) | NOT MET **R** | C:88 "`fix` requires at least one real edit" versus "instead of its own edit" in the same paragraph |
| Claims supported by evidence/rationale | MET | A:82 calibration; A:13-20; A:29-31 | MET | B:89-98 replay; B:407 derivation | NOT MET **R** | C:62 limits are "initial engineering choices"; C:313/C:317 forecast 1/1 with no derivation (withdrawn in debate, C-024) |
| **Subtotal** | **4/5** | | **3/5** | | **1/5** | |

### Structure (5 criteria)

All 15 verdicts agree across passes: MET for every variant (logical order: A:35, B:100, C:20; hierarchy without orphans; causes, changes and risks in separate sections; section cross-references: A:144-148, B:170, C:285; the eight seed sections A:5-372, B:5-469, C:3-349).

| Criterion | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Logical ordering | MET | MET | MET |
| Consistent hierarchy | MET | MET | MET |
| Separation of concerns | MET | MET | MET |
| Navigation aids | MET | MET | MET |
| Artifact-type conventions | MET | MET | MET |
| **Subtotal** | **5/5** | **5/5** | **5/5** |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| Unambiguous language | MET | A:61 | MET | B:132; B:211 | MET | C:62; C:122 |
| Concrete | MET | A:45-48; A:73-78 | MET | B:183-193; B:284-289 | MET | C:189-190; C:209 |
| Section purpose | MET | A:7; A:37 | MET | B:102; B:218 | MET | C:5 |
| Terms defined on first use | NOT MET | D9 (A:151), D10/V1-V6 (A:308), D5 (A:298) undefined | NOT MET | D10/D11/D12 (B:9), V1-V6 (B:378) undefined | NOT MET | D10 (C:297), D5 (C:299) undefined |
| Actionable next steps | MET | A:271-273; A:325 | MET | B:479; B:353-355 | MET | C:289; C:358 |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| >=3 risks with probability and impact | NOT MET | A:349-355, one likelihood word only | NOT MET | B:444 table has no probability column | NOT MET | C:329 table has no probability column |
| Mitigation per risk | MET | A:349-352 | MET | B:446-456 | MET | C:331-343 |
| Failure modes and recovery | MET | A:62; A:105-110 | MET | B:204; B:211 | MET | C:96; C:259-267 |
| External dependencies | MET | A:180; A:110 | MET | B:106; B:451 | MET | C:289; C:342 |
| Monitoring/validation | MET | A:302-308 | MET | B:381 V7; B:318 | MET | C:291; C:307 |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

All 15 verdicts agree across passes: MET for every variant (A:193, A:233, A:244 / B:211, B:327 / C:195, C:216, C:275 for boundaries; A:42, A:66 / B:131 / C:47, C:126 for state interactions; A:50, A:99 / B:166, B:453 / C:195 for guards; A:237 / B:327 tests 2 and 4 / C:90, C:214 for off-by-one; A:350 / B:48, B:447 / C:62, C:335 for interactions).

| Criterion | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Collection boundaries | MET | MET | MET |
| State interactions | MET | MET | MET |
| Guard condition gaps | MET | MET | MET |
| Count divergence | MET | MET | MET |
| Interaction effects | MET | MET | MET |
| **Subtotal** | **5/5** | **5/5** | **5/5** |

### Qualitative Summary

| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Completeness | 4/5 | 4/5 | 5/5 |
| Correctness | 4/5 | 3/5 | 1/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 | 4/5 |
| Invariant & Edge Case | 5/5 | 5/5 | 5/5 |
| **qual_score** | **26/30 = 0.867** | **25/30 = 0.833** | **24/30 = 0.800** |

Pass totals for reference: pass 1 A 27, B 26, C 25; pass 2 A 26, B 26, C 26.

## Position-Bias Mitigation

Six criteria disagree between pass 1 (A,B,C) and pass 2 (C,B,A). Each was re-evaluated by reading the cited variant lines and the ground truth (`src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`, `tests/skills/test_worker_contract.py:831-839`).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Correctness 1 (no factual errors) | A | MET | NOT MET | DISAGREE | NOT MET |
| Completeness 1 (all explicit requirements) | B | NOT MET | MET | DISAGREE | NOT MET |
| Correctness 2 (feasible with constraints) | B | MET | NOT MET | DISAGREE | NOT MET |
| Correctness 3 (terminology consistent) | C | MET | NOT MET | DISAGREE | NOT MET |
| Correctness 4 (no internal contradictions) | C | NOT MET | MET | DISAGREE | NOT MET |
| Correctness 5 (claims supported) | C | NOT MET | MET | DISAGREE | NOT MET |

Agreements with different reasons (verdict kept, no re-evaluation): A Completeness 1 (NOT MET in both: pass 1 the inherited `src/superclaude/` path, pass 2 over-budget fixes reaching a review); B Correctness 4 (NOT MET in both: pass 1 M2 versus M5, pass 2 minor budget 12 versus 0); C Correctness 2 (NOT MET in both: pass 1 coordinator duties and byte offsets, pass 2 coordinator duties and `## Unattended mode`).

### Re-evaluation log

1. **A, Correctness 1.** Pass 1 spot-checked external facts (A:9 report figures, A:151 install rule, A:162 test lines) and found them correct; that evidence stands. Pass 2 cites A:82 and A:314. Read: A:82 says "Expected cycle-1 ceiling at 13 blocking findings (2 `C`, 11 `B`, 1 `L`): 160 + 440 + 150 = 750"; 2 + 11 + 1 = 14, and the three addends are the budgets of 14 findings (2 x 80, 11 x 40, 1 x 150). A:314 labels the growth row "(bytes)" but computes the ceiling from "at most 870 added words ... 390 ... against an 8,148-word draft". A wrong count and a wrong unit are factual errors in the document even though the external facts are right. **Final: NOT MET.**
2. **B, Completeness 1.** Pass 2 holds that bullets 1-7 kept byte-identical satisfy "keep its 7 bullets". Pass 1 cites the seed constraint "Installed primitives never cite `src/superclaude/` paths". Read: B:241 makes the new command "a copy of `spec-panel.md`", B:331 pins it to "equals `src/superclaude/commands/spec-panel.md` line for line" outside the listed regions, and ground truth `src/superclaude/commands/spec-panel.md:220` (and the 472-line `plugins/` copy at line 218) reads "`src/superclaude/examples/release-spec-template.md` — read when generating scoped release specs". The installed variant therefore cites a `src/superclaude/` path, an explicit constraint B does not meet. (Whether an appended bullet 8 breaks "keep its 7 bullets" is arguable and is not relied on.) **Final: NOT MET.**
3. **B, Correctness 2.** Pass 1 found B's briefs feasible (B:364, B:370), which is true for the experiment file built on the 472-line text. Pass 2 cites the repository file. Read: B:241 says the copy "carries ... a 12-line `## Unattended mode` section"; B:362 "the repository file is the same change applied to current `src/`"; B:331 M2 locks the copy to the original; B:248 lists the tests that "may need a row" and omits `test_worker_contract.py`. Ground truth `test_worker_contract.py:831-839` asserts the set of commands with `^## Unattended mode` equals `UNATTENDED_COMMANDS` exactly, so the repository file as specified fails an existing test, and B's own pin forbids the fix. **Final: NOT MET.**
4. **C, Correctness 3.** Pass 1 checked concept terms (baseline, candidate, state, receipt, ledger) and found them consistent; that is correct. Pass 2 cites file names. Read: C:47 "creates `cycle-1/state.json`", C:68 "`cycle-1/ledger.json`", C:126 "`minfix-cycle-N/` ... contains `state.json`, `freeze-receipt.json`, `ledger.json` and `check.json`". The same folder has two names in the operational contract, which an implementer must reconcile. **Final: NOT MET.**
5. **C, Correctness 4.** Pass 2 found the budget numbers consistent (C:58 = C:245-246); true. Pass 1 cites C:88. Read: "`fix` requires at least one real edit; `escalate` and `defer_minor` allow none. ... A finding answered only by another finding's edit may therefore have `fix` with an incoming `also_answers` link instead of its own edit." C:195 then states a third form, "covered by an owned edit or incom[ing link]". The first sentence, read as a ledger validation rule, rejects what the second allows, so the document carries two versions of one rule. **Final: NOT MET.**
6. **C, Correctness 5.** Pass 2 cites the evidence table C:9-16, which does support the problem framing. Pass 1 cites the design's own quantitative claims. Read: C:62 "These are initial engineering choices, not empirically optimized limits" (the 60-word and 600-word caps); C:313 forecasts R3 proxy "1 / 1 | 1.0"; C:317 "These are deliberately testable forecasts, not confidence intervals or arithmetic consequences of 427". The budget values and the headline forecast have no derivation in the document, and C's advocate withdrew the 1/1 forecast in the debate (Scoring Matrix C-024). Only the 21.3% growth bound (C:317) is derived. **Final: NOT MET.**

Disagreements re-evaluated: 6
Final verdicts changed: 3 of the 6 pass-1 verdicts (A Correctness 1, B Correctness 2, C Correctness 3 move to NOT MET) and 3 of the 6 pass-2 verdicts (B Completeness 1, C Correctness 4, C Correctness 5 move to NOT MET). All six resolve to NOT MET because in each case the MET pass checked a different, narrower piece of evidence and did not rebut the defect the other pass cited.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (opus:architect) | 0.4913 | 0.4333 | **0.9246** | 18 of 55 points (32.7%) |
| B (sonnet:analyzer) | 0.4928 | 0.4167 | **0.9095** | 28 of 55 points (50.9%) |
| C (haiku:backend) | 0.4823 | 0.4000 | **0.8823** | 7 of 55 points (12.7%) |

**Margin**: 1.51% (A 0.9246 minus B 0.9095 = 0.0151), below the 5% threshold.
**Tiebreaker applied**: Yes. Level 1 (debate points won) decides: B 28 versus A 18, a gap of 18.2 percentage points of the 55 points, so the debate is not tied and levels 2 (correctness count) and 3 (input order) are not reached.

Robustness of the decision:
- The qualitative layer moves a variant by 0.5/30 = 0.0167 per criterion; the three qual totals span 2 criteria and the quant scores span 0.021, so these inputs cannot put the top two more than 0.05 apart. With pass 1 alone (A 0.9413, B 0.9262), with pass 2 alone (B 0.9262, A 0.9246) and with the YAML SR formula (A 0.9326, B 0.9153) the top two stay within 0.05 and level 1 selects B in every case.
- C is also within 0.05 of A (0.0423). A.4 compares only the top two; applying level 1 to all three would still select B (28 > 18 > 7).

## Edge-Case Floor Check

| Variant | Invariant & Edge Case | Floor (>= 1/5) |
|---|---|---|
| A | 5/5 (both passes) | Eligible |
| B | 5/5 (both passes) | Eligible |
| C | 5/5 (both passes) | Eligible |

No variant is excluded. Note the tension with the debate: this dimension scores each variant's own text, and all three cover the five edge-case categories; the invariant probe scores the debate consensus, a mix of the three, and finds 10 HIGH gaps in it (several are seams between parts taken from different variants, such as INV-006). The floor result does not clear those gaps; they are carried below.

## Selected Base: Variant B (sonnet:analyzer)

### Selection Rationale

- Combined scores put A first (0.9246) and B second (0.9095), 0.0151 apart. B leads the quantitative layer (0.9856, highest specificity: 189 of 205 lines concrete); A leads the qualitative layer by one criterion (26 versus 25), the difference being B's `## Unattended mode` feasibility defect (Correctness 2).
- The margin is under 5%, so A.4 level 1 decides: B won 28 of 55 diff points, A 18, C 7. B's wins are mostly evidence and measurement content (S-003, S-006, S-007, C-024, C-025, C-029, X-010, X-011) and the checker's core (C-001, C-002, C-003, C-006, C-007, C-009, C-013, X-005), the parts hardest to rebuild in a merge. A's wins are mostly contract shape (seven bullets, reviewer-owned override, no coordinator duty, ids out of the spec), which are short edits to apply onto B.
- Selection is forced under the `no_convergence` rule: the debate ended BLOCKED_BY_INVARIANTS, so B is a base for the merge, not a converged design. The required changes below must be in `refactor-plan.md`.

### Strengths to Preserve from Base

All are Scoring Matrix points B won (confidence in brackets).

1. Six evidence tables in section 1 (S-003, 95%) and the derivation tables a reader can recompute (S-006, 95%), with the chain taxonomy and cap replay (C-029, 95%; B:36-98).
2. Risk table with detection, mitigation and residual columns per risk (S-007, 95%; B:442-456).
3. The all-findings `fixbudget` block with a derived class (C-001, 95%), amended with C's hard-gate check (but see INV-005).
4. Budget values: MAJOR 80 gross / 50 net (C-002, 95%); CRITICAL 120 gross with B's net and add-only caps (C-003, 90%); B:170-176.
5. Universal and exec-recipe gates (C-006, 95%), extended with A's condition-word counter and C's byte counters.
6. Ledger inside the disposition file, matching T08's single write target (C-007, 95%).
7. Lookahead sentence splitter, amended to one owner per hunk and gated by the replay harness (C-008, 70%; A-001, 70%).
8. Reviewer hash plus `STALE-BASE` refusal with no coordinator duty (C-009, 95%; B:131).
9. Script-side `enforce` reverting whole failing findings, with a coupled revert, as the termination guarantee (C-013, 70%; X-005, 70%; A-002, 70%; A-004, 70%; B:210-211).
10. Reviser prose kept out of the next review; numbers and ids only (X-008, 95%).
11. In-scope deletions free but measured (X-009, 70%); whole-fix measurement (X-010, 95%); the finding that fix size alone does not separate parents with blocking children (X-011, 95%).
12. `@`-anchored brief substitution (C-021, 95%) and the exact 472-line 427 text as the experiment file's base (C-023, 80%; X-014, 95%; B:362).
13. Derived forecast with wide uncertainty, B 1.1-5.6 beside A's about 4.1 (C-024, 95%); replay-derived growth with C's byte bound stated beside it (C-025, 70%); itemised cost (C-027, 95%); behaviour tests plus the `enforce` property test (C-030, 90%; B:324-338).
14. Forced L1 outcomes B won: skill folder `sc-fixcheck` (unanimous) and the section name `## Fix Budget` (B and C). C-010 (folder name, 70%, a tie between B and A) is settled by the `sc-fixcheck` vote.

### Strengths to Incorporate from Non-Base Variants

Every diff point B lost, and the forced L1 outcomes.

From Variant A (opus:architect):
1. Mechanism steps grouped by actor and phase (S-004, 95%; A:35-70), numbered H3 per mechanism step (forced L1 S-002, A and B), and a file table followed by one H3 per artifact (S-005, 80%; A:138-262). Keep the eight seed sections in seed order (forced L1 S-001).
2. Zero edits for non-blocking findings, replacing B's 12-word minor budget; report the proxy and blocking counts separately (C-004, 70%; X-001, 70%; A-003, 70%). This also removes B's 12-versus-0 contradiction.
3. One `check` invocation with B's revert folded in (C-011, 70%).
4. Override owned by the reviewer, one per report, A's `L` class (C-014, 95%; X-006, 95%; A:50, A:78). INV-008 (MEDIUM) asks for one merged limit set.
5. Seven Review Loop bullets with bullet 6 amended in place; drop B's bullet 8 (C-016, 95%; X-002, 95%; A:163). Single-advocate L1-A3 (keep 427's bullet-6 wording and append) is recorded, not resolved.
6. Finding ids kept out of the spec text (C-017, 70%; X-003, 70%).
7. The re-review's own read-only checker run is authoritative (C-018, 95%; A:64-66). INV-003 (MEDIUM) asks for its call shape.
8. No coordinator duty that the unchanged briefs cannot deliver (C-022, 80%; X-012, 80%; A:37).
9. Fail line at the seed bar with causal falsifiers, no "promising" band (C-026, 70%; X-013, 70%; A:324-330).
10. One short fit assessment per later adopter (C-028, 70%; A:256-262).
11. Removal of `## Unattended mode` from the repository command file, with the `test_worker_contract.py:831-839` reason (A:162; agreed by all three advocates, INV-025). This fixes B's Correctness 2 defect.
12. A's condition-word counter (C-006 amendment) and its rename-counts-as-one-site rule (A:80; INV-015 MEDIUM).
13. Forced L1: spelled-out class labels where a person reads them (`CRITICAL`, `blocking MAJOR`, `minor`, `override`; A and C). Single-advocate L1-A4 (budget numbers only in the checker constants) recorded.

From Variant C (haiku:backend):
1. Fixed cycle cap of gross words and bytes including overrides, 600 words / 6,144 bytes (C-005, 95%; C:62), with C's 21.3% byte bound (C:317).
2. Exit-code layout: argparse keeps 2, crash is 70, input, hash and output failures separate (C-012, 95%; X-004, 95%; C:259-267). INV-006 requires B's reviser and `enforce` triggers to be rewritten in these codes.
3. Hard-gate or CRITICAL finding graded minor treated as an input error (C-015, 95%), changed per INV-005 below.
4. Fail closed on a missing or stale input (C-019, 95%; X-007, 95%), with the escalation rule of INV-007 below.
5. Fresh-worker valid/invalid probe as proof of delivery (C-020, 95%; C:289).
6. Removal of the inherited `src/superclaude/examples/...` lookup from the installed variant (C:160). Only C met Completeness 1; B's M2/M5 pins must change so the copy omits that path and M5 passes.
7. Byte counters beside the word counters (C-006 amendment; INV-013 MEDIUM).
8. Single-advocate L1-C2 (field name `finding_id`) and L1-B4 (one `fix*` artifact name family) recorded, not resolved.

### Required Changes from the Invariant Probe (HIGH, UNADDRESSED)

The refactor plan must carry all ten as required changes. Starting point: `invariant-probe.md`, "Suggested resolution per UNADDRESSED HIGH item".

| ID | Gap | Suggested resolution (invariant-probe.md) |
|---|---|---|
| INV-001 | `snapshot` writes `.fixcheck/` files, but T08 allows only the spec and the disposition file, so an obedient reviser leaves no receipt and the fail-closed re-review stops | Use the coordinator's existing saved copy (SP:261) as the baseline, and put the receipt data inside the disposition file, so the reviser writes no `.fixcheck/` file |
| INV-002 | Prior blocking findings carried into cycle 2 are not in the review-2 `fixbudget` block, get budget 0 and stay open into review 3 | Make the review-N `fixbudget` block list every still-open prior blocking id with its class, not only the findings new to this review |
| INV-005 | Real S1 review 1 grades FR-8 GAP findings non-blocking, so the hard-gate validation stops cycle 1 with an input error no actor can repair | When the checker sees a hard-gate finding graded minor, reclassify it as class M and record a warning, instead of exiting with an input error |
| INV-006 | Exit codes are C's, but reviser steps and `enforce` triggers are keyed to B's codes, and C's action table assigns actions to the coordinator | Write one exit-code table used by every actor; rewrite B's reviser actions and `enforce` triggers in terms of C's codes; assign each action to the reviser or the reviewer, never the coordinator |
| INV-007 | A fail-closed stop before review 3 is neither a PASS nor a justified escalation | Add one rule: any fail-closed stop before review 3 escalates to the user with the open blocking findings and the named input error |
| INV-012 | The 600-word cycle cap is below the sum of per-finding caps for 13 blocking ids, with no agreed revert order | Fix the cycle-cap revert order (lowest class first, then smallest gross) and record each cut finding as escalated with its need |
| INV-023 | FR-8/FR-9 gap fills need guard branches, but MAJOR allows 1 normative and 1 condition word | Exempt the condition words of an FR-8/FR-9 gap fill from the condition counter, up to the guard rows the finding names, and keep those rows within the finding's budget |
| INV-026 | Within-budget fixes in the S1 chains had blocking children, so the budget alone does not drive review 3 to 3 or fewer | Withdraw the claim that the mechanism alone reaches 3 or fewer; pre-register within-budget parents with blocking children as a measured column (B's `attacks:`), and state the convergence claim only as conditional on it |
| INV-027 | In trt-r1, 5 of 6 review-3 blockers are guard GAPs from short revisions; the condition-word list misses `where` | Add guard-introducing words (`where`, `only when`, `unless`, `if`) to the condition counter, and count each new guard against the finding's budget |
| INV-028 | No cut-down success rate is measured; 11 of 17 MAJOR fixes are over cap, so 4 or more carried blockers would fail the review-3 bar | Pre-register a cut-down success-rate check in the replay harness, and report the review-3 count split into carried and new findings before the bar is applied |

The 13 MEDIUM UNADDRESSED items (INV-003, 008, 009, 013, 014, 015, 016, 019, 020, 021, 029, 030, 031) do not block selection; the refactor plan should list them for review.

### Base-specific defects the merge must also fix

From the final qualitative verdicts on B: the installed copy must not cite `src/superclaude/` (Completeness 1; resolve with C:160 and rewrite M2 so it excludes that line); the repository file must drop `## Unattended mode` (Correctness 2; A:162); M2 versus M5 and the 12-versus-0 minor budget (Correctness 4) disappear once those two changes and A's zero minor budget are applied. Shared by all variants: define D5/D9/D10/D11/V1-V6/FR-8/FR-9 on first use (Clarity 4) and give each listed risk a probability (Risk 1).
