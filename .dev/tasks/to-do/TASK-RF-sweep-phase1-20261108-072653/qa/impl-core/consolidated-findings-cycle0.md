# Consolidated findings, cycle 0 (item 8.21)

Source: a Glob of `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/impl-core/qa-*-report.md` found 7 reports (not a hard-coded list):

| Report | Lens item | Verdict | Blocking count | Raw findings | Checks PASS | Checks FAIL |
|---|---|---|---|---|---|---|
| qa-classification-report.md | 8.15 | FAIL | 2 | 6 | 25 | C11, C15, C16, C18 |
| qa-conventions-report.md | 8.20 | FAIL | 1 | 10 | 11 | C4, C5, C7, C12, C13, C14, C15, C16, C19, C20 |
| qa-edge-case-report.md | 8.18 | FAIL | 4 | 22 | 20 | C4, C9, C10, C12, C15, C17, C18, C20, C22, C24, C29, C30, C31 |
| qa-interface-report.md | 8.14 | FAIL | 1 | 12 | 17 | C13 |
| qa-readonly-safety-report.md | 8.16 | FAIL | 1 | 6 | 13 | C8 |
| qa-report-surface-report.md | 8.19 | FAIL | 1 | 8 | 21 | C12 |
| qa-test-guard-report.md | 8.17 | PASS | 0 | 9 | 23 | none |

Dedup rule (item 8.21): two findings are one when they name the same `file:line` and the same defect; the highest severity is kept and the merged duplicates are listed under the kept id. 73 raw findings were merged into 67 kept findings. Severity words are the reporting agent's own (BLOCKING, MAJOR, MINOR); the test-guard report used only MINOR.

## F_0 and the cycle-0 PASS set

- `F_0` = {CORE-F1, CORE-F2, CORE-F3, CORE-F4, CORE-F5, CORE-F6, CORE-F7, CORE-F8, CORE-F9, CORE-F10}
- `|F_0|` = 10
- Cycle-0 PASS set: 130 check ids, listed in full in the section "Cycle-0 PASS set" at the end of this file (and in the cycle-0 row of `cycle-ledger.md`).
- Findings that touch a DESIGN rule (the fix agent changes the code, because DESIGN wins over the code): CORE-F5 (the carry versus DESIGN line 341) and CORE-F9 (the SP-15 contract time). The fix agent leaves a finding OPEN only when it needs a DESIGN change.

## BLOCKING and MAJOR findings

### CORE-F1 (BLOCKING): The package folder scan and the `.archiving` marker check do not re-resolve inside the root; only the `progress.md` ledger does

- Reported by: qa-readonly-safety-report:F1. Kept severity BLOCKING; merged duplicates: none.
- Evidence: `probes.py:571-591 (`_packages`, `_marker`)` (files under `src/superclaude/cli/sweep/`).
- Defect: The package folder scan and the `.archiving` marker check do not re-resolve inside the root; only the `progress.md` ledger does. A symlinked package folder lists an outside folder as a package, and an outside `.archiving` file sets `archiving_marker`.
- Smallest fix: In `_packages`, skip a folder or package that is not `_inside(..., worktree)` with an `unscanned: outside root` row; make `_marker` take the root.

### CORE-F2 (MAJOR): `WorktreeState.frozen` is never populated, so the FR-013 `frozen plan` condition cannot fire in a real sweep and the JSON `frozen` key is always null

- Reported by: qa-interface-report:F1. Kept severity MAJOR; merged duplicates: none.
- Evidence: `probes.py:840 and :862 (`frozen=None`); classify.py:851-868 (`_prepare_worktrees`)` (files under `src/superclaude/cli/sweep/`).
- Defect: `WorktreeState.frozen` is never populated, so the FR-013 `frozen plan` condition cannot fire in a real sweep and the JSON `frozen` key is always null. `policy_of` and `OrcaObservation.worktree_path` are already available.
- Smallest fix: In `classify_all`, set `frozen=True` on a worktree that hosts a row whose `policy_of` is `frozen` (never False); add a fixture that goes through `classify_all`.

### CORE-F3 (MAJOR): Ready Task rows (status `ready`, no Dispatch) are counted as scoped Dispatch rows by guard cases 1, 2 and 4, so a person's transcript gets three wrong notes, is not True, and a false `could not join Orca workers` line prints

- Reported by: qa-classification-report:CL-1. Kept severity MAJOR; merged duplicates: none.
- Evidence: `classify.py:758, :759, :764 (`_guard`)` (files under `src/superclaude/cli/sweep/`).
- Defect: Ready Task rows (status `ready`, no Dispatch) are counted as scoped Dispatch rows by guard cases 1, 2 and 4, so a person's transcript gets three wrong notes, is not True, and a false `could not join Orca workers` line prints.
- Smallest fix: Count only rows that are real Dispatch rows (exclude `status == "ready"` rows) in the three guard cases.

### CORE-F4 (MAJOR): A contract that `probes.py` found through a row's report folder (`--report-dir`) is not attached to that row, because `_contract_for` only matches a full contract path inside the row text

- Reported by: qa-classification-report:CL-2. Kept severity MAJOR; merged duplicates: none.
- Evidence: `classify.py:597-606 (`_contract_for`); probes.py:939-953` (files under `src/superclaude/cli/sweep/`).
- Defect: A contract that `probes.py` found through a row's report folder (`--report-dir`) is not attached to that row, because `_contract_for` only matches a full contract path inside the row text. A blocked, settled worker then comes out as could not determine instead of waiting on a person (a).
- Smallest fix: In `_contract_for`, also match `<folder>/return-contract.yaml` for a report folder named in the row text, or have `collect` record the join.

### CORE-F5 (MAJOR): An unused `worker-show` share only flows forward to later Runs, so `min(D, 50)` is missed (Run A 40 rows, Run B 10 rows: 35 of 50 used) and the report then says the cap was reached

- Reported by: qa-edge-case-report:E1. Kept severity MAJOR; merged duplicates: none.
- Evidence: `probes.py:134-150 (`Budget.take_show`)` (files under `src/superclaude/cli/sweep/`).
- Defect: An unused `worker-show` share only flows forward to later Runs, so `min(D, 50)` is missed (Run A 40 rows, Run B 10 rows: 35 of 50 used) and the report then says the cap was reached.
- Smallest fix: Split the 50 shows after every Run's `worker-list` is read, by real row counts; or drop the carry and change DESIGN line 341 and the bound-line text.

### CORE-F6 (MAJOR): `last_ts = ts` runs for every JSON object, so a trailing record without a timestamp (36 of 60 real transcripts end this way) blanks `last_record_ts`, and the activity time falls back to file mtime

- Reported by: qa-edge-case-report:E2. Kept severity MAJOR; merged duplicates: none.
- Evidence: `probes.py:709-715 and :720 (`_tail_from_bytes`)` (files under `src/superclaude/cli/sweep/`).
- Defect: `last_ts = ts` runs for every JSON object, so a trailing record without a timestamp (36 of 60 real transcripts end this way) blanks `last_record_ts`, and the activity time falls back to file mtime.
- Smallest fix: Set `last_ts` only inside the complete-record test (timestamp and sessionId both present).

### CORE-F7 (MAJOR): `collect` can raise: `candidate.exists()` and the age `os.stat` are unguarded, so a contract removed or unreadable after its read turns the whole sweep into an exit-1 failure instead of one unscanned row

- Reported by: qa-edge-case-report:E3. Kept severity MAJOR; merged duplicates: none.
- Evidence: `probes.py:1242 and :1254-1257 (`_read_contracts`)` (files under `src/superclaude/cli/sweep/`).
- Defect: `collect` can raise: `candidate.exists()` and the age `os.stat` are unguarded, so a contract removed or unreadable after its read turns the whole sweep into an exit-1 failure instead of one unscanned row.
- Smallest fix: Wrap the per-candidate body in `try/except (OSError, ValueError, OverflowError)` and record an unscanned row.

### CORE-F8 (MAJOR): `bound_reached` is inferred from `all four show fields are None`, so merged duplicate Dispatch rows and an empty show are reported as `Show cap or time budget reached` although neither was cut

- Reported by: qa-edge-case-report:E4. Kept severity MAJOR; merged duplicates: none.
- Evidence: `classify.py:871-874 (`_not_enriched`) and :966 (`bound_reached`)` (files under `src/superclaude/cli/sweep/`).
- Defect: `bound_reached` is inferred from `all four show fields are None`, so merged duplicate Dispatch rows and an empty show are reported as `Show cap or time budget reached` although neither was cut.
- Smallest fix: Count only rows whose own `orca worker-show <dispatch>` source row carries the cap or budget reason, or set an explicit flag in `probes._show`.

### CORE-F9 (MAJOR): The Waiting (a) Age ignores the blocked contract's file time (SP-15: the earlier of contract mtime and agentWait time), so blocked-contract rows always show unknown age and cannot sort oldest first

- Reported by: qa-report-surface-report:F-1. Kept severity MAJOR; merged duplicates: none.
- Evidence: `report.py:129-138 (`_wait_age_s`); models.py:78-86 (`ContractRecord`)` (files under `src/superclaude/cli/sweep/`).
- Defect: The Waiting (a) Age ignores the blocked contract's file time (SP-15: the earlier of contract mtime and agentWait time), so blocked-contract rows always show unknown age and cannot sort oldest first. No DESIGN deviation records this.
- Smallest fix: Add `mtime` to `ContractRecord` (set in `probes._contract`) and use the earlier time in `_wait_age_s`; or record a DESIGN deviation and change the FR-011 test.

### CORE-F10 (MAJOR): Three time parsers exist where DESIGN names one (`probes.parse_time`); they disagree with each other, and the six-key list of guessed agentWait keys is copied into two modules

- Reported by: qa-conventions-report:F1, qa-report-surface-report:F-7. Kept severity MAJOR; merged duplicates: qa-report-surface-report:F-7.
- Evidence: `classify.py:111-138 (`_as_utc`, `_wait_time`), report.py:108-126 (`_wait_time`), probes.py `parse_time`; `_WAIT_TIME_KEYS` at classify.py:97 and report.py:41` (files under `src/superclaude/cli/sweep/`).
- Defect: Three time parsers exist where DESIGN names one (`probes.parse_time`); they disagree with each other, and the six-key list of guessed agentWait keys is copied into two modules.
- Smallest fix: Parse the agentWait time once (in `probes.parse_worker_show`, stored on the observation) and delete the duplicates.

## MINOR findings

| Id | file:line | Defect | Reported by | Merged duplicates |
|---|---|---|---|---|
| CORE-F11 | __init__.py:4, :12 | `__getattr__` has no `-> object`; `__all__` is not in the design and raises until `commands.py` exists. | qa-interface-report:M1 | none |
| CORE-F12 | report.py:566, :599 | `sanitize` and `cell` take `object`, the design says `str`. | qa-interface-report:M2 | none |
| CORE-F13 | report.py:542 | `SECTIONS` has no type annotation. | qa-interface-report:M3 | none |
| CORE-F14 | probes.py:549, :691, :772 | `read_ledger`, `read_contract` and `read_transcript_tail` take an extra optional `root`. | qa-interface-report:M4 | none |
| CORE-F15 | probes.py:94-97, :222, :268 | `OrcaResult.data` for ok is the envelope `result` object, the design comment says parsed JSON. | qa-interface-report:M5 | none |
| CORE-F16 | probes.py:990 | A third source row per Run (`orca task-list --ready <run>`) that DESIGN 7.4 does not name. | qa-interface-report:M6 | none |
| CORE-F17 | models.py:125-134 | Nine dimension fields plus `freshness_age_s`; the tenth, policy, is printed from `ClassifiedRow.policy` (recorded OQ-11 decision). | qa-interface-report:M8 | none |
| CORE-F18 | tests/sweep/conftest.py:149-157 | `sweep_home` moves only HOME and XDG_STATE_HOME; DESIGN 11 also lists a package, contract, transcript and tab-map layout. | qa-interface-report:M10 | none |
| CORE-F19 | classify.py:657-660, :683-686, :914-916 | A second transcript that joins an already-joined Orca row vanishes without a note. | qa-classification-report:CL-3 | qa-edge-case-report:M9 |
| CORE-F20 | classify.py:337-350 | Rule 8 accepts a future `last_activity` as an active person session. | qa-classification-report:CL-4 | qa-edge-case-report:M8 |
| CORE-F21 | classify.py:37, :755; probes.py:397, :399 | Rule 5 cannot match live data (open item 6); the DESIGN 11 FR-010 fixtures need `JOIN_PATH = "A"`. | qa-classification-report:CL-5 | qa-interface-report:M11 |
| CORE-F22 | probes.py:938 | A relative `--report-dir` (the WORKER-CONTRACT form) finds no contract (the path regex needs a leading `/`). | qa-classification-report:CL-6 | none |
| CORE-F23 | probes.py:1240-1248, :1256 | The contract read itself does not re-resolve (`_contract(candidate, None)`); the allowed base includes every `worktree ps` path. | qa-readonly-safety-report:F2 | none |
| CORE-F24 | probes.py:810-821 | `read_orca_version` reads a fixed path with no resolve. | qa-readonly-safety-report:F3 | none |
| CORE-F25 | probes.py:174-176 | `ORCA_CLI_COMMAND` can name bare `orca` (follows the design; operator-set). | qa-readonly-safety-report:F4 | none |
| CORE-F26 | probes.py:278-284 | `git status` still honours repository config such as `core.fsmonitor`, and an inherited `GIT_DIR` (UNVERIFIED; design-level limit). | qa-readonly-safety-report:F5 | none |
| CORE-F27 | report notes | Notes only, no action for this gate (allowlist tests and the AST import test do not exist yet). | qa-readonly-safety-report:F6 | none |
| CORE-F28 | tests/sweep/test_readonly.py:151-157 | The control's lock-free call passes both the flag and the env variable, so it cannot show the flag alone carries the guarantee. | qa-test-guard-report:F-01 | none |
| CORE-F29 | tests/sweep/test_readonly.py:90-99 | `one git argv per worktree` is a loop the test writes itself (item 10.4 re-points it at `collect`). | qa-test-guard-report:F-02 | none |
| CORE-F30 | tests/sweep/conftest.py:20-40 | The guard itself has no durable regression test. | qa-test-guard-report:F-03 | none |
| CORE-F31 | tests/sweep/conftest.py:38-40 | The guard blocks only the three named entry points, not `os.posix_spawn` and others. | qa-test-guard-report:F-04 | none |
| CORE-F32 | tests/sweep (integration mark) | `exactly one integration test` holds only by convention; nothing counts them. | qa-test-guard-report:F-05 | none |
| CORE-F33 | tests/sweep/test_readonly.py:139-142 | Assertion 4 runs plain `git status --porcelain`, not `STATUS_ARGS`, and has no positive control. | qa-test-guard-report:F-06 | none |
| CORE-F34 | tests/sweep/test_readonly.py:116-127, :152 | The real-git test never calls `probes._git`; it runs a copy of the argv. | qa-test-guard-report:F-07 | none |
| CORE-F35 | tests/sweep/test_readonly.py:109-110, :126 | `git init -b main` needs git 2.28; an older git errors instead of skipping. | qa-test-guard-report:F-08 | none |
| CORE-F36 | tests/sweep/conftest.py:116-118, :123 | `OrcaFake` hedges with `getattr(probes, ...)` for names that now exist, so a rename would be silent. | qa-test-guard-report:F-09 | none |
| CORE-F37 | probes.py:530-532 | A ledger tail window that starts exactly at a line start drops that first full line as if partial. | qa-edge-case-report:M1 | none |
| CORE-F38 | probes.py:536 | `str.splitlines()` splits on form feed, `\x1c`, `\x85` and U+2028, so `FINAL:` after such a separator counts. | qa-edge-case-report:M2 | none |
| CORE-F39 | probes.py:527-533 | A ledger over 1 MiB reads only the tail; the head is never read (no behavioural difference). | qa-edge-case-report:M3 | none |
| CORE-F40 | probes.py:514-521 | `_stable` takes no budget, so the one re-read happens even when the time budget is spent. | qa-edge-case-report:M4 | none |
| CORE-F41 | probes.py:680-682 | A contract that grows past 1 MiB between the size check and `read_bytes` is read whole. | qa-edge-case-report:M5 | none |
| CORE-F42 | probes.py:1003 | The full-page test uses `len(workers)` after non-dict rows were dropped. | qa-edge-case-report:M6 | none |
| CORE-F43 | probes.py:1050-1063 | A `worker-list` row with no `dispatchId` gets no session row, so `total` does not count it. | qa-edge-case-report:M7 | none |
| CORE-F44 | classify.py:476-497; probes.py:890-896 | A worktree whose `git status` failed but whose folder exists still reports `removable: no` from its packages. | qa-edge-case-report:M10 | none |
| CORE-F45 | probes.py:593-602; classify.py:429-435 | A `to-do/` package with no `progress.md` is `unknown`, not `unfinished` (GQ-105). | qa-edge-case-report:M11 | none |
| CORE-F46 | classify.py:825-844 | An over-1-MiB or outside-root contract is noted as `contract not readable`; the cause is lost. | qa-edge-case-report:M12 | none |
| CORE-F47 | probes.py:800-801 | A tab-map file with fewer than three non-empty lines is skipped without an unscanned mark. | qa-edge-case-report:M13 | none |
| CORE-F48 | probes.py:466-474 | The old git header `Initial commit on <branch>` is read as no upstream. | qa-edge-case-report:M14 | none |
| CORE-F49 | probes.py:741, :921-922 | `datetime.fromtimestamp` is not guarded against an absurd mtime. | qa-edge-case-report:M15 | none |
| CORE-F50 | probes.py:75-77, :349 | Python 3.10 `fromisoformat` accepts only 3 or 6 fractional digits (not run on 3.10). | qa-edge-case-report:M16 | none |
| CORE-F51 | probes.py transcript tail | One JSONL record over 256 KiB leaves no complete record in the tail, so the transcript is unreadable (matches DESIGN 7.2). | qa-edge-case-report:M17 | none |
| CORE-F52 | tests/sweep | None of the edge cases has a test yet. | qa-edge-case-report:M18 | none |
| CORE-F53 | report.py (`_waiting_b`) | The Waiting (b) column `Policy reason` prints the rule name, not a reason. | qa-report-surface-report:F-2 | none |
| CORE-F54 | report.py:587-602 (`sanitize`) | `sanitize` neutralises Markdown link syntax but not bare URLs. | qa-report-surface-report:F-3 | none |
| CORE-F55 | report.py (`cell`) | A 200-character cut can split a backslash escape and leave a lone `\` before `...`. | qa-report-surface-report:F-4 | none |
| CORE-F56 | report.py:164-171 | The lock-line version match strips only after the first `-`. | qa-report-surface-report:F-5 | none |
| CORE-F57 | report.py (`to_json`); classify.py:500-516 | JSON `safe_to_close.reason` echoes `release` vocabulary. | qa-report-surface-report:F-6 | none |
| CORE-F58 | report.py (count lines) | `Every count over sessions` is read as every count line; two count displays have no Distinct line. | qa-report-surface-report:F-8 | none |
| CORE-F59 | classify.py:65, :75; report.py:34-35 | Byte-exact note literals and class indexes are duplicated between classify and report. | qa-conventions-report:F2 | qa-interface-report:M9 |
| CORE-F60 | probes.py:549, :691, :772 | Six public readers nothing calls, with a `root` option nothing passes. | qa-conventions-report:F3 | none |
| CORE-F61 | models.py (`SweepResult.context`, `SessionRow.freshness_age_s`) | A field nobody reads, and a field added without the DESIGN mark or a comment. | qa-conventions-report:F4 | none |
| CORE-F62 | tests/sweep/conftest.py | Dead fallbacks and task-item numbers that go stale. | qa-conventions-report:F5 | none |
| CORE-F63 | classify.py:37, :755 | `JOIN_PATH` is a one-value switch that is only half wired. | qa-conventions-report:F6 | none |
| CORE-F64 | tests/sweep/conftest.py:21 | The autouse fixture name breaks the repo's underscore convention. | qa-conventions-report:F7 | none |
| CORE-F65 | models.py:230 | `collections are tuples` is not true of `summary` (a dict). | qa-conventions-report:F8 | qa-interface-report:M7 |
| CORE-F66 | models.py, probes.py | Some builder decisions have no one-line comment; two comments point to `the final report`, which is not in the repo. | qa-conventions-report:F9 | none |
| CORE-F67 | report.py | Nine `# type: ignore` come from typing parameters as `object`. | qa-conventions-report:F10 | none |

## Coverage check: every raw report finding and its kept id

| Report | Raw ids | Kept ids |
|---|---|---|
| qa-interface-report | F1, M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11 | CORE-F2, CORE-F11, CORE-F12, CORE-F13, CORE-F14, CORE-F15, CORE-F16, CORE-F65, CORE-F17, CORE-F59, CORE-F18, CORE-F21 |
| qa-classification-report | CL-1, CL-2, CL-3, CL-4, CL-5, CL-6 | CORE-F3, CORE-F4, CORE-F19, CORE-F20, CORE-F21, CORE-F22 |
| qa-readonly-safety-report | F1, F2, F3, F4, F5, F6 | CORE-F1, CORE-F23, CORE-F24, CORE-F25, CORE-F26, CORE-F27 |
| qa-test-guard-report | F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09 | CORE-F28, CORE-F29, CORE-F30, CORE-F31, CORE-F32, CORE-F33, CORE-F34, CORE-F35, CORE-F36 |
| qa-edge-case-report | E1, E2, E3, E4, M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15, M16, M17, M18 | CORE-F5, CORE-F6, CORE-F7, CORE-F8, CORE-F37, CORE-F38, CORE-F39, CORE-F40, CORE-F41, CORE-F42, CORE-F43, CORE-F20, CORE-F19, CORE-F44, CORE-F45, CORE-F46, CORE-F47, CORE-F48, CORE-F49, CORE-F50, CORE-F51, CORE-F52 |
| qa-report-surface-report | F-1, F-2, F-3, F-4, F-5, F-6, F-7, F-8 | CORE-F9, CORE-F53, CORE-F54, CORE-F55, CORE-F56, CORE-F57, CORE-F10, CORE-F58 |
| qa-conventions-report | F1, F2, F3, F4, F5, F6, F7, F8, F9, F10 | CORE-F10, CORE-F59, CORE-F60, CORE-F61, CORE-F62, CORE-F63, CORE-F64, CORE-F65, CORE-F66, CORE-F67 |

## Cycle-0 PASS set

qa-classification-report:C1 (item 8.15), qa-classification-report:C2 (item 8.15), qa-classification-report:C3 (item 8.15), qa-classification-report:C4 (item 8.15), qa-classification-report:C5 (item 8.15), qa-classification-report:C6 (item 8.15), qa-classification-report:C7 (item 8.15), qa-classification-report:C8 (item 8.15), qa-classification-report:C9 (item 8.15), qa-classification-report:C10 (item 8.15), qa-classification-report:C12 (item 8.15), qa-classification-report:C13 (item 8.15), qa-classification-report:C14 (item 8.15), qa-classification-report:C17 (item 8.15), qa-classification-report:C19 (item 8.15), qa-classification-report:C20 (item 8.15), qa-classification-report:C21 (item 8.15), qa-classification-report:C22 (item 8.15), qa-classification-report:C23 (item 8.15), qa-classification-report:C24 (item 8.15), qa-classification-report:C25 (item 8.15), qa-classification-report:C26 (item 8.15), qa-classification-report:C27 (item 8.15), qa-classification-report:C28 (item 8.15), qa-classification-report:C29 (item 8.15), qa-conventions-report:C1 (item 8.20), qa-conventions-report:C2 (item 8.20), qa-conventions-report:C3 (item 8.20), qa-conventions-report:C6 (item 8.20), qa-conventions-report:C8 (item 8.20), qa-conventions-report:C9 (item 8.20), qa-conventions-report:C10 (item 8.20), qa-conventions-report:C11 (item 8.20), qa-conventions-report:C17 (item 8.20), qa-conventions-report:C18 (item 8.20), qa-conventions-report:C21 (item 8.20), qa-edge-case-report:C1 (item 8.18), qa-edge-case-report:C2 (item 8.18), qa-edge-case-report:C3 (item 8.18), qa-edge-case-report:C5 (item 8.18), qa-edge-case-report:C6 (item 8.18), qa-edge-case-report:C7 (item 8.18), qa-edge-case-report:C8 (item 8.18), qa-edge-case-report:C11 (item 8.18), qa-edge-case-report:C13 (item 8.18), qa-edge-case-report:C14 (item 8.18), qa-edge-case-report:C16 (item 8.18), qa-edge-case-report:C19 (item 8.18), qa-edge-case-report:C21 (item 8.18), qa-edge-case-report:C23 (item 8.18), qa-edge-case-report:C25 (item 8.18), qa-edge-case-report:C26 (item 8.18), qa-edge-case-report:C27 (item 8.18), qa-edge-case-report:C28 (item 8.18), qa-edge-case-report:C32 (item 8.18), qa-edge-case-report:C33 (item 8.18), qa-interface-report:C1 (item 8.14), qa-interface-report:C2 (item 8.14), qa-interface-report:C3 (item 8.14), qa-interface-report:C4 (item 8.14), qa-interface-report:C5 (item 8.14), qa-interface-report:C6 (item 8.14), qa-interface-report:C7 (item 8.14), qa-interface-report:C8 (item 8.14), qa-interface-report:C9 (item 8.14), qa-interface-report:C10 (item 8.14), qa-interface-report:C11 (item 8.14), qa-interface-report:C12 (item 8.14), qa-interface-report:C14 (item 8.14), qa-interface-report:C15 (item 8.14), qa-interface-report:C16 (item 8.14), qa-interface-report:C17 (item 8.14), qa-interface-report:C18 (item 8.14), qa-readonly-safety-report:C1 (item 8.16), qa-readonly-safety-report:C2 (item 8.16), qa-readonly-safety-report:C3 (item 8.16), qa-readonly-safety-report:C4 (item 8.16), qa-readonly-safety-report:C5 (item 8.16), qa-readonly-safety-report:C6 (item 8.16), qa-readonly-safety-report:C7 (item 8.16), qa-readonly-safety-report:C9 (item 8.16), qa-readonly-safety-report:C10 (item 8.16), qa-readonly-safety-report:C11 (item 8.16), qa-readonly-safety-report:C12 (item 8.16), qa-readonly-safety-report:C13 (item 8.16), qa-readonly-safety-report:C14 (item 8.16), qa-report-surface-report:C1 (item 8.19), qa-report-surface-report:C2 (item 8.19), qa-report-surface-report:C3 (item 8.19), qa-report-surface-report:C4 (item 8.19), qa-report-surface-report:C5 (item 8.19), qa-report-surface-report:C6 (item 8.19), qa-report-surface-report:C7 (item 8.19), qa-report-surface-report:C8 (item 8.19), qa-report-surface-report:C9 (item 8.19), qa-report-surface-report:C10 (item 8.19), qa-report-surface-report:C11 (item 8.19), qa-report-surface-report:C13 (item 8.19), qa-report-surface-report:C14 (item 8.19), qa-report-surface-report:C15 (item 8.19), qa-report-surface-report:C16 (item 8.19), qa-report-surface-report:C17 (item 8.19), qa-report-surface-report:C18 (item 8.19), qa-report-surface-report:C19 (item 8.19), qa-report-surface-report:C20 (item 8.19), qa-report-surface-report:C21 (item 8.19), qa-report-surface-report:C22 (item 8.19), qa-test-guard-report:C1 (item 8.17), qa-test-guard-report:C2 (item 8.17), qa-test-guard-report:C3 (item 8.17), qa-test-guard-report:C4 (item 8.17), qa-test-guard-report:C5 (item 8.17), qa-test-guard-report:C6 (item 8.17), qa-test-guard-report:C7 (item 8.17), qa-test-guard-report:C8 (item 8.17), qa-test-guard-report:C9 (item 8.17), qa-test-guard-report:C10 (item 8.17), qa-test-guard-report:C11 (item 8.17), qa-test-guard-report:C12 (item 8.17), qa-test-guard-report:C13 (item 8.17), qa-test-guard-report:C14 (item 8.17), qa-test-guard-report:C15 (item 8.17), qa-test-guard-report:C16 (item 8.17), qa-test-guard-report:C17 (item 8.17), qa-test-guard-report:C18 (item 8.17), qa-test-guard-report:C19 (item 8.17), qa-test-guard-report:C20 (item 8.17), qa-test-guard-report:C21 (item 8.17), qa-test-guard-report:C22 (item 8.17), qa-test-guard-report:C23 (item 8.17)
