# QA Report: Fix verification, qualitative, Phase 3 research gate

**Topic:** observer visual-parity research, cycle-1 fix verification
**Date:** 2026-11-18
**Phase:** fix-cycle (report-qualitative lens)
**Fix cycle:** 1
**Fix authorization:** false (report only)

---

## Overall Verdict: PASS

Remaining blocking findings: 0

## Checks

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Finding 1 fix (safe_box ASCII claim) in 03 is substantive | PASS | 03 line 194 now tags the old claim CODE-CONTRADICTED, gives the probe, the Rich source lines (rich/box.py:79-83) and the required action (explicit `box=rich.box.ASCII`, chosen in render code). Re-ran the probe on Rich 15.0.0: Panel with safe_box True and False both print `╭──────────────────╮`; `box=box.ASCII` prints `+------------------+`. box.py lines 79-83 read as cited (`if options.ascii_only and not box.ascii: box = ASCII`). |
| 2 | Finding 1 fix in 04 (G-1 row, line 147) is substantive | PASS | The CODE-VERIFIED text no longer says safe_box covers Rich boxes; a CODE-CONTRADICTED correction with the same probe is added; the test_terminal.py:114-116 support is correctly narrowed to the attribute value. Cross-references to 01 lines 204 and 229 (both read, both state it correctly) and 03 section 6 rule 3 resolve. |
| 3 | Finding 2 fix: new section 9 in 02 is substantive, not vague | PASS | Section 9 has a 7-hop trace with file:line, four measurements, a route table and consequences. Re-ran measurement 1 (width 10, height 3, force_terminal): bytes are identical to those quoted (`ESC[?1049h ESC[H ESC[?25l ESC[H ... L1 L2 L3 ... ESC[?25h ESC[?1049l`, rows padded to 10, lines 4-5 dropped, no ellipsis). LiveScreen code at commands.py:257-279 and render() at render.py:524-531 and the reserved/capacity lines (render.py ~499-502) match the cited lines. |
| 4 | Finding 2 claim "no test references LiveScreen or run_interactive" | PASS | grep over tests/observe for `LiveScreen\|run_interactive` returned no file. `tests/observe/spike_child.py:64` does hold `Live(..., screen=True)` as cited. `MIN_ROWS = 8` at terminal.py:22 as cited. |
| 5 | Fixes do not contradict other files | PASS | Section 9 is consistent with 02 section 3 (updated takeaway, line 61), 01 (cross-ref at line 234), 05 (cross-ref at line 76) and 03 line 229 (no LiveScreen test). The G-1 correction agrees with 01 lines 204 and 229. Base fixture still gives 40 lines at width 80 (`wc -l` = 40), matching the "no spare row" claim. |
| 6 | Q1 to Q7 still have their evidence | PASS | Q tags remain in all six research files (27 occurrences). The two fixes only add to Q2/Q5-type evidence (ASCII boxes, live path, height budget); nothing was removed. |
| 7 | Honest tagging of what was not measured | PASS | Section 9 marks heights below 40, whether `run_interactive` accepts `--fixture`, and the real LiveScreen under a pty as [UNVERIFIED]; it says measurement 3 used a stand-in console, not the real LiveScreen. |

## Issues Found (all MINOR, notes only, none introduced by the fixes)

| # | Severity | Location | Issue | Note |
|---|----------|----------|-------|------|
| 1 | MINOR | 01 lines 55 and 231 versus 02 section 2 | 01 still says a styled capture "would have to use `export_text(styles=True)`" with no caveat, while 02 shows that route ignores NO_COLOR and colour down-conversion. Already recorded by the gate as a minor (analyst F-02/F-03, "02 wins"); the fixes did not touch it. | Synthesis must use 02's `console.file.getvalue()` route. |
| 2 | MINOR | 02 section 9.2 measurement 3 | The height-38 crop was measured with the fixture's lines in a stand-in console, not the real `LiveScreen`. Disclosed in the text. | No action. |
| 3 | MINOR | 02 section 9.4 | Frame cost at heights 24 and 44 is still not derived (already a recorded depth note). | Carry to synthesis as a caveat. |

## Summary
- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Blocking findings remaining: 0

## Self-Audit

**(a) Reliance list:** none. No Inherited Structural Verdict was supplied; the fix log and consolidated findings were read as claims to test, not as proof.

**(b) Independent semantic checks:**
- Rich ASCII-box claim: re-ran a Panel probe (Bash, `uv run python -I`) with safe_box True, False and `box.ASCII`; read rich/box.py:79-83.
- Live path bytes: re-ran the Live(screen=True) probe at width 10, height 3 and compared the bytes to section 9.2.
- Code citations: read commands.py:257-279, render.py:495-503 and :524-531, spike_child.py:60-66, terminal.py MIN_ROWS; grep for LiveScreen/run_interactive under tests/observe (empty).
- Cross-file consistency: grep for section-9 references (01:234, 05:76), the safe_box mentions in 01, 03, 04, and `export_text(styles=True)` across the folder.

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 4 | Glob: 1 | Bash: 2

Web research: none performed (no Tavily or fallback calls).

## QA Complete
