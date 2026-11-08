# QA Report - test-adequacy lens (Final gate, Step 9.F6)

**Topic:** issue-watch implementation, tests/issue_watch/
**Date:** 2026-11-08
**Phase:** task-qualitative (test-adequacy lens)
**Fix cycle:** 1 (report only, fix_authorization: false)

## Overall Verdict: FAIL (4 blocking findings: TA-1, TA-2, TA-3, TA-4; 11 minor notes)

## 1. Scope, method and environment

- Report-only lens (fix_authorization: false). Repository files were not modified; the only file written inside the repository is this report. Mutation work ran on copies under `/tmp/mutwork-tadq*` (eight working copies of `src/superclaude/` + `tests/issue_watch/`, one per parallel lane); all were removed at the end (section 10).
- Inputs read: `final-change-set.md`; the tests of `tests/issue_watch/` that carry a lens-listed property (`test_audit.py` 1-260, `test_crash_injection.py`, `test_concurrency.py`, `test_runner.py`, `test_no_shell.py`, `test_module_boundaries.py`, `test_marker_contract.py`, `test_cli_e2e.py`, `test_security_invariants.py` 160-520, `test_no_text.py` 1-330, `test_github.py` 1-360, `test_launch.py` 1-250, `test_record.py` 1290-1580, `test_cycle.py` 96-220, 560-940, 3975-4670, `test_cli.py` 700-1040, `conftest.py` 1-330 and 1060-1155) and the modules they test (`predicates.py`, `launch.py`, `runner.py`, `cycle.py`, `github.py` 30-960, `record.py` 120-866, `audit.py` 100-400, `cli.py` 30-348).
- Baseline run on this checkout (uid 1000): `uv run pytest tests/issue_watch/ -q -rs` = 2628 passed, 0 skipped, 17 s.
- Branch coverage (`uv run --offline --with pytest-cov`, data file under `/tmp`): 98 % overall (2297 statements, 26 missed; 686 branches, 20 partial). Missed lines are listed in section 5.
- Mutation harness: each mutant is ONE exact-once text replacement applied to a copy of one module. The copy's `tests/issue_watch` is the original plus two edits that make a mutant visible to the `test_cli_e2e.py` child process (`conftest.stub_path` gets a `PYTHONPATH` entry that points at the copy; `test_ac1_fixture_guard...` accepts that key). Run: `pytest tests/issue_watch -x`. KILLED = some test fails; SURVIVED = all 2628 pass; ERROR = the replacement text did not match exactly once (re-run with corrected text where it mattered). Kills were checked for flaky-timing causes (none: no kill names `test_concurrency`, `test_runner` or a timeout).
- Grading rule used for a SURVIVING mutant (stated so the split is reproducible): BLOCKING when the mutant is observable in a reachable state AND it breaks a sentence the spec, the design or a plan row states as behaviour (a missing required test: spec-final.md:361 "Each FR criterion and each Section 7 row is one test case"); MINOR when the mutant is equivalent in every reachable state, or the guarded step is redundant with a second check, or the behaviour is only a hygiene detail the design does not state.

## 2. Lens checks (the named items of the lens prompt)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Reason pin | PASS (note TA-13) | `test_audit.py:214-227`: `EXPECTED_NAMES` (59 literal names, lines 39-99) and `EXPECTED_TABLE` (59 literal `(kind, exit)` pairs, lines 102-162) are typed in the test, never imported; `REASONS == frozenset(...)`, `list(REASON_TABLE) == EXPECTED_NAMES`, `REASON_TABLE == EXPECTED_TABLE`. The count is 59, not the 57 the lens prompt and the plan name: spec-final.md:332-358 gives 52 names, DF-02/03/22/57 add 5 (= 57), Gate C fixes C-2/C-3 add `cycle_complete` and `cycle_crashed` (= 59). I counted the spec rows myself (52). Meaningful: every name has its exit and kind pinned, and `test_cycle.py:876-913` pins 31 reason-to-exit pairs a second way. |
| 2 | 12-element launch argv | PASS | `test_launch.py:75-92` (literal 12 elements), `:102-109` (five flags, no permission flag), `:117-146` (19 refused prompts), `:152-171` (retry argv), `test_security_invariants.py:204-219` and `:290-296` (literal argv rebuilt independently and compared for every launch of every scenario), `test_cli_e2e.py:242-277,357-368` (the child process reaches the stub with exactly these 12 elements). Mutants L1, L2, L10, L11, L12 (agent id, surface, bool accepted, retry flag position, `path:` selector) all killed. |
| 3 | Five crash points, five reruns | PASS | `test_crash_injection.py`: C1, C2 (patched `os.replace`, orphan tmp file asserted), C3, C4, C5 plus an exception out of the launcher; `RERUNS = 5` (line 36) and `reruns()` (131-149) asserts five more real cycles each, `launcher_calls <= 1` after every one, `launches == 1` once a launcher call exists, lock free after `SystemExit`. Mutant C13 (remove the `pending` save before the launch) killed; C14, C16-C21 (disabled mid-cycle, approval re-check, origin re-check, cut-off) killed. |
| 4 | Two-process lock test | PASS | `test_concurrency.py:146-187`: real `spawn` processes ordered by files, not sleeps; worker 1 proves it holds the lock from inside the launcher (`_lock_is_held`), worker 2 must exit 75 with zero runner and launcher calls; all waits are bounded polls (`WAIT_S` 30, `JOIN_S` 60, `terminate()` in `finally`). One masking weakness: TA-9. |
| 5 | 50-cycle and acceptance-property tests | PASS | `test_cycle.py:4024-4061` (50 cycles, changing world: failures, claims, re-approval, issues leaving discovery; per-cycle `made in (0, 1)`, every entry `launches <= 1`, the 24 h window never holds more than 6, all four states seen); `:4069-4118` (N in 1, 2, 6, 7, 50, 99: 48 half-hour cycles, exact day-cap set, second day launches `min(N-6, 6)`, one per cycle). Mutants C1, C2, C10, R4, R8, R9, R10 killed. |
| 6 | AST tests | PASS with limits (TA-12) | `test_no_shell.py` and `test_module_boundaries.py` each carry positive and negative self-tests (21 + 15 and 35 + 18 synthetic sources), so the scans cannot pass vacuously. The mutant N1 (`shell=False` to `True` in `runner.py`) was void (the string occurs twice); the property is pinned instead by `test_runner.py:82-95` (`kwargs["shell"] is False` on the call that reaches `subprocess.run`, list-only argv, `stdin=DEVNULL`) and by the scanner's own positive case `shell=True` (`test_no_shell.py:206,257-261`). |
| 7 | Hostile-text test | PASS | `test_no_text.py`: canary `PWNED-TITLE` in label names, logins, extra `title`/`body` fields, non-JSON stdout and over-500-byte stderr, run through the real CLI for `once`, `once --dry-run` and `status`; every scenario proves the canary was served (`SpyRunner.canary_served`), scans every file under the state directory including rotated audit files, every argv and prompt, and the command output; the checkers have their own positive tests (lines 188-208 and the self-tests below). Mutants K19 (print the exception text) and K17/K18 killed. |
| 8 | Vacuous assertions | PASS | AST scan of all 21 files (`/tmp/mutwork-tadq/astscan.py`, read-only): 29 test functions without a direct `assert`; I read every one (`test_cycle.py:153-374, 506-521, 625-792`, `test_record.py:841, 2213, 2222`) and each calls the asserting helper `_expect(...)` or `pytest.raises`; 7 `assert <name>` and 7 `is not None` shapes are guarded by an equality assertion in the same function; the one `assert a or b` (`test_cycle.py:4041`) is the property "no launch, or a launch that is an unknown outcome". No `assert True`. |
| 9 | Expectations derived from the code under test | PASS with notes | Pins are literal copies: reason table (check 1), argv G1-G7 (`test_github.py:119-259`, constants copied at lines 37-76), the closed audit key set (`test_no_text.py:70-80`), config limits and exit precedence (`test_cycle.py:809-873`, an exhaustive subset test over the 7 codes). Derived-from-source spots, each backed by an independent literal elsewhere: `FakeLauncher.launch` calls the production `launch_argv`; `GhWorld` keys its script by the production `github.argv_*`; `test_cli.py:845` builds the expected retry text with production `retry_argv`; `test_module_boundaries.py` relaxes the design (TA-14). |
| 10 | Missing negative and boundary cases | FAIL | Mutation + coverage found them: section 4 (blocking TA-1 to TA-4; minor TA-5 to TA-9 and TA-15). |
| 11 | Hostile or boundary value never enters the system | PASS | Hostile issue numbers: `test_github.py:355-362,1286` (bad number in discovery is `non_json`), `:2069-2150` (trigger, login, cursor); `test_security_invariants.py:451-513` (seeded 1,600-draw property over nine value families, then full cycles at 1, 9 and 999999999); hostile labels, logins, assignees, config labels and own login at `:521-610`. Boundary values: 100 results, 99 results, 20/21-digit approver ids, 50/51-char labels, 1 MiB/1 MiB+1 approvers file, 120/121 s, 24 h exactly, 10 min exactly, 60 min exactly are pinned at one step each side. |
| 12 | Wall clock, real HOME, PATH, network, path outside `tmp_path` | PASS with notes | `FakeClock` everywhere; `HOME`/`XDG_STATE_HOME` set by autouse fixtures (`test_cycle.py:62-64`, `test_no_text.py:243-247`, `conftest.tmp_state`); `test_cli_e2e.py` runs the child with a curated five-key environment and a stub-only `PATH`; `refuse_real_processes` makes any real `SubprocessRunner.run` a failure. Exceptions: `test_marker_contract.py:22-24,34-39` reads the real `~/.claude` (TA-11); `test_cli_e2e.py:190-192` uses `datetime.now()` for the world clock (the child's store is stamped by the real clock; drift over 60 s only adds a `clock_skew` warning line, which no assertion forbids); `test_origin_parity.py:23-27` and `test_cycle.py:4642-4648` read repository / `/proc` files read-only; loading `origin_repo.py` by path writes a `__pycache__` next to the source (git-ignored, TA-11). No network call exists (`grep` for socket/urllib/requests: none; `socket.gethostname` is patched or compared with itself). |
| 13 | Flaky under xdist | PASS | section 6: two xdist runs. Shared names: none (every test uses `tmp_path`); the spawn worker imports `tests.issue_watch.test_concurrency` by name, which resolves because `tests/__init__.py` exists. Process-global state touched: `os.umask` (restored in `finally`, `test_record.py:636-641,1772-1777,2004-2008`), `os.geteuid` / `sys.platform` / `os.replace` (monkeypatch). |
| 14 | Joins without timeouts | PASS | Every `join` has a timeout (`test_concurrency.py:161-169`); `subprocess.run` in `test_cli_e2e.py:103-123` has `timeout=60`; the runner timeout test sleeps 5 s inside a child killed at 0.5 s and asserts `elapsed < 4.0` (`test_runner.py:217-226`). No `Popen`, `communicate`, `Thread` or bare `wait`. |
| 15 | Pytest markers | PASS | No custom marker and no `pytestmark`; the only `pytest.mark` use besides the five skip sites of check 16 is the built-in `parametrize`. `--strict-markers` is on in `pyproject.toml:112-116`, so an unregistered marker would fail collection. research/03:13 allows built-ins. |
| 16 | Skipped tests | PASS for the recorded runs; MINOR note TA-10 | See section 3. |
| 17 | A test that weakens an earlier assertion | UNVERIFIABLE | `tests/issue_watch/` is untracked (no history to diff). The Gate A and Gate D fix reports state "no assertion was weakened or deleted" (`qa/gate-a/qa-fix-report.md:6`, `qa/gate-d/qa-fix-report.md:6`); that is reliance, not verification. The one relaxation I could see in the files is TA-14. |

## 3. The skip question (judged by the definition)

The plan forbids `pytest.skip`, `skipif` and `xfail` (TASK-RF file, lines 188 and 581: "because gates G-1 and G-3 require zero skipped tests"). Grep of `tests/issue_watch/` finds these sites, all root guards except the last:

| Site | Test (cases) | Guard |
|---|---|---|
| `test_record.py:739` | `test_ac11_unopenable_lock_file_is_lock_invalid__fr017` (1) | `skipif(os.geteuid() == 0)` |
| `test_cycle.py:735` | `test_validate_approvers_unreadable_file__fr027` (1) | `skipif(os.geteuid() == 0)` |
| `test_cli.py:892` | `test_status_exits_6_for_an_unreadable_store` (1) | `skipif(os.geteuid() == 0)` |
| `test_cli.py:995` (`NOT_ROOT`) used at `:1184`, `:1552` (two parameters), `:1578` | init-state parent not writable (1), reset in an unwritable state directory (2), refusal in an unwritable state directory (1) | `skipif(os.geteuid() == 0)` |
| `test_cycle.py:4643-4644` | `test_the_real_proc_mountinfo_gives_a_filesystem_type_for_the_root__df52_c13` (1) | `pytest.skip` when `sys.platform != "linux"` |

Judgment: **minor (TA-10), not blocking.** The rule exists to keep the zero-skip gates true, and in every recorded and re-run Linux, non-root run nothing is skipped: my run `2628 passed` with `-rs` printed no skip line, and two xdist runs gave `2628 passed` twice. A permission-bit test cannot fail under root, so the guard is the honest outcome there, and the product is Linux-only by design (design line 69), so the platform guard never fires on a supported host. It remains a letter violation of the plan, and it has one real cost: run as uid 0 (a root container, or CI as root), 7 failure-path cases (unwritable state directory, unreadable approvers file and store, unopenable lock) vanish silently and gate G-3 ("zero skips") fails; the 8th skippable case is the Linux-only platform one. Cheap fix: drive those cases with a monkeypatched `os.open` / `Path.write_bytes` that raises `PermissionError`, as `test_record.py:754-759` and `test_cycle.py:680-690` already do for `geteuid`.

## 4. Mutation and coverage findings

Totals: 289 mutant runs = 284 distinct mutants (5 first attempts whose replacement text did not match were re-run with corrected text and killed: C56, G18, G25, L9, R12). 6 are void and not counted (G36 and X16 were typing slips that replace a string with itself, K9 is a no-op `; pass`, N1 and S8 and X15 had replacement text that matches twice or zero times). Valid mutants 278: **255 killed, 23 survived** (91.7 % killed; 94.8 % after removing the 9 survivors I show below to be equivalent or unreachable). The 255 kills include: every `predicates.py` mutant except the two equivalent ones (approval order, bots, outsiders, edit-after-approval, window edges, Project item), every `record.py` constant and transition guard but R20, every `github.py` argv, cap and classification, the `launch.py` argv and outcome mapping, the audit schema and rotation, and in `cycle.py` the exit precedence, every deadline and cap constant, the revalidation steps, the dry-run isolation, the pre-launch `pending` save (C13), the mid-cycle disable (C14), and the CLI reset / status / once paths.

### 4.1 Survivors that are blocking

**TA-1 (blocking). `status` prints a retry command for every state, not only `unknown`.** Mutant Q19 (`cycle.py:1271`, `if entry.state == "unknown" and entry.operation_id and entry.launch_cwd:` reduced to `if entry.operation_id and entry.launch_cwd:`) survives all 2628 tests. Design 10.2 line 739: `retry` = "`unknown` entries with an `operation_id`"; AC-9 (design line 882). The only store that feeds `status` retry tests is `seed_rich_store` (`test_cli.py:717-762`): two `unknown` entries, one stale `abandoned` without an operation id, one `claimed` without one. No test has a `launched`, `claimed` or `abandoned` entry that carries `operation_id` and `launch_cwd`, and every normal launch produces exactly that. Demonstrated on the copy (`/tmp/mutwork-tadq5/demo_q19.py`, record API only): after `mark_pending` + `mark_launched(op-9)`, the unmutated `status_report` returns `retry: []`, the mutant returns a full `--retry-launch op-9` command for the successfully launched issue. Fix: add a case with `launched`, `claimed` and `abandoned` (`claim_not_observed`) entries that carry an id and a cwd, and assert they are absent from `retry` in `status --json` and in the text form.

**TA-2 (blocking). FR-023 "written only on cycles that examined something" is not tested.** Mutants C49 and V19 (`cycle.py:1097`, `if self.examined and self.discovered is not None:` reduced to `if self.discovered is not None:`) survive. spec-final.md:166 states the sentence; design line 356 (step 13). With nothing examined the mutant still prunes `considered` to the discovery set and forces a save, so a stale `considered` entry disappears on an idle or all-`budget_exhausted` cycle, which the spec says must not happen. No test seeds a `considered` entry outside the discovery set and then runs a cycle that examines nothing (`test_ten_skipping_candidates_...` examines 8 issues). Fix: store with `considered = {5: t}`, discovery `[]`, assert `considered` is unchanged after the cycle; and the same with a discovery whose only candidate is `budget_exhausted`.

**TA-3 (blocking). `consumed_log` pruning "in every saving cycle" is not tested.** Mutant V21 (`cycle.py:1105`, `self.doc = record.prune_consumed_log(doc, now)` reduced to `self.doc = doc`) survives. Design 7.5 table, line 501: "`consumed_log` pruning | drop t <= now − 24 h | done in every saving cycle and in `reset`". `record.prune_consumed_log` and the `reset` path are tested (`test_record.py:1308-1318`, `test_cli.py` reset cases; mutants R11 and R12 are killed), but no test runs a cycle against a store whose `consumed_log` holds a time at or before `now - 24 h` and reads the file back. Day-cap counts are unaffected (they window-check on read), so the omission is silent: times that `reset` appended stay in `dispatch.json` until the next reset instead of leaving at the next saving cycle. Fix: one cycle test with `consumed_log = (now - 24h, now - 24h + 1s)`, assert only the second survives the cycle's final save.

**TA-4 (blocking). `once` is not checked for the Linux-only gate at the CLI.** Mutant K13 (`cli.py:120`, `config = _load_config(config_path)` in `once_command` changed to `platform=False`) survives. Design line 69: "Platform: Linux only; `once`, `check-config`, `init-state` exit 2 elsewhere." Tests monkeypatch `sys.platform` to `darwin` for check-config (`test_cli.py:415-421`), init-state (`:1219-1225`) and reset (`:1292-1299`) only; the unit test `test_cycle.py:570-579` covers `check_platform`, which `run_cycle` never calls (its docstring, `cycle.py:1180`, makes it the caller's job). The one command a timer runs has no test that it refuses a non-Linux host. Fix: a `once` and a `once --dry-run` case with `sys.platform = "darwin"` expecting exit 2, `platform_unsupported` on stderr and no runner call.

### 4.2 Survivors that are minor

**TA-5 (minor). The `re-approved` decision note can never be written, and nothing tests the code that would write it.** V5 (`note = None`) and V6 (condition inverted) survive. `_issue_line` (`cycle.py:635-642`) compares `e.approval_event_id` with the current approval, but `_examine` (`cycle.py:896-942`) only computes an approval for candidates that have no entry or a `failed` / attempts-exhausted entry, whose approval ids are null; for `launched`, `unknown`, `claimed` and dispatched `abandoned` entries it returns before any approval is computed. So `reapproved` is false in every reachable state. The plan records this openly as OQ-49 (TASK-RF file, line 960: "This task adds no code for it"), yet `cycle.py` carries code that looks like it does; spec-final.md:272 and 357 still say a newer approval "is reported as re-approved". Not a test defect I can fix with a test: the design lens owns the open question. Either delete the dead branch or build the state in a test and implement the read.

**TA-6 (minor). The cut-off check before the second `git` origin call has no test.** C22 (`cycle.py:1039-1040`) survives; C21 (the check after the call, `:1048`) and the 5 s floor are killed. Design 646-647 forbids starting the Orca launch after 120 s and a `git` call under 5 s left; it does not forbid a `git` call between 120 s and 235 s, and the post-call check still stops the launch. The Gate C fix comment (`cycle.py:1035-1038`) says no git call starts after the cut-off; `test_cycle.py:4302-4326` documents "the pre-check passes (115 <= 120)" but never drives the clock to 130 s to see the pre-check refuse. Add one case.

**TA-7 (minor). The day-cap re-check inside the launch step never executes.** C15 (`cycle.py:1031-1032`) survives and coverage reports line 1032 as never run. Design line 355 lists it in step 12. Under the lock and a forward clock the count cannot rise between the check at `:917` and this one, so it is a redundant guard; a test needs a clock stepped backwards or a future-dated `consumed_at`. Either test that, or drop the guard.

**TA-8 (minor). Untested validators and boundaries** (each found by coverage or a surviving mutant, none guards a stated invariant): `LaunchOutcome.__post_init__` (`launch.py:251-259`, the four `raise` lines 253/255/257/259 never execute; `cycle.py:1065` relies on the "launched needs an id" rule); short audit write (A5, `audit.py:138-139`); SLO lease-end boundary `now >= end` (Q24, `cycle.py:1361`); `status` is allowed on a non-Linux host (K11, `cli.py:169`; no sentence in the design requires it); dry-run shadow retention `t > cutoff` (V22, `cycle.py:1121`); `cli.py:45-46` (`~` expansion failure) and `cycle.py:190-191` (no home directory); `cycle.py:1279-1280` (an unprintable operation id in `status`, unreachable because `record.validate` already rejects it, `record.py:183`); `github.py:414`, `record.py:787-788,799-800`.

**TA-9 (minor). The lock inode check is masked.** R20 (`record.py:411-412`, the `st_dev, st_ino` comparison replaced by `False`) survives, and coverage shows the `st_nlink == 0` raise at `record.py:413-414` never executes. The one scenario tested (`test_concurrency.py:255-275`, `os.replace` of a fresh file over the lock) is caught by whichever check runs first, and the old inode loses its only link, so removing the inode comparison changes nothing the tests see. FR-017 "lock replaced → 75" is covered; the isolating case (hard-link the lock first so the old inode keeps `nlink` 1, then replace the path) is missing. The `nlink` raise is dead code.

**TA-15 (minor, notes). Equivalent or unreachable survivors, listed so nobody chases them:** P1 (`predicates.py:228`, `<=` to `<`: equal timestamps already return `events_incomplete` at `:206-209`); P23 (`predicates.py:37`, `fullmatch` to `match`: `strptime` rejects trailing text); C5 (`cycle.py:456`, only differs for an exit code outside the precedence list and 75); C11 (`cycle.py:901`, `pending` entries are swept before they are examined); A8 (`audit.py:120`, `json.dumps` already escapes to ASCII); X9 (`cycle.py:989`, `not again.approved` is implied by the event-id comparison); X14 (`cycle.py:836-837`, `marker_in_window` already returns False without a floor); V9 (`cycle.py:1130-1131`, exit != 0 with a different `stop_reason` cannot occur after a launch step halts the cycle); Q13 (`cycle.py:321`, `O_NOFOLLOW` after an `lstat` regular-file check is a TOCTOU guard that a test cannot force).

### 4.3 Coverage

Branch coverage 98 % (`predicates.py` 100 %). Uncovered statements: `audit.py:139`; `cli.py:45-46`; `cycle.py:190-191, 366, 370 (Protocol bodies), 837, 1032, 1129->1132, 1130->1129, 1279-1280, 1351->1333`; `github.py:414`; `launch.py:253, 255, 257, 259, 269`; `record.py:164, 228, 414, 787-788, 799-800` and the `->exit` branches at 323-331 (Protocol bodies); `runner.py:45, 54`. Everything that is not a Protocol body or a documented dead guard is named in TA-5 to TA-9.

## 5. Findings from reading the tests (not mutation)

**TA-10 (minor).** The skip sites of section 3.

**TA-11 (minor). Environment touches outside `tmp_path`.** (a) `test_marker_contract.py:22-24,34-39` reads the real `~/.claude/skills/sc-issue-protocol/**` and fails if an installed older copy lacks the marker; the plan says "the real HOME" is forbidden and the test is the DF-46 decision, read-only, absent folders pass. (b) `test_origin_parity.py:23-27,116` loads `origin_repo.py` by path; Python writes `src/superclaude/skills/sc-issue-protocol/scripts/__pycache__/` (exists, git-ignored). (c) `test_cli_e2e.py:65-73,301` fails if `tmp_path` is on a network filesystem (documented as a failure, not a bypass). None is flaky on the supported host.

**TA-12 (minor). The AST scanners are heuristics.** `test_no_shell.py` and `test_module_boundaries.py` do not see `subprocess.run(**{"shell": True})` (a keyword unpack has `kw.arg is None`), `__import__("subprocess")`, `importlib.import_module`, or the `os.exec*` / `os.spawn*` / `pty.spawn` family. No such call exists today, so nothing fails; the scans pin the forms the design names, not the property. Add the cases to the self-test tables if the property matters.

**TA-13 (minor). The reason pin is 59 names, the plan and the lens prompt say 57; the module docstring miscounts.** `test_audit.py:3-9` says "the five proposals DF-02, DF-03, DF-22 and DF-57" and lists four ids, plus the two Gate C names. The assertion itself (`:214-220`) is correct and literal (59). Fix the docstring and the plan text.

**TA-14 (minor). One test rule is looser than the design it names.** `test_module_boundaries.py:20-21` and `:57-61` let `record` import any name from `predicates`, while design line 239 says "`predicates` (types only, for `Entry` fields that hold an issue number)". `record.py` imports four functions and a type (gate D finding D-6 recorded only the docstring count). `predicates` is pure, so no harm, but the test encodes the code, not the design. Align the design text or tighten the rule.

## 6. Flakiness and isolation runs

Two runs of `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/`: `2628 passed in 6.43s` and `2628 passed in 6.51s`, no skip, no warning. The seven mutation lanes (up to seven concurrent pytest runs on a loaded 28-core host) produced no timeout-caused kill.

## 7. Items Reviewed (format table with the axis column)

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Reason pin (59 literal names and pairs) | none | PASS | section 2 row 1 |
| 2 | 12-element launch argv | none | PASS | section 2 row 2 |
| 3 | Five crash points, five reruns | none | PASS | section 2 row 3 |
| 4 | Two-process lock test | none | PASS | section 2 row 4 (TA-9 is a minor masking note) |
| 5 | 50-cycle and acceptance-property tests | none | PASS | section 2 row 5 |
| 6 | AST tests (no-shell, module boundaries) | none | PASS | section 2 row 6 (TA-12 minor) |
| 7 | Hostile-text test | none | PASS | section 2 row 7 |
| 8 | Vacuous assertions | none | PASS | section 2 row 8; all 7 `assert <name>` and 7 `is not None` lines read in context and guarded by exact assertions |
| 9 | Expectations derived from the code under test | none | PASS | section 2 row 9 (TA-14 minor) |
| 10 | Missing negative and boundary cases | AX-3 | FAIL | TA-1 to TA-4 blocking; TA-5 to TA-9, TA-15 minor |
| 11 | Hostile or boundary value never enters | none | PASS | section 2 row 11 |
| 12 | Wall clock, real HOME, PATH, network, outside `tmp_path` | none | PASS | section 2 row 12 (TA-11 minor) |
| 13 | Flaky under xdist | none | PASS | section 6 |
| 14 | Joins without timeouts | none | PASS | section 2 row 14 |
| 15 | Pytest markers | none | PASS | section 2 row 15 |
| 16 | Skipped tests, root guards, platform guard | none | PASS (TA-10 minor) | section 3 |
| 17 | Weakened earlier assertion | none | UNVERIFIABLE | no history; section 2 row 17 |

## 8. Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| TA-1 | IMPORTANT (blocking) | `cycle.py:1271` / `test_cli.py:717-762,768-848` | `status` retry list for non-`unknown` states untested; mutant Q19 survives; a launched entry would print a retry command (demonstrated) | add `launched`, `claimed`, `abandoned` entries with `operation_id` + `launch_cwd` and assert they are not in `retry` (JSON and text) |
| TA-2 | IMPORTANT (blocking) | `cycle.py:1097` / spec-final.md:166 | FR-023 "written only on cycles that examined something" untested; mutants C49 and V19 survive | cycle test with a stale `considered` entry and a cycle that examines nothing (idle; all `budget_exhausted`): `considered` unchanged |
| TA-3 | IMPORTANT (blocking) | `cycle.py:1105` / design line 501 | `consumed_log` pruning "in every saving cycle" untested; mutant V21 survives | cycle test with `consumed_log` times at and just after `now - 24 h`; only the later one remains in the file |
| TA-4 | IMPORTANT (blocking) | `cli.py:120` / design line 69 | `once` Linux-only gate has no CLI test; mutant K13 survives | `once` and `once --dry-run` under `sys.platform = "darwin"` exit 2, `platform_unsupported`, no runner call |
| TA-5 | MINOR | `cycle.py:635-642` | `re-approved` note branch unreachable and untested (OQ-49 tracks the missing emission) | design lens: implement the read or delete the branch |
| TA-6 | MINOR | `cycle.py:1039-1040` | cut-off check before the second `git` call untested (C22) | one case at 130 s expecting a single origin call |
| TA-7 | MINOR | `cycle.py:1031-1032` | step-12 day-cap re-check never executes (C15) | backwards-clock test, or drop the guard |
| TA-8 | MINOR | `launch.py:251-259`, `audit.py:138-139`, `cycle.py:1361`, `cli.py:169`, `cycle.py:1121` and others | validators and boundaries untested (section 4.2) | add the cases listed there |
| TA-9 | MINOR | `record.py:411-414` | inode comparison masked by the `nlink` check (R20); the `nlink` raise is dead | hard-link-then-replace test; delete the dead check |
| TA-10 | MINOR | 8 test cases in 5 files (section 3) | `skipif` / `pytest.skip` contradict the plan letter; nothing skipped in recorded runs | replace root guards with monkeypatched `PermissionError` |
| TA-11 | MINOR | `test_marker_contract.py:22-24`, `test_origin_parity.py:23-27`, `test_cli_e2e.py:65-73` | reads real `~/.claude`; writes a git-ignored `__pycache__` outside `tmp_path`; fails on a network `tmp_path` | none required; document |
| TA-12 | MINOR | `test_no_shell.py`, `test_module_boundaries.py` | scanners miss `**{"shell": True}`, `__import__`, `importlib`, `os.exec*` | extend the self-test tables |
| TA-13 | MINOR | `test_audit.py:3-9` | docstring miscounts (five proposals, four ids); plan says 57, test pins 59 | fix the docstring and plan text |
| TA-14 | MINOR | `test_module_boundaries.py:20-21,57-61` / design line 239 | rule for `record` imports from `predicates` is looser than the design | align design or tighten the rule |
| TA-15 | MINOR | section 4.2 | nine equivalent or unreachable survivors | none |

## 9. Summary

- Checks passed: 15 / 17 (row 10 failed, row 17 unverifiable); Checks failed: 1
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)
- Blocking findings: 4 (TA-1, TA-2, TA-3, TA-4); minor notes: 11 (TA-5 to TA-15)
- drift-axis-inactive

## 10. Actions Taken

None in the repository (fix_authorization: false). Mutation copies under `/tmp/mutwork-tadq*` were created and then removed; `ls -d /tmp/mutwork-tadq*` reports nothing and `git status --short` outside `.dev/` is identical to its state at the start (`src/superclaude/cli/main.py` modified, the designs, package and tests untracked, as before). The coverage data file was written to `/tmp` and removed with them.

## 11. Inherited Structural Verdict - Reliance Audit and Self-Audit

No `## Inherited Structural Verdict` section was supplied in the spawn prompt; this review ran standalone and relied on no inherited PASS item.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None (no inherited verdict was provided).

**(b) Independent semantic checks (>=1 required, INV-019):**
- Reason-table pin is literal and complete - verified by counting the spec rows myself (`spec-final.md:334-358` = 52 names) and reading `test_audit.py:39-162` (59 names and pairs).
- Test adequacy of every design rule by mutation - 278 valid mutants run on `/tmp` copies, 255 killed, 23 survived; four survivors reduced to blocking findings after I confirmed reachability in the source (`cycle.py:1271`, `:1097`, `:1105`, `cli.py:120`) and absence of a covering test by grep of `tests/issue_watch/`.
- TA-1 demonstrated, not inferred - `/tmp/mutwork-tadq5/demo_q19.py` printed `retry: []` unmutated and a full `--retry-launch op-9` command for a launched entry under the mutant.
- Equivalent-mutant claims - each of P1, P23, C5, C11, A8, X9, X14, V9, Q13 traced to the guarding line in the source before being called equivalent.
- Branch coverage 98 % measured with `pytest-cov`; every uncovered line mapped to a finding or to a Protocol body.
- Skip judgment - grep of all `skip` sites, a `-rs` run (0 skipped) and two xdist runs (0 skipped).

**Confidence:** Verified: 16/17 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: ~45 | Grep: ~45 | Glob: 0 | Bash: ~60 (the mutation drivers, the AST scan, the coverage and xdist runs, and the cleanup)
**Unverifiable:** row 17 (weakened earlier assertion): `tests/issue_watch/` is untracked, so there is no earlier version to diff.
**Tavily:** no external lookup was needed or made.

## Recommendations

1. Fix cycle (blocking): add the four tests of TA-1 to TA-4. All four are test-only; no source change is needed, and each fails today against the named mutant.
2. Optional in the same pass: TA-6, TA-7, TA-9 (three small cases) and replace the root guards of TA-10 so a root run keeps the failure-path coverage.
3. Ask the design lens to decide TA-5 (OQ-49): the `re-approved` branch is dead code until the owner decides.

## Overall Verdict: FAIL (4 blocking findings: TA-1, TA-2, TA-3, TA-4)

## QA Complete
