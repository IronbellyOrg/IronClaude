# QA Report — Research-Gate Fix-Cycle Verification (Structural)

**Topic:** FR-DRS TDD — research-gate fix cycle 1 (C-1..C-4)
**Date:** 2026-06-21
**Phase:** fix-cycle (research-gate)
**Fix cycle:** 1
**Fix authorization:** FALSE (verification only)
**Stance:** Adversarial — assumed a fix was misapplied or introduced a new defect.

---

## Overall Verdict: PASS

All four research-fix items (C-1, C-2, C-3, C-4) were applied correctly. No fix corrupted
surrounding content, all four research files parse as well-formed markdown (balanced code
fences), and no NEW evidence error was introduced by the fix cycle.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| C-1 | file 01 L3 now `**Status: Complete**` (was "In Progress") | PASS | Read `research/01-runtime-surface-algorithm.md:3` = `**Status: Complete**`. `grep "In Progress"` → NONE. Footer L281 also `**Status: Complete**` — header/footer now agree (the original contradiction is gone). |
| C-2 | file 03 header carries a `**Status:** Complete` marker | PASS | Read `research/03-consumer-surfaces.md:3` = `**Status:** Complete`, inside the header block (L1-9). `grep "Status:"` → exactly one hit, at L3. |
| C-3 | file 01 §6 FR-RSR.7 forbidden-keys citation re-anchored to SKILL.md §9.1 L721-730 (not "SKILL:L491") | PASS | The three contract-discipline citations in §6 (lines 230, 235, 245) now read `SKILL §9.1 MANDATORY EMISSION comment, SKILL.md:L721–L730`. Cross-checked source: SKILL.md 721-730 IS the `MANDATORY EMISSION (FR-RSR.7)` comment block; the three forbidden keys (`runtime_surface_reachable`, `reachability_path`, `static_caller_absent_is_expected`) appear verbatim at SKILL.md:723-724 (`sed -n 721,730p`). Re-anchor is accurate. |
| C-4 | file 04 says grader.py is 518 lines (was 519) | PASS | `wc -l grader.py` = **518**. `research/04-eval-path-integration.md:12` now reads `grader.py (518 lines)`. `grep "519"` → NONE. |
| S1 | No collateral corruption / fence balance | PASS | Code-fence parity: file 01 = 6 fences (balanced), file 03 = 0 (balanced), file 04 = 2 (balanced). `wc -l`: 281 / 294 / 180 — all substantial, none truncated. |
| S2 | No NEW evidence error introduced | PASS | grader.py internal citations in file 04 (318, 410, 434, 448, 449, …) all < 518, so the 518 correction invalidates no other citation. Remaining `SKILL:L491` / `L465–L491` refs in file 01 (L187, L255, L271) are legitimate §6.1 step-4b'/4b prose citations (SKILL.md 465-491 confirmed), NOT the forbidden-keys claim — correctly left intact. |

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (verification-only; fix_authorization: FALSE)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| A-1 | OUT-OF-SCOPE (advisory, pre-existing) | research/04-eval-path-integration.md:13 | `evals.json (1134 lines)` uses editor-line convention while the sibling grader.py count uses `wc -l` (518). `wc -l evals.json` = 1133; the file ends with a trailing `\n` so the editor shows 1134. Mixed conventions within one bullet list. | NOT a fix-cycle defect — not among C-1..C-4, not touched by the fix, and does not affect any line-range citation (1030-1110, 1112-1132 all valid). Optional future hygiene: standardize on `wc -l`. Does NOT change the PASS verdict. |

## C-3 nuance (adversarial note, resolved)
The fix-cycle brief asked me to confirm the forbidden-keys content "actually lives at SKILL.md
721-730." It does — the MANDATORY EMISSION comment block (721-730) names all three forbidden
keys at 723-724. Note that the SAME FR-RSR.7 contract-discipline rule ALSO appears in prose form
at SKILL.md:491 ("Do NOT improvise alternative keys … runtime_surface_reachable, reachability_path,
static_caller_absent_is_expected"). The original "SKILL:L491" anchor was therefore not *content-wrong*,
but the canonical §9.1 contract-block home of the MANDATORY EMISSION / forbidden-keys list is 721-730,
and that is the correct, more-specific anchor. The re-anchoring is an improvement and is accurate; the
residual `L491`/`L465–L491` references that remain in file 01 cite the §6.1 step prose (a different,
legitimate source span), not the forbidden-keys list — they were correctly NOT changed.

## Confidence Gate
- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: ~9 (within Bash) | Glob: 0 | Bash: 5
- Every checklist item was verified with direct tool output (Read of the edited lines + Bash
  `wc -l` / `grep` / `sed` against both the research files and SKILL.md / grader.py source truth).
- No UNCHECKED items. No UNVERIFIABLE items.

## Recommendations
- Green light: all four research-fixes are correctly applied with no new defect. The research gate's
  C-1..C-4 fix scope is satisfied; synthesis may proceed (subject to the C-5/C-6/C-7 TDD-synthesis
  carry-forwards already recorded in the consolidated findings, which are not research-file edits).
- Optional, non-blocking: harmonize file 04's `evals.json` line-count to the `wc -l` convention (1133)
  used elsewhere. Advisory only.

## QA Complete
