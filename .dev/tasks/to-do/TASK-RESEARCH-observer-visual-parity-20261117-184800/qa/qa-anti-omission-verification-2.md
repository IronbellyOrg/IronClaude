# QA Report: Gate 5 anti-omission fix verification (report-qualitative)

**Topic:** Observer visual-parity research report (issue #606), cycle-1 anti-omission fixes
**Date:** 2026-11-18
**Phase:** report-qualitative (fix-cycle re-verification)
**Fix cycle:** 1
**Report under review:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md` (1938 lines)
**Inputs:** `qa/qa-anti-omission-consolidated-findings.md`, `qa/qa-anti-omission-fix-log.md`
**Inherited Structural Verdict:** none supplied; standalone behaviour.
**fix_authorization:** false (no file modified except this report)

---

## Overall Verdict: PASS (with notes). Remaining blocking: 0

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Blocking finding 1: severity scale now exists in the Section 4 header and 4.1 intro | PASS | Report line 628 holds the scale (Critical = FINDINGS High or a C8 defect; Important = Medium, a gating decision or a Gate 1 Important gap; Minor = Low or a note) and defines C8 defect; line 632 repeats the mapping. Compared with `synthesis/synth-02-target-gaps.md` line 11: the wording matches, the report adds the C8 definition. The dangling "scale in the header" reference (4.1 intro) now resolves. |
| 2 | Abbreviation legend (FIND, RR, R01-R05, W01/W02, GAPS row N, synth-05, OBS) with full paths | PASS | Report lines 23-33. Ran `ls` on every legend path (FINDINGS.md, rendering-rules.md, observe/, research 01-05, web-01, web-02, gaps-and-questions.md, synth-05): all exist. `T`, `VP`, `RR`, `OBS` used by the plan are separately defined at line 1342. |
| 3 | O1 recovered (render_current.py data-mode mix, uncaptured cases) sits correctly | PASS | Report line 339 (a), in 2.4 right after "Spec lines". Source `research/04` line 196 says the same (ledger fixture-mode, questions and desk live-mode, no NO_COLOR/ascii/live/error/hash/height other than 50). Consistent with P0 step 0.3 (line 1482), which already adds NO_COLOR, ASCII and heights and says 50 is not like for like. |
| 4 | O2 recovered (RR 17 header contract wording) | PASS | Line 339 (b) vs `research/04` line 17: `SYNTHETIC FIXTURE <variant>, not Orca data`, `one Run only: <runId>`, no READ ONLY badge. Agrees with M-13 row (line 650) and the P7 spec edit. |
| 5 | O3 recovered (RR 26 untruncated inspector/export vs Desk 4-line cap) | PASS | Line 339 (c) vs `research/04` lines 203 and 205. `grep -n "DESK_TEXT_LINES = " view.py` gives line 99 = 4, so the citation holds. Agrees with M-04 row (line 641) and P0 step 0.6. |
| 6 | O4 recovered (RR 21 key list, no `r` key) | PASS | Line 339 (d) vs `research/04` line 19. No conflicting `r` key anywhere in the plan (grep). Consistent with M-11 (key list not cut). |
| 7 | Recovered text sits in the right sections and does not contradict recommendation, plan or Q1-Q7 | PASS | O1-O4 are in 2.4 (current state), which is where spec-versus-code facts live. No contradiction with Section 7 or the P0-P7 plan found. Marked "read from the files, not run", so it stays honest about verification. |
| 8 | Justified dedups are honest: "release1_surface.py imports only release-1 names" | PASS | This was the dedup most likely to touch the plan (step 1.6(c) edits `release1_surface.py`). The step imports `strip_sgr` from `tests.observe.conftest` (the module already imports `FakeClock` from there), not from `superclaude.cli.observe`, so the research 03 line 136 constraint is respected. The omission does not change a step. |
| 9 | Justified dedups: Zellij and command-pane detail (O5-O9) | PASS | Facts do remain in the cited files: `--max-panes` in `research/05` line 34; `start_suspended`, exit code and Enter re-run in `research/web-02` line 22. The Zellij verdict (optional layout only, never a dependency) does not use them. |
| 10 | Justified dedups: the 27 minor omissions from report 1 | PASS | Counts reconcile: 27 + 9 = 36 minor, 4 recovered (O1-O4), 32 justified (27 + O5-O9). Spot-checked `test_f04` (`research/03` line 49: pins one `[no longer in source window]` line and state-before-subject): it is a constraint inside P4 layout work and does not alter a phase or gate; the `>` marker is already carried by plan step 2.4 (line 1538). Section 4.5 (lines 767-780) already states the collector, parse and key-map internals as intentionally excluded. |
| 11 | Report still scannable, not bloated | PASS | The fix added one legend table (9 rows), one scale paragraph, one severity-words paragraph and one paragraph in 2.4: about 15 lines in a 1938-line, 337 KB report. The 2.4 addition is a dense four-part paragraph (note N3) but is labelled "Further detail from 04". |
| 12 | Severity vocabulary consistent across 1.3, 4.1, 8.10 and the legend | PASS with note | The mapping High = Critical is stated everywhere and matches 4.1 for M-01 to M-05. The Med = Important mapping has a C8 exception that the short mapping sentences omit (note N1). |

## Summary
- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Blocking findings remaining: 0 (the one IMPORTANT omission is fixed and verified)
- Issues fixed in-place: 0 (not authorized)

## Issues Found (all MINOR, notes only, not rechecked later)

| # | Severity | Location | Issue | Suggested fix |
|---|----------|----------|-------|---------------|
| N1 | MINOR | Report lines 35 (legend), 56 (1.3), 1771 (8.10) vs 4.1 rows M-08, M-10, M-11 (lines 645, 647, 648) | The mapping sentences say FIND Med = Important, but M-08, M-10 and M-11 are FIND Medium and Critical in 4.1 because of the C8 rule (the scale in line 628 does say "or a C8 defect"). 8.10 lists those three as "Medium" with no pointer. No decision or phase is affected. | Add "except the three C8 defects M-08, M-10, M-11, which are Critical" to the mapping sentence at line 35. |
| N2 | MINOR | Report line 339 (a) | The mixed fixture/live baseline modes are recorded but no P0 step (0.2, 0.8) says whether the harness keeps the mixed `mode=` header or normalises it, so a reviewer may score a header difference that is a data-mode artefact. | Add one sentence to step 0.8 or the rubric prompt note in 0.5. |
| N3 | MINOR | Report line 339 | The four recovered facts are one long paragraph with (a) to (d) inline. | Optional: turn into a four-row list. |

## Actions Taken
None. fix_authorization is false. No file other than this report was written.

## Inherited Structural Verdict: Reliance Audit
No `## Inherited Structural Verdict` section was supplied, so there is no reliance on rf-qa PASS items.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None (no inherited verdict was provided).

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Severity scale equals the synthesis source: read `synthesis/synth-02-target-gaps.md` line 11 and report line 628.
- O1 to O4 against `research/04` lines 17, 19, 196, 203, 205 (Read), and `DESK_TEXT_LINES = 4` at `view.py:99` (grep).
- Legend paths exist (`ls` of 15 paths, Bash).
- Plan step 1.6(c) read in full to test the "release-1 names" dedup; research 03 line 136 read via grep.
- Dedup locations confirmed in `research/05` line 34 and `research/web-02` line 22; `test_f04` in `research/03` line 49.
- Counts (27 + 9 = 36 minor; 4 recovered; 32 justified) recomputed from the consolidated table.
- Verified claims: about 24. Files read: report (ranges 1-125, 294-363, 626-695, 767-782, 1340-1344, 1470-1524, 1765-1805, headings), consolidated findings, fix log, research 03/04/05/web-02 (targeted), synth-02, `view.py`.
- Why trust a result with no blocking findings: the dedup most likely to be dishonest was tested against the plan step it could break and held; three minor notes were found, so the review was not a rubber stamp.
- Web research: none performed. Tavily not needed (all checks local).

## Confidence
Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 15 | Grep: 8 | Glob: 0 | Bash: 2 (23 Read/Grep/Glob calls for 12 checklist items)

## Recommendations
- Proceed. Optionally apply N1 (one sentence) when the report is next edited; N2 and N3 are optional.

## QA Complete

**PASS. Remaining blocking count: 0.**
