# Base Selection Report

Variants: Variant A = `variant-1-original.md` (Option A of C05, hardened single-reviewer veto). Variant B = `variant-2-original.md` (Option D of C05, blind grader). Neither carries an `--agents` spec (Mode A), so they are identified by letter.

Protocol notes:
- `SKILL.md` states both "30-criterion" and "25-criterion" for the qualitative rubric (the position-bias section says 25, the template lists five dimensions). This run uses the 30-criterion, six-dimension rubric stated in the scoring section and in `refs/scoring-protocol.md`, so `qual_score = criteria met / 30`.
- The quantitative layer is deterministic and was computed by the orchestrator with shell greps over the normalized variant copies (no LLM judgment). It turns out to be weakly discriminating for two design proposals that share one template; the qualitative layer and the debate carry the selection. Both facts are stated openly below.

## Quantitative Scoring (50% weight)

Source requirements for RC (no formal FR-/NFR- IDs exist, so section-level topic matching is used, per the protocol's edge case): 26 requirement topics derived from the C05 block and the proposal template, each matched by keyword regex in each variant. A topic counts as matched when any of its keywords occurs. Topics: R01 decision rule stated; R02 spec-panel and tasklist consumers; R03 reflect UC-1/UC-2; R04 data flow; R05 contract fields; R06 CLI surface; R07 the 65-versus-38 measurement; R08 the 2.75-3.25 wrong-blocker result; R09 the 0-of-8 recall result; R10 the 56.8% singleton evidence; R11 `contract.py:295-296` single-reviewer degrade; R12 contract 1.8.0; R13 `merge_method`; R14 rubric B1-B3; R15 calibrator option; R16 debate option; R17 quorum option; R18 existing tests that change; R19 new tests; R20 Cost section; R21 weakest point; R22 owner decisions; R23 falsifiability; R24 benchmark or replay; R25 prerequisite defects D2/D5; R26 telemetry.

IC inputs: scorable claims were counted as the enumerated evidence items, correctness steps and risk items of each variant (A: 17 + 8 + 8 = 33; B: 38 table claims + 5 P-claims + 11 R-rows = 54). Intra-variant contradictions come from Step 1 and the debate: A has 2 (X-005, and X-007 in its intra form, A's Correctness step 7 against A's own Test item 3, which both advocates confirmed); B has 1 (X-006). Sensitivity: counting only 1 for A gives IC_A = 0.9697 and quant_A = 0.9924.

SR inputs: lines containing a digit or a code span are concrete (A 89, B 157); lines containing the protocol's vague terms ("appropriate", "as needed", "properly", "adequate", "should consider", "might", "various", "etc.", "best practices", "industry standard") are vague (A 0, B 0), excluding headings, blank and table-rule lines.

DC inputs: every internal reference resolves in both variants (A: E-1 to E-17, "Test coverage, item 3" and "item 9"; B: V1-V9, G1-G8, K1-K6, F1-F5, X1-X10, P1-P5, R1-R11). References to other conflicts (C02, C13, C19 and so on), research files, and B's "X1-X13" (which names exposures in research file R10 §5, not B's own X1-X10) are external and excluded, per the protocol.

SC inputs: top-level (H2) sections, A 7, B 7.

| Metric | Weight | Variant A | Variant B |
|--------|--------|-----------|-----------|
| requirement_coverage | 0.30 | 1.0000 (26/26) | 1.0000 (26/26) |
| internal_consistency | 0.25 | 0.9394 (1 - 2/33) | 0.9815 (1 - 1/54) |
| specificity_ratio | 0.15 | 1.0000 (89/(89+0)) | 1.0000 (157/(157+0)) |
| dependency_completeness | 0.15 | 1.0000 (all internal refs resolve) | 1.0000 (all internal refs resolve) |
| section_coverage | 0.15 | 1.0000 (7/7) | 1.0000 (7/7) |
| **quant_score** | | **0.9848** | **0.9954** |

Weighted (x 0.50): Variant A 0.4924, Variant B 0.4977. The quantitative layer separates the variants by 0.0106 in B's favour, all of it from IC (B has fewer confirmed intra-variant contradictions per claim). Determinism check: the counts above come from fixed greps over fixed files and re-running them yields the same numbers.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Two independent scorer agents ran the 30-criterion rubric (pass 1: A then B; pass 2: B then A), each with CEV evidence, counting only errors that an advocate verified against source or conceded (the transcript records them). The four criterion-variant pairs on which the passes disagreed were re-evaluated by a third agent with both passes' evidence in front of it (see Position-Bias Mitigation); the tables below show the FINAL verdicts. Evidence cells are condensed from the scorers' CEV text.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| C1 Covers all explicit requirements | MET | Per-consumer table: document loop, reflect UC-1/UC-2, tasklist, PR review and rf-qa; all seven template sections | MET | "What each consumer does": document loop, tasklist, reflect Tier 2, `ensemble.py`, future consumers; lens table |
| C2 Edge cases and failure scenarios | MET | Partial reviewers abstain; rejected lines persisted; unresolved anchors cannot block (Risks 1-8) | MET | Batch rejected on malformed line, missing or repeated `cid`, wrong canary; `unconfirmed`; `dropped-unfounded` |
| C3 Dependencies and prerequisites | MET | "four fixes that other conflicts already decide" (C02, C16, C15, C12); D2 named a prerequisite | MET | Owner decisions (G-03, G-04, G-05, C03, G-59); promote `finding-grader` into `src/`; C20 benchmark |
| C4 Success or completion criteria | MET | Test item 9: owner-set tolerance on control-package wrong blockers, baseline 0.83; falsifiable (step 8) | MET | R1: pre-registered replay condition, grader wrong blockers below the veto's with no loss of real-blocking recall |
| C5 Out of scope | MET | "A does not touch it" (C13); "this proposal does not promote anything"; prerequisites "not charged to A" | MET | R4 "Not in the first build"; R9 "stops short of" the contract bump; ensemble placement "not decided here" |
| **Subtotal** | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| K1 No factual errors | NOT MET | Confirmed: E-5 and Correctness step 6 contamination argument has the wrong sign (D1, D6 depress counted blockers); `row.blocking = cluster.blocking_any (ledger.py:187)` conflates the v1 ledger copy and the v2 cluster copy; E-7 cap rests on the defect-rich column (0.25), control is 1.25; "no decider can add recall" is false for B's promotion path | NOT MET | Confirmed: P1 "E2 measured that direction" (control flat by panel size); V7 omits D1; K1 and the candidate rule treat v2 fields as available on the v1 document-loop path; "`_brief_ids` need no change" but undecided rows let `defer()` PASS; "PENDING mirrors stoprule" approximate; stoprule seal rule not ported |
| K2 Feasible with stated constraints | MET | XS/S change inside contract 1.8.0; reuses `ledger.py:187,274`, `cluster.py:375`; v1 path already has a missing-anchor signal (`span is None`) | NOT MET | The document loop's `merge_round` is v1 and lacks `channel`, citations and `outcome`; adapter conceded and uncosted; `defer()` bypasses PENDING; grader pins `model: sonnet` |
| K3 Terminology consistent | MET | `blocking`, `blocking_effective`, `degraded`, "certified PASS" defined in the contract-fields table and used consistently | NOT MET (re-evaluated) | In the verdict-logic block "decision" means both the grader outcome (`decision == blocking`) and the ledger routing word (`decision REVISE, or ESCALATE`); "class" means model class in the `grader` record and deviation class in `clusters{cid}` |
| K4 No internal contradictions | NOT MET | Step 7 "only option that leaves every pin ... alone" versus Test item 3; round-1-scoped PASS rule versus unscoped Design step 6 and Risk 7; Test item 1 keeps `:279-300` green while item 3 changes `:296-298` | NOT MET | P4 "Fail-closed ... by construction" versus R5 "graded not blocking by the rubric's default" (conceded) |
| K5 Claims supported by evidence or rationale | MET | Each E-item carries a line reference and a tag; step 8 states what the argument does not establish | MET | Source-column tables V/G/K/F/X with tags; "What would falsify P1"; "Weakest point" |
| **Subtotal** | **3/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| S1 Logical section ordering | MET | Seven template sections in order; tag key at the start of Evidence | MET | Template order; a "Key" at the top of Evidence defines R01-R13, S4 and the tags |
| S2 Consistent hierarchy depth | MET | H1 plus H2 with bold lead-ins only; no orphans | MET | H2 with H3 subsections; no orphans |
| S3 Separation of concerns | NOT MET | Evidence items carry argument (E-3 "What the 65 versus 38 gap is", E-4, E-9, E-12) | MET | Evidence tables carry sources only; argument isolated in Correctness P1-P5 and "Why D over the other deciders" |
| S4 Navigation aids | MET | E-1 to E-17, "(see Risks)", "(Test coverage, item 9)", tag legend | MET | Key, stable row IDs (V1, G3, X5, R1) and cross-references |
| S5 Conventions of the artifact type | MET | Seven template sections | MET | Seven template sections |
| **Subtotal** | **4/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| L1 Unambiguous language | NOT MET | "whether it keeps exit 0 or gets its own code follows the verdict vocabulary of C19"; "owner-set tolerance" with no number | NOT MET | "(names proposed)"; "design parameters to fix at build time"; "depends on C17 and is not decided here" |
| L2 Concrete rather than abstract | MET | Field table, seven-step data flow, line-referenced rules, exit codes | MET | Command pipeline with flags, `review-decisions/1` field table, verdict pseudo-code, reply schema |
| L3 Section purpose | MET | Each H2 has one summarizable purpose | MET | Each H2 has one summarizable purpose |
| L4 Terms defined on first use | NOT MET | "D3", "D2", "D5", "C13" used before E-5 defines D1-D6; "UC-1" and "E2" never expanded | NOT MET | "PoLL-style", "C11 Option A", "G-57", "B1-B3", "D9 conflict" used before definition |
| L5 Actionable next steps | MET | Benchmark before "declared done"; singleton-filter fallback; owner decision on tolerance | MET | Four ordered Rollout steps; owner-decision list |
| **Subtotal** | **3/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| R1 At least 3 risks with probability and impact | MET (re-evaluated) | Risk 1 baseline "0.83 per run ... up to 1.75" with impact "Option A has failed on its own terms"; Risk 7 "80 reviewer-level invalid-block cases"; Risk 2 "27 over-graded catches" | NOT MET (re-evaluated) | R1-R11 Residual cells use modal words ("can fail to separate the two", "can drop a real blocker"); only R7 carries a figure ("about 3 per run") and its residual reads "real and unmeasured" |
| R2 Mitigation per risk | MET | Each of Risks 1-8 has an italic *Mitigation* | MET | Every R1-R11 row has a Mitigation cell |
| R3 Failure modes and recovery | MET | "Cost of being wrong": follow-up filter on singleton blockers; a degraded outcome "can be re-run" | MET | One rerun then `unconfirmed`; an inconclusive replay "keeps D in shadow" |
| R4 External dependencies and their failure | MET | Risk 6 (one gateway, judge variance); Risks 3 and 8 (prerequisite fixes) | MET | R3 vendor diversity; R6 transport invalidation of the live trial; served-model drift |
| R5 Monitoring or validation mechanism | MET | Reviewer-flag versus effective-flag disagreement rate in telemetry; `singleton_blockers`; benchmark | MET | `overruled` and `promoted` counts, paired veto record, bias battery, replay gate |
| **Subtotal** | **5/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| I1 Collection boundaries | MET | "fewer than two valid reviewer blocks"; cap of three finders; 19-member chained row; test 7 count 1 versus 0 | MET | At most 6 candidates plus 2 canaries; MINOR-only excluded; singletons included; all citations lost gives `dropped-unfounded` |
| I2 State variable interactions across boundaries | MET (re-evaluated) | Risk 3: a re-found row takes the current round's flag (`ledger.py:216-218`, pinned at `test_review_ledger.py:518-544`), with D2 as the stated prerequisite | MET | "A re-found row keeps its decision unless its cited text changed"; rubric hash refused in later rounds |
| I3 Guard condition gaps | MET | `channel: advisory` and `grounding-gap` "may carry `blocking: true` today"; missing anchor gives an effective false | MET | Reply key-set check, duplicate or unknown `cid`, `grade apply` refuses a graded batch; R5 flags the not-blocking default |
| I4 Count divergence | MET | `singleton_blockers` boundary tests (1 versus 2 reviewers, partial reviewer counted); "fewer than two" | MET | `summary {candidates, graded, unconfirmed, ...}`; missing or repeated `cid` rejects the batch; 25% canary overhead |
| I5 Interaction effects | MET | Risk 8 complete-link chains versus the veto; degrade rule versus one-reviewer fallback; D2 with C13 | MET | Grader composes with the reflect debate under 1.8.0; never overrides evidence-sourced regressions; `--decide flag` default versus rollout |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 |
| Correctness | 3/5 | 1/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 3/5 | 3/5 |
| Risk Coverage | 5/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.8333** | **23/30 = 0.7667** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case subtotal | Floor (at least 1/5) | Eligible as base |
|---------|-------------------------------|----------------------|------------------|
| A | 5/5 | pass | yes |
| B | 5/5 | pass | yes |

Caveat recorded for the floor: both variants score the maximum here although the invariant probe (Round 2.5) found 25 boundary and sufficiency findings against the debate's consensus. The rubric scores whether a proposal considers these categories, not whether its design is free of defects in them; the probe's findings are carried forward separately as unaddressed invariants.

## Position-Bias Mitigation

Pass 1 evaluated A then B; pass 2 evaluated B then A; both ran in parallel as separate agents. Each pass produced 24/30 for each variant, but not on the same criteria. Of the 60 criterion-variant pairs, 56 agreed and 4 disagreed. Each disagreement was re-evaluated by a third agent, which was given both passes' evidence, read the variant text, and had to apply one stated standard for R1 to both variants. Its verdict is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| R1 (3 risks with probability and impact) | A | NOT MET | MET | DISAGREE | MET (standard applied to both variants: a risk counts only if the text states a likelihood basis, meaning a measured rate, count, frequency or explicit rating, plus its consequence; modal words such as "can" or "unmeasured" do not count; Risks 1, 7 and 2 of A qualify) |
| R1 | B | NOT MET | MET | DISAGREE | NOT MET (same standard; only R7 is quantified, so three are not reached) |
| I2 (state interactions across boundaries) | A | MET | NOT MET | DISAGREE | MET (Risk 3 is a cross-round state interaction with D2 as its mitigation; deferring the re-find-or-verify choice to C13 does not remove it) |
| K3 (terminology) | B | MET | NOT MET | DISAGREE | NOT MET ("decision" is both the grader outcome and the ledger REVISE/ESCALATE routing word in one block; "class" means model class and deviation class) |

Disagreements re-evaluated: 4. Final verdicts differ from one of the two passes in each of the four pairs; the final matches pass 1 in two (I2 for A, R1 for B) and pass 2 in two (R1 for A, K3 for B). The disputed pairs move the totals by at most one criterion each, which the sensitivity analysis below tests.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate tiebreaker (diff points won of 33) |
|---------|---------------|--------------|-----------------|-------------------------------------------|
| A (Option A, hardened veto) | 0.4924 | 0.4167 | **0.9091** | 2 won (6.1%): C-015, X-004 |
| B (Option D, blind grader) | 0.4977 | 0.3833 | **0.8810** | 6 won (18.2%): S-004, S-005, C-006, C-013, X-001, X-007 |

**Margin**: 0.0281 (2.8 percentage points), below the 5% threshold. Variant A leads on the combined score. **Tiebreaker applied**: Yes.
- Level 1, debate performance (diff points won in the Step 2 scoring matrix): Variant B 6, Variant A 2. The gap is 12.1 percentage points of 33 points, which is above the 5% bar, so level 1 decides and levels 2 and 3 are not reached. (Level 2 for reference: correctness criteria met, A 3, B 1, would favour A; it is not used because level 1 is decisive.)
- Debate-performance context: of 33 points, 13 ended HYBRID, 6 EQUAL, 3 OPEN and 3 QUALIFY, so only 8 produced a one-sided winner. The tiebreak therefore rests on a small count and is reported as such.

**Sensitivity of the selection** (to show it does not hinge on a disputed verdict or on the IC count):
- If A-I2 were NOT MET: A 24/30, combined 0.8924, margin 0.0114 over B (0.8810); still within 5%, level 1 decides: B.
- If B-R1 were MET: B 24/30, combined 0.8977 versus A 0.9091, margin 0.0114; level 1 decides: B.
- If both flipped: A 24/30 (0.8924) and B 24/30 (0.8977); B leads outright.
- If A's IC counted one contradiction (0.9697) instead of two: A combined 0.9129, margin 0.0319; level 1 decides: B.
- If the debate-points count were tied (it is not), level 2 would favour A (correctness 3 versus 1). The selection of B therefore depends on the level-1 tiebreak, and a reader who weights correctness criteria above debate wins would pick A. That is stated here so the choice is not mistaken for a clear score win.

## Selected Base: Variant B (Option D, blind grader after clustering, staged behind a replay gate)

### Selection Rationale
- Variant A led the combined score by 0.0281, inside the 5% band, so the protocol's tiebreaker decided. Variant B won more diff points in the debate (6 against 2), so Variant B is the base.
- The debate's own outcome points the same way structurally. After Round 2 both advocates converged on a merged shape that B already contains as its rollout: the veto stays the live default (`--decide flag`) and the grader runs in shadow and goes live per lens only after a pre-registered paired replay passes. Variant A's text has no staging, no paired baseline and no per-run veto-versus-decider record; Variant B has all three. The base therefore needs fewer structural additions to express the consensus than the alternative would.
- Variant B is the base despite its weaker correctness score (1/5 against 3/5): the confirmed errors in B are mostly in claims that the refactor plan must rewrite anyway (P1, V7, P4, K1 wiring, the PENDING details), and every one of them was conceded by B's own advocate with a concrete fix.
- The selection says nothing about whether the grader is accurate. Nobody has measured it; the merged proposal must not claim it is.

### Strengths to Preserve from Base (Variant B)
1. Candidate and decision split with a deterministic candidate rule, and the veto recorded on every cluster (U-009, U-014).
2. Blindness by construction with a test (U-010); canaries, batch rejection, `unconfirmed` (U-011).
3. Frozen rubric per lens as data with its hash recorded (U-012); `reflect-post` rubric mirrors the halting set (U-013).
4. Staged rollout with `--decide flag` as default until the replay passes (U-015, S-005); inconclusive result keeps D in shadow.
5. Pre-registered paired replay on identical candidates with disjoint canary and benchmark sets (C-013).
6. Evidence tables with a Source column and a falsifier for each argument (S-003, K5).
7. Risk table with a Residual column (S-004).
8. Grader independence and served-model recording (U-016); transport and provenance lessons (U-017).

### Strengths to Incorporate from Non-Base Variant (Variant A)
1. Asymmetric verdict: one valid reviewer may fail, a certified PASS needs two valid blocks at round 1, later rounds inherit, `defer()` recomputes (U-001 with the Round 2 scoping fix; see INV-004 for the residual gap).
2. `singleton_blockers` count and the pre-agreed singleton-first filter (U-002, C-004).
3. The four input fixes stated as prerequisites that act on the veto's inputs (U-003): evidence gate (with the named resolver the debate required), per-lens predicate as data, partial reviewers abstain (with the D2 fix), complete-link clustering.
4. Error-cost asymmetry argument and the blocking-gate evidence (U-004), corrected for the debate's finding that the re-find rate is unmeasured.
5. Rule-parity and monotonicity tests, plus the test accounting corrected in Round 2 (exact-dict `verdict()` equality at `test_review_ledger.py:299-304`, `defer`, exit-code pins) (U-006, S-006, C-014).
6. Panel cap of three kept only as a cost cap (U-005, C-005) and the reading of the 65-versus-38 gap against its definition (U-007, X-003).
7. The "cost of being wrong" argument: the fallback reuses what A adds (U-008).
8. Effort S for the interim and zero extra model calls (C-015, where A won).

### Weaknesses of the Base that the Merge Must Fix (from the debate, each with a source)
- P1 "E2 measured that direction" must become "g is independent of n by construction; E2 neither supports nor refutes a size effect" (X-004).
- V7 must name D1 and say D1 pushes counted wrong blockers down; the cause of the wrong blockers stays unmeasured (X-002, C-012).
- P4 "fail-closed by construction" must be limited to procedure; the grader replies true, false or undecidable, `false` names a failed criterion, doubt keeps the reviewer's flag or goes to PENDING (X-006).
- The document loop is on the v1 `findings` path: state the adapter and the parity test across the v1 ledger rule and the v2 cluster rule (C-015, A-007).
- The stoprule seal rule must be ported (a quote not found is never graded blocking); `unverified` evidence must not be sole support (C-007).
- `defer()` at `ledger.py:356-360` and `EXIT_BY_DECISION` at `ledger_cmd.py:13` must be handled for PENDING.
- The terminology collisions "decision" and "class" must be renamed (K3).
- Risk table must carry likelihood bases, not only modal words (R1).
- Undefined terms (L4) and open phrases (L1) must be defined or closed.

