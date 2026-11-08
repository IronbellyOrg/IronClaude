# QA Report: Research Gate, Gap Detection Lens (fix cycle 1, round 2)

**Topic:** GitHub issue watcher MDTM task build (TASK-RF-issue-watcher-20261107-150955)
**Date:** 2026-11-07
**Phase:** research-gate (gap-fill re-check)
**Lens:** gap-detection
**Fix cycle:** 1 (fix_authorization: false, report only)
**Scope read:** `research/06-gap-fill-decisions.md` (all 219 lines), `research-notes.md`, `qa/qa-research-gap-report.md`, design `docs/designs/issue-watcher.md` lines 104-167, 248-303, 392-402, 560-640, 690-745, 747-935, spec-final.md 296-395, `.pre-commit-config.yaml`, `Makefile` gate targets, `.github/workflows/test.yml`, `tests/cli/test_cli_registration.py`, task-builder `SKILL.md` lines 408, 2223, 2237.

---

## Part 1: Round-1 findings (I1 to I5), resolved or not

| Round-1 id | Finding | Decision in 06 | Status | Remaining defect |
|---|---|---|---|---|
| I1 (single list) | No merged decision register | 06 header, Section 1 and DF-40 make 06 the one register; 11 DEVIATION rows listed | RESOLVED (DF-40) | 06's precedence clause omits `research-notes.md` (see M-3) |
| I1(a) | Failed G4 marker read or G5 edit read had no reason | DF-02: new reasons `marker_unreadable`, `edits_unreadable`, kind skip, exit 0, no entry written; pin test goes 52 to 56 | RESOLVED (DF-02) | I counted spec-final.md 334-358 = 52 reasons; 52 + 2 + 1 + 1 = 56 holds |
| I1(b) | `reset` audit line had no reason | DF-03: `operator_reset`; `decision` line for `reset N`, `warning` line for `--rate-limit`, never a `cycle` line | RESOLVED (DF-03) for the success exits only; non-success exits are open (N-1); line shape details are open (M-1) |
| I1(c) | `reset N` with no entry undefined | DF-04: exit 2, stderr line, no store write, no audit line | RESOLVED as a decision, but it contradicts design 7.1 line 399 without saying so (N-1) |
| I1(d) | AC-23 `make test` vs unsafe full run | DF-05: named subset (G-1, G-2) plus `make lint`; "full suite: CI only" recorded; listed as DEVIATION | RESOLVED (DF-05). All five G-2 files exist (checked); `tests/cli/test_cli_registration.py` asserts a subset (`EXPECTED_TOP_LEVEL_COMMANDS` used in `-` and loops only), so a new top-level group does not break it |
| I2 | "six verbs" vs five Click commands | DF-06: five commands, six usage forms; `test_cli.py` asserts the five names; G-9 lists exactly five | RESOLVED (DF-06). Design lines 177 and 759 still say "six"; 06 says the task text overrides, which is enough |
| I3 | Empty `{BASE}..HEAD` diff | DF-07: BASE SHA captured in P1 (checked today: origin/master `0b8a5801...`, merge-base = HEAD `e8db2fe6...`, both match 06), explicit-path commit in P10, POST reflect uses `<BASE SHA>..HEAD` | RESOLVED as a mechanism. The authority for the commit is not sourced (N-2) |
| I4 | `~` in default `--config` | DF-13: `expanduser()` on default and passed `--config`; `state_dir` default from `XDG_STATE_HOME` or `Path.home()`; `~` inside JSON values is rejected as non-absolute; HOME-monkeypatch test with no `--config` | RESOLVED (DF-13) |
| I5 | Gate commands not runnable as written | Table 1.2 G-1 to G-9; pinned ruff form. I ran `uvx --offline ruff@0.15.20 --version`: prints `ruff 0.15.20`. `make lint` is `lint-architecture` then `uv run ruff check .` (Makefile 48-50); `make verify-deps` runs `uv run python scripts/verify_deps.py`; `make sync-dev` precedes `make verify-sync` in G-6 | RESOLVED (DF-09). One checkpoint wording defect (M-4) |

Result for the five round-1 blocking findings: 5 of 5 have a concrete decision. None of them is NOT RESOLVED. Two of them (I1(c) and I3) carry new blocking defects listed below.

## Part 2: New gaps left or introduced by file 06

### Blocking

**N-1 (IMPORTANT). `reset` non-success exits have no audit decision, and DF-04 contradicts design 7.1 line 399 without recording it.**
Design line 399 says `audit.jsonl` is written by "every exit of `once` and `reset`". DF-03 defines the audit line only for the two success paths. DF-04 then says the missing-entry case writes no audit line, and its DEVIATION cell says only "case absent from D 118 and S 297", which is wrong: line 399 does cover it. Still undecided in 06, and an author of `cli.py`, `record.py` and `test_cli.py` must invent each: (a) `reset N` on an entry that is not `abandoned`/`unknown` (exit 2, defined at D 118); (b) exit 6 (store unreadable) for both reset forms; (c) exit 75 (`lock_held`) for both reset forms; (d) exit 2 usage errors. The AC-17 test ("each verb's exit codes match section 4") will need an assertion on `audit.jsonl` for every one of these.
Required fix: add one sentence to DF-03/DF-04 listing, per reset exit (0, 2 wrong state, 2 missing entry, 2 usage, 6, 75), whether a line is written, its `kind`, its `reason`, or "stderr fallback only" (D 722). Add "D 399 ('every exit of reset')" to DF-04's DEVIATION cell.

**N-2 (IMPORTANT). DF-07 says the commit is "owner-authorized for this task only"; no source for that exists.**
The only place the idea appears is in the QA reports, as a suggestion ("owner-authorized local commit item before POST", `qa/qa-research-depth-report.md` line 27). DF-07's own Source cell lists only QA reports (RD 1, RG I3, AC MIN-6). `research-notes.md` line 26 says "no commit or PR step inside the task file", and the user's rule is to commit only when asked. So the register records a user authorization as fact when it was a reviewer proposal. Because the item executes `git commit` unattended in P10, a false authorization claim is a data-integrity problem, not wording. DF-40 also calls the DEVIATION rows "Open Questions", but DF-07 gives the executor no condition to stop on while the question is open.
Required fix: either (a) cite the owner message that approved the commit, or (b) rewrite DF-07 so the P10 commit item is conditional on an owner confirmation line in the Task Log, with a stated fallback that needs no commit (stage the same explicit paths with `git add` and run POST reflect with the single-ref working-tree form the CLI arm uses, `SKILL.md` 2237), and mark the deviation "proposed, not approved". The main session should ask the user before the task file is built.

**N-3 (IMPORTANT). `conftest.py` is placed once, in P2, but its contents depend on modules built in P4, P5 and P8, and later additions have no phase.**
Phase plan line 170 puts `conftest.py` with `FakeRunner`, `FakeClock`, `FakeLauncher`, `tmp_state` in P2, with checkpoint "G-1 passes". `FakeLauncher(outcomes)` takes `LaunchOutcome` values and implements `Launcher.launch(orca, worktree, prompt, timeout)` (design 5.4 lines 276-285); both are defined in `launch.py`, which is P5. `tmp_state` and `CrashingStore(real, ...)` (DF-15, "`conftest.py`") need `FileStore`, which is P4. DF-10 puts the PATH-stub fixture in `conftest.py` too, and P8 lists `test_cli_e2e.py` but never says `conftest.py` gains the stub fixture or `CrashingStore`. A module-level import of a P4/P5 name in the P2 `conftest.py` makes every `tests/issue_watch/` test fail at collection at the P2, P3 and P4 checkpoints. An author has to invent which fixture lands in which phase.
Required fix: split the conftest deliverable across the plan: P2 `FakeRunner`, `FakeClock`; P4 `tmp_state` (and `FileStore` use); P5 or P6 `FakeLauncher`; P8 `CrashingStore` and the PATH-stub fixture. State "no module-level import of a later phase's module in `conftest.py`".

**N-4 (IMPORTANT). AC-19 (sleeping stub gives `gh_timeout`) has no implementable mechanism after DF-10 and DF-34.**
Table 1.4's scenario record is closed: `{argv_prefix, exit, stdout, stderr}`. It has no sleep field, although research 05 line 260 had one. DF-34 runs `test_cli_e2e.py` as a real child process (`python -m superclaude.cli.main`), so a `monkeypatch` of a timeout constant (research 05 lines 224 and 416) cannot reach the child. The design makes timeouts module constants, not config (D 139; gh 20 s at D 819), and research 03 line 115 says "lower the timeout through the config/Clock seam", but no such seam exists. So the AC-19 test is either a real 20 s wait, or the author invents an environment variable or a new constant, which the design does not allow (unknown config keys are rejected; no operator knobs). The same Table 1.4 also drops the research-05 behaviour "stub `orca` reads `dispatch.json` when invoked" (FR-010 GWT), with no replacement stated.
Required fix: add to DF-34 or Table 1.4 an explicit AC-19 recipe. Suggested: scenario rule gains `sleep_s`; AC-19 runs in-process (`CliRunner` or `cycle.run_cycle` with the real `SubprocessRunner`) with `monkeypatch.setattr` on the `github` timeout constant set to about 0.5 s, and the stub sleeping 3 s. Say which in-process test owns "no launch starts after 120 s" (FakeClock, `test_cycle.py`). State that the FR-010 "pending saved before launch" check is done by `FakeLauncher` reading the store at call time.

### Minor (notes, not blocking)

| Id | Location | Issue | Suggested fix |
|---|---|---|---|
| M-1 | DF-03 | `operator_reset` is registered as kind `skip` (DF-03 text) but `reset --rate-limit` writes it on a `warning` line; the spec table's warning-line reasons are `discovery_count`, `clock_skew` (spec 358). Schema 10.1 (D 701-716) also requires `ts`, `host`, `cycle_id`, `dry_run` on every line; DF-03 states only `issue`, `login`, `state`, approval fields, `note`. | Say: `host` and `ts` as usual, `cycle_id` fresh `uuid4().hex`, `dry_run` false; note the kind of `operator_reset` is "skip (decision) and warning (rate-limit)". |
| M-2 | DF-07, P10 | The staged-path check is negative only (no `.claude/`, `.dev/issues/`, `.dev/brainstorms/`); anything else already staged is committed. Today `git status` shows only `.dev/tasks` content staged, so it is safe now. After the commit and the POST reflect, Task Log edits and reflect output under `.dev/tasks` are unstaged, and the P10 row has no final `git add .dev/tasks` (project rule, SKILL.md line 408). | Compare `git diff --cached --name-only` to an allowlist of the DF-07 path prefixes; add a final `git add .dev/tasks` (staging only) after POST. |
| M-3 | 06 line 3, `research-notes.md` | 06 says it supersedes "research files 01 to 05" and names `research-notes.md` only for AMBIGUITIES. `research-notes.md` still says: stubs `stubs/gh`, `stubs/orca` (line 20, reversed by DF-10), "no commit ... step" (line 26, reversed by DF-07), `__init__.py` needed because two `test_cli.py` would collide (line 24, false per DF-27). | Extend line 3 to "research-notes.md and research files 01 to 05". |
| M-4 | Table 1.2 G-1, P1 checkpoint | G-1 pass is "exit 0, N passed". P1's checkpoint is "collects 0 tests without error"; pytest exits 5 when it collects nothing, so an executor reading G-1 literally fails P1. | P1: "exit 5 (no tests collected) is the expected result". |
| M-5 | DF-32 | Pre-commit hooks in `.pre-commit-config.yaml` that touch the new files and are not mentioned: end-of-file-fixer (line 11; applies to `.py`, `.json`, `.md`), trailing-whitespace (line 9; `.md` excluded), mixed-line-ending (line 21), check-added-large-files (17), check-merge-conflict (19), detect-private-key (47), the hardcoded-secret regex hook (54-63), yamllint (n/a, no YAML). ruff-format (109-113) is covered by G-5. No hook is installed here (`.git/hooks` holds only samples), so none runs at DF-07's commit. | Add one rule: every new file is LF, ends with exactly one newline, no trailing spaces in `.py` and `.json`; check with a grep in the final gate. |

Verification coverage requested in the lens: pre-commit hooks (partly, M-5), `lint-architecture` (covered by G-4: `lint: lint-architecture`, Makefile line 48; CI runs it at `test.yml:135`), `verify-deps` and `verify-sync` (G-6; CI `test.yml:123,131`). The CI "verify-sync hook checks" step (`test.yml:137`) maps to the `tests/cli/test_verify_sync_hooks.py` that DF-05 excludes locally; DF-05 records it as CI only, which is consistent.

Phase-plan file coverage (design section 11): every path in section 11 is in exactly one phase (P1 `__init__.py` files; P2 runner, predicates, audit and their tests; P3 github, fixtures, test_github; P4 record; P5 launch, parity and marker tests; P6 cycle, slo test; P7 cli, main.py; P8 cross-cutting tests; P9 runbook). `stubs/gh` and `stubs/orca` are intentionally not produced (DF-10, recorded DEVIATION). The only coverage hole is the late content of `conftest.py` (N-3).

DF-07 safety check: explicit paths (yes), `.claude/` excluded and checked (yes), no `git add -A`, no `--no-verify`, no push (yes), base ref captured as a SHA and no fetch (yes), conventional-commit subject matches the `conventional-pre-commit` hook, attribution trailer present. The unsafe parts are the authority (N-2) and the negative-only path check (M-2).

## Part 3: DEVIATION items recorded for the task

DF-40 lists DF-01, 02, 03, 04, 05, 07, 10, 12, 17, 20, 22 = 11 ids. I counted the rows whose DEVIATION cell starts with "yes" in Section 1.1 and 1.7: the same eleven, no more, no fewer. P9 deliverables include "Open Questions / Deviations list (DF-40)", so the task can list them. PASS, with two notes: (1) DF-04's DEVIATION cell misses the conflicting source D 399 (N-1); (2) DF-07's row needs the "proposed, not approved" status (N-2). Rows recorded "no" that still change design text (DF-24, 25, 27, 28, 29, and DF-23's skip on unreadable mountinfo) are design-internal conflicts or prose errors; I do not grade that classification as blocking.

## Summary

- Round-1 blocking findings: 5. Resolved with a concrete decision: 5 of 5 (two carry new blocking defects, N-1 and N-2).
- New blocking findings (IMPORTANT): 4 (N-1, N-2, N-3, N-4). CRITICAL: 0. Minor: 5 (M-1 to M-5).
- Blocking count fell from 5 to 4, so the monotonicity guard (`|F_2| < |F_1|`) is satisfied. No round-1 item regressed.
- Fixes needed are edits to 06 only: add per-exit audit rules for `reset` (N-1), re-source or condition the commit (N-2), re-phase `conftest.py` (N-3), add an AC-19 recipe (N-4).

## Confidence

Verified: 17/18 | Unverifiable: 0 | Unchecked: 1 | Confidence: 94.4% (below the 95% bar, and the verdict is FAIL anyway)
Unchecked: that `uv run superclaude issue-watch --help` (G-9) runs offline in this checkout; I did not run `uv run` commands that may sync `.venv`. `superclaude` is on PATH and `.venv` exists, so I expect it to work.
Tool engagement: Read: 14 | Grep: 9 | Glob: 2 | Bash: 4

## QA Complete

VERDICT: FAIL

