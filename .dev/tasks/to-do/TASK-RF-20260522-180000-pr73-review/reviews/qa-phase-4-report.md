# QA Report — Phase 4: Wave 1 / Wave 1.7 Split

**Topic:** PR #73 sc-troubleshoot-protocol Wave 1 → Wave 1 + Wave 1.7 structural restructure
**Date:** 2026-05-22
**Phase:** synthesis-gate (Issue 3 fix verification)
**Fix cycle:** 1
**File under review:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`

---

## Overall Verdict: PASS

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Wave Structure code-block lists 4 lines (1, 1.5, 1.7, 2) with Wave 1.7 between 1.5 and 2 | PASS | `grep -cE "^Wave (1|1\.5|1\.7|2):"` returns 4. Block at lines 75-85: Wave 1.7 line is line 79, between Wave 1.5 (line 78) and Wave 2 (line 80). Wave 1.7 text reads `Wave 1.7: Tier 1 — Hypothesis Formation ← always; consumes Wave 1.5 Documentation Context Card; produces single hypothesis card + calibration` |
| 2 | Wave 1 line renamed to "Wave 1: Tier 1 — Real-Code Grounding" with grounding+reproduce annotation | PASS | Line 77: `Wave 1: Tier 1 — Real-Code Grounding  ← always; loads refs/triage-checklist.md on demand (grounding + reproduce only)` |
| 3 | Wave 1 section header reads `### Wave 1: Tier 1 — Real-Code Grounding` | PASS | Line 129 |
| 4 | Wave 1 body contains ONLY step 1 (real-code grounding) and step 2 (reproduce/observe); steps 3 and 4 removed | PASS | Read lines 129-148. Numbered steps are exactly two: (1) "Ground the symptom in real code" (lines 137-140), (2) "Reproduce or observe" (lines 141-144). No step 3 or 4 present. |
| 5 | Wave 1 exit criteria emits grounding-handoff string only | PASS | Line 146: `Emit "Wave 1 complete: grounding done; handing off to Wave 1.5"` |
| 6 | Wave 1 token-budget reflects only grounding+reproduce, references Wave 1.7 for hypothesis budget | PASS | Line 148: `Token budget for Wave 1: target ≤ ~3k Claude tokens (MCP retrieval offloads the bulk of the work). Hypothesis formation's separate token budget is in Wave 1.7.` |
| 7 | NEW `### Wave 1.7: Tier 1 — Hypothesis Formation` section inserted between Wave 1.5 closing `---` and Wave 2 header | PASS | Line 190 = Wave 1.7 header. Line 188 = closing `---` of Wave 1.5. Line 210 = Wave 2 header. Section structure intact. |
| 8 | Wave 1.7 has Goal stating "one calibrated Tier 1 hypothesis card, consuming the Wave 1.5 Documentation Context Card" | PASS | Line 192 |
| 9 | Wave 1.7 Preconditions reference Wave 1 grounding done + Wave 1.5 card or `--no-doc-discovery` → null | PASS | Line 194 |
| 10 | Wave 1.7 Step 1 spawns root-cause-analyst with `consistency_with_docs` enum requirement preserved verbatim | PASS | Line 198: includes `consistency_with_docs` to one of `aligned \| conflicts \| not_applicable \| no_docs_found` enum verbatim. References Wave 1 step 1 / step 2 outputs correctly. |
| 11 | Wave 1.7 Step 2 spawns confidence-calibrator with inline-fallback bullet | PASS | Lines 199-200: confidence-calibrator spawn with rubric_path, card_tier=1, flags_context, output_path. Fallback bullet at line 200: "if `confidence-calibrator` fails ... fall back to inline orchestrator calibration ... mark `calibration: inline-fallback` in the audit log" |
| 12 | Wave 1.7 exit criteria emits "Wave 1.7 complete: confidence=<x>" | PASS | Line 202 |
| 13 | Wave 1.7 has Failure handling line | PASS | Line 204: failure handling for root-cause-analyst subprocess crash with hypothesis_source: inline-fallback |
| 14 | Wave 1.7 token budget ≤ ~3k | PASS | Line 206: `target ≤ ~3k Claude tokens` |
| 15 | Wave 1.5 Preconditions updated to "Wave 1 (real-code grounding) is complete" | PASS | Line 156: `Wave 1 (real-code grounding) is complete` (no longer says "Wave 1 step 1") |
| 16 | Refs loader table row for `refs/hypothesis-card-template.md` reads "Wave 1.7 and Wave 3" | PASS | Line 452: `\| `refs/hypothesis-card-template.md` \| Wave 1.7 and Wave 3 (passed to agents) \|` |
| 17 | No orphan "Wave 1 complete: confidence=" strings remain | PASS | `grep -c "Wave 1 complete: confidence="` returns 0 |
| 18 | Wave 2 header preserved byte-identical | PASS | Line 210: `### Wave 2: Confidence Gate` — unchanged |
| 19 | Other Refs loader rows for `refs/triage-checklist.md`, `refs/doc-discovery.md` byte-identical | PASS | Lines 450-451 unchanged. (Note: see Observations below re: secondary Wave 1 references in unchanged rows — these are out-of-scope for Issue 3.) |
| 20 | Wave Structure code block syntax valid (no missing arrows, proper alignment) | PASS | Manual read of lines 75-85 confirms clean code-block structure with consistent `←` arrow formatting on all 4 annotated waves |
| 21 | No content loss: old Wave 1 steps 1-4 all preserved somewhere | PASS | Old step 1 → new Wave 1 step 1 (line 137). Old step 2 → new Wave 1 step 2 (line 141). Old step 3 → new Wave 1.7 step 1 (line 198), including the `consistency_with_docs` enum. Old step 4 → new Wave 1.7 step 2 (line 199-200) including inline-fallback bullet. |
| 22 | Output Contract table (lines 41-57) unmodified | PASS | Read lines 41-57; all rows present including `test_is_wrong`, `behavior_is_documented`, `doc_context_card_path`. Format unchanged. |

## Summary

- Checks passed: 22 / 22
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none needed)

## Confidence

**Verified:** 22/22 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence: 100.0%**
**Tool engagement:** Read: 2 | Grep: 2 (multi-pattern grep calls) | Glob: 0 | Bash: 3

## Issues Found

None — all acceptance criteria met.

## Observations (Out-of-Scope for Issue 3 / Phase 4)

These are NOT failures of this phase but should be flagged for downstream consideration:

1. **Refs loader table `refs/escalation-rubric.md` row** (line 449) still reads "Wave 2 (confidence gate) and Wave 1 (calibration)". Calibration moved to Wave 1.7. The AC explicitly required ONLY the `hypothesis-card-template.md` row to change, and the adversarial check required other rows to be "byte-identical" — so this is correctly unchanged per AC. But the second clause now points at a wave that no longer hosts calibration. Recommend a follow-up to update to "Wave 2 (confidence gate) and Wave 1.7 (calibration)".

2. **Refs loader table `refs/triage-checklist.md` row** (line 450) still reads "Wave 1 (passed to root-cause-analyst as part of the brief)". root-cause-analyst spawn moved to Wave 1.7. Same situation: byte-identical preservation was required per adversarial check, but the annotation is now technically inaccurate. Recommend follow-up.

3. The Wave Structure code block annotation for Wave 1 (line 77) reads `loads refs/triage-checklist.md on demand` — but the actual root-cause-analyst spawn that consumes triage-checklist now happens in Wave 1.7. This annotation is also technically stale post-split but was not in AC scope.

These three observations indicate that **Issue 3's split is structurally complete, but a minor follow-up sweep** of stale ref-annotations would close the consistency loop. They do NOT block PASS for Phase 4 because:
- The AC explicitly scoped the Refs row change to only the hypothesis-card-template row
- The adversarial check required byte-identical preservation of the other rows
- These annotations are descriptive metadata, not execution-blocking content

## Adversarial Stance Notes

I assumed the work contained errors and looked specifically for:

- **Silent step deletion**: Verified by counting steps in Wave 1 body (exactly 2) and confirming both old steps 3 and 4 reappear verbatim in Wave 1.7 with the load-bearing `consistency_with_docs` enum and inline-fallback bullet intact. NO content loss detected.
- **Wave Structure code-block corruption**: Counted 4 matches for the wave-line regex, manually inspected block alignment — clean.
- **Orphan emission strings**: Explicitly grepped for `Wave 1 complete: confidence=` (the old emission that should be GONE) — 0 matches. The only remaining "Wave 1 complete" emission is the new grounding-handoff string.
- **Wave 2 header regression**: Confirmed line 210 is byte-identical `### Wave 2: Confidence Gate`.
- **Section boundary integrity**: Confirmed Wave 1.7 is bounded by Wave 1.5 closing `---` (line 188) and Wave 2 header (line 210) with no overlapping content.
- **Preconditions consistency**: Wave 1.5 preconditions updated to drop "step 1" qualifier (consistent with Wave 1 no longer having steps 3-4 to disambiguate from); Wave 1.7 preconditions correctly reference both Wave 1 grounding AND Wave 1.5 card.

## Actions Taken

None — no fixes required. All AC met on first pass.

## Recommendations

1. **PASS Phase 4 and proceed to next phase** of the PR #73 review-fix pipeline.
2. **Open a minor follow-up** to update the two stale Refs loader annotations (`refs/escalation-rubric.md` and `refs/triage-checklist.md` rows) and the Wave Structure code-block line for Wave 1 to reflect post-split reality. Low priority — these are descriptive only.

## QA Complete

VERDICT: PASS
