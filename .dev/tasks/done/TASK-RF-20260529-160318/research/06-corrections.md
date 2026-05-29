# Research: Corrections (Gap-Fill Round 1)

**Topic type:** Corrections
**Scope:** Pin the 3 line-range fixes that rf-qa research-gate identified in qa-research-gate-report.md (1 IMPORTANT + 2 MINOR)
**Status:** Complete
**Date:** 2026-05-29
**Source-of-truth:** Independently re-verified by the orchestrator at gap-fill time

---

## Authoritative coordinate corrections

These three rows override any contradicting coordinate in `research/01-file-inventory.md`, `research/03-integration-points.md`, or `research/05-doc-cross-validator.md`. The rf-task-builder MUST use these values:

### Correction 1 (IMPORTANT) — Wave 1.5 closing `---` separator line and Wave 1.6 insertion point

- **Coordinate**: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- **Wave 1.5 section ends at line 186** (last prose line of the Token budget paragraph).
- **Line 187 is blank.**
- **Line 188 is the `---` horizontal-rule separator** closing Wave 1.5.
- **Line 189 is blank.**
- **Line 190 is `### Wave 1.7: Tier 1 — Hypothesis Formation` (the next wave header).**
- **Insertion point for new Wave 1.6**: insert a blank line + new content starting at the position currently occupied by line 189 (i.e., after line 188's `---`, before line 190's `### Wave 1.7`). The new content should begin with `### Wave 1.6: Diagnosability Audit`, NOT with another `---` (the existing `---` at line 188 already closes Wave 1.5; Wave 1.6's own closing `---` follows its content).
- **Verification**: `awk 'NR>=185 && NR<=192' SKILL.md` (or `Read offset 185 limit 8`) shows the blank-line/HR/blank/header sequence at 186-190.
- **Supersedes**: R5 §1 row 4 + R5 §3.1 (which said `---` at 187); R1 line 55 was correct.

### Correction 2 (MINOR) — `## Documentation Context` line in report-template.md

- **Coordinate**: `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
- **`## Documentation Context` is at line 31** (not line 32 as R1 §File 7 stated).
- **The section runs from line 31 to line 41.**
- **`## Diagnosis` follows at line 43.**
- **Insertion point for new `## Diagnosability Context` section**: between line 41 (end of Documentation Context) and line 43 (start of Diagnosis) — i.e., the new section text replaces line 42 (which is blank) and pushes Diagnosis down. The new section heading is `## Diagnosability Context`.
- **Verification**: `grep -nE '^## ' src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` returns the canonical line numbers.
- **Supersedes**: R1 §File 7's "32-41" range.

### Correction 3 (MINOR) — Output Contract field count

- **Coordinate**: `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Output Contract table (lines 41-57).
- **The Output Contract table currently has 15 fields**, not 13 as merged-output.md §5 prose claims.
- **Builder instruction**: when generating the per-edit checklist item for the Output Contract addition, cite the insertion point as "append after the existing 15-field table (last row ends at line 57)", NOT "append after the 13th row" (which would be inside the existing table mid-stream).
- **The 4 new fields go after the existing 15** — the table grows from 15 to 19 rows.
- **Verification**: Count rows between the header divider line and the closing newline at SKILL.md:42-57.
- **Supersedes**: any "13-field" framing inherited from merged-output.md §5 prose.

---

## Non-correction items also flagged for builder awareness

These are NOT line-range fixes but were surfaced by rf-qa for the builder's situational awareness:

### A1 — Two NEW sections added since brainstorm landed

R5 §3.2 flagged that two material sections were added to SKILL.md after the brainstorm wrote merged-output.md:

1. **Wave 3 "Tier 2 calibration completeness gate"** (lines 263-277, 15 lines) — internal to Wave 3; no ripple-effect on Wave 1.6.
2. **Wave 5 evidence-validator block** (lines 343-344, expanded inline) — internal to Wave 5; no ripple-effect on Wave 1.6.

**Builder action**: NONE — both sections are downstream of the Wave 1.6 insertion point and do not need modification. Flag preserved for future-self awareness in the Task Log.

### A2 — Builder-critical flag-parsing hook not in spec §10

R3 surfaced (not in the original spec §10 table) that Wave 0's flag-parsing list at SKILL.md:97 must gain the `--no-diagnosability-audit` flag mention (plus optionally `--diagnosability-handoff` and `--reset-diagnosability-rounds` per merged-output.md §7).

**Builder action**: Add this as a 12th checklist item alongside the 11 spec §10 change-points, OR fold into the Wave 0 row of the existing diff-sketch table.

---

## Summary

Three coordinate corrections are pinned above. All claims in R1/R3/R5 are otherwise sound (re-verified via spot-checks during gap-fill). The corrections are mechanical — they do not alter the design, scope, or phase structure. The builder MUST consume this file ALONGSIDE R1-R5 and prefer Corrections 1-3 above any contradicting coordinate in the earlier files.

**Status: Complete.** No further research needed for this gap-fill round.
