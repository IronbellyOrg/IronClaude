# Base Selection Report

Mode A, depth standard, focus correctness / risk / test-coverage. Variant A = `variant-1-original.md` (Option A: re-find and cluster every round, D2/D3/D16 fixed). Variant B = `variant-2-original.md` (Option B: find once, then verify-only). Status of this file: complete (written incrementally: quantitative layer first, then the qualitative layer, position-bias log, combined scoring and selection).

## Quantitative Scoring (50% weight)

Source requirements: the 20 items below, drawn from the C-13 block of `synthesis/synth-04-options-conflicts.md` (the three defects D2, D3, D16a/b/c; round-1 multi-reviewer find; evidenced clearing; one re-review protocol; the seams to C01, C02, C15, C05, C16, C19; reflect off the ledger; late findings; the unmeasured rounds 2-3; the tests the synthesis names; multi-file persistence). No formal FR/NFR IDs exist, so matching is by ID or keyword (protocol edge case: topic matching), by `grep -ciE` over each variant file; an item counts as matched when it occurs at least once. Computed by the orchestrator with a read-only batch; reproducible with the same patterns.

| Metric | Weight | Variant A | Variant B |
|--------|--------|-----------|-----------|
| requirement_coverage (RC) | 0.30 | 0.950 (19 of 20; unmatched: R17, the D5 missing-anchor test `test_review_ledger.py:408-417`) | 1.000 (20 of 20) |
| internal_consistency (IC) | 0.25 | 0.972 (1 intra-variant contradiction, X-005, over 36 evidence-tagged claims) | 0.977 (1 intra-variant contradiction, X-006, over 43 evidence-tagged claims) |
| specificity_ratio (SR) | 0.15 | 1.000 (99 concrete indicators: 90 file:line cites, 2 percentages, 7 counted quantities; 0 vague terms) | 1.000 (113 concrete: 84 cites, 8 percentages, 21 counts; 0 vague terms) |
| dependency_completeness (DC) | 0.15 | 1.000 (every "Evidence item N", "change N" and P1-P6 reference resolves; no dangling internal reference found) | 1.000 (28 of 28 distinct `E-N` references defined; Core items and P1-P6 resolve) |
| section_coverage (SC) | 0.15 | 1.000 (7 H2 sections; max across variants is 7) | 1.000 (7 H2 sections) |
| **quant_score** | | **0.978** | **0.994** |

Computation: A = 0.950x0.30 + 0.972x0.25 + 1.000x0.15 + 1.000x0.15 + 1.000x0.15 = 0.2850 + 0.2431 + 0.4500 = 0.9781. B = 1.000x0.30 + 0.977x0.25 + 0.4500 = 0.3000 + 0.2442 + 0.4500 = 0.9942.

Limits of this layer (stated so the combined score is read correctly): both documents are dense design proposals with no vague hedging words, so SR, DC and SC saturate at 1.0 and the layer separates the variants only through RC (one missed requirement item) and the IC proxy (claims counted as evidence tags, because design proposals have no formal claim list). The quantitative layer therefore moves the combined score by about 0.008 in B's favour and cannot decide the selection alone.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Method: two independent scorer agents (`c13-scorer-pass1`: A then B; `c13-scorer-pass2`: B then A) each applied the 30-criterion rubric with Claim-Evidence-Verdict to the two documents as written (no credit for improvements made in the debate). Raw outputs are in `scorer-pass1-raw.md` and `scorer-pass2-raw.md`. Where the passes agreed the verdict is final; the four criteria where they disagreed were re-evaluated by the orchestrator with both pieces of evidence (see Position-Bias Mitigation). Evidence below is shortened from the scorers' CEV rows; "(both)" means both passes agreed.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| C1 Covers all explicit requirements | MET | Core changes 1-5 cover D2, D3, D16a/b; "D16c closed as by design"; seams table to C01/C02/C05/C12/C15/C16/C19 (both) | MET | Core 3, 3a, 4, 5, 7, 11 cover D2, D3, D16a-c, round-1 merge, one re-review protocol; P6 seams (both) |
| C2 Edge cases and failure scenarios | MET | Degraded round, abstaining reviewer, refused would-be PASS, zero valid blocks, `--cap` mismatch, quorum-denominator risk (both) | MET | `E-INCOMPLETE`, `cannot-verify` as X item, tamper check, re-ask then ESCALATE (P5), Risks 3 and 8 (both) |
| C3 Dependencies and prerequisites | MET | Seams table; Sequencing row; C15 `rejected[]` is a prerequisite of change 5 (both) | MET | "Order of work"; Risk 4 depends on C05 and C12; multi-path snapshots named (both) |
| C4 Success/completion criteria | MET | Gate commands (37 + 178 tests), properties P1-P6, 15 listed new tests (both) | MET | Falsifier with named metrics and the within-arm spread screen; adoption conditional on it (both) |
| C5 Out of scope | MET | "What Option A explicitly does not do"; "Not costed here" (both) | MET | "What B decides and what it leaves alone"; PR and rf-qa "not designed here" (both) |
| **Subtotal** | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| R1 No factual errors | MET | Spot-checked `ledger.py:93-104,114-118,254-258,308-314,328-339` all match (both). Orchestrator note, not a scored disagreement: "nothing is recorded" on a degraded would-be PASS holds for the CLI but not for an in-memory caller, because `merge_round` mutates at `:204-258` before the verdict at `:273` | MET (re-evaluated, passes disagreed) | Cited lines match; Core 11 cites `review_ledger.py:65` (reviser actions) beside `:1591` (`VERIFY_RESULTS`, the correct one) and the claim about the shared status words holds; the extra cite is wrong, the claim is not |
| R2 Feasible with stated constraints | MET | Five local changes around existing calls; one-directional; additive keys (both) | MET | Port of a built, tested script; shim; XL rating stated (both) |
| R3 Terminology consistent | MET | round, quorum, degraded, valid, `block_ok` used consistently (both) | NOT MET | "answer" names both the reviser's claim step (`ledger answer`) and the verifier's per-row reply (both) |
| R4 No internal contradictions | MET | Change 4 agrees with Evidence 4 and P3; silence-clearing is disclosed (both) | MET | Decision formula, Core 7 and exit codes agree; sweep-mandatory versus `sweep: none` reconciled in Core 8 (both). Intra-variant tension X-006 (merge refused vs shim) is a diff point, not scored here as a contradiction of stated claims |
| R5 Claims supported | MET | Evidence items 1-9 carry file:line and tags; P4 labelled [INFERENCE] (both) | MET | E-1..E-28 tagged; properties name E-items (both) |
| **Subtotal** | **5/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| S1 Logical ordering | MET | Design, How it works, Evidence, Correctness, Risks, Tests, Cost (both) | MET | Same order (both) |
| S2 Consistent hierarchy | MET | `##` sections, Evidence items 1-9 as `###` (both) | MET | Evidence A-E as `###`; Core item "3a" is a small irregularity, not an orphan (both) |
| S3 Separation of concerns | MET | Risks, tests, cost in own sections; Evidence 6-8 carry rebuttal of B/C (mild blending) (both) | MET (re-evaluated, passes disagreed) | Comparison table and "weakest point" sit in Correctness and recur in Risks and Test 15: mild blending of the same size as A's Evidence 6-8 |
| S4 Navigation aids | MET | Citation key; "see Risks", "see Cost", "Evidence item 4" (both) | MET | Citation key; E-ids, P1-P6, Risk numbers cross-referenced (both) |
| S5 Artifact conventions | MET | Design, evidence, risks, tests, cost present (both) | MET | Same (both) |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| L1 Unambiguous language | MET | Countable statements; uncertainty labelled [UNVERIFIED]/[INFERENCE] (both) | MET | Formula and refusal codes; "proposed" items labelled (both) |
| L2 Concrete | MET | Three-round worked example; named fields, lines, exit codes (both) | MET | Data-flow diagram, decision formula, CLI table (both) |
| L3 Clear purpose per section | MET | One stated purpose per section (both) | MET | "Position in one paragraph"; Evidence opens with what it can and cannot show (both) |
| L4 Terms defined on first use | MET | D2/D3/D16 glossed in the opening paragraph; `G9`/`G10` test groups left unglossed (both) | MET (re-evaluated, passes disagreed) | D1, D3, D16c are glossed inline ("closes D1, which E2 had to replay...", "the code mode D16c says is missing"); U, X, I defined in the formula right after first use |
| L5 Actionable next steps | MET | Sequencing row; measurement and trigger for a deferral policy (both) | MET | "Decisions this proposal asks of the owner" (1)-(3); order of work (both) |
| **Subtotal** | **5/5** | | **5/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| K1 3+ risks with probability and impact | NOT MET | Table is Risk / Why it matters / Mitigation: impact reasons only, no likelihood per risk (both) | MET (re-evaluated, passes disagreed) | 10 risks; "Why it is real" supplies evidence of likelihood and "Residual" the remaining impact for every row; qualitative, no numeric scale |
| K2 Mitigation per risk | MET | Every row has a mitigation (both) | MET | Every row has a mitigation and a residual (both) |
| K3 Failure modes and recovery | MET | Refusal writes nothing; re-run only the missing reviewer (both) | MET | Fail-closed refusal; one re-ask then ESCALATE; `--dry-run`; shim (both) |
| K4 External dependencies | MET | Seams not ready; decider pre-empted; PR bots re-trigger (both) | MET | Risks 3, 4, 7, 9: model compliance, C05/C12, external ledger files, served-model drift (both) |
| K5 Monitoring/validation mechanism | MET | `unanswered_priors` telemetry; late-row rate from stored fields (both) | MET | Falsifier run with spread screen; `would_block` on outside rows; served-model flag (both) |
| **Subtotal** | **4/5** | | **5/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| I1 Collection boundaries | MET | Quorum `min(2, panel_size)`, quorum 1 for a lone reviewer, zero valid blocks refused, tests 5-7 (both) | MET | Test "k-1 valid blocks cannot write PASS, k can"; unanswered plan row refused (both) |
| I2 State interactions across components | MET | Stored `cap_reviews` versus `--cap`; `--resolution` versus `--report`; degraded gates clearing (both) | MET | Phases, snapshot hashes, plan versus answers; resolution versus round state (both) |
| I3 Guard condition gaps | MET | `block_ok` never read after `:150`; `--round` help versus `IntRange(min=1)` (both) | MET | Same `block_ok` gap (E-2); no integrity check on `load` (E-6); frozen-field and anchor refusals (both) |
| I4 Count divergence | MET | `n > cap` versus `n == len+1`; "never prints 4 of 3"; k-1 versus k (both) | MET | `begin` refuses a fourth review or third fix cycle; k-1 versus k (both) |
| I5 Interaction effects | MET | Degraded x clearing; change 5 x C15 `rejected[]`; prior lines x status invariant (both) | MET | All-or-nothing verify x C15; scope=outside x sweep; exit 12 per profile (both) |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 |
| Correctness | 5/5 | 4/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 |
| Risk Coverage | 4/5 | 5/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **29/30 = 0.967** | **29/30 = 0.967** |

### Edge Case Floor Check

Invariant & Edge Case Coverage: A 5/5, B 5/5. Both variants are above the 1/5 floor and eligible as base. (The rubric measures what each document says about edge cases; the Round 2.5 probe, which found 10 HIGH invariants in the emerging consensus, is not part of this score and does not change eligibility.)

## Position-Bias Mitigation

Pass 1 evaluated A first then B; pass 2 evaluated B first then A. Of 60 criterion-variant pairs, 56 agreed. Disagreements, each re-evaluated by the orchestrator with both passes' evidence (the re-evaluation verdict is final):

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation reasoning |
|-----------|---------|--------|--------|-----------|-------|-------------------------|
| R1 | B | MET | NOT MET | DISAGREE | MET | Pass 2's finding is real: `review_ledger.py:65` is `ANSWER_ACTIONS` (fixed/not-fixed/disputed, the reviser's actions), but Core 11 cites it beside `:1591` (`VERIFY_RESULTS`: resolved/open/regressed/cannot-verify), and the claim that the verifier words match the v1 `prior` words, plus `cannot-verify`, is true. The synthesis (01 §18 item 9) carries the same `:65` cite. A wrong extra cite on a correct claim is not a factual error in the claim |
| S3 | B | NOT MET | MET | DISAGREE | MET | B's Correctness section holds the comparison table and "weakest point", which recur in Risks and Test 15; A's Evidence section holds rebuttals of B and C (items 6-8). Both blend concerns mildly and both section headings disclose it; the same bar gives MET to both |
| L4 | B | NOT MET | MET | DISAGREE | MET | D1, D3, D16c each come with an inline gloss at first use; U, X, I are defined in the formula that follows the data flow naming them. A leaves `G9`/`G10` unglossed and also stays MET |
| K1 | B | NOT MET | MET | DISAGREE | MET | B's table has two columns that between them give a likelihood basis ("Why it is real", with E-ids) and an impact ("Residual") for all 10 rows; A's table gives impact-side reasons only. Neither uses a numeric scale; the rubric asks for an assessment, which B's columns provide |

Disagreements found: 4 of 60 pairs, all on Variant B. Verdicts changed by re-evaluation relative to one of the passes: 4 (each re-evaluation overruled exactly one pass: pass 1 was overruled on S3, L4 and K1, where the final MET follows pass 2; pass 2 was overruled on R1, where the final MET follows pass 1). Pattern noted: Variant A's score was identical in both passes (29 and 29); Variant B scored 26 when evaluated second and 28 when evaluated first, consistent with a small order effect on B. Raw totals: pass 1: A 29, B 26; pass 2: A 29, B 28.

Sensitivity (what the qualitative total would be under the alternative reading of each disputed criterion): all four decided for B gives B 29; if K1 goes to NOT MET, B 28; if K1 and R1 both go to NOT MET, B 27; A stays 29 unless the orchestrator's R1 note (the "nothing is recorded" imprecision) is scored, which would make A 28. The qualitative layer therefore separates the variants by at most 2 criteria in either direction and cannot decide the selection alone.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (variant-1-original, Option A) | 0.4890 (0.9781 x 0.50) | 0.4833 (0.9667 x 0.50) | **0.9724** | 10 of 37 points won (27.0%) |
| B (variant-2-original, Option B) | 0.4971 (0.9942 x 0.50) | 0.4833 (0.9667 x 0.50) | **0.9804** | 14 of 37 points won (37.8%) |

**Margin**: 0.0080 absolute = 0.8 percentage points (below the 5% threshold)
**Tiebreaker applied**: Yes, level 1 (debate performance). B won 14 of 37 diff points in the Step 2 scoring matrix against A's 10; the 10.8-point gap in share of points is above the 5% bar, so level 2 (correctness criteria count, A 5 versus B 4) is not reached.

Sensitivity of the tiebreaker, stated because this is a close call. The 14 B wins include five structural points (S-001 to S-005), which judge document structure rather than design merit. Counting only the 32 non-structural points, B wins 9 and A wins 10 (B 28.1%, A 31.3%, a 3.1-point gap, inside the 5% bar), which would send the tiebreaker to level 2, where A leads on correctness criteria (5 versus 4). The protocol as written counts every point won in the scoring matrix, so the selection follows level 1 and picks B; the selection is therefore a narrow result and the merged proposal does not treat it as a verdict that B's design is better in every respect. Both advocates themselves ended Round 2 recommending a staged hybrid (A's core first, B's answer semantics carried in); that hybrid is what the refactor plan builds on the selected base.

## Selected Base: Variant B (variant-2-original.md, Option B "find once, then verify-only")

### Selection Rationale

1. Combined score 0.9804 against 0.9724 (B ahead by 0.008). B leads on the quantitative layer (0.994 versus 0.978: it matches all 20 source-requirement items where A misses the D5 missing-anchor test pin) and ties on the qualitative layer at 29 of 30 each (B gains K1, loses R3; A loses K1).
2. The margin is inside the 5% band, so the tiebreaker decided: B won 14 of the 37 debated points against A's 10, concentrated on the correctness-bearing mechanics where the advocates agreed with the highest confidence: evidenced clearing (C-002, 93%), the blocking bit (C-005, 95%), clearing sufficiency (X-001, 90%), round-1 evidence misuse in A (X-005, 90%), row identity (C-006, 80%), `prior` semantics (C-008, 80%).
3. A won the shippability and scope points: cap and `--cap` fixes (C-004), multi-reviewer rounds (C-010), reviser machinery (C-011), effort (C-014), prompt surface (C-017), late-finding visibility and the C15/C02 boundary (C-007, X-003, X-004), compatibility of `merge` and the loop prompt (X-006). B's defects on those points are known and conceded (see Strengths to Incorporate and the refactor plan).
4. Both advocates converged on the same end state, so the selection decides the skeleton, not the destination: A's core landed first, B's answer semantics inside it. The base is chosen by the scoring rule; the refactor plan makes the base carry A's strengths and closes the base's conceded weaknesses.
5. Not decided by this selection (kept open in the merge): S-006, C-013, A-002, A-004, and the ten HIGH invariants of the probe (INV-001 to INV-010).

### Strengths to Preserve from Base (Variant B)

1. Positive clearing: a row leaves the blocking set only on a script-checked answer carrying a quote that occurs in the new text (`review_ledger.py:1711-1737`); silence is `E-INCOMPLETE`, never clear.
2. Frozen row identity and a one-way blocking bit, with `E-FROZEN` for any answer or new row that carries a frozen field.
3. `caused_by` provenance for new rows inside a changed hunk, and the characterization-test pair for the near-row misbooking.
4. Cap and order by refusal (`E-CAP`, `E-PHASE`), the computed decision over U, X, I, `cannot-verify` as an X item that forces ESCALATE.
5. Integrity layer: body hash, lock, snapshot hashes (A has none).
6. The post-loop sweep and the delivery outcome distinct from the loop decision, once wired into `decide` for lenses that skip it.
7. The pre-registered falsifier with the experiment's spread screen, the three owner decisions, and E-id traceability of evidence.

### Strengths to Incorporate from Non-Base Variant (Variant A)

1. Cap refusal in `merge_round` (`n > cap_reviews`) and `--cap` default `None` with a conflict error on an existing ledger (A change 1-2; debate point C-004, A won). Lands first because both options need it. Source: A "Core changes" 1-2.
2. Quorum with a `--resolution` denominator, a recorded `degraded` flag and a recorded degraded FAIL for round 1 and for any multi-reviewer round (A change 3-5, U-001; C-003 SPLIT). Source: A "Core changes" 3 and 5, strengthened by INV-007 and INV-016.
3. Multi-reviewer support in rounds 2-3 (C-010, A won): B must either support it with a defined merge rule or state it out of scope. Source: A "How it works" step 3, "A three-round example".
4. Keep `review merge` working for round >= 2 through an adapter, or ship the prompt change and a pin test in the same change; keep `ledger revise` (X-006, C-011, C-017, A won). Source: A "CLI surface", "Consumer modules".
5. The C15/C02 boundary at the verify step: answers all-or-nothing, a bad new-row anchor becomes a flagged problem row while valid answers and rows are written (X-003, A won; B conceded in full).
6. Late-finding visibility: outside-hunk rows that would block must force a visible non-PASS on lenses without a sweep, and the deferral policy is adopted only after the late-row measurement (C-007, X-004, U-004). Source: A P6, Risks "late findings".
7. Additive-key compatibility with a HEAD-generated fixture, `unanswered_priors` telemetry, the E2 flip fixture, the plugin-mirror copy of the loop prompts file (U-002, U-003, U-005, U-006).
8. Debate-surfaced fixes that belong in any version: atomic refusal (deepcopy or compute-before-mutate), sticky one-way blocking, `prior` gating that distinguishes `resolved` from `open`/`regressed`, bounded refusal recorded in the ledger (A-adv Round 2, INV-002, INV-003, INV-020).

