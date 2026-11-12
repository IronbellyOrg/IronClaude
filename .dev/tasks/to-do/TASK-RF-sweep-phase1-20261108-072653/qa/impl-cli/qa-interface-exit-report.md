# QA Report: Interface and exit-mapping lens (T199)

**Gate:** `qa/impl-cli/` (item 9.x CLI shell). **Date:** 2026-11-12. **Reviewer mode:** report-only, `fix_authorization: false`.
**Lens:** commands.py names and signatures vs DESIGN 7.1; options and defaults vs OQ-2 and OQ-5; exit mapping (UsageError and BindingError exit 2; ValueError, other exceptions and every `_publish` failure exit 1 with a `[sweep <stage>]` prefix; `sys.exit` only in `run`).

**Authority used.** DESIGN = `docs/designs/orchestrator-mode.md` (the revised copy; sections 3, 5 and 7.1 were diffed against `artifacts/design-base.md` and differ only in the 7.2-driven additions to `probes.py` signatures and one line in the section 5 diagram, none of which touch `commands.py`). SPEC = `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (FR-001 to FR-004, FR-017, FR-018, section 5.1 to 5.3). Deviation D3 (DESIGN 13, line 830) permits the `Orca unavailable (<reason>); ...` message.

## Method

Everything below was read from disk or run in a private scratch folder under `/tmp` (`uv run python -I`, `CliRunner`, `subprocess.run` and `Popen` replaced by a function that raises, `HOME` and `XDG_STATE_HOME` pointed into the scratch folder, `collect`, `classify_all`, `render` and `to_json` stubbed where a success or late-stage failure was needed). No Orca command was run and `superclaude sweep run` was never run against live Orca. Read-only repo commands run: `ruff check`, `ruff format --check`, `pytest tests/sweep`, `git diff -- src/superclaude/cli/main.py`, `git check-ignore`, greps.

## Findings

No BLOCKING and no MAJOR finding. Six MINOR findings (notes; they never fail the gate).

| ID | Severity | Evidence | What is wrong | Smallest fix |
|---|---|---|---|---|
| F-1 | MINOR | `commands.py:279-281` (`getattr(exc, "message", None) or str(exc)`), `commands.py:282-285` (`exc.lines`) against `commands.py:286-288` (`sanitize(exc)`); `probes.py:258-260` and `probes.py:342-346` build the `BindingError` text from `$ORCA_CLI_COMMAND` and `OSError` text; `commands.py:160-207` put OS error text and the output path into `_PublishError` lines | The exit-1 generic path and every `UsageError` message are sanitized, but the exit-2 `BindingError` message and all `_PublishError` stderr lines are printed raw. Scratch run: a `BindingError` whose text held an ESC sequence reached `click.echo` unchanged; only click's own non-tty ANSI stripping removed it (a tty would show it). The text comes from the operator's own environment and filesystem, so the risk is low | Apply `sanitize(...)` to the variable part only (not to the `[sweep publish]` prefix, because `sanitize` escapes `[` and `]`): `sanitize(exc)` at line 280, and sanitize the tail of each `_PublishError` line |
| F-2 | MINOR | `commands.py:5-6` ("`_publish` (the only function in the package that writes)"); `commands.py:146-150` (`_write_all`: `os.write`, `os.fsync`); `commands.py:137-143` (`_drop_own_temp`: `os.unlink`); task item 9.1 Action ("`_publish` is the only function that writes") | Two helpers outside `_publish` also write or unlink. Both are called only from `_publish` (`_write_all` at line 177; `_drop_own_temp` at lines 181, 193 and 200), so behaviour matches DESIGN 3.2, but the sentence is literally false and a static "one writer" test written to that sentence would fail | Reword the docstring to "the only publication path" (or inline the two helpers) |
| F-3 | MINOR | `commands.py:27-29,32,55,73,95,129,137,146` | Names not listed in DESIGN 7.1: `_PublishError`, `_check_root`, `_has_git`, `_within`, `_sweeps_base`, `_drop_own_temp`, `_write_all`, and the constants `DEFAULT_WINDOW`, `MAX_WINDOW_HOURS`, `MAX_SUFFIX`. All names that 7.1 does list exist with identical signatures (C1), so this is an addition, not a departure | Add the helpers to DESIGN 7.1 at the next design touch, or accept as private detail |
| F-4 | MINOR | `commands.py:70,107,110-111,121-122` pass `Path` objects to `sanitize`; DESIGN 7.1 (`docs/designs/orchestrator-mode.md:429`) types `sanitize(text: str)`; `report.py:547` implements `sanitize(text: object)` | Usage-error paths rely on `sanitize` accepting non-`str`. If `sanitize` were narrowed to the DESIGN type, a bad `--root` or `--output` would raise `TypeError` and exit 1 instead of 2 | `sanitize(str(path))` at those call sites, or change the DESIGN signature to `object` |
| F-5 | MINOR | `commands.py:105` (`(output if output is not None else base).resolve()`); scratch: `--output relative-outside` exit 2 | A relative `--output` is resolved against the current folder, not against `--root`. `--root X --output .dev/sweeps/y` run from another folder exits 2. It fails closed and DESIGN is silent, but the `--output` help text ("`<root>/.dev/sweeps/` or below") suggests root-relative | Document it in the help text, or join a relative value to the checkout before resolving |
| F-6 | MINOR | `src/superclaude/cli/sweep/__init__.py:4` (`def __getattr__(name: str):`) against DESIGN 7.1 `docs/designs/orchestrator-mode.md:360` (`-> object`) | The return annotation from the DESIGN signature is missing. Outside `commands.py`; recorded because the registration depends on it | Add `-> object` |

Notes that are not findings: (N1) `--root ""` is accepted as the current folder (`Path("")` is `.`; scratch reached `collect`), which satisfies the FR-004 wording "existing directory that holds `.git`"; (N2) the validation order in `run` is window, root, run ids, output, whereas the section 5 diagram lists window, root, output, run ids; no SPEC or DESIGN text makes the order observable; (N3) `sweep run --help` in `step-1.7-help.txt` wraps at a different width than my 80-column `CliRunner` run; the words are identical, so this is terminal width only; (N4) `tests/sweep/` holds only `test_readonly.py` (4 tests pass); `test_cli_contract.py` and `test_cli_registration.py` (DESIGN 11) do not exist yet, so exit mapping has no automated test at this gate and my scratch runs are the only evidence.

## Check evidence

| Check | What I did | Result seen |
|---|---|---|
| C1 | `inspect.signature` on `C.run.callback`, `_parse_window`, `_find_root`, `_check_output`, `_check_run_ids`, `_publish`, compared to DESIGN 7.1 lines 434-443 | All identical: `run(run_ids: tuple[str, ...], window: str, root: str \| None, output: str \| None) -> None`; `_parse_window(text: str) -> timedelta`; `_find_root(start: Path) -> Path`; `_check_output(output: Path \| None, root: Path, inputs: tuple[Path, ...]) -> Path`; `_check_run_ids(values: tuple[str, ...]) -> tuple[str, ...]`; `_publish(text: str, output_dir: Path, now: datetime) -> Path` |
| C2 | `type(C.sweep_group)`, `.name`, `.commands` | `Group`, `sweep`, `['run']` |
| C3 | `C.run.params` | `--run` (multiple, dest `run_ids`), `--window`, `--root`, `--output`; matches SPEC FR-001 |
| C4 | `params` defaults, `_check_output(None, ...)`, help artifact | `--window` default `6h` with `show_default`; `--root` and `--output` default `None`; `None` output resolves to `<root>/.dev/sweeps`; matches OQ-5 record line 34 and OQ-2 record line 34 |
| C5 | `grep -rnE "6h\|hours=6\|timedelta\(\|DEFAULT_WINDOW\|MAX_WINDOW" src/superclaude/cli/sweep` | Only `commands.py:27-28,48-49,228`; `DEFAULT_WINDOW = "6h"` is the one default, `MAX_WINDOW_HOURS = 720` is the FR-003 cap, no window constant in `classify.py`, `report.py`, `probes.py` or `models.py`; `SweepContext(now, window, window_start, root, runs)` at `models.py:56-61` carries the value (OQ-5 "no additional window constant") |
| C6 | Success scratch run with frozen `now` 2026-11-12 03:00:00 UTC; `git check-ignore -v .dev/sweeps/x.md` | Report `.dev/sweeps/20261112-030000-sweep.md`; `.gitignore:256:.dev/sweeps/` ignores it (OQ-2) |
| C7 | `_parse_window` direct and through `run` | Accepted: `6h`, `3d`, `720h`, `30d`, `1h`, `1d`. Exit 2: `0h`, `6`, `6m`, `-1h`, `721h`, `31d`, `999999999d`, Arabic-Indic `٦h`, `6h\n`, `06h`, empty, `1H`, `9999d` (FR-003 list plus extras) |
| C8 | `--root` missing/file/no-`.git`; walk from a folder with no `.git` above; `--output` `/tmp/x`, `<root>/.dev`, `<root>/.dev/tasks`, `<root>/.dev/other`, `<root>/.dev/sweeps/../tasks`, relative outside, symlinked `.dev/sweeps`; accepted `<root>/.dev/sweeps/archive`; `_check_output` overlap both directions | All exit 2, stdout empty, tree under the root still only `.git`; messages `invalid --root: <path>`, `no git checkout found above <cwd>`, `invalid --output: ...` match SPEC FR-004; overlap branch raises in both directions (FR-004) |
| C9 | `--run` `""`, `r;x`, `BAD`, `run_ABCDEF012345`, 11 and 13 hex digits; `_check_run_ids((A, B, A))` | Exit 2 `invalid --run value: <sanitized>` for each (FR-002); duplicates collapse first-seen: `('run_000000000000', 'run_111111111111')` |
| C10 | All C7-C9 cases | Exit 2, stdout empty, message on stderr with no `Usage:` wrapper; click's own errors (`--bogus`, `--window` without value) also exit 2 |
| C11 | `probes.bind_run` stubbed to raise `BindingError` | Exit 2 with `no Run bound: pass --run <id>`; with `Orca unavailable (<reason>); no Run binding could be established: pass --run <id>` (DESIGN D3); stdout empty; nothing written |
| C12 | `probes.collect` stubbed to raise `ValueError("orca arguments are not allowed: ('x',)")`; `probes.bind_run` stubbed to raise `ValueError` | Exit 1, `[sweep collect] orca arguments are not allowed: ('x',)` and `[sweep bind] orca arguments are not allowed: bind`; stdout empty; no report |
| C13 | `classify_all` raises `RuntimeError`, `render` raises `KeyError`, `to_json` raises `OSError` | Exit 1 with `[sweep classify]`, `[sweep render]`, `[sweep output]`; the first two leave nothing on disk |
| C14 | Eight `_publish` failure modes: `makedirs` under a file; foreign temp name exists; `os.link` raises `EPERM`; `os.link` `EPERM` plus `os.unlink` fails; link ok then `os.unlink` fails; `os.write` `ENOSPC`; `UnicodeEncodeError` (lone surrogate); 99 names taken | All exit 1, stdout empty, every stderr line starts `[sweep publish]`; messages match DESIGN 3.2 table (`temp file exists:`, `cannot link report:`, `could not remove temp file`, `report name space exhausted:`); foreign temp file untouched; no temp left except where the unlink was forced to fail (then the extra `left temp file` line appears) |
| C15 | `grep -rn "sys.exit\|SystemExit\|click.exceptions\|ctx.exit\|click.Abort" src/superclaude/cli/sweep` | Only `commands.py:281,285,288`, all inside `run`'s `except` clauses |
| C16 | Success scratch run twice in the same frozen second | Exit 0, stdout one JSON line, stderr empty, `report_path` absolute and existing, one file; second run adds `-2.md`; no temp file left |
| C17 | Tree listing after every exit-2 case; after pre-commit exit-1 cases | Exit 2: nothing written. Exit 1 before the link: no `*.md` report name (DESIGN 3.4) |
| C18 | `to_json` raising (stage `output`); link ok then `unlink` fails | Exit 1, no JSON on stdout, the complete report name stays (DESIGN 3.4, post-commit rule) |
| C19 | `git diff -- src/superclaude/cli/main.py`; `main.commands["sweep"] is C.sweep_group`; `superclaude --help` | 4 insertions, 0 deletions after the `issue-watch` pair, comment text identical to its neighbours; registered; top help lists `sweep` |
| C20 | `CliRunner` on `sweep --help` and `sweep run --help` vs `step-1.7-help.txt`; `ruff check src/superclaude/cli tests/sweep`; `ruff format --check` on the sweep folder, `main.py`, `tests/sweep` | Group help byte-identical; run help identical except for terminal-width wrapping; ruff both clean (`All checks passed!`, `11 files already formatted`) |
| C21 | Re-ran `pytest tests/sweep -q`; compared with `phase9-validation.md` | 4 passed, matching the file; ruff lines match. The `tests/unit` line (726 passed, 285 s) was not re-run (out of lens) |
| C22 | Loaded `sweep-live-check-1.4.json` and `-workers.json` with `python -I`; `wc -l`/`tail` on the saved report; `grep -n '"worker-list"' probes.py` | JSON has all 12 top-level keys, `window` `6h`, `report_path` absolute under `.dev/sweeps/`, 71 sources, 0 unscanned, 180 rows all `could not determine`; workers file holds 5 workers with `page.total` 5, `hasMore` false; report 605 lines ending `Report complete`; `probes.py:49` holds the `worker-list` template. Consistent with the exit-0 contract |
| C23 | Compare how each exit path formats stderr | Exit-2 `BindingError` text and `_PublishError` lines are not sanitized, unlike the other paths (F-1, MINOR only) |
| C24 | Compare the `commands.py` name set and docstrings with DESIGN 7.1 and task item 9.1 | Listed names exact; extra private names and an inexact "only function that writes" sentence (F-2, F-3, F-4, MINOR only) |

## Checks

| Check | Result |
|---|---|
| C1 | PASS |
| C2 | PASS |
| C3 | PASS |
| C4 | PASS |
| C5 | PASS |
| C6 | PASS |
| C7 | PASS |
| C8 | PASS |
| C9 | PASS |
| C10 | PASS |
| C11 | PASS |
| C12 | PASS |
| C13 | PASS |
| C14 | PASS |
| C15 | PASS |
| C16 | PASS |
| C17 | PASS |
| C18 | PASS |
| C19 | PASS |
| C20 | PASS |
| C21 | PASS |
| C22 | PASS |
| C23 | FAIL (MINOR only: F-1) |
| C24 | FAIL (MINOR only: F-2, F-3, F-4) |

## Confidence and tool engagement

- **Confidence:** Verified: 24/24 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Limits: the `tests/unit` run in `phase9-validation.md` and the live Orca data behind the live-check artifacts were not re-run (no live Orca allowed); I checked only that the saved artifacts are internally consistent with `commands.py` behaviour. Failure modes in section C14 were produced by patching `os` calls inside `commands`, not by a real full disk or a filesystem without hard links.
- **Tool engagement:** Read: 22 | Grep: 8 | Glob: 1 | Bash: 13 (counts are from my own tool log, rounded to whole calls). Web research: none.

Verdict: PASS

Blocking count: 0
