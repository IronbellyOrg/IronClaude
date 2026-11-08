# Base Selection

## Metadata
- Variants scored: 3 (v1 analyzer/sonnet, v2 qa/haiku, v3 refactorer/opus)
- Scoring protocol: hybrid quantitative (50%) + qualitative 30-criterion CEV rubric (50%), refs/scoring-protocol.md
- Position-bias mitigation: two passes (forward v1, v2, v3; reverse v3, v2, v1)
- Inputs: variant-{1,2,3}-original.md (verbatim copies of the reviewer cards)

## Quantitative Scoring (50% weight)

| Metric | Weight | v1 | v2 | v3 |
|--------|--------|----|----|----|
| Requirement Coverage (RC) | 0.30 | 0.316 | 0.623 | 0.491 |
| Internal Consistency (IC) | 0.25 | 1.000 | 1.000 | 1.000 |
| Specificity Ratio (SR) | 0.15 | 1.000 | 0.991 | 1.000 |
| Dependency Completeness (DC) | 0.15 | 1.000 | 1.000 | 1.000 |
| Section Coverage (SC) | 0.15 | 1.000 | 0.800 | 1.000 |
| **Quant score** | | **0.795** | **0.856** | **0.847** |

### Computation details
- **RC.** The source for this run is the requirement-ID set the three cards were assigned to judge. The cards audit different slices, so the denominator is the union of every `T-N`, `INF-NNN` and `AC-N` ID that appears in any card: 114 IDs (13 T, 76 INF, 25 AC). A variant matches an ID when it names it (grep `\b(T|INF|AC)-[0-9]+\b`). v1 has 36/114 (13 T, 22 INF, 1 AC), v2 has 71/114 (1 T, 45 INF, 25 AC) and v3 has 56/114 (1 T, 54 INF, 1 AC). Keyword fuzzy matching was not applied, because every requirement in the slices carries a formal ID.
- **IC.** Scorable claims are findings, coverage judgements and listed citations: v1 has 60 (5 + 35 + 20), v2 has 93 (2 + 25 AC + 46 slice rows + 20 named-test rows) and v3 has 83 (8 + 55 + 20). Each card was searched for opposing claims about the same subject, requirement-constraint conflicts and impossible sequences, and none were found inside any single card. Disagreements between cards (for example, INF-123 judged covered by v2 and partially_covered by v3) are cross-variant, so they do not count toward IC. Coverage rows that v1 marks "Not re-read in detail" are unsupported claims, not contradictions; they are scored under Correctness criterion 5.
- **SR.** Concrete indicator = a substantive line containing a number, line citation, threshold or named entity. Vague indicators were counted with grep against the protocol list (appropriate, as needed, properly, adequate(ly), should consider, might, various, etc., best practices, industry standard). Results: v1 133 concrete, 0 vague (1.000); v2 115 concrete, 1 vague (line 34, "adequately specified", 115/116 = 0.991); v3 232 concrete, 0 vague (1.000).
- **DC.** Internal references are cross-references to a card's own finding IDs outside their definition and calibration keys: v1 has 7, v2 has 3 and v3 has 5. Every one resolves to a defined finding (for example v1 line 88 "See R1-001", v2 line 43 "R2-001 identifies", v3 line 306 "(R3-002)"). References to DF-NN, TF and design lines are external documents and are excluded.
- **SC.** The cards use two formats. Top-level content sections were counted as YAML top-level content blocks for v1 and v3 (findings, coverage_judgements, self_audit, citations, calibration = 5; the scalar metadata keys reviewer, persona, model_class, best_practice_grade and self_confidence are excluded as metadata) and as H2 headings for v2 (Deviations, Adherence summary, Notes, Calibration = 4). Max = 5, so the scores are v1 1.0, v2 0.8 and v3 1.0.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness
| # | Criterion | v1 | v2 | v3 |
|---|-----------|----|----|----|
| 1 | Covers all explicit requirements from source | MET: "Judgements are given for every row in the brief's Coverage slice (T-1..T-13 plus 22 INF rows)" (l.149) | MET: "All 25 acceptance criteria and all 46 Coverage-slice rows received semantic judgments" (l.154) | MET: 55 coverage_judgements (l.83-303) plus self_audit "Check 1 ... Check 5" (l.306) |
| 2 | Edge cases and failure scenarios | MET: R1-001 "boundary at `attempts` == 3" (l.13) | MET: R2-002 "inject an append `OSError` and a final-save failure" (l.17) | MET: R3-002 "one pre-existing finding leaves the gate with no passing path" (l.20) |
| 3 | Dependencies and prerequisites | MET: R1-004 fix "Add a Phase 1 preflight that proves xdist resolves offline" (l.69) | MET: AC table maps implementing, test and gate items, e.g. "AC-6 / 4.1b, 4.1c, 6.2 / 6.7, 8.2" (l.43) | MET: R3-002 fix "Add a Phase 1 item that records `make lint` ... on the unchanged tree" (l.28) |
| 4 | Success/completion criteria | MET: R1-001 fix "a `failed` entry with `attempts` == 3 is never eligible" (l.21) | MET: R2-001 fix "asserts `revalidation_failed`, no entry and no launcher call" (l.16) | MET: R3-002 fix "define PASS as no finding in a task-touched file and no finding missing from that baseline" (l.28) |
| 5 | Explicitly out of scope | MET: "Not read in this session: tasklist Phases 1-3, Gates A-D ..." (l.155) | MET: "Review boundary: This was a pre-execution review" (l.149) | MET: "Not read: the Gate D steps (619-672), the bodies of Steps 9.M4 to 9.M13" (l.306) |
| | **Subtotal** | **5/5** | **5/5** | **5/5** |

### Correctness
| # | Criterion | v1 | v2 | v3 |
|---|-----------|----|----|----|
| 1 | No factual errors or hallucinated claims | NOT MET: self_audit "I found no blocking defect" (l.125). The debate upheld X-001 (its own R1-002) and X-008 as blocking, 3/3 | NOT MET: INF-123 and INF-155 judged covered under DF-05. The debate resolved X-003 and X-004 as partially_covered 3/3, which v2 conceded | NOT MET: R3-006 (l.59) reports a declared deviation (DF-46, R06:180) as a defect. The debate dropped it 3/3 (C-007) |
| 2 | Technical approaches feasible | MET: R1-005 fix `git diff --exit-code HEAD -- pyproject.toml Makefile .github/` (l.84) | MET: R2-002 fix uses `run_cycle` with injected `OSError` (l.17) | MET: R3-002 baseline-plus-carve-out fix (l.28), upheld as feasible in X-008 |
| 3 | Terminology consistent and accurate | MET: brief severity enum (minor) and category enum used throughout (l.7-8, 23-24) | NOT MET: uses "MEDIUM" severity and "Drift" (l.16-17), outside the brief's binary severity and category enums (S-003, S-004 resolved 3/3) | MET: enum severity and categories throughout (l.7-8, 18-19) |
| 4 | No internal contradictions | MET: IC = 1.000 | MET: IC = 1.000 | MET: IC = 1.000 |
| 5 | Claims supported by evidence | NOT MET: several coverage rows rest on "Not re-read in detail" (l.115-120) | MET: every finding carries verbatim design and tasklist quotes (l.16-17) | MET: each finding has verbatim evidence, and coverage notes state their basis, e.g. l.87 "eager import declared as DF-29" |
| | **Subtotal** | **3/5** | **3/5** | **4/5** |

### Structure
| # | Criterion | v1 | v2 | v3 |
|---|-----------|----|----|----|
| 1 | Logical section ordering | MET: findings, coverage_judgements, self_audit, citations, calibration (l.5-179) | MET: Deviations, Adherence summary, Notes, Calibration (l.12-159) | MET: same order as v1 (l.5-329) |
| 2 | Consistent hierarchy depth | MET: uniform YAML list items | MET: H3 only under the H2 "Adherence summary" (l.32, 64, 117) | MET: uniform YAML list items |
| 3 | Separation of concerns | MET: findings and coverage kept apart | MET: deviations, coverage and notes kept apart | MET: findings and coverage kept apart |
| 4 | Navigation aids / cross-references | MET: l.88 "See R1-001" | MET: l.43 "R2-001 identifies missing revalidation cases" | MET: l.306 "(R3-002)" |
| 5 | Follows artifact-type conventions | MET: YAML card schema (S-001 resolved YAML 3/3) | NOT MET: markdown tables, not the YAML card schema (S-001) | MET: YAML card schema |
| | **Subtotal** | **5/5** | **4/5** | **5/5** |

### Clarity
| # | Criterion | v1 | v2 | v3 |
|---|-----------|----|----|----|
| 1 | Unambiguous language | MET: 0 vague indicators | MET: the single hit, "adequately specified" (l.34), defines the term "Covered" and is not hedging (re-evaluated, see the position-bias table) | MET: 0 vague indicators |
| 2 | Concrete rather than abstract | MET: SR 1.000 | MET: SR 0.991 | MET: SR 1.000 |
| 3 | Each section has a clear purpose | MET: self_audit states "Coverage of my own checks" (l.126) | MET: bold-labelled Notes bullets (l.149-154) | MET: self_audit numbered "Check 1..5" (l.306) |
| 4 | Acronyms and terms defined on first use | NOT MET: "DF-43", "FU-1" and "BASE" are used undefined (l.88, 100, 26) | NOT MET: "DF-05" and "AC-14" are used undefined | NOT MET: "DF-29" and "INF-105" are used undefined (l.84-87) |
| 5 | Actionable next steps | MET: every finding has a `fix` | MET: every finding ends "Fix Step ..." | MET: every finding has a `fix` |
| | **Subtotal** | **4/5** | **4/5** | **4/5** |

### Risk Coverage
| # | Criterion | v1 | v2 | v3 |
|---|-----------|----|----|----|
| 1 | At least 3 risks with probability and impact | MET: 5 findings, each with severity and a finding_confidence (l.190-194) | NOT MET: only 2 findings (l.16-17) | MET: 8 findings, each with severity and a finding_confidence |
| 2 | Mitigation for each risk | MET: every finding has a `fix` | MET: both findings have a fix | MET: every finding has a `fix` |
| 3 | Failure modes and recovery | MET: R1-002 fix "HALT for the owner" (l.36) | MET: R2-002 asserts "lock release" after failure (l.17) | MET: R3-003 fix "attempt cap ... followed by HALT" (l.37) |
| 4 | External dependencies and their failure | MET: R1-004 "resolution fails if xdist is not in the local uv cache" (l.61) | MET: "Unverified reply shapes are consistently assigned to assumed fixtures" (l.153) | MET: self_audit "unverified reply shapes are confined by the 9.F3 prompt" (l.306) |
| 5 | Monitoring / validation mechanism | MET: R1-005 adds a `--cached` listing check (l.84) | MET: "Run through Steps 6.10 and 9.4" (l.16-17) | MET: R3-008 "write a NEEDS OWNER DECISION line" (l.82) |
| | **Subtotal** | **5/5** | **4/5** | **5/5** |

### Invariant & Edge Case Coverage
| # | Criterion | v1 | v2 | v3 |
|---|-----------|----|----|----|
| 1 | Collection boundaries | NOT MET: INF-129 cap is judged "Not re-read in detail" (l.116); no boundary analysis | MET: INF-130 "Rolling-window boundaries and six-launch cap have explicit tests" (l.108) | MET: "consumed_log is kept through reset_entry and the day-cap count stays 6" (l.219) |
| 2 | State variable interactions across boundaries | MET: R1-002 Done status against the gated tree (l.26-29) | MET: R2-001 "reused initial approval/Project evidence at revalidation" (l.16) | MET: R3-001 working tree against commit and gated tree (l.9) |
| 3 | Guard condition gaps | MET: R1-005 G-10 misses staged changes (l.75) | MET: R2-001 revalidation guard untested (l.16) | MET: R3-003 "no attempt cap and no HALT" (l.32) |
| 4 | Count divergence (off-by-one, inclusive/exclusive) | MET: R1-001 "T-2 and T-3 boundary at `attempts` == 3" (l.13) | NOT MET: T-2 "boundary tests" judged covered with no off-by-one analysis (l.70) | MET: "half-open 10-minute boundary; the attempts < 3 check is applied in run_cycle" (l.283) |
| 5 | Interaction effects | MET: R1-003 withdrawn branch against the verbatim-prompt rule (l.41) | MET: R2-002 formatter wired into a real cycle (l.17) | MET: R3-007 format run against the two-line diff check (l.69) |
| | **Subtotal** | **4/5** | **4/5** | **5/5** |

## Qualitative Summary

| Dimension | v1 | v2 | v3 |
|-----------|----|----|----|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 3/5 | 3/5 | 4/5 |
| Structure | 5/5 | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 5/5 | 4/5 | 5/5 |
| Invariant & Edge Case | 4/5 | 4/5 | 5/5 |
| **Total** | **26/30** | **24/30** | **28/30** |
| **Qual score** | **0.867** | **0.800** | **0.933** |

## Position-Bias Mitigation

| Variant | Criterion | Pass 1 (forward) | Pass 2 (reverse) | Agreement | Final (after re-evaluation) |
|---------|-----------|------------------|------------------|-----------|-----------------------------|
| v2 | Clarity 1 | NOT MET (one vague-list hit, "adequately", l.34) | MET (the word defines "Covered" and does not hedge) | Disagree | MET: the sentence fixes the meaning of a term, so it is not ambiguous language |
| v1 | Invariant 1 | MET (INF-129 call cap judged covered) | NOT MET (the judgement is "Not re-read in detail", l.116) | Disagree | NOT MET: there is no boundary analysis, only a coverage assertion without support |
| v2 | Invariant 4 | MET (l.70 "boundary tests") | NOT MET (v2 missed the attempts<3 conjunct that v1 found) | Disagree | NOT MET: the row asserts that boundary tests exist and does not examine the boundary |

All other criteria (87 of 90 verdicts) agreed across both passes.

## Edge Case Floor Check

| Variant | Invariant & Edge Case score | Floor (>=1/5) | Eligible as base |
|---------|-----------------------------|---------------|------------------|
| v1 | 4/5 | Pass | Yes |
| v2 | 4/5 | Pass | Yes |
| v3 | 5/5 | Pass | Yes |

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | Final score |
|---------|---------------|--------------|-------------|
| v1 | 0.795 x 0.50 = 0.397 | 0.867 x 0.50 = 0.433 | **0.831** |
| v2 | 0.856 x 0.50 = 0.428 | 0.800 x 0.50 = 0.400 | **0.828** |
| v3 | 0.847 x 0.50 = 0.424 | 0.933 x 0.50 = 0.467 | **0.890** |

## Margin Analysis
- Top: v3 at 0.890. Second: v1 at 0.831. Margin 0.060.
- The margin is at least 0.05, so the tiebreaker protocol (A.4) was **not applied**.

## Selected Base: Variant 3 (refactorer, opus)

### Selection rationale
v3 has the highest qualitative score (28/30). It loses only Correctness 1 (R3-006, a declared deviation reported as a defect, dropped in C-007) and Clarity 4, which all three cards miss. It also carries the two findings the debate upheld as blocking: R3-001 (X-001, with R1-002) and R3-002 (X-008). Its blocking/minor split matches the consensus resolution of C-010, where the blocking set is X-001 and X-008. Its quantitative score (0.847) is within 0.01 of v2, which has the highest RC because it lists every AC ID. v3 already uses the required YAML card schema and severity enum (S-001, S-003, S-004), so merging into it needs no format conversion.

### Strengths to preserve from the base (v3)
- R3-001 and R3-002 as blocking findings, with their fixes (Step 10.6/10.7 re-gate or report-only; Phase 1 lint baseline plus carve-outs in 3.G2, 9.F2, 9.F11 and 9.F16).
- Minor findings R3-003, R3-004, R3-005, R3-007 and R3-008 (debate points C-004, C-005, C-006, C-008 and C-009, all upheld minor).
- Coverage judgements INF-105..INF-157, including the corrected automatic "none" mappings (INF-108, 122, 135, 147, 153).

### Strengths to incorporate from non-base variants
- From v1: R1-002 as a co-source of M-001 (X-001). Minor findings R1-001 (X-002, T-2 attempts<3 conjunct), R1-003 (C-001), R1-004 (C-002) and R1-005 (C-003). T-1..T-13 coverage and INF-016 coverage, resolved to covered.
- From v2: R2-001 (X-007, AC-6 revalidation cases) and R2-002 (X-006, AC-14/INF-146 cycle-level stderr-fallback test) as minor findings. AC-6 and AC-14 coverage rows resolved to partially_covered.
- Resolutions that change base content: R3-006 is dropped as a declared deviation (DF-46, R06:180). INF-123 and INF-155 stay partially_covered under DF-05, and that is not a defect. INF-146 and INF-138 move to partially_covered (X-006, X-007).
