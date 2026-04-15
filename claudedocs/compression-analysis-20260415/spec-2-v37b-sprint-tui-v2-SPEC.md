# Compression Analysis: v3.7b-sprint-tui-v2-SPEC.md

**Date**: 2026-04-15
**Target**: `/config/workspace/IronClaude/.dev/releases/backlog/v3.7-task-unified-v2/release-split/v3.7b-sprint-tui-v2-SPEC.md`
**Primer**: `/config/workspace/IronClaude/claudedocs/compressed-markdown-dsl-primer.md`
**Document class**: SPEC (per primer §5, row 3 — **Approach 1 ONLY**, 10-15% ceiling, fidelity floor: near-lossless)

---

## 1. File Inventory

| Metric | Value |
|--------|------:|
| Path | `.dev/releases/backlog/v3.7-task-unified-v2/release-split/v3.7b-sprint-tui-v2-SPEC.md` |
| Bytes | 84,284 |
| Lines | 1,437 |
| Words | ~10,023 |
| Heading count (ATX) | 64 |
| Setext headings (`===`/`---` underline) | 0 |
| Horizontal rules | 1 (line 1395) |
| Trailing-whitespace lines | 0 (already clean) |
| YAML front matter | Wrapped inside a ` ```yaml ` code fence (lines 1-21) |

### 1.1 Composition breakdown (line-level)

| Category | Lines | % of file | Notes |
|----------|------:|----------:|-------|
| Code-fence content (including fences) | 599 | 41.7% | Python snippets, bash, workflow ASCII diagram, YAML front matter (mis-wrapped in a fence) |
| Blank lines | 274 | 19.1% | High — target for whitespace pass |
| Pipe-table rows | 184 | 12.8% | 10+ tables: Evidence, Decisions, Arch files, NFRs, Risks, Tests (Unit+Int+E2E), Open Items, Gap Analysis, Glossary, References, Integration Points |
| Bullet list items | 197 | 13.7% | Mostly `**Acceptance Criteria**` checklists and In/Out-of-scope lists |
| ATX headings (`#`..`####`) | 64 | 4.5% | Sections 1-12 + Appendices A/B/C; 17 per-FR subsections (FR-37B.1 … FR-37B.17) |
| Prose / misc | ~119 | 8.2% | Problem Statement, Solution Overview paragraphs, Description fields |

Percentages sum to >100% because bullet-list lines overlap with "under headings" counting; the practical distribution is: **~40% code**, **~20% blank**, **~15% tables**, **~15% bullets**, **~5% headings**, **~5% prose**.

### 1.2 Repeated structural patterns (abbreviation candidates)

Extracted verbatim via frequency count (primer §2.2 — conventions header candidates):

| Phrase | Occurrences | Approx chars per hit |
|--------|-----------:|---------------------:|
| `MonitorState` | 79 | 12 |
| `tests/sprint/` | 78 | 14 |
| `TaskResult` | 53 | 10 |
| `FR-37B` | 49 | 6 |
| `PhaseAccumulator` | 44 | 16 |
| `PhaseResult` | 42 | 11 |
| `tui.py` | 41 | 6 |
| `models.py` | 32 | 9 |
| `summarizer.py` | 28 | 13 |
| `Haiku` | 27 | 5 |
| `executor.py` | 26 | 11 |
| `SummaryWorker` / `PhaseSummarizer` | 22 / 22 | 13 / 15 |
| `SprintConfig` | 20 | 12 |
| `SprintResult` | 18 | 12 |
| `Strategy B` | 12 | 10 |
| `Acceptance Criteria` (label) | 17 | 19 |
| `Verification contract` (label) | 17 | 21 |
| `Commit boundary` (label) | 17 | 15 |
| `Rollback plan` (label) | 18 | 13 |
| `Current code` (label) | 17 | 12 |
| `Dependencies` (label) | 18 | 12 |

**Observation**: The 17-way repetition of the six per-FR structural labels (~100 label instances × ~15 chars avg ≈ 1.5 KB) and the ~560 instances of class/filename identifiers (~6-8 KB) are the dominant redundancy surface. Under a SPEC fidelity floor, only the structural labels are safe to abbreviate (labels are schema, not normative content); class/file names are load-bearing identifiers and MUST NOT be abbreviated (see §4 Risks).

---

## 2. Strategies Identified

All strategies are grounded in the primer. Per primer §5 row 3 and §4.1, **Approach 1 (rule-based textual compression)** is the only approach permitted on specs — Approach 2 (AST) and Approach 3 (LLM rewriting) are explicitly excluded because "the fidelity cost of AST/LLM transforms on normative language is too high" (primer §5 "Compression pipeline composition rules", rule 5).

Every strategy below is therefore a rule-based transform and is mapped to:
- a specific Approach-1 transform from primer §4.1 (numbered 1-10), **or**
- a specific §2.3 redundancy category.

### 2.1 Strategy S1 — Collapse 3+ blank lines → 1 blank line (outside code fences)

**Primer citation**: §4.1 transform 1 ("Collapse 3+ blank lines → 2 blank lines"). Tightened to "→ 1 blank line" because there is no consumer that depends on paragraph visual separation width; Markdown parsers treat 1 and 2 blank lines identically for block separation. This is still §2.3 "Whitespace & formatting".

**Target in this file**: 274 blank lines (19.1% of the file). Spot check of the actual file shows almost no runs of 3+ blank lines (author already uses single blanks between paragraphs), so the conservative §4.1 form will save little; the tightened "all inter-block blank runs → 1" variant is needed to capture meaningful savings.

**Before** (lines 22-24, 38-40):
```
```
(line 21)

## 1. Problem Statement

The sprint TUI...
```

**After** (same region with single-blank normalization — identical rendering):
```
```
(line 21)
## 1. Problem Statement
The sprint TUI...
```

Wait — removing the blank before a heading can affect some strict CommonMark parsers. Keep the blank *before* ATX headings and before fenced code; collapse only runs of **2+ blank lines → 1 blank line** elsewhere.

**Estimated savings**: In a file already averaging ~1 blank between blocks, the narrow primer-faithful rule (§4.1 form: 3+ → 2) would save <50 bytes. The widened form (2+ → 1, preserving blanks adjacent to headings/fences) saves an estimated **~100-180 bytes** (~0.2%). The savings here are small because the author is already disciplined.

**Lossless?** Yes — pure whitespace; no CommonMark semantic change when headings/fences retain their leading blank.

**Risks on this file**: Code fences contain ASCII-art diagrams (§2.2 Workflow / Data Flow, lines 92-179) whose vertical spacing is meaningful to readers. The rule MUST respect fence boundaries (primer §4.1 risks list). A fence-unaware regex would corrupt the diagram. Implementation must track fence state.

### 2.2 Strategy S2 — Strip trailing whitespace

**Primer citation**: §4.1 transform 2.

**Target**: 0 lines have trailing whitespace (verified). **Savings: 0 bytes.** Include in pipeline for discipline but expect no reduction on this file.

**Lossless?** Yes. **Risk**: none.

### 2.3 Strategy S3 — Normalize setext → ATX headings

**Primer citation**: §4.1 transform 3.

**Target**: 0 setext headings (verified — all 64 headings are already ATX). **Savings: 0 bytes.**

**Lossless?** Yes. **Risk**: none. Include for completeness.

### 2.4 Strategy S4 — Remove decorative horizontal rules

**Primer citation**: §4.1 transform 4 + §2.3 "Decorative elements".

**Target**: 1 HR at line 1395 (between §12 Brainstorm Gap Analysis and "## Appendix A"). It is not adjacent to YAML front matter. It is purely visual.

**Before**:
```

---

## Appendix A: Glossary
```

**After**:
```

## Appendix A: Glossary
```

**Savings**: ~5 bytes. Trivial on this file.

**Lossless?** Yes — the following ATX heading fully denotes the section boundary.

**Risk**: none. The file has only one HR and it is decorative.

### 2.5 Strategy S5 — Strip emoji from headings (allowlist pass)

**Primer citation**: §4.1 transform 5 + §2.3 "Decorative elements".

**Target**: spot check shows **no emoji in headings or body** of this file (the author is disciplined). **Savings: 0 bytes.** Include for pipeline consistency; no-op here.

### 2.6 Strategy S6 — Collapse pipe-table column padding

**Primer citation**: §4.1 transform 6 + §2.3 "Table whitespace".

**Target**: 184 table rows across ~12 tables. Spot check of §1.2 Evidence table (lines 31-38), §8.1 Unit Tests table (~70 rows, lines 1256-1326), and Appendix C Integration Points (lines 1425-1436).

**Before** (line 1258, representative, showing inter-cell padding):
```
| 1  | `test_phase_accumulator_init_defaults`                            | `tests/sprint/test_phase_accumulator.py` | PhaseAccumulator fields initialize to correct defaults |
```

**After** (collapsed padding — visually identical for an LLM; humans lose column alignment):
```
|1|`test_phase_accumulator_init_defaults`|`tests/sprint/test_phase_accumulator.py`|PhaseAccumulator fields initialize to correct defaults|
```

**Estimated savings on this file**: The §8.1 table alone has ~70 rows averaging ~180 chars each with ~30-40 chars of pad-spaces per row → ~2.1-2.8 KB. Across all 184 table rows at average ~15 bytes of pad per row: **~2.7-3.5 KB (~3.2-4.2%)**. This is the single largest lever available in the primer-approved set.

**Lossless?** Yes for an LLM consumer (primer §2.1 table explicitly lists this as ✅). CommonMark parses `|a|b|` and `| a | b |` identically.

**Risks on this file**:
1. **Human audit friction** — Specs are frequently re-read by humans (primer §5 "Human-audit frequency"); tight pipe tables are harder to scan. This is a fidelity-adjacent concern, not a correctness concern.
2. **One table contains backticked code identifiers** containing pipes? Spot-check confirms **none** — all backticks in tables wrap single identifiers (`test_phase_accumulator_init_defaults`, `tests/sprint/test_phase_accumulator.py`), none contain `|`. Safe.
3. **Risk Assessment table row lengths** (§7, lines 1243-1250) are ~400+ chars on one logical row; removing pad saves ~30 bytes but makes the row unreadable in a plain editor. Acceptable for compressed output; the human-readable form lives in git.

### 2.7 Strategy S7 — Remove HTML comments (configurable)

**Primer citation**: §4.1 transform 7.

**Target**: Grep confirms **zero** `<!-- ... -->` blocks. **Savings: 0 bytes.** No-op on this file.

### 2.8 Strategy S8 — Drop duplicated version/last-updated blocks

**Primer citation**: §4.1 transform 8.

**Target**: The YAML front matter (lines 2-20, wrapped in a ` ```yaml ` fence) already contains `version: "1.0.0"`, `created: 2026-04-05`, `status: draft`. A grep for a separate "Last updated:" or "Version:" line outside the front matter finds **none**. **Savings: 0 bytes.** No-op.

**Adjacent observation** (not a primer strategy, flagged for S12): the YAML front matter is wrapped inside a code fence (`\`\`\`yaml` … `\`\`\``) rather than being a CommonMark-native front-matter delimiter. This adds 8 bytes (` ```yaml\n` + `\n``` `) but, more importantly, turns the front matter into a fenced code block in the AST. Unwrapping it is NOT a primer §4.1 transform and is therefore NOT recommended on a spec — the author's choice is preserved as-is under the fidelity floor. (See §4 Risks/Caveats R2.)

### 2.9 Strategy S9 — Normalize bullet markers

**Primer citation**: §4.1 transform 10.

**Target**: Spot check of §1.2 Scope Boundary (lines 42-67) and §4.1 New Files (lines 976-983) shows bullets are already uniformly `-`. Grep for `^\s*\*\s` and `^\s*\+\s` returns no hits in list contexts (only inside inline bold `**text**`). **Savings: 0 bytes.** No-op — already normalized.

### 2.10 Strategy S10 — Conventions-header abbreviation of structural labels only

**Primer citation**: §2.2 ("conventions header") + §2.3 "Abbreviable phrases" row + §4.1 transform 9 ("Replace declared abbreviations from conventions header").

**Scope restriction under SPEC fidelity floor**: Per primer §5 row 3 ("fidelity > savings") and the cross-document observation "Spec compression is a trap … the cost of a bad transform is high," abbreviation is restricted to **structural labels only** (the repeating schema of each FR subsection). Normative content — class names, file paths, numeric invariants, MUST/SHALL language — is NOT abbreviated. This is the single point where I am narrowing primer §4.1 transform 9 because it is the load-bearing constraint of a spec.

**Abbreviation set** (six labels that repeat verbatim across 17 FRs):

| Long form | Abbreviation | Occurrences | Per-hit save |
|-----------|--------------|------------:|-------------:|
| `**Acceptance Criteria**:` | `[AC]` | 17 | ~20 chars |
| `**Verification contract**:` | `[VC]` | 17 | ~22 chars |
| `**Commit boundary**:` | `[CB]` | 17 | ~16 chars |
| `**Rollback plan**:` | `[RB]` | 18 | ~14 chars |
| `**Dependencies**:` | `[Dep]` | 18 | ~12 chars |
| `**Current code**` | `[CC]` | 17 | ~12 chars |
| `**Path A adaptation**:` | `[PA]` | 8 | ~18 chars |

**Conventions header** (~40-60 tokens, per primer §2.2):
```
<!-- cmd-dsl v1 (labels only): [AC]=Acceptance Criteria [VC]=Verification contract
[CB]=Commit boundary [RB]=Rollback plan [Dep]=Dependencies [CC]=Current code
[PA]=Path A adaptation. Scope: structural labels ONLY — identifiers, file paths,
and normative language are verbatim. -->
```

**Before** (lines 206-216, verbatim):
```markdown
**Acceptance Criteria**:
- [ ] `PhaseAccumulator` dataclass exists in `models.py` after `MonitorState` (after line 544)
...

**Dependencies**: None. Foundation task.
```

**After** (identical semantics with header present):
```markdown
[AC]
- [ ] `PhaseAccumulator` dataclass exists in `models.py` after `MonitorState` (after line 544)
...

[Dep] None. Foundation task.
```

**Estimated savings**:
- Labels: (17+17+17+18+18+17+8) × avg ~16 chars = 112 × 16 ≈ **1.79 KB** gross
- Header cost: ~220 bytes (one-time)
- **Net savings**: ~1.57 KB (**~1.9%**)

**Lossless?** Yes, **provided the header is present and machine-readable**. The primer §2.1 table lists abbreviation-via-conventions-header as ✅ Lossless. This strategy respects the fidelity floor because it only touches labels, not content.

**Amortization check** (primer §5 composition rule 7): The conventions header costs ~220 bytes; each label save is ~16 bytes. Break-even: **14 label uses**. This file has **112 uses** → amortizes 8× over. Safe even under INV-3 uncertainty (the document is read ≥1 time for the LLM to parse it, and 112 > 5 internal repetitions so the header "pays for itself" within a single read).

**Risks on this file**:
1. **Fidelity creep**: if the set is ever widened to include identifiers (`PhaseAccumulator`, `MonitorState`), the strategy degrades into lossy rephrasing. Must be enforced by a linter on the abbreviation table.
2. **Downstream consumer gap (INV-3)**: if some consumer of the spec does not strip/expand the header, it sees raw `[AC]` tags. Acceptable — `[AC]` is still readable by any LLM as "AC section marker"; the loss is human-audit friction, not semantic.
3. **Bold-markdown loss**: removing `**…**` strips bold styling. For a spec that is read by LLMs, this is irrelevant. For human review, this is a real downgrade. Mitigation: keep the label bolded in the output (`**[AC]**:`), giving up ~4 chars per hit. Recommended for this file to preserve audit ergonomics.

### 2.11 Strategy S11 — Drop repeated rollback plan boilerplate (REJECTED, lossy)

**Primer citation**: §2.1 table "Drop prose explanations" row — **marked ⚠️ Lossy**.

**What it would do**: Many rollback plans are trivial one-liners like "Remove N fields. Terminal panels show no turn/token data (existing behavior)." A naive pass might elide these because they repeat a template.

**Why REJECT on this file**: Under primer §5 row 3, specs are contracts. Rollback plans are part of the contract ("No data migrations needed" is a normative assertion). Dropping them crosses the fidelity floor. Flagged here explicitly per the task requirement to "flag any strategy that is lossy and explain why it should or should not apply to a spec." **Do not apply.**

### 2.12 Strategy S12 — Unwrap YAML front matter from code fence (REJECTED, out of primer scope)

**What it would do**: Lines 1-21 wrap YAML front matter inside a ` ```yaml ` code fence. Unwrapping to raw `---`/`---` native front matter saves 12 bytes (fence lines).

**Why REJECT**: Not one of primer §4.1's ten transforms. It is an AST-level transform (fence → front matter node), which is §4.2 Approach 2 territory and therefore **forbidden on specs** by primer §5 rule 5. Savings are negligible (~0.01%) and the risk of breaking a downstream parser that expects YAML-in-fence is non-zero. **Do not apply.**

### 2.13 Strategy S13 — Dedupe cross-references (REJECTED on specs)

**Primer citation**: Approach 2 §4.2 transform 4 ("Cross-reference deduplication").

**Why REJECT**: The file has multiple `(see Section X)` / `(Debate N ruling)` references that a pure Approach-1 pass cannot safely dedupe (it would require AST navigation). Approach 2 is forbidden on specs. Flagged for completeness; **do not apply**.

---

## 3. Recommended Strategy Stack

**Pipeline**: Apply in order. All transforms are Approach 1 (primer §4.1). Each pass is fence-aware.

| Order | Strategy | Expected saving | Cumulative | Lossless? | Notes |
|------:|----------|----------------:|-----------:|:---------:|-------|
| 1 | S2 Strip trailing whitespace | 0 bytes (0.0%) | 0.0% | ✅ | No-op on this file; keep for pipeline discipline |
| 2 | S3 Setext → ATX headings | 0 bytes (0.0%) | 0.0% | ✅ | No-op |
| 3 | S9 Normalize bullet markers | 0 bytes (0.0%) | 0.0% | ✅ | No-op |
| 4 | S7 Strip HTML comments | 0 bytes (0.0%) | 0.0% | ✅ | No-op |
| 5 | S5 Strip heading emoji | 0 bytes (0.0%) | 0.0% | ✅ | No-op |
| 6 | S8 Drop duplicated version blocks | 0 bytes (0.0%) | 0.0% | ✅ | No-op |
| 7 | S4 Remove decorative HR | ~5 bytes (0.01%) | 0.01% | ✅ | Only 1 HR at line 1395 |
| 8 | S1 Collapse 2+ blank runs → 1 (fence-aware, heading-aware) | ~100-180 bytes (~0.2%) | ~0.2% | ✅ | Low yield — already disciplined |
| 9 | S6 Collapse pipe-table padding | ~2.7-3.5 KB (~3.2-4.2%) | ~3.4-4.4% | ✅ | **Largest lever.** Fence-safe, CommonMark-identical |
| 10 | S10 Conventions-header label abbreviation (labels only, bolded) | ~1.3-1.5 KB (~1.6-1.8%) | ~5.0-6.2% | ✅ | Preserves `**…**` → net ~12-14 chars/hit instead of 16 |

### 3.1 Projected total compression for this file

**Conservative**: ~**5.0%** net reduction (≈ 4.2 KB / 84.3 KB). All lossless by primer §2.1 criteria.

**Optimistic (within fidelity floor)**: ~**6.2%** net reduction (≈ 5.2 KB / 84.3 KB).

**Primer ceiling for specs**: 10-15% (§5 row 3). This file underperforms the primer ceiling because:

1. **~42% of the file is code fences** (primer §4.1 risk list: "Code fences are sacrosanct"). Every Approach-1 transform must skip fence interiors, so the compressible surface is only ~58% of the file ≈ 49 KB.
2. **The author is already disciplined**: no trailing whitespace, no setext headings, no emoji, no HTML comments, single blank lines between blocks, uniform `-` bullets. Six of ten §4.1 transforms are no-ops.
3. **The abbreviable surface is deliberately narrowed** to schema labels only. Expanding to identifiers would hit the 10-12% range but would violate the fidelity floor.

**Bottom line**: 5-6% is the honest Approach-1 ceiling for THIS spec under a strict fidelity interpretation. Reaching the primer's 10-15% range on this specific file would require either (a) abbreviating identifiers (fidelity-risk — rejected) or (b) Approach 2/3 (primer §5 rule 5 forbids — rejected).

### 3.2 Rationale for the ordering

- Passes 1-6 are no-ops on this file but must run first for pipeline commutativity (primer §5 rule 1: "Always run Approach 1 first. … Subsequent approaches should operate on Approach-1-normalized input so their transforms are stable.")
- S1 (blank collapse) runs before S6 (table padding) because blank-line runs can separate tables, and collapsing them first avoids confusing the table-detector.
- S6 runs before S10 because table padding collapse operates on raw text while the label abbreviation pass operates on headings/paragraphs; they do not interact.
- S10 runs last because the conventions header must be placed at the top of the file AFTER all other whitespace passes have settled, so its byte cost is not double-counted against S1's normalization.

---

## 4. Risks & Caveats Specific to This File

### R1 — Code fences are the dominant surface and the dominant risk

41.7% of the file (599 lines) is code-fence content: Python snippets, an ASCII-art workflow diagram (§2.2, lines 92-179), and the YAML-in-fence front matter. Every Approach-1 transform MUST be fence-aware (primer §4.1 risks: "Regex inside code fences can corrupt examples if fence-awareness isn't implemented"). The ASCII diagram in particular is sensitive to column alignment — S1 (blank collapse) and S6 (table padding) would destroy it if they ran inside the fence. Mitigation: every transform uses a fence-state machine.

### R2 — YAML front matter is wrapped in a `yaml` code fence

Lines 1-21 are a ` ```yaml ` block containing `---` / `---` delimited YAML. This is unusual (native front matter is conventionally at column 0 without a fence). Under the fidelity floor, this wrapping is preserved verbatim. **Do not** "fix" this shape — S12 is rejected. Any consumer that expects native front matter will need to read the YAML from inside the fence.

### R3 — Ten+ tables contain >180 rows with load-bearing content

The §8.1 Unit Tests table alone has ~70 rows specifying verification contracts. S6 (pad collapse) is lossless for LLM consumers but the compressed form is significantly harder for a human reviewer to audit. Because specs are "archive for fidelity, not performance" (primer §5 cross-doc observation), the compressed output should be treated as a cache artifact, not a replacement for the source of truth. The uncompressed spec MUST remain the canonical human-reviewed document. This is operational discipline, not a transform gate.

### R4 — Identifier repetition is high but MUST NOT be abbreviated

`MonitorState` (79×), `PhaseAccumulator` (44×), `TaskResult` (53×), `tests/sprint/` (78×) together comprise ~6-8 KB of the file. Abbreviating them via conventions header would yield ~5-6 KB additional savings (pushing this file to the ~12% primer ceiling) BUT these are normative identifiers — the spec binds implementers to these exact names. Under primer §5 row 3 ("Treat fidelity > savings"), identifier abbreviation is a **fidelity violation** and is rejected. This is the single biggest "missed" opportunity on this file and it is missed **intentionally**.

### R5 — Rollback plans look like boilerplate but are normative

Some rollback plans are one-liners that look droppable ("Remove 5 properties. Terminal panels lose aggregate data."). They are NOT droppable. They are part of the contract. S11 (drop rollback prose) is rejected for this reason.

### R6 — Acceptance Criteria checkboxes `- [ ]` look decorative

There are 80+ `- [ ]` checkbox bullets across the 17 FRs. They might be mistaken for decorative list markers and normalized by a naive `- [x]` / `- [ ]` → `-` pass. They are not decorative; they are machine-readable acceptance criteria. Any bullet-normalization transform MUST preserve the `[ ]` / `[x]` marker. S9 (bullet normalization) as specified in primer §4.1 transform 10 only normalizes the marker character (`*`/`+`/`-` → `-`), not the checkbox suffix, so there is no conflict — but the pipeline test must cover this case.

### R7 — INV-1 tokenizer drift (carried from primer §6)

All byte-level savings above are measured in raw UTF-8. Tiktoken tokenization of 5-6% byte savings maps approximately but not exactly to 5-6% token savings; the actual Claude-native figure may drift by ±2pp (primer §6 INV-1). The 5-6% net projection should be re-validated with `messages.count_tokens` before any pipeline commits to it in production.

### R8 — Human audit frequency is high for specs

Per primer §5 variables ("Human-audit frequency — how often humans review it manually"), specs are read by humans multiple times during a release. S6 table-padding collapse, in particular, degrades human scan-ability. Recommended operational stance: **emit the compressed form for LLM consumers only**; keep the uncompressed form as the canonical artifact in git. The CLI pipeline (per primer §7 and the adversarial study roadmap) should treat spec compression as an **ingest-time only** transform, not a storage replacement.

---

## 5. Summary

| Dimension | Value |
|-----------|-------|
| Document type | SPEC |
| Primer-mandated approach | Approach 1 only (primer §5 row 3, §5 rule 5) |
| Primer ceiling for type | 10-15% |
| Realistic ceiling for **this** file | **~5-6%** |
| Strategies applied (non-zero) | S4 (~0.01%), S1 (~0.2%), S6 (~3.2-4.2%), S10 (~1.6-1.8%) |
| Strategies that were no-ops | S2, S3, S5, S7, S8, S9 |
| Strategies rejected under fidelity floor | S11 (drop rollback prose), S12 (unwrap YAML fence), S13 (Approach 2 xref dedupe) |
| Biggest missed opportunity | Identifier abbreviation — intentionally rejected (R4) |
| Biggest single win | S6 table-padding collapse (~3.2-4.2%) |
| Net projected compression | **~5.0% conservative, ~6.2% optimistic** |
| Fidelity class | Near-lossless (all applied strategies are ✅ per primer §2.1) |
| Blocking risks | R1 (fence-awareness), R3/R8 (human audit), R4 (identifier discipline) |

This file is a well-disciplined spec. Most of the primer's Approach-1 transforms have already been pre-applied by the author. The compression ceiling is low specifically BECAUSE the document is already clean — the remaining savings come from mechanical table-padding collapse and a conservative labels-only conventions header. That is the correct outcome under the SPEC fidelity floor.
