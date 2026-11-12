# QA Report: R3-B3 completeness lens (items 4.1 to 4.5)

**Topic:** R3-B3 design fix, SPEC FR-010 incomplete-case fixtures
**Date:** 2026-11-09
**Phase:** fix-cycle verification (completeness lens, fix_authorization: false)
**Fix cycle:** 1
**Files read:** `docs/designs/orchestrator-mode.md` (1030 lines; lines 1-36, 449-520, 546-549, 559-598, 731-755, 768-773, 1000-1030, plus targeted greps), `research/04-design-fixes-r3.md` lines 170-219, SPEC `merged-requirements.md` lines 98-113 (FR-010 is line 104), `phase-outputs/test-results/r3-b3-mechanical.md` (all 137 lines).

Note: `docs/designs/orchestrator-mode.md` is untracked (`git status` shows `??`), so no diff against HEAD exists. Presence was proved by reading the file text, not by a diff.

---

## Completeness inventory (quoted text found in DESIGN)

| # | Required item (research/04 section) | Quoted text found in DESIGN | Location | Mark |
|---|---|---|---|---|
| 1 | 4.2 edit 1: replace "the four incomplete cases" in the `test_classify.py` row | "the three SPEC incomplete cases (an older transcript during an Orca outage, an older unjoined transcript after a full page with uncaptured continuation, an incomplete list after `call_failed`; each stays visible with `person_started` None and its `origin unknown:` note, never idle or Historical)" | DESIGN:746 | PRESENT |
| 2 | 4.2 edit 2: new 7.2 bullet before "The guard's 'join completed' condition fails" | "List-incomplete cases (SPEC FR-010): no transcript can be proved unjoined when Orca is unavailable (`orca_available` False), when any scoped Run's worker list is truncated (`truncated` True: a full page of `WORKER_LIST_PAGE` rows whose continuation is not read), or when any scoped Run's `worker-list` result is `call_failed` ... `origin unknown: Orca unavailable`, `origin unknown: worker list truncated` or `origin unknown: worker list call failed`, in that order when several hold, before any join-guard note. It prints could not determine and is never idle or Historical, even when its activity is older than the window." Directly before the "The guard's \"join completed\" condition fails" bullet | DESIGN:501 (guard bullet at 502) | PRESENT |
| 3 | 4.2 edit 3, design column: add "with its three list-incomplete cases (outage, full page, `call_failed`) and" after "completeness guard" | "completeness guard with its three list-incomplete cases (outage, full page, `call_failed`) and with its four join-incomplete cases" | DESIGN:771 | PRESENT |
| 4 | 4.2 edit 3, test column: add "the three SPEC incomplete-case fixtures" to the `sweep/test_classify.py` parenthesis | "`sweep/test_classify.py` (the D9 join fixtures, the three SPEC incomplete-case fixtures and the SPEC line 236 fixture)" | DESIGN:771 | PRESENT |
| 5 | 4.2 edit 4: Fix cycle 3, R3-B3 row | "Restored the three SPEC incomplete-case fixtures in `test_classify.py` (11), added the list-incomplete rule and its three `origin unknown:` notes (7.2), named them in the FR-010 row (12) ... Corrects cycle 2's \"changed three to four incomplete cases\": the four join-incomplete cases stay in 7.2, D9 and the FR-010 and SP-29 rows" | DESIGN:1030 | PRESENT |
| 6 | Item 4.2 7.4 source sentence (the `orca worker-list <run>` source row) | "Each scoped Run's `worker-list` call has its own source row named `orca worker-list <run>`; a `call_failed` result sets its `unscanned` reason (for example `orca call failed (exit 1)`)." | DESIGN:595 | PRESENT |
| 7 | 4.3 fixture 1 | `test_fr010_outage_older_transcript_unknown_not_historical` (`--run R1`; `orca_available` False and `orca_rows` empty ...: T `person_started` None, could not determine, note `origin unknown: Orca unavailable`; visible, not Historical; `summary.historical` 0) | DESIGN:746 | PRESENT |
| 8 | 4.3 fixture 2 | `test_fr010_full_page_uncaptured_continuation` (R1 with exactly `WORKER_LIST_PAGE` (100) rows, `truncated` True, `page.nextCursor` non-null, none joined to T: None, note `origin unknown: worker list truncated`; not Historical; `summary.total_is_lower_bound` True) | DESIGN:746 | PRESENT |
| 9 | 4.3 fixture 3 | `test_fr010_call_failed_incomplete_list` (R1 and R2; R2 `call_failed`, not call one; `sources` holds `orca worker-list R2` with `unscanned` `orca call failed (exit 1)`; `orca_available` True: None, note `origin unknown: worker list call failed`; not Historical) | DESIGN:746 | PRESENT |
| 10 | 4.3 fixture 4 | `test_fr010_incomplete_notes_order` (outage with guard case 1, `session_join` None; separately truncated with `call_failed`: `origin unknown:` notes first, then `tab map join not observable`) | DESIGN:746 | PRESENT |
| 11 | Shared Given of 4.3 | "`now` fixed, window 6 h, transcript T readable, `last_activity` 8 h before `now`, no tab-map entry, joined to no Orca row, and the join guard otherwise holding (path A, `session_join` present on every scoped row)" | DESIGN:746 | PRESENT |

## Retained-fixture check (same `test_classify.py` row, DESIGN:746)

| Item | Quoted text | Mark |
|---|---|---|
| Guard case 1 fixture | "`person_started` None for every unjoined transcript while `session_join` is None" | PRESENT |
| Guard case 2 fixture | "when guard cases 1 and 2 hold together, the transcript carries the SP-16 literal first, then `tab map join not observable`; the SPEC line 236 fixture (worker rows present, no transcript joined) gives the same" | PRESENT |
| Guard case 3 fixture | "a path-B scoped row whose `session_join` matches no tab-map entry makes every unjoined transcript None with the SP-16 literal" | PRESENT |
| Guard case 4 fixture | "the R2-B1 pane-reuse fixtures under path B, one each for `/clear`, a resume and a person rerunning the command in the tab: the worker's earlier transcript has no entry and is None with note `earlier pane session not joinable (tab map keeps only the latest session)`, never True or Historical" | PRESENT |
| Complete-negative-join control | "FR-010 complete-negative join (an 8 h old unmapped transcript goes to Historical when the list is complete)" | PRESENT |

## Findings

No BLOCKING or MAJOR finding. Three MINOR notes (never fail the gate):

| ID | Severity | Evidence | What is wrong | Smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `docs/designs/orchestrator-mode.md:746` ("... so it departs from the shared Given of the other three: `now` fixed, window 6 h, ...") | The colon after "the other three" makes the shared Given read as part of the sentence about `test_fr010_incomplete_notes_order`. A reader can take the Given as belonging only to that fixture. Content is complete; only the sentence structure is unclear. | Start a new sentence: "The shared Given of the first three is: ...". |
| F2 | MINOR | `docs/designs/orchestrator-mode.md:1030` quotes cycle 2 as "changed three to four incomplete cases"; the cycle 2 row at `:1018` reads `changed "three" to "four" incomplete cases` | The quoted wording is not verbatim. Meaning and the correction are right. | Quote it as `changed "three" to "four" incomplete cases`. |
| F3 | MINOR (outside the four edits, so not a completeness failure) | SPEC `merged-requirements.md:104` lists "tab map unreadable" as an example `origin unknown` reason; `grep -i 'tab map unreadable'` on DESIGN returns no hit | The new 7.2 bullet (`:501`) covers three of the four SPEC reasons. Research 4.2 itself scoped the bullet to the three SPEC fixtures, and the tab-map empty-or-stale case is handled by the SP-16 line (`:502`). No fixture in the SPEC asks for the fourth reason. | None needed for this gate. Optionally record it as a follow-up if "tab map unreadable" should get its own `origin unknown:` note. |

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | 4.2 edit 1: `test_classify.py` row says "the three SPEC incomplete cases (...)" with the `origin unknown:` / never idle or Historical clause (`:746`) | PASS |
| C2 | Four guard-case fixtures and the complete-negative-join control are still in the `test_classify.py` row (`:746`) | PASS |
| C3 | 4.2 edit 2: list-incomplete bullet is in 7.2 immediately before the "join completed" bullet, with all three note literals, the ordering rule and the "never idle or Historical" clause (`:501-502`) | PASS |
| C4 | 7.4 source sentence naming `orca worker-list <run>` with the `call_failed` `unscanned` reason (`:595`) | PASS |
| C5 | 4.2 edit 3, design column of the FR-010 row (`:771`) | PASS |
| C6 | 4.2 edit 3, test column of the FR-010 row (`:771`) | PASS |
| C7 | 4.2 edit 4: Fix cycle 3 R3-B3 row, including the correction of cycle 2's "four incomplete cases" (`:1030`) | PASS |
| C8 | 4.3 shared Given present in full (`:746`) | PASS |
| C9 | 4.3 fixture `test_fr010_outage_older_transcript_unknown_not_historical`: Given, When-equivalent and every Then element (`:746`) | PASS |
| C10 | 4.3 fixture `test_fr010_full_page_uncaptured_continuation`: 100 rows, `truncated`, `page.nextCursor`, note, not Historical, `total_is_lower_bound` (`:746`; `WORKER_LIST_PAGE = 100` defined at `:548`) | PASS |
| C11 | 4.3 fixture `test_fr010_call_failed_incomplete_list`: two Runs, R2 `call_failed` not call one, `sources` row and `unscanned` text, `orca_available` True, note (`:746`) | PASS |
| C12 | 4.3 fixture `test_fr010_incomplete_notes_order`: both combinations and the note order (`:746`) | PASS |
| C13 | Cross-references stay consistent: "four join-incomplete" kept at `:771`, `:822` (D9), `:860` (SP-29), `:1030`; "four incomplete cases" occurs only inside the cycle 3 correction (`:1030`) | PASS |
| C14 | SPEC FR-010 acceptance fixtures (`merged-requirements.md:104`: outage, full page with uncaptured continuation, `call_failed`; "visible and unknown, not Historical") each map to a DESIGN fixture; mechanical file `r3-b3-mechanical.md` claims re-derived from the DESIGN text, not trusted (section map, `:501`, `:595`, `:1030`) | PASS |

## Summary

- Items marked: 11 of 11 research items PRESENT; 5 of 5 retained items PRESENT; 0 PARTIAL; 0 MISSING.
- Checks: 14 PASS, 0 FAIL.
- Findings: 0 BLOCKING, 0 MAJOR, 3 MINOR (F1 to F3).
- Confidence: Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Caveat: the DESIGN file is untracked, so there is no diff to show what changed; the PRESENT marks rest on reading the current file text.
- Tool engagement: Read: 10 | Grep: 4 | Glob: 0 | Bash: 1 (git status and wc). Read + Grep + Glob = 14, equal to the 14 checks.
- Fixes applied: none (`fix_authorization: false`). This report is the only file written.

Verdict: PASS
Blocking count: 0
