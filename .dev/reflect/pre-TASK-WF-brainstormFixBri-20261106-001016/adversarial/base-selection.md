# Base Selection Report

- Generated: 2026-11-06T01:24Z by the debate-orchestrator (Step 3 of `/sc:adversarial`, Mode A, `--depth standard`).
- Variants: V1 = `variant-1-original.md` (reviewer 1, analyzer, sonnet, calibrated 0.85); V2 = `variant-2-original.md` (reviewer 2, qa, haiku slot, calibrated 0.82); V3 = `variant-3-original.md` (reviewer 3, refactorer, opus, calibrated 0.82).
- Inputs: `diff-analysis.md` (24 scored points), `debate-transcript.md` (Round 1, Round 2, scoring matrix, convergence 24/24, final status BLOCKED_BY_INVARIANTS on INV-020), `invariant-probe.md` (14 UNADDRESSED).
- Protocol: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (A.1-A.5) and `refs/artifact-templates.md` Section 3.

## How the scoring was adapted to a plan-audit card

A variant here is a reviewer card: a list of findings (id, priority, tag, claim, evidence) plus `card_claims_disputed`. It has no H2 sections and no requirement IDs, so the protocol's metrics were mapped as follows.

| Metric | Protocol definition | Adaptation for a plan-audit card |
|---|---|---|
| RC | source requirements matched / total | Denominator 29 = the 24 debate points + the 5 work items of `source.md`. A debate point counts for a variant when the variant is named in the point's Round 2 winner label (single or split) in the scoring matrix. `none` points (S-001, S-002) count for no variant. An A- point counts when the card's own findings are consistent with the agreed verdict (ACCEPT/QUALIFY). A brief item counts when the card has at least one finding about the plan's handling of that item. |
| IC | 1 - contradictions / scorable claims | Scorable claims = findings + `card_claims_disputed` lines. A claim counts against the card when the debate reversed its factual core or moved its priority (conceded in Round 2 or ruled in the scoring matrix). A claim repeated in a finding and a dispute line counts once. |
| SR | concrete / (concrete + vague) | Sentence-level count over every claim and dispute line. Concrete = names a file:line, a count, a field value, a test, a phrase or a plan task. Vague = an unresolved hedge ("arguably", "could", "fragile", "less risk", "can drift", "partly ... not verified"). |
| DC | resolved internal references / total | Internal references = a card's references to its own finding IDs (R1-1, R2-2, ...), to the Tier-1 card's findings (F-1 to F-4, `reflection-card.yaml:27-42`), to its line-711 note (`reflection-card.yaml:44`) and to the Tier-1 coverage rows (`REPORT.md:29-33`). Plan, spec and source files are external and excluded. |
| SC | H2 count / max | Finding count / max finding count (10). |
| Qualitative | 30 criteria for a document | Same 30 criteria, each read as a property of an audit card (for example "success criteria" = a readiness verdict naming the fixes needed; "risk mitigation" = a remedy per finding; "external dependency" = a finding about tree state or another tool outside the plan). |

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (analyzer, sonnet) | V2 (qa, haiku slot) | V3 (refactorer, opus) |
|--------|--------|-----------------------|---------------------|-----------------------|
| requirement_coverage | 0.30 | 0.655 (19/29: 10 S/C/X points + 4 A-points + 5 brief items) | 0.586 (17/29: 10 + 3 + 4) | 0.586 (17/29: 10 + 2 + 5) |
| internal_consistency | 0.25 | 0.692 (1 - 4/13) | 0.833 (1 - 2/12) | 0.615 (1 - 5/13) |
| specificity_ratio | 0.15 | 0.862 (25 / 29) | 0.955 (21 / 22) | 0.897 (26 / 29) |
| dependency_completeness | 0.15 | 1.000 (6/6) | 1.000 (12/12) | 1.000 (6/6) |
| section_coverage | 0.15 | 1.000 (10/10 findings) | 0.800 (8/10) | 0.900 (9/10) |
| **quant_score** | | **0.799** | **0.797** | **0.749** |

Computation: quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC.
- V1: 0.1966 + 0.1731 + 0.1293 + 0.1500 + 0.1500 = 0.7989
- V2: 0.1759 + 0.2083 + 0.1432 + 0.1500 + 0.1200 = 0.7974
- V3: 0.1759 + 0.1538 + 0.1345 + 0.1500 + 0.1350 = 0.7492

### RC detail

| Group | V1 | V2 | V3 |
|---|---|---|---|
| S/C/X points whose winner names the variant (scoring matrix, `debate-transcript.md:612-631`) | C-001, C-003, C-005, C-006, C-008, C-009, C-010, C-013, X-002, X-004 (10) | C-001, C-003, C-004, C-008, C-009, C-010, C-013, X-001, X-002, X-005 (10) | C-002, C-005, C-006, C-007, C-008, C-011, C-012, X-001, X-003, X-004 (10) |
| A-001 ACCEPT (edits leave the two extra tests passing; omission is P2) | yes (R1-7 P2) | yes (R2-5 P2) | no (R3-2 rated P1) |
| A-002 QUALIFY (C-001 blocks through the halt path) | yes (R1-2 P1) | yes (R2-1 P1) | no (silent on C-001) |
| A-003 ACCEPT (substring pins) | yes (R1-3, R1-4) | yes (R2-2, R2-3) | yes (R3-6) |
| A-004 QUALIFY (capture baselines at run time) | yes (R1-2 before/after diff, R1-6 before-count) | no (R2-7 fixes the count at 17/18) | yes (R3-7) |
| Brief item 1 (skill, command, routing wording) | R1-4, R1-5 | R2-2 | R3-6, R3-9 |
| Brief item 2 (find and extend every pinning test) | R1-1, R1-3, R1-9 | R2-3, R2-8 | R3-3 |
| Brief item 3 (sync-dev, verify-sync, plugin mirror) | R1-8 (spec item 8, line 443) | none | R3-8 (plugin copy; later withdrawn, counted for coverage only) |
| Brief item 4 (live-check wording and placement) | R1-5, R1-8 | R2-4 | R3-1, R3-4, R3-5 |
| Brief item 5 (affected tests and lint) | R1-7, R1-10 | R2-1, R2-5 | R3-2 |
| Brief items covered | 5 | 4 | 5 |

### IC detail (claims the debate reversed or re-rated)

| Variant | Claims | Counted against | Source |
|---|---|---|---|
| V1 | 13 (10 findings + 3 dispute lines) | R1-1 (Task 1's clause is not vacuous; P1 to P2), R1-2 (counted untracked `??` folders as tracked), R1-4 (P2 to P1), R1-5 (P2 to P1; its "auggie scan" remedy fails) | a1 criticisms 1-5 (`debate-transcript.md:271-275`) |
| V2 | 12 (8 + 4) | R2-1 ("doubly unpassable" overreaches, X-005), dispute line 1 ("three fixes are needed" omits the P1 C-007) | a2 criticism 3 (`debate-transcript.md:363`); X-003 verdict |
| V3 | 13 (9 + 4) | R3-1 remedy (`source` cannot name the tool, `SKILL.md:372`), R3-2 (P1 to P2), R3-5 ("wrong spot" moved to split), R3-8 and dispute line 3 (withdrawn misreading, counted once), R3-9 (drift runs the other way) | a3 criticisms 1, 4, 5, 9, 10 (`debate-transcript.md:454-463`) |

### SR detail (vague statements)

- V1 (4): R1-4 "could drop", R1-5 "arguably also `primary`", R1-8 "could add a pointer", dispute 2 "partly disputed ... though not verified".
- V2 (1): dispute 2 "disputed at the margins ... only partly honored".
- V3 (3): R3-6 "fragile", R3-6 "with less risk", R3-9 "can drift".

## Qualitative Scoring (50% weight): Additive Binary Rubric

Each cell is a Claim-Evidence-Verdict entry: the claim is "criterion N is met in Vx"; the evidence is a quote or finding reference from the card; the verdict is MET (1) or NOT MET (0). No evidence means NOT MET. Verdicts shown are the final verdicts after the position-bias step.

### Completeness (5 criteria)

| Criterion (card reading) | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. Covers every brief work item | MET | Items 1-5 via R1-4/R1-5, R1-1/R1-3/R1-9, R1-8 (spec line 443), R1-5/R1-8, R1-7/R1-10 | NOT MET | No finding on item 3 (sync-dev, verify-sync, plugin mirror); searched R2-1..R2-8 and all four dispute lines | MET | Item 3 via R3-8 ("test_codegraph_adoption reads it"); other items via R3-1..R3-7 |
| 2. Addresses edge and failure cases of the plan's checks | MET | R1-1 "passes on the OLD text"; R1-3 "satisfied by two copies ... in one tier" | MET | R2-1 "unsatisfiable at baseline"; R2-6 "cannot detect a bullet placed in the wrong list" | MET | R3-1 "would fail a correct analyze run that wrote nested/analyze-1/" |
| 3. Includes dependencies and prerequisites | MET | R1-9 "COMMANDS_DIR points at src/, so Task 5 does not depend on sync-dev" | MET | R2-5 names the two test files that read the edited files | MET | R3-2 "pins the exact Tier 2 block that Task 2 edits" |
| 4. Readiness verdict naming the fixes needed | MET | dispute 1 "disputed; R1-1 is a second defect" | MET | dispute 1 "three fixes are needed (F-1, ... R2-2, ... R2-3)" | MET | dispute 1 "R3-1 and R3-2 also need fixing first" |
| 5. States what needs no change (out of scope) | MET | R1-9 "Line 711 ... needs no change" | MET | R2-8 "line 711 is a synthetic mutation needing no change" | MET | R3-8 "The file is not edited, so nothing breaks" |
| **Subtotal** | **5/5** | | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. No factual errors | NOT MET | R1-1 "Task 1's first acceptance clause passes on the OLD text": false, `SKILL.md:195` lacks `fallback_1` (X-001, conceded) | NOT MET | R2-1 "Both the first clause and the done/ clause fail on a correct run": the second is reading-dependent (X-005, conceded "claimed certainty") | NOT MET | R3-1 "decide by the `source` field ... (analyze vs auggie vs codegraph/Grep)": `SKILL.md:372` allows only `codebase \| research-light \| research-deep` |
| 2. Remedies feasible | NOT MET | R1-5 remedy "Say 'an auggie scan (tier primary)'" names a tool the checker cannot read from the contract (a1 New evidence (a)) | MET | Every remedy offered (R2-7 count baseline; R2-2 pin implied) is executable with existing helpers | NOT MET | R3-1 `source`-field rule has no discriminating value (a3 criticism 1) |
| 3. Terms used accurately | MET | R1-5 uses `primary` exactly as `SKILL.md:198` defines it | MET | R2-3, R2-6 use `fallback_1`, `quality_tier`, Activation bullet as defined | NOT MET | R3-1 treats the contract field `source` as a tool name |
| 4. No internal contradictions | MET | No finding or dispute line contradicts another | MET | R2-1 and dispute 3 ("F-1 confirmed but understated") agree | MET | R3-8 and dispute 3 agree; R3-2 and R3-8 address different files |
| 5. Claims supported by cited evidence | MET | Every finding carries file:line evidence; R1-5 marked INFERRED for its prediction | MET | Every finding Grounded with file:line | NOT MET | R3-1's remedy cites `SKILL.md:201`, which lists `{source, quality_tier}` without values; the values are at `SKILL.md:372` and refute it |
| **Subtotal** | **3/5** | | **4/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. P1 findings before P2 | MET | R1-1, R1-2 P1, then P2 | MET | R2-1, R2-2 P1, then P2 | MET | R3-1, R3-2 P1, then P2 |
| 2. Every finding has id, priority, tag, claim, evidence | MET | `variant-1-original.md:7-56` | MET | `variant-2-original.md:7-46` | MET | `variant-3-original.md:7-51` |
| 3. One defect per finding | NOT MET | R1-10 bundles "do not edit any file" with the Tier 2 list ending (S-001) | MET | Each of R2-1..R2-8 holds one defect | NOT MET | R3-3 bundles the vacuous `fallback_1` pin (C-002) with the file-wide routing pin (C-005) |
| 4. Cross-references to own findings and the Tier-1 card | MET | "R1-1 is a second defect"; F-1..F-4 | MET | F-1..F-4, R2-2, R2-3, coverage rows 2, 4, 5 | MET | F-1, R3-1, R3-2, R3-3, R3-8 |
| 5. Follows the reviewer-card schema | MET | reviewer, persona, model_class, self_confidence, findings, card_claims_disputed | MET | same keys | MET | same keys |
| **Subtotal** | **4/5** | | **5/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. Unambiguous language | NOT MET | R1-5 "arguably also `primary`"; R1-8 "could add a pointer" | MET | One hedge ("at the margins") is resolved in the same line by named rows 2, 4, 5 and reasons | NOT MET | R3-6 "fragile ... less risk"; R3-9 "can drift" |
| 2. Concrete, not abstract | MET | R1-6 names the one added id `brainstorm:phrase:writes no nested directory` | MET | R2-7 "the baseline is 17 ... implying 18" | MET | R3-4 "line 142 is in the section 3.1 table ... P2 row at line 222" |
| 3. Each finding summarizable in one sentence | NOT MET | R1-10 joins two unrelated defects | MET | All eight are single-topic | MET | R3-3 halves share one topic (pins that do not pin what they claim) |
| 4. Terms and conventions defined on first use | NOT MET | `plan:N`, `F-n`, tier names undefined | NOT MET | same | NOT MET | same |
| 5. Next steps identified | MET | Remedy named in R1-2, R1-3, R1-4, R1-5, R1-6, R1-8, R1-10 | NOT MET | R2-1, R2-4 and R2-6 name no action (conceded, a2 criticisms 2, 5, 8) | MET | Remedy named in R3-1, R3-5, R3-6, R3-7 and the disputes |
| **Subtotal** | **2/5** | | **3/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. At least 3 risks with impact and likelihood (priority + tag) | MET | 10 findings, priority and Grounded/INFERRED tag each | MET | 8 findings, priority and tag each | MET | 9 findings, priority and tag each |
| 2. Mitigation for each risk | NOT MET | R1-1 and R1-7 name no fix | NOT MET | R2-1, R2-4, R2-6 name no fix | NOT MET | R3-3 and R3-9 name no fix |
| 3. Failure mode with recovery | MET | R1-2 "cannot pass as written ... Use a before/after diff" | MET | R2-7 missing baseline, recovery "baseline is 17" | MET | R3-7 "needs a baseline count recorded before the edit" |
| 4. External dependency and its failure | MET | R1-2 staged archive under `.dev/tasks/done/` | MET | R2-1 "950 staged additions and 3 renames" | NOT MET | Only candidate R3-8 (plugin copy) concludes no failure and was withdrawn; no tree-state or tool-availability finding |
| 5. Detection mechanism proposed | MET | R1-3 per-tier test via the `test_codegraph_adoption.py:56-59` helper | MET | R2-7 collect-only count 17 then 18 | MET | R3-6 shared pinned phrase |
| **Subtotal** | **4/5** | | **4/5** | | **3/5** | |

### Invariant and Edge-Case Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|---|---|---|---|---|---|---|
| 1. Collection boundaries | MET | R1-3 "two copies ... in one tier" | MET | R2-6 bullet in the wrong list | MET | R3-3 "do not pin one bullet per tier" |
| 2. State interactions across components | MET | R1-2 git index state vs Task 7 AC | MET | R2-1 staged archive vs AC | MET | R3-1 `enrichment_used` state vs nested folder |
| 3. Guard-condition gaps | MET | R1-1 vacuous assertion; R1-4 unpinned rule | MET | R2-2 unpinned rule; R2-3 vacuous assertion | MET | R3-3 vacuous `fallback_1` assertion |
| 4. Count divergence | MET | R1-6 "adds exactly one id" | MET | R2-7 17 to 18 | MET | R3-7 "adds one removed-token case" |
| 5. Interaction effects | MET | R1-7 Task 2 edit at the `test_codegraph_adoption` slice boundary | MET | R2-5 "Tier 2 span test ... borders the Task 2 edit" | MET | R3-9 command text vs skill text drift |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 4/5 | 5/5 |
| Correctness | 3/5 | 4/5 | 1/5 |
| Structure | 4/5 | 5/5 | 4/5 |
| Clarity | 2/5 | 3/5 | 3/5 |
| Risk Coverage | 4/5 | 4/5 | 3/5 |
| Invariant and Edge-Case Coverage | 5/5 | 5/5 | 5/5 |
| **qual_score** | **23/30 = 0.767** | **25/30 = 0.833** | **21/30 = 0.700** |

### Edge-case floor check

| Variant | Invariant and edge-case score | Floor (>= 1/5) | Eligible as base |
|---|---|---|---|
| V1 | 5/5 | pass | yes |
| V2 | 5/5 | pass | yes |
| V3 | 5/5 | pass | yes |

## Position-Bias Mitigation

Pass 1 evaluated the cards in input order (V1, V2, V3); Pass 2 in reverse order (V3, V2, V1). 90 criterion verdicts per pass; 84 agreed. Each disagreement was re-evaluated with both passes' evidence side by side; the re-evaluation verdict is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation reason |
|---|---|---|---|---|---|---|
| Completeness 1 | V3 | NOT MET | MET | DISAGREE | MET | The criterion is coverage; R3-8 addresses the plugin-mirror check of brief item 3. Its wrongness is scored under Correctness. |
| Correctness 1 | V2 | MET | NOT MET | DISAGREE | NOT MET | R2-1 states as fact that the `done/` clause fails "on a correct run"; X-005 shows it is reading-dependent and V2 conceded the certainty claim. |
| Correctness 5 | V3 | MET | NOT MET | DISAGREE | NOT MET | R3-1's remedy is a claim, and its cited line (`SKILL.md:201`) does not support it. |
| Clarity 1 | V2 | MET | NOT MET | DISAGREE | MET | The one vague phrase is made concrete in the same line (rows 2, 4, 5 named, each with its reason). |
| Risk 2 | V1 | MET | NOT MET | DISAGREE | NOT MET | The criterion says "each"; R1-1 and R1-7 carry no mitigation. |
| Risk 4 | V3 | MET | NOT MET | DISAGREE | NOT MET | R3-8 was withdrawn as a misreading (a3 criticism 5), so no external-dependency failure remains in the card. |

Disagreements re-evaluated: 6
Final verdicts changed (final differs from Pass 1): 5 (Completeness 1 V3, Correctness 1 V2, Correctness 5 V3, Risk 2 V1, Risk 4 V3)
Direction check: in 2 disagreements the pass that placed the card earlier was more lenient (Completeness 1 V3, Risk 2 V1), in 2 it was stricter (Correctness 5 V3, Risk 4 V3), and 2 concern V2, which sits in the middle in both passes. No systematic order effect is visible.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate tiebreaker (points won of 24) |
|---|---|---|---|---|
| V1 (analyzer, sonnet) | 0.3995 | 0.3833 | **0.783** | 4.83 (0 sole + 9 halves + 1 third) |
| V2 (qa, haiku slot) | 0.3987 | 0.4167 | **0.815** | 5.83 (2 sole + 7 halves + 1 third) |
| V3 (refactorer, opus) | 0.3746 | 0.3500 | **0.725** | 7.33 (5 sole + 4 halves + 1 third) |

**Margin**: V2 0.815 vs V1 0.783 = 0.032 (3.2 points), below the 5% threshold.
**Tiebreaker applied**: Yes. Step 1 (debate points won, scoring matrix `debate-transcript.md:610-635`; sole win = 1, two-way split = 0.5, C-008's three-way split = 1/3 each): V2 5.83 vs V1 4.83, a gap of 17% of V2's total, so not tied within 5%. V2 wins on step 1; steps 2 (correctness: V2 4 vs V1 3) and 3 were not needed and would also select V2.

Note on V3: V3 won the most debate points (7.33), including the debate's most consequential diagnosis (C-007/X-003), but the tiebreaker only compares the top two by combined score. V3's combined score is 0.725, 0.090 below V2, because its Correctness score is 1/5 (the `source`-field remedy, the withdrawn R3-8, the over-rated R3-2).

## Selected Base: Variant 2 (reviewer 2, qa, haiku slot)

### Selection Rationale

V2 has the highest combined score (0.815) and wins the tiebreaker against V1 on debate points (5.83 vs 4.83). Its findings had the fewest reversals in the debate (IC 0.833, two counted claims against 4 for V1 and 5 for V3), it is the most specific card (SR 0.955), and it is the only card with one defect per finding (Structure 5/5). It won the two points that decide whether the plan can run and whether the owner's rule is pinned: X-005 (Task 7 bullet 3's first clause fails on any reading) and C-004 (the "no nested contract in `artifacts`" half of `source.md:6` is pinned nowhere). Its weaknesses are omissions and missing remedies, not wrong claims, which a merge can fill without rewriting the base.

### Strengths to Preserve from Base

1. R2-1: the exact operative clause of Task 7 bullet 3 (the "among tracked paths" first clause), with the 950 `A` / 3 `R` baseline (`diagnostics.txt:3-4`). Drop only the word "doubly" (X-005).
2. R2-2: the per-task audit of what each pin covers (plan:33, 60, 74), which established the C-004 hole; priority P1 (C-004 verdict, 94%).
3. R2-3: the vacuous `fallback_1` assertion in Task 4 (`SKILL.md:199` inside Wave 2A).
4. R2-5: both missing test files, and the sharper point that the one extra test run (`test_routing_plugin_parity.py`) reads none of the edited files.
5. R2-6, R2-7, R2-8: the Activation-bullet ending, the recorded baseline 17 (`diagnostics.txt:11`), and the line offsets 39 and 288 with the line-711 note.
6. The one-defect-per-finding layout and the all-Grounded evidence discipline.

### Strengths to Incorporate from Non-Base Variants

1. From V3, R3-1 (`variant-3-original.md:7-11`): the diagnosis that plan:81 decides the nested folder by `quality_tier`, widened in Round 2 to both tiers (C-007, X-003; P1). The remedy is replaced by the orchestrator's wording in `refactor-plan.md`, not V3's `source`-field rule.
2. From V1, R1-2 (`variant-1-original.md:12-16`): the before/after `git status --porcelain` remedy for Task 7 bullet 3 (C-001 split verdict), with the capture point the invariant probe requires (INV-001).
3. From V3, R3-3 first half and its Round 2 phrasing (`variant-3-original.md:17-21`): Task 1's paragraph clause is not vacuous but is pinned nowhere (C-002, X-001), plus the paragraph-slice fix.
4. From V1 R1-3 and V3 R3-3 second half: scope the routing-ref pins to each codebase tier (C-005).
5. From V1 R1-8 and V3 R3-5: the placement split, general rule in spec 2.1 and live-check sentence in 7.2 step 4 (C-006, X-004), and V1 R1-8's spec item 8 (line 443) plugin-mirror point (brief item 3, which V2 does not cover).
6. From V1 R1-4 / V3 Round 2 New evidence 5: the remedy for C-004 (one shared phrase covering the directory and contract halves).
7. From V1 R1-6 and V3 R3-7: record the collect-only before-count inside Task 5 instead of relying on 17 (C-008, A-004).
8. From V3, R3-4 (section 3.1, not section 6, for spec line 142; C-011) and R3-6 (shared phrase across verb forms; C-012).
9. From V1, R1-10 first half (Task 7 "do not edit any file" vs writing logs; U-006).
10. From V3, R3-9 as reframed in Round 2: plan:30's "listed in `artifacts` only for a nested command that ran" is ambiguous for a failed call, while cmd:157's unconditional sentence is right.
