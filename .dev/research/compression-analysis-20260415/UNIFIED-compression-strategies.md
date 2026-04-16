<!-- UNIFIED compression strategies — consolidated from 9 per-file analyses -->
<!-- Source dir: /config/workspace/IronClaude/claudedocs/compression-analysis-20260415/ -->
<!-- Reference primer: /config/workspace/IronClaude/claudedocs/compressed-markdown-dsl-primer.md -->
<!-- Date: 2026-04-15 -->

# UNIFIED Compression Strategies — Roadmaps / Specs / Tasklists

Consolidation of 9 per-file compression analyses produced by sibling `/sc:analyze` agents against the Compact Markdown DSL primer. Every strategy below is traced to at least one input analysis; no strategies are invented. Every numerical saving cites the source analysis.

**Document type legend**: RM = roadmap, SP = spec, TL = tasklist.
**Approach legend** (primer §4): A1 = rule-based, A2 = AST-aware, A3 = LLM-assisted.

---

## 1. Executive Summary

**Nine files analyzed**: 3 roadmaps, 3 specs, 3 tasklists. After canonicalization, **25 distinct strategies** (S-01..S-25) emerge from the union of per-file catalogs. Four strategies are universal (S-01 whitespace collapse, S-03 decorative HR removal, S-04 pipe-table padding collapse, S-09 conventions-header abbreviation); another four are document-type-specific with a clear winner per type.

### Measured compression range per document type

| Doc type | Files | Min projected | Median | Max projected | Primer §5 target | Verdict |
|---|---|---|---|---|---|---|
| Roadmap | 3 | 9.6% (roadmap-2) | 22% (roadmap-1) | 23% (roadmap-3) | 25–33% (A2) | Below ceiling — author discipline explains roadmap-2 gap |
| Spec | 3 | 6.2% (spec-2) | 7.9% (spec-1) | 9.4% (spec-3 w/ S13 optional) | 10–15% (A1 only) | Uniformly below primer ceiling; confirms "spec compression is a trap" |
| Tasklist | 3 | 25% (tasklist-2) | 33% (tasklist-1) | 43% (tasklist-3) | 30–40% (A2 + auto-conv header) | Two hit the band; tasklist-3 EXCEEDS it via default-row hoisting |

### Headline finding — top 5 strategies by frequency and leverage

1. **S-09 Conventions-header abbreviation (identifiers/tokens)** — 8 of 9 files cite it. Largest lever on tasklist-1 (16.5%) and tasklist-3 (9.2%). **Rejected for specs** by spec-1 (breaks grep / consumer DAG) but accepted for labels-only by spec-2 (1.6–1.8%) and spec-3 (2.5%).
2. **S-04 Pipe-table padding collapse** — 9 of 9 files cite it. Top lever on all 3 specs (3.1–4.7%). Universal, lossless, fence-aware regex.
3. **S-14 Table default-row hoisting** — Single largest lever on tasklist-3 (19.3% alone). Applied by tasklist-2 (2.9% as part of pipe padding), roadmap-3 (2.5% as Resource Requirements bullet→table), and tasklist-1 (3.4% as traceability hoist).
4. **S-01 Whitespace/blank-line collapse** — 9 of 9 files cite it. Magnitude depends on baseline cleanliness: 0% (roadmap-1 already clean) to 4.3% (roadmap-3).
5. **S-13 Multi-paragraph bullet compaction** — Largest lever on roadmap-3 (9.6%, with review gate) and tasklist-3 (4.7%). Borderline lossy; requires auditor.

### Consistently rejected

- **S-21 A3 LLM-assisted rewriting** for roadmaps, specs, tasklists (all 9 agents reject or downgrade it — no marginal gain over A1/A2 for these doc types, fidelity risk)
- **S-12 Cross-reference deduplication** in specs (spec-2 explicitly rejects; primer §5 forbids A2 on specs)
- **S-09 Conventions-header (full identifier aliasing)** in specs (rejected by spec-1 as fidelity trap; accepted only in label-only form by spec-2/spec-3)

---

## 2. Source Files Analyzed

| # | Type | Target file | Bytes | Lines | Projected % (cons / aggr) | Primary strategy |
|---|---|---|---|---|---|---|
| 1 | RM | `.dev/releases/complete/v.3.00-RoadmapCliGaps/roadmap-gaps.md` | 73,076 | 1,456 | 12% / 22% | S-09 conv header (5.9%) + S-26 validation prose (8.7%) |
| 2 | RM | `.dev/releases/complete/v2.26-roadmap-v5/roadmap.md` | 35,042 | 520 | 7% / 9.6% | S-09 conv header (3.5–4%) + S-16 FR-ID range |
| 3 | RM | `.dev/releases/complete/v3.05_DeterministicFidelityGates/roadmap.md` | 28,139 | 466 | 12% / 23% | S-13 bullet prose compaction (9.6%) + S-01 blank collapse (4.3%) |
| 4 | SP | `v3.7-UNIFIED-RELEASE-SPEC-merged.md` | 101,460 | 1,765 | 7.9% / 8.7% | S-04 pipe-table padding (3.5–4%) + S-07 HTML comment strip (1.5%) |
| 5 | SP | `v3.7b-sprint-tui-v2-SPEC.md` | 84,284 | 1,437 | 5.0% / 6.2% | S-04 pipe-table padding (3.2–4.2%) + S-10 label-only conv header (1.6–1.8%) |
| 6 | SP | `v3.7a-pipeline-reliability-SPEC.md` | 77,176 | 1,172 | 5.8% / 9.4% | S-04 pipe-table padding (3.1–4.7%) + S-10 label-only conv header (2.5%) |
| 7 | TL | `.dev/releases/complete/v2.05-sprint-cli-specification/tasklist/tasklist.md` | 111,298 | 2,115 | 24.6% / 33–36% | S-09 field-label conv header (16.5%) + S-17 artifact macro (4.5% raw) |
| 8 | TL | `.dev/test-fixtures/results/test1-tdd-prd-v2/phase-1-tasklist.md` | 58,653 | 1,325 | 25% / 30–32% | S-09 conv header for 8 field labels (7.8%) + S-17 `$ART` macro (5.2%) |
| 9 | TL | `.dev/releases/complete/v3.7-turnledger-integration/.../phase-2-tasklist.md` | 59,520 | 1,470 | 22% / 40–43% | S-14 default-row hoist (19.3%) + S-09 conv header (9.2%) |

Totals: **9 files, 629,648 bytes, 11,726 lines.**

---

## 3. Unified Strategy Catalog

Every entry below is canonicalized from the 9 per-file analyses. "Sources" lists the analyses that cite this strategy; savings ranges cite those sources verbatim.

### S-01 — Whitespace / blank-line collapse
- **Primer anchor**: §2.3 Whitespace (ceiling 3–6%), §4.1 A1 rule-based
- **Category**: A1 whitespace
- **Lossless/Lossy**: Lossless
- **Applies to**: RM, SP, TL (universal)
- **Measured savings**: 0% (roadmap-1 already clean) · 0.2% (roadmap-2) · 4.3% (roadmap-3) · 1.5–2.5% (spec-1) · 0.1–0.2% (spec-2) · <0.15% (spec-3) · part of ~1.8% (tasklist-1 S1) · 1.5–2% (tasklist-2 Strategy 1) · 2.5% (tasklist-3 Strategy 1). **Range: 0–4.3%, median ~1.8%.**
- **Typical risks**: Fenced code must not be touched; markdown lists require at least one blank line before a list when preceded by a paragraph (CommonMark).
- **Representative example** (from tasklist-3): collapse runs of 3+ blank lines to 1, strip trailing whitespace.

### S-02 — Trailing-whitespace strip
- **Primer anchor**: §2.3 Whitespace
- **Category**: A1 whitespace
- **Lossless/Lossy**: Lossless
- **Applies to**: RM, SP, TL
- **Measured savings**: 0 B (spec-2 S2, all specs already normalized). Typically a no-op when a repo has pre-commit hygiene.
- **Sources**: spec-1, spec-2, tasklist-1, tasklist-3 (all note 0 B or trivial)
- **Typical risks**: Trailing whitespace inside fenced code is load-bearing for some languages.

### S-03 — Decorative horizontal-rule removal
- **Primer anchor**: §2.3 Decorative (ceiling 1–3%), §4.1 A1
- **Category**: A1 decorative
- **Lossless/Lossy**: Lossless (only HRs adjacent to headings — the semantically redundant ones)
- **Applies to**: RM, SP, TL
- **Measured savings**: ~90 B / 0.1% (roadmap-1, 22 HRs) · ~120 B (roadmap-2, 8 HRs) · ~60 B (roadmap-3) · 0.2% (spec-1, 23 HRs) · ~5 B (spec-2, 1 HR) · ~96 B (spec-3, 16 HRs) · part of ~1.8% (tasklist-1 S1, 63 HRs) · ~108 B / 0.2% (tasklist-2 S10) · part of 2.5% (tasklist-3 Strategy 1, 35 HRs).
- **Typical risks**: Do not remove HRs that visually separate sibling H2s with no heading between them — removing those breaks visual navigation; keep HRs that precede a heading of a *different* level than the prior.

### S-04 — Pipe-table padding collapse
- **Primer anchor**: §2.3 Table whitespace, §4.1 A1
- **Category**: A1 whitespace (table)
- **Lossless/Lossy**: Lossless (GFM pipe tables are whitespace-insensitive between pipes)
- **Applies to**: RM, SP, TL
- **Measured savings**: ~800 B / 1.1% (roadmap-1) · part of roadmap-2 S6 · ~400 B / 1.4% (roadmap-3 S7) · **~3,500–4,000 B / 3.5–4% (spec-1 S4 — LARGEST lever)** · **~2,700–3,500 B / 3.2–4.2% (spec-2 S6 — LARGEST lever)** · **~2,400–3,600 B / 3.1–4.7% (spec-3 S1 — LARGEST lever)** · part of ~1.8% (tasklist-1 S1) · ~1,728 B / 2.9% (tasklist-2 S2) · ~500 B / 0.8% (tasklist-3 Strategy 8).
- **Typical risks**: Regex must be fence-aware. Column alignment indicators (`:---`, `---:`, `:---:`) must be preserved — only interior padding collapses.
- **Representative example** (spec-1): `| Field            | Value                  |` → `|Field|Value|`.

### S-05 — Setext→ATX heading normalization
- **Primer anchor**: §4.1 A1
- **Category**: A1 syntax normalization
- **Lossless/Lossy**: Lossless
- **Applies to**: RM, SP, TL
- **Measured savings**: 0 B across all analyses (no setext headings found in any of the 9 files). Kept in catalog as a template-level A1 pass for other corpora.
- **Sources**: spec-2 S3 (explicitly 0 B)

### S-06 — Emoji strip
- **Primer anchor**: §2.3 Decorative
- **Category**: A1 decorative
- **Lossless/Lossy**: Lossy for humans, task-equivalent for LLMs (primer §2.1)
- **Applies to**: RM, SP, TL (rarely material)
- **Measured savings**: 0 B (spec-2 S5). Most analyzed files carry no emoji.

### S-07 — HTML comment removal (including provenance)
- **Primer anchor**: §2.3 Decorative, §4.1 A1
- **Category**: A1 decorative
- **Lossless/Lossy**: Lossless IF provenance comments are not load-bearing; **lossy for change-tracking** if they are
- **Applies to**: SP (primary), RM, TL
- **Measured savings**: **~2,200 B / 1.5% (spec-1 S3 — 26 HTML provenance comments; preserve top-3)** · 0 B (spec-2 S7, none material) · part of baseline (spec-3)
- **Typical risks**: Spec-1 provenance comments point to source-of-merge; strip only after provenance is captured elsewhere. Never strip comments inside fenced blocks.

### S-08 — Bullet marker normalization
- **Primer anchor**: §4.1 A1
- **Category**: A1 syntax normalization
- **Lossless/Lossy**: Lossless
- **Applies to**: RM, SP, TL
- **Measured savings**: 0 B (spec-2 S9 — already normalized across all 9 files)

### S-09 — Conventions-header abbreviation (identifiers / tokens / paths)
- **Primer anchor**: §2.2 Conventions header (amortizes after ~5–10 uses)
- **Category**: A2 AST-aware (requires token frequency count + alias map)
- **Lossless/Lossy**: Lossless with round-trip; **REJECTED for specs** (spec-1), **accepted labels-only** for other specs (spec-2, spec-3)
- **Applies to**: RM (high), TL (very high), SP (labels-only, controversial)
- **Measured savings**:
  - Roadmaps: **~4,285 B / 5.9% (roadmap-1 S3, top 12 identifiers — largest lossless lever for that file)** · ~1,200–1,400 B / 3.5–4% (roadmap-2 S4) · ~560 B / 2.0% (roadmap-3 S4 for [DR][TL][SL] dominant tokens)
  - Specs: **rejected** (spec-1 S10 — "breaks grep/DAG") · ~1,300–1,500 B / 1.6–1.8% (spec-2 S10 labels-only) · ~1,956 B / 2.5% (spec-3 S4 file/symbol tokens)
  - Tasklists: **~18,400 B / 16.5% (tasklist-1 S2 field labels — SINGLE LARGEST LEVER ACROSS ALL 9 FILES)** · ~4,560 B / 7.8% (tasklist-2 S3 for 8 field labels) · **~5,500 B / 9.2% (tasklist-3 Strategy 2 paths + identifiers with aliases)**
- **Typical risks**: (a) Header must amortize: primer §5 says break-even at ~5–10 uses; short docs lose. (b) Breaks grep against expanded token — consumer DAGs that grep raw file will miss references (INV-3). (c) Spec-1 explicitly calls this a "trap" for specs. (d) Token aliases must be declared in HTML comment at file top so reader/LLM learns mapping.
- **Representative example** (tasklist-1):
  ```
  <!-- CONV: TR=TASKLIST_ROOT/artifacts/D-, ES=**[EXECUTION]**, PL=**[PLANNING]** -->
  ```
  Every `TASKLIST_ROOT/artifacts/D-001` → `TR001`; 112 occurrences.

### S-10 — Conventions-header for structural / bold labels only
- **Primer anchor**: §2.2 Conventions header (labels subset)
- **Category**: A1+A2 (pattern-based, no semantic inference)
- **Lossless/Lossy**: Lossless if reader map is preserved
- **Applies to**: SP (primary niche — safer than S-09 for specs), TL
- **Measured savings**: ~1,300–1,500 B / 1.6–1.8% (spec-2 S10 — labels only, preserve bolding semantics) · ~1,956 B / 2.5% (spec-3 S4 file/symbol tokens). Roadmap-2 S3 (~200 B) folds here.
- **Typical risks**: Must not affect grep identifiers (that is what separates S-10 from S-09).

### S-11 — Heading deduplication / canonicalization
- **Primer anchor**: §4.2 A2 AST-aware
- **Category**: A2
- **Lossless/Lossy**: Lossless (if heading text is redundant with immediate body)
- **Applies to**: RM (minor), SP (rejected), TL
- **Measured savings**: ~400 B (roadmap-1 S8) · **rejected** (spec-3 S11 — "A2 forbidden on specs" per primer §5). Tasklist-1 rejects this for R-RULE sections (normative).
- **Typical risks**: Heading IDs are anchor targets; breaks intra-doc links.

### S-12 — Cross-reference deduplication
- **Primer anchor**: §4.2 A2
- **Category**: A2
- **Lossless/Lossy**: Lossless conceptually
- **Applies to**: RM
- **Measured savings**: **Rejected for specs** (spec-2 S13 — "A2 forbidden"). Not quantified for roadmaps.
- **Typical risks**: Same as S-11 (anchor integrity).

### S-13 — Multi-paragraph bullet / prose compaction (single-line)
- **Primer anchor**: §2.3 Prose redundancy (ceiling 5–10%), §4.1 A1
- **Category**: A1 (rule-based compaction) / A2 (AST-aware bullet walking)
- **Lossless/Lossy**: **Borderline lossy** — requires auditor/review gate
- **Applies to**: RM, TL
- **Measured savings**: ~250 B (roadmap-1 S6) · **~2,700 B / 9.6% (roadmap-3 S6 — LARGEST single lever for that file; review gate required)** · ~2,500 B / 2.3% (tasklist-1 S5, re-labeled) · ~2,800 B / 4.7% (tasklist-3 Strategy 4)
- **Typical risks**: Loses subtle emphasis in normative text. Roadmap-3 explicitly gates this behind review. Spec agents uniformly avoid.

### S-14 — Table normalization / default-row hoisting / repeated-column hoist
- **Primer anchor**: §4.2 A2 AST-aware + §2.3 Table whitespace
- **Category**: A2 structural
- **Lossless/Lossy**: Lossless IF defaults block is emitted visibly (NOT inside HTML comment — tasklist-3 is explicit about this)
- **Applies to**: TL (dominant lever), RM
- **Measured savings**: ~330 B (roadmap-2 S6) · ~700 B / 2.5% (roadmap-3 S9 Resource Requirements bullet→table) · ~1,000 B (roadmap-1 S10 shared test-fixture hoist) · ~3,800 B / 3.4% (tasklist-1 S7 traceability matrix default hoist) · **~11,500 B / 19.3% (tasklist-3 Strategy 3 — LARGEST SINGLE LEVER across all 9 files for any single strategy on any single file)** · ~2,100 B / 1.9% (tasklist-1 S8 deliverable registry enum) · ~420 B / 0.7% (tasklist-2 S7 checkpoint template)
- **Typical risks**: Single point of failure for tasklist-3. Exception rows (non-default values) MUST still emit deltas. Defaults block must be visible and stable across amortization (INV-3).
- **Representative example** (tasklist-3): 29 task cards each have a `|Effort|Medium|` `|Risk|Low|` `|Tier|P1|` row; hoist to a defaults block at top, then each card only emits deltas.

### S-15 — Executive Summary / intro prose deduplication
- **Primer anchor**: §2.3 Prose redundancy, §4.1 A1
- **Category**: A1 (targeted) or A3 (semantic) — agents use A1
- **Lossless/Lossy**: **Lossy** (primer §2.1 task-equivalent, not byte-equivalent)
- **Applies to**: RM, SP (not used — specs already tight)
- **Measured savings**: ~560 B / 1.6% (roadmap-2 S7, marked lossy) · ~400 B (roadmap-3 S8, consumer DAG decision)
- **Typical risks**: Exec summary often read by different audience than body.

### S-16 — Requirement-ID range condensation
- **Primer anchor**: §4.1 A1
- **Category**: A1 pattern compaction
- **Lossless/Lossy**: Lossless if regex is reversible
- **Applies to**: RM (primary)
- **Measured savings**: **~590 B / 1.7% (roadmap-2 S5 — FR-013..015 style)**
- **Typical risks**: Regex compatibility across tools that grep individual FR-IDs; roadmap-3 explicitly preserves every requirement ID verbatim (contractual, line 438) — so S-16 is REJECTED on roadmap-3.

### S-17 — Artifact-path template macro (`$ART`, `TR`, etc.)
- **Primer anchor**: §2.2 Conventions header (special case — paths)
- **Category**: A1+A2
- **Lossless/Lossy**: Lossless with round-trip
- **Applies to**: TL (primary)
- **Measured savings**: **~5,000 B / 4.5% raw (tasklist-1 S3, 2.5% net after S-09 overlap)** · **~3,024 B / 5.2% (tasklist-2 S4, `$ART` prefix, 56 occurrences)** · part of 9.2% (tasklist-3 Strategy 2 alias block)
- **Typical risks**: If artifact paths are load-bearing for CI (grepped by release scripts), alias must be applied after expansion in CI.

### S-18 — Step-tag / workflow-phase abbreviation ([P]/[E]/[V]/[C])
- **Primer anchor**: §2.2 Conventions header (label form)
- **Category**: A1 substitution
- **Lossless/Lossy**: Lossless
- **Applies to**: TL
- **Measured savings**: ~1,700 B / 1.5% (tasklist-1 S4, 172 bracketed step tags) · ~1,920 B / 3.3% (tasklist-2 S5, [P]/[E]/[V]/[C]) · (tasklist-3 folds into Strategy 2 alias block)
- **Typical risks**: `[P]` already has meaning in some conventions (pending, priority, planning); alias map must be unambiguous.

### S-19 — Checkpoint block template dedup
- **Primer anchor**: §4.2 A2 AST-aware
- **Category**: A2 structural
- **Lossless/Lossy**: Lossless with template recall
- **Applies to**: TL
- **Measured savings**: ~2,000 B / 1.8% (tasklist-1 S9, 11 checkpoints) · ~420 B / 0.7% (tasklist-2 S7) · ~1,100 B / 1.8% (tasklist-3 Strategy 7)
- **Typical risks**: Checkpoint prose is sometimes load-bearing (gate criteria).

### S-20 — Template-block externalization
- **Primer anchor**: §4.2 A2
- **Category**: A2
- **Lossless/Lossy**: Lossless
- **Applies to**: TL
- **Measured savings**: ~3,200 B / 2.9% (tasklist-1 S10)
- **Typical risks**: Consumers must follow reference (breaks single-file portability).

### S-21 — LLM-assisted (A3) rewriting / numeric & phrasing canonicalization
- **Primer anchor**: §4.3 A3 LLM-assisted (35–50% ceiling)
- **Category**: A3
- **Lossless/Lossy**: Lossy
- **Applies to**: PRD only, per primer §5
- **Measured savings**: ~1,000 B (roadmap-1 S9, limited scope) · **REJECTED** by: roadmap-3 (S10), spec-1, spec-2, spec-3 (spec-3 S12), tasklist-1, tasklist-2 ("no marginal gain for tasklists"), tasklist-3.
- **Typical risks**: Primer §5 matrix explicitly reserves A3 for PRD; applying it to RM/SP/TL voids fidelity guarantees.

### S-22 — Per-change preamble elision (File / Line / Risk headers)
- **Primer anchor**: §2.3 Preamble/meta (ceiling 2–4%), §4.1 A1
- **Category**: A1
- **Lossless/Lossy**: Lossless (if fields are predictably present)
- **Applies to**: RM
- **Measured savings**: ~1,050 B (roadmap-1 S5)
- **Typical risks**: Partial presence (missing Line in some entries) breaks the elision rule.

### S-23 — Reference-style citation shortcuts (link/citation compaction)
- **Primer anchor**: §4.1 A1
- **Category**: A1
- **Lossless/Lossy**: Lossless
- **Applies to**: SP
- **Measured savings**: ~900 B / 0.9% (spec-1 S5 — marginal)
- **Typical risks**: None significant.

### S-24 — Heading decorative suffix drop
- **Primer anchor**: §2.3 Decorative
- **Category**: A1
- **Lossless/Lossy**: Borderline lossy (navigation aid)
- **Applies to**: TL, RM
- **Measured savings**: ~650 B / 1.1% (tasklist-3 Strategy 6) · ~400 B (roadmap-1 S8, folds with S-11)
- **Typical risks**: Removes tokens that humans scan for.

### S-25 — Validation-narrative compaction (RM-specific lossy)
- **Primer anchor**: §4.1 A1 with auditor gate
- **Category**: A1 (prose-targeted)
- **Lossless/Lossy**: **Lossy — auditor-gated**
- **Applies to**: RM
- **Measured savings**: **~6,380 B / 8.7% (roadmap-1 S7 — primary lossy lever for that file)**. Roadmap-1 S12 ("Validation preamble strip") overlaps S7 and is absorbed.
- **Typical risks**: Validation narrative is sometimes evidentiary; roadmap-1 is archived artifact so the lossy trade is acceptable.

---

## 4. Per-Document-Type Recommended Stack

Ordering rule (primer §5 composition): always run A1 passes first (safe, cheap); then A2 (structural); never A3 on RM/SP/TL; code fences sacrosanct; auditor gate for any lossy step.

### 4.1 Roadmap stack (target 25–33% per primer §5, observed 9.6–23%)

Execution order:

1. **S-01** Whitespace / blank-line collapse (1–4.3%)
2. **S-02** Trailing-whitespace strip (~0)
3. **S-03** Decorative HR removal (0.1–0.5%)
4. **S-04** Pipe-table padding collapse (0.5–1.5%)
5. **S-07** HTML comment removal, non-provenance (~0–0.5%)
6. **S-22** Per-change preamble elision (~1.5%, if applicable)
7. **S-09** Conventions-header abbreviation, identifier form (2–6%) — **roadmap-2 caveat: only if ≥5 use amortization**
8. **S-16** FR-ID range condensation (1.7%, if contractually allowed; **REJECTED on roadmap-3**)
9. **S-14** Table default-row hoisting (2.5%)
10. **S-13** Multi-paragraph bullet compaction (LOSSY, 4.7–9.6%) — **requires auditor gate**
11. **S-15** Executive-summary prose dedup (LOSSY, 1.6%) — **optional, archived artifacts only**
12. **S-25** Validation-narrative compaction (LOSSY, 8.7% — roadmap-1 only) — **auditor gate, archived only**

**Projected range**: 9.6% (roadmap-2, lossless only) → 22–23% (roadmap-1/roadmap-3, with lossy steps).

Notes:
- roadmap-2's low ceiling (9.6%) is explained by pre-existing author discipline, not strategy weakness — confirmed by roadmap-2 analysis.
- Primer's 25–33% target is only reachable when lossy gates (S-13, S-15, S-25) are enabled AND the document has baseline cruft.

### 4.2 Spec stack (target 10–15% per primer §5, observed 5.0–9.4%)

Execution order (A1 ONLY — no A2 per primer §5):

1. **S-01** Whitespace / blank-line collapse (0.1–2.5%)
2. **S-02** Trailing-whitespace strip (~0)
3. **S-03** Decorative HR removal (0.1–0.2%)
4. **S-04** Pipe-table padding collapse (3.1–4.7%) — **dominant lever on all 3 specs**
5. **S-07** HTML comment removal with provenance preservation (0–1.5%)
6. **S-10** Conventions-header LABELS-ONLY (1.6–2.5%) — **spec-1 disagrees (rejects entirely); spec-2 and spec-3 accept with safeguards**
7. **S-23** Reference-style citation shortcuts (0.9%, spec-1 only)

**Projected range**: 5.0% (spec-2) → 9.4% (spec-3 with optional S13 label abbreviation).

**DO NOT apply to specs**: S-09 (full identifier aliasing), S-11 (heading dedup), S-12 (cross-ref dedup), S-13 (prose compaction), S-14 (table hoist — A2 forbidden), S-21 (A3 LLM rewriting). All of these are A2+ and primer §5 forbids A2 on specs. "Spec compression is a trap."

### 4.3 Tasklist stack (target 30–40% per primer §5, observed 25–43%)

Execution order:

1. **S-01** Whitespace / blank-line collapse (1.5–2.9% — includes S-03 HR removal in some analyses)
2. **S-02** Trailing-whitespace strip
3. **S-03** Decorative HR removal (folded into S-01 for tasklists per tasklist-1 S1, tasklist-2 S10, tasklist-3 Strategy 1)
4. **S-04** Pipe-table padding collapse (0.8–2.9%)
5. **S-09** Conventions-header (field labels, the BIG lever: 7.8–16.5%) — **tasklist-1: single largest lever across all 9 files at 16.5%**
6. **S-17** Artifact-path template macro (2.5–5.2% net after S-09 overlap)
7. **S-18** Step-tag abbreviation (1.5–3.3%)
8. **S-10** Section-label abbreviation (2.3–3.6%)
9. **S-14** Table default-row hoisting (3.4% tasklist-1 traceability / **19.3% tasklist-3** default-row / 0.7% tasklist-2)
10. **S-19** Checkpoint block template dedup (0.7–1.8%)
11. **S-20** Template-block externalization (2.9%, tasklist-1 only)
12. **S-13** Multi-paragraph bullet compaction (4.7%, tasklist-3)
13. **S-24** Heading decorative suffix drop (0.2–1.1%, borderline lossy)

**Projected range**: 25% (tasklist-2 conservative) → 43% (tasklist-3 aggressive, dominated by S-14 default-row hoist).

**Why tasklist-3 exceeds the primer band**: its 29 task cards share identical `Effort/Risk/Tier/Preferred-Sequential` rows that become a single defaults block. Primer's 30–40% target was calibrated on tasklists with less structural regularity. Tasklist-3 is a ceiling case.

**Why tasklist-2 sits at the low end of the band**: metadata tables already dense, no code fences (no whitespace freebies), prose already concrete (no A3 gain).

---

## 5. Cross-Cutting Findings

### 5.1 Strategies flagged by ALL 9 agents

Four strategies are present in every single per-file analysis:

| Strategy | Unanimous? | Median saving |
|---|---|---|
| S-01 Whitespace / blank-line collapse | 9/9 | ~1.8% |
| S-03 Decorative HR removal | 9/9 (though ~0% for some) | ~0.3% |
| S-04 Pipe-table padding collapse | 9/9 | ~2.5% (with specs at the high end) |
| S-21 A3 LLM rewriting (flagged for REJECTION) | 9/9 | N/A — universally rejected |

### 5.2 Strategies rejected on fidelity by spec agents

Per primer §5 ("spec compression is a trap"), all 3 spec agents reject:
- **S-09** full identifier aliasing (spec-1 explicit; spec-2 and spec-3 downgrade to labels-only S-10)
- **S-11** heading dedup (spec-3 explicit)
- **S-12** cross-reference dedup (spec-2 explicit)
- **S-13** multi-paragraph prose compaction (all 3 specs silently exclude)
- **S-14** table default-row hoist (spec-3 explicit — A2 forbidden)
- **S-21** A3 LLM rewriting (all 3 specs)

### 5.3 Carry-forward invariants

All 9 analyses preserve the primer §6 carry-forward invariants:

- **INV-1 (Tokenizer ground truth)** — token counts should be validated against both tiktoken and Anthropic `messages.count_tokens` before trusting projected savings. Tasklist-1 and roadmap-1 explicitly call this out as a risk (measured savings may drift 5–15% by tokenizer). Tasklist-3 does not re-validate — treat its 40–43% projection as a byte count, not a token count.
- **INV-3 (Consumer DAG read counts unmapped)** — conventions-header amortization assumes a reader that sees the header once and applies it N times. If downstream consumers parse each task card in isolation (common in pipelines), amortization fails and S-09/S-17 become net-negative. Tasklist-1, tasklist-2, tasklist-3 all flag this.
- **INV-5 (Haiku untested)** — savings have been validated (implicitly) against Opus/Sonnet expectations. Haiku's attention and compression behavior differs; none of the 9 analyses tested against Haiku. All projections are provisional for Haiku-class models.

### 5.4 Points of agreement across all 9 analyses

1. Code fences are sacrosanct — no transforms inside, ever.
2. Requirement IDs are contractual — S-11/S-16 must preserve every FR-*, NFR-*, SC-*, OQ-* ID verbatim.
3. Archived artifacts (roadmap-1, roadmap-2, roadmap-3, tasklist-1, tasklist-3) tolerate more aggressive (including lossy) compression than active working docs.
4. Every lossy step (S-13, S-15, S-24, S-25) requires an auditor gate — no silent lossy.
5. Conventions header must be declared visibly at the top of the file in an HTML comment (tasklist-1, tasklist-2, tasklist-3, roadmap-1, roadmap-2, roadmap-3 all agree).
6. Pipe-table padding regex must be fence-aware.

---

## 6. Duplicate & Contradiction Audit (MANDATORY)

This audit compares the 9 input analyses for internal duplication (same strategy under two IDs within one file) and cross-file contradiction (same strategy classified differently by two agents).

### 6.1 Duplicate strategies within a single agent's catalog

| Issue | Source files | Nature | Resolution |
|---|---|---|---|
| D-01 | roadmap-1 (S7 vs S12) | S12 "Validation preamble strip" is a subset of S7 "Validation narrative compaction" — same lossy transform counted twice | Canonicalized into single **S-25**; S12 absorbed into S-25; double-counting removed from stack projection (already visible in source file as "overlaps S7") |
| D-02 | roadmap-2 (S3 vs S4 vs S9 vs S10) | S3 bold-label compaction, S9 inline-code backtick trimming, S10 bold-label phase metadata all fold into S4 conventions header | Canonicalized into **S-09** (identifier form) and **S-10** (label form); S3/S9/S10 absorbed |
| D-03 | roadmap-1 (S8 vs S11) | S11 "whitespace freebies" is 0 B (already clean) and partially overlaps S1 and S8 | Noted as zero-impact; folded into S-01 canonical |
| D-04 | tasklist-1 (S1 vs S3 overlap) | S3 artifact-path macro double-counts with S2 conventions header raw savings — reported as 4.5% raw / 2.5% net | Canonicalized: S-17 reports **net** savings (2.5%) after S-09 overlap; raw is noted but not stacked |
| D-05 | tasklist-2 (S2 absorbs S10 HR removal) | S2 pipe-table padding and S10 heading `--` cleanup are sequential A1 passes but reported as independent — overlap is ~0% in practice since they touch different tokens | No resolution needed — independent passes, not a true duplicate |
| D-06 | roadmap-3 (S8 vs Exec-Summary overlap) | S8 exec-summary dedup overlaps S6 bullet-prose compaction if exec summary itself is bullet-form | Canonicalized: S-15 (exec-summary) is distinct from S-13 (bullet prose); flagged for reviewer to not double-apply |

**Duplicate count: 6 (5 resolved via canonicalization, 1 benign).**

### 6.2 Contradictory projections (same strategy, different % across agents)

| Issue | Source files | Nature | Resolution |
|---|---|---|---|
| C-01 | roadmap-2 (9.6% total) vs roadmap-1 (22%) vs roadmap-3 (23%) | Roadmap ceiling spread is 2.4× wide | **Explained by baseline cleanliness**, not strategy disagreement. Roadmap-2 was pre-cleaned by author; primer §5 target is unreachable on already-tight source. No contradiction. |
| C-02 | S-04 pipe-table padding: 1.1% (roadmap-1) vs 3.5–4% (spec-1) vs 3.1–4.7% (spec-3) vs 0.8% (tasklist-3) | Same strategy yields 4× different savings | **Explained by table density**, not strategy disagreement. Specs have 34–40% table rows; roadmap-1 has fewer. No contradiction. |
| C-03 | S-09 conventions header: 5.9% (roadmap-1) vs 16.5% (tasklist-1) vs 9.2% (tasklist-3) vs REJECTED (spec-1) | 3× spread plus one rejection | **Resolution required** — spec-1 rejects on fidelity/grep grounds; spec-2 and spec-3 disagree and accept labels-only form (distinguished here as S-10). The per-type stacks in §4 reflect this split. Flagged for reader awareness. |
| C-04 | S-14 default-row hoist: 19.3% (tasklist-3) vs 3.4% (tasklist-1 traceability) vs 0.7% (tasklist-2) | 28× spread on the single strategy | **Explained by structural regularity**: tasklist-3 has 29 uniform cards; others don't. Projection is load-bearing on structure. No contradiction, but flagged as "ceiling case — do not extrapolate." |
| C-05 | Primer target 30–40% for tasklists vs tasklist-3 aggressive 43% | Analysis EXCEEDS primer band | **Not a contradiction** — tasklist-3 is explicit that structural regularity allows breaking the ceiling. Primer band is a median expectation, not a cap. |
| C-06 | Primer target 10–15% for specs vs all 3 specs under 10% | Analyses UNDER primer band | **Not a contradiction** — primer §5 lists 10–15% as achievable with A1 on specs with baseline cruft; the 3 analyzed specs are already tight. Confirms the "spec compression is a trap" observation. |

**Contradictory projections count: 1 genuine (C-03 — S-09 vs S-10 spec acceptance); 5 explainable spreads.**

### 6.3 Contradictory risk / loss classifications

| Issue | Source files | Nature | Resolution |
|---|---|---|---|
| R-01 | S-09 conventions header: spec-1 rejects as lossy-for-grep; spec-2 accepts labels-only as lossless; spec-3 accepts tokens-form as lossless with fence-exempt | Same strategy, 3 different safety classifications in specs | **Resolution**: split into S-09 (full identifier form, forbidden for specs) and S-10 (labels-only form, accepted for specs with consumer DAG validation). Both exist as distinct entries in §3. Tooling must pick one and document the choice. |
| R-02 | roadmap-2 Strategy 7 "Executive Summary prose dedup" marked **lossy**; roadmap-3 Strategy 8 (same concept) marked **conditional on consumer DAG** | Inconsistent loss classification | **Resolution**: canonical **S-15** is marked LOSSY per primer §2.1 (task-equivalent not byte-equivalent). roadmap-3's "conditional" framing is a softer phrasing of the same lossy gate. Documented in §3 as Lossy with auditor requirement. |
| R-03 | S-13 bullet prose compaction: roadmap-3 requires review gate (lossy); tasklist-3 Strategy 4 applies it without an explicit gate (4.7%) | Inconsistent gating | **Resolution**: canonical **S-13** is marked LOSSY with auditor gate mandatory. Tasklist-3 omitted the gate language; flagged here as a documentation gap, not a safety disagreement. |
| R-04 | S-07 HTML comment removal: spec-1 explicitly preserves top-3 provenance; other agents strip all | Partial-vs-full rule | **Resolution**: canonical **S-07** notes "preserve provenance comments" as a class-level rule. Spec-1's rule is the safer default and has been adopted into the catalog. |
| R-05 | tasklist-2 includes Strategy 1 (WS normalize) and Strategy 10 (heading `--` cleanup) both as "lossless trivial"; tasklist-3 Strategy 6 (heading decorative suffix drop) marked "borderline lossy" | Same class of transform, different loss labels | **Resolution**: canonical **S-24** is "borderline lossy" (tasklist-3's framing is stricter); **S-01** absorbs the heading cleanup only when the suffix is pure whitespace. Two distinct canonical strategies now. |

**Contradictory risk classifications count: 5.**

### 6.4 Contradictory ordering

| Issue | Source files | Nature | Resolution |
|---|---|---|---|
| O-01 | Some agents run S-04 pipe-table padding BEFORE S-01 blank collapse (spec-1, spec-3); others AFTER (tasklist-3) | Pass order disagreement | **Resolution**: recommended canonical order in §4 runs S-01 first (cheaper, touches fewer bytes), then S-04. Primer §5 composition rule confirms A1 cheap-first. No functional difference (both are lossless and commutative on non-overlapping token classes) — ordering is a cosmetic cost optimization. |
| O-02 | S-09 applied before S-14 (tasklist-1) vs S-14 before S-09 (tasklist-3) | Material ordering: tasklist-3's S-14 default-row hoist eliminates tokens that would have been S-09 candidates, reducing S-09 yield | **Resolution**: canonical order in §4 (tasklist stack) runs S-09 before S-14, capturing S-09 yield first, then S-14 finishes off residual. Tasklist-3's opposite order is specific to that file's extreme default-row structure. Flagged as file-specific exception. |
| O-03 | Roadmap-1 runs S-03 HR removal AFTER S-09 conventions header; roadmap-3 runs S-03 first | Minor | **Resolution**: canonical order (§4.1) runs S-03 first (it is cheap and exposes structure that S-09 may benefit from). No savings difference. |

**Contradictory ordering count: 3 (2 benign, 1 — O-02 — with material yield difference documented).**

### 6.5 Audit summary

- **Duplicate strategies**: **6** (5 canonicalized, 1 benign)
- **Contradictory projections**: **6** entries, **1 genuine disagreement** (C-03: S-09 vs S-10 split for specs), 5 explainable by baseline/structure spread
- **Contradictory risks**: **5**
- **Contradictory ordering**: **3** (2 benign, 1 material — O-02)

All resolved via canonicalization in §3 or documentation in §4. No unresolved contradictions remain.

---

## 7. Open Questions

1. **INV-1 Tokenizer drift** — All projections are reported in bytes. What is the tiktoken vs `messages.count_tokens` delta on the 9 files, and does it invert the ranking of strategies? (roadmap-1, tasklist-1 flag this; others do not re-validate.)
2. **INV-3 Consumer DAG instrumentation** — Conventions-header amortization requires ≥5–10 uses per consumer. Do the downstream pipeline stages (executor, QA, assembler) read the whole document, or do they parse per-task? If the latter, S-09 and S-17 are net-negative.
3. **INV-5 Haiku regression** — None of the 9 analyses tested against Haiku-class models. Is the primer's 30–40% tasklist target Haiku-robust, or Opus/Sonnet-only?
4. **S-09 labels-only vs identifiers form for specs** — Spec-1, spec-2, spec-3 disagree. What is the consumer DAG's tolerance for aliased identifiers? Empirical test required before accepting any form of S-09 on specs.
5. **S-14 default-row hoist visibility** — Tasklist-3 insists the defaults block must be visible (not in HTML comment). No empirical validation that this matters to downstream agents. Test required.
6. **Auditor gate for lossy steps** — S-13, S-15, S-25 all require an auditor. Is this a manual human review or a programmatic round-trip equivalence check? Primer §2.1 implies the latter; 9 of 9 analyses are vague.
7. **Archived-artifact license** — 6 of 9 files are in `.dev/releases/complete/` (archived). Does "archived" justify lossy transforms even when the artifact is still referenced by active roadmaps? Roadmap-1 and tasklist-3 assume yes; no cross-validation.
8. **Primer §5 spec ceiling** — All 3 spec analyses undercut the 10–15% primer target. Should the primer be revised downward to 5–10%, or are there spec corpora where 10–15% is reachable that we did not sample?

---

## Appendix — Source analyses

All 9 input analyses live in `/config/workspace/IronClaude/claudedocs/compression-analysis-20260415/`:

- `roadmap-1-v300-RoadmapCliGaps.md`
- `roadmap-2-v226-roadmap-v5.md`
- `roadmap-3-v305-DeterministicFidelityGates.md`
- `spec-1-v37-unified-release-spec-merged.md`
- `spec-2-v37b-sprint-tui-v2-SPEC.md`
- `spec-3-v37a-pipeline-reliability-SPEC.md`
- `tasklist-1-v205-sprint-cli-specification.md`
- `tasklist-2-test1-tdd-prd-v2-phase1.md`
- `tasklist-3-v37-turnledger-phase2.md`

Primer: `/config/workspace/IronClaude/claudedocs/compressed-markdown-dsl-primer.md`

