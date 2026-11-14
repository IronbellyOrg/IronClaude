# QA Report: R3-B1 SPEC-fidelity lens

**Topic:** R3-B1 edits (items 2.1 to 2.6) to `docs/designs/orchestrator-mode.md`
**Date:** 2026-11-09
**Phase:** fix-cycle gate, domain lens (SPEC fidelity)
**Fix authorization:** false (report only; no file other than this report was written)
**Fix cycle:** 1 (first review of R3-B1)

## Method

- Baseline for the diff: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/design-base.md` (1013 lines), compared with the current DESIGN (1023 lines) by `diff` and a word-level `git diff --no-index`. The diff has exactly 12 hunks: DESIGN lines 60, 398, 455, 457, 468 (inserted), 496, 740-741, 766, 887, 993, 1013 and 1016-1023 (inserted). No other line changed.
- Reference text: research/04 lines 77-132 (edits 1 to 9 and fixtures), research/09 Gap 4 (lines 139-174), SPEC (`merged-requirements.md`) lines 96-104, 132, 143, 227-238, 555-563.
- Static Orca bundle check (read-only): `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js`.

## Items Reviewed (what the edits touch vs what the SPEC fixes)

| Area the lens attacks | Result of the diff |
|---|---|
| New Orca verb, flag or allowlist template | None. `ALLOWED_ORCA` (DESIGN 523-532) and `FORBIDDEN_TOKENS` (534) are not in any hunk. Still 8 templates over 7 verbs, as SPEC NFR-014 (`merged-requirements.md:143`) pins. |
| Weakened D9 | None. D9 (DESIGN 817) and the SP-29 row (855) are not in any hunk. D9 already says "a path-B join also needs the Dispatch row's time window"; R3-B1 only defines that window. |
| Change to the FR-010 guard | None. The guard paragraph (DESIGN 499, four cases) and the True-path paragraph (498) are not in any hunk. |
| New read the eight templates do not cover | None. The three Dispatch times come from `worker-show --dispatch <dispatch> --json` (template at DESIGN 526). `first_record_ts` comes from the transcript tail the design already reads (DESIGN 398). Capture item 4 (DESIGN 887) adds a disk read of one transcript, which is the same kind of read as item 16 (DESIGN 986). |
| JSON v1 / NFR-009 | Untouched: DESIGN 556-592 not in any hunk; the new fields stay inside the model and the `notes` strings. |

## Verification of the Orca field names (DESIGN 455, 887, 993)

- Bundle byte 1422409 holds `dispatchedAt:e.dispatched_at,completedAt:e.completed_at` inside `hG`, the `dispatch` projection; `status:e.status` sits in the same object (same `hG` text, a few hundred bytes earlier). `workerShow` is at byte 1447759.
- Both return paths of `orchestration.workerShow` return `dispatch:hG(...)`: the no-worker path `E6e` (`return{dispatch:hG(n),worker:T6e(n),...}`) and the worker path (`return{dispatch:hG(i),worker:gG(a),...}`). So `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` are real names for the non-federated path. The federated path `r8e` returns early and was not checked (outside Phase 1; research/04 line 128 says so, DESIGN does not).
- Dispatch status values in the bundle are `pending`, `dispatched`, `completed`, `failed`, `circuit_broken` (bytes 211580, 1367200), and `status IN ('pending', 'dispatched')` is the bundle's own "active" test (e.g. byte 1352225). The DESIGN rule "open window when `dispatch_status` is `pending` or `dispatched`" (DESIGN 496) matches.

## Findings

All findings are MINOR. No BLOCKING or MAJOR finding was found.

### F-1 (MINOR) Window fixtures drop the join precondition that research/04 carries

- Evidence: DESIGN 741, `test_path_b_window_open_row_joins` reads "row D1 with `dispatch_started` 10:00, `dispatch_ended` None and `dispatch_status` `dispatched`, transcript S with `first_record_ts` 10:05, `collected_start` 12:00: S joins D1". research/04 line 114 has, in the same Given, "`session_join` pane P; tab-map entry P to session S". The preface "path B assumed" (research/04 line 110) is also gone. SPEC FR-010 (`merged-requirements.md:104`) allows a False only from "a positive transcript-to-worker join", and DESIGN 499 case 1 makes every unjoined transcript None while `session_join` is None.
- What is wrong: as written, an implementer who builds exactly the stated Given gets S = None, not "S joins D1". The other three fixtures in the same DESIGN 741 cell (`..._inclusive_bounds`, `..._terminal_row_without_end_has_no_window`, `..._row_without_start_has_no_window`) also never state that the pane key matches a tab-map entry, so their "no join" outcomes could arise without the window rule being exercised.
- Smallest fix: in the DESIGN 741 text of `test_path_b_window_open_row_joins`, add "`session_join` pane P and a tab-map entry mapping P to S" and give the other three fixtures "same pane setup".

### F-2 (MINOR) The time-parsing rule is wider than the window it serves

- Evidence: DESIGN 468 "every Orca and transcript time is parsed to an aware UTC `datetime`. Accepted forms are SQLite ... and ISO 8601 ...". SPEC 238 (`merged-requirements.md:238`) leaves the `agentWait` timestamp field's form UNVERIFIED ("the `agentWait` timestamp field captured in step 1.0a (UNVERIFIED field)"). Text is verbatim research/04 edit 3, so the edit is faithful to the plan; the plan itself reaches past the window.
- What is wrong: the rule fixes the accepted forms for fields whose form the SPEC says is unknown (the `agentWait` time). An epoch-number form would parse to None and the row would fall into the unknown-age group (safe direction, no wrong class), but the design now pre-commits a form it has no evidence for.
- Smallest fix: change "every Orca and transcript time" to "every Dispatch time and transcript `timestamp` the model holds".

### F-3 (MINOR) The fixtures name a parser that 7.1 does not define

- Evidence: DESIGN 740 `test_worker_show_dispatch_times_sqlite_form` etc. use "the `worker-show` parser builds `OrcaObservation`" (research/04 line 106 says the same). DESIGN 7.1 `probes.py` (lines 363-400) lists `collect`, the readers and `read_transcript_tail`, and no `worker-show` parser or time parser. DESIGN 468 does not say which module holds the time parser.
- What is wrong: the six new reader and parser fixtures have no named seam for four of them (the two `read_transcript_tail` ones do). Only `collect` with a patched `_orca` can reach the parser.
- Smallest fix: add one line to 7.1 `probes.py`, for example `def parse_worker_show(data: object) -> OrcaObservation` and `def parse_time(text: object) -> datetime | None`, or say in 468 that the parse runs inside `collect` and the fixtures drive it through `patch_orca`.

### F-4 (MINOR) "Compared as UTC instants" conflicts with the seconds cut

- Evidence: DESIGN 496 "`first_record_ts`, cut to whole seconds, ... both ends included ... Times are compared as UTC instants ... Clock skew or the seconds cut can only move a session to could not determine or False, never to True." DESIGN 741 inclusive-bounds fixture: S at 11:00:00.400 joins a row that ended at 11:00:00, and the iso fixture (740) shows `dispatchedAt` can carry `.123`.
- What is wrong: only `first_record_ts` is cut, so the comparison is not between instants. The cut lets a session that began up to 0.999 s after the end join (a wider False join) and, against a `dispatch_started` with milliseconds, can push a session just before the start. The "never to True" sentence is correct, but only because of guard case 4 (DESIGN 499), which the sentence does not cite. FR-010 stays safe either way (False needs a window match; no path-B session can be True).
- Smallest fix: say "`first_record_ts` is cut to whole seconds and then compared with the other two times as UTC instants" and append "(no path-B session can be True: guard case 4)".

### F-5 (MINOR) The row-level "could not determine" outcome is not tied to `classify.RULES`

- Evidence: DESIGN 496 "A path-B match outside that window does not join: the row is could not determine with note `pane moved to a later session`. A match on a row with no observable window does not join: the row is could not determine with note `Dispatch time window not observable`." SPEC FR-006 (`merged-requirements.md:100`): "Each session row gets exactly one class ... chosen by the ordered rule table." SPEC NFR-010 (`merged-requirements.md:139`): precedence is the order of `classify.RULES`. DESIGN 472-484 has no rule for this outcome. Same prose style at DESIGN 507, 508 and 511, so this is the design's convention, and review 3 accepted the out-of-window form.
- What is wrong: R3-B1 widens the trigger. Before, only "a row with no observable start time" had no window (design-base line 494). Now a terminal row (`completed`, `failed`, `circuit_broken`) with `dispatch_ended` None also has none, and DESIGN 887 itself says it is not known whether `completedAt` is set for `failed` and `circuit_broken`. A pane-matched row that Orca proves exited could therefore print could not determine instead of the class its own rules give. The result is conservative (never a false stall) but the sentence does not say whether the class override comes before or after the nine rules.
- Smallest fix: add to 496 "the join outcome adds the note and the row is classified by `classify.RULES`; the fallback applies only when no earlier rule matched", or add the case to rule 9 in the 472-484 table.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | `ALLOWED_ORCA` unchanged: 8 templates, 7 verbs (DESIGN 523-532 not in any diff hunk; SPEC NFR-014 `:143`) | PASS |
| C2 | No new verb, flag or token; `FORBIDDEN_TOKENS` unchanged (DESIGN 534) | PASS |
| C3 | New Dispatch times come only from the existing `worker-show` template (DESIGN 526); `first_record_ts` from the existing transcript read (DESIGN 398) | PASS |
| C4 | D9 row (DESIGN 817) not weakened: not in any hunk | PASS |
| C5 | FR-010 guard text (DESIGN 497-499) not changed: not in any hunk | PASS |
| C6 | SP-29 row (DESIGN 855) and the FR-010 SPEC rule (`merged-requirements.md:104`) still hold: path B cannot yield True | PASS |
| C7 | Edits 1 to 9 match research/04 lines 87-95 word for word (word-level diff of all 12 hunks) | PASS |
| C8 | Fixture text matches research/04 section 2.3 including the Given of each fixture | FAIL (F-1, MINOR) |
| C9 | Orca field names `dispatch.dispatchedAt`, `dispatch.completedAt`, `dispatch.status` exist in the 1.4.245 bundle on both `worker-show` return paths | PASS |
| C10 | Window-open statuses `pending` and `dispatched` match the bundle's status enum | PASS |
| C11 | JSON v1 key set and NFR-009 untouched (DESIGN 556-592) | PASS |
| C12 | Deviation total 9 (DESIGN 819), open-item total 23 (DESIGN 995), em-dash count 0, no `TODO` or `TBD` (re-run; grep exit 1) | PASS |
| C13 | No R3-B2 or R3-B3 content beyond the permitted forward reference (DESIGN 496); `### Fix cycle 3` holds only the R3-B1 row (DESIGN 1017-1023) | PASS |
| C14 | Section 12 FR-010 trace edit (DESIGN 766) and the FR-010 Covers entry (DESIGN 740) are the research/09 Gap 4 recommendation, within item 2.5's gate | PASS |
| C15 | Time-parsing rule limited to what the window needs (DESIGN 468) | FAIL (F-2, MINOR) |
| C16 | Every new fixture has a named seam in 7.1 | FAIL (F-3, MINOR) |
| C17 | The window comparison is stated consistently (DESIGN 496 vs 740-741) | FAIL (F-4, MINOR) |
| C18 | The row-level could-not-determine outcome is consistent with FR-006 and NFR-010 (`merged-requirements.md:100`, `:139`) | FAIL (F-5, MINOR) |

## Summary

- Checks passed: 13 / 18 (all five FAIL rows, C8 and C15 to C18, are MINOR findings and do not fail the gate).
- BLOCKING: 0. MAJOR: 0. MINOR: 5 (F-1 to F-5).
- Confidence: Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The live Orca output shape stays UNVERIFIED by design until step 1.0a (DESIGN open item 23); that is a design open item, not a check of this lens.
- Tool engagement: Read: 12 | Grep: 11 | Glob: 2 | Bash: 10 (diff against the baseline, bundle byte reads, mechanical re-run). No web research was performed.
- Out of scope per the scope note and not graded: the several-rows rule, the forward reference "Several matching rows follow the R3-B2 rule below." (DESIGN 496), and the transcript outcome for a path-B match that does not join (the sentence "and that transcript is None with the same note" was removed from DESIGN 496; fixtures at 741 still assert it). Phase 3 item 3.1 must restore it, including the transcript's note for the `Dispatch time window not observable` case.

Verdict: PASS
Blocking count: 0
