# Research: Target File State — escalation-rubric.md

**Status:** Complete
**Date:** 2026-05-27
**Track:** 1 of 4 — Change A (rubric formula update)
**Researcher:** target-file-state

---

## Section 1 — File Metadata

- **Absolute path (source of truth):** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`
- **Mirror path (sync-dev output, do NOT edit):** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`
- **Line count:** 52 (verified via `wc -l`)
- **Source-of-truth status:** `src/superclaude/skills/...` is canonical; `.claude/skills/...` is a sync mirror produced by `make sync-dev`. Confirmed by `diff src/ .claude/` returning identical content (mirror size 3703 bytes).
- **File purpose:** Defines the 5-dimension scoring rubric and 4-rule escalation decision table used by `sc-troubleshoot-protocol`'s Wave 1.7 (calibration) and Wave 2 (escalation gate); consumed by the `confidence-calibrator` agent via `rubric_path`.

---

## Section 2 — Structural Map (Line Ranges)

| Lines | Section | Content |
|-------|---------|---------|
| L1 | H1 title | `# Escalation Rubric` |
| L2 | blank | — |
| L3 | preamble | "Used in Wave 1.7 ... and in Wave 2 ..." |
| L4 | blank | — |
| L5 | H2 | `## Confidence calibration (Wave 1.7)` |
| L6 | blank | — |
| L7 | prose | "The `root-cause-analyst` returns ... **re-grades** ... not trusted directly." |
| L8 | blank | — |
| L9 | prose | "Score each dimension 0.0–1.0 and average." (U+2013 en-dash) |
| L10 | blank | — |
| L11 | table header | `\| Dimension \| 1.0 (strong) \| 0.5 (partial) \| 0.0 (weak) \|` |
| L12 | table separator | pipe row |
| L13 | table row 1 | **Evidence grounding** — REPLACE TARGET (anchor a) |
| L14 | table row 2 | **Symptom coverage** |
| L15 | table row 3 | **Reproducibility fit** |
| L16 | table row 4 | **Fix directness** |
| L17 | table row 5 | **Domain coherence** — INSERT site for new **Runtime check** row (anchor b) |
| L18 | blank | — |
| L19 | formula | `**Confidence** = arithmetic mean of the five dimension scores.` — REPLACE TARGET (anchor c) |
| L20 | blank | — |
| L21 | rounding | `Round to two decimals.` — pre-anchor for INSERT (anchors d, e) |
| L22 | blank | — |
| L23 | H2 | `## Escalation decision (Wave 2)` — post-anchor for INSERT (anchors e, f) |
| L24 | blank | — |
| L25 | prose | "After confidence is calibrated, apply these rules **in order**..." |
| L26 | blank | — |
| L27 | rule 1 header | `1. **Hard stops**` |
| L28-29 | rule 1 bullets | `--no-escalate`, `--depth quick` |
| L30 | blank | — |
| L31 | rule 2 header | `2. **Forced escalation**` |
| L32 | rule 2 bullet | `--depth deep` |
| L33 | blank | — |
| L34 | rule 3 header | `3. **Signal-driven escalation** (any one triggers escalation)` |
| L35-38 | rule 3 bullets | low_confidence, multi_domain, intermittent, not_reproducible |
| L39 | rule 3 bullet | `--type security` → security_caution — pre-anchor for INSERT (anchor g) |
| L40 | blank | — |
| L41 | rule 4 header | `4. **Default**` — post-anchor for INSERT (anchor g) |
| L42 | rule 4 bullet | `confidence ≥ 0.85` AND single-domain AND reproducible → STOP |
| L43 | blank | — |
| L44 | H2 | `## Why 0.85?` |
| L45-48 | prose | rationale paragraphs |
| L49 | blank | — |
| L50 | H2 | `## What escalation does NOT mean` |
| L51 | blank | — |
| L52 | prose | trailing paragraph (file ends with newline) |

Section spans: Confidence-calibration = L5–L21. Escalation-decision = L23–L42. Trailing rationale = L44–L52.

---

## Section 3 — Anchor Verbatim Capture

All `old_string` slices below are byte-for-byte exact copies from the current file. Each slice was selected for unique-match property (no second occurrence in the 52-line file). Verified by visual scan; the table rows differ by dimension name (in `**bold**`) so any single row is unique; the formula line "**Confidence** = arithmetic mean" is the only `**Confidence**` line in the file; the `--type security` bullet text is unique.

### (a) Evidence-grounding 1.0-cell — REPLACE

**Current L13 (verbatim, single line):**

```
| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
```

**Unique-match `old_string` candidate (the whole line — `**Evidence grounding**` appears only once):**

```
| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
```

Replacement: per Track 1 / spec-extraction researcher (anchor 1 cell text changes from "Cited `file:line` matches a real code path..." to the proposal's tightened "Cited `file:line` reflects current source after re-verification ..." wording — see research/01-change-a-spec-extraction.md for the exact replacement text).

---

### (b) Runtime check row — INSERT (between L17 Domain coherence and L19 formula)

The "Runtime check" row is a NEW 6th dimension. Per proposal it is appended AFTER the existing 5 rows. Best unique anchor is the L17 Domain-coherence row, with insertion AFTER it. The Edit tool's `old_string`/`new_string` approach: take the L17 row + the blank L18 + the L19 formula as `old_string`, then expand `new_string` to insert the new row between L17 and L18.

**Two-line+ `old_string` candidate (Domain coherence row → blank → formula line):**

```
| **Domain coherence** | Single domain (e.g. pure logic bug, pure config issue) | Touches two related domains (e.g. logic + tests) | Spans unrelated domains (e.g. perf + auth) |

**Confidence** = arithmetic mean of the five dimension scores.
```

`new_string` shape: prepend the new Runtime-check row line BEFORE the trailing blank/formula, then proceed to (c) which replaces the formula line. Cleanest: combine (b) and (c) into a single Edit call (see Section 5).

**Note on uniqueness:** `**Domain coherence**` appears only once; `**Confidence**` appears only once. This slice is unambiguous.

---

### (c) Formula line — REPLACE

**Current L19 (verbatim, single line):**

```
**Confidence** = arithmetic mean of the five dimension scores.
```

**Unique-match `old_string` candidate (the literal line — globally unique in the file):**

```
**Confidence** = arithmetic mean of the five dimension scores.
```

Replacement per proposal: the new clamped-min formula `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)` (exact paste-ready text in research/01-change-a-spec-extraction.md).

---

### (d) `+0.30` buffer prose — INSERT (between formula line L19 and rounding line L21)

The proposal inserts an explanatory paragraph that explains the +0.30 caps. Anchor straddles the formula line (L19) and the rounding line (L21) with the blank L20 between.

**`old_string` candidate (formula line → blank → rounding line):**

```
**Confidence** = arithmetic mean of the five dimension scores.

Round to two decimals.
```

`new_string` shape: replaces the formula with the new formula (anchor c), keeps the blank, inserts the buffer prose paragraph + blank, then preserves `Round to two decimals.` Cleanest: combine (c) and (d) into a single Edit call.

**Uniqueness:** `Round to two decimals.` appears only once globally; combined with the unique `**Confidence**` line above, this 3-line slice is unambiguous.

---

### (e) `### Verdict-direction modifier (M3a)` subsection — INSERT (between L21 rounding line and L23 escalation H2)

The proposal adds a new H3 subsection inside Confidence-calibration. Anchor straddles the rounding line and the H2 boundary, with the blank L22.

**`old_string` candidate (rounding line → blank → next H2):**

```
Round to two decimals.

## Escalation decision (Wave 2)
```

`new_string` shape: keeps `Round to two decimals.`, keeps the blank, inserts the entire `### Verdict-direction modifier (M3a)` subsection content + blank, then preserves `## Escalation decision (Wave 2)`.

**Uniqueness:** `Round to two decimals.` and `## Escalation decision (Wave 2)` are each globally unique; the 3-line slice is unambiguous.

---

### (f) `### Claim-class × evidence-class cross-tab` subsection — INSERT (after the M3a subsection inserted in (e))

**ORDERING CONSTRAINT — COMPOSITE ANCHOR:** This anchor does NOT exist in the original file. It only exists AFTER edit (e) lands. The `old_string` for the (f) Edit call MUST include the closing lines of the M3a subsection (whatever they are per spec-extraction) PLUS the still-following `## Escalation decision (Wave 2)` heading.

**`old_string` shape (post-(e), schematic):**

```
<last line(s) of M3a subsection from (e)>

## Escalation decision (Wave 2)
```

The exact `<last line(s) of M3a subsection>` text must be sourced from the spec-extraction researcher's verbatim capture of the M3a block (research/01-change-a-spec-extraction.md). The cross-tab subsection content is then inserted between those last-of-M3a lines and the `## Escalation decision (Wave 2)` heading.

**Alternative (cleaner):** combine (e) and (f) into a single Edit call whose `new_string` contains BOTH the M3a subsection AND the cross-tab subsection (in proposal order), against the same simple `old_string` from (e). This eliminates the composite-anchor risk entirely. **Recommended.**

---

### (g) New escalation sub-bullet — INSERT (between L39 security_caution bullet and L41 `4. **Default**` heading)

**Current L39 + L40 + L41 (verbatim):**

```
   - `--type security` AND confidence < 0.95 → ESCALATE (`escalation_reason: security_caution`). Security bugs have asymmetric cost-of-being-wrong; raise the bar.

4. **Default**
```

**Unique-match `old_string` candidate (3-line slice, globally unique because `security_caution` and `4. **Default**` each appear only once):**

```
   - `--type security` AND confidence < 0.95 → ESCALATE (`escalation_reason: security_caution`). Security bugs have asymmetric cost-of-being-wrong; raise the bar.

4. **Default**
```

`new_string` shape: preserves the `--type security` bullet, inserts the new `source_only_dynamic_claim` bullet on the next list line (3-space indented `   - ` per existing pattern), preserves the blank, preserves `4. **Default**`.

**Indentation note:** existing rule-3 bullets use 3-space indent + `- ` + backticks. New bullet must match.

---

## Section 4 — Character-Encoding Notes

Verified via `od -c` on the source file:

| Char | Codepoint | UTF-8 bytes | Where used in current file |
|------|-----------|-------------|----------------------------|
| `—` em-dash | U+2014 | `342 200 224` | L5 area metadata + L46 "0.5 or lower — meaning ..." |
| `–` en-dash | U+2013 | `342 200 223` | L9 "0.0–1.0" |
| `→` right-arrow | U+2192 | `342 206 222` | All bullets in L28-29, L32, L35-39, all escalation rules |
| `≥` greater-or-equal | U+2265 | `342 211 245` | L42 `confidence ≥ 0.85` |

**Not present in current file (but required by proposal additions):**

- `≤` U+2264 (less-or-equal) — likely used in M3a verdict-direction modifier table (REFUTE/REJECT → cap at ≤ 0.70).
- `∈` U+2208 (element-of) — possibly used in claim-class × evidence-class cross-tab.
- `⟹` U+27F9 (long right double arrow) — possibly used in cross-tab implications.

Encoding for new content MUST be UTF-8 (file's existing encoding). Edits via Edit tool preserve bytes; ensure pasted spec text uses the same codepoints (not ASCII substitutes like `<=`, `=>`).

---

## Section 5 — Recommended Edit Ordering

The seven anchors collapse into **four** Edit-tool calls when overlapping slices are merged (recommended sequence — minimizes uniqueness risk and the composite-anchor dependency of (f) on (e)):

1. **Edit call 1 (anchor a):** REPLACE the Evidence-grounding row (L13) only. Standalone; uses the full L13 line as `old_string`.
2. **Edit call 2 (anchors b + c + d MERGED):** REPLACE the 4-line slice `Domain coherence row → blank → **Confidence** formula line → blank → Round to two decimals.` `old_string` is 5 lines including the two blanks. `new_string` inserts the Runtime-check row after Domain-coherence, replaces the formula, inserts the +0.30 buffer prose paragraph, preserves `Round to two decimals.`. Merging eliminates re-matching against an already-modified region.
3. **Edit call 3 (anchors e + f MERGED — recommended over composite):** INSERT both the `### Verdict-direction modifier (M3a)` subsection AND the `### Claim-class × evidence-class cross-tab` subsection in a single Edit. `old_string` is the 3-line slice `Round to two decimals. → blank → ## Escalation decision (Wave 2)`. `new_string` keeps the rounding line, keeps the blank, inserts BOTH new H3 subsections in proposal order with blanks between, preserves the H2.
4. **Edit call 4 (anchor g):** INSERT the new `source_only_dynamic_claim` rule-3 bullet between the `--type security` bullet and `4. **Default**`. Standalone; uses the 3-line slice as `old_string`.

**Ordering rationale:**
- Call 2 must precede call 4? No — they touch disjoint regions (L13-21 vs L39-41). Either order works.
- Call 3 must NOT be split into separate (e) and (f) calls; if it is, (f) requires a composite anchor that depends on the exact closing text of the M3a block — fragile.
- Call 1 is independent and can run first or last.

**Safer order:** 1 → 2 → 3 → 4 (top-to-bottom file order). This way, if any earlier edit accidentally drifts a later anchor (it should not — slices are disjoint — but defence in depth), the failure surfaces on the next call rather than mid-file.

**Post-edit:** run `make sync-dev`, then `make verify-sync`, then `pre-commit run markdownlint --files src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`. If markdownlint `--fix` mutates the file, re-run `make sync-dev`.

---

**Status:** Complete

## Summary

The target file `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` is 52 lines, currently in src/.claude sync (mirror diff = empty). Change A's seven anchor points were captured with verbatim unique-match `old_string` slices: (a) Evidence-grounding row L13 REPLACE, (b) Runtime-check row INSERT after L17, (c) formula L19 REPLACE, (d) +0.30 buffer prose INSERT between L19 and L21, (e) Verdict-direction modifier subsection INSERT between L21 and L23, (f) Claim-class × evidence-class cross-tab INSERT after (e), (g) new escalation sub-bullet INSERT between L39 and L41. Recommended sequence collapses to four Edit calls (1 standalone, 2 merging b+c+d, 3 merging e+f to eliminate composite-anchor risk, 4 standalone). All current non-ASCII bytes verified: U+2014 em-dash, U+2013 en-dash, U+2192 right-arrow, U+2265 ≥. New content will introduce U+2264 ≤ (and possibly U+2208 ∈ / U+27F9 ⟹) — ensure UTF-8 preservation. No `≤`, `∈`, `⟹` exist in the current file; no character-collision risk.
