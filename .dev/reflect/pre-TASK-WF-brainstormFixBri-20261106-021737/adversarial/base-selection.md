# Base Selection Report

- Generated: 2026-11-06T04:12Z (Step 3 of /sc:adversarial, Mode A, `--depth standard`)
- Variants: V1 = reviewer-1 card (analyzer, sonnet), V2 = reviewer-2 card (qa, haiku slot), V3 = reviewer-3 card (refactorer, opus). Files: `variant-1-original.md`, `variant-2-original.md`, `variant-3-original.md` (this folder).
- Blind-calibrated confidence (`../artifacts/calibration.yaml`): V1 0.73, V2 0.73, V3 0.75.
- Inputs: `diff-analysis.md`, `debate-transcript.md` (Round 1, Round 2, scoring matrix, convergence 88.5%, status BLOCKED_BY_INVARIANTS on INV-019), `invariant-probe.md`.
- The artifact being merged is a plan-audit card. The merged output is one consolidated verdict card on the plan `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md` ("plan") against its brief `source.md` in the same folder ("brief").

## How the scoring was adapted to a plan-audit card

The protocol (`refs/scoring-protocol.md` A.1-A.5) scores documents with requirement IDs and H2 sections. A reviewer card is a short YAML list of findings, so each metric was mapped as follows.

| Metric | Protocol meaning | Meaning used here |
|---|---|---|
| RC | Source requirements referenced | Share of 31 items the card addresses **correctly after the debate**: the 26 scored diff points (S 2, C 14, X 5, A 5) plus the 5 work items of brief Part 1. Credit 1 = the card took a position the Round 2 resolution upholds; 0.5 = the card is named in a `split` resolution, or the resolution credits it for a sub-point only; 0 = silent, or the position was withdrawn or shown wrong. |
| IC | 1 - contradictions / claims | Claims = findings + `card_claims_disputed` entries. A claim counts as contradicted when the debate withdrew it, conceded it factually wrong, conceded its tag wrong, or lowered it across the P1/P2 line. A P2-to-P3 calibration alone does not count. |
| SR | Concrete / (concrete + vague) | Sentence-level over claim and dispute text (sentences of 4+ words). Concrete = holds a digit, backtick, quote, path, or a WC-/F-/P- id. Vague = holds one of: may, might, could, plausibly, possibly, unquantified, not verified, depends on, some, various, etc, appropriate, properly, adequate. A sentence can count in both. Computed by script. |
| DC | Internal references resolved | Internal finding-ID cross-references **plus** evidence `file:line` refs that resolve to an existing file with that many lines. For a card the evidence refs are its dependencies; their truth is scored in IC, their existence here. |
| SC | H2 sections / max | All three cards have the same six top-level keys (SC would be 1.0 for all and tell nothing), so SC = findings count / max findings count (8, V3). |

Qualitative criteria keep their protocol wording; the CEV evidence column states how each was read for a card. The edge-case floor (Invariant and Edge Case dimension >= 1/5) applies unchanged.

## Quantitative Scoring (50% weight)

### RC detail (31 items)

| Item | V1 | V2 | V3 | Basis (Round 2 resolution) |
|---|---|---|---|---|
| S-001 | 1 | 0 | 0 | none won; "no P1 survives": V1 filed 0 P1, V2 and V3 filed P1s that were conceded |
| S-002 | 1 | 0 | 0 | V1 unanimous (honest INFERRED tags) |
| C-001 | 1 | 0 | 1 | V3 on evidence; V1 credited for severity P2 and fix shape |
| C-002 | 0.5 | 0.5 | 0 | split (V2 recording, V1 severity) |
| C-003 | 0.5 | 1 | 0 | V2; A2 credits V1 for the sync-dev "only" point |
| C-004 | 1 | 0 | 0 | V1 unanimous; R3-2 withdrawn; V2's exposure conceded small |
| C-005 | 1 | 0 | 0 | V1 only raiser, narrowed to Task 4 routing half |
| C-006 | 1 | 0 | 0 | V1 only raiser (format-check part) |
| C-007 | 0 | 0 | 0.5 | split (V3 found it, severity P3) |
| C-008 | 0 | 0 | 1 | V3 |
| C-009 | 0 | 0 | 1 | V3 |
| C-010 | 0 | 0 | 1 | V3 |
| C-011 | 0 | 0 | 0 | none; R3-7 withdrawn; silence earns no credit |
| C-012 | 0 | 1 | 0 | V2 |
| C-013 | 1 | 1 | 0 | none (cosmetic); V1 A-6 and V2 R2-4 state the fact correctly |
| C-014 | 1 | 1 | 1 | all three confirm |
| X-001 | 1 | 0 | 1 | V3 on evidence at P2; V1's stance (P2, INFERRED failure) is the resolved one |
| X-002 | 1 | 0 | 0 | V1 |
| X-003 | 0.5 | 0.5 | 0 | split |
| X-004 | 0.5 | 1 | 0 | V2; V1's "false as written" point re-owned to the brief |
| X-005 | 1 | 0 | 0 | V1 majority |
| A-001 | 1 | 0 | 1 | QUALIFY: V1 A-2 and V3 R3-1 both name the refused and timed-out cases |
| A-002 | 1 | 0 | 0 | QUALIFY: V1 treats the F-16 departure as a nit; V2 treated the brief verifier as a P1 blocker; V3 silent |
| A-003 | 1 | 0 | 0.5 | QUALIFY: V1 A-5 checked the index; V3 R3-2 named the state dependence but on a false premise |
| A-004 | 1 | 1 | 1 | ACCEPT, all three |
| A-005 | 1 | 0.5 | 0 | QUALIFY (note-level gap): V1 rates it a nit; V2 right on recording, wrong as P1 |
| Brief item 1 (wording in skill, command, ref) | 1 | 1 | 1 | V1 A-2, A-7; V2 R2-5 (applied text byte for byte); V3 R3-1, R3-5, R3-8 |
| Brief item 2 (tests pin the wording) | 1 | 1 | 1 | V1 A-1, A-7; V2 disputes list (test anchors confirmed); V3 R3-8 |
| Brief item 3 (sync-dev, verify-sync, plugin mirror) | 1 | 1 | 0 | V1 A-3, A-4; V2 R2-2 (sync-dev rewrites `.claude/`); V3 silent |
| Brief item 4 (live-check wording in the spec) | 1 | 1 | 1 | V1 A-2, A-6; V2 R2-4; V3 R3-1, R3-3, R3-4, R3-6 |
| Brief item 5 (run tests and make lint) | 1 | 0 | 0 | V1 A-3 only |
| **Total** | **23** | **11.5** | **12** | of 31 |

### IC detail

| Card | Claims | Contradicted (debate reference) | IC |
|---|---|---|---|
| V1 | 11 (A-1..A-7, 4 disputes) | A-1 Task 5 half withdrawn (R2-A1 row 6); A-2 tag wrong for the text conflict (R2-A1 row 1); A-3 exit-code part conceded weak (R2-A1 row 9); dispute 4 "plan's wording is the correct one" conceded overstated (R2-A1 row 5) | 7/11 = 0.636 |
| V2 | 8 (R2-1..R2-5, 3 disputes) | R2-1 P1 conceded and "drops the motivating scenario" withdrawn (R2-A2 rows 1, 3); R2-3 tag Grounded conceded INFERRED, exposure small (R2-A2 row 4) | 6/8 = 0.750 |
| V3 | 11 (R3-1..R3-8, 3 disputes) | R3-1 P1 conceded to P2, failure tag conceded INFERRED, remedy withdrawn (R2-A3 rows 1-3); R3-2 withdrawn, premise false (row 4); R3-7 withdrawn to nit (row 7); dispute "R3-1 and R3-2 are P1" (rows 1, 4) | 7/11 = 0.636 |

### Score table

| Metric | Weight | V1 (analyzer/sonnet) | V2 (qa/haiku slot) | V3 (refactorer/opus) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.742 (23/31) | 0.371 (11.5/31) | 0.387 (12/31) |
| internal_consistency | 0.25 | 0.636 (4 of 11 contradicted) | 0.750 (2 of 8) | 0.636 (4 of 11) |
| specificity_ratio | 0.15 | 0.893 (25 concrete, 3 vague, 26 sentences) | 0.950 (19, 1, 22) | 0.913 (21, 2, 29) |
| dependency_completeness | 0.15 | 0.966 (28/29; A-5's "index check" names no file) | 1.000 (14/14) | 1.000 (31/31; one compound ref "plan:38,54,69,122,128 vs source.md:229,230,231,221,217" resolved by hand) |
| section_coverage (findings) | 0.15 | 0.875 (7/8) | 0.625 (5/8) | 1.000 (8/8) |
| **quant_score** | | **0.792** | **0.685** | **0.712** |

Arithmetic: V1 = 0.30(0.7419) + 0.25(0.6364) + 0.15(0.8929) + 0.15(0.9655) + 0.15(0.875) = 0.2226 + 0.1591 + 0.1339 + 0.1448 + 0.1313 = 0.7917. V2 = 0.1113 + 0.1875 + 0.1425 + 0.1500 + 0.0938 = 0.6850. V3 = 0.1161 + 0.1591 + 0.1370 + 0.1500 + 0.1500 = 0.7122.

## Qualitative Scoring (50% weight): Additive Binary Rubric

Final verdicts after both passes and re-evaluation (see Position-Bias Mitigation). Evidence cites the card IDs; "R2" = the Round 2 rebuttal files.

### Completeness (5 criteria)

| Criterion (card reading) | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. Covers all explicit requirements (all 5 brief Part 1 items) | MET | A-2, A-7 (item 1), A-1 (2), A-3/A-4 (3), A-2/A-6 (4), A-3 (5) | NOT MET | No finding on item 5 (tests/lint run); searched R2-1..R2-5 and disputes | NOT MET | No finding on items 3 and 5; searched R3-1..R3-8 |
| 2. Edge cases and failure scenarios | MET | A-2: "A call /sc:analyze refused, or that timed out before writing, leaves a listed path with no contract" | MET | R2-3: false FAIL from writes "under .dev/ outside the package" (kept as small, real) | MET | R3-1: refused directory, "no contract is written" |
| 3. Dependencies and prerequisites | MET | A-5: "The earlier package ...001016 is already in the index" | MET | R2-3: "The plan neither enumerates the executor's write locations" | MET | R3-7: Tasks 2, 3, 6 lack "Depends on: Task 1"; R3-2 names the index dependence |
| 4. Success / completion criteria (a pass condition or fix for its top findings) | MET | A-1: "require git show to exit 0 or print non-empty text"; A-3: "append `echo exit=$?`" | NOT MET | No fix or pass condition in any finding (conceded, R2-A2 row 8) | MET | R3-1: "The skill sentence should say the contract is listed when it was written" (present; its correctness is scored under Correctness 2) |
| 5. Out of scope / limits of evidence | MET | A-7: "No defect in the pins and slicing"; INFERRED tags on A-2, A-3, A-5 | MET | Disputes: "Not disputed: anchors match the files on disk ..."; R2-5 "not a plan failure" | MET | R3-8 "Confirmation, no defect"; R3-2 "neither was verified" |
| **Subtotal** | **5/5** | | **3/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. No factual errors | NOT MET | A-1 "Task 5's check has the same weakness": withdrawn, full path works (R2-A1 row 6) | NOT MET | R2-1 "drops F-16's motivating scenario": withdrawn (R2-A2 row 3) | MET | No stated fact withdrawn as false: R3-2 is explicitly conditional ("If the earlier package were untracked ... neither was verified"); R3-7 conditional ("run out of order") |
| 2. Approaches feasible within constraints | MET | A-1 full path + exit check; A-3 format check: both fit the six-file scope | NOT MET | No approach proposed | NOT MET | R3-1 reword breaks brief:225 and the AC at plan:45 (withdrawn, R2-A3 row 3) |
| 3. Terminology consistent | MET | Grounded/INFERRED, false FAIL / false-PASS used consistently | MET | "verifier", "departure", "necessary deviation" used consistently | MET | Grounded/INFERRED, "false FAIL" consistent |
| 4. No internal contradictions | MET | No two V1 claims conflict (A-5 and its F-3 dispute agree) | MET | R2-1 and R2-2 apply one standard (literal verifier, unrecorded departure) | NOT MET | R3-8 praises byte-for-byte Part 4 copying while R3-1 proposes departing from it (conceded, R2-A3 row 9) |
| 5. Claims supported by evidence | MET | Every finding carries evidence refs | MET | Every finding carries brief-vs-plan refs | MET | Every finding carries refs |
| **Subtotal** | **4/5** | | **3/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. Logical ordering (priority, confirmations last) | MET | All P2, confirmation A-7 last | MET | P1 R2-1 first | MET | P1s first, confirmation R3-8 last |
| 2. Consistent hierarchy (id, priority, tag, claim, evidence) | MET | All 7 findings | MET | All 5 | MET | All 8 |
| 3. Separation of concerns (one issue per finding) | NOT MET | A-3 bundles two defects (exit codes; missing format check), split apart by the debate (R2-A1 row 9) | MET | One issue each | MET | One issue each |
| 4. Navigation aids (cross-references) | MET | Disputes cite (A-5), (A-4), (A-2), (A-1), (A-3) | MET | Disputes cite (R2-1, R2-2) | MET | Disputes cite (R3-1), R3-2 |
| 5. Artifact-type conventions (reviewer card keys) | MET | reviewer, persona, model_class, self_confidence, findings, card_claims_disputed | MET | Same keys | MET | Same keys |
| **Subtotal** | **4/5** | | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. Unambiguous language (vague sentences <= 10%) | NOT MET | 3 of 26 = 11.5% (e.g. "could then fail a correct run", "depends on an unrun baseline") | MET | 1 of 22 = 4.5% | MET | 2 of 29 = 6.9% |
| 2. Concrete rather than abstract | MET | SR 0.893; exact commands and lines | MET | SR 0.950 | MET | SR 0.913 |
| 3. Each finding summarizable in one sentence | MET | Each claim opens with its thesis sentence | MET | Same | MET | Same |
| 4. Terms defined on first use | MET | "Correction F-13's verifier requires the literal sentence '...'" (quotes the term's content) | MET | R2-1 quotes the mandated F-16 line | MET | R3-1 "WC-4 defines artifacts as 'every other file written'" |
| 5. Actionable next steps | MET | A-1 "Spell out the full path"; A-3 "Say to append `echo exit=$?`" | NOT MET | No next step in any finding (R2-A2 row 8) | MET | R3-1 names the change |
| **Subtotal** | **4/5** | | **4/5** | | **5/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. >= 3 risks with likelihood and impact | MET | A-1 (vacuous pass, Grounded), A-2 (false FAIL, INFERRED, named triggers), A-5 (residual exposure: "any other untracked path") | NOT MET | R2-3 calls its own risk "unquantified"; R2-2, R2-4 state no impact | MET | R3-1 (refusal/timeout trigger), R3-2 (conditional), R3-3 ("correct only for --output briefs") |
| 2. Mitigation for each risk | NOT MET | A-2 and A-5 carry no mitigation | NOT MET | None | NOT MET | R3-2, R3-3, R3-4 carry none |
| 3. Failure modes and repair | MET | A-1 vacuous pass + repair | NOT MET | Failure mode named (R2-3), no repair | MET | R3-1 false FAIL + repair (wrong, but present) |
| 4. External dependencies and their failure | MET | A-3 ruff/CI pin (pyproject.toml:50-54), A-5 executor outputs | MET | R2-3 /sc:implement final review | MET | R3-6 session format tool names; R3-1 /sc:analyze refusal |
| 5. Detection mechanism | MET | A-1 git show exit check; A-3 exit capture and format check | NOT MET | None | NOT MET | None proposed |
| **Subtotal** | **4/5** | | **1/5** | | **3/5** | |

### Invariant and Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1. Collection boundaries (missing/empty element) | MET | A-2: a listed path with no contract | MET | R2-3: collapsed-line assumption for status lines | MET | R3-1: listed contract that does not exist |
| 2. State interactions across components | MET | A-2: Task 1 skill text vs Task 6 spec check | MET | R2-3: executor writes vs status delta | MET | R3-3: worker contract vs own contract |
| 3. Guard gaps | MET | A-1: no pipefail, no `git show` exit check | MET | R2-3: AC rests on an unstated collapsed-line assumption (re-evaluated, see log) | MET | R3-7: snapshot step unguarded by Depends-on |
| 4. Count divergence / inclusive-exclusive | MET | A-7: collect-only rises by exactly 2; slice excludes line 197 | NOT MET | No count or range finding | MET | R3-8: each phrase single-occurrence; Tier 2 bullet inside the slice |
| 5. Interaction effects | MET | A-4: sync-dev vs "writes only" | MET | R2-2: F-2 forces the F-13 widening | MET | R3-4: spec sentence vs installed twin |
| **Subtotal** | **5/5** | | **4/5** | | **5/5** | |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 3/5 | 4/5 |
| Correctness | 4/5 | 3/5 | 3/5 |
| Structure | 4/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 5/5 |
| Risk Coverage | 4/5 | 1/5 | 3/5 |
| Invariant and Edge Case | 5/5 | 4/5 | 5/5 |
| **qual_score** | **26/30 = 0.867** | **20/30 = 0.667** | **25/30 = 0.833** |

### Edge Case Floor Check

| Variant | Invariant and Edge Case | Floor (>= 1/5) | Eligible as base |
|---|---|---|---|
| V1 | 5/5 | pass | yes |
| V2 | 4/5 | pass | yes |
| V3 | 5/5 | pass | yes |

## Position-Bias Mitigation

Pass 1 order V1, V2, V3; pass 2 order V3, V2, V1. 90 verdicts per pass.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Re-evaluation | Final |
|---|---|---|---|---|---|---|
| Correctness 1 | V3 | MET | NOT MET | DISAGREE | Pass 2 read R3-2's P1 as a false fact. R3-2 states a conditional and flags it unverified; no stated fact is false. | MET |
| Completeness 4 | V3 | MET | NOT MET | DISAGREE | Pass 2 required a pass condition for every finding. The criterion asks for criteria on the card's top findings; R3-1 has one. | MET |
| Clarity 1 | V1 | NOT MET | MET | DISAGREE | Pass 2 read the vague sentences as bounded conditionals. The 10% threshold is mechanical: 3/26 = 11.5%. | NOT MET |
| Invariant 3 | V2 | NOT MET | MET | DISAGREE | Pass 1 looked only for a missing check. R2-3 names an unstated assumption the AC depends on (collapsed `??` lines), which is the "unguarded assumption" half of the criterion. | MET (changed) |

Disagreements re-evaluated: 4. Final verdicts changed from pass 1: 1 (V2 Invariant 3). All other 86 verdicts agreed in both passes.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate points won (scoring matrix) |
|---|---|---|---|---|
| V1 (analyzer/sonnet) | 0.396 | 0.433 | **0.829** | 6 (S-002, C-004, C-005, C-006, X-002, X-005) |
| V2 (qa/haiku slot) | 0.343 | 0.333 | **0.676** | 3 (C-003, C-012, X-004) |
| V3 (refactorer/opus) | 0.356 | 0.417 | **0.773** | 5 (C-001, C-008, C-009, C-010, X-001) |

**Margin**: V1 - V3 = 0.056 (5.6 points), above the 0.05 threshold. V3 - V2 = 0.097.
**Tiebreaker applied**: No. Sensitivity: the margin is close to the threshold. Removing V1's C-001 credit (RC 22/31) gives 0.824 and a margin of 0.051; counting V1's "index check" as resolved raises V1. If the margin had fallen below 0.05, tiebreaker 1 (debate points won, 6 to 5) would still select V1. The selection is stable under every single-verdict change checked.

## Selected Base: Variant 1 (reviewer-1, analyzer, sonnet)

### Selection Rationale

V1 has the highest combined score (0.829) and the best requirement coverage after the debate (23 of 31, twice V2 and V3). It is the only card that covers all five brief items, it won the most debate points (6), and every one of those wins was unanimous or majority on reproduced evidence (C-004, C-005, X-002 by a `git` run or the index). Its priorities are the ones the debate converged on: no P1, and C-001 at P2 (S-001, X-001). Its weaknesses are a lower IC than V2 (tag and Task 5 errors, both conceded) and blindness to R3-3 and to the three brief-owned notes V3 found; these are additive fixes, not rewrites.

V3 scored close (0.773) and owns the best evidence for the highest-severity point (C-001). It is not the base because two of its eight findings were withdrawn, its one remedy was withdrawn as a brief violation, and it misses brief items 3 and 5. V2 is the only card that held the plan to the brief's literal verifiers, but it proposes no fix anywhere and its P1 did not survive.

None of the three cards found INV-019 (the probe's only HIGH). It enters the merged card from `invariant-probe.md` as an orchestrator finding (refactor-plan.md, M-01).

### Strengths to Preserve from Base (V1)

1. A-5 index-state reasoning: the earlier package is staged, so Task 7 bullet 3 holds; this decided C-004, X-002 and X-005.
2. A-1 mechanical probe of the `git show HEAD:` check, narrowed to Task 4's routing half (C-005).
3. A-2 identification of the listed-contract conflict at the severity the debate settled on (P2), with the timeout path as the reachable trigger.
4. A-7 slicing, pin and count confirmations (SKILL.md:195-197 paragraph slice, collect-only +2).
5. A-3's format-check point (CI runs a pinned `ruff format --check`, pyproject.toml:50-54).
6. Calibration: P2 throughout, INFERRED where the failure is inferred.

### Strengths to Incorporate from Non-Base Variants

1. From V3 R3-1: the Grounded evidence for C-001 (`analyze.md:97-98`, WC-4 `WORKER-CONTRACT.md:32`, `SKILL.md:388`) and the point that plan:133 "no known false FAIL" is false as written.
2. From V3 R3-3: the `--report-dir` contract split, as a P3 note.
3. From V3 R3-4, R3-5, R3-6: three brief-owned owner notes (companion sentence vs installed twin; routing bullet vs `skipped` on timeout; only `Task` is inferred).
4. From V3 R3-8: the byte-for-byte Part 4 confirmation.
5. From V2 R2-1 and R2-2: the recording discipline for the F-16 and F-13 departures, at P3.
6. From V2 R2-5: the coverage-matrix gap note.
7. From the Round 2 rebuttals (V1 advocate's parenthesis, V3 advocate's Edits 2-3) and the invariant probe (INV-019, INV-011, INV-005, INV-002, INV-013): the recommended Part 4 wording fix. Details in `refactor-plan.md`.
