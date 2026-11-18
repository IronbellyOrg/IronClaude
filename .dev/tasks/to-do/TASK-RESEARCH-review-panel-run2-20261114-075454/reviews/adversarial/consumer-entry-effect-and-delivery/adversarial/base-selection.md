# Base Selection Report

Inputs: `variant-1-original.md` (Variant A, Proposal A) and `variant-2-original.md` (Variant B, Proposal B). Quantitative layer computed by `quant-score.py` (output `quant-score-output.json`, `uv run python`). Qualitative layer: two independent scorers (`score-pass1.md` in order A, B; `score-pass2.md` in reverse order B, A) and one re-evaluator for the three disagreements (`score-reeval.md`).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (Proposal A) | Variant B (Proposal B) |
|--------|--------|------------------------|------------------------|
| requirement_coverage | 0.30 | 1.0000 (27 of 27 C-05 topic patterns matched) | 1.0000 (27 of 27) |
| internal_consistency | 0.25 | 0.9655 (1 contradiction in 29 tagged claims) | 0.9231 (3 contradictions in 39 tagged claims) |
| specificity_ratio | 0.15 | 1.0000 (508 concrete, 0 vague indicators) | 1.0000 (505 concrete, 0 vague indicators) |
| dependency_completeness | 0.15 | 0.9167 (11 of 12 internal references resolve) | 1.0000 (67 of 67) |
| section_coverage | 0.15 | 1.0000 (9 H2 sections; max 9) | 1.0000 (9 H2 sections) |
| **quant_score** | | **0.9789** | **0.9808** |

Method notes (limits stated, not hidden): requirement coverage uses keyword matching on the C-05 row and slot brief because the source has no formal requirement IDs (protocol edge case); both variants saturate it. The contradiction counts come from the debate (listed in `debate-transcript.md`, "Intra-variant contradictions"): A 1 (zero edits to call sites versus rule D1), B 3 (E7 versus v1 engine; 1.1 to 1.2 bump versus pinned "1.1"; blocking effect placed at fenced Stage 10.5). The quantitative layer separates the variants by 0.0019 only.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Both passes agreed on 57 of 60 criterion-variant pairs. Evidence for each verdict is in `score-pass1.md` and `score-pass2.md` (CEV lines per criterion); the dimension tables below give the final verdict and the deciding evidence.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Covers all explicit requirements | MET | Sec 1, 4, 5 (INV-M/B/N/K/J), 6, 7, 8 cover every C-05 row element | MET | Sec 1, 2, 5, 6, 7, 8 cover every element |
| Addresses edge cases/failures | MET | Sec 3 item 7 and Obj 2 (quick-depth phases), Sec 4 C-03 (partial panel is `partial`) | MET | Sec 3 (B-replace `skipped`/null), Sec 8 obj 3 (CLI absent), E4 |
| Includes dependencies/prerequisites | MET | Sec 4 (one condition per C-01..C-03, C-04 dependence), Sec 8 obj 3 | MET | Sec 2 table (C-01..C-03 conditions; "does not depend on C-04") |
| Defines success/completion criteria | MET | Sec 6.3 contract-compat assertion; 6.4 four test files unmodified; 6.1 "A is wrong if" rule | MET | Sec 6 item 3 right/wrong rule with ESCALATE and arm-D conditions |
| Specifies out-of-scope items | MET | Sec 2 rows: Stages 6-10, T5 engine, rf-qa/PR review | MET | Sec 2 (T5 outside B), Sec 3 (tasklist skill stays out of plugin; X-15 not decided) |
| **Subtotal** | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| No factual errors | NOT MET | Debate: "fence test must be changed" withdrawn; `coverage_pct`/`tier_reached` cannot carry a panel benefit (INV-007); X-002 wording conceded too strong | NOT MET | Debate: contract 1.1 to 1.2 bump wrong (`eval_workflow_vs_task_builder.py:1140`, `archive_workspace.py:327`); E6, E7 overstated; `:243-248` pin claim wrong |
| Feasible with stated constraints | NOT MET | INV-011/INV-014 F1-F2: no panel-to-status map exists; no engine selector reachable from a consumer call (INV-010) | NOT MET | `tasklist-review`, `plan-review`, `effect` have no code home; new skill needs eval allow-list, staging and `artifacts` edits B did not list |
| Terminology consistent | MET | Sec 1/3: "advisory" used operationally; UC-1 vs UC-2/T5 distinct | MET | `effect` (module data) vs core `blocking`; B-add/B-replace used consistently |
| No internal contradictions | NOT MET | Sec 3 item 1 "zero edits" vs D1 / Obj 2 | NOT MET | Three listed contradictions (E7 vs v1 engine; 1.1/1.2; Stage 10.5 effect) |
| Claims supported by evidence | MET | Sec 3 items 1-10 cite file:line with tags | MET | E1-E13 cite file:line with tags; E11 carries counter-evidence |
| **Subtotal** | **2/5** | | **2/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Logical section ordering | MET | Position, consequence, evidence, slots, invariants, test, downstream, objection, open items | MET | Position, slot dependence, consequence, evidence, invariants, test, downstream, objection, limits |
| Consistent hierarchy depth | MET | Nine numbered `##` sections, flat lists | MET | Nine numbered `##` sections |
| Separation of concerns | MET (re-evaluated: Pass 1 NOT MET, Pass 2 MET; final MET) | Each section has one self-labelled purpose; flat evidence list is normal for a position paper (`score-reeval.md` item 3) | MET | Sec 8 item 4 maps arguments to entry, effect, delivery |
| Navigation aids | MET | In-text cross-references ("item 8", "section 6.1 and 6.3"), tag legend | MET | Cross-references ("section 4, item E8", "section 7") |
| Follows artifact conventions | MET | Position, evidence, invariants, test, objection | MET | Same |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Unambiguous language | NOT MET | Sec 6.1 "materially more ... per cost" and 6.2 "If that share is high" have no threshold | MET (re-evaluated: Pass 1 NOT MET, Pass 2 MET; final MET) | No hedge words by Grep; Sec 6 item 3 rule is concrete; one loose phrase "a small share" (`score-reeval.md` item 1) |
| Concrete rather than abstract | MET | Sec 2 table with exact lines; Sec 6 names four test files and GT counts | MET | Names `panel_status`, `panel_report_path`, parity-test shape; E11 figures |
| Clear section purpose | MET | Sec 1, 4, 7, 9 | MET | Sec 2, 6, 9 |
| Terms defined on first use | NOT MET | T5, UC-1, D1, GT, DO4, U11, INV-L undefined at first use | NOT MET | C-S3, X-15, FX-1/5/8/11, OQ-24, DO4, `Q(re-review)` undefined at first use |
| Actionable next steps | MET | Sec 6 items 1-4; Sec 8 obj 3; Sec 9 open items | MET | Sec 6 items 1-4; Sec 8 second objection; Sec 9 |
| **Subtotal** | **3/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| At least 3 risks with probability and impact | NOT MET | Sec 5 names three endangered items; none has a probability | NOT MET | E11/E12 give rates for one risk; others (double cost, reader degradation, C-02 INV-001/2/3) unquantified |
| Mitigation for each risk | MET | Sec 5 (a)-(c) each tied to a measurement or update; Sec 8 each objection has an answer | NOT MET | INV-J (OQ-24) and C-02 INV-001 named with no mitigation |
| Failure modes and recovery | MET | INV-I fail-open vs T5 fail-closed; partial panel to `partial` | MET | CLI absent returns `skipped`; `defer` exit; panel FAIL blocks only `--handoff implement` |
| External dependencies and failure | MET | Plugin lacks the skill Wave 4 calls; C-01..C-03 dependence | MET | Marketplace CLI availability; plugin lacks reviewer agent |
| Monitoring or validation mechanism | MET | Sec 6.2 routing coverage, 6.3 compat test, 6.4 non-regression (INV-005 shows 6.2 has no working instrument) | MET | Sec 6 free checks, two-arm replay with loop columns, cost column |
| **Subtotal** | **4/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence |
|-----------|-----------|----------|-----------|----------|
| Collection boundaries | MET | Single-vendor degrade (`contract.py:287-288`), partial panel, depth band 0-3 | MET | `requested` collapsing to 1 (INV-007 of C-03), `n_tasks > 0` boundary, no held-out package |
| State-variable interactions across components | MET | `derive_verdict` reads engine fields; INV-L shadow vs `panel`; closed enum readers | MET | `reflect_*` vs `panel_*` keys; `nested/panel-<n>/`; `effect` in module not core |
| Guard-condition gaps | MET | Sec 3 item 8 fence vacuity; plugin parity pins cover few files | MET | Validator tolerates extra keys; plugin tree outside `verify-sync`; no tasklist lens |
| Count divergence | NOT MET (re-evaluated: Pass 1 MET weakly, Pass 2 NOT MET; final NOT MET) | Lists counts ("four" readers, "2 passes" vs "3-review cap") but analyses no divergence scenario; the "four" undercounts (INV-008) (`score-reeval.md` item 2) | MET | INV-J "2 TOTAL passes" vs 2 fix cycles (OQ-24); `requested` collapse; B-add reviews twice |
| Interaction effects | MET | T5 bypasses UC-1; C-02 condition reopens if reflect uses the ledger; P2 vs 10.5 predicate | MET | B-add double review; B-replace degrades readers; revise loop and ledger |
| **Subtotal** | **4/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 |
| Correctness | 2/5 | 2/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 3/5 | 4/5 |
| Risk Coverage | 4/5 | 3/5 |
| Invariant & Edge Case | 4/5 | 5/5 |
| **qual_score** | **23/30 = 0.7667** | **24/30 = 0.8000** |

### Edge Case Floor Check
Variant A scores 4/5 and Variant B 5/5 on Invariant & Edge Case Coverage; both meet the floor (>= 1/5) and are eligible as base. No suspension.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| CLA1 (unambiguous language) | B | NOT MET | MET | DISAGREE | MET (re-evaluation) |
| INV4 (count divergence) | A | MET | NOT MET | DISAGREE | NOT MET (re-evaluation) |
| STR3 (separation of concerns) | A | NOT MET | MET | DISAGREE | MET (re-evaluation) |

Disagreements re-evaluated: 3 of 60 criterion-variant pairs. Final verdicts changed: 3 relative to Pass 1, 0 relative to Pass 2 (the re-evaluator sided with Pass 2 on all three, with reasons recorded in `score-reeval.md`). Pass totals before re-evaluation: Pass 1 A 23, B 23; Pass 2 A 23, B 24. After: A 23, B 24.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (Proposal A) | 0.4894 | 0.3833 | **0.8728** | 4 points won outright |
| B (Proposal B) | 0.4904 | 0.4000 | **0.8904** | 3 points won outright |

**Margin**: 0.0176 (1.76%), below the 5% threshold. Variant B leads on the combined score.
**Tiebreaker applied**: Yes.
- Level 1 (debate performance, points won outright in the Step 2 scoring matrix): Variant A 4 (C-001, C-003, C-009, C-010), Variant B 3 (S-002, S-003, A-006); 13 points ended as Hybrid and 4 as Neither and count for neither variant. Variant A wins on count. The margin is thin: 4 versus 3 is 4.2 percentage points of the 24 points, which is within 5%, so by the protocol's own check Level 1 does not settle it cleanly.
- Level 2 (correctness criteria MET): A 2 (COR3, COR5), B 2 (COR3, COR5): identical.
- Level 3 (input order): Variant A is first.
- Every path through the tiebreaker (Level 1 by count, or Levels 2 and 3 if Level 1 is treated as within 5%) selects Variant A.

## Selected Base: Variant A (Proposal A; `variant-1-original.md`)

### Selection Rationale
The combined score does not select a base on its own: Variant B leads 0.8904 to 0.8728, a margin of 1.76% that is inside the 5% tiebreaker band. The quantitative layer separates the variants by 0.0019 and the qualitative layer by one criterion (B 24, A 23). Both variants have identical Correctness (2/5) because each carries debate-verified errors and internal contradictions. Under the tiebreaker, Variant A is selected (Level 1 by points won, 4 to 3; Levels 2 and 3 give the same answer). The substantive content of the debate points the same way: both advocates' final text names Variant A's position as the merged resolution on the three load-bearing points (entry C-001, delivery C-003, Wave 4 C-009) and a hybrid built on A's text for most of the rest; Variant B's advocate withdrew B-add as a recommendation for this release, the contract version bump, E6 and E7. The base is therefore a text-continuity choice with the merged resolution in Variant A's frame, and Variant B's separable three-part structure, its per-row invariant verdicts and its measurement design are to be merged in.

### Strengths to Preserve from Base
1. One review call shape at Wave 4 and Stage 10.5 (`/sc:reflect --mode pre`), with the closed `reflect_status` enum, the four skill readers and the substring pins untouched (Sec 1, 2, 3 items 3-4).
2. Advisory at generation time, blocking at T5 and Stages 6-10; the panel judged by the same `derive_verdict` map and its 36 tests (Sec 3 items 2 and 5).
3. The consistency section for C-01, C-02, C-03 with one named dependency each, and the C-04 independence note (Sec 4).
4. The code-verified evidence list with tags and the explicit statement that D1 and T5 are limits (Sec 3 items 6-7, Sec 8 objection 2).
5. The plugin position: no panel-only copy; plugin delivery decided as a set (Sec 3 item 9, Sec 8 objection 4).

### Strengths to Incorporate from Non-Base Variants
1. From Variant B (Sec 1, Sec 8 item 4): the three parts entry, effect and delivery stated separately, with which argument carries which (debate S-002, B won).
2. From Variant B (Sec 5): per-row "Keeps / Keeps with a cost / Endangers" verdicts in the invariant table, replacing A's all-"Preserved" table (debate S-003, B won).
3. From Variant B (E4 and the Round 2 reach finding): the reach limit stated plainly, narrower than quick phases alone (workflow reaches a panel only on rubric escalation; tasklist only on forced-deep phases and rubric escalations).
4. From Variant B (Sec 3, E8): any later direct module adds keys only, `contract_version` stays "1.1", `reflect_*` unchanged, `effect` is module data; and the unpinned edits that module would need (the `artifacts` rule at `refs/return-contract.md:52`, nested-kind constants in `tests/skills/test_worker_contract.py`, companion-eval allow-list and staging).
5. From Variant B (Sec 6, E11-E13): the two-arm replay with loop and cost columns where arm D is the path E2 already measured, and the counter-evidence B itself carried (E11, E12, E13).
6. From Variant B (E9, Sec 8 third objection) and Round 2: the three-case account of what a plugin copy delivers, and a parity test per added plugin file (debate A-006, B won).
7. From Variant B (Sec 5 INV-J, INV-G): the INV-J endangerment for a revise loop and the INV-G read-only reviewer requirement for any plugin reviewer agent.
8. From the Round 2.5 probe: the conditions under which the merged text holds (HIGH items INV-001, INV-002, INV-003, INV-005, INV-007, INV-013, INV-014) recorded as open conditions and a corrected "advisory-blocking" wording for Stage 10.5.
