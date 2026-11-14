# Base Selection Report

## Metadata
- Generated: 2026-11-13T18:48:21Z by the debate-orchestrator (Step 3 assembly)
- Variants: 5 alignment reviews. V1 = #409 observer issue vs the sweep; V2 = #450 issue watcher rollout; V3 = Coder#477 workspace listener; V4 = #423 Orchestrator v2 and the #339 boundary; V5 = the built `superclaude observe` vs the sweep
- Protocol: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` A.1 to A.5 (quant 50 percent, qual 50 percent, six dimensions, 30 binary criteria, position-bias mitigation)
- Inputs used: `step3-quantitative.md`, `step3-qualitative-forward.md` (pass 1, order V1 to V5), `step3-qualitative-reverse.md` (pass 2, order V5 to V1), `step3-disagreements.md`, `step3-reevaluation.md`, `debate-transcript.md` (Scoring Matrix, Convergence Assessment), `invariant-probe.md`
- Debate status carried into this report: **BLOCKED_BY_INVARIANTS** (one HIGH and UNADDRESSED invariant, INV-008). This does not change base selection; it is carried into the refactor plan and the return contract, not waived here.
- Orchestrator verification done in this step: (1) quant weighted sums recomputed from the five metric columns; (2) combined scores recomputed; (3) the 30-criterion final matrix rebuilt from pass 2 plus the 14 final verdicts, and its dimension subtotals matched against `step3-reevaluation.md`; (4) the tiebreaker figure re-counted from the debate-transcript Scoring Matrix (the result differs from the figure in the brief; see Combined Scoring).

## Quantitative Scoring (50% weight)

Metric details and detectors: `step3-quantitative.md` sections 3 to 5. The five reviews cover different subjects, so RC is the mean of RC against the whole request (9 binary checks) and RC against each review's own target (5 checks). Weights are the protocol's.

| Metric | Weight | V1 (#409 vs sweep) | V2 (#450 watcher) | V3 (Coder#477) | V4 (#423, #339 boundary) | V5 (built observer vs sweep) |
|--------|--------|----|----|----|----|----|
| requirement_coverage (RC) | 0.30 | 0.789 | 0.944 | 0.889 | 1.000 | 0.889 |
| internal_consistency (IC) | 0.25 | 0.972 (2 documented defects in 72 items) | 1.000 (none on record, 16 items) | 0.966 (1 in 29: F12 vs Edit 7) | 0.970 (1 in 33: F7 vs C2 on WC-13) | 0.987 (1 in 76: X-020 slip) |
| specificity_ratio (SR) | 0.15 | 0.706 | 0.820 | 0.700 | 0.788 | 0.775 |
| dependency_completeness (DC) | 0.15 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| section_coverage (SC) | 0.15 | 0.750 (6 of 8 H2) | 0.750 | 0.750 | 0.750 | 1.000 (8 of 8 H2) |
| **quant_score** | | **0.848** | **0.919** | **0.876** | **0.923** | **0.930** |

Orchestrator recomputation (0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC): V1 0.2367 + 0.2430 + 0.1059 + 0.1500 + 0.1125 = 0.8481; V2 0.2832 + 0.2500 + 0.1230 + 0.1500 + 0.1125 = 0.9187; V3 0.2667 + 0.2415 + 0.1050 + 0.1500 + 0.1125 = 0.8757; V4 0.3000 + 0.2425 + 0.1182 + 0.1500 + 0.1125 = 0.9232; V5 0.2667 + 0.2468 + 0.1163 + 0.1500 + 0.1500 = 0.9297. All five match the reported scores to three places.

Limits of this layer (from `step3-quantitative.md` section 4): IC, DC and R5 inside RC are near-saturated and separate nothing; RC measures presence, not correctness; the central finding of the debate (the observer exists and four reviews missed it) is invisible to all five metrics. The R3 detector was widened after the first run, so V5 versus V4 for first place on this layer alone is not stable (V4 leads by 0.040 in scenario S0 and 0.057 in STRICT; V5 leads by 0.007 in FINAL and 0.023 in RELAXED). Combined-score robustness against those four scenarios is shown under Combined Scoring.

Survival of findings after Round 2 (reported separately, not part of quant_score; `step3-quantitative.md` section 2): strict survival V1 0.889, V2 1.000, V3 1.000, V4 0.970, V5 0.974; weighted V1 0.840, V2 0.906, V3 1.000, V4 0.818, V5 0.941. This is the better guide to which findings enter the merge (see Strengths to Incorporate).

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Rubric: `scoring-protocol.md` A.2 (30 binary criteria in six dimensions; MET = 1, NOT MET = 0; no partial credit; no citable evidence means NOT MET). Pass 1 = `step3-qualitative-forward.md`, pass 2 = `step3-qualitative-reverse.md`. In each table a cell is the FINAL verdict. `A` = both passes agreed (136 of 150 pairs; evidence is in the named pass file sections). `R#` = the passes disagreed and the final verdict is the re-evaluation result in row # of `step3-reevaluation.md` (14 of 150 pairs). Evidence is quoted only where this report or the re-evaluation file shows it; "pass files" means the criterion row for that variant in both pass files.

### Completeness (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence (CEV) |
|-----------|----|----|----|----|----|----------------|
| C1 Covers all explicit requirements | NOT MET (R1) | NOT MET (A) | NOT MET (R2) | NOT MET (R3) | MET (A) | The owner comment asked for alignment with "TUI Panel"; only V5 determined what the observer is. V1: its claim table says "C-03 No observer code exists; 20 synthetic designs await a human choice (L16) \| Verified" and `observe` appears nowhere in the file. V3: scope read says of #409 "only checked that its live body contains 'Coder#477'". V4: scope read says "no read of #409's design branch". V2: never examined the built observer (Round 2 row 9 concession). V5: S1 to S10 describe PR #503, PR #514 and the code. |
| C2 Addresses edge cases and failures | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. Examples seen: V2 W-15 (refused launch still reads as claimed); V3 F6 (Minimal profile has no orchestrator). |
| C3 Includes dependencies and prerequisites | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | V1 "Missing for integration" (10 items); V2 "Waits for" lines; V3 "What IronClaude must supply or wait for" (7 items); V4 F12; V5 "Dependencies for integrating Orchestrator mode with `observe`" table. |
| C4 Defines success or completion criteria | MET (A) | MET (A) | MET (A) | MET (A) | MET (R4) | R4: V5 D1 states what the contract must hold, an optional join-key check (`superclaude observe --once --run <run>` against a sweep's `rows[].row_id`) and a gate ("settle D5 and D6 before anything else is built"). Same bar as V2 "Done when 0". |
| C5 Specifies out-of-scope items | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files (listed items or cross-references count in all five). |
| **Subtotal** | **4/5** | **4/5** | **4/5** | **4/5** | **5/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence (CEV) |
|-----------|----|----|----|----|----|----------------|
| K1 No factual errors or hallucinated claims | NOT MET (A) | MET (R5) | MET (R6) | NOT MET (A) | NOT MET (A) | V1: "No observer code exists" is false (PR #503 merged 2026-11-11, PR #514 merged 2026-11-12). V4: stated facts "confines every path" (F17: holds for file reads only) and the circular C8 boundary proof. V5: O-05 ("the sweep's reason is stronger than the evidence") withdrawn, BC-17 withdrawn as worded, "all four earlier reviews" overgeneralised (X-019), "drop W-3 from the body" mislabel (X-020). R5 (V2): the four Round 2 concessions are wording, an inference V2 itself labels UNVERIFIED, citation drift and a conditional; none is a stated fact that was disproved. R6 (V3): Edit 5 and Edit 8 defects are inside proposals and are scored under K2; findings F1, F6, F8, F14 and the 5-of-8 path result hold. |
| K2 Technical approaches feasible | NOT MET (A) | MET (A) | NOT MET (A) | MET (A) | MET (R7) | V1: recommended answer persists `<stem>.json` beside the report, which breaks NFR-001 (`docs/designs/orchestrator-mode.md:128`, `tests/sweep/test_readonly.py:300`, `tests/sweep/test_cli_contract.py:1474`). V3: Edit 5 "produced without any write" is unachievable for `sweep run` (X-004). R7 (V5): "(a) now, (b) later" is feasible; persist-now and D5(ii) were Round 1 positions withdrawn for consumption risk, not for impossibility. |
| K3 Terminology consistent and accurate | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| K4 No internal contradictions | NOT MET (A) | MET (R8) | MET (A) | MET (A) | MET (A) | V1: verdict "share the same dimension names" opposes its own C-02 and F-02 (X-008). R8 (V2): "no Run" is stated for the bound-Run question while the Orca-record caveat is labelled UNVERIFIED; both can hold. |
| K5 Claims supported by evidence | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| **Subtotal** | **2/5** | **5/5** | **4/5** | **4/5** | **4/5** | |

### Structure (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence (CEV) |
|-----------|----|----|----|----|----|----------------|
| S1 Logical section ordering | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| S2 Consistent hierarchy depth | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| S3 Separation of concerns | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| S4 Navigation aids | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Id cross-references in all five; none has a table of contents (forward notes). |
| S5 Artifact-type conventions | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence (CEV) |
|-----------|----|----|----|----|----|----------------|
| L1 Unambiguous language | MET (A) | NOT MET (R9) | MET (A) | MET (A) | MET (A) | R9 (V2): Fact 4 "so a registered watcher worktree is very likely scanned" is an unlabelled hedge and Fact 5 and W-05 build on it; V3 F9, V4 F12 and V5 D9 hedges are labelled UNVERIFIED or turned into an owner question. |
| L2 Concrete rather than abstract | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| L3 Clear section purposes | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| L4 Terms defined on first use | MET (R10) | MET (R11) | MET (R12) | MET (R13) | NOT MET (A) | R10 to R13: load-bearing ids are glossed beside use ("WC-16 is a cap (at most once per 5 minutes) on coordinator wakes" in V1 F-12; "path A ... path B" in V2 W-03; "D1 option A 'No listener, inbound port or address registry'" in V3; "WC-12 (:61, pulled not pushed)" in V4); stray ids sit in citation cells. V5 stays NOT MET: its coined names (TUIBBS, QUESTION-OBSERVATION) are never defined in the file. |
| L5 Actionable next steps | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| **Subtotal** | **5/5** | **4/5** | **5/5** | **5/5** | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence (CEV) |
|-----------|----|----|----|----|----|----------------|
| R1 At least 3 risks with probability and impact | NOT MET (A) | NOT MET (A) | NOT MET (A) | NOT MET (A) | NOT MET (A) | Literal reading: none of the five rates likelihood and consequence for three or more risks. Rubric-versus-artifact mismatch (alignment reviews use verdict words); applied identically, separates nothing. |
| R2 Mitigation for each risk | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| R3 Failure modes and recovery | MET (A) | NOT MET (A) | MET (A) | NOT MET (A) | MET (A) | V2 and V4 name failure modes and prevention edits but give no recovery step. |
| R4 External dependencies and their failure | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | Pass files. |
| R5 Monitoring or validation mechanism | MET (A) | MET (A) | MET (A) | MET (R14) | MET (A) | R14 (V4): F6 gates #423 on "the #534 live read-only capture"; Edit 2 repeats it; F21 shows an `ls` check. One-off check plus gate, same bar as V5's `observe --once` comparison. |
| **Subtotal** | **4/5** | **3/5** | **4/5** | **3/5** | **4/5** | |

### Invariant and Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 | V4 | V5 | Evidence (CEV, from `step3-qualitative-forward.md` Dimension 6) |
|-----------|----|----|----|----|----|----------------|
| I1 Collection boundaries (empty, single, max) | MET (A) | MET (A) | MET (A) | NOT MET (A) | MET (A) | V1 F-04 "50 `worker-show` calls and 90 s ... rows past 50 are `could not determine`"; V2 W-07 "up to 6 a day"; V3 F6 Minimal profile, stopped and deleted workspaces; V5 S3 "at most 5 calls per read", S8 "at most 100 rows per read, applied after the type filter". V4: no empty, single or maximum case (searched F2 to F6, F12, F17, F18). |
| I2 State across component boundaries | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | V1 F-03; V2 W-03 (watcher record cannot be joined to a transcript or tab-map key); V3 F4 (`/home/coder` is not unique across workspaces); V4 F4, F13; V5 O-08 and S5. |
| I3 Guard condition gaps | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | V1 F-07 (`_git` runs with `{**os.environ}`); V2 W-11; V3 F14 (anonymous heartbeat), F8; V4 F17, F14; V5 O-09 (guard is one boolean, checks no Run id). |
| I4 Count divergence | MET (A) | MET (A) | MET (A) | NOT MET (A) | MET (A) | V1 C-07 (6 threads, 4 resolved, 2 unresolved vs "five review findings"); V2 W-12 (2655 tests vs 2637 and 2653); V3 "five of the eight paths are wrong"; V5 S7 (486, 691, 693 passed). V4: no divergence finding (its own tally is consistent but is not one). |
| I5 Interaction effects | MET (A) | MET (A) | MET (A) | MET (A) | MET (A) | V1 C-18/F-07; V2 W-01/W-02; V3 F8, F12; V4 F18, F16; V5 O-04, O-10. |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **3/5** | **5/5** | |

### Qualitative Summary

| Dimension | V1 | V2 | V3 | V4 | V5 |
|-----------|----|----|----|----|----|
| Completeness | 4/5 | 4/5 | 4/5 | 4/5 | 5/5 |
| Correctness | 2/5 | 5/5 | 4/5 | 4/5 | 4/5 |
| Structure | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 4/5 | 5/5 | 5/5 | 4/5 |
| Risk Coverage | 4/5 | 3/5 | 4/5 | 3/5 | 4/5 |
| Invariant and Edge Case | 5/5 | 5/5 | 5/5 | 3/5 | 5/5 |
| **qual_score** | **25/30 = 0.833** | **26/30 = 0.867** | **27/30 = 0.900** | **24/30 = 0.800** | **27/30 = 0.900** |

Cross-check: the final matrix was rebuilt here from the pass 2 matrix plus the 14 final verdicts (pass 2 totals 25, 25, 26, 24, 25; the 14 final verdicts move V2 by +1 (K1 +1, K4 +1, L1 -1), V3 by +1 (K1), V5 by +2 (C4, K2); V1 and V4 unchanged). Result 25, 26, 27, 24, 27 matches `step3-reevaluation.md` "Effect on the qualitative totals". Second route from pass 1 (totals 25, 25, 27, 23, 27): the 8 pairs where the final differs from pass 1 are C1 for V1, V3, V4 (each -1) and L4 for V1, V2, V3, V4 (each +1) and R5 for V4 (+1), giving V1 25, V2 26, V3 27, V4 24, V5 27. Both routes agree.

## Position-Bias Mitigation

Pass 1 evaluated V1 to V5; pass 2 evaluated V5 to V1. The passes produced 150 criterion-variant verdicts each. They agreed on 136 and disagreed on 14 (14 of 150 = 9.3 percent). Each disagreement was re-evaluated against one stated standard per criterion (`step3-reevaluation.md` "Standards applied"); the re-evaluation verdict is final (protocol A.5). Direction of the bias: pass 1 was too lenient on C1 (it did not charge the missing built-observer half) and too strict on L4 and R5; pass 2 was too strict on K1, K2, K4 and C4 (it counted withdrawn recommendations, hedged inferences and wording concessions as errors) and missed one unlabelled hedge (L1, V2).

| # | Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Decisive evidence |
|---|-----------|---------|--------|--------|-----------|-------|-------------------|
| 1 | C1 all explicit requirements | V1 | MET | NOT MET | DISAGREE | **NOT MET** | Subject is #409 and its work, yet "C-03 No observer code exists" is marked Verified; scope read lists PR #539, #541, #532, no PR #503 or #514; `observe` appears nowhere. R2-V1 row 1: "Concede in full." |
| 2 | C1 | V3 | MET | NOT MET | DISAGREE | **NOT MET** | Never determined what "TUI Panel" is; F5 ends "UNVERIFIED"; R2-V3 row 6: "Concede." Coder#477 half is complete, the observer half is absent. |
| 3 | C1 | V4 | MET | NOT MET | DISAGREE | **NOT MET** | "Not done: no read of #409's design branch"; proposal (b) judged against an issue sentence, not the built observer; R2-V4 row 1: "Concede in full ... Edit 3 is withdrawn". |
| 4 | C4 success criteria | V5 | MET | NOT MET | DISAGREE | **MET** | D1 contract content list, optional join-key check, and the gate "settle D5 and D6 before anything else is built"; at least as concrete as the agreed MET for V2 "Done when 0". |
| 5 | K1 no factual errors | V2 | MET | NOT MET | DISAGREE | **MET** | No stated fact disproved; the four Round 2 concessions are wording, a labelled inference, citation drift and a conditional. R2-V2 re-ran the live check and found no Run key on any agent row. |
| 6 | K1 | V3 | MET | NOT MET | DISAGREE | **MET** | Findings hold (5 of 8 paths omit `image/`, F1 listener vs poller, F6, F8, F14); the conceded items sit inside proposed text (Edit 5, Edit 8) and are scored under K2. |
| 7 | K2 feasible approach | V5 | MET | NOT MET | DISAGREE | **MET** | Recommended approach "(a) now, (b) later and only if wanted" is first-step "one short relationship note"; persist-now and D5(ii) were withdrawn for risk, not impossibility. |
| 8 | K4 no contradictions | V2 | MET | NOT MET | DISAGREE | **MET** | "No Run and no Dispatch row" concerns the bound-Run question; "UNVERIFIED that Orca writes no Run record at all" concerns any Run record; both can be true. A confidence lapse, not a contradiction. |
| 9 | L1 unambiguous language | V2 | NOT MET | MET | DISAGREE | **NOT MET** | "so a registered watcher worktree is very likely scanned" carries no UNVERIFIED label and Fact 5 and W-05 rest on it; V3, V4, V5 hedges are labelled. |
| 10 | L4 terms defined | V1 | NOT MET | MET | DISAGREE | **MET** | "WC-16 is a cap (at most once per 5 minutes) on coordinator wakes" (F-12), "SP-22: person deletes by hand" (F-03); stray ids sit in citation cells. |
| 11 | L4 | V2 | NOT MET | MET | DISAGREE | **MET** | "FU-1 live test (a claim on a test issue)", "path A ... path B" (W-03), ship gate named by role (W-02). |
| 12 | L4 | V3 | NOT MET | MET | DISAGREE | **MET** | "D1 option A 'No listener, inbound port or address registry'", AC ids quoted with text in F1, "the monitor" flagged as undefined in F3. |
| 13 | L4 | V4 | NOT MET | MET | DISAGREE | **MET** | "WC-12 (:61, pulled not pushed)", "WC-13 (:62 ...)", "WC-16 ... only on PR #539"; F22 defines "Orchestrator". |
| 14 | R5 monitoring or validation | V4 | NOT MET | MET | DISAGREE | **MET** | F6 gates #423 on "the #534 live read-only capture"; Edit 2 repeats it; F21 shows an `ls` check. Same bar as V5 `observe --once` comparison and V1 "Test the 80 and 100 session scenarios". |

Pass columns follow `step3-disagreements.md` and `step3-reevaluation.md` (pass 1 = forward, pass 2 = reverse); they agree with each other on all 14 rows.

Disagreements re-evaluated: 14 of 150 (9.3 percent).
Final verdicts changed relative to pass 1 (forward): 8 (rows 1, 2, 3 MET to NOT MET; rows 10, 11, 12, 13, 14 NOT MET to MET).
Final verdicts changed relative to pass 2 (reverse): 6 (rows 4, 5, 6, 7, 8 NOT MET to MET; row 9 MET to NOT MET).
Final equal to pass 1: 6 (rows 4 to 9). Final equal to pass 2: 8 (rows 1, 2, 3, 10 to 14). No re-evaluation created a third verdict outside the two passes.

## Edge Case Floor Check

Dimension: Invariant and Edge Case Coverage (needs at least 1/5 to be eligible as base; protocol A.2).

| Variant | Invariant score | Eligible as base |
|---------|-----------------|------------------|
| V1 | 5/5 | yes |
| V2 | 5/5 | yes |
| V3 | 5/5 | yes |
| V4 | 3/5 | yes |
| V5 | 5/5 | yes |

No variant is under 1/5. The floor is not suspended and no warning is raised. V4's 3/5 reflects two real absences (I1 collection boundaries, I4 count divergence), not scoring severity.

## Combined Scoring

Combined = 0.50 x quant + 0.50 x qual. The Debate Tiebreaker column is the share of the 36 X and A diff points that each variant won in the Step 2 Scoring Matrix (`debate-transcript.md`, "Scoring Matrix", winner column, Round 2 modal winner for contested points).

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker (points won of 36) |
|---------|---------------|--------------|-----------------|--------------------------------------|
| V5 (built observer vs sweep) | 0.930 -> 0.4649 | 0.900 -> 0.4500 | **0.915** | 18 of 36 = 50.0% |
| V2 (#450 watcher) | 0.919 -> 0.4594 | 0.867 -> 0.4333 | **0.893** | 3 of 36 = 8.3% |
| V3 (Coder#477) | 0.876 -> 0.4379 | 0.900 -> 0.4500 | **0.888** | 0 of 36 = 0% |
| V4 (#423, #339 boundary) | 0.923 -> 0.4616 | 0.800 -> 0.4000 | **0.862** | 3 of 36 = 8.3% |
| V1 (#409 vs sweep) | 0.848 -> 0.4241 | 0.833 -> 0.4167 | **0.841** | 6 of 36 = 16.7% |

Arithmetic verified: V5 (0.9297 + 0.9000) / 2 = 0.9149; V2 (0.9187 + 0.8667) / 2 = 0.8927; V3 (0.8757 + 0.9000) / 2 = 0.8878; V4 (0.9232 + 0.8000) / 2 = 0.8616; V1 (0.8481 + 0.8333) / 2 = 0.8407. Rounded: 0.915, 0.893, 0.888, 0.862, 0.841, as in the brief.

Points not won by any variant in the matrix: 6 (A-005, A-011, X-009, X-019, X-020 labelled none or process, and A-009 "none, unresolved by evidence"). 18 + 6 + 3 + 3 + 6 = 36.

**Verification note on the tiebreaker figure.** The brief and `step3-quantitative.md` say "V5 won 24 of 36". That number is the Round 1 plurality count (a variant named as winner by at least 2 of the 5 advocates' own point tables; V1 11, V2 4, V3 2, V4 7, V5 24), not the Step 2 Scoring Matrix. Counting the winner column of the Scoring Matrix directly gives V5 18, V1 6, V2 3, V4 3, V3 0, none or process 6. The figure recorded above is the matrix count (18 of 36) because the protocol's tiebreaker is "won more diff points in Step 2". The outcome does not change under either measure: V5 beats V2 by 15 points on the matrix (24 versus 4 on the Round 1 count).

**Margin**: top two V5 0.915 and V2 0.893 differ by 0.022 (2.2 points on the 0 to 1 scale), below the 5 point threshold. V3 (0.888) is also within 0.05 of V5 (0.027); V4 (0.862) is 0.053 below V5 and out of range.
**Tiebreaker applied**: Yes, Level 1 (debate performance). V5 18 of 36 against V2 3 of 36 (and against V3 0 of 36). Levels 2 and 3 not needed. For the record the Level 2 count (correctness criteria met) is V5 4 of 5, V2 5 of 5, V3 4 of 5; it would favour V2 but is not reached because Level 1 is not tied.

### Robustness of the choice to the quant-detector scenarios

`step3-quantitative.md` section 5 shows the quant ranking of V5 versus V4 flips with the RC thresholds. Combined scores recomputed under all four scenarios (qual layer unchanged):

| Scenario | V5 | V2 | V3 | V4 | V1 | First | Margin to second |
|----------|----|----|----|----|----|-------|------------------|
| FINAL (reported) | 0.915 | 0.893 | 0.888 | 0.862 | 0.841 | V5 | 0.022 (V2) |
| S0 (first run, R3 at 8 markers only) | 0.892 | 0.869 | 0.865 | 0.862 | 0.818 | V5 | 0.022 (V2) |
| RELAXED | 0.923 | 0.893 | 0.888 | 0.862 | 0.873 | V5 | 0.030 (V2) |
| STRICT | 0.883 | 0.861 | 0.856 | 0.862 | 0.824 | V5 | 0.022 (V4) |

V5 is first in all four, the margin is under 0.05 in all four, and the Level 1 tiebreaker favours V5 in every pairing. The choice does not rest on the post-hoc R3 detector.

## Selected Base: Variant 5

Selected: **Variant 5** (review 05, "The built `superclaude observe` versus Orchestrator mode (#339)", `variant-5-original.md`).

### Selection Rationale

1. Highest combined score (0.915) and first in all four quant-detector scenarios; qual 27 of 30 (tied with V3); highest quant (0.930) and the only variant with full section coverage (8 of 8).
2. Won the tiebreaker decisively: 18 of 36 diff points in the Step 2 matrix against 3 for the nearest rival on combined score (V2). It owns the points that decided the debate: X-012 (the observer is built; 98 percent), X-013 (the observer does not read the sweep JSON; 95), A-003, A-014 (two JSON "v1"; 94), A-010, A-016, X-008, X-015, X-014, X-017, X-018.
3. Only variant to meet C1 (cover the built observer, the half the owner's "TUI Panel" comment asked about). V1, V3 and V4 each conceded the miss in Round 2; V2 conceded it too. Because the other four reviews judged alignment against an observer that exists only in their premises, V5 is the only structurally correct base for a document the owner and a downstream `/sc:brainstorm` will rely on.
4. Its Round 2 section 5 is the only worked integration contract in the folder (owner and location, units, publication rules, versioning, mapping table, `check` and `projection.attention`, merge-order first steps). Three other variants' proposals (V3's status record, V4's field list, V1's mapping table) depend on it.
5. Survival after Round 2 is high (strict 0.974, weighted 0.941), and the losses are specific and already conceded by its own advocate (O-05, BC-17 as worded, D5(ii), persist-now, X-019, X-020), so they are repairable in the merge rather than structural.
6. Why not V2 or V3 (the nearest scores): V2 scores 5 of 5 on Correctness after re-evaluation and has the best SR, but reviews one subject (the watcher), has an unlabelled hedge (L1, re-evaluation row 9) and no recovery step (R3), and wins only 3 of 36 matrix points; V3 ties V5 on qual (27) but wins 0 of 36 matrix points and was never the sole winner of a contested point. Neither covers the observer half (C1).

Known weaknesses of the base the merge must repair (from the debate, not new findings): L4 NOT MET (TUIBBS, QUESTION-OBSERVATION and WC-16 used without a gloss); K1 NOT MET (O-05 withdrawn, BC-17 withdrawn as worded, X-019 and X-020 slips, "CLOSED" headline for F-04 holds for the Orca ledger only); silent on the watcher, trust and v2 (scope limit); the owner records it relies on are not on master (A-015, INV-002); its D5(ii) recommendation and "persist now" were withdrawn.

### Strengths to Preserve from Base

1. The corrected state of the observer: S1 releases table (PR #503 `9e2608b03` 2026-11-11, PR #514 `cd8736199` 2026-11-12, the unpushed flip commits `1ae72e1a1` and `f104ca51a`), S2 registration (`main.py:572-574`), S3 the three argv shapes and caps, S5 snapshot v1 fields, S8 what "live read off" means and the flip rule, S9 who decided what, S10 what is next.
2. The overlap table O-01 to O-16 (minus O-05's verdict and wording) and the "Facts each program owns" table.
3. The re-test of review 01 findings F-01 to F-18 (RT-F01..RT-F18), with F-04 qualified as "closed for the Orca ledger on one host".
4. The 23 exact-wording corrections to the #409 body (BC-01..BC-23), as changed by the debate (see refactor plan Part 6).
5. Decisions D1 to D9, each with options, recommendation and smallest reversible first step, and the dependency table.
6. Round 2 section 5: contract note content, versioning rule, mapping table, merge-order table 5.9.
7. Its habit of labelling what it did not run or read (UNVERIFIED; "Unverified and not claimed" list).

### Strengths to Incorporate from Non-Base Variants

1. **From V1** (`variant-1-original.md`, `round2-rebuttal-V1.md`): F-07 and C-18 (the `git status` environment hole, the origin of the open security thread and of INV-008); C-07 (PR #539 thread and CI state), C-25 (`policy` IS a JSON row key; #409's "not keys in the JSON" is wrong), C-34 and W-7 (the decision-8 boundary sentence is not in the old or new body; relabel "proposed boundary"); F-02 (ten dimensions: only lifecycle, health, result, freshness and policy get values; `unknown` must never render as `not admitted`) as the base of the mapping table; F-05, F-08 to F-11, F-13, F-17, F-18 (sweep-side findings that survived); R2-V1 section 1 row 5 and the NFR-001 pins; R2-V1 section 5 item 5 (merge order and the record-path problem for the flip PR); A-011 mechanism.
2. **From V2** (`variant-2-original.md`, `round2-rebuttal-V2.md`): W-01 and W-02 (the watcher prompt runs the claim at default `worktree` level; ship gate), W-03, W-04 (as UNVERIFIED), W-09 (FU-1 capture items), W-05 (machine-started label, Phase 2 row), W-07 (watcher worktree owner), W-08, W-10 reworded to "no watcher panel in `observe` before FU-1", W-11 (`healthy` false on planned stops), W-12 (#450 item 4 done in #485), proposed edits 1 to 5 to #450; R2-V2 sections 5.1 (permission boundary), 5.4 (double-launch, `reset --forfeit-guarantee`), 5.6 (what the FU-1 test writes); the point that "read-only" must be a per-caller verb list because the watcher is a third Orca caller.
3. **From V3** (`variant-3-original.md`, `round2-rebuttal-V3.md`): F1 (a listener is not needed under watcher option A), F2, F6 (workspace lifecycle and the Minimal profile), F8 (a listener is a second command channel into bypass sessions), F10 to F14 (credential rule, trust criteria against #339, anonymous heartbeat collector), F17; R2-V3 5.1 to 5.5 (listener under option A, "TUI Panel" estimate 75 percent and 15 percent, allowed and never-exposed fields, identity from Coder not from self-registration, bypass default); 5.6 A, B, C (exact Coder#477 rewrites: narrow, keep, close comment); 5.7 checklist.
4. **From V4** (`variant-4-original.md`, `round2-rebuttal-V4.md`): F1 and F7 (#423 gate and per-class acceptance criteria), F14 (determinism boundary, LLM entries marked inferred), F9 (one grant vocabulary, as the owner-decision default for X-005); R2-V4 5.1 (three meanings of "v1" and "v2"), 5.2 (a catalogue is at least an eighth data store), 5.3 to 5.5 (who may read whose sessions, untrusted relay, guards at the v1/v2 boundary), 5.6 checklist, 5.7 (the #423 rewrite and the #339 comment, with its four corrections); A-011 cross-issue edit order.
