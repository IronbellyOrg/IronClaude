# QA Report: R3-B2 gate, cycle 1 verification (rf-qa)

**Topic:** R3-B2, several scoped Dispatch rows match one pane session (`docs/designs/orchestrator-mode.md`)
**Date:** 2026-11-08
**Phase:** fix-cycle (verifier, `fix_authorization: false`)
**Fix cycle:** 1 (second review of three)
**Files edited by this verifier:** none besides this report.

Inputs read: `consolidated-findings-cycle0.md` (F_0), `fix-log-cycle1.md`, `cycle-ledger.md` (cycle-0 PASS set, 111 ids), the `## Checks` table of each of the nine `qa-*-report.md` files, DESIGN `docs/designs/orchestrator-mode.md` (1026 lines; 7.2 at 449-517, section 11 at 728-752, rows 768, 819, 857, 994, 1026), research/04 lines 120-176, research/09 Gap 4 (lines 139-175), `phase-outputs/test-results/r3-b2-mechanical.md`. The DESIGN is untracked in git (`??`), so there is no diff to read; every verdict below comes from the file as it is on disk now.

Reading applied to count-style checks: the cycle-1 fix deliberately added three fixtures (`test_path_b_two_rows_incomplete_tail`, `test_path_b_live_session_spans_two_dispatches`, `test_path_b_duplicate_dispatch_rows_count_once`), one note literal (`session started before this Dispatch window`), a lead-in with setup values, a "Gate fixes" sentence on the section 18 R3-B2 row, and a tail-complete clause in D9 and SP-29. A check that counted the seven earlier fixtures, or compared a row word for word with research/04, is read as "every earlier item is still present, nothing earlier was removed except what a F_0 finding asked to remove". Where I apply that reading the Checks table says "(reading)".

## Overall Verdict: PASS

All 9 findings of F_0 are RESOLVED. All 111 checks of the cycle-0 PASS set still pass. No new BLOCKING or MAJOR finding. |F_1| = 0 against |F_0| = 9, so the monotonicity guard is satisfied and no regression is present.

## Re-check of F_0 (BLOCKING and MAJOR findings)

### R3B2-F1 (BLOCKING): RESOLVED
- `docs/designs/orchestrator-mode.md:498`: "If the transcript has `tail_complete` False, the several-rows rule does not apply and no window is tested: every matching row with an observable window is could not determine with `session start not observable: transcript tail only`, every other matching row is could not determine with `Dispatch time window not observable`, and the transcript is None with the tail-only note when at least one matching row has an observable window, else with `Dispatch time window not observable`. The rest of this paragraph applies only when `tail_complete` is True." (grep: `applies only when \`tail_complete\` is True` occurs once.)
- Fixture `test_path_b_two_rows_incomplete_tail` at `:743` (both row orders, a variant with `dispatch_started` None, no SP-16 line). I worked it against the rule by hand: D1 09:00-10:00 and D2 from 10:30 both have observable windows, so both get the tail-only note and S is None with it; with D2's start None, D2 gets the window note and S keeps the tail-only note. Matches.
- `:768` (FR-010 row) says the incomplete tail is handled before the count.

### R3B2-F2 (BLOCKING): RESOLVED
- `:498`: "First, an open window has no upper bound: while a row stays `pending` or `dispatched`, a later session of the same pane that a person starts ... falls inside the window and joins as False, shown as `orca:<dispatch>`".
- `:819` (D9): "D9 as first written covers only True becoming None. Two residual path-B cases are new and need the same owner sign-off, which is still pending: a window with no end ...". `:857` (SP-29) and `:994` (open item 22) carry the same case; item 22 keeps "the classify step does not start until the owner signs off D9 or names a stricter rule".
- Fixture `test_path_b_window_open_row_joins` at `:743` now says the join "is the first D9 limit, which needs the owner's sign-off at step 1.0b".
- The finding's smallest fix was to state the residual risk so the owner signs it off. That is done in all four places; the sign-off itself stays pending by design and is gated at `:994`.

### R3B2-F3 (MAJOR): RESOLVED
- `:498`: new note `session started before this Dispatch window` for a matching row whose `dispatch_started` is later than `first_record_ts`; `pane moved to a later session` only when `first_record_ts` is after the window end (single-row sentence and the several-rows sentence both). "Second, a second Dispatch sent to an agent still running in the pane does not start a new session: that session joins the older row whose window holds its first record, and the newer row ... is could not determine with `session started before this Dispatch window`."
- The limit is also in `:819`, `:857`, `:994`. Fixture `test_path_b_live_session_spans_two_dispatches` at `:743`: D1 09:00-10:00, D2 from 10:30, S first 09:05 joins D1 only; D2 gets the new note. Hand-checked.
- Literal check: `session started before this Dispatch window` occurs at lines 498, 743, 1026 only, spelled identically each time; `pane moved to a later session` stays at 498, 743, 1015.

### R3B2-F4 (MAJOR): RESOLVED
- `:498`: "(a reused pane or two rows on one terminal handle)". The word "retry" occurs 0 times in line 498 (grep -o count).

### R3B2-F5 (MAJOR): RESOLVED
- `:498`: "Rows that share one Dispatch id are merged first (the Duplicate Dispatch bullet below): the merged identity counts as one matching row, has no observable window, and keeps its reason `conflict: duplicate Dispatch rows disagree`."
- `:509`: "The merge comes before every join rule: the merged identity counts as one row in the several-rows rule, and its `dispatch_started`, `dispatch_ended` and `dispatch_status` are None, so it has no observable window."
- Fixture `test_path_b_duplicate_dispatch_rows_count_once` at `:743`; `:768` mentions merge-first. The merged row's fields are now defined.

### R3B2-F6 (MAJOR): RESOLVED
- `:501`, guard case 2: "a transcript that matched a tab-map entry of a scoped Dispatch row and was left unjoined by the tail, window or several-rows rules carries its pane or tail note only, not the SP-16 line"; "the line is not printed when every affected transcript is one that the second case leaves with its pane or tail note only".
- Fixtures at `:743` that assert no SP-16 line: `..._two_windows_hold_session_is_conflict`, `..._no_matching_window_holds`, `..._entry_failing_window_note_order`, `..._two_rows_incomplete_tail`, `..._duplicate_dispatch_rows_count_once`. `..._live_session_spans_two_dispatches` joins S, so guard case 2 does not apply to it.

### R3B2-F7 (MAJOR): RESOLVED
- `:743` lead-in of the R3-B2 fixtures: "all under path B and all with aware UTC times, on 2026-11-08, with `now` and `collected_start` 12:00, `window` 6 h, `tail_complete` True unless a fixture says otherwise, S `last_record_ts` 11:30, and every row in Run R1 (in `ctx.runs`)". Every open row (D1 or D2 "from ... `dispatched`") now has its `collected_start`.

### R3B2-F8 (MAJOR): RESOLVED
- `:743` `test_path_b_two_windows_hold_session_is_conflict` Then: "S is None (`person_started` None) with the same note and no `orca:` row carries S; `Could not determine` does not print the SP-16 line". "not Historical" occurs 0 times in line 743. Every term used is defined by DESIGN (`person_started`, `orca:` row, note).

### R3B2-F9 (MAJOR): RESOLVED
- `:498`: "A join outcome that makes a row could not determine is applied after rules 1 to 8: it replaces their class with rule `fallback` and keeps the rule's own evidence in `evidence`, so a `completed` row with a settled contract is could not determine, not `finished`."
- `:743` fixture 1: D1 has "a settled contract that rule 6 would class `finished` if the join had succeeded"; Then "D1 is could not determine with rule `fallback`, not `finished`". An implementation that only adds the note now fails the fixture.

## New findings

No new BLOCKING and no new MAJOR finding. Three MINOR notes (never fail the gate, not rechecked later):

| Id | Severity | Location | Note |
|---|---|---|---|
| R3B2-V1 | MINOR | `docs/designs/orchestrator-mode.md:498` | The F9 override puts a failed join ahead of rules 1 to 8, so a row with a blocked contract (rule 1) or an exit proof (rule 2) also becomes could not determine when its path-B join fails. The single-row R3-B1 text already did this for the window notes; the fix log (Other notes) says so. It is conservative and the row stays visible, but the owner may want to see it at the D9 sign-off. |
| R3B2-V2 | MINOR | `:498`, `:819` | "A second Dispatch sent to an agent still running in the pane does not start a new session" is stated flat, with no citation and no UNVERIFIED mark in DESIGN. Its evidence is in the domain-accuracy report (fact 5: `orca orchestration dispatch --to <handle>` delivers to a terminal that already runs an agent). The DA report's optional 15.1 capture line was not added. |
| R3B2-V3 | MINOR | `:743` | The R2-B1 fixture wording "the later session, whose earliest timestamp is outside the Dispatch row's window" now covers two notes (after the end: `pane moved to a later session`; before the start: the new note). It says "later session", so it still holds for what it describes. |

## Checks

Every id of the cycle-0 PASS set (111, from `cycle-ledger.md`) re-checked against the file on disk. Mechanical facts used below, all from one read-only batch run today: DESIGN has 1026 lines; em dash, en dash and horizontal bar counts are 0; no `TODO`, `TBD` or `FIXME`; `Total: 9 deviations.` at 821 and `Total: 23 open items.` at 997; the 15 path-B fixture names (5 R3-B1, 10 R3-B2) each occur once, all in line 743; unescaped-pipe counts keep every edited table row at its neighbours' cell count (rows 741-745 and 768: 4 pipes; 819: 6; 857: 4; 994: 5; 1026: 4); literal lines: `conflict: one pane session matches several Dispatch rows` 498, 743, 1026; `pane moved to a later session` 498, 743, 1015; `joined by pane: latest session of the pane` 498, 743, 1015; `Dispatch time window not observable` 498, 743, 995; `session started before this Dispatch window` 498, 743, 1026; `exactly one window holding it` 819, 857; `several rows matching one pane session` 768; no DESIGN line number cited in the edited lines (only SPEC lines and `ccsession:574`, `:607`).

| Check id | Result | Evidence |
|---|---|---|
| qa-actionability-report:C1 | PASS | Worker bullet at 498 read in full; notes and landing places listed in the F_0 section above. |
| qa-actionability-report:C2 | PASS | One window holds, two or more hold, none holds: one 7.2 sentence each (count 1 each at 498) and fixtures at 743. |
| qa-actionability-report:C6 | PASS | Fixture `no_matching_window_holds` at 743: Given and Then complete, setup now in the lead-in, no SP-16 line added. |
| qa-actionability-report:C7 | PASS | Reversed-order fixture at 743 refers to fixtures 1 and 2, whose text is complete. |
| qa-actionability-report:C8 | PASS | `entry_failing_window_note_order` at 743 unambiguous, now also asserts no SP-16 line. |
| qa-actionability-report:C9 | PASS | `rows_share_terminal_handle` at 743 unchanged and unambiguous. |
| qa-actionability-report:C10 | PASS | 498 says which notes go on the rows and which on the transcript for all three outcomes; the none-holds transcript note is the first of three named notes. |
| qa-actionability-report:C14 | PASS (reading) | 7.2, section 11, research/04 3.4 and research/09 Gap 4 agree on the seven earlier names, Givens and times; additions are additive (F8 replaced the "not True, not idle, not Historical" tail by a DESIGN-defined Then, as F8 asked). |
| qa-actionability-report:C15 | PASS | 768, 819, 857 carry the same several-rows clause and the same tail-complete and merge-first additions as 498. |
| qa-actionability-report:C16 | PASS | DESIGN is 1026 lines, still the 500-1500 row of research/09 Gap 5. |
| qa-actionability-report:C17 | PASS | The single-row sentences (outside window, no observable window, tail incomplete, inside window) give the same notes as the several-rows sentences. |
| qa-completeness-report:C1 | PASS | Several-rows text sits after "a person rerun inside the window cannot be told apart", has all three outcomes and "those notes are not added to the transcript". |
| qa-completeness-report:C2 | PASS | Fixture names follow "a row with no observable start time never joins by path B;" at 743. |
| qa-completeness-report:C3 | PASS | 768 carries "one rule for several rows matching one pane session". |
| qa-completeness-report:C4 | PASS | "exactly one window holding it" at 819 and 857, once each. |
| qa-completeness-report:C5 | PASS (reading) | 1026 starts with the exact research/04 edit 5 sentence; the "Gate fixes" sentence is the cycle-1 addition. |
| qa-completeness-report:C6 | PASS | 498: a tab-map entry that joins no row because of the tail, window or several-rows rules takes these notes instead of `Orca pane session, not in scoped Runs`. |
| qa-completeness-report:C7 | PASS | `pane_reused_joins_later_row_only` present once; times kept; D1 outcome extended with rule `fallback` (F9). |
| qa-completeness-report:C8 | PASS | `two_windows_hold_session_is_conflict` present once; Given kept; Then restated (F8). |
| qa-completeness-report:C9 | PASS | `shared_boundary_second_is_conflict` present once, unchanged. |
| qa-completeness-report:C10 | PASS | `no_matching_window_holds` present once; Then adds no SP-16 line. |
| qa-completeness-report:C11 | PASS | `multi_row_result_ignores_row_order` present once, unchanged. |
| qa-completeness-report:C12 | PASS | `entry_failing_window_note_order` present once; Then adds no SP-16 line. |
| qa-completeness-report:C13 | PASS | `rows_share_terminal_handle` present once, unchanged. |
| qa-completeness-report:C14 | PASS | Each of the three 7.2 outcomes has a named fixture at 743. |
| qa-completeness-report:C15 | PASS | Re-run today: em dash 0, no TODO/TBD, totals at 821 and 997. |
| qa-crossref-chain-report:C1 | PASS | Anchors hold: 7.2 449-517, worker bullet 498, section 11 728-752, hit lines 498/743/768/819/857/1015/1026, totals 821 and 997. |
| qa-crossref-chain-report:C2 | PASS | `conflict: one pane session matches several Dispatch rows` at 498, 743, 1026; 768 has `conflict:`; 819 and 857 do not carry the literal. |
| qa-crossref-chain-report:C3 | PASS | `pane moved to a later session` at 498, 743, 1015 only. |
| qa-crossref-chain-report:C4 | PASS | `joined by pane: latest session of the pane` at 498, 743, 1015 only; one spelling. |
| qa-crossref-chain-report:C5 | PASS | `Dispatch time window not observable` at 498, 743, 995 only. |
| qa-crossref-chain-report:C6 | PASS | 509 starts "Duplicate Dispatch" and says "No row wins by position"; 499 holds `Orca pane session, not in scoped Runs`; "R3-B2 rule below" is the later part of 498 (the new "(the Duplicate Dispatch bullet below)" also resolves to 509). |
| qa-crossref-chain-report:C7 | PASS (reading) | The seven earlier names occur once each; ten R3-B2 names, all once, none collides with the five R3-B1 names. |
| qa-crossref-chain-report:C8 | PASS | FR-010 row 768 cites 2.2, 7.1, 7.2, 13, all present; 742 Covers FR-010; 743 Covers FR-010, SP-29, D9. |
| qa-crossref-chain-report:C9 | PASS | 768, 819, 857 agree with 498. |
| qa-crossref-chain-report:C10 | PASS | 1026 names 7.2, 11, 12, 13, 14 and now 17; item 22 at 994 was edited. |
| qa-crossref-chain-report:C11 | PASS | No DESIGN line number cited in edited lines (batch M10). |
| qa-crossref-chain-report:C12 | PASS | Open items 22 and 23 (994, 995) and capture items 4 and 13 (15.1) exist; "Behaviour until closed" of both unchanged. |
| qa-crossref-chain-report:C13 | PASS | Counters reproduced by my own batch (see above). |
| qa-domain-accuracy-report:C1 | PASS | One sentence per outcome in the 498 bullet. |
| qa-domain-accuracy-report:C2 | PASS | `ccsession` lines 574, 602, 605, 607, 613 read: `orca_tab_session()` opens at 574 and closes at 605, `orca_tab_reopen()` opens at 607; cite range still ends early (cycle-0 minor). |
| qa-domain-accuracy-report:C3 | PASS | `/clear` sequence: S2 joins only inside the window; S1 has no entry and is None through guard case 4 (501). |
| qa-domain-accuracy-report:C4 | PASS | `/resume` sequence unchanged by the fix; old row stays unjoined. |
| qa-domain-accuracy-report:C5 | PASS | Retry or reused pane with closed windows: fixture 1 still joins the later row only; D1 could not determine, now with rule `fallback`. |
| qa-domain-accuracy-report:C6 | PASS | ccsession `OWNER` check facts untouched; fix edited DESIGN only (no newer file in the task folder besides the fix log and the task file). |
| qa-domain-accuracy-report:C7 | PASS | Same; a plain `claude` writes no entry, so it cannot join. |
| qa-domain-accuracy-report:C11 | PASS | Result is set-based; shared boundary second gives `conflict:` (fixture 3 hand-checked: 10:00:00.400 cut to 10:00:00 is held by D1's end and D2's start). |
| qa-domain-accuracy-report:C13 | PASS | Mechanical report facts match disk: 449-517, 498, 728-752, em dash 0, no TODO/TBD. |
| qa-evidence-quality-report:C1 | PASS | Orca-behaviour claims of the new text re-listed; the one new claim (second Dispatch keeps the session) has evidence in DA fact 5 but no DESIGN citation (minor R3B2-V2). |
| qa-evidence-quality-report:C2 | PASS | DESIGN asserts no refusal rule; bundle guard facts unchanged. |
| qa-evidence-quality-report:C4 | PASS | Worker-start rows still not asserted in DESIGN. |
| qa-evidence-quality-report:C5 | PASS | DESIGN still does not pin the `session_join` value (994 still says "which tab-map value equals the item 4 field"). |
| qa-evidence-quality-report:C6 | PASS | "a reused pane or two rows on one terminal handle" rests on the static `$nt` evidence; "retry" is gone (count 0 on 498). |
| qa-evidence-quality-report:C7 | PASS | Bundle evidence is outside the edited file; unchanged. |
| qa-evidence-quality-report:C9 | PASS | Mechanical claims reproduce: totals, `exactly one window holding it` at 819 and 857, `several rows matching one pane session` at 768, the `conflict: one pane session ...` literal once each in 498, 743, 1026. |
| qa-evidence-quality-report:C11 | PASS | 768, 819, 857 add nothing beyond 498; the two residual cases appear in 498 too. |
| qa-evidence-quality-report:C12 | PASS | New and edited fixtures state inputs and expected outputs only; `live_session_spans_two_dispatches` states "one session serving both Dispatches" as an input. |
| qa-evidence-quality-report:C13 | PASS (reading) | 1026 R3-B2 row begins with the research/04 edit 5 text word for word; m11 (review 3 line 137) is still the note-order point. |
| qa-evidence-quality-report:C14 | PASS | Each of the three outcomes maps to a named fixture at 743. |
| qa-evidence-quality-report:C15 | PASS | Self-audit: defects located by sentence and line; no refusal, worker-start or `session_join` value claims added. |
| qa-internal-consistency-report:C1 | PASS | All inputs read in chunks of at most 150 lines. |
| qa-internal-consistency-report:C2 | PASS | 0, 1, 2 or more holding rows are exhaustive and exclusive for a complete tail; the incomplete-tail branch is carved out before the count. |
| qa-internal-consistency-report:C3 | PASS | Sentences are set-based; "the first of the three notes" is a fixed note order, not row position; "the older row" is chosen by window. |
| qa-internal-consistency-report:C4 | PASS | Inclusive whole seconds, no window for a terminal row without end, open window to `collected_start`: unchanged. |
| qa-internal-consistency-report:C8 | PASS | 499 and D9 note rule agree; 498 states the tab-map-entry note order. |
| qa-internal-consistency-report:C9 | PASS | 768, 819, 857 agree with each other and now all carry the tail-complete condition. |
| qa-internal-consistency-report:C10 | PASS (reading) | All ten R3-B2 fixtures worked by hand against the 498 rule (times, notes, joins); none contradicts it. |
| qa-internal-consistency-report:C11 | PASS | Branches have fixtures, incl. incomplete tail, live session, merged duplicate; the none-observable branch still has only the duplicate fixture (cycle-0 minor). |
| qa-internal-consistency-report:C12 | PASS | Edits 1 to 5 of research/04 3.3 present at 498, 743 (after the "never joins by path B;" anchor), 768, 819 and 857, 1026. |
| qa-internal-consistency-report:C13 | PASS | No em dash, no TODO/TBD, totals at 821 and 997. |
| qa-internal-consistency-report:C14 | PASS | `conflict:` appears at 498, 509, 510, 742, 743, 768, 1026; no consumer keys off the prefix. |
| qa-numbers-metrics-report:C1 | PASS (reading) | The seven earlier fixture names are present once each; three added names also once. |
| qa-numbers-metrics-report:C2 | PASS | Three outcome sentences, count 1 each at 498. |
| qa-numbers-metrics-report:C3 | PASS | Outcome-to-fixture mapping intact. |
| qa-numbers-metrics-report:C4 | PASS (reading) | "exactly one window holding it" once in D9 (819); the research/04 phrase is intact inside the longer D9 sentence. |
| qa-numbers-metrics-report:C5 | PASS (reading) | Same once in SP-29 (857). |
| qa-numbers-metrics-report:C6 | PASS | 768 carries the rule once and agrees with 819 and 857. |
| qa-numbers-metrics-report:C7 | PASS | One `Total: 9 deviations.` at 821; D1 to D9 are rows 811 to 819. |
| qa-numbers-metrics-report:C8 | PASS | One `Total: 23 open items.` at 997; rows 21, 22, 23 at 993-995; no row added. |
| qa-numbers-metrics-report:C9 | PASS | Em dash, en dash, horizontal bar: 0, 0, 0. |
| qa-numbers-metrics-report:C10 | PASS | `grep -nw 'TODO\|TBD\|FIXME'` has no match. |
| qa-numbers-metrics-report:C11 | PASS | New fixture times (09:05 in 09:00-10:00; 10:40 vs 10:30; 09:30 merged) consistent with the inclusive whole-second rule. |
| qa-numbers-metrics-report:C12 | PASS | R3-B1 fixtures and the six `test_probes_allowlist.py` fixtures: times unchanged; only the open-row fixture gained a sign-off sentence. |
| qa-numbers-metrics-report:C13 | PASS (reading) | Every time value of research/04 3.4 is still in the DESIGN fixtures; the F8 rewording of fixture 2's Then is the requested change. |
| qa-numbers-metrics-report:C14 | PASS (reading) | 1026 equals research/04 edit 5 as a prefix and names 7.2, 11, 12, 13, 14 (plus 17). |
| qa-numbers-metrics-report:C15 | PASS | 1026 lines; 7.2 449-517; bullet 498; section 11 728-752; literal lines 498/743/1015/1026. |
| qa-numbers-metrics-report:C16 | PASS | Line 730 unchanged: seven new files, one command test, three edited files. |
| qa-numbers-metrics-report:C17 | PASS | 1026 lines is in the 500-1500 row: 4 + 4 + 1 domain lens = 9. |
| qa-numbers-metrics-report:C18 | PASS | `collected_start` 12:00 is now in the R3-B2 lead-in (cycle-0 minor M1 cleared); R3-B1 rows state it in their text. |
| qa-spec-fidelity-report:C1 | PASS | No outcome gives `person_started` True for a tab-map entry: one holds False, conflict None, none-holds None, incomplete tail None, merged duplicate None. |
| qa-spec-fidelity-report:C2 | PASS | SP-29 "never True" for a tab-map entry holds at 498-501. |
| qa-spec-fidelity-report:C3 | PASS | 499 unchanged: an unmatched entry gets None with `Orca pane session, not in scoped Runs`. |
| qa-spec-fidelity-report:C4 | PASS | 7.3 (518-534) still has 8 templates; the rule reads only `dispatch_started`, `dispatch_ended`, `dispatch_status` of the existing `worker-show`. |
| qa-spec-fidelity-report:C5 | PASS | Conflict and none-holds leave the transcript visible as None; the in-window False cases are now disclosed in 498, 819, 857, 994 and gated at 994. |
| qa-spec-fidelity-report:C9 | PASS | 768, 819, 857 carry the same several-rows wording. |
| qa-spec-fidelity-report:C10 | PASS | Outcome-to-fixture mapping intact. |
| qa-spec-fidelity-report:C11 | PASS | Edits 1 to 5 present (498; 743; 768; 819 and 857; 1026). |
| qa-spec-fidelity-report:C12 | PASS | No row wins by position; the join is chosen by which window holds the transcript. |
| qa-spec-fidelity-report:C13 | PASS | Mechanical claims reproduce today. |
| qa-template-conformance-report:C1 | PASS | Section 11 rows 741-745 keep 4 pipes (3 cells). |
| qa-template-conformance-report:C2 | PASS | Section 12 FR-010 row 768 keeps 4 pipes. |
| qa-template-conformance-report:C3 | PASS (reading) | Row 1026 keeps 4 pipes and begins with the research/04 edit 5 text. |
| qa-template-conformance-report:C4 | PASS | D9 row 819 keeps 6 pipes like 818; SP-29 row 857 keeps 4 like 858; both carry the edit 4 wording. |
| qa-template-conformance-report:C5 | PASS | New 498 sentences use the same verb forms and backticked note literals; no own-line-number citations. |
| qa-template-conformance-report:C8 | PASS | Dash counts 0; no ` - ` or ` -- ` separator in the edited lines. |
| qa-template-conformance-report:C9 | PASS | No TODO, TBD or FIXME. |
| qa-template-conformance-report:C10 | PASS | The seven earlier names are unchanged. |
| qa-template-conformance-report:C11 | PASS | One 7.2 sentence and at least one fixture per outcome. |
| qa-template-conformance-report:C12 | PASS | Each literal has one spelling at every hit (batch M7), including the new `session started before this Dispatch window`. |
| qa-template-conformance-report:C13 | PASS | 9 deviations and 23 open items. |
| qa-template-conformance-report:C16 | PASS | `r3-b2-mechanical.md` commands 1 to 7 reproduce on the current file; its outcome-to-fixture hit counts (1, 1, 1 in 7.2; 1, 2, 1 in 11) still hold. |

Checks passed: 111 / 111. Checks failed: 0. Regressions (a cycle-0 PASS now failing): 0.

## Summary

- F_0: 9 of 9 RESOLVED (R3B2-F1 to R3B2-F9), each with `file:line` above. Open blocking findings: 0.
- New BLOCKING or MAJOR findings: 0. New MINOR notes: 3 (R3B2-V1 to R3B2-V3).
- Monotonicity: |F_0| = 9, |F_1| = 0, strictly smaller. Regression check: no cycle-0 PASS id fails.
- Open owner decisions are not defects here: the D9 sign-off (now covering the two residual path-B cases) is pending at step 1.0b and gated by open item 22 (`:994`). The MINOR findings F10 to F24 of cycle 0 were not rechecked, as the severity rule says.

**Confidence:** Verified: 120/120 (9 findings + 111 checks) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 25 | Grep: 2 | Glob: 1 | Bash: 4 (one of them a single batch of 15 read-only blocks). No web research; no Tavily or fallback calls.
Limit of the evidence: the PASS checks that concern bundle and `ccsession` facts (domain-accuracy C3 to C7, evidence-quality C2, C4, C7) were re-checked by confirming that the fix touched only the DESIGN and by reading the `ccsession` cite lines; I did not re-open the Orca bundle.

Verdict: PASS
Blocking count: 0

## QA Complete

