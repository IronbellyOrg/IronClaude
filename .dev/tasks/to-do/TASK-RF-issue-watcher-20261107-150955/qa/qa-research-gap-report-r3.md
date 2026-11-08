# QA Report: Research Gate, Gap Detection Lens (FINAL re-check, round 2 fixes, third review)

**Topic:** GitHub issue watcher MDTM task build (TASK-RF-issue-watcher-20261107-150955)
**Date:** 2026-11-08
**Phase:** research-gate (fix-cycle, final review)
**Lens:** gap-detection
**Fix cycle:** 2 (fix_authorization: false, report only)
**Prior report:** `qa/qa-research-gap-report-r2.md` (4 blocking: N-1, N-2, N-3, N-4)
**Scope:** `research/06-gap-fill-decisions.md` (314 lines), research-notes.md, research/01-05, design sections 11, 12, 13, 17

---

## Part 1: Round-2 blockers N-1 to N-4

| Id | Status | DF id and evidence in file 06 |
|---|---|---|
| N-1 reset non-success exits | RESOLVED | DF-57 (06 line 191): order lock, store load, entry check. Exit 2 wrong state or missing entry: `warning` line, reason `reset_refused`, `issue` = N. Exit 6 `store_invalid`/`store_missing`/`lock_missing`/`lock_invalid`: `warning` line with that reason. Exit 6 `state_dir_unwritable`: `stderr_fallback` only (matches D 722, read at design line 722). Exit 75: `warning` line `lock_held`, no rotation (D 720). Usage errors before `state_dir` is known: `stderr_fallback("reset_refused", 2)`; invalid config: `stderr_fallback("config_invalid", 2)`; Click parse errors write nothing. Every line has `ts`, `host`, fresh `cycle_id`, `dry_run` false. DF-04 (line 27) now points at DF-57 and its DEVIATION cell names D 399. DF-03 (line 26) states the kind as skip plus warning and lists the D 701-716 keys. Design line 399 ("every exit of `once` and `reset`") is now met. `reset_refused` is counted: REASON_TABLE has 52 + 5 = 57 (DF-41, line 175; DF-02, line 25). |
| N-2 commit authority | RESOLVED, with a provenance note | DF-07 (line 30) no longer claims owner authorization. It cites `[SOURCE: coordinator brief]` (steps 6 and 7 after the build: `/task`, then `/sc:pr-submit`), is marked DEVIATION yes (it is one of the 24 in DF-40, line 167), and has HALT on commit or hook failure. I cannot verify the brief: the ids `task_0b795fb7069a` and `ctx_58a8c8b54cbd` appear only in file 06 (Grep over the worktree). It is an agent brief, not an owner statement, and the commit is an inference ("therefore"), not a quoted instruction. See M-1 below. The commit is local, reversible, and runs only when the owner runs `/task`. |
| N-3 conftest ordering | RESOLVED | DF-56 (line 190) and Section 2 (lines 202, 204, 205, 206, 208): P2 `FakeRunner` + `FakeClock`; P4 `tmp_state` + `CrashingStore`; P5 `FakeLauncher`; P6 deps factory; P8 stub-on-PATH fixture and scenario helper; "no module-level import of a module a later phase creates"; P1 expects exit 5. I walked each addition against the modules built before it: `FakeRunner` needs `runner.CommandResult` (P2); `FakeClock` is structural and needs no import of `cycle.Clock` (P6); `tmp_state` and `CrashingStore` need `record` (P4); `FakeLauncher` needs `launch.LaunchOutcome` (P5); the deps factory needs `cycle.Deps` (P6), `audit` (P2), `record` (P4), `launch` (P5). No forward import. |
| N-4 AC-19 mechanism | RESOLVED | DF-55 (line 189) plus Table 1.4 rows Scenario (line 77, `sleep` field), Log (line 78, `matched`), State snapshot (line 79, `IW_STUB_STATE_DIR`, FR-010) and AC-19 (line 80). The sleeping case is a `test_runner.py` unit test of `SubprocessRunner` with `timeout=0.5`, which returns `CommandResult(timed_out=True)` (D 218). Exit 3 `gh_timeout` and the 120 s no-launch cutoff run in-process with `FakeRunner` timed-out replies and `FakeClock` (`test_cycle.py`). It is a DEVIATION from D 892 and is in the DF-40 list. The old objection (a monkeypatch cannot reach a child process) is gone because AC-19 is no longer an e2e case. |

Blocking count: r2 had 4; r3 has 0 open from r2. Monotonicity guard satisfied (4 to 0). No regression of a round-1 item (spot-checked: DF-02 pin count, DF-06 five commands, DF-07 BASE).

## Part 2: New-gap sweep

Facts re-checked this round (Bash): branch `ironbelly/issue-331-github-issue-watcher`; origin/master `0b8a5801d75f159bcbca7087b99507c2a50d8dba`; merge-base = HEAD `e8db2fe660d9104cbe8cdbcdc6f2c967f4994f4b`; 83 staged files, all under `.dev/tasks/`; `docs/designs/issue-watcher.md` untracked; neither `src/superclaude/cli/issue_watch` nor `tests/issue_watch` exists yet. All match DF-07.

### Design section 11 (files) to phase

Every path in D 751-766 has a phase in Section 2: `__init__.py` files (P1), runner/predicates/audit and tests (P2), github + fixtures (P3), record (P4), launch + four parity/contract tests (P5), cycle + `test_slo_helper` (P6), cli + `main.py` (P7), cross-cutting tests (P8), runbook (P9). `stubs/gh` and `stubs/orca` are not produced (DF-10, recorded DEVIATION). Nothing orphaned.

### Design section 12 (tests) to phase

All 8 per-module tests and all 11 cross-cutting tests (D 762-763) appear in exactly one phase. The four fakes in D 774-780 map to DF-24, DF-48, DF-15 and DF-10/Table 1.4. Rows in D 782-791 each have a recipe (crash: Table 1.3; concurrency: DF-34; fifty cycles and acceptance property: P6; no_shell: G-8 plus AST; marker contract: DF-46).

### Design section 17 (AC-1 to AC-25) to test and phase

Each AC maps to a test file (research 03 lines 181-195) and each test file has a phase (06 Section 2): AC-1, 2, 5, 12, 15 test_cycle + test_github (P6, P3); AC-3, 4 test_predicates (P2); AC-6, 10, 18 test_record + test_cycle (P4, P6); AC-7 test_launch + test_no_text + test_security_invariants (P5, P8); AC-8, 9 test_launch + test_cli (P5, P7); AC-11 test_concurrency + test_record (P8, P4); AC-13, 14, 17 test_cli + test_audit (P7, P2); AC-16 test_origin_parity (P5); AC-19 DF-55 (P2 and P6, not P8); AC-20 test_security_invariants (P8); AC-21 test_no_shell (P8); AC-22 crash + fifty cycles (P8, P6); AC-23 gates G-1 to G-11 (P9); AC-24 test_slo_helper (P6); AC-25 boundaries + parity (P8, P5). All 25 are covered; none is missing. The only weakness is that the table lives in research 03, not in 06 (M-4).

### Gate verification items

| Check | Where | Result |
|---|---|---|
| pre-commit hooks | DF-58 (line 192), G-11 (line 56), DF-32 (line 159); `.pre-commit-config.yaml` ids read: trailing-whitespace 9, end-of-file-fixer 11, check-json 15, check-added-large-files 17, check-merge-conflict 19, check-case-conflict 20, mixed-line-ending 21, detect-secrets 29, detect-private-key 47, conventional-pre-commit 69, markdownlint 77, shellcheck 101, ruff-format 112, block-claude-generated-mirrors 121 | Covered: whitespace, CR, EOF by G-11; ruff-format by G-5; json by `json.loads` in `test_github.py`; secrets and markdownlint by reading; shellcheck not engaged; `.claude/` mirror hook by G-10 and the P10 allowlist. Gaps are only M-5. |
| `lint-architecture` | G-4 `make lint` (Makefile 48-50) at P3, P5, P7, P9 | Covered |
| `verify-deps` | G-6 | Covered |
| `verify-sync` | G-6 (`sync-dev` then `verify-sync`) | Covered; CI-only `tests/cli/test_verify_sync_hooks.py` recorded by DF-05 |
| Commit item (DF-07) | line 30, P10 line 210 | Explicit paths yes; `.claude/`, `.dev/issues/`, `.dev/brainstorms/` excluded and checked; allowlist by prefix; BASE = `git rev-parse HEAD` immediately before the commit; no `-A`, no `--no-verify`, no `--no-gpg-sign`, no push, no PR; HALT on commit or hook failure; final `git add .dev/tasks`; trailer matches the attribution reminder. Residuals: M-2. |
| 24 deviations | DF-40 line 167 | I counted the rows whose DEVIATION cell starts with "yes": DF-01, 02, 03, 04, 05, 06, 07, 09, 10, 12, 13, 17, 18, 20, 22, 24, 25, 27, 28, 29, 43, 50, 55, 57 = 24. Matches DF-40. The I19-vs-2140 tension, Q1-Q4 and X1-X5 are listed separately. |
| Gate map arithmetic | Table 1.6 | 4 x 6 + 7 + 2 = 33. Matches. |

### Phase checkpoints collect cleanly

P1 exit 5 expected; P2 conftest imports only `runner`; P3 uses only P2 fakes; P4 adds fixtures that import only `record`; P5, P6, P8 likewise (Part 1, N-3). No phase imports a later module at module level. One test-level dependency crosses phases (M-3).

## Part 3: Issues found

No CRITICAL and no IMPORTANT issue. The items below are minor: notes only, never rechecked, and none fails the gate.

| # | Severity | Location | Issue | Suggested fix |
|---|---|---|---|---|
| M-1 | MINOR | DF-07 (06 line 30), header line 12 | The authority is a coordinator brief that is not in the repository, and the header says it "is not UNVERIFIED". I cannot verify it, and the commit is inferred from "PR is step 7", not quoted. The commit is local and reversible, HALT guards failure, and DF-07 is in the DF-40 Open Questions list, so the owner sees it before `/task` runs. | In the task's Open Questions entry for DF-07, say "inferred from the dispatch brief; owner may veto before `/task`". |
| M-2 | MINOR | DF-07 items (3) and (4) | (a) No stated action when the allowlist check finds a stray path (HALT and do not commit is implied by the P10 checkpoint, not written). (b) No guard that the current branch is not `master` or `main` before an unattended commit (global rule 4). Today the branch is a feature branch. | Add: "`git branch --show-current` must not print master or main; allowlist violation = HALT, no commit, no automatic unstage." |
| M-3 | MINOR | DF-55 (c), Table 1.4 AC-19 row, P2 vs P8 | The P2 `test_runner.py` sleeping-stub case reads as using the Table 1.4 stub, but that fixture arrives in P8 (DF-56). Used from P2 it would fail with "fixture not found". | Say the P2 case runs a self-contained child (`[sys.executable, "-c", "import time; time.sleep(5)"]`), not the P8 stub. |
| M-4 | MINOR | Section 3 "Gates and ACs" row; P9 trace-table deliverable | The AC-to-test table is in research 03 lines 181-195, whose AC-19 row (`test_cli_e2e.py`) is superseded by DF-55. The builder must apply 06's precedence to build the P9 trace table. | Copy the 25-row AC to test to phase table into 06, with AC-19 as DF-55. |
| M-5 | MINOR | DF-35 (06 line 162), D 439 | DF-35 gives a 3.10-safe parser for GitHub times, but `record.validate` must also parse the store's own "aware UTC ... ending Z" strings (D 439), and `record`, `audit` and `cycle` must format them. A helper in `github.py` is not importable by `record` (D 5.3). The G-7 grep will flag `fromisoformat`, but the replacement is left to the author. | Say: each of `record`, `audit`, `cycle` uses its own 3-line `strptime` / `strftime("%Y-%m-%dT%H:%M:%SZ")` helper, or the shared helper lives in `predicates.py`. |
| M-6 | MINOR | DF-34, D 300 | `test_cli.py` runs `once` in-process through `CliRunner`, but `cli.build_deps` builds a real `SubprocessRunner`. The injection seam (monkeypatch `cli.build_deps`) is not stated, and a forgotten patch would run a real `gh`. | State "`test_cli.py` monkeypatches `cli.build_deps`", and add an autouse guard in `test_cli.py` that fails on any real `SubprocessRunner.run`. |
| M-7 | MINOR | DF-27 (06 line 154) vs Section 2 P1 (line 201) | DF-27 puts `tests/issue_watch/__init__.py` in a "P2 setup item"; Section 2 creates it in P1. | Change DF-27 to P1. |
| M-8 | MINOR | `research-notes.md` lines 20, 24, 51 | Still say stubs `stubs/gh`, "`__init__.py` required because two `test_cli.py` collide", and `AMBIGUITIES_FOR_USER: None`. 06 line 3 and DF-40 say 06 supersedes it, so this is covered. Noted so the builder reads 06 first. | None needed. |

## Summary

- Round-2 blockers: 4. RESOLVED: 4. NOT RESOLVED: 0.
- New blocking findings: 0 (CRITICAL 0, IMPORTANT 0). Minor notes: 8 (M-1 to M-8).
- Monotonicity: 4 to 0 blocking. No regression.
- Coverage checked: design 11 files, 12 tests, 17 ACs (all 25), gates (hooks, lint-architecture, verify-deps, verify-sync), commit item safety, 24 deviations (count verified), 33-agent gate arithmetic.

## Confidence

Verified: 21/21 | Unverifiable: 1 (the coordinator brief behind DF-07, outside the repository; recorded as M-1) | Unchecked: 0 | Confidence: 100.0% of the checkable items
Tool engagement: Read: 12 | Grep: 4 | Glob: 1 | Bash: 1

## QA Complete

VERDICT: PASS
