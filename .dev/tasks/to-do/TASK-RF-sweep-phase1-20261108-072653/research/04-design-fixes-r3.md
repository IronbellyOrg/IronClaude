# Research: Design fixes R3-B1 to R3-B3

**Topic type:** Solution Research + Data Flow Tracer (design defects R3-B1, R3-B2, R3-B3)
**Scope:** `docs/designs/orchestrator-mode-review-3.md` (Blocking findings); `docs/designs/orchestrator-mode.md` sections 7.2, 11, 12 (FR-010, SP-29), 13 D9, 17 items 22-23, 18; `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` FR-010; `orca orchestration worker-show/worker-list --help`; `.dev/issues/339/analysis/inv-005-orca-index-lock.md`; Orca bundle under `/opt/Orca/resources/app.asar.unpacked/out/` (static grep only); ccsession tab map source.
**Status:** Complete
**Date:** 2026-11-08

---

## 0. Line-number drift (read first)

Review 3 cites DESIGN lines from before the section 1 "Review status" block (DESIGN lines 7-11) was added. Current lines in `docs/designs/orchestrator-mode.md` (read 2026-11-08):

| Review 3 says | Current line | Content |
|---|---|---|
| 54 (GQ-103(3)) | 60 | "The model carries every field a rule reads" |
| 392 (`read_transcript_tail` comment) | 398 | `def read_transcript_tail(path: Path) -> TranscriptTail  # last 256 KiB, first partial line dropped` |
| 449 (`OrcaObservation`) | 455 | `OrcaObservation` row of the 7.2 table |
| 451 (`TranscriptTail`) | 457 | `TranscriptTail` row: `path`, `session_id`, `readable`, `last_record_ts`, `mtime`, `project_key` |
| 488 (path-B window) | 494 | Worker definition bullet with the window rule |
| 489 / 490 / 491 | 495 / 496 / 497 | tab-map-entry-alone bullet / path-A-only True bullet / four guard cases |
| 499 (duplicate Dispatch) | 505 | Duplicate Dispatch observation rule |
| 733 (`test_classify.py`) | 739 | `test_classify.py` row of section 11 |
| 758 (FR-010 row) | 764 | FR-010 traceability row |
| 809 (D9) | 815 | D9 row |
| 847 (SP-29) | 853 | SP-29 row of section 14 (there is no SP-29 row in section 12; the "SP-29 row" the review means is section 14) |
| 879 (capture item 4) | 885 | Step 1.0a item 4 |
| 984 / 985 (open items 22, 23) | 990 / 991 | Open items 22 and 23 |
| 1005 (cycle 2 R2-B1 row) | 1011 | Fix cycle 2, R2-B1 row |

The task file must cite the current lines, or better, anchor each edit by its quoted text.

## 1. Evidence gathered (static, no live Orca call)

### 1.1 Orca help text (only `--help` was run)

- `orca orchestration worker-show --help` (exit 0): usage `--dispatch <dispatch_id> [--json]`; no time field is named. It names `observation.agentWait` only.
- `orca orchestration worker-list --help` (exit 0): "Returns at most 100 local rows, newest first, by default"; "`--cursor <cursor>` Opaque page cursor copied from `page.nextCursor`". So the continuation field of a full page is `page.nextCursor` (help text only; the JSON shape is UNVERIFIED until step 1.0a item 3).

### 1.2 Orca bundle: what `worker-show --json` returns (installed version `1.4.245-aidev02.780594c521aa`)

File: `/opt/Orca/resources/app.asar.unpacked/out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js` (2,654,414 bytes).

- CLI side: `out/cli/handlers/orchestration/worker-observation-handlers.js` calls `client.call('orchestration.workerShow', {dispatch})` and prints `value.dispatch?.id`, `value.worker.state`, `value.projection.liveness.verdict`, `value.observation.agentWait`. `--json` prints the raw result.
- Runtime handler `orchestration.workerShow` at byte offset 1447759: returns `{dispatch: hG(i), worker: gG(a), projection: vG(...), terminal, observation: mG(s), terminalResource}`. For a context-only Dispatch (no worker row) it returns `E6e(...)` with `worker: T6e(n)`.
- `hG` (the `dispatch` object) at offset 1421905. Fields: `id`, `runId`, `taskId`, `task_id`, `contractVersion`, `assigneeHandle` (@1422020), `assigneePaneKey` (@1422053), `processIncarnation`, `capabilityRevokedAt`, `retryOfDispatchId` (@1422174), `creatorDispatchId`, `hostScope`, `status`, `failureCount`, `lastFailure`, `terminationReason`, `depth`, **`dispatchedAt: e.dispatched_at` (@1422409)**, **`completedAt: e.completed_at` (@1422438)**, `createdAt: e.created_at` (@1422465), `lastHeartbeatAt`.
- `gG` (the `worker` object) at offset 1422710: `dispatchId`, `runtimeEpoch`, `state`, `stage`, `worktreeId`, `agentTerminalHandle`, `setupState`, `effects`, `residualResources`, `startOptions`, `lastError`, `createdAt`, `updatedAt`.
- `T6e` (context-only worker) at offset ~1421600: `createdAt: e.created_at`, `updatedAt: e.completed_at ?? e.created_at`.
- There is no field named `startedAt` or `endedAt` in the `worker-show` result. The start time is `dispatch.dispatchedAt` (fallback `dispatch.createdAt`); the end time is `dispatch.completedAt`.
- Schema `dispatch_contexts` at offset 1776005: `dispatched_at TEXT` (@1777908), `completed_at TEXT`, `created_at TEXT NOT NULL DEFAULT (datetime('now'))`, `status` in `pending`, `dispatched`, `completed`, `failed`, `circuit_broken`. The schema comment on `assignee_orca_session_id` says "Bare Orca session id the agent is addressed by ... for a /clear'd chat, its lineage root's"; `hG` does NOT project that column, so it is not in `worker-show` output.
- Both insert paths write `dispatched_at = datetime('now')`: `$nt` at offset 1629395 (status `dispatched`, `orchestration dispatch`) and `ert` at offset 1630462 (status `pending`, ends at @1630756 `'pending', ?, datetime('now'))`). So `dispatchedAt` is set when the row is created, which is before the worker pane runs its session. SQLite `datetime('now')` gives `YYYY-MM-DD HH:MM:SS` in UTC, second precision, no `T`, no `Z`.
- `$nt` refuses the insert when another row with the same `assignee_handle` (@1629916) or the same `assignee_pane_key` (@1630095) is `pending` or `dispatched`. So rows created by `orchestration dispatch` never have two active rows on one pane at once. `ert` (worker-start, `pending`, no handle yet) has no such guard in its text; the handle and pane key are set later by the update at @1840874 (`WHERE id = ? AND status = 'pending'`), which shows no pane-key guard.
- The write of `dispatch_contexts.completed_at` was NOT found statically (59 `completed_at` hits; the `completed_at = ...` writes found are on `coordinator_runs` @1619766 and `worker_terminal_resources` @1836381 / @1857706). How and when `completedAt` is set is UNVERIFIED.
- `worker-list` rows come from the fleet projection (`out/shared/orchestration-fleet-worker-projection.js`, 9,892 bytes, `projectOrchestrationFleetWorker`): `id`, `dispatchId`, `taskId`, `runId`, `parent`, `provider`, `host`, `workspace`, `stage`, `outcome`, `liveness`, `evidence.lastObservedAt`, `resource`, `nextAction`, `attention`. No start or end time and no pane key. So the window fields and the path-B join value are available only from `worker-show`, which is capped at 50 calls (design section 6 line 341).

### 1.3 ccsession tab map (design citation check)

- `command -v ccsession` gives `/home/coder/.local/bin/ccsession`, a symlink to `~/.claude/skills/ccsession-tag/ccsession`; the repo source is `src/superclaude/skills/ccsession-tag/ccsession` (`install_ccsession.py:13-14` names `skill / "ccsession"`).
- `ccsession:574-605` is `orca_tab_session()`: one file per pane (`orca_tab_file`, 566-572, `:` written as `+`), three lines `session id`, `pwd -P`, `ORCA_TERMINAL_HANDLE` (590); "The hooks run it at each session start and prompt, so /clear and /resume inside Claude Code move it along" (576-577); the session id is removed from every other tab file (594-600); atomic rewrite (601-602).
- `ccsession:607-613` is the `orca_tab_reopen()` comment: "The same terminal means a person ran the command again in the tab".
- The design 7.2 citation `ccsession:574-602`, `:607-613` (DESIGN line 494) is accurate. Section 1 (DESIGN line 32) cites `ccsession:564-602`, which also covers it.
- Consequence for R3-B2: each tab-map file holds exactly one session per pane key, so one tab-map entry can match several Dispatch rows only when those rows share a pane key or terminal handle.

### 1.4 `inv-005-orca-index-lock.md`

- Line 28 (E4): `worker-show` calls `orchestration.workerShow` (`worker-observation-handlers.js:10-12`), matching 1.2.
- Line 81: `worker-show` reads the runtime database plus terminal liveness and "may write the database, not git". The bundle confirms a write path inside the handler (`markWorkerStartUnknown` / `markWorkerStopUnknown` near @1447759). Out of scope here; noted for researcher 3.
- inv-005 names no Dispatch time field.

### 1.5 SPEC FR-010 (`merged-requirements.md:104`)

Acceptance text, verbatim parts that matter: "Incomplete cases [V3R3:33]: an older transcript during an outage; an older unjoined transcript after a full page with uncaptured continuation; an incomplete list after `call_failed`. All three remain visible and unknown, not Historical." FR-010 body: "an origin-unknown transcript is could not determine, with an explicit reason such as Orca unavailable, worker list truncated, worker list call failed or tab map unreadable." Complete-negative-join case: "an 8 h old unmapped one is listed under Historical", which fixes "older" as 8 h against the 6 h default window.

The design 7.2 joins (DESIGN lines 490-498) state only the "join completed" half of the guard (four cases). The list-completeness half (every scoped Run's list complete, nothing unscanned or truncated) is not restated anywhere in 7.2; DESIGN line 484 says only "Rule conditions are the SPEC table text". No note literal exists for the three SPEC reasons (grep for `worker list truncated`, `worker list call failed`, `Orca unavailable` as a note: no match in 7.2).


## 2. R3-B1: the window rule reads fields the model lacks

### 2.1 Defect

The path-B window at DESIGN line 494 compares "the earliest `timestamp` in the transcript tail" with the Dispatch row's start and end times, but `OrcaObservation` (line 455) has no start or end time and `TranscriptTail` (line 457) has only `last_record_ts`, so pure `classify.py` cannot evaluate the rule and GQ-103(3) at line 60 is false.

### 2.2 Exact design edits

Anchor each edit by its quoted text; current line numbers are given for orientation.

1. **7.2, `OrcaObservation` row (line 455).** Replace the parenthesis at the end of the row with: "plus `dispatch: str`, `run: str`, `session_join: str | None` (design: the Orca-side join value, section 2.2 path A or B; None until step 1.0a names the field), `dispatch_started: datetime | None`, `dispatch_ended: datetime | None`, `dispatch_status: str | None` (design: from `worker-show` `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status`, names read statically from the Orca 1.4.245 bundle and confirmed by step 1.0a item 4, open item 23; all three are None for a row with no `worker-show` result, such as a row past the 50-call cap or a `call_failed` show)".
2. **7.2, `TranscriptTail` row (line 457).** Insert after `last_record_ts: datetime | None`: "`first_record_ts: datetime | None` (the earliest `timestamp` among the complete records in the tail; for a file over 256 KiB this is not the session start)".
3. **7.2, new sentence after the `TabMapEntry` row's table ends (before "Constants in `models.py`", line 468).** "Time parsing (design): every Orca and transcript time is parsed to an aware UTC `datetime`. Accepted forms are SQLite `YYYY-MM-DD HH:MM:SS` (no zone, read as UTC; the form `datetime('now')` writes) and ISO 8601 with `Z` or an offset (`Z` is rewritten to `+00:00` first, because Python 3.10 `datetime.fromisoformat` does not accept `Z`). An unparseable or missing value is None and raises nothing (unknown row schema rule, line 504)."
4. **7.2, worker bullet (line 494).** Replace "A path-B join therefore also needs session identity: the earliest `timestamp` in the transcript tail must fall inside the Dispatch row's own window, from the row's start time to its end time, or to `collected_start` when the row has not ended. The `worker-show` fields that carry those times are UNVERIFIED and come from the step 1.0a item 4 capture (open item 23)." with: "A path-B join therefore also needs session identity: `first_record_ts`, cut to whole seconds, must fall inside the row's window, from `dispatch_started` to `dispatch_ended`, both ends included, or to `collected_start` when `dispatch_ended` is None and `dispatch_status` is `pending` or `dispatched`. Times are compared as UTC instants. A row whose `dispatch_started` is None, or whose `dispatch_status` is anything else while `dispatch_ended` is None, has no observable window. The names behind the three fields come from the static bundle read and are confirmed by step 1.0a item 4 (open item 23). Clock skew or the seconds cut can only move a session to could not determine or False, never to True." Then replace "A path-B match outside that window, or on a row with no observable start time, does not join: the row is could not determine with note `pane moved to a later session`, and that transcript is None with the same note." with "A path-B match outside that window does not join: the row is could not determine with note `pane moved to a later session`. A match on a row with no observable window does not join: the row is could not determine with note `Dispatch time window not observable`. Several matching rows follow the R3-B2 rule below." (The second sentence folds in review 3 minor note m5; the third points to section 3.)
5. **7.1, line 398.** Change the comment to "`# last 256 KiB, first partial line dropped; sets first_record_ts and last_record_ts`".
6. **2.2 GQ-103(3), line 60.** Append to the field list: "`OrcaObservation.dispatch_started`, `dispatch_ended`, `dispatch_status` and `TranscriptTail.first_record_ts` (the path-B window)".
7. **15.1 item 4, line 885.** Replace "and the fields that carry the Dispatch start and end times" with "and whether `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` are present with the shapes the static bundle read gives (SQLite `YYYY-MM-DD HH:MM:SS` UTC); also record, for one worker, whether `dispatchedAt` is earlier than the first transcript record of its session, and whether `completedAt` is set for `failed` and `circuit_broken` rows".
8. **17 open item 23, line 991.** Item text: "That `worker-show` `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` (read statically from the 1.4.245 bundle) carry a Dispatch row's start time, end time and status live, in the parsed form of 7.2". Behaviour until closed: unchanged, except the note becomes `Dispatch time window not observable` (m5).
9. **18.** Add `### Fix cycle 3` with one row per finding, instead of rewriting the cycle 2 row. Review 3 asks to edit the cycle 2 R2-B1 row; a new table keeps the cycle history true and still names every change. R3-B1 row: "Added `OrcaObservation.dispatch_started`, `dispatch_ended`, `dispatch_status` and `TranscriptTail.first_record_ts`, the time-parsing rule and the inclusive UTC window (7.2); `read_transcript_tail` comment (7.1); GQ-103(3) list (2.2); capture item 4 and open item 23 name the bundle fields (15.1, 17); reader, parser and window fixtures (11)". Also fix the cycle 2 row's "the transcript's earliest timestamp" to "the earliest `timestamp` in the transcript tail" (m2).

### 2.3 Fixtures to add

In `tests/sweep/test_probes_allowlist.py` (reader and parser cases; section 11 line 738):

| Name | Given | When | Then |
|---|---|---|---|
| `test_read_transcript_tail_sets_first_and_last_record_ts` | A JSONL file of 3 complete records with `timestamp` 07:00:01Z, 07:00:05Z, 07:00:09Z and one `sessionId` | `read_transcript_tail(path)` | `first_record_ts` is 07:00:01 UTC and `last_record_ts` is 07:00:09 UTC, both aware |
| `test_read_transcript_tail_first_record_ts_is_minimum` | Records whose timestamps are out of file order (07:00:05Z, 07:00:01Z, 07:00:09Z) | `read_transcript_tail(path)` | `first_record_ts` is 07:00:01 (earliest value, not first line) |
| `test_read_transcript_tail_first_record_ts_over_256k` | A file over 256 KiB whose first record (07:00:00Z) lies before the tail and whose first complete tail record is 08:00:00Z | `read_transcript_tail(path)` | `first_record_ts` is 08:00:00, not 07:00:00 (the tail only) |
| `test_worker_show_dispatch_times_sqlite_form` | A synthetic `worker-show` JSON with `dispatch.dispatchedAt: "2026-11-08 07:00:00"`, `completedAt: null`, `status: "dispatched"` | The `worker-show` parser builds `OrcaObservation` | `dispatch_started` is 2026-11-08 07:00:00 UTC (aware), `dispatch_ended` None, `dispatch_status` `"dispatched"` |
| `test_worker_show_dispatch_times_iso_z_form` | `dispatchedAt: "2026-11-08T07:00:00.123Z"`, `completedAt: "2026-11-08T08:00:00Z"` | Parser | Both parsed as aware UTC |
| `test_worker_show_dispatch_times_missing_or_bad` | One fixture with no `dispatch` times, one with `dispatchedAt: "yesterday"` | Parser | Field None, nothing raised (line 504) |

In `tests/sweep/test_classify.py` (line 739), path B assumed:

| Name | Given | When | Then |
|---|---|---|---|
| `test_path_b_window_open_row_joins` | Row D1 `dispatch_started` 10:00, `dispatch_ended` None, `dispatch_status` `dispatched`, `session_join` pane P; tab-map entry P to session S; transcript S `first_record_ts` 10:05; `collected_start` 12:00 | `classify_all` | S joins D1, `person_started` False, shown as `orca:D1`, note `joined by pane: latest session of the pane` |
| `test_path_b_window_inclusive_bounds` | D1 10:00:00 to 11:00:00 `completed`; three runs with S `first_record_ts` 10:00:00.700, 11:00:00.400, 11:00:01.000 | `classify_all` | First two join (seconds cut, both ends included); third does not join: D1 could not determine with `pane moved to a later session`, S None |
| `test_path_b_terminal_row_without_end_has_no_window` | D1 started 10:00, `dispatch_ended` None, `dispatch_status` `completed`; S first 10:30 | `classify_all` | No join; D1 could not determine with `Dispatch time window not observable`; S None with the same note (m4) |
| `test_path_b_row_without_start_has_no_window` | D1 `dispatch_started` None (for example past the 50-call show cap) | `classify_all` | No join; D1 could not determine with `Dispatch time window not observable`; S None; never True |

### 2.4 Evidence

- DESIGN lines 455, 457, 494, 398, 60, 885, 991 (read 2026-11-08); review 3 lines 83-99.
- Bundle `out/main/chunks/orcad-migration-source-retention-B_-OYaBD.js`: `orchestration.workerShow` @1447759; `hG` @1421905 with `dispatchedAt` @1422409, `completedAt` @1422438, `createdAt` @1422465; `gG` @1422710; schema @1776005 and `dispatched_at TEXT` @1777908; inserts `$nt` @1629395 and `ert` @1630462 both with `datetime('now')`.
- `out/shared/orchestration-fleet-worker-projection.js` `projectOrchestrationFleetWorker`: no time field in `worker-list` rows other than `evidence.lastObservedAt`.
- `orca orchestration worker-show --help`: names no time field.

### 2.5 UNVERIFIED until step 1.0a

- That live `worker-show --json` output contains `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` with these names (static read of one installed version only; the federated path `r8e` may differ and is out of Phase 1 scope).
- The live string format (static evidence is `datetime('now')`; other tables in the same bundle write `toISOString()`, @1619766 area, so the parser accepts both).
- Where and when `completed_at` is written for a Dispatch row, and whether it is set for `failed` and `circuit_broken` rows (no write found statically).
- Whether `dispatchedAt` precedes the worker session's first transcript record on the worker-start path (insert time suggests yes; m2).
- That transcript timestamps and the Orca database use the same host clock (Phase 1 scans the local host only, DESIGN line 512).

## 3. R3-B2: several scoped Dispatch rows match one pane session

### 3.1 Defect

When two scoped Dispatch rows carry the same pane key or terminal handle, DESIGN line 494 makes one transcript both False (joined to the row whose window holds it) and None (`pane moved to a later session` from the other row), or joins it to two rows when both windows hold it, and no rule decides.

### 3.2 How likely it is (static evidence)

- `orchestration dispatch` inserts (`$nt` @1629395) refuse a new row while another row with the same `assignee_handle` (@1629916) or `assignee_pane_key` (@1630095) is `pending` or `dispatched`. So two rows on one pane are normally sequential: the earlier is terminal before the later starts.
- Sequential rows still both match one tab-map entry (pane reuse, a retry: `retryOfDispatchId` @1422174), which is the False-and-None contradiction.
- Overlapping windows remain possible: a terminal row with no end time (fixed by the 2.2 edit 4 rule: no window), the worker-start insert `ert` @1630462 and its later handle update @1840874, which show no pane-key guard, and two rows meeting in the same second (seconds precision).

### 3.3 Exact design edit

1. **7.2, worker bullet (line 494), after "...because a person rerun inside the window cannot be told apart."** Add: "Several scoped Dispatch rows can match one tab-map entry by path B (a reused pane, a retry, or two rows on one terminal handle). The result does not depend on row order, and no row wins by position (as for duplicate Dispatch rows, line 505). If exactly one matching row's window holds the transcript, the transcript joins that row only and is False with note `joined by pane: latest session of the pane`; each other matching row is could not determine with note `pane moved to a later session` (or `Dispatch time window not observable` when it has no observable window), and those notes are not added to the transcript. If two or more matching rows' windows hold it, it joins none of them: each of those rows is could not determine with note `conflict: one pane session matches several Dispatch rows`, the other matching rows get the notes above, and the transcript is None with the `conflict:` note. If no matching row's window holds it, every matching row is could not determine with its note, and the transcript is None with `pane moved to a later session`, or with `Dispatch time window not observable` when no matching row has an observable window. A transcript with a tab-map entry that fails the window takes these notes instead of `Orca pane session, not in scoped Runs` (line 495)." The last sentence settles review 3 minor note m11 in the same place.
2. **11, `test_classify.py` row (line 739).** After "a row with no observable start time never joins by path B;" add the fixture names of 3.4.
3. **12, FR-010 row (line 764).** After "with a path-B join also needing the Dispatch row's time window" add ", and one rule for several rows matching one pane session (join only the one row whose window holds it; `conflict:` when two or more do)".
4. **13 D9 (line 815) and 14 SP-29 (line 853).** After "a path-B join also needs the Dispatch row's time window" / "a path-B join needs the Dispatch row's time window" add "and, when several rows match one pane session, exactly one window holding it".
5. **18 Fix cycle 3, R3-B2 row.** "Added the several-rows rule with the `conflict: one pane session matches several Dispatch rows` note, and the note order for a tab-map entry that fails the window (m11) (7.2); fixtures (11); FR-010, D9 and SP-29 rows (12, 13, 14)".

### 3.4 Fixtures to add (`tests/sweep/test_classify.py`, path B)

| Name | Given | When | Then |
|---|---|---|---|
| `test_path_b_pane_reused_joins_later_row_only` | D1 on pane P, 09:00 to 10:00, `completed`; D2 on pane P, from 10:30, `dispatched`; tab-map P to session S; S `first_record_ts` 10:40 | `classify_all` | S joins D2 only, False, shown as `orca:D2` with `joined by pane: latest session of the pane`; D1 could not determine with `pane moved to a later session`; S's notes do not contain `pane moved` |
| `test_path_b_two_windows_hold_session_is_conflict` | D1 on P from 09:00, `dispatched`, no end; D2 on P from 10:00, `pending`, no end; S first 10:05 | `classify_all` | No join; D1 and D2 each could not determine with `conflict: one pane session matches several Dispatch rows`; S None with the same note; S not True, not idle, not Historical; no `orca:` row carries S |
| `test_path_b_shared_boundary_second_is_conflict` | D1 on P 09:00:00 to 10:00:00 `completed`; D2 on P from 10:00:00 `dispatched`; S first 10:00:00.400 | `classify_all` | Both windows hold S (seconds cut, inclusive), so both rows get the `conflict:` note and S is None |
| `test_path_b_no_matching_window_holds` | D1 09:00 to 09:30 and D2 10:00 to 10:30, both `completed`, both on P; S first 11:00 | `classify_all` | Both rows could not determine with `pane moved to a later session`; S None with `pane moved to a later session` |
| `test_path_b_multi_row_result_ignores_row_order` | The first two fixtures with `orca_rows` reversed | `classify_all` | Same classes, notes and `row_id` values as the forward order |
| `test_path_b_entry_failing_window_note_order` | A tab-map entry P to S, D1 on P ended before S's first record | `classify_all` | S's note is `pane moved to a later session`, not `Orca pane session, not in scoped Runs` (m11) |
| `test_path_b_rows_share_terminal_handle` | As the first fixture, but D1 and D2 match by `terminal_handle` (tab-map line 3), not file name | `classify_all` | Same result as the first fixture |

### 3.5 Evidence

- DESIGN lines 494, 495, 505; review 3 lines 101-114.
- `ccsession:574-605` (one session per pane file; `/clear` and `/resume` move it); `:607-613` (same terminal means a person rerun).
- Bundle: `$nt` @1629395 with guards @1629916 and @1630095; `ert` @1630462; handle update @1840874; `retryOfDispatchId` @1422174; `assigneePaneKey` @1422053; `assigneeHandle` @1422020.

### 3.6 UNVERIFIED until step 1.0a

- Which `worker-show` value is `session_join` under path B: `dispatch.assigneePaneKey`, `dispatch.assigneeHandle` or `worker.agentTerminalHandle` (open item 22, capture item 13). The rule is written for either.
- Whether the worker-start path can leave two `pending` or `dispatched` rows on one pane in practice.
- Whether a retry (`retryOfDispatchId`) reuses its pane.

## 4. R3-B3: the SPEC's three incomplete-case fixtures are not pinned

### 4.1 Defect

The `test_classify.py` row (DESIGN line 739) says "the four incomplete cases", which drops SPEC FR-010's three acceptance fixtures (an older transcript during an Orca outage, an older unjoined transcript after a full page with uncaptured continuation, an incomplete list after `call_failed`); the design names them nowhere, and 7.2 gives them no rule or note text to assert.

### 4.2 Exact design edits

1. **11, `test_classify.py` row (line 739).** Replace "the four incomplete cases" with "the three SPEC incomplete cases (an older transcript during an Orca outage, an older unjoined transcript after a full page with uncaptured continuation, an incomplete list after `call_failed`; each stays visible with `person_started` None and its `origin unknown:` note, never idle or Historical)". Keep the four guard-case fixtures that the same cell lists later.
2. **7.2, new bullet before "The guard's 'join completed' condition fails" (line 497).** "List-incomplete cases (SPEC FR-010): no transcript can be proved unjoined when Orca is unavailable (`orca_available` False), when any scoped Run's worker list is truncated (`truncated` True: a full page of `WORKER_LIST_PAGE` rows whose continuation is not read), or when any scoped Run's `worker-list` result is `call_failed` (its `sources` row `orca worker-list <run>` has `unscanned` set). Every unjoined transcript is then None with note `origin unknown: Orca unavailable`, `origin unknown: worker list truncated` or `origin unknown: worker list call failed`, in that order when several hold, before any join-guard note. It prints could not determine and is never idle or Historical, even when its activity is older than the window." The note literals follow the SPEC reasons "Orca unavailable, worker list truncated, worker list call failed" (SPEC line 104). The source name `orca worker-list <run>` is a design choice: the design does not yet name per-Run source rows (section 7.4 has only `{"name": str, ...}`).
3. **12, FR-010 row (line 764).** In the design column, after "completeness guard", add "with its three list-incomplete cases (outage, full page, `call_failed`) and". In the test column, add "the three SPEC incomplete-case fixtures" to the `sweep/test_classify.py` parenthesis.
4. **18 Fix cycle 3, R3-B3 row.** "Restored the three SPEC incomplete-case fixtures in `test_classify.py` (11), added the list-incomplete rule and its three `origin unknown:` notes (7.2), and named them in the FR-010 row (12). Corrects cycle 2's 'changed three to four incomplete cases': the four join-incomplete cases stay in 7.2, D9 and the FR-010 and SP-29 rows". Also correct the cycle 2 R2-B1 row text as review 3 asks (line 123), or leave it and let cycle 3 correct it; the cycle 3 row is enough.

### 4.3 Fixtures to add (`tests/sweep/test_classify.py`)

Shared Given for all three: `now` fixed, window 6 h, transcript T readable, `last_activity` 8 h before `now`, no tab-map entry, joined to no Orca row; the join guard otherwise holds (path A, `session_join` present on every scoped row).

| Name | Given | When | Then |
|---|---|---|---|
| `test_fr010_outage_older_transcript_unknown_not_historical` | `--run R1`; `orca_available` False, `orca_rows` empty (the run continued on disk sources, DESIGN line 285) | `classify_all` | T `person_started` None, class could not determine, note `origin unknown: Orca unavailable`; T is in the visible rows, not Historical; `summary.historical` 0 |
| `test_fr010_full_page_uncaptured_continuation` | Scoped R1 with exactly `WORKER_LIST_PAGE` (100) rows, `truncated` True (synthetic page with `page.nextCursor` non-null), none joined to T | `classify_all` | T None, could not determine, note `origin unknown: worker list truncated`; not Historical; `summary.total_is_lower_bound` True |
| `test_fr010_call_failed_incomplete_list` | Scoped Runs R1 and R2 (the repeat form of `--run` is not checked here); R1 `worker-list` ok; R2 `worker-list` is `call_failed` (not call one, since a nonzero exit on call one is `unavailable`, open item 4), so `sources` holds `orca worker-list R2` with `unscanned` `orca call failed (exit 1)`; `orca_available` True | `classify_all` | T None, could not determine, note `origin unknown: worker list call failed`; not Historical |
| `test_fr010_incomplete_notes_order` | Outage and the guard case 1 (`session_join` None) together; separately, truncated and `call_failed` together | `classify_all` | Notes in order: `origin unknown:` notes first (unavailable, truncated, call failed), then `tab map join not observable` |

Control already in the plan: the FR-010 complete-negative-join fixture (an 8 h old unmapped transcript goes to Historical when the list is complete). Keep it beside these so each incomplete fixture differs from it by one input.

### 4.4 Evidence

- SPEC `merged-requirements.md:104` (FR-010 body reasons and the three acceptance fixtures; "older" is 8 h against 6 h by the complete-negative-join case).
- DESIGN lines 739 ("the four incomplete cases"), 764, 497, 285, 973 (open item 5: full page sets truncated), 972 (open item 4: call one nonzero is unavailable), 1011 (cycle 2 "changed 'three' to 'four'").
- `orca orchestration worker-list --help`: 100 rows by default; continuation in `page.nextCursor`.
- Review 3 lines 116-123.

### 4.5 UNVERIFIED until step 1.0a

- The live `worker-list --json` page shape and the `page.nextCursor` location (help text only; capture item 3, open item 5).
- The `call_failed` shape of a non-first `worker-list` call (never induced; synthetic fixture; capture item 8 covers only the unknown-Run case).
- Nothing in the three rules depends on the capture: they read `orca_available`, `truncated` and `sources`, which `collect` sets from result kinds already defined in 7.1.

## 5. QA gate per finding (for the task file)

Each finding is one task with its own gate, before any code task:

- R3-B1 gate: every field a 7.2 rule reads exists in the 7.2 model table (grep `first_record_ts`, `dispatch_started`, `dispatch_ended`, `dispatch_status` in 7.1, 7.2, 2.2, 11, 15.1, 17, 18); the window rule names the fields; GQ-103(3) lists them.
- R3-B2 gate: 7.2 gives exactly one outcome for each of: one window holds, two or more hold, none holds; each outcome has a fixture in section 11; D9, SP-29 and FR-010 rows agree.
- R3-B3 gate: grep finds "outage" and "uncaptured continuation" in section 11; the three `origin unknown:` notes appear in 7.2 and in section 11; "four incomplete cases" no longer appears in section 11.
- All three: em-dash count 0, no `TODO` or `TBD`, deviation total still 9, open-item total still 23 (no item added; item 23 reworded).

## Summary

- **R3-B1.** The static Orca 1.4.245 bundle shows that `worker-show --json` carries the Dispatch times as `dispatch.dispatchedAt` (start, written `datetime('now')` when the row is created), `dispatch.completedAt` (end) and `dispatch.status`. There is no `startedAt` or `endedAt`. `worker-list` rows carry no time field. Fix: add `dispatch_started`, `dispatch_ended`, `dispatch_status` to `OrcaObservation` and `first_record_ts` to `TranscriptTail`, add a UTC parsing rule that accepts the SQLite and ISO `Z` forms (Python 3.10 cannot parse `Z` directly), and make the window inclusive at whole seconds. A terminal row with no end time has no window (m4). 6 reader and parser fixtures, 4 classify fixtures.
- **R3-B2.** `orchestration dispatch` refuses a second active row on the same pane key or handle, so two rows on one pane are normally sequential. Overlap can still come from a missing end time, the worker-start path or a shared boundary second. Rule: join only the one row whose window holds the session. When two or more windows hold it, nothing joins and each row gets `conflict: one pane session matches several Dispatch rows`. When none holds, `pane moved to a later session`. Row order does not matter. 7 fixtures.
- **R3-B3.** 7.2 has no rule or note for the SPEC's list-incomplete half of the FR-010 guard. Fix: add one bullet with three notes taken from the SPEC reasons (`origin unknown: Orca unavailable`, `... worker list truncated`, `... worker list call failed`), restore the three SPEC fixtures in section 11 using an 8 h old transcript, and add 1 fixture for the note order. The source name `orca worker-list <run>` is a design choice and needs the gate's approval.
- **Still UNVERIFIED** until step 1.0a: the live field names and string format, where `completedAt` is written (not found statically), which value is `session_join`, and the live `page.nextCursor` shape.
- **Line drift.** Review 3 line numbers are 6 lower than the current design (for example 488 is now 494, 733 is now 739). Anchor every edit by its quoted text.
