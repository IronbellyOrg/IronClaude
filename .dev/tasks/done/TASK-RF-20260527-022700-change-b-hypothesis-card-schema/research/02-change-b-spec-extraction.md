# Research: Change B Source Spec Extraction
**Topic type:** Source Spec Extraction
**Scope:** CROSS-ENV-PROPOSAL-MERGED.md L110-186
**Status:** Complete
**Date:** 2026-05-27
**Source file:** `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md`
**Target file (from proposal):** `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`

---

## 1. Change B header (verbatim, proposal L110-117)

```
## Change B — `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`

[Provenance: V1 base; `evidence_class` frontmatter field merged from V2 Change 1]

**Sections affected**: frontmatter block (lines 12-16), per-dimension self-assessment (lines 48-53), and append two new required sections after `## If I'm wrong, it's probably because…`.

**Shape**: insert (frontmatter fields, dimension row, Falsification section, Evidence-classification section, Runtime check section) — additive only; no replacement of existing required fields.
```

Note: the "Sections affected" line cites legacy line numbers (12-16, 48-53) in the proposal's reference; R1 (file inventory) has the current byte-level state of the target file.

---

## 2. Insertion Block 1 — Frontmatter additions (REQUIRED)

**Source:** proposal L122-137 (lines stripped of leading `+`).
**Insertion point:** after `**Cause class**` line, before `**Consistency with docs**` line.
**Status:** REQUIRED (additive frontmatter)

### Paste-ready block (use exactly as below)

```
**Claim class**: `static_defect` | `runtime_behavior` | `environment_dependent` | `config_value` | `doc_contract` | `mixed`
  — `static_defect`: source-reading alone is sufficient evidence (typos, missing imports, regex literals, syntax errors)
  — `runtime_behavior`: claim depends on dynamic control flow, side effects, executed semantics, or library call dispatch
  — `environment_dependent`: claim depends on OS / runtime / feature-flag / network / data state
  — `config_value`: claim depends on configuration / settings / env vars
  — `doc_contract`: claim depends on a documented contract (RFC, spec, README)
  — `mixed`: spans more than one class
**Evidence class**: `runtime_repro` | `runtime_trace` | `log_evidence` | `source_static` | `doc_static` | `none`
  — `runtime_repro`: executed reproducer with captured stdout/stderr
  — `runtime_trace`: live execution trace, debugger output, instrumentation log
  — `log_evidence`: post-hoc log excerpt from the failing run
  — `source_static`: source file Read + cited line (no execution)
  — `doc_static`: documentation citation (no execution, no source)
  — `none`: prose only / no evidence
**Verdict direction**: `AFFIRM` | `REFUTE` | `REJECT`
  — REFUTE/REJECT verdicts on `runtime_behavior` claims face a higher calibration bar (see escalation-rubric § Verdict-direction modifier).
```

### Enum value enumeration (per-field count)

- **`Claim class`** — **6 values** (NOT 7 as the later "Evidence classification" section's prose `<one of the seven above>` suggests):
  1. `static_defect`
  2. `runtime_behavior`
  3. `environment_dependent`
  4. `config_value`
  5. `doc_contract`
  6. `mixed`

  **DISCREPANCY RESOLUTION:** The proposal's L162 says `<one of the seven above>` but only 6 enum values are declared. This is a defect in the source proposal (off-by-one in prose). The builder MUST paste the L162 text **verbatim** as `<one of the seven above>` (instructions are to paste character-for-character), and the task file should flag this as a "known prose defect to carry forward" in Risks. Optionally, the task may include a follow-up note recommending the proposal author correct this to `<one of the six above>`, but the V1.5 commit ships verbatim.

- **`Evidence class`** — **6 values**:
  1. `runtime_repro`
  2. `runtime_trace`
  3. `log_evidence`
  4. `source_static`
  5. `doc_static`
  6. `none`

- **`Verdict direction`** — **3 values**:
  1. `AFFIRM`
  2. `REFUTE`
  3. `REJECT`

---

## 3. Insertion Block 2 — Per-dimension dimension row (REQUIRED)

**Source:** proposal L146 (stripped of leading `+`).
**Insertion point:** after `- Evidence grounding: <0.0|0.5|1.0> — <one-line reason>` line, before `- Symptom coverage: <0.0|0.5|1.0> — <one-line reason>` line.
**Status:** REQUIRED (additive dimension row)

### Paste-ready block

```
- Runtime check: <0.0|0.5|1.0> — <derived from (claim_class, evidence_class) cross-tab; cite the executed-reproducer command + captured output, OR cite a runtime-asserting test by name + its execution state. For claim_class=static_defect, mark "inherits Evidence grounding" with no further evidence required.>
```

---

## 4. Insertion Block 3 — `## Falsification standard` section (REQUIRED)

**Source:** proposal L156-158 (stripped of leading `+`).
**Insertion point:** after the body of `## If I'm wrong, it's probably because…`, before `## Alternatives considered`.
**Status:** REQUIRED (new section)

### Paste-ready block

```
## Falsification standard

One sentence. What concrete evidence — an executable command and expected output, a named test outcome, a log assertion, or a measurable observation — would prove this hypothesis WRONG? "Re-reading the source differently" is NOT a falsification standard. If you cannot name a falsification standard, the claim_class is `runtime_behavior` and Runtime check self-scores ≤ 0.5.
```

Em-dashes (`—`), curly characters, and inline backticks must be preserved verbatim.

---

## 5. Insertion Block 4 — `## Evidence classification [V2 merged]` section (REQUIRED)

**Source:** proposal L160-167 (stripped of leading `+`).
**Insertion point:** immediately after Insertion Block 3 (`## Falsification standard`).
**Status:** REQUIRED (new section)

### Paste-ready block

```
## Evidence classification [V2 merged]

- **Claim class**: <one of the seven above> — <one-line reason>
- **Evidence class**: <one of the six above> — <one-line reason>
- **Runtime check performed?**: yes | no — <if no, one-line reason why not>
- **If REFUTE verdict, coverage statement**: <which paths/files/conditions were inspected; explicitly name anything not inspected that could flip the verdict>

Filling rule: an empty or "Not applicable" value on `evidence_class` is a defect; cards with `claim_class: runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` MUST self-cap their confidence at 0.65 in the per-dimension self-assessment and state the cap in the rationale.
```

### Explicit cap value

**Filling rule cap = 0.65** — confidence MUST be self-capped at **0.65** for cards where `claim_class: runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}`. The cap value is **0.65** (not 0.70, not 0.80).

### Carry-forward prose defect note

Line `<one of the seven above>` carries the same "7 vs 6" off-by-one as flagged in §2. Paste verbatim per instructions; surface as Risk.

---

## 6. Insertion Block 5 — `## Recommended evidence shape (v2.0 preview)` section (OPTIONAL in v1.5, RECOMMENDED for inclusion)

**Source:** proposal L173-185 (stripped of leading `+`).
**Insertion point:** immediately after Insertion Block 4 (`## Evidence classification [V2 merged]`).
**Status:** OPTIONAL per the proposal's "New optional section" header (L170), but **the proposal labels this as "the recommended shape" and the task SHOULD include it in this commit** — it is opt-in for card authors in v1.5 and mandatory in v2.0.

### Paste-ready block

```
## Recommended evidence shape (v2.0 preview)

For new cards, the recommended evidence shape is a typed table that makes each item's evidence kind explicit:

| # | Kind | Source | Content |
|---|------|--------|---------|
| E1 | `source_citation` | `path/to/file.py:142` | (verified snippet) |
| E2 | `executed_reproducer` | `uv run python -c "..."` | (captured stdout/stderr) |
| E3 | `test_assertion` | `tests/.../test_x::test_y` | (execution state: fails / passes / not-run) |

Kinds: `source_citation`, `executed_reproducer`, `test_assertion`, `documentation`, `log_artifact`.

This shape is **OPTIONAL in v1.5** — the existing bulleted-list evidence shape remains valid. The typed table will become **MANDATORY in v2.0** (target: follow-up commit after pin-test corpus in `calibrator-eval-cases.md` confirms v1.5 stability).
```

---

## 7. Definitive insertion ordering (final state of new sections)

Per the proposal's L114 ("append two new required sections after `## If I'm wrong, it's probably because…`") plus L170's optional section, the in-file order INSIDE the template block must be:

1. existing `## If I'm wrong, it's probably because…` (untouched)
2. **NEW** `## Falsification standard` (Insertion Block 3 — REQUIRED)
3. **NEW** `## Evidence classification [V2 merged]` (Insertion Block 4 — REQUIRED)
4. **NEW** `## Recommended evidence shape (v2.0 preview)` (Insertion Block 5 — OPTIONAL but RECOMMENDED)
5. existing `## Alternatives considered` (untouched)
6. existing `## Grounding gaps` (untouched)

Frontmatter ordering (Insertion Block 1) is fixed by the diff sketch: insert the three new fields **as a contiguous group** after `**Cause class**`, before `**Consistency with docs**`. Per-dimension row (Insertion Block 2) inserts between `Evidence grounding` and `Symptom coverage` in the dimension list.

---

## 8. Migration / backward-compat constraints (from proposal L555-565)

The card template itself does NOT enforce migration — that responsibility belongs to Change C (the confidence-calibrator agent). However, the template MUST NOT make the new fields read as retroactively mandatory on legacy cards. Relevant rows verbatim from L555-565:

```
| In-flight cards without `Claim class` frontmatter | Calibrator defaults to `runtime_behavior` (fail-safe). Recorded in Notes. |
| In-flight cards without `Evidence class` frontmatter [V2 merged] | Calibrator defaults to `none`. Recorded in Notes. |
| In-flight cards without `Verdict direction` | Calibrator defaults to `AFFIRM`. Recorded in Notes. |
| In-flight cards without `Runtime check` self-assessment | Calibrator derives from (claim_class, evidence_class) cross-tab. No fallback to old mean. |
| Old calibration reports (e.g., `tier2-root-cause-analyst-calibration.md`) | Schema additions are additive; new rows don't break downstream parsers. |
| pr86 / T4's already-shipped calibration results | Optionally re-run with v1.5 rubric (yields lower scores for source-only runtime claims — intentional). Otherwise annotate old reports with `[calibrated under pre-M1+M2+M3a rubric]`. |
| The optional typed evidence table in Change B | Card authors may opt in or stay on the bulleted-list form in v1.5. v2.0 will require it. |
```

Per Fixture 5 (L323-324):

```
v1.0 frontmatter with no `Claim class`, `Evidence class`, or `Verdict direction` fields.
**Expected behavior**: calibrator defaults claim_class to `runtime_behavior`, evidence_class to `none`, verdict_direction to `AFFIRM` (fail-safe), records in Notes, proceeds.
```

**Template-level implication:** The new frontmatter fields MUST be presented as additive — no introductory prose in the template should say "all cards MUST have these fields" or similar. The enum descriptions are presented as field-level definitions; the existing template's overall framing (presumably "fill in these fields") is preserved without modification.

---

## 9. Cross-change dependency notes (for "Risks / known limitations" section of the task file)

Per proposal L416-421 (Minimal-change subset) and L491 (Implementation order):

- **Change B alone is incomplete.** The proposal states: *"Change B alone exposes claim_class + evidence_class + Runtime check field but the rubric still averages it into the old mean; verdict-direction modifier still absent."* (L421)
- **Required composition:** Changes A (rubric formula + cross-tab + verdict-direction modifier) and C (calibrator applies the new rule and reads the new fields) are **compositional, not exchangeable** with B. Shipping B without A+C means the rubric cannot leverage the new fields.
- **Implementation order (per L488-495):** Rubric (A) → card template (B) → calibrator (C) → audit gate (F) → eval corpus (E). This task implements **only step 2** (Change B).
- **Cause→Fix matrix (L408):** Change B's specific contribution to M2 (source-vs-runtime conflation) is: *"claim_class + evidence_class + Runtime check self-assessment + Falsification standard"*. It contributes the **schema slots**; A contributes the **formula**; C contributes the **scoring**.

**Risk to capture in task file:** Shipping Change B in isolation produces a template with fields no consumer reads. This is expected and intentional for the sequenced rollout, but the task's acceptance criteria should NOT include "calibrator scores cards using new fields" (that is Change C). Acceptance is limited to "the template includes the new fields, dimension row, and sections in the specified order, additively."

---

## 10. Proposal-cited gotchas — MUST / MUST NOT statements (verbatim)

These statements appear inside the paste-ready blocks above and MUST land in the target file verbatim. Listed here so the builder can verify each one is captured:

- **From Insertion Block 4 (Filling rule):**
  > "an empty or 'Not applicable' value on `evidence_class` is a defect"

- **From Insertion Block 4 (Filling rule):**
  > "cards with `claim_class: runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` MUST self-cap their confidence at 0.65 in the per-dimension self-assessment and state the cap in the rationale"

- **From Insertion Block 3 (Falsification standard body):**
  > "If you cannot name a falsification standard, the claim_class is `runtime_behavior` and Runtime check self-scores ≤ 0.5"

- **From Insertion Block 1 (Verdict direction sub-bullet):**
  > "REFUTE/REJECT verdicts on `runtime_behavior` claims face a higher calibration bar (see escalation-rubric § Verdict-direction modifier)."

  Note: this sub-bullet creates a **cross-reference** to the escalation-rubric file's "Verdict-direction modifier" subsection (Change A territory). The reference is forward-looking — if Change A has not yet landed, the reference is dangling. Per the sequenced ordering (A then B), this is acceptable; the task file should note it as an "expected dangling reference until Change A lands."

- **From Insertion Block 2 (Runtime check dimension):**
  > "For claim_class=static_defect, mark 'inherits Evidence grounding' with no further evidence required."

- **From Insertion Block 5 (v1.5/v2.0 prose):**
  > "This shape is **OPTIONAL in v1.5** … The typed table will become **MANDATORY in v2.0**"

---

## Provenance line (proposal L573)

```
- §Change B — V1 §"Change B"; `evidence_class` frontmatter + Evidence-classification section merged from V2 §"Change 1"
```

Confirms: `Claim class` + `Verdict direction` + the per-dimension row + Falsification standard + Recommended-evidence-shape preview come from V1; `Evidence class` enum + `## Evidence classification [V2 merged]` section come from V2. The `[V2 merged]` suffix on the section heading is a deliberate provenance marker that MUST be preserved verbatim.

---

## Summary

- **5 insertion blocks** extracted verbatim from CROSS-ENV-PROPOSAL-MERGED.md L110-186, each as a paste-ready block stripped of leading `+` markers with backticks, em-dashes, vertical bars, and bold markers preserved.
- **4 REQUIRED, 1 OPTIONAL-but-RECOMMENDED**: Frontmatter (REQ), Runtime check dimension row (REQ), `## Falsification standard` (REQ), `## Evidence classification [V2 merged]` (REQ), `## Recommended evidence shape (v2.0 preview)` (OPTIONAL — proposal recommends inclusion).
- **One off-by-one prose defect** in the source proposal (`<one of the seven above>` vs 6 declared enum values) — flagged for verbatim paste-through and Risk-section disclosure; not a blocker since the proposal explicitly says "paste character-for-character."
- **Cap value = 0.65** for runtime_behavior + static-evidence cards (Filling rule).
- **Change B is the second of a 4-change sequence (A→B→C→F)**; isolated shipment is intentional but leaves fields with no downstream consumer until Change A lands the rubric and Change C lands the calibrator updates.
