# QA Report: publication-safety lens (impl-cli gate, T200)

**Topic:** `superclaude sweep run` publication path (`commands._publish`, DESIGN 3.2) and its exit mapping
**Date:** 2026-11-12
**Phase:** code gate, publication-safety lens
**Fix cycle:** N/A (`fix_authorization: false`; no file edited except this report)
**Reviewer stance:** adversarial; every claim below comes from a file read or a command run in this session, not from the producer's summaries.

## What was read

| Input | How |
|---|---|
| `src/superclaude/cli/sweep/commands.py` (288 lines) | Read in two chunks (1-150, 151-289) |
| `src/superclaude/cli/sweep/__init__.py`, `git diff -- src/superclaude/cli/main.py` | Read / diff |
| DESIGN sections 3, 5, 7.1 | Live `docs/designs/orchestrator-mode.md` lines 82-155, 223-292, 353-447. The base copy (`artifacts/design-base.md`) section 3 is byte-identical to the live one (diff of the two ranges printed nothing). Neither revision folder (`chat-output-exception-20261109-133150`, `plan-defect-fixes-20261110`) touches 3, 5 or 7.1 |
| OQ-2 and OQ-5 records | Both `status: RESOLVED`, owner-approved: `<root>/.dev/sweeps/`, `<YYYYMMDD-HHMMSS>-sweep.md` UTC, default window `6h` |
| `step-1.7-help.txt`, `phase9-validation.md`, `sweep-live-check-1.4.{json,md}`, `sweep-live-check-1.4-workers.json` | Read / sampled / cross-checked against the code and the on-disk `.dev/sweeps/` |

## Overall result

No departure from the seven `_publish` steps or from the error table. Findings: 0 BLOCKING, 0 MAJOR, 4 MINOR. Details in the sections below.

## Step-by-step walk (DESIGN 3.2 against `commands.py`)

| Design step | Code | Result |
|---|---|---|
| 1. `stem = now.strftime("%Y%m%d-%H%M%S") + "-sweep"` (UTC) | `commands.py:155`; `now` is `datetime.now(timezone.utc).replace(microsecond=0)` read once at `:248` and passed at `:275` | matches |
| 2. `os.makedirs(output_dir, exist_ok=True)`, then re-resolve and confirm still `<root>/.dev/sweeps/` or below, else `[sweep publish] output dir escaped <root>/.dev/sweeps/` | `:156` base computed (pure), `:158-160` makedirs, `:161-164` `output_dir.resolve()` compared with base, message `f"... escaped {base}/"` | matches (see M2 for how `base` is derived) |
| 3. `os.open(output_dir / f".{stem}.{pid}.tmp", O_WRONLY\|O_CREAT\|O_EXCL, 0o666)` | `:168`, `:170`; observed flags `0o301`, mode `0o666` | matches |
| 4. write all bytes (loop), `fsync`, `close` | `:165` encode before the temp exists; `:146-150` `_write_all` loops on a `memoryview` then `os.fsync`; `:175-179` `os.close` in `finally` | matches |
| 5. `os.link(tmp, output_dir / name)` over `stem.md`, `stem-2.md` to `stem-99.md`; `FileExistsError` goes to the next name; success is the commit point | `:182-196`; `published` set only after a successful link (`:195`) | matches |
| 6. no name left: unlink temp, exit 1 `[sweep publish] report name space exhausted: <dir>` | `:197-201` | matches |
| 7. after the commit point `os.unlink(tmp)`; failure gives exit 1 with no success JSON | `:202-207`, then `return published` at `:208`; `run` prints JSON only after `_publish` returns (`:275-278`) | matches |

Error-table rows (DESIGN 3.2, lines 121-129):

| Row | Code | Result |
|---|---|---|
| `makedirs` fails: `[sweep publish] <error>`, no file written | `:158-160` | matches |
| Temp name exists: `[sweep publish] temp file exists: <path>`, file left alone | `:171-172`, no unlink on that branch | matches |
| Write, fsync or close fails: unlink own temp, exit 1 | `:180-181` with `_drop_own_temp` | matches |
| `os.link` fails other than `FileExistsError`: unlink temp, `[sweep publish] cannot link report: <error>`, no fallback | `:191-194` | matches |
| Unlink fails on an exit-1 path: second stderr line naming the left temp | `:137-143` returns `[sweep publish] left temp file <path>`; both lines echoed at `:283-284` | matches |
| Unlink fails after commit: `[sweep publish] could not remove temp file <path>`, no JSON, report stays | `:202-207` | matches |
| Printing the success JSON fails: exit 1, report stays | `:276-278` inside the generic handler, `[sweep output] <error>` at `:286-288` | matches |

Exit-2 ordering: in `run.callback`, the AST call order is `_parse_window` (line 31 of the callback), `_check_root` (32), `_check_run_ids` (33), `_check_output` (36), `bind_run` (48), `collect` (51), `classify_all` (53), `render` (55), `_publish` (57), `to_json` (59). Every `click.UsageError(` raise in `commands.py` is at lines 50, 70, 83, 91, 107, 109 and 119, all inside `_parse_window`, `_find_root`, `_check_root`, `_check_run_ids` and `_check_output`. `probes.BindingError` is raised only at `probes.py:342-343` in `bind_run`. `sys.exit` appears only at `commands.py:281, 285, 288`, inside `run`. So no exit-2 check can run once `_publish` has started.

No rename, replace or overwrite: the write-verb grep over `src/superclaude/cli/sweep/*.py` finds `os.unlink`, `os.write`, `os.makedirs`, `os.open`, `os.link` only in `commands.py` (lines 140, 149, 158, 170, 186, 203). The only `open(` calls are `"rb"` reads in `probes.py` (559, 810, 874). The `.replace(` hits are `str`/`datetime` methods (`report.py:78, 576`, `probes.py:372, 703`, `classify.py:621`, `commands.py:248`). There is no `os.rename`, `os.replace`, `shutil`, `tempfile`, `O_TRUNC`, `write_text`, `write_bytes` or `Path.touch/mkdir` in the package.

## Dynamic evidence (scratch only, private `/tmp/pubqa.UjqyRHas`, removed `cases/` afterwards; no Orca command run)

Probe 1 calls `commands._publish` directly into temp folders: 31 checks, 0 failed. Probe 2 drives `sweep_group run` through `CliRunner` with `probes.collect`, `classify_all`, `render` and `to_json` stubbed (so no Orca or git was touched): 20 checks PASS plus 1 informational line (its last, source-order check crashed on a script error, `inspect.getsource(run)` on a click Command; I re-ran that check separately on `run.callback`, which gave the call order stated above). Probe 3 runs 24 publishes from 12 forked processes with the same `now`: 24 distinct names, 24 complete bodies, 0 temps left (`CONC_PASS`). What they showed:

- Event order for a normal publish is exactly `open, write, fsync, close, link, unlink`; `os.rename` and `os.replace` were armed to raise and never fired.
- Collisions give `stem.md`, `stem-2.md`, `stem-3.md`, `stem-4.md` with earlier bodies untouched. A pre-existing file, a directory named `stem-2.md`, a dangling symlink named `stem-3.md` and a file `stem-4.md` are all skipped and the new report lands at `stem-5.md`; the sentinel bytes and the symlink target are untouched.
- With `stem.md` and `stem-2.md` to `stem-99.md` all present: exit 1, exactly `[sweep publish] report name space exhausted: <dir>`, 99 files intact, no temp. With `-99` free it is used.
- A foreign file at the temp name, and a dangling symlink at the temp name, both give exactly `[sweep publish] temp file exists: <path>`; the foreign file is untouched and the symlink target is never created.
- Swapping the output folder for a symlink during `makedirs` gives `[sweep publish] output dir escaped <base>/` and nothing is written at the symlink target.
- Injected failures: `os.write` ENOSPC, `os.fsync` EIO, `os.close` EIO each leave no temp and no report; `os.link` EPERM gives `cannot link report: [Errno 1] Operation not permitted` and no temp; `os.link` EPERM plus `os.unlink` EACCES gives two stderr lines, the second `left temp file <path>`, the temp present; `os.unlink` EACCES after the commit gives `could not remove temp file <path>` with one complete report ending `Report complete` and the temp present.
- Short writes (7 bytes per `os.write`) still produce the full 55 KB body.
- Through the CLI: a bad `--window`, an `--output` outside `.dev/sweeps`, `--output .dev/tasks`, `--output .dev`, a bad `--run`, a bad `--root`, a symlinked `.dev/sweeps`, and a `BindingError` all exit 2 with empty stdout, an empty tree and none of collect/classify/render/publish called. A render error and an allowlist `ValueError` exit 1 with `[sweep render]` / `[sweep collect]` and nothing created, not even `.dev`. A `to_json` failure after the commit exits 1 with `[sweep output] ...`, empty stdout, and one complete report. A successful run prints exactly one JSON line whose `report_path` is the only file in the tree.
- Mode is `0o644` under umask 022 and `st_nlink` is 1 after the unlink.

## Artifact cross-checks

- `step-1.7-help.txt`: `--window` shows `[default: 6h]` and `--output` shows `Default: <root>/.dev/sweeps/.`, matching OQ-5 and OQ-2 and `commands.py:27, 237-241`. The only `6h`/`72h` literal in the package is `DEFAULT_WINDOW` (`commands.py:27`), as OQ-5 requires.
- `sweep-live-check-1.4.json`: key list ends with `report_path`; the path is `.dev/sweeps/20261112-031239-sweep.md`, whose stem equals `observed_at` 03:12:39Z (the stem uses the start time, as the design says). The file has 605 lines and ends `Report complete`, as `sweep-live-check-1.4.md` claims. `.dev/sweeps/` holds exactly three reports (031151, 031209, 031239) and no `.tmp` file, consistent with the three live runs the record describes. `git check-ignore -v` confirms `.gitignore:256 .dev/sweeps/`.
- `phase9-validation.md` records ruff check, ruff format, `sweep --help` and `pytest tests/sweep tests/unit` (726 passed, 2 skipped) as PASS. I re-ran `ruff check src/superclaude/cli/sweep` (clean), `ruff format --check` on `commands.py` and `main.py` (clean) and `pytest tests/sweep -q` (4 passed).
- `main.py` diff is four added lines: a deferred import with the same `noqa` comment as the `issue-watch` registration just above it, and `main.add_command(sweep_group, name="sweep")`. `__init__.py` imports `commands` lazily only on attribute access.

## Findings

| id | Severity | Evidence | What is wrong | Smallest fix |
|---|---|---|---|---|
| M1 | MINOR | `commands.py:142, 163, 172, 199, 207` | These stderr lines put a raw path into an f-string. `OSError` messages repr the filename, but these do not, and `_PublishError` lines are not passed through `sanitize` (which `_check_*` and the generic handler do use). In probe 2, an ANSI escape inside the `--output` folder name was removed by `click.echo` on a non-terminal, but other control characters (a newline, for example) would pass through unchecked. The design prints `<dir>` and `<path>` verbatim, so this is not a departure, and the path comes from the caller's own `--output`. | Optional: wrap the interpolated paths in `sanitize(...)` at those five sites. |
| M2 | MINOR | `commands.py:129-134, 156, 161-164` | `_publish` has no `root` parameter (signature fixed by DESIGN 7.1), so the escape check compares the re-resolved folder with the nearest ancestor of `output_dir` that is named `.dev/sweeps`, not with `<root>/.dev/sweeps`. For a folder like `<root>/.dev/sweeps/x/.dev/sweeps` the message names the inner folder, and the `base is None` branch prints `output_dir`. I could not construct a swap that escapes the real `<root>/.dev/sweeps` (any swap changes the resolved path away from the lexical base), so this is safe, only less literal than the design text. | None needed; if desired, add a one-line comment that `base` is derived from the already-checked path. |
| M3 | MINOR | `commands.py:161`, `:146-150` | `output_dir.resolve()` can raise `OSError`/`RuntimeError` (symlink loop) outside `_PublishError`; it reaches the generic handler and still exits 1 with `[sweep publish] <sanitized error>` and nothing written, so the outcome is right but the row is not in the design table. `_write_all` would loop forever if `os.write` ever returned 0 for a non-empty buffer, which does not happen on regular files. | None needed. |
| M4 | MINOR | `tests/sweep/` holds only `conftest.py`, `fixtures/` and `test_readonly.py` | No durable test pins `_publish` yet. DESIGN 12 maps FR-017 and FR-018 to `tests/sweep/test_cli_contract.py`, which task item 10.7 creates later (`TASK-...md:1825-1828`). My probes are scratch and were deleted. This is a scheduling note for the later gate, not a defect in the code under review. | Item 10.7 should include the cases listed under Dynamic evidence (collision names, 99 exhaustion, temp exists, escape, injected write/link/unlink failures, post-commit unlink failure). |

## Checks

| id | Check | Result |
|---|---|---|
| C1 | Stem format `%Y%m%d-%H%M%S` + `-sweep`, UTC, from the single `now` | PASS |
| C2 | makedirs then re-resolve and confirm under `.dev/sweeps`; escape message and nothing written | PASS |
| C3 | Temp name `.<stem>.<pid>.tmp`, `O_WRONLY\|O_CREAT\|O_EXCL`, mode `0o666` | PASS |
| C4 | Write loop, `fsync`, `close` in that order before any link; failure unlinks own temp | PASS |
| C5 | `os.link` over `stem.md`, then `stem-2.md` to `stem-99.md`; `FileExistsError` continues; other `OSError` gives `cannot link report` | PASS |
| C6 | Exhausted message byte-exact and own temp unlinked | PASS |
| C7 | Unlink after the commit point; failure message exact, no success JSON, report kept | PASS |
| C8 | Every row of the DESIGN 3.2 error table | PASS |
| C9 | Each stderr message byte-exact against the design text | PASS |
| C10 | No exit-2 check runs after `_publish` starts; exit 2 writes nothing | PASS |
| C11 | Nothing overwritten (file, directory, dangling symlink, foreign temp) | PASS |
| C12 | No rename, replace, truncate, shutil or other write verb anywhere in the package | PASS |
| C13 | Concurrent same-second runs get distinct complete reports and no temp remains | PASS |
| C14 | Exit-1 and exit-0 on-disk state matches DESIGN 3.4 (through the CLI) | PASS |
| C15 | `main.py` diff is registration only and follows the existing pattern | PASS |
| C16 | Help output matches OQ-2 and OQ-5 | PASS |
| C17 | Live-check artifacts agree with the code and with `.dev/sweeps/` on disk | PASS |
| C18 | ruff check, ruff format --check, `pytest tests/sweep` | PASS |
| C19 | Stderr path text is sanitized (extra, not required by the design) | PASS with note M1 |
| C20 | Durable tests exist for `_publish` (extra, scheduled for item 10.7) | PASS with note M4 |

## Confidence and tool engagement

Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Not covered by this lens and not claimed: report layout (7.5), classification rules, the skill text, and behaviour against live Orca (not run, as instructed).

Tool engagement (approximate counts): Read: 10 | Grep: 7 | Glob: 0 | Bash: 11 (including 3 scratch probes run with `uv run python -I`; all scratch files are under `/tmp/pubqa.UjqyRHas`, and the repository has no change from this review other than this report).

Verdict: PASS
Blocking count: 0

## QA Complete
