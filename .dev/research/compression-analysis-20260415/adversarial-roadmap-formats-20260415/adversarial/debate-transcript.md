# Debate Transcript: Research Validation of Roadmap Format Alternatives

**Pipeline**: `/sc:adversarial` Mode B — generate + compare from source
**Source**: `claudedocs/research_roadmap-format-alternatives_20260415.md`
**Depth**: deep (3 rounds + invariant probe)
**Convergence target**: 0.85
**Mode**: BLIND (variant identities stripped during debate)
**Focus areas**: quantitative-claims, benchmark-provenance, recommendation-validity, haiku-model-risk, toon-maturity
**Date**: 2026-04-15

## Blind-mode variant key (unblinded post-debate)

| Blind label | Model:persona | Role |
|-------------|---------------|------|
| V-A | opus:analyzer | Attack every quantitative claim; demand falsifiable primary sources; produce independent recommendation |
| V-B | opus:architect | Steelman the source's Hybrid XML+TOON+MD recommendation; identify weakest links and shore up |
| V-C | sonnet:scribe | Neutral auditor; check for confirmation bias in benchmark selection; evaluate Haiku weighting |

Variants remained blinded (V-A/V-B/V-C) for the entire 5-step protocol to mitigate model-identity bias. Unblinding occurs only in post-merge provenance annotations.

---

## Taxonomy & scope

Per Interactive Checkpoint 1, debate was scoped to the 5 highest-severity priority points:

| ID | Topic | Taxonomy | Severity |
|----|-------|----------|----------|
| D-1 | Top-ranked format recommendation | L2 structural | HIGH |
| D-2 | "-35% to -50%" headline compression claim | L3 state-mechanics | HIGH |
| D-4 | Anthropic "30% quality gain" attribution | L3 state-mechanics | HIGH |
| D-7 | arXiv 2601.12014 TOON correctness penalty | L3 state-mechanics | HIGH |
| D-10 | Selective loading as compression-saving mechanism | L3 state-mechanics | HIGH |

Haiku model risk was deferred to Round 2.5 invariant probe per checkpoint 1 "auto-resolve via invariant probe" selection.

---

## Round 1: Opening statements (parallel)

All three advocates produced opening statements with mandatory steelman of opposing positions before critique. Full transcripts archived at:

- V-A: `/tmp/.../tasks/a866a586c4fd94b8b.output`
- V-B: `/tmp/.../tasks/af66fb0ab09acad0a.output`
- V-C: `/tmp/.../tasks/ad678f9b4d67f1e05.output`

### Round 1 key positions

**V-A (opus:analyzer)** — Quantitative claim audit
- D-1: Compact Markdown DSL #1 (estimated 19.2-25% savings)
- D-2: Rejected -35-50%; derived ceiling of -13% to -20% from direct composition measurement (25.4% tables, 47.7% bullets)
- D-4: Verbatim Anthropic quote proves MISATTRIBUTION — 30% refers to query-at-end placement, not XML tags
- D-5: arXiv 2604.03616 misapplied — closed-weight frontier models show little format tax
- D-6: arXiv 2603.03306 cherry-picked — paper's own abstract says "Plain JSON shows best one-shot accuracy"
- D-7: Did not cite 2601.12014 (claim-audit methodology gap — cannot detect sins of omission)
- D-10: "Deferred tokens are not saved tokens" for current whole-file consumption

**V-B (opus:architect)** — Steelman of hybrid
- Direct tiktoken cl100k_base measurement on Phase 2 slice (1,399 chars):
  - Original Markdown: 350 tokens (baseline)
  - Hybrid XML+TOON+prose: 308 tokens (-12.0%)
  - **Compact Markdown DSL: 233 tokens (-33.4%)**
- D-1: After cross-exposure to V-C, ranking updated: #1 Compact MD DSL, #2 Hybrid XML+MD (no TOON), #3 Hybrid XML+TOON+MD (demoted)
- D-4: Softened "trained priors" to "RLHF-reinforced disambiguation scaffold" citing Anthropic disclaimer
- D-7: Cited 2603.03306 (TOON-favorable) but missed 2601.12014 (TOON-critical) — asymmetric citation
- D-10: Reframed from headline value to "conditional future value if per-phase loading ships"

**V-C (sonnet:scribe)** — Methodological audit
- **D-7: Found arXiv 2601.12014 "Are LLMs Ready for TOON?"** — TOON GCS 38.9% lower than JSON, 30.9% lower than XML, 42.2% lower than YAML. Single strongest counter-benchmark missed by source.
- D-1: XML + Markdown (no TOON) #1 based on section-extraction reliability
- D-2: Ceiling of -25% to -32% (higher than V-A/V-B but still below -35-50%)
- D-4: "Speculative neuroscience language" in source's "trained structural priors" framing
- Source has 12 citations, 2 TOON-favorable academic, 0 TOON-critical — asymmetric sampling

### Round 1 convergence: ~0.33

Hard remaining disagreements after Round 1:
- D-1: 3-way split (V-A/V-B on CMD DSL #1; V-C on XML+MD #1)
- D-7: V-C unique contribution; V-A/V-B had not seen paper
- D-10: V-A vs V-B split on current vs future consumption patterns

---

## Round 2: Rebuttals (parallel, each advocate receives all Round 1 transcripts)

### CRITICAL: Independent re-verification of arXiv 2601.12014

**V-A result**: Fetched PDF directly from arxiv.org/abs/2601.12014. Page 5 contains verbatim: `"(-38.9%, -30.9%, and -42.2% with respect to JSON, XML, and YAML, respectively)"`. V-C's numbers CONFIRMED.

**V-B result**: Fetched via arxiv.org + papers.cool + DBLP. Authors confirmed (Masciari, Moscato, Napolitano, Orlando, Perillo, Russo; Univ. Naples Federico II / Univ. Bergamo). GCS numbers confirmed to decimal. Token savings: TOON -26.4% vs JSON, -49.4% vs XML, -15.3% vs YAML.

**Critical caveat (raised by V-A and V-B, not V-C)**: Paper tested ONLY open-weight models — GPT-oss (20B/120B), Gemma 3 (4B/12B/27B), Mistral 7B, Llama 3.3 70B, Qwen 3 4B. **Zero Claude models, zero closed-weight frontier models.** Abstract states penalty "progressively narrows as model scale increases"; at Llama 3.3 70B some comparisons show "no statistically significant differences." Combined with arXiv 2604.03616's finding that closed-weight frontier models show "little to no format tax," the TOON GCS penalty likely attenuates on Claude Sonnet 4.6 / Opus 4.6.

**V-C result**: Could not independently re-verify the exact 38.9%/30.9%/42.2% numbers via search (PDF body returned as compressed binary). Confirmed paper exists, direction matches abstract. V-C honestly downgraded to "confirmed direction, magnitude pending table verification" — but V-A and V-B's direct PDF fetches resolve this.

### Round 2 position updates

**V-A concessions**:
- Withdrew "60-token conventions header reliably closes MD-JSON gap on Haiku" claim (V-C critique accepted — untested assertion)
- Softened "most downstream agents read whole file" to likely-but-unverified
- Narrowed claim-audit methodology: necessary but not sufficient; symmetric search required for sins of omission
- Adopted V-B's -33.4% measurement as empirical anchor for CMD DSL #1
- Demoted hybrid-with-TOON from #4 to #5 after 2601.12014 verification

**V-B concessions**:
- Hybrid-with-TOON drop from #2 to #3 made **permanent** (was conditional in Round 1)
- Withdrew "rerank hybrid to #1 when per-phase loading ships" in favor of V-A's surgical `<phase id="N">` XML overlay on Compact MD DSL
- Withdrew "3-parser cognitive load" claim as speculative-and-unmeasured
- Reframed Haiku risk: bounded for CONSUMPTION; unpriced for GENERATION (2601.12014 measures generation-side GCS)
- Conceded asymmetric citation pattern flagged by V-C

**V-C concessions** (largest position shift):
- **Compact MD DSL is plausibly #1 on present evidence** — conceded after V-B's -33.4% measurement
- XML+MD survives only as reliability-first alternative (#2), not empirically superior
- Arithmetic ceiling moves from -25% to -32% down to -13% to -22% after adopting V-A's measured composition (25.4% tables / 47.7% bullets)
- Retracted format-switching cognitive load argument as speculative and load-bearing
- Admitted asymmetric search in own analysis (did not surface TOON-positive engineering evidence)
- Reliability argument for XML narrowed from "trained priors" to "RLHF-reinforced disambiguation scaffold + unambiguous delimiters" (aligning with V-B's framing)

### Round 2 convergence on 5 priority points: ~0.90

| Point | Converged position |
|-------|-------------------|
| D-1 | **Compact Markdown DSL #1** on present evidence (unanimous: V-A firm, V-B firm, V-C conceded "plausibly #1"). Optional `<phase id="N">` XML overlay for selective extraction (V-A's surgical approach, adopted by V-B). XML+MD survives as reliability-first #2 alternative. Hybrid-with-TOON demoted to #3 or lower pending Claude-specific GCS validation. |
| D-2 | **UNANIMOUS** rejection of -35% to -50% headline. Defensible range: -12% to -22% hybrid (anchored on V-B's tiktoken + V-A's composition arithmetic), -25% to -33% Compact MD DSL (V-B measured). Headline is arithmetically unsupported under measured file composition. |
| D-4 | **UNANIMOUS** misattribution finding. 30% quality gain attaches to query-at-end placement, not XML tags (V-A verbatim quote). "No canonical 'best' XML tags Claude is specifically trained on" (V-B Anthropic disclaimer). "Trained structural priors" is speculative neuroscience framing (V-C). Three independent framings of the same correction. |
| D-7 | **CONVERGED**. Paper is real; 38.9%/30.9%/42.2% GCS penalties verified verbatim by V-A and V-B direct PDF fetch. However: tested only open-weight models up to 70B; penalty narrows with scale; measures generation-only; not tested on Claude. Position: "probable TOON risk pending Claude-specific empirical probe." Hybrid-with-TOON is not production-ready without validation. |
| D-10 | **UNANIMOUS** on compression framing — deferred tokens are not saved tokens in current whole-file consumption. XML section-anchor reliability survives as SEPARATE claim (not tied to compression), independent of selective-loading implementation. |

---

## Round 2.5: Invariant probe

Full invariant probe artifact: inline below. Identifies 10 shared blind spots across 5 categories (state/lifecycle, guard/boundary, concurrency/ordering, correctness semantics, environment/deployment).

### HIGH-severity UNADDRESSED invariants (populate return contract)

| ID | Name | Category | Issue |
|----|------|----------|-------|
| INV-1 | Tokenizer Generalization | GUARD + CORRECTNESS | V-B's load-bearing -12%/-33% measurements used `cl100k_base` (OpenAI's tokenizer), not Claude's native tokenizer. ±2-8pp drift plausible — wide enough to change ranking magnitudes. No variant flagged the substitution or re-ran on Anthropic's `count_tokens` API. |
| INV-3 | Consumption Pattern DAG | STATE/LIFECYCLE | D-10's V-A↔V-B contradiction collapses to an unmapped consumer DAG. Roadmap files are consumed by sc:tasklist, sc:pm, sc:validate-roadmap, sc:adversarial, human reviewers, CI. No variant enumerated read patterns across consumers. |
| INV-5 | HAIKU UNTESTED | ENVIRONMENT | Per checkpoint 1 directive, all three candidate formats (Compact MD DSL, Hybrid XML+TOON+MD, XML+MD) are **untested on Haiku 4.5**. V-A withdrew its "conventions header closes the gap" claim. Only anchor is webmaster-ramos's single data point. Compact MD DSL, Hybrid, and XML+MD Haiku performance all UNTESTED. |

### HIGH-severity PARTIAL invariants (decision-load-bearing)

| ID | Name | Issue |
|----|------|-------|
| INV-4 | Generation-vs-Consumption Benchmark Applicability | V-C's 2601.12014 measures GENERATION (LLM emitting TOON); roadmap use case is strictly CONSUMPTION. V-B partially distinguishes; V-A/V-C conflate. Consumption-only micro-benchmark never run. |
| INV-9 | Closed-Weight Format-Tax Silence | arXiv 2604.03616 says closed-weight frontier models have little/no format tax. If true, format engineering's expected value on Opus 4.6 is near-zero and all optimization concentrates on Haiku — which lands on INV-5 (UNADDRESSED). |

### Net invariant-probe convergence: ~0.70

The 5 priority points converged at ~0.90. The shared blind spots cap honest convergence at ~0.70 because three HIGH-severity invariants remain UNADDRESSED and cannot be resolved by further debate — they require empirical tests:
1. Re-measure on Anthropic's `count_tokens` API (INV-1)
2. Enumerate consumer DAG with read patterns (INV-3)
3. Run Haiku-specific A/B on the three candidate formats with ≥20 retrieval prompts (INV-5)

---

## Round 3 decision: SKIP

**Convergence threshold**: 0.85
**Priority-point convergence**: 0.90 (exceeds threshold)
**Invariant-probe convergence**: 0.70 (below threshold, but unresolvable by debate)

**Rationale for skip**: Round 3 would debate the same 5 priority points that already converged. The gap between priority-point convergence (0.90) and invariant-probe convergence (0.70) is not a debate-resolvable gap — it is a measurement gap. No additional argument moves the 3 HIGH-severity UNADDRESSED invariants; only empirical tests do.

**Consequence**: The final recommendation must carry INV-1, INV-3, and INV-5 as explicit caveats in the merged output, and they populate the `unaddressed_invariants` list in the return contract.

---

## Per-point scoring matrix

| Point | Winner | Confidence | Evidence summary |
|-------|--------|-----------|------------------|
| D-1 | V-A + V-B (Compact MD DSL #1) | HIGH | V-B's tiktoken measurement (-33.4%) is single strongest empirical datum. V-C conceded in Round 2. |
| D-2 | V-A + V-B (headline falsified) | HIGH | V-B measurement + V-A arithmetic + V-C reconstruction all converge on -12% to -22% hybrid. V-C conceded composition error. |
| D-4 | V-A (verbatim quote dispositive) | HIGH | Verbatim Anthropic quote proves misattribution. V-B and V-C findings are complementary. |
| D-7 | V-C (paper identification) + V-A/V-B (caveats) | MEDIUM-HIGH | V-C found the paper. V-A and V-B verified numbers and added dispositive caveat (open-weight-only test set). |
| D-10 | V-A (deferred ≠ saved) on compression, V-B on reliability | HIGH | Unanimous on compression framing. XML-reliability claim survives independently. |
| INV-5 Haiku | UNRESOLVED | UNADDRESSED | No variant has tested any format on Haiku. Flagged HIGH-severity UNADDRESSED per checkpoint 1. |

---

## Surviving disagreements (post-Round 2, post-invariant-probe)

1. **Strength of 2601.12014 as TOON blocker**: V-A/V-B = "probable pending Claude-specific test"; V-C Round 1 = "hard blocker" softened to "probable-pending-verification" in Round 2. Effectively converged.
2. **XML section-anchor reliability value on current pipeline**: V-B "realized immediately"; V-A "unobserved"; V-C "delimiter disambiguation is real but not load-bearing for this file." Narrow, unresolvable without consumer-DAG audit (INV-3).
3. **Ranking of XML+MD vs plain Compact MD DSL**: V-A/V-B rank plain CMD DSL #1; V-C ranks XML+MD as reliability-first alternative #2. Both parties concede plain CMD DSL is "plausibly #1" — difference is in risk tolerance, not ranking strength.

---

## Convergence summary

- **Priority-point convergence**: 0.90 (5/5 points have substantive convergence with measurable agreement)
- **Invariant-probe convergence**: 0.70 (3 HIGH UNADDRESSED blind spots cap honest convergence)
- **Overall effective convergence**: 0.80 (midpoint reflecting both the debate quality and the unresolved measurement gaps)

Pipeline proceeds to Step 3 (Hybrid Scoring) with 3 HIGH-severity UNADDRESSED invariants carried forward as caveats on the final recommendation.
