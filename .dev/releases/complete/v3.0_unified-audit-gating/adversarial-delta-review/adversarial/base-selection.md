# Base Selection: Adversarial Delta Review

## Quantitative Scoring (50% weight)

### Per-Metric Scores

| Metric | Weight | Variant 1 (Architect) | Variant 2 (Analyzer) | Variant 3 (Scribe) |
|--------|--------|----------------------|---------------------|---------------------|
| Requirement Coverage (RC) | 0.30 | 0.85 — covers all 5 focus areas; addresses all 11 deltas and 7 NRs | 0.90 — covers all focus areas; addresses all deltas/NRs + 10 new findings | 0.80 — covers all focus areas but evaluates from spec perspective only; misses MF-1 class findings |
| Internal Consistency (IC) | 0.25 | 0.90 — consistent OVERSTATED/ACCURATE taxonomy; one self-identified count error (8 OVERSTATED includes items not in Delta list) | 0.85 — consistent CONFIRMED/PARTIALLY_CONFIRMED taxonomy; SprintGatePolicy described as "stub" and "not a pure stub" in same doc | 0.92 — highly consistent spec-quality framework; no internal contradictions identified |
| Specificity Ratio (SR) | 0.15 | 0.82 — cites specific file:line evidence for most claims; some claims lack counter-evidence ("could be intentionally preserved") | 0.95 — every finding backed by specific file:line with independent verification; highest evidence density | 0.78 — provides corrected language but many claims are spec-interpretation without code verification |
| Dependency Completeness (DC) | 0.15 | 0.80 — cross-references between sections; P2a/P2b proposal references prior findings | 0.88 — MF-1 through MF-10 are self-referentially complete; cross-references to delta analysis | 0.85 — well-structured cross-references to spec sections; NR redundancy check is systematic |
| Section Coverage (SC) | 0.15 | 0.83 — 5 sections covering all required areas | 0.92 — 6 sections with dedicated MISSED FINDINGS section expanding coverage | 1.00 — 8 sections; broadest structural coverage (highest section count) |

### Quantitative Scores

| Variant | RC×0.30 | IC×0.25 | SR×0.15 | DC×0.15 | SC×0.15 | Total |
|---------|---------|---------|---------|---------|---------|-------|
| Variant 1 | 0.255 | 0.225 | 0.123 | 0.120 | 0.125 | **0.848** |
| Variant 2 | 0.270 | 0.213 | 0.143 | 0.132 | 0.138 | **0.895** |
| Variant 3 | 0.240 | 0.230 | 0.117 | 0.128 | 0.150 | **0.865** |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| Covers all explicit requirements from source input | MET — all deltas and NRs addressed | MET — all addressed + 10 new | MET — all addressed from spec perspective |
| Addresses edge cases and failure scenarios | NOT MET — did not identify MF-1 class failures | MET — MF-1, MF-10 (preflight bypass) | NOT MET — missed MF-1 entirely |
| Includes dependencies and prerequisites | MET — P2/P3 dependency identified | MET — MF-1 as architectural prerequisite | NOT MET — called phase chain "clean" |
| Defines success/completion criteria | NOT MET — identifies problems but no criteria | NOT MET — identifies problems but no criteria | MET — 10 missing acceptance criteria catalogued |
| Specifies what is explicitly out of scope | NOT MET | NOT MET | MET — "not a spec requirement" framing for NR-7 |
| **Subtotal** | **2/5** | **3/5** | **3/5** |

### Correctness (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| No factual errors or hallucinated claims | MET — all file:line citations verified | MET — highest verification rigor | MET — spec-level claims verified |
| Technical approaches feasible with stated constraints | MET — runtime derivation alternative is valid | MET — forensic approach is replicable | MET — corrected language is implementable |
| Terminology used consistently and accurately | MET | NOT MET — "stub" used then retracted | MET |
| No internal contradictions | MET | NOT MET — SprintGatePolicy characterization inconsistency | MET |
| Claims supported by evidence | MET | MET — strongest evidence base | NOT MET — some claims based on spec interpretation without code verification |
| **Subtotal** | **5/5** | **3/5** | **4/5** |

### Structure (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| Logical section ordering | MET | MET | MET |
| Consistent hierarchy depth | MET | MET | MET |
| Clear separation of concerns | MET | MET | MET |
| Navigation aids present | NOT MET — no summary table until end | MET — tables throughout | MET — tables and cross-references |
| Follows conventions of artifact type | MET | MET | MET |
| **Subtotal** | **4/5** | **5/5** | **5/5** |

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| Unambiguous language | MET | MET | MET |
| Concrete rather than abstract | MET — specific code citations | MET — specific code citations | NOT MET — some claims at spec-interpretation level |
| Each section has clear purpose | MET | MET | MET |
| Acronyms and domain terms defined | NOT MET | NOT MET | MET — defines spec section references |
| Actionable next steps identified | MET — revised phase ordering proposed | MET — severity reclassifications proposed | MET — corrected replacement language provided |
| **Subtotal** | **4/5** | **4/5** | **4/5** |

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| Identifies at least 3 risks | MET — false dependencies, severity inflation, missing coverage | MET — MF-1, GateResult collision, orphaned code | MET — ambiguous language, missing criteria, spec drift |
| Provides mitigation strategy for each risk | MET — revised phase ordering | NOT MET — identifies risks but minimal mitigation | MET — corrected language is the mitigation |
| Addresses failure modes and recovery | NOT MET | MET — branch (a)/(b) implicitly surfaced | NOT MET |
| Considers external dependencies | MET — cli/audit/ module dependency | MET — cli/audit/, cleanup_audit/ | NOT MET — focused on spec-internal |
| Includes monitoring or validation mechanism | NOT MET | NOT MET | MET — acceptance criteria as validation |
| **Subtotal** | **3/5** | **3/5** | **3/5** |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| Addresses boundary conditions for collections | NOT MET | MET — empty/dead code paths identified | NOT MET |
| Handles state variable interactions | NOT MET | MET — MF-1 state interaction with audit model | NOT MET |
| Identifies guard condition gaps | MET — auto-resume call-site guard noted | MET — watchdog disabled-by-default identified | NOT MET |
| Covers count divergence scenarios | NOT MET | MET — 2-field vs 13-field GateResult | NOT MET |
| Considers interaction effects | MET — P2/P3 chicken-and-egg | MET — MF-1 interaction with task-scope model | NOT MET |
| **Subtotal** | **2/5** | **5/5** | **0/5** |

### Edge Case Floor Check

| Variant | Invariant Score | Eligible? |
|---------|----------------|-----------|
| Variant 1 | 2/5 | Yes (≥1/5) |
| Variant 2 | 5/5 | Yes (≥1/5) |
| Variant 3 | 0/5 | **NO — below 1/5 floor** |

**Edge case floor applied**: Variant 3 is ineligible as base variant due to 0/5 on Invariant & Edge Case Coverage. Variant 3's strengths (corrected language, acceptance criteria) must be incorporated via merge, not as the base.

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|-----------|----|----|-----|
| Completeness | 2/5 | 3/5 | 3/5 |
| Correctness | 5/5 | 3/5 | 4/5 |
| Structure | 4/5 | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 3/5 | 3/5 |
| Invariant & Edge Case | 2/5 | 5/5 | 0/5 |
| **Total** | **20/30** | **23/30** | **19/30** |
| **Qual Score** | **0.667** | **0.767** | **0.633** |

## Position-Bias Mitigation

Dual-pass evaluation performed (forward: V1→V2→V3, reverse: V3→V2→V1). No disagreements detected on the binary criteria — all verdicts consistent across passes.

## Combined Scoring

| Variant | Quant (50%) | Qual (50%) | Combined | Rank |
|---------|-------------|------------|----------|------|
| Variant 1 (Architect) | 0.424 | 0.333 | **0.757** | 2 |
| Variant 2 (Analyzer) | 0.448 | 0.383 | **0.831** | **1** |
| Variant 3 (Scribe) | 0.433 | 0.317 | **0.749** | 3* |

*Variant 3 ineligible as base due to edge case floor. Rank is for merge priority.

### Tiebreaker Analysis

Not required — Variant 2 leads by 7.4% margin over Variant 1 (exceeds 5% threshold).

## Selected Base: Variant 2 (opus:analyzer — Forensic Analyst Validation)

### Selection Rationale

Variant 2 is selected as the base for four evidence-backed reasons:

1. **Highest completeness**: Only variant to discover 10 missed findings (MF-1 through MF-10), including the CRITICAL MF-1 (execute_phase_tasks dead code) that all three advocates converged on as the single most consequential finding.

2. **Strongest evidence base**: Every finding independently verified against the codebase with specific file:line citations. Highest specificity ratio (0.95) across all variants.

3. **Best invariant coverage**: Perfect 5/5 on edge case and invariant analysis — the only variant to identify boundary conditions (2-field vs 13-field GateResult), state interactions (MF-1 impact on task-scope model), and guard condition gaps (watchdog disabled by default).

4. **Debate performance**: Won the most contested diff points outright (X-005, C-009) and provided the strongest evidence for consensus positions (MF-1 concession drove both other advocates' Round 2 updates).

### Strengths to Preserve from Base
- 10 missed findings (MF-1 through MF-10) with full evidence
- Independent file:line verification methodology
- Severity reclassification evidence (NR-7 → CRITICAL, Delta 2.6 → HIGH)
- GateScope enum discovery, ShadowGateMetrics discovery, KPI partial wiring

### Strengths to Incorporate from Non-Base Variants

**From Variant 1 (Architect)**:
- NR-3 reclassification to recommended spec amendment (validated by INV-005)
- NR-5/NR-6 merge rationale
- P2a/P2b phase resequencing proposal
- NR-1 determinism reframing (auditability, not determinism)
- Revised severity table (6 downgrades with evidence)

**From Variant 3 (Scribe)**:
- Corrected §4.4 replacement language (all items)
- 10 missing acceptance criteria catalogue
- Line citations removal as systemic requirement
- Undefined terms list (AuditLease, audit_lease_timeout, max_turns, Critical Path Override, audit_gate_required, audit_attempts)
- 4 missing spec sections (§5.2, §7.2, §8, §10.3)
- §4.4 item 7 placement correction (→ §12.3/§12.4)
- NR-2 severity upgrade (LOW → MEDIUM)
- D1.2/D1.3 missing from summary table
