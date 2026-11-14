# QA Report: R3-B1 actionability lens (doc-qualitative, adversarial)

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` after items 2.1 to 2.6 (R3-B1, path-B window fields)
**Date:** 2026-11-09
**Phase:** doc-qualitative with the actionability lens (domain lens, research/09 Gap 5 row for a 500 to 1500 line design)
**Fix cycle:** 1 (first review of this gate)
**fix_authorization:** false. Only this file was written.
**Drift axis:** not applicable (doc-qualitative, no task file).

Lens: I act as the developer who must write `models.py`, `probes.read_transcript_tail`, the `worker-show` time parser and the path-B rule in `classify.py` from DESIGN alone, and I list every point where I would have to guess.

Scope note honoured: the R3-B2 several-rows rule and the transcript outcome for a path-B match that does not join are Phase 3 work (task item 3.1). They are not findings here.

## Overall Verdict: FAIL (2 MAJOR findings)

## What was read (all in chunks of at most 150 lines)

- DESIGN: lines 58-60, 205-218, 228-264, 351-480, 480-520, 536-555, 730-750, 880-899, 990-995, 1000-1023.
- research/04 lines 44-73 and 75-140; research/09 lines 139-175; `phase-outputs/test-results/r3-b1-mechanical.md` lines 1-126.
- SPEC history: `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/spec-panel-review.md` lines 91-94 (SP-15, for the `last_activity` source).

## Reliance audit (what I did not trust)

- Not trusted: the mechanical report. I re-ran `wc -l` (1023 lines), `grep -c '—'` (0) and `grep -nw 'TODO\|TBD'` (no hit). They agree with it.
- Not trusted: the producer's claim that research/04 edits 1 to 9 are applied. I compared each edit with the DESIGN text (see C9).
- Not trusted: that the model "carries every field a rule reads" (GQ-103(3)). I traced each operand of the window rule to a model field and to a place that sets it (see C14 and findings A1, A2).

## Findings

### A1. MAJOR. The time parser and the `worker-show` parser have no name, module or signature

- Evidence: DESIGN 7.1 (lines 353-446) lists `read_transcript_tail` (line 398) and `collect` (line 390) in `probes.py`, but no function that parses a time and no function that turns a `worker-show` result into an `OrcaObservation`. The time-parsing rule is a free-standing paragraph at line 468 in 7.2 (the data-model section), owned by no module. The module table (lines 209-211) lets `models.py` import `datetime`, but the `probes.py` row does not list `datetime`. Section 11 (line 740) and research/04 lines 106-108 test "the `worker-show` parser builds `OrcaObservation`" with six fixtures, and the DESIGN never names the unit under test.
- Why it blocks: I cannot write the six R3-B1 parser fixtures without inventing an import path. I also have to choose whether the parser is a `models.py` helper, a `probes.py` function or a private part of `collect`. That choice decides who imports `datetime` and `timezone`, and `read_transcript_tail` and the `worker-show` code must share one parser or they will drift on `Z`.
- Smallest fix: in 7.1 under `probes.py` add two lines, for example `def parse_time(value: object) -> datetime | None  # section 7.2 Time parsing; never raises` and `def parse_worker_show(data: object, dispatch: str, run: str) -> OrcaObservation  # missing key gives None, extra key ignored`. Say that `read_transcript_tail` and `collect` both call `parse_time`. Add `datetime` to the `probes.py` may-import row (line 211). Change the fixture "When" cells to name `parse_time` and `parse_worker_show`.

### A2. MAJOR. Only parsed Orca and transcript times are said to be timezone-aware; `now`, `collected_start`, `collected_end` and `mtime` are not

- Evidence: line 468 says "every Orca and transcript time is parsed to an aware UTC `datetime`". Line 231 says `now (UTC, read once)`. Line 454 declares `collected_start` and `collected_end` with no type. Line 457 declares `mtime: datetime` with no zone. No line says "aware" for any of them (grep for `aware|naive|timezone` hits only line 468). Yet the window rule (line 496) compares the aware `first_record_ts` with `collected_start`, and line 490 compares `last_activity` with `now`.
- Why it blocks: `datetime.utcnow()` and `datetime.fromtimestamp(st_mtime)` give naive values. Comparing a naive value with an aware one raises `TypeError`, which also breaks the rule at line 468 and line 506 that nothing in this path raises. A developer must guess, and a test author must guess what `collected_start 12:00` in `test_path_b_window_open_row_joins` (line 741) means.
- A second guess in the same field: when `collected_start` is read. The diagram (line 260) shows it returned with `SweepInput`. For an open row it is the upper end of the window, and it can differ from `now` by up to the 90 s budget. DESIGN does not say whether it is read at the top of `collect`, before the first `worker-show`, or at its return.
- Smallest fix: extend the line 468 paragraph: "`now`, `collected_start`, `collected_end` and `TranscriptTail.mtime` are aware UTC `datetime` values (`datetime.now(timezone.utc)`, `datetime.fromtimestamp(st_mtime, tz=timezone.utc)`); `collected_start` is read once at the top of `collect`, before the first Orca call". In the fixtures at lines 741 and research/04 lines 114-117, say the times are UTC and aware.

### Minor findings (never fail the gate)

- **M1 (whole-second cut, operand and open-end bound).** Line 496 cuts `first_record_ts` to whole seconds but does not say whether `dispatch_started` and `dispatch_ended` are cut too. With the accepted ISO form `2026-11-08T07:00:00.123Z` (fixture at line 740) `dispatch_started` keeps `.123`, and a real first record at 07:00:00.500 cut to 07:00:00 falls before it and is rejected. The direction is safe (could not determine), but I would guess. Floor (not rounding) is pinned by the fixture `test_path_b_window_inclusive_bounds` (10:00:00.700 and 11:00:00.400 join). "Both ends included" is stated for `dispatch_started` and `dispatch_ended`, not for the `collected_start` end of an open window. Fixture `..._iso_z_form` says "Both parsed as aware UTC" and does not give the expected value, so I cannot tell whether `.123` is kept. Fix: "dispatch times are compared at their parsed precision; only `first_record_ts` is cut", state the `collected_start` bound as included, and give the expected datetimes in the fixture.
- **M2 (row with no end time: fully specified, two small edges).** Status `pending` or `dispatched` with no end gives a window to `collected_start`; any other status with no end, and a None status, give no window (line 496). That answers the question. Unstated: an end earlier than the start (empty window; which note) and status string case. Fix: one clause, "an end earlier than the start is no observable window".
- **M3 (transcript with no usable first timestamp).** A transcript is readable when one complete record has both `timestamp` and `sessionId` (line 511), but `first_record_ts` is None when no timestamp parses (line 468). A readable transcript with `first_record_ts` None that path-B matches has no rule: which note (`pane moved to a later session` is wrong, `Dispatch time window not observable` is also wrong, because the window is fine). Fix: say it does not join and gets could not determine with one named note.
- **M4 (transcript over 256 KiB, mostly derivable).** Over the limit, the tail is used and `first_record_ts` is not the session start (lines 457, 740). Left to me to infer: (a) a file at or under 256 KiB is read whole and its first line is kept (only fixture 1 pins this, and line 398 says "first partial line dropped" without condition); (b) when the cut offset lands exactly on a line start, is that complete line dropped; (c) one JSON line longer than 256 KiB leaves no complete record, so the transcript is unreadable (line 511), which is a plausible real case for large tool results; (d) UTF-8 decoding at the cut. Fix: add "read the whole file when size <= `TRANSCRIPT_TAIL`; otherwise drop everything up to the first newline after the cut; decode each line separately, undecodable lines are skipped".
- **M5 (`last_record_ts` and `session_id` are not defined in DESIGN).** The `TranscriptTail` row (line 457) defines only `first_record_ts`. Whether `last_record_ts` is the largest timestamp or the last complete line's is open, and fixture 2 (records 07:00:05, 07:00:01, 07:00:09) cannot tell them apart. The SPEC fix SP-15 says "the timestamp of the last complete JSONL record", so last line is the likely answer, but DESIGN line 763 points to a "`last_activity` source rule (7.2)" that 7.2 does not contain (only the age rule at line 490). `session_id` is the join key and DESIGN never says which record supplies it when records disagree. These predate R3-B1.
- **M6 (accepted time forms).** A timezone-less `T` form (`2026-11-08T07:00:00`), a SQLite form with a fraction, and a numeric epoch are not in the accepted list, so by line 468 they are None. That is derivable, but the fixture `..._missing_or_bad` tests only `"yesterday"`. Add one naive-`T` case so the dev knows the intended answer.
- **M7 (fallback start time).** research/04 line 49 names `dispatch.createdAt` as a fallback start. DESIGN line 455 carries only `dispatchedAt`, so a null `dispatchedAt` gives no window. That is a clear reading, but it silently drops a research option; one clause would close it.
- **M8 (out of scope, recorded only).** Line 741 still says the later transcript is "None with the same note" for the pane-moved case, while line 496 says nothing about the transcript. Per the scope note, task item 3.1 closes this.

## The guess list the lens asked for

| Point | Guess needed? | Where it is settled |
|---|---|---|
| Time zone of Orca and transcript times | No | Line 468 (aware UTC, SQLite form read as UTC, `Z` rewritten) |
| Time zone of `now`, `collected_start`, `mtime` | Yes (A2) | Not settled |
| Inclusive bounds | No for start and end of a closed row; minor for the open end (M1) | Line 496 "both ends included"; fixture at line 741 |
| Whole-second truncation | Direction no (floor, pinned by fixture); operand yes (M1) | Line 496 and fixture |
| Row with no end time | No (M2 edges only) | Line 496 |
| Row with no start time | No | Line 496, open item 23, fixture `test_path_b_row_without_start_has_no_window` |
| Transcript over 256 KiB | Mostly no; edges yes (M4) | Lines 457, 511, 740 |
| Name and home of the two parsers | Yes (A1) | Not settled |

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Time zone of parsed Orca and transcript times is stated (line 468) | PASS |
| C2 | Time zone and awareness of `now`, `collected_start`, `collected_end`, `mtime`, and when `collected_start` is read | FAIL (A2) |
| C3 | Inclusive bounds of the closed window are stated (line 496) | PASS |
| C4 | Whole-second truncation: direction is pinned by fixture; operand and fractional dispatch times are minor (M1) | PASS (minor M1) |
| C5 | Row with no end time: window or no window is decided for every status (line 496) | PASS (minor M2) |
| C6 | Row with no start time: no window, outcome and note named (line 496, open item 23, fixture) | PASS |
| C7 | Transcript over 256 KiB: tail only, `first_record_ts` not the session start, fixture present | PASS (minor M4) |
| C8 | The time parser and the `worker-show` parser can be named, imported and tested from DESIGN | FAIL (A1) |
| C9 | research/04 section 2 edits 1 to 9 are all present in DESIGN (lines 455, 457, 468, 496, 398, 60, 887, 993, 1023; the cycle 2 row at line 1013 reads "earliest `timestamp` in the transcript tail") | PASS |
| C10 | The ten R3-B1 fixtures (lines 740-741) have a given, a trigger and an expected value; the iso_z expected value is loose (M1) | PASS (minor M1) |
| C11 | The pure `classify.py` can evaluate the window from model fields alone: `first_record_ts` on `TranscriptTail`, `dispatch_*` on `OrcaObservation`, `collected_start` on `SweepInput` (line 454) | PASS |
| C12 | Section references agree across 7.1 line 398, 2.2 line 60, 15.1 line 887, 17 line 993 and 18 line 1023 | PASS |
| C13 | The mechanical report's counts reproduce (1023 lines, 0 em-dashes, no TODO or TBD) | PASS |
| C14 | No contradiction inside the R3-B1 text itself (line 496 vs open item 23 vs fixtures); the transcript-outcome gap is Phase 3 scope (M8) | PASS |

## Self-Audit

**(a) Reliance list:** I relied on no inherited structural verdict. The spawn prompt carried none, so I ran standalone and re-checked structure myself.

**(b) Independent semantic checks:**
- Window operands traced to fields and setters: `first_record_ts` (line 457, set by `read_transcript_tail`, line 398), `dispatch_*` (line 455, set from `worker-show`), `collected_start` (line 454, line 260). The setters of the last two have no named function (A1) and no stated time zone (A2).
- research/04 edits compared edit by edit with the DESIGN lines (C9).
- Evidence for the status vocabulary and `datetime('now')` form read in research/04 lines 44-53 (`pending`, `dispatched`, `completed`, `failed`, `circuit_broken`; start fallback `createdAt`, M7).
- SPEC definition of `last_activity` read in spec-panel-review.md lines 91-94 to decide M5.

Claims verified independently: 21 (14 checks plus the guess-list rows and minor findings). Files read: DESIGN, research/04, research/09 Gap 4, the mechanical report, the spec-panel review. If I had found nothing, you could not trust it: the findings above each cite a line I read.

## Confidence

Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 17 | Grep: 9 | Glob: 0 | Bash: 1 (one `wc`, `grep` and `ls` call). One no-op Edit call on this report path was rejected before the file existed; no file other than this report was written.

No web research was done, so no Tavily call applies.

Verdict: FAIL
Blocking count: 2
