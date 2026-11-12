# Refactoring Plan

Abbreviations: TL is the tasklist `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`. DESIGN is `docs/designs/orchestrator-mode.md`. research/04 is `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/04-design-fixes-r3.md`. DA is `diff-analysis.md`. INV is `invariant-probe.md`. CAL is a card's Part 2 blind calibration. Severities below are CALIBRATED severities, not card self-ratings.

## Overview

- Base variant: V2 (qa card, `variant-2-original.md`), combined score 0.847.
- Incorporating from: V1 (analyzer card, row ledger and R1 findings), V3 (refactorer card, design-fix rows and R3 findings), and the Round 2.5 probe (fix sufficiency).
- Total planned changes: 25 (23 merged findings, one per register entry, plus 2 ledger changes).
- Merged register: 23 findings. HIGH 3, MEDIUM 6, LOW 14.
- Overall risk: Moderate. The three HIGH fixes touch many TL sites each, and a partial edit leaves a deadlock or a failing check.

## Merged Findings Register

One entry per de-duplicated finding. "Sources" names every card finding, debate point and probe item merged into the entry. Every file:line from those sources is kept.

| ID | Sev | Title | Sources | Evidence |
|---|---|---|---|---|
| F-01 | HIGH | Owner-gate deadlock: Branch 1 fires on PENDING before Branch 2 can resolve, at every owner-decision site | R2-G7 (HIGH), R2-G2 (MEDIUM, 7.15 and 14.7 quote parts), V1 R2 New Evidence 2, V3 R2 New Evidence 1 and 3, C-002, X-001, INV-001 to INV-008 | TL:982-992, TL:989, TL:1140, TL:1151, TL:1165, TL:1179, TL:1193, TL:1207, TL:1221, TL:1242-1248, TL:2481-2484, TL:2488, TL:192, TL:978, TL:184, TL:988, TL:1138, TL:1298-1314 |
| F-02 | HIGH | 8.3 `grep -c` "appears once" fails a correct `models.py` | R2-G5, V1 R2 New Evidence 1, V2 R2 New Evidence 1, C-007, INV-012, INV-013, INV-014 | TL:1426-1435, TL:1431, TL:1434, DESIGN:447-468, DESIGN:466 |
| F-03 | HIGH | 7.16 step (6) records two discovery commands (`echo` of the tab-map path, `ls -la` of that path) but four texts allow only the eight templates or a file read | R2-G3, T1 F3, V2 R2 New Evidence 3, C-001, INV-009, INV-010, INV-011 | TL:1248, TL:1249-1256, TL:1257, TL:1258-1261, TL:1314, DESIGN:894 |
| F-04 | MEDIUM | 14.11 test-traceability lens searches the wrong folders for FR-023 and FR-024 | R1-G3, V1 R2 New Evidence 4, C-006 | TL:2509, DESIGN:777, DESIGN:778 |
| F-05 | MEDIUM | Task-level rule (cite GAPS line 138 for counts, never edit REPORT) is missing; INF-001 match to 7.26 is false | R2-G1 (partly), C-005, C-015 | DESIGN:78-80, TL:1326-1331 |
| F-06 | MEDIUM | 7.3 and 7.4 ask the owner only for the rule id, not the revised WC-16 text and its cadence change | R3-G4, INV-021 | DESIGN:5, DESIGN:988, TL:1156-1168, TL:2877, src/superclaude/core/WORKER-CONTRACT.md:110 |
| F-07 | MEDIUM | 8.1 counts six combined grep matches, not one PASS per gate file | R2-G6 | TL:1417-1421 |
| F-08 | MEDIUM | 8.9 has no negative guard test; INF-013 row overstates coverage | R2-G8, X-007, V2 R2 (INF-013 relabel) | TL:1467-1476 |
| F-09 | MEDIUM | SP-28 byte-limit rationale has no deliverable | R2-G10 (partly), C-009 | DESIGN:987, TL:1535-1539 |
| F-10 | LOW | Nothing HALTs when item 1.4 records an anchor as CHANGED (probe-sourced, INV-017; no card holds it, not calibrated) | INV-017, A-007, V1 R2 New Evidence 3 | TL:224, TL:229-234, TL:233, src/superclaude/core/WORKER-CONTRACT.md:110, tests/skills/test_worker_contract.py:25, tests/skills/test_worker_contract.py:155-173 |
| F-11 | LOW | 5.5 greps `:545`, `:865`, `:470`, `:398`, which cannot match "(line 545)"; `line 624` unchecked | R3-G3 | TL:796 (card cited TL:792), TL:827, DESIGN:677-680, DESIGN:686 |
| F-12 | LOW | FR-010 single-row clause lost after R3-B1 edit 4; the R3-B2 text is framed for several rows | R3-G1 (partly), V3 R2 New Evidence 2, C-003, X-002, A-001, INV-015 (MEDIUM, fix scope), INV-016 | research/04:90, research/04:115-116, research/04:148, TL:249, TL:251, TL:293-349, TL:423, TL:425 |
| F-13 | LOW | 3.1 fallback "(as for duplicate Dispatch rows, in this bullet)" points at the wrong place | R3-G2 | TL:425 (card cited TL:423), DESIGN:494-505, research/04:148 |
| F-14 | LOW | 11.1 Triggers text lacks "at most once every 5 minutes" | R3-G5, C-012 | TL:1952, TL:773, TL:787, TL:2258 |
| F-15 | LOW | 13.6 adds a CHANGELOG test bullet not in routing row R8 | R3-G6, C-013 | TL:2293, DESIGN:701 |
| F-16 | LOW | B5 holds by construction but no item runs `make lint-architecture` | R3-G8, C-014 | src/superclaude/contracts/__init__.py:1-6, src/superclaude/contracts/__init__.py:35-36, src/superclaude/contracts/__init__.py:302-313, TL:1430 |
| F-17 | LOW | 8.8 fake `patch_git` rebuilds the env instead of recording what it receives (preference) | R3-G7 (partly), X-012 | TL:1467, tests/cli/reflect/conftest.py:59-74 |
| F-18 | LOW | 14.5 uses an unchanged full-tree count (168), blind to one hit removed and one added | R1-G6 (count part only) | DESIGN:939, DESIGN:940, TL:2470 |
| F-19 | LOW | No TL text names the M2 owner route for unparseable run-current output | R1-G1 (partly), X-005, INV-020 | DESIGN:874, DESIGN:971, TL:1258, TL:1265 |
| F-20 | LOW | 8.6 and 9.2 fixed insertion counts measure the whole working tree | R2-G4 (partly) | TL:1453-1456, TL:1634 (card cited TL:1635-1636) |
| F-21 | LOW | Delivery items do not carry their FR or NFR ids | R1-G2 (partly), C-004 | TL:1784, TL:2677, DESIGN:777, DESIGN:783 |
| F-22 | LOW | The R1+R2+R3 one-commit grouping is carried by no item | R1-G4 (partly), C-010 | DESIGN:705, DESIGN:932, TL:2254, TL:2754 |
| F-23 | LOW | Coverage matrix has no B2 row | R2-G9 (partly, matrix row only), X-004 | DESIGN:215-219, coverage-matrix.yaml:232-237, coverage-matrix.yaml:849-880, TL:1784-1785 |

## Planned Changes

Target for Changes 1 to 23 is the merged verdict's findings list, entry F-nn, built on V2's finding schema (`gap_class`, calibrated `severity`, `evidence`, `recommendation`). Each recommendation below is the text the merged entry carries.

### Change 1: F-01 owner-gate deadlock, complete fix (HIGH)

- Source: V2 R2-G7 and R2-G2; V1 and V3 Round 2 New Evidence; INV-001 to INV-008.
- Target: merged F-01, replacing V2 R2-G7 and the 7.15 and 14.7 parts of R2-G2.
- Rationale: C-002 (V2, 98%) and X-001 (V2, 99%). INV-001 (HIGH) shows that a fix "once, in 6.2 and TL:1140" misses six inline copies; INV-002 (HIGH) shows 7.15 deadlocks the same way.
- Integration point: findings, HIGH group, first entry.
- Recommendation text, applied at every site: 6.2 (TL:989), the shared procedure (TL:1140), the six inline copies in 7.2, 7.4, 7.6, 7.8, 7.10, 7.12 (TL:1151, TL:1165, TL:1179, TL:1193, TL:1207, TL:1221), 7.15 (TL:1242) and 14.7 (TL:2481):
  1. Add a transcription step before the branch test that copies the owner's words from the current session into the record (for 7.15, also the Run id, `Given by:` and `Source:`).
  2. Branch 1 HALTs only when `Chosen:` is empty (for 7.15, only when `Run id:` is empty), not on PENDING status.
  3. Branch 2 sets RESOLVED only when every record line is filled and `Decision source:` quotes the owner's words from the current session. 14.7 and 7.15 get the same quote clause; 7.16 rechecks it before any live call (R2-G2).
  4. Add a final else-branch that HALTs for any other state (filled `Chosen:` with an empty `Decided by:` or `Decision source:`, a non-quote source, or a choice outside (a) and (b)) (INV-003).
  5. If the owner's words are not in the current session (for example after a rollover), HALT; do not transcribe from memory or an earlier transcript (INV-004).
  6. Add a resume clause to the HALT rule at TL:192 (and TL:978): on re-entry, the executor clears the Blocked status and re-runs the HALTed item first (INV-005, INV-008 for 14.8 Branch (B) at TL:2488).
  7. Use one record line count everywhere (four lines, as TL:1140), and align the inline items and the 7.22 lens (TL:1298-1314) to it (INV-006).
- Check: a grep of "PENDING or" over TL returns 0 lines; a grep of the else-branch HALT sentence returns 9 lines (TL:989, 1140, 1151, 1165, 1179, 1193, 1207, 1221, 2481) plus 7.15.
- Risk: Medium. Nine near-identical edits; missing one site keeps 7.13 blocked (it needs seven RESOLVED rows).

### Change 2: F-02 8.3 declaration count (HIGH)

- Source: V2 R2-G5; INV-012, INV-013, INV-014.
- Target: merged F-02, replacing V2 R2-G5.
- Rationale: C-007 (V2, 98%). INV-012 widens the defect to most DESIGN 7.2 names (SweepInput, SweepResult.rows, WorktreeState name each other); INV-013 requires a stated pattern.
- Integration point: findings, HIGH group.
- Recommendation text: in 8.3 (TL:1434), replace "appears once (`grep -c` per name)" with a declaration count using the pattern `^(class NAME\b|NAME\s*[:=])`, expecting exactly 1 per name. State the name set as "the DESIGN 7.2 names (DESIGN:447-468, including the constants JSON_SCHEMA_VERSION, CLASSES, PACKAGE_STATES, SAFE_VALUES) plus ClassifiedRow" (INV-014), so the required OQ-14 and OQ-11 comment line on ClassifiedRow is not counted.
- Check: the pattern accepts `class SessionRow`, `CLASSES: tuple[str, ...] = (` and `SAFE_VALUES = ...`, and does not match `row: SessionRow` (TL:1431).
- Risk: Low. Single item; Change 16 edits the same item.

### Change 3: F-03 7.16 command allowance, all four texts (HIGH)

- Source: V2 R2-G3; INV-009, INV-010, INV-011.
- Target: merged F-03, replacing V2 R2-G3.
- Rationale: C-001 (V2, 97%). INV-009 (HIGH): an allowance in 7.16 alone still fails TL:1248, TL:1260 and the 7.24 lens (TL:1314, each breach BLOCKING); DESIGN:894 says "read the files only".
- Integration point: findings, HIGH group.
- Recommendation text: allow exactly two extra commands, in step (6) of 7.16 and nowhere else: `echo "${XDG_STATE_HOME:-$HOME/.local/state}/ccsession/orca-tabs/"` and `ls -la <printed path>`. A file read of a literal path cannot list the tab-map folder, so both commands stay. Edit all four texts together:
  - (a) TL:1248: change "The ONLY commands allowed" to "The ONLY commands allowed are the eight templates below and the two step (6) discovery commands (the `echo` of the tab-map path and `ls -la` of that printed path)".
  - (b) TL:1257 and TL:1258: keep step (6) as written and add that these two are the only non-template commands.
  - (c) TL:1260: change "one of the eight templates or a file read" to "one of the eight templates, one of the two step (6) discovery commands, or a file read".
  - (d) The 7.24 lens (TL:1314): add the same two commands to the set it accepts, so no breach is raised for them.
- Also, with the same edit:
  - Write each command to the probe file as a `$ ` command record line, separate from captured stdout and stderr, and run the TL:1260 grep over command records only (INV-010).
  - Either add a step that writes the forbidden-list sentence into the probe file, or drop the "only the forbidden-list sentence" expectation (INV-010).
  - Add `check` to the TL:1260 grep pattern, matching TL:1257 (INV-011).
- Check: a correct run's probe file passes TL:1260 and the 7.24 lens, and a grep for `ls` or `echo` in command records finds only the two step (6) commands.
- Risk: Medium. Four texts read the same command list; a mismatch between them fails a correct run.

### Change 4: F-04 14.11 lens folders (MEDIUM)

- Source: V1 R1-G3.
- Target: merged F-04 (new to the base).
- Rationale: C-006 (V1, 99%), CAL holds MEDIUM.
- Integration point: findings, MEDIUM group.
- Recommendation text: in the 14.11 lens (TL:2509), replace "in tests/sweep/ or tests/commands/test_sweep_command.py" with "in the test file the row names (tests/sweep/, tests/commands/, tests/skills/, tests/core/ or tests/recommend/)", and note that NFR-012 has no test by design (DESIGN:777-778).
- Check: the edited prompt names tests/skills and tests/recommend.
- Risk: Low.

### Change 5: F-05 GAPS line 138 rule (MEDIUM)

- Source: V2 R2-G1.
- Target: merged F-05, replacing V2 R2-G1 at calibrated MEDIUM (self HIGH dropped, X-008).
- Rationale: C-005 (V2, 97%); DA greps for `GAPS line 138`, `113 rows`, `never edit the REPORT` return 0 hits.
- Integration point: findings, MEDIUM group.
- Recommendation text: add the DESIGN:78-80 rule to TL Key Constraints with the counts 113/88/25 and the GQ-113 interpretation; the text cites GAPS line 138 and says never edit REPORT. Record the INF-001 to 7.26 match (TL:1326-1331) as a false match.
- Check: the three greps above each return at least 1 hit in TL.
- Risk: Low.

### Change 6: F-06 owner approves the WC-16 text (MEDIUM)

- Source: V3 R3-G4.
- Target: merged F-06 (new to the base), kept separate from F-01 per INV-021.
- Rationale: CAL holds MEDIUM; V2 conceded in Round 2 (D6).
- Integration point: findings, MEDIUM group.
- Recommendation text: put the full revised WC-16 text and the cadence difference from "Phase 1 sets no cadence" into the 7.3 decision file (TL:1156-1168); change the 7.4 completion gate to require owner approval of the text as well as the id (DESIGN:5, DESIGN:988, TL:2877, WORKER-CONTRACT.md:110). Relabel D6 `partial`.
- Check: the 7.4 gate text names approval of the rule text.
- Risk: Low. Interacts with Change 1 at 7.4 (TL:1165); apply both in the same item edit.

### Change 7: F-07 8.1 per-file PASS (MEDIUM)

- Source: V2 R2-G6.
- Target: merged F-07, at calibrated MEDIUM.
- Rationale: CAL holds MEDIUM.
- Integration point: findings, MEDIUM group.
- Recommendation text: in 8.1 (TL:1417-1421), check each of the six named gate files separately for existence and exactly one final PASS outcome; reject duplicates and contradictory outcomes.
- Check: six named PASS results.
- Risk: Low.

### Change 8: F-08 negative guard test and INF-013 row (MEDIUM)

- Source: V2 R2-G8; X-007.
- Target: merged F-08 and the merged INF-013 row.
- Rationale: C-008 (V2, 96%); X-007 (V3, 92%).
- Integration point: findings, MEDIUM group; row ledger, INF-013.
- Recommendation text: in 8.9 (TL:1467-1476), add a non-integration test that asserts the three guarded entry points raise AssertionError before any seam override; require its named PASS. Relabel row INF-013 "construction assigned; verification partial, see F-08".
- Check: the named test appears in 8.9 Verification.
- Risk: Low.

### Change 9: F-09 SP-28 rationale deliverable (MEDIUM)

- Source: V2 R2-G10.
- Target: merged F-09, with the either-or recommendation narrowed to one option.
- Rationale: C-009 (V2, 92%), CAL partly MEDIUM; qualitative Clarity C1 penalised the either-or.
- Integration point: findings, MEDIUM group.
- Recommendation text: add a byte-limit rationale deliverable to 14.9, recorded in the task package (DESIGN:987); 8.18 boundary tests (TL:1535-1539) do not close it.
- Check: 14.9 names the rationale file.
- Risk: Low.

### Change 10: F-10 HALT on a CHANGED anchor (LOW)

- Source: INV-017 (probe-sourced; no card holds it, not calibrated); A-007 (QUALIFY, unanimous); V1 R2 New Evidence 3.
- Target: merged F-10 (new finding).
- Rationale: A-007 (V3, 91%). Set to LOW, not INV-017's MEDIUM: item 1.3 (TL:224) already compares HEAD with `5dc29d23` and adds a re-check note, and item 1.4 (TL:229 to 234) already re-reads the anchors. The only gap is that neither item HALTs when an anchor status is CHANGED.
- Integration point: findings, LOW group.
- Recommendation text: one edit to item 1.4's Verification (TL:233): "If any row has status CHANGED, apply the HALT rule with a blocker_reason naming the anchor, instead of continuing."
- Check: item 1.4 Verification contains a HALT on CHANGED.
- Risk: Low.

### Change 11: F-11 5.5 pin greps (LOW)

- Source: V3 R3-G3.
- Target: merged F-11, citation corrected to TL:796.
- Rationale: CAL holds LOW; 40 of 40 V3 citations verified.
- Recommendation text: in 5.5 (TL:796, TL:827), grep for 'line 545', 'line 865', 'line 470', 'line 398' and 'line 624', expecting one hit each (DESIGN:677-680, 686).
- Integration point: findings, LOW group.
- Risk: Low.

### Change 12: F-12 FR-010 wording, all copies (LOW; fix scope set by INV-015 MEDIUM)

- Source: V3 R3-G1; V3 R2 New Evidence 2; INV-015, INV-016.
- Target: merged F-12 (new to the base). Register severity stays at calibrated LOW; INV-015 sets the fix scope.
- Rationale: C-003 (V3, 94%) and X-002 (V3, 94%): wording ambiguity, not a lost rule.
- Recommendation text: in item 2.2 (TL:249), change "Several matching rows" to "One or more matching rows". Apply the same change to the nine 2.8 to 2.16 scope notes (TL:293 to TL:349) and to research/04:90, or drop the "copied verbatim from research/04" claim at TL:251 (INV-015). Reword the R3-B2 opening at TL:425 ("Several scoped Dispatch rows can match") to "One or more" so a one-row reader is not sent to a several-row rule (INV-016; research/04:148 already covers one row).
- Check: a grep of "Several matching rows" over TL and research/04 returns 0 lines.
- Integration point: findings, LOW group.
- Risk: Low. Eleven small edits; a missed scope note makes a reviewer flag an unexplained R3-B1 change.

### Change 13: F-13 3.1 fallback pointer (LOW)

- Source: V3 R3-G2. Target: merged F-13, citation corrected to TL:425. Rationale: CAL holds LOW.
- Recommendation text: point the fallback at the observation rules (DESIGN:494-505, around line 505), or drop the parenthesis. Apply with Change 12 (same line).
- Integration point: findings, LOW group. Risk: Low.

### Change 14: F-14 11.1 cadence (LOW)

- Source: V3 R3-G5. Target: merged F-14. Rationale: C-012 (V3, 95%).
- Recommendation text: add "at most once every 5 minutes" to the 11.1 Triggers wording (TL:1952), matching TL:773, TL:787 and TL:2258.
- Integration point: findings, LOW group. Risk: Low.

### Change 15: F-15 13.6 CHANGELOG bullet (LOW)

- Source: V3 R3-G6. Target: merged F-15. Rationale: C-013 (V3, 96%).
- Recommendation text: drop the tests/sweep/ and test_sweep_command.py bullet from 13.6 (TL:2293), matching routing row R8 (DESIGN:701).
- Integration point: findings, LOW group. Risk: Low.

### Change 16: F-16 lint-architecture in 8.3 (LOW)

- Source: V3 R3-G8. Target: merged F-16. Rationale: C-014 (V3, 96%).
- Recommendation text: add `make lint-architecture` to 8.3 Verification (TL:1430), expected exit 0 (contracts `__init__.py:1-6`, `:35-36`, `:302-313`).
- Integration point: findings, LOW group; same item as Change 2. Risk: Low.

### Change 17: F-17 8.8 fake seam (LOW, preference)

- Source: V3 R3-G7. Target: merged F-17, class changed from `missing-reuse` to a test-design preference (X-012). Rationale: CAL partly LOW; conftest.py:59-74 also replaces the whole `_git`.
- Recommendation text: in 8.8 (TL:1467), have the fake `patch_git` record the argv and env it receives rather than rebuild them; optionally build them in a pure helper with its own unit test.
- Integration point: findings, LOW group. Risk: Low.

### Change 18: F-18 14.5 scoped diff (LOW)

- Source: V1 R1-G6, count part only. Target: merged F-18. Rationale: CAL partly LOW; the pipx clause is dropped (X-006).
- Recommendation text: in 14.5 Verification (TL:2470), also run `git diff` on the five folders and confirm no added line contains `src/superclaude` (DESIGN:939).
- Integration point: findings, LOW group. Risk: Low.

### Change 19: F-19 name the M2 route (LOW)

- Source: V1 R1-G1, partly. Target: merged F-19, target corrected to open item 3. Rationale: X-005 (V1, 73%): DESIGN:971 is open item 3 and already routes to the owner; only the TL naming is missing.
- Recommendation text: in 7.17 (TL:1265), add one line: if the run-current plain output (TL:1258) is not parseable, DESIGN open item 3 applies and the allowlist change goes to the owner as M2 (DESIGN:874, DESIGN:971).
- Integration point: findings, LOW group. Risk: Low.

### Change 20: F-20 per-item content checks (LOW)

- Source: V2 R2-G4, partly. Target: merged F-20, citation corrected to TL:1634, severity MEDIUM to LOW.
- Recommendation text: in 8.6 (TL:1453-1456) and 9.2 (TL:1634), replace total insertion counts with checks for the exact new content and placement, and make Verification and the completion gate agree.
- Integration point: findings, LOW group. Risk: Low.

### Change 21: F-21 FR and NFR ids on delivery items (LOW)

- Source: V1 R1-G2, partly. Target: merged F-21. Rationale: C-004 (V1, 65%).
- Recommendation text: add "(FR-023)", "(NFR-003)", "(FR-025)", "(FR-002)", "(NFR-014)" to the Context lines of 12.1, 8.10, 8.6 and the 10.x items (TL:1784, TL:2677; DESIGN:777, DESIGN:783). No new QA item.
- Integration point: findings, LOW group. Risk: Low.

### Change 22: F-22 commit grouping line (LOW)

- Source: V1 R1-G4, partly. Target: merged F-22. Rationale: C-010 (V1, 91%).
- Recommendation text: in the 14.46 Action (TL:2754), add "Commit R1, R2 and R3 (items 13.1, 13.2, 13.4) together; 13.4 goes with 13.2" (DESIGN:705, DESIGN:932, TL:2254).
- Integration point: findings, LOW group. Risk: Low.

### Change 23: F-23 B2 matrix row (LOW)

- Source: V2 R2-G9, matrix row part only. Target: merged F-23, severity MEDIUM to LOW. Rationale: X-004 (V1, 95%): DESIGN:216 says the NFR-004 import test enforces B2, so the "import check insufficient" part is a design question, not a TL gap.
- Recommendation text: add a B2 row to coverage-matrix.yaml (near :232-237 and :849-880) mapped to NFR-004 and TL:1784-1785 (DESIGN:215-219).
- Integration point: findings, LOW group. Risk: Low.

### Change 24: incorporate the V1 row ledger

- Source: V1 `row_verdicts` (76 rows: FR-001 to FR-026, NFR-001 to NFR-015, step rows).
- Target: merged `row_verdicts`, added beside V2's 51 rows; de-duplicate by row id, V2 verdict kept on overlap.
- Rationale: S-001 (V1, 97%); RC 0.503 is the widest coverage.
- Integration point: merged `row_verdicts`.
- Corrections on merge: the 2.16 row describes a QA lens, not an edit (X-003, TL:347); no row may say `pipx run` "installs nothing" (X-006, TL:2488); X-011 keeps V1's `partial` for the capture-run row (TL:263 is a DESIGN edit).
- Risk: Low. Row ids overlap across cards; de-duplicate before counting.

### Change 25: incorporate the V3 design-fix rows

- Source: V3 `row_verdicts` (24 rows, phases 2 to 6).
- Target: merged `row_verdicts`.
- Rationale: S-002 (tie, 94%): the only coverage of the design-fix slice.
- Integration point: merged `row_verdicts`.
- Corrections on merge: keep V2's INF-005 and INF-014 delivery verdicts over V3's false-match verdicts (X-010); the R3-B1 FR-010 row reads "ambiguous after edit 4, see F-12" (V3 R2); D6 reads `partial` (Change 6). Delegated (`covered-in-substance`) rows carry the A-001 caveat: valid only if the row survives the Phase 2 to 6 edits.
- Risk: Low.

## Base Weaknesses (V2)

| Issue | Better Variant | Fix |
|---|---|---|
| Severity inflation: 7 self HIGH, 3 calibrated (X-008) | CAL, all advocates | Every merged entry uses calibrated severity (Changes 5, 7, 8, 20, 23) |
| R2-G2 `gate-bypass` class contradicted by its own CAL | CAL | Folded into F-01 as an evidence-condition defect (Change 1) |
| R2-G7 fix names only 6.2, TL:1140 and 14.7 | Probe (INV-001, INV-002) | All nine sites plus 7.15 (Change 1) |
| R2-G3 fix edits 7.16 only | Probe (INV-009) | Allow the two step (6) discovery commands in all four texts together (Change 3) |
| R2-G5 fix names no pattern | Probe (INV-013) | Stated declaration pattern (Change 2) |
| INF-013 row `covered` against R2-G8 (X-007) | V3 | Relabel (Change 8) |
| R2-G4 cite off by two lines | CAL | TL:1634 (Change 20) |
| Either-or recommendations (R2-G9, R2-G10) | V1 style | One option each (Changes 9, 23) |
| 51 rows only (RC 0.338); no design-fix slice | V1, V3 | Changes 24, 25 |
| Misses R1-G3 and R3-G4 | V1, V3 | Changes 4, 6 |
| No deviation category (S-008) | none | Shared by all; not fixed here |

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale |
|---|---|---|
| R1-G5 | V1 confirmation that order matches the SPEC column (DESIGN:907-912, TL:1416) | Confirmation, no change (C-011 tie, S-007) |
| R3-G9 | V3 positive check on publish precedents (recovery.py:424-434, atomic.py:22-38, config.py:64-78) | Confirmation, no change (S-007) |
| R3-G10 | V3 says the owner gate is sound (TL:764-806, TL:843, TL:987, TL:1003) | Refuted by TL:982 and TL:989 (X-001, 99%); V3 conceded |
| R1-G6 pipx clause | "pipx run ... installs nothing"; label 1.29 "pipx run, not install" (TL:2474) | False: TL:2488 shows `pipx run --spec` installs runtime dependencies (X-006, 98%) |
| R1-G1 target and owner-route claim | HALT naming "open item 2"; "no owner step" | DESIGN:971 is open item 3 and its behaviour-until-closed routes to the owner (X-005, 73%); only the naming survives (Change 19) |
| R2-G9 import-check part | Add a path-as-data acceptance check to 8.4 and 8.12 | DESIGN:216 asserts the NFR-004 import test enforces B2; this critiques DESIGN, not TL (X-004, 95%) |
| R2-G2 label and severity | `gate-bypass`, HIGH | CAL MEDIUM and not a bypass (X-008); substance merged into F-01 |
| R2-G1, R2-G6, R2-G8 self HIGH | HIGH | CAL MEDIUM (X-008); kept at MEDIUM (Changes 5, 7, 8) |
| R3-G7 class | `missing-reuse` | conftest.py:59-74 also replaces the whole `_git`; a preference only (X-012, 96%) |
| R3-G1 "rule lost" | MEDIUM, transcript rule removed from DESIGN 7.2 | research/04:148 closing clause covers one row; wording only, LOW (X-002, C-003) |
| V3 INF-005, INF-014 | false-match with no gap entry | V2 finds real delivery for both (X-010, 95%) |
| V1 2.16 row | 2.16 is an edit | TL:347: 2.16 is a SPEC-fidelity QA lens (X-003, 98%) |
| R1-G2 new QA item | F4's final grep item | Duplicates the 14.11 and 14.35 lenses; R1-G2 itself rejects it |
| S-008 | Add the Aligned, Refinement, Drift, Regression category | No variant has it; outside the merge of these cards |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | One missed site keeps 7.13 and every later item blocked | Re-grep "PENDING or"; restore V2 R2-G7 text and re-apply per site |
| 2 | Low | A correct `models.py` fails 8.3 | Revert to V2 R2-G5 text |
| 3 | Medium | One of the four texts is missed, so a correct probe run fails TL:1260 or the 7.24 lens | Re-apply the allowance to all four texts (TL:1248, TL:1257-1258, TL:1260, TL:1314) |
| 4 | Low | False BLOCKING "missing test" in 14.11 | Revert entry |
| 5 | Low | Counts cited from the wrong source | Revert entry |
| 6 | Low | 7.4 passes on an id alone | Revert entry |
| 7 | Low | 8.1 passes with a missing PASS | Revert entry |
| 8 | Low | Guard regression goes unseen | Revert entry and row label |
| 9 | Low | SP-28 open at release | Revert entry |
| 10 | Low | A CHANGED anchor is recorded but Phase 1 continues | Drop entry |
| 11 | Low | 5.5 check passes without testing | Revert entry |
| 12 | Low | Reviewer flags an unexplained R3-B1 change | Revert entry |
| 13 | Low | Reader sent to the wrong rule | Revert entry |
| 14 | Low | Docs contradict WC-16 | Revert entry |
| 15 | Low | Unrouted CHANGELOG bullet | Revert entry |
| 16 | Low | B5 redefinition unchecked | Revert entry |
| 17 | Low | Fake copies logic it should test | Drop entry |
| 18 | Low | Moved hit unseen | Revert entry |
| 19 | Low | Owner route not visible in TL | Drop entry |
| 20 | Low | Correct work rejected on a dirty file | Revert entry |
| 21 | Low | Traceability by id only | Drop entry |
| 22 | Low | Split commit fails the parity test | Drop entry |
| 23 | Low | B2 untraced in the matrix | Drop entry |
| 24 | Low | Duplicate or contradictory rows | Re-run de-duplication by row id |
| 25 | Low | False-match verdicts re-enter | Re-apply X-010 correction |

## Revision log: review 1

| ID | Finding | What changed |
|---|---|---|
| B-1 | F-03 / Change 3: the preferred "literal file read" option cannot list the tab-map folder | Dropped the either-or. Change 3 now allows exactly the two step (6) discovery commands (`echo` of the tab-map path, `ls -la` of that path) and edits TL:1248, TL:1257, TL:1258, TL:1260 and the 7.24 lens (TL:1314) together. New check: a grep for `ls` or `echo` in command records finds only those two. F-03 row, Base Weaknesses row and Risk row 3 updated to match. |
| B-2 | F-10 / Change 10: copied INV-017's false claim that item 1.3 does not compare HEAD; uncalibrated MEDIUM | F-10 set to LOW and labelled probe-sourced (INV-017, no card holds it, not calibrated). Gap restated as "nothing HALTs when item 1.4 records an anchor as CHANGED". The HEAD-compare and re-run text is deleted; the fix is one HALT sentence in item 1.4 Verification (TL:233). Register counts now HIGH 3, MEDIUM 6, LOW 14; Risk row 10 updated. |

## Review Status

- Approval: auto-approved
- Timestamp: 2026-11-08T11:20:00Z
