# Captured Orca fixtures: sources and sanitize rules

All files here were copied from the step 1.0a read-only capture (item 7.16) and then sanitized. Source of record: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md` (capture date 2026-11-11, Orca `1.4.245-aidev02.9cfecdd30b2a`, Run `run_a4723d345399`). The section numbers below are that file's `## N.` headings. Hand-made fixtures would carry `synthetic` in the file name; none is here.

## Sanitize rules applied (every file)

1. Home paths: the capture machine's home directory prefix is replaced by `/home/user`.
2. User names: the capture machine's account name, as a whole word, is replaced by `user`.
3. Session ids, pane keys, terminal handles and every other UUID (worktree, instance, runtime and request ids included): each distinct UUID is replaced by a stable fake UUID of the same shape, `00000000-0000-4000-8000-<12 digits>`, numbered in first-seen order across all files of this folder. The same real UUID gets the same fake value in every file, so the joins hold: a `captured-worker-show-<n>.json` `dispatch.assigneePaneKey` (`<tabId>:<leafId>`) matches the `file_name` of its `captured-tab-map-<n>.json` entry (`<tabId>+<leafId>`), and `dispatch.assigneeHandle` (`term_<uuid>`) matches the third item of that entry's `lines`. Checked for all 5 workers.
4. Orca Run, Dispatch, Task, message and resource ids (`run_...`, `ctx_...`, `task_...`, `msg_...`, `wtr_...`) are kept as captured: they carry no personal data and the id regexes in the design are written from their shape.
5. Free text that could carry other sessions' conversation or task wording is replaced by the string `<text removed>` (the value stays a string; a dict or list value becomes `{}` or `[]`): the keys `spec`, `prompt`, `lastAssistantMessage`, `toolInput`, `taskTitle`, `comment`, and `preview` (except in the `worker-show` files, where the 266-300 character terminal preview is a short startup banner and is kept after rules 1 to 3). In `captured-task-list.json` the `result` value is a JSON string; its inner string values longer than 80 characters are replaced the same way and its keys are kept.
6. Field names and value types are unchanged everywhere. Two arrays are cut and one count follows the cut: `worktrees[]` in `captured-worktree-ps.json` and `captured-worktree-list.json` keeps only 3 and 2 entries (this worktree first, then other worktrees under the capture machine's workspaces folder), and `result.totalCount` is set to the kept count. The captured `totalCount` was 28 and `truncated` false.

## Files

| File | readonly-probe section | Template (command as issued) | Exit | Rules beyond 1 to 3 |
|---|---|---|---|---|
| `captured-run-current.json` | 1 (capture item 1) | `orca-ide orchestration run-current` | 0 | The captured stdout is plain text, not JSON (the no-binding shape: one sentence), so it is wrapped: `{command, exit_code, stdout_format, stdout}`; `stdout` is the captured text byte for byte. |
| `captured-worker-list.json` | 3 (and 0, the first read of the same call) | `orca-ide orchestration worker-list --run run_a4723d345399 --json` | 0 | None. 5 worker rows. |
| `captured-worker-show-1.json` | 4 | `orca-ide orchestration worker-show --dispatch ctx_4e3237d227c3 --json` | 0 | Rule 5 except `terminal.preview` kept. |
| `captured-worker-show-2.json` | 4 | `orca-ide orchestration worker-show --dispatch ctx_6a0e3e3baaee --json` | 0 | Same. |
| `captured-worker-show-3.json` | 4 | `orca-ide orchestration worker-show --dispatch ctx_7c86fffa9716 --json` | 0 | Same. |
| `captured-worker-show-4.json` | 4 | `orca-ide orchestration worker-show --dispatch ctx_9a3728b21883 --json` | 0 | Same. |
| `captured-worker-show-5.json` | 4 | `orca-ide orchestration worker-show --dispatch ctx_dad78c5c1332 --json` | 0 | Same. |
| `captured-task-list-ready.json` | 5 | `orca-ide orchestration task-list --ready --run run_a4723d345399 --json` | 0 | None. Empty `tasks` list. |
| `captured-task-list.json` | 5 | `orca-ide orchestration task-list --run run_a4723d345399 --json` | 0 | Rule 5 (`spec` and long `result` text removed). 5 tasks. |
| `captured-worktree-ps.json` | 6 | `orca-ide worktree ps --json` | 0 | Rules 5 and 6 (3 of 28 worktrees kept). |
| `captured-worktree-list.json` | 7 | `orca-ide worktree list --json` | 0 | Rules 5 and 6 (2 of 28 worktrees kept). |
| `captured-worktree-current.json` | 7 | `orca-ide worktree current --json` | 0 | Rule 5. |
| `captured-worker-list-unknown-run.json` | 8 | `orca-ide orchestration worker-list --run run_000000000000 --json` | 0 | None. Empty list, not an error. |
| `captured-task-list-unknown-run.json` | 8 | `orca-ide orchestration task-list --run run_000000000000 --json` | 1 | None. Error body `run_not_found`; this read is Deviation D1 in the probe file. |
| `captured-tab-map-1.json` | 13 | file read inside `~/.local/state/ccsession/orca-tabs/` (worker `ctx_4e3237d227c3`, file `00000000-0000-4000-8000-000000000015+00000000-0000-4000-8000-000000000016`) | n/a | The captured file is plain text (3 lines: session id, launch folder, Orca terminal handle), not JSON, so it is wrapped: `{source, file_format, file_name, lines}`; `file_name` is the fake pane key with `+`, `lines` are the 3 lines. |
| `captured-tab-map-2.json` | 13 | same folder (worker `ctx_6a0e3e3baaee`, file `00000000-0000-4000-8000-000000000019+00000000-0000-4000-8000-000000000020`) | n/a | Same wrapper. |
| `captured-tab-map-3.json` | 13 | same folder (worker `ctx_7c86fffa9716`, file `00000000-0000-4000-8000-000000000023+00000000-0000-4000-8000-000000000024`) | n/a | Same wrapper. |
| `captured-tab-map-4.json` | 13 | same folder (worker `ctx_9a3728b21883`, file `00000000-0000-4000-8000-000000000027+00000000-0000-4000-8000-000000000028`) | n/a | Same wrapper. |
| `captured-tab-map-5.json` | 13 | same folder (worker `ctx_dad78c5c1332`, file `00000000-0000-4000-8000-000000000031+00000000-0000-4000-8000-000000000032`) | n/a | Same wrapper. |

## Notes

- Items 1 and 13 of the capture are plain text, not JSON. Each is stored as a small JSON wrapper that holds the captured text unchanged, so every fixture here is a `captured-*.json` file (19 files) and the folder holds only those and this file. A first version stored them as `.txt` and plain tab-map files; the item 7.20 check on this folder allows only `captured-*.json` and `SOURCES.md`, so they were converted (logged in `### Phase 7 Findings`).
- All five workers in this capture had exited (`liveness.verdict` `exited`, `dispatch.status` `completed`). No fixture shows a live worker, a `failed` or `circuit_broken` row, a bound `run-current`, a second `worker-list` page or the Orca-unavailable shape; those stay UNVERIFIED (`phase-outputs/discovery/1.0a-facts.md`).
- The sanitized UUID numbering is stable only for the file set above; regenerating from a new capture renumbers them.
