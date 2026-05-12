# Compression Analysis: roadmap-gaps.md (v3.00 RoadmapCliGaps)

**Target**: `/config/workspace/IronClaude/.dev/releases/complete/v.3.00-RoadmapCliGaps/roadmap-gaps.md`
**Reference primer**: `/config/workspace/IronClaude/claudedocs/compressed-markdown-dsl-primer.md`
**Analysis date**: 2026-04-15
**Classification**: multi-proposal roadmap / gap-remediation document (treated as "Roadmap" row in primer §5 strategy matrix, with one important caveat — see §4)

---

## Section 1: File Inventory

### 1.1 Raw measurements

| Metric | Value |
|---|---|
| Path | `.dev/releases/complete/v.3.00-RoadmapCliGaps/roadmap-gaps.md` |
| Bytes | 73,076 |
| Lines | 1,456 |
| Avg line length | 49.2 chars |
| Blank lines | 426 (29.3% of lines) |
| Heading lines (`^#`) | 125 (8.6% of lines) |
| Table-row lines (`^|`) | 131 (9.0% of lines) |
| Code fence delimiters (```` ``` ````) | 70 (→ 35 code blocks) |
| Code block content bytes | 18,214 (24.9% of bytes) |
| Horizontal-rule lines (`^---$`) | 18 |
| Bullet lines (`^[-*] `) | 84 |
| Trailing-whitespace lines | 0 (already clean) |
| Triple-blank runs | 0 (already normalized) |
| Emoji in headings | 0 |
| YAML front matter | None |

### 1.2 Structural composition by byte category

These are approximate slices summing to ~100%. Numbers are derived from the raw counts above plus hand-tallied representative line-length averages per category.

| Category (primer §2.3) | Est. bytes | Share | Notes |
|---|---:|---:|---|
| Code fences (Python / YAML blocks) | 18,214 | ~25% | 35 fenced blocks. Sacrosanct per primer §5 rule 2 — never touched. |
| Tables (pipe tables) | ~8,400 | ~11.5% | 131 table rows across 18 distinct tables. Many padded with spaces. |
| Headings | ~2,900 | ~4.0% | 125 heading lines; 5 H1 (one per Gap), many repeated H2/H3 labels. |
| Blank lines | ~450 | ~0.6% | Count is 426 lines × ~1 byte; already at minimum. |
| Horizontal rules (`---`) | ~72 | ~0.1% | 18 decorative dividers between sub-sections. |
| Bold-label preambles (`**File**:`, `**Line**:`, `**Risk**:`, `**Rationale**:`) | ~1,300 | ~1.8% | Heavily repeated per-change boilerplate. |
| Prose (body paragraphs + bullets) | ~41,800 | ~57% | Analysis, rationale, validation write-ups. |
| **Total** | **~73,076** | **100%** | |

### 1.3 Repeating patterns that would benefit from a conventions header

Grep-verified repetition counts (candidates for abbreviation per primer §2.2):

| Phrase | Occurrences | Avg length | Gross bytes consumed |
|---|---:|---:|---:|
| `complexity_class` | 79 | 16 | ~1,264 |
| `frontmatter` | 74 | 11 | ~814 |
| `gates.py` | 35 | 8 | ~280 |
| `extraction_mode` | 35 | 15 | ~525 |
| `domains_detected` | 35 | 16 | ~560 |
| `prompts.py` | 33 | 10 | ~330 |
| `interleave_ratio` | 27 | 16 | ~432 |
| `EXTRACT_GATE` | 24 | 12 | ~288 |
| `src/superclaude/cli/roadmap/` (path prefix) | 30 | 26 | ~780 |
| `tests/roadmap/` (path prefix) | 34 | 15 | ~510 |
| `validation_milestones` | 17 | 21 | ~357 |
| `TEST_STRATEGY_GATE` | 16 | 18 | ~288 |
| `SemanticCheck` | 11 | 13 | ~143 |
| `_parse_frontmatter` | 10 | 18 | ~180 |
| `semantic_checks` | 11 | 15 | ~165 |
| `validation_philosophy` | ~9 | 21 | ~189 |
| `major_issue_policy` | ~9 | 18 | ~162 |
| `LOW|MEDIUM|HIGH` | 7 | 15 | ~105 |

Gross abbreviable footprint: **~7,400 bytes** (≈10% of file) before counting the additional prose repetitions inside sentences. This strongly motivates a conventions header (primer §2.2).

### 1.4 Structural-regularity observations

The file is **five merged gap proposals** stitched together (Gaps #1, #2, #3, #4+#6 merged, #5). Each proposal reproduces the same skeleton:

- `## Problem Statement` (5 occurrences)
- `## Analysis` or `## Analysis Summary`
- `## Proposed Changes` / `## Implementation Plan`
- `### Change N:` sub-sections (15 total across the file)
- `## Risk Assessment` (4 occurrences)
- `## Files Modified` / `## Files to Modify` / `## Files Changed` table
- `## Validation Result` (5 occurrences)

This is **extreme structural regularity** — exactly the redundancy profile the primer §5 says AST-aware compression (Approach 2) targets best.

### 1.5 Caveat: this is a "Roadmap-shaped" document, not a true roadmap

The primer's strategy matrix row for "Roadmap" assumes phases/milestones/bullets with moderate prose. This document is actually **5 merged per-gap implementation proposals** — closer to the "PRD" or "TDD" rows in prose density (lots of rationale, Q&A analysis, validation write-ups) but with the structural regularity of a roadmap. It also has a **large code-block share (~25%)** that is closer to a TDD. The recommended stack in §3 accounts for this hybrid profile.

---

## Section 2: Strategies Identified

Each strategy is numbered, cites the primer, shows a real before/after snippet from the file, and estimates byte savings specific to this file.

---

### Strategy 1 — Collapse pipe-table column padding

**Approach**: Rule-based (primer §4.1, transform #6).
**Primer citation**: §4.1 "Collapse pipe-table padding: `| foo | bar |` → `|foo|bar|`".
**Lossless**: Yes (pure whitespace inside pipe cells).

**Before** (lines 8-12):
```
| Location | Enum Values | Role |
|----------|-------------|------|
| `src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` (source protocol) | `LOW \| MEDIUM \| HIGH` | Source of truth for milestone count selection, interleave ratios, effort mapping |
| `src/superclaude/cli/roadmap/prompts.py` line 88 (CLI extract prompt) | `simple \| moderate \| complex \| enterprise` | Instructs the LLM what values to emit in extraction frontmatter |
```

**After** (column separators tightened, rule row shrunk):
```
|Location|Enum Values|Role|
|-|-|-|
|`src/superclaude/skills/sc-roadmap-protocol/refs/templates.md` (source protocol)|`LOW\|MEDIUM\|HIGH`|Source of truth for milestone count selection, interleave ratios, effort mapping|
|`src/superclaude/cli/roadmap/prompts.py` line 88 (CLI extract prompt)|`simple\|moderate\|complex\|enterprise`|Instructs the LLM what values to emit in extraction frontmatter|
```

**Estimated saving for this file**: 131 table rows × ~6 bytes of intra-cell padding/rule-row bytes ≈ **~800 bytes (~1.1%)**. Lower end of primer's §2.3 table-whitespace ceiling of 3-5% because this file's tables are already fairly tight.

**Risks**: Literal `\|` escapes inside cells (escaped pipes in the enum examples) must be preserved; a naive regex could corrupt them. Mitigated by using a CommonMark-aware pipe-table tokenizer rather than raw `s/ \|/\|/g`.

---

### Strategy 2 — Remove decorative horizontal rules between sibling sections

**Approach**: Rule-based (primer §4.1, transform #4).
**Primer citation**: §4.1 "Remove decorative horizontal rules not adjacent to YAML front matter"; §2.3 "Decorative elements".
**Lossless**: Yes (headings already delimit the sections; rules are purely visual).

**Before** (lines 432-435):
```
...change 2. The semantic check in Change 2 provides a regression safety net.

---

## Validation Result
```

**After**:
```
...change 2. The semantic check in Change 2 provides a regression safety net.

## Validation Result
```

**Estimated saving for this file**: 18 `---` lines × ~5 bytes (including surrounding blank lines) ≈ **~90 bytes**. Trivial on its own but costless. Included for completeness of §2.3 "Decorative elements" category.

**Risks**: None — the file has no YAML front matter, so no delimiter collision is possible. (Verified: `^---$` count is 18, all are mid-document dividers.)

---

### Strategy 3 — Synthesize a conventions header for the top 12 repeated identifiers

**Approach**: AST-aware (primer §4.2, transform #5) — "Front-matter → conventions-header synthesis: scan for frequently-used multi-word phrases (>5 occurrences, >20 chars each) and auto-generate an abbreviation in the conventions header; apply substitution in body".
**Primer citation**: §2.2 "The conventions header"; §4.2 transform #5.
**Lossless**: Yes (reversible via header).

**Proposed header** (one line, ~200 bytes, amortizes across hundreds of body uses):
```markdown
<!-- cmd-dsl v1: [cc]=complexity_class [fm]=frontmatter [em]=extraction_mode [dd]=domains_detected [ir]=interleave_ratio [vm]=validation_milestones [wm]=work_milestones [vp]=validation_philosophy [mip]=major_issue_policy [EG]=EXTRACT_GATE [TSG]=TEST_STRATEGY_GATE [SC]=SemanticCheck [CLI/]=src/superclaude/cli/roadmap/ [T/]=tests/roadmap/ [P/]=src/superclaude/skills/sc-roadmap-protocol/refs/ -->
```

**Before** (line 14):
```
The source protocol's milestone count table maps `LOW`, `MEDIUM`, `HIGH` to specific milestone ranges (3-4, 5-7, 8-12). When the CLI prompt tells the LLM to emit `simple`, `moderate`, `complex`, or `enterprise`, no downstream code or template logic can match those values to the protocol's decision tables. The gate (`EXTRACT_GATE` in `gates.py`) only checks that `complexity_class` is present in frontmatter -- it does not validate the value itself.
```

**After** (with abbreviations applied):
```
The source protocol's milestone count table maps `LOW`, `MEDIUM`, `HIGH` to specific milestone ranges (3-4, 5-7, 8-12). When the CLI prompt tells the LLM to emit `simple`, `moderate`, `complex`, or `enterprise`, no downstream code or template logic can match those values to the protocol's decision tables. The gate ([EG] in CLI/gates.py) only checks that [cc] is present in [fm] -- it does not validate the value itself.
```

**Estimated saving for this file**:
- `complexity_class` (79×) → `[cc]` saves (16−4)×79 ≈ 948 bytes
- `frontmatter` (74×) → `[fm]` saves (11−4)×74 ≈ 518 bytes
- `extraction_mode` (35×) → `[em]` saves (15−4)×35 ≈ 385 bytes
- `domains_detected` (35×) → `[dd]` saves (16−4)×35 ≈ 420 bytes
- `interleave_ratio` (27×) → `[ir]` saves (16−4)×27 ≈ 324 bytes
- `EXTRACT_GATE` (24×) → `[EG]` saves (12−4)×24 ≈ 192 bytes
- `validation_milestones` (17×) → `[vm]` saves (21−4)×17 ≈ 289 bytes
- `TEST_STRATEGY_GATE` (16×) → `[TSG]` saves (18−5)×16 ≈ 208 bytes
- `SemanticCheck` (11×) → `[SC]` saves (13−4)×11 ≈ 99 bytes
- `semantic_checks` (11×) → left alone (lowercase collides with `[SC]`; ~0 savings or apply with variant)
- `_parse_frontmatter` (10×) — leave (appears inside code blocks; see Risk)
- Path prefixes: `src/superclaude/cli/roadmap/` (30×) → `CLI/` saves ~22×30 ≈ 660 bytes
- Path prefixes: `tests/roadmap/` (34×) → `T/` saves ~13×34 ≈ 442 bytes

**Gross body savings**: ~4,485 bytes. **Header cost**: ~200 bytes. **Net**: ~**4,285 bytes (~5.9%)**. This is the single largest lever for this file.

**Risks**:
- Many occurrences are inside **code fences** (e.g., `_parse_frontmatter`, field names in YAML examples). The primer is explicit (§5 rule 2, §4.1 risks): code fences are sacrosanct. The substitution must only apply to prose regions. A rule-based pass cannot safely do this; only an AST-aware pass (Approach 2) can fence-gate the substitution. **This strategy is strictly Approach 2, not Approach 1.**
- `_parse_frontmatter` is function identifier inside Python fences — excluded from substitution.
- Abbreviation collisions: `[SC]` vs literal SuperClaude abbreviation — mitigated by using bracketed forms that do not appear in the source.
- Amortization check (§2.2, INV-3): this file is read many times during implementation planning and retrospective — the ≥5-read bar is easily cleared, so the 200-byte header cost is recoverable.

---

### Strategy 4 — Cross-reference / duplicate-line-number deduplication

**Approach**: AST-aware (primer §4.2, transform #4) — "Cross-reference deduplication: detect `(see Section 3.2)` repeated with same target and replace second occurrence with pure anchor".
**Primer citation**: §4.2 transform #4.
**Lossless**: Yes for intra-document anchors; lossy-to-humans for cross-file line references (see Risks).

**Before** — The same line references are stated in the proposal and then re-stated verbatim in the Validation Result. Example: lines 88, 213:
```
Line 88 of prompts.py:
"- complexity_class: (string) one of: simple, moderate, complex, enterprise\n"
```
...then in the validation section (line 213):
```
- `prompts.py:88` -- confirmed: `"- complexity_class: (string) one of: simple, moderate, complex, enterprise\n"`
```

**After** — in the validation section, collapse the re-quoted code to an anchor reference:
```
- `prompts.py:88` -- confirmed (matches Change 1 Before block)
```

**Estimated saving for this file**: Each of the 5 gaps has a Validation Result section that re-quotes code/line references already shown in the body. Rough count: ~15 re-quoted snippets × ~90 bytes each ≈ **~1,350 bytes (~1.8%)**.

**Risks**:
- Human readers lose the convenience of "self-contained validation section". For a validated-and-archived doc this is acceptable; for an in-flight proposal it is lossy-to-workflow.
- Anchors must be stable (heading IDs) — the primer flags this as a "can break navigation for humans" risk.

---

### Strategy 5 — Elide repeated preamble labels under per-Change sub-sections

**Approach**: AST-aware list compaction (primer §4.2, transform #3) + preamble/meta category (primer §2.3 "Preamble & meta").
**Primer citation**: §2.3 preamble category; §4.2 transform #3.
**Lossless**: Yes.

Each `### Change N` block uses the same boilerplate pattern:
```
**File**: `src/superclaude/cli/roadmap/prompts.py`
**Line**: 88

Replace:
```python
<snippet>
```
With:
```python
<snippet>
```

**Risk**: LOW. This only changes the LLM instruction...
```

Counted: `**File**:` 14×, `**Line**:` 3×, `**Risk**:` 4×, `**Rationale**:` 2×, plus repeated `Replace:`/`With:` structural labels.

**Before** (lines 84-98):
```
### Change 1: Fix the extract prompt enum (prompts.py:88)

**File**: `src/superclaude/cli/roadmap/prompts.py`
**Line**: 88

Replace:
```python
"- complexity_class: (string) one of: simple, moderate, complex, enterprise\n"
```
With:
```python
"- complexity_class: (string) one of: LOW, MEDIUM, HIGH\n"
```

**Risk**: LOW. This only changes the LLM instruction.
```

**After** (single-line header collapses file+line; diff-style code block collapses replace/with):
```
### Change 1: Fix extract prompt enum — CLI/prompts.py:88

```diff
-"- complexity_class: (string) one of: simple, moderate, complex, enterprise\n"
+"- complexity_class: (string) one of: LOW, MEDIUM, HIGH\n"
```
Risk: LOW. Only changes the LLM instruction.
```

**Estimated saving for this file**: ~15 Change sub-sections × ~70 bytes of boilerplate elision ≈ **~1,050 bytes (~1.4%)**.

**Risks**:
- Converting paired `Replace:`/`With:` fences into a single `diff` fence changes code-fence language from `python` to `diff`, which a strict code-fence preservation rule would reject. However, primer §5 rule 2 says code fence **boundaries** are sacrosanct; the **language tag** is metadata. This is a judgment call — if implementers want hard fence preservation, keep the two-fence form and only collapse the `**File**:`/`**Line**:` labels (savings drop to ~600 bytes).
- The diff-form loses syntax highlighting for Python — acceptable for archived artifacts, less ideal for in-flight review.

---

### Strategy 6 — Collapse multi-paragraph bullets into single-line bullets

**Approach**: AST-aware (primer §4.2, transform #3) — "List compaction: convert multi-paragraph bullets into single-line bullets when the paragraph is one sentence".
**Primer citation**: §4.2 transform #3.
**Lossless**: Yes.

**Before** (lines 70-81):
```
**The protocol's `LOW|MEDIUM|HIGH` must win.** Rationale:

1. **Source of truth**: `templates.md` is the canonical reference document loaded during Waves 2-3. It defines the decision tables that consume `complexity_class`.

2. **Downstream coupling**: Milestone count selection, interleave ratios, and effort estimation all key on `LOW|MEDIUM|HIGH`. The CLI's `simple|moderate|complex|enterprise` set has zero downstream consumers.
```

**After** (blank-line separators between list items removed):
```
**The protocol's `LOW|MEDIUM|HIGH` must win.** Rationale:
1. **Source of truth**: `templates.md` is the canonical reference document loaded during Waves 2-3. It defines the decision tables that consume `complexity_class`.
2. **Downstream coupling**: Milestone count selection, interleave ratios, and effort estimation all key on `LOW|MEDIUM|HIGH`. The CLI's `simple|moderate|complex|enterprise` set has zero downstream consumers.
```

**Estimated saving for this file**: The file has many numbered/bulleted lists with blank-line separators. Rough count: 84 bullets + ~60 enumerated list items, of which ~90 are immediately preceded by a blank line that is semantically redundant. ~90 × ~1 byte + normalization of paragraph structure ≈ **~250 bytes (~0.3%)**.

Marginal alone, but belongs in the Approach 2 stack for completeness.

**Risks**: Some markdown renderers treat loose vs tight lists differently (tight lists render without `<p>` wrapping). Semantically equivalent for LLM consumption.

---

### Strategy 7 — Drop `## Validation Result` narrative wrappers, keep factual rows only

**Approach**: AST-aware (primer §4.2) with semantic dedup across distant sections. Borderline lossy — see Risks.
**Primer citation**: §4.2 — transform #6 "Prose summarization of introduction paragraphs (bounded, deterministic): if an `## Introduction` section restates content found verbatim later, elide the restated sentences". §2.3 "Prose redundancy (restatement)".
**Lossless**: Partially — **lossy for narrative voice, lossless for factual assertions**.

Every gap proposal has a ~40-80 line `## Validation Result` section that restates the proposal's claims as a verification table ("all line numbers confirmed", "no downstream consumers", etc.). Much of this is prose wrapping around a small factual core.

**Before** (lines 205-249, 44 lines of Validation Result for Gap #1):
```
## Validation Result

**Reviewed**: 2026-03-18 | **Verdict**: PASS with minor clarifications noted below.

### Line Numbers and Code References

All line numbers verified against current source:

- `prompts.py:88` -- confirmed: `"- complexity_class: (string) one of: simple, moderate, complex, enterprise\n"`
- `gates.py:523-541` -- confirmed: `EXTRACT_GATE` definition with no `semantic_checks` field
- `release-spec-template.md:28` -- confirmed: `complexity_class: {{SC_PLACEHOLDER:simple_or_moderate_or_high}}`
- `tests/roadmap/test_pipeline_integration.py:86` -- confirmed: `"complexity_class": "moderate"`
...
### Completeness Assessment

The change set is **complete**. Exhaustive codebase search for `complexity_class` in `src/superclaude/` found exactly the touchpoints listed in the proposal...
```

**After** (collapse to a single verification table + bullet list of clarifications):
```
## Validation (2026-03-18, PASS)

Line refs verified: prompts.py:88, gates.py:523-541, release-spec-template.md:28, T/test_pipeline_integration.py:86, T/test_executor.py:102, T/test_integration_v5_pipeline.py:91.

Completeness: exhaustive `complexity_class` search in CLI/ matches proposal touchpoints; no additional Python consumers.

Clarifications (non-blocking):
1. Change 5 must import `_complexity_class_valid` in T/test_gates_data.py
2. Add `test_generate_gates_have_semantic_checks`-analogue for EG
3. Coordinate with Gap-4 to share `_complexity_class_valid` definition
```

**Estimated saving for this file**: Across the 5 Validation Result sections (roughly 44+55+60+10+40 = ~210 lines of narrative), compaction to fact-dense bullet form removes ~60-65% of the prose. ~210 lines × 49 bytes × 0.62 ≈ **~6,380 bytes (~8.7%)**.

**Risks**:
- **This is the primary lossy transform** on the list. The factual assertions (PASS/FAIL verdict, line-number confirmations, clarifications) survive; the narrative voice ("All line numbers verified against current source", "The change set is complete") is stripped.
- Per primer §4.3, this is the kind of transform that normally requires LLM-assisted rewriting with an auditor pass. But the Validation sections in this file are already highly structured — a rule-based reviewer could probably do it deterministically, making it an unusual sweet-spot case for AST-aware compaction.
- If the file is used as evidence in an audit, the voice loss might be unwelcome. Mitigation: only apply to archived (complete) releases, not in-flight proposals. This file is in `.dev/releases/complete/`, so the condition is met.

---

### Strategy 8 — Canonicalize "Problem Statement" / "Risk Assessment" / "Files Modified" section headings across the 5 proposals

**Approach**: AST-aware (primer §4.2, transform #1) — "Heading deduplication: detect `## Phase 2` appearing twice and merge second occurrence into an anchor reference".
**Primer citation**: §4.2 transform #1.
**Lossless**: Yes.

The file has 5 copies of `## Problem Statement`, 4 of `## Risk Assessment`, 5 of `## Validation Result`. These are not duplicates in the AST-merge sense — they belong to different H1 sections — but their **consistent heading text** could be shortened in the compressed form without information loss because the enclosing H1 gap number disambiguates.

**Before** (H1 at line 1, H2 at line 3):
```
# Gap #1: `complexity_class` Enum Mismatch -- Implementation Proposal

## Problem Statement
```

**After**:
```
# Gap #1: `complexity_class` Enum Mismatch

## Problem
```

**Estimated saving for this file**: Removing `-- Implementation Proposal` suffix from 5 H1s (~25 bytes each = 125 bytes), shortening `Problem Statement` → `Problem` (5× saves 50 bytes), `Risk Assessment` → `Risk` (4× saves 44 bytes), `Validation Result` → `Validation` (5× saves 35 bytes), `Proposed Changes` → `Changes` (2× saves 18 bytes), `Implementation Plan` → `Plan` (6× saves 90 bytes), `Files Modified` / `Files to Modify` / `Files Changed` → `Files` (5× saves 45 bytes). Total: **~400 bytes (~0.55%)**.

**Risks**: Minor — any anchor link referencing these headings by full text would break. Grepping the repo for `#problem-statement` link targets is a one-shot precheck.

---

### Strategy 9 — Numeric / phrasing canonicalization in prose

**Approach**: LLM-assisted (primer §4.3, transform #5) — "Numeric canonicalization: 'approximately 200 milliseconds' → '~200ms'".
**Primer citation**: §4.3 transforms #1, #5.
**Lossless**: Task-equivalent (primer §2.1 definition) but requires auditor pass.

The file has multiple verbose equivalents:

**Before** (line 273):
```
- **`chunked`**: Multi-chunk extraction activated when the spec exceeds 500 lines. The value includes chunk count metadata, e.g., `chunked (4 chunks)` (per `extraction-pipeline.md` L357).
```

**After**:
```
- `chunked`: activated when spec >500 lines; value carries chunk count, e.g. `chunked (4 chunks)` (extraction-pipeline.md:357)
```

**Estimated saving for this file**: ~25-40 sentences similarly rewritable, ~30 bytes each ≈ **~900-1,200 bytes (~1.3-1.6%)**.

**Risks**:
- Primer §4.3 flags LLM rewriting as ★★☆☆☆ determinism. An auditor pass is required.
- The primer's strategy matrix (§5) notes "Roadmaps sit between PRDs and tasklists. The prior adversarial study found Approach 2 (AST) is the sweet spot at 25-33%. Approach 3 offers marginal gains only on the rationale sections." The marginal ~1.5% here confirms that finding.
- Not recommended as a primary lever; include only if the stack's cumulative target has not been hit.

---

### Strategy 10 — Collapse three near-identical "test fixture update" blocks across Gaps #1, #2, #3

**Approach**: AST-aware semantic-dedup (primer §4.2, transform #2 table-dedup analog) + cross-section deduplication.
**Primer citation**: §4.2 transform #2 "Table normalization: detect repeated column values... hoist into a caption"; §4.2 transform #4 cross-reference dedup.
**Lossless**: Yes.

Gaps #1, #2, and #3 each emit **the same 3 test files** with one-field-per-gap updates:
- `tests/roadmap/test_pipeline_integration.py`
- `tests/roadmap/test_executor.py`
- `tests/roadmap/test_integration_v5_pipeline.py`

Each gap's "Files Modified" / "Test fixtures" section re-lists these 3 file paths with near-identical commentary. ~150 bytes × 3 gaps × 3 files ≈ 1,350 bytes of restatement.

**Before** (Gap #1 Change 4 + Gap #2 Correction 1 + Gap #3 Change 3 — all list the same 3 files):
```
- `tests/roadmap/test_pipeline_integration.py:86` -- `"complexity_class": "moderate"`
- `tests/roadmap/test_executor.py:102` -- `"complexity_class": "moderate"`
- `tests/roadmap/test_integration_v5_pipeline.py:91` -- `"complexity_class": "moderate"`
```
(...and the same three file-paths show up in Gap #2 and Gap #3 with different field changes.)

**After** (hoist a shared fixture table once near the top, reference by field per gap):
```
## Shared Test-Fixture Touchpoints

| File | L86-91 | L102-107 | L87-96 |
|---|---|---|---|
| test_pipeline_integration.py | cc | em | dd |
| test_executor.py | cc | em | dd |
| test_integration_v5_pipeline.py | cc | em | dd |

(cc=complexity_class "moderate"→"MEDIUM"; em=extraction_mode "full"→"standard"; dd=domains_detected int→list)
```

Then each gap's "Files Modified" section just says "see Shared Test-Fixture Touchpoints table".

**Estimated saving for this file**: ~900-1,100 bytes (~1.3%).

**Risks**: Introduces a forward reference that a linear reader must resolve. Acceptable for a machine consumer; a human reviewer loses some section-locality. Primer §4.2 flags this class of transform as safe if a conventions/shared-section header is present.

---

### Strategy 11 — Code-fence-aware whitespace collapse inside code blocks (bounded)

**Approach**: Rule-based with fence-awareness (primer §4.1 transforms #1-#2, restricted to outside fences per §5 rule 2).
**Primer citation**: §4.1 transform #1 "Collapse 3+ blank lines → 2 blank lines (outside code fences)"; §5 rule 2.
**Lossless**: Yes (outside fences).

The file already has zero triple-blank runs (`awk` count = 0) and zero trailing whitespace (`grep -Pc ' +$'` = 0). So the standard Approach 1 freebies are already extracted. **This strategy therefore produces ~0 bytes for this file.**

Included only to document that the rule-based freebies are exhausted. Any downstream pipeline scanning this file should skip Approach 1's whitespace transforms as no-ops.

**Estimated saving for this file**: **~0 bytes.**

**Risks**: None.

---

### Strategy 12 — Remove `-- Implementation Proposal` / verdict preambles from Validation Results

**Approach**: Preamble/meta stripping (primer §2.3 "Preamble & meta").
**Primer citation**: §2.3.
**Lossless**: Yes.

Each of the 5 Validation Results has a preamble pattern like:
```
**Reviewed**: 2026-03-18 | **Verdict**: PASS with minor clarifications noted below.
```
or
```
**Status: PASS WITH CORRECTIONS**

Independent review validated the proposal on 2026-03-18 against the actual codebase. The analysis is sound, the line number references are accurate, and the proposed changes are correct...
```

**After**:
```
Verdict: PASS (2026-03-18, minor clarifications)
```

**Estimated saving for this file**: 5 preambles × ~100-200 bytes of narrative ≈ **~750 bytes (~1.0%)**. Overlaps with Strategy 7 (which folds this transform inside the broader Validation-narrative compaction). Cite once, count once.

**Risks**: None.

---

## Section 3: Recommended Strategy Stack

### 3.1 Ordered application

The stack respects primer §5 composition rules 1 (Approach 1 first), 2 (code fences sacrosanct), 3 (Approach 2 when structural regularity > prose density), 5 (never exceed Approach 1 on specs — N/A here, this is not a spec), 6 (auditor gate for lossy), and 7 (amortization check).

| Order | Strategy | Approach | Lossless? | Est. bytes | Est. % of file | Cumulative % |
|---:|---|---|---|---:|---:|---:|
| 1 | S11: rule-based whitespace freebies | 1 | Yes | 0 | 0.0% | 0.0% |
| 2 | S1: pipe-table padding collapse | 1/2 | Yes | 800 | 1.1% | 1.1% |
| 3 | S2: remove decorative `---` rules | 1 | Yes | 90 | 0.1% | 1.2% |
| 4 | S8: canonicalize heading text | 2 | Yes | 400 | 0.5% | 1.8% |
| 5 | S6: list tightening | 2 | Yes | 250 | 0.3% | 2.1% |
| 6 | S5: per-Change preamble elision (safe variant, no diff-fence fold) | 2 | Yes | 600 | 0.8% | 2.9% |
| 7 | S10: hoist shared test-fixture table | 2 | Yes | 1,000 | 1.4% | 4.3% |
| 8 | S4: validation re-quote dedup | 2 | Yes | 1,350 | 1.8% | 6.2% |
| 9 | S3: conventions header for top identifiers (fence-gated) | 2 | Yes | 4,285 | 5.9% | 12.0% |
| 10 | S12: Validation preamble strip | 2 | Yes | (covered by S7) | — | 12.0% |
| 11 | S7: Validation-narrative compaction (lossy, auditor-gated) | 2→3 | Lossy-to-voice | 6,380 | 8.7% | 20.8% |
| 12 | S9: prose canonicalization (optional, LLM+auditor) | 3 | Task-equivalent | 1,000 | 1.4% | **22.2%** |

**Projected cumulative compression for this file: ~22% bytes** (~16,100 bytes of 73,076).

### 3.2 Rationale for the 22% projection vs the primer's 25-33% roadmap ceiling

The primer's §5 Roadmap row targets 25-33% (matching V-B's -33.4% measurement). This file lands slightly lower (~22%) for three file-specific reasons:

1. **~25% of the bytes are inside Python/YAML code fences**, which are sacrosanct (primer §5 rule 2). That ceiling is hard. If code fences were treatable, the ceiling would rise by another 5-10 points.
2. **The document is already whitespace-clean** (0 trailing-whitespace lines, 0 triple-blank runs, 0 emoji) — the free 8-12% whitespace savings from primer §2.3 row 1 are already extracted by whoever authored/normalized the file. This eats ~5 points out of the ceiling.
3. **The document is a hybrid** (roadmap-structure + TDD-style code density + PRD-style prose in the Validation sections). Primer §5 rule 4 says Approach 3 is warranted only once Approach 2 has exhausted structural savings. Here, S7 (Validation compaction) is the gate-crossing between Approach 2 and Approach 3; going further (per-sentence prose rewriting) offers only ~1.5% more (S9), confirming the primer's observation that "Approach 3 offers marginal gains only on the rationale sections" for roadmap-shaped content.

### 3.3 If the user is willing to skip the lossy step

Stopping before S7 gives **~12% lossless compression** (~8,800 bytes). This is the "safe" tier — fully reversible, no auditor pass required, no voice loss.

### 3.4 If the user accepts auditor-gated lossy compression

S7 alone moves the projection from 12% to ~21%. S9 adds a final ~1% at high marginal cost (API calls, auditor pass per primer §4.3). For an archived release artifact, S7 is worth it; S9 probably is not.

---

## Section 4: Risks & Caveats Specific to This File

### 4.1 The 25% code-fence share is a hard ceiling

Python snippets (function definitions, gate criteria, test fixtures) make up ~18,214 bytes (~25%). Per primer §5 rule 2, none of this can be touched by any of the three approaches. Any tool that tries to regex-compress inside fences risks corrupting the `_complexity_class_valid` / `_extraction_mode_valid` / etc. function definitions that are the operative deliverables of this document.

**Mitigation**: Every strategy above is fence-gated. Strategy 3 (conventions header) in particular is **only safe as an Approach 2 AST-aware pass**, not as a naive `sed` — because `_parse_frontmatter`, `complexity_class`, `EXTRACT_GATE`, etc. appear inside Python fences dozens of times and must be left untouched.

### 4.2 `^---$` ambiguity is a non-issue

The file has 18 `^---$` lines, all of which are decorative horizontal rules (no YAML front matter exists). An AST parser will classify them as `thematic_break` tokens, cleanly separable from YAML delimiters. A pure-regex pass must be confirmed fence-aware (Python fences do not contain `---` lines, so collision is practically zero, but principled implementations should still use a tokenizer).

### 4.3 The document is an archived release artifact

Path is `.dev/releases/complete/v.3.00-RoadmapCliGaps/`. This classification matters for two reasons:

- **Amortization (primer §2.2, INV-3)**: archived release docs are read many times (post-release retros, audit trails, training data for future proposals). The conventions-header 200-byte overhead clears the ≥5-read amortization bar easily.
- **Lossy tolerance (primer §4.3)**: "archive for fidelity, not performance" applies to specs, not to release retrospectives. S7's voice-loss is acceptable here because the factual assertions (verdicts, line-number confirmations, clarifications) are preserved and the narrative voice is not contractually load-bearing.

### 4.4 Cross-proposal dedup has a correctness trap

Strategy 10 hoists test-fixture references into a shared table. The three gaps update **different fields** in **the same three files** (Gap #1 updates `complexity_class`, Gap #2 updates `extraction_mode`, Gap #3 updates `domains_detected`). A careless hoist could lose the per-gap mapping. The before/after example in S10 explicitly uses a 3-column mapping to preserve it, but implementers must verify the hoist preserves all field-to-gap bindings.

### 4.5 Line-number references are load-bearing

This document's primary content is **line-number citations** into the CLI codebase (e.g., `prompts.py:88`, `gates.py:523-541`, `templates.md:414`). Any compression strategy that touches these numeric citations — or the code snippets they validate — risks changing the document's meaning. Specifically:

- Strategy 4 (re-quote dedup) elides duplicated code snippets but **must preserve the line-number citation** on every reference.
- Strategy 9 (numeric canonicalization) must exclude line-number contexts — `"line 88"` cannot become `"~88"`.

### 4.6 Gap #4+#6 merged section has its own internal deduplication

Lines 757-1212 already apply semantic deduplication between Gap #4 and Gap #6 (see the "Deduplication Record" table at lines 1179-1187). The author has already shrunk this section by ~40% relative to what a naive merge would produce. Any compression pass targeting this section has a lower ceiling because the easy dedups are already taken.

### 4.7 Approach 3 (LLM-assisted) is low-leverage here

The primer §5 matrix row for Roadmaps explicitly says "LLM rewriting offers little marginal gain on already-structured content". This file's structural regularity is high, prose regularity is high, and the remaining prose compression opportunity is in the Validation Result narratives (S7), which is deterministic enough for Approach 2. Approach 3 should be used only for S9, and only if the 22% target is insufficient.

### 4.8 INV-1, INV-3, INV-5 carry-forward

Per primer §6, all three unresolved invariants from the adversarial-validated study apply:

- **INV-1**: All byte estimates above are in raw bytes, not tokens. The primer warns of ±2-8 pp drift when re-measured against Claude's native tokenizer. The projected 22% byte compression could land anywhere from ~14% to ~30% in tokens.
- **INV-3**: Consumer DAG for this specific file is not instrumented. The conventions-header amortization argument (§4.3 above) is qualitative, not quantitative.
- **INV-5**: If any downstream Haiku consumer reads this file, default to uncompressed per the primer's Haiku caveat.

---

## Summary

- **File**: 73,076 bytes / 1,456 lines, hybrid roadmap-ish multi-proposal document with ~25% code-fence content and high structural regularity across 5 replicated gap skeletons.
- **Approach**: Primer §5 "Roadmap" row with §5 rule 2 (fence preservation) as the binding constraint and §4.2 (AST-aware) as the primary lever; §4.1 Approach 1 freebies are mostly already extracted.
- **Recommended stack**: 12 strategies, ordered by safety, producing ~12% lossless compression (stop at S6/S10/S4/S3) or ~21-22% with one auditor-gated lossy step (S7) for Validation-narrative compaction.
- **Largest single lever**: Strategy 3 (conventions header for top 12 repeated identifiers), ~5.9% of file, must be fence-gated (Approach 2 only).
- **Largest lossy lever**: Strategy 7 (Validation-narrative compaction), ~8.7% of file, justified only because the file lives in `.dev/releases/complete/` (archived).
- **Projected ceiling**: ~22% bytes (below the primer's 25-33% Roadmap target because ~25% of the file is sacrosanct code fences and the whitespace freebies are already extracted).
