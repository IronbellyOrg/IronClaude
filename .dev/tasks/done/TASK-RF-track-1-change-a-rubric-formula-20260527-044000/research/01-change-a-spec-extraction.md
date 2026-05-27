# Research: Change A Source Spec Extraction

**Topic type:** Source Spec Extraction (paste-ready diff blocks)
**Scope:** CROSS-ENV-PROPOSAL-MERGED.md L43-109 (Change A section) → escalation-rubric.md
**Status:** Complete
**Date:** 2026-05-27

## Purpose

Extract every paste-ready insertion/replacement block from the Change A diff sketch
in the merged cross-env proposal. Each block is classified as REQUIRED-INSERT,
REQUIRED-REPLACE, or OPTIONAL with anchor, verbatim text, and MUST statements.

## Source

- Proposal: `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md`
- Change A spec block: proposal L43-106 (diff sketch fenced block at L51-106)
- Provenance header (proposal L45): `[Provenance: V1 base; cross-tab table merged from V2]`
- Section-affected summary (proposal L47): dimension table at lines 11-17 + formula at line 19; add `### Verdict-direction modifier (M3a)` subsection; add `### Claim-class × evidence-class cross-tab` subsection (V2-merged); add one new rule under `## Escalation decision` § 3.
- Shape summary (proposal L49): `insert (6th dimension row, modifier subsection, cross-tab subsection, escalation rule) + replace (Evidence grounding 1.0 anchor, formula line)`.
- Target file: `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (52 lines, current head)

## Dimension count change

- BEFORE: 5 dimensions (Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence) — target file L11-17.
- AFTER: 6 dimensions (adds `Runtime check` as the 6th row).
- Formula transform: `arithmetic mean of the five dimension scores` → `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)` (gated minimum with +0.30 buffer).

---

## Block 1 — REQUIRED-REPLACE: Evidence-grounding 1.0 anchor cell

**Block type:** REPLACE (cell-level edit inside an existing table row)
**Proposal source:** L56 (`-` line) → L57 (`+` line)
**Target anchor:** existing escalation-rubric.md L13 (the `**Evidence grounding**` row of the dimension table at L11-17).

### Diff (proposal L56-57, markers stripped)

OLD (paste-target text to find):

```
| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
```

NEW (paste-ready replacement):

```
| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom (snippet match verified by calibrator's spot-check) | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
```

### Semantic delta

- The 1.0 (strong) anchor no longer includes the `OR diagnostic command output reproduces the symptom` clause — that pathway now belongs to the new `Runtime check` dimension.
- Adds `(snippet match verified by calibrator's spot-check)` qualifier — narrows Evidence grounding to source-grounding only with calibrator verification.

### MUST statements

- None embedded in this cell itself; calibrator's spot-check obligation is documented elsewhere (Change C — confidence-calibrator.md).

---

## Block 2 — REQUIRED-INSERT: New `Runtime check` 6th dimension table row

**Block type:** INSERT (new table row appended after the 5 existing rows)
**Proposal source:** L62 (`+` line)
**Target anchor:** After the existing `**Domain coherence**` row (target file L17), still inside the dimension table at L11-17 — i.e. inserted as a new L18 that becomes the new 6th data row of the table.
**Surrounding context (proposal L58-61, unchanged lines):**

```
| **Symptom coverage** | ... |
| **Reproducibility fit** | ... |
| **Fix directness** | ... |
| **Domain coherence** | ... |
```

### Paste-ready insertion (proposal L62, marker stripped)

```
| **Runtime check** | Hypothesis includes an executed reproducer with captured stdout/stderr that reproduces the symptom; OR an asserted-by-test runtime invariant (test cited by name AND its execution-state declared) | Hypothesis includes a runnable command but no captured output; OR cites a test that exists but was not exercised at hypothesis time | Hypothesis is source-only — no executed reproducer, no test assertion. For `claim_class: static_defect`, this dimension inherits the Evidence grounding score (static defects' source IS their runtime). For `claim_class: runtime_behavior` or `environment_dependent`, source-only cards mandatorily score 0.0. |
```

### MUST statements embedded in the 0.0 cell

- `For claim_class: static_defect, this dimension inherits the Evidence grounding score (static defects' source IS their runtime).` — conditional inheritance rule.
- `For claim_class: runtime_behavior or environment_dependent, source-only cards mandatorily score 0.0.` — hard rule (the word `mandatorily` is the MUST signal).

### Semantic delta

- Introduces a 6th dimension that explicitly distinguishes source-grounding (Evidence grounding) from execution-grounding (Runtime check).
- Embeds claim-class-aware scoring logic directly in the 0.0 cell text — these rules are formalized in Block 6's cross-tab.

---

## Block 3 — REQUIRED-REPLACE: Formula line (arithmetic mean → gated minimum)

**Block type:** REPLACE (single line)
**Proposal source:** L64 (`-` line) → L65 (`+` line)
**Target anchor:** existing escalation-rubric.md L19 (`**Confidence** = arithmetic mean of the five dimension scores.`).

### Diff (proposal L64-65, markers stripped)

OLD (paste-target text to find):

```
**Confidence** = arithmetic mean of the five dimension scores.
```

NEW (paste-ready replacement):

```
**Confidence** = `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)`.
```

### Semantic delta

- Changes from arithmetic mean to gated minimum.
- The min has THREE arguments: (a) mean of all 6 dims, (b) evidence_grounding + 0.30, (c) runtime_check + 0.30.
- The `+0.30` buffer is the **gate**: a dimension at 0.5 caps composite at 0.80 (below 0.85 STOP gate); a dimension at 0.0 hard-caps composite at 0.30.

### MUST statements

- The formula itself is the MUST: confidence cannot exceed `min(mean, EG+0.30, RC+0.30)`. This is the load-bearing change.

---

## Block 4 — REQUIRED-INSERT: +0.30 buffer prose paragraph

**Block type:** INSERT (new paragraph immediately after the new formula)
**Proposal source:** L66-67 (`+` lines; L66 is the blank-line marker, L67 is the prose)
**Target anchor:** Immediately after the new formula line (post-Block-3 L19), before existing `Round to two decimals.` at target file L21.

### Paste-ready insertion (proposal L66-67, markers stripped)

```

The +0.30 buffer means a 0.5 dimension caps the composite at 0.80, *below* the 0.85 STOP gate. A 0.0 dimension hard-caps the composite at 0.30. The gates apply unconditionally (no claim_class exemption); for `static_defect` claims, Runtime check auto-inherits Evidence grounding so the gate is satisfied whenever the citation is.
```

(Note: leading blank line is part of the insert — separates from the formula line per proposal L66.)

### MUST statements

- `The gates apply unconditionally (no claim_class exemption)` — explicit MUST NOT (no exemption permitted).
- `for static_defect claims, Runtime check auto-inherits Evidence grounding` — restatement of Block 2's inheritance rule, reinforcing it at the formula-explanation layer.

### Semantic delta

- Makes the gate semantics explicit in prose: 0.5 → 0.80 cap; 0.0 → 0.30 cap.
- Confirms the unconditional-application rule (no claim_class can escape the gate; only `static_defect` gets the inheritance shortcut).

---

## Block 5 — REQUIRED-INSERT: `### Verdict-direction modifier (M3a)` subsection

**Block type:** INSERT (new H3 subsection between `## Confidence calibration (Wave 1.7)` and `## Escalation decision (Wave 2)`)
**Proposal source:** L71-80 (`+` lines)
**Target anchor:** After `Round to two decimals.` at target file L21, before `## Escalation decision (Wave 2)` at target file L23. Inserts the M3a subsection at the tail of the calibration section.

### Paste-ready insertion (proposal L71-80, markers stripped)

```
### Verdict-direction modifier (M3a)

After computing the gated-minimum confidence, apply this modifier when the card's frontmatter declares `claim_class: runtime_behavior` AND `runtime_check < 1.0`:

| Verdict direction | Cap on calibrated confidence |
|-------------------|------------------------------|
| REFUTE / REJECT   | 0.70 |
| AFFIRM            | 0.84 |

Rationale: a wrong REFUTE on runtime behavior closes the investigation door (the H3 0.95-REFUTE case); a wrong AFFIRM is caught by CI. Source-only REFUTEs of runtime claims are the precise failure mode under repair and must not clear the 0.85 STOP gate. The 0.84 AFFIRM cap means source-only AFFIRMs of runtime claims still ESCALATE to Tier 2 (below the 0.85 STOP).
```

### Cap table — verbatim values

| Verdict direction | Cap on calibrated confidence |
|-------------------|------------------------------|
| REFUTE / REJECT   | 0.70 |
| AFFIRM            | 0.84 |

### Trigger conditions (proposal L73)

- Applied **after** the gated-minimum formula (Block 3) computes confidence.
- Only when BOTH of these frontmatter conditions hold:
  - `claim_class: runtime_behavior`
  - `runtime_check < 1.0`

### MUST statements

- `must not clear the 0.85 STOP gate` — explicit MUST NOT for source-only REFUTEs of runtime claims.
- The 0.70 REFUTE/REJECT cap and 0.84 AFFIRM cap are hard ceilings (below the 0.85 STOP), guaranteeing ESCALATE.

### Rationale logic captured (proposal L80)

- Wrong REFUTE on runtime behavior = closes the investigation door (cited failure case: H3 0.95-REFUTE).
- Wrong AFFIRM = caught by CI (lower asymmetric cost).
- Cap of 0.84 (not 0.85) on AFFIRM is deliberate: 0.84 < 0.85 ⇒ guaranteed ESCALATE under the low_confidence rule.

---

## Block 6 — REQUIRED-INSERT: `### Claim-class × evidence-class cross-tab [V2 merged]` subsection

**Block type:** INSERT (new H3 subsection, V2-merged provenance)
**Proposal source:** L82-95 (`+` lines)
**Provenance marker:** `[V2 merged]` suffix in the H3 heading itself — the only block in Change A with an explicit inline V2-merge marker (proposal L82). Per provenance header at proposal L45, the full Change A is V1 base + this cross-tab table from V2.
**Target anchor:** Immediately after Block 5's M3a subsection, still before `## Escalation decision (Wave 2)`.

### Paste-ready insertion (proposal L82-95, markers stripped)

```
### Claim-class × evidence-class cross-tab [V2 merged]

The Runtime check dimension score is derived from the (claim_class, evidence_class) pair declared in the card frontmatter:

| claim_class \ evidence_class | runtime_repro | runtime_trace | log_evidence | source_static | doc_static | none |
|------------------------------|---------------|---------------|--------------|---------------|------------|------|
| `runtime_behavior`           | 1.0           | 1.0           | 0.5          | **0.0**       | **0.0**    | **0.0** |
| `environment_dependent`      | 1.0           | 1.0           | 0.5          | **0.0**       | **0.0**    | **0.0** |
| `static_defect`              | 1.0           | 1.0           | 1.0          | inherits EG   | inherits EG | 0.0  |
| `doc_contract`               | 1.0           | 1.0           | 1.0          | 0.5           | 1.0        | 0.0  |
| `config_value`               | 1.0           | 1.0           | 1.0          | inherits EG   | inherits EG | 0.0  |
| `mixed`                      | min of the two component classes' scores                                                          |

The bolded cells (0.0) trigger the verdict-direction modifier when the card's verdict is REFUTE/REJECT.
```

### Cross-tab — full 6 claim_class × 6 evidence_class verbatim

- **Rows (claim_class):** `runtime_behavior`, `environment_dependent`, `static_defect`, `doc_contract`, `config_value`, `mixed`
- **Columns (evidence_class):** `runtime_repro`, `runtime_trace`, `log_evidence`, `source_static`, `doc_static`, `none`
- **Bolded cells (0.0 — modifier triggers):** `runtime_behavior` × {source_static, doc_static, none}; `environment_dependent` × {source_static, doc_static, none} — 6 bolded cells total.
- **Inherits-EG cells:** `static_defect` × {source_static, doc_static}; `config_value` × {source_static, doc_static} — 4 cells.
- **Special row:** `mixed` collapses to a single merged cell: `min of the two component classes' scores`.

### MUST statements

- `The Runtime check dimension score is derived from the (claim_class, evidence_class) pair declared in the card frontmatter` — derivation rule (MUST consult the cross-tab).
- `The bolded cells (0.0) trigger the verdict-direction modifier when the card's verdict is REFUTE/REJECT` — explicit linkage to Block 5 (M3a).

### Semantic delta

- Formalizes the prose rule from Block 2's 0.0 cell into a deterministic lookup table.
- Creates the bridge between Change B's frontmatter (`claim_class`, `evidence_class`) and Block 5's verdict-direction modifier.

---

## Block 7 — REQUIRED-INSERT: New escalation rule under § 3

**Block type:** INSERT (new sub-bullet, appended to the existing § 3 `Signal-driven escalation` list)
**Proposal source:** L105 (`+` line)
**Target anchor:** After the existing `--type security` bullet at target file L39, before `4. **Default**` heading at target file L41.
**Surrounding context (proposal L99-104, unchanged lines):**

```
3. **Signal-driven escalation** (any one triggers escalation)
   - `confidence < 0.85` → ESCALATE (`escalation_reason: low_confidence`).
   - Multi-domain symptom ...
   - Symptom described as intermittent ...
   - Reproducibility dimension scored 0.0 ...
   - `--type security` AND confidence < 0.95 → ESCALATE (`escalation_reason: security_caution`).
```

### Paste-ready insertion (proposal L105, marker stripped)

```
   - `claim_class ∈ {runtime_behavior, environment_dependent}` AND `runtime_check < 0.5` → ESCALATE (`escalation_reason: source_only_dynamic_claim`).
```

### Escalation rule — verbatim

- **Trigger condition:** `claim_class ∈ {runtime_behavior, environment_dependent}` AND `runtime_check < 0.5`
- **Action:** ESCALATE
- **Reason code:** `source_only_dynamic_claim`

### Characters of note

- `∈` is U+2208 (ELEMENT OF) — matches existing project character set per research-notes L22.
- The bullet uses 3-space indent + `- ` to match the existing § 3 sub-bullet style at target file L35-39.

### MUST statements

- Conditional MUST: when both trigger conditions are met, the calibrator MUST emit `escalation_reason: source_only_dynamic_claim` and ESCALATE.
- New `escalation_reason` enum value: `source_only_dynamic_claim` (joins `low_confidence`, `multi_domain`, `intermittent`, `not_reproducible`, `security_caution`).

---

## Summary

### Block count by type

| Block # | Type | Section | Proposal lines |
|---------|------|---------|----------------|
| 1 | REQUIRED-REPLACE | Evidence-grounding 1.0 anchor cell | L56→L57 |
| 2 | REQUIRED-INSERT  | New `Runtime check` 6th dimension row | L62 |
| 3 | REQUIRED-REPLACE | Formula line (gated min) | L64→L65 |
| 4 | REQUIRED-INSERT  | +0.30 buffer prose paragraph | L66-67 |
| 5 | REQUIRED-INSERT  | `### Verdict-direction modifier (M3a)` subsection + cap table | L71-80 |
| 6 | REQUIRED-INSERT  | `### Claim-class × evidence-class cross-tab [V2 merged]` subsection (6×6 table) | L82-95 |
| 7 | REQUIRED-INSERT  | New § 3 escalation sub-bullet (`source_only_dynamic_claim`) | L105 |

**Totals:** 7 blocks; 2 REPLACE + 5 INSERT; 0 OPTIONAL. All 7 are REQUIRED.

### Dimension count change

- 5 → 6 dimensions (Block 2 adds `Runtime check`).
- Formula change: arithmetic mean (5 dims) → gated minimum with +0.30 buffer (6 dims; Block 3).

### Key MUST statements

1. **(Block 2 — 0.0 cell)** `For claim_class: runtime_behavior or environment_dependent, source-only cards mandatorily score 0.0.`
2. **(Block 2 — 0.0 cell)** `For claim_class: static_defect, this dimension inherits the Evidence grounding score.` (inheritance rule)
3. **(Block 4 — buffer prose)** `The gates apply unconditionally (no claim_class exemption).`
4. **(Block 5 — M3a rationale)** Source-only REFUTEs of runtime claims `must not clear the 0.85 STOP gate`.
5. **(Block 5 — cap table)** REFUTE/REJECT capped at 0.70; AFFIRM capped at 0.84 (both below 0.85 STOP).
6. **(Block 6 — cross-tab)** Runtime check score `is derived from the (claim_class, evidence_class) pair declared in the card frontmatter` — deterministic lookup.
7. **(Block 7 — § 3 rule)** `claim_class ∈ {runtime_behavior, environment_dependent}` AND `runtime_check < 0.5` → ESCALATE (`escalation_reason: source_only_dynamic_claim`).

### V2-merge provenance notes

- **Top-of-section provenance (proposal L45):** `[Provenance: V1 base; cross-tab table merged from V2]` — declares the entire Change A is V1 base, with Block 6 contributed by V2.
- **Inline marker (proposal L82):** Block 6's H3 heading literally contains `[V2 merged]` suffix: `### Claim-class × evidence-class cross-tab [V2 merged]`. This suffix is part of the paste-ready text — preserve verbatim.
- **No other blocks carry inline V2 markers.** Blocks 1-5 and Block 7 are V1-origin.
- **Top-of-document context (proposal L1-5):** the merged proposal converged at 1.00 cross-environment agreement; V1 won the debate at 0.876 vs V2's 0.845 and is the structural base; V2 contributions were the evidence_class taxonomy (which Block 6 operationalizes), the audit gate (Change 4 — outside Change A scope), WebFetch URL detection (outside Change A scope), and real-card replay fixtures (Change 5 — outside Change A scope).

### Cross-referenced changes (for downstream tracks)

- **Change B (hypothesis-card-template.md):** introduces the `claim_class` + `evidence_class` + `verdict_direction` frontmatter fields that Blocks 2, 5, 6, 7 depend on. PR #89 already shipped Change B.
- **Change C (confidence-calibrator.md):** must apply the new formula (Block 3), the +0.30 gate (Block 4), the M3a modifier (Block 5), the cross-tab derivation (Block 6), and the new escalation rule (Block 7). Change C consumes everything Change A produces.

### Edit order recommendation (for executor)

1. Block 1 (REPLACE EG cell) — narrowest, anchor at L13.
2. Block 2 (INSERT Runtime check row) — after L17 Domain coherence row.
3. Block 3 (REPLACE formula line) — at L19.
4. Block 4 (INSERT buffer prose) — after the new formula.
5. Block 5 (INSERT M3a subsection) — after `Round to two decimals.` at L21.
6. Block 6 (INSERT cross-tab subsection) — after Block 5.
7. Block 7 (INSERT § 3 escalation rule) — after L39 security_caution bullet, before L41 `4. **Default**` heading.

This order preserves anchor uniqueness — earlier edits do not invalidate later anchor strings.
