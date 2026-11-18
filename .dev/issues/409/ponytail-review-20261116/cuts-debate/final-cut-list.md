<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (sonnet:qa) -->
<!-- Merge date: 2026-11-16 -->

# Final cut list for the Orca observer (issue 409)

<!-- Source: Base (original, modified) - intro framing from Variant B header; survival rule from refactor-plan.md "Decision rules" item 3 -->
Date 2026-11-16, branch 409-Phase2, worktree /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp. This list is read-only output of a quick-depth /sc:adversarial debate of 3 variants (Variant A opus:architect, Variant B sonnet:qa, Variant C opus:analyzer) and 3 Round 1 advocates (`adversarial/round1-advocate-1.md`, `-2.md`, `-3.md`). Nothing here has been executed.

Survival rule: an item survives (EXECUTE-NOW) only when its final verdict is CUT or CUT-SMALLER, its confidence is at least 70 percent, and no unresolved factual contradiction remains. KEEP and sub-70 items are NOT-NOW; DEFER-OWNER items are OWNER-NEEDED.

<!-- Source: refactor-plan.md "Counts" (Change 2); figures from debate-transcript.md Convergence Assessment -->
## Counts
- Items: 39 (R1-R10, T1-T10, S1-S6, D1-D13). The brief said 36; the ID list adds to 39.
- Final verdict: CUT 0, CUT-SMALLER 15, DEFER-OWNER 9, KEEP 15, REJECTED 0 (rejected sub-parts are listed inside rows).
- Execution class: EXECUTE-NOW 11, OWNER-NEEDED 9, NOT-NOW 19.
- Convergence 0.934 (57 of 61 diff points), status CONVERGED, depth quick.

<!-- Source: Base (original) table skeleton, columns replaced per Change 1; row content from debate-transcript.md Scoring Matrix and round1-advocate-1/2/3.md per-point matrices -->
## Final row table

| ID | Final verdict | Exact scope if narrowed | Surviving guard | Conf % | Execution class |
|---|---|---|---|---|---|
| R1 | CUT-SMALLER | Production: terminal.py:41-53 (`PALETTE`, `_FORBIDDEN_ATTRS`), :161-172 (`palette_style`), glyphs `sep` (:33), `vrule` (:37), `cross` (:38), `TerminalPolicy.box_style` (:72-74), and the imports that become unused (`Style`, `box`; `field` at commands.py:14). adapter.py:65-82 `CODES` deleted (not moved) and the comment at :340 reworded (V2 dissents: would keep `CODES`). parse.py:723-733 `Fixture.parse`. questions.py:70-76 `closure_evidence`, `never_read`, and `CLOSURE_EVIDENCE` (:25). commands.py:142 `Deps.extra`. collector.py `question_fixture` argument, state and replay (:97, :102-104, :134-140); keep `read_questions` as a 2-line stub returning FAILED `no-question-fixture` (the CycleSource protocol needs it). Tests: delete test_terminal.py:56-59 and :73-82 (not :65-70, see T9); edit :126 (drop the `box_style` assert), :132-133 (use `selected`), and the `box` and `palette_style` imports; delete test_adapter.py:719; test_collector.py keep :662-666, delete :667-678; rewrite test_fixtures.py:44 and :139-151 through `parse_page` + `apply_frozen`; edit only test_questions.py:46, :52, :98. | No-blink: test_render.py:182-190. `--fixture` with `--questions` refused: commands.py:177-178. ASCII boxes: `safe_box` test test_terminal.py:142-149. Closure wording: view.py:65 and :693 pins. T34 frozen marker: the rewritten test. Exact code check: test_adapter.py:718. | 80 | EXECUTE-NOW |
| R2 | CUT-SMALLER | Delete `QuestionsPanel.count_text` (view.py:209) and its assignment (:732); drop `open_text` only if it becomes unused. Keep the other 21 fields; no comment edits. | T19/T54 panel tests (test_question_cap.py:71-134); T47 golden (questions off); export reads `open_total`, `window_full`, `retained`, `evicted` (export.py:165-168). | 80 | EXECUTE-NOW |
| R3 | CUT-SMALLER | Delete `ParsedPage.unrecognised_keys` (parse.py:177) and its sum (:409); `Coverage.unrecognised_keys` (:195) and its sum (:647). Keep `_FIELDS`, `_KNOWN`, `_count_unexpected`, `_BLOCK_FIELDS` (:91-93, sanitizer block mode), the row count (:155, :356) and the inspector line (view.py:407). | test_parse.py:188, :198; test_fixtures.py:145, :166; test_view.py:722. | 75 | EXECUTE-NOW |
| R4 | KEEP | none. The "clip, e exports all" option is unsound (the `e` record lacks the inspector fields, export.py:65-80). | test_inspector_scroll.py (7 tests); issue AC 5 (full identifiers in selected detail). Owner note: rendering-rules.md:13 and extract-prd-ux.md:106 say "no per-panel scrolling" and the built feature contradicts them. | 72 | NOT-NOW |
| R5 | KEEP | none | T47 golden `lines_<w>x<h>` and `printed_<w>` at 160/116/80 (release1_surface.py:25-60) | 80 | NOT-NOW |
| R6 | KEEP | none | T35 (test_render.py:196 on) and the T47 golden; a plain wrap changes bytes | 75 | NOT-NOW |
| R7 | KEEP | none | about 15 lines saved against about 90 test references | 80 | NOT-NOW |
| R8 | KEEP | none; stale comment and help text are fixed under D2 | test_commands.py:743-745 (True only with a cited owner record); release-gates.md:12 | 85 | NOT-NOW |
| R9 | KEEP | none now; precondition for any future attempt: add question-path tests for `RunnerFailure("output-cap")`, `OSError` and budget-limited overrun | test_adapter.py:724-734 is the only question-path error test | 70 | NOT-NOW |
| R10 | KEEP | none | test_questions.py:118-135 (T46 bound, evicted counted once); fix 2083db2ae | 90 | NOT-NOW |
| T1 | KEEP | none | test_render.py:616-629 (T47); golden cannot be regenerated from current code (release1_surface.py:3-7) | 80 | NOT-NOW |
| T2 | CUT-SMALLER | test_golden_contract.py:333-365 only (tests at :333, :342, :348). Keep :282, :566, :596; the recorder scripts stay (their fate is an owner question). V1 would also cut :596-638; V3 and V2 would keep it. | redaction tests :282-331, :566-594, :596-638; leak scans :206-216, :508-527 | 65 | NOT-NOW (confidence under 70; exact scope split) |
| T3 | KEEP | none | test_keys_spike.py:133-151 and :208-222 back the written spike criteria (ARCHITECTURE-SPINE.md:154); :153-178 and :180-206 are the terminal-restore tests (binding rule 1) | 72 | NOT-NOW |
| T4 | CUT-SMALLER | test_fixtures.py:258-278 and :291-297 only. :226-230 is contested (2 of 3 would cut). | :81-134 (AC 6 shapes), :232-256 (T37), :280-288 (`make_rows` for T16), :208-223, :310-324 | 65 | NOT-NOW (confidence under 70) |
| T5 | CUT-SMALLER | test_question_quiet_scope.py:192-203 only (the tests of the fake mailbox itself). Not cut: :148-171 (2 of 3 advocates would cut it; orchestrator keeps it, see override a). | :137-145, :148-171, :174-179, :182-189; the fake asserts the exact argv on every call (:68-76); forbidden-prefix and argv tests in test_adapter.py (:158-192) | 70 | EXECUTE-NOW |
| T6 | CUT-SMALLER | test_export.py:238-244 and test_collector.py:414-421 only. test_view.py:864-869 stays: the only check that export.py and render.py do not import `observe.parse`. Keep test_adapter.py:158-192 and :585-589, test_terminal.py:214-231, test_commands.py:578-594. | the kept tests; T40 fake-clock behaviour tests | 68 | NOT-NOW (confidence under 70) |
| T7 | CUT-SMALLER | test_golden_contract.py:214-215 and :518-519 (the duplicated SENSITIVE loops) only. Keep :213 and :517 (`isascii`), :216 (32-character rule), :520 (Run, terminal and message id rule), :521-527. Drop the `SENSITIVE` import there only if it becomes unused. | test_fixtures.py:185-191 runs the same scan over every packaged fixture, goldens included (`fixture_files()` :25-30) | 75 | EXECUTE-NOW |
| T8 | CUT-SMALLER | test_render.py:95-100: replace the assertion that ends in `or True` with `assert len(overflow) == 1`; keep all 27 cases. Run it; a failure is a finding to report, not a reason to loosen. | T16 (acceptance-tests.md:28), issue AC 6 | 89 | EXECUTE-NOW |
| T9 | CUT-SMALLER | Delete test_terminal.py:65-70 (the decorator and `test_no_blink_code_in_any_console_output`, with the T28 header at :62) in the same change as R1; keep test_render.py:182-190. The proposed target (the test_render copy) is REJECTED. | test_render.py:182-190 (AC 5 no blinking, real screen, every width, both colour modes) | 70 | EXECUTE-NOW |
| T10 | KEEP | none | test_snapshot_schema.py:80-92 and :297-327 (redaction per variant); test_collector.py:372 runs 8 variants, not 10 | 75 | NOT-NOW |
| S1 | DEFER-OWNER | none until answered | if kept: test_snapshot_schema.py:448-558 (no subject, body, handle or payload); additive-only rule (snapshot.schema.json:4) | 70 | OWNER-NEEDED (question Q1) |
| S2 | CUT-SMALLER | export.py:14 (`resources` import), :18 (`Draft7Validator` import), :24-25 (`SCHEMA_PACKAGE`, `SCHEMA_FILE`), :29-34 (schema load and `check_schema`). Keep :23 `SCHEMA_VERSION` (used at :195). Define `SCHEMA` in tests/observe/conftest.py (read the schema file, run `Draft7Validator.check_schema`); update imports at test_commands.py:34 and test_snapshot_schema.py:15. After the move, test_snapshot_schema.py:60 compares the file with itself; keep :61-62 and the closed-object checks. | test_snapshot_schema.py:54-72 (draft 7, closed producer side) | 77 | EXECUTE-NOW |
| S3 | KEEP | none | the files are not byte duplicates (5,069 vs 8,271 bytes); the pointer target `.dev/issues/409/tuibbs-review/` is untracked | 88 | NOT-NOW |
| S4 | KEEP | none | T47 golden holds `changedDuringRead` and `duplicatesIgnored` 5 times each; both are on screen (view.py:513-514, :905); additive-only rule | 85 | NOT-NOW |
| S5 | DEFER-OWNER | none until answered | `write_snapshots=live or bool(options.snapshot)` (commands.py:369) and its tests stay | 75 | OWNER-NEEDED (question Q2) |
| S6 | KEEP | none | the proposed Ordering text is false (view.py:842, export.py:207); the Options table is the only tracked record behind owner decision 2 | 74 | NOT-NOW |
| D1 | CUT-SMALLER | In place only: mark open decision 6 (permission to read the question scope) and decision 8 (what identifies a human question) as decided by `.dev/issues/409/owner-decisions-20261111.md` in SPEC.md:104 and :106 and owner-decisions-and-risks.md:22 and :24; check prd.md:423 and :469 and fix the same rows if they still read open. No collapse of the lists, no pointer in place of prd.md 12.1 (the OQ-n labels exist only there). Decision 5 (fallback date) stays open. | owner-decisions-20261111.md; "open owner decision N" numbering and OQ-n labels keep resolving | 70 (median 65 plus 5 for the orchestrator read) | EXECUTE-NOW |
| D2 | CUT-SMALLER | QUESTION-OBSERVATION status lines only, citing `.dev/issues/409/owner-pass-record-20261112.md`: prd.md:106 and :491; unverified-register.md:27; adapter-contract.md:3 and :62; rendering-rules.md:89; commands.py:63-66 comment, :86-88 HELP text and :452-453 `--questions` help. Do not touch `QUESTION_GATE_TEXT` (commands.py:68-70, pinned by test_commands.py:632), any DIRECTION-SELECTED line, or the untracked handoff-mvp-brainstorm.md. | owner-pass-record-20261112.md; release-gates.md:12 and :38 already correct | 77 | EXECUTE-NOW |
| D3 | DEFER-OWNER | none until answered | git history (36 tracked files) | 75 | OWNER-NEEDED (Q3) |
| D4 | DEFER-OWNER | none until answered; no deletion of any untracked file | `.dev/brainstorms/20261108-132433-orca-observer-mvp/` is untracked (rule 3) | 85 | OWNER-NEEDED (Q4) |
| D5 | DEFER-OWNER | none until answered | the two ARCHITECTURE-SPINE.md copies are byte-identical (54,129 bytes); both tracked | 75 | OWNER-NEEDED (Q5) |
| D6 | DEFER-OWNER | none until answered | both UX folders tracked; `ux-orca-observer` is current | 80 | OWNER-NEEDED (Q6) |
| D7 | DEFER-OWNER | none until answered | all files tracked | 75 | OWNER-NEEDED (Q7) |
| D8 | CUT-SMALLER | unverified-register.md row :52 ("What identifies a human question", decided 2026-11-11) only | owner-decisions-20261111.md decision 8 | 52 | NOT-NOW (confidence under 70) |
| D9 | DEFER-OWNER | none until answered | handoff-step1..5.md tracked; handoff-mvp-brainstorm.md untracked | 75 | OWNER-NEEDED (Q8) |
| D10 | KEEP | none | the owner's quoted words; release-gates.md:38 | 75 | NOT-NOW |
| D11 | KEEP | none | issue AC 11 (issue-body.md:85); attachment-status.json says the zip upload did not happen, so the committed zip is the delivery | 85 | NOT-NOW |
| D12 | DEFER-OWNER | none until answered; an agent must not write the record | issue AC 1 (issue-body.md:75); release-gates.md:22 | 90 | OWNER-NEEDED (Q9) |
| D13 | CUT-SMALLER | acceptance-tests.md: add the snapshot schema test id (tests/observe/test_snapshot_schema.py); mark T7, T17, T45 and T50 "not built / no automated test" with the reason (T7 cannot run as written: commands.py:177-178 refuses `--questions` with `--fixture`); strike nothing | rows T45 (OQ-13) and T50 (AC-S) keep their references | 70 | EXECUTE-NOW |

<!-- Per-row sources (V1 = Variant A opus:architect = round1-advocate-1; V2 = Variant B sonnet:qa = round1-advocate-2; V3 = Variant C opus:analyzer = round1-advocate-3)
R1: round1-advocate-1 + round1-advocate-3 (CODES deleted with test_adapter.py:719); round1-advocate-2 (read_questions stub); symbol-level edit list from Variant A (opus:architect)
R2: round1-advocate-1 + round1-advocate-3
R3: round1-advocate-3 (Variant C (opus:analyzer))
R4: round1-advocate-1 + round1-advocate-3
R5, R6, R7, R8, R10: round1-advocate-1 + round1-advocate-2 + round1-advocate-3 (unanimous)
R9: round1-advocate-1 + round1-advocate-2
T1: unanimous (round1-advocate-1/2/3)
T2: intersection of round1-advocate-1 and round1-advocate-3 scopes; round1-advocate-2 defers
T3: round1-advocate-1 + round1-advocate-3
T4: round1-advocate-1 + round1-advocate-3
T5: round1-advocate-1 (+ round1-advocate-3 concession), narrowed by orchestrator override (a)
T6: synthesis of round1-advocate-1/2/3, narrowed by orchestrator override (b)
T7: round1-advocate-2 (Base (original))
T8: unanimous (round1-advocate-1/2/3)
T9: round1-advocate-1 + round1-advocate-3
T10: unanimous (round1-advocate-1/2/3)
S1: round1-advocate-1 + round1-advocate-2
S2: round1-advocate-3 (Variant C (opus:analyzer))
S3: round1-advocate-1 + round1-advocate-2
S4, S5: unanimous (round1-advocate-1/2/3)
S6: round1-advocate-2 + round1-advocate-3
D1: round1-advocate-2, confidence raised by orchestrator override (c)
D2: union of round1-advocate-1/2/3 stale spots
D3, D5, D7: unanimous (round1-advocate-1/2/3)
D4, D6, D9: round1-advocate-1 + round1-advocate-3
D8: round1-advocate-2 + round1-advocate-3
D10, D11, D12, D13: unanimous (round1-advocate-1/2/3)
-->

<!-- Source: refactor-plan.md Change 3; round1-advocate-2 Extra 7 (cut ordering); round1-advocate-3 A-001 (pytest and ruff after each cut); Variant A and Variant C file groupings -->
## Execution sequence (EXECUTE-NOW only)
Gate after every step: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` (694 passed minus the tests deliberately removed, counted in the step) and `uv run ruff check src/superclaude/cli/observe tests/observe`. Re-grep every target right before editing (other sessions share the worktree; HEAD f104ca51a when checked). None of these steps touches the sanitizer, the argv allow-list, process-group kill, terminal restore, snapshot redaction or the disclosure label.
1. R1 + T9 (one change): terminal.py, adapter.py, parse.py (:723-733), questions.py, commands.py (:14, :142), collector.py, and tests test_terminal.py, test_adapter.py, test_collector.py, test_fixtures.py, test_questions.py.
2. R3 + R2: parse.py aggregate counters (after step 1 touched parse.py), view.py `count_text`.
3. S2: export.py, tests/observe/conftest.py, test_commands.py:34, test_snapshot_schema.py:15.
4. Test-only: T8 (test_render.py), T5 (test_question_quiet_scope.py:192-203), T7 (test_golden_contract.py).
5. Text and help: D2 (documents plus commands.py comment and help; run test_commands.py), D1, D13 (documents).
Staging note: `.dev/tasks/` stays staged as usual; nothing in this list stages `.claude/` paths.

<!-- Source: refactor-plan.md Change 4; OWNER-NEEDED rows of Variant A, Variant B and Variant C; Q10 and Q11 are extra questions the debate found (Base (original) Extra-findings idea) -->
## Questions for the owner
- Q1 (S1): May the R2 `questions` group be withdrawn from snapshot.json? Your 2026-11-08 "versioned, additive-only" rule makes that a schemaVersion 2 change. Recommendation: keep it.
- Q2 (S5): UX-OQ-4: should live mode write the snapshot every cycle to the per-user state directory by default, or only when `--snapshot PATH` is given?
- Q3 (D3): May the step-5 review evidence in `.dev/issues/409/bmad/final-review/` (raw/, graded/, verify/, fixes/, inputs/, the four briefs, progress.md, workflow-input.md; 36 tracked files, 660 KB for the whole folder) be archived, keeping REPORT.md, findings.md and owner-decision-pack.md, with links in REPORT.md and handoff-step5.md fixed?
- Q4 (D4): Do you want `.dev/brainstorms/20261108-132433-orca-observer-mvp/` (untracked) staged or archived first? Only after that may `adversarial/merged-output.md` (byte-identical to the root `merged-requirements.md`, 78,427 bytes) be removed.
- Q5 (D5): May `bmad/architecture-orca-observer/ARCHITECTURE-SPINE.md` become a one-line pointer to the spec copy? Fix handoff-step5.md:6 and the REPORT.md "cmp identical" claim with it.
- Q6 (D6): `ux-orca-observer` is current (updated 2026-11-12). May `ux-orca-observer-r2-review` be archived except `validation-report.md`, which the current document cites?
- Q7 (D7): May the PRD build scaffolding (extract-gates-risks, extract-spec-core, reconcile-spec-*, polish-*, adversarial-review.json, .memlog.md) be archived? Keep prd.md, addendum.md, extract-originals.md, validation-report.md and the files it cites.
- Q8 (D9): May `handoff-step1.md` to `handoff-step5.md` (tracked) be archived? `handoff-mvp-brainstorm.md` is untracked: stage it first, never delete it.
- Q9 (D12): In a record you write, does the staged choice of 2026-11-08 plus your production authorization satisfy DIRECTION-SELECTED? Only then may OQ-1, OQ-2 and the AC-S text be dropped.
- Q10 (extra): May the untracked owner and review files (`owner-decisions-20261108.md`, `live-test-guide.md`, `handoff-mvp-brainstorm.md`, `tuibbs-review/`, the brainstorm folder) be staged? Today one `git clean` would lose the only record of the additive-only rule that decides S1 and S4.
- Q11 (extra, R4): `rendering-rules.md:13` and `extract-prd-ux.md:106` say "no per-panel scrolling"; the built inspector scrolls with d and u and the live test guide expects it. Which one is right?

<!-- Source: Variant C (opus:analyzer) false-claims list (Extra 1-25), with Variant A Extra and Variant B Extra 2; refactor-plan.md Change 5; Base (original) Extra-findings idea -->
## Facts found false or stale in proposed-cuts.md
1. "36 candidate cuts": the ID list is 39 items.
2. R1 test ranges: test_terminal.py:57-82 includes the T28 no-blink test (:65-70); test_questions.py:46-98 includes the T11, T12 and no-read-marker tests (only :46, :52, :98 touch the removed names); the test_collector.py test spans :662-678; test_fixtures.py:139-151 is T34 and must be rewritten, not deleted; R1 missed test_terminal.py:132-133 (uses `sep`), `CLOSURE_EVIDENCE` (questions.py:25) and the unused imports `Style`, `box`, `field`.
3. R1 and T9 together (as proposed) delete every no-blink test.
4. R2: the "owner decision 2026-11-12" is not in the owner files but is recorded (as stated to the update run, not owner-written) in bmad/ux-orca-observer/EXPERIENCE.md:32-36 and SPEC rendering-rules.md:51; "the same facts as pre-built strings" holds only for `count_text`.
5. R3: parse.py:91-93 is `_BLOCK_FIELDS` (sanitizer block mode), not counter code; :356 is a call, not a sum; the five fields cannot be dropped without making every row report 5 more unrecognised keys; the dead code is the two aggregate counters.
6. R4: the "smaller option" fails because the `e` record has no inspector fields.
7. R6: the denominator rule is issue-body.md line 81 and spec T35, not "issue AC 3".
8. R9: the cited range 436-454 overstates the shared block; "behaviour must stay identical" cannot be shown because the question path has no tests for `RunnerFailure`, `OSError` or overrun.
9. R10: the `evicted` integer does not stay correct without the evicted-key list (reverts 2083db2ae).
10. T2: the question-recorder block starts at test_golden_contract.py:530, not :540.
11. T4: "cut :208-308 but keep :208-218" is self-contradictory; :232-256 is spec test T37 and :280-288 is what T16 relies on.
12. T5: :148-171 runs the real Collector; it is not only a test of the fake.
13. T6: test_adapter.py:158-192 is spec test T2 and also checks the forbidden-prefix set; test_view.py:864-869 is a unique check; test_terminal.py:214-231 guards the single `Console`.
14. T7: there are four extra checks, not two; the 32-character rule cannot move into the all-fixture scan (long-identifiers.json matches it); only the SENSITIVE loops are duplicated.
15. T8: "the matrix could be 12 cases" contradicts spec T16 (27 renders).
16. T9: the two tests are not duplicates; the redundant one is the test_terminal copy.
17. T10: test_collector.py:372 runs 8 variants, not 10.
18. S1: "golden file regeneration" is not needed (the golden has no `"questions"` key); "not in the owner's field list" ignores the additive-only rule (owner-decisions-20261108.md:17, snapshot.schema.json:4).
19. S2: `SCHEMA_VERSION` (export.py:23) is used at :195; the `resources` import (:14) must go too.
20. S3: the two files are not duplicates (5,069 vs 8,271 bytes); the pointer target folder is untracked; the tracked name is referenced by 19 files (37 occurrences) outside the review folders, not "about 20".
21. S4: both counters are shown on screen and sit in the release-1 golden, so the cut breaks T47.
22. S6: the proposed Ordering sentence ("rows are in ledger order") is false; rows are sorted by timestamp (view.py:842; export.py:207).
23. D1: the stale decisions are 6 and 8, not 5 and 6; decision 5 is the still-open fallback date.
24. D2: missed rendering-rules.md:89 and commands.py:453; `QUESTION_GATE_TEXT` must not change (pinned).
25. D3: the whole folder is 660 KB and 36 files; the archive set is about 528 KB and 33 files; not 560 KB and 30.
26. D4: `merged-requirements.md` sits at the folder root, not inside `adversarial/`.
27. D6: `ux-orca-observer` (updated 2026-11-12) is the current folder, not r2-review (2026-11-08); sizes are 416K and 272K.
28. D8: rows :51 and :64 are not the rows described; the human-question row is :52 and the AC restatement is :65.
29. D12: the "2026-11-10 authorization" is in no file under `.dev/issues/409` outside the review folders.
30. "the three owner files": the owner records are four files plus issue-body.md.
31. Reported by one variant, not cross-checked by another: the zip on disk is 14,438,526 bytes while issue-body.md:23 records 14,435,766.

## Orchestrator overrides and dissent

<!-- Source: orchestrator override (refactor-plan.md "Decision rules applied by the orchestrator" item 4) -->
Overrides (documented by the orchestrator; not re-derived here):
- (a) T5 narrowed to :192-203 only although 2 of 3 advocates would also cut :148-171, because :148-171 is an independent argv log for the forbidden-verb rule (binding rule 1) and a future broad `except` could swallow the fake's assertion.
- (b) T6 excludes test_view.py:864-869 after the orchestrator read showed it is the only check that export.py and render.py do not import `observe.parse`.
- (c) D1 confidence 65 -> 70: the orchestrator read owner-decisions-20261111.md and confirmed decisions 6 and 8 are decided, closing V2's stated reservation, and the pointer part that V3 and V2 doubted is dropped (OQ-n labels exist only in prd.md 12.1).

<!-- Source: debate-transcript.md Scoring Matrix (C-001, C-012, C-014, C-015) and the R1, T2, T4, T5 rows above -->
Open dissents:
- R1: V2 would keep `CODES` (adapter.py:65-82); the 2 of 3 result deletes it with test_adapter.py:719, relying on :718.
- T2: scope split on test_golden_contract.py:596-638 (V1 would also cut it; V3 and V2 would keep it); no 2 of 3 on exact scope, so T2 stays NOT-NOW at 65.
- T4: test_fixtures.py:226-230 is contested (2 of 3 would cut); T4 stays NOT-NOW at 65.
- T5: a 2 of 3 majority would also cut test_question_quiet_scope.py:148-171 (in Round 1, advocates 1 and 3; in the original variants, V1 and V2); the round1-advocate-2 position keeps it; kept by override (a).
