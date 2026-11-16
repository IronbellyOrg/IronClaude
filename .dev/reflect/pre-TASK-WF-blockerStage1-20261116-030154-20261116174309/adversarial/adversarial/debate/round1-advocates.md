# Round 1: advocate statements (parallel)

Persisted by the orchestrator in condensed form: arguments, evidence and every per-point row and A-NNN answer are kept; prose steelmen are shortened. Advocates: A1 = Variant 1 (general-purpose agent, sonnet), A2 = Variant 2 (haiku), A3 = Variant 3 (opus). Each verified claims against the live plan, spec and code with read-only reads and greps.

## A1 (Variant 1) position
V1's one blocking finding (Task 7 grep lists `.pyc`) is real and live-confirmed (`grep -rln "ledger" src/superclaude/cli/review` lists 10 `.pyc`; `PYTHONDONTWRITEBYTECODE` unset; `grep -rln --include='*.py' "follow_ups" ...` prints nothing today). V1's 5 non-blocking findings hold. V1 missed C-007 and C-008 (SPEC:501, 512, 516 versus PLAN:159) but V2 over-graded them. Concessions: R1-F2 fix "MAJOR=Blocking" collapses a conditional (V3's UNSET-for-conditional is better); header sentence contradicts F1/F5 lines (X-003); `verify` left as a nit inside F8.
Steelman of V2: only card reading SPEC 7.2 "Needs from code" against Task 10; PLAN:94 will document an input that no code supplies.
Criticism: V2's C-007/C-008 have no stage 1 consequence: M never enabled for BLOCKING (stage1 request line 7, REQ-22), exit tests T6/T11/T12 do not need the presence check, SPEC:501 supplies basis only "when code can supply it", SPEC:615 item 3 is a stage 2 duty; R2-F4 grades the review's own matrix.

## A2 (Variant 2) position
Retains C-007 BLOCKING (a supplied list is not a completed mechanical presence check; a deliverable can have the list and already contain the item, and the PLAN:164/177 tests let M be asked without the precheck) and C-008 BLOCKING for the missing D-input path (PLAN:159 names exactly three supplier outputs, none a decision basis, yet "S, W and D always"; Tasks 9, 11, 12 do not close it), but qualifies runtime Q support as deferrable. Concessions: C-008 bundles two claims; C-011 overstated (COVER header already says degraded); X-004 not a demonstrated contradiction; bytecode finding conditional on ordinary cache-producing execution; missed C-002..C-005, C-009, C-010. Criticism of V1: conditional-label fix unsafe; both opponents leave the SPEC:512/516 versus PLAN:159/164 contradiction unaddressed.

## A3 (Variant 3) position
R3-F1 correct and confirmed on disk (`grep -rl "verify_cmd"` lists both `verify_cmd` `.pyc`; no bytecode switch-off in pyproject, Makefile or conftests; `.gitignore:2`). R3-F3 checked across all four stage plans (grep rc=1). Concessions: missed C-007, C-008, C-009, the multi-path separator, "fixed" label for F5; R3-F5 fix (subprocess) less consistent than load-by-path. Criticism: V2 overgrades C-007/C-008 because stage 1 builds only FixtureJudge and ReviewerJudge (PLAN:146), excludes Jev/LLM judges (PLAN:22), the classifier has no authority, no exit test covers the inputs (SPEC:945) and no judge in stages 1 and 2 reads them (stage 2 plan line 26): real weakness, missing input, no wrong result. V1 calls the Task 1 gate "correct" but the halt comes after SKILL.md is written.

## Per-point positions (correct grade of the underlying finding; confidence)

| Point | A1 | A2 | A3 | Agreement |
|---|---|---|---|---|
| S-001 | NOT-A-DEFECT 90 | NOT-A-DEFECT 99 | NOT-A-DEFECT 70 | unanimous |
| S-002 | NOT-A-DEFECT 70 | NOT-A-DEFECT 92 | NOT-A-DEFECT 75 | unanimous |
| C-001 | BLOCKING 88 | BLOCKING 97 | BLOCKING 92 | unanimous (winner V1/V3 tie) |
| C-002 | NON-BLOCKING 70 | NON-BLOCKING 89 | NON-BLOCKING 80 | unanimous (V3/V1) |
| C-003 | NON-BLOCKING 65 | NON-BLOCKING 84 | NON-BLOCKING 65 | unanimous |
| C-004 | NON-BLOCKING 72 | NON-BLOCKING 94 | NON-BLOCKING 75 | unanimous |
| C-005 | NON-BLOCKING 75 | NON-BLOCKING 92 | NON-BLOCKING 75 | unanimous |
| C-006 | NON-BLOCKING 92 | NON-BLOCKING 99 | NON-BLOCKING 90 | unanimous |
| C-007 | NON-BLOCKING 55 | BLOCKING 95 | NON-BLOCKING 65 | majority NON-BLOCKING (2 of 3); V2 superior treatment |
| C-008 | NON-BLOCKING 62 | BLOCKING 90 | NON-BLOCKING 65 | majority NON-BLOCKING (2 of 3); V2 superior treatment |
| C-009 | NON-BLOCKING 65 | NON-BLOCKING 88 | NON-BLOCKING 70 | unanimous (V1) |
| C-010 | NON-BLOCKING 55 | NON-BLOCKING 90 | NON-BLOCKING 60 | unanimous (V3) |
| C-011 | NOT-A-DEFECT of the plan 75 | NON-BLOCKING 87 | NOT-A-DEFECT of the plan 70 | majority NOT-A-DEFECT of the plan |
| C-012 | NON-BLOCKING 80 | NON-BLOCKING 97 | NON-BLOCKING 85 | unanimous (V3) |
| X-001 | NON-BLOCKING 55 | NON-BLOCKING 90 | NON-BLOCKING 60 | unanimous (V3) |
| X-002 | NON-BLOCKING 70 | NON-BLOCKING 92 | NON-BLOCKING 75 | unanimous (V1 label "partly fixed" accurate) |
| X-003 | NON-BLOCKING (card wording) 70 | NON-BLOCKING 88 | NOT-A-DEFECT of the plan 80 | majority: card wording only, not a plan finding |
| X-004 | NOT-A-DEFECT 70 | NOT-A-DEFECT 96 | NOT-A-DEFECT 70 | unanimous |

## Shared assumptions

| A | A1 | A2 | A3 |
|---|---|---|---|
| A-001 | ACCEPT (live grep lists 10 `.pyc` for "ledger") | ACCEPT (inclusion mechanism shown) | ACCEPT (`verify_cmd` and "ledger" `.pyc` listed) |
| A-002 | ACCEPT (variable unset, pycache present, pytest before grep) | QUALIFY ("always fails" too absolute; `-B` or other arrangements possible) | ACCEPT (no switch-off in repo; pytest-9.2.0 pycs show writes) |
| A-003 | ACCEPT (precedent: first-review F1 graded blocking) | ACCEPT | ACCEPT |
| A-004 | QUALIFY (supplier claim holds M to its row; D limited by "when code can supply it"; neither reaches exit tests, so non-blocking) | QUALIFY (once PLAN:159/164 define the supplier, SPEC:512/516 apply; Q runtime may be deferred explicitly) | QUALIFY (in scope, gaps real, but no stage 1/2 judge consumes them: non-blocking; fix is to add the inputs or defer explicitly) |

No omissions flagged: every advocate answered A-001 to A-004.

## Round 1 convergence (agreement on the correct grade)
18 of 22 points settled by unanimity or majority at the grade level; open contests: C-007 and C-008 (grade 2 to 1), A-004 (all QUALIFY, grade of the underlying C-007/C-008 contested), and A-002 (2 ACCEPT, 1 QUALIFY). Round 2 targets: C-007, C-008, A-004, A-002, C-011, X-003 and the Task 1 ordering (C-010/X-001).
