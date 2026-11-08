# QA Report — Gate D, security-invariants lens

**Topic:** issue-watch Phase 8 tests
**Date:** 2026-11-08
**Phase:** task-qualitative (lens: security-invariants)
**Fix cycle:** 1
**Fix authorization:** false (report-only)

## Overall Verdict: PASS (0 blocking findings, 9 minor notes)

Scope read in full: `conftest.py` part 5 (lines 959-1155) plus the fakes it depends on (lines 1-420, 476-710, 920-958), `test_cli_e2e.py` (443 lines), `test_security_invariants.py` (961), `test_crash_injection.py` (373), `test_concurrency.py` (275), `test_no_shell.py` (191), `test_no_text.py` (961), `test_module_boundaries.py` (375), and the code they exercise (`github.py` argv builders and cursor and login patterns, `launch.py`, `record.py` lock and sweep, `cycle.py` launch step, `cli.py` once and reset, `runner.py`). Binding sources read: design lines 651-693 and 760-791, research/06 table 1.4 and rows DF-10, DF-12, DF-28.

Experiments ran only on a `/tmp` copy of `src/superclaude` and `tests/issue_watch` (the repository tree was not touched). Baseline on the copy: 130 passed (security, no-shell, crash, concurrency) and 243 passed (e2e, no-text, boundaries). Then 18 mutations of the package (details under Self-Audit). Every mutation of a security control was caught by the Phase 8 set, except M12 (caught by `test_security_invariants.py` only, note N-3) and M24 to M26 (three narrow input validators, caught by the earlier `test_github.py`, so no finding). Two call forms and one subpackage case escaped the static no-shell guard (notes N-1 and N-2).

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | E2E PATH holds only stub and link dirs; guard proves it for all four names | none | PASS | `conftest.py:1139-1150` builds `PATH = stubbin:linkbin`, asserts `shutil.which(name, path=PATH) == stubbin/name` for gh, orca, orca-ide, git at fixture setup; `test_cli_e2e.py:281-296` asserts the exact PATH string, the four stub names, `linkbin == [python3]` and the exact env key set. `find tests/issue_watch -type f -perm /111` printed nothing. The package has no absolute-path tool lookup (`launch.find_orca` and `cycle` use `which`; grep of the package found no `/usr/` or `.orca` literals). |
| 2 | No real gh (or git, orca) runs against any repository | none | PASS | In-process tests use `FakeRunner`/`SpyRunner`; `test_no_text.refuse_real_processes` patches `SubprocessRunner.run` to raise; the only real-runner uses are `sys.executable -I -S -c` children (`test_no_text.py:701-721`) and the stub-PATH test (`:739-787`, PATH monkeypatched to the stub dirs after the fixture guard). Grep of the seven Phase 8 files for `SubprocessRunner(`, `subprocess.`, `shutil.which` found nothing else. |
| 3 | `SuperClaude-Org` appears only as a negative needle | none | PASS | Phase 8 files: `test_security_invariants.py:62,756,804` (needle and BAD_ARGVS only). Other hits are earlier-gate negative fixtures (`test_launch.py:448-449`, a `check_origin` mismatch case; `test_github.py:350`). No argv served by any scenario names it (`classify_argv` rejects it). |
| 4 | Every recorded argv scanned against allowed forms; `--method GET` on every REST path call | none | PASS | `classify_argv` (`test_security_invariants.py:222-296`) is default-deny: an argv matching none of user, discover, rest, graphql, origin, probe, launch fails on `os.path.isabs(argv[0])`. It runs on every argv of the five scenarios, of every hostile scenario (`run_world`, line 356), and on every builder output with pages and cursors (`:692-718`). The REST branch requires `argv[2:4] == ["--method","GET"]` (line 263). Mutation M1 (drop `--method GET`) caught. All 18 `BAD_ARGVS` are rejected (I ran `classify_argv` over each and printed the rejection; none accepted). |
| 5 | No mutation in any GraphQL constant; no title or body field in any argv | none | PASS | `test_security_invariants.py:872-898` scans every `str` constant of `github` and both queries (`mutation`, `subscription`, `$owner`, text fields); `classify_argv` lines 235 and 244-248 apply per argv; `test_no_text.text_requests` adds the `--json` whitelist, `--template`, jq and query word scans. Mutation M2 (discovery asks for `title`) caught. |
| 6 | Prompt property covers ints, hostile strings, floats, bools, None with the seeded generator | none | PASS | `test_prompt_regex_property`: `random.Random(331)`, 2000 draws plus 32 edge values (bool, float nan/inf, None, bytes, containers, an `int` subclass with hostile `__str__`), generator-shape assertions (`valid >= 400`, `invalid >= 1200`, 8 families), 21 `PROMPT_ATTACKS`, and 12 full cycles. Design 693 and DF-12 (no marker, seed 331, 2000 draws) are satisfied. Mutations M3 (bool accepted) and M27 (`match` for `fullmatch`) caught. |
| 7 | Hostile GitHub, config and login text never reaches the prompt | none | PASS | `:520-625`: 12 hostile strings as label, actor, commenter, assignee, config label, own login (18 logins), discovery number (13 values); asserts `prompts == ["/sc:issue --claim 9"]`, forms unchanged, hostile text in no argv. Mutation M4 (extra launch flag) caught. |
| 8 | Hostile-text test scans every file under the state dir including rotated audit files | none | PASS | `assert_state_dir_clean` uses `rglob("*")` (`test_no_text.py:120-129`); `test_rotated_audit_files_are_scanned_and_stay_clean` forces rotation and asserts `audit.jsonl.1` exists and is in the scanned list. The canary is proven served (`SpyRunner.canary_served`) in every scenario. The one `skip=("dispatch.json",)` use is the damaged-store case where the canary is planted in that file on purpose (note N-6). Mutation M8 (exception text in the crash line) caught. |
| 9 | Crash tests prove at most one launch across six runs per crash point | none | PASS | `Rig.check_at_most_once` runs after the crash and after each of the five reruns (`test_crash_injection.py:117-125`, `:142`); C1 to C5 and the launcher-exception case each end with exact launcher-call totals (0 or 1). Mutations M5 (no pending save before launch), M7 (lock not released) and M10 (pending entries not swept) caught by the crash tests. |
| 10 | Concurrency test proves exit 75 for the loser | none | PASS | `test_two_processes_one_store_one_launch` uses real `spawn` processes, file-ordered (worker 1 holds the lock inside the launcher call), asserts `(one.exitcode, two.exitcode) == (0, 75)`, `lock_held_during_launch is True`, the loser made 0 runner and 0 launcher calls, one launch in total, and the two cycle audit lines. Joins have timeouts (`JOIN_S`), waits are bounded polls, leftovers are terminated. The CLI mapping 75 is pinned by `test_cli.py:438-472`. Mutation M6 (lock not exclusive) caught. |
| 11 | No secret-like or token-like value in a fixture | none | PASS | Regex search of the 19 `_assumed_shape` JSON fixtures and the seven test files for `ghp_`, `github_pat`, bearer, authorization, `x-oauth`, 32-char hex and 36-char base64 runs found none (only test names and the prose "the token lacks the read:project scope"). `PVT_test_project_0001` is a placeholder. |
| 12 | No test reads or writes the real HOME, real state dir or repository tree | none | PASS | Experiment: `test_security_invariants`, `test_no_shell`, `test_module_boundaries` run with an empty `HOME`, `XDG_STATE_HOME` unset and `UV_CACHE_DIR` elsewhere created nothing under `HOME`. e2e uses `HOME=tmp/home`, `XDG_STATE_HOME=tmp/xdg`, `cwd=HOME`, explicit `state_dir`. No_shell and boundaries read `src/` by design (read-only). See N-7 (real `/proc/self/mountinfo` read) and N-8 (no bytecode suppression in the e2e child). |
| 13 | Stub unmatched-argv guard | none | PASS | Teardown assertion in `stub_path` (`conftest.py:1152-1155`) and exit 99 plus `matched:false` record in the stub (`:1029-1032`). No current test bypasses it; see N-4 for ways a future test could weaken it. |
| 14 | No-shell static guard (T6, NFR-004) | none | PASS | Implements the three design forms (design 788); 15 positive and 12 negative self-tests; mutations M9 (`shell=True` in runner) and M11 (`import subprocess` in `github.py`) caught. Residual bypasses are minor notes N-1 and N-2. |
| 15 | Tests cannot themselves cause harm | none | PASS | Hostile strings (`$(touch /tmp/pwned)`, `; rm -rf /`) only enter argv lists of `FakeRunner`/`SpyRunner`, never a real process or a shell; the only real children are `sys.executable` runs and PATH stubs. Global patches (`os.replace`, `fcntl.flock`, `SubprocessRunner.run`, `cycle._read_mountinfo`) use `monkeypatch` and are restored (`test_crash_injection.py:254` asserts `os.replace is real_replace`). |
| 16 | Module-boundary guard (NFR-014, AC-25) | none | PASS | Resolves relative and absolute imports to one name, walks function-level imports, over 30 flagged and 18 clean synthetic sources. Not a security control; checked for guard soundness only. |

## Summary
- Checks passed: 16 / 16
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)
- Axis lens status: drift-axis-inactive

## Issues Found

Blocking findings: none. Every note below is minor (cosmetic, wording, or a weakness no current property depends on); minor notes are not rechecked in later rounds.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| N-1 | MINOR | `test_no_shell.py:89-90,98-103`; `test_module_boundaries.py:187-190,198-202` | Both guards read `PACKAGE_DIR.glob("*.py")`, which is not recursive. `all(p.parent == PACKAGE_DIR for p in files)` is therefore always true. Experiment: a new `issue_watch/sub/helper.py` holding `import subprocess` and `subprocess.run("true", shell=True)` left all 103 tests of the two files green. (`test_exactly_four_protocol_classes` does use `rglob`.) | Use `rglob("*.py")` in `_package_files` and `_sources`, and make the coverage test compare against an independent `rglob` count. |
| N-2 | MINOR | `test_no_shell.py:44-86` | The scan recognises only `shell=` keywords, `os.system`/`os.popen` and `import subprocess`. Experiments on `cycle.py` (copy): `__import__("subprocess").getoutput("true")` (M30) and `os.spawnlp(...)` (M31) both passed the guards. By reading: `importlib.import_module`, `os.exec*`, `asyncio.create_subprocess_shell` and `run(**{"shell": True})` also pass. The design lists only the three literal forms (design 788), so this is not a defect against the spec. | Optionally add a deny-list of `__import__`/`importlib` use of `subprocess` and the `os.exec*`/`os.spawn*`/`os.posix_spawn*` names. |
| N-3 | MINOR | `test_no_text.py:188-208,297-310` | `Run.check` never asserts `spy.unexpected == []`, although design 12 says an unknown argv "fails the test at teardown" and T9 relies on it. Experiment M12 (a `gh label create pwn` write call added to the launch step) survived `test_no_text.py` alone (168 passed) and was caught only by `test_security_invariants.py::test_prompt_regex_property` (the unexpected-argv assert at `:354` and the form scan). Suite-level cover exists, so no property is lost today. | Add `assert not self.world.runner.unexpected` to `Run.check`. |
| N-4 | MINOR | `conftest.py:1046-1065,992-1039` | The stub guard can be weakened by a future test: `write_scenario` accepts `argv_prefix: []` (a catch-all rule marks every call `matched`), and a stub that dies before logging (for example `IW_STUB_SCENARIO` naming a missing file) leaves no record for the teardown check. Rules also match by prefix, so extra trailing arguments are answered; the e2e exact-sequence assertions (`test_cli_e2e.py:353,431`) compensate. | Reject an empty `argv_prefix` in `write_scenario`; log the call record before reading the scenario file. |
| N-5 | MINOR | `test_security_invariants.py:250-262,857-860` | `classify_argv` leaves the discovery label (`argv[8]`) and assignee (`argv[10]`) unchecked and does not pin the REST flags between the path and `--jq`; `test_the_argv_scan_rejects_a_forbidden_argv` uses `pytest.raises(AssertionError)` with no `match`, so the rejection reason is not pinned (all 18 are rejected, reasons plausible when printed). The exact forms are pinned elsewhere (`DISCOVERY_ARGV` in `test_cli_e2e.py:46-61`, `test_github.py`). | Optional: assert argv[8] and argv[10] against the config label and the login pattern; add `match=` per bad argv. |
| N-6 | MINOR | `test_no_text.py:120-129,693` | `assert_state_dir_clean(skip=...)` skips by file name anywhere under the state tree. The only use skips `dispatch.json` in the damaged-store case (the canary is planted there), so a cycle that rewrote that file with extra text would go unseen. | Skip by relative path and assert the file is byte-identical to what the test wrote. |
| N-7 | MINOR | `test_security_invariants.py` (`run_world`), `test_crash_injection.py`, `test_cli_e2e.py:65-73` | These read the real `/proc/self/mountinfo` through the unpatched `cycle._read_mountinfo`, whereas `test_concurrency.py:48-51` and `test_no_text.py:242-247` patch it. Read-only and not HOME, state dir or repo tree, but a network-filesystem `tmp_path` changes results for the first two. The e2e file fails on purpose in that case (documented). | Patch `_read_mountinfo` in `run_world` and `Rig`, or document the dependency. |
| N-8 | MINOR | `conftest.py:1139-1145`; change set line 3 | The e2e child gets a five-key env with no `PYTHONDONTWRITEBYTECODE`, so it could write `.pyc` under `src/` when sources are newer than their cache (git-ignored). `tests/issue_watch/__pycache__` also still holds bytecode for four deleted scratch tests (`test_smoke_x`, `test_zz_scratch_world`, `test_tmp_orig`, `test_dbg_tmp`), which shows scratch files were created in the tree during Phase 8; the directory is ignored (`.gitignore:2`) and no source exists, so pytest does not collect them. | Optional: add `PYTHONDONTWRITEBYTECODE=1` to the e2e env (and extend the key-set assert); delete the four stale `.pyc` files. |
| N-9 | MINOR | `test_concurrency.py:134`; `test_crash_injection.py:9-11` | The loser's "exit 75" is the worker's own `sys.exit(res.exit_code)` of `run_cycle`, not a CLI process (the CLI mapping is pinned in `test_cli.py:438-472`); crash tests simulate a kill with an in-process `SystemExit`, as design 779 prescribes and the docstring says, so a real SIGKILL is not exercised. | None needed; recorded so nobody reads these tests as process-kill proof. |

## Actions Taken
None. `fix_authorization: false`. The only files written are this report and scratch files under `/tmp/secinv.*` and `/tmp/secinv-harness` (removed at the end of the run).

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
The spawn prompt carried no `## Inherited Structural Verdict` block, so standalone behaviour applied: no structural item was skipped on the strength of another report.
- Relied on rf-qa PASS for: none (no verdict was injected). The change-set file `phase-outputs/reports/gate-d-change-set.md` was used only for the file list and gate results; its line counts were re-checked with `wc -l` and match (1155, 443, 961, 373, 275, 191, 961, 375).

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No Inherited Structural Verdict was present in the spawn prompt (standalone fallback).

**(b) Independent semantic checks (>=1 required, INV-019):**
- PATH guard soundness -- verified by reading `conftest.py:1108-1155`, `test_cli_e2e.py:281-296`, and grep of the package for absolute-path lookups (none); `find -perm /111` empty.
- Argv allow-list is default-deny -- verified by running `classify_argv` over all 18 `BAD_ARGVS` (script in `/tmp/secinv-harness/bad_argv_reasons.py`): all rejected; and by mutation M1 (drop `--method GET`), M2 (ask for `title`), M4 (extra launch flag), M12 (write call), each caught by the Phase 8 set.
- Prompt boundary -- mutations M3 (`isinstance` instead of `type(n) is int`) and M27 (`match` instead of `fullmatch`) caught by `test_prompt_regex_property`; M24 to M26 (open login, int and cursor patterns) survived the Phase 8 files alone and were caught by `test_github.py` in the full `tests/issue_watch` run.
- At-most-once and lock -- M5 (delete the pending save before the launch), M7 (lock never released) and M10 (sweep skips pending) caught by `test_crash_injection.py`; M6 (non-exclusive lock) caught by `test_concurrency.py`.
- No text leaks -- M8 (exception text appended to the crash line) caught by `test_no_text.py::test_crash_line_names_the_exception_class_never_its_text`; M12 survived that file alone (note N-3).
- Static no-shell guard -- M9 (`shell=True` in `runner.py`) and M11 (`import subprocess` in `github.py`) caught; M30, M31 and a subpackage file survived (notes N-1, N-2).
- No real HOME use -- ran three Phase 8 files with an empty `HOME`, `XDG_STATE_HOME` unset and a separate `UV_CACHE_DIR`: 189 passed, `find $HOME -mindepth 1` printed nothing.
- Secret scan -- grep of fixtures and test files for token and key patterns: none.

**Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 41 | Grep: 17 | Glob: 0 | Bash: 15 (counts are approximate; the Bash calls are the /tmp copy, baselines, mutation runs and the HOME check; Read+Grep exceed the 16 checks).
**Web research:** none performed; Tavily not needed.
**Other-lens boundary:** design-correctness and test-adequacy items (for example the DF-15 rerun expectations and xdist flakiness) were read only where they touch a security property; no finding is raised on them here.

## Recommendations
- Proceed: no blocking finding. Carry N-1 to N-9 forward as minor notes (never rechecked).
- If one change is made, take N-3 (a one-line assert) and N-1 (`rglob`), the two that close an actual hole in a guard.

## QA Complete
