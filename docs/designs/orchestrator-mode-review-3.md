# Orchestrator mode design, review 3

Reviewer: independent of the design author and of reviews 1 and 2. Inputs: `docs/designs/orchestrator-mode.md` (DESIGN, after fix cycle 2), `docs/designs/orchestrator-mode-review-2.md` (REVIEW2), and `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (SPEC). Line numbers are DESIGN lines unless another file is named.

## Verdict

**FAIL.** Three blocking findings.

- R3-B1: the new path-B time window reads fields the data model does not have. `OrcaObservation` has no Dispatch start or end time, and `TranscriptTail` has only `last_record_ts`, not the earliest timestamp the rule compares. `classify.py` is pure and reads only `SweepInput`, so the rule cannot run as written, and the GQ-103(3) claim at line 54 ("The model carries every field a rule reads") is now false.
- R3-B2: one transcript can match several scoped Dispatch rows by path B (a pane reused for a second Dispatch, or two rows whose windows overlap because one has no end time). Line 488 then gives that transcript two values at once: False under the row whose window holds it, and None with `pane moved to a later session` under the row whose window does not. Two windows that both hold it give a double join. No rule decides.
- R3-B3: the cycle 2 edit changed "the three incomplete cases" in the `test_classify.py` row (line 733) to "the four incomplete cases". In that sentence the list follows SPEC FR-010's acceptance text, which names exactly three incomplete cases (an Orca outage, a full page with uncaptured continuation, an incomplete list after `call_failed`). The four guard cases are already pinned one by one later in the same cell. The design names those three SPEC fixtures nowhere else (no match for "outage" or "uncaptured continuation"), so the edit leaves them without a clear pin.

R2-B2 is fixed correctly. R2-B3 is fixed correctly. R2-B1 is correct in direction (no path-B session can now be True) but carries R3-B1 and R3-B2.

## R2-B1 check

What the fix says (7.2 lines 488 to 491):

- A path-B join needs the earliest `timestamp` in the transcript tail to fall inside the Dispatch row's window, from its start time to its end time, or to `collected_start` when the row has not ended.
- A match outside the window, or on a row with no observable start time, does not join. The row is could not determine with note `pane moved to a later session`, and the transcript is None with the same note.
- A join inside the window is False with note `joined by pane: latest session of the pane`.
- Fourth guard case: under path B, when at least one scoped Dispatch row exists, every unjoined transcript with no tab-map entry is None with note `earlier pane session not joinable (tab map keeps only the latest session)`.
- Line 490: the no-entry True path applies under path A only.

`/clear`, resume and a person rerun, under path B:

| Case | Worker's earlier transcript | Pane's latest session | Result |
|---|---|---|---|
| `/clear` while the Dispatch is running | No entry; fourth case gives None | New short transcript, earliest record inside the open window (to `collected_start`); joins, False, latest-session note | Correct and safe. The worker's continuation is shown as the worker |
| `/clear` after the Dispatch ended | No entry; None | Earliest record after the end time; does not join; row could not determine, transcript None | Correct and safe |
| Resume inside the window (for example Orca resuming a worker) | No entry; None | Records after the Dispatch start; joins, False | Correct |
| Resume of an old session after the Dispatch ended | No entry; None | Earliest tail record is either old (before the start) or new (after the end); both outside; None | Correct and safe |
| Person rerun after the Dispatch ended | No entry; None | Starts after the end time; None | Correct and safe |
| Person rerun while the Dispatch is still open | No entry; None | Inside the window; False with the latest-session note | Not True, so FR-010 holds. Line 488 states this limit ("a person rerun inside the window cannot be told apart") |

Under path B, with any scoped Dispatch row, no transcript can now be True: an entry that joins no row is None (line 489), a no-entry transcript is None (fourth case), and an outside-window match is None. So every earlier session of a reused pane is None, never True. That part of the fix is right.

A Dispatch row with no end time: handled; the window runs to `collected_start`. A row that has ended but whose end-time field is missing is not told apart from a running row (minor note m4).

Clock skew: the design says nothing about it. Transcript timestamps and Orca times come from the same host clock in Phase 1 (remote hosts are not scanned, line 506), so true skew is small, but no tolerance, no time zone rule and no boundary rule (inclusive or exclusive) is stated. Every skew outcome is None or False, never True, so this is minor (m3), not blocking.

The open-item 23 dependency on step 1.0a is stated in three places that agree: 7.2 line 488 (fields UNVERIFIED, from step 1.0a item 4), capture item 4 at line 879 (names "the fields that carry the Dispatch start and end times" and open item 23), and open item 23 at line 985 (closed by step 1.0a item 4; until then no path-B join is made).

What is wrong: R3-B1 (the fields are not in the model) and R3-B2 (several rows per pane). Also, "earliest timestamp in the transcript tail" is not the session start for a transcript over 256 KiB, and the revision log (line 1005) says "the transcript's earliest timestamp", which is a different value (minor note m2).

## R2-B2 check

Result: fixed. No blocking finding.

- 7.2 line 490: every True reached by the no-entry path carries `origin not proved: no tab-map entry; may be a worker of a Run outside the scope`, "in the report row and in the JSON `notes`". The report has a `Notes` column (section 7.5), and `Classification.notes` is in the model (line 457) and the JSON schema (line 564).
- Pinned in classify: line 733, "under path A a transcript with no tab-map entry and no join is True when the guard holds and carries note `origin not proved ...`", plus a worker of an unscoped Run in the same worktree that "is never True without that note".
- Pinned in the report and the JSON: line 734, "a True row with the `origin not proved` note prints the note in its row and in the JSON `notes` (D9)".
- D9 (line 809) states the same note with the same text, says "Under path A only", and names R2-B2 as a source. Section 14 SP-29 (line 847), the FR-010 row (line 758) and open item 22 (line 984) agree.

The note text names only Runs outside the scope. Under path A, a scoped worker's own session after a `/clear`, with no tab-map entry, can also take this True (minor note m6).

## R2-B3 check

Result: fixed. No blocking finding.

- 7.2 line 503: a transcript is unreadable when its open raises `OSError`, or when its tail (`read_transcript_tail`, the last 256 KiB with the first partial line dropped) holds no complete JSON record with both `timestamp` and `sessionId`. "A last line cut mid-object is skipped, and the transcript stays readable when an earlier complete record has both fields."
- Fixture (line 733): a truncated-JSONL transcript ("last record cut mid-object, no complete record with both `timestamp` and `sessionId`") gives could not determine with its `unscanned:` note; a transcript cut only in its last line with an earlier complete record "stays readable and is classified normally"; an `OSError` open gives `unscanned: transcript not readable`. The rule and the fixture now agree, and the truncated-last-line case is pinned as readable, as the brief requires.
- Open item 16 (line 978) uses the same two triggers and points to 7.2.
- SPEC byte-limit rules (SPEC line 294): the tail read is "the normal case, not a limit hit: drop bytes up to and including the first newline, decode as UTF-8 with `errors="replace"`, and parse the remaining complete lines". The design's rule is that parse, plus a definition of "no usable record". It agrees. The SP-28 limits are unchanged (`TRANSCRIPT_TAIL = 256 * 1024` in section 7.3; open item 19 still marks the limits proposed). The 256 KiB boundary fixtures in `test_probes_allowlist.py` (line 732) remain.
- SPEC line 442 detection says only "`OSError` on open" while its fixture is truncated JSONL. The design resolves that SPEC gap by reading lines 294 and 442 together. It is not listed under "Not counted as deviations" in section 13 (minor note m7).

Two edges the rule does not name, both safe (could not determine, never True): a transcript whose last record alone is over 256 KiB (a large tool result) has no complete record in the tail and is marked unreadable though valid (minor note m8); and "first partial line dropped" differs from SPEC line 294's unconditional "drop bytes up to and including the first newline" for a file under 256 KiB (minor note m9).

## Regression scan

- Sections 3 and 5: not touched by cycle 2. Publication statements still agree (one report on exit 0, none at a report name on exit 1 before the commit point).
- Section 7: the path-B window (line 488) reads fields absent from the 7.2 model (R3-B1), and line 488 has no rule for several rows per pane (R3-B2). Line 490 says "Under path A only" and then "Under path B, when any scoped Dispatch row exists, this True path never applies", which leaves path B with no scoped Dispatch row undefined (minor note m1). Section 2.2 GQ-108 (line 59) is still accurate.
- Section 11: the "four incomplete cases" edit (R3-B3). Otherwise every new note text in 7.2 has a fixture: the four guard cases, the three pane-reuse fixtures, the no-start-time row, the latest-session note, the `origin not proved` note in classify and report, and the readable and unreadable transcript cases.
- Section 12: the FR-010 row (line 758) names the four join cases and the time window. Its test column names `test_report.py` only for the SP-16 literal, not for the `origin not proved` case (minor note m10).
- Section 13: D9 agrees with 7.2. "Total: 9 deviations." (line 811) matches the revision log, which adds no deviation in cycle 2.
- Section 17: open items 1 to 23, "Total: 23 open items." (line 987). Matches the revision log (item 23 added). Open items 16, 22 and 23 agree with 7.2.
- Section 18: the cycle 2 table names 7.2, 11, 12, 13, 14, 15.1 and 17. Each has a matching change, apart from the data model gap of R3-B1. Line 1005 says "the transcript's earliest timestamp"; 7.2 says "the earliest `timestamp` in the transcript tail" (m2).
- Allowlist: `ALLOWED_ORCA` (lines 515 to 524) is still exactly eight templates over seven verbs: `run-current`, `worker-list`, `worker-show`, `task-list --ready`, `task-list`, `worktree ps`, `worktree list`, `worktree current`. `FORBIDDEN_TOKENS` still holds `--include-remote` and `--agent-wait`. The window rule adds no Orca call; it reads `worker-show` fields only.
- Em dashes: none (`grep -c` gives 0). `TODO`, `TBD`, `FIXME`, `XXX`: none.

## Blocking findings, each with an exact fix

### R3-B1. The path-B time window reads fields the model does not carry

Defect. Line 488 compares "the earliest `timestamp` in the transcript tail" with "the Dispatch row's own window, from the row's start time to its end time". The data model in 7.2 has neither value:

- `OrcaObservation` (line 449) is the SPEC list (SPEC line 231) plus `dispatch`, `run` and `session_join`. Neither list has a start or end time.
- `TranscriptTail` (line 451) has `last_record_ts` only.

`classify.py` is pure and reads only `SweepInput` (section 7.1), so the rule cannot be implemented from the model as designed. Line 54 (GQ-103(3)) says "The model carries every field a rule reads", which is now false. The fix for R2-B1 is therefore incomplete.

Exact fix:

- 7.2 line 449, `OrcaObservation`: append "`dispatch_started: datetime | None`, `dispatch_ended: datetime | None` (design: the Dispatch row's start and end times from `worker-show`, for the path-B window; None until step 1.0a item 4 names the fields, open item 23)".
- 7.2 line 451, `TranscriptTail`: add "`first_record_ts: datetime | None` (the earliest `timestamp` among the complete records in the tail; for a file over 256 KiB this is not the session start)".
- 7.2 line 488: name the fields: "`first_record_ts` must fall inside `dispatch_started` to `dispatch_ended`, or to `collected_start` when `dispatch_ended` is None".
- Section 7.1 line 392: change the `read_transcript_tail` comment to "last 256 KiB, first partial line dropped; sets `first_record_ts` and `last_record_ts`".
- Section 11: add a reader case "`read_transcript_tail` sets `first_record_ts` to the earliest complete record's timestamp".
- Section 18 cycle 2 R2-B1 row: add "and the two `OrcaObservation` fields and `TranscriptTail.first_record_ts` (7.2)".

### R3-B2. One pane session can match several scoped Dispatch rows by path B, with no rule

Defect. Under path B, `session_join` is a pane key or terminal handle. Two scoped Dispatch rows can carry the same one: a worker pane reused for a later Dispatch, or a retry in the same pane. The tab map holds one session for that pane. Line 488 then says two things about the same transcript:

1. For the row whose window holds it: it joins, False, shown as `orca:<dispatch>` with `joined by pane: latest session of the pane`.
2. For the row whose window does not: "the row is could not determine with note `pane moved to a later session`, and that transcript is None with the same note".

A transcript cannot be both False and None. If both windows hold it (for example the first row has no end time, so its window runs to `collected_start`), it joins two rows and is shown as two Orca rows. The implementer has to guess. The duplicate Dispatch rule (line 499) covers only rows that share one Dispatch id, not this case.

Exact fix:

- 7.2 line 488, after "carries note `joined by pane: latest session of the pane`...": add "When several scoped Dispatch rows match one tab-map entry by path B: if exactly one row's window holds the transcript, it joins that row only and is False; each other matching row is could not determine with note `pane moved to a later session`, and that note is not added to the transcript. If two or more windows hold it, it joins none of them: each such row is could not determine with note `conflict: one pane session matches several Dispatch rows`, and the transcript is None with the same note. The transcript is None with `pane moved to a later session` only when no matching row's window holds it."
- Section 11 `test_classify.py` (line 733): add "two scoped Dispatch rows with the same pane key, the first ended before the second started: the latest session joins only the second row and is False, and the first row is could not determine with `pane moved to a later session`; and two rows whose windows both hold the session: both rows could not determine with the `conflict:` note, and the transcript None".
- Section 18 cycle 2 R2-B1 row: name the added rule.

### R3-B3. "Four incomplete cases" replaced the SPEC's three FR-010 incomplete-case fixtures

Defect. Line 733 reads "FR-010 complete-negative join, the four incomplete cases, the five exemptions and the SP-29 two-Run fixture". That list follows SPEC FR-010's acceptance column item for item (SPEC line 104): "Complete-negative-join case ...; Incomplete cases: an older transcript during an outage; an older unjoined transcript after a full page with uncaptured continuation; an incomplete list after `call_failed`. All three ...; Exemptions: one fixture each for ... [five]; Other-Run fixture [SP-29]". The SPEC has three incomplete cases. REVIEW2 (line 125) read "the three incomplete cases" as the three guard cases and asked for "four", and the revision log (line 1005) records "changed 'three' to 'four' incomplete cases". The four guard cases are already pinned one by one later in the same cell (`session_join` None, the SPEC line 236 fixture, the path-B no-entry row and the pane-reuse fixtures). The design names the SPEC's outage, full-page and `call_failed` fixtures nowhere (no match for "outage" or "uncaptured continuation"). So the count is now wrong against the SPEC, and an implementer who follows the revision log drops three FR-010 acceptance fixtures.

Exact fix:

- Section 11 line 733: replace "the four incomplete cases" with "the three SPEC incomplete cases (an older transcript during an Orca outage, an older unjoined transcript after a full page with uncaptured continuation, an incomplete list after `call_failed`; each stays visible with `person_started` None, never idle or Historical)". Keep the four guard-case fixtures as they are listed later in the cell.
- Section 18 cycle 2 R2-B1 row: replace "changed 'three' to 'four' incomplete cases" with "named the four join-incomplete cases in 7.2, D9 and the FR-010 and SP-29 rows; the three SPEC incomplete-case fixtures in section 11 are unchanged".

## Minor notes

- m1. Line 490 says the no-entry True path applies "Under path A only", then "Under path B, when any scoped Dispatch row exists, this True path never applies". For path B with no scoped Dispatch row, the first sentence forbids True and no guard case gives None, so the value is undefined. Fix: "Under path A, or under path B when no scoped Dispatch row exists, ...", and make D9 and the SP-29 row match.
- m2. "Earliest timestamp in the transcript tail" is not the session start for a transcript over 256 KiB, and a session started before its Dispatch row's start (a pane launched first, then dispatched) never joins. Both outcomes are None, so they are safe, but 7.2 should say so, and step 1.0a item 4 should record whether Orca records the Dispatch start before or after the pane's session starts. The revision log (line 1005) says "the transcript's earliest timestamp"; make it match 7.2.
- m3. No clock rule: state that both times are compared as UTC instants, that the window is inclusive at both ends, and that skew can only move a row to could not determine or to False, never to True.
- m4. A row that has ended but whose end-time field is absent gets a window to `collected_start`, so a later person rerun can join as False. Fix: "a row whose status is terminal and whose end time is None has no observable window and does not join by path B".
- m5. A row with no observable start time, and every path-B match while open item 23 is open (line 985), get note `pane moved to a later session`, which states a fact nobody observed. Use `Dispatch time window not observable` for those cases.
- m6. Under path A, a scoped worker's own session after a `/clear`, with no tab-map entry, can be True with the `origin not proved` note, whose text names only Runs outside the scope. Consider "may be a worker session not joined to a scoped Dispatch row".
- m7. The R2-B3 rule reads SPEC lines 294 and 442 together (the SPEC detection says only `OSError` on open). Add it to section 13 "Not counted as deviations" with that reason.
- m8. A transcript whose last record alone is over 256 KiB (a large tool result) has no complete record in the tail and is marked `unscanned: transcript not readable` though valid. Name this case in line 503 and give it a fixture, or a clearer note such as `last record over 256 KiB`.
- m9. "First partial line dropped" (lines 392 and 503) differs from SPEC line 294, which always drops bytes up to the first newline, for a file under 256 KiB. State which one applies; the 256 KiB minus 1 boundary fixture will expose the difference.
- m10. The FR-010 traceability row (line 758) lists `test_report.py` only for the SP-16 literal. Add the `origin not proved` report case (line 734).
- m11. A later session that has a tab-map entry and fails the window gets two candidate notes: `Orca pane session, not in scoped Runs` (line 489) and `pane moved to a later session` (line 488). State the order, or that the second replaces the first.

Minor count: 11.

## Self-audit

What I checked, and how:

- REVIEW2 lines 1 to 150 (verdict, all three blocking findings and their exact fixes) against DESIGN lines 26, 54, 59, 386 to 400, 441 to 507, 508 to 547, 586 to 633 (report notes column), 731 to 734, 758, 795 to 830, 847, 879, 886 to 890, 901, and 957 to 1007.
- SPEC lines 104 (FR-010 with SP-29 and its acceptance fixtures), 229 to 234 (the `OrcaObservation` and `SweepInput` field lists), 236 (SP-16), 286 to 296 (seams and byte limits, SP-28) and 442 (unreadable inputs).
- Each new note text in 7.2 against a fixture in section 11, and each changed row in sections 12, 13, 14, 15.1 and 17 against 7.2.
- Each data field the new rules read against the model in 7.2 and the SPEC field list (this found R3-B1).
- The `/clear`, resume and person-rerun cases, an open row, a missing end time, skew, and two rows on one pane, traced through lines 488 to 491 (this found R3-B2 and m1 to m5).
- The SPEC acceptance list for FR-010 against the section 11 wording, plus a grep for "outage" and "uncaptured continuation" in DESIGN (this found R3-B3).
- Counts: "Total: 9 deviations." and "Total: 23 open items."; the eight `ALLOWED_ORCA` templates and the two forbidden tokens; a grep for an em dash, `TODO`, `TBD`, `FIXME` and `XXX` (no matches).

Not checked: the ccsession source itself (REVIEW2 checked it and cycle 2 did not change those citations), sections 8 to 10 and 16 (not touched by cycle 2), and Orca's real `worker-show` time fields (UNVERIFIED until step 1.0a).
