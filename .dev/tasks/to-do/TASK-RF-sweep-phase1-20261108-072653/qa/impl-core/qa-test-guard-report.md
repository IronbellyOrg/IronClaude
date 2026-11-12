# QA Report - Test-guard lens (T182, impl-core gate)

**Date:** 2026-11-12
**Phase:** code gate, test-guard lens (report-only, `fix_authorization: false`)
**Scope:** `tests/sweep/conftest.py`, `tests/sweep/test_readonly.py`, `tests/sweep/__init__.py`, `.gitignore` lines 255-256, `src/superclaude/cli/sweep/probes.py` (seams), `src/superclaude/pytest_plugin.py:206-228`, DESIGN `docs/designs/orchestrator-mode.md` sections 2.1, 10, 11, SPEC `merged-requirements.md` NFR-001, NFR-002, NFR-013, FR-025, research/05 sections 2, 3, 8.

Severity rule used: a `FAIL` in the Checks table needs a BLOCKING or MAJOR finding. Checks whose only findings are MINOR are marked PASS and the minor ids are named in the Note column.

## Method (what I actually ran)

- Read conftest.py (158 lines), test_readonly.py (167 lines), probes.py 1-150, 180-304, 880-910, 1150-1180, pytest_plugin.py 200-229, pyproject.toml 105-134, DESIGN 39-50 and 731-768, SPEC lines 91, 129-131, 142.
- `uv run --no-sync pytest tests/sweep -v -rA -p no:cacheprovider` (no cache, bytecode writing off): 4 passed, no warnings section, so the real-git control was conclusive.
- Drove the `no_subprocess` fixture body directly with fake requests (no file written): results in C1 to C7.
- `git diff -U0 -- .gitignore`, `git check-ignore -q` on both paths, `grep` for other process starters and for `integration` marks.

## Findings

No BLOCKING and no MAJOR finding. Nine MINOR findings (notes, never fail the gate).

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F-01 | MINOR | `tests/sweep/test_readonly.py:151-157` (lock-free call has `--no-optional-locks` AND `env={**env, "GIT_OPTIONAL_LOCKS": "0"}`); SPEC NFR-002 assertion (1); DESIGN 2.1 line 49 and open item 12 (`docs/designs/orchestrator-mode.md:980`) | The control cannot tell which of the two lock-free mechanisms works. If the flag were a no-op and the env variable did the work, the test would still pass, so "the flag alone carries the guarantee" (DESIGN 2.1, open item 12) is not shown. The SPEC wording is the flag alone. Production uses both (`probes.py:279-280`), so the product is covered; only the claim about the flag is not. | Run the lock-free call with `env=env` (no `GIT_OPTIONAL_LOCKS`), or run it twice, once with each mechanism. |
| F-02 | MINOR | `test_readonly.py:90-99` (comment at :91 says item 10.4 re-points it); task item 8.9 and 10.4 (`TASK-...md:1480`, `:1804-1805`); `probes.py:1150` `collect` now exists | DESIGN 11 case "one git argv per discovered worktree" is only a loop the test writes itself: it asserts N calls recorded for N calls made. It covers no discovery. Planned interim (item 10.4 is still unchecked), and `collect` already exists, so the re-point could be done now. | Re-point at `probes.collect` with `patch_git` at item 10.4 as planned; re-check this case at that gate. |
| F-03 | MINOR | `conftest.py:20-40`; `tests/sweep/` has no test of the fixture; `tests/sweep/__pycache__/test_tmp_guard_check.cpython-311-pytest-9.2.0.pyc` is the only trace; Phase 8 Findings (`TASK-...md:2961`) says the check used a temporary file that was deleted | The guard, including its one subtle rule (own decorator marks only, because `pytest_plugin.py:216-222` marks by path), has no durable regression test. Anyone can swap in `get_closest_marker` and the suite stays green. Item 8.9's "deliberate check" left no saved artifact (`step-1.4a-pytest.txt` shows only the 4 passing tests). | Add one small test file (not marked `integration`) that calls the guard-protected `subprocess.run`, `Popen` and `os.system` inside `pytest.raises(AssertionError)`. |
| F-04 | MINOR | `conftest.py:38-40`; direct run: `os.posix_spawn` ALLOWED | The guard blocks exactly the three entry points DESIGN 11 and SPEC NFR-001 name. `os.posix_spawn`, `os.spawn*`, `os.exec*`, `os.fork` and `asyncio.create_subprocess_*` are not blocked. No sweep code uses them (grep over `src/superclaude/cli/sweep` and `tests/sweep`: none). | None needed now; add `os.posix_spawn` only if the owner wants the guard wider than the spec. |
| F-05 | MINOR | no `integration` mark pin; grep for `pytest.mark.integration` in `tests/sweep`: only `test_readonly.py:109` | "Exactly one test" is true today but only by convention. The guard steps aside for any test with the mark, and nothing fails when a second one is added. | Optional: a collection-time check that counts the marked tests in `tests/sweep` and expects 1. |
| F-06 | MINOR | `test_readonly.py:139-142` | Assertion (4) runs plain `git status --porcelain`, not the sweep's `STATUS_ARGS` (`--untracked-files=all`, `-z`, `--branch`), and has no positive control that status lists an untracked file outside `.dev/sweeps/` (research/05 section 8 reads control (1) that way; the SPEC reads it as the index-rewrite control, which the test implements). The ignore rule is still detected, since a missing rule shows `?? .dev/`. | Use `*STATUS_ARGS` for the before/after status and add one untracked file outside `.dev/sweeps/` that must appear. |
| F-07 | MINOR | `test_readonly.py:116-127` (hand-built argv at :152); `probes.py:272-296` | The real-git test never calls `probes._git`. The argv it runs is a copy, so a change to the seam would not be seen by the real-git assertions (the recorded-argv test at :59-77 still covers the seam). | Call `probes._git(repo, *STATUS_ARGS, timeout=30)` inside the integration test with `HOME` and `GIT_*` set through `monkeypatch`. |
| F-08 | MINOR | `test_readonly.py:109-110, 126`; `git --version` here: 2.47.3 | The skip checks only that git exists; `git init -b main` needs git 2.28 or newer, so an older git errors instead of skipping. | `git init -q` then `git symbolic-ref HEAD refs/heads/main`, or skip on old versions. |
| F-09 | MINOR | `conftest.py:116-118` (`getattr(probes, "check_orca_argv", None)`), `:123` (`getattr(probes, "OrcaResult", None) or SimpleNamespace`) | Both hedges were for item 8.10, which has landed (`probes.py:93, 186`). If either name were renamed, `OrcaFake` would silently skip the real allowlist check or return a namespace, and tests would not notice. | Call `probes.check_orca_argv` and build `probes.OrcaResult` directly. |

Informational (not findings): `sweep_home` (`conftest.py:149-157`) holds only `HOME` and `XDG_STATE_HOME`; DESIGN 11 also wants packages, contracts, transcripts and an `orca-tabs/` folder, which Phase 8 Findings assign to item 10.1. Stale `.pyc` files of two deleted temporary tests sit in the git-ignored `tests/sweep/__pycache__/` (not collected, not tracked).

## Checks

| id | check | result | evidence / note |
|---|---|---|---|
| C1 | Guard patches `subprocess.run` | PASS | `conftest.py:38`; direct run: `run` and `check_output` BLOCKED (AssertionError) for an unmarked function |
| C2 | Guard patches `subprocess.Popen` | PASS | `conftest.py:39`; direct run: `Popen` and `os.popen` BLOCKED |
| C3 | Guard patches `os.system` | PASS | `conftest.py:40`; direct run: `system` BLOCKED |
| C4 | Guard reads only the function's own `pytestmark`, never `get_closest_marker` | PASS | `conftest.py:28`; grep for `get_closest_marker` in `tests/sweep`: no hit (the docstring says "closest-marker" in prose only); direct run used a request whose `get_closest_marker` raises, and it was never called |
| C5 | Guard steps aside only for an `integration` mark on the function | PASS | `conftest.py:29`; direct run: function with `integration` mark all ALLOWED; function with only a `skipif` mark all BLOCKED; no marks BLOCKED. Plugin auto-mark (`pytest_plugin.py:216-222`) uses `item.add_marker`, which does not touch `function.pytestmark` |
| C6 | Exactly one test gets through | PASS | grep `pytest.mark.integration` in `tests/sweep`: one hit, `test_readonly.py:109`. Convention only: F-05 |
| C7 | Patches are undone after the test | PASS | direct run printed "restored" for all three cases; the `recorder` fixture (`test_readonly.py:51-56`) patches on top and unwinds first |
| C8 | `integration` marker is registered under `--strict-markers` | PASS | `pyproject.toml:114, 119`; 4 tests collected and run |
| C9 | Recorded argv: `--no-optional-locks` at index 1, `-C` at 2, path at 3 | PASS | `test_readonly.py:69-74`; passes in my run |
| C10 | Child env has `GIT_OPTIONAL_LOCKS=0` even when the caller sets `1` | PASS | `test_readonly.py:60-62, 75` |
| C11 | Other `git` argv rejected before any process starts | PASS | `test_readonly.py:80-87`; `recorder.calls == []` at :87 |
| C12 | One git argv per discovered worktree | PASS | interim only, planned for item 10.4: F-02 |
| C13 | Real-git test copies the repository `.gitignore` | PASS | `test_readonly.py:127` from `REPO_ROOT` (`parents[2]`, :21) |
| C14 | Real-git test runs the four SPEC assertions | PASS | (1) control `:146-166`; (2) `:134` returncode 0; (3) `:136` returncode 1; (4) `:139-142`. Notes: F-01, F-06, F-07, F-08 |
| C15 | Inconclusive control is reported, not failed (SPEC NFR-002 (1)) | PASS | `:162-166` `warnings.warn`; `pyproject.toml` has no `filterwarnings = error`; no warning in my run, so the control was conclusive |
| C16 | No test can start Orca, ccsession or Claude | PASS | only `probes.py` starts processes (grep); unmarked tests are blocked (C1-C3); the one marked test runs `GIT` only (`shutil.which("git")`, :24) with `HOME` in `tmp_path` (:105) |
| C17 | `tests/sweep/__init__.py` exists and is empty | PASS | Read: file exists, empty (research/05 section 3) |
| C18 | `.gitignore` has the two `.dev/sweeps/` lines after `.dev/sprint-state/` | PASS | `git diff -U0`: 2 insertions at new lines 255-256; `.dev/sprint-state/` is line 254 |
| C19 | `.dev/sweeps/` ignored, `.dev/tasks/` not | PASS | `git check-ignore -q .dev/sweeps/x.md` exit 0; `.dev/tasks/to-do/x.md` exit 1 (matches `gitignore-check.md`) |
| C20 | Seam fakes call the real allowlist check first and match real signatures | PASS | `conftest.py:63` (`check_git_args`), `:116-118` (`check_orca_argv`); fake `GitFake.__call__(cwd, *args, timeout)` fits `probes._git` (`probes.py:272`). Note: F-09 |
| C21 | Saved test outputs agree with a fresh run | PASS | `step-1.4a-pytest.txt`, `step-1.4-pytest.txt`, `phase8-validation.md`: 4 passed; my run: 4 passed |
| C22 | A durable test of the guard itself | PASS | not required by DESIGN 11; gap recorded as F-03 (MINOR) |
| C23 | Guard covers process starters beyond the three named | PASS | not required by DESIGN 11 or SPEC NFR-001; F-04 (MINOR) |

## Summary

- Checks passed: 23 / 23 (no BLOCKING or MAJOR finding). Findings: 0 BLOCKING, 0 MAJOR, 9 MINOR (F-01 to F-09).
- Confidence: Verified 23/23 | Unverifiable 0 | Unchecked 0 | Confidence 100.0%
- Tool engagement: Read: 24 | Grep: 14 | Glob: 5 | Bash: 3 (pytest run, guard direct run x2 incl. one failed import attempt, git/grep checks)
- Not done: no scratch test file was written (report-only); the guard was exercised by calling its fixture body, not by a collected test, so a collected-test run of the guard is not shown.

Verdict: PASS

Blocking count: 0
