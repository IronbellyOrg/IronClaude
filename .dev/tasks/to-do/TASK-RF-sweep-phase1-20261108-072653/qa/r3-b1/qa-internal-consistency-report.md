# QA Report: R3-B1 internal-consistency lens

**Target:** `docs/designs/orchestrator-mode.md` (1023 lines, read this session) as edited by items 2.1 to 2.6.
**Inputs read:** DESIGN lines 1-36, 56-67, 351-404, 440-510, 736-741, 766, 868-901, 965-1023; research/04 lines 40-140; research/09 Gap 4 (lines 139-175); `phase-outputs/test-results/r3-b1-mechanical.md`; SPEC `merged-requirements.md` lines 225-245.
**fix_authorization:** false. No file edited except this report.
**Scope note applied:** the R3-B2 several-rows rule, the forward reference "Several matching rows follow the R3-B2 rule below." (DESIGN:496) and the transcript outcome for a path-B match that does not join are Phase 3 work and are not graded here.

## Method

I took every field the 7.2 path-B rule (DESIGN:496) reads and looked each one up in the 7.2 model table (DESIGN:451-466). I then compared the names across 7.1 (398), 2.2 GQ-103(3) (60), section 11 (740, 741), section 12 (766), 15.1 item 4 (887), 17 items 22 and 23 (992, 993) and 18 (1023). I listed all eight `UNVERIFIED` hits in the file and checked each against open item 23.

Fields read by DESIGN:496 and where the model defines them:

| Field read by the rule | Model definition | Same name and type |
|---|---|---|
| `first_record_ts` | DESIGN:457 `first_record_ts: datetime \| None` | yes |
| `dispatch_started` | DESIGN:455 `dispatch_started: datetime \| None` | yes |
| `dispatch_ended` | DESIGN:455 `dispatch_ended: datetime \| None` | yes |
| `dispatch_status` | DESIGN:455 `dispatch_status: str \| None` | yes |
| `session_join` | DESIGN:455 `session_join: str \| None` | yes |
| `file_name`, `terminal_handle`, `session_id` | DESIGN:458 `TabMapEntry` | yes |
| `collected_start` | DESIGN:454 `SweepInput`, name only, no type | name yes, type not stated (IC-2) |
| transcript `sessionId` | `TranscriptTail.session_id` (DESIGN:457) | JSON key versus model field, pre-existing (IC-2 note) |

Cross-section name comparison: 7.1:398, GQ-103(3):60, 15.1:887, 17:993, 18:1023, and the fixtures at 740 and 741 all use the same four model names. The three source names `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` appear only in 455, 740, 887 and 993, and 455 maps them to the three model fields. DESIGN:496 matches research/04 edit 4 word for word. DESIGN:455, 457, 468, 398, 60, 887, 993 and 1017-1023 match research/04 edits 1, 2, 3, 5, 6, 7, 8 and 9. The cycle 2 row at 1013 now reads "the earliest `timestamp` in the transcript tail" (m2 applied).

## Findings

All findings are MINOR. I found no BLOCKING and no MAJOR finding.

### IC-1 (MINOR) Section 1 still states the defect in the present tense

- Side A, DESIGN:9: "R3-B1: the session-to-Dispatch time-window rule reads three time fields (Dispatch start, Dispatch end, and the earliest transcript timestamp) that the data model (`OrcaObservation`, `TranscriptTail`) lacks."
- Side B, DESIGN:455 and 457: the model now defines `dispatch_started`, `dispatch_ended`, `dispatch_status` and `first_record_ts`.
- Effect: a reader of section 1 is told the model lacks the fields, and section 7.2 says it has them. It also says "three" where the fix adds four fields (`dispatch_status` is the fourth).
- Why only MINOR: lines 7-8 frame the bullets as findings "closed by its own review gate", and section 18 (1017-1023) records the fix. research/04 gives no edit for section 1.
- Smallest fix: append "(fixed in fix cycle 3, section 18)" to the bullet, or change it to past tense, when the R3-B1 gate closes.

### IC-2 (MINOR) `collected_start` has no type or time zone in 7.2, but the path-B rule compares it with aware UTC values

- Side A, DESIGN:454: `collected_start`, `collected_end` appear with no type. The SPEC types them (`merged-requirements.md:230` says `collected_start: datetime`).
- Side B, DESIGN:468 says every Orca and transcript time is an aware UTC `datetime`, and DESIGN:496 compares `first_record_ts` with "`collected_start`" when `dispatch_ended` is None.
- Effect: Python raises `TypeError` when an aware and a naive `datetime` are compared. The design never says `collected_start` is aware UTC.
- Related, same cause: GQ-103(3) (DESIGN:60) claims "every field a rule reads" but lists neither `session_join` nor `collected_start`. It is a list of examples, so this is not a contradiction. The transcript `sessionId` (DESIGN:495) is the JSON key, and the model field is `session_id`.
- Smallest fix: at DESIGN:454 write `collected_start: datetime`, `collected_end: datetime` (aware UTC), or extend the DESIGN:468 sentence to cover them.

### IC-3 (MINOR) The path-B rule does not say what a None `first_record_ts` does

- Side A, DESIGN:457: `first_record_ts: datetime | None`. DESIGN:468 says an unparseable value becomes None.
- Side B, DESIGN:496: "`first_record_ts`, cut to whole seconds, must fall inside the row's window" reads it with no None branch. A transcript with a complete record whose `timestamp` string does not parse is still "readable" under the DESIGN:1015 rule, so it can reach the rule with `first_record_ts` None.
- Effect: the outcome (join or no join) is undefined for that input. The other three window fields have a stated None outcome (`has no observable window`).
- Smallest fix: add "A None `first_record_ts` is not inside any window" to DESIGN:496, with the same row outcome as a match outside the window.

### IC-4 (MINOR) Section 11 and section 12 use looser wording than the rule

- DESIGN:741 (the test_classify.py row) says "a row with no observable start time never joins by path B", while DESIGN:496 defines "no observable window" as a None `dispatch_started`, or any status other than `pending` or `dispatched` with `dispatch_ended` None. The later fixture `test_path_b_terminal_row_without_end_has_no_window` covers the wider case, so the behaviour is not contradicted.
- DESIGN:741 also says "whose earliest timestamp is outside the Dispatch row's window", where the model name is `first_record_ts`.
- DESIGN:766 (FR-010 row) names "the six reader and parser fixtures of the path-B time fields" in the `test_probes_allowlist.py` column but does not name the four path-B window fixtures in the `sweep/test_classify.py` parenthesis ("the D9 join fixtures and the SPEC line 236 fixture"). research/04 left the anchor phrase "no observable start time" in place for the R3-B2 insertion, which explains the first item.
- Smallest fix: wording only. Change "start time" to "window" and "earliest timestamp" to `first_record_ts` when item 3.1 edits that cell, and add the four window fixtures to the DESIGN:766 test column.

### IC-5 (MINOR) Section 11 names a `worker-show` parser that section 7.1 never declares

- Side A, DESIGN:740: three fixtures say "The `worker-show` parser builds `OrcaObservation`" and check `dispatch_started`, `dispatch_ended` and `dispatch_status`.
- Side B, DESIGN:386-399: the 7.1 signature list for `probes.py` has `read_worktree`, `parse_status`, `read_packages`, `read_ledger`, `read_contract`, `read_transcript_tail`, `read_tab_map`, `read_orca_version`, `bind_run` and `collect`. It has no function that turns a `worker-show` body into `OrcaObservation`. A grep for `parse_worker`, `parse_show` and `_to_observation` finds nothing.
- Effect: the three parser fixtures test a unit whose name and signature the design does not give. The same gap is in research/04 (2.3 table), so it was inherited, not introduced by items 2.1 to 2.6.
- Smallest fix: add one signature to 7.1, for example `def parse_worker_show(data: object) -> OrcaObservation`, and name it in the DESIGN:740 fixtures.

### IC-6 (MINOR) "confirmed by step 1.0a" reads as already confirmed

- DESIGN:455: "names read statically from the Orca 1.4.245 bundle and confirmed by step 1.0a item 4, open item 23". DESIGN:496: "are confirmed by step 1.0a item 4 (open item 23)".
- DESIGN:993 (open item 23) says the same fields are open: "That `worker-show` `dispatch.dispatchedAt`, ... carry a Dispatch row's start time, end time and status live".
- Effect: no sentence now calls the times `UNVERIFIED`, and the word does not appear for them anywhere (all eight `UNVERIFIED` hits, at lines 49, 65, 126, 518, 605, 898, 954 and 985, are about other things). Two sentences use present-tense "are confirmed". The document's own convention for a pending capture is the word UNVERIFIED (for example DESIGN:518).
- Why only MINOR: research/04 edit 4 prescribes this wording, open item 23 and capture item 4 hold the fields open, and the behaviour column of item 23 is consistent with 496.
- Smallest fix: write "to be confirmed by" in both places, or add "UNVERIFIED until" to the DESIGN:455 sentence.

## Points looked at that are not findings

- No sentence contradicts open item 23. Item 23's behaviour ("every path-B match is could not determine with note `Dispatch time window not observable`") agrees with DESIGN:496 for a row with no observable window.
- Open item 23 also says "and its transcript is None", which DESIGN:496 no longer says for the outside-window or no-window cases. This is the transcript outcome that the scope note assigns to Phase 3, so I did not grade it. Item 3.1 must close it on both sides (496 and 993, and the matching fixtures at 741 that say "S is None").
- Fixture numbers agree with the rule: `test_path_b_window_inclusive_bounds` (10:00:00.700 and 11:00:00.400 join after the seconds cut, 11:00:01.000 does not), the open-row fixture (`dispatched`, `collected_start` 12:00) and the terminal-row fixture (`completed`, no end, no window).
- Time forms in DESIGN:468 match the fixtures (SQLite form, ISO with `Z`, `yesterday`).
- 15.1 item 4 names the same three bundle fields and says it feeds "the path-B time window, GQ-108, open item 23"; item 13 feeds open item 22. This agrees with 17.
- Totals reproduced: `Total: 9 deviations.` at 819, `Total: 23 open items.` at 995, em-dash count 0, no `TODO` or `TBD` (Bash re-run this session).
- Section 18 has `### Fix cycle 3` at 1017 with an R3-B1 row naming all four fields, and the "re-anchor to master `5dc29d23`" matches the recent commit list in the session context.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Every model field read by the 7.2 path-B rule (`first_record_ts`, `dispatch_started`, `dispatch_ended`, `dispatch_status`) is in the 7.2 table with the same name and type | PASS |
| C2 | Join fields (`session_join`, `file_name`, `terminal_handle`, `session_id`) match the 7.2 table | PASS |
| C3 | `collected_start` is defined in the table with a type compatible with the rule | PASS (MINOR IC-2: type not stated) |
| C4 | 7.1 `read_transcript_tail` comment names `first_record_ts` and `last_record_ts` | PASS |
| C5 | 2.2 GQ-103(3) lists the same four names as the model | PASS (MINOR IC-2 note) |
| C6 | 15.1 item 4 names the bundle fields and maps to the model fields stated at DESIGN:455 | PASS |
| C7 | 17 open item 23 names the same fields, and its behaviour agrees with 7.2 for a no-window row | PASS (MINOR IC-6) |
| C8 | 18 Fix cycle 3 R3-B1 row names the same four fields; cycle 2 row wording fixed (m2) | PASS |
| C9 | Section 11 and section 12 fixtures use the model names | PASS (MINOR IC-4, IC-5) |
| C10 | No sentence calls the Dispatch times UNVERIFIED in a way that contradicts open item 23 (all 8 `UNVERIFIED` hits checked) | PASS |
| C11 | Section 1 status text agrees with the edited 7.2 | PASS (MINOR IC-1) |
| C12 | DESIGN edits agree with research/04 section 2.2 edits 1 to 9 | PASS |
| C13 | Time-parsing rule and fixture forms agree | PASS |
| C14 | Window rule (inclusive, seconds cut, status values) agrees with the four window fixtures | PASS |
| C15 | Mechanical file's counts reproduced (1023 lines, 9 deviations, 23 open items, 0 em-dashes, no TODO or TBD) | PASS |
| C16 | None-handling of every nullable field the rule reads is stated | PASS (MINOR IC-3: `first_record_ts` None undefined) |

## Summary

- Checks passed: 16 of 16 (6 with MINOR notes).
- BLOCKING: 0. MAJOR: 0. MINOR: 6 (IC-1 to IC-6).
- Confidence: Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 9 | Grep: 6 | Glob: 1 | Bash: 6

Verdict: PASS
Blocking count: 0
