# Compression Analysis: v3.7a Pipeline Reliability SPEC

**Target**: `/config/workspace/IronClaude/.dev/releases/backlog/v3.7-task-unified-v2/release-split/v3.7a-pipeline-reliability-SPEC.md`
**Reference primer**: `/config/workspace/IronClaude/claudedocs/compressed-markdown-dsl-primer.md`
**Document class**: SPEC (contract-grade, fidelity-first)
**Primer governing row**: §5 — Spec row: "Approach 1 (rule-based) only", **target 10-15%**, rationale "Specs are contracts. Compression must be reversible and auditable; AST transforms introduce risk of semantic drift on normative language."
**Analysis date**: 2026-04-15

---

## Section 1 — File Inventory

| Metric | Value |
|---|---|
| Path | `v3.7a-pipeline-reliability-SPEC.md` |
| Bytes | 77,176 |
| Chars | 76,354 |
| Lines | 1,172 |
| Headings (ATX) | 51 |
| Fenced code lines (incl. fences) | 432 |
| Table lines | 159 |
| Blank lines | 271 |
| Horizontal rules (`---` on own line) | 17 |
| Trailing-whitespace lines | 0 |
| Emoji count | 0 |
| Non-ASCII chars (box-drawing + em-dashes) | 411 |
| Bold-prefix labels (`**Xxx**:`) | 104 |

### Composition by category (bytes)

| Category | Bytes | % of total | Notes |
|---|---:|---:|---|
| Fenced code blocks (incl. fences) | 15,745 | 20.6% | 25 blocks: python snippets, 2 ASCII diagrams, 1 dependency-graph box-drawing |
| Pipe tables | 30,352 | 39.8% | 20+ tables: Evidence, Design Decisions, Modified Files, Interface Contracts, NFRs, Risks, Test Plan, Gap Analysis, Glossary, References |
| Prose paragraphs + lists | 28,213 | 37.0% | FR sections dominate (28 functional-requirement subsections) |
| Headings | 1,742 | 2.3% | 51 ATX headings, nested up to 4 levels |
| Blank lines | 234 | 0.3% | Already near-minimal (single blank lines only) |
| Horizontal rules | 68 | 0.1% | 17 `---` separators between FR sections |

### Repeating structural patterns (conventions-header candidates)

| Repeated token | Occurrences | Avg len | Body bytes |
|---|---:|---:|---:|
| `executor.py` | 45 | 11 | 495 |
| `TaskResult` | 39 | 10 | 390 |
| `process.py` | 28 | 10 | 280 |
| `models.py` | 28 | 9 | 252 |
| `count_turns_from_output` | 25 | 23 | 575 |
| `task-unified` | 25 | 12 | 300 |
| `extract_task_block` | 22 | 18 | 396 |
| `gate_rollout_mode` | 20 | 17 | 340 |
| `monitor.py` | 11 | 10 | 110 |
| `config.py` | 10 | 9 | 90 |

### Repeated labelled sub-section blocks (FR schema)

| Label | Count |
|---|---:|
| `**Description**:` | 12 |
| `**Current code**` / `**After code**` pair | 5 / 4 |
| `**Acceptance Criteria**:` | 14 |
| `**Verification Contract**:` | 12 |
| `**Impact Analysis**:` | 9 |
| `**Approach Evaluated and Rejected**:` | 5 |
| `**Consequence Analysis**:` | 5 |
| `**Commit Boundary**:` | 14 |
| `**Rollback Plan**:` | 12 |
| `**Dependencies**:` | 13 |
| TOTAL labelled lines | 104 |

### Baseline-ceiling observation

The document is already **unusually clean**:

- Zero trailing whitespace
- Zero emoji
- Blank-line budget already at single-blank minimum (0.3% of bytes)
- ATX headings throughout (no `===`/`---` underline style)
- Bullet markers already normalised to `-`
- No `<!-- comment -->` blocks

This means the "free wins" category of Approach 1 (primer §4.1 items 1-4, 7, 10) is mostly already banked. The remaining pressure has to come from **abbreviation via a conventions header** (primer §2.2) and **pipe-table padding collapse** (primer §4.1 item 6), plus residual heading/HR savings.

---

## Section 2 — Strategies Identified

Every strategy below is anchored in the primer. Because this is a SPEC, the primer §5 spec row restricts us to **Approach 1 (rule-based) only**; any strategy that requires AST semantic rewriting or LLM rewriting is either rejected outright or noted as out-of-scope and not counted in the final stack.

### Strategy S1 — Pipe-table padding collapse

**Primer anchor**: §4.1 Approach 1 item 6 ("Collapse pipe-table padding: `| foo   | bar  |` → `|foo|bar|`"); §2.3 "Table whitespace ~3-5%".

**Applies because**: Tables account for 39.8% of bytes (30,352), dominating every other category. Most rows use padded pipes with column alignment whitespace.

**Before** (lines 32-33 from §1.1 Evidence table):
```
| Evidence | Source | Impact |
|----------|--------|--------|
| `turns_consumed` hardcoded to `0` at `executor.py:1092` -- comment says "Turn counting is wired separately in T02.06" but T02.06 does not exist in any release spec | `executor.py:1091-1092` | TurnLedger reimbursement math produces `int(0 * 0.8) = 0` for every task. Budget tracking is non-functional. |
```

**After**:
```
|Evidence|Source|Impact|
|-|-|-|
|`turns_consumed` hardcoded to `0` at `executor.py:1092` -- comment says "Turn counting is wired separately in T02.06" but T02.06 does not exist in any release spec|`executor.py:1091-1092`|TurnLedger reimbursement math produces `int(0 * 0.8) = 0` for every task. Budget tracking is non-functional.|
```

**Estimated saving on this file**: ~8-12% of the 30,352 table bytes = **~2,400-3,600 bytes (~3.1-4.7% of total)**. This is the largest single lever and falls within §2.3's "3-5% table ceiling" projection when scaled to the whole file.

**Lossy?**: **Lossless**. CommonMark/GFM treats `|a|b|` and `| a | b |` as structurally identical. The separator row requires at least one `-` per column; `|-|-|-|` is valid GFM.

**Risks specific to this file**:
- The Interface Contracts table at lines 968-978 contains bolded text and code spans. Collapse must not eat spacing inside code spans (regex must be fence- and code-span-aware).
- The Gap Analysis table at line 1127 has a very wide Description column with inline commas and escaped pipes — pathological rows can confuse naive regex. Use a fence-aware rule that only collapses padding adjacent to pipes, not inside code spans.
- Human review of the table-heavy sections (Section 5, Section 8) will be harder. Acceptable for LLM consumption per §2.1 "task-equivalent lossless".

### Strategy S2 — Decorative horizontal-rule removal between FR sections

**Primer anchor**: §4.1 Approach 1 item 4 ("Remove decorative horizontal rules not adjacent to YAML front matter"); §2.1 "Remove decorative headers — Lossless".

**Applies because**: The file uses 17 `---` horizontal rules. One (line 1) is the YAML front-matter terminator (KEEP). The other 16 are decorative separators between FR subsections. FR subsections already have `###` headings — the `---` adds zero semantic signal.

**Before** (lines 231-234):
```
**Dependencies**: None. Independent foundation task.

---

### FR-37A.02: Wire TaskResult.output_path (PA-05)
```

**After**:
```
**Dependencies**: None. Independent foundation task.

### FR-37A.02: Wire TaskResult.output_path (PA-05)
```

**Estimated saving**: 16 rules × (4 bytes `---\n` + 1 surrounding blank line = ~6 bytes) = **~96 bytes**. Tiny in absolute terms (~0.1%) but zero-risk and sets up cleaner downstream transforms.

**Lossy?**: **Lossless**. Headings retain all section boundaries.

**Risks**: None material. The YAML front-matter closing `---` at line 19 must be preserved (rule-based regex must skip the first two `---` lines of the file).

### Strategy S3 — Collapse repeated `---\n\n---` blank sandwiches and excess blank runs

**Primer anchor**: §4.1 Approach 1 item 1 ("Collapse 3+ blank lines → 2 blank lines"); §2.3 "Whitespace & formatting ~8-12%".

**Applies because**: The file already uses single blanks between paragraphs (0.3% of bytes). But around each of the 16 removed HRs, collapsing `prose\n\n---\n\n###` → `prose\n\n###` produces modest additional savings already counted in S2. Independent incremental saving here is near-zero for this file.

**Before / after**: N/A, already minimal.

**Estimated saving**: <100 bytes (~0.1%). Included for completeness; the file is already tight on whitespace.

**Lossy?**: Lossless.

**Risks**: Regex must be fence-aware (primer §4.1 risk #1). The spec contains 25 fenced code blocks where blank-line preservation is semantically meaningful in the displayed ASCII diagrams (lines 96-132, 136-187, 815-846) — collapsing blanks inside fences would distort the diagrams. The rule-based transform must skip lines between ```` ``` ```` pairs, per primer §4.1 risks.

### Strategy S4 — Conventions header for abbreviable file/symbol tokens

**Primer anchor**: §2.2 "The conventions header" (40-60 token preamble); §4.1 Approach 1 item 9 ("Replace declared abbreviations from conventions header (if present in front matter)"); §2.3 "Abbreviable phrases ~10-15%".

**Applies because**: The token frequency table in Section 1 shows 10+ symbols repeating ≥10 times each. These are not prose restatement (which is Approach 3 territory) but **literal token substitution** — pure lookup-table replacement, which the primer explicitly authorizes under Approach 1 when the header is declared.

**Proposed conventions header** (added to YAML front-matter region):
```
<!-- cmd-dsl v1:
 [EX]=executor.py [MO]=models.py [MN]=monitor.py [CF]=config.py [PR]=process.py
 [TR]=TaskResult [GM]=gate_rollout_mode [CT]=count_turns_from_output
 [ET]=extract_task_block [EU]=extract_token_usage [TU]=task-unified -->
```

Header cost: ~50 tokens / ~260 bytes.

**Before** (line 33):
```
| `turns_consumed` hardcoded to `0` at `executor.py:1092` ... | `executor.py:1091-1092` | TurnLedger reimbursement math ...
```

**After**:
```
| `turns_consumed` hardcoded to `0` at `[EX]:1092` ... | `[EX]:1091-1092` | TurnLedger reimbursement math ...
```

**Estimated saving on this file** (literal substitution math):

| Token | Orig len | Abbr len | Saved/occ | Count | Bytes saved |
|---|---:|---:|---:|---:|---:|
| `executor.py` → `[EX]` | 11 | 4 | 7 | 45 | 315 |
| `TaskResult` → `[TR]` | 10 | 4 | 6 | 39 | 234 |
| `process.py` → `[PR]` | 10 | 4 | 6 | 28 | 168 |
| `models.py` → `[MO]` | 9 | 4 | 5 | 28 | 140 |
| `count_turns_from_output` → `[CT]` | 23 | 4 | 19 | 25 | 475 |
| `task-unified` → `[TU]` | 12 | 4 | 8 | 25 | 200 |
| `extract_task_block` → `[ET]` | 18 | 4 | 14 | 22 | 308 |
| `gate_rollout_mode` → `[GM]` | 17 | 4 | 13 | 20 | 260 |
| `monitor.py` → `[MN]` | 10 | 4 | 6 | 11 | 66 |
| `config.py` → `[CF]` | 9 | 4 | 5 | 10 | 50 |
| **Gross saving** | | | | | **2,216** |
| Minus header overhead | | | | | −260 |
| **Net saving** | | | | | **~1,956 bytes (~2.5%)** |

**Lossy?**: **Lossless** by primer §2.1 Table row ("Abbreviate via conventions header — Lossless (if header present)"). The conventions header makes every abbreviation mechanically invertible.

**Risks specific to this file — this is where it gets subtle for a SPEC**:

1. **Code fences must be exempt**. Lines like `from superclaude.cli.sprint.monitor import count_turns_from_output` (line 205, 621) and `def extract_task_block(...)` (line 302) are **executable Python inside fenced blocks**. Substituting `[CT]` for `count_turns_from_output` inside a code block would produce non-compiling code that an LLM consumer might then copy-paste or reason about as if it were real. **HARD RULE**: the abbreviation substitution regex must skip fenced code blocks. This aligns with primer §4.2 compression pipeline rule #2 ("Code fences are sacrosanct").
2. **Line-number references are load-bearing**. Strings like `executor.py:1064-1068`, `models.py:329`, `process.py:114` are normative pointers to code locations. `[EX]:1064-1068` preserves this 1:1, but a downstream human reader loses direct `grep`-ability until they decompress. For a spec that will be implemented by engineers, this is a real ergonomic tax — but it is task-equivalent-lossless for the LLM consumer, which is the primer's definition.
3. **Backticks around symbols**. The file uses inline code spans like `` `executor.py` `` ubiquitously. The substitution should happen **inside** the backticks (so `` `[EX]` ``), preserving the visual marker that this is a symbol reference.
4. **Spec-fidelity floor**. The primer §5 spec row caps compression at 10-15% and warns against "AST transforms [that] introduce risk of semantic drift on normative language". Literal string substitution is not AST rewriting — it is the primer's own Approach 1 item 9, and it is by construction reversible given the header. It is within the spec row's envelope **as long as** code fences are exempt.

### Strategy S5 — Heading emoji strip

**Primer anchor**: §4.1 Approach 1 item 5 ("Strip emoji from headings").

**Applies because**: N/A. The file contains **zero emoji**. Strategy is a no-op for this target.

**Estimated saving**: 0 bytes.

### Strategy S6 — Heading underline → ATX normalization

**Primer anchor**: §4.1 Approach 1 item 3.

**Applies because**: N/A. All 51 headings already use ATX syntax.

**Estimated saving**: 0 bytes.

### Strategy S7 — HTML comment removal

**Primer anchor**: §4.1 Approach 1 item 7.

**Applies because**: N/A. The file contains zero HTML comments (we would be **adding** one in S4 for the conventions header, not removing any).

**Estimated saving**: 0 bytes.

### Strategy S8 — Bullet-marker normalization

**Primer anchor**: §4.1 Approach 1 item 10.

**Applies because**: N/A. All lists already use `-`.

**Estimated saving**: 0 bytes.

### Strategy S9 — Trailing-whitespace strip

**Primer anchor**: §4.1 Approach 1 item 2; §2.1 Table row 1.

**Applies because**: N/A. Zero trailing-whitespace lines measured.

**Estimated saving**: 0 bytes.

### Strategy S10 — "Last updated / Version" preamble drop

**Primer anchor**: §4.1 Approach 1 item 8.

**Applies because**: The YAML front-matter already holds `version: "1.0.0"`, `created: 2026-04-05`, `status: draft`. There is **no duplicated version/last-updated block** elsewhere in the body. No-op.

**Estimated saving**: 0 bytes.

### Strategy S11 — AST heading deduplication / table hoisting / cross-ref dedup  *(REJECTED)*

**Primer anchor**: §4.2 Approach 2.

**Why rejected for this file**: Primer §5 spec row is explicit: "**Approach 1 (rule-based) only**" with the rationale "AST transforms introduce risk of semantic drift on normative language". Even though this file has enticing candidates for AST work (the FR-37A sections have a highly regular `Description / Current code / After code / Acceptance Criteria / Verification Contract / Impact Analysis / Commit Boundary / Rollback Plan / Dependencies` schema that an AST pass could template-compress, primer §4.2 item 3), **the primer forbids it for specs**. Also listed in primer §4.3 cross-document rules #5: "Specs should never exceed Approach 1." Not counted in the stack.

**Lossy?**: Primer rates Approach 2 at ★★★★☆ fidelity — very strong but not provable. For a contract-grade spec, that is below the fidelity floor.

### Strategy S12 — LLM-assisted prose rewriting  *(REJECTED)*

**Primer anchor**: §4.3 Approach 3.

**Why rejected for this file**: Same §5 spec row prohibition. Additionally, primer §4.3 risks enumerate "hallucinated facts" and "may smooth over inconsistencies in the source by making up a coherent version" — catastrophic for a spec containing normative MUSTs, line numbers, enum values, and executable code. Primer §4.3 fidelity rating is ★★★☆☆, which is below the spec-fidelity floor. Not counted in the stack.

### Strategy S13 — Drop FR-schema label repetition via a schema-header *(REJECTED as AST; noted for completeness)*

**Primer anchor**: Hypothetical extension of §2.2 conventions-header concept to schema labels (would require §4.2 AST-level work to inject/strip consistently).

**Why rejected**: There are 104 bold-prefix schema labels. Abbreviating `**Acceptance Criteria**:` → `**[AC]**:` via the conventions header would save ~14 × (22-8) = 196 bytes; `**Verification Contract**:` → `**[VC]**:` saves ~12 × (25-8) = 204 bytes; full schema-label abbreviation totals ~1,200-1,500 bytes (~1.6-2.0%). However: (a) for bold labels that sit at paragraph-starts, a human reader scanning the doc depends on the labels for navigation, and (b) primer §2.2 warns the conventions header must amortize over ≥5 reads per INV-3. For a label that appears ~12 times **in one document**, amortization is fine, but the cognitive cost of an opaque `**[AC]**:` in a contract document is material. **Spec-row rationale ("reversible AND auditable") pushes against it**. I flag this as an **optional tier** — if the consumer DAG is purely machine and never human, re-enable; otherwise skip.

---

## Section 3 — Recommended Strategy Stack

Ordered per primer §5 pipeline composition rule #1 ("Always run Approach 1 first") and §5 spec row ("Approach 1 only").

| # | Strategy | Lossless? | Bytes saved | % of 77,176 | Cumulative % |
|---|---|---|---:|---:|---:|
| 1 | **S9** Trailing-whitespace strip | Yes | 0 | 0.0% | 0.0% |
| 2 | **S3** Collapse excess blank runs (fence-aware) | Yes | ~50 | 0.1% | 0.1% |
| 3 | **S6** Heading ATX normalization | Yes | 0 | 0.0% | 0.1% |
| 4 | **S8** Bullet-marker normalization | Yes | 0 | 0.0% | 0.1% |
| 5 | **S2** Decorative `---` HR removal (preserve front-matter closer) | Yes | ~96 | 0.1% | 0.2% |
| 6 | **S5** Heading emoji strip | Yes | 0 | 0.0% | 0.2% |
| 7 | **S7** HTML comment removal | Yes | 0 | 0.0% | 0.2% |
| 8 | **S10** Duplicated version/last-updated drop | Yes | 0 | 0.0% | 0.2% |
| 9 | **S1** Pipe-table padding collapse (fence-aware, code-span-aware) | Yes | ~2,400–3,600 | 3.1–4.7% | 3.3–4.9% |
| 10 | **S4** Conventions-header abbreviation (fence-exempt) | Yes (header-reversible) | ~1,956 (net) | 2.5% | **5.8–7.4%** |

**Projected total compression**: **≈ 5.8-7.4%** on this file.

### Why the projection sits below the primer's 10-15% spec ceiling

The primer §5 spec row projects 10-15%. This file will come in at the **low end or below** because the author (or a prior formatter) has already banked most of Approach 1's free wins:

- Zero trailing whitespace (normally ~1-2%)
- Zero emoji (~0.5-1% on emoji-heavy docs)
- Zero HTML comments (~0.5-1%)
- Single-blank paragraph separators already (~2-4%)
- All-ATX headings already
- All-`-` bullets already

The remaining compressible mass is concentrated in **tables** (S1) and **repeated symbol references** (S4). Those two strategies together project ~5.5-7%, which is the realistic ceiling for this particular file under the spec-row constraint.

### Optional extension if the consumer is purely machine (not authorised by default)

- **S13** (schema-label abbreviation): **+1.6-2.0%**, bringing projected total to **~7.4-9.4%**. This is still **below** the primer's 10-15% spec ceiling and remains lossless via the conventions header, but it sacrifices human auditability on contract language. Enable only if INV-3 consumer DAG analysis shows zero human reads. Default: **off**.

### Respecting the spec-fidelity floor

Every strategy in the recommended stack is either:
1. **Pure whitespace/formatting** (S2, S3, S5-S10) — primer §2.1 rates these as Lossless unconditionally, or
2. **Deterministic textual substitution with a declared reverse mapping** (S1 table-padding, S4 conventions header) — primer §2.1 rates these as Lossless when the header is present, and primer §4.1 item 9 explicitly authorizes them under Approach 1.

No strategy in the stack touches:
- **Code fence content** (sacrosanct per primer §4.2 rule #2 and §4.1 risk #1)
- **Table row semantics** (rows kept intact; only padding collapses)
- **Prose rephrasing** (forbidden by spec row; would be Approach 3)
- **Structural AST transforms** (forbidden by spec row)
- **Normative language** (MUST/SHOULD/MAY clauses and acceptance-criteria checklists are untouched)

The stack is therefore **inside the primer's "near-lossless" spec-fidelity floor** by construction.

---

## Section 4 — Risks & Caveats Specific to This File

### R-1 — ASCII-art diagrams inside fenced code blocks

**Where**: lines 96-132 (Diagram A: Current State Buggy), lines 136-187 (Diagram B: After R1), lines 815-846 (Module Dependency Graph using box-drawing chars ┌─┐│└┘).

**Risk**: A naive regex transform that is not fence-aware will destroy the visual alignment of these diagrams. The dependency-graph uses `─│┌┐└┘` box-drawing characters whose visual positioning depends on exact column counts. Any blank-line collapse, padding strip, or substitution that crosses the fence boundary is **lossy for LLM comprehension** because the spatial relationships encode the data flow.

**Mitigation**: The rule-based transformer **MUST** track fence state (toggle on each `^```` line) and skip all lines where `in_code == True`. This is primer §4.1 risk #1 verbatim, and it is non-negotiable for this file. S1, S3, S4 all need this guard.

### R-2 — Inline Python code spans referencing symbols

**Where**: Every `**Current code**` and `**After code**` subsection under each FR (FR-37A.01 through FR-37A.09), and the Data Models section 4.5.

**Risk**: If S4's substitution regex fires inside a fenced Python block, it will replace `count_turns_from_output` with `[CT]` in code like:
```python
from superclaude.cli.sprint.monitor import count_turns_from_output
```
turning it into a non-runnable `[CT]`. Downstream LLM agents reading the spec might then treat the abbreviation as a real Python identifier or try to complete the import path against it.

**Mitigation**: S4 applies **only outside fenced code blocks**. Inline single-backtick spans (e.g., `` `executor.py:1064` ``) are safe to substitute — they are inline code, not executable Python — but the regex should still preserve the backticks around the abbreviation to keep visual marker.

### R-3 — Line-number contracts are normative

**Where**: Section 1.1 Evidence table, Section 4.2 Modified Files table, every FR subsection with "Current code (`executor.py:1089-1092`)" citations, Section 5 Interface Contracts table.

**Risk**: The spec binds implementation tasks to **specific line numbers** in specific files. `executor.py:1091-1092` is a contract. S4's abbreviation turns this into `[EX]:1091-1092`, which is reversible but adds indirection. A worker agent that reads the compressed spec and tries to `Grep` for `executor.py:1091` before decompressing will find zero matches.

**Mitigation**: Either (a) publish the conventions header prominently at the top of the compressed document so all consumers decompress first, or (b) restrict S4 to non-locator contexts by excluding substitutions where the next character is `:` followed by digits (keeping `executor.py:1091` verbatim while abbreviating bare `executor.py` mentions). Option (b) reduces S4's projected saving by roughly 30-40% (many of the 45 `executor.py` occurrences are followed by line numbers). **Conservative recommendation**: adopt option (b) for this file, dropping S4's net saving to ~1,200-1,400 bytes (~1.5-1.8%) and pushing total projected compression to **~4.8-6.7%**. This is well inside the spec-fidelity floor at the cost of losing roughly one-third of S4's value.

### R-4 — Escaped pipes and inline code spans inside tables

**Where**: Section 1.1 Evidence table (line 33 onwards), Section 5 Interface Contracts table, Section 7 Risk Assessment table, Section 12 Gap Analysis table.

**Risk**: S1's pipe-padding collapse must not collapse whitespace **inside** inline code spans that happen to sit between two `|` characters. Example from line 33: `` `turns_consumed` hardcoded to `0` at `executor.py:1092` `` — a greedy whitespace-strip between pipes could corrupt spacing inside backticks.

**Mitigation**: Use a GFM-aware table transformer (still Approach 1 — the primer §4.1 is defined as "regex/line-based" but explicitly lists table-padding collapse as item 6, so a table-aware tokenizer is within scope). Pseudocode: for each `|`-delimited cell, `strip()` only the outermost leading/trailing whitespace between the pipe and the first non-space character; do not touch whitespace inside backtick spans. Alternatively skip cells containing backticks.

### R-5 — YAML front-matter closing `---` must be preserved

**Where**: Line 19 (`---` closing the YAML block opened on line 1).

**Risk**: S2 removes decorative `---` horizontal rules. A naive implementation will also remove the front-matter closer, corrupting the YAML block and breaking any tool that parses the spec's metadata.

**Mitigation**: S2's regex must skip the first `---\n` that follows a YAML block opener on line 1. Easiest: count `---` occurrences from the top; the first two are front-matter delimiters (keep), all remaining `^---$` lines are decorative (remove). Primer §4.1 item 4 says "not adjacent to YAML front matter" — this is the rule.

### R-6 — Spec is read at implementation time by both humans and worker agents

**Where**: Whole document. Per the primer §2.2 amortization math and INV-3, we need to estimate read count.

**Risk**: This SPEC will be read by: (a) the human engineer implementing FR-37A.01 through FR-37A.34, (b) a `sc:tasklist` generator that emits MDTM task definitions from the spec, (c) worker agents executing each task in isolation. If the human reader is in the loop, the ergonomic cost of abbreviations (R-3, R-4) matters. If only agents read it, S4 and S13 are pure wins.

**Mitigation**: Default stack (S1-S10, no S13) assumes a **mixed** human + agent consumer DAG. This is the safe posture. Revisit S13 and the aggressive S4 variant only once INV-3 instrumentation confirms read counts and consumer identities (primer §6 explicitly carries this invariant forward as UNADDRESSED).

### R-7 — Append-mode documentation inside ASCII diagrams

**Where**: Lines 158-161 inside Diagram B:
```
  Output: phase-1-output.txt opened in "a" mode [MA-03: process.py:114]
    Task 1 NDJSON ... (PRESERVED)
    Task 2 NDJSON ... (PRESERVED)
    Task 3 NDJSON ... (APPENDED)
```

**Risk**: This is not executable code but it **is** inside a fenced block and uses indentation + parentheses to encode state-transition semantics. Any transform that touches it risks altering the meaning. Already covered by R-1's "do not touch fenced content" rule, flagged separately because this diagram is particularly meaning-rich per character.

**Mitigation**: Fence-skip, as per R-1.

### R-8 — Primer invariants still unaddressed

**Where**: Primer §6, applies to every compression in this repo.

**Caveats**:
- **INV-1 (tokenizer generalization)**: the -5.8-7.4% projection uses byte counts, not Claude-native tokens. Actual token savings may drift ±2-8 percentage points per primer §6. A 6% byte reduction is not guaranteed to be a 6% token reduction.
- **INV-3 (consumer DAG unmapped)**: S4's conventions header amortizes over reads. If this spec is read once and discarded (e.g., only consumed at roadmap-generation time), the ~260-byte header cost is dead weight and S4 should be dropped; net saving collapses by ~260 bytes. If read ≥5 times, S4 is the win it projects to be.
- **INV-5 (Haiku untested)**: if any consumer in the DAG is Haiku 4.5, primer §6 says "Haiku paths must default to uncompressed Markdown". None of this analysis applies to Haiku consumers until the Haiku A/B test runs.

These invariants gate **any** production rollout of this compression stack, not just this file.

---

## Summary

| Dimension | Finding |
|---|---|
| Governing primer row | §5 SPEC: Approach 1 only, 10-15% ceiling, near-lossless floor |
| File baseline cleanliness | Already tight: zero trailing ws, zero emoji, zero HTML comments, ATX headings, `-` bullets, single-blank separators |
| Dominant compressible mass | Tables (39.8%) and repeated symbol references (~10 tokens × 10-45 occurrences) |
| Recommended strategies in stack | S2, S3, S5-S10 (free wins, mostly no-ops), **S1** (table padding, ~3-5%), **S4** (conventions header, ~2.5% net, fence-exempt, locator-exempt per R-3) |
| Rejected | S11 (Approach 2 AST), S12 (Approach 3 LLM), S13 (schema-label abbreviation — optional) |
| Projected compression | **~5.8-7.4%** standard stack; **~4.8-6.7%** with the conservative R-3 locator exemption; **~7.4-9.4%** if S13 enabled under machine-only consumer DAG |
| Spec-fidelity floor | Respected. Every strategy is either whitespace/formatting or reversible textual substitution. No AST, no prose rewriting, no fence touching. |
| Blocking invariants | INV-1 (tokenizer drift ±2-8 pp), INV-3 (read-count amortization), INV-5 (Haiku gating) — all inherited from primer §6, all UNADDRESSED |

The headline number (~6%) sits **below** the primer's 10-15% spec ceiling because the document has already been groomed for most of Approach 1's free wins. The remaining compressible mass lives in tables and in the repetition of 10-ish symbol tokens, and neither lever can be pushed further without crossing into Approach 2/3 territory — which the primer §5 spec row explicitly forbids.
