# R3-B3 gate, cycle 1: verification (rf-qa, fix_authorization false)

Design file under test: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/docs/designs/orchestrator-mode.md`

Date: 2026-11-09. Phase: fix-cycle verification (cycle 1 of at most 2). `fix_authorization: false`; only this report was written. No `orca` command and no network call were made. Bash was used only for read-only `grep`, `sed -n` and `wc`.

Inputs read (each in chunks of at most 150 lines): consolidated findings (95 lines), cycle ledger (3 lines), fix log (169 lines), the nine cycle-0 lens reports, research/04 lines 178-215, SPEC `merged-requirements.md` lines 102-105, `r3-b3-mechanical.md` (136 lines), and the design file at the lines named below (the file is 1030 lines on disk, `wc -l`). I did not rely on the fix log for any verdict; every line cited below was read from the design file in this run.

## Section 1: F_0 findings (R3B3-F1 to R3B3-F9)

| Id | Severity | Status | Evidence on disk now (`docs/designs/orchestrator-mode.md`) |
|---|---|---|---|
| R3B3-F1 | BLOCKING | RESOLVED | `:501` has a fourth case "Run not confirmed": the `orca worker-list <run>` row has no `unscanned`, no `OrcaObservation` has that Run, and the `orca task-list <run>` row has `unscanned`, only while `orca_available` is True; note `origin unknown: Run not confirmed`; the bullet states that an unknown Run id gives a complete empty `worker-list` (exit 0, `ok` true, live read 2026-11-08, shape UNVERIFIED until step 1.0a item 8, open item 4) and that a real zero-row Run whose `task-list` did not fail is complete. The row `orca task-list <run>` is named at `:595` and its template is allowlisted at `:531`. `:245` now reads "unknown Run id: ok, zero rows; task-list --run R fails (7.2)"; `:896` (capture item 8) and `:979` (open item 4) are reworded to the empty-list reading; fixture `test_fr010_unknown_run_empty_list_unknown` is at `:746` with its control (same input, `task-list` not unscanned, gives the control result). The live evidence (exit 0, `ok` true, empty `workers`; `task-list` gives `run_not_found`) is quoted in `qa-domain-accuracy-report.md:20-21`. Totals unchanged (`:824`, `:1000`). |
| R3B3-F2 | MAJOR | RESOLVED | `:502` now begins "The guard's 'join completed' condition fails, and every unjoined transcript is None, in four cases." A search of the file for "in the window" finds only the quotation in the section 18 row (`:1030`). |
| R3B3-F3 | MAJOR | RESOLVED | `:746` shared Given now adds transcript U whose `sessionId` equals D1's `session_join` ("so U is joined and guard case 2 does not hold"), names the control ("In the control T is True with the `origin not proved` note and is Historical"), replaces "differ by one input" with "each fixture changes only the list-completeness inputs it names" (a search for "by one input" finds nothing), and says T's notes are "exactly the one `origin unknown:` note the fixture names, with no SP-16 literal and no `tab map join not observable`". Fixture 1 (outage) has `orca_rows` empty, so case 2 cannot hold; fixtures 2 and 3 keep D1 and U. |
| R3B3-F4 | MAJOR | RESOLVED | `test_fr010_incomplete_notes_order` at `:746` has an exact Given. Part (a): R1 ok with D1 whose `session_join` is None, then `orca_available` False, no U; guard cases 1 and 2 hold; notes exactly `origin unknown: Orca unavailable`, the SP-16 literal, `tab map join not observable`, which agrees with `:502` ("the SP-16 literal first and then `tab map join not observable`") and `:501` ("before any join-guard note"). Part (b): R1 100 rows `truncated`, D1 matching U, R2 `call_failed`, R3 zero rows with `orca task-list R3` unscanned, `ccsession orca-tabs` unscanned; notes exactly truncated, call failed, Run not confirmed, tab map unreadable, none of the join-guard notes; this is the `:501` order. `:501` now says "every note that holds, attached in this order". |
| R3B3-F5 | MAJOR | RESOLVED | `:501` third case is "its `sources` row `orca worker-list <run>` has `unscanned` set while `orca_available` is True"; "While `orca_available` is False the outage note alone covers the unavailable case ... and do not also count as `call_failed`"; a budget cut counts; and `classify_all` "evaluates all five from `orca_available`, `truncated`, `orca_rows` and `sources` only". Fixture 1 at `:746` says `sources` holds `orca worker-list R1` with `unscanned` `orca unavailable` and T carries one note; fixture 3 says "`orca_available` True, which the trigger needs". `SweepInput` (`:456`) has `orca_rows`, `sources`, `orca_available`, `truncated`; `OrcaObservation` (`:457`) has `run`; `SourceCoverage` (`:467`) has `unscanned`; so the branch can be evaluated by pure `classify_all`. |
| R3B3-F6 | MAJOR | RESOLVED | `:501` fifth case: `collect` set `unscanned` on the row `ccsession orca-tabs` (folder exists but cannot be listed or read; a missing or empty readable folder is not this case), note `origin unknown: tab map unreadable`, last in the note order. Row named at `:595`; fixture `test_fr010_tab_map_unreadable_older_transcript_unknown` at `:746` (with a control: empty readable folder gives the control result); `collect` test at `:745`; FR-010 row `:771` names the case and the fixtures. No deviation was recorded and `Total: 9 deviations.` holds (see Section 3 for the owner decision recorded in the fix log). |
| R3B3-F7 | MAJOR | RESOLVED | `:501`: "Every Run in `ctx.runs` has that row ... a Run whose `worker-list` was never started because the budget ran out carries `unscanned: time budget reached (90 s)` and counts as `call_failed` for this rule." `:595` says the same. Fixture `test_fr010_run_not_reached_budget_unknown` at `:746` (R2 never started; note `origin unknown: worker list call failed`). The budget values it relies on are at `:367` and `:371`. |
| R3B3-F8 | MAJOR | RESOLVED | Fixture 2 at `:746` is a hand-built `SweepInput` (100 `OrcaObservation` rows, distinct Dispatch ids, `session_join` values different from T's, one matching U, `truncated` True); `page.nextCursor` is "UNVERIFIED until step 1.0a item 3 (open item 5) and is not an input here" (`:891`, `:980` agree); the page-to-flag rule is moved to the `collect` test at `:745` ("a body of 100 rows sets `truncated` True and a body of 99 rows leaves it False"). |
| R3B3-F9 | MAJOR | RESOLVED | `:745` adds `test_collect_worker_list_source_rows_and_truncated` over a fake `_orca`: rows exactly `orca worker-list R1` and `orca worker-list R2`, prefix "the literal word `orca`, not `$ORCA_CLI_COMMAND`", R2 `unscanned` non-null and R1 None, a failed `task-list --run R2` sets `orca task-list R2` only, budget spent before R2 gives `unscanned: time budget reached (90 s)`, unreadable and missing `orca-tabs/`, 100 rows versus 99 rows. `:747` adds the lower-bound line `[Orca rows: 100 shown; total is a lower bound (paging not yet captured)]`, which equals `:614` character for character, and `summary.total_is_lower_bound` True. `:595` states the literal `orca` prefix and that `collect` sets `truncated` at `WORKER_LIST_PAGE` rows (`:548`). |

F_0 result: 9 of 9 RESOLVED. Open BLOCKING or MAJOR from F_0: 0.

Form and totals re-measured on the file now: `Total: 9 deviations.` at `:824` (9 rows `D1` to `D9`); `Total: 23 open items.` at `:1000` (23 rows); em dash and en dash count 0, non-ASCII count 0; `TODO`, `TBD`, `FIXME` count 0; headings 47, same ranges as before (7.2 at `:449`, 7.4 at `:559`, section 11 at `:731`, section 18 at `:1002`); code fences 28 (even); backticks and parentheses balance on every edited line (`:501`, `:502`, `:595`, `:745` to `:747`, `:771`, `:896`, `:979`, `:1030`); every edited table row has the cell count of its table.

## Checks

One row per id of the cycle-0 PASS set (100 ids), tested against the design file on disk now. The Result cell is exactly PASS or FAIL. The Basis cell gives the reason; "(S)" marks a check whose cycle-0 wording named the original research/04 edit or an exact count, where the text now holds that content in the form the F_0 fixes required (see Section 3, table S). Ids V1 and V2 are new checks of mine.

### Checks 1 to 62 (actionability, completeness, crossref, domain, evidence, internal)

| Check id | Result | Basis on disk now |
|---|---|---|
| qa-actionability-report:C1 | PASS | (S) research/04 4.2 edits 1 to 4 are present at `:746`, `:501`, `:771`, `:1030` in the extended form |
| qa-actionability-report:C2 | PASS | the three original `origin unknown:` literals are identical at `:501` and `:746` and keep the SPEC `:104` order |
| qa-actionability-report:C3 | PASS | `orca_available` and `truncated` are named inputs (`:456`, `:501`) |
| qa-actionability-report:C5 | PASS | order unavailable, truncated, call failed is fixed at `:501` and pinned by `:746` part (b) |
| qa-actionability-report:C10 | PASS | row name `orca worker-list <run>` at `:595`, instance names at `:745` and `:746` |
| qa-actionability-report:C16 | PASS | em dash 0, TODO/TBD 0, "four incomplete cases" only at `:1030`, literals at `:501` and `:746` |
| qa-actionability-report:C17 | PASS | `:501` "never idle or Historical, even when its activity is older than the window" |
| qa-completeness-report:C1 | PASS | (S) `:746` "three SPEC incomplete cases (...; each stays visible with `person_started` None and its `origin unknown:` note, never idle or Historical)" |
| qa-completeness-report:C2 | PASS | `:746` keeps the guard case 1 to 4 fixtures and the control (now named "the control") |
| qa-completeness-report:C3 | PASS | `:501` directly before `:502`, with the three literals, the order rule and the never-idle clause |
| qa-completeness-report:C4 | PASS | `:595` names `orca worker-list <run>` and the `call_failed` `unscanned` reason |
| qa-completeness-report:C5 | PASS | (S) `:771` design column names the outage, full page and `call_failed` cases as the three SPEC cases inside five list-incomplete cases |
| qa-completeness-report:C6 | PASS | `:771` test column names "the three SPEC incomplete-case fixtures" |
| qa-completeness-report:C7 | PASS | `:1030` R3-B3 row, including the correction of cycle 2's "four incomplete cases" |
| qa-completeness-report:C8 | PASS | (S) shared Given at `:746` holds every cycle-0 element (`now`, 6 h, T 8 h old, no tab-map entry, joined to no row, path A, `session_join` on every row) plus U |
| qa-completeness-report:C9 | PASS | fixture 1 at `:746`: Given, `orca_available` False, `orca_rows` empty, every Then element |
| qa-completeness-report:C10 | PASS | (S) fixture 2: 100 rows, `truncated`, note, not Historical, `total_is_lower_bound` True; `page.nextCursor` moved out of the Given by F8 and kept as an UNVERIFIED mention |
| qa-completeness-report:C11 | PASS | fixture 3: R1 ok, R2 `call_failed` not call one, `orca call failed (exit 1)`, `orca_available` True, note |
| qa-completeness-report:C12 | PASS | (S) fixture 4 holds both combinations (outage with guard case 1; truncated with call failed) and the order |
| qa-completeness-report:C13 | PASS | "four join-incomplete" at `:771`, `:822`, `:860`, `:1030`; "four incomplete cases" only at `:1030` |
| qa-completeness-report:C14 | PASS | each SPEC `:104` fixture maps to a design fixture; the section map, `:501`, `:595`, `:1030` claims re-derived from the design text (see V1 for the snapshot file) |
| qa-crossref-chain-report:C1 | PASS | headings read: 7.1 `:353`, 7.2 `:449`, 7.3 `:519`, 7.4 `:559`, 11 `:731`, 12 `:756`, 17 `:970`, 18 `:1002`, Fix cycle 3 `:1022` |
| qa-crossref-chain-report:C2 | PASS | the three literals at `:501` equal research/04 4.2 item 2 and the SPEC reasons |
| qa-crossref-chain-report:C3 | PASS | (S) literals identical at `:501` and `:746`; the four original fixture names are still present among seven; Givens of fixtures 2 and 4 changed by F8 and F4 |
| qa-crossref-chain-report:C4 | PASS | defined at `:595`, used at `:501`, instances `orca worker-list R1` and `R2` at `:745` and `:746` |
| qa-crossref-chain-report:C5 | PASS | pointers (7.2, 7.4, 11, 12) and (15.1, 17) in `:1030` all resolve; capture item 8 `:896`, open item 4 `:979` |
| qa-crossref-chain-report:C6 | PASS | `:979` still holds the call-one rule that `:746` cites; closed by 1.0a item 8 = `:896` |
| qa-crossref-chain-report:C7 | PASS | open item 5 `:980` agrees with `:501`, `:548`, `:614`, `:891` |
| qa-crossref-chain-report:C8 | PASS | result kinds at `:374-378`, `collect` at `:392` |
| qa-crossref-chain-report:C9 | PASS | (S) `:771` five list-incomplete (three SPEC plus two) with four join-incomplete; `:502`, `:822`, `:860` speak only of the four join-incomplete cases, so no clash |
| qa-crossref-chain-report:C10 | PASS | `:1030` correction of cycle 2 is accurate in meaning |
| qa-crossref-chain-report:C11 | PASS | (S) research/04 4.2 items 1 to 4 are applied at `:746`, `:501`, `:771`, `:1030` in the extended form |
| qa-crossref-chain-report:C12 | PASS | "four incomplete cases" once at `:1030`; em dash 0; TODO/TBD 0; `:824` and `:1000` totals |
| qa-crossref-chain-report:C13 | FAIL | `r3-b3-mechanical.md` is the cycle-0 snapshot and its per-section table is now wrong for `outage` in 7.2 (snapshot 0, disk 1 at `:501`); see V1 and Section 3 table M. Not a design defect |
| qa-domain-accuracy-report:C1 | PASS | `:501` carries all SPEC reasons with SPEC wording |
| qa-domain-accuracy-report:C2 | PASS | literals and order agree across `:501`, `:746`, research/04 |
| qa-domain-accuracy-report:C3 | PASS | outage = `orca_available` False, covering call one and later calls (`:250-251`, `:286`, `:501`) |
| qa-domain-accuracy-report:C4 | PASS | truncated rule unchanged (`:501`, `:548`) |
| qa-domain-accuracy-report:C7 | PASS | `:501` "A real Run with zero rows whose `task-list` did not fail is complete and is not this case"; `:746` unknown-Run fixture pins the control result |
| qa-domain-accuracy-report:C8 | PASS | unchanged by the fixes; cycle-0 minor F4 stays a note |
| qa-domain-accuracy-report:C9 | PASS | no filter change |
| qa-domain-accuracy-report:C10 | PASS | `:537` and `:517` unchanged |
| qa-domain-accuracy-report:C11 | PASS | (S) edits 1 to 3 reflected at `:746` and `:771`; the three SPEC cases stay distinct from the four join-incomplete cases |
| qa-evidence-quality-report:C1 | PASS | 100-row default at `:299`, `:346`, `:548`, `:614`, `:980` |
| qa-evidence-quality-report:C3 | PASS | `orca call failed (exit <n>)` at `:595` and `:746` |
| qa-evidence-quality-report:C4 | PASS | fixture 3 (R2, not call one) agrees with `:979` |
| qa-evidence-quality-report:C5 | PASS | (S) the 7.2 bullet keeps the research/04 item 2 text for its three cases and extends it; no contradiction |
| qa-evidence-quality-report:C6 | PASS | (S) Thens of fixtures 1 to 3 equal research/04 4.3; Givens amended by F3 and F8 |
| qa-evidence-quality-report:C7 | PASS | all three SPEC fixtures present and named |
| qa-evidence-quality-report:C8 | PASS | `:891` ("cursor or continuation field, if any") and `:980` hedge |
| qa-evidence-quality-report:C12 | PASS | 1030 lines; em dash 0; TODO/TBD 0; each `origin unknown:` SPEC literal on `:501` and `:746`; "four incomplete cases" once; ranges unchanged |
| qa-evidence-quality-report:C13 | PASS | items 4.1 to 4.5 present at `:746`, `:501`, `:771`, `:1030`, `:595` |
| qa-evidence-quality-report:C14 | PASS | "four incomplete cases" only in the `:1030` quotation |
| qa-internal-consistency-report:C1 | PASS | literals spelled the same at `:501`, `:746` |
| qa-internal-consistency-report:C2 | PASS | `orca_available` False matches the `unavailable` kind and `:979` |
| qa-internal-consistency-report:C4 | PASS | `truncated` matches `WORKER_LIST_PAGE` (`:548`), `:980`, `total_is_lower_bound` (`:346`, `:589`) |
| qa-internal-consistency-report:C5 | PASS | fixtures assert `summary.historical` 0 and `total_is_lower_bound` True consistently with `:586-589` |
| qa-internal-consistency-report:C6 | PASS | idle and Historical still need `person_started` True; `:501` makes the five cases None |
| qa-internal-consistency-report:C9 | PASS | no input found that makes one transcript both `origin unknown:` and Historical or idle; the two adjacent paths of cycle 0 (guard scope "in the window", unreadable tab map) are closed at `:502` and `:501` |
| qa-internal-consistency-report:C13 | PASS | `:746`, `:771`, `:1030` agree on "three SPEC cases" and "four join-incomplete cases" |
| qa-internal-consistency-report:C14 | PASS | `:245` no longer states a nonzero exit; `:979` keeps the call-one rule; `:749` "unknown-Run then R2" is the cycle-0 minor R3B3-F15 |
| qa-internal-consistency-report:C15 | FAIL | same cause as qa-crossref-chain-report:C13: the snapshot's Command 2 hit list (`:11`, `:746`, `:771`, `:1030`) now also has `:501`; see V1 and Section 3 table M. Not a design defect |

### Checks 63 to 100 (numbers, spec, template)

| Check id | Result | Basis on disk now |
|---|---|---|
| qa-numbers-metrics-report:C1 | PASS | SPEC `:104` lists 3 incomplete-case fixtures |
| qa-numbers-metrics-report:C2 | PASS | "three SPEC" at `:11`, `:746`, `:771`, `:1030` |
| qa-numbers-metrics-report:C3 | PASS | (S) the three SPEC literals are identical at `:501` and `:746`; the design now has five literals (two added by F1 and F6), also identical in both places (`:501`, `:746`) |
| qa-numbers-metrics-report:C4 | PASS | (S) 7 distinct `test_fr010_*` names on disk; `:746`, `:771`, `:1030` all say seven; the four original names are kept |
| qa-numbers-metrics-report:C5 | PASS | T is 8 h old against a 6 h window in the shared Given (`:746`) |
| qa-numbers-metrics-report:C6 | PASS | `WORKER_LIST_PAGE` 100 at `:548`, `:299`, `:346`, `:746` |
| qa-numbers-metrics-report:C7 | PASS | `:824` "Total: 9 deviations." and 9 rows (`grep -c '^| D[0-9]'` gives 9) |
| qa-numbers-metrics-report:C8 | PASS | `:1000` "Total: 23 open items." and 23 rows; item 4 `:979`, 5 `:980`, 22 `:997`, 23 `:998`; new pointers to capture items 3 and 8 resolve (`:891`, `:896`) |
| qa-numbers-metrics-report:C9 | PASS | dash and non-ASCII counts 0; TODO/TBD/FIXME 0 |
| qa-numbers-metrics-report:C10 | PASS | "four incomplete cases" once (`:1030`); four join-incomplete at `:502`, `:771`, `:822`, `:860`, `:1030` |
| qa-numbers-metrics-report:C11 | FAIL | section ranges match, but the snapshot's per-section table says `outage` 7.2 = 0 and the disk gives 1 (`:501` "the outage note alone"); see V1 and Section 3 table M. Not a design defect |
| qa-numbers-metrics-report:C12 | PASS | adjacent counts unedited: six path-B fixtures (`:771`), nine boundaries (`:745`), five exemptions (`:746`), 8 templates and 7 verbs (`:535`) |
| qa-spec-fidelity-report:C1 | PASS | (S) the 7.2 bullet is no longer byte-identical to research/04 item 2; it contains item 2's three cases and notes and adds two cases and the F5 qualifier |
| qa-spec-fidelity-report:C2 | PASS | SPEC fixture (a) present with the same assertions (`:746`) |
| qa-spec-fidelity-report:C3 | PASS | SPEC fixture (b) present; hand-built per F8 |
| qa-spec-fidelity-report:C4 | PASS | SPEC fixture (c) present and uses a non-first call |
| qa-spec-fidelity-report:C5 | PASS | 8 h against 6 h (`:746`) |
| qa-spec-fidelity-report:C6 | PASS | every fixture asserts not Historical; `summary.historical` 0 stated for fixture 1 and for the first six |
| qa-spec-fidelity-report:C10 | PASS | `:501` order agrees with `:746` part (a) and (b) and with `:502` |
| qa-spec-fidelity-report:C12 | PASS | `:771` names the three SPEC cases and the three SPEC fixtures |
| qa-spec-fidelity-report:C13 | PASS | "four incomplete cases" only in the `:1030` correction |
| qa-spec-fidelity-report:C14 | PASS | four join-incomplete cases and their four guard-case fixtures kept (`:502`, `:746`) |
| qa-spec-fidelity-report:C15 | PASS | the four original fixture names are present (seven names on disk) |
| qa-spec-fidelity-report:C16 | PASS | per-Run rows are an allowed open-ended `sources[].name` use; the 7.4 JSON block (`:563-593`) is not edited and `:595` adds no key |
| qa-template-conformance-report:C1 | PASS | `:501` is still one `- ` bullet between `:500` and `:502` |
| qa-template-conformance-report:C2 | PASS | literals as SPEC `:104`; the SPEC's first three in SPEC order, then the two further notes |
| qa-template-conformance-report:C3 | PASS | 7.4 code block unchanged; `:595` is prose and adds no key |
| qa-template-conformance-report:C4 | PASS | pipe counts: `:745`, `:746`, `:747`, `:749`, `:771`, `:896`, `:1030` have 4 cell pipes, `:979` has 5, matching their tables |
| qa-template-conformance-report:C5 | PASS | dash and non-ASCII counts 0 |
| qa-template-conformance-report:C6 | PASS | TODO/TBD/FIXME 0 |
| qa-template-conformance-report:C7 | PASS | backticks and parentheses are even on every edited line; 28 fences |
| qa-template-conformance-report:C8 | PASS | 47 headings; totals at `:824` and `:1000` by row count |
| qa-template-conformance-report:C9 | PASS | "four incomplete cases" only at `:1030`; four join-incomplete consistent |
| qa-template-conformance-report:C10 | PASS | (S) section 11 cell holds research/04 4.2 item 1 and the four 4.3 names; Givens extended by F3, F4, F8 |
| qa-template-conformance-report:C11 | PASS | (S) `:771` carries the research/04 item 3 content (three SPEC cases, three SPEC fixtures) in extended form |
| qa-template-conformance-report:C12 | PASS | `:1030` has the item 4.2 text and the 3-cell shape of `:1028`, `:1029` |
| qa-template-conformance-report:C13 | PASS | `call_failed` (`:376`), `WORKER_LIST_PAGE` (`:548`), `truncated` and `orca_available` (`:456`), `summary.historical` and `total_is_lower_bound` (`:588-589`) exist |
| qa-template-conformance-report:C14 | PASS | `orca worker-list <run>` and `orca call failed (exit <n>)` agree across `:501`, `:595`, `:746` |

### Checks added by this verifier

| Check id | Result | Basis on disk now |
|---|---|---|
| V1 | FAIL | `phase-outputs/test-results/r3-b3-mechanical.md` was not regenerated after the fix: its pass-rule table says `outage` 7.2 = 0 (disk 1), its Command 2 lists four lines (disk five, `:501` added), its Command 5 prints an old `:595` prefix. Its nine Checks still hold on the current file. MINOR, snapshot only |
| V2 | PASS | no new BLOCKING or MAJOR defect found in the edited text (Section 3) |

Check totals: 100 ids of the cycle-0 PASS set, 97 PASS and 3 FAIL (qa-crossref-chain-report:C13, qa-internal-consistency-report:C15, qa-numbers-metrics-report:C11). All 3 have one cause, the stale snapshot file (V1). Plus V1 (FAIL) and V2 (PASS).

## Section 3: new findings, notes and judgement calls

### New BLOCKING or MAJOR findings

None. I tried to break the edited rule with these inputs and found no path to True or Historical that the five cases and the join guard leave open: a Run id that exists in no Orca (F1 case); a real Run with zero rows and a healthy `task-list` (stays complete, pinned by the control inside the unknown-Run fixture); two Runs where the second is never reached (F7 case); an outage after one good `worker-list` (outage note only, `:501`); a full page together with a failed second Run and an unreadable tab map (part (b) of the order fixture); a missing `orca-tabs/` folder (treated as readable and empty, a stated owner choice). I also checked the fixtures against the guard cases in `:502` one by one (cases 1 and 2 are false in fixtures 1 to 3 and the three added fixtures; part (a) of the order fixture holds both on purpose).

### V1 (MINOR): `r3-b3-mechanical.md` is the cycle-0 snapshot

`phase-outputs/test-results/r3-b3-mechanical.md` was written before the fix. Measured now on the design file:

| Item in the snapshot | Snapshot says | Disk now |
|---|---|---|
| `outage` in 7.2 (`:449-518`) | 0 | 1 (`:501`) |
| Command 2 hit lines | `:11`, `:746`, `:771`, `:1030` | also `:501` |
| Command 5, `:595` text | begins "Each scoped Run's `worker-list` call has its own source row named" | begins "Every Run in `ctx.runs` has its own source row named" |
| every other count and range | as printed | same (`origin unknown:` literals 1/0/1 per section, `orca worker-list <run>` 1/1/0, "four incomplete cases" 0/0/0, sections `:449`, `:559`, `:731`) |

Its nine Checks all still hold on the current file (I re-ran each: outage and "uncaptured continuation" in section 11; the three literals in 7.2 and 11; "four incomplete cases" once, in section 18; the row name in 7.2 and 7.4; dashes 0; TODO/TBD 0; `:824`; `:1000`). The fix log's section "Orchestrator re-check" holds the current output and I confirmed its Command 2 and Command 5 line lists against the disk. Remedy, no design edit: the orchestrator re-runs the item 4.6 commands and overwrites the snapshot. Cycle-0 minor R3B3-F17 (Command 7 prints no captured result) is still open in that file and can be fixed in the same re-run.

### Other MINOR notes (never fail the gate)

| Id | Note | Where |
|---|---|---|
| V3 | The rule needs `collect` to set `unscanned` on `ccsession orca-tabs`, but `read_tab_map` still returns a bare tuple (`:401`) while `:394` says each reader returns data plus a `SourceCoverage` row. How `collect` learns that the folder was unreadable is not stated. A task builder will have to choose (return a pair, or probe the folder in `collect`). | `:394`, `:401`, `:501`, `:595` |
| V4 | The unknown-Run rule relies on `task-list --run <unknown>` being a `call_failed` (nonzero exit). The live evidence quoted in `qa-domain-accuracy-report.md:21` gives `ok` false and `run_not_found` but no exit code. Capture item 8 (`:896`) does ask for "stderr and exit code" and `:501` marks the shape UNVERIFIED, so this is a recorded unknown. No fallback is stated if the exit code turns out to be 0. | `:501`, `:896`, `:979` |
| V5 | Fixture 2 is hand-built with `session_join` on all 100 rows. In a real run only 50 rows get `worker-show` (`:341`), so a real full page also trips guard case 1 and T would also carry `tab map join not observable`. The fixture is correct for its stated input. | `:341`, `:502`, `:746` |
| V6 | "`classify_all` evaluates all five from `orca_available`, `truncated`, `orca_rows` and `sources` only" leaves out `ctx.runs`, which the "every Run in `ctx.runs`" wording also needs. `classify_all` takes `ctx` (`:462`), so nothing is missing; the word "only" is loose. | `:501` |
| V7 | Carried cycle-0 minors R3B3-F10 to R3B3-F25 are untouched, as intended. Of these, F11 (section 18 misquotes cycle 2) and F15 (`:749` "unknown-Run then R2") are the two the fix touched nearest to; both are still minor. | `:1018`, `:1030`, `:749` |

### Table S: checks whose cycle-0 wording named the original research/04 edit or an exact count

These are marked PASS "(S)" above. Read literally, the cycle-0 wording no longer holds because an F_0 fix required the change; the content the check protects is still present. A literal reading would flip them to FAIL, so they are listed here for the orchestrator to overrule if it disagrees.

| Check ids | Cycle-0 wording | Disk now | Cause |
|---|---|---|---|
| qa-spec-fidelity-report:C1, qa-evidence-quality-report:C5 | bullet byte-identical or word for word equal to research/04 item 2 | `:501` has item 2's three cases and notes, then two more cases and the F5 "while `orca_available` is True" qualifier | R3B3-F1, F5, F6, F7 |
| qa-evidence-quality-report:C6, qa-crossref-chain-report:C3, qa-template-conformance-report:C10 | fixtures match research/04 4.3 Given, When, Then | Thens equal for fixtures 1 to 3; Givens now include U, a hand-built page and no `page.nextCursor`; fixture 4 has an exact Given and note list | R3B3-F3, F4, F8 |
| qa-completeness-report:C5, qa-template-conformance-report:C11, qa-crossref-chain-report:C9 | `:771` says "three list-incomplete cases (outage, full page, `call_failed`)" | `:771` says five list-incomplete cases, of which the three SPEC cases are named | R3B3-F1, F6 |
| qa-completeness-report:C8, C10, C12 | shared Given text, `page.nextCursor` in fixture 2, fixture 4 text | shared Given extended; `page.nextCursor` kept only as an UNVERIFIED remark; fixture 4 rewritten | R3B3-F3, F4, F8 |
| qa-numbers-metrics-report:C3, C4 | exactly 3 `origin unknown:` literals; exactly 4 `test_fr010_*` fixtures | 5 literals and 7 fixtures, with the same counts stated in `:501`, `:746`, `:771`, `:1030` | R3B3-F1, F6, F7 |
| qa-actionability-report:C1, qa-crossref-chain-report:C11, qa-domain-accuracy-report:C11, qa-completeness-report:C1, qa-template-conformance-report:C12 | research/04 4.2 edits applied as written | applied and extended | R3B3-F1 to F9 |

### Table M: the three FAIL ids

| Check id | What it tests | Why it fails now |
|---|---|---|
| qa-crossref-chain-report:C13 | the snapshot's section ranges and per-section literal counts are true | `outage` in 7.2 is 1, not 0 |
| qa-internal-consistency-report:C15 | the snapshot matches the file (ranges, hit counts, dashes, TODO/TBD, totals) | Command 2 hit list lacks `:501`; ranges, dash, TODO/TBD and totals do match |
| qa-numbers-metrics-report:C11 | the snapshot's ranges and per-section counts match the file | `outage` in 7.2 is 1, not 0 |

Judgement call: qa-evidence-quality-report:C12 and qa-completeness-report:C14 also read the snapshot, but each tests only claims that still hold (the `origin unknown:` literal lines, "four incomplete cases" once, the section map, `:501`, `:595`, `:1030`), so they stay PASS.

### Owner decisions recorded by the fix agent (not defects)

From `fix-log-cycle1.md` "Owner attention", confirmed present in the design text: a zero-row Run is complete only while its `task-list --run` did not fail (`:501`); the SPEC tab-map reason is enforced as a rule with no deviation (`:501`, `:771`, `Total: 9 deviations.` unchanged); a missing `orca-tabs/` folder counts as readable and empty (`:501`); after an outage only the outage note is attached (`:501`); a Run the budget never reached gets the `worker list call failed` note (`:501`).

## Self-audit

- Tool calls that map to checks: Read of the design at `:9-11`, `:240-289`, `:340-350`, `:366-406`, `:449-520`, `:521-548`, `:590-598`, `:605-614`, `:744-749`, `:771`, `:818-825`, `:858-860`, `:890-900`, `:970-1001`, `:1002-1031`; Grep counts for dashes, TODO/TBD, totals, "in the window", "by one input", `nextCursor`, `tab map unreadable`, the `test_fr010_*` names and the fixture-count phrases; one Bash recount of literals per section range, heading lines, D and open-item rows, pipe, backtick and parenthesis balance of twelve edited lines, fence count and non-ASCII count.
- Not verified: the live Orca behaviour behind R3B3-F1 (no `orca` command allowed; I relied on the output quoted in `qa-domain-accuracy-report.md:20-21`); the exit code of `task-list --run <unknown>` (V4).
- Confidence: Verified 100/100 check ids plus V1 and V2 | Unverifiable 0 | Unchecked 0.
- Tool engagement: Read 23 | Grep 6 | Glob 0 | Bash 3 (read-only `grep`, `sed -n`, `wc`).

## Regression protocol output

Regression detected on Item qa-crossref-chain-report:C13, previously PASS at cycle 0, now FAIL. Halt overrides monotonicity check.
Regression detected on Item qa-internal-consistency-report:C15, previously PASS at cycle 0, now FAIL. Halt overrides monotonicity check.
Regression detected on Item qa-numbers-metrics-report:C11, previously PASS at cycle 0, now FAIL. Halt overrides monotonicity check.

All three come from V1 alone. No design edit is needed. After the orchestrator re-runs the item 4.6 commands and overwrites `r3-b3-mechanical.md`, these three ids read PASS and only they need re-checking. The monotonicity count itself is fine: |F_0| = 9, open BLOCKING or MAJOR now = 0.

Verdict: FAIL
Blocking count: 0
