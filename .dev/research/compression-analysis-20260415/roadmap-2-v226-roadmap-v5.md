# Compression Analysis: v2.26-roadmap-v5/roadmap.md

**Date**: 2026-04-15
**Target**: `/config/workspace/IronClaude/.dev/releases/complete/v2.26-roadmap-v5/roadmap.md`
**Primer**: `/config/workspace/IronClaude/claudedocs/compressed-markdown-dsl-primer.md`
**Document type**: Roadmap (per primer §5 matrix: Approach 2 AST-aware + optional conventions header, target 25–33%)

---

## 1. File Inventory

| Metric | Value |
|---|---|
| Path | `.dev/releases/complete/v2.26-roadmap-v5/roadmap.md` |
| Size (bytes) | 35,042 |
| Lines | 520 |
| YAML frontmatter | Lines 1–5 (5 lines) |
| ATX headings (`#`/`##`/`###`/`####`) | ~52 headings |
| Horizontal rules (`---` outside frontmatter) | 8 occurrences as phase separators |
| Pipe tables | 7 tables (3 risk tables, Files Modified, Parallelization, SC Mapping, Timeline Summary) |
| Fenced code blocks | **0** (important: no fenced code to protect) |
| Inline code spans (backticks) | ~180+ occurrences (file names, function names, identifiers) |
| Emoji | 0 |
| Requirement-ID tokens (`FR-###`, `NFR-###`) | ~140 distinct references |
| Other ID tokens (`OQ-[A-J]`, `SC-##`, `R-##`, `DEV-###`, `D-##`) | ~70 references |

### Composition breakdown (approximate %)

| Category (per primer §2.3) | Estimated share of bytes | Notes |
|---|---:|---|
| Headings (ATX, bold labels like `**Goal**:`) | ~7% | Phase sub-section labels are repeated every phase |
| Structural prose (phase intros, rationale) | ~38% | Paragraph-length narrative inside every phase |
| Pipe tables | ~22% | Three risk tables share column schema; Files Modified, Timeline, SC Mapping tables |
| Task-list bullets (`- [ ]` exit criteria) | ~14% | Repeats across phases |
| Inline-code identifiers (file/function names) | ~8% | Load-bearing; not safe to abbreviate without header |
| Requirement parenthetical chains (`(FR-013, FR-070, FR-085)`) | ~5% | Dense, highly compressible |
| Whitespace & blank lines | ~4% | Standard single-blank separation, no 3+ runs observed |
| Decorative horizontal rules | ~1% | 8 `---` separators |
| YAML frontmatter | <1% | Small and semantically live |

### Repeating patterns suitable for a conventions header (primer §2.2)

- `**Goal**:`, `**Duration estimate**:`, `**Dependencies**:` occur once per phase (6 phases)
- `### Phase N Exit Criteria` occurs 6 times
- `**Requirements covered**:` occurs in Phases 1 and 2
- `spec-deviations.md`, `deviation-analysis.md`, `spec-fidelity.md`, `roadmap.md`, `debate-transcript.md`, `diff-analysis.md` — each referenced 6–15 times
- `annotate-deviations`, `deviation-analysis` step names — 10+ occurrences each
- `remediation_attempts`, `roadmap_hash`, `_check_annotate_deviations_freshness()`, `_print_terminal_halt()`, `parse_frontmatter()`, `_parse_routing_list()` — each 4–8 occurrences
- `INTENTIONAL_IMPROVEMENT`, `PRE_APPROVED`, `SLIP`, `AMBIGUOUS` — 10+ occurrences each
- `SPEC_FIDELITY_GATE`, `CERTIFY_GATE`, `ANNOTATE_DEVIATIONS_GATE`, `DEVIATION_ANALYSIS_GATE` — 4–6 each
- `FR-###` IDs: 140+ total references; many phases repeat the same requirement IDs

---

## 2. Strategies Identified

### Strategy 1 — Rule-based blank line & trailing whitespace normalization (primer §4.1, Approach 1 transforms #1–2)

**Description**: Apply Approach-1 rule-based pass to strip trailing whitespace and ensure no 3+ blank-line runs. Though this file appears reasonably tidy, a normalization sweep is free.

**Before** (lines 27–29, with a 1-blank separator preserved):
```
...after Phase 0 completion with actual OQ resolution outcomes. Proceed to release only after Phase 5 evidence review — code-complete status is not a release gate.

---
```

**After**: Same; blank lines already collapsed. Still strip any trailing spaces on 520 lines.

**Savings**: Low on this file — ~40–80 bytes (0.1–0.3%). The file is already tidy.
**Lossless**: Yes (primer §2.1 table).
**Risk**: None. File has no code fences to damage.

---

### Strategy 2 — Remove decorative phase-separator horizontal rules (primer §2.3 "decorative elements"; Approach 1 transform #4)

**Description**: The 8 `---` horizontal rules (lines 28, 85, 154, 238, 301, 345, 400, 431, 473, 501) act purely as visual phase separators between `## Phase N` headings. The ATX heading itself is the semantic boundary; the rule is decorative.

**Before** (lines 83–87):
```
- [ ] Architecture constraint verification complete against live codebase

---

## Phase 1: Foundation — Data Model, Parsing, and Gate Infrastructure
```

**After**:
```
- [ ] Architecture constraint verification complete against live codebase

## Phase 1: Foundation — Data Model, Parsing, and Gate Infrastructure
```

**Savings**: 8 occurrences × ~5 bytes (`\n---\n`) + blank-line absorption ≈ 60–80 bytes, plus reclaimed structural blank lines ≈ ~120 bytes total (0.3–0.4%).
**Lossless**: Yes (primer §2.1 "Remove decorative headers").
**Risk**: Very low. If a downstream renderer relied on `<hr>` for ToC generation, navigation could degrade — but this file is LLM-consumed.

---

### Strategy 3 — Collapse bold-label metadata lines into a compact inline form (primer §4.2, Approach 2 transform #3 "List compaction")

**Description**: Every phase begins with three bold-label lines:
```
**Goal**: …
**Duration estimate**: …
**Dependencies**: …
```
Via AST-aware transform these collapse into a single blockquote or dash list, saving repeated `**`/newlines across 6 phases.

**Before** (lines 32–36):
```
**Goal**: Establish implementation constraints, resolve deferred architecture decisions, and freeze the intended design before modifying any behavior.

**Duration estimate**: 0.5–1.5 days

**Dependencies**: None
```

**After** (compact triple-field bullet using conventions header abbreviations `G=Goal D=Duration Dep=Dependencies`):
```
- G: Establish implementation constraints, resolve deferred architecture decisions, and freeze the intended design before modifying any behavior.
- D: 0.5–1.5 days
- Dep: None
```

**Savings**: Per phase: ~30 bytes (removes `**...**` × 3, two blank lines → zero). × 6 phases ≈ 180–240 bytes (~0.6%).
**Lossless**: Yes — labels are abbreviated via conventions header; semantics preserved (primer §2.1 "Abbreviate via conventions header").
**Risk**: Low. If Phase 0 has no `Dependencies: None` line, do not invent one.

---

### Strategy 4 — Conventions-header abbreviations for heavy-use artifact/function names (primer §2.2 conventions header; Approach 2 transform #5 "Front-matter → conventions-header synthesis")

**Description**: The primer explicitly calls out auto-generating a conventions header from phrases that occur `>5 times` and are `>20 chars`. Several qualify in this file. A single header block pays for itself after ~5 body uses (primer §2.2).

**Proposed header** (inserted between YAML frontmatter and `# v2.25 Roadmap…`):
```
<!-- cmd-dsl v1:
[SD]=spec-deviations.md [DA]=deviation-analysis.md [SF]=spec-fidelity.md
[DT]=debate-transcript.md [DIFF]=diff-analysis.md [RM]=roadmap.md
[AD]=annotate-deviations [DAN]=deviation-analysis [RH]=roadmap_hash
[RA]=remediation_attempts [PF]=parse_frontmatter [PRL]=_parse_routing_list
[SFG]=SPEC_FIDELITY_GATE [CG]=CERTIFY_GATE [ADG]=ANNOTATE_DEVIATIONS_GATE [DAG]=DEVIATION_ANALYSIS_GATE
[II]=INTENTIONAL_IMPROVEMENT [PA]=PRE_APPROVED [SL]=SLIP [AM]=AMBIGUOUS
-->
```

**Before** (line 196):
```
1. Add `annotate-deviations` step in `_build_steps()` between `merge` and `test-strategy` (FR-004)
   - Inputs: `spec_file`, `roadmap.md`, `debate-transcript.md`, `diff-analysis.md`
   - Output: `spec-deviations.md`
   - Gate: `ANNOTATE_DEVIATIONS_GATE` (STANDARD), timeout 300s, retry_limit=0
```

**After**:
```
1. Add `[AD]` step in `_build_steps()` between `merge` and `test-strategy` (FR-004)
   - Inputs: `spec_file`, `[RM]`, `[DT]`, `[DIFF]`
   - Output: `[SD]`
   - Gate: `[ADG]` (STANDARD), timeout 300s, retry_limit=0
```

**Savings** (per-phrase × occurrence count × bytes saved):
- `spec-deviations.md` → `[SD]` (−15B × ~13 occurrences ≈ 195B)
- `deviation-analysis.md` → `[DA]` (−17B × ~10 ≈ 170B)
- `spec-fidelity.md` → `[SF]` (−13B × ~8 ≈ 104B)
- `debate-transcript.md` → `[DT]` (−16B × ~6 ≈ 96B)
- `diff-analysis.md` → `[DIFF]` (−11B × ~6 ≈ 66B)
- `annotate-deviations` → `[AD]` (−16B × ~12 ≈ 192B)
- `deviation-analysis` (step) → `[DAN]` (−15B × ~10 ≈ 150B)
- `ANNOTATE_DEVIATIONS_GATE` → `[ADG]` (−20B × ~5 ≈ 100B)
- `DEVIATION_ANALYSIS_GATE` → `[DAG]` (−19B × ~6 ≈ 114B)
- `SPEC_FIDELITY_GATE` → `[SFG]` (−14B × ~5 ≈ 70B)
- `CERTIFY_GATE` → `[CG]` (−8B × ~5 ≈ 40B)
- `INTENTIONAL_IMPROVEMENT` → `[II]` (−18B × ~6 ≈ 108B)
- `PRE_APPROVED` → `[PA]` (−8B × ~7 ≈ 56B)
- `parse_frontmatter`/`_parse_routing_list` (−10B × ~6 ≈ 60B)
- Other gate/function names (~100B)

Gross savings ≈ 1,600–1,800 bytes. Header cost ≈ 380 bytes.
**Net savings**: ≈ **1,200–1,400 bytes (~3.5–4.0%)**.
**Lossless**: Yes, conditional on header presence (primer §2.1, §2.2).
**Risk**: Amortization requires ≥5 reads (primer §2.2 + INV-3, primer §6). Also, abbreviating file paths inside the document can confuse humans; reversible only with the header. Must ensure the abbreviation tokens (`[SD]`, `[AD]`) do not collide with existing Markdown link syntax. For this file there is no `[SD]:` reference-link target, so collision-safe.

---

### Strategy 5 — Abbreviate the repeated requirement-ID fan-out lines (primer §4.2, Approach 2 transform #4 "Cross-reference deduplication")

**Description**: Two very long lines enumerate requirements covered per phase. Phase 1 (line 138) lists 19 FR/NFR IDs; Phase 2 (line 224) lists 44 IDs. These are primarily LLM-consumed provenance, and the same IDs also appear inline at individual bullets. The AST transform detects cross-references already cited inline and keeps only the non-redundant remainder, or replaces the full list with a terse footer.

**Before** (line 138):
```
**Requirements covered**: FR-013, FR-014, FR-015, FR-026, FR-027, FR-028, FR-029, FR-046, FR-053, FR-054, FR-056, FR-057, FR-070, FR-074, FR-079, FR-080, FR-081, FR-085, FR-086, NFR-007, NFR-021
```

**After** (condensed-range form; same bytes-per-ID reduced ~40%):
```
**Req**: FR-013..015,026..029,046,053,054,056,057,070,074,079..081,085,086; NFR-007,021
```

**Savings**:
- Line 138 (Phase 1): 247B → ~108B ≈ 139B saved
- Line 224 (Phase 2): ~520B → ~215B ≈ 305B saved
- Line 286 (Phase 3): ~260B → ~110B ≈ 150B saved

Total ≈ **~590 bytes (~1.7%)**.
**Lossless**: Yes — every ID recoverable from the range notation (primer §2.1 "Abbreviate via conventions header" combined with explicit enumeration).
**Risk**: Low. Range notation (`FR-013..015`) is unambiguous but non-standard; must be declared in the conventions header so the LLM reads `..` as a range operator. If the downstream agent uses regex-based ID extraction, it must support range expansion.

---

### Strategy 6 — Table normalization: hoist repeating column values (primer §4.2, Approach 2 transform #2 "Table normalization")

**Description**: Three risk tables (HIGH / MEDIUM / LOW) share the **exact** same 7-column schema (`ID | Risk | Severity | Probability | Phase | Mitigation | Validation Evidence`). The `Severity` column is constant within each sub-table (HIGH, MEDIUM, or LOW). That column can be hoisted into a caption and dropped from the rows.

**Before** (line 408–411, partial):
```
| ID | Risk | Severity | Probability | Phase | Mitigation | Validation Evidence |
|----|------|----------|-------------|-------|------------|---------------------|
| R-1 | Deviation laundering / over-approval | HIGH | LOW | 2 | Separate subprocess; … | … |
| R-2 | Resume/freshness corruption | HIGH | MEDIUM | 3 | Atomic `roadmap_hash` injection; … | … |
| R-3 | Routing/frontmatter parsing fragility | MEDIUM | MEDIUM | 2 | Flat comma-separated fields only; … | … |
```
(Note: R-3 is in the HIGH table in the source but labeled MEDIUM — a pre-existing data quirk to preserve.)

**After** (hoist Severity column; three sub-tables collapse into one with explicit severity-group divider, or keep three sub-tables each with one fewer column):
```
### Risks (Severity=HIGH)
| ID | Risk | Prob | Phase | Mitigation | Evidence |
|--|--|--|--|--|--|
| R-1 | Deviation laundering / over-approval | LOW | 2 | Separate subprocess; … | … |
| R-2 | Resume/freshness corruption | MEDIUM | 3 | Atomic `[RH]` injection; … | … |
```

**Savings**:
- Drop one column across ~11 rows × ~12B avg = ~130B
- Shorten column headers (`Probability` → `Prob`, `Validation Evidence` → `Evidence`): ~20B per table × 3 = ~60B
- Table padding collapse (Approach 1 transform #6): remove intra-cell padding spaces, ~50B
- Also applies to Files Modified table (line 437–448, 9 rows): ~40B
- SC Mapping table (line 488–499, 10 rows): column header shortening ≈ ~30B
- Timeline Summary table (line 505–512, 6 rows): header shortening ≈ ~20B

Total table normalization ≈ **~330 bytes (~0.9%)**.
**Lossless**: Yes (primer §2.3 "Table whitespace", §4.2 transform #2).
**Risk**: Collapsing Severity into a caption changes the join key downstream code would use. Must verify no tool parses this table expecting the Severity column. Also, visually less scannable for humans reading the raw MD.

---

### Strategy 7 — Drop or compress Executive Summary prose restatement (primer §4.2, Approach 2 transform #6 "Prose summarization of introduction paragraphs")

**Description**: Lines 11–26 (Executive Summary) restate content that is then fully re-articulated in the per-phase sections, the Risk Assessment, and the Timeline Summary. Per primer §4.2 transform #6, when an introduction restates content found verbatim later, elide the restated sentences. The "Key architectural properties" bullet list (lines 17–22) is independently useful and should be retained.

**Before** (lines 11–15):
```
v2.25 introduces a **deviation-aware fidelity subsystem** into the roadmap pipeline, solving a systematic failure where intentional architectural improvements were misclassified as specification violations, causing pipeline halts and futile remediation cycles.

The solution adds two new pipeline steps (`annotate-deviations`, `deviation-analysis`) and modifies three existing components (`spec-fidelity`, `remediate`, `certify`), all built on existing executor primitives. The architecture follows a **classify → route → act** pattern: deviations are annotated against the debate record, classified by intent, routed to appropriate handlers (fix, spec-update, no-action, human-review), and only genuine SLIPs reach remediation.

**Delivery strategy**: The primary failure mode of this pipeline is not that valid slips fail to remediate — it is that invalid intentional classifications silently pass. Negative validation (what the pipeline refuses to do) is treated as the primary correctness boundary, not an equivalent to positive validation. Release is blocked on evidence, not implementation confidence.
```

**After** (keep delivery-strategy claim that is load-bearing and not restated verbatim downstream; drop the first two paragraphs which are covered by Phase 1–3 and the Risk Assessment):
```
Pattern: classify → route → act. Adds 2 steps ([AD], [DAN]); modifies [SF], remediate, certify. Only [SL] reaches remediation.

**Delivery**: Negative validation is the primary correctness boundary. Release blocked on evidence, not code-complete.
```

**Savings**: ~780B → ~220B ≈ **560 bytes (~1.6%)**.
**Lossless**: **Lossy** — this is primer §4.2 transform #6 which is bounded but not strictly lossless. The deleted sentences are recoverable from the body, so LLM-task-equivalence holds (primer §2.1 "task-equivalent").
**Risk**: Medium. If a downstream consumer reads *only* the Executive Summary (e.g., a dashboard snippet), truncation loses the framing. Requires INV-3 consumer DAG check (primer §6). For a release-artifact roadmap that is read cover-to-cover, safe.

---

### Strategy 8 — Compact the dense exit-criteria task lists (primer §4.2, Approach 2 transform #3 "List compaction")

**Description**: Every phase ends with `- [ ]` task-list exit criteria — 6 phases × ~8–11 items. Each item is a single-sentence assertion. Multi-paragraph bullets are already absent here, but the bullets include decorative bold labels and repeated phrasing ("verified with", "passes all", "confirmed by"). An AST pass can canonicalize phrasing.

**Before** (lines 141–153):
```
- [ ] `Finding("test", deviation_class="SLIP")` constructs successfully
- [ ] `Finding("test", deviation_class="INVALID")` raises `ValueError`
- [ ] `Finding("test")` defaults to `"UNCLASSIFIED"`
- [ ] All 9+ semantic check functions pass unit tests with boundary inputs — including **missing**, **malformed**, and **failing-value** cases with distinct log messages
```

**After** (strip the task-list checkbox to `-` since no machine is checking them, and canonicalize "semantic check functions" etc.):
```
- `Finding("test", deviation_class="SLIP")` constructs
- `Finding("test", deviation_class="INVALID")` raises ValueError
- `Finding("test")` defaults to "UNCLASSIFIED"
- 9+ gates.py checks: unit tests cover missing/malformed/failing-value with distinct logs
```

**Savings**: Dropping `[ ] ` is 4B per item × ~55 items ≈ 220B; canonicalization of recurring phrases ≈ 150B. Total ≈ **~370 bytes (~1.1%)**.
**Lossless**: The `- [ ]` vs `-` distinction is load-bearing if the release process uses GFM task-list state. If checklists are rendered for human tracking, this strategy is **lossy** for the human workflow; task-equivalent for LLM. Must confirm via consumer DAG.
**Risk**: GFM task-list semantics (primer §4.2 risk note on GFM plugins). Skip if release process renders task lists.

---

### Strategy 9 — Inline-code span trimming for monospace identifiers used inside conventions-header abbreviations (primer §4.1 Approach 1 transform #6 + §2.2 header amortization)

**Description**: Backtick-quoted file and function names become double-cost when they also appear in conventions-header abbreviations (Strategy 4). Once `[AD]` replaces `` `annotate-deviations` ``, the backticks go too — a further 2B per occurrence.

**Before**: `` `annotate-deviations` `` (22B)
**After**: `[AD]` (4B, no backticks)

**Savings**: Counted inside Strategy 4 above. Calling this out separately to remind that backticks are an additional ~2B × ~80 occurrences ≈ 160B of free savings rolled into Strategy 4.
**Lossless**: Yes, conditional on conventions header.
**Risk**: If the abbreviation expansion is re-rendered, identifiers lose their code-span styling. LLM consumers are insensitive to this.

---

### Strategy 10 — Bold-label compaction for phase field metadata (primer §4.1 Approach 1 transform #10 + §4.2 transform #3)

**Description**: Labels like `**Requirements covered**:`, `**Goal**:`, `**Duration estimate**:` consume 4B overhead each (two pairs of `**`). With the conventions header in place, these become single-letter prefixes (`R:`, `G:`, `D:`, `Dep:`).

**Before** (line 224, start):
```
**Requirements covered**: FR-002, FR-003, …
```

**After** (combined with Strategy 5):
```
R: FR-002..010,012,016..025,033..038,045,055,058,073,075,078,082,083,087,089,090; NFR-002,022..024
```

**Savings**: Already counted in Strategies 3 and 5; highlight ~4B × ~20 bold-label occurrences ≈ 80B beyond those strategies. Negligible on its own but tidy.
**Lossless**: Yes.
**Risk**: None beyond Strategy 4's header dependency.

---

### Strategy 11 — Frontmatter compaction & inline meta-line merge (primer §2.3 "Preamble & meta")

**Description**: The existing YAML frontmatter (3 fields) is already minimal. No action needed — flagged as **not applicable** to confirm the primer category was considered.

**Savings**: 0.
**Lossless**: N/A.
**Risk**: N/A — listing for completeness.

---

## 3. Recommended Strategy Stack

Apply in this order per primer §5 pipeline composition rules (§5: "Always run Approach 1 first… Code fences are sacrosanct… Run Approach 2 when structural regularity > prose density").

| Order | Strategy | Approach | Lossless? | Est. bytes saved | Cumulative % |
|---:|---|---|---|---:|---:|
| 1 | Strategy 1: blank / trailing whitespace normalization | §4.1 | Yes | ~60 | 0.2% |
| 2 | Strategy 2: remove decorative `---` separators | §4.1 | Yes | ~120 | 0.5% |
| 3 | Strategy 6: table column hoist + padding collapse | §4.2 | Yes | ~330 | 1.4% |
| 4 | Strategy 8: exit-criteria list compaction (GFM-safe subset only) | §4.2 | Conditionally lossless | ~220 | 2.0% |
| 5 | Strategy 3: phase-header bold-label → compact bullet | §4.2 | Yes (with header) | ~200 | 2.6% |
| 6 | Strategy 4 + 9 + 10: synthesize conventions header & apply abbreviations | §4.2 #5 | Yes (with header) | ~1,300 | 6.3% |
| 7 | Strategy 5: requirement-ID range condensation | §4.2 #4 | Yes (with header-declared range operator) | ~590 | 8.0% |
| 8 | Strategy 7: Executive Summary redundancy elision | §4.2 #6 | Lossy (task-equivalent) | ~560 | 9.6% |

**Total projected savings (bytes)**: ~3,380 of 35,042 ≈ **9.6%** on rule + AST alone.

### Why this is below the primer's 25–33% roadmap target

This file is already unusually well-written:
- Zero fenced code blocks (no code-comment compression)
- Zero emoji (no decorative stripping)
- No duplicated heading sections (no §4.2 transform #1 heading-dedup wins)
- No paragraph-in-bullet structures (§4.2 transform #3 mostly doesn't apply)
- No redundant cross-references like "(see Section X.Y)" (no transform #4 wins)
- Prose is dense and largely non-restating (Strategy 7 is the only prose elision win)
- Inline-code identifiers dominate the token surface; the conventions header is the only strong lever

**The primer's 25–33% ceiling assumes roadmaps with typical restated introductions, emoji, and repeated "see section N" pointers.** This document has already had much of that redundancy removed by hand. The realistic AST-aware ceiling for *this specific file* is closer to **9–12%**, not 25–33%.

### If additional compression is desired: escalate to Approach 3 (primer §4.3)

An LLM-assisted pass (primer §4.3) applied *only* to the prose-dense sections (Executive Summary, phase Goal paragraphs, Risk Assessment mitigations, Negative Validation Release Blockers intro) could add another 5–8%, bringing the total to **~15–18%**. This is primer §5 TDD guidance ("Apply approaches surgically to prose regions"). The auditor-pass requirement (primer §4.3 constraint #6) is mandatory because the file contains normative "refuse"-class assertions (lines 315–323) where a factual drift would be release-blocking.

### Stop here if

- The file will be read fewer than 5 times by Claude (primer §2.2: header does not amortize → cancel Strategies 4/5/10).
- The downstream consumer preserves GFM task-list state (cancel Strategy 8).
- Human reviewers must read the raw file (cancel Strategies 4, 5, 7).

---

## 4. Risks & Caveats Specific to This File

### Blockers / show-stoppers (investigate before applying)

1. **Consumer DAG is unknown (primer §6 INV-3).** The file lives under `.dev/releases/complete/` — the directory name suggests archival. Archival files are read fewer times than active roadmaps; the conventions-header amortization (Strategy 4) may not pay off. **Do not apply Strategy 4 until read-count is confirmed ≥5 per lifecycle.**

2. **Tokenizer drift (primer §6 INV-1).** All byte savings above are *bytes*, not Claude-native tokens. Claude's tokenizer can merge or split on punctuation differently from `cl100k_base`. A conventions header saturated in `[AD]`/`[DA]`/`[SD]` tokens may tokenize *worse* than the original file and function names, because short-bracketed abbreviations often split into 2–3 tokens each. **Measure with `messages.count_tokens` before committing.**

3. **Normative language in Phase 4 "Negative Validation Release Blockers" (lines 311–323).** These five "Refuse X" items are release-contract assertions. Per primer §5 ("Specs should never exceed Approach 1… fidelity > savings"), the Phase 4 Negative Validation section should be **excluded** from Strategies 3, 5, 7, and 8. Apply only Strategies 1, 2, 6 to that region.

4. **Requirement-ID range notation (Strategy 5) is non-standard.** `FR-013..015` reads as a range only if the conventions header declares it. If any downstream consumer extracts requirement IDs via `FR-\d{3}` regex, range notation will under-match. Strategy 5 must ship with a conventions-header declaration AND a compatibility check of any requirement-extraction tooling (e.g., `sc:validate-roadmap`).

### Secondary caveats

5. **GFM task-list preservation.** Exit-criteria lists (Strategy 8) use `- [ ]`. If the release workflow converts these into tracked items in an issue tracker, stripping the checkbox is destructive. Confirm via release pipeline inspection before applying.

6. **Inline code-span backticks are load-bearing for some readers.** Stripping backticks around identifiers (Strategy 9) is safe for LLMs but breaks syntax highlighting in Markdown renderers. Acceptable here because the file is LLM-consumed in the release pipeline.

7. **Table column hoist (Strategy 6) changes table shape.** If any tool (including a downstream `/sc:validate-roadmap` gate check) asserts column counts or column names on the three risk tables or the Files Modified table, Strategy 6 will cause gate failure. Review `gates.py` semantic checks that touch risk tables before applying.

8. **Horizontal rule removal (Strategy 2) affects anchor generation.** Some Markdown processors generate implicit section boundaries at `---`. For LLM consumption and for the IronClaude pipeline, this is not load-bearing — but if a docs renderer pulls this file, ToC/anchor behavior may change.

9. **Executive Summary elision (Strategy 7) is the only lossy strategy in the stack.** It is justifiable under primer §2.1 (task-equivalent losslessness) but fails strict byte-for-byte losslessness. Gate it behind an auditor pass (primer §4.3 constraint #6) even though the strategy itself is AST-level, because the summary contains the only statement of `Delivery strategy` framing not duplicated elsewhere.

10. **No fenced code blocks means Approach 1 regex transforms are safe here** — this is unusual for a TDD but typical for roadmaps. The primer's "code fences are sacrosanct" rule (§5 rule #2) is trivially satisfied. No special code-fence handling required.

### Strategies explicitly rejected

- **LLM-assisted rewriting of the entire document (primer §4.3 applied broadly)**: rejected because the file contains release-contract language (Phase 4 refusal behaviors, NFR-009/010 zero-modification assertions) where hallucinated paraphrase risk outweighs marginal byte savings. Apply Approach 3 only to the four prose-dense regions called out above, and only under an auditor pass.
- **Heading deduplication (primer §4.2 transform #1)**: rejected. No duplicate headings detected in the source.
- **Mermaid/plantuml drop (primer §4.2 transform #7)**: N/A. No diagrams in this file.
- **Auto-abbreviation of requirement IDs themselves (`FR-013` → `F13`)**: rejected. Requirement IDs are the primary join keys for traceability across this document and downstream validation; abbreviating them would complicate the invariants that `_check_…` functions rely on.

---

**Bottom line**: This roadmap is already tightly written. The realistic AST-aware compression ceiling for this file is **~9–12%** (primer §4.2 Approach 2), well below the generic roadmap-class target of 25–33%. To exceed 12%, a surgical Approach 3 pass on four named prose regions is required (+5–8%), gated by an auditor pass. The conventions-header amortization (Strategy 4) is the single largest lever at ~4% but is conditional on INV-3 consumer-DAG confirmation that the file is read ≥5 times. All projected savings remain provisional until re-measured against Claude's native tokenizer per INV-1.
