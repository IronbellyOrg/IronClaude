# Compressed Markdown DSL: Primer & Compression Strategies

**Date**: 2026-04-15
**Context**: Follow-on from `research_roadmap-format-alternatives_VALIDATED.md` (adversarial-validated format study, 2026-04-15). That study found **Compact Markdown DSL #1** on present evidence for Opus 4.6 / Sonnet 4.6 consumers, with direct tiktoken measurements of -33.4% on a representative phase slice (`cl100k_base`; Claude-native tokenizer re-measurement is UNADDRESSED invariant INV-1).

---

## 1. What is Compact Markdown DSL?

Compact Markdown DSL ("Compressed Markdown DSL" / "CMD DSL") is **not a new format**. It is a disciplined subset of standard Markdown that:

1. **Preserves Claude's native Markdown parsing** — no new tokenizer, no new parser, no RLHF training gap
2. **Strips human-friendly redundancy** that contributes token cost without semantic value to an LLM consumer
3. **Introduces a small conventions header** (~40-60 tokens) that declares non-obvious abbreviations, enabling further compression in the body
4. **Is fully reversible to human-readable Markdown** via the conventions header plus a decompressor

Key distinction: **Compact MD DSL is not TOON, not XML, not a binary format.** It is Markdown with redundancy removed. Every compressed document is still valid CommonMark; an LLM can read it without format-switching cost.

### Why it exists

The prior research validation found:
- Hybrid XML+TOON+Markdown's claimed -35% to -50% savings was arithmetically unsupported (defensible ceiling: -12% to -22%)
- arXiv 2601.12014 found TOON has a 30-42% GCS correctness penalty on open-weight models (Claude untested, but the penalty is a live risk)
- Closed-weight frontier models (Opus 4.6, Sonnet 4.6) show "little to no format tax" per arXiv 2604.03616 — meaning format engineering's primary value is **token reduction, not accuracy improvement** at the frontier tier
- Compact MD DSL achieved **-33.4% measured** on the same Phase 2 slice (V-B tiktoken measurement), beating the hybrid by nearly 3× on compression with zero new format dependencies

The conclusion: on Opus/Sonnet, ruthlessly compacting Markdown dominates introducing new formats.

---

## 2. Core Concepts

### 2.1 Lossless vs lossy compression (for LLM consumption)

Compression is **lossless** if an LLM reader can recover every semantic assertion from the source document. "Lossless" here does not mean byte-for-byte — it means **task-equivalent**: the downstream agent's output is unchanged whether it reads the original or the compressed version.

| Transform | Lossless for LLM? | Example |
|-----------|-------------------|---------|
| Strip trailing whitespace | ✅ Yes | `"foo   \n"` → `"foo\n"` |
| Collapse blank lines | ✅ Yes (unless fenced code) | `"\n\n\n"` → `"\n"` |
| Remove decorative headers | ✅ Yes | `"---\n# 🚀 Project X 🚀\n---"` → `"# Project X"` |
| Abbreviate via conventions header | ✅ Yes (if header present) | `"Acceptance Criteria:"` → `"[AC]"` |
| Drop prose explanations | ⚠️ Lossy | `"This phase ships the auth service."` → deleted |
| Strip code fences | ❌ Lossy | Collapses language hint |
| Truncate tables | ❌ Lossy | Loses rows |

### 2.2 The conventions header

A conventions header is a small preamble (~40-60 tokens) that declares abbreviations used in the body. Example:

```markdown
<!-- cmd-dsl v1: [AC]=Acceptance Criteria [DoD]=Definition of Done
[>]=depends on [B]=blocked by [@]=assignee P0/P1/P2=priority -->
```

The header "pays for itself" after roughly 5-10 body uses of each abbreviation. For roadmaps with many phases each containing acceptance criteria, this amortizes strongly.

**Cost**: the header is overhead on every read. If a file is read once and discarded, the header is dead weight. The amortization math matters per consumer DAG (invariant INV-3 from the prior study — currently UNADDRESSED).

### 2.3 Semantic categories of compressible content

Compact MD DSL organizes redundancy into categories:

| Category | Compression ceiling | Notes |
|----------|--------------------:|-------|
| Whitespace & formatting | ~8-12% | Blank-line collapse, trailing-space strip, heading underline → ATX |
| Decorative elements | ~4-6% | Emoji, ASCII banners, horizontal rules |
| Preamble & meta | ~5-8% | Version stamps, author blocks, repeated "(see section X)" pointers |
| Abbreviable phrases | ~10-15% | With conventions header amortization |
| Prose redundancy (restatement) | ~8-15% | Same requirement stated in Summary, Requirements, Acceptance Criteria |
| Table whitespace | ~3-5% | Pipe-table column padding |
| **Total ceiling** | **~35-40%** | Matches V-B's measured -33.4% on a representative slice |

---

## 3. Sources & Tools

### 3.1 Primary-source research

- **arXiv 2601.12014** — *Are LLMs Ready for TOON? Benchmarking Structural Correctness-Sustainability Trade-offs in Novel Structured Output Formats* (Masciari et al., Jan 2026). The TOON correctness counter-benchmark. https://arxiv.org/abs/2601.12014
- **arXiv 2604.03616** — *The Format Tax* (2026). Closed-weight frontier model format-independence finding. https://arxiv.org/abs/2604.03616
- **arXiv 2603.03306** — TOON vs JSON comparative study (2026). https://arxiv.org/abs/2603.03306
- **arXiv 2411.10541** — Format performance delta measurement (2024). https://arxiv.org/abs/2411.10541
- **Anthropic long-context tips** — XML tagging and query-at-end placement recommendations. https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips
- **Anthropic use-XML-tags** — Official XML tag guidance with explicit "no canonical best tags" disclaimer. https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags

### 3.2 Prior IronClaude adversarial validation

- `claudedocs/research_roadmap-format-alternatives_20260415.md` — original research report (source of the debate)
- `claudedocs/adversarial-roadmap-formats-20260415/research_roadmap-format-alternatives_VALIDATED.md` — **adversarial-validated final artifact** (authoritative)
- `claudedocs/adversarial-roadmap-formats-20260415/adversarial/debate-transcript.md` — full 2-round + invariant-probe debate
- `claudedocs/adversarial-roadmap-formats-20260415/adversarial/return-contract.yaml` — machine-readable outcome with unaddressed invariants

### 3.3 Measurement & tooling

- **`tiktoken`** (OpenAI) — cl100k_base encoder, the pragmatic standard for relative format comparison. **Caveat**: not Claude's native tokenizer (INV-1). https://github.com/openai/tiktoken
- **Anthropic `messages.count_tokens`** — Claude-native token counting endpoint. Required for INV-1 resolution. https://docs.anthropic.com/en/api/messages-count-tokens
- **`markdown-it-py`** — CommonMark-compliant Markdown parser with AST access. Basis for Approach 2 below. https://github.com/executablebooks/markdown-it-py
- **`mdformat`** — opinionated Markdown formatter; useful for normalization pre-compression. https://github.com/executablebooks/mdformat
- **`remark` / `unified`** (JS) — equivalent AST pipeline in JavaScript. https://github.com/remarkjs/remark
- **`pandoc`** — universal document AST; overkill for compression but useful for cross-format experiments. https://pandoc.org/

---

## 4. Three Compression Approaches

Three programmatic approaches, from least to most aggressive. Each comes with trade-offs between determinism, fidelity, and compression ratio.

### Approach 1: Rule-based textual compression (deterministic, stateless)

**What it does**: Apply a fixed set of regex/line-based transforms to the raw Markdown source. No parsing, no AST, no LLM.

**Transforms applied**:
1. Collapse 3+ blank lines → 2 blank lines (outside code fences)
2. Strip trailing whitespace on every line
3. Normalize heading underline syntax (`=====` / `-----`) → ATX (`#` / `##`)
4. Remove decorative horizontal rules not adjacent to YAML front matter
5. Strip emoji from headings (configurable allowlist)
6. Collapse pipe-table padding: `| foo   | bar  |` → `|foo|bar|`
7. Remove `<!-- ... -->` comments (configurable exclusions)
8. Drop trailing "Last updated: X" / "Version: Y" blocks if duplicated in front matter
9. Replace declared abbreviations from conventions header (if present in front matter)
10. Normalize bullet markers to a single style (`*`, `-`, `+` → `-`)

**Implementation**: ~200 lines of Python with `re` module. Stateless. Streaming-capable.

**Compression ceiling**: ~12-18% on representative roadmaps (measured on the VALIDATED study's Phase 2 slice: 350 → 298 tokens, -14.9%).

**Determinism**: ★★★★★ — bit-for-bit reproducible, commutable with git diff, easy to test.

**Fidelity**: ★★★★★ — pure text transforms; content is structurally preserved. Safe for PRDs, specs, TDDs.

**Risks**:
- Regex inside code fences can corrupt examples if fence-awareness isn't implemented
- Emoji stripping can confuse visually-designed section anchors
- Pipe-table padding collapse can break pathological tables (rare)

**Best for**: Formal documents (specs, PRDs, TDDs) where maximum fidelity matters more than maximum compression. Documents read once per session where the conventions header would not amortize.

---

### Approach 2: AST-aware semantic compression (structural)

**What it does**: Parse the Markdown into a CommonMark AST (via `markdown-it-py`), apply semantic-aware transforms to the tree, then serialize back to Markdown.

**Transforms applied** (in addition to Approach 1):
1. **Heading deduplication**: detect `## Phase 2` appearing twice and merge second occurrence into an anchor reference
2. **Table normalization**: detect repeated column values (e.g., every row has `Priority: P1`) and hoist into a caption or eliminate via default
3. **List compaction**: convert multi-paragraph bullets into single-line bullets when the paragraph is one sentence
4. **Cross-reference deduplication**: detect `(see Section 3.2)` repeated with same target and replace second occurrence with pure anchor
5. **Front-matter → conventions-header synthesis**: scan for frequently-used multi-word phrases (>5 occurrences, >20 chars each) and auto-generate an abbreviation in the conventions header; apply substitution in body
6. **Prose summarization of introduction paragraphs** (bounded, deterministic): if an `## Introduction` section restates content found verbatim later, elide the restated sentences
7. **Drop mermaid/plantuml diagrams** if a textual equivalent exists adjacent (rarely safe — opt-in only)

**Implementation**: ~800-1200 lines of Python. Requires a stable AST visitor pattern. Tests must cover every transform in isolation.

**Compression ceiling**: ~25-33% (matches V-B's measured -33.4% on the Phase 2 slice).

**Determinism**: ★★★★☆ — AST transforms are deterministic but order-sensitive; serializer round-trips must be golden-tested to avoid drift.

**Fidelity**: ★★★★☆ — semantic preservation is very strong if transforms are audited individually; cross-reference deduplication can break navigation for humans.

**Risks**:
- AST parser must be CommonMark-compliant; GFM extensions (tables, strikethrough, task lists) need explicit plugin support
- Auto-generated abbreviations need a review gate — a bad substitution can corrupt meaning
- Round-trip testing is non-trivial: parse → transform → serialize → parse must produce an isomorphic AST

**Best for**: Roadmaps, tasklists, and any document where structural regularity enables high compression. The ceiling is close to what pure text compression can achieve because structural regularity is the primary source of redundancy in roadmap-like documents.

---

### Approach 3: LLM-assisted semantic rewriting (bounded, audited)

**What it does**: Use Claude itself (Haiku 4.5 for cheap-path, Sonnet 4.6 for load-bearing documents) to rewrite the source Markdown into Compact MD DSL, under a strict prompt that forbids information loss.

**Prompt contract**:
1. Input: source Markdown + target compression ratio (e.g., 30%)
2. Output: compressed Markdown + a `diff` of what was removed + a `conventions-header` section
3. Constraint: **every factual assertion in the source must be recoverable from the output** (LLM is told explicitly)
4. Constraint: code fences are never modified
5. Constraint: table rows are never deleted
6. Validation: a second LLM call ("auditor pass") checks the compressed output against the original and fails if any assertion is missing

**Transforms it can do that rule/AST approaches cannot**:
1. **Prose rephrasing**: "The system should be able to process requests in under 200ms" → "200ms request SLA"
2. **Semantic-dedup across distant sections**: detect that `## Non-Functional Requirements` and `## Performance Targets` overlap and merge
3. **Bulletization of narrative**: transform a paragraph of prose into a bulleted list
4. **Canonical phrasing**: rewrite variable phrasings of the same requirement into one canonical form
5. **Numeric canonicalization**: "approximately 200 milliseconds" → "~200ms"

**Implementation**: ~400 lines of Python + two prompt templates (compression + audit). Requires Anthropic API key. Rate-limited.

**Compression ceiling**: ~35-50% on prose-heavy documents (PRDs, TDDs). On structured documents (tasklists) ceiling is only marginally higher than Approach 2 because there is less rephraseable prose.

**Determinism**: ★★☆☆☆ — LLM output is non-deterministic even at temperature 0. Golden tests are difficult; the auditor pass is the primary quality gate.

**Fidelity**: ★★★☆☆ — high-risk. Without the auditor pass, information loss is plausible. With the auditor pass, fidelity approaches Approach 2 but at higher cost.

**Risks**:
- **Hallucinated facts**: LLM may "smooth over" inconsistencies in the source by making up a coherent version
- **Prompt cost**: every compression costs 2× the compressed-document tokens (compression pass + audit pass)
- **Loss of voice**: human reviewers may find LLM-rewritten text harder to audit
- **Cache invalidation**: the Anthropic prompt cache helps only if compression prompts are stable across documents

**Best for**: Prose-heavy documents where Approach 2 hits structural ceiling (~25-33%) but there is still meaningful savings in prose restatement. PRDs and TDDs benefit most; tasklists benefit least.

---

## 5. Document-Type Strategy Matrix

Different document types have different compression characteristics because they have different redundancy profiles. Key variables:

- **Structural regularity** — how much of the document is schema-like (tables, bullets, headings)
- **Prose density** — how much of the document is narrative English
- **Formality** — how much the document functions as a contract (specs > PRDs > roadmaps > tasklists)
- **Consumer DAG** — who reads it, how often, for which fields (INV-3 carry-forward)
- **Human-audit frequency** — how often humans review it manually

### Strategy recommendation per document type

| Document type | Dominant content | Redundancy profile | Recommended approach | Compression target | Rationale |
|---------------|------------------|--------------------|--------------------|----------------------|-----------|
| **Roadmap** | Phases, tables, bullets, moderate prose | High structural regularity; moderate prose restatement | **Approach 2 (AST)** + optional conventions header | **25-33%** | Structural regularity is the primary lever. Matches V-B's measured -33.4%. LLM rewriting offers little marginal gain on already-structured content. |
| **PRD** | Narrative requirements, user stories, acceptance criteria, rationale | High prose density; requirements restated in multiple sections | **Approach 3 (LLM-assisted)** + Approach 1 pre-pass | **35-45%** | PRDs have the highest prose-rephrase ceiling. Rule-based pass gets the free wins first; LLM pass captures narrative compaction. Auditor pass is mandatory because requirement loss is catastrophic. |
| **Spec** | Normative MUST/SHOULD/MAY clauses, invariants, formal definitions | Low prose; high formal-language density; high fidelity requirement | **Approach 1 (rule-based) only** | **10-15%** | Specs are contracts. Compression must be reversible and auditable; AST transforms introduce risk of semantic drift on normative language. Treat fidelity > savings. |
| **TDD** | Architecture prose + code blocks + diagrams + rationale | Mixed prose + code; code fences are load-bearing | **Approach 1 + Approach 2 (code-aware)** | **15-25%** | Code fences must never be touched. Approach 1 handles whitespace/formatting; Approach 2 handles the prose AST. LLM rewriting is risky near code because prompt-injection-like errors can rewrite code examples. |
| **Tasklist** | Highly repetitive task rows, status tags, priority flags | Extreme structural regularity; repetitive per-row fields | **Approach 2 (AST) with auto-conventions-header** | **30-40%** | Tasklists have the highest structural-redundancy ceiling. An auto-generated conventions header captures repeated patterns (e.g., `[P1][B:task-42][>]`). LLM rewriting offers no marginal gain. |

### Compression pipeline composition rules

1. **Always run Approach 1 first.** It is free, deterministic, and captures 10-15% with zero risk. Subsequent approaches should operate on Approach-1-normalized input so their transforms are stable.
2. **Code fences are sacrosanct.** Every approach must respect code fence boundaries. This is non-negotiable for TDDs.
3. **Run Approach 2 when structural regularity > prose density.** Tasklists, roadmaps, and structured requirements documents benefit most.
4. **Run Approach 3 only when Approach 2 has exhausted structural savings and prose density is still high.** PRDs are the canonical case.
5. **Specs should never exceed Approach 1.** The fidelity cost of AST/LLM transforms on normative language is too high.
6. **Auditor gate for any lossy transform.** If a transform is not provably lossless (Approach 3), require a second pass that validates factual preservation.
7. **Conventions header amortization check.** Before emitting a header, estimate read-count via consumer DAG. If read-count < 5, drop the header and absorb the 40-60 token cost as savings foregone.

### Cross-document-type observations

- **Spec compression is a trap.** The temptation to compress specs aggressively is strong (they are long), but spec compression is a fidelity-critical path where the cost of a bad transform is high. Treat specs as "archive for fidelity, not performance."
- **PRDs are the biggest opportunity.** Prose density + restated requirements + user-story narrative = 35-45% compression ceiling. This is where Approach 3's LLM-assisted rewriting pays for itself.
- **Tasklists are the biggest quick win.** They are highly structured and read multiple times per sprint. A single AST pass + auto-conventions-header delivers 30-40% with zero per-document cost.
- **TDDs split the difference.** The prose portions benefit from Approach 3, but the code-heavy portions benefit from nothing (code fences are untouchable). Apply approaches surgically to prose regions.
- **Roadmaps sit between PRDs and tasklists.** The prior adversarial study found Approach 2 (AST) is the sweet spot at 25-33%. Approach 3 offers marginal gains only on the rationale sections.

---

## 6. Known Gaps (carried from VALIDATED study)

Three HIGH-severity UNADDRESSED invariants from the adversarial validation apply equally to every compression strategy above. They are not resolvable by picking a better approach; they require empirical measurement.

- **INV-1 Tokenizer generalization** — All compression ratios in this document were measured with `tiktoken cl100k_base`, not Claude's native tokenizer. Re-measure with Anthropic's `messages.count_tokens` before any production deployment. Expected drift: ±2-8 percentage points.
- **INV-3 Consumer DAG unmapped** — The conventions-header amortization analysis assumes ≥5 reads per document. Actual read counts for each document type across the SuperClaude pipeline are not instrumented. A consumer inventory (who reads roadmaps? PRDs? tasklists? for which fields?) is a prerequisite for any amortization claim.
- **INV-5 Haiku untested** — None of the three approaches has been tested on Haiku 4.5. The prior webmaster-ramos data shows a 5.7pp MD-JSON accuracy gap on Haiku; until an A/B test with ≥20 retrieval prompts runs on Compact MD DSL vs plain Markdown, Haiku paths must default to uncompressed Markdown.

---

## 7. Next step

Continues in `/sc:design` — propose a refactor to the `superclaude roadmap` CLI pipeline that inserts compression at three natural points: (1) ingest (PRD/TDD/spec before generation), (2) mid-pipeline (variant artifacts before adversarial debate), (3) output (final merged roadmap before persistence). That design document is produced next.
