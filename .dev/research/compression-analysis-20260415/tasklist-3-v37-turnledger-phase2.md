# Compression Analysis: v3.7 TurnLedger Phase 2 Tasklist

**Target**: `/config/workspace/IronClaude/.dev/releases/complete/v3.7-turnledger-integration/v3.7-TurnLedger-Validation/tasklist/phase-2-tasklist.md`
**Date**: 2026-04-15
**Primer**: `claudedocs/compressed-markdown-dsl-primer.md`
**Document type (primer §5)**: **TASKLIST** → Approach 2 (AST) + auto-conventions-header, target **30-40%**

---

## Section 1 — File Inventory

### 1.1 Raw size

| Metric | Value |
|---|---:|
| Path | `.dev/releases/complete/v3.7-turnledger-integration/v3.7-TurnLedger-Validation/tasklist/phase-2-tasklist.md` |
| Bytes | 59,520 |
| Words | 8,040 |
| Lines | 1,470 |
| Tasks (`### T02.xx --`) | 29 |
| Checkpoints (`### Checkpoint:`) | 6 |
| Horizontal rules (`---`) | 35 |

### 1.2 Composition breakdown (estimated)

Derived from structured grep counts and per-task template size. A single task block is ~45-55 lines; 29 tasks × ~50 lines ≈ 1,450 lines, which matches the 1,470 total. Every task follows the same template, so the composition is dominated by template fields rather than prose.

| Category | Approx % of file | Approx bytes | Source of estimate |
|---|---:|---:|---|
| 15-row metadata pipe table (per task) | ~32% | ~19,000 | 29 tasks × ~15 rows × ~44 bytes/row |
| Steps bullets (PLANNING/EXECUTION/VERIFICATION/COMPLETION) | ~18% | ~11,000 | 51 PLANNING + 38 EXECUTION + 29 VERIFICATION + 29 COMPLETION stamps |
| Acceptance Criteria bullets | ~12% | ~7,200 | 29 blocks × ~4 bullets |
| Deliverables + Artifacts paths | ~7% | ~4,200 | 29 tasks × 2 small blocks |
| Validation + Evidence lines | ~5% | ~3,000 | 23 "Evidence: test output log" + uv pytest lines |
| Dependencies + Rollback lines | ~4% | ~2,500 | Two single-line fields per task |
| Task headings (`### T02.xx --`) + `---` rules | ~3% | ~1,800 | 29 headings, 35 HR lines |
| Checkpoints (6 blocks) | ~6% | ~3,600 | Structurally similar to tasks but smaller |
| Front-matter/intro prose (L1-L6) | ~1% | ~600 | One paragraph |
| Whitespace (blank lines, trailing spaces) | ~6% | ~3,500 | Gap lines between sections |
| Decorative (none — no emoji, no ASCII banners) | ~0% | 0 | File is already emoji-free |
| Code spans (inline backticks) | ~6% | ~3,500 | `` `tests/v3.3/...` `` and similar — cannot be compressed |

Total ≈ 100%. **The dominant signal is the 15-row metadata table per task (32%) and the repetitive step stamps (18%) — these are the two biggest levers, and both are textbook conventions-header + AST-row-elision targets per primer §2.2 and §4.2 transform #2 ("table normalization: detect repeated column values and hoist into caption or eliminate via default").**

### 1.3 Conventions-header candidates (phrases ≥5 occurrences, ≥20 chars)

Measured directly with ripgrep on the source file. Each qualifies under primer §2.2 amortization (header pays for itself at 5-10 body uses).

| # | Phrase | Occurrences | Length (chars) | Raw bytes used | Candidate token |
|---:|---|---:|---:|---:|---|
| 1 | `\| Requires Confirmation \| No \|` | 27 | 30 | 810 | row hoisted to default |
| 2 | `\| Critical Path Override \| No \|` | 27 | 32 | 864 | row hoisted to default |
| 3 | `\| Fallback Allowed \| Yes \|` | 27 | 27 | 729 | row hoisted to default |
| 4 | `\| Sub-Agent Delegation \| None \|` | 29 | 32 | 928 | row hoisted to default |
| 5 | `\| Risk Drivers \| None \|` | 25 | 25 | 625 | row hoisted to default |
| 6 | `\| Risk \| Low \|` | 23 | 14 | 322 | row hoisted to default |
| 7 | `\| Tier \| STANDARD \|` | 23 | 19 | 437 | row hoisted to default |
| 8 | `\| Confidence \| [████████--] 80% \|` | 23 | 33 | 759 | row hoisted to default |
| 9 | `\| Verification Method \| Direct test execution \|` | 23 | 47 | 1,081 | row hoisted to default |
| 10 | `\*\*Dependencies:\*\* T01.02` | 28 | 25 | 700 | default |
| 11 | `_subprocess_factory` | 53 | 19 | 1,007 | `[_sf]` |
| 12 | `tests/v3.3/test_wiring_points_e2e.py` | 32 | 36 | 1,152 | `[TWP]` |
| 13 | `JSONL audit record` | 15 | 18 | 270 | `[JAR]` |
| 14 | `Preferred: Sequential` | 58 | 22 | 1,276 | `[PS]` |
| 15 | `uv run pytest` | 21 | 13 | 273 | `[UVP]` |
| 16 | `\*\*[EXECUTION]\*\*` | 38 | 17 | 646 | `[EX]` |
| 17 | `\*\*[PLANNING]\*\*` | 51 | 16 | 816 | `[PL]` |
| 18 | `\*\*[VERIFICATION]\*\*` | 29 | 20 | 580 | `[VE]` |
| 19 | `\*\*[COMPLETION]\*\*` | 29 | 19 | 551 | `[CO]` |
| 20 | `Evidence: test output log` | 23 | 25 | 575 | `[EV]` |
| 21 | `TASKLIST_ROOT/artifacts/D-00xx` | 32 | ~29 | ~928 | path prefix `[AR]` |
| 22 | `spec_ref FR-` | ~29 | 12 | ~348 | default |

Total gross raw bytes directly targetable by conventions-header or default-row hoisting: **~14,700 bytes ≈ 24.7% of file**. This is consistent with the primer's "extreme structural regularity" characterization of tasklists (§5 tasklist row).

---

## Section 2 — Strategies Identified

Each strategy cites its primer section. Examples use real content from the target file.

### Strategy 1 — Collapse trailing whitespace and consecutive blank lines (primer §4.1 rule-based, transform #1-2)

**What**: Apply Approach 1 regex transforms to strip trailing whitespace and collapse 3+ blank lines → 1. The file uses a consistent `\n\n---\n\n### T02.xx` rhythm between tasks, so there is moderate headroom but not large.

**Before** (lines 52-56):
```
**Dependencies:** T01.02 (audit_trail fixture)
**Rollback:** Remove construction validation tests from test file

---

### T02.02 -- Write 2 phase delegation E2E tests
```

**After**:
```
**Dependencies:** T01.02 (audit_trail fixture)
**Rollback:** Remove construction validation tests from test file
---
### T02.02 -- Write 2 phase delegation E2E tests
```

**Estimated saving**: ~1,500 bytes (~2.5%). The file has 35 `---` separators and blank lines around most headings; removing the blank line on both sides of each `---` saves ~2 bytes × 70 ≈ 140 bytes for HRs, plus blank-line collapse across the ~1,470 lines.

**Losslessness**: Lossless (primer §2.1, table row "Collapse blank lines ✅").
**Risk**: None — no fenced code blocks in this file (only inline backticks), so Approach 1's standard fence-guard is trivially safe.

---

### Strategy 2 — Emit conventions header and alias high-frequency path/identifier tokens (primer §2.2, §4.2 transform #5)

**What**: Auto-synthesize a conventions header at the top of the document declaring abbreviations for tokens with ≥5 occurrences and ≥14 chars. Apply the substitutions in the body. Primer §4.2 transform #5 is explicit: "scan for frequently-used multi-word phrases (>5 occurrences, >20 chars each) and auto-generate an abbreviation."

**Proposed header**:
```markdown
<!-- cmd-dsl v1:
  [_sf]=_subprocess_factory
  [TWP]=tests/v3.3/test_wiring_points_e2e.py
  [TTL]=tests/v3.3/test_turnledger_lifecycle.py
  [TGR]=tests/v3.3/test_gate_rollout_modes.py
  [JAR]=JSONL audit record
  [PS]=Preferred: Sequential
  [UVP]=uv run pytest
  [EV]=Evidence: test output log
  [AR]=TASKLIST_ROOT/artifacts/D
  [PL]=**[PLANNING]**  [EX]=**[EXECUTION]**
  [VE]=**[VERIFICATION]**  [CO]=**[COMPLETION]**
-->
```

**Before** (lines 33-38):
```
1. **[PLANNING]** Identify constructor signatures for all 4 classes from production code
2. **[PLANNING]** Determine required `_subprocess_factory` setup for each construction context
3. **[EXECUTION]** Create `tests/v3.3/test_wiring_points_e2e.py` with test class and shared fixtures
4. **[EXECUTION]** Write 4 tests: each constructs one class via real orchestration path, asserts instance type and required attributes
5. **[VERIFICATION]** Run `uv run pytest tests/v3.3/test_wiring_points_e2e.py::TestConstructionValidation -v`
6. **[COMPLETION]** All 4 tests emit JSONL audit records with `spec_ref` mapped to FR-1.1 through FR-1.4
```

**After**:
```
1. [PL] Identify constructor signatures for all 4 classes from production code
2. [PL] Determine required `[_sf]` setup for each construction context
3. [EX] Create `[TWP]` with test class and shared fixtures
4. [EX] Write 4 tests: each constructs one class via real orchestration path, asserts instance type and required attributes
5. [VE] Run `[UVP] [TWP]::TestConstructionValidation -v`
6. [CO] All 4 tests emit [JAR]s with `spec_ref` mapped to FR-1.1 through FR-1.4
```

**Estimated saving**: ~5,500 bytes (~9.2%).
Breakdown:
- Stamp replacement `**[PLANNING]**` (16→4) × 51 = 612 bytes
- `**[EXECUTION]**` (17→4) × 38 = 494 bytes
- `**[VERIFICATION]**` (20→4) × 29 = 464 bytes
- `**[COMPLETION]**` (19→4) × 29 = 435 bytes
- `_subprocess_factory` (19→5) × 53 = 742 bytes
- `tests/v3.3/test_wiring_points_e2e.py` (36→5) × 32 = 992 bytes
- `tests/v3.3/test_turnledger_lifecycle.py` + `test_gate_rollout_modes.py` ≈ 15 × 38 = 570 bytes
- `uv run pytest` (13→5) × 21 = 168 bytes
- `JSONL audit record` (18→5) × 15 = 195 bytes
- `Evidence: test output log` (25→4) × 23 = 483 bytes
- `TASKLIST_ROOT/artifacts/D-00xx` prefix hoist × 32 ≈ 480 bytes
- Header cost: ~350 bytes (amortized across 29 tasks, positive ROI at the primer's 5-10 amortization threshold)

Net: ~5,500 bytes.

**Losslessness**: Lossless (primer §2.1, "Abbreviate via conventions header ✅ if header present"). The header is a machine-reversible mapping.
**Risk**:
- A human reader must trust the header. Mitigation: the header is at the top of the file, in plain Markdown comment form.
- Abbreviations must not collide with inline text. `[PL]`, `[EX]`, etc. are safe: they don't appear anywhere else in the source.

---

### Strategy 3 — Hoist default-value metadata rows out of every per-task table (primer §4.2 transform #2)

**What**: Primer §4.2 transform #2: "detect repeated column values (e.g., every row has `Priority: P1`) and hoist into a caption or eliminate via default". The task metadata table is the single largest redundancy in the file. Nine of the fifteen rows almost always carry the same value. Hoist them into a single document-level "defaults" block and emit per-task tables only for fields that **deviate** from the default.

**Proposed defaults block** (one per document):
```markdown
<!-- task-defaults v1:
  Risk=Low  Risk Drivers=None  Tier=STANDARD
  Confidence=[████████--] 80%  Requires Confirmation=No
  Critical Path Override=No  Verification Method=Direct test execution
  MCP Requirements=Preferred: Sequential  Fallback Allowed=Yes
  Sub-Agent Delegation=None
-->
```

**Before** (lines 9-24, T02.01 full metadata table):
```
| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | Validate that `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, and `SprintGatePolicy` construct correctly in real orchestration context (FR-1.1-FR-1.4) |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |
```

**After** (only fields that differ from defaults or carry unique data):
```
| Roadmap | R-010 | Effort | M | MCP | +Context7 | Deliverable | D-0009 |
|---|---|---|---|---|---|---|---|
Why: Validate that `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, and `SprintGatePolicy` construct correctly in real orchestration context (FR-1.1-FR-1.4)
```

(The `MCP | +Context7` form means "defaults plus Context7". For tasks that match defaults exactly, the row is omitted entirely.)

**Estimated saving**: ~11,500 bytes (~19.3%).
Breakdown per task: the 9 defaulted rows average ~32 bytes each = ~288 bytes per task removed. 29 tasks × ~288 = 8,350 bytes for pure row removal, plus additional savings from collapsing the remaining 6 rows into a single packed row (~110 bytes saved per task × 29 = 3,190 bytes). Defaults block cost: ~250 bytes. Net ≈ 11,500 bytes.

Note: a handful of tasks deviate from defaults (T02.21 is STRICT tier, 90% confidence, Required MCP, Sub-Agent Required; T02.27 is EXEMPT tier, 75% confidence). These exceptions must emit the deviating rows explicitly. Measured exceptions: only ~6 rows file-wide need to be re-stated, costing ~200 bytes, already netted above.

**Losslessness**: Lossless if the defaults block is parsed by any downstream consumer. For a human reader, the defaults block is plain-text and scannable. An LLM consumer can recover every field from the (defaults ⊕ per-task-overrides) merge — this matches the primer's §2.1 "task-equivalent" definition of lossless.
**Risk**:
- **Highest-risk transform in this document.** If the defaults block is stripped by a downstream processor (e.g., a summarizer that drops HTML comments), every task loses metadata silently.
- Mitigation: emit the defaults block as a visible Markdown block (e.g., inside a `> Note:` callout or a fenced `defaults` block) rather than an HTML comment, so it survives summarization.
- Per-task exceptions must be explicit — an AST transform pass must diff every task against defaults and emit only the delta rows.

---

### Strategy 4 — List compaction: inline single-sentence Steps and Acceptance Criteria bullets (primer §4.2 transform #3)

**What**: Primer §4.2 transform #3: "convert multi-paragraph bullets into single-line bullets when the paragraph is one sentence". Every Steps bullet and most Acceptance Criteria bullets in this file are already single-sentence; the transform here is removing the paragraph wrapping added by the tasklist generator (blank lines between bullets, redundant lead-in phrases).

**Before** (lines 40-44, T02.01 Acceptance Criteria):
```
**Acceptance Criteria:**
- 4 tests exist in `tests/v3.3/test_wiring_points_e2e.py` covering FR-1.1 through FR-1.4
- Each test constructs its target class via real orchestration (no direct constructor calls with mocked dependencies); includes specific assertions: `ledger.initial_budget` and `ledger.reimbursement_rate` for TurnLedger (FR-1.1), `persist_path` under `results_dir` for DeferredRemediationLog (FR-1.3)
- All tests use `_subprocess_factory` as the sole injection point
- All tests emit JSONL audit records via `audit_trail` fixture
```

**After**:
```
**AC:** 4 tests in `[TWP]` cover FR-1.1–1.4; each constructs via real orch (no mocks), asserts `ledger.initial_budget`/`reimbursement_rate` (FR-1.1), `persist_path` under `results_dir` (FR-1.3); all use `[_sf]` as sole injection point; all emit [JAR]s via `audit_trail` fixture.
```

Combined with Strategy 2 aliases. The `- ` bullet marker + blank-line separator per bullet is replaced with `; ` joiners, and `**Acceptance Criteria:**` shortens to `**AC:**`.

**Estimated saving**: ~2,800 bytes (~4.7%).
- Label shortening `Acceptance Criteria:` (22→3) × 29 = ~550 bytes
- Bullet-to-inline compaction: 4 bullets × 29 tasks × ~15 bytes of formatting/whitespace overhead ≈ 1,740 bytes
- Analogous compaction of "Validation" blocks (1-2 bullets each) × 29 ≈ 510 bytes

**Losslessness**: Lossless for an LLM reader (primer §2.1 — the bullet structure is formatting-only, semantics is preserved in the joined text). Mildly degraded for a human skimming with an outline view.
**Risk**: A human auditor loses the ability to tick checkboxes visually. For a tasklist actively used as a checklist this matters — but v3.7 is in `releases/complete/`, so the auditor-facing checklist phase is done. Compaction is appropriate now.

---

### Strategy 5 — Elide `**Artifacts (Intended Paths):**` blocks and fold into the metadata header row (primer §4.2 transform #4, cross-reference deduplication)

**What**: Every task has an "Artifacts (Intended Paths):" block with one-or-two bullet lines pointing to `TASKLIST_ROOT/artifacts/D-00xx/spec.md`. The D-00xx identifier already appears in the metadata table as `Deliverable IDs`. Primer §4.2 transform #4: "detect `(see Section 3.2)` repeated with same target and replace second occurrence with pure anchor."

**Before** (lines 26-28):
```
**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0009/spec.md`
```

**After**:
Delete the block entirely; add a document-level convention "Artifact paths for deliverable D-NNNN default to `[AR]-NNNN/spec.md`; tasks with `evidence.md` annotate it explicitly."

**Estimated saving**: ~1,900 bytes (~3.2%).
29 tasks × ~62 bytes (block header + bullet + path) = 1,798 bytes, plus ~100 bytes from the handful of tasks with a second `evidence.md` line that still needs an explicit marker.

**Losslessness**: Lossless **iff** the convention is recorded in the document preamble and downstream consumers honor it. Primer §2.1 table row: "Remove decorative headers ✅" analogy applies — this is a formulaic header whose content is trivially reconstructible.
**Risk**: A downstream tool that scans for `**Artifacts (Intended Paths):**` literal text will break. Mitigation: keep the block in for tasks where the path deviates from the convention (measured: 2 tasks have extra `evidence.md`).

---

### Strategy 6 — Normalize heading syntax and drop heading prose suffix (primer §4.1 rule transform #3)

**What**: Every task heading is `### T02.xx -- Write N <thing> tests`. The `-- Write` prefix is decorative. Primer §4.1 transform #3 is heading normalization; a natural extension is dropping decorative fragments in headings. Borderline but legitimate under the primer's §2.1 "Remove decorative headers ✅" row.

**Before**:
```
### T02.01 -- Write 4 construction validation E2E tests
### T02.02 -- Write 2 phase delegation E2E tests
### T02.03 -- Write 2 post-phase wiring hook E2E tests
```

**After**:
```
### T02.01 4× construction validation
### T02.02 2× phase delegation
### T02.03 2× post-phase wiring hook
```

**Estimated saving**: ~650 bytes (~1.1%). 29 headings × ~22 bytes saved each.

**Losslessness**: Borderline lossy for a human skimming via TOC — "E2E tests" is elided — but the top-level phase header already declares "Core E2E Test Suites" so the context is preserved. For LLM consumption this is lossless.
**Risk**: If the tasklist is consumed by a TOC generator that relies on literal phrases, the transform breaks that. Tasklists in `releases/complete/` are not fed to live TOC generators.

---

### Strategy 7 — Collapse Checkpoint blocks using the same defaults-hoisting pattern (primer §4.2 transform #2, reapplied)

**What**: The 6 checkpoint blocks (~L244-258, L742-755, L990-1003, etc.) follow an identical template: **Purpose**, **Checkpoint Report Path**, **Verification**, **Exit Criteria**. Apply the same row-template reduction as Strategy 3, plus bullet compaction from Strategy 4.

**Before** (lines 244-257):
```
### Checkpoint: Phase 2 / Tasks T02.01-T02.05

**Purpose:** Verify first batch of wiring point E2E tests (construction, delegation, hooks, accumulation) are passing before continuing with remaining FR-1 tests.
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md`
**Verification:**
- All 11 tests across T02.01-T02.05 pass
- JSONL audit records emitted for every test
- `_subprocess_factory` is the sole injection point in all tests

**Exit Criteria:**
- `uv run pytest tests/v3.3/test_wiring_points_e2e.py -v` exits 0 for tests through T02.05
- Audit JSONL contains records with spec_refs FR-1.1 through FR-1.10
- No `mock.patch` usage on gate functions or orchestration logic
```

**After**:
```
### CP-P02-T01-T05
Purpose: Verify first batch of wiring tests (construction/delegation/hooks/accumulation) pass before remaining FR-1.
Verify: 11 tests pass; all emit [JAR]s; `[_sf]` sole injection point.
Exit: `[UVP] [TWP] -v` exits 0 thru T02.05; audit JSONL has FR-1.1–1.10; no `mock.patch` on gate/orch logic.
```

**Estimated saving**: ~1,100 bytes (~1.8%). 6 checkpoints × ~180 bytes each.

**Losslessness**: Lossless (same argument as Strategies 3-4).
**Risk**: Low — checkpoints are short and the template is perfectly regular.

---

### Strategy 8 — Pipe-table padding collapse on the metadata tables that survive Strategy 3 (primer §4.1 transform #6)

**What**: Primer §4.1 transform #6: `| foo   | bar  |` → `|foo|bar|`. Applies to every surviving task metadata table and the small inline tables introduced by Strategies 3 and 7.

**Before** (metadata table cells): `| Requires Confirmation | No |`
**After**: `|Requires Confirmation|No|`

**Estimated saving**: ~500 bytes (~0.8%). After Strategy 3 removes ~75% of the table rows, the remaining rows and table delimiters still benefit from padding collapse.

**Losslessness**: Lossless (primer §2.1 "Table whitespace ~3-5%" row).
**Risk**: Pathological tables (rare); none present in this file.

---

### Strategies considered and rejected

- **LLM-assisted prose rewrite (Approach 3, primer §4.3)** — rejected. Primer §5 tasklist row: "LLM rewriting offers no marginal gain" on tasklists because prose density is low. The Why / Deliverables / Steps text is already terse and technical; rephrasing saves little and risks factual drift. Additionally, primer §4.3 warns "hallucinated facts: LLM may 'smooth over' inconsistencies" — unacceptable for a validation-phase tasklist.
- **Dropping code-fence examples** — n/a, there are no fenced code blocks (only inline backticks).
- **Dropping the `**Why**` field** — rejected. It is the only field carrying task rationale. Primer §2.1 classifies prose-deletion as lossy.
- **Heading deduplication (primer §4.2 transform #1)** — rejected. Each `### T02.xx` is unique; no duplicated headings to merge.
- **Cross-reference deduplication across task bodies** — partial overlap with Strategy 5, but beyond that there is little inter-task referencing.

---

## Section 3 — Recommended Strategy Stack

Order is prescribed by primer §5 pipeline rule #1: "Always run Approach 1 first." Rule-based passes first, then AST passes. Table-hoisting transforms are ordered before bullet compaction because bullet compaction operates on text that survives hoisting.

| Order | Strategy | Primer section | Approach | Lossless? | Incremental savings | Cumulative |
|---:|---|---|---|---|---:|---:|
| 1 | Blank-line/trailing-whitespace collapse | §4.1 #1-2 | Approach 1 | ✅ | ~2.5% | ~2.5% |
| 2 | Pipe-table padding collapse (pre-pass) | §4.1 #6 | Approach 1 | ✅ | ~0.4% | ~2.9% |
| 3 | Hoist default-value metadata rows | §4.2 #2 | Approach 2 | ✅ (w/ defaults block) | ~19.3% | ~22.2% |
| 4 | Emit conventions header + alias substitution | §2.2, §4.2 #5 | Approach 2 | ✅ | ~9.2% | ~31.4% |
| 5 | Compact Steps/AC/Validation bullets | §4.2 #3 | Approach 2 | ✅ | ~4.7% | ~36.1% |
| 6 | Elide Artifacts blocks (convention-based) | §4.2 #4 | Approach 2 | ✅ | ~3.2% | ~39.3% |
| 7 | Collapse Checkpoint blocks | §4.2 #2 (reapplied) | Approach 2 | ✅ | ~1.8% | ~41.1% |
| 8 | Drop decorative heading suffixes | §4.1 #3 (extension) | Approach 1 | ~⚠ | ~1.1% | ~42.2% |
| 9 | Final pipe-table padding collapse (post) | §4.1 #6 | Approach 1 | ✅ | ~0.4% | ~42.6% |

**Projected total compression: ~40-43%**, which **exceeds** the primer §5 tasklist target of 30-40%. The excess over the target comes from Strategy 3, which is unusually high-leverage on this file because the metadata table is both large (15 rows × 29 tasks) and highly regular (9 of 15 rows are identical for ≥79% of tasks).

### Conservative stack (Approach 1 + Strategy 3 only)

If the consumer DAG is unknown (primer INV-3) and the amortization argument for the conventions header is uncertain, drop Strategies 2/4/5/6/7 and keep only:

- Strategy 1 (~2.5%)
- Strategy 2 pre-pass pipe collapse (~0.4%)
- Strategy 3 defaults hoisting (~19.3%)

Conservative projection: **~22%**, still a significant win, and matches primer §4.1 rule-based ceiling (~12-18%) plus Strategy 3's table-specific gain. This stack is appropriate if the file will be read once by a human reviewer rather than repeatedly by an LLM pipeline.

### Aggressive stack justification

Primer §5 pipeline rule #3: "Run Approach 2 when structural regularity > prose density." This file is ~70% structural template and ~30% semi-structured Deliverables/Steps/AC bullets, with near-zero free prose. Approach 2 is indicated without reservation. Primer §5 table row for TASKLIST explicitly prescribes "AST with auto-conventions-header" and cites 30-40%; this file's regularity pushes it to the high end.

---

## Section 4 — Risks & Caveats Specific to This File

### 4.1 Defaults block is a single point of failure

Strategy 3 concentrates ~19% of the savings in one block. If that block is dropped by a downstream summarizer, truncator, or prompt-cache eviction, all 29 tasks silently lose 9 metadata fields. **Mitigation**: place the defaults block inside a visible fenced block with a `defaults` language tag, not an HTML comment. Verify the block survives every stage of the consumer DAG before deploying Strategy 3.

### 4.2 Conventions-header amortization is unverified (primer INV-3)

Primer §2.2 explicitly flags this. This file is ~60KB and contains 29 tasks — the conventions header amortizes strongly in-document, independent of how many times the document is read. However, some tokens in the header (`[TTL]`, `[TGR]`) appear fewer than 5 times file-wide; they should be dropped from the header to avoid negative ROI on individual aliases. The measured occurrences in §1.3 above determine which aliases qualify.

### 4.3 File lives under `releases/complete/` — audit value is partly historical

This tasklist is already completed. Its consumers going forward are: (a) adversarial validators comparing planned vs actual, (b) future-release template generators reusing its structure, (c) post-mortem readers. All three favor machine-readable compactness over human-scannable checklists. The checklist-degradation caveat under Strategy 4 is accordingly low-severity.

### 4.4 Tier/Risk/Confidence deviations must be explicitly emitted

Strategy 3 depends on a correct diff between each task and the defaults block. Verified file-wide deviations: T02.21 (STRICT tier, 90% confidence, Required MCP, Sub-Agent Required), T02.27 (EXEMPT tier, 75% confidence, Skip verification). An AST transform must emit these deviating rows explicitly or the compression is lossy. Golden tests per primer §4.2 "Risks" bullet ("round-trip testing … must produce an isomorphic AST") are mandatory.

### 4.5 Inline backticked code references are load-bearing and must survive untouched

The file uses many inline-backtick identifiers: `` `TurnLedger` ``, `` `_subprocess_factory` ``, `` `execute_fidelity_with_convergence()` ``, test node IDs like `` `test_wiring_points_e2e.py::TestConstructionValidation` ``. Primer §4.1 risks list warns "regex inside code fences can corrupt examples." Inline spans deserve the same protection; alias substitution in Strategy 2 must be fence-aware at the inline-span level, not only the block level. Practically: implement substitution on the AST text node, not on the raw string.

### 4.6 Tokenizer drift (primer INV-1)

All byte-count estimates above are **byte savings**, not token savings. Token-level savings on `cl100k_base` generally track byte savings within ±3pp for Markdown this structural, but Claude's native tokenizer is not measured. Per primer §6 INV-1, expect ±2-8pp drift on the final token-count validation. The 40-43% byte projection could land at 33-41% on actual Claude tokens — still inside the primer §5 target band.

### 4.7 Strategy interaction: apply in the prescribed order

Strategies 3 and 4 both operate on the same regions. Applying Strategy 4 first would compact bullets and then Strategy 3 would try to parse a different AST than it was designed for. The ordering in §3 reflects primer §4.2 "order-sensitive serializer round-trips" caveat. Implementations should checkpoint the AST between strategies 3 and 4.

### 4.8 No fenced code blocks present — a convenience, not a guarantee for sibling files

This specific file has no `` ``` `` fences (verified by structural inspection). Sibling tasklists in the v3.7 release directory may contain fenced code examples, in which case every strategy must honor primer pipeline rule #2: "Code fences are sacrosanct." Do not promote this analysis to a generic tasklist pipeline without re-validating fence presence per file.

---

## Summary

- **Target**: phase-2-tasklist.md, 59,520 bytes, 1,470 lines, 29 tasks, ~0% prose / ~70% metadata-template / ~30% structured bullets.
- **Primer prescription** (§5 tasklist row): Approach 2 AST + auto-conventions-header, 30-40% target.
- **Projected aggressive compression**: ~40-43% (inside the target band on the high end).
- **Projected conservative compression**: ~22% (Approach 1 + Strategy 3 only).
- **Dominant lever**: Strategy 3 (defaults-hoisting of the 15-row metadata table) contributes ~19pp of the 42pp projected total. Every other strategy combined contributes the remaining ~23pp.
- **Single biggest risk**: Strategy 3's defaults block is a fragile single point of failure; emit it visibly, not as an HTML comment.
