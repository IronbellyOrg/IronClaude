# QA Report - Isolation Lens (tests/sweep)

**Date:** 2026-11-12
**Phase:** tests gate, isolation lens
**fix_authorization:** false (report-only)

---

## Method notes

Scope: `tests/sweep/` (conftest.py plus six test files, 559 tests), the modules under `src/superclaude/cli/sweep/`, `src/superclaude/pytest_plugin.py:206-228`, `pyproject.toml:112-122`, the six result maps and `phase10-validation.md`, DESIGN section 11 (`artifacts/design-base.md:724-747`).

Every cited line was read from disk during this review. The three allowed commands were run: `uv run pytest tests/sweep -q` (559 passed in 1.68 s), `uv run ruff check ...` (All checks passed), `uv run ruff format --check ...` (15 files already formatted). `git status --short -- tests src` was identical before and after.

Dynamic proof method (private copy only, deleted at the end): `tests/sweep/` copied to `/tmp/iso-t227/repo/tests/sweep` (with a `.gitignore` copy and a symlink to `src/`), run under a private pytest plugin that installs a Python audit hook (`sys.addaudithook`). The hook logs `subprocess.Popen`, `os.system`, `os.exec`, `os.posix_spawn`, `os.spawn`, `os.fork`, sockets, every `open` with a write flag, `os.mkdir/rename/remove/rmdir/link/symlink/chmod/truncate/utime`, `shutil.rmtree/copyfile/move`, every `Path.home()` call, host reads under `/opt/Orca`, `~/.claude`, `~/.local/state`, `~/.config`, and the `HOME`/`XDG_STATE_HOME`/cwd values at the start of each test body. Write confinement was checked against each test's own `tmp_path` in the call phase, and against the pytest base temp folder in setup and teardown. Positive control: a one-test file that opens `/opt/Orca/x`, opens `~/.claude/x`, writes a file outside tmp, makes a folder outside tmp and runs `subprocess.run(["true"])` produced all five expected events (so the hook is live). No repository file was edited.

## Checks (run log)

### C1 Baseline
`uv run pytest tests/sweep -q`: 559 passed. Ruff check and format check clean. PASS.

### C2 The guard reads only the function's own `pytestmark`
Source: `tests/sweep/conftest.py:22-42`. Line 30 is `marks = getattr(request.function, "pytestmark", [])`, line 31 is `if any(m.name == "integration" for m in marks): return`. It never calls `request.node.get_closest_marker`, `request.node.iter_markers` or reads `request.module` or `request.cls`.

Mutation proof (private copy `/tmp/iso-t227/mut/integration/tests/`, conftest copied byte for byte; a folder literally named `integration` so the superclaude plugin's path rule at `src/superclaude/pytest_plugin.py:221-222` fires):

| Case | Marker present on the item (control assert) | Result |
|---|---|---|
| M3 path under `/integration/` (plugin adds the marker) | yes, `get_closest_marker("integration")` not None | `subprocess.run` and `os.system` still blocked |
| M5 `pytest.param(..., marks=pytest.mark.integration)` | yes | blocked |
| M2 class-level `pytestmark = pytest.mark.integration` | yes (class) | blocked |
| M4 function decorator `@pytest.mark.integration` (control) | yes | `subprocess.run(["/bin/true"])` runs, returncode 0 |
| M6 wrappers `check_output`, `call`, `check_call`, `getoutput`, `os.popen`, `asyncio.create_subprocess_exec` | no | all six blocked (they reach the patched `subprocess.run` or `Popen` attribute) |

6 passed. PASS. The plugin's directory rule cannot unlock the guard (the reason the fixture reads the function only), and the checkout path `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/tests/sweep/` contains no `/integration/` or `/unit/` segment anyway.

### C3 Exactly one test carries `@pytest.mark.integration`
- `grep` of `tests/sweep/*.py` for `pytest.mark.`, `pytestmark`, `integration`, `marks=`, `add_marker`, `import mark`, `from pytest import`: the only decorator is `tests/sweep/test_readonly.py:471` (`@pytest.mark.integration`, followed by `@pytest.mark.skipif(GIT is None, ...)` at :472 and `def test_real_git_lock_free_status_and_gitignore(tmp_path)` at :473). The other `integration` hits are prose (`conftest.py:5,24,27,31`, `test_readonly.py:5`). The only `pytestmark` token in the folder is the `getattr` string in `conftest.py:30`.
- `uv run pytest tests/sweep --collect-only -q -m integration -o addopts=""` printed `tests/sweep/test_readonly.py::test_real_git_lock_free_status_and_gitignore` and `1/559 tests collected (558 deselected)`.
- The marker is registered (`pyproject.toml:119`) and `--strict-markers` is on (`pyproject.toml:114`), so no new marker was needed; this matches DESIGN `design-base.md:731`.
- Producer claim `phase10-validation.md:89` (1 selected of 559) confirmed independently. PASS.

### C4 No test starts a process except the integration test (dynamic, whole run including collection)
Audit run, file order as on disk, 559 tests: 9 `subprocess.Popen` events, all attributed to `test_readonly.py::test_real_git_lock_free_status_and_gitignore`, all `/usr/bin/git` with `-C /tmp/iso-t227/bt/test_real_git_lock_free_status0/repo` (git init, add, commit, check-ignore x2, status x4). Zero events with no owning test (so none at import or collection time, including the `import superclaude.cli.main` in `test_cli_registration.py:26`). Second run, test files in reverse order, `-m "not integration"`: 558 passed, 0 process events. PASS.

### C5 No Orca, ccsession or Claude start (static)
- `grep` for `subprocess|Popen|os.system|os.exec*|os.spawn*|os.fork|posix_spawn|asyncio|pty|ctypes|multiprocessing|socket|urllib|requests|http` in `src/superclaude/cli/sweep/`: the only process starts are `probes.py:248` (`subprocess.run([binary, *args], ...)` in `_orca`) and `probes.py:299` (`subprocess.run(argv, ...)` in `_git`). Both call `subprocess.run` through the module attribute at call time, so the guard's `monkeypatch.setattr(subprocess, "run", _blocked)` (`conftest.py:40`) applies. No `from subprocess import ...` anywhere in `src/superclaude/cli/sweep/` or `tests/sweep/` (the single `from os import path` hit is a string in `test_classify.py:1795`).
- Every test that reaches the real `_orca` or `_git` does it over a recorded stand-in that replaces `probes.subprocess.run` after the guard (`test_probes_allowlist.py:194-200` `fake_run`; `test_cli_contract.py:140-146` `proc`; `test_readonly.py:65-70` `recorder`). The 9 real Popen events in C4 are git only; none names `orca-ide`, `orca`, `claude` or `ccsession`. PASS.

### C6 Guard coverage limits (what the guard does not patch)
The guard patches only `subprocess.run`, `subprocess.Popen` and `os.system` (`conftest.py:40-42`). Control M7 in the private copy: `os.posix_spawn("/bin/true", ...)` and `os.spawnv(os.P_WAIT, "/bin/true", ...)` are NOT blocked in a guarded test (output `ROUTES {'posix_spawn': 'NOT BLOCKED', 'os.spawnv': 'NOT BLOCKED'}`); by the same reading `os.exec*`, `os.fork`, `pty` and `ctypes` are not patched. No test or module uses any of them: the `grep` in C5 over `src/superclaude/cli/sweep/` found none, and a grep over `tests/sweep/*.py` for `putenv|os.chdir|os.environ[...]|os.fork|posix_spawn|ctypes|multiprocessing|socket|os.exec|os.spawn|os.popen|asyncio|pty|pexpect` matched only the word "empty" and prose (`conftest.py:176`, `test_readonly.py:182`) with no call. The earlier `subprocess`-name grep over the tests matched only recorders, `subprocess.DEVNULL`/`TimeoutExpired` constants, the guard-liveness test (`test_readonly.py:434-437`), the real-git test and the AST banned-name table (`test_classify.py:1784-1797`). The dynamic audit in C4 (which does see `os.posix_spawn`, `os.spawn`, `os.exec`, `os.fork`) logged none. This is a hardening gap, not a breach: finding F1 (MINOR). PASS for the lens (no test starts a process); gap recorded.

### C7 `HOME` and `XDG_STATE_HOME` are inside `tmp_path` in every test that reads them
Readers (grep of `src/superclaude/cli/sweep/` for `HOME|XDG_STATE_HOME|expanduser|Path.home|environ|getenv`): `probes.py:1287-1290` (`os.environ.get("XDG_STATE_HOME") or Path.home()/.local/state`), `probes.py:1365` (`Path.home()` in `_read_transcripts`), `commands.py:252-253` (`Path.home()` and `XDG_STATE_HOME` in `run`), plus `probes.py:193,297` (`ORCA_CLI_COMMAND`, a copy of `os.environ` for git). `collect` (called from `commands.py:269`) always reaches `probes.py:1365`, so every test that runs `collect` or `sweep run` past argument checks calls `Path.home()`.

Fixture: `sweep_home` (`conftest.py:151-159`) does `monkeypatch.setenv("HOME", str(home))` and `monkeypatch.setenv("XDG_STATE_HOME", str(state))` with `home = tmp_path / "home"`, `state = home/.local/state`. It is pulled in by `sweep_root` (`conftest.py:327-334`), by `env` (`test_cli_contract.py:80-107`) and by `sweep_env` (`test_readonly.py:303-347`).

Dynamic proof: `Path.home` was wrapped and every call logged with its owner test. 157 calls from 98 distinct tests; 0 returned a path outside the pytest base temp folder; for each of the 98 tests `HOME` and `XDG_STATE_HOME` at the start of the test body both started with that test's own `tmp_path`; list of offenders: empty. The other 461 tests had `HOME` and `XDG_STATE_HOME` outside tmp (host values; `XDG_STATE_HOME` is unset on this host) but never called `Path.home()` (they are pure `classify`, `report` and allowlist tests). The real-git test sets only the git child's `HOME` to `tmp_path / "home"` (`test_readonly.py:464-468`). PASS.

### C8 No test writes outside its `tmp_path`
Audit result over all 559 tests (call phase confined to the test's own `tmp_path`, setup and teardown to the base temp folder): 0 `WRITE_OUTSIDE`, 0 `MUTATE_OUTSIDE`. One `MUTATE_RELATIVE` event: `os.remove(".git")` during `test_worktree_removed_between_the_seams_is_unscanned_and_the_others_continue[stat-fails]`; that is `shutil.rmtree(gone)` (`test_probes_allowlist.py:1462`) of `sweep_root.worktree("gone")`, a folder under `tmp_path/worktrees/gone` (`conftest.py:194-199`), removed through a directory file descriptor (hence the relative name). 382 tests have no `tmp_path` in their fixture closure and the confinement set for them was "nothing", so they wrote nothing at all. The cwd at the start of every test was the checkout root of the copy; the three tests that change directory use `monkeypatch.chdir` into a `tmp_path` folder (`test_cli_contract.py:714,726,747`), and no relative write appeared. The tests that mutate files do so in tmp only: symlinks and unlinks `test_probes_allowlist.py:1566,1584,1601-1602,1621`, appends `:1672`, `test_readonly.py:235,242,248,255,261,413,489` (the `shutil.copyfile` writes `repo/.gitignore` inside `tmp_path`; its source `REPO_ROOT/.gitignore` is read only), and the publication tests `test_cli_contract.py:1178-1402` write under `env.sweeps` (`tmp_path/root/.dev/sweeps`).

Repository side: `.dev/sweeps/` exists in the worktree with four reports dated 2026-11-12 03:11 to 03:45, earlier than this review's runs (clock 05:24), and `git check-ignore -v .dev/sweeps/x.md` shows it is ignored (`.gitignore:256`). The audit shows no test wrote there, and `git status --short -- tests src` did not change over this review's pytest runs. PASS.

### C9 Host reads
`probes.read_orca_version` reads `/opt/Orca/resources/app.asar.unpacked/out/package.json` (`probes.py:67`, `:887`, called at `:1247`). It is stubbed in every file that runs `collect` or the CLI: autouse `_no_orca_version_file` in `test_probes_allowlist.py:208-211`, `env` at `test_cli_contract.py:88`, and the `no_orca_version_file` fixture at `test_readonly.py:123-126` (requested by `sweep_env`, `:303-312`, and by the two `collect` tests at :130-131 and :144-145). Audit: 0 `READ_HOST` events (no `open` or directory scan of `/opt/Orca`, `/home/coder/.claude`, `/home/coder/.local/state`, `/home/coder/.config`, `/home/coder/.aidev*`) in any test; the positive control proves the hook fires for a path that does not exist. `ORCA_CLI_COMMAND` is cleared by `fake_run` (`test_probes_allowlist.py:199`) and `env` (`test_cli_contract.py:89`), set to a fixed value elsewhere via `monkeypatch.setenv` (`test_probes_allowlist.py:517,525,573,1181`). PASS.

### C10 Patch scope and order independence
Process-wide patches are all `monkeypatch`-scoped: the guard (`conftest.py:40-42`), `_fail_in_commands` over `commands.os` (the shared `os` module; gated on the caller frame, `test_cli_contract.py:232-245`), `builtins.open` inside `monkeypatch.context()` (`test_classify.py:753-772`), `Path.read_bytes` (`test_probes_allowlist.py:1633-1646`, `test_classify.py:775-792`), `probes.os.scandir` (`test_probes_allowlist.py:1257`), `sys.modules` entries (`test_cli_registration.py:48-69`). No assignment to `os.environ`, `os.putenv` or `os.chdir` exists in the folder (grep). Test files run in reverse order with the integration test deselected: 558 passed. PASS.

### C11 The one real-git test is itself confined
`test_readonly.py:471-528`: repo at `tmp_path / "repo"`; child env drops every `GIT_*` variable, sets `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, fixed author and committer, `GIT_TERMINAL_PROMPT=0`, and `HOME=tmp_path/"home"` (`:40-49`, `:464-468`); only `git` is started (C4: init, add, commit, check-ignore, status); it skips when git is absent (`:472`). The Python process writes only inside `tmp_path` (the `shutil.copyfile` destination, `tracked.txt`, `.dev/sweeps/x.md`, `os.utime` on `tracked.txt`). See F2 for one host-dependence. PASS with note.

### C12 A guard trip inside the CLI cannot hide as a pass
`commands.py:286-288` catches `Exception`, so the guard's `AssertionError` raised inside `sweep run` would become exit 1 plus `[sweep <stage>] ...` on stderr. Every `exit 1` test asserts the whole stderr text (`test_cli_contract.py:1135,1162,1224-1229,1247,1271-1275,1289,1317,1333,1354,1374,1401`), and every exit 0 test asserts exit 0 with empty stderr (`_payload`, `test_cli_contract.py:179-187`; `test_readonly.py:443,377`). A trip would therefore fail those tests. PASS.

### C13 Producer evidence against disk
- `phase10-validation.md:62` (559 passed) and `:89` (exactly 1 integration test): both reproduced.
- `test-readonly.txt:66` ("the only integration-marked test; PASSED, not skipped"): reproduced (the audit shows its 9 git starts).
- `test-cli-registration.txt:26-27` quotes "469 passed" for `tests/sweep` (an older count; the folder now holds 559). Wording only, see F3.
- DESIGN `design-base.md:731-732` (guard steps aside only for the `integration` marker, used by exactly one test; `HOME` and `XDG_STATE_HOME` moved inside `tmp_path`) matches `conftest.py:22-42` and `:151-159`. PASS.

## Findings

No BLOCKING and no MAJOR finding. Four MINOR findings (notes; they never fail the gate).

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `tests/sweep/conftest.py:40-42`; control M7 in the private copy (`os.posix_spawn` and `os.spawnv` ran `/bin/true` inside a guarded test) | The guard patches only `subprocess.run`, `subprocess.Popen` and `os.system`. `os.posix_spawn`, `os.spawn*`, `os.exec*`, `os.fork`, `pty` and `ctypes` can still start a process. No test uses them today (C4, C6). | Add `monkeypatch.setattr(os, name, _blocked)` for `posix_spawn`, `posix_spawnp`, `spawnv`, `spawnve`, `spawnvp`, `spawnvpe`, `execv`, `execve` and `fork` next to line 42, or leave it and rely on the module banned-import test; no urgency. |
| F2 | MINOR | `tests/sweep/test_readonly.py:464-468` (`_git_env` copies `os.environ` minus `GIT_*`, sets `HOME` only); reproduced in `/tmp` with `XDG_CONFIG_HOME` pointing at a `git/ignore` file: `git check-ignore probe.txt` exits 0 with `GIT_CONFIG_GLOBAL=/dev/null` set, and exits 1 without `XDG_CONFIG_HOME` | The real-git test keeps the host `XDG_CONFIG_HOME`, so a developer's global ignore file at `$XDG_CONFIG_HOME/git/ignore` can change the `check-ignore` results asserted at `:496` and `:498`. It is a read of host state, not a write, and unset on this host. | In `_git_env` add `env["XDG_CONFIG_HOME"] = str(home / ".config")` (one line). |
| F3 | MINOR | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-cli-registration.txt:26-27` | The order-independence note says `tests/sweep` gave 469 passed; the folder is now 559. Stale count only; the behaviour it describes still holds (C10). | Re-run and replace the numbers when the file is next regenerated. |
| F4 | MINOR | `conftest.py:31` (unlock by marker name); `tests/sweep/test_readonly.py:471`; `phase10-validation.md:89` | "Exactly one test carries `integration`" is held only by a one-time `-m integration` run and a grep. No test or collection hook fails if a second `@pytest.mark.integration` is added; that test would silently regain `subprocess.run`. | Optional: in `conftest.py` add `pytest_collection_modifyitems` that fails collection when more than one item has a function-level `integration` mark. |

Limits of the proof: the audit hook sees Python-level events in the pytest process only. File writes made by the `git` child process in the integration test are not audited; their confinement rests on `-C <tmp_path>/repo` in every argv (seen in all 9 Popen events), `HOME` in `tmp_path` and `GIT_CONFIG_GLOBAL=/dev/null` (`test_readonly.py:40-49,464-468,479-486`). The audit ran on a private copy of the folder (so repository-relative writes would show as writes outside the copy's tmp folders, none did); the in-repo run of the same files passed with an unchanged `git status` for `tests` and `src`.

## Checks

| check id | result |
|---|---|
| C1 | PASS |
| C2 | PASS |
| C3 | PASS |
| C4 | PASS |
| C5 | PASS |
| C6 | PASS (gap recorded as F1, MINOR) |
| C7 | PASS |
| C8 | PASS |
| C9 | PASS |
| C10 | PASS |
| C11 | PASS (note F2, MINOR) |
| C12 | PASS |
| C13 | PASS (note F3, MINOR) |

## Self-audit and confidence

- Confidence: Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (counts the 13 checks above; the limits paragraph names what the audit cannot see).
- Tool engagement: Read: 34 | Grep: 13 | Glob: 0 | Bash: 24 (the Bash calls are the three allowed commands, `--collect-only -m integration`, the private-copy audit and mutation runs, the positive control, the git `XDG_CONFIG_HOME` probe, and file listings).
- Question asked before the verdict: "if I told the user 0 breaches, what would I point to?" Answer: the audit event logs (0 process starts outside the integration test, 0 writes outside tmp, 0 host reads, 98 of 98 home readers inside tmp), the positive control, and the six-case guard mutation run. The four MINOR findings show the review was not a rubber stamp.
- Cleanup: the private copy `/tmp/iso-t227` is removed after this report; this report is the only repository file written.

Verdict: PASS
Blocking count: 0


