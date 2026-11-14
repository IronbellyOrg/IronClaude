# QA Report - impl-cli gate, read-only safety lens (T201)

**Topic:** `superclaude sweep run` CLI shell (`src/superclaude/cli/sweep/commands.py`, `main.py` registration, step 1.4 live check)
**Date:** 2026-11-12
**Phase:** code gate, rf-qa read-only and allowlist safety domain lens
**Fix cycle:** N/A (`fix_authorization: false`, nothing edited except this report)

## Overall Verdict: PASS (no BLOCKING and no MAJOR finding; 5 MINOR notes)

Scope of the lens: prove that `_publish` is the only write, that it writes only under `<root>/.dev/sweeps/`, that the CLI adds no Orca or git call outside the `probes` seams, that there is no `run-list` fallback, and that the live check used only the `worker-list` template and the sweep run command. All five were proved from the files and from scratch runs. The scratch runs used a fake Orca binary and throwaway git repos under a private `/tmp` folder (removed afterwards). No live Orca command was run and `superclaude sweep run` was never pointed at live Orca by me.

## Checks

A check is marked FAIL only when it has a BLOCKING or MAJOR finding. Checks that carry only MINOR notes are PASS, with the note id in the Evidence column.

| Check | Result | Evidence (short; detail below) |
|---|---|---|
| C1 `_publish` is the only write in the package | PASS | grep of every write/process/env call across `sweep/`; see C1 below |
| C2 `_publish` writes only under `<root>/.dev/sweeps/` on the CLI path | PASS | `_check_output` matrix and full-run snapshot; MINOR notes F1, F2 |
| C3 `_check_output` containment and input-overlap rejection | PASS | 12 hostile `--output` cases, all rejected or accepted correctly |
| C4 every exit-2 path writes nothing | PASS | usage errors and no-binding run; tree snapshot unchanged |
| C5 a successful run leaves exactly one report, no temp file, and touches nothing else | PASS | snapshot diff of a full run with 2 stat-dirty git worktrees |
| C6 report names are never overwritten | PASS | two same-second `_publish` calls gave `-sweep.md` and `-sweep-2.md` |
| C7 only `probes.py` starts a process; no shell | PASS | 2 `subprocess.run` sites, list argv, no `shell=` |
| C8 the CLI adds no Orca or git call outside the `probes` seams | PASS | `commands.py` touches only `probes.Budget/bind_run/collect/RUN_ID_RE/BindingError` |
| C9 Orca allowlist: 10 templates, 7 verbs, token-exact, `--include-remote` rejected | PASS | 17 hostile argvs all raise `ValueError` |
| C10 git allowlist: one exact argv, lock-free prefix and env | PASS | `check_git_args` probe; `probes.py:296-297`; MINOR note F3 |
| C11 no `run-list` call and no fallback | PASS | grep zero hits; template absent; no-binding run issues only `run-current`, exits 2 |
| C12 disk and tab-map readers are read-only | PASS | three `open(..., "rb")`, `scandir`, `stat`, `read_text`, `read_bytes` only |
| C13 the live check used only the `worker-list` template and the sweep run command | PASS | record, saved JSON and OQ-8 agree; MINOR note F4 |
| C14 `main.py` diff is the registration only | PASS | 4 inserted lines, no deletions |
| C15 recorded help output equals live help output | PASS | `diff` of both `--help` outputs, no difference |
| C16 OQ-2 and OQ-5 decisions are honored | PASS | default folder, file name pattern, `6h` default, `.gitignore:256` |
| C17 repo hygiene for the gate: ruff, `tests/sweep`, no stray modified files from the CLI | PASS | ruff clean, 4 passed; MINOR note F5 on test coverage at this point |

## Findings

No BLOCKING finding. No MAJOR finding.

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `src/superclaude/cli/sweep/commands.py:158` (`os.makedirs`) runs before the escape re-check at `commands.py:161` | `_publish` creates the output folder first and verifies afterwards. Called directly with a folder outside any `.dev/sweeps`, it creates that folder, then raises `output dir escaped` (scratch run: `.../evil/dir` existed after the error). On the CLI path `_check_output` has already resolved and checked the folder, so only a race (a path part swapped for a symlink between the check and `makedirs`) could create an empty folder outside the tree. It follows DESIGN 3.2 step 2 order, but DESIGN 3.2 says an escape "writes nothing" and 3.4 limits leftover folders to ones "under `<root>/.dev/sweeps/`". | Do the `_within(output_dir.resolve(), base)` check once before `makedirs` (non-strict `resolve()` works on missing paths) and keep the second check after it; or reword DESIGN 3.2 step 2 to say an empty folder may remain. |
| F2 | MINOR | `commands.py:129-134` (`_sweeps_base`), `commands.py:161` | `_publish` finds its base from the output path's own ancestors (the nearest folder named `sweeps` under `.dev`), because its design signature has no root. Its guard therefore confirms "no symlink escape below a `.dev/sweeps`", not "inside this run's `<root>/.dev/sweeps`". Containment rests on `_check_output` alone. Already recorded as choice (5) in `### Phase 9 Findings` (task file line 2972). | None needed for Phase 1; if wanted, pass `root` into `_publish`. |
| F3 | MINOR | `probes.py:63-65` (`ALLOWED_GIT`), `probes.py:296-297` (argv and env) | The git seam is lock-free (`--no-optional-locks`, `GIT_OPTIONAL_LOCKS=0`, proved on a stat-dirty index: `.git/index` byte-identical after a full run) but it does not neutralize repo-config effects. `git status` honors `core.fsmonitor` (a hook command, or the built-in daemon, which starts a process and writes under `.git`) in every worktree `worktree ps` reports. Not configured on this host (`git config --get-all core.fsmonitor` and `core.untrackedCache`: no value). DESIGN 2.1 and section 17 do not mention it. | Record it as an accepted residual in DESIGN section 17, or add `-c core.fsmonitor=false` to the seam prefix together with the recorded-argv test (`tests/sweep/test_readonly.py:59-77`). |
| F4 | MINOR | `artifacts/sweep-live-check-1.4.md:3,7,13,15`; `artifacts/sweep-live-check-1.4.json` | The live-check claim is self-reported: no argv log exists for the live run, and the output of runs 1 and 2 was not kept (their reports sit in the gitignored `.dev/sweeps/`). What I could confirm independently: the saved JSON has exactly 9 Orca source rows (1 `worker-list`, 2 `task-list`, 5 `worker-show`, 1 `worktree ps`) and 30 `git status` rows, matching the record; every one of those is an allowlisted template and the seam makes any other impossible (C9); the Run id equals the OQ-8 record (`OQ-8-run-id-decision.md:26`); the `worker-list` file is a plain `ok:true` envelope for that Run (5 workers, `hasMore` false); the re-run log is in `### Phase 9 Findings` (task file line 2973), as item 9.3 requires. `ORCA_CLI_COMMAND` is unset now; its state at run time cannot be re-observed. | None; note only. |
| F5 | MINOR | `tests/sweep/` holds only `test_readonly.py` (4 tests, all pass) plus fixtures | There is not yet a test for `_publish` confinement, the no-`run-list` rule or the exit-code map. DESIGN section 15.2 plans them for later steps (1.10 `test_probes_allowlist.py`, 1.11 extends `test_readonly.py`, line 940-941). My scratch runs covered the same ground now. | Make sure steps 1.10 and 1.11 include the F1 direct-call case and the symlinked-sweeps cases below. |

## Check detail

**C1. `_publish` is the only write.** Grep over `src/superclaude/cli/sweep/` for `os.(write|open|makedirs|mkdir|rename|replace|remove|unlink|link|symlink|chmod|utime|truncate)`, `open(`, `.write`, `write_text`, `write_bytes`, `shutil`, `tempfile`, `.touch`, `.mkdir`, `.unlink`: every hit is in `commands.py` lines 140, 149, 150, 158, 170, 186, 203, all inside `_drop_own_temp`, `_write_all` or `_publish`. `probes.py` has three `open(path, "rb")` (lines 559, 810, 874). `classify.py`, `report.py`, `models.py` and `__init__.py` have no filesystem, process or environment access at all (grep for `.exists/.stat/.resolve/.read_text/Path.home/Path.cwd/importlib/eval/exec/ctypes` found only `re` and string `.replace` hits there). `click.echo` writes stdout or stderr only. No `os.rename` or `os.replace` anywhere.

**C2, C3. Containment (scratch, tmp root with `.git`).** `_check_output` accepted only the default folder and `<root>/.dev/sweeps/a`. It rejected: `sweeps/../tasks`, an absolute folder elsewhere, the root, `.dev`, `.dev/tasks/to-do`, `.dev/sweeps-evil` (prefix trap), a symlink child pointing outside (and a path below it), `.dev/sweeps` itself a symlink (default and sub path), and `.dev` a symlink. `_publish` called on a folder reached through a symlink to another folder raised `output dir escaped` and left the other folder empty. `--output <elsewhere>` through the CLI exit 2, other folder empty afterwards.

**C4, C5, C6. Full run (scratch, fake Orca binary set through `ORCA_CLI_COMMAND`, two real git repos with stat-dirty index entries).** Exit 0, JSON has the 12 schema keys, `.dev/sweeps/` held exactly one file `20261112-032407-sweep.md` (no temp), the only difference in the whole temp tree outside `.dev/sweeps/` was the mtime of the `.dev` folder entry itself, and `.git/index` of both repos was byte-identical. A no-binding run (`FAKE_BIND=none`, no `--run`) exited 2 with `no Run bound: pass --run <id>`, the Orca log held only `orchestration run-current`, and the tree was unchanged. `--window 0h`, `--run bad`, and `--output` outside exited 2. Two same-second `_publish` calls gave `-sweep.md` and `-sweep-2.md`.

**C7, C8.** `import subprocess` appears only in `probes.py:15`; its two `subprocess.run` calls (`probes.py:248`, `probes.py:299`) use list argv with no `shell=`, a timeout and a size check, and each is preceded by `check_orca_argv` or `check_git_args` (`probes.py:245`, `:295`). In `commands.py` the only `probes.` uses are lines 90 (`RUN_ID_RE`), 263 (`Budget`), 266 (`bind_run`), 269 (`collect`), 279 (`BindingError`). Every Orca or git call in the full run went through `_call` to `_orca` or `_git`. Recorded argvs of the full run: `run-current`, `worker-list --run R --json`, `task-list --ready --run R --json`, `task-list --run R --json`, `worker-show --dispatch D --json`, `worktree ps --json`; each passed `check_orca_argv`.

**C9, C10. Allowlists.** `ALLOWED_ORCA` has 10 templates and 7 verb pairs (`probes.py:47-58`), equal to DESIGN 7.3. Rejected with `ValueError`: `run-list` (with and without `--json`), `--include-remote` appended to `worker-list` and to both `worktree ps` forms, a run id with a trailing newline, an id with an extra character, an upper-case id, a run id given to `--dispatch`, `worker-start`, `task-create`, `worktree rm`, `worktree ps` with no flag, `run-current --json`, `gate-list`, an empty argv, `task-list --run R` without `--json`. `check_git_args` rejected `status` alone, a shortened status, `stash`, `gc`, and the exact status argv plus `--ignored`. The default binary is `orca-ide` (`probes.py:41`, `:193`); bare `orca` is only possible if the person sets `ORCA_CLI_COMMAND`, as DESIGN 7.1 allows.

**C11. No `run-list`.** Grep for `run-list`, `run_list`, `runlist` in `src/superclaude/cli/sweep/` finds nothing; the template is not in `ALLOWED_ORCA`; DESIGN GQ-104 (line 61) says the same. `run()` (`commands.py:264-266`) calls only `bind_run`, and `bind_run` (`probes.py:336-346`) raises `BindingError` (exit 2) on `no_binding` or unavailable.

**C12.** Readers use `open(..., "rb")`, `os.scandir`, `os.stat`, `Path.read_bytes`, `Path.read_text`, `Path.exists`; every path read from Orca text or from `worktree ps` is checked with `_inside` (symlink-following) before use (`probes.py:1315`, `:611`, `:634`, `:851`, and `_check_inside` in `_ledger`, `_contract`, `_transcript`). `_ledger` was changed during the live check so a missing `progress.md` is "no FINAL line" (`probes.py:578-582`), matching DESIGN GQ-105.

**C13.** Item 9.3 allows exactly: step (0) a local grep, step (1) `orca-ide orchestration worker-list --run <id> --json`, step (2) `uv run superclaude sweep run --run <id>`. The `.md` record shows those three and nothing else; the command quoted at line 7 equals `ALLOWED_ORCA` entry `probes.py:49` with `<run>` filled. `uv.lock` is not modified in `git status`. The re-run is allowed by item 9.3's own verification text and logged.

**C14.** `git diff -- src/superclaude/cli/main.py`: 4 insertions after the `issue-watch` pair (`main.py:566-568`: deferred import with the same `noqa` comment, then `main.add_command(sweep_group, name="sweep")`), no deletions. Import is lazy through `sweep/__init__.py:4-9`; no module-level I/O in `commands.py` or `probes.py`.

**C15.** `uv run --frozen --no-sync superclaude sweep --help` and `sweep run --help` exited 0; `diff` against the blocks recorded in `phase-outputs/test-results/step-1.7-help.txt` printed nothing.

**C16.** `commands.py:27` `DEFAULT_WINDOW = "6h"` (OQ-5 chosen `6h`, `OQ-5-GQ-61-window-decision.md:34`); `commands.py:101-102` default folder `<root>/.dev/sweeps`, `commands.py:155` name `%Y%m%d-%H%M%S` + `-sweep` in UTC (OQ-2 chosen, `OQ-2-GQ-10-report-location-decision.md:34`); `.gitignore:256` holds `.dev/sweeps/` and `git check-ignore -v .dev/sweeps/x.md` matched it.

**C17.** `uv run ruff check --no-cache src/superclaude/cli/sweep src/superclaude/cli/main.py tests/sweep`: All checks passed. `uv run pytest tests/sweep -q -p no:cacheprovider`: 4 passed. `phase9-validation.md` records ruff, format, help and `726 passed, 2 skipped` (not re-run by me: the 285 s unit suite is out of this lens). `src/superclaude/output-styles/pragmatic.md` shows as modified in `git status`; its mtime (2026-11-11 20:29) is before the CLI work and the change is the sweep chat-summary exception of the design addendum, not a write by the CLI.

## Summary
- Checks passed: 17 / 17
- Checks failed: 0
- BLOCKING: 0, MAJOR: 0, MINOR: 5 (F1 to F5, notes only)

**Self-audit.** If I told the user "no breach", the evidence is: seven grep passes over the whole package, two Python scratch harnesses (full run against a fake Orca with snapshot diff, 12 containment cases, 17 hostile Orca argvs, git argv probes), a live-JSON parse, two `--help` diffs, ruff, and the 4 `tests/sweep` tests. What I did not do: re-run the 726-test suite, observe the original live run (so F4 stays an inference from the saved JSON plus the seam), or test a filesystem without hard-link support.

**Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: about 30 | Grep: 7 | Glob: 0 | Bash: 12 (scratch harnesses under a private `/tmp` folder, removed afterwards; no web research)

Verdict: PASS
Blocking count: 0
