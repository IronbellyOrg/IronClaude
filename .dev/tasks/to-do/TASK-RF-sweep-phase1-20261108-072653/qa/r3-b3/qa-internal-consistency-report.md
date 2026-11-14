# QA Report - R3-B3 internal-consistency lens

**Topic:** R3-B3, the three SPEC FR-010 incomplete-case fixtures and the list-incomplete rule
**Date:** 2026-11-09
**Phase:** fix-cycle review of items 4.1 to 4.5 (read-only, `fix_authorization: false`)
**Subject:** `docs/designs/orchestrator-mode.md` (1030 lines on disk, counted with Grep)
**Inputs read:** DESIGN 1-36, 223-352, 353-448, 449-518, 519-646, 731-756, 756-785, 822, 860, 873-902, 968-1030; research/04 lines 170-219; SPEC `merged-requirements.md` lines 98-109 and rule rows 255-257; `r3-b3-mechanical.md` lines 1-137.

## Method

I read the list-incomplete bullet (DESIGN 501), the join-guard bullet (502), the 7.1 result kinds (376-378), the 7.4 summary fields (586-595), the section 11 fixtures (746) and the traceability and revision-log rows. I tried to build an input in which one transcript is both `origin unknown:` and Historical or idle, and I compared every fixture Given against the rules it claims to exercise.

## Checks

| Id | Check | Result |
|---|---|---|
| C1 | The three `origin unknown:` literals are spelled the same in DESIGN 501, DESIGN 746 and research/04 4.2 | PASS |
| C2 | The `orca_available` False trigger matches the 7.1 `unavailable` kind and open item 4 (nonzero exit on call one) | PASS |
| C3 | The `call_failed` trigger can be evaluated by pure `classify` from `SweepInput` and cannot be confused with an unavailable or budget-cut source row | FAIL (F3) |
| C4 | The `truncated` trigger matches `WORKER_LIST_PAGE`, open item 5 and the 7.4 `total_is_lower_bound` rule | PASS (minor m3) |
| C5 | 7.4 `summary.historical` and `summary.total_is_lower_bound` agree with fixtures 1 to 3 (historical 0, lower bound True when truncated or unscanned) | PASS |
| C6 | Historical and idle are reachable only through `person_started` True, so a None transcript from the new bullet cannot be Historical or idle | PASS |
| C7 | Join-guard note order: `origin unknown:` first, then the SP-16 literal, then `tab map join not observable` | FAIL (F2) |
| C8 | The scope of the join-guard bullet (502) agrees with the scope of the list-incomplete bullet (501), fixture 4 and open item 1 | FAIL (F1) |
| C9 | Search for an input where a transcript is both `origin unknown:` and Historical or idle | PASS for the new rule (none found); two adjacent paths reach Historical or idle with no origin-unknown note (F1, F4) |
| C10 | Fixtures 1 to 3 hold the "join guard otherwise holds" and "differs from the control by one input" claims | FAIL (F2) |
| C11 | Fixture 4 can be built from its Given and its expected note list is consistent with 502 | FAIL (F2) |
| C12 | The new bullet covers every FR-010 reason the SPEC sentence names | FAIL (F4) |
| C13 | Traceability row 771, the section 11 cell and the Fix cycle 3 row (1030) agree on "three SPEC cases" and "four join-incomplete cases" | PASS |
| C14 | The sequence diagram and test list agree with open item 4 about a nonzero `worker-list` exit | PASS (minor m1) |
| C15 | The mechanical report matches the file: section ranges, hit counts, em-dash, TODO/TBD, totals (re-run with Grep) | PASS (minor m6) |

## Findings

### F1 (MAJOR) The join-guard bullet is scoped "in the window"; the new bullet, fixture 4 and open item 1 are not

Evidence:
- DESIGN 502: "The guard's 'join completed' condition fails, and every unjoined transcript **in the window** is None, in four cases. First, `session_join` is None on any scoped Dispatch row: note `tab map join not observable`".
- DESIGN 501 (new): the `origin unknown:` notes apply to "Every unjoined transcript ... even when its activity is older than the window".
- DESIGN 746, `test_fr010_incomplete_notes_order`: the shared Given is `last_activity` 8 h before `now` with a 6 h window, so T is outside the window; the Then says T carries the `origin unknown:` notes "first, then `tab map join not observable`".
- DESIGN 746 and 976 say None "for every unjoined transcript while `session_join` is None" and "for every unmatched transcript", with no window qualifier. SPEC line 104: "None never becomes idle or Historical".

What is wrong: by the letter of 502, an 8 h old unjoined transcript is not "in the window", so guard case 1 does not make it None and does not give it `tab map join not observable`. Fixture 4 requires that note on exactly such a transcript. For the same input without the list-incomplete conditions (guard case 1 only, T 8 h old), 502 leaves T unconstrained, so it can be True and go to Historical, which SPEC line 104 forbids. This is the nearest input to the one the lens asked for: with the list-incomplete bullet T is protected "even when older", with the join-guard bullet it is not.

Smallest fix: delete "in the window" from DESIGN 502 so the four cases apply to every unjoined transcript, matching 746, 976 and SPEC line 104.

### F2 (MAJOR) The fixture Givens contradict guard case 2 and each other

Evidence:
- DESIGN 746 and research/04 line 193: the shared Given for fixtures 1 to 3 is "transcript T readable ... joined to no Orca row, and the join guard otherwise holding (path A, `session_join` present on every scoped row)". The only transcript named is T.
- DESIGN 746, fixture 2: "scoped R1 with exactly `WORKER_LIST_PAGE` (100) rows ... none joined to T".
- DESIGN 502, second case: "Orca returned at least one worker row and no transcript joined any Orca row". With 100 rows and T the only transcript, this case holds, so the guard does not "otherwise hold". Per 502, T then also carries the SP-16 literal, and `Could not determine` prints `could not join Orca workers to transcripts (tab map empty or stale)`. DESIGN 746 itself says "the SPEC line 236 fixture (worker rows present, no transcript joined) gives the same".
- Fixture 3 has the same exposure: "R1 `worker-list` ok" with no stated joined transcript.
- DESIGN 746: "the first three each differ from the complete-negative-join control by one input". The control (SPEC line 104) has 2 transcripts, one mapped to an Orca row. Fixtures 1 to 3 drop that mapped transcript, and fixture 3 also adds a second Run, so each differs by more than one input.
- Fixture 4: "outage together with guard case 1 (`session_join` None)". Guard case 1 needs a scoped Dispatch row (502: "`session_join` is None on any scoped Dispatch row"), but fixture 1's outage has `orca_rows` empty. Also, once a Dispatch row with a None `session_join` exists and no transcript joins it, case 2 holds as well, and 502 says "the transcript carries the SP-16 literal first and then `tab map join not observable`". Fixture 4's expected list ("`origin unknown:` notes first, then `tab map join not observable`") omits the SP-16 literal, so the expected order is wrong or incomplete.

Smallest fix: add to the shared Given a second transcript U joined by `sessionId` to one returned Orca row (as in the control), so case 2 does not hold and "one input" is true. For fixture 4, state that the outage is a later `unavailable` (R1 returned a row with `session_join` None, R2 unavailable) and list the full expected order: `origin unknown: Orca unavailable`, the SP-16 literal only if case 2 holds, then `tab map join not observable`.

### F3 (MAJOR) The `call_failed` trigger cannot be evaluated from `SweepInput`

Evidence:
- DESIGN 501: "when any scoped Run's `worker-list` result is `call_failed` (its `sources` row `orca worker-list <run>` has `unscanned` set)".
- DESIGN 456 and 467: `classify_all` receives `orca_available`, `truncated` and `sources: tuple[SourceCoverage]` with fields `name, coverage, age_seconds, unscanned`. No per-Run `OrcaResult.kind` reaches classify (kind is a 7.1 `probes` type).
- DESIGN 250 and 850: after a later `unavailable`, the remaining reads are marked unscanned, with the text `unscanned: orca unavailable`. DESIGN 287 and 378: a budget cut is `call_failed` with a reason such as `unscanned: time budget reached (90 s)`, which differs from fixture 3's `orca call failed (exit 1)`.

What is wrong: "the row has `unscanned` set" is true for call_failed, for unavailable-marked rows and for budget cuts. Read literally, a plain outage (fixture 1) also matches the call_failed trigger, so T gets both `origin unknown: Orca unavailable` and `origin unknown: worker list call failed`. Matching on the `orca call failed` text instead would miss budget-cut call_failed. research/04 4.5 asserts that the rules "read `orca_available`, `truncated` and `sources`" with nothing else needed, which this shows is not enough as written.

Smallest fix: write the trigger as "a `sources` row `orca worker-list <run>` has `unscanned` set while `orca_available` is True" (so the outage note owns the unavailable case), and add that qualifier to fixture 3's Then.

### F4 (MAJOR, adjacent to the three fixtures) The SPEC's fourth reason, tab map unreadable, has no rule

Evidence:
- SPEC line 104: "Only when every scoped Run's worker list is complete, no relevant list or join is unscanned or truncated, **and the tab map is read** and the join completed may an unjoined transcript be True ... with an explicit reason such as Orca unavailable, worker list truncated, worker list call failed or tab map unreadable."
- DESIGN 501 lists three conditions and no tab-map-read condition. A search of the design for "tab map unreadable" returns nothing. DESIGN 401: `read_tab_map` returns `tuple[TabMapEntry, ...]`, and DESIGN 394 says each reader "never raises past collect", so an unreadable `orca-tabs/` folder yields an empty tuple plus an unscanned source row.
- Under path A (DESIGN 500), a transcript with no tab-map entry and no scoped join "may be True when the FR-010 guard holds". Guard cases 2 and 3 do not fire when path-A `sessionId` joins are intact, so an unreadable tab map still allows True, then idle or Historical, with no `origin unknown:` note.

Smallest fix: add a fourth trigger to DESIGN 501 (`origin unknown: tab map unreadable` when the `orca-tabs/` source row is unscanned), put it in the stated note order, and add it to the section 11 cell. If the owner decides the SPEC sentence is only illustrative ("such as"), record that as a deviation instead.

### Minor findings (do not fail the gate)

- m1: DESIGN 245 (sequence diagram) says an unknown-Run shape is "call_failed for R, next Run", and DESIGN 749 lists the case "unknown-Run then R2". DESIGN 979 (open item 4) says "Any nonzero `worker-list` exit on call one is `unavailable`, not `call_failed`". With `--run R1 --run R2` and R1 unknown, call one is `worker-list R1`, so the three places disagree about whether R2 is read. Fixture 3 correctly avoids call one. Qualify 245 with "after call one" until capture item 8 closes.
- m2: DESIGN 500, 771 (FR-010 row), 822 (D9) and 860 (SP-29) say True is allowed "when the guard holds", and the guard is defined as the four join-incomplete cases (502). The list-incomplete conditions are a separate necessary condition (501) that these True statements never name. An implementer reading only D9 could reach True with a truncated list.
- m3: Fixture 2 (DESIGN 746) sets `truncated` "from a synthetic page whose `page.nextCursor` is non-null". DESIGN 557 and open item 5 (980) say the cursor field is not captured and the rule is "a full page sets truncated". Say the fixture sets truncated by the 100-row count and that the cursor value is cosmetic.
- m4: `OrcaResult.reason` (DESIGN 378) carries the prefix `unscanned: ...`, while the `SourceCoverage.unscanned` example (DESIGN 595, 746) is `orca call failed (exit 1)` with no prefix. Pick one form.
- m5: Note order is not stated between `origin unknown:` and the notes `Orca pane session, not in scoped Runs` (499), `unscanned: transcript not readable` (514) and `earlier pane session not joinable ...` (502 fourth case). 501 only says "before any join-guard note".
- m6: `r3-b3-mechanical.md` Command 7 prints "(no output expected ...)" instead of a captured result, so check 7 has no recorded evidence. I re-ran it (Grep for `TODO`, `TBD`, em-dash: no hits) and it holds.

## Answer to the lens question

No input makes a transcript both `origin unknown:` and Historical or idle through the new bullet itself: idle (rule 7) and person session (active, rule 8) require `person_started is True` (SPEC lines 255-256), Historical is the older-than-window outcome of the same person-started set (SPEC line 383), and 501 makes every unjoined transcript None whenever one of its three conditions holds. The contradictions are at the edges: F1 (a stale transcript under guard case 1 is not forced to None by the letter of 502) and F4 (an unreadable tab map under path A has no rule at all). F2 and F3 are specification faults in the fixtures and the trigger wording.

## Summary

- Checks: 15 run, 9 PASS, 6 FAIL (C3, C7, C8, C10, C11, C12). C9 passes for the new rule and points at F1 and F4.
- Findings: 0 BLOCKING, 4 MAJOR (F1 to F4), 6 MINOR (m1 to m6).
- Confidence: Verified 15/15 | Unverifiable 0 | Unchecked 0 | Confidence 100.0%. Tool engagement: Read 13 | Grep 10 | Glob 0 | Bash 1 (a `git diff` that showed the design file is untracked, so no diff baseline existed).

Verdict: FAIL
Blocking count: 4
