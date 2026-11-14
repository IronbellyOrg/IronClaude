# QA Report: Read-only-safety lens (final gate)

Date: 2026-11-12
Scope: `src/superclaude/cli/sweep/probes.py`, `src/superclaude/cli/sweep/commands.py` (plus `report.py`, `classify.py`, `models.py` for stray subprocess/write paths)
fix_authorization: false

## Findings

No BLOCKING or MAJOR finding. Two MINOR findings (notes; they do not fail the gate) and one scope note.

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| RO-1 | MINOR (real but non-blocking weakness: follow-up candidate) | `src/superclaude/cli/sweep/probes.py:296-300` (`_git` runs `git --no-optional-locks -C <cwd> status ...`) | `git status` runs a `core.fsmonitor` hook command if the scanned worktree's own git config sets one. Reproduced in a private /tmp repo (config `core.fsmonitor=<script>`): after `probes._git(repo, *ALLOWED_GIT[0], timeout=10)` the script's marker file existed. So a worktree's config can make the sweep run a command, which could write. Only the owner's own worktrees are scanned (root plus the paths `worktree ps` reports), `core.fsmonitor` is unset in this checkout (`git config --get-all core.fsmonitor` printed nothing), and the built-in fsmonitor daemon is "not supported on this platform" here, so the daemon form is UNVERIFIED. | Add `-c core.fsmonitor=false` to the fixed git prefix and pin it in `tests/sweep/test_readonly.py::test_git_argv_and_env_are_lock_free`. It changes the pinned argv of NFR-002, so it needs the owner's note; for Phase 1 leave it and record it. |
| RO-2 | MINOR (availability, not a write) | `probes.py:575` (`_ledger_has_final`: `os.stat` then `open(path, "rb")`), `probes.py:756` (`path.read_bytes()` in `_contract`), `probes.py:665-666` (ledger path `<worktree>/.dev/tasks/to-do/<pkg>/progress.md`) | The disk readers never check that the file is a regular file. Reproduced in /tmp: `probes.read_ledger` on a FIFO named `ledger` was still blocked after 6 s (`timeout 6` exit 124). The 90 s budget does not interrupt a file read, so a FIFO planted as `progress.md` or the contract file hangs the sweep. Transcripts and the tab map are guarded (`probes.py:1373` `e.is_file()`, `probes.py:871` `path.is_file()`). | Use `stat.S_ISREG(os.stat(path).st_mode)` before `open` in `_ledger_has_final` and `_contract`; report `not a regular file`. |
| RO-3 | NOTE (scope wording, not a defect) | `commands.py:158` (`os.makedirs`), `commands.py:140` and `:203` (`os.unlink(tmp)`) | The lens sentence lists only the temp file, `fsync` and `os.link` as writes. `_publish` also creates the output folder and removes its own temp file. Both are designed and documented (DESIGN lines 13, 106, 123 and 128: "plus that directory when it is new"), and both stay inside `<root>/.dev/sweeps/` (checked in C10). Nothing outside `_publish` writes. | None. |

## Verified safe, in short

- Two process starts exist in the package, both `subprocess.run([...])` with a list argv and no `shell=True`; each is reached only after an exact-allowlist check inside its own seam.
- 23 hostile Orca argv and 15 hostile git argv were rejected with `ValueError` before any process could start (a patched `subprocess.run` raised if reached); all 10 allowed Orca templates were accepted.
- A real `git status` through `probes._git` left a stat-dirty test repo byte-identical (28 files compared by size, mtime and sha1); a plain `git status` control did change it.
- The only writes in the whole package are in `commands._publish`.

## Checks

Evidence per check (read from disk now; line numbers are for the files as they are today).

| id | check | result | evidence |
|---|---|---|---|
| C1 | Every process start in `src/superclaude/cli/sweep/` is one of two `subprocess.run` calls with a list argv, no `shell=True`, no `os.system`, `Popen`, `exec*`, `spawn` | PASS | grep over `*.py` in the package for `subprocess\|shell\s*=\|os.system\|Popen\|popen\|spawn\|fork\|exec` matched only `probes.py:15` (import), `:248` (`_orca`) and `:299` (`_git`); `report.py`, `classify.py`, `models.py`, `commands.py`, `__init__.py` start no process |
| C2 | `_orca` is the only Orca seam; the argv check runs before the process | PASS | `probes.py:243-254`: `check_orca_argv(tuple(args))` (245), then `subprocess.run([binary, *args], ...)`. Only caller of `_orca` is `_call` (`:331`); `_call` is called at `:354`, `:1072`, `:1085`, `:1098`, `:1199`, `:1253`, each with literal verbs and ids |
| C3 | Every Orca argv equals one allowlisted template exactly (same length, literal tokens, placeholders by `re.fullmatch` of `run_[0-9a-f]{12}` / `ctx_[0-9a-f]{12}`) | PASS | `probes.py:47-58` (10 templates, equal to DESIGN 7.3 lines 526-537), `:196-215`. Probe over 23 hostile argv (extra flag, trailing newline in id, upper-case id, Arabic-Indic digit, wrong placeholder type, `worker-read`, `gate-list`, `check`, `send`, `worktree rm`, `worktree ps` bare, flag order swapped, empty, bytes and `Path` elements, the literal `<run>`) all raised `ValueError` before a process; 10 allowed templates accepted |
| C4 | No `FORBIDDEN_TOKENS` entry (`--include-remote`) can reach argv | PASS | `probes.py:60` (`frozenset({"--include-remote"})`), rejected first at `:208` in any position; also no template holds it, so exact matching would reject it anyway. Probe: `--include-remote` appended to `worker-list`, `worktree ps --json`, `worktree ps --agent-wait`, and placed before the verb: all `ValueError` |
| C5 | argv[0] (the binary) | PASS (by design) | `probes.py:191-193`: `$ORCA_CLI_COMMAND` else `orca-ide`; DESIGN 7.3 line 521 matches "after argv[0]" and line 382 documents the env var. The binary is not allowlisted, so `ORCA_CLI_COMMAND=orca` would run bare `orca` (the owner's own environment; accepted by the design) |
| C6 | `_git` is the only git seam; exact allowlist; fixed prefix and env | PASS | `probes.py:218-221` (`tuple(args) in ALLOWED_GIT`, one entry `status --porcelain=v1 -z --branch --untracked-files=all`), `:289-313`: argv `git --no-optional-locks -C <cwd> ...` (296), env `GIT_OPTIONAL_LOCKS=0` (297). Only caller `:968`. Probe: 15 hostile git argv (`status` bare, `--ignored` added, `stash`, `log`, `rev-parse`, `-c core.fsmonitor=x`, `branch -D`, `worktree add`, `gc`, `fetch`, `checkout .`, `clean -fd`, `add .`) all `ValueError`, no process |
| C7 | No git verb writes | PASS | Only `status` is allowed (C6). Real run through `probes._git` on a stat-dirty /tmp repo with an untracked file: 28 files byte-identical afterwards; control (plain `git status`) changed the tree, so the check can detect a write. Output `'## main\x00?? u.txt\x00'`. Caveat: RO-1 (repo-configured `core.fsmonitor` hook) |
| C8 | The only filesystem write is `_publish` (temp file, `fsync`, `os.link` of one report) | PASS | grep over the package for `write\|unlink\|makedirs\|mkdir\|touch\|truncate\|utime\|rename\|replace\|copy\|move\|rmtree\|tempfile\|chmod\|symlink\|O_WRONLY\|O_CREAT` hits writes only in `commands.py:140, 149, 150, 158, 170, 179, 186, 203`, all inside `_drop_own_temp`, `_write_all` and `_publish`. No `write_text`, `write_bytes`, `Path.open`, `shutil`, `tempfile` anywhere. See RO-3 for `makedirs` and own-temp `unlink` |
| C9 | Every other file access is a read | PASS | `open(` only at `probes.py:575, 826, 890`, all mode `"rb"`; the rest are `os.stat`, `os.scandir` (`:635, 857, 1371`), `read_bytes` (`:756`), `read_text` (`:873`), `path.exists()`. `classify.py` and `report.py` have no file access at all |
| C10 | `_publish` cannot overwrite or escape | PASS | `commands.py:153-208`: `O_CREAT\|O_EXCL` (170, refuses an existing file or symlink), `os.link` fails on an existing name (186-190), names `stem.md` to `stem-99.md`, escape re-check after `makedirs` (161). `_check_output` (`:99-123`) rejects `None` default, `<root>/elsewhere`, `/tmp` and `..` paths when `<root>/.dev/sweeps` is a symlink to another folder (probe in /tmp: all five `UsageError`, the symlink target stayed empty) |
| C11 | An allowlist `ValueError` is never swallowed or retried | PASS | grep of `except` clauses: `probes.py:391, 549, 761, 1354` catch `ValueError` only around time parsing, path resolution and file reads, none around `_call`; `commands.py:286` turns any other exception into exit 1 with `[sweep <stage>]` |
| C12 | Registration adds only the command | PASS | `git diff 5dc29d23b -- src/superclaude/cli/main.py`: 4 added lines (import and `main.add_command(sweep_group, name="sweep")`) |
| C13 | Tests, lint, sync | PASS | `uv run pytest tests/sweep tests/commands/test_sweep_command.py -q`: 694 passed; `uv run ruff check` clean and `ruff format --check` 15 files formatted on `src/superclaude/cli/sweep tests/sweep`; `make verify-sync`: "All components in sync" |
| C14 | The tests pin the seams, not only the code | PASS | `tests/sweep/test_readonly.py:73` (argv and env recorded), `:94` (git negatives never reach a subprocess), `:434-457` (process guard live; recorded Orca argv is a subset of the four expected calls; each passes `check_orca_argv`), `:473-529` (real git, with control). Gap: the real-git test builds its own argv rather than calling `_git`; `:73` covers the seam argv, and my own run in C7 covers the pair |
| C15 | Skill and command cannot run anything else | PASS | `src/superclaude/skills/sc-sweep-protocol/SKILL.md:4` `allowed-tools: Bash(superclaude sweep run:*), Bash(uv run --frozen --no-sync superclaude sweep run:*), Read`; lines 62 and 64 forbid any other command; `src/superclaude/commands/sweep.md:68` forbids changing Orca, git or a worktree or writing any file but the report |
| C16 | RO-1: git config can run a command during `_git` | FAIL (MINOR) | see RO-1; does not fail the gate |
| C17 | RO-2: readers accept special files | FAIL (MINOR) | see RO-2; does not fail the gate |
| C18 | The Phase 14 argument that the 3 full-run failures are not this change's | PASS | `git diff --stat 5dc29d23b -- src/superclaude/cli/eval tests/cli/eval tests/hooks src/superclaude/hooks` printed nothing and `git status --short` on those paths is empty; `uv run python -c "import importlib.util as u; print(u.find_spec('ruff') is not None)"` printed `False` while `uv run ruff --version` printed `ruff 0.17.3`, which matches the two `python -m ruff` failures. The `[1MB-big]` timing case I did not re-run (a 16-minute full run, 228 s alone under load per `phase14-full-pytest.md`); that part is taken from the record and is UNVERIFIED by me, but it touches no sweep file |
| C19 | My own experiments left no repository change | PASS | All experiments used `mktemp -d /tmp/ro*` folders, deleted afterwards (`ls -d /tmp/ro*` printed nothing). `git status --short` shows only the task's files plus this report; the three reports in `.dev/sweeps/` are dated 20261112-0311, from earlier runs, not mine (I ran no `sweep run`, no Orca, no ccsession) |

Confidence: Verified: 19/19 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100% (one sub-claim inside C18 is taken from the record and flagged)
Tool engagement: Read: 14 | Grep: 11 | Glob: 0 | Bash: 10 (read-only probes, tests, lint, verify-sync; no tavily or web calls)

## Follow-up candidates (Medium, never fail a gate)

- RO-1 (git config `core.fsmonitor` hook runs during `_git`; fix needs an owner note because it changes the pinned NFR-002 argv).
- RO-2 (readers hang on a FIFO; add a regular-file check).

Verdict: PASS
Blocking count: 0
