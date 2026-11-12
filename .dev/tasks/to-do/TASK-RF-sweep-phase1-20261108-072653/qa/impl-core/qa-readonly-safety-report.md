# QA Report - Read-only and allowlist safety lens (T181)

**Date:** 2026-11-12
**Phase:** code gate (impl-core), read-only and allowlist safety domain lens
**fix_authorization:** false (no file edited except this report)
**Scope read:** `src/superclaude/cli/sweep/{__init__,models,classify,probes,report}.py` (probes.py read in full, 1294 lines, in 150-line chunks), `tests/sweep/{conftest,test_readonly}.py`, `.gitignore` diff, DESIGN `docs/designs/orchestrator-mode.md` sections 2.1, 4 (boundaries), 7.1, 7.2 (observation rules), 7.3, 10, 11, the 1.0a facts, the gitignore check, and the three pytest records.

## Method

1. Read every line of `probes.py` and located each process start, each file open and each path read.
2. Grepped the whole sweep package for `subprocess|Popen|os.system|os.exec|os.spawn|os.popen|shell=`, for write and lock calls (`open(` modes, `write_*`, `touch`, `mkdir`, `fcntl`, `flock`, `unlink`, `rename`, `replace`, `shutil`, `tempfile`, `chmod`, `utime`, `symlink`), and for write verbs as strings.
3. Ran an independent probe (private `/tmp` dir, removed on exit, `uv run --no-sync python -I -B`) that replaced `probes.subprocess.run` with a recorder and (a) fed `check_orca_argv` 10 allowed and 22 hostile argv, (b) fed `_orca` and `_git` hostile arguments and counted process starts, (c) built a symlinked package tree to see which readers re-resolve.
4. Re-ran `uv run --no-sync pytest tests/sweep -q -p no:cacheprovider`: 4 passed.

## Checks

| Check | What it proves | Result |
|---|---|---|
| C1 | `ALLOWED_ORCA` holds exactly the ten DESIGN 7.3 templates, 7 verbs | PASS |
| C2 | No Orca argv outside the ten templates can reach a process start | PASS |
| C3 | `check_orca_argv` runs before every Orca subprocess call | PASS |
| C4 | No git argv outside `ALLOWED_GIT` can reach a process start; `check_git_args` runs first | PASS |
| C5 | `FORBIDDEN_TOKENS` is exactly `{"--include-remote"}` and is tested in any position | PASS |
| C6 | Git always gets `--no-optional-locks -C <path>` and `GIT_OPTIONAL_LOCKS=0` | PASS |
| C7 | No file is opened for writing, created, renamed, removed or locked in the package | PASS |
| C8 | Every reader re-resolves its path inside the root | FAIL (F1) |
| C9 | `subprocess` is imported as a module and used as `subprocess.run` | PASS |
| C10 | `classify.py` and `report.py` import none of `subprocess`, `click`, `os`, `shutil` (and `models.py` imports only `dataclasses`, `datetime`, `pathlib`) | PASS |
| C11 | The package holds no write verb, even as a string | PASS |
| C12 | Orca binary is `orca-ide` by default, with the env override DESIGN names | PASS (note F4) |
| C13 | `.gitignore` gets exactly the two `.dev/sweeps/` lines and does not cover `.dev/tasks/` | PASS |
| C14 | The committed read-only tests pass and exercise the real `_git` seam | PASS |

## Evidence per check

**C1.** `probes.py:43-54` lists ten tuples; text compared line by line with DESIGN 7.3 (`orchestrator-mode.md:526-537`): identical. My probe: all 10 accepted, distinct verbs counted 7. Matches the cursor decision in `1.0a-facts.md:60` (no cursor template).

**C2.** `check_orca_argv` (`probes.py:186-198`) requires every element to be `str` (189), rejects any `FORBIDDEN_TOKENS` member (191), then needs a template of the same length where each token is a literal match or an `re.fullmatch` of `RUN_ID_RE` / `DISPATCH_ID_RE` (179-183, 194-196). No prefix match. Probe: 22 of 22 hostile argv rejected (`check`, `inbox`, `worker-read`, `gate-list`, `run-list`, `worktree rm`, extra flag, trailing `--include-remote`, a lone `--include-remote`, id with trailing newline, 13-char id, upper-case id, Arabic-digit and full-width-digit ids, the literal `<run>`, a run id in the dispatch slot, reordered flags, empty tuple, truncated tuples, a `bytes` token). `fullmatch` and the ASCII class `[0-9a-f]` close the newline and Unicode-digit gaps.

**C3.** The only two process starts in the package are `probes.py:231` (Orca) and `probes.py:282` (git). The Orca one sits in `_orca`, whose first statement is `check_orca_argv(tuple(args))` at line 228. Every Orca call goes through `_call` (299-316) which calls `_orca` (306); the call sites are `probes.py:321, 995, 1008, 1021, 1109, 1163`, all through `_call`. Probe: after 22 hostile calls to `_orca`, recorded process starts = 0.

**C4.** `_git` calls `check_git_args(args)` at line 278 before `subprocess.run` at 282. `check_git_args` (201-204) is `tuple(args) in ALLOWED_GIT`, an exact tuple match against the single template at 59-61. The only caller is `_read_worktree` at line 891, which passes `*ALLOWED_GIT[0]`. Probe: 6 hostile git argument sets (`rev-parse`, `status`, status plus an extra token, `--version`, `stash`, empty), process starts = 0.

**C5.** `probes.py:56` is `frozenset({"--include-remote"})`; checked at 191 against the whole argv, before template matching, so position does not matter. Probe confirmed rejection in the last position and alone.

**C6.** `probes.py:279` builds `["git", "--no-optional-locks", "-C", str(cwd), *args]`; line 280 builds `{**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`; both are passed at 282-284 with `check=False` and no `shell`. A caller cannot supply the prefix. Probe recorded `['git', '--no-optional-locks', '-C', '/x', 'status', '--porcelain=v1']` with env value `0`. `test_readonly.py:59-77` asserts the same on the real `_git`, including that a caller's `GIT_OPTIONAL_LOCKS=1` does not leak. Paths given to `-C` come from `Path.resolve()` (`probes.py:1144, 1188`), so none starts with `-`.

**C7.** Opens are `probes.py:526`, `749`, `813`, all `"rb"`. Other file access is `os.stat`, `os.scandir`, `Path.read_bytes` (682), `Path.read_text` (796), `Path.exists` (1242), `Path.is_file` (794), all reads. Grep for write, create, remove, lock and temp-file calls in the package returned only `str.replace` / `datetime.replace` hits and a comment in `report.py:6` that says publication lives in `commands`. `git status` is made lock-free by C6. The DESIGN 11 test of the index file being untouched is `test_readonly.py:144-159` and it passes.

**C9.** `probes.py:15` is `import subprocess`; both starts are `subprocess.run(`. No `from subprocess import`. The autouse guard in `conftest.py:20-40` and the recorder in `test_readonly.py:55` patch the same module attribute, so they would see every start.

**C10.** Import lines of `classify.py`: `re`, `collections.abc`, `dataclasses`, `datetime`, `pathlib`, `.models`. `report.py`: `re`, `unicodedata`, `.models`. A grep of both for `os`, `sys`, `click`, `shutil`, `subprocess`, `__import__`, `importlib`, `exec(`, `eval(`, `.exists(`, `.stat(`, `.resolve(`, `.read_text`, `.read_bytes`, `.iterdir`, `.glob(`: no matches, so DESIGN B2 (paths are data only) also holds. Note: the AST import test named in DESIGN 11 does not exist yet (`tests/sweep/test_classify.py` is not written); the property holds today by inspection only.

**C11.** Grep for `worker-start|task-create|task-update|"send"|"reply"|"inbox"|"ask"|"dispatch"|"stop"|"rm"|"open"|"check"|--include-remote` found only `FORBIDDEN_TOKENS` and JSON key lookups named `dispatch` (not argv).

**C12.** `ORCA_BINARY_DEFAULT = "orca-ide"` (37); `orca_binary()` (174-176) returns `$ORCA_CLI_COMMAND` or the default, as DESIGN 7.1 line 382 states. See F4.

**C13.** `git diff -- .gitignore` shows two added lines (`# superclaude sweep reports...` and `.dev/sweeps/`) after `.dev/sprint-state/`, matching DESIGN section 10. `gitignore-check.md` records check-ignore 0 for `.dev/sweeps/x.md` and 1 for `.dev/tasks/to-do/x.md`; the real-git test repeats both (`test_readonly.py:134-136`).

**C14.** `step-1.4a-pytest.txt`, `step-1.4-pytest.txt` and `phase8-validation.md` each show 4 passed; I re-ran and got 4 passed. The tests patch `probes.subprocess.run` and call the real `_git`, so they test the seam, not a copy. (The `GitFake` in `conftest.py:43-76` rebuilds the argv itself; tests that use it do not prove the prefix, but `test_readonly.py` does.)

**C8 (FAIL).** See F1 below. Reader by reader:

| Reader | Re-resolve inside root? | Evidence |
|---|---|---|
| `_ledger` / `read_ledger` | Yes when a root is passed; `_packages` passes the worktree (`probes.py:595`) | `504-506`, `539-546` |
| `_transcript` / `read_transcript_tail` | Yes; `_read_transcripts` passes the project-key folder (`1288`) | `739-745` |
| `_tab_map` entries | Yes, each entry against the `orca-tabs` folder (`790`) | `790-792` |
| `_contract` via `_read_contracts` | Caller checks, reader skipped (`_contract(candidate, None)`, `1248`); see F2 | `1240-1248` |
| `_packages` folder scan and `.archiving` marker | **No** | `571-573`, `585-591`, `554-559` |
| `read_orca_version` | No, fixed system path constant (see F3) | `810-821` |
| `_worktree_paths` / `_read_worktree` `os.stat(path)` | Paths come from `Path.resolve()`; used only for `git -C` and a stat | `1136-1147`, `881` |

## Findings

### F1 - BLOCKING - package folder scan and `.archiving` marker do not re-resolve inside the root

- **Evidence:** `probes.py:571-573` runs `os.scandir(<worktree>/.dev/tasks/<to-do|done>)` and keeps entries where `e.is_dir()` (follows symlinks); `probes.py:586` records `folder / name`; `probes.py:591` calls `_marker(p / ".archiving")`, and `_marker` (`554-559`) is a bare `os.stat`. None of these paths goes through `_inside` / `_check_inside` (`496-506`). Only the `progress.md` ledger is checked (`595`). DESIGN 7.2 line 512 says "every discovered input path is passed through `Path.resolve()`" and must stay under the folder it was found in; DESIGN section 4 lists `.archiving` among the files read.
- **Reproduced:** in a temp tree, `wt/.dev/tasks/to-do/evil` as a symlink to a directory outside `wt` holding `.archiving`: `_packages(wt)` returned a `PackageRecord(id='evil', location='to-do', archiving_marker=True, ...)` and only the ledger got `unscanned: outside root`. With `wt2/.dev/tasks/to-do` itself a symlink to an outside directory, the outside directory names (`pkgA`) were listed as packages. So the sweep stats and lists paths outside the root and turns an outside file into a package state (`archive-blocked`).
- **What is wrong:** a reader that does not re-resolve inside the root, which the lens counts as a breach. The effect is read-only and small (a name list and one stat, no content), but it is a wrong-source observation reported as a root fact.
- **Smallest fix:** in `_packages`, before the scandir and for each `places` entry, skip with an `unscanned: outside root` row when `not _inside(folder, worktree)` or `not _inside(folder / name, worktree)`; make `_marker` take the root and return False (or flag unscanned) when `not _inside(path, root)`. Add a symlink-out test for a package folder and for `.archiving` (DESIGN 11 already plans a symlink-out fixture).

### F2 - MINOR - contract reader skips its own check; allowed base is wider than "the root"

- `probes.py:1240-1248`: the caller tests `_inside(candidate, base)` against `allowed = (root, *Orca worktree paths)` and then calls `_contract(candidate, None)`, so the read itself does not re-resolve (a symlink swapped between the check and the read is not caught; `_stable` compares size and mtime, not the resolved path). DESIGN 7.2 line 512 names the root only; the code also trusts every path `worktree ps` reports. Candidate paths come from Orca task and body text (`944-954`), so they are untrusted strings; a reported worktree path of `/` would put any file named `return-contract.yaml` in scope. Local single-user tool, so MINOR. Fix: pass the matching `base` as the `root` argument (`_contract(candidate, base)`) and record the widening as a DESIGN deviation.
- Also `probes.py:1256` calls `os.stat(candidate)` with no `OSError` guard after the read; a file removed in between raises past `collect`.

### F3 - MINOR - `read_orca_version` reads a fixed path with no resolve

- `probes.py:810-821` opens `ORCA_VERSION_FILE` (a constant) bounded to 1 MiB + 1; DESIGN line 259 labels it "bounded, resolve()". No path escape is possible from a constant, so no exposure. Add a resolve or drop the label.

### F4 - MINOR - `ORCA_CLI_COMMAND` can name bare `orca`

- `orca_binary()` (`174-176`) accepts any value; I confirmed `ORCA_CLI_COMMAND=orca` yields `orca`. DESIGN says the default is `orca-ide` and the variable overrides it (7.1 line 382), so this follows the design; the argv after the binary is still limited to the ten templates. Operator-set, not a code-path breach. Optional: document that the override is trusted.

### F5 - MINOR - `git status` can still act on repository config

- The fixed argv (DESIGN 2.1) has no `-c core.fsmonitor=false`. A swept repository that sets `core.fsmonitor` to a hook program would have `git status` run it, and with the built-in monitor enabled git may start its daemon. I did not test either (UNVERIFIED). The environment is also inherited, so a stray `GIT_DIR` or `GIT_INDEX_FILE` in the caller's environment would point `git status` at a different repository. This is a design-level limit of the one-call allowlist, not a bug in the code against the design. Consider a design note, or add `-c core.fsmonitor=false` to the prefix with the matching test.

### F6 - MINOR - notes, no action for this gate

- `tests/sweep/test_probes_allowlist.py` (DESIGN 11, NFR-003) does not exist yet, so the Orca allowlist has no committed test; C2 and C3 rest on my probe and on reading. The AST import test for `classify.py` and `report.py` is likewise not yet written (C10).
- `__init__.py` lazily imports `.commands`, which is not in the package yet (`ls` shows five files); `from superclaude.cli.sweep import sweep_group` fails until the commands item lands.
- `_ledger_has_final`, `_contract` (`read_bytes`) and the 8 MiB output limit are checked after the data is in memory (`capture_output` buffers first); resource bound, not a read-only issue.

## Self-audit

Tool calls that back the verdict: 9 chunked Reads of `probes.py` (1-1294), Reads of `__init__.py`, `test_readonly.py`, `conftest.py`, DESIGN sections 2.1, 4, 7.1, 7.2, 7.3, 10, 11, `1.0a-facts.md`, `gitignore-check.md`, `phase8-validation.md`, both pytest records; greps for process starts, write and lock calls, write verbs, imports and path calls; one executed probe (fuzz of both seams plus symlink trees); one pytest re-run. Not verified: live Orca or git behaviour against a real Run, F5's fsmonitor behaviour, and the classify/report logic outside this lens.

Verdict: FAIL
Blocking count: 1
