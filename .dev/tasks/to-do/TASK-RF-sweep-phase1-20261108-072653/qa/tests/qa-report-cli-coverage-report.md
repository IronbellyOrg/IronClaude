# QA Report: Report and CLI coverage lens (T226)

**Date:** 2026-11-12
**Phase:** code gate, tests (report-only; fix_authorization: false)
**Scope:** DESIGN 11 rows for test_report.py, test_cli_registration.py, test_cli_contract.py; DESIGN 3.2 _publish error-table rows.

**Rule used in the Checks table:** a check is FAIL when it produced any finding of any severity. The verdict depends only on BLOCKING and MAJOR findings (MINOR never fails the gate).

**Run on disk now:** `uv run pytest tests/sweep -q`: 559 passed. `uv run ruff check src/superclaude/cli/sweep tests/sweep`: All checks passed. `uv run ruff format --check ...`: 15 files already formatted. No live Orca, ccsession or Claude command was run.

## Section 1: DESIGN 11 case map (read from `docs/designs/orchestrator-mode.md` lines 756-765 and 99-129)

### 1a. `tests/sweep/test_report.py` row (41 tests, read lines 1-1175)

| DESIGN 11 case | Test (line) | Assertion checked | Gap |
|---|---|---|---|
| Heading order equals 7.5 | `test_heading_order_equals_section_7_5[full,empty]` (534) | `headings_of(text) == HEADINGS` for a full and an empty result | none |
| (a) sort, 3 ages + 1 unknown, tie by ID | `test_waiting_a_sorts_...` (573) | exact `(ID, Age)` list; input shuffled with D3 before D2, so the tie-break is by ID, not input order | none |
| (b) never prints question text | `test_waiting_b_lists_frozen_...` (639) | secret absent from the section and the whole text; no `Question` header; order frozen, sub-heading, ready, count | none |
| Injection fixture (5 payloads) | `test_injection_keeps_the_column_count_...[5 ids]` (741) | expected neutralised text present, no Cc/Cf char, no `<`, no live `](`, headings unchanged, unescaped-pipe count equal per table, `checked >= 10` | none |
| 300-char cell prints 200, JSON whole | 772, 777, 784 | boundary 199/200/201/300 and the JSON `evidence == long` | none |
| Render twice equal; JSON equal apart from `report_path` | 802 | bytes equal, JSON equal after `report_path` swap, time comes from `ctx.now` | none |
| Source-loss fixture | 821 | control is `finished`; lost source gives `could not determine`/`fallback` with the `unscanned:` note, in both tables, in JSON; no `failed`, no `finished` cell, no `not frozen` | "a recommendation" is not asserted on the row itself; covered only through the banned-word test at 962 (see F-6) |
| Version line, 3 inputs | 874 | exact line for `1.4.245-aidev02...`, `1.4.246`, None; one line only | none |
| `bound_reached` line text | 881 | present at 2, absent at 0, also in Retained problems | boundary value 1 untested (F-5) |
| SP-24 footnote | 921 | inside `## Sessions`, count 1, full and empty | none |
| Empty-section string | 927 | 7 sections plus Waiting (b) twice; absent from a full report | none |
| Next-inspection map | 962, 971 | keys equal `{r.name for r in RULES}`; no banned word; every Sessions row has a map cell | none |
| Rule 6 wording | 1025 | `admitted`/`accepted` absent from text and JSON although the guard body quotes both | none |
| Remote coverage | 905 | `remote hosts` row with `unknown`; Scope line literal; no `no sessions` | none |
| WC-13 under Retained problems | 996 | exact `- orca:D9: WC-13 violation, review`, D8 absent | none |
| SP-16 literal under Could not determine | 987 | standalone line and the row note; absent without the note | none |
| D9 `origin not proved` in row and JSON | 1008 | row `Notes` cell and JSON `notes`; `person_started is True` | none |
| Lower-bound line + JSON True | 890 | `PAGE_LINE` in header for `truncated=True`, absent otherwise; JSON True | JSON assertion cannot tell the cases apart (F-1) |
| Last line `Report complete` | 549 | `endswith`, last `splitlines()` item, `Inspection only.` line | none |
| Builder decisions and reflect-run-2 cases | 1091, 1114, 1130, 1149, 1161, 1169 | ten dimensions are columns and not JSON keys; `frozen`/`unknown`; set-union counts 2,2,2,5; no checkbox/tag/fenced block/`$ `/delete advice | none |

### 1b. `tests/sweep/test_cli_registration.py` row (3 tests, read lines 1-69)

| DESIGN 11 case | Test (line) | Assertion checked | Gap |
|---|---|---|---|
| `sweep --help` exits 0 under CliRunner | `test_sweep_help_exits_zero` (32) | exit 0, `Usage:`, `run` in output, invoked on `main` (registration at `main.py:567-569`) | none |
| `sweep run --help` exits 0 | `test_sweep_run_help_exits_zero` (40) | exit 0, `--window` in output | only `--window` asserted (F-6) |
| Import records no seam call; `commands` not imported until `sweep_group` is read | `test_import_is_lazy_and_runs_no_seam` (48) | `COMMANDS not in sys.modules` after import; `patch_orca.calls == []`, `patch_git.calls == []`; after reading `sweep_group` the module loads and the group is named `sweep`; matches `__init__.py:4-9` | none |

### 1c. `tests/sweep/test_cli_contract.py` row (90 tests, read lines 1-1409)

| DESIGN 11 case | Test (line) | Assertion checked | Gap |
|---|---|---|---|
| Run id `""`, `r;x`, duplicate | 260, 271, 281, 303, 312, 322 | exit 2, exact stderr, `env.orca.calls == []`, `.dev` absent; dedup keeps one argv and first-seen order | none |
| Unknown Run then R2 | 332 | real `_orca` over recorded `subprocess.run` with captured fixtures; both Runs read; `orca task-list BAD` `unscanned == orca call failed (exit 1)`; note `origin unknown: Run not confirmed` | none |
| Binding tests 1, 2, 3 and 4 (gated) | 375, 392, 411, 458 | argv lists exact (1, 1, 2, 1); exit 2/0/0/2; report or no report; 4 is skipif on the capture file, which exists | none |
| Disk-only continuation prints `unscanned: orca unavailable` | helper 429, used at 408 and 426 | 3 JSON source rows, the same 3 rows printed in `## Source coverage`, banner, root worktree, transcript note | `orca worker-list <run>` row itself not asserted (nit) |
| FR-003 parser | 480, 502, 508 | 8 valid forms reach JSON; default 6h; 17 invalid forms exit 2 with exact message and no Orca call | none (matches `_parse_window`, `commands.py:43-52`) |
| FR-004 output and root | 550-744 | default, below, equal, outside, 5 `.dev` siblings, escaping symlink, symlinked sweeps folder, 3 bad roots, `.git` file/folder, walk-up, no git call | overlap wiring untested (F-3) |
| FR-005 fixture, reconciliation | 802, 822, 835 | 4 rows, 2 worktrees, `## Sessions (4/4)`, `sessions 4/4`; `total = visible + historical`; counts sum; `(2/3)` with one historical row | none |
| Golden v1 key set and types | 947, 971, 993 | 12 keys; exact key sets and exact types at every level compared with DESIGN 7.4 (checked field by field, lines 565-594); checker self-test | none |
| Zero counts; `waiting` ids only | 1003, 1018 | all 8 classes in `CLASSES` order; `waiting == {"a": [], "b": []}`; ids are `str` and equal the row ids | none |
| Two runs with one `now` give `stem.md`, `stem-2.md` | 1064 (and 1052, 1090) | name, bytes+inode+mtime of first report unchanged, third run `-3`, no temp left | none |
| One test per exit code | 1113, 1126, 1139 (and 1154) | exit 0: report complete, `st_nlink == 1`; exit 1: exact `[sweep collect] ...`; exit 2: exact usage line; pure-stage errors write nothing | none |
| Publication cases | 1178-1409 | see Section 2 | see F-4 |

## Section 2: DESIGN 3.2 `_publish` error table (lines 121-129) and steps 2 and 6, mapped to tests

| Row | Test (line) | Assertion checked | Verified against `commands.py` | Gap |
|---|---|---|---|---|
| `makedirs` fails | 1322 | exit 1, stderr `[sweep publish] [Errno 13] Permission denied`, `.dev` absent | `commands.py:157-160` | none |
| Temp name exists (`O_EXCL`) | 1309 | exact `temp file exists: <path>`, file bytes unchanged, no report | `:169-172` | symlink at the temp name not tested (F-4) |
| Write, `fsync` or close fails | 1236, 1252 | `os.write` raising ENOSPC: exit 1, temp removed, no report; with unlink also failing: second stderr line `left temp file <path>` | `:175-181`, `_write_all :146-150` | `fsync` and `close` failures and a short write are not exercised (F-4) |
| `os.link` fails with other than `FileExistsError` | 1178, 1205 | `cannot link report: [Errno 1] ...`, earlier report byte-identical, temp removed; with unlink failing, second line names the temp path | `:185-194` | none |
| Unlink fails on an exit-1 path | 1205, 1252 | exact two-line stderr, temp left | `_drop_own_temp :137-143` | the name-space-exhausted path with a failing unlink is not tested (F-4) |
| Unlink fails after the commit point | 1380 | exit 1, stdout empty, exact `could not remove temp file <path>`, one report ending `Report complete`, temp has the same bytes, `st_nlink == 2` | `:202-207` | none |
| Printing the success JSON fails after the commit point | 1359 | exit 1, `[sweep output] print failed`, one complete report, no temp | `:276-278, :286-288` | none |
| Step 2: path escapes after `makedirs` | 1337 | `output dir escaped <root>/.dev/sweeps/`, nothing written through the link | `:161-164` | none |
| Step 6: names `stem.md` to `stem-99.md` all taken | 1280, 1295 | `report name space exhausted: <dir>`, 99 files byte-identical, no temp; `-99` is taken when 2..98 are used | `:182-201`, `MAX_SUFFIX = 99` | none |

## Section 3: Mutation experiments (private copy under `/tmp`, deleted afterwards; repository files untouched)

Method: `src/`, `tests/conftest.py`, `tests/sweep/` and `pyproject.toml` were copied to a private `/tmp` directory and run with `PYTHONPATH` set to the copy (confirmed `superclaude.__file__` pointed into the copy). Each mutant was one `sed` edit to the copy, then the named tests. The one baseline failure in the copy (`test_real_git_lock_free_status_and_gitignore`, needs the repo `.gitignore`) was deselected.

| Mutant | Edit | Tests run | Result |
|---|---|---|---|
| M1 | `report.py` bound line `>= 1` to `>= 2` | test_report.py | 41 passed: SURVIVED |
| M2 | `commands.py` drop `~/.claude/projects` and `orca-tabs` from the `_check_output` inputs tuple | test_cli_contract.py | 90 passed: SURVIVED |
| M3 | `report.py` `_discovery_incomplete` second branch (`orca worktree ps` unscanned while Orca is available) returns False | tests/sweep | 558 passed: SURVIVED |
| M4 | `commands.py` `_write_all` single `os.write`, no short-write loop | tests/sweep | 558 passed: SURVIVED |
| M5 | `commands.py` remove `os.fsync(fd)` | tests/sweep | 558 passed: SURVIVED |
| M10 | `commands.py` temp file mode `0o666` to `0o600` | tests/sweep | 558 passed: SURVIVED |
| M19 | `report.py` remove the `Messages coverage: partial` line | tests/sweep | 558 passed: SURVIVED |
| M20 | `report.py` remove the `Untracked paths:` lines | tests/sweep | 558 passed: SURVIVED |
| M23 | `report.py` remove the `Orca binary:` line | tests/sweep | 558 passed: SURVIVED |
| M24 | `report.py` remove the `Sources:` line | tests/sweep | 558 passed: SURVIVED |
| M25 | `report.py` never print the child-worktrees banner at all | tests/sweep | 1 failed (run stopped at the first failure with `-x`; the failing test id was not printed): KILLED. The only banner assertion I found in the tests is `test_cli_contract.py:443`, inside the Orca-unavailable helper |

M3 left the first branch (`not result.orca_available`) intact, so it isolates the case where Orca answered but `orca worktree ps` failed.

## Section 4: Findings

No BLOCKING and no MAJOR finding. Every case named in the three DESIGN 11 rows and every row of the DESIGN 3.2 error table maps to a test whose assertions I read on disk and which passes. The findings below are MINOR (recorded as notes; they never fail the gate).

**F-1 (MINOR) `total_is_lower_bound` is pinned as always True; DESIGN section 6 still says it is conditional.**
Evidence: `docs/designs/orchestrator-mode.md:346` says it "is true when any list is truncated (a full 100-row page) or unscanned". `src/superclaude/cli/sweep/classify.py:973-976` sets it to `True` unconditionally with a `shortcut:` comment. The tests pin the shortcut: `tests/sweep/test_report.py:898-902` (a non-truncated result gives True), `tests/sweep/test_cli_contract.py:832` and `:1015`. No test can see a False value, so the `truncated` branch of the DESIGN 11 case ("a result with `truncated` True ... JSON `summary.total_is_lower_bound` is True") is satisfied vacuously. The value is truthful in Phase 1 (remote hosts are never scanned, DESIGN 7.5 Scope line), and DESIGN section 13 does not record it as a deviation.
Smallest fix: edit DESIGN `:346` to "always true in Phase 1, because remote hosts are never scanned; conditional when they are", and optionally add a deviation row in section 13.

**F-2 (MINOR) Five DESIGN 7.5 header lines and the discovery-incomplete banner have no assertion in `test_report.py`.**
Evidence: `report.py:179-187` builds `Orca binary:`, `Sources:`, `Messages coverage: partial`, `Untracked paths:` and the child-worktrees banner. Mutants M3, M19, M20, M23 and M24 (Section 3) all survived. `full_result` (`test_report.py:274-410`) has Orca available with `orca worktree ps` unscanned, so it already exercises the banner branch of M3, but nothing asserts the line. The banner is asserted only in the Orca-unavailable case (`test_cli_contract.py:443`). These lines are in DESIGN 7.5 but not in the DESIGN 11 `test_report.py` row, so this is a gap beyond the row.
Smallest fix: in `test_header_first_line_and_scope_line_are_exact` (or a sibling) assert `lines[2]` is `Orca binary: orca-ide` and that the next four lines are present; assert the banner is in `header_block(text)` for `full_result` and absent for `empty_result`.

**F-3 (MINOR) The FR-004 overlap rule is tested only on the helper, not through `sweep run`, and never for two of the three input folders.**
Evidence: `test_cli_contract.py:643-658` calls `commands._check_output` with hand-made input tuples. `commands.py:254-262` builds the real tuple (`.dev/tasks`, `~/.claude/projects`, `<state>/ccsession/orca-tabs`). Mutant M2 (delete the last two entries) survived all 90 tests. In practice the overlap cannot happen unless the root sits inside `~/.claude/projects` or `orca-tabs`, so this is defence in depth, which is why it is MINOR.
Smallest fix: one CLI test that points `HOME` or `XDG_STATE_HOME` so an input folder contains `<root>/.dev/sweeps` and asserts exit 2 with `overlaps the input folder`.

**F-4 (MINOR) `_publish` error-table row 3 and step 4 are exercised for `os.write` only.**
Evidence: DESIGN `:125` says "Write, `fsync` or close fails" and step 4 says "loop until all are written"; the DESIGN 11 row names only "a full disk on write", and the tests at `test_cli_contract.py:1236` and `:1252` match that. Mutants M4 (no short-write loop), M5 (no `fsync`) and M10 (mode `0o600` instead of the umask-governed `0o666`) survived. Also untested: a symlink at the temp name (DESIGN step 3 says `O_EXCL` refuses it) and a failing temp unlink on the name-space-exhausted path (`commands.py:197-201`). Each shares the same `except` clause as a tested path, so I found no wrong behaviour; this is missing regression protection.
Smallest fix: one test with `os.fsync` raising `OSError` (same shape as the `os.write` test at `:1236`), and one with `os.write` returning fewer bytes than asked.

**F-5 (MINOR) The `bound_reached` boundary value 1 is not tested.**
Evidence: `test_report.py:881-887` uses 2 and 0. The test name says "at least one" and DESIGN 7.5 says `(bound_reached >= 1)`. M1 (`>= 2`) survived. `full_result` uses `bound_reached=1` (`:409`) but nothing asserts the line there.
Smallest fix: change `bound_reached=2` to `1` at `:882`.

**F-6 (MINOR) Small assertion nits.**
(a) `test_report.py:821-853` checks "never finished, failed, not frozen" for the source-loss row but not "a recommendation"; the banned-word test at `:962` covers the Next-inspection cell, so the risk is low. (b) `test_cli_registration.py:45` asserts only `--window` in `sweep run --help`; `--run`, `--root` and `--output` are not checked. (c) `_assert_disk_only_continuation` (`test_cli_contract.py:429-448`) does not assert the `orca worker-list <run>` source row itself. (d) Result map `test-cli-registration.txt` quotes `469 passed` for the whole suite; the suite now has 559 tests (the map is a historical record, and `phase10-validation.md:62` records 559).
Smallest fix: none needed for the gate.

## Section 5: Result maps and validation file against disk

- `test-report.txt`: 41 tests listed; `test_report.py` has 41 (`uv run pytest` and the map agree). The 19 mapped cases agree with my own mapping in Section 1a. Its note on item 18 ("also True when not truncated, per the recent classify change") is accurate and is the same drift as F-1.
- `test-cli-registration.txt`: 3 tests, same three tests as Section 1b.
- `test-cli-contract.txt`: 90 tests (confirmed by the 90 passed in my mutant run of that file); its 22 mapped items agree with Section 1c and Section 2. Its claim that item 20 cases give "no file at a report name" is right for a to f, g and h; for 20e all 99 names already exist by construction and the test asserts the listing is unchanged.
- `phase10-validation.md`: ruff check, ruff format check and 559 passed all reproduced by me now.

## Checks

| Check | What it covers | Result | Findings |
|---|---|---|---|
| C1 | Every DESIGN 11 case of the `test_report.py` row maps to a test with a real assertion (Section 1a) | PASS | none |
| C2 | Every DESIGN 11 case of the `test_cli_registration.py` row maps to a test (Section 1b) | PASS | none |
| C3 | Every DESIGN 11 case of the `test_cli_contract.py` row maps to a test (Section 1c) | PASS | none |
| C4 | Every DESIGN 3.2 `_publish` error-table row plus steps 2 and 6 maps to a test with exact stderr, exit code, no report and no success JSON (Section 2) | PASS | none (all 7 rows and steps 2 and 6 have a test) |
| C5 | Run id, binding (4 tests), window parser, exit code and naming cases: assertion strength and agreement with `commands.py` | PASS | none |
| C6 | Golden JSON v1 test agrees with DESIGN 7.4 field by field and is not vacuous | PASS | none |
| C7 | `total_is_lower_bound` behaviour pinned by the tests agrees with DESIGN | FAIL | F-1 (MINOR) |
| C8 | DESIGN 7.5 header lines and the discovery-incomplete banner are asserted | FAIL | F-2 (MINOR) |
| C9 | FR-004 overlap rule is exercised through `sweep run` for all three input folders | FAIL | F-3 (MINOR) |
| C10 | `_publish` failure rows are exercised for every named failing call (`write`, `fsync`, `close`, short write, temp symlink, exhausted-path unlink) | FAIL | F-4 (MINOR) |
| C11 | `bound_reached` line is tested at the boundary value | FAIL | F-5 (MINOR) |
| C12 | Small assertion nits (recommendation word, help options, source row, map count) | FAIL | F-6 (MINOR) |
| C13 | Mutation experiments in a private `/tmp` copy (Section 3): 11 mutants, 1 killed, 10 survived; all survivors map to F-2 to F-5 | PASS | recorded as F-2 to F-5 |
| C14 | Result maps and `phase10-validation.md` agree with disk (Section 5) | PASS | none |
| C15 | Gates reproduced now: `uv run pytest tests/sweep` 559 passed; `ruff check` clean; `ruff format --check` clean | PASS | none |
| C16 | I wrote only this report; the mutation copy was deleted (`ls /tmp/t226*` found nothing); no live Orca, ccsession or Claude command ran | PASS | none |

Tool engagement: Read 30 (test files, DESIGN, source, maps, in chunks of at most 150 lines) | Grep 8 | Glob 1 | Bash 9 (pytest, ruff, private-copy mutation runs, cleanup).
Limits: I did not run the suite in a second order or with a changed clock. Mutants were a hand-picked set of 11, not an exhaustive mutation run.

Verdict: PASS

Blocking count: 0
