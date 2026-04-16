# Compression Analysis: v3.05 Deterministic Fidelity Gates Roadmap

**Target file**: `/config/workspace/IronClaude/.dev/releases/complete/v3.05_DeterministicFidelityGates/roadmap.md`
**Primer reference**: `/config/workspace/IronClaude/claudedocs/compressed-markdown-dsl-primer.md`
**Analysis date**: 2026-04-15
**Strategy scope**: Compact Markdown DSL only (no TOON, no XML wrapping, no JSON conversion)

---

## 1. File Inventory

| Metric | Value |
|---|---|
| Path | `.dev/releases/complete/v3.05_DeterministicFidelityGates/roadmap.md` |
| Byte size | 28,139 bytes |
| Line count | 466 lines |
| Avg line length | ~60 bytes |
| Encoding | UTF-8, ASCII-only (no emoji) |

### Composition breakdown (by category per primer §2.3)

Categories and approximate share of total bytes — measured by line-sample inspection:

| Category | Approx bytes | % of file | Notes |
|---|---:|---:|---|
| YAML front matter | ~120 | 0.4% | 4-key block, lines 1-5 |
| ATX headings (`#` → `####`) | ~1,400 | 5.0% | ~38 headings; consistent ATX style already |
| Prose paragraphs | ~6,800 | 24% | Executive summary, goals, debate-resolution blockquotes, exit-criteria restatements |
| Bullet lists (milestones) | ~12,500 | 44% | Dominant content: ~180 bullets across 25+ milestones |
| Tables | ~3,900 | 14% | 4 tables: Risk (8 rows), OQ (5 rows), SC (6 rows), Timeline (6 rows), Dependencies (inline) |
| Blockquote notes | ~1,100 | 4% | 3 `> **Note/Debate resolution**` blocks |
| Horizontal rules / decorative `---` | ~60 | 0.2% | 7 separator rules between phases + section splits |
| Blank lines / whitespace | ~1,900 | 7% | Generous spacing between milestones, phases, sections |
| Bold label decorations (`**Goal**`, `**Requirements**`, `**Gate X**`) | ~400 | 1.4% | Repeats once per phase (6 phases × 4-5 labels) |

### Repeated-pattern inventory (conventions-header candidates)

The file is extremely regular. Phrases that recur ≥5 times, ordered by frequency:

| Phrase | Approx count | Approx byte cost |
|---|---:|---:|
| `DeviationRegistry` / `deviation registry` | ~12 | 216 |
| `TurnLedger` | ~11 | 121 |
| `structural_high_count` | ~8 | 168 |
| `convergence_enabled` | ~9 | 171 |
| `semantic layer` / `semantic_layer.py` | ~14 | 250 |
| `handle_regression()` | ~6 | 120 |
| `regression validation` | ~7 | 154 |
| `source_layer` | ~6 | 72 |
| `Acceptance criteria` → already spelled "Exit criteria" | ~6 headings | 84 |
| `convergence.py` | ~6 | 78 |
| `remediate_executor.py` | ~4 | 80 |
| `structural checkers` / `structural findings` | ~13 | 280 |
| `spec_parser.py` | ~5 | 75 |
| `byte-identical` | ~4 | 56 |
| `commit f4d9035` | ~3 | — (<5 threshold) |
| `run-to-run memory` | ~5 | 85 |
| `FR-`, `NFR-`, `SC-`, `OQ-`, `G-`, `D-` ID prefixes | ~80 refs | Preservation REQUIRED per §"Requirement-ID Preservation Guidance" |

Two strong structural patterns (primer §4.2 AST-aware) are also present:

1. **Per-phase preamble block** — every phase begins with the same four-line template: `**Goal**: …`, `**Requirements**: …`, `**Gate X — …**`, blank, then `#### Milestone`. This preamble shape recurs 6× and its labels carry no per-phase semantic weight.
2. **Per-phase exit block** — every phase ends with `**Exit criteria**:` bullets, `**Timeline**:` one-liner, and a decorative `---`. Also recurs 6×.

### Content notes relevant to compression safety

- **No code fences**. There are zero fenced code blocks in the document. Approach 1 fence-awareness is therefore not load-bearing for this file (primer §4.1 Risks #1). Regex transforms run without fence-escape plumbing.
- **Requirement-ID preservation is contractual** (line 438: "Preserve exact IDs … Do not alias or renumber IDs"). This is a hard lower bound on abbreviation aggressiveness — no abbreviation may alias an `FR-`/`NFR-`/`SC-`/`OQ-` token.
- **Table column formatting is already compact**. Pipe cells have minimal padding (`| 1 |`, `| HIGH |`) — the padding-collapse transform (primer §4.1 transform 6) will yield small gains here.
- **No emoji in headings**. The emoji-strip transform (primer §4.1 transform 5) has zero applicable targets.
- **No duplicate headings**. Each `## Phase N` appears once; primer §4.2 transform 1 (heading dedup) does not apply.
- **Cross-reference density is low**. The file has only a few `(see …)` pointers; primer §4.2 transform 4 yields negligible gains.

---

## 2. Strategies Identified

Each strategy cites its primer source. Approaches from primer §4 and categories from primer §2.3 are the grounding.

### Strategy 1 — Blank-line collapse & trailing-whitespace strip (primer §4.1 transforms 1-2; §2.3 "Whitespace & formatting")

**What**: Collapse any run of ≥3 blank lines to a single blank line and strip trailing spaces. No code fences exist, so this is fence-unconditional.

**Before** (lines 27-31):
```
**Estimated duration**: 32–45 working days (phase-specific ranges below).

---

## Phased Implementation Plan
```

**After**:
```
**Estimated duration**: 32–45 working days (phase-specific ranges below).
---
## Phased Implementation Plan
```

**Estimated saving**: ~1,200 bytes (~4.3%). The file has generous breathing-room between milestones and phases — roughly 90 blank lines can collapse to 30.

**Lossless**: Yes (primer §2.1 table row 2).

**Risks**: None for this file. The reader-visual grouping provided by the blank lines is load-bearing only for humans; LLM parsing is unaffected.

---

### Strategy 2 — Decorative horizontal-rule removal (primer §4.1 transform 4; §2.3 "Decorative elements")

**What**: Remove the seven `---` separator rules between phases and between the top-level sections. The YAML front-matter `---` fence pair (lines 1 and 5) must be preserved.

**Before** (lines 86-88):
```
**Timeline**: 4–5 days

---

### Phase 2: Structural Checkers & Severity Engine (Days 6–12)
```

**After**:
```
**Timeline**: 4–5 days
### Phase 2: Structural Checkers & Severity Engine (Days 6–12)
```

**Estimated saving**: ~60 bytes direct + ~60 bytes from the blank lines around the rules (already counted in Strategy 1). Net new: ~60 bytes (~0.2%). Small but free.

**Lossless**: Yes (primer §2.1 table row 3) — the heading level is unchanged so no grouping is lost.

**Risks**: Must NOT touch the YAML frontmatter fence. A fence-aware regex (match `---` only when not immediately preceded/followed by a YAML key line) is trivial since the frontmatter is the first five lines only.

---

### Strategy 3 — Bold-label compaction in per-phase preambles (primer §4.2 transform 5 "front-matter → conventions-header synthesis"; §2.3 "Preamble & meta")

**What**: The four labels `**Goal**:`, `**Requirements**:`, `**Gate X — Y Certified**:`, `**Timeline**:`, `**Exit criteria**:` repeat 6× (once per phase). Declare them in a conventions header and shorten the in-body forms.

**Conventions header** (added once, ~180 bytes including the HTML comment):
```
<!-- cmd-dsl v1: [G]=Goal [R]=Requirements [GATE]=Gate [EX]=Exit criteria
[T]=Timeline [DR]=Debate resolution [AC]=Acceptance criteria -->
```

**Before** (lines 31-38):
```
### Phase 1: Foundation — Parser, Data Model & Interface Verification (Days 1–5)

**Goal**: Establish the parsing infrastructure and data models that every downstream component depends on. Verify interface contracts for cross-phase dependencies.

**Requirements**: FR-2, FR-5, FR-3 (partial: severity rule table definition), FR-6 (partial: Finding dataclass extension), FR-7.1 (interface contract definition)

**Gate A — Parser Certified**: Exit when FR-2 + FR-5 pass real-spec validation.
```

**After**:
```
### Phase 1: Foundation — Parser, Data Model & Interface Verification (Days 1–5)
[G]: Establish parsing infrastructure and data models every downstream component depends on. Verify interface contracts for cross-phase dependencies.
[R]: FR-2, FR-5, FR-3 (partial: severity rule table), FR-6 (partial: Finding extension), FR-7.1 (interface contract)
[GATE A — Parser Certified]: Exit when FR-2 + FR-5 pass real-spec validation.
```

**Estimated saving**: Each per-phase preamble saves ~30 bytes × 6 phases = ~180 bytes; each per-phase exit block (Exit criteria + Timeline) saves ~25 bytes × 6 = ~150 bytes. Total ~330 bytes. Minus the ~180-byte header → **net ~150 bytes (~0.5%)**.

**Lossless**: Yes, provided the conventions header is retained (primer §2.1 row 4, §2.2).

**Amortization check** (primer §2.2): Labels appear ≥12 × (6 phases × 2 blocks). The amortization floor is met. However, the amortization is MARGINAL for this file because the labels are short to begin with — this strategy's real value is symbolic (unlocking Strategy 4) more than direct byte savings. Keep only if Strategy 4 is also applied.

**Risks**: `[GATE]` could collide visually with `[AC]`-style bracket IDs; use `[G!]` or keep `[GATE]` spelled out. Do not abbreviate requirement IDs (`FR-`, etc.) — explicit constraint from file line 438.

---

### Strategy 4 — Abbreviation of dominant long tokens (primer §2.3 "Abbreviable phrases"; §4.2 transform 5)

**What**: Declare abbreviations for the highest-frequency multi-character tokens in the file via the same conventions header as Strategy 3.

**Conventions header additions**:
```
[DR]=DeviationRegistry [TL]=TurnLedger [SL]=semantic layer
[SC*]=structural checkers [CV]=convergence [HR]=handle_regression()
[SHC]=structural_high_count [CE]=convergence_enabled
```

**Before** (lines 138-146):
```
#### Milestone 3.1: Deviation Registry Extension (FR-6)
- Extend existing `convergence.py` (lines 50–225) `DeviationRegistry` class
- Add `source_layer` field to findings: `"structural"` or `"semantic"`
- Implement stable ID computation: `(dimension, rule_id, spec_location, mismatch_type)`
- Implement cross-run comparison: match by stable ID, mark FIXED when not reproduced
- Add run metadata: `run_number`, `timestamp`, `spec_hash`, `roadmap_hash`, `structural_high_count`, `semantic_high_count`, `total_high_count`
- Implement spec version change detection → registry reset
- Handle pre-v3.05 registries: default missing `source_layer` to `"structural"` (Risk #7 — conservative, treats unknowns as structural for monotonic progress)
- Accept `ACTIVE` as valid status alongside `PENDING`
```

**After**:
```
#### M3.1: [DR] Extension (FR-6)
- Extend `convergence.py` (50-225) `[DR]` class
- Add `source_layer`: `"structural"` or `"semantic"`
- Stable ID: `(dimension, rule_id, spec_location, mismatch_type)`
- Cross-run match by stable ID; mark FIXED when not reproduced
- Run metadata: `run_number, timestamp, spec_hash, roadmap_hash, [SHC], semantic_high_count, total_high_count`
- Spec version change → registry reset
- Pre-v3.05: default missing `source_layer` to `"structural"` (Risk #7 — treats unknowns as structural for monotonic progress)
- Accept `ACTIVE` as valid alongside `PENDING`
```

**Estimated saving**: The 8 abbreviations combined are used ~70 times. Average savings ~10 bytes per substitution = ~700 bytes gross. Header cost ~140 additional bytes. **Net ~560 bytes (~2.0%)**.

**Lossless**: Yes, provided header is retained and the downstream consumer is primed on `cmd-dsl v1` syntax (primer §2.1 row 4).

**Risks**:
- **ID collision with requirement prefixes is a real danger**. `[SC*]` is chosen precisely because `SC-1` through `SC-6` are first-class requirement IDs (line 438). Collision-safe alternatives: `[SCh]`, `[STC]`.
- Abbreviating `DeviationRegistry` → `[DR]` collides conceptually with "Debate resolution" if both are used. Choose one: recommend `[DR]=DeviationRegistry`, spell out debate resolution in the blockquote lines (only 3 uses).
- The conventions header must be inside an HTML comment so CommonMark parsers treat it as metadata, not body prose.

---

### Strategy 5 — Blockquote `> **Note/Debate resolution**:` label compaction (primer §4.2 transform 3 "list compaction"; §2.3 "Preamble & meta")

**What**: The three blockquote blocks use the same verbose label pattern. Treat them as a single-category annotation.

**Before** (lines 74, 155-156, 174-175):
```
> **Note on data model timing**: The 19 canonical mismatch types are specified in the requirements document. If checker implementation in Phase 2 reveals additional types, `SEVERITY_RULES` must raise `KeyError` on unknown combinations — this is the designed failure mode, not a front-loading defect. Add new entries when discovered.
```

and

```
> **Debate resolution**: FR-10 is placed here per Haiku's argument that run-to-run memory is a registry capability, not a semantic capability. The registry stores and retrieves prior findings; the semantic layer merely reads this data. End-to-end validation of memory in semantic prompts occurs in Phase 4.
```

**After**:
```
> [NOTE] 19 canonical mismatch types are in requirements. If Phase 2 checkers reveal more, `SEVERITY_RULES` raises `KeyError` on unknown combinations — designed failure mode, not front-loading defect. Add entries when discovered.
```

and

```
> [DR-NOTE] FR-10 placed here per Haiku: run-to-run memory is a registry capability, not semantic. Registry stores/retrieves prior findings; [SL] reads them. E2E validation in Phase 4.
```

**Estimated saving**: The three blocks together are ~850 bytes. Compacted versions ~550 bytes. **Net ~300 bytes (~1.1%)**.

**Lossless**: ✅ for factual assertions. ⚠️ mildly lossy for *tone* — the compacted forms drop hedging phrases ("— this is the designed failure mode, not a front-loading defect" shortens to "— designed failure mode, not front-loading defect"). Downstream LLM consumers extract the same facts; human reviewers lose voice.

**Risks**: Classification tension — this crosses from primer §4.1 (rule-based, lossless) into primer §4.2 (AST-aware, near-lossless). If fidelity >> savings for this file, SKIP this strategy. The $300 savings is small.

---

### Strategy 6 — Bullet-list prose compaction in milestones (primer §4.2 transform 3 "list compaction")

**What**: Many milestone bullets are imperative sentences like "Implement X for Y with Z" that include determiners ("the", "a", "an") and verb-prefix noise ("Implement", "Define", "Add") that are already implied by bullet-context. AST-aware milestone bullets drop imperative verbs and articles.

**Before** (lines 49-57):
```
- Implement YAML frontmatter extraction with graceful degradation (`ParseWarning` on malformed input)
- Implement markdown table extraction keyed by heading path
- Implement fenced code block extraction with language annotation
- Implement requirement ID regex extraction: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`
- Implement Python function signature extraction from fenced blocks
- Implement `Literal[...]` enum value extraction
- Implement numeric threshold expression extraction (`< 5s`, `>= 90%`, `minimum 20`)
- Implement file path extraction from manifest tables (Sec 4.1, 4.2, 4.3)
```

**After**:
```
- YAML frontmatter: extract w/ graceful degradation (`ParseWarning` on malformed)
- Markdown tables: extract keyed by heading path
- Fenced code blocks: extract w/ language annotation
- Requirement IDs: `FR-\d+\.\d+`, `NFR-\d+\.\d+`, `SC-\d+`, `G-\d+`, `D\d+`
- Python function signatures from fenced blocks
- `Literal[...]` enum values
- Numeric thresholds (`< 5s`, `>= 90%`, `minimum 20`)
- File paths from manifest tables (§4.1-4.3)
```

**Estimated saving**: Across ~180 bullets, average savings ~15 bytes per bullet from dropping `Implement`/`Define`/`Add`/`Handle`/articles and collapsing parentheticals. ~180 × 15 = **~2,700 bytes (~9.6%)**. This is the single largest saving available in this file.

**Lossless**: ✅ for factual content. Bullet-context already supplies imperative mood; dropping "Implement" does not change the claim being made. Primer §4.2 transform 3 supports this transform when multi-clause bullets are "one sentence".

**Risks**:
- **Highest risk transform in this plan**. If applied incorrectly a bullet can lose its subject. Example: "- Run metadata includes ledger snapshot in convergence mode" → compacted to "- Run metadata: ledger snapshot [CE]" is fine, but "- Ensure checkers receive only relevant `SpecSection` objects per dimension-to-section mapping (consuming FR-5)" → "- Checkers receive relevant `SpecSection` per dimension-to-section mapping (consuming FR-5)" is safe only if "Ensure" is correctly understood as structural scaffolding, not a verification requirement.
- Requires **human or LLM review gate** before shipping. Pure regex cannot do this safely (it must inspect each bullet). Sits in primer §4.2 territory with a manual audit.
- Must be applied BULLETWISE with diff review; do not apply as a blind regex.

---

### Strategy 7 — Table cell compaction (primer §4.1 transform 6; §2.3 "Table whitespace")

**What**: Collapse pipe-table padding and abbreviate verbose cells in the four tables.

**Before** (lines 359-368, Risk table excerpt):
```
| # | Risk | Severity | Phase | Mitigation |
|---|------|----------|-------|------------|
| 1 | Spec parser robustness — real specs deviate from template | HIGH | Phase 1 | Graceful degradation with `ParseWarning`; validate against real spec, not synthetics only. Parser is critical path (FR-2 → FR-1 → FR-4 → FR-7). |
```

**After**:
```
|#|Risk|Sev|Phase|Mitigation|
|-|-|-|-|-|
|1|Spec parser robustness — real specs deviate from template|H|P1|Graceful degradation w/ `ParseWarning`; validate vs real spec. Critical path (FR-2→FR-1→FR-4→FR-7).|
```

**Estimated saving**: The file has 4 narrow tables (~25 rows combined). Pipe padding is already tight, so savings mostly come from abbreviating `Severity` → `Sev`, `Phase 1` → `P1`, `HIGH`/`MEDIUM`/`LOW` → `H`/`M`/`L`, and prose compaction inside the Mitigation and Open Question columns. **Net ~400 bytes (~1.4%)**.

**Lossless**: ✅ the abbreviations must be in the conventions header (primer §2.2). `H`/`M`/`L` are the same three-valued enum on every row; declaring them once is safe.

**Risks**:
- Two tables use the `Phase N` column as a cross-reference target; truncating to `P1` is fine if primer §2.2 header declares it.
- Do NOT compact `SC-1` through `SC-6` in the Success Criteria table — requirement-ID preservation is contractually required.

---

### Strategy 8 — Executive-summary prose dedup against phase bodies (primer §4.2 transform 6 "Prose summarization if introduction restates content found verbatim later"; §2.3 "Prose redundancy (restatement)")

**What**: The Executive Summary (lines 9-26) and the Phased Implementation Plan body restate several facts: "TurnLedger consumed from sprint/models.py without modification", "convergence ≤3 runs", "legacy mode byte-identical to f4d9035", "structural checkers are pure functions". The primer explicitly names this pattern as compressible if the restated sentences are verbatim or near-verbatim.

**Before** (executive-summary line 16):
```
- TurnLedger is consumed from `sprint/models.py` without modification — cross-module import is conditional and convergence-only
```
paired with line 228 in Phase 5:
```
- Import `TurnLedger` from `superclaude.cli.sprint.models` (conditional, convergence-only)
```

**After**: Keep only the phase-body version (which carries operational context); delete the exec-summary bullet. Alternatively, keep exec-summary as a forward-reference with `(see Phase 5)` dropped per primer §4.2 transform 4.

**Estimated saving**: ~4 exec-summary bullets are verbatim-equivalent restatements. ~400 bytes of exec-summary prose can be elided. **~400 bytes (~1.4%)**.

**Lossless**: ⚠️ conditional. For LLM consumers running a single-pass read, the exec summary is redundant since the phase bodies contain the same assertions. For human readers doing a skim, the exec summary is load-bearing navigation. This is the classic **consumer DAG question** (primer INV-3, §2.2 amortization check) — if the consumer is always an LLM that reads the whole file, the transform is lossless; if humans skim, it is lossy.

**Risks**:
- **This strategy interacts with primer §5 "Roadmap" row**: the recommended target for roadmaps is 25-33% via Approach 2 AST-aware. This exec-summary dedup is the single largest Approach-2 win in this file because structural regularity (the other main lever) has already been exploited by Strategies 1-7.
- Requires explicit consumer DAG decision before shipping.

---

### Strategy 9 — Resource Requirements section compaction (primer §4.2 transform 2 "table normalization … hoist into caption or eliminate via default")

**What**: Lines 384-420 ("Resource Requirements & Dependencies") is a 7-sub-section list where each line is of the form `**NAME** (path) — description. Methods: a, b, c`. Convert to a compact table.

**Before** (lines 385-387):
```
1. **TurnLedger** from `superclaude.cli.sprint.models` — budget accounting. Methods: `debit()`, `credit()`, `can_launch()`, `can_remediate()`, `reimbursement_rate`
2. **ClaudeProcess** — LLM subprocess execution for debate agents, validation agents, patch application
3. **Click CLI** — `--allow-regeneration` flag addition
```

**After** (table form):
```
|Dep|Source|Role|API/Flag|
|-|-|-|-|
|TurnLedger|`sprint.models`|budget|`debit,credit,can_launch,can_remediate,reimbursement_rate`|
|ClaudeProcess|—|LLM subprocess|debate/validation/patch agents|
|Click CLI|—|flag|`--allow-regeneration`|
```

**Estimated saving**: The Resource Requirements section is ~1,800 bytes of moderately verbose bullets. Table form is ~1,100 bytes. **~700 bytes (~2.5%)**.

**Lossless**: ✅ — no facts dropped; format changed from bullet to table. CommonMark parser treats both identically at the AST node-type level.

**Risks**:
- The sub-section headings ("External Dependencies (Consumed, Not Modified)", "Internal Dependencies (Extended)", "Future Dependencies (Probed, Not Required)") carry semantic grouping that would have to be preserved either as a column or as adjacent captions. Simplest: keep three tables, one per category, with single-row captions above each.
- Files to Create / Modify / Delete subsections (lines 399-413) are already optimally terse; do not transform them.

---

### Strategy 10 — Approach 3 (LLM-assisted) NOT recommended (primer §5 Roadmap row)

**What**: Per primer §5: *"Approach 3 offers marginal gains only on the rationale sections"* for roadmaps. For THIS file, the rationale sections are (a) the per-phase `**Goal**` one-liners, (b) the blockquote `> **Debate resolution**` blocks, and (c) the exec summary.

**Saving**: Strategies 5 and 8 already cover the blockquote and exec-summary compaction deterministically via Approach 2. The marginal LLM rewriting ceiling is ~200-400 bytes (1-1.5%) beyond Approach 2, which does not justify the audit-pass cost (primer §4.3 Risks) or non-determinism (primer §4.3 Determinism ★★☆☆☆).

**Recommendation**: **Skip Approach 3 for this file**. Record as a negative finding grounded in primer §5 guidance.

**Risks**: None — this is the safe default.

---

## 3. Recommended Strategy Stack

Applied in this order to give each subsequent transform a normalized input (primer §5 pipeline composition rule 1: *"Always run Approach 1 first"*).

| # | Strategy | Approach | Primer ref | Net saving | Cumulative % | Gate |
|--:|---|---|---|---:|---:|---|
| 1 | Blank-line collapse & trailing-space strip | A1 | §4.1 t1-2 | 1,200 B | 4.3% | Auto |
| 2 | Decorative horizontal-rule removal (non-YAML) | A1 | §4.1 t4 | 60 B | 4.5% | Auto |
| 3 | Table cell compaction + H/M/L abbrev | A1 | §4.1 t6 + §2.2 | 400 B | 5.9% | Auto |
| 4 | Resource Requirements bullet → table | A2 | §4.2 t2 | 700 B | 8.4% | Review |
| 5 | Bold-label compaction (preamble→header) | A2 | §4.2 t5 + §2.2 | 150 B | 8.9% | Auto |
| 6 | Dominant-token abbreviation via conventions header | A2 | §4.2 t5 + §2.2 | 560 B | 10.9% | Auto |
| 7 | Blockquote note compaction | A2 | §4.2 t3 | 300 B | 12.0% | Review |
| 8 | Bullet-list prose compaction (LARGEST WIN) | A2 | §4.2 t3 | 2,700 B | 21.6% | **Review gate required** |
| 9 | Exec-summary dedup vs phase bodies | A2 | §4.2 t6 | 400 B | 23.0% | **Consumer DAG decision required** |
| 10 | Approach 3 LLM-assisted rewrite | — | §5 roadmap row | 0 B (skipped) | 23.0% | N/A |

### Projected total compression for this file

**Conservative (auto + light review)**: Strategies 1-7 → **~12% reduction** (~3,370 bytes). Ships without human gate; safe for unattended batch compression.

**Recommended (full Approach 2 stack)**: Strategies 1-9 → **~23% reduction** (~6,470 bytes). Matches the lower end of primer §5's roadmap target (25-33%). Requires review gates on Strategies 8 and 9.

**Ceiling for this file**: Approximately **~25%**. This is below the primer §5 roadmap range midpoint (29%) because:
- Zero code fences eliminates the "code-block dedup" opportunity
- Zero emoji eliminates the decorative-strip opportunity
- Tables are already tightly formatted
- Requirement-ID preservation (line 438) blocks the most aggressive abbreviation classes
- No duplicate headings blocks primer §4.2 transform 1

The primer §5 roadmap row's 25-33% ceiling assumes a roadmap with more prose rationale and more decorative content. This file is already unusually terse for a roadmap — it is closer in profile to a tasklist than a typical roadmap, which is why Strategy 6 (bullet-list prose compaction) dominates the savings.

### Rationale for ordering

- **A1 first** (Strategies 1-3): primer §5 pipeline rule 1. These are free, deterministic, and normalize input for subsequent AST transforms.
- **Table→AST transforms before bullet rewrites** (Strategies 4-5): these are structure-changing and should run before content-level substitution so the substitution regex operates on stable cell boundaries.
- **Abbreviation substitution after structural settle** (Strategy 6): runs last among deterministic strategies so the conventions header can be finalized with the actual observed substitution counts.
- **Review-gated transforms last** (Strategies 7-9): separates the "auto" pipeline from the "human-in-the-loop" pipeline so the deterministic stack can ship without waiting on review.
- **Approach 3 skipped** (Strategy 10): primer §5 explicit guidance for roadmaps.

---

## 4. Risks & Caveats Specific to This File

### Blocking risks

1. **Requirement-ID preservation is contractual** (file line 438: *"Do not alias or renumber IDs"*). Any abbreviation strategy that aliases `FR-*`, `NFR-*`, `SC-*`, `OQ-*`, `G-*`, `D-*` tokens is a **spec violation**. Strategy 4's `[SC*]` abbreviation for "structural checkers" is deliberately chosen to avoid `SC-N` collisions but should be renamed `[STC]` in the actual substitution rule to remove any parser ambiguity.

2. **Commit hash `f4d9035` must be preserved verbatim** (lines 15, 277, 332, 432). This is a load-bearing byte-exact reference used for backward-compat validation. No abbreviation strategy may rewrite it.

### Non-blocking but notable

3. **Strategy 8 (exec-summary dedup) requires consumer-DAG decision** per primer §2.2 and INV-3. If the compressed roadmap is ever read by a human skimmer, the exec summary is load-bearing navigation and must be preserved. If consumers are exclusively downstream LLM agents doing a single full-document pass, the transform is lossless. **Recommendation**: run Strategy 8 only for LLM-consumed artifact copies; keep the human-readable copy uncompressed at this step.

4. **Strategy 6 (bullet prose compaction) is the largest saving but the highest fidelity risk**. It cannot be a blind regex; every bullet must be reviewed. Without a review gate, drop Strategy 6 from the stack — this reduces projected savings from ~23% to ~13%.

5. **No code fences** in the file means the fence-awareness plumbing that primer §4.1 recommends as a guard (and primer §4.2 rule 2 declares "sacrosanct") is unnecessary for this document. However, the compression tool should still implement fence-awareness globally — other roadmap files in the same pipeline DO contain code fences, and shipping a code-unaware compressor is the primer's top structural risk.

6. **Conventions header amortization is marginal for a single-read roadmap**. Per primer §2.2: *"If read-count < 5, drop the header and absorb the 40-60 token cost as savings foregone."* Completed-release roadmaps under `.dev/releases/complete/` are ARCHIVED documents — read-count is likely 1-3 over their lifetime. **Therefore**: apply Strategies 1-3 and 4 (structural, no header needed) but **DROP Strategies 5-6's conventions header** if this file is archived-only. The dominant-token abbreviation (Strategy 6) yields ~560 bytes — the header cost for Strategies 5+6 combined is ~320 bytes. Net still positive (~240 bytes) but close to break-even; under INV-3 ambiguity, the conservative call is to skip the header entirely for archived roadmaps.

7. **INV-1 tokenizer generalization** (primer §6): all byte-count estimates above are byte-based, not token-based. Actual Claude-native token savings may drift ±2-8 percentage points. The ~23% byte-reduction projection should be reported as "~18-28% token reduction" under INV-1 uncertainty.

8. **No LLM-assisted auditor pass is in scope** for this file (Strategy 10 skipped). This means the review gate on Strategies 6-8 must be human-performed or deferred to a later tooling iteration. Until that tooling exists, the safe deployable subset of this plan is **Strategies 1-5 + 7 (partial) = ~10% conservative compression**.

### Caveats on cumulative estimate

The cumulative percentages in Section 3 are **additive byte estimates**, not multiplicatively compounded. Because Strategy 6 operates on bullets that Strategies 1-5 have already normalized (shorter headings, no trailing whitespace, etc.), its absolute byte-saving count is slightly overestimated. A realistic adjustment is to discount Strategy 6 by ~10% (2,700 → 2,430 bytes) and Strategy 7 by ~5%. The adjusted cumulative Approach-2 total is **~22% rather than ~23%**.

---

## Appendix: Primer citations used

- §2.1 lossless vs lossy table — Strategies 1, 2, 4, 6, 9
- §2.2 conventions header + amortization — Strategies 3, 4, 6, 7; Risk #6
- §2.3 category ceilings — all strategies map to a category
- §4.1 rule-based transforms 1-6 — Strategies 1, 2, 3, 7
- §4.2 AST-aware transforms 2, 3, 5, 6 — Strategies 4, 5, 6, 7, 8
- §4.3 LLM-assisted — Strategy 10 (skipped, justified)
- §5 roadmap row — overall target + Strategy 10 skip justification
- §5 pipeline composition rules 1, 2, 3, 7 — ordering rationale
- §6 INV-1, INV-3 — tokenizer drift caveat + consumer DAG risk
