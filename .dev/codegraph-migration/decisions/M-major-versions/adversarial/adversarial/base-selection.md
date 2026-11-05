# Base Selection

Requirements used for coverage: the decision question (what happens on a 1.x to 2.0.0 candidate) plus the four focus areas: (R1) safety of Phase 3 skills that call codegraph tools, (R2) reviewer burden, (R3) code paths to test, (R4) fit with the rule that a human merges. Verified facts from context.md are the correctness baseline.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (A) | V2 (B) | V3 (C) | Computation notes |
|--------|--------|--------|--------|--------|-------------------|
| Requirement Coverage (RC) | 0.30 | 0.75 | 1.00 | 1.00 | A never addresses Phase 3 skills by name or mechanism (R1 only via the cost line); B and C cover R1 to R4. |
| Internal Consistency (IC) | 0.25 | 0.83 | 0.86 | 1.00 | A: rationale "the proof plus the human merge is the review" contradicts its own cost line (1 of 6 claims). B: code line "one comparison plus an issue step" omits the within-major selector its cost line relies on (1 of 7). C: none of 7. |
| Specificity Ratio (SR) | 0.15 | 0.86 | 0.88 | 0.89 | Concrete: titles, flags, labels, states. Vague: "normal-looking" (A); "ways the proof cannot see" (B); "the label and title tell them apart" (C). |
| Dependency Completeness (DC) | 0.15 | 1.00 | 0.67 | 1.00 | B's "if the script picks the newest release within the pinned major" depends on a rule B does not define (2 of 3 resolved). External references (sibling decision) excluded. |
| Section Coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | Each has the same five sections (no H2s; bullet sections counted). |
| **quant_score** | | **0.862** | **0.898** | **0.984** | (RC×0.30)+(IC×0.25)+(SR×0.15)+(DC×0.15)+(SC×0.15) |

## Qualitative Scoring (50% weight): Additive Binary Rubric

### Completeness
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | Covers explicit requirements | MET | MET | MET | Each answers the question with a defined major-path output. |
| 2 | Edge cases and failure scenarios | MET | MET | MET | A: semantic 2.0 passes proof; B: minors while major pending; C: draft overload. |
| 3 | Dependencies and prerequisites | MET | MET | MET | A/C: "Same pipeline" / "shares every other step"; B: `--allow-major`. |
| 4 | Success/completion criteria | MET | MET | MET | Ready PR on pass; issue opened; draft until marked ready. |
| 5 | Explicit out of scope | NOT | MET | NOT | Only B states an exclusion: "does not create a branch or PR". |

### Correctness
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | No factual errors | NOT | MET | MET | A's "the proof plus the human merge is the review" contradicts the verified fact that the proof does not check tool semantics. C's "label and title" claim holds via the title. |
| 2 | Feasible with constraints | NOT | MET | MET | A inlines notes of 76,281 chars; feasibility not shown (GitHub body limit unverified). |
| 3 | Terminology consistent | MET | MET | MET | Consistent use of pin, proof, PR. |
| 4 | No internal contradictions | NOT | NOT | MET | Matches IC findings above. |
| 5 | Claims supported by rationale | MET | MET | MET | Each has a Rationale line. |

### Structure
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | Logical ordering | MET | MET | MET | Behaviour, rationale, cost, code. |
| 2 | Consistent hierarchy | MET | MET | MET | Flat bullets under H1. |
| 3 | Separation of concerns | MET | MET | MET | Rationale, cost and code are separate bullets. |
| 4 | Navigation aids | NOT | NOT | NOT | None; searched all lines. |
| 5 | Artifact-type conventions | MET | MET | MET | All follow the shared option-file shape. |

### Clarity
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | Unambiguous language | MET | NOT | MET | B hedges: "if the script picks the newest release within the pinned major". |
| 2 | Concrete | MET | MET | MET | Named titles, flags, states. |
| 3 | Each section has a clear purpose | MET | MET | MET | One concern per bullet. |
| 4 | Terms defined in the document | MET | NOT | NOT | B and C use "Phase 3 skills" without defining it in the file (defined only in context.md). |
| 5 | Actionable next steps | NOT | MET | MET | A gives no reviewer action beyond "notice the MAJOR word"; B gives commands; C gives a checklist. |

### Risk Coverage
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | 3+ risks with probability and impact | NOT | NOT | NOT | No variant rates probability. |
| 2 | Mitigation per risk | NOT | MET | MET | A names the risk but leaves it on the reviewer; B mitigates semantic risk (no PR) and minor flow (selector); C mitigates overload (title/label). |
| 3 | Failure modes and recovery | NOT | MET | MET | B: manual `--allow-major` run; C: person marks draft ready. |
| 4 | External dependency failure | NOT | NOT | NOT | None discuss GitHub API or label availability failure. |
| 5 | Monitoring/validation mechanism | MET | MET | MET | Proof (A, C); issue as signal (B); checklist (C). |

### Invariant and Edge Case Coverage
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | Collection boundaries (several newer releases) | NOT | MET | NOT | Only B says which release is picked when several are newer. |
| 2 | State interactions across components | NOT | MET | MET | B: pending major vs minor bumps; C: draft state shared with failed-proof path. |
| 3 | Guard condition gaps | MET | MET | MET | All name the proof's blind spot on tool semantics. |
| 4 | Count divergence / range boundaries | NOT | NOT | NOT | None define the major comparison for prerelease tags (A-001). |
| 5 | Interaction effects | NOT | MET | MET | B: minors bump while major waits; C: draft meaning collision. |

### Qualitative Summary
| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 4 | 5 | 4 |
| Correctness | 2 | 4 | 5 |
| Structure | 4 | 4 | 4 |
| Clarity | 4 | 3 | 4 |
| Risk Coverage | 1 | 3 | 3 |
| Invariant & Edge Case | 1 | 4 | 3 |
| **Total / 30** | **16 (0.533)** | **23 (0.767)** | **23 (0.767)** |

### Edge Case Floor Check
- V1: 1/5, eligible. V2: 4/5, eligible. V3: 3/5, eligible.

## Position-Bias Mitigation
- Pass 1 order: V1, V2, V3. Pass 2 order: V3, V2, V1. Both passes were run by the orchestrator in-context (not by independent agents), which limits their independence.
- Disagreements found: 2. (a) V3 Correctness-1: pass 2 first marked NOT because the `codegraph-major` label does not exist; re-evaluated to MET because the claim names the title as a disambiguator, which works without the label. (b) V1 Risk-2: pass 1 first marked MET ("MAJOR" word as mitigation); re-evaluated to NOT because V1's own cost line says the reviewer "must notice" it, which is not a mitigation strategy.
- Verdicts changed by re-evaluation: 2 (both now as shown above).

## Combined Scoring
| Variant | Quant (×0.5) | Qual (×0.5) | Final |
|---------|--------------|-------------|-------|
| V1 (A) | 0.431 | 0.267 | **0.697** |
| V2 (B) | 0.449 | 0.383 | **0.832** |
| V3 (C) | 0.492 | 0.383 | **0.875** |

- Margin V3 over V2: 0.043 (4.3%), under 5%, so the tiebreaker applies.
- Tiebreaker level 1 (debate points won): V3 = 5, V2 = 4. Not within 5% of each other; V3 wins at level 1.

## Selected Base: Variant 3 (Option C, draft PR for majors)

**Selection rationale.** Highest combined score, most debate points won, zero internal contradictions, and all three advocates (including A's and B's) recommended C as the base of the merge. It keeps the full automated evidence for the riskiest release while using the only hard non-mergeable state available.

**Strengths to preserve.** Same verify + rewrite + proof for majors; draft always, even when the proof passes; checklist naming Phase 3 skills that call codegraph tools; one comparison in shared code.

**Strengths to incorporate.**
- From V2 (B): candidate selection within the pinned major (U-003, C-005); idempotency by fixed identifier (U-001, A-003); link-only release notes (C-007); keep draft meanings distinct (X-003).
- From V1 (A): no extra manual path; one shared pipeline (C-004), so B's `--allow-major` manual route is not adopted.
- From shared assumptions: strict tag parsing with prerelease skip (A-001).
