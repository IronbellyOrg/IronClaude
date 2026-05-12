# Compression Analysis — v3.7 Unified Release Spec (merged)

**Target file**: `/config/workspace/IronClaude/.dev/releases/backlog/v3.7-task-unified-v2/v3.7-UNIFIED-RELEASE-SPEC-merged.md`
**Primer reference**: `/config/workspace/IronClaude/claudedocs/compressed-markdown-dsl-primer.md`
**Analysis date**: 2026-04-15
**Document type**: SPEC (normative release specification, contract-bearing)
**Applicable strategy row**: primer §5 "Spec" — Approach 1 (rule-based) ONLY, **10–15% ceiling**, **near-lossless floor**.

---

## 1. File Inventory

| Metric | Value |
|---|--:|
| Absolute path | `.dev/releases/backlog/v3.7-task-unified-v2/v3.7-UNIFIED-RELEASE-SPEC-merged.md` |
| Byte size | 101,460 B (~99 KiB) |
| Line count | 1,765 |
| Word count | 13,594 |
| Approx. token estimate (words × 1.35) | ~18,350 tokens |

### 1.1 Structural composition (line-based)

| Category | Lines | % of total | Notes |
|---|--:|--:|---|
| Table rows (`^|`) | 612 | 34.7% | 15 scope tables + 16 per-task metadata tables + 7 file-inventory tables + 10 cross-cutting tables |
| Table separators (`|---|…`) | 79 | 4.5% | ATX-style pipe-column dividers |
| Blank lines (`^$`) | 404 | 22.9% | Includes triple-blank-line separators around HRs |
| Headings (`^#…`) | 115 | 6.5% | 1 H1, 15 H2 sections, 60+ H3/H4 task entries |
| Horizontal rules (`^---$`) | 23 | 1.3% | Section dividers, all redundant with `## N.` heading resets |
| HTML provenance comments (`<!-- Source: … -->`) | 26 | 1.5% | Adversarial-merge provenance; not semantically load-bearing to readers |
| Bullet lines (`^- `) | 109 | 6.2% | |
| Prose / step bodies / bold-intro / misc | ~397 | ~22.5% | Remainder — Steps, Rollback, Source footers, bold field intros |
| Code fences (`^````) | 18 markers | — | **9 fenced blocks**: 3 ASCII diagrams (Appendix B UI layouts), 2 ASCII callgraphs (Appendix C), 1 JSON event example, 1 python helper, 1 prompt snippet, 1 architecture diagram |

### 1.2 Repeated string inventory (amortization candidates)

| Token | Occurrences | First appears in | Amortization note |
|---|--:|---|---|
| `Checkpoint` (free-standing word) | 113 | §2.1 | Appears as domain prefix everywhere |
| `src/superclaude/` path prefix | 65 | §3.3 | Identical prefix on every Target File |
| `task-unified` | 48 | §2.3 | Canonical rename target |
| `checkpoints.py` | 31 | §3.1 | |
| `executor.py` | 30 | §3.1 | |
| `process.py` | 24 | §2.1 | |
| `PASS_MISSING_CHECKPOINT` | 22 | §3.1 | Load-bearing enum identifier |
| `sc-tasklist-protocol` | 17 | §3.3 | |
| `analysis-checkpoint-enforcement.md` | 16 | §1 Source footer | Repeated in 16 `**Source**` footers |
| `/sc:task-unified` | ~15 | §2.3 | |

### 1.3 Structural regularity signals

- **16 task metadata tables** with identical column shape: `| Field | Value |` × rows `Proposal Reference | Why | Effort | Risk | Risk Drivers | Tier | Confidence | Verification Method`
- **16 Target File / Steps / Acceptance Criteria / Rollback** block quartets (one per task T01.01..T04.03)
- **22 `**Source**:` footers** — all have identical bold-intro format
- **26 provenance HTML comments** — 100% decorative for LLM consumption (they describe the merge history of this doc, not the spec content)

---

## 2. Strategies Identified

Every strategy below is grounded in primer §2 (categories), §4.1 (rule-based), or §5 (spec row). **Specs are fidelity-first — no strategy below alters normative semantics.**

### Strategy S1 — Collapse consecutive blank lines (primer §2.3 "Whitespace & formatting", §4.1 transform #1)

**What**: Wherever the file contains 2 or 3 consecutive blank lines (outside fenced code), collapse to a single blank line.

**Before** (lines 33–36):
```
15. [Appendices](#15-appendices)

---

<!-- Source: Base (original, modified) -- Change #6 adds LOC estimates to scope table -->
```

**After**:
```
15. [Appendices](#15-appendices)

---
<!-- Source: Base (original, modified) -- Change #6 adds LOC estimates to scope table -->
```

**Saving**: File has 404 blank lines total. Inspection shows most section breaks use `\n\n---\n\n` (4 chars of wasted whitespace per section). With 23 HRs × ~2 redundant blank-line chars + general double-to-single collapse across the document, savings ≈ 200–300 lines stripped. Estimated **~1.5–2.5% byte reduction** (~1.5–2.5 KB, ~300–500 tokens).

**Loss profile**: LOSSLESS (primer §2.1 table: "Collapse blank lines ✅ Yes (unless fenced code)"). Safe for spec.

**Risk**: Must be fence-aware. 9 fenced blocks exist (Appendix B ASCII art relies on layout). Regex must detect `^```` fence state. Low risk with a 20-line Python state machine.

---

### Strategy S2 — Remove horizontal rules adjacent to H2 headings (primer §2.3 "Decorative elements", §4.1 transform #4)

**What**: The file uses `\n---\n` as a section divider between every numbered H2 section. Since `## 1.`, `## 2.`, ... already semantically terminate the prior section in Markdown, the HRs are redundant decoration.

**Before** (lines 63–67):
```

**Source**: `analysis-checkpoint-enforcement.md` Section 1; `analysis-sprint-tui-v2.md` Section 1; `analysis-naming-context.md` Section 1

---

<!-- Source: Base (original) -->
## 2. Problem Statement
```

**After**:
```

**Source**: `analysis-checkpoint-enforcement.md` Section 1; `analysis-sprint-tui-v2.md` Section 1; `analysis-naming-context.md` Section 1

<!-- Source: Base (original) -->
## 2. Problem Statement
```

**Saving**: 23 HRs × 4 bytes (`---\n`) + 23 adjacent blank lines = ~115 B directly; factoring section-divider whitespace collapse, **~0.2% byte reduction** (small, but fully free).

**Loss profile**: LOSSLESS for LLM consumption — heading `##` is unambiguous section terminator in CommonMark. Primer §2.1 table explicitly lists "Remove decorative horizontal rules" as LLM-lossless.

**Risk**: None for this file — no HR appears inside a sub-section where it functions as content separator (manually verified). Three Appendix code blocks use ASCII `===` / `+---+` art but those live inside fences, untouched.

---

### Strategy S3 — Strip provenance HTML comments (primer §2.3 "Preamble & meta", §4.1 transform #7)

**What**: The file contains 26 `<!-- Source: ... -->` / `<!-- Provenance: ... -->` / `<!-- Base: ... -->` / `<!-- Merge date: ... -->` comments that annotate the adversarial-merge history. These are artifacts of the rf-assembler pipeline, not spec content. An LLM reading the spec does not need "Change #1 renumbers sections 6+ to 7+".

**Before** (lines 1–4 + 36):
```
<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B ("Assembled", rf-assembler output) -->
<!-- Merge date: 2026-04-02 -->

...

<!-- Source: Base (original, modified) -- Change #6 adds LOC estimates to scope table -->
## 1. Release Overview
```

**After**:
```
## 1. Release Overview
```

**Saving**: 26 comments × average ~85 B each = **~2,200 B directly, ~1.5% byte reduction, ~450 tokens**.

**Loss profile**: LOSSLESS for downstream LLM task equivalence (the merge trail does not alter any normative MUST/SHOULD in the spec). **Caveat**: this is lossless *for LLM consumption* but it removes human audit trail — if the file is also consumed by a human reviewing merge history, the comments are meaningful. Primer §2.1 and §4.1 #7 explicitly allow comment stripping with "configurable exclusions"; for SPEC fidelity, recommend **preserving** the top-of-file provenance block (lines 1–3) and stripping only the inline 22 `<!-- Source: ... -->` merge markers. That keeps the audit anchor while removing the body noise.

**Risk**: Must be configurable to preserve the top-3 provenance lines. Inline comments are never fence-crossed, so the regex is safe.

---

### Strategy S4 — Collapse pipe-table padding (primer §2.3 "Table whitespace", §4.1 transform #6)

**What**: The 612 table rows use generous column padding for human readability: e.g. `| # | Cause                                       | File                                     | Evidence                                |`. Collapsing to `|#|Cause|File|Evidence|` is parse-equivalent in CommonMark GFM tables and in every Markdown renderer that Claude has been trained on.

**Before** (lines 77–80, task metadata table from §2.1):
```
| # | Cause | File | Evidence |
|---|-------|------|----------|
| 1 (Primary) | Agent prompt contains no checkpoint instructions | `process.py` lines 169-203 | `build_prompt()` tells agent "After completing all tasks, STOP immediately" with zero mention of checkpoints |
```

**After** (illustrative — most padding in this file is already moderate; bigger wins come from the heavily-padded comparison tables):
```
|#|Cause|File|Evidence|
|---|---|---|---|
|1 (Primary)|Agent prompt contains no checkpoint instructions|`process.py` lines 169-203|`build_prompt()` tells agent "After completing all tasks, STOP immediately" with zero mention of checkpoints|
```

**Saving**: 612 table rows × average ~6 B of collapsible pad/separator whitespace each = **~3.5–4 KB, ~3.5% byte reduction, ~700 tokens**. Separator rows (79) collapse from `|-------|------|--------------------|` to `|---|---|---|` for additional savings.

**Loss profile**: LOSSLESS. GFM pipe-table parsing does not depend on column padding; every mainstream Markdown parser handles unpadded pipes identically. Primer §4.1 transform #6 explicitly lists this as a rule-based safe transform.

**Risk**: Some visual Markdown previewers render unpadded tables awkwardly for humans; this is irrelevant for LLM consumption. Tables inside code fences (none in this file) would be off-limits. Low risk.

---

### Strategy S5 — Deduplicate `**Source**:` footers via local shorthand (primer §2.3 "Preamble & meta", §4.1 transform #8 analogue)

**What**: The file has **22 `**Source**:` footers**, 16 of which cite one or more of three analysis files (`analysis-checkpoint-enforcement.md`, `analysis-sprint-tui-v2.md`, `analysis-naming-context.md`) plus section numbers. Because these are **traceability footers** (contract-bearing for a spec — they anchor normative claims to their source analysis), we cannot delete them. But a **rule-based transform** can shorten them via the primer's §4.1 transform #8 pattern: "Drop trailing X / repeated Y blocks".

**Before** (e.g., line 102):
```
**Source**: `troubleshoot-missing-p03-checkpoint.md` Sections 1-4; `analysis-checkpoint-enforcement.md` Section 2
```

**After** (conservative — add reference-style link shortcuts at the bottom of the file):
```
**Source**: [troubleshoot-p03] §1-4; [a-checkpoint] §2
```
with footer:
```
[troubleshoot-p03]: troubleshoot-missing-p03-checkpoint.md
[a-checkpoint]: analysis-checkpoint-enforcement.md
[a-tui]: analysis-sprint-tui-v2.md
[a-naming]: analysis-naming-context.md
```

**Saving**: Each full-filename citation is ~45 B; shortcut reduces to ~15 B. 22 footers × ~50 B savings − ~200 B of footer definitions = **~900 B, ~0.9% byte reduction, ~200 tokens**.

**Loss profile**: LOSSLESS (CommonMark reference-style links are parsed to the same URL). **But this approaches the edge of spec-fidelity policy**: it introduces an indirection that a human auditor must follow. For a strict spec, this is acceptable because reference-style links are valid CommonMark and are part of the universally-understood Markdown surface. **Marginal call** — recommend including only if byte budget matters.

**Risk**: Low. Parser-equivalent. The citations remain programmatically discoverable.

---

### Strategy S6 — Normalize bullet / list markers (primer §4.1 transform #10)

**What**: The file uses a consistent `-` bullet throughout (109 bullet lines verified). No `*` or `+` mixing was observed. **This transform is already applied**.

**Saving**: 0 B. Strategy is listed for completeness per primer §4.1 #10 but is a no-op for this file.

**Loss profile**: N/A.

---

### Strategy S7 — Strip trailing whitespace (primer §4.1 transform #2)

**What**: Remove any trailing spaces before `\n`.

**Saving**: File has **0 lines with trailing whitespace** (verified via `grep -cE ' +$'`). No-op — already applied, likely by an upstream `mdformat` pass.

**Loss profile**: N/A.

---

### Strategy S8 — Normalize heading underline syntax (primer §4.1 transform #3)

**What**: Convert Setext headings (`=====`, `-----`) to ATX (`#`, `##`).

**Saving**: 0 B. All 115 headings already use ATX form.

**Loss profile**: N/A.

---

### Strategy S9 — Emoji stripping from headings (primer §4.1 transform #5)

**What**: Remove decorative emoji from headings.

**Saving**: 0 B. Verified: the file contains no emoji in headings (all headings are plain ASCII `## N. Title`).

**Loss profile**: N/A.

---

### Strategy S10 — Conventions header with abbreviation substitution (primer §2.2, §4.1 transform #9) — **FLAGGED: not recommended for this spec**

**What**: Per primer §2.2, introduce a conventions header declaring abbreviations for the heavily-repeated load-bearing tokens in this file:

```markdown
<!-- cmd-dsl v1:
  [CE]=Checkpoint Enforcement  [PMC]=PASS_MISSING_CHECKPOINT
  [SP]=src/superclaude/  [CP.py]=checkpoints.py  [EX.py]=executor.py
  [PR.py]=process.py  [tul]=task-unified  [stl]=sc-tasklist-protocol
-->
```

**Hypothetical saving**: With 113 "Checkpoint" + 22 "PASS_MISSING_CHECKPOINT" + 65 "src/superclaude/" + 31 "checkpoints.py" + 30 "executor.py" + 24 "process.py" + 48 "task-unified" + 17 "sc-tasklist-protocol" = 350 occurrences, saving ~6 B each average = **~2.1 KB, ~2% byte reduction**.

**Loss profile**: **LOSSLESS per primer §2.1 when the conventions header is present**, BUT:

**Why this is flagged DO-NOT-APPLY for this spec**:
1. **Primer §5 SPEC row explicitly caps at 10–15% with Approach 1 only.** S10 is an abbreviation substitution which primer §4.1 #9 places in Approach 1, so it is *technically* in-scope — but it violates the **semantic principle** behind the spec row: *"Compression must be reversible and auditable; AST transforms introduce risk of semantic drift on normative language"*. Replacing `PASS_MISSING_CHECKPOINT` (a load-bearing Python enum identifier) with `[PMC]` introduces a **non-code token that looks like a Python identifier in some contexts**, risking misinterpretation by a downstream code-gen agent.
2. **Cross-file symbol integrity**: `executor.py`, `process.py`, `checkpoints.py`, `PASS_MISSING_CHECKPOINT`, `src/superclaude/` are all **grep targets** for humans and for downstream agents reading the spec to plan implementation. Abbreviating them breaks grep-search workflows across the repository. This is a consumer-DAG concern that primer §2.2 explicitly flags (INV-3).
3. **Primer §5 cross-observation**: *"Spec compression is a trap."*
4. The header cost (~60 tokens) plus reduced greppability is not worth the ~2% gain on a document that is spec-contract material.

**Recommendation**: **Do NOT apply S10 to this file.** Document the decision explicitly per primer §5 guidance.

---

### Strategy S11 — Inline bold-field table flattening (primer §4.1 #1–#4 union, marginal)

**What**: The 16 task blocks use a repetitive pattern:
```
| Field | Value |
|---|---|
| Proposal Reference | Solution 1, Wave 1 |
| Why | ... |
| Effort | S |
| Risk | Very Low |
...
```
A rule-based transform could replace the `| Field | Value |` header row (which carries no information — every task table has the identical header) with nothing and keep only data rows. CommonMark GFM still parses a headerless pipe table if the first line is a separator — however **this is NOT a safe transform** because CommonMark GFM requires a header row.

**Saving**: 16 tables × 2 rows removed × ~15 B = **~480 B, ~0.5%**.

**Loss profile**: **Borderline LOSSY**. Technically the header `| Field | Value |` is decorative (primer §2.1 "decorative"), but removing it produces **non-CommonMark output** in most renderers. This violates the primer's core promise (§1: "Every compressed document is still valid CommonMark").

**Recommendation**: **Do NOT apply.** Fails CommonMark validity invariant.

---

### Strategy S12 — Scope-boundary of compression: preserve all fenced blocks (primer §5 compression pipeline rule #2 "Code fences are sacrosanct")

**What**: Explicit non-transform. The 9 fenced blocks in this file are:
1. Architecture diagram (§3.1 three-layer defense, ASCII)
2. JSON event example (§T02.03)
3. Prompt snippet (§T01.01 checkpoint instructions)
4. ASCII UI layout — Active Sprint (Appendix B)
5. ASCII UI layout — Sprint Complete (Appendix B)
6. ASCII UI layout — Sprint Halted (Appendix B)
7. ASCII UI layout — Tmux 3-pane (Appendix B)
8. Callgraph — Sprint Pipeline Flow (Appendix C)
9. Callgraph — Checkpoint Failure Path (Appendix C)
10. Rollout timeline (§9.1)

(Strictly 10 fenced blocks; count shows 18 fence markers.)

Every one of these uses whitespace-sensitive ASCII layout. **No whitespace, no blank-line, and no padding transform may cross a fence boundary.** This is not a strategy per se — it is a constraint that bounds every other strategy.

---

## 3. Recommended Strategy Stack

Per primer §5 spec row, the ceiling is **10–15% with Approach 1 only**. The stack below respects that ceiling and the near-lossless fidelity floor.

### 3.1 Ordered application

| Order | Strategy | Cumulative byte save | Cumulative % | Fidelity |
|:--:|---|--:|--:|---|
| 1 | **S1** — collapse blank lines (fence-aware) | ~2,000 B | ~2.0% | Lossless |
| 2 | **S2** — strip decorative H2-adjacent HRs | ~200 B | ~2.2% | Lossless |
| 3 | **S3** — strip inline `<!-- Source: ... -->` merge markers (preserve top-3 provenance block) | ~2,000 B | ~4.2% | Lossless-for-LLM; preserves human audit anchor |
| 4 | **S4** — collapse pipe-table padding | ~3,800 B | ~7.9% | Lossless (CommonMark GFM) |
| 5 | **S5** — reference-style citation shortcuts (optional) | ~900 B | **~8.7%** | Lossless; marginal call, include only if budget matters |
| — | S6 / S7 / S8 / S9 | 0 | — | No-op (already normalized) |
| — | S10 (conventions header) | — | — | **Rejected** — breaks grep/DAG; primer §5 "trap" |
| — | S11 (remove table header row) | — | — | **Rejected** — breaks CommonMark |
| — | S12 (fence preservation) | — | — | Constraint, not transform |

### 3.2 Projected totals

- **Without S5 (conservative)**: ~**7.9% byte reduction** (~8,000 B of 101,460 B). Token estimate: ~1,450 tokens saved on an ~18,350-token file.
- **With S5 (aggressive but still Approach 1)**: ~**8.7%** (~8,900 B, ~1,650 tokens saved).
- **Ceiling remaining under primer §5**: 10–15%. This stack lands in the lower half of the allowed window — by design. The remaining 2–6 pp would only be reachable with S10 (conventions header) which we reject above on fidelity grounds.

### 3.3 Rationale for under-compressing vs ceiling

This spec sits closer to 8% than 15% because:
1. The file has already been partially normalized (zero trailing whitespace, ATX headings, no emoji, consistent bullets) — S6–S9 yield zero.
2. The document is **table-dominated** (39% of lines are tables); S4 is the single biggest lever and it is inherently bounded.
3. Prose restatement is relatively low — the document is already information-dense because it is the adversarially-merged output of two variants.
4. The biggest tempting lever (S10 conventions header, ~2% additional) is disqualified on spec-fidelity grounds per primer §5 and §2.2 INV-3.

**Decision**: Ship 7.9% (conservative) as the canonical compression output. Mark S5 as "apply only if byte budget is binding".

---

## 4. Risks and Caveats Specific to This File

### 4.1 Fidelity-critical hazards

1. **Fence-crossing regex** — any S1, S2, S3, S4 implementation MUST track `^```` fence state. Appendix B's ASCII UI layouts and Appendix C's callgraphs rely on blank-line and column alignment. A naïve regex that strips blank lines globally will corrupt those diagrams. Primer §4.1 "Risks" bullet #1 calls this out; this file has **10 fenced blocks** making it the highest-risk area.
2. **Provenance comments at top-of-file (lines 1–3)** carry the adversarial-merge audit trail. S3 must preserve them; only strip the 22 inline `<!-- Source: Base ... -->` markers. If a compressor strips all comments indiscriminately it destroys the audit anchor and should be rejected.
3. **Load-bearing Python identifiers** — `PASS_MISSING_CHECKPOINT`, `_verify_checkpoints()`, `build_prompt()`, `extract_checkpoint_paths()`, `checkpoint_gate_mode`, etc. must survive untouched. S10 (rejected) would alias some of these; no applied strategy should rewrite any backticked or un-backticked symbol string.
4. **Path strings** — every `src/superclaude/cli/sprint/*.py` path is a navigation target for downstream implementation agents. S10 abbreviation of the prefix would make spec-to-codebase correlation require a decompression step. Rejected.
5. **Table column semantics** — S4 collapses padding but must NOT reorder, drop, or merge columns. Table data rows are normative (e.g., §4.1 T01.01 task metadata is the contract for that task's implementation).
6. **`### Checkpoint:` literal** — the string `### Checkpoint:` appears as normative content in §2.1 describing the structural anomaly in Phase 3. A "decorative heading removal" transform must NOT touch it because it is *data about a heading format*, not *a heading being formatted*. This is a primer §2.1 edge case — the literal `### Checkpoint:` inside a table cell or prose passage is content, not structure. Any decorator-stripping transform must be fence-aware AND context-aware (inside `` ` `` backticks → leave alone).

### 4.2 Cross-strategy hazards

7. **Ordering sensitivity** — S1 (blank-line collapse) should run AFTER S2 (HR removal) and S3 (inline comment removal), because those transforms create new empty lines. Running S1 first wastes half of S1's savings.
8. **S4 before or after S1** — table padding collapse is independent and can run in either order, but running it last makes golden-diff testing easier.
9. **S5 reference-style citation indirection** — if the compressor emits the reference list `[a-checkpoint]: analysis-checkpoint-enforcement.md` but a downstream tool strips "unused" link references, the spec becomes unresolvable. Requires a test that parses the compressed output and confirms reference resolution.

### 4.3 Non-hazards (explicit clearances)

- **No YAML front matter** present — primer §4.1 transform #8 "front matter deduplication" is a no-op here.
- **No duplicate headings** in the body (each `## N.` appears once) — primer §4.2 Approach-2 heading deduplication is irrelevant (and out of scope for spec anyway).
- **No mermaid/plantuml blocks** — primer §4.2 transform #7 diagram-drop is a no-op.
- **Approach 2 (AST) and Approach 3 (LLM rewriting) are out of scope per primer §5 spec row and §5 pipeline rule #5.** Do not apply. A spec rewritten by an LLM is no longer a contract; it is a paraphrase.

### 4.4 Consumer-DAG note (INV-3 carry-forward)

Per primer §2.2 and §6 INV-3, the amortization math for any conventions header depends on read counts. This spec file is:
- Read once by a roadmap generator (`superclaude roadmap`)
- Read once by a tasklist generator (`superclaude tasklist`)
- Read potentially 0–N times by human reviewers
- Grep-indexed by multiple skills that reference it by path

Estimated read count: **3–5**. Per primer §5 pipeline rule #7, a conventions header requires ≥5 reads to amortize. This file sits at the margin — another reason to reject S10.

### 4.5 Summary verdict

This spec is a **low-compressibility, high-fidelity** document. The ~8% achievable via S1+S2+S3+S4 is close to the practical floor for a spec of this composition and well under the 10–15% ceiling the primer permits. Apply the stack; do not chase the ceiling.

---

## Appendix: Raw counts (for reproducibility)

```
lines:                    1765
bytes:                    101460
words:                    13594
blank_lines:              404   (22.9%)
headings:                 115   (6.5%)
table_rows:               612   (34.7%)
table_separators:         79    (4.5%)
horizontal_rules:         23    (1.3%)
html_comments:            26    (1.5%)
bullet_lines:             109   (6.2%)
code_fence_markers:       18    (9 blocks)
trailing_whitespace:      0     (already normalized)
bold_source_footers:      22
acceptance_criteria:      16
rollback_lines:           16
target_file_lines:        16
'Checkpoint' word count:  113
'task-unified':           48
'executor.py':            30
'process.py':             24
'PASS_MISSING_CHECKPOINT':22
'src/superclaude/':       65
'checkpoints.py':         31
'sc-tasklist-protocol':   17
```
