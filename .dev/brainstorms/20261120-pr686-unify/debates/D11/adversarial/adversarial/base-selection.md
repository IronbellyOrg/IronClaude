# Base Selection Report

Read this first: base selection scores the QUALITY OF THE TWO PAPERS as documents (how complete, correct, clear and risk-aware each is). It does not decide who wins the question. The winner of each diff point is in `debate-transcript.md` (scoring matrix: OURS 5, CLAY 2, HYBRID 7). The merged output is therefore the better-structured paper (Variant 2) with the debate outcome written into it.

## Quantitative Scoring (50% weight)

Source requirements used (no formal IDs in the source, so topic matching on the six items of the question): R1 one data source, R2 one report, R3 one dashboard, R4 living report, R5 nine-row table, R6 cap of 5 notices a day.

| Metric | Weight | Variant 1 (OURS) | Variant 2 (CLAY) |
|--------|--------|------------------|------------------|
| requirement_coverage | 0.30 | 0.833 (5 of 6: R1, R2, R3, R5, R6 addressed; R4 the living report is only mentioned as a design phrase, not decided) | 1.000 (6 of 6; R1 and R3 only loosely: "let the sweep and the observer feed or read it") |
| internal_consistency | 0.25 | 1.000 (0 contradictions found in the paper's claims) | 1.000 (0 found) |
| specificity_ratio | 0.15 | 0.964 (53 concrete indicators, 2 vague words; counted with grep for file:line, backticked identifiers, numbers with units, PR/issue/ruling numbers versus a list of vague words) | 1.000 (44 concrete, 0 vague) |
| dependency_completeness | 0.15 | 1.000 (internal references resolve; external issue and PR references excluded) | 1.000 |
| section_coverage | 0.15 | 1.000 (6 H2 sections; max across variants is 6) | 1.000 (6) |
| **quant_score** | | **0.9446** | **1.0000** |

Arithmetic: V1 = 0.30x0.833 + 0.25x1 + 0.15x0.964 + 0.15x1 + 0.15x1 = 0.2499 + 0.25 + 0.1446 + 0.15 + 0.15 = 0.9445. V2 = 0.30 + 0.25 + 0.15 + 0.15 + 0.15 = 1.000.

## Qualitative Scoring (50% weight): Additive Binary Rubric

Two independent evaluator agents (sonnet, read-only) scored all 30 criteria for both papers with Claim-Evidence-Verdict. Pass 1 evaluated A (OURS) then B (CLAY); Pass 2 evaluated B then A. Both passes agreed on 54 of 60 verdicts. The six disagreements were re-evaluated by the orchestrator (see Position-Bias Mitigation). Evidence shown is the shorter of the two passes' citations.

### Completeness (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| C1 covers all explicit requirements | NOT MET | living report appears only as a passing phrase, never proposed or rejected | NOT MET | no single data source or one dashboard specified, only "feed or read it" |
| C2 edge cases and failure scenarios | MET | "'could not determine' instead of guesses" | MET | "a failed read carries items, never closes them" |
| C3 dependencies and prerequisites | MET | "A contract note and a pinning test ... before the observer" | MET | "still says `/sc:orchestrator` and `.dev/coordinator/`" |
| C4 success or completion criteria | NOT MET | none found in all sections | NOT MET | none found in all sections |
| C5 out of scope | NOT MET | none found | NOT MET | none found |
| **Subtotal** | **2/5** | | **2/5** | |

### Correctness (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| K1 no factual errors | MET | `ALLOWED_ORCA` at `probes.py:49`, `observe/` has no `sweep` reference (spot checked on master) | MET | 142 tests, `"person": "clayphi"`, ruling 39 confirmed (one loose cite: ruling-39 text is at orchestrator.md line 1177, the paper says 1164 for OD13) | 
| K2 feasible approaches | MET | "additive change to schema v1 or a schema v2" | MET | "`run.py refresh` ... with no model call" |
| K3 consistent terminology | MET (re-evaluated) | "the report" mostly means the work report; "one dated report" for the sweep appears once | MET | work report and sweep named separately |
| K4 no internal contradictions | MET | none found | MET | none found |
| K5 evidence for claims | MET | numbered cited facts with paths | MET | numbered cited facts with paths |
| **Subtotal** | **5/5** | | **5/5** | |

### Structure (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| S1 logical order | MET | claim, mechanism, facts, costs, risks, gets right | MET | same order |
| S2 consistent depth | MET | uniform H2 sections | MET | uniform H2 sections |
| S3 separation of concerns | MET | "What it costs" versus "What it risks" | MET | same |
| S4 navigation aids | NOT MET | no contents or cross-references | NOT MET | none |
| S5 artifact conventions | MET | "What OURS gets right" | MET | "What CLAY gets right" |
| **Subtotal** | **4/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| L1 unambiguous language | MET (re-evaluated) | "it must sit on top of that source" | MET (re-evaluated) | "keep the report as the work-item layer" |
| L2 concrete | MET | "`ALLOWED_ORCA`, a fixed list of argv templates" | MET | "`templates/item-template.md` (73 lines)" |
| L3 clear section purpose | MET | each section has one job | MET | each section has one job |
| L4 terms defined on first use | NOT MET | "WC-16", "AD-B4" not defined | NOT MET | "OD13", "Step 4b", "Decision Desk" not defined |
| L5 actionable next steps | MET | "contract note and a pinning test" | MET | "Do not hold working code until a contract note" |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| R1 at least 3 risks with probability and impact | NOT MET | two risks, no probability or impact | NOT MET | two risks, no probability or impact |
| R2 mitigation for each risk | NOT MET | none in "What it risks" | NOT MET | none in "What it risks" |
| R3 failure modes and recovery | NOT MET | "may stay on paper" has no recovery | MET | "a failed read carries items, never closes them" |
| R4 external dependencies and failure | NOT MET | ClickUp token noted, no failure case | MET | "every source not read is listed under 'Not checked'" |
| R5 monitoring or validation for risk detection | NOT MET (re-evaluated) | the pinning test guards the schema, not the listed risks, and is unbuilt | MET | "No report that failed a check reaches Clay" (`check.py`, `run.py gate`) |
| **Subtotal** | **0/5** | | **3/5** | |

### Invariant and Edge Case Coverage (5 criteria)

| Criterion | OURS | Evidence | CLAY | Evidence |
|-----------|------|----------|------|----------|
| E1 collection boundaries | MET (re-evaluated) | "a cap on notices, with the entry ... never dropped" (maximum and overflow rule) | MET (re-evaluated) | "capped at 5 per repo per 24 hours; the entry on the page is never dropped" |
| E2 state variables across components | NOT MET | status words not compared | MET | "working, progressed ... against the sweep's eight classes" |
| E3 guard condition gaps | MET | `config.json` sets `"person": "clayphi"` (hard-coded) | MET | "DM and commit steps are writes the sweep ... forbid" |
| E4 count divergence | NOT MET | eight classes and nine rows never reconciled | NOT MET | "102 kept + 28" never reconciled with 142 |
| E5 interaction effects | MET | "for a while three outputs exist" | MET | "Three overlapping readers ... can disagree" |
| **Subtotal** | **3/5** | | **4/5** | |

### Qualitative Summary

| Dimension | OURS | CLAY |
|-----------|------|------|
| Completeness | 2/5 | 2/5 |
| Correctness | 5/5 | 5/5 |
| Structure | 4/5 | 4/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 0/5 | 3/5 |
| Invariant & Edge Case | 3/5 | 4/5 |
| **qual_score** | **18/30 = 0.600** | **22/30 = 0.733** |

### Edge Case Floor Check

Floor is 1/5 on Invariant & Edge Case Coverage. OURS 3/5 (eligible), CLAY 4/5 (eligible).

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| K3 | OURS | NOT MET | MET | DISAGREE | MET: "the report" is used for the work report throughout; the sweep's report is called "dated report" once |
| L1 | OURS | NOT MET | MET | DISAGREE | MET: the key sentences ("must sit on top of that source") are unambiguous |
| L1 | CLAY | NOT MET | MET | DISAGREE | MET: "keep the report as the work-item layer" is unambiguous; "feed or read it" is the one loose phrase |
| R5 | OURS | MET | NOT MET | DISAGREE | NOT MET: the only mechanism is a pinning test for the schema, unbuilt, and it does not detect the two risks the paper lists |
| E1 | OURS | MET | NOT MET | DISAGREE | MET: states a maximum (cap) and the overflow rule (entries never dropped) |
| E1 | CLAY | MET | NOT MET | DISAGREE | MET: same cap and overflow rule |

Disagreements re-evaluated: 6 of 60 criterion-variant pairs. Final verdicts changed from one of the two passes: 6 (each re-evaluation sides with one pass). Net effect: OURS 17 to 18, CLAY 21 to 22. The ranking does not change.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| 1 OURS (opus:architect) | 0.4723 | 0.3000 | **0.7723** | not needed |
| 2 CLAY (opus:analyzer) | 0.5000 | 0.3667 | **0.8667** | not needed |

**Margin**: 9.4 points (above the 5% threshold)
**Tiebreaker applied**: No

## Selected Base: Variant 2 (CLAY, opus:analyzer)

**Selection rationale.** The CLAY paper is the better document: it states how it handles failed reads and missing sources, names the status-vocabulary mismatch, and covers all six items of the question. Its gap (no single data source or dashboard decision) is the one the debate settled. This is a statement about the paper, not about who should win the question.

**Strengths to preserve (from the base):** the per-issue plain-English item template and the script gate (`check.py`, `run.py gate`); the silent-loss rules; the no-model living-report refresh; the honest cost list (one person's config, daily token cost, naming drift).

**Strengths to incorporate from OURS:**
- The sweep is the one source of session facts; stateless, zero-token, read-only, "recommend nothing" (`probes.py:49-56`, `sc-sweep-protocol/SKILL.md:61`) (C-001, C-004, X-001).
- The proof-based eight classes with "could not determine" are the only session states shown (C-008).
- The dependency direction and owner chain: watcher, orchestrator, dashboard; the observer is the one screen.
- Owner naming and layout win (C-010); person-specific values leave `config.json` (C-005).
- The cap and the nine rows are unbuilt policy, to be adopted as proposals pending the owner (C-006, C-007; `reach_daily_max` parser returns 0 today).
- The two HIGH invariants and the MEDIUM requirements from the probe (INV-001 to INV-012) as required statements.
