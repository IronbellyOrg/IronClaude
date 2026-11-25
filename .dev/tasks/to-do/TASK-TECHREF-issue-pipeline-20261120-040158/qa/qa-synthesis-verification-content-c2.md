# QA Report - Synthesis-gate verification (qualitative), cycle 2

QA phase: synthesis-gate verification (qualitative), cycle 2
Fix authorization: false
Date: 2026-11-20
Status: Complete (see the final line)

Inputs read: the task prompt block (task file lines 1659-1686), the cycle-2 BLOCKING list (`qa/qa-synthesis-consolidated-findings-c2.md`, N-1 only), the cycle-2 fix log (`qa/qa-synthesis-fix-cycle2-report.md`), the cycle-1 content report (`qa/qa-synthesis-verification-content-c1.md`), synth-06 lines 170-320 in full, and whole-file greps over all six synth files. Source claims were re-read only under `/home/coder/.cache/ic-snap-20261120/master` (read-only; nothing was written there). Only `synth-06` was modified after the cycle-1 report (file times: synth-01..05 06:21-06:40, synth-06 06:50); the cycle-2 fix touched one table in synth-06 (458 to 459 lines, one row split into two), so the other five files were re-checked by grep for the D-18 / D-21 / decision wording, not re-read line by line.

## Verdict: PASS

0 BLOCKING findings. N-1 is FIXED-OK. No new BLOCKING finding.

## Previous coherence-type BLOCKING findings

| ID | Location | FIXED-OK / STILL-OPEN | Evidence |
|---|---|---|---|
| N-1 | synth-06 Section 14.3 "Future Considerations", former row "Binding coordinator-started workers (D-18) and the OB-H gate as code (D-21)", now two rows at lines 283 and 284; versus D-18 (line 261), D-21 (line 264), 14.1.1 row (line 186) | FIXED-OK | The row is split. Line 283 (D-18): Deferred Because "No decision found in the files this reference cites (D-18); the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`)"; Revisit When "No revisit trigger found in the files read (Q-11)". OD-1, OD-3 and the `OW:822` trigger are gone from it. Line 284 (D-21): "No decision found that leaves the gate prose-only (D-21); the one related owner decision (OD-3) keeps the IR-7 refusal off (`IR7_REFUSE = False`, `OW:818-822`) until the #442 observations pass"; Revisit "After the #442 observations pass, for the IR-7 refusal (`OW:822`); none recorded for the OB-H gate as code". Source checks (snapshot): `docs/designs/sc-issue-launch-level-hook.md:23` reads "A worker that a coordinator starts after a `--pipeline none` claim ... is not launched by the claim script, so this guard does not govern it" (true). `orca_worktree.py:818-822` reads "The refusal path exists but is off (owner decision OD-3)" and `IR7_REFUSE = False  # IR-7: turn on only after the #442 observations pass (owner decision 2026-11-08)` (true, and it is about IR-7 only). Design `:534` is "Limits (OD-1)" (L2 same-user guard), now cited only at 14.1.1 line 187 and D-29 line 272, where it is the right decision. Coherence with D-18 line 261 ("No decision found in the files this reference cites; the guard design says it does not govern such a worker (`...hook.md:23`)"), D-21 line 264 ("Design `:625` says 'Pending, none run'; no decision lets the gate stay unenforced in code") and 14.1.1 line 186 ("none recorded (D-18)"): all say the same thing. `design:625` read: "Pending, none run ... No governed claim ... is used on a real issue until OB-H1 item 1 ... have passed" (a stated gate, no decision to leave it unenforced in code). Q-11 (gaps-and-questions.md:152) is the open question "Should coordinator-started workers be bound?" and says whether binding is wanted is an owner decision, so "no revisit trigger found (Q-11)" is accurate. |

## New BLOCKING findings

| ID | Location | Problem | Evidence | carried-over / new | previously-rated-PASS yes/no |
|---|---|---|---|---|---|
| none | - | No new BLOCKING finding. | See "Checks performed". | - | - |

## MINOR notes (not blocking, not rechecked)

| ID | Location | Note |
|---|---|---|
| m-1 | synth-06 line 284 | The "Deferred Because" cell of the D-21 row states what is not decided rather than a reason for deferral; accurate, awkward fit to the column heading. |
| m-2 | synth-06 D-21 line 264 "12 tests skip" vs synth-04 line 322 / synth-05 line 345 "one test parametrized over 12 entries" | Same fact; "12 tests" counts cases, not functions. Wording only. |
| m-3 | Carried minor notes M-1 to M-10 from cycle 1 | Not rechecked, per the severity rule. |

## Checks performed

1. N-1 fix verified in the live text of synth-06 lines 261, 264, 186, 283, 284 and against the snapshot sources (`design:23`, `design:534`, `design:625`, `OW:818-822`). FIXED-OK.
2. Whole-file grep `owner decision|OD-[0-9]|decided|decision` over all six files: every decision claim traced to a file that records it. OD-1 appears only at 14.1.1 line 187 and D-29 line 272 (design `:534`, true). OD-3 appears only at D-19 line 262 and 14.3 line 284 (`OW:818-822`, true, about IR-7 only; also synth-04 line 321 "owner decision 2026-11-08", true). O-15 appears at synth-04 line 241 and synth-05 line 164 (design `:627`, "owner decision O-15", true). The "Decision:" cells of D-04, D-05, D-06, D-13, D-17, D-22, D-27 and D-29 were verified in cycle 1 and sit in unchanged text; `CHANGELOG.md:17` (removal of the issue-pipeline group and WC-17) and `GUARD:494-497` (rule 1 text retired) re-read and true. The "No decision found" rows (D-01, D-02, D-07..D-10, D-18, D-20, D-21, D-23, D-25, D-30, D-31, synth-04 line 378) make no positive decision claim.
3. Coherence of D-18 across sections: synth-01 line 155 (row 6), line 160 (row 10), line 169 (row 18); synth-04 lines 315 and 389; synth-05 line 88; synth-06 lines 186, 200, 261, 283, 306, 455. All say: no production caller of `pending`, NOT BUILT (binding and caller) with the `pending` verb BUILT-ON, the guard design says it does not govern such a worker (`design:23`), no decision or revisit trigger found. No file attributes a decision to D-18.
4. Coherence of D-21 across sections: synth-01 lines 46 and 164, synth-02 lines 289 and 346, synth-04 lines 30 and 322, synth-05 line 345, synth-06 lines 264, 284, 293, 307. All say NOT BUILT as a mechanism, the gate is prose, the 12 observation cases skip, whether the observations passed is [UNVERIFIED]. Same status word everywhere.
5. Coherence of 14.1.1 / 14.2 / 14.3 for the two items: 14.1.1 "none recorded (D-18)" = D-18 "No decision found" = 14.3 line 283. D-21 line 264 "no decision lets the gate stay unenforced in code" = 14.3 line 284 "No decision found that leaves the gate prose-only". The IR-7 item stays BUILT-OFF in synth-01 row 12, synth-02 lines 201/226/288, synth-04 lines 26/321, synth-05 line 146, D-19; its trigger (#442 observations, `OW:822`) is the same in D-19 and 14.3.
6. PR 686: grep `PR ?#?686|rewrite design|orchestrator.md|unif(y|ied)|dashboard|orchestrator (design|v2|refactor)|brainstorm` over all six files: exactly one hit, synth-01 line 44 ("PR 686 and the rewrite design are out of scope for this reference."). No other mention. `orchestrator.md` has zero hits in the synth files (Q-11's gap-log text names it, but the gap log is not a synth file and no synth file cites it).
7. Aspirational content as current: D-18 / D-21 / IR-7 / hand-off / grant row all carry NOT BUILT, BUILT-OFF, REMOVED or "not found in snapshot"; 14.3 "Future Considerations" rows describe no future work as present.
8. [UNVERIFIED] versus evidence limits: synth-01 line 46, synth-04 line 324, synth-06 U-1..U-11 (U-4 covers OB-H, U-6 covers `pending` callers) agree; unchanged since cycle 1.
9. Fix-introduced defects: hunted at the only edited location (synth-06 lines 283-284); none found (m-1 and m-2 are wording).

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- No Inherited Structural Verdict block was in the spawn prompt, and `qa-synthesis-verification-structural-c2.md` was not read; no structural PASS item was skipped. Standalone behaviour applied (row ids and line numbers were read from the live files, not taken from any report).

**(b) Independent semantic checks (>=1 required, INV-019):**
- N-1 text versus source - verified by reading synth-06 lines 170-320 and `design:23`, `:530-545`, `:620-630`, `OW:812-826` in the snapshot.
- Decision-claim sweep - verified by grep `owner decision|OD-[0-9]|decided|decision` over all six files plus reads of `CHANGELOG.md:17`, `GUARD:494-498`, `docs/designs/issue-watcher.md:28-34`, `design:627`.
- Q-11 meaning - verified by reading `gaps-and-questions.md:152` and synth-04 line 389.
- Single PR 686 sentence - verified by grep over all six files.
- D-18 / D-21 cross-section coherence - verified by grep `coordinator-started|OB-H|prose gate|IR-7|IR7` over synth-01..05 and reads of the matching synth-06 rows.

**Confidence:** Verified: 9/9 checks above | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Limit: synth-01..05 were not re-read line by line this cycle (unchanged since cycle 1, where they were read in full); only grep-based re-checks of D-18 / D-21 / decision / PR 686 wording were done on them.

**Tool engagement:** Read: 6 | Grep: 1 | Glob: 1 | Bash: 7 (read-only greps and `sed -n` on the snapshot). No web research (Tavily not used; none needed).

Status: Complete

