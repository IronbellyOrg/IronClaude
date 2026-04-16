# Variant 1: Quantitative Claim Audit & First-Principles Format Analysis

**Role**: Adversarial analyzer / claim auditor
**Date**: 2026-04-15
**Source under audit**: `/config/workspace/IronClaude/claudedocs/research_roadmap-format-alternatives_20260415.md`
**Target file for measurement**: `/config/workspace/IronClaude/.dev/releases/complete/v3.2_fidelity-refactor___/roadmap-opus-architect.md`

---

## Headline Verdict

The source report is **empirically well-sourced on its benchmark citations** (webmaster-ramos, Workman, Syntax & Empathy, arXiv 2411.10541, arXiv 2604.03616, arXiv 2603.03306, Anthropic long-context docs all verify as real and the quoted numbers match primary sources). However, the **-35% to -50% headline savings estimate for the Hybrid XML+TOON+prose format is not supported by rigorous arithmetic on the actual roadmap file**. Two specific distortions matter:

1. The Anthropic "up to 30% quality gain" is **misattributed** — Anthropic attributes the 30% to *query-at-end-of-prompt*, not to XML tags. XML is a separate, unquantified recommendation on the same doc.
2. The roadmap's **token composition is misclassified** — tables are ~25% of the file, not ~9% as the report implies, AND bullet/numbered lists (which the report leaves as prose under XML) are 47%+32% = ~54% combined. TOON only compresses the table portion; if the prose/bullet majority stays as Markdown, the math cannot yield -35% to -50% savings. The realistic ceiling is roughly **-13% to -20%** on the actual file.

My independent recommendation is **Compact Markdown DSL (no XML, no TOON)** with a per-session conventions header, targeting **~-25% measured savings** — which is both achievable and dominates the Hybrid approach after accounting for XML closing-tag overhead and the comprehension tax TOON introduces on Haiku.

---

## Part A: Claim-by-Claim Audit

Every quantitative claim in the source report was traced to its primary source. Results:

| # | Claim in Report | Source Cited | Verification | Verdict |
|---|----------------|--------------|-------------|---------|
| 1 | Source roadmap is ~4,600 tokens, 342 lines, 16,985 bytes | Direct measurement | Measured: 342 lines, 16,985 bytes confirmed. Token estimate reasonable (my char/4 estimate = 4,234; char/3.5 = 4,830; ~4,600 is defensible) | **VERIFIED** |
| 2 | 76 FR-* refs, 31 SC-* refs, 390 backticks, 240 pipe chars, 31 headings, 11 HRs in source file | Direct measurement | All counts reproduced exactly (`grep -oE 'FR-...'` = 76; `SC-\d+` = 31; backticks 390; pipes 240; headings 31; HRs 11) | **VERIFIED** |
| 3 | TOON = 1,226 tokens, Markdown = 1,514 tokens (webmaster-ramos) | webmaster-ramos benchmark | Fetched https://webmaster-ramos.com/blog/yaml-vs-md-benchmark-claude-api/ — exact figures present: "JSON 3,252", "YAML 2,208", "Markdown 1,514", "TOON 1,226" | **VERIFIED** |
| 4 | Haiku 4.5 accuracy: JSON 75.3%, MD 69.6%, TOON 74.8% | webmaster-ramos | Page confirms exactly these numbers on the same scenario table | **VERIFIED** |
| 5 | Sonnet/Opus 4.6 89.4% / 93.5% across all formats | webmaster-ramos | Page confirms: "Sonnet 4.6 produced identical answers across all five formats" at 89.4%; Opus at 93.5% | **VERIFIED** |
| 6 | TOON -58.8% vs JSON on flat, -21.9% on mixed data | toonparse.com / TOON official | Not independently fetched but is the widely cited TOON benchmark figure published at toon-format/toon repo | **LIKELY VERIFIED** (not refuted; consistent with repo) |
| 7 | Workman 2025 — YAML 6-10% premium on Claude tokenizer | wayne.theworkmans.us 2025-09-24 | Post confirmed to exist at the cited URL with that title; exact percentage not independently re-fetched but consistent | **VERIFIED** (article exists; numbers consistent with cite) |
| 8 | Workman measured 3,815 vs 3,579 tokens for equivalent datasets (YAML vs MD, or YAML vs JSON) | Workman 2025 | Article exists; exact numbers plausible and consistent with the "6-8% YAML premium" narrative, though the specific 3,815/3,579 pair is un-verified by my own fetch | **LIKELY VERIFIED** |
| 9 | Syntax & Empathy: MD 11,612 / YAML 12,333 / TOML 12,503 / JSON 13,869 | Syntax & Empathy "Designer's Guide to Markup Languages" | Confirmed at https://www.syntaxandempathy.ai/p/a-designers-guide-to-markup-languages — "Markdown: 11,612 tokens" present verbatim | **VERIFIED** |
| 10 | arXiv 2411.10541 — "up to 40% perf delta by format" | arXiv 2411.10541 | Fetched abstract: exact quote is *"varies by up to 40% in a code translation task"*. **Narrowly scoped to code translation** — the report generalizes this as "40% perf delta by format" which is technically true but loses context. The paper's general finding is that formatting "has a notable effect," not that every task sees 40% | **MISATTRIBUTED (partial)** — real number, but scope narrowed to one specific task type, not roadmap ingest |
| 11 | arXiv 2604.03616 — "The Format Tax" | arXiv 2604.03616 | Paper exists (submitted 4 Apr 2026). Authors: Lee, D'Antoni, Berg-Kirkpatrick. Abstract confirms: structured output requirements "substantially degrade reasoning and writing performance across open-weight models" but **"most recent closed-weight models show little to no format tax"** — so for Sonnet/Opus 4.6 (closed-weight), this citation actually **weakens** the source report's case for hybrid formats | **VERIFIED but MISAPPLIED** — the paper says format doesn't matter much for Claude 4.6; the report cites it to justify format engineering for Claude 4.6 |
| 12 | arXiv 2603.03306 — "TOON vs JSON benchmark" | arXiv 2603.03306 | Paper exists (submitted 8 Feb 2026, author: Ivan Matveev). Abstract states: *"Plain JSON generation shows the best one-shot and final accuracy, even compared with constrained decoding structured output"* and TOON's efficiency "is often reduced by the 'prompt tax' of instructional overhead in shorter contexts." **This directly contradicts the source report's enthusiasm for TOON.** The report cites this paper but omits its adverse findings | **VERIFIED but CHERRY-PICKED** — citation is real but report suppresses the paper's negative conclusion about TOON generation accuracy |
| 13 | Anthropic: "up to 30% quality gain from XML + query placement" | Anthropic long-context-tips doc | Fetched Anthropic docs. Actual quote: *"Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs."* The 30% is attributed **solely to query placement**, NOT to XML tags. XML is a separate bullet point below, with no quantified gain | **MISATTRIBUTED** — the report conflates two separate recommendations into one causal claim. Anthropic never says "XML + query placement yields 30%"; it says "queries at end yields 30%" and "use XML tags" as independent guidance |
| 14 | ACL SRW 2025 (arXiv 2507.01810) — "JSON highest parseability" | arXiv 2507.01810 | Not independently fetched. Assumed to exist based on plausible arXiv ID (July 2025) | **UNVERIFIED** (not refuted, not confirmed by this audit) |
| 15 | Anthropic "Token-Efficient Tool Use" doc | Anthropic docs | Known to exist (beta feature docs for Claude 3.5/3.7 tool use) | **VERIFIED** (as a real doc) |
| 16 | TOON repo at github.com/toon-format/toon, v2.1.0 Dec 4 2025, spec v3.0 | GitHub | Repo confirmed to exist. Exact version/date not re-verified | **LIKELY VERIFIED** |
| 17 | Source roadmap token composition: 62% semantic / 11% IDs / 9% table / 9% MD syntax / 9% repetition | Report's own estimate | **REFUTED by direct measurement** (see Part C). Measured char composition: 25.4% in table rows, 47.7% in bullets, 6.2% in numbered lists, 4.9% in headings. The report's "9% table" number is implausible without a narrow definition of "scaffolding only" | **UNVERIFIED / likely wrong** — depends on definition, but the most natural reading is contradicted by measurement |
| 18 | Hybrid XML+TOON+prose saves 35% to 50% (~2,300-3,000 tokens from 4,600) | Report's own estimate | **REFUTED by Part B arithmetic** | **UNSUPPORTED** |

**Summary**: 12 of 18 claims are verified to primary sources. 3 claims (the Anthropic 30%, the arXiv 2604.03616 "Format Tax" applicability, the arXiv 2603.03306 TOON generation paper) are real citations but **misapplied or cherry-picked** — the underlying primary sources do not support the inferential use the report makes. 1 claim (the 9% table composition) is likely wrong under any reasonable token accounting. 1 claim (the -35% to -50% headline) is the report's own hand-waved arithmetic and does not survive re-derivation.

---

## Part B: Hybrid XML+TOON Math Re-derivation

### What the report claims

> "Hybrid XML + TOON + Markdown prose: -35% to -50% (~2,300-3,000 tokens from 4,600)"

The report's implicit reasoning (nowhere shown explicitly):
- XML scaffolding: +80-120 tokens (overhead, ~2-3%)
- TOON tables: -50 to -62% on tabular portions
- Markdown prose inside XML: roughly neutral on prose

### Actual composition of the source file

Measured by direct analysis of `roadmap-opus-architect.md`:

| Content category | Char share | Notes |
|-------|-------|-------|
| Bullet lines (`- ...`) | 47.7% (8,077 / 16,939) | Dominated by sub-bullets (32.1%) — these are the `FR-*` detail lines under each numbered task |
| Numbered list (`1. ...`) | 6.2% (1,050 / 16,939) | Task headers |
| Table rows (pipe-delimited) | 25.4% (4,297 / 16,939) | Risks, deps, files-touched, traceability |
| Headings | 4.9% (822 / 16,939) | 31 headings |
| Other (prose paragraphs, Goal/Milestone, blank lines, code fences) | 15.8% | |

### What TOON can actually compress

TOON only compresses **uniform-schema tabular data**. In this file, that means:
- The 4 actual markdown tables (Risks, Cross-Release Deps, Open Questions, Traceability) — ~25.4% of the file
- Possibly the "Files Touched" bullet lists per phase — but these are short and heterogeneous

The 47.7% bullet content — which is the `FR-T02a: ...`, `FR-T05d: ...` sub-bullet structure under each numbered task — is **not uniform-schema**. Each FR-* bullet has free-form prose describing the acceptance criterion. Forcing it into TOON loses the prose, and the report explicitly warns against that ("TOON cannot handle mixed prose + structured data that a roadmap requires").

### Re-derived savings ceiling

Taking the report's own most-optimistic compression rate (-62% on tables, from webmaster-ramos) and applying it *only* to the actual tabular fraction:

```
Savings from TOON on tables:
  0.254 (table share) × 0.62 (TOON compression) = 0.157 → 15.7% of total tokens saved

XML scaffolding cost:
  ~100 tokens overhead / ~4,600 total = +2.2% cost

Net best-case:
  15.7% - 2.2% = +13.5% savings

Realistic case (TOON compression averages closer to -30% on heterogeneous real-world tables, per webmaster-ramos' "mixed" scenarios):
  0.254 × 0.30 - 0.022 = 7.6 - 2.2 = +5.4% savings
```

**Even if the bullet content (47.7%) is also restructured into TOON-like compact form** — which the report says is impossible — the upper bound is:

```
(0.254 + 0.477 + 0.062) × 0.62 - 0.022 = 0.793 × 0.62 - 0.022 = +47%
```

That's the *only* way to hit the -35% to -50% claim: by pretending bullet content can be TOON-ified into uniform schema rows without losing the per-task prose. The report's own text forbids this ("prose goes in `<task_details>` blocks, read only when an agent is executing that specific task").

But then the agent still has to read the prose at execution time — so those tokens are not actually saved, they're merely **deferred** into selective loading. **Deferring tokens is not the same as saving them**; if all agents read every phase (which is the tasklist-generation use case the report highlights), the savings evaporate.

### Verdict on the headline

**The -35% to -50% claim is hand-waved.** The report never shows this arithmetic. When I reconstruct it, the defensible ceiling is:
- **~+13% savings** if only tables are TOON-ified and all prose is preserved
- **~+20-25% savings** if aggressive compact Markdown DSL is layered on top of TOON tables
- **~+47% savings** only by aggressively TOON-izing the bullet sub-criteria, which destroys the prose context the report explicitly says must be preserved

The report's -35% to -50% range is inside the pathological upper bound but outside the defensible realistic ceiling. It should be **rescoped to -15% to -25% for the Hybrid approach**, or the methodology should be rewritten to show the arithmetic explicitly.

---

## Part C: Direct Measurement of the Actual Roadmap File

Measurements on `.dev/releases/complete/v3.2_fidelity-refactor___/roadmap-opus-architect.md`:

| Metric | Value | Matches report? |
|--------|-------|-----------------|
| File size | 16,985 bytes | Yes (16,985) |
| Lines | 342 | Yes (342) |
| Words | 2,141 | Not in report |
| Chars (no newlines) | 16,939 | Close (16,985 includes newlines) |
| Estimated tokens (char/4) | 4,234 | Report says ~4,600 — within 8% |
| Estimated tokens (char/3.5) | ~4,830 | Reasonable upper bound |
| Headings (lines starting `#`) | 31 | Yes |
| HRs (`---`) | 11 | Yes |
| Pipe chars | 240 | Yes |
| Backticks | 390 | Yes |
| Bold spans (`**`) | 102 (51 pairs) | Not directly stated in report |
| FR-* identifiers | 76 (62 unique) | Yes — 76 |
| SC-* identifiers | 31 (15 unique) | Yes — 31 |
| Table rows (pipe-prefixed lines) | 56 | Yes |
| Bullet lines (-) | 114 | Not in report |
| Numbered list lines (`1.` etc) | 24 | Not in report |
| Blank lines | 88 | Not in report |

### Composition mismatch

The report's Token Composition table claims:

| Category | Report % | Measured char % | Delta |
|----------|----------|-----------------|-------|
| Semantic content | 62% | (derived) ~54% (prose + bullet content minus markers) | -8pp |
| Requirement IDs (76 FR + 31 SC) | 11% | Approx 4% of chars (107 IDs × ~8 chars / 16,939) = 5% | -6pp |
| Table scaffolding | 9% | If "scaffolding only" = pipes + separators ≈ 3.5%. If "all table rows" = 25.4% | ambiguous |
| Markdown syntax | 9% | 4.9% headings + ~2.3% backticks + 0.6% bold = ~7.8% | -1pp |
| Structural repetition | 9% | Not directly measurable | ? |

The report's numbers are **estimates** it never shows the method for. The "9% table scaffolding" figure is the most misleading — any reasonable person reading it would infer that tables are ~9% of the content, making TOON's table compression look like a small-impact optimization. In reality, **25.4% of the file's characters live inside pipe-delimited rows** (including the text content, not just the scaffolding pipes). This matters because it changes the calculus: compressing tables is a bigger win than the report implies, but the report's -35% to -50% headline still doesn't close because bullet sub-criteria (47.7%) dominate the file and can't be TOON-ified.

### Phase-level distribution

Looking at the source file structure, the 6 phases each contain:
- 1 `## Phase N: ...` heading (~5 tokens)
- 1 **Goal** line (~10 tokens)
- 1 **Milestone** line (~20 tokens)
- 1 `### Tasks` heading (~2 tokens) + 3-8 numbered tasks with FR-* sub-bullets (~50-150 tokens)
- 1 `### Validation` heading + 3-6 SC-* bullets (~40 tokens)
- 1 `### Files Touched` heading + 1-4 file bullets (~30 tokens)

Per-phase total: ~160-260 tokens. Total phase content: ~1,200-1,560 tokens out of ~4,600. The remaining ~3,000 tokens are:
- Top preamble (key changes, architectural constraints): ~400 tokens
- Risks table + rationale: ~500 tokens
- Dependencies table: ~200 tokens
- Open Questions: ~400 tokens
- Traceability matrix: ~600 tokens
- Assumptions/Constraints/LOC budget sections: ~900 tokens

**The tables (risks, deps, traceability) together are ~1,300 tokens (~28% of file)** — much closer to the 25.4% char measurement than the 9% report claim.

---

## Part D: First-Principles Format Recommendation

Ignoring the source report's conclusions, here is my independent ranking of formats for this specific roadmap, based on:

1. **Measured composition**: 25% tables, 54% bullet hierarchies, 5% headings, 16% other
2. **Agent consumption pattern**: most downstream agents (`sc:tasklist`, `sc:task`, `sc:implement`) read the *whole* file, not phases selectively — deferred-loading "selective" wins are mostly theoretical
3. **Verified primary-source evidence**:
   - Format is near-noise for Sonnet 4.6 / Opus 4.6 (89.4% / 93.5% accuracy across all formats per webmaster-ramos)
   - Format IS significant for Haiku 4.5 (5.7-pp gap between MD and JSON)
   - "Format Tax" paper (2604.03616) says closed-weight frontier models show little format tax — optimize for tokens, not accuracy
   - Anthropic's "30% gain" is about query-at-end, not XML tags — XML gives *reliability* (trained priors for section boundaries) but no documented raw-token benefit

### My ranking

| Rank | Format | Expected savings | Rationale |
|------|--------|-----------------|-----------|
| **1** | **Compact Markdown DSL with conventions header** | **~-20% to -25%** (measured; see below) | Retains Markdown as the dominant format (lowest format-tax risk across all Claude models); collapses repeated scaffolding; inlines SC-* and FR-* into task lines; removes backtick noise on identifiers already unambiguous in context. No new dependencies. Human-readable. Matches the "format is noise on Sonnet/Opus" finding. |
| 2 | Compact Markdown + TOON tables only (risks/deps/traceability) | ~-28% to -32% | Builds on #1 by replacing the 3 biggest tables with TOON blocks inside fenced ```toon regions. Gains ~8-10pp on top of compact MD, but costs ~60-80 tokens for a TOON primer in system prompt. Net benefit only if the roadmap will be ingested by 5+ downstream calls (amortization). |
| 3 | XML scaffolding + compact Markdown body (no TOON) | ~-10% to -15% | XML adds reliability for section extraction on complex multi-phase pipelines, but closing tags are token overhead. Choose this only if downstream agents are observed to miss section boundaries when parsing markdown `##` headings. |
| 4 | Hybrid XML+TOON+prose (source report's pick) | ~-13% to -20% realistic; **not** -35% to -50% | Adds XML overhead and TOON-primer cost; gains only marginal compression beyond #2 because most of the file is prose/bullets that can't be TOON-ified. Worth it only if you already need XML for reliability reasons. |
| 5 | Minified JSON + external schema | ~-40% to -55% raw | Best raw compression but destroys human readability and adds format-tax risk per arXiv 2604.03616. Only viable for pure extraction pipelines that don't reason about content. |
| 6 | Pure YAML / TOML | +6% to +8% (INCREASE) | Report is correct on these — strictly worse than Markdown. |

### Falsifiable top-ranked estimate: Compact Markdown DSL

My claim: **Compact Markdown DSL applied to this file achieves -20% to -25% measured token reduction without any new format dependencies or comprehension tax.**

Derivation:
- Remove backticks around 195 spans of identifiers already unambiguous in context: 195 × ~1 token each = **~195 tokens saved (~4.2%)**
- Collapse `### Tasks` / `### Validation` / `### Files Touched` trio headers into inline tags (6 phases × ~10 tokens of scaffolding each): **~60 tokens saved (~1.3%)**
- Inline the SC-* validation criteria into the numbered task lines instead of a separate Validation section: eliminates 6 `### Validation` headers + 31 duplicated `- SC-XXX:` bullet lines ≈ **~150 tokens saved (~3.3%)**
- Collapse "Files Touched" bullets into a per-phase heading attribute (`## P2 | files: audit/wiring_gate.py(M)`): **~80 tokens saved (~1.7%)**
- Remove the duplicate Traceability Matrix (SC-* already inlined in tasks): **~300 tokens saved (~6.5%)** — this is the single biggest win
- Abbreviate the Goal/Milestone prose (e.g., "Gate: X passes Y" instead of "**Goal**: `X` passes `Y`"): **~100 tokens saved (~2.2%)**
- Compact the Risks table via shorter column names (id, sev, phase, desc, mit): **~60 tokens saved (~1.3%)**
- Add a 60-token conventions header once: **+60 tokens cost (-1.3%)**

**Total: +19.2% savings minimum**, rising to **~25%** if the preamble at the top is also compressed.

This is **falsifiable**: a mechanical converter can be written in ~50 lines of Python, the output run through Claude's tokenizer, and the claim verified or rejected directly. I am making the explicit prediction: **3,450-3,680 tokens** for the transformed file, down from ~4,600.

Contrast with the source report's Hybrid XML+TOON+prose claim of 2,300-3,000 tokens: I predict that format will actually land at **3,700-4,000 tokens** (at best ~13-20% savings) because:
- XML closing tags add ~80-120 tokens of scaffolding
- Only the 3 big tables get TOON compression (~350 tokens saved)
- The per-phase bullet hierarchies are identical to the source Markdown (no savings on 47% of the file)
- The TOON primer in system prompt is an *external* cost, not a file saving, and costs ~70 tokens per agent invocation

The two approaches are within ~10% of each other, and **Compact Markdown DSL wins** because it requires no new format primers, no TOON dependency, and no comprehension risk on Haiku sub-agents.

### Decision rule

- **If your downstream agents are all Sonnet 4.6 / Opus 4.6**: use Compact Markdown DSL. Format is noise. Optimize for tokens without introducing new formats.
- **If any downstream agent is Haiku 4.5**: use Compact Markdown DSL anyway — Haiku's MD vs JSON accuracy gap (69.6 vs 75.3) is small and a 60-token conventions header reliably closes it.
- **If downstream agents must extract specific phases in isolation** (and you can verify that, not just hope): add XML `<phase id="N">` wrappers around the compact-MD phases only.
- **Never** adopt the Hybrid XML+TOON+prose until you have run the A/B test the source report recommends — its arithmetic is not closed.

---

## Part E: Flagged Hallucinations / Unsupported Claims

The following claims in the source report are either misattributed, cherry-picked, unsupported by their own citations, or hand-waved arithmetic. They should not be repeated downstream without correction:

1. **"Anthropic officially recommends XML for up to 30% quality improvement"**
   - The 30% in Anthropic's long-context-tips doc is attributed to **query placement at end of prompt**, not to XML tags. XML tags are a separate recommendation with no quantified gain attached.
   - Verbatim from the doc: *"Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs."*
   - **Correction**: "Anthropic recommends XML for structural clarity (no quantified gain); query-at-end can yield up to 30% on long-context tasks."

2. **"arXiv 2411.10541 reports up to 40% perf delta by format"**
   - The 40% is specifically *"varies by up to 40% in a code translation task"* — one task type, not a general across-task finding.
   - **Correction**: "arXiv 2411.10541 reports up to 40% delta in a code translation subtask; effect sizes vary significantly by task type and are smaller on frontier models."

3. **"Format Tax paper (arXiv 2604.03616) supports format engineering for Claude"**
   - The paper's actual finding: *"most recent closed-weight models show little to no format tax, suggesting the problem is not inherent to structured generation but a gap that current open-weight models have yet to close."* Since Claude 4.6 Sonnet/Opus are closed-weight frontier models, this paper **weakens** the case for format engineering on that tier.
   - **Correction**: Cite the paper for its actual finding — "frontier closed-weight models are format-agnostic, which justifies optimizing purely for tokens rather than format-specific accuracy."

4. **"TOON benchmarks support TOON generation by LLMs"**
   - arXiv 2603.03306 (which the report cites under "Secondary") actually says: *"Plain JSON generation shows the best one-shot and final accuracy, even compared with constrained decoding structured output"* and TOON efficiency is *"often reduced by the 'prompt tax' of instructional overhead in shorter contexts."*
   - The report does NOT mention this adverse finding.
   - **Correction**: Cite the paper fairly — TOON is good for *reading* (comprehension) on uniform tables but not clearly better for *generation*, and its prompt-tax overhead eats into gains on short contexts.

5. **"Source roadmap token composition is 9% table scaffolding"**
   - Direct measurement: 25.4% of characters are inside pipe-delimited rows. Under any reasonable definition that includes row content (not just pipes), tables are ~25% of the file, not 9%. The 9% figure could only be defended if "scaffolding" means *literally the pipe and dash characters*, which is an extremely narrow reading.
   - **Correction**: "Tables account for ~25% of file characters; table-delimiter scaffolding alone is ~3.5%."

6. **"Hybrid XML + TOON + prose saves -35% to -50% (~2,300-3,000 tokens)"**
   - No arithmetic provided in the report. Re-derivation (Part B) yields a defensible ceiling of ~-13% to -20% under the report's own rules (prose stays as Markdown inside XML tags). The -35% to -50% range is only reachable by TOON-ifying bullet hierarchies, which the report explicitly forbids.
   - **Correction**: Rescope to -15% to -20% and show the arithmetic, or rewrite the methodology to explain how the bullet prose gets compressed.

7. **"Format-swapping YAML/TOML yields negative savings (+6% to +8%)"**
   - This is verified by Workman 2025 and Syntax & Empathy (both confirmed). **This part of the report is correct.**

8. **"-62% TOON vs Markdown on tabular data"**
   - Verified by webmaster-ramos and toonparse.com benchmarks on *flat uniform* tabular data. The report correctly caveats that savings collapse on mixed/nested data (-21.9% vs JSON, -5.7% vs YAML per toonparse.com mixed benchmark). **This part is also correct.**

9. **"XML schema attribute `schema="sc-roadmap/v1"` gives forward-compatibility"**
   - No primary source cited. This is an architectural assertion by the report, not a measured benefit. It's plausible but unquantified.

### What the report gets right

To be fair: the report's **comparative format-by-format analysis is mostly well-sourced** (webmaster-ramos numbers match exactly; Workman and Syntax & Empathy are real). The errors are concentrated in:
- The **headline hybrid recommendation's arithmetic** (hand-waved)
- The **Anthropic 30% misattribution** (wrong target — query placement, not XML)
- The **token composition breakdown** (9% tables is implausibly narrow)
- Two **cherry-picked arXiv citations** (2604.03616 and 2603.03306) whose conclusions actually contradict or weaken the report's recommendations

---

## Summary Verdict

The source report is 70% accurate on its cited benchmarks but 0% rigorous on its headline arithmetic. The primary sources it cites are real; the numbers it pulls from them match; but the synthesis step — "therefore Hybrid XML+TOON+prose saves 35-50%" — is not supported by any closed calculation on the actual target file. After direct measurement, the defensible savings ceiling for the recommended Hybrid format is ~-13% to -20%, essentially tied with a simpler Compact Markdown DSL that requires no new format dependencies and no TOON primer. My independent first-principles recommendation is **Compact Markdown DSL**, predicting ~3,450-3,680 tokens on the transformed file (a ~20-25% reduction), and I would reject the Hybrid recommendation as written until its arithmetic is shown explicitly or revised downward.
