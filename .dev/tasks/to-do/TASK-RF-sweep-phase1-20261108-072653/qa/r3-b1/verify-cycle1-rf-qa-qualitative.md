# QA Report: R3-B1 gate, cycle 1 verification (rf-qa-qualitative)

**Topic:** orchestrator-mode DESIGN, R3-B1 (session-to-Dispatch time-window rule)
**Date:** 2026-11-09
**Phase:** fix-cycle (doc-qualitative lens, developer-must-build-from-DESIGN reader)
**Fix cycle:** 1
**fix_authorization:** false (no file other than this report was written)
**Design file read:** `docs/designs/orchestrator-mode.md`, 1025 lines (matches fix-log-cycle1.md; `wc -l` = 1025)

## Overall Verdict: PASS

Blocking count: 0 (all 7 cycle-0 findings RESOLVED; no cycle-0 PASS check now fails; no new BLOCKING or MAJOR finding). Minor notes are listed at the end and are not rechecked in later rounds.

## 1. Cycle-0 BLOCKING and MAJOR findings (F_0, |F_0| = 7)

All line numbers are the current numbers in the 1025-line file, each read in this session.

| Id | Status | Evidence (current file) |
|---|---|---|
| R3B1-F1 | RESOLVED | `orchestrator-mode.md:889` (15.1 item 4) now says the static bundle read gives the SQLite form `YYYY-MM-DD HH:MM:SS` UTC "for `dispatchedAt` only", that the form of `completedAt` "is UNVERIFIED and either that form or ISO 8601 is possible, which 7.2 accepts", and that `status` is one of `pending`, `dispatched`, `completed`, `failed`, `circuit_broken`. Independent check: research/04:46 and :53 (the `completed_at` write was not found), and the Orca bundle (`grep -o` finds `dispatchedAt:e.dispatched_at`, `completedAt:e.completed_at`, and the five-value dispatch status list `pending, dispatched, completed, failed, circuit_broken`). The old "present with the shapes ... (SQLite ... UTC)" wording is gone (grep for it finds nothing). |
| R3B1-F2 | RESOLVED | UNVERIFIED is back at all three places: `:457` ("names read statically from the Orca 1.4.245 bundle and UNVERIFIED until step 1.0a item 4 (open item 23)"), `:498` ("are UNVERIFIED until step 1.0a item 4 confirms them (open item 23)"), `:995` (open item 23 starts "UNVERIFIED: that `worker-show` ..."). A grep for `confirm` finds no remaining "confirmed by step 1.0a" (only `:106` the unrelated output_dir re-check and `:498` "confirms them"). Matches research/04:128. |
| R3B1-F3 | RESOLVED | `:743`, fixture `test_path_b_window_open_row_joins`: "row D1 with `session_join` pane P, `dispatch_started` 10:00, `dispatch_ended` None and `dispatch_status` `dispatched`, a tab-map entry from P to session S, transcript S with `first_record_ts` 10:05, `collected_start` 12:00: S joins D1 ...". Same Given as research/04:114. Join cause (P, tab-map P to S) is present. |
| R3B1-F4 | RESOLVED | `:390` `def parse_time(value: object) -> datetime \| None` (never raises, the one time rule of 7.2, used by `read_transcript_tail` and `parse_worker_show` and so by `collect`); `:391` `def parse_worker_show(run: str, list_row: object, show: object \| None) -> OrcaObservation` (never raises, show value wins, sets the three Dispatch fields through `parse_time`); `:400` `read_transcript_tail` comment ends "(times via parse_time)"; `:211` the `probes.py` may-import row lists `datetime`; `:470` names `probes.parse_time` as the owner and says both callers use it; `:742` names `probes.read_transcript_tail` (first three fixtures), `probes.parse_worker_show` (last three) and `probes.parse_time`. A developer can now name, import and test both parsers. |
| R3B1-F5 | RESOLVED | `:470`: "`now`, `collected_start`, `collected_end` and `TranscriptTail.mtime`" are aware UTC `datetime` values, "`collected_start` is read once at the top of `collect`, before the first Orca call, and `collected_end` once when `collect` returns. A naive value never reaches `classify`." `:456` types both as `datetime` (aware UTC) and SPEC `merged-requirements.md:230` confirms those two names are SPEC fields, so the "field names other than the last two are design" remark is true. `:743` says every time in the window fixtures is aware UTC. |
| R3B1-F6 | RESOLVED | `:459` `tail_complete: bool` (True when the read began at byte 0; False when the first partial line was dropped, "every file over 256 KiB"); `:60` GQ-103(3) lists `first_record_ts` and `tail_complete`; `:498` window observable plus `tail_complete` False gives no join, the row is could not determine with note `session start not observable: transcript tail only`, the transcript is None with the same note, and `Dispatch time window not observable` keeps priority because the tail test only applies when the window is observable; `:742` first reader fixture gains `tail_complete` True and the over-256 KiB fixture gains `tail_complete` False; `:743` new fixture `test_path_b_incomplete_tail_has_no_session_start` (window 10:00:00 to 11:00:00, `first_record_ts` 10:30:00, `tail_complete` False: no join, D1 could not determine, S None, never False or True); `:768` FR-010 row says a path-B join also needs "a transcript whose tail is complete"; `:1025` revision row names it. The fixture agrees with the `:498` rule (traced by hand). |
| R3B1-F7 | RESOLVED | `:730`: "Seven new files under `tests/sweep/` ..., one new command test, and edits to three existing test files (`tests/commands/test_routing_plugin_parity.py` must also still pass, unchanged)". Rows `:748` (`test_worker_contract.py`) and `:749` (`test_how_we_work_routing_table.py`, `test_routing_refresh.py`) are the three edited files; `test_routing_plugin_parity.py` is "unchanged, must pass". The "seven new files" count is right: `conftest.py` plus six test rows at `:741` to `:746`. |

Scope note honoured: the forward reference "Several matching rows follow the R3-B2 rule below." is still the only R3-B2 text (`:498`; grep for `R3-B[23]` finds this one hit in the design). No several-rows rule was written. The transcript outcome for an ordinary path-B match that does not join (outside window, no window) is still item 3.1's and is not graded here.

Mechanical re-run by this verifier (not only the fix log): section map unchanged (18 numbered sections plus `### Fix cycle 3`); em-dash 0, en-dash 0, ` -- ` 0; `TODO|TBD|FIXME` none (case-insensitive, rc=1); `Total: 9 deviations.` at `:821`; `Total: 23 open items.` at `:997`; the model-name grep (`first_record_ts|dispatch_started|dispatch_ended|dispatch_status`) hits 9 lines, same as the fix log; table cell shape: rows `:60`, `:457`, `:459`, `:742`, `:743`, `:768`, `:889`, `:995`, `:1025` have the same unescaped-pipe count as their table headers; `git merge-base --is-ancestor 5dc29d23 origin/master` rc=0.

## 2. Checks

The 129 check ids of the cycle-0 PASS set (`cycle-ledger.md`, row 0) re-checked against the file as it is now. Line numbers are current ones (the fix moved most of them by +2; a moved line number on a true claim is minor and does not change a result). Three judgement calls apply to several rows and are stated once here, then pointed to as J1 to J3:

- J1 (verbatim-to-research/04 checks): the fix deliberately departs from research/04 section 2.2 where the cycle-0 findings required it. I treated "matches research/04" as "every difference from research/04 is traceable to one of F1 to F7 and nothing else differs". Differences found: edit 1 "confirmed" became UNVERIFIED (F2, backed by research/04:128); edits 2, 5 and 6 gain `tail_complete` (F6); edit 3 gains the `parse_time` owner sentence (F4) and the aware-UTC sentence (F5); edit 4 gains the incomplete-tail sentences (F6) and UNVERIFIED (F2); edit 7 narrows the shape claim to `dispatchedAt` (F1, backed by research/04:53); edit 8 starts "UNVERIFIED:" (F2); the edit 9 row is longer (F4 to F6); fixture 7 Given gains P and the tab-map entry (F3). No other difference.
- J2 (fixture counts): `test_classify.py` now names five R3-B1 window fixtures, not four, because F6 added `test_path_b_incomplete_tail_has_no_session_start`. The four required by research/04:114-117 and research/09 Gap 4 are all present with unchanged values. The design states no count of "four" for them (my grep for four/ten/five/six fixture phrases finds only "the six reader and parser fixtures" at `:768`, which is still true).
- J3 (mechanical file): `phase-outputs/test-results/r3-b1-mechanical.md` is the cycle-0 snapshot (1023-line design, line numbers 2 lower). Its claims were true of that file, and the same names, counts and totals reproduce on the 1025-line file (my own re-run, and the fix log's "Orchestrator re-check"). I treated the stale line numbers as minor.

| Check id | Result | Evidence now |
|---|---|---|
| qa-actionability-report:C1 | PASS | `:470` aware UTC for parsed Orca and transcript times |
| qa-actionability-report:C3 | PASS | `:498` "both ends included" |
| qa-actionability-report:C4 | PASS | `:498` "cut to whole seconds"; fixture `:743` pins direction (10:00:00.700 and 11:00:00.400 join, 11:00:01.000 does not) |
| qa-actionability-report:C5 | PASS | `:498` open only for `pending` or `dispatched`; other status with no end has no window |
| qa-actionability-report:C6 | PASS | `:498`, `:995`, fixture `test_path_b_row_without_start_has_no_window` `:743` |
| qa-actionability-report:C7 | PASS | `:459`, `:498` incomplete-tail rule, fixtures `:742` and `:743`; stronger than in cycle 0 |
| qa-actionability-report:C9 | PASS | the nine research/04 edits are present at `:457`, `:459`, `:470`, `:498`, `:400`, `:60`, `:889`, `:995`, `:1025`; cycle-2 row `:1015` reads "earliest `timestamp` in the transcript tail"; see J1 |
| qa-actionability-report:C10 | PASS | every window and reader fixture at `:742` and `:743` has Given, trigger and expected value, including the new one |
| qa-actionability-report:C11 | PASS | pure `classify` can evaluate the window from model fields: `first_record_ts` and `tail_complete` (`:459`), `dispatch_*` (`:457`), `collected_start` (`:456`) |
| qa-actionability-report:C12 | PASS | `:400`, `:60`, `:889`, `:995`, `:1025` agree on the names |
| qa-actionability-report:C13 | PASS | counts reproduce on the 1025-line file; see J3 |
| qa-actionability-report:C14 | PASS | `:498` vs `:995` vs `:742`/`:743`: no contradiction; the incomplete-tail rule and its fixture agree; the ordinary non-join transcript outcome is item 3.1 |
| qa-completeness-report:C1 | PASS | edit 1 present, `:457` |
| qa-completeness-report:C2 | PASS | edit 2 present, `:459` |
| qa-completeness-report:C3 | PASS | edit 3 present, `:470` |
| qa-completeness-report:C4 | PASS | edit 4 present, `:498` |
| qa-completeness-report:C5 | PASS | edit 5 present, `:400` |
| qa-completeness-report:C6 | PASS | edit 6 present, `:60` |
| qa-completeness-report:C7 | PASS | edit 7 present, `:889` |
| qa-completeness-report:C8 | PASS | edit 8 present, `:995` |
| qa-completeness-report:C9 | PASS | edit 9 present, `:1019` to `:1025`; cycle-2 wording `:1015` |
| qa-completeness-report:C10 | PASS | fixture 1 named at `:742` |
| qa-completeness-report:C11 | PASS | fixture 2 named at `:742` |
| qa-completeness-report:C12 | PASS | fixture 3 named at `:742`, values 07:00:00Z and 08:00:00Z unchanged |
| qa-completeness-report:C13 | PASS | fixture 4 named at `:742` |
| qa-completeness-report:C14 | PASS | fixture 5 named at `:742` |
| qa-completeness-report:C15 | PASS | fixture 6 named at `:742` |
| qa-completeness-report:C17 | PASS | fixture 8 `test_path_b_window_inclusive_bounds`, `:743` |
| qa-completeness-report:C18 | PASS | fixture 9 `test_path_b_terminal_row_without_end_has_no_window`, `:743` |
| qa-completeness-report:C19 | PASS | fixture 10 `test_path_b_row_without_start_has_no_window`, `:743` |
| qa-completeness-report:C20 | PASS | em-dash 0, no TODO/TBD, `:821` 9 deviations, `:997` 23 open items (own re-run) |
| qa-completeness-report:C21 | PASS | pre-fix wording gone: no "present with the shapes", no "confirmed by step 1.0a", no "earliest `timestamp` in the transcript tail must fall"; the remaining "earliest" hits (`:9`, `:459`, `:742`, `:743`, `:1015`) are history, the definition or fixture text |
| qa-completeness-report:C22 | PASS | `:768` FR-010 row traces the six parser fixtures; `:742` Covers cell holds FR-010 |
| qa-crossref-chain-report:C1 | PASS | sections 2.2, 7.1, 7.2, 11, 12, 15.1, 17, 18 exist (heading grep) and hold the edits |
| qa-crossref-chain-report:C2 | PASS | names present in 7.1 (`:391`, `:400`), 7.2 (`:457`, `:459`, `:498`), 2.2 (`:60`), 11 (`:742`, `:743`), 18 (`:1025`); Orca source names at `:457`, `:742`, `:889`, `:995` |
| qa-crossref-chain-report:C3 | PASS | `:60` lists the names, points to `models.py` (7.2); `tail_complete` and the rest exist in the table |
| qa-crossref-chain-report:C4 | PASS | `:457` cites section 2.2 path A or B (GQ-108 `:65`), step 1.0a item 4 (`:889`), open item 23 (`:995`) |
| qa-crossref-chain-report:C5 | PASS | `:498` cites item 4, item 23, `collected_start` (`:456`), `pending`/`dispatched`, 50-call cap (`Budget(shows=50)` `:367`) |
| qa-crossref-chain-report:C6 | PASS | `:470` "the 'Unknown row schema' bullet below" resolves to `:508`; `:742` "per the unknown row schema rule" |
| qa-crossref-chain-report:C7 | PASS | `:400` comment, `:459` row and `:742` reader fixtures agree, now including `tail_complete` |
| qa-crossref-chain-report:C8 | PASS | fixture arithmetic unchanged and correct (10:00:00.700 and 11:00:00.400 in; 11:00:01.000 out; open row to 12:00); six plus five names, see J2 |
| qa-crossref-chain-report:C9 | PASS | `:768` cites `sweep/test_probes_allowlist.py` and "six" |
| qa-crossref-chain-report:C11 | PASS | `:889` Feeds cell cites the path-B time window and open item 23; row 13 (`:898`) and open item 22 (`:994`) agree; see J1 |
| qa-crossref-chain-report:C12 | PASS | open item 23 `:995`, "Closed by" step 1.0a item 4 exists, behaviour agrees with `:498`, 23 rows; see J1 |
| qa-crossref-chain-report:C13 | PASS | see J1 |
| qa-crossref-chain-report:C14 | PASS | `:1021` cites master `5dc29d23`, an ancestor of `origin/master` (rc=0); row text cites existing sections |
| qa-crossref-chain-report:C16 | PASS | `:1015` reads "the earliest `timestamp` in the transcript tail" |
| qa-crossref-chain-report:C20 | PASS | `:821`, `:997`, em-dash 0, no TODO/TBD |
| qa-crossref-chain-report:C21 | PASS | see J3 |
| qa-crossref-chain-report:C22 | PASS | Python 3.10 `fromisoformat` rejects `Z` (reason at `:470` unchanged); status set re-confirmed in the bundle (`pending`, `dispatched`, `completed`, `failed`, `circuit_broken`) |
| qa-crossref-chain-report:C23 | PASS | section 1 `:9` still states the defect as found; D9 `:819` and SP-29 `:857` say "a path-B join also needs the Dispatch row's time window", which the new rule extends and does not contradict |
| qa-domain-accuracy-report:C1 | PASS | `:470` `Z` rewritten to `+00:00` first, with the 3.10 reason |
| qa-domain-accuracy-report:C2 | PASS | `:470` SQLite form, no zone, read as UTC |
| qa-domain-accuracy-report:C3 | PASS | `:470` result is aware UTC |
| qa-domain-accuracy-report:C7 | PASS | inclusive bounds and arithmetic unchanged |
| qa-domain-accuracy-report:C8 | PASS | `:498`: skew or the seconds cut can only move a session to could not determine or False; the new incomplete-tail branch also ends in could not determine and None, never True |
| qa-domain-accuracy-report:C9 | PASS | `.mmmZ` transcript form, `:33`, and the out-of-order `is_minimum` fixture `:742` |
| qa-domain-accuracy-report:C12 | PASS | `pending`/`dispatched` open-window set matches the bundle status list |
| qa-domain-accuracy-report:C14 | PASS | six reader/parser fixtures and four window fixtures present; see J2 |
| qa-domain-accuracy-report:C15 | PASS | `:889` and `:995` agree with research/04 edits 7 and 8 as corrected by F1 and F2; see J1 |
| qa-domain-accuracy-report:C16 | PASS | see J3 |
| qa-evidence-quality-report:C1 | PASS | I read every edited region (`:1` to `:80`, `:200` to `:230`, `:353` to `:523`, `:726` to `:776`, `:805` to `:906`, `:965` to `:1025`) |
| qa-evidence-quality-report:C2 | PASS | `:457` field names and nesting still trace to research/04:46 |
| qa-evidence-quality-report:C3 | PASS | `:457` "None for a row with no `worker-show` result" ties to the 50-call cap (research/04:54, `:367`) |
| qa-evidence-quality-report:C4 | PASS | `:470` forms trace to research/04:51 and :129; no widening |
| qa-evidence-quality-report:C6 | PASS | `:889` status set and `:498` open-window rule trace to research/04:50 and the bundle |
| qa-evidence-quality-report:C10 | PASS | `:30` version string `1.4.245-aidev02.780594c521aa` unchanged |
| qa-evidence-quality-report:C12 | PASS | fixture shapes unchanged apart from the F3 and F6 additions; the cycle-0 minor note F19 stands as a note |
| qa-evidence-quality-report:C13 | PASS | `:1015` and `:1025` make no claim that is not in the design (each clause of `:1025` checked against 7.1, 7.2, 4, 2.2, 15.1, 17, 11, 12) |
| qa-evidence-quality-report:C14 | PASS | only the permitted R3-B2 forward reference exists |
| qa-internal-consistency-report:C1 | PASS | names and types match between `:457`, `:459`, `:498`, `:60`, `:742`, `:743` |
| qa-internal-consistency-report:C2 | PASS | `session_join`, `file_name`, `terminal_handle`, `session_id` in `:457`, `:460`, `:459` |
| qa-internal-consistency-report:C3 | PASS | `:456` now types `collected_start` and `collected_end` (the cycle-0 minor IC-2 is also closed) |
| qa-internal-consistency-report:C4 | PASS | `:400` names `first_record_ts`, `last_record_ts`, `tail_complete` |
| qa-internal-consistency-report:C5 | PASS | `:60` list equals the model rows |
| qa-internal-consistency-report:C6 | PASS | `:889` maps to `:457` |
| qa-internal-consistency-report:C7 | PASS | `:995` and `:498` agree for a no-window row (note `Dispatch time window not observable`) |
| qa-internal-consistency-report:C8 | PASS | `:1025` names the four fields plus `tail_complete` |
| qa-internal-consistency-report:C9 | PASS | sections 11 and 12 use the model names; `tail_complete` is used the same way at `:459`, `:498`, `:742`, `:743` |
| qa-internal-consistency-report:C10 | PASS | the 5 UNVERIFIED hits that touch the Dispatch times (`:457`, `:498`, `:889`, `:995`, `:1025`) say the same thing; the other 4 (`:49`, `:65`, `:520`, `:956`) are unrelated |
| qa-internal-consistency-report:C11 | PASS | `:9` still describes the defect as found |
| qa-internal-consistency-report:C12 | PASS | see J1 |
| qa-internal-consistency-report:C13 | PASS | time rule at `:470` and fixture forms (SQLite, `...123Z`, `...Z`, "yesterday") agree |
| qa-internal-consistency-report:C14 | PASS | window rule agrees with all five window fixtures (each traced by hand) |
| qa-internal-consistency-report:C15 | PASS | 1025 lines, 9 deviations, 23 open items, no em-dash, no TODO/TBD; see J3 |
| qa-internal-consistency-report:C16 | PASS | None-handling of each nullable field is stated; `first_record_ts` None is still not stated (cycle-0 minor F9, left as a note) |
| qa-numbers-metrics-report:C1 | PASS | six named fixtures at `:742`; "six" at `:768` |
| qa-numbers-metrics-report:C2 | PASS | four required window fixtures present; five named in total; see J2 |
| qa-numbers-metrics-report:C3 | PASS | `:821` Total: 9 deviations; D1 to D9 rows `:811` to `:819` |
| qa-numbers-metrics-report:C4 | PASS | `:997` Total: 23 open items; rows 1 to 23 `:973` to `:995` |
| qa-numbers-metrics-report:C5 | PASS | 256 KiB is the figure in 7.1 (`:400`), 7.2 (`:459`, `:513`), 7.3 (`:546`), `:742` |
| qa-numbers-metrics-report:C6 | PASS | em-dash 0, en-dash 0 |
| qa-numbers-metrics-report:C7 | PASS | per-section name rule holds: 7.1 has `first_record_ts` (`:400`) and the three `dispatch_*` (`:391`); 7.2, 2.2, 18 and 11 hold all four; 15.1 and 17 hold the three source names |
| qa-numbers-metrics-report:C8 | PASS | names reproduce at `:60`, `:391`, `:400`, `:457`, `:459`, `:498`, `:742`, `:743`, `:1025` (9 lines); see J3 |
| qa-numbers-metrics-report:C9 | PASS | fixture values still equal research/04 section 2.3 |
| qa-numbers-metrics-report:C10 | PASS | inclusive-window arithmetic unchanged and correct |
| qa-numbers-metrics-report:C11 | PASS | "all three are None" (`:457`) and "the three fields" (`:498`) are the same three |
| qa-numbers-metrics-report:C12 | PASS | 8 templates and 7 verbs re-read at `:525` to `:534`; 9 rules; 7 new test files; 4 join-incomplete cases (`:501`); 13 capture items; 41 FR/NFR rows in section 12 (26 + 15, grep count 41); the F7 count at `:730` is now right |
| qa-numbers-metrics-report:C13 | PASS | four FR-008 inputs, two FR-009 cases, five exemptions still in the `:743` cell |
| qa-numbers-metrics-report:C14 | PASS | section 8 count untouched by the fix |
| qa-numbers-metrics-report:C16 | PASS | no DESIGN self-line pointer in any new or changed text (grep `lines? N` over every changed line finds only SPEC pointers: SPEC 231, 556, 229, 297, 440, 444, 236, 259) |
| qa-numbers-metrics-report:C18 | PASS | project floor `>=3.10` unchanged; reason at `:470` unchanged |
| qa-spec-fidelity-report:C1 | PASS | `ALLOWED_ORCA` re-read at `:525` to `:534`: 8 templates, 7 verbs, untouched |
| qa-spec-fidelity-report:C2 | PASS | `FORBIDDEN_TOKENS` `:536` unchanged; `parse_worker_show` adds no verb, flag or token |
| qa-spec-fidelity-report:C3 | PASS | Dispatch times come from the existing `worker-show` template (`:528`); `first_record_ts` and `tail_complete` come from the existing transcript read (`:400`) |
| qa-spec-fidelity-report:C4 | PASS | D9 row `:819` not edited this cycle |
| qa-spec-fidelity-report:C5 | PASS | guard bullets `:499` to `:501` not edited; the `:498` change only adds a more conservative case (no join, could not determine) |
| qa-spec-fidelity-report:C6 | PASS | SP-29 row `:857`; path B still cannot yield True (`:498` ends in False or could not determine) |
| qa-spec-fidelity-report:C7 | PASS | see J1 (every difference from research/04 lines 87-95 is traced to F1 to F7) |
| qa-spec-fidelity-report:C9 | PASS | field names found in the 1.4.245 bundle (`dispatchedAt:e.dispatched_at`, `completedAt:e.completed_at`) |
| qa-spec-fidelity-report:C10 | PASS | status set confirmed in the bundle |
| qa-spec-fidelity-report:C11 | PASS | JSON v1 section 7.4 untouched; `tail_complete` appears only at `:60`, `:400`, `:459`, `:498`, `:742`, `:743`, `:768`, `:1025`, never in 7.4 |
| qa-spec-fidelity-report:C12 | PASS | `:821`, `:997`, em-dash 0, no TODO/TBD (own re-run, rc=1) |
| qa-spec-fidelity-report:C13 | PASS | no R3-B2 or R3-B3 content beyond the forward reference `:498`; `### Fix cycle 3` has the single R3-B1 row `:1025` |
| qa-spec-fidelity-report:C14 | PASS | `:768` and the `:742` Covers cell are the research/09 Gap 4 recommendation |
| qa-template-conformance-report:C1 | PASS | `:60` has 5 unescaped pipes, same as header `:55` |
| qa-template-conformance-report:C2 | PASS | `:457` has 3, same as header `:453` |
| qa-template-conformance-report:C3 | PASS | `:459` has 3, same as header `:453` |
| qa-template-conformance-report:C4 | PASS | `:742` and `:743` have 4 each, same as header `:739` |
| qa-template-conformance-report:C5 | PASS | `:889` has 4 (header `:884` 4); `:995` has 5 (header `:971` 5) |
| qa-template-conformance-report:C6 | PASS | header `:1023` 4 pipes, separator `:1024`, row `:1025` 4 pipes, blank line `:1022` before the table |
| qa-template-conformance-report:C7 | PASS | intro `:1021` unchanged |
| qa-template-conformance-report:C8 | PASS | heading list re-run: unchanged 18 numbered sections plus `### Fix cycle 3` |
| qa-template-conformance-report:C9 | PASS | em-dash 0, en-dash 0, ` -- ` 0 |
| qa-template-conformance-report:C10 | PASS | `TODO`, `TBD`, `FIXME` absent, case-insensitive (rc=1) |
| qa-template-conformance-report:C11 | PASS | marketing-word grep: no hits |
| qa-template-conformance-report:C12 | PASS | new text keeps the surrounding short-declarative style; the `:498` bullet is long, as before (cycle-0 minor F14) |
| qa-template-conformance-report:C13 | PASS | all nine anchors present; see J1 and J2 |
| qa-template-conformance-report:C14 | PASS | `:821` and `:997` |

Totals: 129 of 129 cycle-0 PASS-set checks still PASS (0 FAIL). The 26 cycle-0 checks that were FAIL-marked are not in the PASS set; the 7 blocking ones are the findings in section 1, and the rest are the minor notes F8 to F24, which are not rechecked.

## 3. New findings from the cycle-1 edits

No new BLOCKING or MAJOR finding. Minor notes only (never fail the gate, not rechecked later). I read each changed passage as a developer who must build the sweep package from the DESIGN alone: `parse_time`, `parse_worker_show`, the aware-UTC rule, the window rule and the incomplete-tail rule can all be implemented and tested from the text as it stands.

| Id | Severity | Location | Note |
|---|---|---|---|
| V1-m1 | MINOR | `:498` | The reason given for the incomplete-tail rule has "later" and "earlier" the wrong way round: "it can place a later session inside the window or an earlier one outside it". The tail's first record is never earlier than the true session start, so truncation can make an earlier-started session look as if it began inside the window (false join) or make the worker's own session look as if it began after the window end (false "moved"); it cannot move a later session inside. The rule itself (no join, could not determine) is right and the fixture is right, so a builder is not misled about behaviour. Suggested wording: "so it can place an earlier session inside the window or the worker's own session outside it". |
| V1-m2 | MINOR | `:498`, `:743` | When the window is observable and `tail_complete` is False and `first_record_ts` is also outside the window, both the incomplete-tail note and `pane moved to a later session` could apply. The text gives the incomplete-tail sentence first and no fixture covers this case, so precedence rests on sentence order. Only the note text differs; the outcome (no join, could not determine, transcript None) is the same either way. Suggested: one clause stating the incomplete-tail note wins, plus one fixture row. |
| V1-m3 | MINOR | `:459`, `:498` | Effect to know before building: `tail_complete` is False for every file over 256 KiB, and a worker transcript of that size is common, so path B will join only short sessions and many workers will end as could not determine (with guard case four then making unjoined transcripts None). That is safe (never True) and is what F6 asked for. If the owner wants path B to be useful for long sessions, a later change could read the first record of the file separately; this is a design option, not a defect of the fix. |
| V1-m4 | MINOR | `:213` | `commands.py` creates `now` (aware UTC) and `_parse_window` returns a `timedelta`, but its may-import row (`:213`) lists only `click`, `json`, `os` besides the package modules. This was already so before cycle 1; the F5 sentence makes it more visible. |
| V1-m5 | MINOR | `:819`, `:857` | D9 and SP-29 say a path-B join "also needs the Dispatch row's time window" but do not mention the complete-tail condition now at `:768`. They are shorter, not contradictory. |
| V1-m6 | MINOR | `:391` | "sets `dispatch_started`, `dispatch_ended`, `dispatch_status` through `parse_time`": only the first two are times; `dispatch_status` is copied as a string. Wording only. |

The cycle-0 minor notes F8 to F24 are unchanged by this verification and are not rechecked.

## Self-Audit

**(a) Reliance list (no Inherited Structural Verdict block was in the spawn prompt, so no structural PASS was inherited):**
- Relied on the cycle-0 PASS set only as the list of ids to re-test. For every id I re-read the current text; none was passed on the strength of its cycle-0 verdict.

**(b) Independent semantic checks (at least one required):**
- Incomplete-tail rule against its fixture and against the "never True" claim: read `:459`, `:498`, `:743`, traced the new fixture by hand. This found V1-m1 (inverted rationale) and V1-m2 (note precedence), which no earlier report had.
- Window arithmetic: re-derived 10:00:00.700, 11:00:00.400 and 11:00:01.000 against 10:00:00 to 11:00:00 inclusive, and the open row (10:05 against 12:00).
- Dispatch status set and field names: `grep -o` in the installed Orca 1.4.245 bundle found `dispatchedAt:e.dispatched_at`, `completedAt:e.completed_at` and the five-value status list.
- SPEC cross-check for `collected_start` and `collected_end`: `merged-requirements.md:230` names both, so "field names other than the last two are design" at `:456` is true.
- Table shape: counted unescaped pipes in every edited row and its header (`:55`/`:60`, `:453`/`:457`/`:459`, `:739`/`:742`/`:743`, `:757`/`:768`, `:884`/`:889`, `:971`/`:995`, `:1023`/`:1025`).
- Totals and anchors: `Total: 9 deviations.` (`:821`), `Total: 23 open items.` (`:997`), 41 FR/NFR rows in section 12, `git merge-base --is-ancestor 5dc29d23 origin/master` rc=0.

**Confidence:** Verified: 136/136 (7 findings + 129 checks) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: about 26 | Grep: 11 | Glob: 1 | Bash: 4 (three batches of read-only greps/counts plus one pipe count). No Python was run.
**Not independently re-run:** the Orca bundle was grepped for names and the status list only; the `completed_at` write sites were not re-traced (the design correctly leaves that UNVERIFIED).

Verdict: PASS
Blocking count: 0
