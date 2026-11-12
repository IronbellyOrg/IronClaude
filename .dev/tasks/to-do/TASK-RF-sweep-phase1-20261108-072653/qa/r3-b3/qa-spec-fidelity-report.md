# QA Report: R3-B3 SPEC-fidelity lens

**Topic:** R3-B3, the three restored SPEC FR-010 incomplete-case fixtures, the 7.2 list-incomplete bullet and the `orca worker-list <run>` source row
**Date:** 2026-11-09
**Phase:** fix-cycle review (design gate), SPEC-fidelity lens, `fix_authorization: false`
**Design file read:** `docs/designs/orchestrator-mode.md` (1030 lines at review time)

## Sources read (all in chunks of at most 150 lines)

- SPEC FR-010 row: `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md:104` (body and acceptance cell), plus 99-106, 232-259 (SessionRow, `row_id`, SP-16, rule table 7 to 9) and 338-340.
- research/04 section 4: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/04-design-fixes-r3.md:170-215`.
- DESIGN: 1-36, 238-289, 353-402, 449-518 (7.2), 559-615 (7.4), 731-780 (11, 12), 808-831 (13), 1002-1030 (18).
- Mechanical results: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r3-b3-mechanical.md`.
- One Bash run (read-only `grep -cF`, `grep -o`, `wc -l`) to confirm the bullet text matches research/04 byte for byte and that the design has no `tab map unreadable` text.

## SPEC FR-010 requirements this lens compared against (SPEC:104)

1. Reasons for None: "Orca unavailable, worker list truncated, worker list call failed **or tab map unreadable**".
2. True needs: every scoped Run's list complete, no relevant list or join unscanned or truncated, **and the tab map read** and the join completed.
3. Acceptance fixtures: (a) an older transcript during an outage; (b) an older unjoined transcript after a full page with uncaptured continuation; (c) an incomplete list after `call_failed`. "All three remain visible and unknown, not Historical."

## Word-for-word comparison

| SPEC item | DESIGN location | Result |
|---|---|---|
| Fixture (a) outage | `test_fr010_outage_older_transcript_unknown_not_historical`, DESIGN:746. Given: 8 h old, readable, no tab-map entry, `orca_available` False, `orca_rows` empty. Then: `person_started` None, could not determine, note `origin unknown: Orca unavailable`, in visible rows, `summary.historical` 0. | Matches SPEC and research/04 4.3 row 1. "Older" is 8 h against a 6 h window, as the SPEC control uses. Strongest of the three: asserts visible and historical 0. |
| Fixture (b) full page, uncaptured continuation | `test_fr010_full_page_uncaptured_continuation`, DESIGN:746. Exactly `WORKER_LIST_PAGE` (100) rows, `truncated` True from non-null `page.nextCursor`, none joined to T. Then: None, could not determine, `origin unknown: worker list truncated`, not Historical, `total_is_lower_bound` True. | Matches. Does not say "in the visible rows" (F2). |
| Fixture (c) `call_failed` | `test_fr010_call_failed_incomplete_list`, DESIGN:746. R1 ok, R2 `call_failed` (not call one, which is `unavailable`, open item 4), `sources` row `orca worker-list R2` with `unscanned` `orca call failed (exit 1)`. Then: None, could not determine, `origin unknown: worker list call failed`, not Historical. | Matches. The "not call one" setup is correct against DESIGN:979 and the diagram at DESIGN:245. Does not say "in the visible rows" (F2). |
| (extra) note order | `test_fr010_incomplete_notes_order`, DESIGN:746. `origin unknown:` notes first, then `tab map join not observable`. | Consistent with the bullet at DESIGN:501 ("before any join-guard note") and with DESIGN:502 (SP-16 literal then `tab map join not observable`). Not a SPEC case, so it adds, does not weaken. |
| 7.2 bullet | DESIGN:501 | Byte-identical to research/04 4.2 item 2 (confirmed with `grep -cF`, count 1). Covers three of the four SPEC reasons (F1). |
| Count wording | DESIGN:746 "the three SPEC incomplete cases ... pinned by four fixtures" | Correct: three SPEC fixtures plus the order fixture. "Four incomplete cases" left only in the section 18 correction (DESIGN:1030). |
| Traceability | DESIGN:771 FR-010 row names "three list-incomplete cases (outage, full page, `call_failed`)" and keeps "four join-incomplete cases"; the test column names "the three SPEC incomplete-case fixtures" | Matches research/04 4.2 item 3. |
| Revision log | DESIGN:1030 R3-B3 row | Matches research/04 4.2 item 4, and adds the source-row name. |

No fixture name was renamed in a way that changes meaning. No SPEC acceptance fixture is missing. No restored fixture lets an unproved transcript reach Historical.

## Findings

### F1 (MAJOR): the SPEC reason "tab map unreadable" and the "tab map is read" condition are not in the design, so an unproved transcript can reach True and then Historical

- **SPEC evidence:** `merged-requirements.md:104` lists four reasons ("Orca unavailable, worker list truncated, worker list call failed or tab map unreadable") and makes True require that "the tab map is read and the join completed".
- **Design evidence:** the 7.2 bullet at `docs/designs/orchestrator-mode.md:501` carries only three: `orca_available` False, `truncated` True, `call_failed`. research/04 4.2 item 2 shows the same trim: it says the note literals follow "the SPEC reasons 'Orca unavailable, worker list truncated, worker list call failed'" and drops the fourth. A search of the design finds no `tab map unreadable` text (0 hits), and `read_tab_map` (DESIGN:401) is the only mention of the reader, with no unreadable outcome. The four join-incomplete cases at DESIGN:502 cover `session_join` None, no join with at least one worker row, path-B unmatched entry, and path-B with any scoped row. None fires on an unreadable tab map when the Run has no worker row, or under path A when workers join by `sessionId` and the other transcripts have no visible entry.
- **What is wrong:** when `orca-tabs/` cannot be read, `tab_map` is empty, so a worker transcript of an unscoped Run (or a person's `ccsession` pane session) shows "no tab-map entry". DESIGN:500 then lets it be True ("Under path A only ... may be True when the FR-010 guard holds"; under path B the True path is open when no scoped Dispatch row exists, DESIGN:500). An 8 h old one then goes to Historical. That is the weakening the lens targets: an unproved transcript reaches Historical, and the SPEC condition "tab map is read" is not enforced anywhere.
- **Smallest fix:** extend the DESIGN:501 bullet with a fourth clause, "or when the `orca-tabs` folder cannot be read (its source row has `unscanned` set; an empty but readable folder is not this case)", with note `origin unknown: tab map unreadable`, placed last in the note order, before any join-guard note. Add one non-SPEC fixture `test_fr010_tab_map_unreadable_older_transcript_unknown` to the `test_classify.py` cell (same Given, `read_tab_map` source `unscanned`), and add "tab map unreadable" to the FR-010 row at DESIGN:771. The three SPEC fixtures and their names stay as they are.

### F2 (MINOR): fixtures (b) and (c) do not assert that T is in the visible rows

- **Evidence:** DESIGN:746. Fixture (a) says "T is in the visible rows, not Historical; `summary.historical` is 0". Fixtures (b) and (c) say only "not Historical". SPEC:104 says "All three remain visible and unknown, not Historical". The cell's lead-in says "each stays visible", which covers it by reading, but a fixture-by-fixture implementer could omit the visible assertion.
- **Smallest fix:** add "T is in the visible rows; `summary.historical` is 0" to the Then of (b) and (c).

### F3 (MINOR): "each differ from the complete-negative-join control by one input" is loose

- **Evidence:** DESIGN:746. Fixture (c) adds a second scoped Run (R1 and R2) as well as the `call_failed`. Fixture (a) changes `orca_available` and `orca_rows` together. The SPEC control (2 transcripts, one mapped) is not a named fixture in the cell.
- **Smallest fix:** say "differs by the stated incompleteness input" or name the control fixture and its inputs.

### F4 (MINOR): note precedence is unstated for an unjoined transcript that has a tab-map entry under an incomplete list

- **Evidence:** DESIGN:499 gives such a transcript `Orca pane session, not in scoped Runs`; DESIGN:501 says "every unjoined transcript" gets an `origin unknown:` note. All three fixtures use "no tab-map entry", so the overlap is untested. The class (None, could not determine, never Historical) is the same either way, so no SPEC behaviour is lost.
- **Smallest fix:** add one clause to DESIGN:501 saying the `origin unknown:` note comes first and the pane note follows.

## Design choice: source-row name `orca worker-list <run>`

**Verdict: APPROVE. It stays inside the SPEC.**

- The SPEC does not pin source names. `SourceCoverage` is `name`, `coverage`, `age_seconds`, `unscanned` (SPEC:243), the report prints "one entry per SourceCoverage" (SPEC:358, :376), and a new source "adds one coverage row" (SPEC:218). Per-Run rows are an allowed use of that open-ended list.
- The SPEC condition is per Run ("every scoped Run's worker list", "no relevant list ... unscanned"), so a per-Run row is needed to say which list failed. A single `orca` row could not tell Run R1 ok from Run R2 failed, which fixture (c) depends on.
- The name appears only as a value in `sources[].name` (DESIGN:595 against the schema at DESIGN:571, `"name": str`), so the NFR-009 pinned key set is unchanged.
- `<run>` is already validated by `_check_run_ids` (DESIGN:763), so the value is safe to print.
- DESIGN:501 uses the row only as a parenthetical for `call_failed`, and budget cuts are `call_failed` (DESIGN:287), so no case depends on the name alone.
- It is not a SPEC deviation, so no new D-row is needed in section 13; it is recorded in 7.4 (DESIGN:595) and the section 18 R3-B3 row (DESIGN:1030).

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | 7.2 bullet (DESIGN:501) is byte-identical to research/04 4.2 item 2 | PASS |
| C2 | SPEC fixture (a), the outage case, is present with the same meaning and assertions | PASS |
| C3 | SPEC fixture (b), the full page with uncaptured continuation, is present with the same meaning | PASS |
| C4 | SPEC fixture (c), the `call_failed` case, is present and uses a non-first call | PASS |
| C5 | "Older" is realised as 8 h against a 6 h window, matching the SPEC control | PASS |
| C6 | No restored fixture lets an unproved transcript reach idle or Historical | PASS |
| C7 | All four SPEC None reasons (Orca unavailable, truncated, call failed, tab map unreadable) and the "tab map is read" True condition are enforced by the design | FAIL (F1) |
| C8 | Each of the three fixtures asserts "visible" as well as "not Historical" | FAIL (F2, MINOR) |
| C9 | Control-difference claim in the test cell is accurate | FAIL (F3, MINOR) |
| C10 | Note order in the bullet agrees with the notes-order fixture and with DESIGN:502 | PASS |
| C11 | Overlap of the `origin unknown:` notes with the tab-map-entry pane note is specified | FAIL (F4, MINOR) |
| C12 | FR-010 traceability row (DESIGN:771) names the three list-incomplete cases and the three fixtures | PASS |
| C13 | "Four incomplete cases" is gone from section 11 and survives only in the section 18 correction (DESIGN:1030) | PASS |
| C14 | The four join-incomplete cases and the four guard-case fixtures were kept | PASS |
| C15 | Fixture names match research/04 4.3 (four `test_fr010_*` names confirmed by grep) | PASS |
| C16 | Source-row name `orca worker-list <run>` is inside the SPEC | PASS (approved) |

## Summary

- Checks passed: 12 / 16. Failed: 4 (one MAJOR, three MINOR).
- The three SPEC acceptance fixtures are restored faithfully and none is weakened.
- One SPEC reason is missing: `tab map unreadable`. This was dropped in research/04 and carried into the design, and it leaves a path from an unreadable tab map to True and Historical.
- Tool engagement: Read 12 | Grep 9 | Glob 0 | Bash 2. No web research.
- Confidence: Verified 16/16 checks with tool evidence | Unverifiable 0 | Unchecked 0.

Verdict: FAIL
Blocking count: 1
