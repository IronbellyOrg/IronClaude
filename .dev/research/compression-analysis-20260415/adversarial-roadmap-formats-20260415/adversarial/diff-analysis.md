# Step 1: Diff Analysis

**Date**: 2026-04-15
**Mode**: Mode B (generate + compare), Blind
**Variants under analysis**: 3 (labels anonymized — V-A, V-B, V-C)
**Source under evaluation**: `claudedocs/research_roadmap-format-alternatives_20260415.md`
**Focus areas**: quantitative-claims, benchmark-provenance, recommendation-validity, haiku-model-risk, toon-maturity
**Convergence target**: 0.85

---

## Blind Variant Key (preserved for merge step; hidden during debate)

| Label | Variant file | Role tag (hidden from debate) |
|-------|--------------|-------------------------------|
| V-A | variant-1-opus-analyzer.md | Claim auditor / attacker |
| V-B | variant-2-opus-architect.md | Steelman / defender |
| V-C | variant-3-sonnet-scribe.md | Methodological auditor |

Blind mode requirement: subsequent debate rounds MUST refer to variants as V-A/V-B/V-C only. Role tags are sealed until Step 5 merge execution.

---

## Part 1: Structural Diff

| Variant | Major sections | Length | Distinctive structural feature |
|---------|----------------|--------|--------------------------------|
| V-A | 5 parts (Claim Audit / Math Re-derivation / Direct Measurement / First-Principles Ranking / Flagged Hallucinations) | ~290 lines | Tabular claim-audit matrix with verdict column |
| V-B | 7 parts (Pillar 1 XML / Pillar 2 TOON / Pillar 3 Prose / Weaknesses / Prototype / Haiku Risk / Ranked List) | ~300 lines | Only variant with live `tiktoken cl100k_base` code/measurements |
| V-C | 6 parts (Benchmark Inventory / Missing Benchmarks / Haiku Weighting / Sample Size / Confirmation Bias / Bias-Aware Recommendation) | ~265 lines | Only variant with a benchmark-inventory grid listing symmetric-search verdicts |

**Structural severity**: LOW. All three use section-based organization compatible with merge. No contradictory structural requirements.

---

## Part 2: Content Diff (Topic-by-Topic)

### D-1: Top-ranked format

| Variant | Rank #1 | Rank #2 | Rationale |
|---------|---------|---------|-----------|
| V-A | Compact Markdown DSL | Compact MD + TOON tables only | "-20% to -25% measured; no new format dependency" |
| V-B | Compact Markdown DSL | Hybrid XML+TOON+prose | "-33.4% measured on Phase 2 slice via tiktoken" |
| V-C | XML + Markdown (no TOON) | (TOON as Phase 2 A/B migration) | "Avoids TOON correctness risk from arXiv 2601.12014" |

**Convergence**: PARTIAL (2/3 pick Compact MD DSL as #1; 1/3 picks XML+MD).
**Severity**: HIGH.
**Taxonomy**: L2 (structural — format choice is an architecture decision).

### D-2: Headline -35% to -50% savings claim

| Variant | Verdict | Defensible ceiling |
|---------|---------|-------------------|
| V-A | UNSUPPORTED (hand-waved arithmetic) | -13% to -20% on hybrid; -20-25% on Compact MD DSL |
| V-B | FALSIFIED by direct measurement | -12.0% measured on Phase 2 slice (hybrid); -33.4% measured (Compact MD DSL) |
| V-C | NOT SUPPORTED by evidence chain | -25% to -32% at most (arithmetic re-derivation) |

**Convergence**: UNANIMOUS REJECTION of the -35% to -50% headline as currently formulated.
**Severity**: HIGH.
**Taxonomy**: L3 (falsifiable quantitative claim).

### D-3: Hybrid XML+TOON+prose status

| Variant | Ranking | Justification for keeping it viable |
|---------|---------|-------------------------------------|
| V-A | #4 of 6 | "Worth it only if you already need XML for reliability" |
| V-B | #2 of 5 | "Value prop should be reliability + selective loading, NOT compression" |
| V-C | Migration target | "Requires Phase 2 A/B empirical validation before adoption" |

**Convergence**: PARTIAL — all 3 keep the hybrid defensible but demote it from #1.
**Severity**: HIGH.
**Taxonomy**: L2 (architecture — value proposition framing).

### D-4: Anthropic "up to 30% quality gain" attribution

| Variant | Treatment |
|---------|-----------|
| V-A | EXPLICIT MISATTRIBUTION FLAG: "30% is for query-at-end placement, NOT XML tags" with verbatim Anthropic quote |
| V-B | Softens to "Anthropic-recommended disambiguation scaffold"; notes the doc disclaims "trained priors" framing |
| V-C | Flags as "speculative neuroscience language" without verbatim quote |

**Convergence**: FULL — all 3 agree the source's 30% framing is an overreach.
**Severity**: HIGH.
**Taxonomy**: L3 (falsifiable specific-source claim).

### D-5: arXiv 2604.03616 "The Format Tax" applicability

| Variant | Treatment |
|---------|-----------|
| V-A | "Paper says closed-weight frontier models show little to no format tax — **WEAKENS** the source's case for format engineering on Claude 4.6" |
| V-B | Not directly addressed |
| V-C | "Undermines the urgency of optimizing away from Markdown on frontier models" |

**Convergence**: V-A + V-C in agreement; V-B silent.
**Severity**: HIGH.
**Taxonomy**: L3 (falsifiable citation semantics).

### D-6: arXiv 2603.03306 (TOON vs JSON) cherry-picking

| Variant | Treatment |
|---------|-----------|
| V-A | EXPLICIT: "Paper says 'Plain JSON shows best one-shot and final accuracy'; report suppresses this adverse finding" |
| V-B | Not addressed |
| V-C | Cited as "appropriately used" in the inventory but not cross-checked for completeness |

**Convergence**: UNIQUE to V-A.
**Severity**: HIGH if V-A is right.
**Taxonomy**: L3 (falsifiable citation integrity).

### D-7: Missing counter-benchmark arXiv 2601.12014 ("Are LLMs Ready for TOON?")

| Variant | Treatment |
|---------|-----------|
| V-A | NOT mentioned |
| V-B | NOT mentioned |
| V-C | "TOON structural correctness (GCS) is 38.9% lower than JSON, 30.9% lower than XML, 42.2% lower than YAML. Single strongest evidence of confirmation bias in source report." |

**Convergence**: UNIQUE to V-C — but carries extreme weight if the claim survives scrutiny.
**Severity**: HIGH.
**Taxonomy**: L3 (state-mechanics: TOON parser correctness is a guard/boundary condition).

### D-8: Source roadmap token composition — 9% tables vs 25% tables

| Variant | Treatment |
|---------|-----------|
| V-A | Direct measurement: "25.4% of chars in pipe-delimited rows; 47.7% in bullet lines; 6.2% numbered; 4.9% headings. Report's 9% table figure is implausible without extremely narrow 'scaffolding-only' definition" |
| V-B | Uses measurement but does not audit the source's compositional breakdown directly |
| V-C | Does not re-measure |

**Convergence**: UNIQUE to V-A — a testable factual claim.
**Severity**: MEDIUM (changes compression math but not direction of recommendation).
**Taxonomy**: L3 (measurement fidelity, state-of-document).

### D-9: Haiku risk weighting fairness

| Variant | Verdict |
|---------|---------|
| V-A | "Bounded; 60-token conventions header reliably closes the MD↔JSON gap on Haiku" |
| V-B | "Bounded concern, not killer — mitigated by conservative XML+MD fallback" |
| V-C | "UNFAIR weighting — 0.5pp TOON-vs-JSON gap cited, but hybrid format never benchmarked; format-switching cognitive load unmeasured" |

**Convergence**: SPLIT — V-A/V-B say bounded; V-C says insufficiently hedged.
**Severity**: MEDIUM.
**Taxonomy**: L3 (state-mechanics: Haiku model behavior + format-switching).

### D-10: Selective-loading as justification for the hybrid

| Variant | Position |
|---------|----------|
| V-A | NEGATIVE: "Deferring tokens is not saving tokens; if all agents read every phase the savings evaporate" |
| V-B | AFFIRMATIVE: "Hybrid's actual strength is unambiguous `<phase id=N>` anchors for per-phase context loading in /sc:pm, /sc:tasklist — I would rerank it to #1 the moment per-phase loading ships" |
| V-C | Silent |

**Convergence**: DIRECT CONTRADICTION V-A vs V-B.
**Severity**: HIGH — only one can be right, depends on actual consumer behavior.
**Taxonomy**: L2 (architecture — consumption pattern).

### D-11: Format-switching cognitive load

| Variant | Position |
|---------|----------|
| V-A | Not addressed |
| V-B | Not addressed |
| V-C | "Agent must parse XML structure, switch to TOON for tables, switch to Markdown for prose — cognitive load of format-switching within a single document is unbenchmarked" |

**Convergence**: UNIQUE to V-C.
**Severity**: MEDIUM.
**Taxonomy**: L3 (state-mechanics: parser context switching).

### D-12: "Trained priors" framing strength

| Variant | Position |
|---------|----------|
| V-A | Not addressed at this level (focuses on 30% misattribution) |
| V-B | "Anthropic explicitly clarifies on the same docs page that there are NO canonical 'best' XML tags Claude is specifically trained on. Mechanism is 'unambiguous delimiter pairs + RLHF exposure,' not 'trained priors'" |
| V-C | "'Activates trained structural priors' is speculative neuroscience language" |

**Convergence**: V-B + V-C agree the source's "trained priors" framing is too strong.
**Severity**: MEDIUM.
**Taxonomy**: L3 (falsifiable claim about Claude internals).

### D-13: Benchmark search symmetry

| Variant | Position |
|---------|----------|
| V-A | Implicitly addressed by the claim audit (catches misapplications) |
| V-B | Implicitly addressed by discovering the dev.to/Medium Codex disputes |
| V-C | EXPLICIT: "No evidence of symmetric search. Of 12 cited sources, 2 are TOON-favorable academic, 0 are TOON-critical academic. Asymmetric sampling." |

**Convergence**: FULL (different framings, same finding).
**Severity**: HIGH.
**Taxonomy**: L2 (methodology — search protocol).

### D-14: Direct `tiktoken` measurement on an actual phase slice

| Variant | Output |
|---------|--------|
| V-A | Character-based estimates only; predicts 3,450-3,680 tokens for Compact MD DSL |
| V-B | **Actual tiktoken cl100k_base measurements**: Original MD 350 → Hybrid 308 (-12.0%) → XML-only 316 (-9.7%) → Compact MD DSL 233 (-33.4%). Plus risk table: MD 255 → TOON 218 (-14.5%) |
| V-C | Arithmetic re-derivation only; no direct measurement |

**Convergence**: UNIQUE to V-B — **this is the most falsifiable empirical contribution in the entire variant pool**.
**Severity**: HIGH — objectively verifiable.
**Taxonomy**: L3 (state-mechanics: tokenizer output).

---

## Part 3: Contradictions (Specific + Falsifiable)

| ID | Claim (V-X) | Counter-claim (V-Y) | Resolution method |
|----|-------------|---------------------|-------------------|
| C-1 | V-A: "Compact MD DSL is #1" | V-C: "XML + Markdown is #1 (Compact MD DSL not ranked top)" | Apply V-B's tiktoken measurement on a larger slice + invariant probe on accuracy delta |
| C-2 | V-B: "Selective loading is the hybrid's primary value — rerank to #1 the moment per-phase loading ships" | V-A: "Deferred tokens are not saved tokens; whole-file read patterns dominate" | Debate must surface empirical evidence of actual consumption pattern in /sc:pm and /sc:tasklist |
| C-3 | V-A + V-B: "Webmaster-ramos Haiku numbers (69.6/75.3/74.8) are reliable" | V-B-secondary: "dev.to critical-analysis article reports Haiku at ~50% across all formats on a different suite" | Benchmark provenance audit — is webmaster-ramos the authoritative Claude measurement? |
| C-4 | V-C: "arXiv 2601.12014 shows TOON has 30-42% structural correctness penalty" | V-B: "Medium Codex aggregate study shows TOON at 73.9% accuracy, highest of all formats" | Cross-check both papers' methodology; identify which subset of use cases favors each result |
| C-5 | V-A + V-B: "Hybrid's best-case compression ceiling ≈ -13% to -22%" | Source (target): "-35% to -50%" | V-B's tiktoken measurement settles this — unless the measurement slice is unrepresentative |

**Contradiction severity**: 5 HIGH, 0 MEDIUM, 0 LOW.

---

## Part 4: Unique Contributions

| # | Contribution | Variant | Value |
|---|--------------|---------|-------|
| U-1 | Anthropic 30% misattribution with verbatim quote from long-context-tips doc | V-A | HIGH |
| U-2 | Direct tiktoken cl100k_base measurement: Phase 2 slice 350 → 308 (-12%); Compact MD DSL 350 → 233 (-33.4%) | V-B | HIGH |
| U-3 | arXiv 2601.12014 "Are LLMs Ready for TOON?" — GCS correctness penalty 30-42% vs JSON/XML/YAML | V-C | HIGH |
| U-4 | arXiv 2604.03616 Format Tax paper applies *against* the source report on closed-weight frontier models | V-A + V-C | HIGH |
| U-5 | arXiv 2603.03306 cherry-picked: paper's own conclusion is "Plain JSON generation shows best accuracy," suppressed in source | V-A | HIGH |
| U-6 | Direct composition re-measurement: tables are 25.4% not 9%; bullets are 47.7% (non-TOON-izable) | V-A | MEDIUM |
| U-7 | Itemized Compact MD DSL savings breakdown: 19.2% floor, rising to 25% with preamble compaction | V-A | MEDIUM |
| U-8 | Reframing of hybrid's value prop from "compression" to "reliability + selective loading" | V-B | MEDIUM |
| U-9 | Symmetric-search audit grid: 12 benchmarks classified by methodology match + search symmetry | V-C | MEDIUM |
| U-10 | Format-switching cognitive load hypothesis (parser context switching XML→TOON→MD→XML→TOON) | V-C | MEDIUM |
| U-11 | 3-phase migration path: XML+MD now → Phase 2 A/B → conditional TOON | V-C | MEDIUM |
| U-12 | Anthropic doc disclaimer: "no canonical best XML tags Claude is specifically trained on" | V-B | MEDIUM |

---

## Part 5: Shared Assumptions (with classification)

| ID | Assumption | Classification | Notes |
|----|------------|---------------|-------|
| A-001 | The target file (`roadmap-opus-architect.md`) is representative of the class of files we want to optimize | UNSTATED | All 3 variants measure on this single file; promotes to [SHARED-ASSUMPTION] diff point. **L2.** |
| A-002 | Token savings on the source file generalize across all SuperClaude roadmap files | UNSTATED | No variant validates on >1 file. **L2.** |
| A-003 | Webmaster-ramos Claude accuracy numbers (69.6/75.3/74.8 on Haiku; 89-93 on Sonnet/Opus) are reliable | STATED in source, CONTRADICTED by V-B's discovery of dev.to critique | **L3.** |
| A-004 | TOON is a viable production format | **CONTRADICTED across variants**: V-A conditional, V-B partial with caveats, V-C "NO — 30-42% correctness penalty" | **L3.** |
| A-005 | Accuracy matters more than raw token count on frontier models | STATED | All 3 implicitly concede this. **L3.** |
| A-006 | Convention/primer headers amortize across many agent invocations (≥5 calls) | UNSTATED | V-A states explicitly; others implicit. **L2.** |
| A-007 | Downstream consumer behavior (whole-file vs selective) is knowable in advance | UNSTATED | **Direct contradiction (C-2)** between V-A and V-B. **L2.** |
| A-008 | Claude's Markdown training-data dominance makes Markdown prose the format-of-least-resistance | STATED in source, REINFORCED by V-B pillar 3 | **L2.** |
| A-009 | Closed-weight frontier models are format-agnostic on reasoning tasks (per arXiv 2604.03616) | UNSTATED | V-A + V-C cite; source does not integrate. **L3.** |

### Shared assumptions promoted to synthetic diff points

- **[SHARED-ASSUMPTION A-001/A-002]**: Generalization from N=1 file. **L2.**
- **[SHARED-ASSUMPTION A-003]**: Webmaster-ramos benchmark authoritativeness. **L3.**
- **[SHARED-ASSUMPTION A-006]**: Convention-header amortization threshold. **L2.**
- **[SHARED-ASSUMPTION A-007]**: Downstream consumption pattern as knowable. **L2.**
- **[SHARED-ASSUMPTION A-009]**: Format-tax paper applicability to Claude 4.6. **L3.**

---

## Part 6: Debate Topic Taxonomy (auto-tagged)

Mutually exclusive level assignment per diff point (priority L3 > L2 > L1). Fallback L2 if no signals match.

| Diff point | Level | Signal terms matched |
|------------|-------|---------------------|
| D-1 top-ranked format | **L2** | "architecture", "format" |
| D-2 -35% to -50% headline | **L3** | "validation rule", "falsifiable claim" |
| D-3 hybrid value proposition | **L2** | "architecture", "value proposition" |
| D-4 Anthropic 30% misattribution | **L3** | "validation rule", "specific claim" |
| D-5 Format Tax paper applicability | **L3** | "validation rule", "citation semantics" |
| D-6 arXiv 2603.03306 cherry-pick | **L3** | "validation rule", "citation integrity" |
| D-7 arXiv 2601.12014 correctness penalty | **L3** | "guard", "boundary", "correctness" |
| D-8 token composition fidelity | **L3** | "boundary", "measurement", "state" |
| D-9 Haiku weighting fairness | **L3** | "state", "model behavior", "weighting" |
| D-10 selective-loading justification | **L2** | "architecture", "consumption pattern" |
| D-11 format-switching cognitive load | **L3** | "state", "transition", "parser" |
| D-12 trained-priors framing | **L3** | "validation rule", "claim about internals" |
| D-13 benchmark search symmetry | **L2** | "methodology", "search protocol" |
| D-14 tiktoken direct measurement | **L3** | "measurement", "state" |
| [SHARED-ASSUMPTION A-001/A-002] | **L2** | "architecture", "generalization" |
| [SHARED-ASSUMPTION A-003] | **L3** | "validation rule" |
| [SHARED-ASSUMPTION A-006] | **L2** | "architecture" |
| [SHARED-ASSUMPTION A-007] | **L2** | "consumption pattern" |
| [SHARED-ASSUMPTION A-009] | **L3** | "validation rule" |

**Level distribution**: 11 L3 / 8 L2 / 0 L1.

**State-mechanics gate coverage**: 11 L3 topics (≥ 30% of debate surface) — **taxonomy coverage gate PASSED**. Debate cannot bypass state-mechanics-level scrutiny.

---

## Part 7: Convergence Preview (before debate)

Pre-debate naive convergence count (diff points where all 3 variants align on the same direction):

| Diff point | V-A | V-B | V-C | Aligned? |
|------------|-----|-----|-----|----------|
| D-2 headline -35-50% is unsupported | REJECT | REJECT | REJECT | **YES** |
| D-3 hybrid demoted from #1 | YES (to #4) | YES (to #2) | YES (migration target) | **YES** |
| D-4 Anthropic 30% overstated | YES | YES | YES | **YES** |
| D-13 asymmetric benchmark search | YES | YES | YES | **YES** |
| [SA A-001/A-002] N=1 generalization risk | Implicit | Implicit | Explicit | **YES** |
| D-1 top-ranked format | CMD DSL | CMD DSL | XML+MD | NO |
| D-5 Format Tax paper against source | YES | Silent | YES | PARTIAL |
| D-6 arXiv 2603.03306 cherry-picked | YES | Silent | Silent | NO |
| D-7 arXiv 2601.12014 correctness penalty | Silent | Silent | YES | NO |
| D-8 25% not 9% tables | YES | Silent | Silent | NO |
| D-9 Haiku fair weighting | Bounded | Bounded | Unfair | NO |
| D-10 selective-loading value | REJECT | AFFIRM | Silent | CONTRADICTED |
| D-11 format-switching load | Silent | Silent | YES | NO |
| D-12 trained-priors framing | Silent | Soften | Soften | PARTIAL |
| D-14 tiktoken measurement | N/A | YES | N/A | N/A |

**Pre-debate convergence**: 5 full alignments out of 15 substantive points = **0.33**.
**Convergence target**: 0.85.
**Delta to close via debate**: 0.52 (10+ points to move into alignment).

The bulk of the debate surface is not "left vs right" disagreement — it is "one variant found evidence the others did not." Round 1 steelman cross-exposure should close several of these quickly (e.g., V-A + V-B will accept V-C's arXiv 2601.12014 once they see it; V-C will adjust Haiku weighting once it sees V-A's conventions-header argument).

The HARD remaining disagreements after evidence cross-exposure will likely be:
1. **D-1**: Compact MD DSL vs XML+MD as #1 (requires invariant probe on correctness risk)
2. **D-10**: Selective-loading value (requires evidence on actual consumer behavior)
3. **D-9**: Haiku weighting fairness (requires invariant probe on format-switching load)

---

## Summary

- 3 variants, 14 substantive diff points + 5 shared-assumption promotions
- **Unanimous finding**: the source report's -35% to -50% headline is not defensible as currently formulated
- **Near-unanimous finding**: the Hybrid XML+TOON+prose recommendation should not be primary without amendments
- **Splits remain on**: which alternative is better (Compact MD DSL vs XML+MD), and whether selective-loading salvages the hybrid
- **Killer evidence brought by single variants** (V-A: Anthropic 30% misattribution; V-B: tiktoken measurement; V-C: arXiv 2601.12014) must be cross-exposed in Round 1 of debate — any variant that misses another's HIGH-value unique contribution will lose convergence mass
- **State-mechanics coverage**: 11 L3 topics — debate cannot skip state-level scrutiny
- **Pre-debate convergence**: 0.33 (target 0.85, delta 0.52)

**Ready for Interactive Checkpoint 1.**
