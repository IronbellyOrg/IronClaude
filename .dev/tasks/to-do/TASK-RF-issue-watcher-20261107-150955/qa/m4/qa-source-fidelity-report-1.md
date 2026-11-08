# QA Report: Source Fidelity Gate, design-fidelity lens (report 1 of 3)

**Topic:** issue-watch implementation versus the design `docs/designs/issue-watcher.md` (935 lines, read in full)
**Date:** 2026-11-08
**Phase:** M4 source-fidelity gate (Step 9.M1), report-only (`fix_authorization: false`)
**Fix cycle:** 1 (first review of this gate)
**Change set reviewed:** `phase-outputs/reports/final-change-set.md` (9 source files, `main.py` registration, 21 test files, 19 fixtures, `docs/designs/issue-watcher-setup.md`)
**Accepted deviations applied:** the 29 DF decisions of the prompt, the owner questions Q1 to Q4, section D of the Open Questions (OQ-36, OQ-41a, OQ-47, OQ-48, OQ-49 to OQ-51), and `phase-outputs/reports/deviation-register.md` Table 2 (including `cycle_complete` and `cycle_crashed`). None of these is reported as drift below.

## Overall Verdict: PASS (with minor notes). Blocking findings: 0. Minor findings: 8.

Stance: I started from "at least 15 errors exist". After reading the design in full and every source module (`runner`, `predicates`, `audit`, `github`, `record`, `launch`, `cycle`, `cli`), the runbook, the deviation register, the AC trace and about 40 test bodies, I did not find 15 real defects and I did not manufacture any. I found 8 minor divergences, listed with evidence, and 0 blocking ones. Four earlier gates (A to D) already closed the large findings, and each design constant I checked is pinned by a test that asserts the value.

---

## Items Reviewed (coverage table by design section)

| # | Design section | Result | Evidence (tool-verified this session) |
|---|---|---|---|
| 1 | 1 Purpose and scope | PASS | Package `src/superclaude/cli/issue_watch/` holds 9 files; `main.py:563-565` registers `issue_watch_group` after `reflect_group` (561); runbook exists (651 lines); deployment gate restated in runbook 0, 8.5, 14.1. |
| 2 | 2 Binding decisions (D1 to D3, NG-1 to NG-5, OD-3, OD-4) | PASS | `launch.build_claim_prompt` (launch.py:84-92: `type(n) is not int`, range 1..999999999); GraphQL constants contain no `mutation` (`test_security_invariants.py:879-902`); project unreadable fails closed (`project_unreadable` skip, `scope_missing` stops the cycle). |
| 3 | 3 Corrections C1 to C22, S1 | PASS | C4 save path (`record.FileStore.save` 370-378: `write_prepared_bytes`, `chmod 0o600`, dir fsync); C18 lazy import (record.py:372, 853); C19 non-dict topic rejected (launch.py:158); C21 `--method GET` (github.py:206, 257); C22 per-issue clamp (`cycle._rate_stop` 644-649); S1 halt (`cycle._candidates` 814-815). |
| 4 | 4.1 Verbs, 4.2 Config, 4.3 Exit codes | PASS with note M1 | `cli.py` five commands (DF-06); `load_config` 195-283 rejects unknown keys at both levels, enforces 50-char labels, `PVT_` regex, account id range; approvers rules `validate_approvers` 298-342 (lstat, S_ISREG, uid, `S_IWGRP or S_IWOTH`, id regex, non-empty); `resolve_exit` 447-458 gives 2,6,7,5,3,4 then 75. |
| 5 | 5.1 to 5.4 Components, dependency rules, Protocols | PASS with note M5 | Exactly four Protocols (`Runner`, `Store`, `Launcher`, `Clock`); import table enforced by the AST test `test_module_boundaries.py` RULES (lines 51-76), which matches design 5.3 except the "types only" qualifier (M5). |
| 6 | 6.1 to 6.3 Cycle, steps 1 to 15, quantity flow | PASS with notes M2, M3 | `_Cycle.run`/`_steps`/`_examine`/`_launch` order: platform, config, enabled, approvers, worktree, lock, DISABLED, load, G1, origin, sweep, G2, order, per-candidate, probe, prompt, re-read, day cap, DISABLED, origin, pending save, launch. Constants: `MAX_CANDIDATES` 10, `CALL_CAP` 35 with `RESERVED_CALLS` 3, `DAY_CAP` 6. |
| 7 | 7.1 to 7.6 Store, schema, state machine, windows, atomic write, lock, crash points | PASS | 17 `Entry` fields (record.py:68-88) and 7 store keys (`_STORE_KEYS`) pinned by `test_record.py:196-197`; T-1 to T-13 each a function (`fail`, `backoff_elapsed`, `mark_pending`, `mark_launched`, `mark_unknown`, `mark_spawn_error`, `sweep`, `mark_claimed`, `reset_entry`); `LEASE` 60 min, `BACKOFF` 10 min, `MAX_ATTEMPTS` 3, window `now-24h < t <= now` (record.py:689-690); lock steps 1 to 5 (record.py:391-419) match the table; crash points C1 to C5 exercised in `test_crash_injection.py`. |
| 8 | 8.1 GitHub argv G1 to G7 | PASS | `github.py` 175-262 equals the design table: G2 `-L 100`, G3/G4 `--method GET -F per_page=100 -F page=P --jq`, G5/G6 `graphql -f query -F number [-f after]`, G7; asserted literal by `test_g2_argv_is_the_fr003_literal__fr003` (test_github.py:126-143). |
| 9 | 8.2 Paging and classification, 8.3 Rate-limit time | PASS with note M6 | `PAGE_CAP` 5, `PAGE_SIZE` 100, repeated id/cursor incomplete (github.py:592-702); `classify` 345-371 follows the row order; `rate_limit_wait` 418-431 implements the table (`Retry-After` 1..3600, reset epoch within 3600, else clamp). |
| 10 | 8.4 Orca contract, 8.5 Timeouts and deadline | PASS with note M2 | `launch_argv` is the 12-element list (launch.py:95-116, asserted at test_launch.py:75-92); outcome mapping `outcome_of` 311-334; `Deadline` 240 s, floor 5, cutoff 120 (cycle.py:383-412); `LAUNCH_TIMEOUT_S` 120 passed unshortened (cycle.py:1062). |
| 11 | 9.1 to 9.3 Security design T1 to T17, trust boundaries, D3 path | PASS | T6 `TypeError` on `str` argv (runner.py:82-87); T11 stderr cap 500 (runner.py:15, 57-64); T13 as in row 4; T17 probe (launch.py:144-160); operation-id regex checked before store and print (record.py:183, launch.py:127-130); property test is the seeded loop of DF-12. |
| 12 | 10.1 Audit schema and rotation, 10.2 `status`, 10.3 SLO helper | PASS with notes M4, M7 | `audit.py` 159-285 closed key sets per line kind; rotation 5 MiB with `.1` to `.4` and dir fsync (audit.py:141-156); `status_report` 1233-1298 fields match 10.2; `slo_numbers` 1322-1369 gives the four numbers (nearest-rank p95 at 1356). |
| 13 | 11 Files to create or change | PASS | All 9 modules, all 8 per-module test files and all 11 cross-cutting test files exist in the change set; stubs written at test time (DF-10). |
| 14 | 12 Tests | PASS | `FakeRunner` exit 99 plus teardown assert (conftest.py:84-121); `CrashingStore` C1/C3/C4/C5 plus an `os.replace` patch for C2 (DF-15); `test_acceptance_property` (test_cycle.py:4113-4162) covers N in {1,2,6,7,50,99} and the +24 h step; `test_fifty_cycles` (4068-4105). |
| 15 | 13 Gates, sync, packaging | PASS | `p9-g6-verify-deps.txt` ends `PASS ... EXIT=0`; `p9-g10.txt` EXIT=0; `git diff --stat -- pyproject.toml Makefile` printed nothing (unchanged); `p9-g1-summary.md` records 2635 passed. |
| 16 | 14 Defaults | PASS | Every row matched to a constant: timeouts 20/10/10/120/240 (cycle.py:37-41), skew 300 (predicates.py:17), clamp 3600 (github.py:376), stderr 500, audit 5 MiB and 4 files, health 900 and stale 86400 (cycle.py:45-46), op-id regex. |
| 17 | 15 Commands cited | PASS | Every UNVERIFIED row is carried by an `_assumed_shape` fixture or a code comment (`# [PROPOSAL, UNVERIFIED]` at github.py:71, 267; launch.py:39). |
| 18 | 16 Follow-ups FU-1 to FU-12 and Q1 to Q4 | PASS | All 12 follow-ups are in runbook 15.3; Q3 and Q4 are quoted in runbook section 10; Q1 and Q2 are implemented (S1 halt, full-argv retry). |
| 19 | 17 Acceptance criteria AC-1 to AC-25 | PASS | See the phantom-coverage check L3. |
| 20 | 18 Traceability | PASS | Each FR/NFR row of design 18 has a test row in `ac-trace.md` Table 2 whose cited function names I confirmed exist by Grep. |

### Lens checks

| # | Lens check | Result | Evidence |
|---|---|---|---|
| L1 | Semantic coverage: module, signature, schema field, table row, T-1 to T-13, argv G1 to G7, exit code, call contract, timeout, security control, test, AC | PASS | Rows 1 to 20. No design signature is missing; deviations in shape are only the accepted ones (DF-01, DF-25, DF-44, DF-48, OQ-41/41a/48). |
| L2 | Detail preservation: 12-element argv, 35 calls with 3 reserved, 5-page cap, 100-item pages, 24 h cap of 6, 60-min lease, 10-min backoff, 3 attempts, 240 s deadline, 120 s cutoff, 500-byte stderr cap, 5 MiB with 4 files, 0600/0700, 17 entry fields, 7 store keys | PASS | Constants located in code (runner.py:15; github.py:40-49; cycle.py:34-47; record.py:434-443; audit.py:106-107) and pinned by tests (test_runner.py:117-119, test_no_text.py:714, test_github.py:317 and 771, test_record.py:196-197, `test_deadline_constants_are_the_design_values__fr029`). Modes: `os.makedirs(mode=0o700)` plus `os.chmod` (record.py:777-778), `fchmod`/`chmod` 0o600 (792, 377, 864), audit `os.open(..., 0o600)` (audit.py:133). |
| L3 | Phantom coverage: every `ac-trace.md` row names a test that proves the criterion | PASS | I opened the test bodies for AC-1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 24 and 25. Examples: `test_cycle.py:2684-2712` (AC-5) asserts state `claimed`, `launches` 0, no launcher call; `test_concurrency.py:146-186` (AC-11) runs two real spawned processes and asserts exit 75 and one launch; `test_crash_injection.py:287-324` (AC-22) asserts `pending` after C3/C4 and no second launch; `test_cli_e2e.py:299-382` (AC-1) asserts the ordered call list. AC-18 and AC-23 were read through `test_cycle.py:1806-1836` and the gate files. No row proves nothing. |
| L4 | Operational completeness of the runbook | PASS | Runbook sections cover pre-flight (1), config (2), approvers (3), labels (4), init-state and re-approval (5), per-issue order (6), shadow run (7), before cron (8), kill switch (9), exit and reason codes (10, all 59 names), recovery (11), alerting (12), while enabled (13), deployment gate and permissions (14), residual risks R10 to R18 and FU-1 to FU-12 (15). The spec's ten steps (spec lines 386 to 395) each have a section. |

---

## Issues Found

### Blocking findings

None.

### Numbered findings table (all minor)

| id | Severity | Design lines | Implementation location | Expected versus actual |
|---|---|---|---|---|
| M1 | MINOR | 344 (step 1 order: `validate_approvers`, then worktree) | `cycle.validate_setup` 352-358 | Expected the approvers file to be validated before the worktree directory. Actual: the worktree is checked first, and a test pins that order (`test_validate_setup_checks_the_worktree_before_the_approvers__fr027`). Both are exit 2; only the reason name differs when both are invalid. Not in the deviation register. |
| M2 | MINOR | 614 (probe cached in the `OrcaLauncher` instance), 647 | `cycle._launch` 1017-1022; `launch.find_orca` 163-188 | The cache moved to the cycle by accepted OQ-41a, and with one launch per cycle the probe runs at most once, so behaviour is the same. One undeclared addition: `find_orca` skips a `which` result that is not absolute (launch.py:184). Design 8.4 says only "resolved with the injected `which`". It is a hardening with a stated reason in its docstring, but a relative PATH entry now ends as `orca_not_found`. Not in the register. |
| M3 | MINOR | 166 (7 with 5 and 7 with 3 "can occur") | `cycle._candidates` 814-815, `_fail` 999-1005 | The design says a `failed` entry written and then a rate-limited or timed-out later read can both occur in one cycle. The code halts after any launch-step outcome (S1, design 386), so those two combinations are unreachable and exist only as `resolve_exit` tests (test_cycle.py:844-849). The runbook (section 10 Precedence) states the code's behaviour. An internal inconsistency of the design resolved in favour of S1, with no unsafe effect. |
| M4 | MINOR | 715 (cycle line carries `clock_skew_s`: "yes") | `audit._KEYS` 162-166, `cycle._conclude` 1143-1155 | The table marks `clock_skew_s` as present on a cycle line but `discovery_count` as "optional". The implementation treats `clock_skew_s` as optional and writes it only when a skew above 60 s was measured; the runbook (section 10.3) also calls it optional. No behavioural risk. |
| M5 | MINOR (already recorded as Gate B finding B-24 and partly in OQ-46) | 239 (`record` may import `predicates` "types only") | record.py:23-29 imports `format_utc`, `parse_utc`, `valid_issue_number`, `valid_operation_id` and `ApprovalResult`; `test_module_boundaries.py` RULES lines 57-61 put no name limit on `predicates` | The "types only" qualifier is not met and the boundary test no longer enforces it. The test docstring (lines 20-22) says "three functions and one type", but the module now imports four functions. No design type exists to import instead (design line 220), so the departure is forced, but it is not in the Open Questions or the register. Not new; carried forward. |
| M6 | MINOR | 584 (`auth_failed` row: "exit 3 `gh_auth_failed`", no shared or per-issue split) | `cycle._val` 817-827, `cycle._rv` 946-958, `github._failed` 580-581 | Experiment on a `/tmp` copy (`exp1.py`): a 401 on a per-issue events read returns `events_unreadable` with kind `auth_failed`; on the re-read `revalidation_failed`; on G1 `gh_auth_failed`. The cycle turns the per-issue ones into a skip, while it does stop the cycle for per-issue `scope_missing` (exit 3) and `rate_limited` (exit 5). The spec ties `gh_auth_failed` to FR-002 (own login) and treats per-issue read failures as skips (spec lines 337 and 379), so the code follows the spec and the design row is ambiguous. Fail-closed: nothing launches. Cost: a token revoked between G1 and a later call is reported as an ordinary exit-0 `cycle_complete` and refreshes the health age. No cycle-level test covers a per-issue 401. |
| M7 | MINOR | 716 (`note` "re-approved" when the approval event changed) | `cycle._issue_line` 627-642; runbook section 10.2 (`re-approved` row) | The note branch cannot be reached. `c.approval` is set only for candidates that carry no stored approval (no entry, a `failed` entry, or an `attempts_exhausted` tombstone; `record.fail` leaves their approval fields null), and entries that do carry one (`pending`, `launched`, `unknown`, `abandoned` with `pending_at`, `claimed`) never compute an approval. OQ-49 accepts "no emission", and no cycle-level test covers emission (Grep of `test_cycle.py` for `note` found nothing; only `test_audit.py` builds the note). The runbook says the note is "written when the approval event differs from the stored one", which cannot happen; OQ-49 is itself stale because the branch exists. |
| M8 | MINOR | 906 to 933 (traceability) and report counts | `ac-trace.md` lines 5 and 7, `final-change-set.md` section 2 | These reports say 2628 passed and 844 tests; the post-fix `p9-g1-summary.md` says 2635 passed after the Final-gate fix cycle added 7 cases. Wording only. |

---

## Actions Taken

None. Report-only run. The only file written is this report. The single experiment (`/tmp/iwexp/exp1.py`, a `/tmp` copy of the package with the one external import stubbed) read nothing from and wrote nothing into the worktree.

## Recommendations

- Proceed to the next gate steps. No fix pass is needed for this lens.
- Optional, owner decision after the task: M6 (decide whether a per-issue 401 should end the cycle as `gh_auth_failed`; it needs a small rule in `cycle._val` and `_rv` plus one test), M7 (either make the note reachable or delete the dead branch and the runbook sentence), M5 (amend design cell to "pure helpers and types").
- M8: update the two stale counts when the change-set record is next touched.

## Summary

- Checks passed: 24 / 24 (20 design sections and 4 lens checks); 8 minor notes attached
- Checks failed: 0
- Critical issues: 0; blocking (CRITICAL or IMPORTANT): 0; MINOR: 8
- Issues fixed in-place: 0 (report-only)

## Self-audit

If I told the user I found 0 blocking issues, would they believe me? What I did: read all 935 design lines; read all nine source modules (4,743 lines), the runbook (651 lines), the deviation register and the AC trace; compared the design tables to the code line by line; opened about 40 test bodies; ran one experiment. The areas where earlier gates were weakest (cross-module imports, auth-failure classification, the dead `re-approved` branch) produced M5, M6 and M7. I did not find an unimplemented requirement, a wrong constant, a security-control gap or a data-loss path.

## Confidence Gate

- **Confidence:** Verified: 24/24 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 27 | Grep: 50 | Glob: 0 | Bash: 4 (one experiment on a `/tmp` copy; no web research, so no tavily or fallback counts)
- Unchecked items: none. Unverifiable items: none.
- Limits stated openly: the 844 tests were not all read (about 40 bodies, plus Grep confirmation of every cited name); the design's `gh` and Orca reply shapes are UNVERIFIED by the design itself and no real `gh` or Orca was run; the spec is the other agents' lens and was read only at lines 337, 378 to 395 and the T14 to T17 rows.

## QA Complete
