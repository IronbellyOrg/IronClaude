# Refactoring Plan: Merge into Base (Variant B, V2 sonnet:qa)

## Overview
- Base: Variant B (`variant-2-sonnet-qa.md`, sonnet:qa): skeleton is one verdict table plus an "Extra findings" section.
- Incorporating strengths from: Variant A (`variant-1-opus-architect.md`), Variant C (`variant-3-opus-analyzer.md`), and the three Round 1 advocate files (`round1-advocate-1.md`, `-2.md`, `-3.md`), which hold the post-debate positions.
- Output to produce: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/ponytail-review-20261116/cuts-debate/final-cut-list.md`
- Planned changes: 7 (document-level). Row content is fully specified in section "Target content" below; the merge executor copies it verbatim and does not re-decide any verdict.
- Risk level: Low (document assembly; no product code, tests or docs outside the output directory are touched).

## Decision rules applied by the orchestrator (apply, do not re-derive)
1. Final verdict = the verdict that at least 2 of 3 advocates reached in Round 1; scope = the scope those advocates share (intersection when they differ).
2. Confidence = median of the supporting advocates' stated confidences (mean of two). D1 carries +5 documented below.
3. Survives = final verdict CUT or CUT-SMALLER, confidence >= 70, no unresolved factual contradiction. Survivors are EXECUTE-NOW. KEEP and sub-70 items are NOT-NOW. DEFER-OWNER items are OWNER-NEEDED.
4. Orchestrator overrides (documented): (a) T5 narrowed to :192-203 only although 2 of 3 advocates would also cut :148-171, because :148-171 is an independent argv log for the forbidden-verb rule (binding rule 1) and a future broad `except` could swallow the fake's assertion; (b) T6 excludes test_view.py:864-869 after the orchestrator read showed it is the only check that export.py and render.py do not import `observe.parse`; (c) D1 confidence 65 -> 70: the orchestrator read owner-decisions-20261111.md and confirmed decisions 6 and 8 are decided, closing V2's stated reservation, and the pointer part that V3 and V2 doubted is dropped (OQ-n labels exist only in prd.md 12.1).

## Planned Changes

### Change 1: Row table with the five requested fields (from Variants A, B, C; post-debate)
- **Source**: debate-transcript.md scoring matrix; round1-advocate-1/2/3.md per-point matrices.
- **Target**: Base Variant B table (columns replaced by: ID, Final verdict, Exact scope if narrowed, Surviving guard, Confidence %, Execution class).
- **Rationale**: the request requires verdict, scope, guard, confidence and execution class for all 39 IDs.
- **Integration point**: replace the base table in full with the Target content table below.
- **Risk**: Low, additive-replace of a table that no other file reads.

### Change 2: Header counts and survival rule (from the request)
- **Source**: this plan, "Counts".
- **Target**: top of final-cut-list.md.
- **Rationale**: the caller wants counts per execution class and per final verdict.
- **Integration point**: a short summary before the table, including the rule that binds survival (CUT or CUT-SMALLER, confidence >= 70, no unresolved factual contradiction) and the note that the brief said 36 items but the ID list has 39.
- **Risk**: Low.

### Change 3: Ordered execution sequence for EXECUTE-NOW items (from V2 Extra 7 cut ordering; V1/V3 file groupings)
- **Source**: round1-advocate-2.md Extra 7; round1-advocate-3.md A-001; this plan.
- **Target**: new section "Execution sequence (EXECUTE-NOW only)".
- **Rationale**: items touching the same files go together (parse.py in R1 and R3; test_terminal.py in R1 and T9; commands.py in R1 and D2).
- **Integration point**: section text below, verbatim.
- **Risk**: Low.

### Change 4: Owner questions (from V1, V2, V3 DEFER-OWNER rows)
- **Source**: the OWNER-NEEDED rows.
- **Target**: new section "Questions for the owner" listing each question once, plus two extra questions the debate found.
- **Integration point**: text below.
- **Risk**: Low.

### Change 5: Facts the debate found false in the source (from V1 Extra, V2 Extra 2, V3 Extra 1-25)
- **Source**: variant Extra findings and X-001..X-014.
- **Target**: new section "Facts found false or stale in proposed-cuts.md".
- **Integration point**: list below, verbatim.
- **Risk**: Low.

### Change 6: Provenance annotations (from artifact-templates Section 6)
- **Target**: HTML comments at top and per section: `<!-- Source: Base (original) -->` for the table skeleton, `<!-- Source: Variant A ... -->`, `<!-- Source: Variant C ... -->`, `<!-- Source: round1-advocate-N ... -->` for the content taken from them, and `<!-- Source: orchestrator override ... -->` for the three overrides above.
- **Risk**: Low.

### Change 7: Concrete anchors preserved
- Every file:line, count and byte figure in the Target content is copied exactly; none is generalized.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base/Debate Result |
|---|---|---|
| T9 as proposed | delete test_render.py:182-190 | REJECTED: that copy is the real-screen guard (AC 5); the other copy is deleted instead. |
| T8 "27 cases to 12" | shrink the matrix | REJECTED: spec T16 is 27 renders. |
| S6 Ordering rewrite | "Rows are in ledger order" | REJECTED: code sorts by timestamp (view.py:842). |
| D1 collapse/pointer | replace prd.md 12.1 with a pointer | REJECTED: OQ-n labels exist only there. |
| D13 strike T45, T50 | strike rows | REJECTED: they pre-decide OQ-13 and AC-S. |
| R3 five fields | drop five row fields | REJECTED: `_KNOWN` is built from `_FIELDS`; every row would count 5 more. |
| S4, S1 removal | drop snapshot fields | Additive-only rule (schemaVersion 2 needed); S1 goes to the owner. |
| Any deletion of untracked files (D4, D9, S3) | | Binding rule 3. |
| Writing DIRECTION-SELECTED text (D12) | | Binding rule 4. |

Anchor-level omissions: no requirement ID, threshold or named system of any variant is dropped; items the debate rejected are listed above with the reason.

## Threshold preservation

| Value | Source | Disposition |
|---|---|---|
| 694 passed baseline | proposed-cuts.md line 3 | preserved-exact; not re-measured by any variant; every step must still pass (minus tests deliberately removed with their code) |
| Survival confidence 70% | request | preserved-exact |
| Convergence 0.80 | default | preserved-exact; result 0.934 |
| Tiebreak margin 5% | protocol | preserved-exact; margin 3.06% |
| T16 = 27 renders | acceptance-tests.md:28 | preserved-exact (T8) |
| Disclosure label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` | binding rule 1 | not touched by any item |

## Target content (copy verbatim into final-cut-list.md)

### Counts
- Items: 39 (R1-R10, T1-T10, S1-S6, D1-D13). The brief said 36; the ID list adds to 39.
- Final verdict: CUT 0, CUT-SMALLER 15, DEFER-OWNER 9, KEEP 15, REJECTED 0 (rejected sub-parts are listed inside rows).
- Execution class: EXECUTE-NOW 11, OWNER-NEEDED 9, NOT-NOW 19.
- Convergence 0.934 (57 of 61 diff points), status CONVERGED, depth quick.

### Final row table

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

### Execution sequence (EXECUTE-NOW only)
Gate after every step: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` (694 passed minus the tests deliberately removed, counted in the step) and `uv run ruff check src/superclaude/cli/observe tests/observe`. Re-grep every target right before editing (other sessions share the worktree; HEAD f104ca51a when checked). None of these steps touches the sanitizer, the argv allow-list, process-group kill, terminal restore, snapshot redaction or the disclosure label.
1. R1 + T9 (one change): terminal.py, adapter.py, parse.py (:723-733), questions.py, commands.py (:14, :142), collector.py, and tests test_terminal.py, test_adapter.py, test_collector.py, test_fixtures.py, test_questions.py.
2. R3 + R2: parse.py aggregate counters (after step 1 touched parse.py), view.py `count_text`.
3. S2: export.py, tests/observe/conftest.py, test_commands.py:34, test_snapshot_schema.py:15.
4. Test-only: T8 (test_render.py), T5 (test_question_quiet_scope.py:192-203), T7 (test_golden_contract.py).
5. Text and help: D2 (documents plus commands.py comment and help; run test_commands.py), D1, D13 (documents).
Staging note: `.dev/tasks/` stays staged as usual; nothing in this list stages `.claude/` paths.

### Questions for the owner
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

### Facts found false or stale in proposed-cuts.md
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

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | a wrong cell sends an executor to the wrong lines | executor re-greps before every edit (stated in the sequence) |
| 2-5 | Low | counts or lists out of date | recount from the table |
| 6 | Low | provenance tag missing | add tags |

## Review Status
- [x] Auto-approved (default, not `--interactive`)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-16 (orchestrator run)
