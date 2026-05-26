# Base Selection — Fix B Proposals

## Quantitative Scoring (50% weight)

| Metric | Weight | Opus | Sonnet | Notes |
|---|---|---|---|---|
| Requirement Coverage (RC) | 0.30 | 1.00 | 0.94 | Opus covers all 3 factors + the `populate` correctness gain; Sonnet covers 3 factors but misses `populate` |
| Internal Consistency (IC) | 0.25 | 0.95 | 0.95 | Both internally consistent; no contradictions within their own text |
| Specificity Ratio (SR) | 0.15 | 0.85 | 0.82 | Both highly specific (regex deltas, line refs); Opus marginally more |
| Dependency Completeness (DC) | 0.15 | 0.92 | 0.85 | Opus has more explicit cross-references to existing tests with PASS/AT_RISK status |
| Section Coverage (SC) | 0.15 | 1.00 | 0.83 | Opus has explicit §2.5 (architectural rationale) + §5 (effort estimate) sections Sonnet lacks |

**Quant score formula**: `(RC×0.30) + (IC×0.25) + (SR×0.15) + (DC×0.15) + (SC×0.15)`

- Opus: (1.00×0.30) + (0.95×0.25) + (0.85×0.15) + (0.92×0.15) + (1.00×0.15) = 0.30 + 0.2375 + 0.1275 + 0.138 + 0.15 = **0.953**
- Sonnet: (0.94×0.30) + (0.95×0.25) + (0.82×0.15) + (0.85×0.15) + (0.83×0.15) = 0.282 + 0.2375 + 0.123 + 0.1275 + 0.1245 = **0.895**

## Qualitative Scoring (50% weight) — 30-criterion CEV

### Completeness (5 criteria)

| # | Criterion | Opus | Sonnet |
|---|---|---|---|
| 1 | Covers all explicit requirements | MET (3 factors + `populate`) | MET (3 factors) |
| 2 | Addresses edge cases | MET (`if not idents` branch explicit) | NOT MET (hash fallback obscures empty-set semantics) |
| 3 | Includes dependencies | MET | MET |
| 4 | Defines success criteria (test plan) | MET (5 tests with TUIBBS fixtures + 2 regression checks) | MET (6 test cases) |
| 5 | Specifies out-of-scope | MET (§5 "no changes to gate/executor/AST") | NOT MET (implicit only) |

**Subtotals**: Opus 5/5, Sonnet 3/5.

### Correctness (5 criteria)

| # | Criterion | Opus | Sonnet |
|---|---|---|---|
| 1 | No factual errors | MET | MET |
| 2 | Technically feasible | MET | MET |
| 3 | Terminology consistent | MET | MET |
| 4 | No internal contradictions | MET | MET |
| 5 | Claims have evidence (file:line) | MET | MET |

**Subtotals**: Opus 5/5, Sonnet 5/5.

### Structure (5 criteria)

| # | Criterion | Opus | Sonnet |
|---|---|---|---|
| 1 | Logical section ordering | MET | MET |
| 2 | Consistent hierarchy | MET | MET |
| 3 | Clear separation of concerns | MET (§2.1-2.5 cleanly partitioned) | MET (Parts 1-3) |
| 4 | Navigation aids | MET | MET |
| 5 | Follows conventions | MET | MET |

**Subtotals**: Opus 5/5, Sonnet 5/5.

### Clarity (5 criteria)

| # | Criterion | Opus | Sonnet |
|---|---|---|---|
| 1 | Unambiguous language | MET | MET |
| 2 | Concrete actions | MET | MET |
| 3 | Each section has clear purpose | MET | MET |
| 4 | Acronyms defined | MET (acceptable for code-change proposal) | MET |
| 5 | Actionable next steps | MET | MET |

**Subtotals**: Opus 5/5, Sonnet 5/5.

### Risk Coverage (5 criteria)

| # | Criterion | Opus | Sonnet |
|---|---|---|---|
| 1 | Identifies 3+ risks | MET (enumeration brittleness, `test_sequential_id_assignment` soft risk, broader counter-argument) | MET (hash collision, extractor narrowing, stem-coverage false positive) |
| 2 | Provides mitigation per risk | MET (each risk has concrete code-level mitigation cited) | NOT MET (stem-coverage mitigation is "could be added later" without concrete diff) |
| 3 | Failure modes | MET | MET |
| 4 | External dependencies | MET (none beyond stdlib) | MET |
| 5 | Monitoring/validation | MET (explicit pytest command + test list) | MET |

**Subtotals**: Opus 5/5, Sonnet 4/5.

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | Opus | Sonnet |
|---|---|---|---|
| 1 | Boundary conditions for collections (empty-set ident handling) | MET (explicit `if not idents: return sig in seen`) | NOT MET (handled only via `len(idents) < 2` hash fallback path) |
| 2 | State variable interactions | MET | MET |
| 3 | Guard condition gaps | MET (explicit guard in `_signature_subsumed`) | NOT MET (implicit via length-check) |
| 4 | Count divergence | MET | MET |
| 5 | Interaction effects (between the 3 changes) | MET (§2.5 explicitly articulates how the 3 parts compose) | NOT MET (implicit only) |

**Subtotals**: Opus 5/5, Sonnet 2/5.

**Edge Case Floor Check**: threshold 1/5. Opus 5/5 → ELIGIBLE. Sonnet 2/5 → ELIGIBLE (above floor).

### Qualitative Summary

| Dimension | Opus | Sonnet |
|---|---|---|
| Completeness | 5/5 | 3/5 |
| Correctness | 5/5 | 5/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 |
| Risk Coverage | 5/5 | 4/5 |
| Invariant & Edge Case | 5/5 | 2/5 |
| **Total** | **30/30** | **24/30** |

**Qual scores**:
- Opus: 30/30 = **1.000**
- Sonnet: 24/30 = **0.800**

## Position-Bias Mitigation

Pass 1 (Opus first, Sonnet second) and Pass 2 (Sonnet first, Opus second) were both conducted. Disagreements found:

| Criterion | Variant | Pass 1 | Pass 2 | Final |
|---|---|---|---|---|
| Completeness #2 (Sonnet edge-case coverage) | Sonnet | NOT MET | NOT MET | NOT MET (agreement) |
| Risk Coverage #2 (Sonnet mitigation completeness) | Sonnet | NOT MET | NOT MET | NOT MET (agreement) |
| Invariant #5 (Sonnet interaction-effects articulation) | Sonnet | NOT MET | NOT MET | NOT MET (agreement) |

No pass-1/pass-2 disagreements occurred. All Sonnet "NOT MET" verdicts were stable across orderings.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | Combined |
|---|---|---|---|
| Opus | 0.953 × 0.50 = 0.4765 | 1.000 × 0.50 = 0.500 | **0.9765** |
| Sonnet | 0.895 × 0.50 = 0.4475 | 0.800 × 0.50 = 0.400 | **0.8475** |

**Margin**: 0.129 (12.9%) — above 5% tiebreaker threshold. No tiebreaker needed.

## Selected Base: Variant 1 (Opus) — combined score 0.9765

### Selection Rationale

Opus wins on the dimensions that matter most for the gate's mission:

1. **Robust dedup semantics (C-003)**: Subsumption is strictly more general than exact-match for the asymmetric-identifier-set case that A-001 surfaces. Sonnet's solution depends empirically on identifier sets being equal across context windows — a fragile assumption.

2. **`populate` verb addition (U-001)**: This is a real correctness gain Sonnet missed. Post-Fix-A roadmaps use "populates the dispatch table" (TUIBBS-scp roadmap.md:396) and Sonnet's `impl_verbs` does not include it.

3. **Invariant & Edge Case dimension (5/5 vs 2/5)**: Opus explicitly articulates how the three changes compose (§2.5) and handles the empty-identifier boundary case. Sonnet's empty-set handling is reachable only via the hash-fallback path, which is correct-by-coincidence rather than correct-by-design.

4. **Architectural framing**: Opus's framing of "three contributing factors are one design flaw" is more durable as documentation than Sonnet's "three minimal changes" framing. Future maintainers reading the diff will understand WHY the refactor was structured this way.

### Strengths to Preserve (from Opus base)

- `mechanism_signature: tuple[str, frozenset[str]]` field on `IntegrationContract` with default value
- `_signature_subsumed` with strict-subset + intersection rule
- Compound-noun pattern in DISPATCH_PATTERNS[0]
- `dispatch_family` regex in the coverage check
- Adding `populate` to `impl_verbs`
- §2.5 architectural rationale
- §6 explicit strongest counter-argument

### Strengths to Incorporate (from Sonnet)

1. **Explicit `DISPATCH_TABLE` alternation** in the tightened pattern (U-004). Opus matches it via `dispatch[_\s]?table` + IGNORECASE, but Sonnet's explicit alternation is clearer for readers and removes a class of "did the IGNORECASE catch this?" review confusion. Cheap to merge.

2. **Generic stem-based fallback** (U-006) as a TERTIARY coverage check (after `dispatch_family` regex and identifier-substring match). The stem fallback works for ANY compound mechanism noun (middleware_chain, event_binding, di_container), filling a gap Opus's dispatch-family-only approach leaves. Same-line constraint preserved to limit semantic looseness.

3. **Sonnet's own §counter-argument mitigation** ("secondary check that the stem match's surrounding context shares at least one identifier with the contract's spec_evidence") should be adopted NOW, not as future work. The merged proposal will require the stem-match path to verify at least one of the contract's `mechanism_signature` identifiers appears in the matching roadmap line's 3-line window. This directly defeats the "Implement priority dispatch for logging" false-positive class Sonnet acknowledged.

### Edge Case Floor

Both variants pass. No suspension required.
