# Compression Analysis — v2.05 Sprint CLI Specification Tasklist

**Target file**: `/config/workspace/IronClaude/.dev/releases/complete/v2.05-sprint-cli-specification/tasklist/tasklist.md`
**Primer**: `/config/workspace/IronClaude/claudedocs/compressed-markdown-dsl-primer.md`
**Date**: 2026-04-15
**Document type (per primer §5)**: TASKLIST → Approach 2 (AST) + auto-conventions-header → target **30-40%**

---

## Section 1 — File Inventory

### 1.1 Raw measurements

| Metric | Value |
|---|---|
| Path | `.dev/releases/complete/v2.05-sprint-cli-specification/tasklist/tasklist.md` |
| Bytes | 111,298 |
| Lines | 2,115 |
| Task cards (`### T##.##`) | 35 |
| Checkpoint cards (`### Checkpoint:`) | 11 |
| Horizontal rules (`---`) | 63 |
| `| Field | Value |` tables | 35 (one per task card) |

### 1.2 Composition breakdown (by category, approximate)

Measured by sampling the four top-level sections (Metadata/Source/Rules/Registries = lines 1–157; 35 task cards = lines 159–1985; Traceability matrix + templates = lines 1988–2115).

| Category | Approx. bytes | % of file | Notes |
|---|---:|---:|---|
| Task-card field tables (15 rows × 35 tasks) | ~36,000 | ~32% | `| Field | Value |` blocks — the single biggest lever |
| Task-card prose bullets (Deliverables/Steps/AC/Validation/Dependencies/Rollback/Notes) | ~42,000 | ~38% | 7 labeled sections × 35 tasks = 245 sections; 172 bracketed step tags |
| Deliverable Registry table (35 rows) | ~7,800 | ~7% | Every row mentions two `TASKLIST_ROOT/artifacts/D-NNNN/…` paths |
| Traceability Matrix (42 rows) | ~5,200 | ~5% | Same path template repeated, plus confidence ASCII meters |
| Roadmap Item Registry (42 rows) | ~4,200 | ~4% | Flat table, limited redundancy |
| Checkpoint cards (11) | ~4,000 | ~4% | Shorter but still uniform |
| Preamble (Metadata, Source Snapshot, Rules, Tasklist Index) | ~6,500 | ~6% | Mostly one-shot prose |
| Templates (execution log / checkpoint report / feedback) | ~3,500 | ~3% | Scaffolding, read rarely |
| Decorative (`---` rules, blank lines, trailing whitespace) | ~2,100 | ~2% | 63 horizontal rules + interstitial blanks |
| **Total** | **~111,300** | **100%** | |

**Key observation**: ~77% of the file (task cards + their tables) is schema-regular and templated. This is the primer §5 "extreme structural regularity" profile — the tasklist row's entire reason for targeting 30-40%.

### 1.3 Repeated phrases qualifying as conventions-header abbreviations

Per primer §2.2, the header pays for itself after ~5-10 uses. All phrases below cross that threshold by large margins (measured via Grep):

| Phrase (verbatim) | Occurrences | Bytes per occurrence | Gross bytes in file |
|---|---:|---:|---:|
| `TASKLIST_ROOT/artifacts/D-` | 112 | 26 | 2,912 |
| `[█████████-] 90%` | 61 | 16 | 976 |
| `\`TASKLIST_ROOT/artifacts/D-NNNN/spec.md\`, \`TASKLIST_ROOT/artifacts/D-NNNN/evidence.md\`` (full pair) | 70 (35 in Deliverable Registry + 35 in task cards) | ~90 | ~6,300 |
| `| **Roadmap Item ID(s)** |` | 35 | 24 | 840 |
| `| **Requires Confirmation** | No |` | 35 | 32 | 1,120 |
| `| **Sub-Agent Delegation** | No |` | 35 | 31 | 1,085 |
| `| **Fallback Allowed** |` | 35 | 22 | 770 |
| `| **Critical Path Override** |` | 35 | 28 | 980 |
| `| **MCP Requirements** | None |` | 27 | 31 | 837 |
| `Direct test execution` | 26 | 21 | 546 |
| `Sub-agent (quality-engineer)` | 10 | 28 | 280 |
| `[PLANNING]` / `[EXECUTION]` / `[VERIFICATION]` tags | 172 | 11–15 | ~2,100 |
| `**Deliverables**:` / `**Steps**:` / `**Validation**:` / `**Dependencies**:` / `**Rollback**:` / `**Notes**:` | 210 | 14–19 | ~3,400 |
| `src/superclaude/cli/sprint/` | 15 | 26 | 390 |
| `uv run pytest` | 35 | 13 | 455 |
| `Acceptance Criteria` | 35 | 19 | 665 |

**Gross repeated-phrase budget**: ~23,600 bytes (~21% of file) in phrases that each appear ≥5 times. Per primer §2.2 this is exactly the content class a conventions header monetizes.

---

## Section 2 — Strategies Identified

Each strategy cites a primer section and provides a real before/after from the target file. Savings are bytes, estimated from measured occurrence counts. Lossy/lossless is stated per primer §2.1.

### Strategy S1 — Whitespace & horizontal-rule collapse (Approach 1, primer §4.1)

**Primer anchor**: §4.1 Approach 1 transforms 1–4; §2.3 "Whitespace & formatting ~8-12%".

**What**: Collapse multiple blank lines, strip trailing whitespace, and delete decorative `---` rules that are not load-bearing front-matter separators. The file contains 63 `---` rules; many sit between a task card and its sibling where the `### T##.##` heading already provides a visual break.

**Before** (lines 211–215, between T01.01 and T01.02):

```
**Notes**: Foundation task — block all subsequent phases until verified complete. Use `@dataclass(frozen=False)` for mutability where spec requires it (e.g., MonitorState).

---

### T01.02 — Create sprint module __init__.py
```

**After**:

```
**Notes**: Foundation task — block all subsequent phases until verified complete. Use `@dataclass(frozen=False)` for mutability where spec requires it (e.g., MonitorState).

### T01.02 — Create sprint module __init__.py
```

**Savings**: 63 rules × ~5 bytes (`---\n` + leading/trailing blank) ≈ 315 bytes, plus ~1,700 bytes of trailing-whitespace/blank-line collapse across 2,115 lines (~0.8 byte/line measured average). **~2,000 bytes ≈ 1.8%.**

**Loss profile**: **Lossless** for LLM consumption — `---` serves as a visual separator only; the `###` heading provides the same semantic split to a CommonMark parser.

**Risk**: Human readers lose visual rhythm between task cards. No content risk.

---

### Strategy S2 — Field-label abbreviation via conventions header (Approach 2, primer §4.2 transform 5)

**Primer anchor**: §4.2 "Front-matter → conventions-header synthesis"; §2.2 conventions header; §5 TASKLIST row "auto-generated conventions header captures repeated patterns".

**What**: The 15-row `| Field | Value |` table appears **35 times verbatim**. Every task card duplicates the same field names. Declare them once in a conventions header and replace with 1–3 char codes in each card.

**Proposed header** (~130 bytes, one-time cost):

```
<!-- cmd-dsl v1:
[RID]=Roadmap Item ID(s) [EF]=Effort [RK]=Risk [RD]=Risk Drivers
[T]=Tier [CB]=Confidence Bar [RC]=Requires Confirmation
[CPO]=Critical Path Override [VM]=Verification Method
[MCP]=MCP Requirements [FA]=Fallback Allowed [SAD]=Sub-Agent Delegation
[DID]=Deliverable IDs [AP]=Artifacts (Intended Paths)
90=[█████████-] 90% 85=[████████--] 85% -->
```

**Before** (lines 168–184, the T01.01 field table):

```
| Field | Value |
|---|---|
| **Roadmap Item ID(s)** | R-002 |
| **Why** | All other milestones depend on these dataclasses and enums; this is the pure-data foundation with zero external dependencies |
| **Effort** | M (multiple types: 2 enums + 5 dataclasses + property methods) |
| **Risk** | Medium (model changes may be needed in later milestones) |
| **Risk Drivers** | Data model extensibility; property method correctness; spec compliance for 7 types |
| **Tier** | STRICT — keywords: model, schema, dataclass, system-wide (all milestones depend on this) |
| **Confidence Bar** | [█████████-] 90% — spec Section 2 fully defines all types |
| **Requires Confirmation** | No |
| **Critical Path Override** | Yes — foundation for entire sprint |
| **Verification Method** | Sub-agent (quality-engineer): verify all 7 types match spec Section 2 |
| **MCP Requirements** | Sequential (structured analysis of spec compliance) |
| **Fallback Allowed** | No — STRICT tier |
| **Sub-Agent Delegation** | No — single file, focused scope |
| **Deliverable IDs** | D-0001 |
| **Artifacts (Intended Paths)** | `TASKLIST_ROOT/artifacts/D-0001/spec.md`, `TASKLIST_ROOT/artifacts/D-0001/evidence.md` |
```

**After** (15 key-value pairs become compact lines; table chrome dropped since labels are coded):

```
RID:R-002 EF:M RK:Med RD:extensibility;property correctness;7-type compliance
T:STRICT(model,schema,dataclass,system-wide) CB:90(spec§2 defines all types)
RC:N CPO:Y VM:sub-agent(qe): 7 types vs spec§2  MCP:Seq(compliance analysis)
FA:N(STRICT) SAD:N(single-file) DID:D-0001
AP:[AP-1]   <!-- [AP-N]=TASKLIST_ROOT/artifacts/D-000N/{spec,evidence}.md -->
Why: foundation dataclasses/enums; zero external deps; all milestones depend.
```

**Savings per table**: original ~950 bytes, compressed ~420 bytes → ~530 bytes saved × 35 tables = **~18,500 bytes ≈ 16.6%**. Header overhead: ~130 bytes once. Net: **~18,400 bytes ≈ 16.5%.**

**Loss profile**: **Lossless** per primer §2.1 row "Abbreviate via conventions header" — every field value is recoverable given the header.

**Risk**: Decoder must respect the header. If a task card is read in isolation without the header, abbreviations become opaque. Pair with a linter that asserts every abbreviation used in body appears in header. AST transform (markdown-it-py) must handle GFM tables.

---

### Strategy S3 — Artifact-path template macros (Approach 2, primer §4.2 transform 2)

**Primer anchor**: §4.2 "Table normalization: detect repeated column values… hoist into a caption or eliminate via default"; §2.3 "Abbreviable phrases ~10-15%".

**What**: The path pair `` `TASKLIST_ROOT/artifacts/D-NNNN/spec.md`, `TASKLIST_ROOT/artifacts/D-NNNN/evidence.md` `` appears **70 times** (35 in the Deliverable Registry, 35 in task cards, plus additional references in the Traceability Matrix). Declare one macro, reference by deliverable id only.

**Header addition** (~60 bytes, one-time):

```
<!-- [A:D-NNNN]={TASKLIST_ROOT/artifacts/D-NNNN/spec.md, evidence.md} -->
```

**Before** (line 107, Deliverable Registry row for D-0001):

```
| D-0001 | T01.01 | R-002 | models.py with enums and dataclasses | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0001/spec.md`, `TASKLIST_ROOT/artifacts/D-0001/evidence.md` | M | Medium |
```

**After**:

```
|D-0001|T01.01|R-002|models.py enums+dataclasses|STRICT|SA(qe)|[A:D-0001]|M|Med|
```

**Savings**: per occurrence ~80 bytes (full pair) → ~8 bytes (`[A:D-0001]`), net ~72 bytes × 70 occurrences = **~5,000 bytes ≈ 4.5%**. (This subsumes and extends part of S2's AP row savings; in the stacked total below I net-adjust to avoid double-counting.)

**Loss profile**: **Lossless** — macro expansion is deterministic on deliverable id.

**Risk**: Linters/validators that search for literal `TASKLIST_ROOT/artifacts/D-0001/spec.md` strings will break unless they learn the macro. The tasklist validator in `superclaude sprint` should expand macros before assertion checks.

---

### Strategy S4 — Step-tag abbreviation (Approach 2, primer §4.2 transform 5)

**Primer anchor**: §4.2 transform 5 "scan for frequently-used multi-word phrases (>5 occurrences, >20 chars each)"; §2.3 "Abbreviable phrases".

**What**: Three bracketed step tags dominate: `[PLANNING]`, `[EXECUTION]`, `[VERIFICATION]`. Total 172 occurrences. Replace with single letters `[P]` `[E]` `[V]` declared in the header.

**Before** (lines 190–196, T01.01 Steps):

```
1. `[PLANNING]` Read spec Section 2 and extract all type definitions, field names, and property signatures
2. `[PLANNING]` Map enum members and dataclass fields to Python types with default values
3. `[EXECUTION]` Create `src/superclaude/cli/sprint/models.py` with PhaseStatus and SprintOutcome enums
4. `[EXECUTION]` Add Phase, SprintConfig, PhaseResult, SprintResult, MonitorState dataclasses with all fields per spec
5. `[EXECUTION]` Implement property methods: `is_terminal`, `is_success`, `is_failure`, `duration_display`, `resume_command`, `stall_status`
6. `[VERIFICATION]` Run `uv run pytest tests/sprint/test_models.py -v` to validate all types
```

**After**:

```
1. [P] Read spec §2; extract type defs, fields, property signatures
2. [P] Map enum members/dataclass fields to Python types with defaults
3. [E] Create src/superclaude/cli/sprint/models.py with PhaseStatus/SprintOutcome enums
4. [E] Add Phase/SprintConfig/PhaseResult/SprintResult/MonitorState dataclasses per spec
5. [E] Property methods: is_terminal, is_success, is_failure, duration_display, resume_command, stall_status
6. [V] Run `uv run pytest tests/sprint/test_models.py -v`
```

**Savings**: `[PLANNING]` 11 bytes → `[P]` 3 bytes = 8 saved × ~70 uses; same for `[EXECUTION]` (12→3) and `[VERIFICATION]` (15→3) × ~100 total uses. Weighted: **~1,700 bytes ≈ 1.5%.** Plus minor prose tightening shown in the example (not counted here; see S6).

**Loss profile**: **Lossless** with header.

**Risk**: None — tags are purely categorical.

---

### Strategy S5 — Prose-section label abbreviation (Approach 2, primer §4.2 transform 5)

**Primer anchor**: §4.2 transform 5; §2.3 "Abbreviable phrases".

**What**: Every task card has six labeled bullet blocks: `**Deliverables**:`, `**Steps**:`, `**Acceptance Criteria**:`, `**Validation**:`, `**Dependencies**:`, `**Rollback**:`, `**Notes**:`. Total 210 occurrences. Replace with coded section markers declared once in the header: `[D]`, `[S]`, `[AC]`, `[Val]`, `[Dep]`, `[RB]`, `[N]`.

**Before** (lines 186–210, the seven labels across T01.01):

```
**Deliverables**:
- `models.py` containing …

**Steps**:
1. `[PLANNING]` …

**Acceptance Criteria**:
1. All 7 types …

**Validation**:
1. `uv run python …`

**Dependencies**: None
**Rollback**: Delete `src/superclaude/cli/sprint/models.py`
**Notes**: Foundation task …
```

**After**:

```
[D]
- models.py containing …

[S]
1. [P] …

[AC]
1. All 7 types …

[Val]
1. `uv run python …`

[Dep]: None
[RB]: Delete src/superclaude/cli/sprint/models.py
[N]: Foundation task …
```

**Savings**: average label 16 bytes → average code 4 bytes = ~12 bytes saved × 210 occurrences = **~2,500 bytes ≈ 2.3%.**

**Loss profile**: **Lossless** with header.

**Risk**: `[AC]` conflicts if the body ever mentions "Acceptance Criteria" inline; the conventions header must scope abbreviations to start-of-line position. Primer §4.2 flags this as "auto-generated abbreviations need a review gate" — honour that gate.

---

### Strategy S6 — Redundant-prose elision in task-card `Why` and `Notes` (Approach 2, primer §4.2 transform 6)

**Primer anchor**: §4.2 transform 6 "prose summarization of introduction paragraphs (bounded, deterministic)"; §2.3 "Prose redundancy (restatement) ~8-15%".

**What**: The `Why` field and the `Notes` field frequently restate content that also appears in `Deliverables`, `Steps`, or `Acceptance Criteria`. Example: T01.01's `Why` field says "All other milestones depend on these dataclasses and enums; this is the pure-data foundation with zero external dependencies" — the same fact is stated in the Phase 1 header and the `Notes` line ("Foundation task — block all subsequent phases"). Deterministic elision rule: if `Why` content is a strict superset or near-duplicate of an earlier Phase-header sentence, reduce it to a single referential marker.

**Before** (line 171):

```
| **Why** | All other milestones depend on these dataclasses and enums; this is the pure-data foundation with zero external dependencies |
```

**After**:

```
| Why | pure-data foundation; all milestones depend |
```

**Savings**: averaged ~50 bytes per task card × 35 cards ≈ **~1,750 bytes ≈ 1.6%**. Similar elision in `Notes` where the text restates Rollback or Dependencies yields another ~1,000 bytes ≈ 0.9%.

**Loss profile**: **Borderline-lossless.** Primer §2.1 marks "drop prose explanations" as lossy. This strategy is only lossless if the elided content is verifiably restated elsewhere in the same document. Requires an AST-level duplicate-sentence check (primer §4.2 cross-reference deduplication semantics). If unsure, defer to S6-lite: only strip the trailing explanatory clause after a semicolon.

**Risk**: Moderate. Over-aggressive application corrupts rationale. Run only as part of Approach 2 with an audit diff.

---

### Strategy S7 — Traceability Matrix row compaction (Approach 2, primer §4.2 transforms 2 & 5)

**Primer anchor**: §4.2 transform 2 "table normalization: detect repeated column values… hoist into a caption or eliminate via default"; §5 TASKLIST row.

**What**: The 42-row Traceability Matrix has columns whose mode values dominate: `Tier` is mostly `STANDARD`, `Confidence` is mostly `[█████████-] 90%`, and the artifact paths are all `TASKLIST_ROOT/artifacts/D-NNNN/`. Apply: (a) declare default `Tier=STANDARD`, `Confidence=90` in a caption above the table; show only deviations; (b) drop the `Artifact Paths (rooted)` column entirely because it is derivable from `Deliverable ID(s)` given the S3 macro.

**Before** (line 1994):

```
| R-003 | T01.02 | D-0002 | STANDARD | [█████████-] 90% | `TASKLIST_ROOT/artifacts/D-0002/` |
```

**After** (with `<!-- default Tier=STANDARD Confidence=90 -->` caption):

```
|R-003|T01.02|D-0002|||
```

…or more aggressively, omit the row entirely since it carries zero deviation information, and list only the rows that deviate:

```
<!-- defaults: Tier=STANDARD Confidence=90; rows omitted = defaults; Artifact=[A:D-NNNN] -->
|R-021|T03.06|D-0018|.|85|
|R-022|T04.01–T04.03|D-0019..21|.|85|
|R-023|T04.01|D-0019|.|85|
...
```

**Savings**: matrix is ~5,200 bytes in the raw file; compacted to ~1,400 bytes. **~3,800 bytes ≈ 3.4%.**

**Loss profile**: **Lossless** — recovery requires applying the caption defaults to elided cells; this is the canonical primer §4.2 table-normalization transform.

**Risk**: Non-trivial. The Traceability Matrix is consumer-facing and used by `superclaude sprint` validation. Any consumer that expects a fully-populated table without default-expansion must be updated. Primer §4.2 "round-trip testing is non-trivial" applies — golden-test the decompressor.

---

### Strategy S8 — Deliverable Registry default-column hoisting (Approach 2, primer §4.2 transform 2)

**Primer anchor**: §4.2 transform 2 "detect repeated column values".

**What**: In the 35-row Deliverable Registry table: `Verification` is almost always one of two values (`Direct test execution` 26/35, `Sub-agent (quality-engineer)` 10/35 — note: one row differs, counted as 9 STRICT + rare override, so the default+override pattern applies). Similarly `Risk` is drawn from a four-member enum `{Low, Medium, High}` and `Effort` from `{XS, S, M, L}`. Replace verbose values with 1-letter codes declared in the header.

**Before** (line 107):

```
| D-0001 | T01.01 | R-002 | models.py with enums and dataclasses | STRICT | Sub-agent (quality-engineer) | `TASKLIST_ROOT/artifacts/D-0001/spec.md`, `TASKLIST_ROOT/artifacts/D-0001/evidence.md` | M | Medium |
```

**After** (header: `V:D=Direct test V:S=Sub-agent(qe) R:L=Low R:M=Med R:H=High`):

```
|D-0001|T01.01|R-002|models.py enums+dataclasses|STRICT|V:S|[A:D-0001]|M|R:M|
```

**Savings**: per row ~140 bytes → ~80 bytes = ~60 bytes × 35 rows = **~2,100 bytes ≈ 1.9%** (net of overlap with S3's artifact macro — the S3 macro savings are still counted above; this strategy adds the `Verification`/`Risk`/`Effort` encoding on top).

**Loss profile**: **Lossless** with header.

**Risk**: Low — enums are already small vocabularies.

---

### Strategy S9 — Checkpoint-card template deduplication (Approach 2, primer §4.2 transform 1)

**Primer anchor**: §4.2 transform 1 "heading deduplication"; §4.2 transform 2 table normalization.

**What**: 11 Checkpoint cards share the same 4-field structure: `Purpose`, `Checkpoint Report Path`, `Verification` (bullet list), `Exit Criteria` (bullet list). Extract the scaffold as a single template comment, keep only the values per checkpoint.

**Before** (lines 350–361):

```
### Checkpoint: End of Phase 1

**Purpose:** Verify foundation models and module structure
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-END.md`
**Verification:**
- All 4 tasks (T01.01–T01.04) marked completed
- models.py importable with all 7 types; `uv run pytest tests/sprint/test_models.py` passes
- `superclaude sprint --help` works
**Exit Criteria:**
- All deliverables D-0001 through D-0004 verified
- `superclaude sprint --help` works
- Phase 2 and Phase 3 unblocked
```

**After** (with `[CKPT N]` header abbreviation declared once):

```
[CKPT 1] End of Phase 1 @CP-P01-END
Purpose: Verify foundation models and module structure
Verify: tasks T01.01–T01.04 done; models.py import (7 types); `uv run pytest tests/sprint/test_models.py`; `superclaude sprint --help`
Exit: D-0001..D-0004 verified; `superclaude sprint --help` works; P2+P3 unblocked
```

**Savings**: ~180 bytes saved per checkpoint × 11 = **~2,000 bytes ≈ 1.8%**.

**Loss profile**: **Lossless** — purely syntactic.

**Risk**: Low.

---

### Strategy S10 — Template-block fencing (Approach 2, primer §4.2 transform 2 + §2.3 "Preamble & meta")

**Primer anchor**: §4.2 table normalization; §2.3 "Preamble & meta ~5-8%".

**What**: The Execution Log Template, Checkpoint Report Template, and Feedback Collection Template at the end of the file (lines 2039–2115) are **pure scaffolding** for later fill-in. They contain ~3,500 bytes of prose plus table headers. The primer §2.2 amortization rule: if this scaffold is read once per sprint by humans and never by LLMs consuming the tasklist as context, wrap it in an HTML comment or move it to a sibling file referenced by pointer. This cuts LLM-visible bytes without losing the scaffold for human use.

**Before** (lines 2052–2096, the Checkpoint Report Template code fence block):

```
## Checkpoint Report Template

```markdown
# Checkpoint Report — C{PP}.{NN}

**Phase**: {N}
… (44 lines) …
```
```

**After**:

```
## Checkpoint Report Template

<!-- template: see TASKLIST_ROOT/templates/checkpoint-report.md -->
```

**Savings**: ~3,200 bytes ≈ **2.9%** if all three templates are externalized. Or ~1,800 bytes ≈ 1.6% if only the Checkpoint Report Template (the largest) is moved.

**Loss profile**: **Lossless for LLM consumption** per primer §2.1 — the templates are never referenced by per-task execution logic; they exist to be copied once into per-phase reports. Per primer §7 rule "conventions header amortization check", this content fails the ≥5 reads threshold for LLMs.

**Risk**: Human workflow. If a user greps the tasklist for a template example, they hit a dead link until they chase the pointer. Gate: keep inline if users have asserted they scan the tasklist for templates.

---

## Section 3 — Recommended Strategy Stack

Ordered per primer §5 pipeline composition rules (rule 1: always run Approach 1 first; rule 3: Approach 2 when structural regularity dominates; rule 6: auditor gate for any lossy transform).

| # | Strategy | Approach | Lossy? | Est. saving | Cumulative |
|---|---|---|---|---:|---:|
| 1 | **S1** Whitespace + horizontal-rule collapse | A1 | No | 1.8% | 1.8% |
| 2 | **S2** Field-label conventions header | A2 | No | 16.5% | 18.3% |
| 3 | **S3** Artifact-path macro | A2 | No | 2.5%* | 20.8% |
| 4 | **S4** Step-tag abbreviation `[P]/[E]/[V]` | A2 | No | 1.5% | 22.3% |
| 5 | **S5** Prose-section label abbreviation | A2 | No | 2.3% | 24.6% |
| 6 | **S7** Traceability Matrix default hoisting | A2 | No | 3.4% | 28.0% |
| 7 | **S8** Deliverable Registry enum coding | A2 | No | 1.9% | 29.9% |
| 8 | **S9** Checkpoint card template dedup | A2 | No | 1.8% | 31.7% |
| 9 | **S10** Template-block externalization (one-of-three: Checkpoint Report Template) | A2 | No (for LLM) | 1.6% | 33.3% |
| 10 | **S6** Redundant `Why`/`Notes` prose elision | A2 | Borderline | 2.5% (combined) | **35.8%** |

\* S3 savings are net of the double-counted AP row already reduced by S2's header; adjusted from the raw ~4.5% to ~2.5% to avoid overlap.

**Projected total compression**: **~33-36%**, landing squarely in the primer §5 TASKLIST target band of 30-40% and bracketing the primer §4.2 measured ceiling of 25-33% for Approach 2 alone (the extra ~2-3% comes from the auto-conventions header, which is explicitly part of the TASKLIST strategy row).

### Rationale for ordering

1. **S1 first** — primer §5 pipeline rule 1: free, deterministic, zero risk. Run before parsing so AST work sees normalized input.
2. **S2 second** — the single largest lever (16.5%). Without it, downstream strategies operate on a still-verbose substrate. S2 also establishes the conventions-header mechanism that S3/S4/S5/S7/S8 all depend on.
3. **S3, S4, S5** are additive header abbreviations with zero structural risk; safe to run in a single AST pass after S2.
4. **S7 and S8** touch the two large matrix tables. Both require the S3 macro and conventions header. Requires golden round-trip tests per primer §4.2 "round-trip testing is non-trivial".
5. **S9** is isolated and low-risk.
6. **S10** is a consumer-DAG decision per primer §2.2 amortization check and INV-3. Only apply if the Checkpoint Report Template is proven to be read rarely by LLMs. Default: apply only the Checkpoint Report Template, leave the Execution Log Template (which humans fill during sprint) and the Feedback Collection Template inline.
7. **S6 last** — borderline-lossy, must run under an auditor diff (primer §5 pipeline rule 6). If S1-S9 already crossed 33%, S6 can be dropped entirely; the TASKLIST target is already met.

### Stop-at-30% minimal stack (safest path)

If risk budget is tight, stop after **S1+S2+S3+S4+S5 = 24.6%**. This is entirely Approach-1 and header-based; no table-hoisting, no prose elision. Falls short of the 30% target but is guaranteed lossless and reversible with a ~130-byte conventions header.

### Approaches explicitly **not** recommended

- **Approach 3 (LLM-assisted)** — primer §4.3 closing sentence and §5 TASKLIST row both say "LLM rewriting offers no marginal gain" on tasklists. The prose density is too low. Skip.
- **Code-fence touching** — primer §4.2 rule "code fences are sacrosanct". The Checkpoint Report Template fenced block is not modified by S10; we replace the fence with a pointer, we do not edit its contents.
- **Spec-style treatment** — primer §5 row warns "Spec compression is a trap". This document contains normative R-RULE-01..R-RULE-10 rules that look spec-like. They live outside the task cards and should be left untouched by S2–S9; only S1 whitespace transforms apply to them.

---

## Section 4 — Risks & Caveats Specific to This File

### 4.1 R-RULE normative rules are spec-like (primer §5 "spec compression is a trap")

Lines 39–50 contain R-RULE-01 through R-RULE-10. These are normative statements about execution semantics (phase sequencing, rollback, quality gates). Per primer §5, spec-like content should be limited to Approach 1 transforms only. **Exclusion rule for the compressor**: detect headings matching `^## Deterministic Rules Applied$` and their following block; apply only S1 within that region.

### 4.2 Confidence-bar unicode (`█`, `-`) is ASCII-art, fragile in tables

The `[█████████-] 90%` pattern appears 61 times with 90%, plus 11 times with 85% (plus others). It is purely decorative for an LLM — the numeric suffix is the only semantic payload. Replace `[█████████-] 90%` → `CB:90` in the header (covered by S2). **Risk**: if a human renders the compressed file, the visual progress bar is gone. Acceptable for LLM-first storage; not acceptable if humans consult the tasklist via cat/less on the terminal. This is an INV-3 consumer-DAG decision (primer §6).

### 4.3 TASKLIST_ROOT is a symbolic prefix, not a real path

All `TASKLIST_ROOT/…` strings are template placeholders. The macro-ification in S3 is safe because the prefix is already abstract. **However**: any downstream validator that does literal path existence checks must expand `TASKLIST_ROOT` before file I/O. Verify the `superclaude sprint` implementation already expands this variable before comparing paths.

### 4.4 GFM tables dominate — Approach 2 parser must handle them

35 `| Field | Value |` tables + 4 large registry/matrix tables. Primer §4.2 risk bullet: "GFM extensions (tables, strikethrough, task lists) need explicit plugin support". `markdown-it-py` supports GFM tables via `markdown-it-py[linkify,plugins]` or the `mdit-py-plugins` package. Confirm before running an AST pass.

### 4.5 S6 (prose elision) must run under an auditor diff

Primer §2.1 marks prose deletion as **lossy**. The temptation to trim `Why` and `Notes` is strong because they restate context, but primer §5 rule 6 is firm: "Auditor gate for any lossy transform". The auditor for this file should verify that for every elided clause, the same assertion is present in Deliverables, Steps, or Acceptance Criteria of the same task card. If the auditor cannot find a semantic duplicate, refuse the elision.

### 4.6 Conventions-header amortization (INV-3, primer §6)

The header costs ~250-300 bytes after S2+S3+S4+S5+S7+S8+S9 declarations. Primer §2.2: the header pays for itself after 5-10 body uses of each abbreviation. This file has 35-210 uses of every abbreviation — amortization is overwhelming. **However**, per primer §6 INV-3, the tasklist's real read count by LLM consumers is unmeasured. If the tasklist is generated once, consumed by `superclaude sprint`, and never re-read by an LLM, the header is overhead that should have been spent as savings foregone. The amortization check should happen in the compressor output, not be assumed.

### 4.7 Traceability Matrix round-trip risk (S7)

The matrix is consumed by `superclaude sprint validate` (or an equivalent traceability check). Primer §4.2 "round-trip testing is non-trivial" applies acutely: the decompressor must expand default cells before the validator reads them. Add a golden test: compress → decompress → diff against original; require zero diff. This is the single highest-risk strategy in the stack; it is included because its 3.4% saving materially helps hit the 30% target, but can be dropped to 30.9% cumulative (still in-band) if the round-trip harness is not yet in place.

### 4.8 INV-1 tokenizer generalization still unresolved (primer §6)

All byte-percentage estimates in this analysis are byte counts, not Claude-native tokens. Bytes correlate strongly with tokens but are not identical. Primer §6 expects ±2-8 percentage-point drift between `tiktoken cl100k_base` and Anthropic `messages.count_tokens`. Byte-to-token drift is plausibly similar. **Action**: re-measure the compressed output with Anthropic's `messages.count_tokens` endpoint before claiming the 33-36% number operationally.

### 4.9 File is already archived under `complete/`

The target path is `.dev/releases/complete/v2.05-sprint-cli-specification/`. This is a **finished** sprint artifact — unlikely to be re-read by an LLM consumer in the normal pipeline. If the read-count is effectively zero, **none** of these strategies pay off (primer §2.2: header cost vs amortization). The compression case here is archival-storage, not live-context, and the savings are disk-bytes. For a live sprint tasklist (under `.dev/releases/current/`), the same analysis applies but amortization is guaranteed because `superclaude sprint` re-reads it on every phase transition.
