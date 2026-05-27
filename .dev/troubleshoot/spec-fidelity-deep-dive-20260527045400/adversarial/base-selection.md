# Base Selection — Adversarial Scoring

## Quantitative Scoring (50% weight)

Per the scoring rubric: 5 metrics computed deterministically from artifact text.

| Metric | Weight | fix-1 | fix-2 | fix-3 | fix-4 | fix-5 |
|---|---|---|---|---|---|---|
| Requirement Coverage (RC) — does the proposal address the cited TUIBBS failure? | 0.30 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| Internal Consistency (IC) — does the proposal have internal contradictions? | 0.25 | 1.00 | 0.95 | 0.90 | 0.90 | 1.00 |
| Specificity Ratio (SR) — concrete vs vague language | 0.15 | 0.92 | 0.85 | 0.88 | 0.80 | 0.95 |
| Dependency Completeness (DC) — all referenced sections/files resolve | 0.15 | 1.00 | 0.95 | 1.00 | 0.90 | 1.00 |
| Section Coverage (SC) — does the proposal hit all sections of the template | 0.15 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| **quant_score** | — | **0.974** | **0.948** | **0.953** | **0.926** | **0.985** |

**Scoring notes**:
- IC: fix-2 has the INV-003 undefined-threshold gap (small inconsistency). fix-3 has the `roadmap_quote` regression (acknowledged in risks but no concrete mitigation in the minimal version). fix-4 introduces an `ADVISORY` tier without enumerating downstream consumers.
- SR: fix-4 uses more abstract language ("architectural completion of three precedents") than fix-1/5 (concrete LOC counts, exact line numbers, mechanical effect).
- DC: fix-2 references "FIXABILITY_GUIDANCE_TEMPLATES" but doesn't enumerate the templates. fix-4 references `Finding.severity` enum modification without specifying the exact file path of the enum.

## Qualitative Scoring (50% weight) — 30-criterion Additive Binary Rubric

### Completeness (5 criteria)

| Criterion | fix-1 | fix-2 | fix-3 | fix-4 | fix-5 |
|---|---|---|---|---|---|
| Covers all explicit requirements from source input (TUIBBS unblock + recurrence + restrictions) | 1 | 1 | 1 | 1 | 1 |
| Addresses edge cases and failure scenarios | 1 (over-canon risk) | 1 (mis-classification risk) | 1 (round-trip surprise) | 1 (downstream consumer audit) | 1 (hypothesis dep posture) |
| Includes dependencies and prerequisites | 1 | 1 | 1 | 1 | 1 |
| Defines success/completion criteria | 1 (54 HIGH → 0) | 1 | 1 | 1 | 1 |
| Specifies what is explicitly out of scope | 1 (no S6, no LLM drift) | 1 | 1 (no value-object refactor) | 1 (only ID-class) | 1 (no semantic drift) |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** |

### Correctness (5 criteria)

| Criterion | fix-1 | fix-2 | fix-3 | fix-4 | fix-5 |
|---|---|---|---|---|---|
| No factual errors or hallucinated claims | 1 | 1 | 1 | 1 | 1 |
| Technical approaches feasible with stated constraints | 1 | 0 (INV-003: threshold undefined makes the classifier non-deterministic) | 0 (minimal 12 LOC version breaks roadmap_quote; full version exceeds budget) | 1 (assuming consumer audit is performed) | 1 |
| Terminology used consistently and accurately throughout | 1 | 1 | 1 | 1 | 1 |
| No internal contradictions | 1 | 1 | 1 | 1 | 1 |
| Claims supported by evidence within the document | 1 | 1 | 1 | 1 | 1 |
| **Subtotal** | **5/5** | **4/5** | **4/5** | **5/5** | **5/5** |

### Structure (5 criteria)

| Criterion | fix-1 | fix-2 | fix-3 | fix-4 | fix-5 |
|---|---|---|---|---|---|
| Logical section ordering | 1 | 1 | 1 | 1 | 1 |
| Consistent hierarchy depth | 1 | 1 | 1 | 1 | 1 |
| Clear separation of concerns between sections | 1 | 1 | 1 | 1 | 1 |
| Navigation aids present | 1 | 1 | 1 | 1 | 1 |
| Follows conventions of the artifact type | 1 | 1 | 1 | 1 | 1 |
| **Subtotal** | **5/5** | **5/5** | **5/5** | **5/5** | **5/5** |

### Clarity (5 criteria)

| Criterion | fix-1 | fix-2 | fix-3 | fix-4 | fix-5 |
|---|---|---|---|---|---|
| Unambiguous language (no "should consider", "might") | 1 | 0 ("might wrongly classify"; "could theoretically") | 1 | 0 ("operators want a runtime knob — maybe true, maybe false") | 1 |
| Concrete rather than abstract | 1 | 1 | 1 | 0 (more architectural-pattern language) | 1 |
| Each section has clear purpose | 1 | 1 | 1 | 1 | 1 |
| Acronyms defined on first use | 1 | 1 | 1 | 1 | 1 |
| Actionable next steps clearly identified | 1 | 1 | 1 | 1 | 1 |
| **Subtotal** | **5/5** | **4/5** | **5/5** | **3/5** | **5/5** |

### Risk Coverage (5 criteria)

| Criterion | fix-1 | fix-2 | fix-3 | fix-4 | fix-5 |
|---|---|---|---|---|---|
| Identifies at least 3 risks with probability and impact | 1 (4 risks) | 1 (5 risks) | 1 (4 risks) | 1 (4 risks) | 1 (5 risks) |
| Provides mitigation strategy for each risk | 1 | 1 | 1 | 1 | 1 |
| Addresses failure modes and recovery procedures | 1 | 1 | 1 | 1 | 1 |
| Considers external dependencies and failure scenarios | 0 (doesn't enumerate downstream MEDIUM consumers) | 1 | 0 (doesn't enumerate roadmap_quote consumers) | 0 (acknowledges but doesn't perform consumer audit) | 1 (acknowledges hypothesis dep posture explicitly) |
| Includes monitoring/validation mechanism for risk detection | 0 | 0 | 0 | 0 | 1 (property-based + flatline tests ARE the monitor) |
| **Subtotal** | **3/5** | **4/5** | **3/5** | **3/5** | **5/5** |

### Invariant & Edge Case Coverage (5 criteria) — **Edge-case floor applies (1/5 minimum)**

| Criterion | fix-1 | fix-2 | fix-3 | fix-4 | fix-5 |
|---|---|---|---|---|---|
| Addresses boundary conditions for collections | 0 | 0 | 0 | 0 | 1 (flatline-halt test + cross-cutting integration) |
| Handles state variable interactions across component boundaries | 1 (registry passed-through; pass condition unchanged) | 1 | 1 (eliminates the boundary) | 1 | 1 |
| Identifies guard condition gaps | 0 | 0 | 1 (notes parse-time warning for collision) | 0 | 1 (Layer B(4) integration test) |
| Covers count divergence scenarios | 0 | 0 | 0 | 0 | 0 |
| Considers interaction effects when features combine | 1 (S5 + S2 + this fix combine cleanly) | 1 (fixability + canonicalizer combine) | 1 (eliminates seam ⇒ no future interaction) | 1 (CLI lane + severity tier) | 1 |
| **Subtotal** | **2/5** | **2/5** | **3/5** | **2/5** | **4/5** |
| **Edge-case floor** | PASS (≥1/5) | PASS | PASS | PASS | PASS |

### Qualitative Summary

| Variant | Completeness | Correctness | Structure | Clarity | Risk | Edge-case | Total | qual_score |
|---|---|---|---|---|---|---|---|---|
| fix-1 | 5 | 5 | 5 | 5 | 3 | 2 | **25/30** | 0.833 |
| fix-2 | 5 | 4 | 5 | 4 | 4 | 2 | **24/30** | 0.800 |
| fix-3 | 5 | 4 | 5 | 5 | 3 | 3 | **25/30** | 0.833 |
| fix-4 | 5 | 5 | 5 | 3 | 3 | 2 | **23/30** | 0.767 |
| fix-5 | 5 | 5 | 5 | 5 | 5 | 4 | **29/30** | 0.967 |

## Position-Bias Mitigation (Dual Pass)

Pass 1 (input order 1→2→3→4→5) and Pass 2 (reverse 5→4→3→2→1) were evaluated. Disagreements:

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Risk Coverage criterion 5 (monitoring/validation mechanism) | fix-5 | 1 (passes have value) | 1 (passes have value) | Agree | 1 |
| Edge-case criterion 1 (boundary conditions) | fix-5 | 1 (flatline test covers it) | 1 (cross-cutting test) | Agree | 1 |
| Clarity criterion 1 | fix-2 | 0 (hedged language) | 0 (hedged) | Agree | 0 |
| Clarity criterion 1 | fix-4 | 0 (operator-might language) | 0 (architectural-pattern language) | Agree | 0 |

No disagreements requiring re-evaluation. Disagreement rate: 0% (all 30 criteria × 5 variants = 150 cells; full agreement between passes).

## Combined Scoring

| Variant | quant_score (0.50) | qual_score (0.50) | Combined | Edge-case floor |
|---|---|---|---|---|
| fix-1 | 0.974 × 0.50 = 0.487 | 0.833 × 0.50 = 0.417 | **0.904** | PASS |
| fix-2 | 0.948 × 0.50 = 0.474 | 0.800 × 0.50 = 0.400 | **0.874** | PASS |
| fix-3 | 0.953 × 0.50 = 0.476 | 0.833 × 0.50 = 0.417 | **0.893** | PASS |
| fix-4 | 0.926 × 0.50 = 0.463 | 0.767 × 0.50 = 0.383 | **0.846** | PASS |
| fix-5 | 0.985 × 0.50 = 0.493 | 0.967 × 0.50 = 0.483 | **0.976** | PASS |

**Ranking**:
1. **fix-5** — 0.976
2. fix-1 — 0.904
3. fix-3 — 0.893
4. fix-2 — 0.874
5. fix-4 — 0.846

**Margin**: fix-5 vs fix-1 = 0.072 (7.2%) — outside the 5% tiebreaker band. **No tiebreaker required.**

## Selected Base: Variant 5 (fix-5: Tier 1 code + property-based + flatline-halt tests)

**Selection rationale**:
- Highest combined score (0.976) with margin >5% over runner-up.
- Highest Risk Coverage (5/5) — only proposal with a monitoring/validation mechanism (property-based tests as the monitor).
- Highest Edge-case Coverage (4/5) — flatline-halt integration test addresses the SPECIFIC failure shape; cross-cutting integration test addresses the all-fixes-unfixable scenario.
- Highest qual_score (0.967) with strongest test surface in the candidate set.
- Code change is IDENTICAL to fix-1 (mirror of `integration_contracts.py:445` precedent), so it inherits fix-1's lowest-blast-radius property.
- Mechanical sufficiency confirmed by INV-006 (all proposals drop 54 HIGHs to 0; fix-5's mechanism is identical to fix-1's).

**Strengths to preserve from base (fix-5)**:
- Layer A code: `_canonicalize_requirement_id` helper + phantom_id block modification at `structural_checkers.py:372-391`
- Layer B(1): 5 golden-fixture asymmetric-ID tests across all families
- Layer B(2): property-based test in NEW file `test_structural_checkers_properties.py` with `pytest.importorskip("hypothesis")` (respects "not declared dependency" posture, matches `tests/sprint/test_property_based.py` precedent)
- Layer B(3): flatline-halt integration test in `tests/roadmap/test_convergence.py` — locks the structurally-unfixable verdict shape
- Layer B(4): cross-cutting "all-findings-unfixable" integration test in `tests/roadmap/test_remediate_executor.py`

**Strengths to incorporate from non-base variants**:

| From | Strength | Integration point | Rationale |
|---|---|---|---|
| fix-3 | Note in `_canonicalize_requirement_id` docstring that the helper could move upstream into `extract_requirement_ids` in a future refactor; design helper signature `(family: str, raw: str) -> str` to support both checker-side and parser-side use | Helper definition in `structural_checkers.py` | Future-proofing for value-object refactor; explicit acknowledgment of the seam-elimination framing without committing to it now. |
| fix-2 | Add a docstring on the `_canonicalize_requirement_id` helper noting that the demoted-to-MEDIUM rule_id `id_schema_drift` is a SPECIFIC INSTANCE of the broader "fixability" concept; flag in the helper for future generalization | Comment block in helper | Records the deeper structural insight without committing to the ~30 LOC scaffolding now. |
| fix-4 | Defer the `--strict-no-advisory` CLI flag to a follow-up release; do NOT introduce a new severity tier in this fix | (Not incorporated; documented as deferred) | The ADVISORY tier's audit burden is not justified by a single rule_id; defer until 2+ drift classes are identified. |
| fix-1 | The minimal-code framing is preserved verbatim in fix-5 Layer A (fix-5 explicitly inherits fix-1's code) | (Already in base) | — |

**Strengths NOT incorporated (changes-not-made)**:

| Source | Proposal | Why rejected |
|---|---|---|
| fix-3 | Move `_canonicalize_requirement_id` into `extract_requirement_ids` (parser-side) | Breaks `Finding.roadmap_quote` at `structural_checkers.py:389`; the minimal-LOC framing of fix-3 doesn't survive that mitigation. Document upstream relocation as a future refactor path. |
| fix-2 | Add `_classify_fixability` + `FIXABILITY_GUIDANCE_TEMPLATES` + modify `_make_finding` to accept `fixability` arg | INV-003 (HIGH UNADDRESSED): the `CLASS_DRIFT` count threshold is undefined, making the classifier non-deterministic. Without a defined threshold the scaffolding is unsafe to ship. Reconsider for next release with a defined calibration. |
| fix-4 | New `ADVISORY` severity tier + CLI flags `--allow-advisory-drift` / `--strict-no-advisory` | New severity tier introduces ongoing audit burden on every `Finding.severity` consumer; CLI flag is a permanent API surface. Only justified if 2+ drift classes need taxonomic distinction. Currently 1 (ID-schema). Defer. |
| fix-2 | `FIXABILITY_GUIDANCE_TEMPLATES` dict alongside existing `FIX_GUIDANCE_TEMPLATES` | Same INV-003 concern; the templates are well-formed but they're keyed on a classifier whose deterministic operation is not yet defined. |

**Unresolved diff points carried to the return contract**:
- A-001 (spec immutability assumption) — surfaced as a follow-up question for product/team alignment
- A-002 (canonicalization direction) — documented in the helper docstring; chosen direction is "strip leading zeros" with rationale
- A-003 (30% diff guard correctness) — S3 from backlog remains deferred; no debate in this round
- X-002 (root-cause framing: comparator vs fixability) — partially resolved (the comparator IS where this fix lives; the fixability framing is documented as future work)
