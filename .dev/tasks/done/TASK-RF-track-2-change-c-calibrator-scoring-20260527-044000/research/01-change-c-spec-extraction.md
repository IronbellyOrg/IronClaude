# Research 01 — Change C Source Spec Extraction

**Researcher:** spec-extraction (Track 2 of 4)
**Date:** 2026-05-27
**Source:** `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` (main checkout)
**Lines covered:** L190-255 (Change C block)
**Target file:** `src/superclaude/agents/confidence-calibrator.md` (118 lines)
**Status:** In Progress

---

## Overview

Change C contains FOUR diff sketches against `src/superclaude/agents/confidence-calibrator.md`:

| # | Diff sketch | Proposal lines | Block types | Anchor section |
|---|-------------|----------------|-------------|----------------|
| 1 | Responsibilities | L196-213 | 3 REPLACE + 3 INSERT | `## Responsibilities` (target L48-54) |
| 2 | New `## Claim-class handling` subsection | L215-223 | 1 INSERT (whole section) | Between `## Independence Instruction` (L23-27) and `## Inputs` (L39-45) |
| 3 | Output Format additions | L225-244 | 1 INSERT (table row) + 1 INSERT (Stage-2 trace subsection) | Per-dimension table (target ~L70) + before `## Confidence` subsection (target L76) |
| 4 | Confidence section additions | L246-251 | 1 REPLACE + 1 INSERT | `## Confidence` (target L76-80) |

**Sections affected** (per proposal L194 verbatim):
> "`## Independence Instruction` (lines 23-27); `## Responsibilities` (lines 48-54); `## Output Format` (lines 58-93). Insert new subsection `## Claim-class handling` between Independence Instruction and Inputs."

**Cross-references to Change A (HARD prerequisite — must land first):**
- §5 of Responsibilities references "the rubric's gated-minimum formula" — only exists post-Change A.
- §4 of Responsibilities references "the cross-tab table in the rubric" for Runtime check — only exists post-Change A.
- §5a references the "rubric's M3a table" / verdict-direction modifier — only exists post-Change A.
- §6 extends `escalation_reason` allowed-values with `source_only_dynamic_claim` — only valid post-Change A.

---

## Diff Sketch 1 — Responsibilities (proposal L196-213)

**Block type:** Mixed (3 REPLACE + 3 INSERT) against existing `## Responsibilities` section at target L47-54.
**Anchor (top):** the literal heading `## Responsibilities` followed by blank line.
**Net effect:** existing 6-item numbered list becomes a 9-item list (items 1, 4, 5 REPLACED; new 2a, 3a, 5a INSERTED).

### Sub-block 1.A — REPLACE item #1 (proposal L201-202)

**Block type:** REQUIRED-REPLACE (single numbered list item)

**Old (verbatim, stripped of `-` marker):**
```
1. **Read the rubric** at `rubric_path`. Note the 5 dimensions: Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
```

**New (verbatim, stripped of `+` marker):**
```
1. **Read the rubric** at `rubric_path`. Note the 6 dimensions: Evidence grounding, Runtime check, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
```

**Diff semantics:** "5 dimensions" → "6 dimensions"; insert "Runtime check," as 2nd dimension in the listed order.

### Sub-block 1.B — INSERT new item #2a (proposal L204)

**Block type:** REQUIRED-INSERT (new numbered list item after existing #2)

**Anchor (preceding line, unchanged in diff):** ` 2. **Read the card** at `card_path`.`

**New (verbatim, stripped of `+` marker):**
```
2a. **Resolve `claim_class`, `evidence_class`, and `verdict_direction` from frontmatter.** If `claim_class` is absent, default to `runtime_behavior` (fail-safe). If `evidence_class` is absent, default to `none`. If `verdict_direction` is absent, default to `AFFIRM`. Record all defaults in Notes (preserves backward-compat with v1.0 cards; v2.0 will require explicit declaration).
```

**MUST defaults captured (fail-safe migration semantics):**
- `claim_class` absent → `runtime_behavior` (fail-safe — assumes harder claim class)
- `evidence_class` absent → `none`
- `verdict_direction` absent → `AFFIRM`
- All defaults MUST be recorded in Notes (audit trail for backward-compat)

### Sub-block 1.C — INSERT new item #3a (proposal L206)

**Block type:** REQUIRED-INSERT (new numbered list item after existing #3 spot-check rule)

**Anchor (preceding line, unchanged in diff):** existing item #3 ending "…let that drive the Evidence grounding score."

**New (verbatim, stripped of `+` marker):**
```
3a. **WebFetch URL detection** [V2 merged]: For any evidence citation that is a remote URL (e.g., `https?://(raw\.)?github(?:usercontent)?\.com/...`), mark `spot_check_unverifiable: <url>` in Notes per citation. Do NOT cap on this alone; surface the unverifiability so the user can act on it. This forces unverifiable cites into the calibration report rather than silently treating them as verified.
```

**MUST statements:**
- For any remote-URL evidence citation, MUST mark `spot_check_unverifiable: <url>` in Notes
- MUST NOT cap score on URL-unverifiability alone (surfacing-only, not penalizing)
- Provenance: "[V2 merged]" — this clause is the V2 hard-fail rule 4 merged into the V1 base

### Sub-block 1.D — REPLACE item #4 (proposal L207, L209)

**Block type:** REQUIRED-REPLACE (single numbered list item, substantially rewritten)

**Old (verbatim, stripped of `-` marker):**
```
4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score.
```

**New (verbatim, stripped of `+` marker):**
```
4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. For **Runtime check**: use the cross-tab table in the rubric to derive the score from (claim_class, evidence_class). 0.5 requires a runnable command in the card without captured output (overrides cross-tab when evidence_class=source_static + a command is present). For `claim_class: static_defect`, Runtime check inherits the Evidence grounding score.
```

**MUST statements:**
- Runtime check scoring MUST consult the rubric's (claim_class, evidence_class) cross-tab (Change A dependency)
- The 0.5 score requires "a runnable command in the card without captured output"
- The 0.5 override condition: when `evidence_class=source_static` AND a runnable command is present, 0.5 overrides the cross-tab
- For `claim_class: static_defect`, Runtime check MUST inherit the Evidence grounding score (static-defect inheritance rule)

### Sub-block 1.E — REPLACE item #5 (proposal L208, L210)

**Block type:** REQUIRED-REPLACE (replaces "arithmetic mean" with gated-min formula + introduces Stage-2 trace requirement)

**Old (verbatim, stripped of `-` marker):**
```
5. **Compute the arithmetic mean**, rounded to 2 decimals.
```

**New (verbatim, stripped of `+` marker):**
```
5. **Compute calibrated confidence** using the rubric's gated-minimum formula: `min(arithmetic_mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)`. Round to 2 decimals. Emit a **Stage-2 trace** in your report (see Output Format) showing each gate's value so the formula application is auditable.
```

**MUST statements:**
- Calibrated confidence MUST use the gated-minimum formula `min(arithmetic_mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)`
- Round to 2 decimals
- MUST emit a Stage-2 trace showing each gate's value (auditable formula application)
- Formula references "all_six" dimensions — depends on Change A introducing the 6th dimension

### Sub-block 1.F — INSERT new item #5a (proposal L211)

**Block type:** REQUIRED-INSERT (new numbered list item after the new #5)

**Anchor (preceding line — the NEW item #5 from sub-block 1.E above)**

**New (verbatim, stripped of `+` marker):**
```
5a. **Apply the verdict-direction modifier** per the rubric: when `claim_class: runtime_behavior` and `runtime_check < 1.0`, cap calibrated at 0.70 (REFUTE/REJECT) or 0.84 (AFFIRM). Record whether the cap was binding in the Stage-2 trace.
```

**MUST statements:**
- Verdict-direction cap applies WHEN `claim_class: runtime_behavior` AND `runtime_check < 1.0`
- Cap value: 0.70 if `verdict_direction` is REFUTE/REJECT; 0.84 if `verdict_direction` is AFFIRM
- MUST record whether the cap was binding in the Stage-2 trace
- References "the rubric" — depends on Change A's M3a table

### Sub-block 1.G — REPLACE item #6 (proposal L212, implicit replace)

**Block type:** REQUIRED-REPLACE (existing item #6 is extended with a trailing sentence about the new allowed-value)

**Old (verbatim, target file L54):**
```
6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`.
```

**New (verbatim, stripped of context marker — proposal L212 has NO `+`/`-` so this is presented as unchanged context but is in fact extended):**
```
6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`. Note: the allowed-value set for `escalation_reason` is extended with `source_only_dynamic_claim`.
```

**Interpretation note (anchor unambiguity):** the proposal L212 line begins with a space (unified-diff "context" line), indicating the entire line REPLACES the existing #6. The trailing sentence "Note: the allowed-value set for `escalation_reason` is extended with `source_only_dynamic_claim`." is the new content; everything before it matches L54 verbatim. Classifying as REPLACE for clarity (a strict reading of the diff hunk would call this "context modified in place," which the executor MUST treat as REPLACE).

**MUST statement:**
- `escalation_reason` allowed-value set MUST be extended with `source_only_dynamic_claim` (Change A dependency)

---

## Diff Sketch 2 — New `## Claim-class handling` subsection (proposal L215-223)

**Block type:** REQUIRED-INSERT (entire new subsection inserted as a whole)

**Insertion anchor (per proposal L215):** "insert after Independence Instruction" — target file L23-27 ends the Independence Instruction block; the new subsection lands BEFORE the `## Safety Constraint` heading at L29 (which currently follows Independence Instruction).

**Important anchor clarification:** the proposal L194 says "Insert new subsection `## Claim-class handling` between Independence Instruction and Inputs." But the current target file order is: Independence Instruction (L23-27) → Safety Constraint (L29-31) → Behavioral Mindset (L33-37) → Inputs (L39-45). The proposal L215 says "insert after Independence Instruction" without specifying "before Safety Constraint" vs "before Inputs". The executor MUST resolve this ambiguity (likely insertion immediately after Independence Instruction's closing paragraph, i.e., between L27 and L29).

**New (full verbatim subsection, stripped of `+` markers — proposal L218-222):**
```
## Claim-class handling

The card declares `claim_class` and `evidence_class` in frontmatter. You read them but you do not redetermine them from scratch (that invites anchoring on whether you *can* verify the claim with Read alone). Trust the card's declaration with ONE exception: if `claim_class: static_defect` is declared but the card's claim references dynamic control flow ("falls through to", "the runtime would", "after the side effect", "dispatched via", "the helper actually returns"), flag the misdeclaration in Notes and score the card AS IF `claim_class: runtime_behavior`. Surface the discrepancy explicitly so the orchestrator can act on it.

Why this matters: the failure mode under repair (Cause #2) is calibrators scoring runtime-behavior claims at 0.85+ on source-only evidence because the rubric's Evidence-grounding OR-clause permitted it. The `claim_class` + `evidence_class` fields + the Runtime check dimension cross-tab make the structural inadequacy of source-only evidence visible at the dimension level rather than hidden inside Evidence grounding's old OR-clause. Your job is to enforce the visibility, not to relitigate the claim_class declaration.
```

**MUST statements:**
- "Trust the card's declaration with ONE exception" — the rule is trust-the-card by default
- The ONE exception: if `claim_class: static_defect` is declared BUT the claim references dynamic control flow, MUST flag misdeclaration in Notes AND score AS IF `claim_class: runtime_behavior`
- The dynamic-control-flow trigger phrases (verbatim list, used as heuristic): "falls through to", "the runtime would", "after the side effect", "dispatched via", "the helper actually returns"
- MUST surface the discrepancy explicitly for the orchestrator

**MUST NOT statements:**
- MUST NOT redetermine `claim_class`/`evidence_class` from scratch (anchoring risk)
- MUST NOT relitigate the claim_class declaration (your job is to enforce visibility, not redetermine)

---

## Diff Sketch 3 — Output Format additions (proposal L225-244)

**Block type:** Mixed (1 INSERT into table + 1 INSERT of new subsection)

### Sub-block 3.A — INSERT "Runtime check" row in per-dimension table (proposal L228-232)

**Block type:** REQUIRED-INSERT (single table row, inserted between existing "Evidence grounding" and "Symptom coverage" rows)

**Diff context (verbatim, stripped of leading space markers):**
```
| Dimension | Score | Justification (cite card content) |
|-----------|-------|-----------------------------------|
| Evidence grounding | 1.0 / 0.5 / 0.0 | <one-line citing what in the card supports this> |
```

**Inserted row (verbatim, stripped of `+` marker — proposal L231):**
```
| Runtime check | 1.0 / 0.5 / 0.0 | <derived from (claim_class, evidence_class) cross-tab; cite the executed-reproducer block or named test, or its absence; for claim_class=static_defect, note "inherits Evidence grounding"> |
```

**Trailing context (unchanged, proposal L232):**
```
| Symptom coverage | ... |
```

**Anchor (target file):** the per-dimension table at L68-74. The "Runtime check" row inserts between line 70 (Evidence grounding row) and line 71 (Symptom coverage row).

### Sub-block 3.B — INSERT new `## Stage-2 trace (REQUIRED)` subsection (proposal L234-244)

**Block type:** REQUIRED-INSERT (entire new subsection)

**Insertion anchor:** AFTER the per-dimension table (which ends at target L74 with the "Domain coherence" row) and BEFORE the existing `## Confidence` subsection (target L76).

**Critical context (per research-notes GAP):** This new subsection lands INSIDE the fenced code block (the ```markdown ... ``` Output Format template at target L58-93). The new subsection is part of the report template, not a separate doc section.

**New (full verbatim subsection, stripped of `+` markers — proposal L234-244):**
```
## Stage-2 trace (REQUIRED)

| Step | Value | Notes |
|------|-------|-------|
| arithmetic_mean(all_six) | <X.XX> | raw mean |
| gate_M1: evidence_grounding + 0.30 | <X.XX> | always applies |
| gate_M2: runtime_check + 0.30 | <X.XX> | always applies |
| gated_min | <X.XX> | min of the three above |
| verdict_cap | <none | 0.70 | 0.84> | M3a; binding only if claim_class=runtime_behavior AND runtime_check<1.0 |
| **calibrated** | <X.XX> | final |
| spot_check_unverifiable | <list of URLs> | V2-merged WebFetch detection |
```

**MUST statements:**
- The subsection heading is literally `## Stage-2 trace (REQUIRED)` — the "(REQUIRED)" suffix is part of the heading
- Table MUST have exactly these 7 rows in this order:
  1. `arithmetic_mean(all_six)` — raw mean
  2. `gate_M1: evidence_grounding + 0.30` — always applies
  3. `gate_M2: runtime_check + 0.30` — always applies
  4. `gated_min` — min of the three above
  5. `verdict_cap` — M3a; binding only if `claim_class=runtime_behavior` AND `runtime_check<1.0`
  6. `**calibrated**` (bolded) — final
  7. `spot_check_unverifiable` — V2-merged WebFetch detection (list of URLs)
- The `verdict_cap` cell uses the syntax `<none | 0.70 | 0.84>` to indicate the three possible cap values
- The `calibrated` row label MUST be bolded with `**...**` markdown emphasis

---

## Diff Sketch 4 — Confidence section additions (proposal L246-251)

**Block type:** Mixed (1 REPLACE + 1 INSERT)

### Sub-block 4.A — REPLACE Self-reported bullet (proposal L247-248)

**Block type:** REQUIRED-REPLACE (single bullet, extended with explanatory clause)

**Old (verbatim, stripped of `-` marker — target file L78):**
```
- **Self-reported (in card)**: <X.XX>
```

**New (verbatim, stripped of `+` marker):**
```
- **Self-reported (in card)**: <X.XX> — read but NOT used as input to your score (independence instruction)
```

**MUST statement (emphasis):**
- The bullet MUST now include the clause "— read but NOT used as input to your score (independence instruction)" — this is the visible enforcement of the existing Independence Instruction at target file L23-25 ("Self-reported confidence on the card is a signal, not a number") and L25 ("never inherit the card's self-reported confidence" from the Role paragraph)

### Sub-block 4.B — INSERT Formula applied bullet (proposal L250)

**Block type:** REQUIRED-INSERT (new bullet between "Calibrated" and "Delta")

**Anchor (preceding line, unchanged):** `- **Calibrated (this report)**: <Y.YY>`
**Anchor (following line, unchanged):** `- **Delta**: <signed difference, and a one-line read on why it differs>`

**New (verbatim, stripped of `+` marker):**
```
- **Formula applied**: `min(mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)` then verdict-direction cap if applicable
```

**MUST statement:**
- The bullet MUST surface the literal formula `min(mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)` (matches §5 Responsibilities) PLUS the trailing clause "then verdict-direction cap if applicable" (matches §5a Responsibilities)

---

## Consolidated MUST / MUST-NOT inventory

### Defaults (fail-safe migration)
- `claim_class` absent → default `runtime_behavior` (fail-safe — harder class)
- `evidence_class` absent → default `none`
- `verdict_direction` absent → default `AFFIRM`
- All defaults MUST be recorded in Notes

### Trust rules
- Trust the card's `claim_class` declaration BY DEFAULT
- ONE exception: `claim_class: static_defect` + dynamic-control-flow phrasing → flag misdeclaration and score AS IF `runtime_behavior`
- MUST NOT redetermine `claim_class` / `evidence_class` from scratch (anchoring risk)

### Scoring rules
- 6 dimensions (was 5) — Evidence grounding, Runtime check, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence
- Runtime check derives from (claim_class, evidence_class) cross-tab (Change A dependency)
- Runtime check = 0.5 requires runnable command without captured output (overrides cross-tab when `evidence_class=source_static` + command present)
- For `claim_class: static_defect`, Runtime check inherits Evidence grounding score
- Calibrated confidence = `min(arithmetic_mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)`, rounded 2dp
- Apply verdict-direction cap when `claim_class: runtime_behavior` AND `runtime_check < 1.0`:
  - REFUTE/REJECT → cap at 0.70
  - AFFIRM → cap at 0.84

### Independence enforcement
- "Self-reported confidence on the card is a signal, not a number" (PRE-EXISTING at target L25 — context for the new "read but NOT used" clause)
- "Self-reported confidence is NEVER passed through" (PRE-EXISTING — emphasized via the new bullet text "read but NOT used as input to your score")

### Surface rules
- MUST emit Stage-2 trace with all 7 rows (audit trail for formula application)
- MUST mark `spot_check_unverifiable: <url>` in Notes for any remote-URL evidence citation
- MUST NOT cap score on URL-unverifiability alone (surface, don't penalize)
- MUST extend `escalation_reason` allowed-values with `source_only_dynamic_claim` (Change A dependency)

---

## Cross-references to other Changes (HARD dependencies)

Change C cannot ship before Change A — multiple Responsibilities reference Change-A constructs that do not yet exist:

| Responsibility | References Change A construct |
|----------------|-------------------------------|
| §1 — "6 dimensions" | Change A adds Runtime check as the 6th dimension to `refs/escalation-rubric.md` |
| §4 — "use the cross-tab table in the rubric" | Change A introduces the (claim_class, evidence_class) cross-tab in the rubric |
| §5 — "rubric's gated-minimum formula" | Change A defines `min(mean, evidence_grounding+0.30, runtime_check+0.30)` in the rubric |
| §5a — "Apply the verdict-direction modifier per the rubric" | Change A introduces the M3a verdict-direction modifier table |
| §6 — "`source_only_dynamic_claim`" | Change A extends the rubric's `escalation_reason` enum |

Change C also DEPENDS on hypothesis-card-template (`refs/hypothesis-card-template.md`) declaring `claim_class`, `evidence_class`, `verdict_direction` in frontmatter — that exists post PR #89 (per research-notes EXISTING_FILES line 15) so this dependency is already satisfied as of 2026-05-27.

---

## Block-type classification summary

| Diff sketch | Sub-block | Block type | Approximate target lines |
|-------------|-----------|-----------|--------------------------|
| 1 — Responsibilities | 1.A | REQUIRED-REPLACE | L49 |
| 1 — Responsibilities | 1.B | REQUIRED-INSERT (between L50 and L51) | after L50 |
| 1 — Responsibilities | 1.C | REQUIRED-INSERT (between L51 and L52) | after L51 |
| 1 — Responsibilities | 1.D | REQUIRED-REPLACE | L52 |
| 1 — Responsibilities | 1.E | REQUIRED-REPLACE | L53 |
| 1 — Responsibilities | 1.F | REQUIRED-INSERT (between new #5 and existing #6) | after new L53 |
| 1 — Responsibilities | 1.G | REQUIRED-REPLACE (extension) | L54 |
| 2 — Claim-class handling | (whole) | REQUIRED-INSERT (new subsection) | between L27 and L29 |
| 3 — Output Format | 3.A | REQUIRED-INSERT (table row) | between L70 and L71 |
| 3 — Output Format | 3.B | REQUIRED-INSERT (new subsection inside fenced template) | between L74 and L76 |
| 4 — Confidence | 4.A | REQUIRED-REPLACE | L78 |
| 4 — Confidence | 4.B | REQUIRED-INSERT (new bullet) | between L79 and L80 |

**Total operations:** 5 REPLACE + 7 INSERT = 12 distinct edits. Target file grows from 118 lines to approximately 140-150 lines (six new Responsibilities-section items + 6-line new subsection + 1 table row + 9-line Stage-2 trace + 1 extended bullet + 1 new bullet, minus the 4 lines being replaced).

---

## Status: Complete

**Summary:** Captured all four Change-C diff sketches verbatim from proposal L190-255 with block-type classification (5 REPLACE + 7 INSERT = 12 total edits), full MUST/MUST-NOT inventory (fail-safe defaults, trust rules, scoring formulas, verdict-direction caps, Stage-2 trace audit requirements, URL-unverifiability surfacing), and explicit Change-A cross-reference table (5 hard dependencies). Stage-2 trace's exact 7-row table and the new `## Claim-class handling` subsection are reproduced verbatim. One anchor ambiguity flagged for the executor: the "insert after Independence Instruction" position for the new subsection — most likely between target L27 and L29 (before Safety Constraint), but proposal L194 says "between Independence Instruction and Inputs" which is broader; executor should resolve by placing immediately after Independence Instruction's closing paragraph.
