# QA Report — Gate D design-correctness lens (task-qualitative)

**Topic:** issue-watch Phase 8 (cross-cutting tests)
**Date:** 2026-11-08
**Phase:** task-qualitative (design-correctness lens)
**Fix cycle:** N/A (report only, fix_authorization: false)

---

## Overall Verdict: PASS (with minor notes; blocking findings: 0)

Binding sources read and compared with the code of the tests: `docs/designs/issue-watcher.md` lines 205-250, 334-363, 495-583, 640-700, 755-800, 870-899; `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` lines 112-257 (FR-001 to FR-029, NFR-001 to NFR-013); `research/06-gap-fill-decisions.md` Tables 1.2 to 1.4 and rows DF-10, DF-12, DF-15, DF-28, DF-29, DF-31, DF-34, DF-39, DF-55, DF-56 (DEVIATION rows treated as overriding the design text they name, and not reported); task items 8.1 to 8.8 and the Step 8.G5 prompt. All eight Phase 8 files were read in full.

## Items Reviewed

The 15 task-qualitative checks are adapted to the lens: "does this Phase 8 test encode the contract of its binding source correctly".

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate and command dry-run: the gate commands the tests encode match the sources | none | PASS | `gate-d-change-set.md` lists G-1 (2616 passed), G-3 (2616 passed, xdist), G-8 (NO_MATCH), G-5; commands equal research/06 Table 1.2 rows G-1, G-3, G-8, G-5. I did not re-run them (lens agent 1 does). A patched copy of `test_no_text.py` under /tmp (assert no unscripted argv at the end of each scenario) ran 168 passed, so no hidden exit-99 argv exists in that file. |
| 2 | Project convention: DF-31 (no test reads `.dev/` or the design), DF-39 (only `tmp_path`, HOME and XDG patched), DF-10 (nothing executable committed) | none | PASS | Grep over the 8 files for `\.dev/`, `docs/designs`, `brainstorms`, `spec-final`, `Path.home`, `expanduser`: no hit; `os.environ` only inside the stub template and a `no_shell` negative fixture string. `stub_path` writes stubs into `tmp_path` at test time (conftest.py:1108-1151); `find -perm /111` in the change set printed nothing. |
| 3 | Intra-phase order: 8.1 conftest part 5 precedes the tests that use `stub_path`, `write_scenario`, `read_calls` | none | PASS | `test_cli_e2e.py` imports `STUB_TOOLS`, `read_calls`, `write_scenario` from conftest part 5 (conftest.py:968, 1046, 1068); `test_no_text.py` imports `write_scenario` and uses `stub_path`. |
| 4 | Stub protocol equals research/06 Table 1.4 line by line | none | PASS | Location (`stubbin`, `linkbin`), four stubs with `#!/usr/bin/env python3` and mode 0o755 (conftest.py:973, 1135), `linkbin/python3` symlink to `sys.executable` only (1136), PATH exactly `stubbin:linkbin` (1140), scenario JSON with first-prefix-wins (989-994), exit 99 with stderr `stub: unscripted argv` and `matched: false` (1029-1032, teardown assert 1152-1155), log header and per-arg records with the exact keys (1003-1013), `IW_STUB_STATE_DIR` snapshot only for `orca` and `orca-ide` on `agent launch` (1014-1021), `which` guard for all four names (1146-1150). |
| 5 | Module context: sibling consistency of shared input shapes | none | PASS | `stub_path` env keys (5) equal what `Watcher` and `make_watcher` add (`IW_STUB_STATE_DIR`); `make_watcher` uses `tmp_path / "state"`, equal to `make_config(tmp_path).state_dir` (the snapshot is non-null, otherwise `json.loads(None)` would raise in the e2e test). |
| 6 | Downstream consumers: the cross-cutting tests consume code from Phases 2 to 7 with the right shapes | none | PASS | `CrashingStore` saves counted per DF-15 recipe (conftest.py:166-173: C1 and C4 raise before delegating, C3 and C5 after); `read_calls` rebuilds argv and asserts no missing index (1100-1103). |
| 7 | Test validity: end-to-end test (FR-001, FR-010, FR-013, NFR-010) | none | PASS | See rows 7a to 7d. |
| 7a | FR-001 idle cycle: exactly two `gh` calls | none | PASS | `test_fr001_idle_cycle_makes_exactly_two_gh_calls` (test_cli_e2e.py:299-331): `gh_calls == [USER_ARGV, DISCOVERY_ARGV]` (the FR-003 literal list, written out, lines 46-61), tool order `["gh","git","gh"]` (step 6 origin check, design line 349), no Orca call, one cycle line, `gh_calls` 2. Equals spec line 116. |
| 7b | FR-013 and FR-010 eligible cycle | none | PASS | 12-element argv equals the literal list (test_cli_e2e.py:242-257, 361-364), prompt `/sc:issue --claim 9`, cwd equals worktree (DF-01), `orca` stub never called while `orca-ide` is, snapshot taken exactly once and at the launch call, entry `pending`, `launches` 1, `consumed_at` set, `launch_cwd` set (378-385), final `launched` with `operation_id`. The call sequence (probe, re-read, events, items, second origin check, launch) equals FR-014 (spec line 157) and design step 12 (line 355). |
| 7c | NFR-010 second run | none | PASS | `test_nfr010_second_once_launches_nothing` (401-443): same scenario file, exactly 4 further calls (user, git, discovery, comments for the marker), no Orca call, `launched` entry unchanged on 5 keys, decisions `launched` then `already_dispatched`. Equals spec line 223 and design step 11 (marker read for entries that can reach `claimed`). |
| 7d | Stub guard | none | PASS | `test_ac1_fixture_guard_names_resolve_to_stubs` (281-296). |
| 8 | Crash points C1 to C5 with five reruns and per-point durable state | none | PASS | `RERUNS = 5`; `Rig.reruns` runs five cycles after a lock-free probe, checks at most one launcher call in total and `launches == 1` once a call is recorded (test_crash_injection.py:117-125, 131-149). Per point against Table 1.3 and design 7.6: C1 store bytes and file list unchanged, no entry (217-230); C2 one-shot `os.replace` patch on a `dispatch.json` destination, old bytes unchanged, one orphan `dispatch.json.*.tmp` equal to the patched `src`, ignored by reruns, no stderr, audit kinds only decision and cycle (238-279); C3 pending, `launches` 1, zero launcher calls, swept to `abandoned` `pending_orphan` in rerun 1 (287-302); C4 same with one recorded call (310-324); C5 final state saved (`considered` and `last_completed_cycle_at` ride save 2, design step 13), audit untouched, no relaunch (347-373). Rerun spacing 300 s x 5 stays under the 60 min lease, so `claim_not_observed` cannot fire. |
| 9 | Two-process lock test and lock-file failures | none | PASS | `spawn` context, bounded polls and joins, worker 1 holds the lock from inside its launcher while worker 2 starts (test_concurrency.py:86-187): exits (0, 75), worker 2 makes zero runner and launcher calls (FR-017: no external call), one launch, cycle lines `[(0,cycle_complete),(75,lock_held)]`. Symlink and directory give 6 `lock_invalid`, missing gives 6 `lock_missing` and is not recreated, path replaced after flock gives 75 (208-275); all with no call and `dispatch.json` bytes unchanged. Equals design 7.6 lock table steps 1 and 4 (inode mismatch); step 2 (regular file, owner) and the link-count-0 half of step 4 are not exercised, which task item 8.5 does not require (issue 3, minor). |
| 10 | AST tests (no shell, module boundaries) encode design 233-242 and T6 | none | PASS | `RULES` (test_module_boundaries.py:51-76) equals the design table except the `record` to `predicates` wording (see issue 2). Function-level and `TYPE_CHECKING` imports are walked (`ast.NodeVisitor`, depth counter), relative imports resolve (level arithmetic, 111-113), 35 flagged and 18 clean synthetic sources plus walker, protocol and `select` detectors prove the scan is not vacuous. `test_no_shell.py` flags non-`False` `shell=`, `os.system`, `os.popen` (aliases too) and `subprocess` imports outside `runner.py`, with 15 positive and 12 negative synthetic sources; the real scan covers only the package directory. |
| 11 | Hostile-text test (T1, T11, NFR-006) | none | PASS | Sentinel as label name, login-like string, non-JSON stdout, over-500-byte stderr with six sign variants for each of nine call kinds, plus launch replies, whole `once` and `status` through `CliRunner` (real and dry-run), rotated audit files scanned by `rglob`, closed key sets equal design 10.1 (test_no_text.py:70-80 vs design lines 701-716), real `SubprocessRunner` cap equals 500 bytes (701-723), argv scan for title, body, text fields and templates (137-163), mutation guards for every checker (857-961). |
| 12 | Security tests: prompt property, argv allow-list, DF-28 | none | PASS | `SEED 331`, `DRAWS 2000` (design line 693, DF-12, no marker), nine value families plus the FR-012 edge list including `9`, `"9"`, `True`, `0`, `-1`, `10**9`, `9.0`; valid values must produce `/sc:issue --claim n`, every other value must raise `ValueError` (test_security_invariants.py:451-512). `classify_argv` implements NFR-002 forms, DF-28 (every `gh api` other than G1 and graphql needs `--method GET`), NFR-003 needles, NG-2 (`mutation`, write verbs), 12-element launch literal, and 18 forbidden argvs prove it rejects (721-860). |
| 13 | Error paths: hostile login, hostile discovery number, hostile assignee, hostile config labels | none | PASS | Login gives exit 3 `login_invalid` with only the `api user` argv (FR-002, 602-610); a non-claim number gives 3 `gh_non_json` with only `_START` calls and no entry (618-625); `{own, hostile}` assignee gives `assigned_other` with no per-issue call (FR-003, FR-008, 564-570); hostile config labels stay one argv element and never reach the prompt (581-594). |
| 14 | Existence and citation claims in docstrings and comments (grep-verified) | AX-1 | FAIL (minor) | `test_crash_injection.py:1` cites AC-17; design line 890 defines AC-17 as the verb exit-code criterion and line 895 defines AC-22 as the crash-point criterion (see issue 1). All other AC, FR, NFR, DF and line citations in the eight files match their sources (AC-1, AC-7, AC-11, AC-20, AC-25, design line 693, research/06 Table 1.3). |
| 15 | Template and spec cross-references: spec FR-014 order, design 5.3 table, 10.1 schema, 8.1 argv table | none | PASS | Re-read from the files named above; every table the tests encode was compared with the cited lines. |

## Summary
- Checks passed: 14 / 15 (row 7 is the parent of 7a to 7d, all four PASS)
- Checks failed: 1 (row 14, minor only)
- Critical issues: 0
- Blocking findings (CRITICAL or IMPORTANT): 0
- Minor findings: 5 (notes; never rechecked)
- Issues fixed in-place: 0 (report only)
- Axis lens status:
drift-axis-inactive

## Issues Found

No blocking finding. The change set does encode the contracts of its binding sources correctly: the idle two-call cycle, the 12-element launch argv, the pending-at-launch snapshot, the second-run no-launch, the stub protocol, the five reruns and durable state per crash point, the two-process lock test, the AST tests, and the hostile-text test all match design lines 507-533, 653-672, 691-693, 765, 772-791, spec FR-001/FR-010/FR-013/NFR-010, and the DF rows named in the gate prompt. The assumption of at least 10 errors was tested by comparing every table the tests encode line by line; the few differences found are minor.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR (blocking: no) | `tests/issue_watch/test_crash_injection.py:1` | Docstring cites "NFR-005, AC-17". Design line 890 defines AC-17 as "Each verb's exit codes match section 4; check-config and status write nothing"; the crash-point criterion is AC-22 (design line 895: "Crash points C1 to C5 and 50 cycles never exceed one launch per issue"). A wrong citation on a true property. | Change `AC-17` to `AC-22` in the docstring. |
| 2 | MINOR (blocking: no) | `tests/issue_watch/test_module_boundaries.py:57-61, 20-22`; design line 239 | Design 5.3 lets `record` import from `predicates` "(types only, for Entry fields that hold an issue number)". The test allows any name; the real `record.py:23-29` imports four functions (`format_utc`, `parse_utc`, `valid_issue_number`, `valid_operation_id`) and one type. The relaxation is stated in the test docstring and task item 8.8 omits "types only", but no DF row records it as a DEVIATION. No data-loss or security consequence (pure helpers, no I/O). | Record the design wording as corrected in the Gate D verdict notes (or in the deviation register), or add a names-only rule to `RULES["record"]` once the design is amended. |
| 3 | MINOR (blocking: no) | `tests/issue_watch/test_concurrency.py:208-275`; design 7.6 lock table steps 2 and 4 | The single-process lock cases cover steps 1 and the inode half of step 4 only. Step 2 (not a regular file or foreign owner gives 6 `lock_invalid`) and the link-count-0 half of step 4 (lock path unlinked after `flock`, `os.stat` raising `FileNotFoundError`, which `record.py:409-410` maps to `lock_held`) have no test. Task item 8.5 did not ask for them, and `record.py` handles both. | Optional: add a test that unlinks the lock inside the patched `flock` wrapper and expects 75 `lock_held`. |
| 4 | MINOR (blocking: no) | `tests/issue_watch/test_security_invariants.py:263-272` (`classify_argv`, REST branch); design 8.1 table rows G3, G4 | The allow-list scan checks path, `--jq` position and the jq constants for events and comments argv, but not the `-F per_page=100 -F page=P` pair, and the e2e expected sequence builds its argv with the same `github.argv_*` functions it checks. Dropping `per_page=100` (GitHub then pages at 30 items, so the "page shorter than 100 means complete" rule would read truncated history as complete) is covered only by `test_github.py` from Phase 3, not by Phase 8. NFR-002 and AC-20 do not require the pair. | Optional: assert `argv[5:9] == ["-F", "per_page=100", "-F", f"page={p}"]` for the events and comments forms. |
| 5 | MINOR (blocking: no) | `tests/issue_watch/test_no_text.py:530` and scenarios `label_names`, `extra_text_fields`, `malformed_discovery_number`; item 8.7 ("sentinel present in at least one reply of every kind the scenario scripts") | `canary_served()` proves that some reply carried the sentinel. In these three scenarios the discovery reply already carries it, so the check passes even if the targeted reply kind (the events label name, the comment field) were never read. Scenarios `login_like_strings`, `non_json_stdout_*`, `stderr_*`, `timeout_with_stderr` and the launch scenarios do depend on the targeted reply, and `test_a_launching_cycle_records_the_prompt_and_stays_clean` shows the label-name events are read. The invariant itself is still enforced. | Optional: assert `canary_served()` per reply kind (argv prefix of the serving call) in those three scenarios. |

Notes that are not findings: the e2e test pins exact stdout strings (`state created: ...`, `cycle: cycle_complete` and `exit: 0`) that no design line fixes; they are code behavior, so a later wording change will need a test edit. The `rate_limited` scenario in the argv scan expects reason `rate_limit_clamped` because its rate reply carries no `Retry-After`, which is the FR-028 clamp path; the unclamped `rate_limited` reason is covered elsewhere (Phase 6). `WAIT_S` in `test_concurrency.py` is 30 s where item 8.5 says 10 s; it is a bound, not a delay, so the change only affects hung-worker time.

## Actions Taken
None. fix_authorization was false. The only file written is this report. One experiment ran on a /tmp copy of `tests/issue_watch/` (a check for unscripted argv added to `test_no_text.py::Run.check`); the copy was deleted and `git status` shows no change under `tests/issue_watch/` or `src/superclaude/cli/issue_watch/` caused by this review.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
The spawn prompt carried no `## Inherited Structural Verdict` section, so the standalone path applied. No structural PASS was relied on. The rf-qa lens reports in `qa/gate-d/` were not read.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. The message carried no inherited verdict table; the gate-command and change-set facts in `gate-d-change-set.md` were treated as claims, not as verification (I did not re-run G-1, G-3, G-8, G-5, which belong to the gate-command-reproduction lens).

**(b) Independent semantic checks (at least 1 required, INV-019):**
- FR-014 call order versus the e2e `expected_eligible_sequence`: read spec line 157 and design step table lines 349-355, compared with `test_cli_e2e.py:260-278`; order matches (probe, re-read, events, items, second origin check, launch).
- Stub protocol versus research/06 Table 1.4: read Table 1.4 (lines 70-83) and `conftest.py:968-1155` line by line; all eight rows match, including exit 99, `matched: false`, teardown failure and the `which` guard.
- Crash recipes versus Table 1.3 and design 7.6: read Table 1.3 (lines 58-68), `CrashingStore` (conftest.py:129-177) and `test_crash_injection.py` in full; per-point triggers and durable-state assertions match; checked the 60-minute lease cannot interfere with the 5 x 300 s reruns.
- Audit closed key set versus design 10.1: read design lines 701-716 and `test_no_text.py:70-80`, and grep of `audit.py` `_COMMON` and `_KEYS` (lines 159-174); sets agree.
- AC citations: grep of design lines 872-898 against docstring citations; found the AC-17 versus AC-22 mismatch (issue 1).
- Unscripted-argv guard in `test_no_text.py`: ran a patched /tmp copy (Bash, `uv run pytest`, 168 passed) to check whether any scenario hides an exit-99 argv; none does.
- Import table: read design 233-242, `record.py:23-29` and `launch.py` imports against `RULES`; found the "types only" relaxation (issue 2).

If this report had said 0 issues the user would have had little reason to believe it; the five minor findings above come from line-by-line comparison against the design tables, not from sampling. Claims verified independently against files: about 70 (14 design or spec line ranges, 10 DF rows, 8 test files in full, 5 source locations).

## Recommendations
- Proceed with Gate D: no blocking finding from this lens, so no fix agent is needed for it.
- Carry the five minor notes forward (never rechecked). Issue 1 is a one-word docstring fix if any fix pass happens anyway for another lens.
- Record the `record` to `predicates` relaxation (issue 2) in the Gate D verdict notes so the deviation register and the test agree.

## Confidence Gate

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: about 30 | Grep: 11 | Glob: 0 | Bash: 3 (one blocked by the UV-only hook, then retried with sed and `uv run pytest`) . Tool calls exceed the 15 checklist items.
- Unchecked items: none. Unverifiable items: none.
- Not done on purpose: no re-run of the four gate commands (another lens owns them); no web research (Tavily not needed, no external lookup).

## QA Complete
