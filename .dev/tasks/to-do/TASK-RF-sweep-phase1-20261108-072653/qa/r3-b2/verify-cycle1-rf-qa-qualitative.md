# QA Report: R3-B2 gate, cycle 1 verification (rf-qa-qualitative)

**Topic:** `docs/designs/orchestrator-mode.md`, R3-B2 several-rows rule after the cycle-1 fix
**Date:** 2026-11-09
**Phase:** fix-cycle (qualitative re-verification), fix_authorization false
**Fix cycle:** 1 (second review of three)

Design file state read: 1026 lines (`wc -l`), untracked in git (no diff available; compared by reading). Worker bullet is line 498, guard bullet 501, Duplicate Dispatch bullet 509, section 11 rows 741-744, FR-010 row 768, D9 819, SP-29 857, open item 22 at 994, Fix cycle 3 R3-B2 row 1026.

## Overall Verdict: PASS (with minor notes)

All 9 findings of `F_0` are RESOLVED. All 111 checks of the cycle-0 PASS set still PASS. No new BLOCKING or MAJOR finding. Four new MINOR notes are recorded (N1 to N4); they never fail the gate.

## Part 1: Re-check of F_0 (BLOCKING and MAJOR findings)

| Id | Severity | Status | Evidence now on disk |
|---|---|---|---|
| R3B2-F1 | BLOCKING | RESOLVED | `orchestrator-mode.md:498`: "If the transcript has `tail_complete` False, the several-rows rule does not apply and no window is tested: every matching row with an observable window is could not determine with `session start not observable: transcript tail only`, every other matching row is could not determine with `Dispatch time window not observable`, and the transcript is None with the tail-only note when at least one matching row has an observable window, else with `Dispatch time window not observable`. The rest of this paragraph applies only when `tail_complete` is True." Fixture `test_path_b_two_rows_incomplete_tail` at `:743` (both row orders, plus a `dispatch_started` None variant). I worked the fixture by hand: D1 (09:00 to 10:00, observable) and D2 (from 10:30, observable) both get the tail-only note, S is None with it; in the variant D2 has no observable window and gets the window note, D1 and S keep the tail-only note. Matches the sentence. FR-010 row `:768` says "an incomplete tail is handled before the count". |
| R3B2-F2 | BLOCKING | RESOLVED (risk stated for owner sign-off; no behaviour bound added, as the smallest fix allowed) | `:498` last sentences: "First, an open window has no upper bound: while a row stays `pending` or `dispatched`, a later session of the same pane that a person starts ... joins as False, shown as `orca:<dispatch>`, and the worker's own session is None." D9 `:819`: "Two residual path-B cases are new and need the same owner sign-off, which is still pending: a window with no end ... joins the row as False and is shown as `orca:<dispatch>`, not as a person session". SP-29 `:857` and open item 22 `:994` name the same case. Fixture `test_path_b_window_open_row_joins` (`:743`) now says "this join is the first D9 limit, which needs the owner's sign-off at step 1.0b". The claim that the later person session joins is backed by the ccsession facts already in the design (`ccsession:607-613`, a rerun in the same terminal replaces the pane's session). |
| R3B2-F3 | MAJOR | RESOLVED | `:498`: `pane moved to a later session` only "when `first_record_ts` is after the window end"; `session started before this Dispatch window` "when it is before `dispatch_started`" (single-row sentence and the non-holding-row sentence). Same-session-two-Dispatches limit is the "Second" limit at `:498`, repeated in D9 `:819`, SP-29 `:857`, item 22 `:994`. Fixture `test_path_b_live_session_spans_two_dispatches` (`:743`): D1 09:00 to 10:00, D2 from 10:30, S first 09:05; hand-worked, only D1's window holds, so S joins D1, False, `orca:D1`; D2 gets `session started before this Dispatch window`, not `pane moved`. The existing fixtures still hold under the split: fixture 1 (S 10:40 after D1's end gives `pane moved` for D1), fixture 4 (S 11:00 after both ends), fixture 6, and `window_inclusive_bounds` (S 11:00:01 after the end). The claim behind the limit is supported by the Orca bundle error text "pick a terminal that already runs one" (my grep of `orcad-migration-source-retention-B_-OYaBD.js`), see N3. |
| R3B2-F4 | MAJOR | RESOLVED | `:498` reads "(a reused pane or two rows on one terminal handle)". `grep -io 'retr(y|ies)'` finds no hit in the R3-B2 text (hits are lines 311, 638, 661, 674, 711, 744, unrelated). |
| R3B2-F5 | MAJOR | RESOLVED | `:498`: "Rows that share one Dispatch id are merged first (the Duplicate Dispatch bullet below): the merged identity counts as one matching row, has no observable window, and keeps its reason `conflict: duplicate Dispatch rows disagree`." `:509`: "The merge comes before every join rule ... its `dispatch_started`, `dispatch_ended` and `dispatch_status` are None, so it has no observable window." Fixture `test_path_b_duplicate_dispatch_rows_count_once` (`:743`) is well built: unmerged, D1a (open from 09:00) and D1b (09:00 to 10:00) would both hold S at 09:30 and give a `conflict:` outcome; the fixture asserts the opposite. FR-010 row `:768` names the order. |
| R3B2-F6 | MAJOR | RESOLVED | `:501` guard case 2 now says a transcript that matched a tab-map entry of a scoped row and was left unjoined by the tail, window or several-rows rules "carries its pane or tail note only, not the SP-16 line", and "the line is not printed when every affected transcript is one that the second case leaves with its pane or tail note only". Fixtures at `:743` that assert no SP-16 line: `two_windows_hold_session_is_conflict`, `no_matching_window_holds`, `entry_failing_window_note_order`, `two_rows_incomplete_tail`, `duplicate_dispatch_rows_count_once`. (`live_session_spans_two_dispatches` joins S, so case 2 cannot hold.) |
| R3B2-F7 | MAJOR | RESOLVED | `:743` R3-B2 lead-in: "all under path B and all with aware UTC times, on 2026-11-08, with `now` and `collected_start` 12:00, `window` 6 h, `tail_complete` True unless a fixture says otherwise, S `last_record_ts` 11:30, and every row in Run R1 (in `ctx.runs`)". Every S `first_record_ts` used (09:05, 10:05, 10:40, 10:00:00.400, 11:00, 09:30) is not after 11:30 and is not after `now`. |
| R3B2-F8 | MAJOR | RESOLVED | `:743` `test_path_b_two_windows_hold_session_is_conflict` Then: "S is None (`person_started` None) with the same note and no `orca:` row carries S; `Could not determine` does not print the SP-16 line". Every term is defined in DESIGN (`person_started` is a `SessionRow` field, `:461`); the "not True, not idle, not Historical" wording is gone. |
| R3B2-F9 | MAJOR | RESOLVED | `:498`: "A join outcome that makes a row could not determine is applied after rules 1 to 8: it replaces their class with rule `fallback` and keeps the rule's own evidence in `evidence`, so a `completed` row with a settled contract is could not determine, not `finished`." Fixture 1 (`:743`) now gives D1 a settled contract "that rule 6 would class `finished` if the join had succeeded" and asserts "D1 is could not determine with rule `fallback`, not `finished`". An implementation that only adds a note would fail this fixture, which was the cycle-0 objection. |

Open count of F_0: 0.

## Part 2: Re-read of the changed passages as the intended readers

### Developer who must build the sweep package from the DESIGN alone (`:498`, `:501`, `:509`, `:743`)

I traced the algorithm from the text. For a transcript T with a tab-map entry E: the matching rows are the scoped Dispatch rows (after the duplicate merge) whose `session_join` equals E's file name or terminal handle; no match gives the `Orca pane session, not in scoped Runs` note (`:499`); with `tail_complete` False the tail branch decides; otherwise each row is classed as window-holds, after-end, before-start or no-observable-window, and the three hold counts (exactly one, two or more, none) decide the join, with the notes as written. The hold-count split is exhaustive and exclusive, no sentence depends on row position, "the first of the three notes" refers to the order of the list of notes and not to row order, and the merged duplicate row can never hold a session. Ten R3-B2 fixtures plus five R3-B1 window fixtures pin each branch (all 15 fixture names occur exactly once in the file). I could build this without guessing, with the wording gaps in N1 and N2.

### Owner who signs off D9 (`:819`, `:857`, `:994`, fixture `:743`)

D9 now says plainly that it "as first written covers only True becoming None", names two new residual path-B cases, says each in terms of what the owner would see (a person's later session shown as `orca:<dispatch>` and not as a person session; a live session serving two Dispatches joined to the older row while the newer row is could not determine), and says the sign-off is "still pending", repeating "Needs the owner's sign-off at step 1.0b". Open item 22 repeats both cases and the fallback "the classify step does not start until the owner signs off D9 or names a stricter rule". The owner can decide from D9 alone. One consequence the owner is not told is in N2.

## Part 3: New findings

No new BLOCKING or MAJOR finding. Minor notes (never fail the gate, not rechecked later):

| Id | Severity | Location | Note |
|---|---|---|---|
| N1 | MINOR | `orchestrator-mode.md:498` | The scope sentence "The rest of this paragraph applies only when `tail_complete` is True" is wider than intended: two later sentences, the class precedence ("A join outcome that makes a row could not determine is applied after rules 1 to 8 ...") and the note replacement ("... because of the tail, window or several-rows rules ..."), are meant to cover the tail-incomplete outcome too (the second one names "the tail" itself). Read literally, the precedence rule and the `fallback` rule name would not apply to a tail-incomplete row. Impact is small: the class of that row is already fixed by the earlier sentences (could not determine), and no fixture pins its `rule` name. Smallest fix: "The next three sentences (notes of non-holding rows, order independence, the three hold counts) apply only when `tail_complete` is True." |
| N2 | MINOR | `:498`, `:819` | The F9 reading (the join outcome replaces rules 1 to 8) means a row that rule 1 would call waiting on a person, or rule 2 stalled (proved), becomes could not determine when its pane join fails, with its own evidence kept in `evidence`. The fix log notes this for rule 2 (fix-log "Other notes"); D9 does not tell the owner. The design already did this for a single row before the fix (R3-B1), and the direction is the safe one, so it is not a defect, but the owner who signs off D9 should see it. Smallest fix: one clause in D9. |
| N3 | MINOR | `:498`, `:743` | The "second Dispatch to an agent still running in the pane does not start a new session" limit is stated as fact. It rests on the DA report's reading of the Orca bundle (the dispatch error text says "pick a terminal that already runs one"; I confirmed that text in the bundle), which is an inference about the Claude session, not a capture. The fix log chose not to add a step 1.0a capture line for it. If the inference is wrong the limit simply does not occur, so the risk is conservative. Smallest fix: one line in 15.1 item 13 or 4. |
| N4 | MINOR | `:498`, `:509` | "Rows that share one Dispatch id are merged first" and "keeps its reason `conflict: duplicate Dispatch rows disagree`" assume the duplicates disagree; `:509` merges only rows that "differ in state". Two identical rows with one Dispatch id would be counted twice by the several-rows rule. The `session_join` of a merged row whose duplicates carry different values is also unstated. Both are pre-existing edges of the Duplicate Dispatch bullet. |

The cycle-0 MINOR findings R3B2-F10 to R3B2-F24 stay as notes and were not rechecked, except where a check below touches them (F15: Section 1 `:7-11` still lists R3-B2 as open and `:743` still says "the four incomplete cases"; both are R3-B3 or later scope).

One small inaccuracy in the fix log (not in the DESIGN): it says `session started before this Dispatch window` appears "in the Joins bullet (`:498`) and in the fixtures (`:743`) only"; it also appears in the Fix cycle 3 row (`:1026`), which is correct and consistent.

## Checks

Reading applied where the fix cycle deliberately added fixtures and a note literal: a check that counted, compared or matched the earlier fixtures or the earlier text is read as "every earlier item is still present". The seven earlier R3-B2 fixture names are all present, once each, among now ten; fixtures 1, 2, 4 and 6 were edited on purpose (settled contract and `fallback` for 1; the F8 Then for 2; no-SP-16 lines for 4 and 6) and 3, 5 and 7 are unchanged; the Fix cycle 3 R3-B2 row (`:1026`) and the research/04 section 3.3 wording are present as the start of the longer text. I marked such checks "PASS (reading)".

Mechanical facts re-run on disk now: 1026 lines; em dash 0 and en dash 0; no `TODO`, `TBD` or `FIXME` (grep exit 1); `Total: 9 deviations.` at 821 and `Total: 23 open items.` at 997; table rows 741 to 744, 768, 857, 1026 each 4 unescaped pipes (3 cells), 819 has 6 (5 cells, as the D-table header), 994 has 5 (4 cells); `conflict: one pane session matches several Dispatch rows` once each on 498, 743, 1026; `exactly one window holding it` on 819 and 857; `several rows matching one pane session` on 768; ALLOWED_ORCA still 8 templates (`:525-534`).

| Check id | Lens item | Result | Note |
|---|---|---|---|
| qa-actionability-report:C1 | 3.10 | PASS | Every note and where it lands can be listed from `:498` and `:501`. |
| qa-actionability-report:C2 | 3.10 | PASS | Each outcome has a sentence in `:498` and a fixture in `:743`. |
| qa-actionability-report:C6 | 3.10 | PASS | Fixture 4 complete (lead-in setup now states the common items; no-SP-16 clause added). |
| qa-actionability-report:C7 | 3.10 | PASS | Fixture 5 unambiguous (unchanged). |
| qa-actionability-report:C8 | 3.10 | PASS | Fixture 6 unambiguous. |
| qa-actionability-report:C9 | 3.10 | PASS | Fixture 7 unambiguous (unchanged). |
| qa-actionability-report:C10 | 3.10 | PASS | Notes on transcript versus row are stated per outcome, including "the first of the three notes" for none-holds. |
| qa-actionability-report:C14 | 3.10 | PASS (reading) | Names agree; Givens and outcomes of the seven earlier fixtures survive with the deliberate additions. |
| qa-actionability-report:C15 | 3.10 | PASS | `:768`, `:819`, `:857` carry the same wording as `:498` (tail-complete, exactly-one window, merge-first). |
| qa-actionability-report:C16 | 3.10 | PASS | 1026 lines, still the 500-1500 row, so 9 agents. |
| qa-actionability-report:C17 | 3.10 | PASS | Single-row sentences (window, tail, no-window, before-start) do not contradict the several-rows sentences; the tail check comes first in both. |
| qa-completeness-report:C1 | 3.9 | PASS (reading) | Several-rows text still follows the person-rerun sentence, with the three outcomes and the "not added to the transcript" clause. |
| qa-completeness-report:C2 | 3.9 | PASS | Fixture names sit at the required anchor ("a row with no observable start time never joins by path B;") in `:743`. |
| qa-completeness-report:C3 | 3.9 | PASS | FR-010 row `:768` carries the clause. |
| qa-completeness-report:C4 | 3.9 | PASS | D9 `:819` and SP-29 `:857` each carry "exactly one window holding it". |
| qa-completeness-report:C5 | 3.9 | PASS (reading) | `:1026` begins with the research/04 edit 5 wording, then adds the "Gate fixes" sentence; it names 7.2, 11, 12, 13, 14, 17, all of which carry edits. |
| qa-completeness-report:C6 | 3.9 | PASS | m11 note-order sentence present in `:498` and extended with the tail. |
| qa-completeness-report:C7 | 3.9 | PASS (reading) | Fixture 1 present; edited (settled contract, rule `fallback`). |
| qa-completeness-report:C8 | 3.9 | PASS (reading) | Fixture 2 present; Then restated (F8). |
| qa-completeness-report:C9 | 3.9 | PASS | Fixture 3 unchanged. |
| qa-completeness-report:C10 | 3.9 | PASS (reading) | Fixture 4 present; no-SP-16 clause added. |
| qa-completeness-report:C11 | 3.9 | PASS | Fixture 5 unchanged. |
| qa-completeness-report:C12 | 3.9 | PASS (reading) | Fixture 6 present; no-SP-16 clause added. |
| qa-completeness-report:C13 | 3.9 | PASS | Fixture 7 unchanged. |
| qa-completeness-report:C14 | 3.9 | PASS | Each outcome still has a fixture; the three sentences quoted in the mechanical report's outcome table are on disk. |
| qa-completeness-report:C15 | 3.9 | PASS | Mechanical facts above re-run by me. |
| qa-crossref-chain-report:C1 | 3.12 | PASS | Mechanical-report anchors still match: 449-517, 498, 728-752, hit lines 498/743/768/819/857/1015/1026, totals 821 and 997 (file kept at 1026 lines). |
| qa-crossref-chain-report:C2 | 3.12 | PASS | Conflict literal on 498, 743, 1026; `conflict:` on 768; not in 819 or 857. |
| qa-crossref-chain-report:C3 | 3.12 | PASS | `pane moved to a later session` still 498, 743, 1015 (one spelling only). |
| qa-crossref-chain-report:C4 | 3.12 | PASS | `joined by pane: latest session of the pane` one spelling only. |
| qa-crossref-chain-report:C5 | 3.12 | PASS | `Dispatch time window not observable`: one spelling only; item 23 at `:995` still names it. |
| qa-crossref-chain-report:C6 | 3.12 | PASS | "Duplicate Dispatch bullet" is `:509` and says "No row wins by position"; "the bullet that follows this one" is `:499`; the new "Duplicate Dispatch bullet below" also resolves to `:509`. |
| qa-crossref-chain-report:C7 | 3.12 | PASS (reading) | All 10 R3-B2 fixture names occur once each; the seven earlier ones are still there; no collision with the 5 R3-B1 names (each once). |
| qa-crossref-chain-report:C8 | 3.12 | PASS | FR-010 row cites sections that exist and three test files that exist in section 11; Covers cells of `:742` and `:743` carry FR-010. |
| qa-crossref-chain-report:C9 | 3.12 | PASS | `:768`, `:819`, `:857` agree with `:498`. |
| qa-crossref-chain-report:C10 | 3.12 | PASS | `:1026` names 7.2, 11, 12, 13, 14, 17; each carries an edit; m11 is still the note-order point. |
| qa-crossref-chain-report:C11 | 3.12 | PASS | New text cites no DESIGN line number (only SPEC lines and `ccsession:` ranges). |
| qa-crossref-chain-report:C12 | 3.12 | PASS | Open items 22 and 23 and capture items 13 and 4 exist (`:994`, `:995`, `:898`, `:889`) and agree; item 22 "Behaviour until closed" is unchanged. |
| qa-crossref-chain-report:C13 | 3.12 | PASS | Counters re-run by me. |
| qa-domain-accuracy-report:C1 | 3.13 | PASS | One sentence per outcome at `:498`. |
| qa-domain-accuracy-report:C2 | 3.13 | PASS | ccsession cite unchanged (`:574-602`, `:607-613`; the range still ends 3 lines early, cycle-0 minor M-1). |
| qa-domain-accuracy-report:C3 | 3.13 | PASS | `/clear`: S2 joins only inside the window, S1 is None through guard case 4 (`:501`). |
| qa-domain-accuracy-report:C4 | 3.13 | PASS | `/resume` unchanged. |
| qa-domain-accuracy-report:C5 | 3.13 | PASS | Reused pane with closed windows (fixture 1): later row only, earlier row could not determine; no claim now that a retry causes it. |
| qa-domain-accuracy-report:C6 | 3.13 | PASS | Nested `claude -p` unchanged. |
| qa-domain-accuracy-report:C7 | 3.13 | PASS | Plain `claude` unchanged. |
| qa-domain-accuracy-report:C11 | 3.13 | PASS | No sentence depends on row order; shared boundary (S 10:00:00.400 cut to 10:00:00, held by D1's end and D2's start) still gives `conflict:`. |
| qa-domain-accuracy-report:C13 | 3.13 | PASS | Mechanical file facts reproduce (see above). |
| qa-evidence-quality-report:C1 | 3.8 | PASS | Orca-behaviour claims in the R3-B2 text re-listed: the one new one is the second-Dispatch limit, supported by the bundle text I grepped (N3). |
| qa-evidence-quality-report:C2 | 3.8 | PASS | The Dispatch refusal guard is not asserted in the DESIGN; it exists in the bundle (`assignee_handle` and `assignee_pane_key` NOT EXISTS guards, which I read). |
| qa-evidence-quality-report:C4 | 3.8 | PASS | Worker-start rows still not asserted. |
| qa-evidence-quality-report:C5 | 3.8 | PASS | `session_join` value still not pinned (`:497`, `:889`, `:994`). |
| qa-evidence-quality-report:C6 | 3.8 | PASS | "A reused pane" and "two rows on one terminal handle" are supported by the static evidence; "a retry" is removed (F4). |
| qa-evidence-quality-report:C7 | 3.8 | PASS | Bundle re-read by me: the dispatch insert has the `assignee_handle` and `assignee_pane_key` guards; `retryOfDispatchId` and `assigneePaneKey` are present as mapped fields. |
| qa-evidence-quality-report:C9 | 3.8 | PASS | Mechanical claims reproduce: 819 and 857 carry "exactly one window holding it", 768 carries the other phrase, conflict literal on 498/743/1026, totals at 821 and 997. |
| qa-evidence-quality-report:C11 | 3.8 | PASS | `:768`, `:819`, `:857` add no Orca claim beyond `:498`. |
| qa-evidence-quality-report:C12 | 3.8 | PASS | Fixtures state inputs and pin only rules written in 7.2 (N3 for the one assumed given). |
| qa-evidence-quality-report:C13 | 3.8 | PASS (reading) | `:1026` equals research/04 edit 5 as its first part; m11 (review 3 line 137) is still the point settled. |
| qa-evidence-quality-report:C14 | 3.8 | PASS | Gap 4 gate (each outcome has a named fixture) holds. |
| qa-evidence-quality-report:C15 | 3.8 | PASS | The one defect named in cycle 0 is fixed at the cited place (`:498` no longer relies on the point research/04:176 marks UNVERIFIED). |
| qa-internal-consistency-report:C1 | 3.7 | PASS | All inputs read in chunks of at most 150 lines. |
| qa-internal-consistency-report:C2 | 3.7 | PASS | Hold count 0, 1, 2 or more is exhaustive and exclusive for a complete tail; the merged duplicate cannot hold. |
| qa-internal-consistency-report:C3 | 3.7 | PASS | No positional wording; "first of the three notes" is list order. |
| qa-internal-consistency-report:C4 | 3.7 | PASS | Inclusive whole-second window, no window for a terminal row with no end, open window ends at `collected_start`: unchanged and used the same way by all new text and fixtures. |
| qa-internal-consistency-report:C8 | 3.7 | PASS | `:499` and the D9 note rule agree; the notes-instead-of sentence now names the tail, window and several-rows rules (N1 is wording only). |
| qa-internal-consistency-report:C9 | 3.7 | PASS | `:768`, `:819`, `:857` agree with each other and with 7.2. |
| qa-internal-consistency-report:C10 | 3.7 | PASS (reading) | I worked all ten R3-B2 fixtures by hand against `:498`; each gives the stated outcome. |
| qa-internal-consistency-report:C11 | 3.7 | PASS | Branch coverage is wider than in cycle 0: tail-incomplete, no-observable-window (duplicate merge), before-start, after-end, one, two, none. |
| qa-internal-consistency-report:C12 | 3.7 | PASS (reading) | research/04 edits 1 to 5 are all present (`:498`, `:743` at the anchor, `:768`, `:819` and `:857`, `:1026`) with the deliberate fix-cycle additions. |
| qa-internal-consistency-report:C13 | 3.7 | PASS | Counters re-run by me. |
| qa-internal-consistency-report:C14 | 3.7 | PASS | `conflict:` still used only for rules and reasons at 498, 509, 510 and the fixture, FR-010 and log rows; no consumer keys off the prefix. |
| qa-numbers-metrics-report:C1 | 3.11 | PASS (reading) | The seven earlier names are present once each, among ten. |
| qa-numbers-metrics-report:C2 | 3.11 | PASS | The three outcome sentences are each present once in `:498`. |
| qa-numbers-metrics-report:C3 | 3.11 | PASS | Each outcome has a fixture (1; 2 and 3; 4). |
| qa-numbers-metrics-report:C4 | 3.11 | PASS | D9 carries "exactly one window holding it" once. |
| qa-numbers-metrics-report:C5 | 3.11 | PASS | SP-29 carries it once. |
| qa-numbers-metrics-report:C6 | 3.11 | PASS | FR-010 row carries the several-rows rule once and agrees with D9 and SP-29. |
| qa-numbers-metrics-report:C7 | 3.11 | PASS | `Total: 9 deviations.` once (821); D1 to D9 = 9 rows (`:811-819`). |
| qa-numbers-metrics-report:C8 | 3.11 | PASS | `Total: 23 open items.` once (997); rows run to 23 (`:995`). |
| qa-numbers-metrics-report:C9 | 3.11 | PASS | Em dash 0, en dash 0. |
| qa-numbers-metrics-report:C10 | 3.11 | PASS | No `TODO`, `TBD`, `FIXME`. |
| qa-numbers-metrics-report:C11 | 3.11 | PASS | Every R3-B2 time re-worked against the inclusive whole-second rule, including the new ones (09:05, 09:30, 10:40, 10:30 tail cases). |
| qa-numbers-metrics-report:C12 | 3.11 | PASS | The 5 R3-B1 fixtures and the six `test_probes_allowlist.py` fixtures are unchanged and consistent with the rule; the R3-B1 open-row fixture gains only the sign-off clause. |
| qa-numbers-metrics-report:C13 | 3.11 | PASS (reading) | Fixture text equals research/04 3.4 for fixtures 3, 5, 7 and keeps every time value of 1, 2, 4, 6; only the Then of fixture 2 ("S not True, not idle, not Historical") was replaced on purpose (F8). |
| qa-numbers-metrics-report:C14 | 3.11 | PASS (reading) | `:1026` begins with research/04 edit 5 word for word, then the "Gate fixes" sentence; its section list is correct. |
| qa-numbers-metrics-report:C15 | 3.11 | PASS | 1026 lines; 7.2 is 449-517; worker bullet 498; section 11 is 728-752; literal lines 498/743/1015/1026. |
| qa-numbers-metrics-report:C16 | 3.11 | PASS | `:730` unchanged: seven new files, one new command test, three edited test files. |
| qa-numbers-metrics-report:C17 | 3.11 | PASS | 4 + 4 + 1 = 9 agents for the 500-1500 row still holds. |
| qa-numbers-metrics-report:C18 | 3.11 | PASS | Cycle-0 minor M1 is gone: the lead-in now states `collected_start` 12:00, so every open-ended row is deterministic. |
| qa-spec-fidelity-report:C1 | 3.14 | PASS | No outcome yields `person_started` True for a transcript with a tab-map entry: exactly-one False, conflict None, none-holds None, tail-incomplete None, live-session S False. |
| qa-spec-fidelity-report:C2 | 3.14 | PASS | SP-29 "never True" holds for every outcome (`:498` to `:501`). |
| qa-spec-fidelity-report:C3 | 3.14 | PASS | SP-29 other-Run fixture unaffected; `:499` unchanged. |
| qa-spec-fidelity-report:C4 | 3.14 | PASS | `ALLOWED_ORCA` is still 8 templates (`:525-534`); the rule reads only `dispatch_started`, `dispatch_ended`, `dispatch_status` (`:457`). |
| qa-spec-fidelity-report:C5 | 3.14 | PASS | No person session is hidden without disclosure: the within-window and open-window cases are now stated in `:498`, D9, SP-29 and item 22. |
| qa-spec-fidelity-report:C9 | 3.14 | PASS | `:768`, `:819`, `:857` carry the same wording. |
| qa-spec-fidelity-report:C10 | 3.14 | PASS | Each outcome has a fixture. |
| qa-spec-fidelity-report:C11 | 3.14 | PASS (reading) | research/04 edits 1 to 5 present with the deliberate additions. |
| qa-spec-fidelity-report:C12 | 3.14 | PASS | No row wins by position. |
| qa-spec-fidelity-report:C13 | 3.14 | PASS | Counters re-run by me. |
| qa-template-conformance-report:C1 | 3.6 | PASS | Section 11 rows 741 to 744: 4 unescaped pipes each. |
| qa-template-conformance-report:C2 | 3.6 | PASS | FR-010 row `:768`: 4 pipes. |
| qa-template-conformance-report:C3 | 3.6 | PASS | `:1026`: 4 pipes. |
| qa-template-conformance-report:C4 | 3.6 | PASS | D9 `:819` has 6 pipes (5 cells, as the D-table header at `:809`); SP-29 `:857` has 4. |
| qa-template-conformance-report:C5 | 3.6 | PASS | New text in `:498` keeps the note-literal form and cites no DESIGN line numbers. |
| qa-template-conformance-report:C8 | 3.6 | PASS | No em dash or en dash. |
| qa-template-conformance-report:C9 | 3.6 | PASS | No `TODO`, `TBD`, `FIXME`. |
| qa-template-conformance-report:C10 | 3.6 | PASS (reading) | Seven earlier fixture names present, now ten. |
| qa-template-conformance-report:C11 | 3.6 | PASS | Each outcome has one 7.2 sentence and a fixture. |
| qa-template-conformance-report:C12 | 3.6 | PASS | Note literals are spelled identically at every hit (one spelling each in my `grep -o` counts). |
| qa-template-conformance-report:C13 | 3.6 | PASS | 9 deviations and 23 open items unchanged. |
| qa-template-conformance-report:C16 | 3.6 | PASS (with note) | Mechanical report still reproduces on disk; its Command 5 line says "no output expected", but the fix log shows the observed result and I re-ran it (exit 1). |

Totals: 111 of 111 PASS (16 marked "reading", 1 "with note"). 0 FAIL.

Cycle-0 FAILs that the fix addresses, for the record: DA:C8, C9, C10, C12, C14, AC:C3, C4, C5, C11, C12, C13 and EQ:C3 now hold. The remaining cycle-0 FAILs (EQ:C8, EQ:C10, TC:C6, C7, C14, C15, CR:C14 to C18, IC:C5 to C7, SF:C6 to C8, C14, C15) are minor-note checks or were merged into F_0 and were not rechecked as gates.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No Inherited Structural Verdict was in the spawn prompt, so I ran standalone. I used the mechanical report `r3-b2-mechanical.md` only as a pointer and re-ran its facts myself (see Checks).

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Hand-worked all ten R3-B2 fixtures and the five R3-B1 window fixtures against `:498` (hold counts, window arithmetic with the seconds cut, which note goes where). Verified by reading `:498` and `:743` in full.
- Unmerged versus merged duplicate rows: without merge-first, fixture `test_path_b_duplicate_dispatch_rows_count_once` would give a `conflict:` outcome, so the fixture detects an implementation that skips the merge (`:743`, `:509`).
- An implementation that only adds a note (no class change) fails fixture 1 (D1 with a settled contract must be rule `fallback`, not `finished`).
- Found the scope-wording gap N1 by reading the tail sentence against the later "because of the tail" sentence in `:498`.
- Checked the second-Dispatch limit against the Orca bundle (`orcad-migration-source-retention-B_-OYaBD.js`: "pick a terminal that already runs one") and re-read the dispatch-insert guards on `assignee_handle` and `assignee_pane_key`.
- Re-ran the counters (line count, dashes, TODO/TBD/FIXME, totals, pipe counts per table row, literal and fixture-name counts) with `wc`, `grep` and `sed` on the file now.

**Confidence:** Verified: 120/120 (9 findings + 111 checks) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The bundle was checked by greps and one 560-byte excerpt, not read in full; the cycle-1 edit adds no claim that depends on more of it than that.
**Tool engagement:** Read: 15 | Grep: 11 | Glob: 1 | Bash: 5 (all read-only). No web research was needed, so Tavily was not used and no fallback was taken.

## Recommendations

- Proceed. No fix cycle 2 is needed for the blocking list.
- Optional, in any later edit pass: N1 (narrow the tail scope sentence), N2 (one clause in D9 saying a failed pane join demotes a rule 1 or rule 2 row to could not determine, with its evidence kept), N3 (a capture line for "does a second Dispatch keep the same session"), N4 (identical duplicate rows and the merged row's `session_join`).
- Owner action (not a QA item): D9, SP-29 and open item 22 still need the owner's sign-off at step 1.0b on the two residual path-B cases.

## QA Complete

Verdict: PASS
Blocking count: 0
