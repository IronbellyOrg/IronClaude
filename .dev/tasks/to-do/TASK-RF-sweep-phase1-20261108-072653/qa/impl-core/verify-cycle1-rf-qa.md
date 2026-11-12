# Verify cycle 1 (rf-qa, T188)

Verifier: rf-qa, `fix_authorization: false`. Inputs read: consolidated-findings-cycle0.md (lines 1-150), fix-log-cycle1.md, cycle-ledger.md, the seven cycle-0 qa-*-report.md check tables, and the sweep sources named below. Status: complete (the sections were appended as each was checked; the verdict is at the end).

## Findings (F_0 re-check)

Method: read the current `probes.py` (1-1371), `classify.py` (1-996), `models.py` (1-256) and `report.py` (1-673) in 150-line chunks; ran `uv run ruff check`, `uv run ruff format --check`, `uv run pytest tests/sweep`; ran `uv run python -I` scratch scripts (temp dirs under /tmp only, nothing written in the repository). File times: `tests/sweep/*`, `__init__.py`, `.gitignore`, DESIGN and SPEC are older than the cycle-0 consolidated file; only `models.py`, `probes.py`, `classify.py`, `report.py` changed after it (02:41-02:42); `pyproject.toml` and `uv.lock` are untouched.

| Id | Sev | Status | Evidence |
|---|---|---|---|
| CORE-F1 | BLOCKING | RESOLVED | `probes.py:604-636` (`_packages`): `_inside(folder, worktree)` for `to-do`/`done` (row `outside root`, `continue`), `_inside(folder / name, worktree)` per package; `probes.py:587-595` (`_marker(path, root)`) returns False unless `_inside`; call at `probes.py:641` passes `worktree`. Scratch: symlinked `to-do` lists no package + `outside root` row; symlinked package skipped + row; `.archiving` symlink to an outside file gives `archiving_marker False`; real inside `.archiving` gives True; `read_ledger` of an inside file still True. |
| CORE-F2 | MAJOR | RESOLVED | `classify.py:928-935` (`frozen_paths` from built rows with `policy_of(row) == "frozen"`), `classify.py:830-854` (`_prepare_worktrees` sets `frozen=True` only, never False), `classify.py:457-458` (`removable` gives `("no","frozen plan")`). Scratch through `classify_all`: hosting worktree `frozen True`, `removable ("no","frozen plan")`, a second worktree stays `None`, `to_json` `worktrees[].frozen` is `[true, null]` (`report.py:647`). |
| CORE-F3 | MAJOR | RESOLVED | `classify.py:734` (`rows = [r for r in rows if r.status != "ready"]` in `_guard`). Scratch: ready Task + one transcript gives `person_started True` and the `origin not proved` note only (no could-not-join, join-not-observable or earlier-pane note); ready Task + real in-progress Dispatch row + same transcript gives `person_started None` + `NOTE_COULD_NOT_JOIN`; the ready row is still Waiting (b). |
| CORE-F4 | MAJOR | RESOLVED | `classify.py:568-577` (`_contract_for`: folders from the shared `REPORT_DIR_RE` (`models.py:22-24`), exact `str(c.path.parent) in folders`); `probes.py:993-1006` uses the same `CONTRACT_FILE` and `REPORT_DIR_RE`. Scratch: `--report-dir <rd>` attaches `<rd>/return-contract.yaml`; `<rd>x` does not; the `=` and trailing-slash form attaches; the attached contract feeds rule 1 (row is Waiting (a)). |
| CORE-F5 | MAJOR | RESOLVED | `probes.py:129-167` (`share_shows(runs, wanted=None)`, `take_show`), `probes.py:1015-1101` (`_orca_reads` reads every list first, then `budget.share_shows(runs, {run: _show_demand(w)})`, then `_run_rows`). DESIGN `docs/designs/orchestrator-mode.md:341` (`min(D, 50)`; 2 Runs of 40 rows get 25 each) is met. Scratch: A 40 / B 10 gives 40 + 10; A 10 / B 60 gives 10 + 40; 2x40 gives 25/25; 3x40 gives 18/16/16; no `wanted` gives 25/25; through `_orca_reads` with a faked `_call` exactly 50 `worker-show` calls (56 calls in all), no row cut. |
| CORE-F6 | MAJOR | RESOLVED | `probes.py:765-770` (`last_ts = ts` inside the `ts is not None and sid` test). Scratch: records at 07:00 and 08:00 then `{"type":"last-prompt","sessionId":"S1"}` gives `last_record_ts` 08:00 and `first_record_ts` 07:00; a tail with no complete record is unreadable. |
| CORE-F7 | MAJOR | RESOLVED | `probes.py:1305-1337` (`_read_contracts` body in `try/except (OSError, ValueError, OverflowError)` -> `unscanned` row `contract not readable`), `probes.py:728-743` (`_contract` takes `mtime` once, catches `ValueError`/`OverflowError`). Scratch: `os.stat` raising for the contract, and `Path.exists` raising `PermissionError`, both return without raising and with an `unscanned` row; the normal read keeps `mtime` and a `read` row with an age. |
| CORE-F8 | MAJOR | RESOLVED | `classify.py:857-864` (`_show_cut`), `classify.py:965-966` (`bound_reached` counts rows whose own `orca worker-show <dispatch>` source row carries `SHOW_CAP_REASON` or `TIME_BUDGET_REASON`); constants `models.py:28-29`; `probes.py:181-185` builds the reasons from them. Scratch: two disagreeing duplicate rows + an empty show with a `read` source row give `bound_reached 0`; cap and budget rows give 2 and `total_is_lower_bound True`; an `orca call failed (exit 1)` row is not counted; `BOUND_LINE` prints at >= 1 and not at 0; real `Budget` reason texts contain the constants. |
| CORE-F9 | MAJOR | RESOLVED | `models.py:103` (`ContractRecord.mtime`), `probes.py:737,743` (set from the stat after the stable read), `report.py:106-119` (`_wait_age_s` = now - min(blocked-contract mtime, agentWait since); None if none known or the earlier is in the future). Matches SPEC `merged-requirements.md:238` (SP-15). Scratch: contract 3 h old gives 10800 and renders `3h 0m`; with an agentWait 7 h old gives 25200; sort is oldest first with the unknown-age row last; a future mtime gives None. |
| CORE-F10 | MAJOR | RESOLVED | `probes.py:461-472` (`_WAIT_TIME_KEYS`, `_wait_since` using `parse_time`), `probes.py:421` (`agent_wait_since` stored by `parse_worker_show`), `models.py:90`; `classify.py:228` and `report.py:113-114` read the field. `_as_utc`, `_wait_time`, `_WAIT_TIME_KEYS` and `fromisoformat` no longer appear in `classify.py` or `report.py` (checked with `inspect.getsource`). Scratch: dict with `startedAt` 09:00 and `since` 08:00 gives 08:00; a string gives its time; `agentWait: null` gives None with `agent_wait_present True`; no show gives None. |

Nothing in F_0 is OPEN. The 54 scratch assertions for F_0 all passed.

## Gate commands run now

| Command | Result |
|---|---|
| `uv run ruff check src/superclaude/cli/sweep tests/sweep` | `All checks passed!` |
| `uv run ruff format --check src/superclaude/cli/sweep tests/sweep` | `9 files already formatted` |
| `uv run pytest tests/sweep -q -p no:cacheprovider` | `4 passed in 1.33s` (all in `test_readonly.py`) |
| `git diff -- .gitignore` | exactly two added lines after `.dev/sprint-state/` (comment + `.dev/sweeps/`) |
| `git check-ignore -v .dev/sweeps/x.md` / `.dev/tasks/to-do/x.md` | rc 0 (`.gitignore:256`) / rc 1 |
| `git diff --stat -- pyproject.toml uv.lock Makefile` | empty (no dependency change) |

## New findings

None BLOCKING, none MAJOR. I looked for regressions the fixes could cause (the `_orca_reads` reordering, `share_shows` redistribution, the `_guard` filter, the `frozen` pass moving after the row build, `_read_contracts` exception scope, `agent_wait_since` for merged duplicate rows through `_merge_group`, `_marker` signature change) and found none; each was exercised by a scratch assertion above or by the 4 repository tests. Notes only (MINOR, not rechecked in later rounds):

| Id | Sev | Note |
|---|---|---|
| V1-N1 | MINOR | DESIGN is not updated for the fix-agent additions: `Budget.share_shows(runs, wanted=None)` (DESIGN 7.1 `orchestrator-mode.md:369` shows `share_shows(self, runs)`), `OrcaObservation.agent_wait_since` and `ContractRecord.mtime` (DESIGN 7.2 field rows at `:459-460` list neither). The code carries a one-line comment on each (`models.py:89`, `:102`; `probes.py:134-136`), the old call form still works, and SPEC `merged-requirements.md:238` (SP-15) needs the contract time. Sync the DESIGN tables at the next DESIGN revision. |
| V1-N2 | MINOR | `Source coverage` row order changed: every `worker-list`/`task-list` row now precedes the `worker-show` rows (`probes.py:1086-1090`); the call count and argv are unchanged (56 calls for 2 Runs with 50 shows in the scratch run). DESIGN `:244-249` lists the reads "per Run" without pinning an order across Runs. Phase 10 tests must not assume the old order. |
| V1-N3 | MINOR | `tests/sweep/__pycache__/` holds `test_tmp_guard_check` and `test_tmp_orca_fixture` `.pyc` files with no source; they are leftovers of cycle-0 scratch tests, are git-ignored (`git check-ignore` matched) and pytest collects only 4 tests. A private `/tmp/ironclaude-batch.tZVrGdXI` directory also exists that this verifier did not create. Neither affects the gate. |
| V1-N4 | MINOR | The worktree also shows ` M src/superclaude/output-styles/pragmatic.md`, unrelated to `src/superclaude/cli/sweep` or `tests/sweep`; do not stage it with this work unless intended. |

## Checks

Evidence key: **A** = F_0 scratch run above (54 assertions); **B** = read-only safety scratch run (27 assertions: allowlist, hostile argv with process-start recorder, git prefix/env, AST import and write-call walk); **C** = classification scratch run (52 assertions, plus a corrected 12-permutation order check); **D** = edge-case scratch run (35 assertions: limits at minus 1, at, plus 1, parsers, duplicates, stable-read conflict); **E** = interface introspection (models fields and frozen, signatures, constants, captured-fixture parse of 5 `worker-show` captures); **F** = report scratch run (37 assertions on a populated and an empty result); **G** = direct run of the `no_subprocess` fixture body (3 mark cases) plus `uv run pytest tests/sweep` (4 passed); **H** = current source read in this session at the cited lines; **I** = file unchanged since cycle 0 (mtime older than `consolidated-findings-cycle0.md`, 02:36) and still passing.

| Check | Result | Evidence |
|---|---|---|
| qa-classification-report:C1 | PASS | C: `RULES` names in order; H `classify.py:337-347` |
| qa-classification-report:C2 | PASS | C: settled, ruling halt without Orca row, no-halt decline note, live+ask decline note, report-blocked policy |
| qa-classification-report:C3 | PASS | C: exit proof stalls; unreadable evidence declines with `NOTE_EXITED_UNREADABLE` |
| qa-classification-report:C4 | PASS | C: `fenced_evidence present` gives fenced |
| qa-classification-report:C5 | PASS | C: agentWait (a), future-wait note, frozen plan (b), ready Task (b) |
| qa-classification-report:C6 | PASS | C: four conditions; each single failing condition declines |
| qa-classification-report:C7 | PASS | C: guard-refused first line only, partial note; grep of `classify.py` for `admitted\|accepted`: no hit |
| qa-classification-report:C8 | PASS | C: idle at 7 h with `window_start` 6 h |
| qa-classification-report:C9 | PASS | C: person active at 1 h (CL-4 future stamp stays a MINOR note) |
| qa-classification-report:C10 | PASS | C: fallback; rule 1 beats rule 4 |
| qa-classification-report:C12 | PASS | C: `session_join == session id` joins (path A block, H `classify.py:659-668`) |
| qa-classification-report:C13 | PASS | C: path B joins by `terminal_handle` and by `file_name` with the session id |
| qa-classification-report:C14 | PASS | C: no Orca row and no map gives True + `origin not proved`; map entry gives None + `Orca pane session, not in scoped Runs` |
| qa-classification-report:C17 | PASS | C: `session_join` matching no entry gives None + `could not join` note |
| qa-classification-report:C19 | PASS | C: aware UTC comparisons at the window bounds; H `classify.py:540-550` |
| qa-classification-report:C20 | PASS | C: inclusive bounds, whole-second cut (22:00:00.9 joins, 22:00:01 does not), open window, no observable window |
| qa-classification-report:C21 | PASS | C: unique containing window joins one row and notes the other; two containing rows get the several-rows note |
| qa-classification-report:C22 | PASS | C: `tail_complete` False gives no join and `NOTE_TAIL_ONLY` |
| qa-classification-report:C23 | PASS | C: differing duplicates merge into one conflict row with window fields None; identical ones collapse |
| qa-classification-report:C24 | PASS | C: all 12 row x transcript permutations give an equal `SweepResult` |
| qa-classification-report:C25 | PASS | C: unavailable, truncated, worker-list failed, run not confirmed, tab map unreadable notes |
| qa-classification-report:C26 | PASS | C: origin notes precede `could not join`, then `tab map join not observable`, then `earlier pane` |
| qa-classification-report:C27 | PASS | C: all 28 `NOTE_*`/`REASON_*` literals in `classify.py` found verbatim in DESIGN or SPEC |
| qa-classification-report:C28 | PASS | C: unreadable transcript and unreadable contract (source row `contract <dispatch>` unscanned) both give could not determine plus the `unscanned:` note |
| qa-classification-report:C29 | PASS | C: future `last_activity` never idle and adds `timestamp in the future` |
| qa-conventions-report:C1 | PASS | H `__init__.py:1-12` read; I (mtime 01:14) |
| qa-conventions-report:C2 | PASS | `tests/sweep/__init__.py` exists, 0 bytes (`wc -c`); I |
| qa-conventions-report:C3 | PASS | H `conftest.py:79-86`, `:127-134` (`monkeypatch.setattr`, import of `probes` inside the fixture, names `patch_git`/`patch_orca`); I |
| qa-conventions-report:C6 | PASS | E: all 15 `models.py` dataclasses are frozen and no other dataclass is defined |
| qa-conventions-report:C8 | PASS | B: AST import sets of `models.py`, `classify.py`, `report.py` are stdlib plus `.models` only |
| qa-conventions-report:C9 | PASS | `git diff --stat -- pyproject.toml uv.lock Makefile` empty; imports stdlib or pytest only |
| qa-conventions-report:C10 | PASS | `git diff -- .gitignore`: two lines after `.dev/sprint-state/`, nothing else |
| qa-conventions-report:C11 | PASS | B and D: ten `ALLOWED_ORCA` templates, `ALLOWED_GIT`, `FORBIDDEN_TOKENS`, byte limits equal DESIGN 7.3 |
| qa-conventions-report:C17 | PASS | H `models.py:140` and `report.py:381` carry the OQ-11 comments (moved from 123-124 and 400) |
| qa-conventions-report:C18 | PASS | H `models.py:230` carries the OQ-14 comment (moved from 213) |
| qa-conventions-report:C21 | PASS | ruff check and ruff format --check clean on the 9 files |
| qa-edge-case-report:C1 | PASS | D and A: 18/16/16 without `wanted` |
| qa-edge-case-report:C2 | PASS | D: 50th `take_show` True, 51st False, reason `show cap reached (50)` |
| qa-edge-case-report:C3 | PASS | D: 10.0, 9.999 (cut), 1.0, 0.999 (None) seconds left |
| qa-edge-case-report:C5 | PASS | D: 8 MiB at minus 1, at, plus 1 for `_orca` and `_git`; stdout + stderr summed |
| qa-edge-case-report:C6 | PASS | D: contract `over 1 MiB` only at plus 1 |
| qa-edge-case-report:C7 | PASS | D: ledger whole-file read at limit, tail-only at plus 1, tail FINAL found |
| qa-edge-case-report:C8 | PASS | D: transcript tail_complete True at 262143 and 262144, False at 262145 |
| qa-edge-case-report:C11 | PASS | D: cut last line skipped; lone cut record unreadable |
| qa-edge-case-report:C13 | PASS | D: missing file and outside-root symlink give the reasons and an unreadable tail |
| qa-edge-case-report:C14 | PASS | C: future agentWait time adds the note, future `last_activity` never idle |
| qa-edge-case-report:C16 | PASS | D: removed worktree gives `unscanned: worktree not readable`; H `probes.py:937-952` git failure branch |
| qa-edge-case-report:C19 | PASS | D: identical duplicates use one show; differing ones use none and stay two rows |
| qa-edge-case-report:C21 | PASS | D: one re-read then `conflict: inconsistent observation` (4 stat keys); C: the note lands on the row |
| qa-edge-case-report:C23 | PASS | D: missing, extra and non-dict show leave fields None without raising |
| qa-edge-case-report:C25 | PASS | D: ahead, ahead+behind, behind, synced, no upstream, gone, detached, no commits, rename pair, space in path |
| qa-edge-case-report:C26 | PASS | D: SQLite form, Z and offset, junk, non-string, naive ISO, date-only, overflow, leap second |
| qa-edge-case-report:C27 | PASS | D and B: constants and the 10 templates |
| qa-edge-case-report:C28 | PASS | `git diff -- .gitignore`; `check-ignore` rc 0 for `.dev/sweeps/x.md`, rc 1 for `.dev/tasks/to-do/x.md` |
| qa-edge-case-report:C32 | PASS | G: 4 passed, same as `step-1.4a-pytest.txt`; no edge-case tests exist yet |
| qa-edge-case-report:C33 | PASS | E: all five `captured-worker-show-*.json` parse (status, verdict, assignee, start time) and the list and `worktree ps` captures hold the keys read |
| qa-interface-report:C1 | PASS | H `__init__.py`; I |
| qa-interface-report:C2 | PASS | E: 15 frozen types; every cycle-0 field keeps its order; only additions are `OrcaObservation.agent_wait_since` and `ContractRecord.mtime` (default None, at the end; see V1-N1) |
| qa-interface-report:C3 | PASS | E: `JSON_SCHEMA_VERSION`, `CLASSES` (8), `PACKAGE_STATES` (6 in order), `SAFE_VALUES` |
| qa-interface-report:C4 | PASS | E: `ClassifiedRow` fields `row, classification, policy, safe` |
| qa-interface-report:C5 | PASS | E: all classify signatures equal the DESIGN 7.1 strings |
| qa-interface-report:C6 | PASS | E and C: nine `RULES` names in order |
| qa-interface-report:C7 | PASS | E: `Budget` defaults and methods (`share_shows(runs)` still valid), `OrcaResult`, seams, `bind_run`, check functions |
| qa-interface-report:C8 | PASS | E: signatures of `parse_time`, `parse_worker_show`, `collect`, `read_worktree`, `parse_status`, `read_packages`, `read_tab_map`, `read_orca_version` |
| qa-interface-report:C9 | PASS | B, D and H `probes.py:41-77`: constants and Run/Dispatch id regexes |
| qa-interface-report:C10 | PASS | E: `CHECKED_ORCA_VERSION`, `CELL_MAX`, 12 `SECTIONS`, `render`, `to_json` parameters |
| qa-interface-report:C11 | PASS | F: 12 top-level keys, 9 row keys, no dimension key, summary keys, counts with zeros, worktree keys |
| qa-interface-report:C12 | PASS | F: ten `##` headings in render order, ends `Report complete`, fixed lines match DESIGN text |
| qa-interface-report:C14 | PASS | `git diff -- .gitignore` and `check-ignore` rc 0 / rc 1 |
| qa-interface-report:C15 | PASS | H `conftest.py` and `test_readonly.py` read; G: 4 passed; the names they use exist |
| qa-interface-report:C16 | PASS | E: five captured `worker-show` files and the list and `worktree ps` captures parse with the field paths used |
| qa-interface-report:C17 | PASS | B: AST import sets; only `probes.py` imports `subprocess` |
| qa-interface-report:C18 | PASS | E: no missing or renamed name; new names are `models.CONTRACT_FILE`, `REPORT_DIR_RE`, `SHOW_CAP_REASON`, `TIME_BUDGET_REASON` and the two fields above (V1-N1) |
| qa-readonly-safety-report:C1 | PASS | B: 10 templates, 7 distinct verbs, every token present in DESIGN |
| qa-readonly-safety-report:C2 | PASS | B: 18 hostile argv (newline id, wrong-length id, upper case, Arabic-digit id, literal `<run>`, reordered flags, empty, bytes, `--include-remote`) rejected with 0 process starts |
| qa-readonly-safety-report:C3 | PASS | B: `_orca` raised `ValueError` before `subprocess.run` for every hostile argv; H `probes.py:245` |
| qa-readonly-safety-report:C4 | PASS | B: 6 hostile git argument sets rejected, 0 process starts; H `probes.py:295` |
| qa-readonly-safety-report:C5 | PASS | B: `FORBIDDEN_TOKENS == {"--include-remote"}`; rejected last and alone |
| qa-readonly-safety-report:C6 | PASS | B: real `_git` gives `git --no-optional-locks -C /x status ...`, env `GIT_OPTIONAL_LOCKS=0` even with caller value 1, no `shell` |
| qa-readonly-safety-report:C7 | PASS | B: AST walk of all five modules finds no write, create, remove, lock or temp-file call and no `open` mode other than `rb`; `probes.py` opens at 559, 805, 869 |
| qa-readonly-safety-report:C9 | PASS | B: `import subprocess`, two `subprocess.run(` starts, no `from subprocess import` |
| qa-readonly-safety-report:C10 | PASS | B: import sets of `classify.py` and `report.py` hold no `subprocess`, `click`, `os`, `shutil` |
| qa-readonly-safety-report:C11 | PASS | B: the only write-verb-like string constant in the four modules is the JSON key `dispatch` (no argv) |
| qa-readonly-safety-report:C12 | PASS | B: default `orca-ide`, `ORCA_CLI_COMMAND` override |
| qa-readonly-safety-report:C13 | PASS | `git diff -- .gitignore` (two lines) and `check-ignore` rc 0 / rc 1 |
| qa-readonly-safety-report:C14 | PASS | G: 4 passed; H `test_readonly.py:59-77` patches `probes.subprocess.run` and calls the real `_git` |
| qa-report-surface-report:C1 | PASS | F: heading order and the Ready Tasks sub-heading and count line |
| qa-report-surface-report:C2 | PASS | F: seven header lines in order; three bracketed lines absent when no condition holds, present in order when all hold |
| qa-report-surface-report:C3 | PASS | F: empty-section string printed in the empty report |
| qa-report-surface-report:C4 | PASS | F: 300 gives 200 ending `...`; 200 and 201 give 200 |
| qa-report-surface-report:C5 | PASS | F: ESC/CSI/OSC, control, bidi, BOM, CR, NEL, U+2028 removed or folded; pipe, backslash, tags, brackets neutralised; newline cannot start a heading |
| qa-report-surface-report:C6 | PASS | F: `1.4.245` and `1.4.245-beta` unlikely; `1.5.0` and None UNVERIFIED |
| qa-report-surface-report:C7 | PASS | F and C: bracketed literals found in DESIGN; Sessions count equals `summary.visible`; `bound_reached` is the fixed count (CORE-F8) |
| qa-report-surface-report:C8 | PASS | F: `SP24_LINE` found in DESIGN |
| qa-report-surface-report:C9 | PASS | F: output ends `Report complete\n`, once |
| qa-report-surface-report:C10 | PASS | F: ten dimension names only in the Sessions header; Policy cell `frozen` or `unknown`; no `not frozen` text; no dimension key in JSON |
| qa-report-surface-report:C11 | PASS | F: no recommendation vocabulary in the rendered report; `safe_to_close` never yes |
| qa-report-surface-report:C13 | PASS | F: Waiting (b) lists the Ready Tasks sub-heading and count and no question text |
| qa-report-surface-report:C14 | PASS | F: Sessions header and Waiting (a) header exact |
| qa-report-surface-report:C15 | PASS | F: no DONE/NEXT text in `report.py`; window shown as `6h` |
| qa-report-surface-report:C16 | PASS | B: `report.py` imports only `re`, `unicodedata`, `.models`; F: two renders equal; the new `_wait_age_s` reads only the row and `ctx` |
| qa-report-surface-report:C17 | PASS | F: 12 JSON keys, counts with zeros, two serialisations equal |
| qa-report-surface-report:C18 | PASS | F: `Distinct affected sessions: N (set union, not a sum)` equals DESIGN `:645` |
| qa-report-surface-report:C19 | PASS | `.gitignore` diff and `check-ignore` results |
| qa-report-surface-report:C20 | PASS | G: 4 passed, matching `step-1.4-pytest.txt`, `step-1.4a-pytest.txt`, `phase8-validation.md`; ruff clean |
| qa-report-surface-report:C21 | PASS | F: Retained problems, Shift Brief text, remote-hosts lower-bound text |
| qa-report-surface-report:C22 | PASS | F: `NEXT_INSPECTION` keys equal the nine rule names, every value starts with `read` |
| qa-test-guard-report:C1 | PASS | G: `subprocess.run` blocked for an unmarked function, a `skipif`-only function and (not) for an `integration` one; H `conftest.py:38` |
| qa-test-guard-report:C2 | PASS | G: `subprocess.Popen` blocked / allowed the same way; H `conftest.py:39` |
| qa-test-guard-report:C3 | PASS | G: `os.system` blocked / allowed the same way; H `conftest.py:40` |
| qa-test-guard-report:C4 | PASS | G: the fake request's `get_closest_marker` raised if called and was never called; `grep get_closest_marker( tests/sweep/*.py` counts 0 |
| qa-test-guard-report:C5 | PASS | G: only the function's own `integration` mark steps aside |
| qa-test-guard-report:C6 | PASS | `grep pytest.mark.integration tests/sweep`: one hit, `test_readonly.py:109` |
| qa-test-guard-report:C7 | PASS | G: `subprocess.run`, `Popen`, `os.system` restored after each case |
| qa-test-guard-report:C8 | PASS | `pyproject.toml:114` `--strict-markers`, `:119` `integration` registered; 4 tests collected and run |
| qa-test-guard-report:C9 | PASS | H `test_readonly.py:69-74`; G: passes |
| qa-test-guard-report:C10 | PASS | H `test_readonly.py:60-62, 75`; G: passes |
| qa-test-guard-report:C11 | PASS | H `test_readonly.py:80-87`; G: passes; B: rejected git argv start no process |
| qa-test-guard-report:C12 | PASS | H `test_readonly.py:90-99` interim test passes (CORE-F29 stays a MINOR note) |
| qa-test-guard-report:C13 | PASS | H `test_readonly.py:127` copies `REPO_ROOT / ".gitignore"` |
| qa-test-guard-report:C14 | PASS | H `test_readonly.py:133-166` holds the four assertions; G: passes |
| qa-test-guard-report:C15 | PASS | H `test_readonly.py:161-166` `warnings.warn` on an inconclusive control; `grep filterwarnings pyproject.toml`: no hit |
| qa-test-guard-report:C16 | PASS | B: only `probes.py` imports `subprocess`; H `test_readonly.py:24, 105` real-git test runs `git` only with `HOME` in `tmp_path` |
| qa-test-guard-report:C17 | PASS | `tests/sweep/__init__.py` exists, 0 bytes |
| qa-test-guard-report:C18 | PASS | `git diff -- .gitignore`: two insertions after `.dev/sprint-state/` |
| qa-test-guard-report:C19 | PASS | `check-ignore` rc 0 for `.dev/sweeps/x.md`, rc 1 for `.dev/tasks/to-do/x.md` |
| qa-test-guard-report:C20 | PASS | H `conftest.py:63` (`check_git_args`) and `:116-118` (`check_orca_argv`) run first; E: signatures fit `probes._git` / `probes._orca` |
| qa-test-guard-report:C21 | PASS | G: 4 passed, same as the three saved records |
| qa-test-guard-report:C22 | PASS | not required by DESIGN 11; gap stays CORE-F30 (MINOR); G: guard exercised directly |
| qa-test-guard-report:C23 | PASS | not required; gap stays CORE-F31 (MINOR) |

130 rows, all PASS. The seven reports hold 160 check ids in all: the 130 above plus the 30 that failed in cycle 0 (outside the PASS set, so not rows of the table). Of those 30, the ones whose cause was a CORE-F1 to CORE-F10 finding now hold on the evidence in the findings table (classification C11, C15, C16, C18; interface C13; edge-case C4, C12, C18, C20; report-surface C12; conventions C12; readonly-safety C8 for its BLOCKING cause CORE-F1, while its MINOR residue CORE-F23 and CORE-F24 stays as a note). The other 18 failed only on MINOR findings that this round does not recheck.

## Summary

- F_0: 10 of 10 RESOLVED, 0 OPEN. PASS set: 130 of 130 still PASS, 0 regressions. New BLOCKING: 0. New MAJOR: 0. New MINOR notes: 4 (V1-N1 to V1-N4).
- Confidence: Verified: 140/140 (10 findings + 130 PASS-set ids) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Caveat: the 100% is the share of items I ran, not a claim the code is defect-free. Items marked I (unchanged files) rest on an unchanged file plus a passing test run, not a new independent probe; live Orca shapes (open item 6, the `agentWait` keys) cannot be checked here.
- Tool engagement: Read: about 48 | Grep: 8 | Glob: 3 | Bash: 14 (ruff, pytest, git, stat, and 7 `uv run python -I` scratch runs writing only to /tmp; scratch dirs `/tmp/vc1-*` and `/tmp/vc1e-*` removed). Tavily/web research: none. Scratch mistakes that I corrected in my own scripts, not in the code: a `d/"x%d"%off` precedence error, an unregistered module in the guard import, quoted annotation strings in the signature compare, and an order-independence compare over unequal row sets; each was re-run and passed.
- Files written: this report only. No repository file was edited.

Verdict: PASS
Blocking count: 0

