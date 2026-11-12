# QA Report - Cycle 1 verification of the sweep core (item T189, fix-cycle re-check)

**Topic:** `superclaude sweep` core (`src/superclaude/cli/sweep/{__init__,models,classify,probes,report}.py`, `tests/sweep/`), cycle-0 findings CORE-F1 to CORE-F10
**Date:** 2026-11-12
**Phase:** fix-cycle (rf-qa-qualitative, `fix_authorization: false`; no file other than this report was written)
**Fix cycle:** 1

---

## Overall Verdict: PASS (the closing `Verdict:` and `Blocking count:` lines are at the end of this report)

All ten cycle-0 BLOCKING and MAJOR findings (`F_0`, `|F_0|` = 10) are RESOLVED on disk. All 130 check ids of the cycle-0 PASS set still PASS. No new BLOCKING or MAJOR finding. Six MINOR notes are recorded (N-1 to N-6); they never fail a review and are not rechecked in later rounds.

How I checked: I read the four edited modules end to end in chunks of at most 150 lines (`models.py` 256 lines, `probes.py` 1371, `classify.py` 996, `report.py` 673), re-read each changed passage against the fix log's `file:line` list, and then ran four scratch scripts (`uv run --no-sync python -I`, written to a private `/tmp/ironclaude-batch.*` directory, removed on exit, nothing written in the repository) with about 110 assertions in total, all PASS (one assertion in script 3 ends in `or True` and proves nothing; I do not cite it, and the two assertions after it cover the same fact). The gate commands were re-run by me, not copied from the fix log.

Gate commands re-run in this session:

| Command | Exit | Result |
|---|---|---|
| `uv run ruff check src/superclaude/cli/sweep tests/sweep` | 0 | `All checks passed!` |
| `uv run ruff format --check src/superclaude/cli/sweep tests/sweep` | 0 | `9 files already formatted` |
| `uv run pytest tests/sweep -p no:cacheprovider` | 0 | 4 passed in 0.29 s (same 4 tests as `step-1.4a-pytest.txt`, `step-1.4-pytest.txt`, `phase8-validation.md`) |
| `git diff .gitignore` | 0 | exactly the comment line and `.dev/sweeps/` after `.dev/sprint-state/` (`.gitignore:255-256`); nothing covers `.dev/tasks/` |
| file times (`ls -l --time-style=full-iso`) | 0 | only `models.py`, `probes.py`, `classify.py`, `report.py` changed after the cycle-0 reports; `__init__.py`, `tests/sweep/*`, `.gitignore` and the evidence files predate them |

## Findings of `F_0`: RESOLVED or OPEN

| Id | Severity | Status | Evidence (file:line on disk now) | Independent proof (scratch scripts 1 to 3) |
|---|---|---|---|---|
| CORE-F1 | BLOCKING | RESOLVED | `probes.py:604-636` `_packages` checks `_inside(folder, worktree)` for `to-do` and `done` (row `outside root` at :609) and `_inside(folder / name, worktree)` for each package (row at :632); `probes.py:587-595` `_marker(path, root)` returns False unless `_inside(path, root)`; call at `probes.py:641` passes `worktree`; ledger already used `_ledger(ledger, worktree)` at :645 | Symlinked `to-do` gives no package plus an `outside root` row; symlinked package folder skipped (`['pkgY', 'pkgZ']`) plus a row; `.archiving` symlink to an outside file gives `archiving_marker False`; real inside `.archiving` gives True; `.dev` itself symlinked outside gives nothing and two rows; a normal tree gives both packages and no row; a missing worktree gives no packages and no row |
| CORE-F2 | MAJOR | RESOLVED | `classify.py:830-854` `_prepare_worktrees(worktrees, frozen_paths)` sets `frozen=True` (never False) at :846; `classify.py:928-936` builds `frozen_paths` from built rows whose `orca.worktree_path` is set and `policy_of(row) == "frozen"`, then calls `_prepare_worktrees` and `by_path` after the rows exist; `removable()` at :457-458 now returns `("no", "frozen plan")`; `probes.py:918` comment names `classify_all` as the setter | Through `classify_all`: failed contract with `E-HALT-QA` on a row whose `worktree_path` is the worktree gives `frozen True`, `removable ("no","frozen plan")`; a second worktree stays `None`; JSON `worktrees[].frozen` is `[true, null]`; a trailing-slash path still matches (`_norm`); a failed contract with no STOP code leaves `frozen None`. The same result came out of the full `collect` then `classify_all` run with faked seams (script 3) |
| CORE-F3 | MAJOR | RESOLVED | `classify.py:733-734` `_guard` filters `r.status != "ready"` before the four case expressions (:737-743) | One ready Task plus one transcript: `person_started True`, notes exactly `('origin not proved: ...',)`, no `could not join` note, no `join not observable`, no `earlier pane`. Ready Task plus a real in-progress Dispatch row (`session_join` `h1`, not in the tab map) plus the transcript: `person_started None` with the `could not join` note. A real Dispatch row with no `session_join` still triggers guard case 1 (`tab map join not observable`) |
| CORE-F4 | MAJOR | RESOLVED | `classify.py:562-583` `_contract_for` builds `folders` with the shared `REPORT_DIR_RE` (:570) and attaches a contract whose `str(c.path.parent)` equals one folder (:574); `models.py:21-24` holds `CONTRACT_FILE` and `REPORT_DIR_RE`; `probes.py:993-1006` uses both (the local copies are gone: grep for `_CONTRACT_FILE`, `_REPORT_DIR_RE` has no hit) | `probes._read_contracts` finds `<rd>/return-contract.yaml` from `--report-dir <rd>` text and `classify._contract_for` attaches it; `--report-dir <rd>x` attaches nothing; the `=` form with a trailing slash attaches; two rows naming two folders each get their own; in the full run the frozen row got its contract through the report folder only |
| CORE-F5 | MAJOR | RESOLVED | `probes.py:129-153` `share_shows(runs, wanted=None)`: even split, then each Run takes `min(share, wanted)` and the unused rest goes to the Runs that still need shows; `probes.py:155-167` `take_show` allows `share - taken` (the one-way carry is gone: grep `carry` has no hit); `probes.py:1015-1091` `_orca_reads` reads every `worker-list`, ready `task-list` and `task-list` first, calls `share_shows(runs, {run: _show_demand(...)})` at :1086, then `_run_rows`; `_show_demand` at :1094-1101 counts exactly the shows `_run_rows` takes (valid Dispatch ids whose duplicate rows all agree) | Shares: A40/B10 gives 40,10; A10/B60 gives 10,40; A5/B5/C60 gives 5,5,40; two Runs of 40 give 25,25 (DESIGN line 341); three Runs without `wanted` give 18,16,16. Random property (2000 cases): sum of shares equals `min(cap, demand)` and no share exceeds demand. Through `_orca_reads` with a faked `_call`: A40/B10 = 50 `worker-show` calls, none cut; 2x40 = 50 calls, 30 cut, 80 rows; 3x40 = 50 calls; all lists are read before the first show; call count is `3R + shows`; the argv count and the 60-row and 50-row DESIGN 11 fixtures hold (see F8) |
| CORE-F6 | MAJOR | RESOLVED | `probes.py:763-770` `_tail_from_bytes`: `last_ts = ts` sits inside `if ts is not None and isinstance(sid, str) and sid:` | Records 07:00 and 08:00 then `{"type":"last-prompt","sessionId":"S1"}`: `last_record_ts` 08:00 (was None); a record with a timestamp but no `sessionId` does not set it; no complete record gives unreadable and `last_record_ts None`; a last line cut mid-object keeps the earlier record |
| CORE-F7 | MAJOR | RESOLVED | `probes.py:1296-1338` `_read_contracts`: the per-candidate body is inside `try/except (OSError, ValueError, OverflowError)` (:1333) and records `unscanned: contract not readable`; `probes.py:728-743` `_contract` reads the file time once after the stable read into `ContractRecord.mtime` (:737) and also catches `ValueError`, `OverflowError`; the age comes from `record.mtime` (:1322-1325), no second `os.stat` | `os.stat` made to raise `FileNotFoundError` on the 4th call (after the read) gives no record and exactly one `unscanned` row with `contract not readable`, no exception; `Path.exists` raising `PermissionError` gives the same; a normal read keeps `mtime` and an age; an absent contract is no source row; an outside-root contract gives one `outside root` row |
| CORE-F8 | MAJOR | RESOLVED | `classify.py:857-864` `_show_cut` collects source rows whose `unscanned` holds `SHOW_CAP_REASON` or `TIME_BUDGET_REASON`; `classify.py:965-966` counts only Orca rows whose own `orca worker-show <dispatch>` row is in that set; `_not_enriched` is gone; `probes.py:181-185` builds both reason texts from the same two constants (`models.py:28-29`) | Two disagreeing duplicate Dispatch rows plus one empty show (source row `read`): `bound_reached 0`. A row cut by the real `_show` cap path (`show cap reached (0)`) and one cut by a spent time budget (`time budget reached (90 s)`) count; a `orca call failed (exit 1)` show row does not. 60-row Run: 50 shows and `bound_reached 10`; 50-row Run: 50 shows and 0; 2x40: 30; all `<= summary.visible` (DESIGN line 345) |
| CORE-F9 | MAJOR | RESOLVED | `report.py:106-119` `_wait_age_s` takes the earlier of a blocked contract's `mtime` and the agentWait time, None when neither is known or the earlier is in the future (SP-15, `merged-requirements.md:238`); `models.py:102-103` `ContractRecord.mtime`; set in `probes.py:737` and passed through `_contract_from_text` (:703-724) | Blocked contract with `mtime` 3 h old: age 10800 s and the rendered Waiting (a) row prints `3h 0m`; with an agentWait time 7 h old as well: 25200 s (the earlier); agentWait only: 25200; future agentWait: unknown age plus `timestamp in the future`; no time known: unknown; a `failed` contract's `mtime` is not used; three rows (1 h, 5 h, unknown) sort 5 h, 1 h, unknown |
| CORE-F10 | MAJOR | RESOLVED | one parser: `probes.py:352-376` `parse_time` holds the only `fromisoformat` call in the package (grep: `fromisoformat` only at `probes.py:366`); `probes.py:461-472` `_WAIT_TIME_KEYS` and `_wait_since` (the only copy, grep confirms); `probes.py:421` stores `agent_wait_since` on the observation; `models.py:89-90` the field; `classify.py:228` and `report.py:114` read it; `_as_utc`, `_wait_time`, both `_WAIT_TIME_KEYS` copies and the `timezone` import in `classify.py` are gone (grep: no hit in `classify.py`/`report.py`) | `agentWait` as a dict with `startedAt` 09:00 and `since` 08:00 gives 08:00; a plain time string gives its time; `agentWait: null` gives present, value None, time None; absent key gives not present; no show gives all None; junk values (`123`, `[1]`, `{"x": object()}`, `""`, `True`, `{"since":"junk","at":5}`) raise nothing |

Per the review severity rule the 57 MINOR findings CORE-F11 to CORE-F67 were not rechecked; they stay recorded as notes. The fix log's note that CORE-F22 and CORE-F61 now read slightly differently is accurate (relative `--report-dir` still finds no contract; `ContractRecord.mtime` and `OrcaObservation.agent_wait_since` are new fields, each with a comment at `models.py:89` and `models.py:102`).

## New findings from the fix

BLOCKING: none. MAJOR: none.

MINOR notes (all graded minor by the severity rule: documentation drift or an extremely uncommon edge; none changes behaviour that DESIGN or SPEC pins):

| Id | Location | Note |
|---|---|---|
| N-1 | `models.py:12` | `models.py` now imports `re` (for `REPORT_DIR_RE`). DESIGN section 4's boundary table (`docs/designs/orchestrator-mode.md:209`) lists `dataclasses`, `datetime`, `typing`, `pathlib` for `models.py`, and cycle-0 `qa-readonly-safety-report:C10` and `qa-interface-report:C17` quote "only `dataclasses`, `datetime`, `pathlib`". The binding column is "must not import" (every other sweep module); `re` is stdlib and pure, so NFR-004 purity holds. Update the DESIGN table text in the next DESIGN pass. |
| N-2 | `probes.py:129-131` | `Budget.share_shows` has a second optional argument `wanted`. DESIGN 7.1 line 369 shows `share_shows(self, runs)` with the comment "even split, remainder to the first Run"; production now passes `wanted`, so that comment describes only the default. The DESIGN call `share_shows(runs)` still works and gives 18/16/16 (scratch). Same class as cycle-0 CORE-F14. |
| N-3 | `models.py:21-29`, `:90`, `:103` | Four new public constants and two new defaulted fields (`OrcaObservation.agent_wait_since`, `ContractRecord.mtime`) are not in DESIGN 7.2's field lists. Both fields are read (classify.py:228, report.py:112-114), and each has a comment. Phase 10 fixtures that build an `OrcaObservation` by hand must set `agent_wait_since` themselves for the age and future-wait cases; setting only `agent_wait` leaves the time None. |
| N-4 | `classify.py:570-574` | The folder match compares the raw text folder with `str(Path.parent)`, so `--report-dir /a//b` (double slash) does not attach (scratch: False). It failed before the fix as well; not a regression. |
| N-5 | `probes.py:1015-1091` | The order of rows in `Source coverage` changed (all list rows before the show rows), as the fix log says. DESIGN does not pin a source order (grep found none); Phase 10 tests that assert an order must use the new one. |
| N-6 | `fix-log-cycle1.md` | Cosmetic: the log cites `probes.py:129-161` for `share_shows` and `take_show`; `take_show` ends at :167. Every other `file:line` in the log matched the file on disk. |

## Checks

Result for every check id of the cycle-0 PASS set (130 ids) plus the 12 cycle-0 FAIL ids that were tied to a BLOCKING or MAJOR finding. Basis codes: R = re-read of the code on disk now; S = scratch assertion (scripts 1 to 4); G = gate command or grep run now; U = file unchanged since cycle 0 (file times) and re-run.

| Check id | Result | Basis |
|---|---|---|
| qa-classification-report:C1 | PASS | R `classify.py:337-347`; S `RULES` names printed: the nine DESIGN names in order |
| qa-classification-report:C2 | PASS | R `classify.py:160-187,210-211`; S a settled-failed row with a blocked contract matches `blocked_contract` (a) |
| qa-classification-report:C3 | PASS | R `classify.py:190-215` (unchanged) |
| qa-classification-report:C4 | PASS | R `classify.py:218-222` (unchanged) |
| qa-classification-report:C5 | PASS | R `classify.py:225-247`; S agentWait row matches `waiting_signal` (a), future time adds `timestamp in the future` |
| qa-classification-report:C6 | PASS | R `classify.py:250-263` (unchanged) |
| qa-classification-report:C7 | PASS | R `classify.py:266-286` (unchanged) |
| qa-classification-report:C8 | PASS | R `classify.py:289-305` (unchanged) |
| qa-classification-report:C9 | PASS | R `classify.py:308-321` (unchanged) |
| qa-classification-report:C10 | PASS | R `classify.py:324-334,350-378` (unchanged) |
| qa-classification-report:C11 | PASS | S F4: contract found through `--report-dir` is attached to its row (was FAIL, CORE-F4) |
| qa-classification-report:C12 | PASS | R `classify.py:659-668` (path A, unchanged) |
| qa-classification-report:C13 | PASS | R `classify.py:601-644,669-675` (path B, unchanged) |
| qa-classification-report:C14 | PASS | R `classify.py:747-766`; S ready Task plus transcript gives True plus `origin not proved`; real unjoined row gives None plus pane notes |
| qa-classification-report:C15 | PASS | S F3: a ready Task no longer trips guard case 1 (was FAIL, CORE-F3); a real Dispatch row without `session_join` still does |
| qa-classification-report:C16 | PASS | S F3: guard case 2 ignores a ready-only list (`classify.py:734,738`) and still fires with a real unjoined Dispatch row (was FAIL, CORE-F3) |
| qa-classification-report:C17 | PASS | R `classify.py:739-742`; S a real row with `session_join` `h1` not in the tab map gives the `could not join` note |
| qa-classification-report:C18 | PASS | S F3: guard case 4 (`earlier_pane`, `classify.py:743`) is absent for a ready-only list and present with a real row (was FAIL, CORE-F3) |
| qa-classification-report:C19 | PASS | G no time parser left in `classify.py` (grep `fromisoformat`, `_as_utc`, `timezone`: none); `probes.py:352-376`; S aware comparison in the future-wait case |
| qa-classification-report:C20 | PASS | R `classify.py:540-550` (unchanged) |
| qa-classification-report:C21 | PASS | R `classify.py:623-644` (unchanged) |
| qa-classification-report:C22 | PASS | R `classify.py:611-620` (unchanged) |
| qa-classification-report:C23 | PASS | R `classify.py:504-537,869`; S two disagreeing rows give one merged row with `conflict: duplicate Dispatch rows disagree`; `_merge_group` copes with the new `agent_wait_since` default |
| qa-classification-report:C24 | PASS | R `classify.py:870,939` (sorted transcripts and rows); the fix added no order dependence |
| qa-classification-report:C25 | PASS | R `classify.py:682-712` (unchanged) |
| qa-classification-report:C26 | PASS | R `classify.py:747-766` (note order unchanged) |
| qa-classification-report:C27 | PASS | S all 28 `NOTE_*`/`REASON_*` strings found verbatim in DESIGN or SPEC; report literals found; `classify` and `report` copies equal |
| qa-classification-report:C28 | PASS | R `classify.py:376-377,804-823` (unchanged) |
| qa-classification-report:C29 | PASS | R `classify.py:225-235,373-374`; S future agentWait gives unknown age plus the note |
| qa-conventions-report:C1 | PASS | U `__init__.py` (file time 01:14, lazy `__getattr__` at :4-12) |
| qa-conventions-report:C2 | PASS | U `tests/sweep/__init__.py` present and empty |
| qa-conventions-report:C3 | PASS | U `conftest.py:80-86,127-134` (`patch_git`, `patch_orca`, `monkeypatch.setattr`) |
| qa-conventions-report:C6 | PASS | R every `models.py` class is `@dataclass(frozen=True)` (:55,64,93,106,121,129,154,163,173,190,199,206,214,231,239) |
| qa-conventions-report:C8 | PASS | G import grep: models `re`/`dataclasses`/`datetime`/`pathlib`, classify `re`/`collections.abc`/`dataclasses`/`datetime`/`pathlib`, report `re`/`unicodedata`; none imports `subprocess`, `click`, `os`, `shutil` (see N-1) |
| qa-conventions-report:C9 | PASS | G `git status`: no `pyproject.toml` or lock change; imports are stdlib or pytest |
| qa-conventions-report:C10 | PASS | G `git diff .gitignore`: the comment plus `.dev/sweeps/` after `.dev/sprint-state/`, nothing else |
| qa-conventions-report:C11 | PASS | S 10 `ALLOWED_ORCA` templates, 7 verbs, `ALLOWED_GIT`, `FORBIDDEN_TOKENS` printed and compared |
| qa-conventions-report:C12 | PASS | G one parser: `fromisoformat` only at `probes.py:366`; `_WAIT_TIME_KEYS` only at `probes.py:462`; none in `classify.py`/`report.py` (was FAIL, CORE-F10) |
| qa-conventions-report:C17 | PASS | R OQ-11 comment `models.py:140-141`, `report.py:381` |
| qa-conventions-report:C18 | PASS | R OQ-14 comment `models.py:230` |
| qa-conventions-report:C21 | PASS | G ruff check and ruff format --check exit 0 |
| qa-edge-case-report:C1 | PASS | S 3 Runs without `wanted` give 18/16/16 |
| qa-edge-case-report:C2 | PASS | S 50th take True, 51st False, `show cap reached (50)` |
| qa-edge-case-report:C3 | PASS | S timeouts at 10.0, 9.999, 1.0 and 0.999 s left, and `cut()` |
| qa-edge-case-report:C4 | PASS | S unused share reaches the other Runs: A40/B10 reads 50 shows (was FAIL, CORE-F5) |
| qa-edge-case-report:C5 | PASS | R `probes.py:261-264,306-307` (unchanged; `>` the limit) |
| qa-edge-case-report:C6 | PASS | R `probes.py:733-734` (`over 1 MiB` only above the limit) |
| qa-edge-case-report:C7 | PASS | R `probes.py:557-569` (unchanged) |
| qa-edge-case-report:C8 | PASS | R `probes.py:803-811` (unchanged) |
| qa-edge-case-report:C11 | PASS | R `probes.py:757-781`; S cut last line skipped, earlier record kept, no complete record gives unreadable |
| qa-edge-case-report:C12 | PASS | S trailing record without a timestamp keeps `last_record_ts` (was FAIL, CORE-F6) |
| qa-edge-case-report:C13 | PASS | R `probes.py:795-825` (unchanged) |
| qa-edge-case-report:C14 | PASS | R `classify.py:373-374`; S future waiting time gives unknown age plus the note |
| qa-edge-case-report:C16 | PASS | R `probes.py:930-954` (unchanged) |
| qa-edge-case-report:C18 | PASS | S `os.stat` and `Path.exists` failures inside `_read_contracts` give one unscanned row, no raise (was FAIL, CORE-F7) |
| qa-edge-case-report:C19 | PASS | R `probes.py:1133-1141`; S disagreeing duplicates give one row, no show used, `bound_reached 0` |
| qa-edge-case-report:C20 | PASS | S `bound_reached` counts only rows cut by the cap or the budget (was FAIL, CORE-F8) |
| qa-edge-case-report:C21 | PASS | R `probes.py:547-554` (`_stable`), `classify.py:821` (unchanged) |
| qa-edge-case-report:C23 | PASS | R `probes.py:397-442` (tolerant `_get`); S junk or missing `agentWait` and no show raise nothing |
| qa-edge-case-report:C25 | PASS | R `probes.py:475-516` (unchanged) |
| qa-edge-case-report:C26 | PASS | R `probes.py:352-376`; S SQLite and ISO forms, junk, non-string |
| qa-edge-case-report:C27 | PASS | S constants and 10 templates printed (script 4) |
| qa-edge-case-report:C28 | PASS | G `git diff .gitignore`; `gitignore-check.md`; the real-git test passes |
| qa-edge-case-report:C32 | PASS | G 4 tests pass; `step-1.4a-pytest.txt`, `step-1.4-pytest.txt`, `phase8-validation.md` agree |
| qa-edge-case-report:C33 | PASS | R `probes.py:406-441` field paths against `1.0a-facts.md` rows 1, 6, 23 |
| qa-interface-report:C1 | PASS | U `__init__.py:4-9` lazy `sweep_group` |
| qa-interface-report:C2 | PASS | R all 15 types present and frozen; existing field names and order unchanged; two new defaulted fields at the end (`models.py:90,103`, N-3) |
| qa-interface-report:C3 | PASS | R `models.py:17,31-52` (`JSON_SCHEMA_VERSION`, `CLASSES`, `PACKAGE_STATES`, `SAFE_VALUES`) |
| qa-interface-report:C4 | PASS | R `models.py:231-236` (`row`, `classification`, `policy`, `safe`) |
| qa-interface-report:C5 | PASS | R `classify.py:361,381,415,424,447,471,867` signatures as in DESIGN 7.1 |
| qa-interface-report:C6 | PASS | S `RULES` names and count printed |
| qa-interface-report:C7 | PASS | R `probes.py:96-185`; `share_shows(runs)` still works (N-2) |
| qa-interface-report:C8 | PASS | R `probes.py:352,397,475,656,861,866,957,1219` all present with DESIGN parameters |
| qa-interface-report:C9 | PASS | S 10 templates, `ALLOWED_GIT`, `FORBIDDEN_TOKENS`; R `probes.py:41-77` |
| qa-interface-report:C10 | PASS | R `report.py:23-24,523-536,547,580,586,591` |
| qa-interface-report:C11 | PASS | S JSON v1 top-level keys (12) printed and equal; `frozen` key present in each worktree |
| qa-interface-report:C12 | PASS | R `report.py:523-536` section order; S `render` ends `Report complete\n` |
| qa-interface-report:C13 | PASS | S `WorktreeState.frozen` is now set by `classify_all` (was FAIL, CORE-F2); `agent_wait_since` and `mtime` are set by `probes` and read by `classify`/`report` |
| qa-interface-report:C14 | PASS | G `git diff .gitignore`; `gitignore-check.md` records 0 and 1 |
| qa-interface-report:C15 | PASS | G `uv run pytest tests/sweep` gives 4 passed; U `conftest.py`, `test_readonly.py` |
| qa-interface-report:C16 | PASS | R `probes.py:406-441` field paths; `1.0a-facts.md` rows 1, 6, 23 |
| qa-interface-report:C17 | PASS | G import grep; purity holds (N-1) |
| qa-interface-report:C18 | PASS | R extras are constants and helpers only (`models.py:21-29`, `probes._wait_since`, `probes._show_demand`); none renamed or missing (N-3) |
| qa-readonly-safety-report:C1 | PASS | S 10 templates, 7 verbs |
| qa-readonly-safety-report:C2 | PASS | S `check_orca_argv` rejects `--include-remote`, a bad Dispatch id, an extra flag and an unknown verb |
| qa-readonly-safety-report:C3 | PASS | R `probes.py:245` `check_orca_argv` is the first line of `_orca`; G `subprocess.run` appears only at `probes.py:248,299` |
| qa-readonly-safety-report:C4 | PASS | R `probes.py:295` `check_git_args` first in `_git`; U `test_readonly.py:80-87` passes |
| qa-readonly-safety-report:C5 | PASS | S `FORBIDDEN_TOKENS == {"--include-remote"}`; R `probes.py:208` tests any position |
| qa-readonly-safety-report:C6 | PASS | R `probes.py:296-297`; U `test_readonly.py:59-77` passes |
| qa-readonly-safety-report:C7 | PASS | G grep for `open(`, write, mkdir, unlink, rename, flock, symlink: only `open(..., "rb")` at `probes.py:559,805,869` |
| qa-readonly-safety-report:C8 | PASS | S every reader re-resolves inside the root: package folders, packages, `.archiving`, ledger (`probes.py:604-641,587-595,645`) (was FAIL, CORE-F1) |
| qa-readonly-safety-report:C9 | PASS | R `import subprocess` `probes.py:15`; `subprocess.run` at :248, :299 |
| qa-readonly-safety-report:C10 | PASS | G import grep: purity holds; `models.py` also imports stdlib `re` (N-1) |
| qa-readonly-safety-report:C11 | PASS | G grep for write verbs in `probes.py` (create, delete, merge, push, release, `worktree rm`...): no hit |
| qa-readonly-safety-report:C12 | PASS | R `probes.py:41,191-193` `orca-ide` default, `ORCA_CLI_COMMAND` override |
| qa-readonly-safety-report:C13 | PASS | G `git diff .gitignore` two lines; `git check-ignore` record in `gitignore-check.md` |
| qa-readonly-safety-report:C14 | PASS | G pytest 4 passed; R `test_readonly.py:59-166` runs the real `probes._git` seam |
| qa-report-surface-report:C1 | PASS | R `report.py:523-536` 12 functions in DESIGN 7.5 order |
| qa-report-surface-report:C2 | PASS | R `report.py:164-192` |
| qa-report-surface-report:C3 | PASS | R `report.py:29` `NO_RECORDS` and its uses |
| qa-report-surface-report:C4 | PASS | R `report.py:580-583` cut at `CELL_MAX`; `to_json` (:591-673) does not call `cell` |
| qa-report-surface-report:C5 | PASS | R `report.py:547-577` |
| qa-report-surface-report:C6 | PASS | R `report.py:145-152` |
| qa-report-surface-report:C7 | PASS | R `report.py:188-191,386-392`; S `total == visible + historical` |
| qa-report-surface-report:C8 | PASS | R `report.py:36-39,392` |
| qa-report-surface-report:C9 | PASS | S rendered report ends `Report complete\n` |
| qa-report-surface-report:C10 | PASS | R `report.py:367-383` (policy never `not frozen`) |
| qa-report-surface-report:C11 | PASS | R `report.py:41-54` `NEXT_INSPECTION` values are only "read ..." text |
| qa-report-surface-report:C12 | PASS | S Waiting (a) age uses the earlier of contract mtime and agentWait time, sorts oldest first, unknown group last, renders `3h 0m` (was FAIL, CORE-F9) |
| qa-report-surface-report:C13 | PASS | R `report.py:264-305` |
| qa-report-surface-report:C14 | PASS | R `report.py:386-423` |
| qa-report-surface-report:C15 | PASS | R `report.py:213-261,264-305` layout unchanged |
| qa-report-surface-report:C16 | PASS | G `report.py` imports only `re`, `unicodedata`, `.models`; no clock, file or env read |
| qa-report-surface-report:C17 | PASS | S 12 JSON keys, output equal on a second call |
| qa-report-surface-report:C18 | PASS | R `report.py:141-142,257,304,330` |
| qa-report-surface-report:C19 | PASS | G `git diff .gitignore`; `gitignore-check.md` |
| qa-report-surface-report:C20 | PASS | G `phase8-validation.md` agrees with a fresh run (ruff, format, import, 4 passed) |
| qa-report-surface-report:C21 | PASS | R `report.py:195-210,334-364,480-495` |
| qa-report-surface-report:C22 | PASS | R `report.py:41-54` keys equal the `RULES` names printed in script 4 |
| qa-test-guard-report:C1 | PASS | U `conftest.py:38` |
| qa-test-guard-report:C2 | PASS | U `conftest.py:39` |
| qa-test-guard-report:C3 | PASS | U `conftest.py:40` |
| qa-test-guard-report:C4 | PASS | U `conftest.py:28` reads `request.function.pytestmark` only |
| qa-test-guard-report:C5 | PASS | U `conftest.py:29-30` |
| qa-test-guard-report:C6 | PASS | G one `pytest.mark.integration` in `tests/sweep` (`test_readonly.py:109`) |
| qa-test-guard-report:C7 | PASS | U `conftest.py:38-40` use `monkeypatch`; 4 tests pass in sequence |
| qa-test-guard-report:C8 | PASS | G `pyproject.toml:114` has `--strict-markers` and :119 registers `integration`; pytest ran 4 tests under it |
| qa-test-guard-report:C9 | PASS | U `test_readonly.py:59-77` |
| qa-test-guard-report:C10 | PASS | U `test_readonly.py:59-62,75` |
| qa-test-guard-report:C11 | PASS | U `test_readonly.py:80-87` |
| qa-test-guard-report:C12 | PASS | U `test_readonly.py:90-99` |
| qa-test-guard-report:C13 | PASS | U `test_readonly.py:127` |
| qa-test-guard-report:C14 | PASS | U `test_readonly.py:134-166` |
| qa-test-guard-report:C15 | PASS | U `test_readonly.py:161-166` `warnings.warn` |
| qa-test-guard-report:C16 | PASS | G only `probes.py` starts processes; the one marked test runs git only |
| qa-test-guard-report:C17 | PASS | U `tests/sweep/__init__.py` empty |
| qa-test-guard-report:C18 | PASS | G `git diff .gitignore` (`.gitignore:255-256`) |
| qa-test-guard-report:C19 | PASS | G `gitignore-check.md`; the real-git test asserts return codes 0 and 1 |
| qa-test-guard-report:C20 | PASS | U `conftest.py:63,116-118`; `probes._git(cwd, *args, timeout)` at `probes.py:289` |
| qa-test-guard-report:C21 | PASS | G saved outputs and a fresh run all show 4 passed |
| qa-test-guard-report:C22 | PASS | no change; gap stays a MINOR note (CORE-F30) |
| qa-test-guard-report:C23 | PASS | no change; gap stays a MINOR note (CORE-F31) |

Count: 130 PASS-set ids listed above as PASS (classification 25, conventions 11, edge-case 20, interface 17, readonly-safety 13, report-surface 21, test-guard 23) and 12 cycle-0 FAIL ids tied to a BLOCKING or MAJOR finding that are now PASS (classification C11, C15, C16, C18; conventions C12; edge-case C4, C12, C18, C20; interface C13; readonly-safety C8; report-surface C12). That is 142 rows, 0 FAIL.

"Unchanged" in the Basis column means the passage is outside the fix log's list of changed passages, I read it on disk now, and it still satisfies the check text. I could not diff against cycle 0 because the package is untracked; the file times (02:42 for the four edited modules, all other inputs older than the cycle-0 reports) are the evidence that nothing else moved.

Cycle-0 FAIL ids tied only to MINOR findings (not rechecked, recorded as notes): qa-conventions-report C4, C5, C7, C13, C14, C15, C16, C19, C20; qa-edge-case-report C9, C10, C15, C17, C22, C24, C29, C30, C31. No further check ids exist in the seven reports.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)

The spawn prompt carried no `## Inherited Structural Verdict` section, so I fell back to standalone behaviour and did not skip any structural re-check on the strength of an earlier PASS.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was supplied. The cycle-0 PASS set was treated as claims to re-verify, not as facts: every id above has an R, S, G or U basis from this session. I did not read the other cycle-1 verifier's report (`verify-cycle1-rf-qa.md`, which exists in the folder) so that this result stays independent of it.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Fix F5 end to end: scratch script 2 fakes `probes._call`, runs the real `_orca_reads`, and counts `worker-show` calls (A40/B10: 50 and none cut; 2x40: 50 and 30 cut; 3x40: 50; 60-row Run: 50 and `bound_reached` 10; 50-row Run: 50 and 0), plus a 2000-case property check that the shares add up to `min(cap, demand)`.
- Fix F2 and F4 together on a full `collect` then `classify_all` then `render` and `to_json` run with faked `_orca` and `_git` (script 3): the contract is found through `--report-dir`, attached to its row, the row is `frozen`, its worktree has `frozen True` and the JSON carries it, the other worktree stays `None`, the Orca argv count is `3R + shows + 1` and git runs once per worktree.
- Fix F1 with real symlinks on disk (script 1): symlinked `to-do`, symlinked package folder, symlinked `.archiving`, symlinked `.dev`.
- Fix F7 with `os.stat` raising after the read and `Path.exists` raising `PermissionError` (script 1).
- Fix F9 and F10 on the rendered Waiting (a) section (`3h 0m`, 25200 s earlier-of rule, oldest-first order, unknown group last), and junk `agentWait` values (script 2).
- DESIGN fidelity: all 28 `NOTE_*`/`REASON_*` strings and the report fixed lines were compared with the text of DESIGN and the SPEC by a program (script 4), not by eye.
- Regression for the changed `_merge_group` input (new defaulted field) by feeding two disagreeing duplicate rows through `classify_all` (script 2).

**Confidence:** Verified: 152/152 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (152 = 10 findings + 142 check rows).
**Tool engagement:** Read: about 40 | Grep: about 15 | Glob: 0 | Bash: 12 (4 scratch scripts, gate commands, file times, git status).

Flag (per the Tool Engagement Minimum): Read + Grep + Glob (about 55) is below the 152 items. The shortfall is by design, not padding: the 142 check rows are checked in groups. One Read of a code region serves every check id that cites it, and four scratch scripts (about 110 assertions) cover the behavioural ids. Every row names the region or script it rests on, so a reader can re-run any of them. No web research was done, so no Tavily call was needed or made.

**Items I could not fully close and why:** none open. Limits I want the reader to know: (1) the fix agent's and my scratch proofs run against faked Orca and git seams, not a live Orca (`1.0a-facts.md` row 6: the live `agentWait` key is still UNVERIFIED, so the guessed time keys in `probes.py:462` stay guesses); (2) no committed test covers any of the ten fixes yet, so a regression would not be caught by `tests/sweep` until Phase 10.

## Recommendations

- Proceed. No fix pass is needed for the cycle-0 BLOCKING and MAJOR findings.
- Carry N-1 to N-3 into the next DESIGN edit (module import table, `share_shows` signature and comment, the two new model fields), and carry N-3 and N-5 into the Phase 10 test fixtures.
- Phase 10 should turn the scratch proofs into committed tests: F1 symlink cases, F2 through `classify_all`, F3 ready-Task guard, F4 report-dir attach, F5 and F8 budget cases (the DESIGN 11 60-row, 50-row and 2x40 fixtures), F6 trailing record, F7 vanished contract, F9 age order, F10 single parser.

## QA Complete

Verdict: PASS
Blocking count: 0

