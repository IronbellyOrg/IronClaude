# QA Report - Gate D, test-adequacy lens (rf-qa-qualitative)

**Topic:** issue-watch Phase 8 cross-cutting tests
**Date:** 2026-11-08
**Phase:** task-qualitative (test-adequacy lens, report-only)
**Fix cycle:** 1 (fix_authorization: false)

## Overall Verdict: FAIL (blocking: 1, minor: 8)

One blocking finding (TA-1): the two static guards (`test_no_shell.py`, `test_module_boundaries.py`) read only the top level of the package, so a module placed in a sub-directory of `src/superclaude/cli/issue_watch/` with `shell=True` or `import subprocess` passes all 2616 tests (mutant M9 survived). Every other cross-cutting property was exercised by concrete mutants on copies and each mutant was killed, apart from the minor gaps listed.

## Method

- Read the change set (`phase-outputs/reports/gate-d-change-set.md`), the seven Phase 8 test files, conftest part 5 (lines 959-1155) and the code each one exercises (`record.py` lock, `cycle.py` launch path, `launch.py`, `github.py`, `runner.py`).
- Mutation testing on COPIES only: the source and `tests/issue_watch` were copied to a private directory under `/tmp`, each mutant was applied to a fresh copy and `uv run pytest tests/issue_watch` was run against that copy (`PYTHONPATH` pointed at the copy; the import path was checked to resolve into the copy). All copies and scratch scripts were deleted afterwards. No repository file was modified; the only file written in the repository is this report.
- Baseline on a copy: 2616 passed. Four repeat runs of the concurrency, e2e, crash and no-text files under `pytest -n 12` (xdist): 184 passed each time, no flake.

## Mutation results

| Id | Mutation (copy only) | Result | Killed by |
|---|---|---|---|
| M1 | Lock: drop `O_NOFOLLOW` from the `os.open` in `FileStore.lock` | KILLED (5 failed) | `test_concurrency.py::test_symlinked_lock_is_exit_6_with_no_call__fr017_ac11` (75 instead of 6), `test_record.py::test_ac11_lock_symlink_is_lock_invalid__fr017`, `::test_ac11_dangling_lock_symlink_is_lock_invalid__fr017`, two `test_cli.py` reset cases |
| M2b | Lock: drop the whole identity block after `flock` (the `os.stat`, the dev/ino compare and the `st_nlink` check) | KILLED (3 failed) | `test_concurrency.py::test_lock_path_replaced_after_flock_is_exit_75_with_no_call__fr017_ac11`, `test_record.py::test_ac11_lock_replaced_or_unlinked_after_flock_is_lock_held__fr017[replace]` and `[unlink]` |
| M2d | Lock: drop the dev/ino compare AND the `st_nlink` check (keep the not-found branch) | KILLED (2 failed) | the same replace-after-flock tests |
| M2a | Lock: drop ONLY the `(st_dev, st_ino)` compare | SURVIVED (2616 passed) | not detected: the `st_nlink == 0` check also trips in both swap tests (see TA-2) |
| M2c | Lock: drop ONLY the `st_nlink == 0` check | SURVIVED (2616 passed) | not detected: the dev/ino compare and the not-found branch also trip |
| M6 | Lock never released (no `LOCK_UN`, no `os.close`) | KILLED (31 failed, 19 errors) | `test_crash_injection.py::test_c5...`, `test_cycle.py`, `test_record.py::test_ac22...` |
| M7 | Launch path: remove the durable `pending` save before the Orca call (`cycle.py` line 1061) | KILLED (15 failed) | all five crash tests, `test_cycle.py::test_the_launch_steps_run_in_the_fr014_order_and_pending_is_durable__fr010_fr014` |
| M11 | A second launch after a crash: `sweep` turns a pending orphan into `failed` (so it is eligible again) | KILLED (10 failed) | `test_crash_injection.py` C3, C4 and the launcher-exception case (reruns launch again) |
| M10 | Prompt pattern loosened to accept trailing text | KILLED (6 failed) | `test_security_invariants.py::test_prompt_regex_property`, `test_launch.py` attack cases |
| M20 | Prompt built with the last label appended (and the pattern loosened so it is accepted) | KILLED (37 failed) | `test_security_invariants.py` hostile-label cases, `test_no_text.py` launch scenarios, so the hostile value really enters the system |
| M13a / M13b | `--method GET` changed to `POST` in the re-read / events builder | KILLED | `test_cli_e2e.py`, `test_github.py`, `test_security_invariants.py` |
| M14 | `title` added to the discovery `--json` fields | KILLED | `test_security_invariants.py` |
| M15 | Extra `--dangerously-skip-permissions` element in the launch argv | KILLED | `test_security_invariants.py`, `test_launch.py` |
| M17 | `shell=True` in the runner | KILLED | `test_no_shell.py::test_no_shell_forms_in_issue_watch_package`, runner tests |
| M18 | `import subprocess` added to `cycle.py` | KILLED | `test_no_shell.py` (two tests) |
| M12 | Stderr cap removed from the runner | KILLED (7 failed) | `test_no_text.py` real-runner tests, `test_runner.py` |
| M9 | A new sub-directory module `issue_watch/sub/x.py` with `import subprocess` and `subprocess.run(..., shell=True)` | SURVIVED (2616 passed) | not detected (blocking TA-1) |

Scanner probes (run against the copy of `test_no_shell.scan_source`): `import os.path` followed by `os.system("x")` returns `[]` (not flagged); a `**{"shell": True}` splat in `runner` returns no finding; `__import__("os").system`, `getattr(os, "system")`, `importlib.import_module("subprocess")` and `asyncio.create_subprocess_shell` return `[]`. The control `import os` + `os.system("x")` is flagged.

## Property-by-property adequacy

| Property | Would the test fail if it were violated? | Evidence |
|---|---|---|
| End-to-end through real processes (FR-001, FR-010, FR-013, NFR-010) | Yes | M7, M11, M13a, M15 killed; `test_cli_e2e.py` asserts the exact 13-call sequence, the pending entry read by the stub at launch time, and a second `once` with no `orca*` call. Minor: TA-8. |
| D3 prompt property (NFR-001, AC-7) | Yes | M10 and M20 killed; the property test covers ints, strs, floats, bools, None, containers and an `int` subclass (2000 seeded draws plus 32 edge values plus 21 attack strings), and hostile values are proven to enter the world (M20). |
| Argv allow-list (NFR-002, NFR-003, AC-20) | Yes | M13a, M13b, M14, M15 killed; 20 `BAD_ARGVS` mutation guards, five scenarios and every argv builder are classified. Minor: TA-6. |
| Crash points C1 to C5 | Yes | All five tests (and the launcher-exception case) run the crash and then exactly five reruns (`RERUNS = 5`, asserted by `gh_argvs.count(USER_ARGV) == 1 + RERUNS` and five distinct cycle ids) and check `launcher_calls <= 1` after every run; M7 and M11 killed. |
| Concurrency (FR-017, AC-11) | Yes | Two `spawn` processes ordered by files, not sleeps; the holder probes its own lock from inside the launcher; the loser must be exit 75 `lock_held` with zero runner and launcher calls; every wait and join is bounded (30 s and 60 s) and workers are terminated in a `finally`. M1, M2b, M2d, M6 killed. Minor: TA-2. |
| No shell | Partly | M17 and M18 killed for top-level modules, but M9 (sub-directory module) survives: TA-1 (blocking); scanner evasions: TA-3. |
| No text leaks (NFR-006, T11) | Yes | The canary is proven served in every one of about 118 scenarios (`SpyRunner.canary_served`), every file under the state dir is scanned with `rglob` including `audit.jsonl.1`, outputs of `once`, `status` and `status --json` are scanned, the closed audit key set is checked, the real runner's 500-byte cap is checked with real processes (M12 killed), and each checker has its own mutation guard. Minor: TA-4, TA-5. |
| Module boundaries | Partly | The import table and the relative, absolute and function-level spellings are enforced and mutation-guarded, but the module list is flat (`_sources()` uses `glob("*.py")`) while the Protocol and `select` tests use `rglob`: TA-1. |
| Stub fixture (unmatched-argv guard) | Yes, with a minor limit | PATH holds only `stubbin` and `linkbin`, the fixture asserts all four names resolve to the stubs, the teardown fails on any call that matched no rule, and `test_ac1_fixture_guard_names_resolve_to_stubs` pins the environment key set. The match is by argv prefix: TA-7. |
| Tests that use the real HOME, PATH, clock, network or paths outside `tmp_path` | None found | `stub_path` and `tmp_state` redirect HOME and XDG into `tmp_path`; the e2e subprocess gets an explicit `env=`; `run_world` and the crash rig give `Config` objects whose every path is inside `tmp_path`, so `cycle.py:189` (HOME fallback) and `_read_mountinfo` (called only at config validation, `cycle.py:270`) are not reached; the only real-clock dependence is the e2e `Date` header and event times, and `cycle.py` has no future-timestamp check (grep for `future` and `> now` found none in the cycle). |
| Flakiness under xdist, fixed names, timing | None observed | Four `-n 12` runs of the four process-heavy files: 184 passed each. The only wall-clock dependence is the 3 s timeout in TA-4. |
| Multiprocessing joins | Bounded | `test_concurrency.py` lines 161-169: `join(timeout=...)` and `terminate()` in a `finally`. |
| Pytest markers | Only the built-in `parametrize` | See the note under TA-9. |

## Findings

| Id | Severity | File | Evidence | Expected versus actual |
|---|---|---|---|---|
| TA-1 | BLOCKING | `tests/issue_watch/test_no_shell.py` lines 89-90 (`_package_files`) and `tests/issue_watch/test_module_boundaries.py` lines 187-190 (`_sources`), 198-202 (`test_package_has_exactly_the_designed_modules`) | Both guards enumerate the package with `PACKAGE_DIR.glob("*.py")`, which does not descend. `test_scan_covers_the_package_and_only_the_package` even asserts `p.parent == PACKAGE_DIR`. In the mutation run M9 added `issue_watch/sub/__init__.py` and `issue_watch/sub/x.py` containing `import subprocess` and `subprocess.run(["x"], shell=True)`: the full suite gave 2616 passed. In the same file `test_no_module_is_named_select` and `test_exactly_four_protocol_classes` already use `rglob`, so the two sibling enumerations of the same directory disagree on shape (flat versus recursive). Step 8.6 requires parsing "every `.py` file in `src/superclaude/cli/issue_watch/`"; the module docstrings say "every module in the package". The only remaining check on a nested file is the gate command `grep -rnE` (G-8), which is not a test. | Expected: a `shell=True`, `os.system` or non-runner `subprocess` import anywhere under the package directory fails a test, and a module outside the design table (nested or not) fails `test_package_has_exactly_the_designed_modules`. Actual: a nested module is invisible to both guards. Fix: enumerate with `rglob("*.py")` in both files (key `_sources()` by the path relative to the package, keep `RULES` flat) and add a mutation guard that feeds a synthetic nested path, or assert that the package contains no sub-directory other than `__pycache__`. |
| TA-2 | minor | `tests/issue_watch/test_concurrency.py` lines 255-275 and `tests/issue_watch/test_record.py` lines 790-820 | Lock identity: dropping only the `(st_dev, st_ino)` compare (M2a) or only the `st_nlink == 0` check (M2c) leaves the suite green, because in both swap tests (replace and unlink) the old inode has `st_nlink` 0 and the not-found branch or the inode compare also trips. The whole identity block (M2b) and the inode compare plus nlink check together (M2d) are killed. The inode compare is the only guard in one scenario no test builds: the lock file renamed away (not unlinked) and a new file created at the path, where the old inode keeps `st_nlink` 1. | Add a case that does `os.rename(lock, lock.with_name("lock.old"))` and creates a fresh `lock` inside the patched `flock`, expecting `LockHeld` / exit 75. Not blocking: the tested property (a lock path replaced or removed after `flock`) is enforced. |
| TA-3 | minor | `tests/issue_watch/test_no_shell.py` lines 44-86 (`scan_source`) | `import os.path` then `os.system("x")` is not flagged (only an `Import` whose `alias.name == "os"` binds a name to the module); `**{"shell": True}` is not flagged (only `kw.arg == "shell"` is read, so the splat is invisible in `runner.py`, the one module allowed to import `subprocess`); `__import__`, `getattr` and `importlib` forms are not flagged. No production module uses these spellings today. | Treat any `import os.x` as binding `os`, and flag a `**` keyword (`kw.arg is None`) in any call that could reach `subprocess`, or state the limits in the docstring. |
| TA-4 | minor | `tests/issue_watch/test_no_text.py` lines 716-723 | `test_real_runner_caps_stderr_of_a_timed_out_command` starts a real python child with a 3.0 s timeout and asserts only `len(stderr) <= 500`; unlike its two siblings it does not assert that the canary reached the runner. On a machine so loaded that the child has not written its 2000 bytes within 3 s, the test passes without exercising the cap. M12 was killed by it under normal load. | Assert `got.stderr.startswith(SENT)` as the sibling test does (or make the child signal readiness by file before the timeout is counted). |
| TA-5 | minor | `tests/issue_watch/test_cli_e2e.py` lines 374-376 | The e2e "no title, body, comments" scan is `{"title","body","comments"} & set(arg.split(","))`. It only matches a bare word between commas (the `--json` list). A GraphQL `query=...` argument, a `--jq` projection and a REST path are one comma-free token that never equals `body`, so a query asking for `body` passes this assertion. The stronger scans in `test_security_invariants.py` and `test_no_text.py` do catch it (M14 killed there), so the property is protected. | Delete the weak check or reuse `text_requests` from `test_no_text.py`. |
| TA-6 | minor | `tests/issue_watch/test_security_invariants.py` lines 263-272 (`classify_argv`, REST form) | Only `argv[:5]` and the last two elements are checked; arguments between the path and `--jq` (`-F per_page`, `-F page`) are free, so an extra `--input`, `-H` or `-f` element is classified as an allowed REST form. The literal argv of G3 and G4 is pinned in `test_github.py`, so the production builders are protected. | Compare the middle elements to `["-F", "per_page=100", "-F", "page=<n>"]` for events and comments. |
| TA-7 | minor | `tests/issue_watch/conftest.py` lines 988-994 (stub), `tests/issue_watch/test_no_text.py` lines 747-763 | A stub rule matches when the call's arguments START WITH `argv_prefix`. The real-process no-text test uses 1 to 3 element prefixes (`["-C"]`, `["issue","list"]`, `["api","user","--include"]`) and never asserts the recorded call sequence, so the teardown "unmatched argv" guard would accept any other `git -C ...` or `gh issue list ...` call there. The tests that matter (`test_cli_e2e.py`) compare the full recorded argv, so the property holds where it is claimed. | Pin the full argv in the rules of that test, or assert `read_calls` equals the expected list. |
| TA-8 | minor | `tests/issue_watch/test_cli_e2e.py` lines 356-364 | The comment says the 12-element argv "with the program path" equals the literal list, but the stub does not record its own invocation path (see its own comment at line 369), so the test prepends `orca_ide` to the 11 recorded arguments and compares with a list built from the same value; element 0 and the count of 12 are tautological in the e2e. The absolute program path is asserted in-process by `classify_argv` (`os.path.isabs(argv[0])`). | Have the stub log `sys.argv[0]` and assert it equals the stub path, or reword the comment to "the 11 arguments after the program". |
| TA-9 | minor (outside the Phase 8 change set) | `tests/issue_watch/test_record.py` line 739 | `@pytest.mark.skipif(os.geteuid() == 0, ...)` makes the "zero skipped tests" requirement of gates G-1 and G-3 depend on the user (uid here is 1000, so nothing is skipped). Note on markers: the Phase 8 files use only the built-in `parametrize`; design line 768 says "no marker" about `pyproject.toml` registration, and `--strict-markers` accepts built-ins. This is a note, not a finding. | Leave as is, or run the gate as a non-root user and record that. |

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | Full suite on a copy: 2616 passed; four `-n 12` runs of the process-heavy files: 184 passed each. |
| 2 | Project convention compliance | none | PASS | Tests only under `tests/issue_watch/`; no `.claude/` path; mutants only under `/tmp`, removed afterwards. |
| 3 | Intra-phase execution order | none | PASS | Fixtures build before use (`stub_path` then `Watcher`); concurrency order is by files, not sleeps. |
| 4 | Function signature verification | none | PASS | `FakeLauncher.launch(orca, worktree, prompt, timeout)` matches `OrcaLauncher.launch` and uses `launch_argv`; `CrashingStore` implements the `Store` methods used by `run_cycle`. |
| 5 | Module context and cross-symbol input shape | AX-2 | FAIL | TA-1: `_package_files` / `_sources` (flat) versus `test_no_module_is_named_select` / `test_exactly_four_protocol_classes` (recursive) on the same directory. |
| 6 | Downstream consumers | none | PASS | The scan helpers are used by their own mutation guards and by the real scan; nothing else imports them. |
| 7 | Test validity | none | PASS | Real inputs throughout; no placeholder assertions; minor notes TA-3, TA-4, TA-8 only. |
| 8 | Coverage of the primary use case | none | PASS | One eligible issue end to end through real processes, a second run, idle cycle, five crash points with five reruns, two-process lock; minor TA-5, TA-7. |
| 9 | Error path coverage | none | PASS | Hostile login, number, label, store and gh replies each have a test; symlink, directory, missing and replaced lock each have a test. |
| 10 | Runtime failure path trace | none | PASS | Crash then rerun path traced in `cycle.py` lines 1060-1075 and `record.sweep`; M7 and M11 show the tests follow it. |
| 11 | Completion scope honesty | none | PASS | The gate-d change set matches the files; the only overstatement is the "every module" wording behind TA-1. |
| 12 | Ambient dependency completeness | none | PASS | No marker or dependency added; xdist supplied ad hoc as the gate says. |
| 13 | Kwarg sequencing | none | PASS | No new kwarg is passed to a function that lacks it (`GhWorld(..., runner=...)` and `make_deps(..., which=...)` exist). |
| 14 | Existence claims | none | PASS | Grepped: `record.py` lock lines 381-419, `cycle.py:1061`, `launch.py:33`, `runner.py:63`, `github.py:206,257` exist as cited. |
| 15 | Template/design cross-references | none | PASS | Design lines 770-791 list the same seams and tests as the files; `_read_mountinfo` / HOME facts checked at `cycle.py:178-270`. |

## Summary
- Checks passed: 14 / 15
- Checks failed: 1
- Critical issues: 0 (blocking: 1 = TA-1, grade IMPORTANT; minor: 8 = TA-2 to TA-9)
- Issues fixed in-place: 0 (report-only)
- drift-axis-inactive

## Issues Found
See the Findings table above (TA-1 blocking; TA-2 to TA-9 minor notes that are carried forward and not rechecked).

## Actions Taken
None. fix_authorization was false. No repository file other than this report was written; mutants lived on `/tmp` copies that were deleted.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was in the spawn prompt, so the standalone behaviour applied and no rf-qa PASS item was relied on.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was supplied; the gate-command results recorded in the change set (2616 passed, xdist 2616 passed) were not taken as evidence, they were re-run on a copy.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Lock `O_NOFOLLOW` mutation (M1) - verified by running the suite on a mutated copy: 5 failures including `test_concurrency.py::test_symlinked_lock_is_exit_6_with_no_call__fr017_ac11`.
- Lock identity mutations (M2a, M2b, M2c, M2d) - verified by four separate mutated copies; M2a and M2c survive, M2b and M2d are killed (TA-2).
- Sub-directory module mutation (M9) - suite passes with a `shell=True` module in a sub-directory (TA-1).
- Scanner evasion probes (`import os.path`, `**{"shell": True}`) - executed against a copy of `scan_source` (TA-3).
- Hostile value really enters the system - M20 (label appended to the prompt with the pattern loosened) kills 37 tests, so the hostile-label tests are not vacuous.
- Flakiness - four `-n 12` runs of the four process-heavy files, all passed.
- Environment independence - grepped `cycle.py` for `expanduser`, `Path.home`, `os.environ`, `_read_mountinfo`; `cycle.py:189` and `:270` are on the config-validation path only.

## Recommendations
- Fix TA-1 (blocking): make `_package_files()` and `_sources()` recursive (or assert the package has no sub-directory), add a synthetic nested-path mutation guard, then re-run `uv run pytest tests/issue_watch/test_no_shell.py tests/issue_watch/test_module_boundaries.py`.
- Optionally fold TA-2, TA-3 and TA-4 into the same fix; they are small.

## Confidence and tool engagement
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: about 28 | Grep: 10 | Glob: 3 | Bash: about 20 (mutation runs, xdist repeats, cleanup). Web research: none (no Tavily or fallback call).

## QA Complete
