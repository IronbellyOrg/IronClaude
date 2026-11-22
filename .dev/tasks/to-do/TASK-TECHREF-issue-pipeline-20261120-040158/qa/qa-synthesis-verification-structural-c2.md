# QA Report - Synthesis Gate Verification (structural), cycle 2

**Topic:** IronClaude issue-to-work pipeline technical reference (six synth files)
**QA phase:** synthesis-gate verification (structural), cycle 2
**Date:** 2026-11-20
**Fix authorization:** false (nothing modified except this report)
**Inputs:** previous BLOCKING list `qa/qa-synthesis-consolidated-findings-c2.md` (N-1 only); fix log `qa/qa-synthesis-fix-cycle2-report.md`; synth-01..06 in `synthesis/`; snapshot `/home/coder/.cache/ic-snap-20261120/master` (read only)
**Status:** Complete

## Verdict: PASS

BLOCKING findings: 0 (N-1 FIXED-OK; no new BLOCKING finding).

## Previously BLOCKING findings

| ID | Synth location | FIXED-OK / STILL-OPEN | Evidence |
|---|---|---|---|
| N-1 | synth-06 Section 14.3 "Future Considerations", old single row at line ~283, now two rows at lines 283 and 284 | FIXED-OK | Row 283 (D-18) now reads "No decision found in the files this reference cites (D-18); the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`)" with revisit "No revisit trigger found in the files read (Q-11)". OD-1, OD-3 and the `OW:822` trigger are gone from it. Snapshot `docs/designs/sc-issue-launch-level-hook.md:23` says "A worker that a coordinator starts after a `--pipeline none` claim ... is not launched by the claim script, so this guard does not govern it" (read, true). Row 284 (D-21) says no decision found that leaves the gate prose-only, and that the one related owner decision (OD-3) keeps the IR-7 refusal off (`IR7_REFUSE = False`, `OW:818-822`) until the #442 observations pass; revisit "After the #442 observations pass, for the IR-7 refusal (`OW:822`); none recorded for the OB-H gate as code". Snapshot `orca_worktree.py:818-822` read: comment "owner decision OD-3", `IR7_REFUSE = False  # IR-7: turn on only after the #442 observations pass (owner decision 2026-11-08)`; design line 355 says the refusal "stays off until the #442 observations pass and the owner approves". The text states what OD-3 decides and does not present it as a deferral decision for the OB-H gate. Agrees with D-18 (line 261: "No decision found in the files this reference cites ..."), 14.1.1 row at line 186 ("none recorded (D-18)") and D-21 (line 264: "no decision lets the gate stay unenforced in code"). |

## New BLOCKING findings

| ID | Location | Problem | Evidence | carried-over / new | previously-rated-PASS yes/no |
|---|---|---|---|---|---|
| none | - | - | - | - | - |

## Checks performed

1. N-1 re-read at the live location: synth-06 lines 278-284 (Read lines 236-310), both new rows cited above; the text of every cited source line re-read in the snapshot (`design:23`, `design:355`, `OW:815-823`; Grep of the design for `#442`, `OB-H`, `OD-3`).
2. Table structure after the row split: awk cell count gives 3 cells for every 14.3 row (lines 278-284) and 7 cells for the 14.2 rows checked (header line 242, D-18 line 261, D-21 line 264). `grep -c '^| D-'` gives 31 rows (D-01 to D-31), none lost. synth-06 is 459 lines (458 in the cycle-1 content report) = one added row; `**Status:** Complete` still at line 4.
3. Scope of change: file modification times show synth-01 to synth-05 were last written at or before 06:40:02, before the cycle-1 verification reports (06:46 and 06:49), and their line counts (198, 347, 331, 390, 375) equal those the cycle-1 content report recorded. Only synth-06 changed after cycle 1 (06:50:41). So the other five files carry no cycle-2 edit.
4. Same wrong claim elsewhere: Grep for `D-18`, `D-21`, `OD-1`, `OD-3`, `OW:818`, `OW:822`, `coordinator-started`, "Owner decisions", "After the #442" across all six files. `OD-1` and `OD-3` appear only in synth-06: D-19 (OD-3, correct), D-29 (OD-1 = declared limits, correct, design `:534` read), and row 284 (OD-3, correct). synth-04 lines 26 and 321 state the IR-7 refusal as BUILT-OFF with the same `OW:822` and "#442 observations" wording. No file repeats the old claim.
5. PR 686 / rewrite design: Grep shows `PR 686 and the rewrite design are out of scope for this reference.` only at synth-01 line 44. The other hits for `686` are line ranges (`P/cycle.py:685-686`, `record.py:654-686`, `SET:669-686`); "rewrite" hits are the verb ("job-identity rewrites governed calls"). `orchestrator.md` has zero hits in all six files.
6. Status words: the two new rows use no status word; the D-18, D-19, D-21 rows are unchanged and use only BUILT-ON / BUILT-OFF / NOT BUILT / REMOVED.
7. Placeholder scan: Grep for `TBD|TODO|FIXME|lorem|[placeholder` over synthesis/ returns no matches.
8. Spot-check of the 12-item checklist on synth-06 (the only file touched): section headers 12, 13, 14, Appendix B present; tables keep their column structures; new text cites real paths (all three cited source files exist in the snapshot and the lines were read); no doc-only claim added; stale-doc rows X-28 and KW-5 still in 14.1; Q-11 exists in `gaps-and-questions.md:152`.

## Notes (MINOR, not blocking, not rechecked)

- The row 283 revisit cell points to Q-11, which is defined in `gaps-and-questions.md` but not in synth-06 itself (the dangling-id note M-9 from cycle 1 already covers this class).
- The cycle-1 MINOR notes M-1 to M-10 remain as recorded.

## Self-audit

Evidence for the 0-finding result: Read of synth-06 lines 236-310, the cycle-2 consolidated findings, the cycle-2 fix report and the whole cycle-1 content report; Grep over all six files for the decision terms and for PR 686; Bash for cell counts, line counts, mtimes and the source line reads. The one fix is a single table row split, so the new-error surface is small; I looked for a wrong OD attribution, a column-count break, a lost D row, a second PR 686 mention and a stale repeat elsewhere, and found none.

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 5 | Grep: 8 | Glob: 0 | Bash: 4

Status: Complete
