# QA Report - Domain accuracy lens (R3-B1)

**Topic:** R3-B1 time rules in `docs/designs/orchestrator-mode.md`
**Date:** 2026-11-09
**Phase:** doc-qualitative (domain-accuracy lens; fix_authorization: false)
**Fix cycle:** N/A

Scope: DESIGN `docs/designs/orchestrator-mode.md` (1023 lines at review time) lines 33, 60, 398, 455-457, 468, 496-499, 511, 740-741, 887, 993, 1013, 1023; research/04 section 2 (lines 75-140); research/09 Gap 4; `r3-b1-mechanical.md`. Scope note honoured: the R3-B2 several-rows rule, the "Several matching rows follow the R3-B2 rule below." forward reference and the transcript outcome for a non-joining path-B match are not judged here.

Independent evidence gathered for this lens (not taken from any earlier report):
- Python 3.10.20 (`/home/coder/.local/share/uv/python/cpython-3.10-linux-x86_64-gnu/bin/python3.10`; `pyproject.toml:16` says `>=3.10`) run against `datetime.fromisoformat`.
- A real Claude Code transcript on this host (`~/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-339-orchestrator-mode/*.jsonl`, 20,640,845 bytes), keys and formats only.
- The installed Orca bundle `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js` (schema and write sites of `dispatch_contexts`).

## Findings

### D-1 MAJOR: the path-B window uses `first_record_ts` as proof of session start, but classify cannot tell when the tail is not the session start

- Evidence: DESIGN:457 says "for a file over 256 KiB this is not the session start". DESIGN:496 then makes `first_record_ts` the only session-identity test ("A path-B join therefore also needs session identity: `first_record_ts` ... must fall inside the row's window") and, when it fails, asserts the fact `pane moved to a later session`. `TranscriptTail` (DESIGN:457) has no size or truncation field (`path`, `session_id`, `readable`, `last_record_ts`, `first_record_ts`, `mtime`, `project_key`), so pure `classify.py` cannot apply the caveat that the model row states. The only over-256 KiB fixture, `test_read_transcript_tail_first_record_ts_over_256k` (DESIGN:740), tests the reader, not the join. No `test_classify.py` fixture (DESIGN:741) covers a truncated tail.
- Why it is wrong in practice: the sampled transcript on this host is 20.6 MB, so "over 256 KiB" is the normal case for a worker, not an edge case. Two concrete failures follow. (1) False "moved" claim: a worker session that outlives its Dispatch row's `dispatch_ended` (it keeps working after the row completes, or the same session serves a later Dispatch) has a tail whose first record is after `dispatch_ended`; the row becomes could not determine with the unproven note `pane moved to a later session`. (2) False join: a long person session that began before `dispatch_started`, is the pane's latest session, and has a tail that starts after `dispatch_started`, passes the window as if it had started inside it and is joined as a worker (`person_started` False). For a truncated tail, `first_record_ts >= true start`, so only the lower-bound test (`first_record_ts < dispatch_started` proves the session began earlier) is sound; the upper-bound test and the "started inside" conclusion are not.
- Smallest fix: add `tail_complete: bool` (False when the file is over 256 KiB, that is when the first partial line was dropped) to `TranscriptTail` (DESIGN:457) and to the GQ-103(3) list (DESIGN:60); in DESIGN:496 say that for `tail_complete` False the session start is not observable, the path-B match does not join, and the row and transcript carry a distinct note such as `session start not observable (transcript over 256 KiB)` instead of `pane moved to a later session`; add one `test_classify.py` fixture for it. If the owner wants path B to work for long workers, the alternative is a bounded head read of the first complete record, but that is a probe change and needs the owner.

### D-2 MINOR: the "whole-second comparison" is applied to one side only

- Evidence: DESIGN:496 cuts `first_record_ts` to whole seconds but does not cut `dispatch_started`, `dispatch_ended` or `collected_start`, and says "Times are compared as UTC instants". DESIGN:468 and the fixture `test_worker_show_dispatch_times_iso_z_form` (DESIGN:740, `dispatchedAt: "2026-11-08T07:00:00.123Z"`) accept fractional-second Dispatch times. With a `.123` start, a first record at 07:00:00.900 is cut to 07:00:00 and falls before the start, so the join is refused; with a `.123` end, a first record at 08:00:00.900 is cut to 08:00:00 and passes though it is later than the end. The SQLite-form fixture (DESIGN:741 `..._inclusive_bounds`) is arithmetically right (10:00:00.700 and 11:00:00.400 join, 11:00:01.000 does not), so the defect shows only for fractional Dispatch times. It stays on the safe side (never True), so it is MINOR.
- Smallest fix: write "`first_record_ts`, `dispatch_started`, `dispatch_ended` and `collected_start` are all cut to whole seconds before comparing", and drop or reword "compared as UTC instants".

### D-3 MINOR: the accepted-forms sentence is wider than Python 3.10 `fromisoformat` really accepts

- Evidence: DESIGN:468 accepts "ISO 8601 with `Z` or an offset". I ran 3.10.20: `Z` rewritten to `+00:00` parses (so the rewrite claim is correct); raw `...Z` fails (also as claimed); `.123` and `.123456` fractions parse; `.1`, `.12345` and `.1234567` fail; `+0100` and `+01` offsets fail; `2026-11-08 07:00:00` parses as naive (so it needs `tzinfo=utc`, as the text says). Transcript timestamps on this host are all `YYYY-MM-DDTHH:MM:SS.mmmZ` (958 of 958 stamped records), which parse. A non-conforming value becomes None (safe), so no wrong behaviour on known data.
- Smallest fix: "ISO 8601 with 0, 3 or 6 fractional digits and `Z` or `+HH:MM`; any other form is None".

### D-4 MINOR: the aware-UTC rule covers parsed values only; the comparands are unspecified

- Evidence: DESIGN:468 says "every Orca and transcript time is parsed to an aware UTC `datetime`". The window also compares against `collected_start` (DESIGN:454, type unstated), and DESIGN:741 compares record timestamps with `mtime` (DESIGN:457, source unstated). Python 3.10 raises `TypeError: can't compare offset-naive and offset-aware datetimes` on a mix (verified). DESIGN:105 and :231 say `now` is UTC but not aware.
- Smallest fix: add "`now`, `collected_start`, `collected_end` and `mtime` are aware UTC too (`datetime.now(timezone.utc)`, `datetime.fromtimestamp(st_mtime, timezone.utc)`)".

### D-5 MINOR: "the shapes the static bundle read gives" is claimed for `completedAt` and `status`, but only `dispatched_at` has static write evidence

- Evidence: DESIGN:887 (capture item 4) presents the SQLite form as the known shape of all three fields. In the bundle, `dispatched_at` is written with `datetime('now')` by two inserts (offsets 1629695 and 1630698; status `'dispatched'` and `'pending'`) and the column is `TEXT` (offset 1777908). My scan found no `UPDATE dispatch_contexts SET ... completed_at` in that chunk (0 matches), which matches research/04 section 2.5 ("no write found statically"). The `status` CHECK set is `pending, dispatched, completed, failed, circuit_broken`, so the `pending`/`dispatched` open-window rule (DESIGN:496) is accurate.
- Smallest fix: in DESIGN:887, say the SQLite form is static evidence for `dispatchedAt` only, and that the form and the writer of `completedAt` are what the capture must find.

### D-6 MINOR: DESIGN:33 overstates the transcript record shape, and the first-record definition does not say that timestamp-less records are skipped

- Evidence: DESIGN:33 says "A Claude Code transcript record carries top-level `"timestamp"` ... and `"sessionId"` keys". In the sampled transcript, 10 of 18 record types have no top-level `timestamp` (`last-prompt` 80, `custom-title` 79, `agent-name` 79, `mode` 79, `permission-mode` 79, `atis-latch` 79, `file-history-snapshot` 1, `api-request-blob` 156, `tools-used` 9, `cost-state` 2). The stamped records are also not in ascending file order (the 958 values are not sorted), which supports the `..._is_minimum` fixture. DESIGN:511 already handles this for readability ("a complete JSON record with both `timestamp` and `sessionId`"), but DESIGN:457 says "earliest `timestamp` among the complete records" without saying that records with no `timestamp` are ignored, and no fixture puts a timestamp-less record first in the tail.
- Smallest fix: DESIGN:33 "many record types carry them (one sample)"; DESIGN:457 add "records without a top-level `timestamp` are skipped"; add that case to `test_read_transcript_tail_sets_first_and_last_record_ts`.

## What held up (verified, no finding)

- The `Z` to `+00:00` rewrite and its stated reason are correct for Python 3.10 (raw `Z` raises `Invalid isoformat string`).
- `datetime('now')` is UTC with no zone, form `YYYY-MM-DD HH:MM:SS`; the bundle uses it for `dispatched_at` and `created_at`.
- The "never to True" sentence at DESIGN:496 holds: a window failure leaves the transcript unjoined, an unjoined transcript with a tab-map entry gets None (DESIGN:497), and the no-entry True path is path A only and is shut under path B whenever a scoped Dispatch row exists (DESIGN:498-499).
- The six reader and parser fixtures and the four window fixtures in DESIGN:740-741 match research/04 section 2.3 and research/09 Gap 4; the arithmetic is right.
- `r3-b1-mechanical.md` checks 2 and 3 (line 496 names all four fields; line 60 lists them) are true on disk.

## Checks

| Check | What it tests | Result |
|---|---|---|
| C1 | `Z` rewritten to `+00:00` before `fromisoformat`, with the right reason (3.10) | PASS |
| C2 | SQLite `datetime('now')` is UTC, no zone, `YYYY-MM-DD HH:MM:SS` | PASS |
| C3 | SQLite form read as UTC gives an aware value (naive from 3.10, so tzinfo must be set) | PASS |
| C4 | "ISO 8601 with Z or an offset" matches what 3.10 `fromisoformat` accepts | FAIL (D-3, minor) |
| C5 | Aware/naive consistency of every compared value (`collected_start`, `now`, `mtime`) | FAIL (D-4, minor) |
| C6 | Whole-second comparison applied consistently to both sides | FAIL (D-2, minor) |
| C7 | Inclusive bounds and the fixture arithmetic (10:00:00.700, 11:00:00.400, 11:00:01.000) | PASS |
| C8 | "Never to True" claim holds against DESIGN:497-499 | PASS |
| C9 | Transcript `timestamp` form (`.mmmZ`) and non-file-order timestamps match the `is_minimum` design | PASS |
| C10 | Records without a top-level `timestamp` are handled and the DESIGN:33 claim is accurate | FAIL (D-6, minor) |
| C11 | `first_record_ts` from a tail over 256 KiB is never treated as the session start | FAIL (D-1, MAJOR) |
| C12 | Dispatch status set `pending/dispatched` for the open window matches the Orca schema | PASS |
| C13 | Evidence for the `completedAt` and `status` shapes claimed in 15.1 item 4 | FAIL (D-5, minor) |
| C14 | Fixtures in section 11 equal research/04 section 2.3 and Gap 4 (6 reader/parser, 4 window) | PASS |
| C15 | Open item 23 and 15.1 item 4 agree with research/04 edits 7 and 8 | PASS |
| C16 | `r3-b1-mechanical.md` claims (checks 2, 3, 6, 7) true on disk | PASS |

## Inherited Structural Verdict - Reliance Audit

No `## Inherited Structural Verdict` block was supplied; this review ran standalone.

## Self-Audit

**(a) Reliance list:** none. I relied on `r3-b1-mechanical.md` only as a pointer; checks 2 and 3 were re-read against DESIGN:60 and DESIGN:496.

**(b) Independent semantic checks:**
- `fromisoformat` behaviour on 3.10.20 for 12 inputs, including raw `Z`, odd fraction lengths and offsets (Bash, python3.10 -I).
- Real transcript sample: record types without `timestamp`, timestamp format, and ordering (Bash, python3.10 -I, 20.6 MB file).
- Orca bundle: `dispatch_contexts` schema, `status` CHECK set, `datetime('now')` write sites, and absence of a `completed_at` UPDATE.

**Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 4 | Glob: 0 | Bash: 5
UNVERIFIABLE items: none. Live Orca output was not available (static bundle only); this is recorded under D-5, not as a failed check.

## Verdict

Verdict: FAIL
Blocking count: 1
