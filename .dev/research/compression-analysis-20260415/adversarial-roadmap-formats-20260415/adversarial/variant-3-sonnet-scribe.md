# Variant 3: Methodological Audit of the Format Research Report

**Auditor**: Neutral auditor (Variant 3, Sonnet-scribe perspective)
**Date**: 2026-04-15
**Source report**: `research_roadmap-format-alternatives_20260415.md`
**Verdict**: Bounded biases -- the report's conclusions are defensible directionally, but the headline claim of -35% to -50% token savings is not supported by the quantity and independence of evidence cited. The recommendation is likely correct for the stated use case (Sonnet/Opus roadmap files), but the methodology overweights sympathetic benchmarks and underweights disconfirming evidence.

---

## Part A: Benchmark Inventory & Sampling Audit

| # | Benchmark / Source | Cited in report? | Methodology match to roadmap use case? | Symmetric search evidence? | Verdict |
|---|--------------------|-------------------|---------------------------------------|----------------------------|---------|
| 1 | **webmaster-ramos 2025** (Claude API benchmark: YAML vs MD vs JSON vs TOON) | Yes -- primary accuracy source | Partial -- uses Claude tokenizer, but tests generic extraction, not roadmap-specific prose+table mixes | None visible -- report does not describe searching for counter-benchmarks | **Moderate match. The only Claude-specific accuracy data, but methodology details (dataset, sample size, error bars) are not disclosed in the report. Treated as authoritative without scrutiny.** |
| 2 | **TOON official benchmarks** (toonparse.com) | Yes -- token savings claims | Poor -- measures flat/tabular data compression, not mixed prose+structure | None -- TOON's own benchmarks are a vendor source | **Weak match. The -58.8% vs JSON figure is for flat uniform data; the report itself admits this collapses on mixed data, but the headline still uses the optimistic end.** |
| 3 | **Anthropic official docs** ("Use XML tags," prompt engineering) | Yes -- XML priors claim | Partial -- Anthropic recommends XML for prompt structuring, not specifically for roadmap file encoding. The recommendation is about input structuring for task prompts, not data persistence formats. | Not applicable -- this is vendor guidance, not a benchmark | **Directionally valid but category-confused. The report equates "XML is good for structuring Claude prompts" with "XML is good for encoding roadmap data files." These are different claims.** |
| 4 | **Workman 2025** ("YAML vs JSON: Hidden Token Tax") | Yes -- YAML overhead claim | Partial -- Claude tokenizer confirmed, but the report provides no link, no dataset description, no sample size | None | **Uncorroborated. Referenced by author name only. Cannot verify methodology without the original source.** |
| 5 | **Syntax & Empathy 2025** ("Designer's Guide to Markup Languages") | Yes -- token counts for MD/YAML/TOML/JSON | Poor -- measures token counts of a different document (likely a design document), not a roadmap file | None | **Weak match. Token counts are document-specific and do not generalize without normalization.** |
| 6 | **CuriouslyChase 2025** ("YAML vs JSON Token Efficiency") | Yes -- minified JSON vs YAML | Poor -- measures a single small example (41 vs 133 tokens). Extreme selection bias toward the smallest possible JSON. | None | **Cherry-picked. A 41-token minified JSON example is not representative of a 4,600-token roadmap file.** |
| 7 | **arXiv 2411.10541** ("Prompt Formatting and LLM Performance") | Yes -- "up to 40% performance delta" | Moderate -- measures format impact on LLM performance, but on code translation tasks with GPT-3.5/4, not Claude on roadmap parsing | None | **Misapplied. The 40% figure is for GPT-3.5 on code translation. The report uses it to imply format sensitivity for Claude on roadmaps -- a different model and task.** |
| 8 | **ACL SRW 2025** (arXiv 2507.01810, "Evaluating Structured Output Robustness") | Yes -- "JSON highest parseability" | Moderate -- small language models, JSON vs YAML vs XML parseability | None | **Correctly cited but directionally inconvenient for the report: JSON wins on parseability, yet the report recommends XML+TOON. This is acknowledged but its weight is minimized.** |
| 9 | **arXiv 2604.03616** ("The Format Tax") | Yes -- cited in sources | Strong -- directly measures structured format impact on reasoning performance | None | **Undercited. This paper finds that format requirements degrade reasoning, and crucially notes that closed-weight models (like Claude) show little format tax. The report cites it but does not integrate this finding -- which actually undermines the urgency of format optimization for Claude.** |
| 10 | **arXiv 2603.03306** ("TOON vs JSON benchmark") | Yes -- in sources | Strong -- directly about TOON vs JSON | None | **Appropriately cited.** |
| 11 | **fromjsontotoon.com** | Yes -- TOON performance analysis | Weak -- vendor/promotional site, not a benchmark | None | **Low reliability. This is a TOON marketing site, not an independent benchmark.** |
| 12 | **Medium 2025** ("Tokenization Comparison: CSV, JSON, YAML, TOON") | Yes -- tiktoken benchmarks | Poor -- uses tiktoken (OpenAI tokenizer), not Claude tokenizer | None | **Mismatched tokenizer. Token counts from tiktoken cl100k_base do not transfer to Claude's tokenizer. The report should not use OpenAI tokenizer data to make Claude-specific claims.** |

### Summary of Part A

Of 12 cited sources:
- **2** are high-quality, directly applicable benchmarks (webmaster-ramos for Claude accuracy, arXiv 2603.03306 for TOON vs JSON)
- **3** are vendor/promotional sources (TOON official benchmarks, fromjsontotoon.com, Anthropic docs)
- **3** are mismatched by tokenizer, task, or model (Medium tiktoken, arXiv 2411.10541 on GPT-3.5, CuriouslyChase micro-example)
- **4** are general reference points with uncertain methodology match

**No evidence of symmetric search.** The report does not describe searching for benchmarks where XML or TOON underperform. It does not cite any source that recommends against its conclusion.

---

## Part B: Missing Benchmarks (Ones the Report Ignored)

The following sources were available at the time of writing (January-April 2026) and directly relevant but were not cited:

### B1. arXiv 2601.12014 -- "Are LLMs Ready for TOON?"

**Why it matters**: This is the most direct counter-benchmark to the report's TOON claims. Key findings:
- TOON structural correctness (GCS) is **38.9% lower than JSON, 30.9% lower than XML, and 42.2% lower than YAML**.
- TOON achieves token savings of 26.4% vs JSON and 49.4% vs XML, but the correctness penalty is substantial.
- With balanced scoring (gamma=0.5 weighting correctness vs efficiency), **baseline formats still rank higher than TOON overall**.
- Larger models reduce the gap but do not eliminate it.

**Impact on report**: This paper directly challenges the report's claim that TOON tables are safe for Sonnet/Opus agents. The report cites arXiv 2603.03306 (which is favorable to TOON) but ignores 2601.12014 (which is unfavorable). This is the single strongest piece of evidence of confirmation bias in benchmark selection.

**Does it weaken the conclusion?**: For the hybrid recommendation, partially. If TOON correctness is 30-42% worse than JSON/XML on structural tasks, the hybrid format's TOON tables carry a risk of misparsed risks, traceability entries, or task lists. The report's hedge ("bounded concern on Haiku") understates the issue -- the correctness penalty is model-agnostic per this benchmark, not Haiku-specific.

### B2. arXiv 2604.03616 -- "The Format Tax" (underweighted)

The report cites this paper but does not integrate its central finding: **closed-weight models (including Claude) show little to no format tax**. If Claude's reasoning is largely format-invariant, then the urgency of optimizing away from Markdown (which has the best training-data coverage) is reduced. The entire premise of the report -- that format choice materially impacts Claude's roadmap comprehension -- is called into question by this paper's findings on frontier models.

### B3. "A Comparison of Data Formats for LLMs: Why Markdown Is King" (Medium, April 2026)

This benchmark tests 11 formats for LLM comprehension and finds:
- Markdown-KV is ~16 percentage points better than CSV for comprehension.
- XML/HTML use 40-45% more tokens than Markdown for equivalent data.
- JSON is described as a weak default for text-heavy content.

**Impact**: The report acknowledges Markdown's prose strength but does not engage with evidence that Markdown outperforms XML on comprehension metrics. If Markdown comprehension is significantly better than XML, the hybrid format's XML scaffolding may impose a comprehension cost that offsets its structural reliability gains.

### B4. StructEval (arXiv 2505.20139) -- "Benchmarking LLMs' Capabilities to Generate Structural Outputs"

Tests structured output generation across JSON, YAML, CSV, and other formats. Not cited. Would provide additional data on which formats LLMs parse most reliably.

### B5. LLMStructBench (arXiv 2602.14743)

Structured data extraction benchmark across LLMs. Directly relevant to the question of "which format do LLMs extract from most reliably" but not cited.

### B6. Reddit/community critiques of TOON benchmark methodology

- "Stopping the TOON hype with a proper benchmark" (r/LocalLLaMA) raises concerns about TOON benchmark dataset selection
- "TOON is terrible, so I invented TRON" (r/LocalLLaMA) argues TOON's benchmarks are cherry-picked for flat/tabular data

While not academic sources, these critiques highlight a known community concern about TOON benchmark representativeness that the report should have acknowledged.

### Missing Benchmarks Summary

The report cites 12 sources, of which at least 2 are TOON-favorable and 0 are TOON-critical from academic literature. At minimum, arXiv 2601.12014 (TOON correctness penalty) and arXiv 2604.03616 (frontier models show little format tax) should have been engaged with substantively. Their omission constitutes a meaningful gap in the evidence base.

---

## Part C: Haiku Accuracy Weighting Analysis

### The Report's Treatment

The report mentions Haiku 4.5 accuracy data once, in the TOON section:
> "Haiku 4.5: TOON 74.8% vs JSON 75.3%"

And in the caveats:
> "Haiku 4.5: TOON accuracy 74.8% vs JSON 75.3% -- small penalty on cheaper models."

### Is This Fair Weighting?

**No. The weighting is unfair in two ways:**

1. **The gap is minimized rhetorically.** The report calls this a "small penalty" (0.5 percentage points). But the same benchmark shows Markdown scoring 69.6% on Haiku. The report uses the TOON vs JSON comparison (0.5pp gap) to dismiss Haiku concerns, while the TOON vs Markdown gap (5.2pp) actually favors TOON. The report cherry-picks the comparison that makes TOON look worst and then dismisses it as small. The actual concern is not TOON vs JSON -- it is that all non-JSON formats degrade on Haiku, and the report's hybrid format (which uses XML + TOON + prose) layers multiple non-JSON formats together.

2. **The comparison is incomplete.** The report does not provide accuracy data for the actual recommended hybrid format (XML + TOON + Markdown prose) on Haiku. It extrapolates from individual format scores, but hybrid formats may compound parsing difficulty -- an agent must parse XML structure, switch to TOON for tables, then switch to Markdown for prose, all in one document. The cognitive load of format-switching within a single document is not benchmarked anywhere.

### Deployment Scenarios Where This Flips the Recommendation

The Haiku concern becomes dispositive in these scenarios:

1. **Cost-optimized pipelines using Haiku sub-agents for task extraction.** If a production pipeline uses Haiku 4.5 for cost reasons (the most likely scenario for high-volume agent orchestration), then JSON at 75.3% vs the hybrid format at an unknown-but-likely-lower score could make the hybrid format a net negative. The token savings of -35% to -50% would be offset by accuracy degradation requiring re-prompting or manual correction.

2. **Multi-agent systems where Haiku agents handle specific roadmap sections.** If Haiku agents are responsible for risk table parsing or traceability extraction, the TOON-encoded tables could introduce errors that cascade through the pipeline.

3. **Any deployment where accuracy is more expensive than tokens.** Token costs are declining; error correction costs are not. If a misparsed risk matrix causes a failed sprint, the token savings are irrelevant.

### Fair Treatment Would Be

The report should have:
- Provided an estimated hybrid-format accuracy on Haiku (even if inferred)
- Acknowledged that the hybrid format has no direct accuracy benchmark
- Made the Haiku recommendation conditional on actual measurement: "For Haiku pipelines, validate the hybrid format against JSON in your specific deployment before adopting"
- Disclosed that the webmaster-ramos benchmark tested individual formats, not hybrid combinations

---

## Part D: Sample Size Statistical Assessment

### How Many Independent Measurements Support the -35% to -50% Claim?

Tracing the claim to its sources:

| Evidence Source | What It Measures | Token Savings Claimed | Independent? |
|----------------|-----------------|----------------------|--------------|
| TOON official benchmarks (toonparse.com) | TOON vs JSON on flat tabular data | -58.8% | Vendor source, not independent |
| webmaster-ramos 2025 | TOON vs Markdown token counts (Claude tokenizer) | -19% | Semi-independent (community benchmark) |
| Report's own estimation | Hybrid format applied to the source roadmap file | -35% to -50% | Self-generated, no empirical validation |
| TOON benchmarks (mixed data) | TOON vs JSON on mixed/nested data | -21.9% | Vendor source |
| arXiv 2601.12014 | TOON token savings vs JSON/XML/YAML | -26.4% vs JSON | Independent |

**The -35% to -50% headline claim is not directly supported by any single benchmark.** Here is the chain of reasoning:

1. TOON achieves -50% to -62% on flat tables (vendor benchmark).
2. The roadmap file is ~62% prose + ~38% structured data (report's own characterization).
3. The hybrid format uses TOON for the structured portions only.
4. Therefore, savings = (0.38 * -56%) + (0.62 * -10% to -15% for XML scaffolding) = approximately -25% to -31%.

**The math does not work out to -35% to -50%.** Even with generous assumptions:
- If TOON saves 60% on the 38% that is tabular: 0.38 * 0.60 = 22.8%
- If XML scaffolding + Markdown compaction saves 15% on the 62% that is prose: 0.62 * 0.15 = 9.3%
- Total: ~32.1%

This only reaches -35% with optimistic assumptions on every parameter. It reaches -50% only if you assume the prose sections also compress by 50% (which no cited benchmark supports).

### What I Would Say to a Skeptical Statistician

"I can defend a token savings claim of -25% to -35% for the hybrid format based on one independent benchmark (arXiv 2601.12014 showing TOON at -26.4% vs JSON) plus the report's reasonable structural analysis of the source file. I cannot defend -35% to -50% without additional empirical measurement on an actual converted roadmap file. The upper bound of the claim requires simultaneous optimization of every component (TOON tables, XML scaffolding, Markdown compaction, cross-reference deduplication) and assumes no overhead from format-switching or schema documentation. The sample size supporting the specific headline number is effectively N=1 (the report's own unvalidated estimation on a single file)."

---

## Part E: Confirmation Bias Findings

### E1. The Report "Sounds Too Clean" in Its Recommendation

The hybrid recommendation combines three formats and claims the best properties of each:
- XML's trained priors (from Anthropic docs)
- TOON's tabular compression (from vendor benchmarks)
- Markdown's prose handling (from common knowledge)

This is a "best of all worlds" argument. Real engineering tradeoffs rarely resolve this cleanly. The report does not adequately address:
- The cognitive load of format-switching within a single document (XML -> TOON -> Markdown -> XML -> TOON)
- The overhead of teaching agents three format conventions simultaneously
- The fragility of a format that requires all three parsers to be correct

### E2. Specific Passages Where Reasoning Feels Motivated

**Passage 1** (Executive Summary):
> "Format-swapping alone (YAML, TOML, pretty JSON) yields *negative* savings."

This is stated as fact but is supported by one data point per format (CuriouslyChase for JSON, Workman for YAML). The use of "yields" (present tense, universal) overstates the evidence, which is from small, non-roadmap examples.

**Passage 2** (XML section):
> "XML tags are a *trained structural signal*. Markdown `##` headings get ambiguous when documents themselves contain headings, but `</phase>` cannot be confused with content."

This is a strong claim presented without qualification. XML tags can absolutely be confused with content -- any document containing literal XML (like this research report's examples) would create ambiguity. The claim also assumes the LLM's XML parsing is error-free, which the Format Tax paper (arXiv 2604.03616) shows is not guaranteed.

**Passage 3** (Why Hybrid Wins):
> "XML scaffolding (~80-120 tokens overhead) activates Claude's trained structural priors for reliable section extraction"

"Activates trained structural priors" is speculative neuroscience language. There is no published evidence that Claude has "trained structural priors" for custom XML tags like `<phase id="2" deps="P1">`. Anthropic recommends XML for structuring prompts; the report extrapolates this to "Claude has trained priors for arbitrary XML schemas" -- a different and stronger claim.

**Passage 4** (Haiku caveat):
> "TOON accuracy 74.8% vs JSON 75.3% -- small penalty on cheaper models."

Calling 0.5 percentage points "small" is defensible for the specific TOON-vs-JSON comparison, but the broader context (Markdown at 69.6%, the hybrid format being untested) makes this dismissal premature. The hedge is present but too narrow.

**Passage 5** (Primary recommendation):
> "35-50% token reduction (saving ~1,600-2,300 tokens per roadmap ingest)"

The specificity of "1,600-2,300 tokens" creates a false precision. These are estimated values from a single-file analysis with no empirical validation. Presenting them as if measured is misleading.

### E3. Where Hedges Are Missing

The report hedges individual format analyses well (each format gets a "Failure modes" row) but drops hedging at the recommendation level:
- No "limitations of this analysis" section
- No "what would change our recommendation" section
- No "confidence level" for the -35% to -50% claim
- No sensitivity analysis (what if TOON tables are only -30% instead of -50%?)
- No discussion of what happens if the hybrid format's accuracy is 5-10% lower than any individual format due to format-switching overhead

### E4. Structural Bias in Format Ordering

The report presents formats in an order that builds toward the hybrid recommendation:
1. Compact Markdown (modest savings, familiar)
2. YAML (worse on tokens)
3. JSON (best raw savings but terrible prose)
4. TOML (worst option)
5. YAML-Markdown hybrid (acceptable but not optimal)
6. TOON (exciting new format, huge savings on tables)
7. XML (Claude's native format)

This ordering creates a narrative arc: familiar things are okay, bad things are eliminated, then exciting new thing + Claude's native thing are combined into the optimal solution. A neutral presentation would have led with the hybrid and then evaluated it against alternatives, rather than building toward it as a conclusion.

---

## Part F: Bias-Aware Recommendation

### Format Recommendation

**Primary recommendation: Hybrid XML + Markdown (without TOON), with an optional TOON migration path after empirical validation.**

This recommendation explicitly addresses each bias found in Parts A-E:

**Addressing the benchmark sampling bias (Part A/B):**
The report over-relies on TOON vendor benchmarks and a single Claude-specific community benchmark (webmaster-ramos). The independent academic evidence (arXiv 2601.12014) shows TOON has a 30-42% structural correctness penalty vs established formats. Until TOON correctness is validated on Claude models (which arXiv 2601.12014 may not have tested), it should not be the default for production roadmap files. XML + Markdown avoids this correctness risk while still capturing XML's structural benefits.

**Addressing the Haiku weighting (Part C):**
XML + Markdown has no known accuracy penalty on Haiku. Both formats are well-represented in training data. The hybrid with TOON introduces an untested accuracy surface. For pipelines that may use Haiku sub-agents (the most likely cost-optimization strategy), XML + Markdown is the safer choice.

**Addressing the sample size weakness (Part D):**
XML + Markdown's token savings (-10% to -20%) are modest but honestly supported by the evidence. The -35% to -50% claim for the TOON hybrid is not defensible at N=1. Better to ship a format with a 15% savings that actually measures correctly than chase a 45% savings that may not materialize.

**Addressing confirmation bias (Part E):**
The report's strongest unbiased finding is that XML is Claude's recommended structuring format and Markdown handles prose well. Combining these two is a straightforward application of Anthropic's own guidance. Adding TOON requires accepting vendor claims, dismissing correctness penalties, and introducing a third parser -- all for marginal additional savings that are not empirically validated on the target use case.

### Migration Path

1. **Phase 1 (immediate)**: Adopt XML + Markdown hybrid. Measure actual token savings on 3-5 real roadmap files. Expected: -10% to -20%.
2. **Phase 2 (after validation)**: Run an A/B test of XML + TOON + Markdown vs XML + Markdown on both Sonnet and Haiku. Measure: token count, task extraction accuracy, parsing error rate.
3. **Phase 3 (conditional)**: If Phase 2 shows TOON adds >=10% additional savings with <=2% accuracy degradation, adopt the three-format hybrid.

### When the Source Report's Recommendation Is Correct

The source report's "Hybrid XML + TOON + Markdown" recommendation is appropriate when:
- All consuming agents are Sonnet 4.6+ or Opus 4.6+ (no Haiku)
- The team has capacity to validate TOON parsing correctness in their specific pipeline
- Token costs are a dominant concern over correctness risk
- The roadmap files have a high proportion of tabular data (>40%)

In these conditions, the TOON savings are real and the correctness penalty is acceptable. The report's recommendation is not wrong -- it is insufficiently hedged and based on evidence that is not as strong as presented.

### Final Assessment

The source report's methodology has **bounded biases**: the direction of the conclusion (hybrid format is better than pure Markdown) is sound, but the magnitude of the claimed savings and the confidence in TOON as a component are overstated. The report should be treated as a well-reasoned engineering proposal that needs empirical validation, not as a conclusive benchmark study. The strongest contribution of the report is not the specific format recommendation but the structural analysis of token bloat patterns in roadmap files (Part 2, "Top 5 Bloat Patterns") -- this analysis is model-independent, verifiable, and actionable regardless of which format is ultimately chosen.
