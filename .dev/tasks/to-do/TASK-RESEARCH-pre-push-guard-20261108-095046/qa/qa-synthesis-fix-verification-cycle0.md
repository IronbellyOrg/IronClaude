# QA Report — Synthesis Gate Fix Verification (Gate 2, cycle 0)

**Topic:** git pre-push hook semantics (L2 pre-push guard, issue #441)
**Date:** 2026-11-08
**Phase:** synthesis-gate (verification of fix cycle 1)
**Fix cycle:** 1
**Fix authorization:** false (report only; no synthesis file was edited)

Inputs: `qa/qa-consolidated-findings-phase5-cycle0.md`, `qa/qa-synthesis-fix-log.md`, `synthesis/synth-01..04-*.md`, research files under `research/`.

---

## Overall Verdict: PASS (with notes)

Open blocking (CRITICAL + IMPORTANT): 0. Previous cycle: 8. Monotonicity holds (0 < 8). No regression: no item that passed before now fails.

## Blocking findings B1-B8

| # | Original finding | Fixed | Evidence | New issue |
|---|------------------|-------|----------|-----------|
| B1 | Stdin record order stated in contradictory ways; G-24 called resolved by command-line order; synth-04 row 22 misattributed; no §9.4 row | yes | synth-01 line 309 (diagram "order undocumented, seen both ways"), line 330, line 445; synth-02 G-24 line 195, W1-21 line 305; synth-03 G-24 mapping line 318; synth-04 row 22 (line 43) and new §9.4 row (line 90). All say undocumented, seen both ways, hook scans every record. Checked against research: 04 line 549 (E7 "in command-line order here"), 04 line 702 (E9 "neither alphabetical nor local-ref order"), 04 line 1339 (E24 "identical in both runs ... existing remote ref first"), 04 line 2249 (order rule inferred [UNVERIFIED]), web-01 line 226 (G3 command-line order, one observation), line 428 (code does not sort), line 471 ("no order is documented") | none |
| B2 | IR-7 status inconsistent; Phase 4.4 conditional; OQ-7 re-asks a decided question | yes | synth-03 §7 line 179, Phase 4.4 (line 248), new Phase 6.11 (line 276), Phase 7.5 (line 286), G-17 mapping (line 311), checklist line 392, OQ-7 (line 411); synth-02 G-17 (line 188), DOC-5 (line 258); synth-04 row 12 (line 28) and R3 (line 69). All say default DECIDED off, refusal path built behind a switch and tested; only mechanism and turn-on criterion open. Matches seed-brief line 68 ("exists and is tested, ships switched off") and line 77 | none |
| B3 | Three different stdin rules | yes | One rule in synth-02 T-6 (line 26), T-10 (line 30), §3.3 table and diagram (lines 41-44, 60), SC-12/SC-13 (lines 108-109), G-42 (line 213); synth-03 Phase 1.7 (line 218), Phase 6.2 (line 267), checklist line 384; synth-04 row 32 (line 53) narrowed to "confirm the rule". Source: web-01 line 421 (`transport.c` 1327-1329, EPIPE), line 431 (early exit safe), line 504 (rec 3) | none |
| B4 | L1-8 has no Section 8 step; mapping covers only G-n | yes | synth-03 Phase 5.4 (line 258) adds L1-7 and L1-8; Phase 5.5 (line 259) adds DOC-9; new BP/L1/DOC mapping table (lines 339-377) maps BP-1..14, L1-1..10, DOC-1..11. L1-8 source confirmed: 02 line 185 (`gh $'\x61pi'`, PARTIAL) | none |
| B5 | Open owner decisions (U28, marker, identity-script location) presented as settled | yes | synth-03 Phases 1.3 (line 214), 2.4 (line 229), 2.5, 2.7 (line 232), 4.1 labelled "proposed; conditional on OQ-n"; checklist lines 382, 383, 389; new OQ-18/19/20 (lines 422-424); synth-04 rows 2, 14, 15 (lines 18, 30, 31) say open in seed-brief lines 78, 76, 75. Seed-brief lines 75, 76, 78 confirmed open (read lines 66-79) | MINOR N-13, N-14 |
| B6 | API/library bypass has three statuses | yes | synth-01 D19-30 (line 395), OQ1 (line 441); synth-02 D19-30 (line 146), G-1/G-2 (lines 172-173), §4.5 (line 271), §5.5 (line 401); synth-03 G-1/G-2 mapping (lines 295-296); synth-04 row 11 (line 27), R4 (line 70), R5 (line 71). One status: documented externally (web-01 H/J), not confirmed at runtime | MINOR N-15, N-16 |
| B7 | "2.47.3 or later" generalised | yes | Grep for "2.47.3 or later" across `synthesis/` returns no match. synth-02 §5.5 Version risk (line 405); synth-03 Phase 6.10 (line 275), new Phase 7.8 (line 287); synth-04 rows 34 (line 55) and 40 (line 61). Source: web-01 lines 407-410 (2.54.0 hook API and config hooks, 2.98.0 draft), line 522 (rec 7) | MINOR N-17 |
| B8 | synth-01 §1 L1 row overclaims coverage | yes | synth-01 line 30 now "the non-canonical push spellings it recognises (LL-PUSH-FORM)" with the known misses listed; consistent with 02 line 185 (PARTIAL) and 02 lines 180-182 (smart-HTTP and hidden API hosts ALLOWED) | none |

Fixed: 8 of 8. Still failing: 0.

## Synthesis-gate checklist re-applied to the changed sections

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers | PASS | synth-01 §1-§2, synth-02 §3-§5, synth-03 §6-§8, synth-04 §9 (9.1-9.4) and §10 present; the new mapping table and §9.4 row sit under existing headers |
| 2 | Table structure | PASS | Gap tables keep Gap / Current / Target / Severity / Notes (synth-02 line 195); plan steps keep Step / Action / Files / Details (synth-03 lines 214-289); open-question tables keep # / Question / Impact / Suggested Resolution |
| 3 | No fabrication | PASS | Changed claims spot-checked against sources: 04 lines 549, 702, 1339, 2249; web-01 lines 226, 421, 428, 431, 471, 407-410, 522; 02 lines 180-185; seed-brief lines 68, 73-78. No unsourced claim found in the changed text |
| 4 | Evidence citations | PASS | Changed rows cite file and line (for example synth-04 line 90 cites 04 lines 549, 702, 1339) |
| 5 | Options analysis | PASS | Unchanged by the fixes; Options A, B, C and the comparison table remain (synth-03 lines 27-150) |
| 6 | Plan specificity | PASS | New and changed steps name files: Phase 6.11, 7.5, 7.8 target design §19 lines; Phase 5.4/5.5 target the L1 guard |
| 7 | Cross-section consistency | PASS (notes) | Stdin rule, IR-7 status, bypass status and version wording now agree across all four files. Residual cross-reference staleness N-14 is MINOR |
| 8 | No doc-only claims in S2/S6/S7/S8 | PASS (note) | The bypass status is labelled external in S2 (synth-01 line 395). The §7 bypass table (synth-03 lines 171-174) tags every row [EXTERNAL] in its evidence column but says "hook never runs" without "not confirmed at runtime" (N-16, MINOR) |
| 9 | Stale docs surfaced | PASS | [STALE DOC] IR-7 (synth-04 row 12), D19-47 (row 20), §19.6 artifacts (row 16), guard line 80 (row 8) present |
| 10 | Content rules | PASS | Tables for multi-item data; ASCII diagrams unchanged; no source reproductions |
| 11 | No placeholders | PASS | No TBD/TODO in changed sections; OQ-18..20 carry real questions with seed-brief line cites |
| 12 | No hallucinated paths | PASS | `ls` confirmed: `src/superclaude/cli/install_hooks.py`, `src/superclaude/hooks/scripts/launch-job-identity.sh`, `src/superclaude/hooks/scripts/launch-level-guard.sh`, `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, `tests/hooks/test_launch_level_guard.py`, `tests/hooks/test_launch_job_identity.py`, `tests/cli/test_install_hooks.py`, `tests/hooks/test_launch_level_observations.py`, `docs/designs/sc-issue-launch-level-hook.md` |

## New issues (all MINOR; notes only, they do not fail the gate)

| # | Severity | Location | Issue | Suggested fix |
|---|----------|----------|-------|---------------|
| N-13 | MINOR | synth-03 line 47 (Option A Identity), line 113 (sub-choice A-i), §8 diagram line 203 | State `~/.claude/hooks/launch-job-identity.sh` as the location without the "proposed; conditional on OQ-20" label that Phase 1.3 now carries | Add "(proposed, OQ-20)" to these mentions |
| N-14 | MINOR | synth-04 rows 2, 14, 15 (lines 18, 30, 31); synth-04 §10 synth-03 row (line 122); synth-03 OQ-18 Gap column (line 422) | Rows 2/14/15 do not name OQ-20/19/18 although line 6 promises the OQ cross-reference; §10 still says "OQ-1 to OQ-17"; OQ-18 Gap column says "none" although G-20 is the U28 gap (synth-04 row 15) | Add the OQ numbers; change "OQ-1 to OQ-17" to "OQ-1 to OQ-20"; set the OQ-18 Gap to G-20 |
| N-15 | MINOR | synth-01 line 350 (§2.5(b)) | Still says API and library pushes are "not testable locally [UNVERIFIED], routed to web-01" with no pointer to the external status. Accurate as a report of 04's scope, so it is not a fourth status | Append "; documented externally (web-01 H/J), not confirmed at runtime" |
| N-16 | MINOR | synth-03 §7 bypass table lines 171-174 | "hook never runs" for libraries, REST API, smart-HTTP and GitPython lacks "not confirmed at runtime"; the rows are tagged [EXTERNAL] | Add the qualifier to the cell |
| N-17 | MINOR | synth-03 lines 286-289 | Phase 7.8 is listed between 7.5 and 7.6 | Move 7.8 after 7.7 |

Previous MINOR notes N1-N12 were not rechecked, per the review severity rule.

## Summary

- Blocking findings verified fixed: 8 / 8
- Checklist items passed: 12 / 12
- Open CRITICAL: 0. Open IMPORTANT: 0. New MINOR: 5 (N-13 to N-17)
- Files edited: none other than this report (fix authorization false)

**Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(TOTAL = 8 blocking-finding checks + 12 checklist items.)

**Tool engagement:** Read: 11 | Grep: 4 | Glob: 0 | Bash: 1 (path existence check). No web research (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0). Read+Grep (15) is below TOTAL (20) because several checks rest on the same full-file reads of synth-01..04; each B-row cites the line it relied on.

## Recommendations

- Proceed to assembly (Phase 6). N-13 to N-17 can be applied during assembly; they are wording and cross-reference notes.

## QA Complete
