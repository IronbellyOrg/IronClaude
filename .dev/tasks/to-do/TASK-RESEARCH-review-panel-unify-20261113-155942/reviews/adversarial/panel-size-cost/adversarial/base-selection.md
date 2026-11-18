# Base Selection Report

<!-- Header and quantitative layer first; qualitative, position-bias, combined scoring and selection are appended in order. -->

Variants: **Variant A** = Proposal A (`variant-1-original.md`, Option A, "default to two reviewers now"); **Variant B** = Proposal B (`variant-2-original.md`, Option B, "fix the rubric first, keep 3, decide the count after H-A"). Scoring input is the variants AS WRITTEN; claims the debate showed to be false count against the variant that made them.

## Quantitative Scoring (50% weight)

Computed by `adversarial/quant_score.py` (read-only, run with `uv run python`; identical output on repeated runs, md5 checked). No formal requirement ids exist in the source, so requirement coverage uses the section-level topic edge case against 16 requirement topics taken from the C-14 block and the task statement. The requirement keyword list was amended once after the first run because the R13 (reversibility) keywords missed Variant B's wording ("text revert", "kill switch"); first run: A 0.9722, B 0.9323 (B RC 0.875); amended run: A 0.9722, B 0.9511. The amendment fixed a keyword-list defect that penalised B and was not tuned toward any winner.

| Metric | Weight | Variant A | Variant B |
|--------|--------|-----------|-----------|
| requirement_coverage | 0.30 | 1.0000 (16 of 16 topics) | 0.9375 (15 of 16; misses R14 executor-class exclusion) |
| internal_consistency | 0.25 | 0.8889 (6 contradicted claims of 54 scorable claims) | 0.9394 (4 contradicted claims of 66 scorable claims) |
| specificity_ratio | 0.15 | 1.0000 (404 concrete, 0 vague) | 1.0000 (537 concrete, 0 vague) |
| dependency_completeness | 0.15 | 1.0000 (49 of 49 internal references resolve) | 0.9000 (9 of 10) |
| section_coverage | 0.15 | 1.0000 (7 of max 7 H2) | 1.0000 (7 of max 7 H2) |
| **quant_score** | | **0.9722** | **0.9511** |

Contradicted claims counted for IC (fixed list in the script, taken from the debate): A: A1 "through the parsed-sparse pre-filter"; A8 B removes Tier 2 for "up to 34-35"; section 2 table "up to 34-35 of 38-39"; section 2 table "saves a whole Tier 2 run on 35 of 39"; A9 "cannot be rolled back by data alone"; the Design "no new code" omission of the `SKILL.md:340` shadow-parity coupling and of the task-builder blocking POST gate. B: E-5 "at most 5" and "row 8: 1 clear-cut"; E-6 "clear-cut flag-only run"; R1 "up to 13 percent"; the Phase 1 / G1 branch that cannot open on any recorded data.

Limits of this layer, stated plainly: specificity does not discriminate (both variants score 1.0 because neither contains a listed vague phrase); the contradiction list is a judgment taken from the debate, not an automatic scan; requirement coverage rewards mentioning a topic, not handling it correctly. The quant layer favours A by 0.0211.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Two independent scorer agents ran the 30-criterion rubric with CEV citations. Pass 1 evaluated A then B; pass 2 evaluated B then A. The tables below show the FINAL verdict after the position-bias step (see the next section for the two disagreements). Evidence is condensed from the scorers' CEV lines.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| C1 covers all explicit requirements | MET | Design, Evidence A1-A9/C1-C5, Cost, R1-R8, Tests | MET | Design table, E-1..E-18, Cost, Risks, Tests N1-N6 |
| C2 edge cases and failure scenarios | MET | R2 no slack, R3 executor equals second slot, R5 gateway collapse, floor rule | MET | R1, R2, E-6, "not evaluable", G1-fails branch |
| C3 dependencies and prerequisites | MET | R5 "should not ship ahead of the shadow path recording it", G-59, owner decisions 1-4 | MET | Correctness 6 (no open-conflict dependency), N6 harness fixes, H-A pilot prerequisite |
| C4 success/completion criteria | NOT MET | No success criterion for the default; rollback trigger left to the owner (R1) | MET | G1 "at least three clear-cut candidates and none shows a Tier 2-only blocker"; count rule "within 10 points ... and cheaper" |
| C5 out of scope | MET | "Out of scope but flagged" (document-loop `default` and `live7`) | MET | "Out of scope for C14 under B"; rows 3-7 unchanged |
| **Subtotal** | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| K1 no factual errors | NOT MET | A1 "35 of them through the parsed-sparse pre-filter", A8 and section 2 "up to 34-35" are false (flag decisive in 0 certain, at most 1 of 39); A9 overstated; "rf-qa already runs as a pair" overstated; engine default reaches the blocking post gate unflagged | NOT MET | E-5 / R1 "1 certain, at most 5 (13 percent)" overstated; E-6 "clear-cut" run refuted by its own `reflection-card.yaml` (C 0.68); "only advisory consumers" omits the task-builder blocking POST gate (INV-012) |
| K2 approach feasible | MET (after re-evaluation) | Two-slot templates legal (`panel.py:37-46`); executor-keyed table reproduced by two independent dry runs | MET | Read-only replay script, text edit with `--tier 2` kill switch, "not evaluable" never guessed |
| K3 terminology consistent | MET | "cap is the ceiling, the default is what drops" held throughout | MET | "cap 3" scoped to the reflect profile and `N_eff` (R6) |
| K4 no internal contradictions | MET | None found (disclosed trade-offs only) | MET | Phases, G1 and "closer to Option C" agree; E-5 table sums |
| K5 claims supported | MET | Every item carries a file:line or `CR:n` citation (the A1 recount is cited, not shown, and is wrong) | MET | Every E-n item carries a citation; E-5 table shown; model-written-field caveat stated |
| **Subtotal** | **4/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| S1 logical ordering | MET | Design, How it works, Evidence, Correctness, Risks, Tests, Cost | MET | Same order |
| S2 consistent depth | MET | H2 with H3 | MET | H2 with H3 |
| S3 separation of concerns | MET | Supports versus "What cuts against it"; risks and tests separate | MET | Evidence by subject; weakest point under its own heading |
| S4 navigation aids | MET | Citation key, tags, "see Risks, R3" | MET | Citation forms, tag legend, E-n cross-references |
| S5 artifact-type conventions | MET | All seven proposal sections | MET | All seven proposal sections |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| L1 unambiguous | MET | "`--reviewers` defaults to 2 instead of 3 (`SKILL.md:86`, `commands/reflect.md:100`)" | MET | "One-sentence position"; exact `sparse_flag_decisive` definition |
| L2 concrete | MET | Executor-class table, "5 one-line edits", named tests | MET | Named files, line numbers, `uv run` command, key names |
| L3 clear section purpose | MET | "Correctness argument ... three parts"; "weakest point" flagged | MET | "What the design decides", "The three phases", "Gate G1" |
| L4 terms defined on first use | NOT MET | O-8, H-A, UC-1/UC-2, EV-1, D3/D5, G-67, G-59 used undefined | NOT MET (after re-evaluation) | O-8 in the title and D13 at the first design row used undefined; H-A is glossed on line 4 but O-8, D13, UC-1 are not |
| L5 actionable next steps | MET | "Owner decisions this needs (1)-(4)" | MET | Phase 0/1/2, "G1 is an owner decision", numbered count rule |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| R1 at least 3 risks with probability and impact | NOT MET | R1-R8 give evidence and residuals but no probability or impact ratings | NOT MET | R1-R9 likewise; the only figure ("up to 13 percent") is wrong |
| R2 mitigation for each risk | MET | Mitigation column filled for R1-R8 | MET | Mitigation filled for R1-R9 |
| R3 failure modes and recovery | MET | Floor rule: `single-reviewer-fallback`, DEGRADED, one re-dispatch; "Reverting is the same edit backwards" | MET | Text revert, `--tier 2` kill switch, G1-fails path |
| R4 external dependencies | MET | R5 gateway served-model collapse; E2 pinned commit; low-reliability external sources | MET | R8 pilot unfunded; N6 harness portability; E-18 weak sources |
| R5 monitoring or validation | MET | `panel_shortfall`, `reviewers_default_applied`, R6 calls before and after, R7 convergence by count | MET | Audit keys, replay script, G1 table, N5 strata |
| **Subtotal** | **4/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| I1 collection boundaries | MET | Fewer than two cards degrades; clamp `[2,4]` to `[2,3]`; pool of 2 `ModelPoolTooSmallError`; executor sonnet exhausts `tier1b` | MET | `coverage_pct` null when no ids parsed (0/0 must not pass); cap 3; shadow dirs skipped |
| I2 state interactions across boundaries | MET | `reviewers_requested/resolved`, EV-1 `max(2, resolved)`, exit-gate shortfall rule | MET | `coverage_degraded` versus parsed `coverage_pct` versus `coverage_pct_union`; audit keys versus contract 1.8.0 |
| I3 guard-condition gaps | MET | R3 bare two-slot template has no slack; re-dispatch lapse caveat; G-67 | MET | E-8 nothing pins the pre-filter; N3 limit "pins prose"; R2 under-extraction |
| I4 count divergence | MET | G-67 clamp 4 versus cap 3; default in four places with pin test 8; "2-of-3" label | MET | E-3 clamp 4 versus cap 3 versus document default 4; E-5 counts reconciled |
| I5 interaction effects | MET | R8 exit gate built around 3; R5 diversity collapse; R7 convergence at two variants | MET | R4 Phase 1 changes H-A strata; R5 versus Stage 2 count; pin precedence |
| **Subtotal** | **5/5** | | **5/5** | |

(Invariant coverage here scores what each document states. The independent probe found gaps neither document lists, for example the hard-coded three-card `--compare` list, the task-builder blocking POST gate and the unobservable tripwire; those are recorded in `invariant-probe.md` and are not double-counted in this rubric.)

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 4/5 | 5/5 |
| Correctness | 4/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 |
| Invariant & Edge Case | 5/5 | 5/5 |
| **qual_score** | **26/30 = 0.8667** | **27/30 = 0.9000** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Floor (at least 1/5) | Eligible as base |
|---------|-----------------------------|----------------------|------------------|
| A | 5/5 | pass | yes |
| B | 5/5 | pass | yes |

## Position-Bias Mitigation

Pass 1 (order A, B) totals: A 26/30, B 28/30. Pass 2 (order B, A) totals: A 25/30, B 27/30. Both orders rank B above A by two points, so no order effect favours either variant. The passes agreed on 58 of 60 criterion-variant verdicts and disagreed on two.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| K2 technical approach feasible | A | MET | NOT MET (pass 2 cited the hard-coded three-card `--compare` list at `SKILL.md:695`, INV-004) | DISAGREE | MET |
| L4 terms defined on first use | B | MET (H-A glossed on line 4) | NOT MET (O-8, D13, UC-1, G-67 undefined) | DISAGREE | NOT MET |

Re-evaluation (orchestrator, with both passes' evidence in hand; verdicts final):
- **A.K2: MET.** The criterion asks whether the approach is feasible under its stated constraints. Two-slot templates are already legal (`panel.py:37-46`) and the executor-keyed resolution table was reproduced by two independent dry runs (debate C-005). The missed hard-coded `--compare` list is a missing edit, not an infeasible design; it is recorded as INV-004 and A's factual errors are already penalised under K1, so counting it again here would double-penalise.
- **B.L4: NOT MET.** Both scorers marked A's L4 NOT MET for undefined O-8, D13, UC-1/UC-2, G-67 and E2. Variant B has the same gap (O-8 sits in its title and D13 in its first design row, with no definition), so the same standard applies. The verdict follows the stricter, consistent reading.

Disagreements found: 2. Verdicts changed from either pass: 2 (A.K2 from pass 2; B.L4 from pass 1).

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate points won (tiebreaker) |
|---------|---------------|--------------|-----------------|--------------------------------|
| A (Proposal A, two reviewers now) | 0.4861 | 0.4333 | **0.9194** | 4 |
| B (Proposal B, rubric first, keep 3) | 0.4756 | 0.4500 | **0.9256** | 6 |

**Margin**: 0.0061 (0.6 percentage points), below the 5 percent threshold.
**Tiebreaker applied**: Yes, level 1 (debate performance). Points won in the Step 2 scoring matrix: B 6 (S-004, C-002, C-007, X-001, X-002, X-003), A 4 (S-003, C-012, C-014, A-003); the other 14 resolved points went to MERGE and 6 were unresolved. B leads by 2 of 10 contested points (a 20 percent difference), which is outside the 5 percent band, so level 2 and level 3 were not needed.

Sensitivity (to show the result does not hinge on the two re-evaluations): with A.K2 left NOT MET and B.L4 left MET (the opposite ruling on both), A = 0.9028 and B = 0.9422; with both rulings as made, A = 0.9194 and B = 0.9256; with only A.K2 at its pass 1 value and B.L4 at its pass 2 value (the ruled case) the scores are those in the table. B stays ahead of A in every combination, but by under 5 percent in the ruled case, so the outcome there rests on the tiebreaker, not on the scores alone.

Caveats the owner should weigh:
1. The scores are a near tie: A leads the quantitative layer by 0.021 (requirement coverage and executor-class exclusion), B leads the qualitative layer by 0.033 (success criteria and one fewer contradicted claim set).
2. The tiebreaker's six B wins are all premise-correction points (the escalation figure, the rollback claim, what B ships while G1 is closed, shadow staying at 3). They show B was more right about the facts. They do not show B's design delivers more. The 14 MERGE points are where the two designs complement each other.
3. After Round 2 both advocates, and the Round 2 reading of the evidence, favoured the narrowed "A-min" (skill-path default of 2) as the base of a merge. The protocol selects the base by score, so the base is B. The refactor plan therefore carries A-min into the merged proposal as the main incorporated change, with the conditions the invariant probe added; the tension is recorded here and in the merge log, not hidden.

## Selected Base: Variant B (Proposal B, Option B: "fix the rubric first, keep the cap at 3, decide the count after H-A")

### Selection Rationale
B scored 0.9256 against A's 0.9194; the 0.6-point margin is inside the 5 percent band, and level 1 of the tiebreaker (debate performance, 6 points to 4) selects B. B's qualitative edge comes from a stated completion criterion (G1 and the pre-registered count rule), a Citation forms key and an exposure map that the debate re-verified (the post gate does not read the rubric). B also made the one correction the whole debate turned on (the flag is not the cost driver), and its own text already said its result was "closer to Option C", which the recount confirmed.

### Strengths to Preserve from Base (B)
1. The corrected cost attribution method (recount by escalation path) and the table-wide recount warning for documents that repeat "34 of 38".
2. The exposure map: which consumers can see a rubric change and the finding that the blocking post gate does not read the rubric (extended by INV-012: the task-builder POST gate is a second, skill-path blocking consumer).
3. E-8: nothing under `tests/` pins the pre-filter or `tier_decision.yaml`.
4. Phase 2: a pre-registered count rule (made symmetric: T1, T2 with 2, T2 with 3, owner-set margin, inconclusive outcome stated in advance).
5. Phase 0 kept only as prospective audit keys (all matching rows, blind-calibrated C, `S_domains`, `tier_without_flag`), aimed at rows 4 and 6.
6. B's honesty pattern: weakest point first, residual risks in the table.

### Strengths to Incorporate from Non-Base Variant (A)
1. The narrowed A-min change: skill-path default of 2 with `--reviewers 3` and `--strategy enterprise` as opt-ins (debate C-001, C-014; conditions from INV-001, INV-004, INV-009, INV-012).
2. The floor rule and one bounded re-dispatch (C-004), the N=2 mirror of `test_i5`, and the EV-1 test for a two-resolved run with one card.
3. The executor-class resolution table and the in-memory dry run (C-005), parked for the Stage 3 panel engine.
4. The invariants-preserved table (S-003) and the "does not claim" list (U-005).
5. The telemetry keys, re-specified as three fields (requested, resolved, source) per INV-002.
6. Closing G-67 (clamp) as a separate item owned by C17, and the shadow exit rule generalisation when the count changes (C-006, C-007).
7. The spec-body single-point-of-failure observation (U-006) and the calibrator-disjointness argument (new in Round 2, with the executor-collision limit).

### Weaknesses of the Base That the Plan Must Address
1. Phase 1 (flag advisory) is empty on recorded data (0 certain, at most 1 of 39) and G1 has no candidates: drop it from the committed scope and keep it only as a conditional item behind the prospective keys.
2. B's "count must wait" premise fails: about a quarter of recorded Tier 2 runs already ran two cards (executor exclusion 2, deliberate 1, missing card 1, unstated 5). Replace it with "the default of two is an owner decision before H-A, with a tripwire and a pilot".
3. B's retrospective replay script and its tests N1/N2 re-derive a number that is now known; do not build them. N2 as written asserts counts that are wrong.
4. B's 10-point count margin was invented; make it an owner-set parameter.
5. B's "only advisory consumers" claim omits the task-builder POST gate (INV-012).
