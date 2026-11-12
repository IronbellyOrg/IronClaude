# QA Report - Operator-output lens (impl-cli, item 9.11, agent 7 of 8)

**Topic:** `superclaude sweep run` operator-visible output (stdout, stderr, help text, report wording)
**Date:** 2026-11-12
**Phase:** task-qualitative (code gate, operator-output lens)
**Fix cycle:** N/A (review 1; `fix_authorization: false`, no file edited except this report)
**Inherited Structural Verdict:** none in the spawn prompt (standalone behavior; nothing relied on)

Lens: stdout holds exactly one JSON object on success and nothing on failure; every stderr line starts with `[sweep <stage>]`; the help text names every option with its default; no output recommends an action.

Method: I read `commands.py` (1-288), the `main.py` diff, `step-1.7-help.txt`, `phase9-validation.md`, the saved live-check JSON (parsed with `uv run python -I`, the file is one 312 KB line), `sweep-live-check-1.4.md`, the live report `.dev/sweeps/20261112-031239-sweep.md` (lines 1-30, 83-104, 289-301, 483-605), DESIGN (`artifacts/design-base.md` 82-155, 223-282, 351-445) and the OQ-2 and OQ-5 records. I also ran 15 scratch probes of the real CLI from a private `/tmp` folder with `ORCA_CLI_COMMAND=/nonexistent/orca-none` (so no Orca command ran; no live Orca was touched), plus `ruff check` and `pytest tests/sweep`.

---

## Overall Verdict: FAIL

One MAJOR finding (F1) and five MINOR findings (F2 to F6). F2 and F3 are lens departures that the approved SPEC/DESIGN text itself pins, so they need a coordinator ruling (change the code and the pinned text, or waive the lens wording); they are graded MINOR because the behaviour matches FR-018 and DESIGN 7.1 line 445.

## Findings

### F1 - MAJOR - the JSON says the session total is exact; the report from the same run says it is a lower bound

- Evidence, JSON: `artifacts/sweep-live-check-1.4.json` (parsed): `summary.total` 180, `summary.total_is_lower_bound` false. Code: `src/superclaude/cli/sweep/classify.py:967` and `:974-976` set the flag only from `inp.truncated`, Orca unavailable, an unscanned source or `bound_reached >= 1`. `report.py:670` copies it to the JSON.
- Evidence, report: `.dev/sweeps/20261112-031239-sweep.md:2` says `sessions 180/180 (lower bound: remote hosts not scanned)`; `:530` says `Remote hosts were not scanned; the session count is a lower bound`. `report.py:178` and `:510` print both unconditionally. The report's own coverage line `remote hosts | unknown` (`:83`) confirms remote hosts are never scanned in Phase 1.
- What is wrong: for one run, stdout says "not a lower bound" and the report says "lower bound". The skill reads only the summary counts and `report_path` from stdout, so a reader of stdout alone is told the count is exact. In Phase 1 the count is never exact. DESIGN 7.4/section 6 (`design-base.md:346`) defines the flag narrowly ("truncated or unscanned"), so the code follows the text, but the text leaves operator output self-contradicting.
- Smallest fix: make `total_is_lower_bound` true whenever the report prints the remote-hosts line (always, in Phase 1), or, if the narrow meaning is kept, drop the unconditional `(lower bound: ...)` wording from `report.py:178`/`:510`. Either way, state the flag's meaning in DESIGN 7.4. Not a coordinator-ruling item: one of the two outputs is wrong.

### F2 - MINOR - every exit-2 stderr line lacks the `[sweep <stage>]` prefix; click's own parse errors print up to four unprefixed lines

- Evidence: `commands.py:279-281` prints `exc.message` with no prefix for `click.UsageError` and `BindingError`. Probes (exit 2, stdout empty in all): `--window 7m` -> `invalid --window value: 7m (use <N>h or <N>d, at most 720h or 30d)`; `--root /nope` -> `invalid --root: ...`; `--run bad!` -> `invalid --run value: bad!`; `--output /tmp` -> `invalid --output: /tmp (must be ...)`; no `--run` and no Orca -> `Orca unavailable (binary not found: ...); no Run binding could be established: pass --run <id>`; `--foo` -> 4 lines (`Usage: ...`, `Try ...`, blank, `Error: No such option '--foo'...`); `--window` with no value -> `Error: Option '--window' requires an argument.`; extra positional -> 4 lines.
- Why only MINOR: SPEC FR-018 (`merged-requirements.md:112`, `:157`) and DESIGN 7.1 (`design-base.md:445`) put the `[sweep ...]` prefix on exit 1 only, and DESIGN 5 (`:237-238`) pins the exit-2 texts without a prefix. All exit-1 lines do carry it (C5).
- Smallest fix, if the lens wording stands: prefix the exit-2 echo with `[sweep args]` (and `[sweep bind]` for `BindingError`), and wrap click's parse errors with a `click.Command` subclass. This changes the DESIGN 5 pinned texts and the FR-002 tests, so it needs a ruling first.

### F3 - MINOR - two exit-2 messages tell the operator what to do

- Evidence: `commands.py:51` (`use <N>h or <N>d, ...`); `probes.py:342` (`no Run bound: pass --run <id>`) and `probes.py:343-346` (`... pass --run <id>`). Both texts are pinned by DESIGN 5 (`design-base.md:237-238`) and SPEC (`merged-requirements.md:434`).
- What is wrong against the lens: these are instructions to the operator. They are usage corrections, not advice about the swept Runs, worktrees or sessions, so the harm is small.
- Smallest fix: none needed if the lens is read as "no advice about swept state". If read literally, reword to facts (`valid values: <N>h or <N>d, at most 720h or 30d`; `no Run bound`), and update DESIGN 5 and its tests.

### F4 - MINOR - the `Next inspection` column tells the operator to read something, and its fallback text is wrong for the live data

- Evidence: `report.py:42-55` holds nine imperative strings (`read the ...`). In the live report all 180 Sessions rows end `read the sources in Source coverage that were not scanned` (`report.py:53`, the `fallback` rule). The same report's Source coverage table shows `Unscanned` = `none` for every source, and the saved JSON has 0 sources with an unscanned entry. The 175 transcript rows are `could not determine` because no tab-map join exists (`Notes` column), not because a source was unscanned.
- What is wrong: SPEC line 388 and DESIGN 7.5 (`design-base.md:634`) allow a read-only pointer, so the column itself is sanctioned. But the fallback sentence points at sources that do not exist in this run, on every row.
- Smallest fix: for the `fallback` rule, name what the row's own `Notes` says (the tab-map join), or use the `_NEXT_DEFAULT` text `read the row's evidence and the source it names` (`report.py:55`).

### F5 - MINOR - several stderr texts are printed raw, so a newline in an operator-supplied value splits a line and defeats the prefix rule

- Evidence: `commands.py:280` and `:284` echo `exc.message`/`lines` without `sanitize`; the raw f-strings are at `commands.py:160`, `:162-164`, `:172`, `:174`, `:181`, `:192`, `:199`, `:206` and `:142`; `probes.py:344` embeds the unsanitized `result.reason`. Only the generic handler (`commands.py:287`) and the argument messages (`:51`, `:70`, `:83`, `:91`, `:107-121`) call `sanitize`.
- Probe: `ORCA_CLI_COMMAND=$'/nonexistent/a\nFAKE LINE...'` with no `--run` -> exit 2, stdout 0 bytes, stderr printed as two lines (`Orca unavailable (binary not found: /nonexistent/a` then `FAKE LINEred); no Run binding ...`). click strips ANSI escapes only when stderr is not a terminal.
- Risk is low (the value comes from the operator's own environment or path), but the code treats the same class of value as unsafe in `:51` and `:83`.
- Smallest fix: pass `exc.message` and each `_PublishError` line through `sanitize` after the prefix, or sanitize the interpolated value (`{tmp}`, `{exc}`, `{result.reason}`) at the raise sites.

### F6 - MINOR - the group help truncates the command summary

- Evidence: `step-1.7-help.txt:13` and my probe of `superclaude sweep --help` both print `run  Collect, classify and publish one read-only report; print one JSON...` (click's 45-character summary cut). The full sentence is on `sweep run --help`.
- Smallest fix: shorten the docstring's first sentence (`commands.py:245`) to fit, for example `Publish one read-only report and print one JSON object.`

(no further findings)

## Probe record (scratch run, private `/tmp` folder, removed on exit)

`ORCA_CLI_COMMAND=/nonexistent/orca-none`, `XDG_STATE_HOME` in the private folder, fake root with an empty `.git` folder.

| Probe | Exit | stdout | stderr lines | All start `[sweep <stage>]` |
|---|---|---|---|---|
| `sweep --help`, `sweep run --help` | 0 | help text | 0 | n/a |
| `--window 7m`, `0h`, `٦h` | 2 | 0 bytes | 1 each | no |
| `--root <missing>`, `--run bad!`, `--run ""`, `--output /tmp` | 2 | 0 bytes | 1 each | no |
| `--foo`; extra positional | 2 | 0 bytes | 4 each (click text) | no |
| `--window` with no value | 2 | 0 bytes | 1 (click text) | no |
| no `--run`, Orca binary missing | 2 | 0 bytes | 1 | no |
| `--run run_aaaaaaaaaaaa` (Orca missing, report to private root) | 0 | one JSON object, 1 newline | 0 | n/a |
| same, but `<root>/.dev/sweeps` is a regular file | 1 | 0 bytes | 1: `[sweep publish] [Errno 17] File exists: '...'` | yes |

The success probe wrote exactly one file, `<root>/.dev/sweeps/20261112-032408-sweep.md`, and no temp file.

## Checks

| Check | What | Result |
|---|---|---|
| C1 | Success: stdout is exactly one JSON object (scratch probe: `json.loads` ok, one trailing newline, stderr empty) | PASS |
| C2 | Saved live stdout `sweep-live-check-1.4.json` is one object: 12 keys, `schema_version` 1, 1 newline, 319791 bytes | PASS |
| C3 | Exit 2: stdout empty (11 probes) | PASS |
| C4 | Exit 1: stdout empty (probe; `click.echo(payload)` is the last step before the end of `try`, `commands.py:276-278`) | PASS |
| C5 | Exit 1: every stderr line starts `[sweep <stage>]` (probe; `commands.py:142,160-206,287`) | PASS |
| C6 | Exit 2: every stderr line starts `[sweep <stage>]` | FAIL (F2, MINOR) |
| C7 | Every stderr message is one sanitized line | FAIL (F5, MINOR) |
| C8 | Help names every option with its default (`--run`, `--window` `[default: 6h]`, `--root`, `--output`, `--help`) | PASS |
| C9 | `sweep run --help` and `sweep --help` equal the recorded `step-1.7-help.txt` and the `phase9-validation.md` block | PASS |
| C10 | Group help shows the full command summary | FAIL (F6, MINOR) |
| C11 | Error text does not tell the operator what to do | FAIL (F3, MINOR) |
| C12 | Report and JSON advise no change to the swept state (no stop, retry, release, merge, remove, close advice; `Safe to close` and `Removable` are `no`/`could not determine` classifications) | PASS |
| C13 | `Next inspection` column is accurate and not an action | FAIL (F4, MINOR) |
| C14 | The JSON and the report of one run agree (total, lower bound, counts 180/180, 0 unscanned) | FAIL (F1, MAJOR) |
| C15 | Live-check record claims hold: exit 0 and empty stderr (my probe agrees), 180 of 180 rows `could not determine`, 0 unscanned, `bound_reached` 0, report 605 lines ending `Report complete` | PASS |
| C16 | OQ-2: default folder `<root>/.dev/sweeps/`, name `<YYYYMMDD-HHMMSS>-sweep.md` UTC, gitignored (`git check-ignore` -> `.gitignore:256:.dev/sweeps/`; `git status` shows none) | PASS |
| C17 | OQ-5: default `6h` (`commands.py:27`, help `[default: 6h]`, JSON `window` `6h`) | PASS |
| C18 | `main.py` diff is the lazy `add_command(sweep_group, name="sweep")` registration only (+4 lines); `superclaude --help` prints nothing extra on stderr | PASS |
| C19 | DESIGN 3.2 and 7.1 strings match the code: `output dir escaped`, `temp file exists`, `cannot link report`, `report name space exhausted`, `could not remove temp file`, second `left temp file` line, exit mapping 2/1/1 | PASS |
| C20 | `phase9-validation.md` reproduces: `ruff check` passes on `src/superclaude/cli/sweep`, `main.py`, `tests/sweep`; `pytest tests/sweep` 4 passed (I did not repeat the 285 s `tests/unit` run) | PASS |

## Summary

- Checks passed: 14 / 20
- Checks failed: 6 (C6, C7, C10, C11, C13, C14)
- Critical issues: 0; MAJOR: 1 (F1); MINOR: 5 (F2 to F6)

## Self-Audit

**(a) Reliance list:** none. The spawn prompt had no `## Inherited Structural Verdict`; I relied on no earlier QA report.

**(b) Independent checks that went beyond the producer's records:**
- The producer's live-check record says "stderr empty" and "five PASS lines"; I re-parsed the saved stdout and found `total_is_lower_bound` false against the report's two lower-bound sentences (F1).
- The record says every row has a class; I read the Sessions table and found the same fallback pointer on all 180 rows while `Unscanned` is `none` everywhere (F4).
- The producer captured help text only; I ran 15 CLI probes and found the unprefixed exit-2 lines and the click multi-line errors (F2) and the newline split (F5).

Limits: I did not run `sweep run` against live Orca (not allowed), so the 9 live Orca reads, the `run-current` success path and the paging lines are unchecked here; the tab-map join, sanitize of report cells and the JSON schema beyond key names are other lenses. Run-time stage labels `args`/`bind` stay set through the `SweepContext(...)` line (`commands.py:267`); it cannot fail today, so I did not raise it.

- **Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 25 | Grep: 15 | Glob: 3 | Bash: 9 (no web research; Tavily not used)

Verdict: FAIL
Blocking count: 1
