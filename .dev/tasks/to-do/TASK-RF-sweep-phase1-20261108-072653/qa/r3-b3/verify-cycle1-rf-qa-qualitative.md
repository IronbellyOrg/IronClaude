# R3-B3 gate, cycle 1: verification report (rf-qa-qualitative, fix-cycle phase)

**Topic:** re-check of F_0 (R3B3-F1 to R3B3-F9) and of the 100-id cycle-0 PASS set after the cycle-1 fix
**Phase:** fix-cycle verification, `fix_authorization: false`
**Fix cycle:** 1
**Design file read on disk now:** `docs/designs/orchestrator-mode.md` (1030 lines, `wc -l`)
**Other files read:** consolidated findings, fix log, cycle ledger, nine `qa-*-report.md` files, research/04 lines 170-232, SPEC `merged-requirements.md` lines 96, 104, 236, 320-321, 439, `r3-b3-mechanical.md` (all 136 lines)
**Constraints kept:** no `orca` command, no network call, no file written except this report.

## Summary

- All 9 findings of F_0 (1 BLOCKING, 8 MAJOR) are RESOLVED on disk. I did not take the fix log's word for any of them; each was re-read at the cited line.
- No new BLOCKING or MAJOR finding.
- 7 new MINOR notes (R3B3-N1 to R3B3-N7). They never fail the gate.
- Of the 100 ids in the cycle-0 PASS set, 96 still PASS and 4 now FAIL (qa-crossref-chain-report:C13, qa-evidence-quality-report:C12, qa-internal-consistency-report:C15, qa-numbers-metrics-report:C11). All four have one root cause, MINOR note R3B3-N1: `r3-b3-mechanical.md` was not regenerated after the fix and now states counts that are false on disk. The design text is not at fault.
- Section totals hold: `Total: 9 deviations.` (`orchestrator-mode.md:824`, 9 `D` rows), `Total: 23 open items.` (`:1000`, 23 rows in `:976-998`), em dash 0, non-ASCII 0, TODO/TBD/FIXME 0, 1030 lines, 28 code-fence lines (even).

### How I treated checks whose subject text the fix had to change

Eighteen cycle-0 PASS checks were phrased as equality with the pre-fix text (for example "byte-identical to research/04 4.2 item 2", "exactly 3 literals", "exactly 4 fixtures", "the three list-incomplete cases"). The cycle-1 fixes for R3B3-F1, F3, F5, F6, F7 and F8 had to change that text, so literal equality cannot hold. I re-ran each against the disk and marked it PASS only where (a) every element of the research text is still present as a subset, (b) every departure is one the consolidated file's "Smallest fix" requires, and (c) the new counts agree with each other everywhere the design states them. Those rows carry the word "re-based" in the Note column: qa-actionability-report:C1, qa-completeness-report:C5, C8, C10, qa-crossref-chain-report:C3, C9, C11, qa-domain-accuracy-report:C11, qa-evidence-quality-report:C5, C6, qa-internal-consistency-report:C13, qa-numbers-metrics-report:C3, C4, qa-spec-fidelity-report:C1, C15, qa-template-conformance-report:C10, C11, C12. If the orchestrator wants literal equality scored, those are the rows to flip; none of them hides a defect.

## Findings re-checked (F_0)

All line numbers are `docs/designs/orchestrator-mode.md` as read now.

| Id | Sev | Status | Evidence on disk |
|---|---|---|---|
| R3B3-F1 | BLOCKING | RESOLVED | `:501` adds a fourth case: "a scoped Run is not confirmed: its `orca worker-list <run>` row has no `unscanned` and no `OrcaObservation` has that Run, while its `orca task-list <run>` row ... has `unscanned` set, again only while `orca_available` is True", note `origin unknown: Run not confirmed`. It states the live finding (unknown id gives a complete empty `worker-list`, exit 0, `ok` true, UNVERIFIED until step 1.0a item 8) and that a real zero-row Run whose `task-list` did not fail is complete. `:245` now reads "unknown Run id: ok, zero rows; task-list --run R fails (7.2)". `:896` (capture item 8) and `:979` (open item 4, "Behaviour until closed") say the same; totals stay 9 and 23. Fixture `test_fr010_unknown_run_empty_list_unknown` is in `:746` with its control (the same input with `orca task-list BAD` not unscanned gives the control result). `OrcaObservation.run` exists (`:457`), so the rule reads a field `classify_all` has. The "safe behaviour until closed" sentence (`:972`) is now true for open item 4. One residual is R3B3-N6 (the exit code of the failing `task-list` is not recorded anywhere); it does not reopen F1 because capture item 8 names it. |
| R3B3-F2 | MAJOR | RESOLVED | `:502` reads "every unjoined transcript is None, in four cases"; a search for "in the window" over `:501-502` returns 0. Fixture 7 part (a) expects `tab map join not observable` on a T that is 8 h old (`:746`), which `:502` case 1 now allows. See R3B3-N5 for a SPEC wording side effect. |
| R3B3-F3 | MAJOR | RESOLVED | `:746` shared Given adds transcript U with `sessionId` equal to D1's `session_join` "(so U is joined and guard case 2 does not hold)", names the control ("FR-010 complete-negative join, the control", T True with the `origin not proved` note and Historical), replaces "differ by one input" with "each fixture changes only the list-completeness inputs it names" (I checked each of the six fixtures against that sentence; every changed input is named), and says T's notes are exactly the one `origin unknown:` note with no SP-16 literal and no `tab map join not observable`. Case 2 does not hold in fixtures 2 to 6 because D1 is joined to U; in fixture 1 `orca_rows` is empty so case 2 cannot hold either. |
| R3B3-F4 | MAJOR | RESOLVED | `test_fr010_incomplete_notes_order` (`:746`) has an exact Given and note list. Part (a): R1 ok with D1 whose `session_join` is None, then `orca_available` False, no U, T unjoined. I walked it through `:501-502`: outage holds; guard case 1 holds; guard case 2 holds (a worker row, no transcript joined); so the notes are `origin unknown: Orca unavailable`, the SP-16 literal, `tab map join not observable`, which is what `:746` lists. Part (b): R1 100 rows truncated with D1 matching U, R2 `call_failed`, R3 ok with zero rows and `orca task-list R3` unscanned, `ccsession orca-tabs` unscanned, `orca_available` True: truncated, call failed, Run not confirmed, tab map unreadable, no join-guard note (U is joined, `session_join` present). Matches the `:501` order. `:501` now says "every note that holds, attached in this order ... all before any join-guard note". |
| R3B3-F5 | MAJOR | RESOLVED | `:501` case 3: "its `sources` row `orca worker-list <run>` has `unscanned` set while `orca_available` is True"; the unavailable case is owned by the outage note ("the Orca sources left unread after an outage are marked `unscanned: orca unavailable` (section 5) and do not also count as `call_failed`"); a budget cut counts. Fixture 1 says `sources` holds `orca worker-list R1` with `unscanned` `orca unavailable` and T carries exactly one `origin unknown:` note; fixture 3 says `orca_available` True is what the trigger needs. `:501` says `classify_all` reads `orca_available`, `truncated`, `orca_rows` and `sources` only (see R3B3-N4: it also needs `ctx.runs`). |
| R3B3-F6 | MAJOR | RESOLVED | `:501` fifth case: `collect` set `unscanned` on the source row `ccsession orca-tabs`, with "a missing folder and an empty readable folder are readable and are not this case"; note `origin unknown: tab map unreadable`, last in the order. The row name appears in `:595`, `:745`, `:746`. Non-SPEC fixture `test_fr010_tab_map_unreadable_older_transcript_unknown` is in `:746` with its control. `:771` names it ("the SPEC's `tab map unreadable`"). No D row was added and the total is still 9; I checked this is right because the rule enforces the SPEC sentence (`merged-requirements.md:104`) rather than departing from it. |
| R3B3-F7 | MAJOR | RESOLVED | `:501` and `:595` both say every Run in `ctx.runs` has the row `orca worker-list <run>` and that a Run never started because the budget ran out carries `unscanned: time budget reached (90 s)` and counts as `call_failed` for this rule. Fixture `test_fr010_run_not_reached_budget_unknown` (`:746`) gives R2 that row, no observation with Run R2, `orca_available` True, one note `origin unknown: worker list call failed`. Case 4 does not also fire because R2's `worker-list` row has `unscanned`. |
| R3B3-F8 | MAJOR | RESOLVED | Fixture 2 is a hand-built `SweepInput`: 100 `OrcaObservation` rows, distinct Dispatch ids, `session_join` values different from T's, one (D1) matching U, `truncated` True. `page.nextCursor` occurs once in the whole file (`:746`) and is tagged "UNVERIFIED until step 1.0a item 3 (open item 5)" and "not an input here". The page-to-flag rule moved to the `collect` test. `:548`, `:980` and SPEC `:320-321` still say the trigger is count based, so the contradiction is gone. |
| R3B3-F9 | MAJOR | RESOLVED | `:745` gains `test_collect_worker_list_source_rows_and_truncated`: rows named exactly `orca worker-list R1` and `orca worker-list R2` (prefix "the literal word `orca`, not `$ORCA_CLI_COMMAND`"), R2 `unscanned` non-null and R1 None, a failed `task-list --run R2` sets `orca task-list R2` and not `orca worker-list R2`, budget spent before R2 gives no argv and the `time budget reached (90 s)` row, an unreadable and a missing and an empty `orca-tabs/` folder, 100 rows set `truncated` and 99 do not. `:747` adds the lower-bound line `[Orca rows: 100 shown; total is a lower bound (paging not yet captured)]`, which matches `:614` character for character, and `summary.total_is_lower_bound` True. `:595` states the literal prefix and that `collect` sets `truncated` at `WORKER_LIST_PAGE` rows. The `Budget` clock is injectable (`:367-368`), so "budget spent before R2" is buildable. |

## Re-read as the three intended readers

### Reader 1: the developer who writes the list-incomplete branch of `classify_all` (`:501-502`, `:455-456`, `:467`)

What this reader can now do without guessing: the five triggers and their inputs (`orca_available`, `truncated`, source rows by exact name, `OrcaObservation.run`); the precondition "while `orca_available` is True" for cases 3 and 4; the note literals and their fixed order; that every note that holds is attached; that a hit makes the transcript None and could not determine and never idle or Historical, even outside the window; and that the join-guard notes come after. Each trigger can be checked against a fixture with an exact `sources` list.

Where this reader still has to guess (all MINOR, none changes the class a transcript gets):
- R3B3-N4: `:501` says the five cases are evaluated "from `orca_available`, `truncated`, `orca_rows` and `sources` only", but cases 3 and 4 are per scoped Run, and the scoped Runs come from `ctx.runs` (`:455`; `ctx` is a `classify_all` argument at `:420`), not from those four inputs. The reader will use `ctx.runs`; the word "only" is wrong.
- Carried F10 (not re-graded): for an unjoined transcript that also has a tab-map entry, `:498` and `:499` give it a pane or tail note and `:501` gives it `origin unknown:` notes. The order between the two families, and whether an `origin unknown:` note counts as a "pane or tail note" for the SP-16 line at `:502`, is still not stated, and no fixture has a transcript with an entry under an incomplete list.
- Carried F12 (not re-graded): `:378` shows `unscanned: time budget reached (90 s)` with the prefix, while `:595` and `:746` show stored values with and without it (`orca unavailable`, `orca call failed (exit 1)`, `unscanned: time budget reached (90 s)`). `classify_all` only tests for non-null, so its behaviour is the same either way; the renderer is where the form matters (FR-019 prints `unscanned: orca unavailable`, `:749`).

### Reader 2: the `collect` code that names the per-Run source rows (`:595`, `:392`, `:401`, `:745`)

What this reader can now do: name `orca worker-list <run>` and `orca task-list <run>` (the `--run` call) with the literal prefix `orca`; set `unscanned` on a failed call (`orca call failed (exit <n>)`), on a Run never started (`time budget reached (90 s)`) and on `ccsession orca-tabs`; set `truncated` at 100 rows; and prove all of it with one test that `:745` describes in full.

Where this reader still has to guess (all MINOR; the `:745` test catches a wrong guess for the items it lists):
- R3B3-N2: `read_tab_map(state_dir) -> tuple[TabMapEntry, ...]` (`:401`) returns a bare tuple, while the comment at `:394` says each reader "returns data plus a SourceCoverage row", and `:394` also says readers never raise past `collect`. How `collect` learns that the folder was unreadable (needed for the fifth case) is not specified. Also unsaid: whether one unreadable file inside the folder, or a folder reported `unscanned: outside root` under `:512`, counts as "cannot be listed or read".
- R3B3-N3: the third Orca read per Run, `task-list --ready --run <run>` (`:246`, `:530`), gets no row name. `:595` names two rows per Run and says `orca task-list <run>` is the `--run` call. The natural mapping gives both task-list calls the same name, and the rule at `:501` reads that name.
- R3B3-N6: `:501` and `:746` rely on the unknown-Run `task-list` failing as a `call_failed` (`orca call failed (exit 1)`). SPEC `:439` maps a nonzero exit or an invalid response to `call_failed`; nothing says what `collect` does with an exit 0 body that has `ok: false`.

### Reader 3: the developer who builds the fixtures (`:746`, `:745`, `:747`)

What this reader can now do: build the control and the six single-cause fixtures from one shared Given; build fixture 2 as a plain `SweepInput`; build both halves of the note-order fixture and assert the exact note list; build the `collect` test with a fake `_orca` and an injected `Budget` clock.

Where this reader still has to guess (MINOR):
- R3B3-N7: part (a) of `test_fr010_incomplete_notes_order` says it "departs from the shared Given" and then lists only its own changes, so T's age and tab-map state are inherited without being restated (part (b) says "with the shared Given otherwise"). The control has no test function name (`:746` says "not a `test_fr010_*` name"). The `TranscriptTail` fields other than `last_activity` (`mtime`, `first_record_ts`, `tail_complete`, `project_key`, `session_id`) are still not given for T (carried F13). The whole `test_classify.py` row is still one table cell of about 12 KB.
- R3B3-N7 (second part): fixtures 2 and 7(b) give 100 rows that all have `session_join` set. A real `collect` leaves 50 of 100 rows without a `worker-show` result (`:341`) and `session_join` comes from `worker-show` (`:976`), so a real 100-row page would also trip guard case 1. The fixtures are hand-built `SweepInput` values and are valid unit inputs for `classify_all`; they must not be read as `collect` output.

## New findings

No new BLOCKING and no new MAJOR finding. I looked for one in these places and found none:
- An input that makes one transcript both `origin unknown:` and Historical or idle. Every unjoined transcript is None under any of the five cases, and rules 7 and 8 need `person_started is True` (SPEC `merged-requirements.md:255-256`).
- Two cases that both fire for the same Run. Case 3 needs `unscanned` on the `worker-list` row and case 4 needs it absent, so they are exclusive per Run.
- A case that fires during an outage and adds a second note. Cases 3 and 4 are gated on `orca_available` True.
- A fixture whose Given does not produce its listed notes. I walked all seven against `:501-502`.
- A wrong count or cross-reference. `:771`, `:1030`, `:979` and `:896` agree: three SPEC fixtures, four SPEC reasons, five rule cases, four join-incomplete cases, seven `test_fr010_*`.

MINOR notes (never fail the gate, not re-checked in later rounds):

| Id | Sev | Where | Defect | Smallest fix |
|---|---|---|---|---|
| R3B3-N1 | MINOR | `phase-outputs/test-results/r3-b3-mechanical.md` lines 57-64 and 112-122 | The file was produced before the fix (run time 22:07:38Z) and was not regenerated. Command 2 lists lines 11, 746, 771, 1030; on disk the same grep now also hits `:501`, because the new bullet uses the word "outage". The pass-rule table says `outage` in 7.2 is 0; on disk it is 1 (`sed -n 449,518p` then `grep -cF outage`). Command 7 still prints "(no output expected ...)" (carried F17). The fix log holds a correct re-run, but the file the gate names does not. This is the only cause of the 4 PASS-to-FAIL rows in the Checks table. | Orchestrator re-runs the nine item 4.6 commands and overwrites the file; no design edit and no new fix cycle. |
| R3B3-N2 | MINOR | `:401`, `:394`, `:501` | `read_tab_map` returns a bare tuple, so the text does not say how `collect` learns the folder was unreadable; per-file versus folder, and `unscanned: outside root` (`:512`), are not decided. The `:745` test pins the folder case. | Add one clause at `:401` or `:595`: which function sets `unscanned` on `ccsession orca-tabs`, and whether one unreadable entry file counts. |
| R3B3-N3 | MINOR | `:595`, `:246`, `:530` | The row for `task-list --ready --run <run>` is unnamed; `orca task-list <run>` could be built for both task-list calls. | Name it in `:595`, for example `orca task-list --ready <run>`, and say `:501` reads only `orca task-list <run>`. |
| R3B3-N4 | MINOR | `:501` | "from `orca_available`, `truncated`, `orca_rows` and `sources` only" omits `ctx.runs`, which cases 3 and 4 need to list the scoped Runs. | Add `ctx.runs` to that list. |
| R3B3-N5 | MINOR | `:502`, SPEC `:236` | Deleting "in the window" (the F2 fix) makes guard case 2 wider than the SPEC sentence it cites ("SPEC line 236, SP-16": "every unjoined transcript in the window"). It agrees with FR-010 (SPEC `:104`: True only when "the join completed") and is the safer reading, but it widens a SPEC rule with no D row and no note. | Add half a sentence at `:502` saying the design applies SP-16 to every unjoined transcript because FR-010 requires a completed join for any True; or record a deviation (the owner's call; it would change `Total: 9 deviations.`). |
| R3B3-N6 | MINOR | `:501`, `:746` fixture 4, `:896`, SPEC `:439` | The Run-not-confirmed rule fires only if the unknown-Run `task-list --run` becomes a `call_failed` row. The live evidence quoted in `qa-domain-accuracy-report.md` records `ok: false` with code `run_not_found` for both `task-list` forms but no exit code, and neither the design nor the SPEC says an exit 0 body with `ok: false` is `call_failed`. The fixtures hard-code `(exit 1)`. If real Orca exits 0 here, the rule never fires and F1 fails open again. Step 1.0a item 8 already records "stderr and exit code", and 1.0a runs before any code, so this is graded MINOR. | In `:896` or `:979` say a `task-list` body with `ok: false` counts as `call_failed` whatever the exit code, and add that to the `:745` `collect` test. |
| R3B3-N7 | MINOR | `:746` | Fixture-builder guesses listed under Reader 3: part (a) inheritance of T's age, no name for the control, T's other transcript fields, one 12 KB cell, and 100 rows with `session_join` set that a real `collect` could not produce. | Restate T's age in part (a); give the control a test name; list T's eight `TranscriptTail` fields; add "built directly for `classify_all`" to fixtures 2 and 7(b). |

Carried and not re-graded: R3B3-F10 and F11 to F25 (MINOR in cycle 0, untouched by the fix, as the fix log says). I spot-checked that none became worse: F11 (the section 18 quote) is unchanged at `:1030`; F24 (the unescaped `|` at `:64`) is outside every edited line; F25 is a research file.

## Checks

One row per id of the cycle-0 PASS set (100 rows), then my own rows V1 to V4. The third column gives the reason for a FAIL, or the evidence for a PASS ("re-based" marks the 18 rows described in the Summary).

| Check | Result | Reason (FAIL) or evidence (PASS) |
|---|---|---|
| qa-actionability-report:C1 | PASS | re-based. Research/04 4.2 edits 1 to 4 are present as supersets at `:746`, `:501`, `:771`, `:1030`. |
| qa-actionability-report:C2 | PASS | The three SPEC literals are spelled alike in `:501` and `:746` and follow SPEC `:104` order. |
| qa-actionability-report:C3 | PASS | `orca_available` and `truncated` are `SweepInput` fields (`:456`) and the triggers read them (`:501`). |
| qa-actionability-report:C5 | PASS | Order is stated at `:501` and pinned by `test_fr010_incomplete_notes_order` parts (a) and (b) (`:746`). |
| qa-actionability-report:C10 | PASS | `:595` gives the exact name `orca worker-list <run>` with the literal `orca` prefix. See R3B3-N3 for the unnamed `--ready` row. |
| qa-actionability-report:C16 | PASS | Em dash 0, TODO/TBD 0, "four incomplete cases" once at `:1030`, literals at `:501` and `:746`. |
| qa-actionability-report:C17 | PASS | `:501` last sentence: "never idle or Historical, even when its activity is older than the window". |
| qa-completeness-report:C1 | PASS | `:746` "the three SPEC incomplete cases (...)" with the `origin unknown:` and never idle or Historical clause. |
| qa-completeness-report:C2 | PASS | Guard-case 1 to 4 fixtures and the control are still in `:746` (read). |
| qa-completeness-report:C3 | PASS | The bullet sits at `:501`, directly before the join-guard bullet `:502`, with the literals, the order rule and the never idle clause. |
| qa-completeness-report:C4 | PASS | `:595` names `orca worker-list <run>` and the `call_failed` `unscanned` reason. |
| qa-completeness-report:C5 | PASS | re-based. `:771` now says "five list-incomplete cases (the three SPEC cases: outage, full page, `call_failed` ...)". |
| qa-completeness-report:C6 | PASS | `:771` test column names "the three SPEC incomplete-case fixtures". |
| qa-completeness-report:C7 | PASS | `:1030` has the correction of cycle 2 and the shape of its sibling rows. |
| qa-completeness-report:C8 | PASS | re-based. All research shared-Given elements are in `:746` (now, window 6 h, T, 8 h, no entry, no join, `session_join` present); the "guard otherwise holds" phrase was replaced by explicit inputs. |
| qa-completeness-report:C9 | PASS | Outage fixture `:746` keeps every Then element (None, could not determine, note, visible, not Historical, `summary.historical` 0). |
| qa-completeness-report:C10 | PASS | re-based. 100 rows, `truncated`, note, not Historical, `total_is_lower_bound` are present; `page.nextCursor` is now an UNVERIFIED mention, not a Given, as R3B3-F8 required. |
| qa-completeness-report:C11 | PASS | Fixture 3 keeps two Runs, R2 `call_failed` not call one, `orca call failed (exit 1)`, `orca_available` True, the note. |
| qa-completeness-report:C12 | PASS | Notes-order fixture keeps both combinations (outage plus case 1; truncated plus `call_failed`) and the order. |
| qa-completeness-report:C13 | PASS | "four join-incomplete cases" at `:771`, `:822`, `:860`, `:1030`; "four incomplete cases" only at `:1030` (grep). |
| qa-completeness-report:C14 | PASS | Each SPEC acceptance fixture maps to a design fixture; section map, `:501`, `:595`, `:1030` re-derived from the file, not from the mechanical file. |
| qa-crossref-chain-report:C1 | PASS | Headings at 351, 353, 449, 519, 559, 731, 756, 970, 1002, 1022 (grep). |
| qa-crossref-chain-report:C2 | PASS | The three literals are word for word in `:501`; the added two do not disturb the SPEC order. |
| qa-crossref-chain-report:C3 | PASS | re-based. Literals identical in `:501` and `:746`; the four original fixture names are kept; Given and Then changed only as F3, F4, F5, F8 required. |
| qa-crossref-chain-report:C4 | PASS | `orca worker-list <run>` is in `:501` (1 line), `:595` (1 line), `:746` (0 lines); `orca worker-list R2` is the instance. |
| qa-crossref-chain-report:C5 | PASS | `:1030` pointers (11), (7.2), (12), (7.4) resolve. |
| qa-crossref-chain-report:C6 | PASS | `:979` still supports the "(open item 4)" claim at `:746`; closed by capture item 8 at `:896`. |
| qa-crossref-chain-report:C7 | PASS | `:980`, `:548`, `:614`, `:891` are consistent with `:501`. |
| qa-crossref-chain-report:C8 | PASS | `OrcaResult` kinds (`:376`) and `collect` (`:392`) exist. |
| qa-crossref-chain-report:C9 | PASS | re-based. `:771`, `:501` and `:1030` all say five list-incomplete cases; "four join-incomplete" in `:502`, `:771`, `:822`, `:860`. |
| qa-crossref-chain-report:C10 | PASS | The `:1030` correction of cycle 2 is still accurate in substance (quote form is carried F11). |
| qa-crossref-chain-report:C11 | PASS | re-based. Items 1 to 4 are applied at `:746`, `:501`, `:771`, `:1030` with every research element kept. |
| qa-crossref-chain-report:C12 | PASS | "four incomplete cases" once at `:1030`; em dash 0; TODO/TBD 0; `:824` and `:1000` totals. |
| qa-crossref-chain-report:C13 | FAIL | MINOR only (R3B3-N1). The mechanical file's per-section table says `outage` in 7.2 is 0; disk gives 1. Section ranges are still true. |
| qa-domain-accuracy-report:C1 | PASS | `:501` still carries the three SPEC reasons in SPEC wording, plus two more. |
| qa-domain-accuracy-report:C2 | PASS | Literals and order agree across `:501`, `:746`, research/04 4.2. |
| qa-domain-accuracy-report:C3 | PASS | Outage covers call-one and later unavailable through `orca_available` False (`:501`, `:250-251`, `:286`). |
| qa-domain-accuracy-report:C4 | PASS | Truncated rule agrees across `:548`, `:501`, `:980`; the live page-shape note F3 is carried MINOR. |
| qa-domain-accuracy-report:C7 | PASS | `:501` says a real Run with zero rows whose `task-list` did not fail is complete; fixture 4 pins it. |
| qa-domain-accuracy-report:C8 | PASS | No rule added that depends on read order; carried MINOR F19 is unchanged. |
| qa-domain-accuracy-report:C9 | PASS | `ALLOWED_ORCA` (`:526-535`) has no state filter; unchanged. |
| qa-domain-accuracy-report:C10 | PASS | `--include-remote` is still a forbidden token (`:537`). |
| qa-domain-accuracy-report:C11 | PASS | re-based. `:746` and `:771` keep the three SPEC cases distinct from the four join-incomplete cases while adding two. |
| qa-evidence-quality-report:C1 | PASS | "100 rows by default" at `:299`, `:548`, `:614`, `:980`. |
| qa-evidence-quality-report:C3 | PASS | `orca call failed (exit <n>)` still traces to SPEC `:287`, `:439` (`:595`, `:746`). |
| qa-evidence-quality-report:C4 | PASS | Fixture 3 still says R2, not call one, "a nonzero exit on call one is `unavailable` (open item 4)"; `:979` agrees. |
| qa-evidence-quality-report:C5 | PASS | re-based. The bullet keeps every element of research/04 4.2 item 2 (three triggers, three literals, order, join-guard-after, never idle or Historical clause); wording changed per F1, F5, F6, F7. |
| qa-evidence-quality-report:C6 | PASS | re-based. Fixtures 1 to 3 match research/04 4.3 except for the changes F3, F5, F8 required; fixture 4 changed per F4. |
| qa-evidence-quality-report:C7 | PASS | The three SPEC fixtures are present and named at `:746`. |
| qa-evidence-quality-report:C8 | PASS | `:980` and `:891` still hedge the cursor field and page size; `:746` now points to them. |
| qa-evidence-quality-report:C12 | FAIL | MINOR only (R3B3-N1). The mechanical report's facts no longer all hold: Command 2 lacks `:501`, table row `outage` 7.2 reads 0 against 1. Line count, em dash, TODO and section ranges still hold. |
| qa-evidence-quality-report:C13 | PASS | Items present at `:746`, `:501`, `:771`, `:1030`, `:595`. |
| qa-evidence-quality-report:C14 | PASS | "four incomplete cases" once at `:1030`. |
| qa-internal-consistency-report:C1 | PASS | Three SPEC literals identical in `:501`, `:746`, research/04. |
| qa-internal-consistency-report:C2 | PASS | `orca_available` False trigger agrees with the `unavailable` kind (`:376`) and `:979`. |
| qa-internal-consistency-report:C4 | PASS | `truncated` trigger agrees with `:548`, `:980`, `:595` and `:346`. |
| qa-internal-consistency-report:C5 | PASS | `summary.historical` and `summary.total_is_lower_bound` agree with fixtures (`:588-589`, `:746`). |
| qa-internal-consistency-report:C6 | PASS | None cannot reach rule 7 or 8 (SPEC `:255-256`). |
| qa-internal-consistency-report:C9 | PASS | No input found with both `origin unknown:` and Historical or idle; see New findings. |
| qa-internal-consistency-report:C13 | PASS | re-based. `:771`, `:746`, `:1030` agree on three SPEC cases, five rule cases, four join-incomplete cases. |
| qa-internal-consistency-report:C14 | PASS | `:245` now says unknown Run is ok with zero rows; `:979` agrees; `:749` "unknown-Run then R2" is carried F15. |
| qa-internal-consistency-report:C15 | FAIL | MINOR only (R3B3-N1). Hit counts in the mechanical file no longer match disk (Command 2, `outage` row). Ranges, em dash, TODO and totals match. |
| qa-numbers-metrics-report:C1 | PASS | SPEC `:104` still lists three incomplete-case fixtures. |
| qa-numbers-metrics-report:C2 | PASS | `:746`, `:771`, `:1030`, `:11` name the three SPEC cases. |
| qa-numbers-metrics-report:C3 | PASS | re-based. 5 literals, each on one line in 7.2 and on one line in section 11, identical; the 3 SPEC ones are unchanged. |
| qa-numbers-metrics-report:C4 | PASS | re-based. 7 distinct `test_fr010_*` names (grep of `:746`), the text says "seven" at `:746` and `:771`; the first four names equal research/04 lines 197-200. |
| qa-numbers-metrics-report:C5 | PASS | Shared Given: 8 h against 6 h; part (a) of the note-order fixture inherits it (R3B3-N7). |
| qa-numbers-metrics-report:C6 | PASS | `WORKER_LIST_PAGE` 100 at `:548`; uses at `:299`, `:346`, `:595`, `:746`. |
| qa-numbers-metrics-report:C7 | PASS | 9 `D` rows (`grep -c`), one `Total: 9 deviations.` at `:824`. |
| qa-numbers-metrics-report:C8 | PASS | 23 rows in `:976-998`, `Total: 23 open items.` at `:1000`; rows 4 and 5 at `:979`, `:980`. |
| qa-numbers-metrics-report:C9 | PASS | Em dash 0, non-ASCII 0, TODO/TBD/FIXME 0. |
| qa-numbers-metrics-report:C10 | PASS | "four incomplete cases" once; "four join-incomplete" at `:771`, `:822`, `:860`, `:1030`; "in four cases" at `:502`. |
| qa-numbers-metrics-report:C11 | FAIL | MINOR only (R3B3-N1). The mechanical file's per-section table is false on disk for `outage` in 7.2 (0 stated, 1 found). |
| qa-numbers-metrics-report:C12 | PASS | SPEC 653 lines, 26 FR rows, 15 NFR rows; `:733` "Seven new files"; 8 templates at `:526-535`; six path-B fixtures and nine boundary fixtures are in `:745`; "the five exemptions" in `:746`. |
| qa-spec-fidelity-report:C1 | PASS | re-based. Not byte-identical any more; it contains every element of research/04 4.2 item 2 and every departure is required by F1, F5, F6, F7. |
| qa-spec-fidelity-report:C2 | PASS | Fixture (a) keeps its meaning and adds the `sources` row. |
| qa-spec-fidelity-report:C3 | PASS | Fixture (b) is the same full-page case, now a hand-built `SweepInput` with `truncated` True. |
| qa-spec-fidelity-report:C4 | PASS | Fixture (c) uses R2, not call one. |
| qa-spec-fidelity-report:C5 | PASS | 8 h against a 6 h window in the shared Given. |
| qa-spec-fidelity-report:C6 | PASS | No fixture lets T reach idle or Historical; every fixture says not Historical and `summary.historical` 0. |
| qa-spec-fidelity-report:C10 | PASS | Note order at `:501` agrees with the note-order fixture and with `:502`. |
| qa-spec-fidelity-report:C12 | PASS | `:771` names the three SPEC fixtures and the list-incomplete cases. |
| qa-spec-fidelity-report:C13 | PASS | "four incomplete cases" only at `:1030`. |
| qa-spec-fidelity-report:C14 | PASS | The four join-incomplete cases and the four guard-case fixtures are kept. |
| qa-spec-fidelity-report:C15 | PASS | re-based. The four research fixture names are present (grep); three more, seven in all. |
| qa-spec-fidelity-report:C16 | PASS | `SourceCoverage` is `name, coverage, age_seconds, unscanned` (`:467`); the new names `orca worker-list <run>`, `orca task-list <run>` and `ccsession orca-tabs` are only values of `name`, and the `sources` key set at `:571` is unchanged. |
| qa-template-conformance-report:C1 | PASS | `:501` keeps the `- ` list style in the Joins list `:496-503`. |
| qa-template-conformance-report:C2 | PASS | The SPEC-order relation of the literals holds. |
| qa-template-conformance-report:C3 | PASS | The 7.4 JSON block `:563-593` has the keys of the pinned v1 paragraph `:597`; `:595` is prose. |
| qa-template-conformance-report:C4 | PASS | Pipe counts: rows `:745`, `:746`, `:771`, `:896`, `:1030` have 4 pipes in 3-column tables; `:747` has 4 unescaped; `:979` has 5 in the 4-column table. |
| qa-template-conformance-report:C5 | PASS | Em dash 0, non-ASCII 0. |
| qa-template-conformance-report:C6 | PASS | TODO/TBD/FIXME 0. |
| qa-template-conformance-report:C7 | PASS | Backticks and parentheses are even on all 11 edited lines; 28 fence lines. |
| qa-template-conformance-report:C8 | PASS | 18 numbered `##` headings; both totals present once. |
| qa-template-conformance-report:C9 | PASS | "four incomplete cases" once; "four join-incomplete" consistent. |
| qa-template-conformance-report:C10 | PASS | re-based. Section 11 cell keeps the research fixture names and their Given, When, Then as supersets. |
| qa-template-conformance-report:C11 | PASS | re-based. `:771` keeps both research additions, with "five" and the SPEC three named. |
| qa-template-conformance-report:C12 | PASS | re-based. `:1030` keeps the item 4.2 text and the three-cell shape of its siblings; gate fixes appended. |
| qa-template-conformance-report:C13 | PASS | `call_failed` (`:376`), `WORKER_LIST_PAGE` (`:548`), `truncated` and `orca_available` (`:456`), `OrcaObservation.run` (`:457`), `ctx.runs` (`:455`), summary keys (`:588-589`) exist. |
| qa-template-conformance-report:C14 | PASS | Source name and reason forms agree across `:501`, `:595`, `:746` and SPEC `:439`. |
| V1 | PASS | Totals and form on disk: 9 `D` rows and `:824`; 23 open rows and `:1000`; em dash 0; non-ASCII 0; TODO/TBD/FIXME 0; 1030 lines. |
| V2 | PASS | Reader 1, the `classify_all` branch: buildable from `:501-502`; MINOR guesses N4 and carried F10, F12 only. |
| V3 | PASS | Reader 2, `collect` source rows: buildable from `:595` and `:745`; MINOR guesses N2, N3, N6 only. |
| V4 | PASS | Reader 3, fixtures: all seven walked against `:501-502` and give their stated notes; MINOR guess N7 only. |

Tally: 100 ids from the cycle-0 PASS set, 96 PASS and 4 FAIL; V1 to V4 PASS.

## Self-Audit

**(a) Reliance list.** No `## Inherited Structural Verdict` block was supplied. I relied on no earlier PASS. I read the fix log only to know what to look for; every statement in it that I report on was re-read in the design. The mechanical file was treated as a claim to test, and it failed the test (R3B3-N1).

**(b) Independent semantic checks (each with tool evidence).**
- F1 to F9 re-read at the cited lines of `orchestrator-mode.md` (Read of `:449-523`, `:559-598`, `:731-755`, `:223-293`, `:292-351`, `:353-448`, `:519-558`, `:599-646`, `:873-908`; `sed -n` of `:11`, `:771`, `:822`, `:824`, `:860`, `:976-982`, `:1000`, `:1018`, `:1030`).
- All seven `test_fr010_*` fixtures walked against `:501-502` to confirm the listed notes follow from the Given (this is how I confirmed F3, F4, F5 and F7 are really fixed and not just reworded).
- Counts by command: literal occurrences per line (`grep -o | uniq -c`), per-section line counts (`sed -n range | grep -cF`), fixture names (`grep -o`), `D` rows (9), open-item rows (23), non-ASCII (0), TODO/TBD/FIXME (0), code fences (28), backtick and parenthesis parity on 11 edited lines, pipe counts on 10 table rows, heading lines, SPEC 653 lines with 26 FR and 15 NFR rows.
- `:614` against `:747` (the lower-bound line is identical); SPEC `:104`, `:236`, `:255-256`, `:320-321`, `:439` against the design (this is what produced R3B3-N5).
- The report's 100 check ids diffed against the 100 ids in `cycle-ledger.md` row 0: identical.

**Not verified, stated plainly.**
1. The exit code of `task-list --run <unknown>` against real Orca. I ran no `orca` command as instructed, and no earlier report recorded it (R3B3-N6).
2. The live `worker-list` behaviour for an unknown Run id rests on the evidence quoted in `qa-domain-accuracy-report.md`; I did not repeat it.
3. The design file is untracked, so there is no diff. I read the whole of every edited range and ran whole-file form scans, and I cannot prove no other line changed.

**Counts.** Findings re-checked: 9. Check ids re-tested: 100, plus V1 to V4. New findings: 0 BLOCKING, 0 MAJOR, 7 MINOR. Confidence: Verified 113/113 | Unverifiable 0 | Unchecked 0. Tool engagement: Read about 30 | Grep 11 | Glob 0 | Bash 14 (read-only `sed -n`, `grep`, `awk`, `wc`; no `orca`, no network). Web research: none, so the Tavily-first rule did not apply.

## Recommendation

Accept the design for R3-B3. Before the cycle closes, the orchestrator should regenerate `phase-outputs/test-results/r3-b3-mechanical.md` (R3B3-N1; the nine commands are cheap and the fix log already holds the correct output), so that the four stale-evidence rows go back to PASS. The other six MINOR notes (N2 to N7) are for the owner or the code step; none needs a design fix cycle. The one worth doing now is R3B3-N6, a single clause in `:896` or `:979`, because it is the only note that could make the BLOCKING finding fail open if real Orca behaves unexpectedly.

Verdict: PASS
Blocking count: 0

