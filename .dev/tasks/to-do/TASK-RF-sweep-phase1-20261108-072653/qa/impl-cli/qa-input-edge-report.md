# QA Report: input-edge lens, `superclaude sweep run` (commands.py, main.py registration)

**Date:** 2026-11-12
**Reviewer:** rf-qa-qualitative (report only, fix_authorization false)
**Method:** read `commands.py` (288 lines) in two chunks, the `main.py` diff, the probes/classify code that the edge cases reach, DESIGN 3.2, 3.4, 5, 7.1, 13, 17 and SPEC FR-002 to FR-004; then drove `sweep_group` through click's `CliRunner` in a private /tmp folder (fake HOME and XDG_STATE_HOME, `subprocess.run`, `Popen` and `os.system` patched to raise, `probes.collect` / `probes._orca` / `probes._git` faked). No live Orca command was run and `superclaude sweep run` was never run against live Orca. The scratch folder was removed afterwards.

DESIGN means `docs/designs/orchestrator-mode.md`. SPEC means `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (FR-002 line 96, FR-003 line 97, FR-004 line 98).

## Inputs read

- `src/superclaude/cli/sweep/commands.py` lines 1-288 (all)
- `git diff -- src/superclaude/cli/main.py` (4 added lines, deferred import and `main.add_command(sweep_group, name="sweep")`)
- `probes.py` 84-103, 200-346, 930-1100, 1100-1250 (the paths a Run id and an unknown Run reach); `classify.py` 670-740; `report.py` 520-590 (`sanitize`)
- `step-1.7-help.txt`, `phase9-validation.md`, `sweep-live-check-1.4.md`, head of `sweep-live-check-1.4.json` and `-workers.json`
- OQ-2, OQ-5 and OQ-8 records (all `status: RESOLVED`)
- `uv run superclaude sweep run --help` re-run read-only and diffed against `step-1.7-help.txt` lines 19-31: identical.

## Case-by-case results (what the code does)

### Run ids (FR-002; `_check_run_ids`, commands.py:87-92; `RUN_ID_RE = r"run_[0-9a-f]{12}"`, probes.py:44)

| Case | Result observed | Matches SPEC/DESIGN |
|---|---|---|
| `--run ''` | exit 2, stderr `invalid --run value: `, nothing written, no `_orca` call | yes |
| `--run 'r;x'` | exit 2, `invalid --run value: r;x`, nothing written | yes |
| duplicate `--run A --run A` | collapsed to one id; `--run B --run A --run B` gives `(B, A)`, first-seen order | yes |
| `run_...\n`, uppercase hex, 11 or 13 hex digits, fullwidth and Arabic-Indic digits, ESC sequence | all exit 2 (fullmatch, explicit `[0-9a-f]`); the ESC sequence is stripped from the echo | yes |
| one valid then one invalid id | exit 2 before any Orca call, nothing written | yes |
| no `--run`, `run-current` unavailable | exit 2, `Orca unavailable (runtime_unavailable); no Run binding could be established: pass --run <id>`, exactly one `_orca` argv, no report, no JSON | yes, with recorded deviation D3 (DESIGN line 830) |
| no `--run`, no binding | exit 2, `no Run bound: pass --run <id>`, one argv, nothing written | yes |
| unknown Run, live shape (`worker-list` exit 0 and empty, `task-list` fails: the shape captured in step 1.0a, `tests/sweep/fixtures/SOURCES.md:30-31`) | exit 0, report published; `worker-list` is `read`, both `task-list` rows are `unscanned: orca call failed (exit 1)`; a later good Run is still read (7 argv) | matches DESIGN 5 line 245 and 17 item 4; differs from SPEC wording (see F1) |
| unknown Run with a hypothetical nonzero `worker-list` on call one | `_call` (probes.py:330-332) turns the first-call failure into `unavailable`: only 1 argv is issued, the later Run is never read, report carries the Orca-unavailable banner, exit 0 | differs from SPEC FR-002 (see F1) |
| explicit `--run`, first call unavailable | one argv, report published, exit 0 | yes (SPEC test 2) |

### Window (FR-003; `_parse_window`, commands.py:43-52)

Accepted: `6h`, `3d`, `720h`, `30d`, `1h`, `1d`. Rejected with exit 2 and nothing written: `0h`, `6`, `6m`, `-1h`, `721h`, `31d`, `999999999d`, `٦h`, empty, `6h\n`, ` 6h`, `06h`, `9999h`, `10000h`, `720H`, `6 h`, `+6h`, `1e1h`. Every SPEC FR-003 example behaves as stated. The default is `6h` (commands.py:27), consistent with OQ-5 (`Chosen: 6h`) and the help text `[default: 6h]`.

### Root (FR-004; `_find_root` 64-70, `_check_root` 73-84)

| Case | Result | Matches |
|---|---|---|
| default root, cwd two levels below a `.git` folder | walks up, root found, no subprocess (patched to raise) | yes |
| default root, `.git` is a file (linked worktree) | accepted | yes |
| default root, no `.git` above | exit 2, `no git checkout found above <cwd>` | yes |
| explicit root with `.git` folder or file | accepted | yes |
| explicit root: subfolder without `.git`, a file, missing path, folder without `.git`, symlink loop | exit 2, `invalid --root: <path>` | yes |
| explicit root via symlink | resolved to the real path and used | yes |
| `--root ''` | `Path('')` is `.`, so it is accepted when cwd holds `.git` and gives exit 2 otherwise | not specified (see F3) |
| default root, cwd deleted | `Path.cwd()` raises, falls to the generic handler: exit 1 `[sweep args] ...` | not specified (see F2) |

### Output (FR-004; `_check_output` 99-123, `_publish` 153-208)

Accepted: default, `<root>/.dev/sweeps`, `<root>/.dev/sweeps/archive`, `.../archive/../archive2`, a nested `.../sweeps/.dev/sweeps`, a relative path that resolves below the base from cwd, and a symlink whose target is inside the base (the report lands at the real path). Rejected with exit 2 and no new file or folder: `<root>/.dev`, `<root>/.dev/tasks`, a package folder under `.dev/tasks/to-do/`, `<root>/.dev/other`, a path outside the root, `../..` escapes, the sibling `sweeps-evil`, a symlink inside `sweeps/` that leads outside (both the link and a path below it), `.dev` replaced by a symlink to elsewhere (default and explicit output), and a root placed under `~/.claude/projects` (the overlap guard fires). All SPEC FR-004 examples hold. An output path below a regular file gives exit 1 `[sweep publish] [Errno 20]` (makedirs failure, DESIGN 3.2 table row 1).

Escape after makedirs: when the output folder is swapped for a symlink to outside after `makedirs`, `_publish` exits 1 with `[sweep publish] output dir escaped <root>/.dev/sweeps/`, nothing is written outside, no report or temp file is created (matches DESIGN 3.2 step 2). When the swap happens between `_check_output` and `makedirs` (the base folder replaced by a symlink), `makedirs` first creates the leaf folder outside the base; the later check then exits 1 with the same message but the new folder stays outside `.dev/sweeps/` (see F4).

## Findings

No BLOCKING and no MAJOR finding. Six MINOR findings; none fails the gate.

### F1 (MINOR): an unknown Run never produces the SPEC reason `orca call failed (unknown run)`

- Evidence: SPEC line 96 (FR-002) says a nonzero `worker-list` whose stderr matches the unknown-Run shape is `call_failed` with reason `orca call failed (unknown run)` and later Runs are still read. `grep -i "unknown run"` over `src/superclaude/cli/sweep/` finds no detection code; `_orca` gives `orca call failed (exit N)` (probes.py:274-277) and `_call` turns any `call_failed` on the very first Orca call into `unavailable` (probes.py:330-332). Observed: with a faked nonzero `worker-list` for the first of two Runs, one argv is issued, the second Run is never read and the report carries the Orca-unavailable banner (exit 0).
- Why it is only MINOR: the captured shape (step 1.0a item 8, `tests/sweep/fixtures/SOURCES.md:30-31`) is `worker-list` exit 0 with an empty list and `task-list` exit 1 `run_not_found`. With that shape the code does what DESIGN 5 line 245 and 17 item 4 (line 994) say: the Run is read, `task-list` rows are `unscanned`, and the Run is flagged `origin unknown: Run not confirmed` (classify.py:682-708). A well-formed but mistyped id therefore gives exit 0 and a published report, with no stderr hint.
- Gap: DESIGN section 13 (D1 to D10) has no row recording that the SPEC reason string is dropped.
- Smallest fix: add one deviation row to DESIGN 13 (or a note under SPEC FR-002) stating that the `(unknown run)` reason is not produced because the captured shape is exit 0 with an empty list. No code change.

### F2 (MINOR): two walk-up failures end as exit 1, not as the exit 2 usage error

- Evidence: `_find_root` calls `start.resolve()` outside any `try` (commands.py:66) and `_check_root` calls `Path.cwd()` outside any `try` (commands.py:75). A deleted current folder was run: exit 1, stderr `[sweep args] \[Errno 2\] No such file or directory`. On Python 3.11 (the interpreter used here) a symlink loop in `resolve()` raises `RuntimeError`, which takes the same path. SPEC FR-004 maps "a walk from a directory with no `.git` above it" to exit 2 `no git checkout found above <cwd>`.
- Smallest fix: wrap the `Path.cwd()` and `resolve()` calls in `try/except (OSError, RuntimeError)` and raise `click.UsageError("no git checkout found above ...")`.

### F3 (MINOR): empty `--root` and `--output` mean "the current folder"; a relative `--output` is read against cwd

- Evidence: `Path('')` is `.`, so `--root ''` resolves to cwd and is accepted when cwd holds `.git` (observed exit 0); `--output ''` resolves to cwd (observed exit 2 from the checkout root, but it would be accepted from inside `<root>/.dev/sweeps/`). Compare `--run ''`, which FR-002 rejects. commands.py:76 and commands.py:105. A relative `--output .dev/sweeps/rel2` with `--root <R>` from another folder gave exit 2, because it is resolved against cwd, not against `--root`; the help text (`Report folder, <root>/.dev/sweeps/ or below`) can be read as root-relative. SPEC FR-004 is silent on both.
- Smallest fix: reject an empty string for `--root` and `--output` with the existing `invalid --root:` / `invalid --output:` messages, and state in the `--output` help or in DESIGN 7.1 that a relative path is taken from the current folder.

### F4 (MINOR): `makedirs` runs before the escape check, so a race can leave a folder outside `.dev/sweeps/`

- Evidence: commands.py:158 (`os.makedirs`) precedes commands.py:161-164 (resolve and compare), the same order as DESIGN 3.2 step 2 (line 106). With the sweeps folder swapped for a symlink between `_check_output` and `makedirs` (faked in the scratch run), the run exits 1 with `[sweep publish] output dir escaped ...` as designed, but the new folder `q` was created outside `.dev/sweeps/` (observed under the scratch "outside" folder). DESIGN 3.4 (line 153) says leftovers are only "under `<root>/.dev/sweeps/`". No report or temp file is written outside in either race variant (swapping only the leaf after `makedirs` leaves nothing outside).
- Needs a same-user race against a check-to-use gap of milliseconds, so MINOR.
- Smallest fix: soften the DESIGN 3.4 sentence to name this race, or create the folders one level at a time with a re-check after each (not worth it for Phase 1).

### F5 (MINOR): SPEC acceptance literals cannot be run, and the command layer has no tests yet

- Evidence: SPEC line 96 uses `--run R1`, `--run BAD` and `--run R2`; under `RUN_ID_RE` (probes.py:44) each exits 2 (observed for `R1` and `BAD`). DESIGN 7.1 line 443 says the regex comes from step 1.0a, and the OQ-8 Run ids are all `run_` plus 12 lowercase hex digits, so the implementation is right and the SPEC literals are placeholders. `tests/sweep/` holds only `conftest.py` and `test_readonly.py`, and a search for `CliRunner`, `_check_run_ids`, `_parse_window`, `_check_output` and `_find_root` under `tests/sweep` finds nothing; `tests/**/test_sweep*.py` matches no file. The Phase 9 line `726 passed, 2 skipped` therefore says nothing about the cases above. The task file names `tests/commands/test_sweep_command.py` as a later deliverable (task file line 89 and 134), so this is a gap to close there, not a defect in this item.
- Smallest fix: when the command tests are written, use well-formed ids (`run_aaaaaaaaaaaa`) for the FR-002 cases and note in the test file that the SPEC `R1/R2/BAD` literals stand for well-formed ids.

### F6 (MINOR): rejected values are echoed to stderr without a length limit

- Evidence: `sanitize` has no length cut (report.py:547-577) and the three echoes use it directly (commands.py:51, 83, 91); only `report.cell` cuts, at 200 characters, for table cells. A very long `--run`, `--window` or `--root` value is printed whole. Read from the code; a multi-megabyte value was not run.
- Smallest fix: echo `cell(value)` (200 characters) instead of `sanitize(value)` in the three messages.

## Checks

| id | Check | Result |
|---|---|---|
| C1 | `--run ''` exits 2 with `invalid --run value:` and writes nothing | PASS |
| C2 | `--run 'r;x'` exits 2, nothing written, no Orca call | PASS |
| C3 | Duplicate `--run` collapses, first-seen order kept | PASS |
| C4 | Run id regex is ASCII-only and full-match (newline, case, length, Unicode digits, ESC) | PASS |
| C5 | Run id and window checks run before any `_orca` call (order window, root, run ids, output, bind) | PASS |
| C6 | Unknown Run, captured live shape: read, `task-list` unscanned, exit 0, later Runs still read (DESIGN 5 line 245) | PASS |
| C7 | Unknown Run, SPEC FR-002 nonzero shape and reason `orca call failed (unknown run)` | FAIL (MINOR, F1) |
| C8 | No `--run`: unavailable, no-binding and success paths match FR-002 tests 1 and 4 (with D3 wording) | PASS |
| C9 | Explicit `--run` with first-call failure publishes and exits 0 (FR-002 test 2) | PASS |
| C10 | FR-003 window forms: all accept and reject examples, default `6h` (OQ-5) | PASS |
| C11 | Root found by walking up: `.git` folder and file, no `_git` call, no-`.git` message | PASS |
| C12 | Root walk failure modes (deleted cwd, symlink loop) map to exit 2 | FAIL (MINOR, F2) |
| C13 | Root given: missing, file, no `.git`, loop, symlink all handled; message `invalid --root:` | PASS |
| C14 | Empty `--root` / `--output` and relative `--output` behave as FR-004 reads | FAIL (MINOR, F3) |
| C15 | Output inside `<root>/.dev/sweeps/` accepted (default, archive, `..` that stays inside, nested, inside-symlink) | PASS |
| C16 | Output outside, `.dev`, `.dev/tasks`, package folder, `.dev/other`, `sweeps-evil`, `..` escape, escaping symlink, symlinked `.dev` or `sweeps` all exit 2 and write nothing | PASS |
| C17 | Overlap with input folders rejected (root under `~/.claude/projects`) | PASS |
| C18 | Escape found after `makedirs` exits 1 with the DESIGN message and writes no report or temp file outside | PASS |
| C19 | A race before `makedirs` leaves nothing outside `.dev/sweeps/` (DESIGN 3.4) | FAIL (MINOR, F4) |
| C20 | Exit-2 paths create no file or folder (`NEW` empty in every exit-2 run) | PASS |
| C21 | Report name `<YYYYMMDD-HHMMSS>-sweep.md` in UTC with `-2`, `-3` suffixes on same-second reruns (OQ-2, FR-017) | PASS |
| C22 | `main.py` diff matches the deferred-registration pattern; `sweep --help` and `sweep run --help` match `step-1.7-help.txt` | PASS |
| C23 | Live-check record (`window` `6h`, report under `.dev/sweeps/`, run id from OQ-8, one JSON object) consistent with the code | PASS |
| C24 | SPEC FR-002 literals (`R1`, `BAD`) are runnable against the implemented regex; command-layer tests exist | FAIL (MINOR, F5) |
| C25 | Rejected-value echoes are bounded | FAIL (MINOR, F6) |

## Self-audit

- Tool engagement: Read 12, Grep 9, Glob 1, Bash 11 (five scratch harness runs, one help re-run and diff, file listings, cleanup).
- Claims independently verified by running code: every row in the case tables above that reports an exit code, stderr text or file listing came from the scratch runs, not from the producer's records. Items taken from reading only: F2 symlink-loop on 3.11, F6 length behaviour.
- The producer's records (`phase9-validation.md`, `sweep-live-check-1.4.md`) were used only for consistency checks (C22, C23); the help-output record was re-run and matched.
- One of my own scratch runs mis-built a race (it patched `os.makedirs` globally and recursed); I discarded it and re-ran the race cleanly before relying on C18 and F4.

Verdict: PASS
Blocking count: 0
