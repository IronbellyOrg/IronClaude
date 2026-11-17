# T13 redaction record: the four message-read samples

Made by `tests/observe/record_golden_questions.py --evidence <REPORT evidence folder>`. No Orca call was made: the input is the already recorded, sanitized probe output in `research/evidence/` next to `RESEARCH-REPORT-phase2-gate.md` (files 01, 03, 17 and 24). Output: `src/superclaude/cli/observe/fixtures/golden-question-{success,missing,stale,contradictory}.json`.

All values below are from the two throwaway probe Runs of 2026-11-11. None is from the coordinator's own Run or any Run the research did not create.

## Fields replaced

| Field | Replaced by | Why |
|---|---|---|
| envelope `id` (a UUID) | `env-001` ... `env-005` | not needed; unique per call |
| `_meta.runtimeId` (a UUID) | `redacted` | host-specific id |
| message `id` (`msg_` + 12 hex) | `msg_000000000001`, `msg_000000000002`, ... in first-seen order | synthetic stable ids |
| message `run_id`, `result.runId` | `run-a` (probe Run A), `run-b` (probe Run B) | synthetic Run names |
| message `to_handle` (`run:<id>`) | `run:run-a` or `run:run-b` | same mapping; a non-`run:` value would become `redacted` |
| message `from_handle` (a `term_` handle) | `redacted` | terminal handle |
| message `body` | `redacted` | bodies are never committed |
| message `payload` | `null` stays `null`; any other value becomes `redacted` | the probes sent none; a real value could hold anything |
| message `created_at`, `delivered_at` | shifted by one constant so the newest row of any type read from files 03 and 24 (the status row of file 03) lands one minute before 2026-11-08T12:00:00Z (the observer tests' base time), which puts the newest question one second earlier, at 11:58:59Z; `null` stays `null` | stable ages in tests |
| any message key outside the recorded 13 | `redacted` (name kept) | keys outside the recorded set survive by name only |
| error `message` text | each `run_<12 hex>` replaced with the same mapping (`run-a`, `run-b`) | the `consumer_fenced` text names both Runs |

## Kept as recorded

Key names and value types; `delivery_contract`, `type`, `priority`, `thread_id` (null), `acknowledged` (null), `count`; `subject` (the synthetic probe strings `probe A question` and `probe self q1`, which the research worker wrote itself); the error `code` values `consumer_fenced` and `no_active_terminal`.

## How each kind was built

| Sample | Built from |
|---|---|
| success | file 24 (Run A, `--types question`, 1 row) plus the question row of file 03 (Run B), both re-homed to `run-a`, newest first |
| missing | file 03 with `result.messages` removed, then the `no_active_terminal` error of file 17 |
| stale | the success read, then three `{"fail": "timeout"}` cycles; the test moves the fake monotonic clock past 45 s |
| contradictory | the success read; then the success read plus the status row of file 03 and one question row carrying the other Run; then the `consumer_fenced` error of file 01 |

## Checks

`tests/observe/test_golden_contract.py` (`test_question_golden_files_hold_no_path_handle_token_credential_url_or_escape_byte`) scans the four files with the `SENSITIVE` patterns of `test_fixtures.py`, plus `run_<12 hex>`, `term_` and non-synthetic `msg_` ids, and asserts every message has exactly the recorded key set with `body` and `from_handle` equal to `redacted`. `tests/observe/test_fixtures.py` scans every file in the fixtures folder again.

A first run of the recorder test caught that a non-null `payload` survived redaction; the recorder now redacts it (fixed before the files were committed).
