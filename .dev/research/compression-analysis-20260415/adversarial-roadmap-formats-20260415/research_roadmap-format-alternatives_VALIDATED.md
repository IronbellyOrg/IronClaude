# Research — Roadmap Format Alternatives (VALIDATED)

**Date**: 2026-04-15
**Status**: Adversarially validated via 3-variant debate + invariant probe
**Base variant**: V-B (blind) — selected via scored debate, score 0.870
**Disposition**: Accept with caveats (INV-1, INV-3, INV-5 carry-forward)
**Scope**: Recommendation explicitly scoped to Opus 4.6 and Sonnet 4.6 consumers. Haiku 4.5 pipelines are gated to plain Markdown until the Part I Phase 2 A/B test completes (see Haiku Path and Part H INV-5).

---

## Verdict (preview)

The source report's steelman **holds only in a narrower form** than the source claims. Two of three pillars survive intact; one pillar (TOON compression on roadmaps) requires a significant amendment because the source benchmarked TOON against JSON, not against Markdown tables — and the roadmap is already in Markdown. On a real `tiktoken cl100k_base` measurement of a phase slice, the hybrid delivered **-12.0%**, not the claimed **-35% to -50%**. The hybrid is still defensible, but for a different reason than the source argued: **reliability and selective loading, not raw compression.** An independent counter-benchmark (arXiv 2601.12014) adds a correctness concern to TOON that is not purely Haiku-scoped, and the source report's own "Format Tax" citation (arXiv 2604.03616) actually undercuts rather than supports format engineering on closed-weight frontier models like Sonnet 4.6 and Opus 4.6.

The validated recommendation is:

1. **Compact Markdown DSL (#1)** for Opus 4.6 / Sonnet 4.6 roadmap consumers — measured -33.4% on a Phase 2 slice, dominates the hybrid on pure compression grounds.
2. **Hybrid XML + TOON + prose (#2)** retained as an upgrade candidate gated on the Part I Phase 2 A/B test showing ≥10% additional savings with ≤2% accuracy degradation.
3. **Plain Markdown for any Haiku 4.5 path** until INV-5 resolves (see Haiku Path section).

---

## Part A: Pillar 1 — XML Trained Priors in Claude

### The source's claim

> "XML is explicitly trained into Claude as a structural delimiter and Anthropic officially recommends it for prompt/document structuring... Tag boundaries are a trained signal — not merely a convention."

### Steelman evidence (strongest defensible version)

Anthropic's own prompt-engineering docs at `platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/use-xml-tags` and the Claude 4.6 best-practices page give us the following hard evidence:

1. **Direct Anthropic quote**: *"XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs."* This is exactly the roadmap use case — mixed instructions, tables, examples, and variable identifiers.

2. **Named canonical tags in Anthropic's own examples**: `<documents>`, `<document index="n">`, `<document_content>`, `<source>`, `<instructions>`, `<context>`, `<example>` (plural `<examples>`), `<thinking>`, `<answer>`, `<quotes>`, `<info>`. The docs show these in live code samples used by Anthropic to demonstrate Claude's intended usage patterns.

3. **The 30% long-context number — misattribution corrected.** The source report cites Anthropic's long-context-tips page for "up to 30% quality gain from XML." The verbatim quote on that page is: *"Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs."* Anthropic attributes the 30% gain **solely to query placement at the end of the prompt**, not to XML tags. XML is a separate recommendation on the same doc with **no quantified gain attached**. The source report's conflation of "XML + query placement" into a single 30% causal claim is a misattribution, not a soft reading. The correct characterization is: *"Anthropic recommends XML for structural clarity (no quantified gain); query-at-end can yield up to 30% on long-context tasks."*

4. **Mandatory structural guidance for 20k+ token inputs**: The Anthropic docs explicitly tell you to wrap long-form data in `<document>` tags when context exceeds 20k tokens. A full roadmap ingested alongside its tasklist and PRD regularly exceeds that threshold in the SuperClaude pipeline.

5. **The prefill deprecation in Claude 4.6** (noted in the same docs): Claude Opus/Sonnet 4.6 have deprecated last-turn prefill and instead route structural steering through **explicit XML tags like `<avoid_excessive_markdown_and_bullet_points>`, `<default_to_action>`, `<use_parallel_tool_calls>`, `<investigate_before_answering>`**. Anthropic has migrated its *own* steering patterns to XML tags. That is institutional signal.

### Honest downgrade

The source report's wording "trained into Claude as a structural delimiter" overstates what Anthropic actually says. On the same `use-xml-tags` page, Anthropic explicitly clarifies there are **no canonical "best" XML tags Claude is specifically trained on** and recommends picking meaningful tag names. The mechanism is not "XML tags are special tokens Claude learned to attend to"; it is "unambiguous delimiter pairs resist confusion with content, and Claude's RLHF extensively uses XML-tagged examples." That is a weaker claim than "trained priors" but it is still a claim the roadmap use case can cash in.

### Confidence level

**High (0.90)** for "XML tags are Anthropic's recommended mechanism for document structuring in long-context prompts." **Medium (0.65)** for "XML tags are a distinct trained signal beyond disambiguation." The 30% misattribution is removed from the evidence base entirely; XML earns its place in the hybrid on disambiguation grounds, not on a quantified Anthropic-attributed gain.

The steelman survives Pillar 1, but the language must soften from "trained priors" to "Anthropic-recommended, RLHF-reinforced disambiguation scaffold."

---

## Part B: Pillar 2 — TOON Tabular Compression

### The source's claim

> "TOON achieves -53% vs Markdown on tabular data... -50% to -62% savings on tabular portions."

### Steelman evidence

1. **Provenance**: TOON is real and actively maintained. Johann Schopplich's repo at `github.com/toon-format/toon` has a live spec (v3.0, Dec 2025) and MIT license. Multiple independent benchmarks exist (webmaster-ramos, toonparse.com, fromjsontotoon.com, dev.to ikaganacar critical analysis, Medium codex article, Wyzer blog).

2. **Published JSON savings**: The Medium Codex article (`TOON: The data format slashing LLM costs by 50%`) aggregates multiple studies and reports **30-60% token reductions vs JSON**, with specific data points of 61.9%, 60.7%, 59.0%, and 56% on production payloads. The aggregate Medium benchmark across GPT-5-nano, Gemini-2.5-flash, Claude-Haiku-4.5, and Grok-4-fast shows TOON at **73.9% accuracy** vs JSON-compact at 70.7% — TOON was the *most* accurate format in that study.

3. **Academic backing**: arXiv 2603.03306 ("Token-Oriented Object Notation vs JSON") provides peer-reviewed benchmarking of the accuracy/token tradeoff.

4. **Webmaster-ramos Claude-specific numbers** (cited by source): JSON 3,252 tokens / Markdown 1,514 / TOON 1,226 on the benchmark dataset. This is a real Claude tokenizer measurement.

### Counter-finding from the same paper (arXiv 2603.03306)

The source report cites arXiv 2603.03306 as academic backing for TOON but **suppresses the paper's adverse findings**. The abstract explicitly states: *"Plain JSON generation shows the best one-shot and final accuracy, even compared with constrained decoding structured output"* and that TOON's efficiency is *"often reduced by the 'prompt tax' of instructional overhead in shorter contexts."* TOON is good for *reading* (comprehension) on uniform tables but not clearly better for *generation*, and its prompt-tax overhead eats into gains on short contexts. The source cites the paper but omits this adverse conclusion entirely. A fair citation would read: *"TOON's prompt-tax overhead erodes token savings on short contexts, and plain JSON generation outperforms TOON on one-shot accuracy per the same paper."*

### The critical correction the source missed

**TOON's advertised savings are vs JSON, not vs Markdown.** The webmaster-ramos benchmark itself shows TOON at -19% vs Markdown (1,226 vs 1,514 tokens), not -50-62%. The big TOON wins are on JSON-origin data. When you convert **already-compact Markdown pipe tables** to TOON, the savings collapse dramatically.

I verified this on the actual roadmap risk table. Using `tiktoken cl100k_base`:

| Format | Tokens | Delta |
|--------|--------|-------|
| Risk table (original pipe-Markdown, 8 rows) | 255 | baseline |
| Risk table (TOON equivalent) | 218 | **-14.5%** |

Not -50%. Not -62%. **-14.5%.** The source report's compression claim is vs JSON, but the roadmap is never in JSON to begin with.

### Honest confidence level

**Medium-Low (0.55)** for the source's specific "-50 to -62% on tabular data" claim as applied to this roadmap. **High (0.85)** for "TOON can compress structured tabular data when converting from JSON-origin payloads."

### Independent counter-benchmark (arXiv 2601.12014)

A second academic source — **arXiv 2601.12014 "Are LLMs Ready for TOON?"** — was missing from the source report's bibliography and constitutes the single strongest piece of evidence of confirmation bias in benchmark selection. Its findings directly challenge the premise that TOON tables are safe for Sonnet/Opus agents:

- TOON structural correctness (GCS) is **38.9% lower than JSON, 30.9% lower than XML, and 42.2% lower than YAML**.
- TOON achieves token savings of 26.4% vs JSON and 49.4% vs XML, but the correctness penalty is substantial.
- With balanced scoring (gamma=0.5 weighting correctness vs efficiency), **baseline formats still rank higher than TOON overall**.
- Larger models reduce the gap but **do not eliminate it**.

The verification note: V-A and V-B both fetched and confirmed these numbers verbatim during the debate's Round 2 round-trip. The paper exists; the 38.9/30.9/42.2 GCS breakdown matches the abstract; the open-weight-only caveat is real but does not neutralize the finding. Because the gap narrows but does not close on larger models, the correctness concern is **not purely a Haiku problem** — it affects TOON adoption on Sonnet/Opus pipelines as well, though with smaller magnitude.

This is why Pillar 2 is *demoted*, not collapsed: the hybrid's TOON sub-block carries a measurable correctness risk even on the models the recommendation is scoped to. The demotion is already accommodated by the 0.55 confidence number above; the counter-benchmark grounds the number rather than invalidating the pillar.

*Inline note: Part B injects arXiv 2603.03306 counter-finding (V-A Part E item 4) and arXiv 2601.12014 counter-benchmark (V-C Part B1, verified by V-A/V-B in Round 2).*

---

## Part C: Pillar 3 — Markdown Prose Fidelity

### The source's claim

> "Markdown prose fidelity... prose resists compression because narrative context is what agents reason over."

### Steelman evidence (this pillar is the strongest)

1. **Markdown dominates LLM training data**. This is self-evident from any corpus analysis: GitHub README files, Stack Overflow posts, documentation sites, and blog articles in Common Crawl are overwhelmingly Markdown. Claude has seen more Markdown prose than any other structured format by orders of magnitude.

2. **Anthropic's own docs are Markdown + XML hybrid**. The `platform.claude.com/docs` pages I fetched above render as Markdown with embedded `<section>`, `<Tip>`, `<Note>`, and XML code examples. Anthropic structures its *own documentation* exactly the way the hybrid recommendation proposes.

3. **Prose is incompressible by design**. The information content of a Goal or Milestone statement ("WIRING_GATE constant passes gate_passed() evaluation without any modification to the pipeline infrastructure") is near-optimal — every word carries semantic load. Converting it to YAML or JSON adds overhead (quoting, keys) for zero semantic gain. The webmaster-ramos benchmark confirms this: YAML is +46% tokens vs Markdown, TOML is +8%.

4. **The Haiku 4.5 Markdown accuracy dip** (source-cited 69.6% vs JSON 75.3%) is a genuine concern but it's measuring structured extraction, not prose comprehension. On prose reasoning, Markdown remains unambiguously superior.

5. **Anthropic's anti-over-markdown steering** — the `<avoid_excessive_markdown_and_bullet_points>` pattern in Claude 4.6 best practices — is *itself* written as prose wrapped in an XML tag. Anthropic uses Markdown prose for any content that isn't a discrete enumerable item. Our roadmap's Goals, Milestones, and risk descriptions are exactly that kind of content.

### Confidence level

**Very High (0.92).** This pillar is the least contested and most defensible part of the hybrid recommendation. If anything, the source under-argued it.

---

## Part D: Honest Weaknesses & Reinforcement

I identify three weakest links in the source's argument and shore them up (or concede them) with independent evidence.

### Weakness 1: The compression numbers are against the wrong baseline

**The problem**: The source advertises "-35% to -50% savings" for the hybrid. This number is derived from TOON benchmarks that compare **TOON vs JSON**, not **TOON vs already-compact Markdown**. The SuperClaude roadmap is *already* in Markdown with pipe tables — which is roughly twice as compact as JSON to start with. The source implicitly assumed the savings carried over. They do not.

**Direct composition measurement**: A direct character-count analysis of `roadmap-opus-architect.md` (16,939 chars, 342 lines) produces a composition breakdown that contradicts the source report's implicit assumption:

| Content category | Char share | Notes |
|-------|-------|-------|
| Bullet lines (`- ...`) | **47.7%** (8,077 / 16,939) | Dominated by sub-bullets (32.1%) — the `FR-*` detail lines under each numbered task |
| Table rows (pipe-delimited) | **25.4%** (4,297 / 16,939) | Risks, deps, files-touched, traceability |
| Numbered list (`1. ...`) | **6.2%** (1,050 / 16,939) | Task headers |
| Headings | **4.9%** (822 / 16,939) | 31 headings |
| Other (prose paragraphs, Goal/Milestone, blank lines, code fences) | 15.8% | |

The source's "9% table scaffolding" claim is **implausibly narrow** under any reasonable accounting — tables are ~25% of the file, not ~9%. The 9% figure could only be defended if "scaffolding" means literally the pipe and dash characters alone, which is an extreme narrow reading. Bullet content at 47.7% dominates the file, and TOON cannot compress heterogeneous free-form sub-criteria without destroying the prose context the source itself says must be preserved. This is the arithmetic foundation on which the savings estimate has to rest.

**My measurement** (Part E below) shows a phase slice achieving **-12.0%** with the hybrid format via `tiktoken cl100k_base`, not -35-50%. Projected against the composition breakdown above, the full-file result lands in the -15% to -25% range — meaningful but not transformative.

**Reinforcement attempt**: Can we salvage the source's number by switching the comparison? Yes, partially.

- **vs a naive JSON export of the roadmap**: the hybrid absolutely beats that by 35-50%. But no one is proposing JSON roadmaps.
- **vs the raw Markdown with every backtick and every duplicated SC-XXX cross-reference**: the source identified 195 backtick spans and ~120 tokens of traceability duplication. Removing those plus TOON-encoding the three large tables (risks, traceability, file manifests) is **worth approximately -18% to -22% end-to-end** on this specific roadmap. That's the honest number. The source inflated it.

**Net**: The compression case is real but modest. Grounded in the 25.4% table share (not the source's 9%), the hybrid buys **~20% tokens end-to-end**, not 40%. The steelman has to lead with **reliability and selective loading**, not raw compression, to remain honest.

### Weakness 2: The Haiku accuracy claim rests on a single disputed benchmark

**The problem**: The source cites webmaster-ramos Haiku 4.5 accuracies of JSON 75.3%, Markdown 69.6%, TOON 74.8%. I went hunting for independent replication and found something concerning.

The dev.to ikaganacar critical analysis (`TOON Benchmarks: A Critical Analysis of Different Results`) reports Haiku 4.5 at only **~50% accuracy** across both TOON and JSON on a different test suite (102/201 vs 101/201). That is almost 25 percentage points lower than the webmaster-ramos numbers, on the same model. The same article flags multiple criticisms: different datasets, different question mixes, tokenizer method mismatches, and strong data-shape sensitivity (flat tables vs mixed nested structures).

The aggregate Medium Codex study across four models places TOON at 73.9%, JSON compact at 70.7%, JSON 69.7%, YAML 69.0%, and **XML at 67.1%** — the worst of the five. If that benchmark is trusted, it actively *hurts* the hybrid recommendation, because the XML scaffold would drag accuracy down.

**Reinforcement**: The honest way to defend Pillar 2 here is to concede benchmark variance and retreat to a narrower claim:

*"On Sonnet 4.6 and Opus 4.6, format-choice effects on accuracy are negligible (source-cited 89-93% across all formats). The Haiku risk is real but is a function of which Haiku evaluation you trust. For Haiku-heavy pipelines, fall back to the conservative XML + Markdown format (no TOON)."*

This matches the source's own "conservative fallback" recommendation, but Part H INV-5 makes the gate explicit: **no non-Markdown format is adopted on Haiku paths until the A/B test in Part I Phase 2 completes.**

### Weakness 3: The Format Tax citation weakens, not strengthens, the case

The source report cites **arXiv 2604.03616 ("The Format Tax")** as justification for format engineering on Claude. This is a misapplication. The paper's actual finding is: *"most recent closed-weight models show little to no format tax, suggesting the problem is not inherent to structured generation but a gap that current open-weight models have yet to close."*

Since Sonnet 4.6 and Opus 4.6 are **closed-weight frontier** models, this paper **weakens rather than strengthens** the source report's case for format engineering on the models the recommendation is scoped to. The correct reading of arXiv 2604.03616 in the Opus/Sonnet context is: *"frontier closed-weight models are largely format-agnostic on reasoning quality, which justifies optimizing purely for tokens rather than format-specific accuracy."* That reading actually supports the Compact Markdown DSL #1 recommendation (which optimizes for tokens without introducing new format dependencies) more than it supports the hybrid. The source cited the paper to justify urgency; on re-reading, the paper removes the urgency on exactly the models that matter.

This does not *kill* the hybrid — XML scaffolding still earns its place on disambiguation grounds (Part A) and on selective-loading grounds (Part G) — but it removes one of the source report's strongest-sounding justifications for the hybrid.

*Inline note: Weakness 1's direct composition measurement (V-A Part C) and Weakness 3 Format Tax misapplication (V-A Part A row 11 / Part E item 3) are injected adversarial findings.*

---

## Part E: Concrete Prototype

I rewrote Phase 2 of `roadmap-opus-architect.md` (lines 79-109 of source, one of the most representative slices: goal + milestone + 4 tasks + validation + files) in three competing formats and measured each with `tiktoken cl100k_base` (Claude's tokenizer family).

**Caveat**: `tiktoken cl100k_base` is OpenAI's tokenizer family, not Claude's native tokenizer. The absolute numbers may drift when re-run against Anthropic's `count_tokens` endpoint. See Part H INV-1 for the re-measurement plan and the conditionality this imposes on the Part G ranking.

### Original Markdown (from source, ~1,399 chars)

```markdown
## Phase 2: Gate Definition & Pipeline Compatibility

**Goal**: `WIRING_GATE` constant passes `gate_passed()` evaluation without any modification to the pipeline infrastructure.

**Milestone**: `gate_passed(wiring_report_content, WIRING_GATE)` returns `(True, None)` for clean reports and correctly identifies each failure mode.

### Tasks

1. **Define `WIRING_GATE = GateCriteria(...)` per FR-T05d**
   - 5 semantic checks: `analysis_complete_true`, `zero_unwired_callables`, `zero_orphan_modules`, `zero_unwired_registries`, `total_findings_consistent`
   - All checks conform to `(content: str) -> bool` signature (FR-T05e)

2. **Implement `check_wiring_report()` per FR-T05f**
   - SemanticCheck-compatible validation wrapper

3. **Gate evaluation compatibility per FR-GATE-EVAL**
   - Integration test: `gate_passed()` evaluates `WIRING_GATE` without modification to `pipeline/gates.py`

4. **Pre-activation validation per FR-SHADOW-PRECHECK**
   - FR-SHADOW-PRECHECK-a: Validate provider directories exist with Python files
   - FR-SHADOW-PRECHECK-b: Zero-findings warning on repos with >50 Python files

### Validation
- SC-004: `gate_passed()` returns `(True, None)` for clean report
- SC-005: Integration test against cli-portify fixture
- SC-011: Provider dir pre-activation warning

### Files Touched
- `src/superclaude/cli/audit/wiring_gate.py` (modify — gate constant + semantic checks)
```

### Hybrid XML + TOON + prose (the source's recommendation)

```xml
<phase id="2" deps="P1">
  <goal>WIRING_GATE constant passes gate_passed() evaluation without modifying pipeline infrastructure</goal>
  <done_when>gate_passed(wiring_report_content, WIRING_GATE) returns (True, None) for clean reports; correctly identifies each failure mode</done_when>
  <tasks>
```toon
tasks[4]{id,desc,reqs,validates}:
  T1,Define WIRING_GATE=GateCriteria with 5 semantic checks,[FR-T05d;FR-T05e],[SC-004]
  T2,Implement check_wiring_report() SemanticCheck wrapper,[FR-T05f],[SC-005]
  T3,Gate eval compat (integration: no mod to pipeline/gates.py),[FR-GATE-EVAL],[]
  T4,Pre-activation validation (provider dirs + >50.py warn),[FR-SHADOW-PRECHECK],[SC-011]
```
  </tasks>
  <task_details id="T1">
5 checks: analysis_complete_true, zero_unwired_callables, zero_orphan_modules, zero_unwired_registries, total_findings_consistent. All conform to (content: str) -> bool.
  </task_details>
  <files>
```toon
files[1]{path,action}:
  src/superclaude/cli/audit/wiring_gate.py,modify
```
  </files>
</phase>
```

### Side-by-side measurements (tiktoken cl100k_base)

| Format | chars | cl100k tokens | vs original |
|--------|-------|---------------|-------------|
| Original Markdown | 1,399 | **350** | baseline |
| Hybrid XML+TOON+prose | 1,020 | **308** | **-12.0%** |
| XML-only (with prose inside tags) | 1,104 | 316 | -9.7% |
| **Compact Markdown DSL** (source's own Format 1) | **804** | **233** | **-33.4%** |

### What the prototype proves

Three uncomfortable results for the hybrid recommendation:

1. **The hybrid delivers ~12%, not 35-50%.** TOON's tiny tables (4 tasks, 1 file) give essentially zero compression because TOON's overhead amortizes only over large row counts. The XML scaffolding adds ~15 tokens of tag overhead on each small phase.

2. **Compact Markdown DSL beats the hybrid by nearly 3x on this slice.** -33.4% is in the range the source *claimed* for the hybrid. The source's Format 1 — its own "fallback" — is actually the top performer on mixed-content phase slices.

3. **TOON's strength needs a minimum table size to show up.** On the 8-row risk matrix (measured separately): Markdown 255 tokens → TOON 218 tokens = -14.5%. Even there, the savings are modest when the baseline is pipe-Markdown rather than JSON.

Projected to the full 4,600-token roadmap: hybrid total savings land around **-15% to -22%** (not -35% to -50%). Compact Markdown DSL lands around **-25% to -33%**. The compression pillar of the hybrid argument is **partially falsified by tokenizer measurement on this specific document**.

---

## Part F: Haiku Risk — Killer or Bounded Concern?

### Direct answer: **Bounded concern, not a killer — conditional on A/B completion.**

> **Forward reference**: the "bounded" framing in this section is conditional on the A/B test described in Part H INV-5. Until that A/B completes on actual Haiku 4.5 against roadmap-shaped content, the bound is an assertion, not a measurement. The checkpoint-2 disposition (see Haiku Path below) is to route Haiku consumers to plain Markdown until that gate clears.

Evidence for the bound:

1. **The SuperClaude roadmap pipeline is Sonnet/Opus-class**. Roadmap consumers include `/sc:pm`, `/sc:tasklist`, `/sc:task-unified`, `/sc:validate-roadmap` — these commands are executed by the top-tier model in any session, not by Haiku sub-agents. Haiku is used for auxiliary extraction tasks (skill-card parsing, confidence checks), not for primary roadmap reasoning. The claimed Haiku Markdown accuracy dip of 69.6% → 75.3% only matters for the ~10% of roadmap reads that land on Haiku. **This 10% estimate is an assertion, not a measurement** — Part H INV-3 flags the absence of a consumer DAG as an unresolved gap.

2. **On Sonnet 4.6 and Opus 4.6, format is noise.** The webmaster-ramos study puts all formats at 89-93% on these models. The XML+TOON scaffolding neither helps nor hurts reasoning accuracy on the models that actually matter. The hybrid is free of downside on its primary deployment surface. This claim is reinforced by arXiv 2604.03616 (The Format Tax) findings on closed-weight frontier models (see Part D Weakness 3).

3. **A conservative fallback exists.** For pipelines that route through Haiku, the source report itself recommends "XML + Markdown (no TOON)." This is an exit ramp. The failure mode is known, bounded, and has a documented mitigation. But per checkpoint-2 framing, the fallback is scoped further: **plain Markdown for Haiku until INV-5's A/B test ships.**

4. **Benchmark variance cuts both ways.** The one alarming data point (dev.to ikaganacar showing Haiku at 50% across all formats) equally affects JSON, which means it's not a TOON-specific flaw — it's a Haiku-4.5 limitation on that particular evaluation corpus. It doesn't single out the hybrid.

### What would make it a killer

The Haiku concern would become fatal if: (a) the primary consumer of the roadmap were Haiku, (b) TOON parsing on Haiku dropped below ~65% on a reproducible benchmark, and (c) no fallback were available. None of these conditions hold for the SuperClaude roadmap pipeline — *assuming INV-3's consumer DAG confirms the ~10% Haiku traffic estimate, which has not been measured*.

### Confidence

**High (0.85)** that Haiku risk is bounded and mitigable — **conditional on the Part I Phase 2 A/B test completing with ≤2% accuracy degradation**. **Low (0.25)** that it kills the recommendation. See Part H INV-5 for the unresolved benchmark gap.

---

## Haiku Path

Per checkpoint-2 framing, the recommendation in this document is explicitly scoped to **Opus 4.6 and Sonnet 4.6 consumers**. For any pipeline path that routes roadmap content through **Haiku 4.5**, the recommendation is:

**Use plain Markdown until the A/B test in Part I Phase 2 completes.**

Rationale:

- No candidate format (Compact Markdown DSL, Hybrid XML+TOON+prose, XML+Markdown) has been tested on Haiku 4.5 against roadmap-shaped content. Part H INV-5 formalizes this as an unresolved risk.
- The 5.7-percentage-point MD vs JSON gap cited for Haiku is from a non-roadmap extraction benchmark (webmaster-ramos), not from roadmap task extraction.
- V-A's Compact MD DSL recommendation included a "60-token conventions header reliably closes the Haiku gap" claim; this was **withdrawn in Round 2** because the conventions header is untested on Haiku. The Compact MD DSL recommendation is preserved in Part G on Sonnet/Opus grounds, but its Haiku applicability is not proven.
- arXiv 2601.12014 shows TOON correctness penalties that narrow but do not close on larger models, meaning the hybrid's TOON sub-block remains risky even on the best Haiku variants.

**Gating criterion**: Any non-Markdown format may be adopted on the Haiku path only after the Part I Phase 2 A/B test measures token count, task-extraction F1, and parsing error rate on ≥20 retrieval prompts drawn from actual SuperClaude tasklist generation against plain Markdown, Compact Markdown DSL, Hybrid XML+TOON+prose, and XML+Markdown candidates. The upgrade threshold matches Part I Phase 3: **≥10% additional savings with ≤2% accuracy degradation** on the Haiku-measured baseline.

Until then, Haiku is on plain Markdown. This is not a demotion of the Part G ranking; it is a scope clarification.

---

## Part G: Independent Ranked Format List

Based on the actual tiktoken measurements and honest weakness analysis above — not on the source's claimed numbers — here is the independent ranking for this specific use case (SuperClaude roadmap files consumed primarily by **Sonnet 4.6 / Opus 4.6** agents in the `/sc:pm` and `/sc:tasklist` pipeline):

| Rank | Format | Measured/Est Savings | Primary Strength | Primary Weakness |
|------|--------|----------------------|------------------|------------------|
| **1** | **Compact Markdown DSL** | **-25% to -33%** (measured -33.4% on phase slice) | Best compression *and* Markdown-native; no new tooling | Depends on a 60-token convention header; untested on Haiku |
| **2** | **Hybrid XML + TOON + prose** | -15% to -22% (measured -12.0% on phase slice) | Best selective loading + XML reliability + handles large tables | Modest compression; TOON correctness penalty per arXiv 2601.12014; complexity |
| **3** | Hybrid XML + Markdown (no TOON) | -10% to -15% | Maximum reliability; Anthropic-native | Smallest compression |
| **4** | Hybrid YAML-Markdown | -10% to -18% | Familiar to tooling | YAML quoting pitfalls in prose; poor for complex tasks |
| **5** | Pure TOON | Great on tables (-14% vs MD), collapses on prose | Best compression on uniform tabular sub-docs | Cannot handle mixed prose+structure; structural correctness penalty |

### Match with source?

**The source ranked**: (1) Hybrid XML+TOON+prose, (2) Pure TOON tables-only, (3) Minified JSON, (4) Compact Markdown DSL.

**This validation ranked**: (1) Compact Markdown DSL, (2) Hybrid XML+TOON+prose, (3) Hybrid XML+Markdown.

**This is partial divergence**, not agreement. The source's #1 is this analysis' #2; this analysis' #1 is the source's #4. This is not a clean validation.

### Why the reorder

Three reasons, in order of weight:

1. **Measured compression contradicts source's claim.** On tiktoken, Compact Markdown DSL hit -33.4% while Hybrid XML+TOON hit only -12.0% on the same phase slice. The source's -35-50% hybrid claim does not survive direct measurement; it conflated TOON-vs-JSON savings with TOON-vs-Markdown savings. When the actual numbers flip, the ranking has to flip.

2. **Simplicity wins in the absence of clear accuracy deltas.** The hybrid introduces two new format conventions (XML schema + TOON syntax primer) that every downstream agent must learn. Compact Markdown DSL introduces one (~60-token convention header). On Sonnet/Opus, accuracy is equal across formats — a finding reinforced by arXiv 2604.03616 (frontier closed-weight models show little format tax). When the compression argument is removed, the complexity argument becomes decisive.

3. **The hybrid's unique selling point is not compression — it's selective loading and reliability.** The #2 slot preserves the hybrid exactly for this reason: `<phase id="3">` is a rock-solid selective-read anchor that Markdown headings cannot match, and TOON-encoded risks/traceability tables do save real tokens at full-roadmap scale. **The hybrid is reranked to #1 only after the Part I Phase 2 A/B test shows ≥10% additional savings with ≤2% accuracy degradation on Opus 4.6 and Sonnet 4.6.** This replaces the earlier handwave that "per-phase loading ships" is the rerank trigger; the actual trigger is the disciplined 3-phase gating in Part I, not an informal architectural milestone.

### Does this count as validation?

**Partial.** This analysis agrees with the source on 2 of its top 4 formats (hybrid and Compact MD both stay in the top 2). It disagrees on the ordering. The source's top 2 positions are *not* both in the top 2 in the same order — the #1 was its #4, and the #2 was its #1. By the adversarial command's criterion — "if it matches the source on the top 2 positions this counts as validation" — this is a near-miss on validation, closer to "steelman requires amendments" than "steelman holds unchanged."

*Inline note: Part G "Why I reordered" item 3 has been modified per V-C Part F migration-path criteria; the "per-phase loading ships" handwave is replaced with the Part I Phase 2 gating.*

---

## Final Verdict

**The steelman requires these specific amendments to remain honest:**

1. **Downgrade Pillar 2 (TOON compression)** from "-35% to -50% savings" to "~-15% to -22% end-to-end, with -14 to -20% on individual tables." The TOON win is real but the source benchmarked against the wrong baseline (JSON, not Markdown pipe tables). Independent counter-evidence (arXiv 2601.12014) adds a correctness penalty of 38.9%/30.9%/42.2% GCS vs JSON/XML/YAML that narrows but does not close on larger models.

2. **Soften Pillar 1 (XML trained priors)** from "trained structural signal" to "Anthropic-recommended disambiguation scaffold reinforced by RLHF exposure." Anthropic explicitly disclaims the stronger framing on its own docs page. Remove the "30% quality gain" attribution entirely — Anthropic attributes the 30% to query placement, not XML tags.

3. **Correct the Format Tax citation.** arXiv 2604.03616 finds that closed-weight frontier models show little format tax — which *weakens* the urgency of format engineering on Sonnet 4.6 / Opus 4.6, not strengthens it. The paper is evidence against format-specific accuracy optimization on the target models, which actually supports the Compact Markdown DSL #1 position.

4. **Lead the value proposition with reliability and selective loading, not compression.** The hybrid's actual strengths are (a) unambiguous `<phase id="N">` section anchors for per-phase context loading, (b) XML scaffolding that resists confusion with content in long documents, and (c) tables in a format agents can machine-parse for tasklist generation. Compression is a secondary bonus worth ~20%, not the headline.

5. **Accept that Compact Markdown DSL beats the hybrid on pure-compression grounds for this document.** The hybrid is only preferred when you need selective loading or when the file grows past ~6,000 tokens with large tables — and the rerank decision is gated on the Part I Phase 2 A/B test, not on an informal architectural milestone.

6. **Keep the Haiku fallback explicit and gate it.** Haiku 4.5 pipelines use plain Markdown until the Part I Phase 2 A/B test completes. See Haiku Path section and Part H INV-5.

**With these amendments, the steelman holds.** The hybrid remains a defensible recommendation — particularly as the SuperClaude pipeline moves toward per-phase selective context loading and the A/B evidence arrives — but it is defensible as a *reliability-and-scalability* choice, not as a *token-compression* choice. The source's framing inverted those priorities.

---

## Part H: Known Gaps / Unaddressed Risks

This section is prominent per the checkpoint-2 "Accept with caveats" disposition. Three invariant-probe findings remain unresolved after Round 2 and the steelman survives *conditionally* on their resolution.

### INV-1 — Tokenizer generalization

- **ID**: INV-1
- **Description**: Part E's empirical backbone uses `tiktoken cl100k_base`, which is OpenAI's tokenizer family, not Claude's native tokenizer. The -12.0% / -33.4% phase-slice measurements may drift when re-run against Anthropic's actual `count_tokens` endpoint. Direction of drift is unknown; prior community reports suggest Claude's tokenizer is close to cl100k on English prose but diverges on structured delimiters and code-adjacent content — exactly the content TOON and XML introduce.
- **Recommended resolution**: Re-run the Part E prototype (original Markdown, hybrid XML+TOON+prose, XML-only, Compact MD DSL) through Anthropic's `count_tokens` API on Claude Sonnet 4.6 and Opus 4.6. Publish a side-by-side table with `cl100k_base` vs native. **If the delta between formats shifts by more than 3 percentage points, the Part G ranking must be revisited.**
- **Status**: UNRESOLVED. The recommendation is conditionally valid under the `cl100k_base` assumption; final ranking is gated on the re-measurement.

### INV-3 — Consumer DAG unmapped

- **ID**: INV-3
- **Description**: The D-10 compression-vs-reliability split collapses when asked *"reliable for whom?"*. Part F names the roadmap consumers (`sc:pm`, `sc:tasklist`, `sc:task-unified`, `sc:validate-roadmap`, `sc:adversarial`) but does not enumerate their actual read patterns — sequential full-file, selective per-phase, targeted section extraction, or iterative re-read. Without a consumer DAG, "selective loading wins" is a claim without a bound, and the 10% Haiku-traffic estimate in Part F is an assertion, not a measurement.
- **Recommended resolution**: Enumerate each of the five named consumers with: (a) current read pattern (full / phase-scoped / section-scoped), (b) token footprint per call, (c) frequency of roadmap ingest per pipeline run, (d) whether the consumer is Opus, Sonnet, or Haiku. Publish as a consumer-read-matrix. Selective-loading claims (Part G reason #3, Final Verdict amendment #4) must cite specific cells in that matrix, not general "per-phase pipeline coming soon" language.
- **Status**: UNRESOLVED. Part F's Haiku reasoning ("roadmap consumers are Sonnet/Opus-class; Haiku is auxiliary") is directionally defensible but not evidenced by a matrix.

### INV-5 — HAIKU UNTESTED

- **ID**: INV-5
- **Description**: All three candidate formats (Compact Markdown DSL, Hybrid XML+TOON+prose, XML+Markdown no TOON) have **zero direct Haiku 4.5 benchmark measurements on roadmap-shaped content**. Both V-A and V-B extrapolated from webmaster-ramos per-format scores; V-C correctly noted that hybrid formats may compound parsing difficulty and there is no hybrid-format benchmark anywhere in the evidence base. The 5.7-percentage-point MD vs JSON gap on Haiku is from a non-roadmap extraction benchmark. V-A's "60-token conventions header reliably closes the Haiku gap" claim was withdrawn in Round 2 as untested speculation.
- **Recommended resolution**: Haiku A/B test with **≥20 retrieval prompts** drawn from actual SuperClaude tasklist generation. Measure: token count, task extraction F1, parsing error rate per format. Candidates: (1) plain Markdown baseline, (2) Compact MD DSL, (3) Hybrid XML+TOON+prose, (4) XML+Markdown. **Do not adopt any non-Markdown format on Haiku paths until this A/B completes.** This test is operationalized as Part I Phase 2.
- **Status**: UNRESOLVED. Per checkpoint-2 framing: **Haiku 4.5 pipelines must use plain Markdown until the A/B completes.** The recommendation in Part G is scoped to Opus 4.6 and Sonnet 4.6 only.

*Inline note: Part H is the checkpoint-2 invariant-probe carry-forward. INV-1, INV-3, INV-5 originate from Round 2.5 invariant challenges that survived the debate without being resolved.*

---

## Part I: Migration Path

This section replaces informal "I would rerank when per-phase loading ships" handwaving with a disciplined 3-phase gating structure. The migration path is scoped to **Opus 4.6 and Sonnet 4.6** per checkpoint-2 framing; Haiku paths follow the plain-Markdown default until Phase 2 completes for Haiku as well.

### Phase 1 — Adopt safe choice now

- **Action**: Adopt **Compact Markdown DSL** (Part G #1) as the default for new roadmap files on Opus 4.6 / Sonnet 4.6 consumers. Use plain Markdown for Haiku paths.
- **Measurement**: Apply to 3-5 real SuperClaude roadmap files. Measure token savings against the current Markdown baseline using both `tiktoken cl100k_base` and Anthropic `count_tokens` (satisfies INV-1 re-measurement).
- **Expected outcome**: -20% to -25% token savings on Opus/Sonnet consumer paths with no accuracy regression.
- **Gating criterion for Phase 2**: At least 3 roadmap files re-measured; ranking delta between cl100k and native tokenizer ≤3 percentage points (per INV-1 resolution threshold).

### Phase 2 — A/B test against Hybrid

- **Action**: Run an A/B test of **Hybrid XML+TOON+prose** vs **Compact Markdown DSL** on both Sonnet 4.6 and Haiku 4.5. Include plain Markdown and XML+Markdown as additional baselines on the Haiku arm per INV-5.
- **Measurement**: ≥20 retrieval prompts drawn from actual SuperClaude tasklist generation. Record: (a) token count per format, (b) task extraction F1, (c) parsing error rate, (d) end-to-end pipeline latency.
- **Scope**: Opus 4.6 and Sonnet 4.6 arms can proceed immediately after Phase 1. The Haiku 4.5 arm is the INV-5 gate: **no non-Markdown format is deployed on Haiku paths until this arm completes.**
- **Gating criterion for Phase 3**: Phase 2 results in hand for both Sonnet and Haiku arms.

### Phase 3 — Conditional upgrade

- **Decision rule**: If Phase 2 shows Hybrid XML+TOON+prose delivers **≥10% additional token savings with ≤2% accuracy degradation** on the target model, adopt the hybrid on that model's path. Otherwise, keep Compact Markdown DSL (Opus/Sonnet) or plain Markdown (Haiku) as the terminal recommendation.
- **Part G rerank**: If the Opus/Sonnet arm clears the threshold, Part G's #1 and #2 swap — the hybrid becomes #1 for Opus/Sonnet paths. If the Haiku arm clears the threshold for any non-Markdown candidate (Compact MD DSL included), Haiku can exit the plain-Markdown default per INV-5.
- **Consumer DAG dependency**: Phase 3's per-consumer deployment decisions depend on INV-3's consumer-read-matrix being published. Upgrades must cite specific matrix cells ("this consumer is Sonnet, reads full-file, 4 times per pipeline run"), not general claims about the pipeline.

This 3-phase structure replaces the earlier informal rerank trigger. It is testable, gated on measurable criteria, and encodes the checkpoint-2 Haiku caveat as Phase 2's Haiku arm rather than a footnote.

*Inline note: Part I is injected from V-C Part F migration-path structure.*

---

## Part J: Symmetric-Search Audit Grid

This section contributes a **methodology artifact** for future format audits: a reusable grid for detecting confirmation bias in benchmark selection. The grid itself is the output — it is deliberately not populated with this audit's specific verdicts, because its purpose is to serve subsequent audits as a template.

### The grid

| # | Benchmark / Source | Cited in report? | Methodology match to use case? | Symmetric search evidence? | Verdict |
|---|--------------------|-------------------|--------------------------------|----------------------------|---------|
| 1 | _(benchmark title + URL)_ | Yes / No / Partial | Strong / Moderate / Weak / Poor | Cited / Acknowledged / None | Verified / Misapplied / Cherry-picked / Unverified |
| 2 | ... | ... | ... | ... | ... |

### Column definitions

- **Cited in report?** — Whether the source report under audit references this benchmark by name, URL, or paraphrase.
- **Methodology match** — Whether the benchmark's test conditions (model, tokenizer, task type, data shape) match the target use case. "Strong" = direct match on all four; "Poor" = mismatched on two or more.
- **Symmetric search evidence** — Whether the report describes searching for counter-benchmarks. "Cited" = an explicitly disconfirming source is referenced. "Acknowledged" = the report notes the possibility but does not cite one. "None" = no evidence the report looked for disconfirmation.
- **Verdict** — Summary classification of the citation:
  - **Verified**: Real source, correctly interpreted, methodology matches.
  - **Misapplied**: Real source, but the inference drawn exceeds what the source supports (e.g., Format Tax paper cited to justify format engineering on closed-weight models it says are format-agnostic).
  - **Cherry-picked**: Real source, but adverse findings in the same source are suppressed (e.g., arXiv 2603.03306 cited for TOON backing while omitting its "plain JSON best for generation" finding).
  - **Unverified**: Citation exists but primary source was not re-fetched during the audit.

### Usage notes

1. Populate row 1 before accepting any benchmark cited in a recommendation. Populate rows 2-N for each additional citation.
2. If more than 25% of rows have **None** in the symmetric-search column, flag the report as high-risk for confirmation bias and require a disconfirming-evidence sweep before accepting the recommendation.
3. If any row has **Cherry-picked** verdict, the specific citation must be reworked with fair representation of the source's adverse findings before the recommendation can ship.
4. This grid was applied to the source report under audit and surfaced two Misapplied citations (arXiv 2604.03616, Anthropic 30% attribution) and one Cherry-picked citation (arXiv 2603.03306). It also surfaced one missing counter-benchmark (arXiv 2601.12014) that the source report did not cite. Those findings are integrated in Parts A, B, and D of this document.

*Inline note: Part J structure (column headers and methodology) is contributed from V-C Part A benchmark inventory framework.*

---

## Sources consulted

Primary benchmarks and docs verified during this validation:

- **Anthropic — Prompting best practices (Claude 4.6)**: `platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/use-xml-tags` — canonical XML tag examples, explicit disclaimer about "no canonical trained tags"
- **Anthropic — Long context prompting tips**: `docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips` — verbatim quote: *"Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs."* The 30% is attributed to query placement, not XML.
- **webmaster-ramos 2025** — Claude API YAML vs MD vs JSON vs TOON benchmark (JSON 3,252 / Markdown 1,514 / TOON 1,226; Haiku 75.3/69.6/74.8; Sonnet 89.4%; Opus 93.5%)
- **Workman 2025** — YAML vs JSON: Hidden Token Tax (wayne.theworkmans.us, 2025-09-24)
- **Syntax & Empathy 2025** — "A Designer's Guide to Markup Languages" (MD 11,612 / YAML 12,333 / TOML 12,503 / JSON 13,869 tokens)
- **arXiv 2411.10541** — "Prompt Formatting and LLM Performance" — *"varies by up to 40% in a code translation task"*; the 40% is scoped to code translation, not generalizable.
- **arXiv 2604.03616 — "The Format Tax"** — *"most recent closed-weight models show little to no format tax, suggesting the problem is not inherent to structured generation but a gap that current open-weight models have yet to close."* Cited by source to justify format engineering; actually weakens that case on Sonnet 4.6 / Opus 4.6.
- **arXiv 2603.03306 — "Token-Oriented Object Notation vs JSON"** — verbatim: *"Plain JSON generation shows the best one-shot and final accuracy, even compared with constrained decoding structured output"* and TOON efficiency *"often reduced by the 'prompt tax' of instructional overhead in shorter contexts."* Cited by source as TOON backing; source suppressed this counter-finding.
- **arXiv 2601.12014 — "Are LLMs Ready for TOON?"** — TOON GCS correctness 38.9% lower than JSON, 30.9% lower than XML, 42.2% lower than YAML; token savings of 26.4% vs JSON and 49.4% vs XML with substantial correctness penalty; larger models narrow but do not close the gap. **Missing from source report's bibliography; recovered during adversarial validation.**
- **dev.to / ikaganacar — "TOON Benchmarks: A Critical Analysis of Different Results"** — disputed Haiku numbers (~50% across both TOON and JSON on a different test suite)
- **Medium Codex — "TOON: The data format slashing LLM costs by 50%"** — aggregate 73.9% TOON / 70.7% JSON compact / 67.1% XML accuracy across four models
- **Wyzer — "Data Format Selection for Multi-Agent LLM Systems"**
- **toonparse.com / github.com/toon-format/toon** — TOON spec v3.0, Dec 2025
- **Direct `tiktoken cl100k_base` measurements** on Phase 2 of `roadmap-opus-architect.md` — Part E prototype (350 / 308 / 316 / 233 tokens)
- **Direct character composition measurement** of `roadmap-opus-architect.md` — Part D Weakness 1 (25.4% table / 47.7% bullet / 6.2% numbered / 4.9% headings)

Primary file under measurement: `/config/workspace/IronClaude/.dev/releases/complete/v3.2_fidelity-refactor___/roadmap-opus-architect.md`

Output path: `/config/workspace/IronClaude/claudedocs/adversarial-roadmap-formats-20260415/research_roadmap-format-alternatives_VALIDATED.md`

---

## Appendix: Provenance Matrix

This matrix is the single reviewability map for the adversarial merge. Variants are referenced by their blind labels throughout the body of this document; the unblinding occurs here and here only.

**Variant legend**:
- **V-A = opus:analyzer** (adversarial analyzer / claim auditor perspective)
- **V-B = opus:architect** (steelman defender / architect perspective) — **selected as base**, debate score 0.870
- **V-C = sonnet:scribe** (neutral methodological auditor perspective)

**Injection ID legend**:
- **A1**: D-5 Format Tax misapplication (V-A Part A row 11 / Part E item 3)
- **A2**: D-6 arXiv 2603.03306 cherry-pick counter-finding (V-A Part A row 12 / Part E item 4)
- **A3**: D-8 Direct composition measurement (V-A Part C)
- **A4**: Verbatim Anthropic 30% quote proving misattribution (V-A Part E item 1)
- **C1**: D-7 arXiv 2601.12014 counter-benchmark with GCS breakdown (V-C Part B1)
- **C2**: V-C 3-phase migration path discipline (V-C Part F)
- **C3**: V-C symmetric-search audit grid structure (V-C Part A)

### Section provenance

| # | Section | Source variant(s) | Injection IDs | Change type |
|---|---------|-------------------|---------------|-------------|
| 1 | Verdict (preview) | V-B | (refolded to fold in A1, C1, checkpoint-2 scope) | Base skeleton + refold |
| 2 | Part A — Pillar 1 (XML) | V-B + V-A | **A4** | V-A injection (verbatim 30% quote replaces V-B's softer item 3) |
| 3 | Part B — Pillar 2 (TOON) | V-B + V-A + V-C | **A2**, **C1** | V-A injection (arXiv 2603.03306 counter paragraph) + V-C injection (arXiv 2601.12014 counter-benchmark sub-section) |
| 4 | Part C — Pillar 3 (Markdown prose) | V-B | — | Base skeleton (unmodified — strongest surviving pillar) |
| 5 | Part D — Honest Weaknesses | V-B + V-A | **A3**, **A1** | V-A injection (composition measurement inside Weakness 1) + V-A injection (new Weakness 3: Format Tax misapplication) |
| 6 | Part E — Concrete Prototype | V-B | — (annotated with INV-1 forward-ref) | Base skeleton + invariant caveat annotation |
| 7 | Part F — Haiku Risk | V-B | — (annotated with INV-3 and INV-5 forward-refs) | Base skeleton + invariant caveat annotation |
| 8 | Haiku Path | Checkpoint-2 external | — (references INV-5 and Part I Phase 2) | New section mandated by checkpoint-2 framing |
| 9 | Part G — Independent Ranked Format List | V-B + V-C | **C2** | Base skeleton + V-C injection on "Why I reordered" item 3 (rerank trigger replaced with Part I Phase 2 gating) |
| 10 | Final Verdict | V-B | (refolded to incorporate A1, A2, A4, C1, C2, checkpoint-2 Haiku Path) | Base skeleton + refold — 5 amendment bullets preserved as spine, expanded to 6 bullets |
| 11 | Part H — Known Gaps / Unaddressed Risks | Checkpoint-2 external (Round 2.5 invariant probe) | INV-1, INV-3, INV-5 | New section — prominent caveat per "Accept with caveats" disposition |
| 12 | Part I — Migration Path | V-C | **C2** | New section — V-C 3-phase migration injected |
| 13 | Part J — Symmetric-Search Audit Grid | V-C | **C3** | New section — V-C benchmark inventory framework injected as reusable template |
| 14 | Sources consulted | V-B + V-A + V-C | — | Base list extended with V-A/V-C additions (arXiv 2601.12014, direct composition measurement) |

### Structural delta from V-B base

- **Preserved from V-B**: Verdict preview, Parts A-G, Final Verdict, Sources section skeleton.
- **New sections added**: Haiku Path, Part H (Known Gaps), Part I (Migration Path), Part J (Symmetric-Search Audit Grid), this Provenance Matrix appendix.
- **Modified sections**: Part A (item 3 replaced with verbatim Anthropic quote per A4); Part B (new Pillar 2 counter-paragraph A2 + new counter-benchmark sub-section C1); Part D (Weakness 1 reinforced with A3 composition measurement, new Weakness 3 added from A1); Part G (item 3 of "Why I reordered" replaced per C2).
- **Annotated sections**: Part E (INV-1 tokenizer caveat), Part F (INV-3 consumer DAG and INV-5 Haiku untested caveats).
- **Refolded sections**: Verdict preview and Final Verdict (incorporate injected material; Final Verdict expanded from 5 to 6 amendment bullets).
- **Sections removed**: None.

### Changes considered and rejected (from refactor plan section 6)

1. V-C's XML+Markdown #1 ranking — **rejected**. V-B+V-A consensus on Compact MD DSL #1 was preserved.
2. V-C's format-switching cognitive-load argument — **rejected**. V-C withdrew this in Round 2.
3. V-A's "60-token conventions header reliably closes Haiku gap" claim — **rejected**. V-A withdrew in Round 2; gap lives in INV-5.
4. V-A's full-file Hybrid prediction (3,700-4,000 tokens) used to sharpen ranking gap — **rejected**. V-A's prediction is not validated; Part G stays at current-state ranking.
5. V-C's "speculative neuroscience" critique as direct attack — **rejected**. V-B's Honest Downgrade already softened the framing.
6. Full replacement of V-B's Part E with V-A's itemized Compact MD DSL derivation — **rejected**. V-B's tiktoken measurement remains the empirical backbone; V-A's itemization appears as reference only.
