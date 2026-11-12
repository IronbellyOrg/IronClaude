# Fix log, cycle 1 (item 8.22)

Fix agent: single fix agent, `fix_authorization: true`.
Input: `qa/impl-core/consolidated-findings-cycle0.md`. Fixed: CORE-F1 to CORE-F10 (|F_0| = 10). Left alone as notes: CORE-F11 to CORE-F67 (MINOR).
Files edited: `src/superclaude/cli/sweep/models.py`, `probes.py`, `classify.py`, `report.py`. No test file, no `.gitignore`, no DESIGN, SPEC, 1.0a facts, task file or QA report was edited. Nothing was staged or committed. Line numbers below are after `ruff format`.

Status of all ten: FIXED. None left OPEN (no finding needed a DESIGN change; CORE-F5 and CORE-F9 were closed by changing the code to match DESIGN).

## Shared additions (used by several fixes)

New names are additive; no DESIGN 7.1 to 7.3 public name or signature changed. Every new dataclass field has a default.

| Where | Addition | Used by |
|---|---|---|
| `models.py:21-29` | `CONTRACT_FILE`, `REPORT_DIR_RE`, `SHOW_CAP_REASON`, `TIME_BUDGET_REASON` constants (plus `import re`) | CORE-F4, CORE-F8 |
| `models.py:90` | `OrcaObservation.agent_wait_since: datetime \| None = None` | CORE-F9, CORE-F10 |
| `models.py:103` | `ContractRecord.mtime: datetime \| None = None` | CORE-F7, CORE-F9 |
| `probes.py:129` | `Budget.share_shows(runs, wanted=None)`: second argument optional, so the DESIGN call `share_shows(runs)` still works | CORE-F5 |

## Per-finding changes

### CORE-F1 (BLOCKING): package folder scan and `.archiving` marker did not re-resolve inside the root

- `probes.py:598-641` (`_packages`): each of `to-do`/`done` is checked with `_inside(folder, worktree)` first; each package folder is checked with `_inside(folder / name, worktree)`. A failure adds an `unscanned` row with reason `outside root` (`probes.py:609`, `:632`) and skips the folder or package.
- `probes.py:587` (`_marker(path, root)`): now takes the root; returns False unless `_inside(path, root)`. The call at `probes.py:641` passes `worktree`.
- Proof (scratch): a symlinked `to-do` folder pointing outside lists no package and adds the `outside root` row; a symlinked package folder is skipped (`['pkgY', 'pkgZ']`); a `.archiving` symlink to an outside file gives `archiving_marker False`; a real inside `.archiving` still gives True. 5 checks, all PASS.

### CORE-F2 (MAJOR): `WorktreeState.frozen` never populated

- `classify.py:830-846` (`_prepare_worktrees(worktrees, frozen_paths=frozenset())`): sets `frozen=True` on a worktree whose normalised path is in `frozen_paths`; otherwise keeps the old value (None), never False.
- `classify.py:928-935` (`classify_all`): `frozen_paths` is built from the built rows whose `orca.worktree_path` is set and `policy_of(row) == "frozen"`; `_prepare_worktrees` and `by_path` now run after the rows are built (they ran before). `removable()` is unchanged and now returns `("no", "frozen plan")` for such a worktree.
- `probes.py:918`: comment updated (the value is set by `classify_all`, not by `probes`).
- Proof (scratch): through `classify_all`, a failed contract with `E-HALT-QA` on a row whose `worktree_path` is the worktree gives `frozen True`, `removable ("no", "frozen plan")`, and the JSON `worktrees[0].frozen` is `true`; a second worktree that hosts no frozen row stays `None`. 4 checks, all PASS.

### CORE-F3 (MAJOR): Ready Task rows counted as scoped Dispatch rows by guard cases 1, 2, 4

- `classify.py:734` (`_guard`): `rows = [r for r in rows if r.status != "ready"]` before the four case expressions, so cases 1, 2 and 4 (and 3, which cannot match a ready row) see only real Dispatch rows.
- Proof (scratch): one ready Task plus one transcript gives `person_started True` and only the note "origin not proved ..." (no `could not join` note); a ready Task plus a real in-progress Dispatch row plus the same transcript still gives `person_started None` with the `could not join` note. 3 checks, all PASS.

### CORE-F4 (MAJOR): contract found through `--report-dir` not attached to its row

- `classify.py:570` (`_contract_for`): collects the report folders named in the row text with the shared `REPORT_DIR_RE` and also attaches a contract whose `path.parent` equals one of them (exact folder match, so `<folder>x` does not match). The full-path match is kept.
- `probes.py:993-1004`: now uses `CONTRACT_FILE` and `REPORT_DIR_RE` from `models`, so `collect` and `classify` read the same pattern (the local `_CONTRACT_FILE` and `_REPORT_DIR_RE` are deleted).
- Proof (scratch): a row with `--report-dir <rd>` gets the contract at `<rd>/return-contract.yaml`; a row with `--report-dir <rd>x` gets None. 2 checks, both PASS.

### CORE-F5 (MAJOR): `min(D, 50)` missed when an earlier Run is bigger than its share (code changed to match DESIGN line 341)

- `probes.py:129-161` (`Budget.share_shows(runs, wanted=None)`, `take_show`): the one-way carry is deleted; `take_show` allows `share - taken`. With `wanted` (shows each Run needs), a Run takes `min(share, wanted)` and the unused rest goes to the Runs that still need shows, so the total is `min(D, shows)`. Without `wanted` the split is the old even split, remainder to the first Run.
- `probes.py:1015-1101` (`_orca_reads`, new `_show_demand` at `:1094`): all Runs' `worker-list`, ready `task-list` and `task-list` are read first; then `budget.share_shows(runs, {run: _show_demand(...)})`; then `_run_rows` (which takes the shows) runs for each Run. Call count per Run is unchanged (`1 + 3R + 1 + shows`).
- Proof (scratch): Run A 40 rows and Run B 10 rows: 40 + 10 = 50 shows; A 10 and B 60: 10 + 40; 2 Runs of 40: 25 + 25; 3 Runs of 40: 18/16/16; no `wanted`: 25 + 25. Through `_orca_reads` with a faked `_call` (A 40 rows, B 10 rows): 50 `worker-show` calls, all read, none cut. 6 checks, all PASS.

### CORE-F6 (MAJOR): trailing record without a timestamp blanked `last_record_ts`

- `probes.py:769` (`_tail_from_bytes`): `last_ts = ts` moved inside the complete-record test (timestamp and sessionId both present).
- Proof (scratch): records at 07:00 and 08:00, then `{"type":"last-prompt","sessionId":"S1"}`: `last_record_ts` is 08:00 (it was None). PASS.

### CORE-F7 (MAJOR): `collect` could raise from an unguarded `exists()` and age `os.stat`

- `probes.py:1296-1340` (`_read_contracts`): the per-candidate body is wrapped in `try/except (OSError, ValueError, OverflowError)`; on error it adds `SourceCoverage("contract <dispatch>", "unscanned", None, "contract not readable")`. The age now comes from `record.mtime` (no second `os.stat`).
- `probes.py:728-743` (`_contract`): reads the file time once after the stable read and stores it in `ContractRecord.mtime`; the except clause now also catches `ValueError` and `OverflowError`.
- Proof (scratch): a normal read keeps `mtime` and gives a `read` row with an age; with `os.stat` raising `FileNotFoundError` for the contract after the read, and with `Path.exists` raising `PermissionError`, `_read_contracts` returns no record and one `unscanned` row, no exception. 3 checks, all PASS.

### CORE-F8 (MAJOR): `bound_reached` inferred from "all show fields None"

- `classify.py:857` (`_show_cut`), `:965-966`: `bound_reached` now counts only Orca rows whose own `orca worker-show <dispatch>` source row is `unscanned` with the show-cap or time-budget reason (`SHOW_CAP_REASON`, `TIME_BUDGET_REASON`). `_not_enriched` is deleted.
- `probes.py:Budget.budget_reason` and `show_cap_reason` build their text from the same two constants, so the reason strings are unchanged.
- Proof (scratch): two disagreeing duplicate Dispatch rows plus one empty show (source row `read`): `bound_reached 0` (it was 2). Source rows with `show cap reached (50)` and `time budget reached (90 s)` count (2), and a plain `orca call failed (exit 1)` row does not. 3 checks, all PASS.

### CORE-F9 (MAJOR): Waiting (a) age ignored the blocked contract's file time (code changed to match SPEC line 238)

- `models.py:103`: `ContractRecord.mtime` (default None). Set in `probes._contract` (`probes.py:737`, passed through `_contract_from_text` at `:703-724`).
- `report.py:106` (`_wait_age_s`): the age is `now - min(t)` over the blocked contract's `mtime` (when `worker_status == "blocked"`) and the observation's `agent_wait_since` (when `agent_wait` is not None); None when no time is known or the earlier one is in the future.
- Proof (scratch): a blocked-contract row with `mtime` 3 h old: age 10800 s; with an agentWait time 7 h old as well: 25200 s (the earlier); the rendered report prints `7h 0m`. 4 checks (with the row being Waiting (a)), all PASS.

### CORE-F10 (MAJOR): three time parsers, `_WAIT_TIME_KEYS` copied into two modules

- `probes.py:462-470` (`_WAIT_TIME_KEYS`, `_wait_since`) and `:408-421` (`parse_worker_show`): the agentWait time is parsed once with `parse_time` and stored in `OrcaObservation.agent_wait_since`.
- Deleted: `classify._as_utc`, `classify._wait_time`, `classify._WAIT_TIME_KEYS`, `report._wait_time`, `report._WAIT_TIME_KEYS`, and the now-unused `timezone` import in `classify.py`. `classify.py:228` reads `orca.agent_wait_since`; `report.py:106` reads the same field.
- Proof (scratch): `agentWait` as a dict with `startedAt` 09:00 and `since` 08:00 gives 08:00; a plain string gives its time; `agentWait: null` gives None with `agent_wait_present True`. A text check shows `_WAIT_TIME_KEYS` is only in `probes.py` and `classify.py`/`report.py` hold no `_as_utc` or `fromisoformat`. 5 checks, all PASS.

## Scratch proof

One scratch script (36 checks) was written to a private `/tmp/ironclaude-batch.*` directory, run with `uv run python`, and deleted with its directory afterwards. Result: `ALL PASS`, exit 0. (A first run stopped at a mistake in the script itself, `to_json` needs a `report_path`; the script was fixed and re-run in full.) No test file was added to the repository.

## Verification commands (run in this order)

`ruff format` was run on the four files I edited only. A `ruff format --check` over both folders first showed one file to change (`probes.py`, a line I wrote), so the folder run would have touched the same file.

| # | Command | Exit | Last lines of output |
|---|---|---|---|
| 1 | `uv run ruff format src/superclaude/cli/sweep/probes.py src/superclaude/cli/sweep/classify.py src/superclaude/cli/sweep/report.py src/superclaude/cli/sweep/models.py` | 0 | `1 file reformatted, 3 files left unchanged` |
| 2 | `uv run ruff check src/superclaude/cli/sweep tests/sweep` | 0 | `All checks passed!` |
| 3 | `uv run python -c "import superclaude.cli.sweep.classify, superclaude.cli.sweep.probes, superclaude.cli.sweep.report"` | 0 | (no output) |
| 4 | `uv run pytest tests/sweep -v` | 0 | `tests/sweep/test_readonly.py::test_real_git_lock_free_status_and_gitignore PASSED [100%]` then `============================== 4 passed in 0.32s ===============================` |

## Notes for the next review

- MINOR findings CORE-F11 to CORE-F67 were not touched. Two of them now read slightly differently because of these fixes: CORE-F22 (a relative `--report-dir` still finds no contract, same regex) and CORE-F61 (`SweepResult.context` unchanged; `ContractRecord.mtime` and `OrcaObservation.agent_wait_since` are new fields, each with a comment).
- The order of rows in `Source coverage` changed for a sweep: all `worker-list`/`task-list` rows now come before the `worker-show` rows. The number and the argv of Orca calls are unchanged.
- `tests/sweep/` still has no test for any of these fixes; the real tests come in Phase 10.

## Orchestrator re-check after the agent returned (item 8.22)

### ruff check

Command: `uv run ruff check src/superclaude/cli/sweep tests/sweep`
Exit code: 0

```text
All checks passed!
```

PASS: ruff check

### ruff format --check

Command: `uv run ruff format --check src/superclaude/cli/sweep tests/sweep`
Exit code: 0

```text
9 files already formatted
```

PASS: ruff format --check

### import the three modules

Command: `uv run python -c import superclaude.cli.sweep.classify, superclaude.cli.sweep.probes, superclaude.cli.sweep.report`
Exit code: 0

```text
```

PASS: import the three modules

### pytest tests/sweep -v

Command: `uv run pytest tests/sweep -v`
Exit code: 0

```text
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.venv/bin/python
cachedir: .pytest_cache
SuperClaude: 5.0.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode
configfile: pyproject.toml
plugins: superclaude-5.0.0, anyio-4.16.0
collecting ... collected 4 items

tests/sweep/test_readonly.py::test_git_argv_and_env_are_lock_free PASSED [ 25%]
tests/sweep/test_readonly.py::test_check_git_args_allows_only_the_listed_call PASSED [ 50%]
tests/sweep/test_readonly.py::test_one_git_argv_per_worktree PASSED      [ 75%]
tests/sweep/test_readonly.py::test_real_git_lock_free_status_and_gitignore PASSED [100%]

============================== 4 passed in 1.34s ===============================
```

PASS: pytest tests/sweep -v
