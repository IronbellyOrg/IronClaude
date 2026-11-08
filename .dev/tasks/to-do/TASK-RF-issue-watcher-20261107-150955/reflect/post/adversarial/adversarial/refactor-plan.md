# Refactoring Plan: Merge into Base

## Overview

- **Base:** V2 (qa card), selected in `base-selection.md` (final 0.803 against V3 0.741 and V1 0.718).
- **Merge sources:** V3 (adherent list, runbook claims, gaps C-017, C-035, C-036, C-037, parity-test gap) and V1 (13 gaps, at-most-once notes).
- **Debate:** converged, 56 / 67 = 0.836 (`scoring-matrix.md`).
- **Audited change:** `e8db2fe6..26f551f4` (issue-watch poller, issue #331).
- **Classification rules applied:** a Regression quotes the criterion it contradicts; precedence Regression > Drift > Necessary > Authorized; thin evidence is a Grounding Gap; a code defect with no spec anchor is advisory and never gates; an advocate's label is not evidence; only a Regression can block.
- **Result:** 19 register rows (7 Regression, 4 Drift, 3 Necessary, 5 Authorized), 1 of them blocking; 17 advisory rows; 6 Grounding Gaps.

Path shorthand: code paths are under `src/superclaude/cli/issue_watch/`; "design" is `docs/designs/issue-watcher.md`; "setup" is `docs/designs/issue-watcher-setup.md`; "task" is `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`; "DF register" is `research/06-gap-fill-decisions.md` in the task folder.

## Planned Changes (final deviation register)

This is the one final register. "Authority / criterion" holds the quoted criterion for a Regression and the authorizing artifact or rationale for every other class.

| Row | ids | Category | Severity | Corrected file:line | Authority / criterion | Blocking | Remediation (file; change; verifier) |
|---|---|---|---|---|---|---|---|
| R-1 | X-007, C-014 | Regression | LOW | `cycle.py:1060-1062` (last check `cycle.py:1048`) | Design :647 "not started when `elapsed() > 120`; the step ends with no entry and no reason other than a `budget_exhausted` decision line"; AC-19 (design :892) "no launch starts after 120 s" | **YES** | `cycle.py`; capture the document before `mark_pending`, re-check `launch_allowed()` after `self._save()`, restore and save the captured document and raise `_Skip("budget_exhausted")` if the cutoff has passed (see the late-launch ruling); new `tests/issue_watch/test_cycle.py` case whose clock passes 120 s inside `store.save`: asserts no launcher call, the document restored, and a `budget_exhausted` decision line |
| R-2 | X-001, C-001 | Regression | LOW | `cli.py:35`, `cli.py:123-129` | Design :114 `once` exits "0, 2, 3, 4, 5, 6, 7, 75"; AC-17 (design :890) "Each verb's exit codes match section 4" | no | Design :114 and section 4.3, spec reason table; add exit 1 (`cycle_crashed`) as an amended exit; verifier `tests/issue_watch/test_cli.py:630` (crash exit) unchanged and passing |
| R-3 | X-002, X-010, C-002, C-003 | Regression | LOW | `audit.py:55-57`, `audit.py:62-64`, `cycle.py:1134-1137` | Design :718 "`audit.REASONS` is a `frozenset` equal to the spec's reason table"; task :199 "exactly 57 entries"; DF-41 (DF register :175) names 57 | no | Design :718, task :199, DF-41 and the spec reason table; record 59 names including `cycle_complete` and `cycle_crashed`; verifier `tests/issue_watch/test_audit.py:215-219` (pins 59) |
| R-4 | X-003 (`valid_operation_id` only), C-005 part | Regression | LOW | `record.py:23-29` | Design :239 `record` may import `predicates` "(types only, ...)"; task :332 lists only `parse_utc`, `format_utc`, `valid_issue_number` | no | Either amend task :332 and design :239 to name `valid_operation_id`, or give `record.py` a local copy as `launch.py:36` does; fix the miscounted docstring at `tests/issue_watch/test_module_boundaries.py:20-21` (C-038); verifier `test_module_boundaries.py:57-61` |
| R-5 | X-006, C-013 | Regression | MEDIUM | `tests/issue_watch/test_cli.py:967`, `:1070`; `test_record.py:739`; `test_cycle.py:735`, `:4694` | Task :188 "No test may use `pytest.skip`, `skipif` or `xfail`, because gates G-1 and G-3 require zero skipped tests." (graded minor at task :908) | no | Those four test files; replace the root-only `skipif` marks with checks that hold for root and non-root, and give `:4694` a stubbed mountinfo text instead of reading `/proc/self/mountinfo`; verifier `uv run pytest tests/issue_watch -rs` reports 0 skipped |
| R-6 | C-026 | Regression | LOW | `runner.py:57-64`, `runner.py:126`, `launch.py:322` | Design :634 "`agent_session_operation_unknown` anywhere in stdout or stderr" maps to `unknown` | no | `runner.py` / `launch.py`; detect the operation-unknown marker on the full stderr before the 500-byte cap is applied (`runner.py:15`); new launch test with the marker after byte 500, expecting `unknown` |
| R-7 | C-036 | Regression | LOW (effectively unreachable) | `cycle.py:1271`, `cycle.py:1279-1280` | Design :739 `retry` lists "`unknown` entries with an `operation_id`" | no | `cycle.py`; when an `unknown` entry with an id has no usable retry argv, print it with a warning instead of dropping it; new `test_cycle.py` case |
| D-1 | C-034 | Drift | LOW | setup :53, setup :432, design :726 | Rationale: documentation disagrees with design :115 (`status` 0, 1, 2, 6), `cli.py:169` (exit 2) and `cli.py:314` (`reset` runs the platform check) | no | Setup :53 add `reset` to the platform list; setup :432 and design :726 add exit 2; verifier: re-read against `cli.py:169` and `:314` |
| D-2 | C-006 | Drift | LOW | `cli.py:319` | Rationale: `cli` uses `cycle.format_utc`, a `predicates` function re-exported by `cycle`; design :242 does not list `predicates` for `cli` | no | Design :242; note the transitive use, or give `cycle` a public stamp helper; verifier `test_module_boundaries.py` |
| D-3 | C-008, C-009 (cycle copy) | Drift | LOW | `cycle.py:468`, `cycle.py:76` | Rationale: `_LOGIN` copies `github.py:134` `_LOGIN_RE` and `_UTC_TS_FORMAT` copies the `predicates` format although design :241 lets `cycle` import both modules | no | `cycle.py`; use the `github` and `predicates` values; verifier: existing login and timestamp tests in `test_cycle.py` |
| D-4 | C-012 (`stderr_fallback`) | Drift | LOW | `audit.py:395-397` | Rationale: reads the wall clock directly instead of a time passed by the caller; the docstring calls it "a stamp, not a decision" | no | `audit.py` callers; pass `ts` where the caller holds the cycle clock; verifier `test_audit.py` fallback cases |
| N-1 | X-004, C-007, C-010, C-011, C-009 (audit copy) | Necessary | LOW | `audit.py:203`, `launch.py:30`, `launch.py:36`, `record.py:310-315`, `audit.py:204-206` | Design :237 (`audit` imports nothing from the package) and :240 (`launch` imports only `runner`) force local copies | no | None required; parity test is advisory (see Advisory Gaps) |
| N-2 | C-030 | Necessary | LOW | `tests/issue_watch/test_cycle.py:4150-4154` | Rationale: test keeps the six-per-24h cap (`cycle.py:36` `DAY_CAP = 6`) reachable under the test clock | no | None |
| N-3 | C-033 | Necessary | LOW | `cycle.py:1225-1230` | Rationale: reads `launch._ORCA_CLIS`, the one name design :240 lets `launch` take from `install_user_setup` | no | None |
| A-1 | X-003 (three functions plus `ApprovalResult`), C-005 part | Authorized | n/a | `record.py:23-29` | Task :332 (`parse_utc`, `format_utc`, `valid_issue_number`); design :239 "types only" covers `ApprovalResult` | no | None |
| A-2 | X-005, C-012 (runner part) | Authorized | n/a | `runner.py:89` | Task :193 `duration_s` with `time.monotonic()`, "never used for a decision" | no | None |
| A-3 | C-004 | Authorized | n/a | `audit.py:55-57` region | Task :199 lists the five proposed reasons | no | None |
| A-4 | C-031 | Authorized | n/a | gh dependency | DF-05 (DF register :28) | no | None |
| A-5 | C-032 | Authorized | n/a | `src/superclaude/cli/main.py:563-565` | DF-29 (DF register :208) | no | None |

## Explicit Rulings

### Late-launch ruling (X-007 / C-014, row R-1)

- **Defect.** `cycle.py:1048` is the last cutoff check. After it, `cycle.py:1060` marks the entry pending and `cycle.py:1061` saves it durably; `cycle.py:1062` then launches with no further check. If the fsync'd save crosses 120 s, a launch starts after the cutoff, contradicting design :647 and AC-19 (design :892). The Gate C fix (task :901) closed the git-call window but not the save window.
- **Severity LOW, blocking YES.** The window is one local save, so the chance is small, but it contradicts a stated acceptance criterion, and a Regression of that kind blocks.
- **Required fix.** In `cycle.py`, before line 1060 capture `prev = self.doc`. After `self._save()` at 1061 and before the launch at 1062: if `not self.deadline.launch_allowed()`, call `self._set(prev)`, `self._save()`, then `raise _Skip("budget_exhausted")`. Durable-before-launch (FR-010) is kept because the save still precedes any launch.
- **INV-003 (crash between save and restore).** A crash there leaves a pending entry that the sweep turns into `pending_orphan` (`record.py:638-639`): safe (no launch happened, no double launch possible) but stranded until `reset --forfeit-guarantee`. Accepted; restoring is still better than leaving the entry pending, because no agent would ever post a marker for it.
- **INV-004 (what to restore).** Restore the whole document captured before `mark_pending`, not individual fields: `validate` rejects `launches == 1` without `consumed_at` and `pending_at` (`record.py:206-207`) and rejects `failed` with `launches != 0` (`record.py:208-209`), so a field-by-field undo can write an invalid store.
- **INV-005 (240 s budget).** Not part of this fix and not a defect: the launch timeout is a fixed 120 s, and design :649 already accepts a worst case of 240 s inside the 300 s cadence. Advisory only.
- **INV-006 (DISABLED after the save).** Advisory LOW; a DISABLED re-check may sit next to the cutoff re-check but is not required by any criterion.

### Other rulings

| Point | Ruling | Basis |
|---|---|---|
| X-001 | Regression LOW, non-blocking (R-2). V1's Necessary rejected. | Design :114 and AC-17 (design :890) list no exit 1 for `once`; the `[PROPOSAL]` comment at `cli.py:35` is not authority (A-002 rejected). Remedy is a design amendment; behaviour stays. |
| X-002 | Regression LOW, non-blocking (R-3). V1's MEDIUM rejected. | Design :718 equality with the spec reason table is broken by `cycle_complete` (`cycle.py:1134-1137`); exit 0, so behaviour-neutral. |
| X-010 | Same root as X-002, folded into R-3. | Task :199 and DF-41 say 57; code and setup :344 say 59. One document amendment fixes both. |
| X-003 | Split: Authorized for `parse_utc`, `format_utc`, `valid_issue_number` and `ApprovalResult` (A-1); Regression LOW for `valid_operation_id` (R-4). | Task :332 names the three functions; design :239 "types only" covers the type; neither names `valid_operation_id`. |
| X-004 | Necessary LOW (N-1). | Design :237 and :240 forbid the imports that would remove the copies. |
| X-005 | Authorized (A-2). | Task :193 orders the monotonic clock read in `runner`. |
| X-006 / C-013 | Regression MEDIUM, non-blocking (R-5). | Task :188 forbids `skipif`; five sites exist. No production behaviour changes and nothing was skipped in a recorded run (task :908), so it does not gate. |
| C-034 | Drift LOW, documentation only (D-1). | Docs disagree with design :115 and `cli.py:169`, `:314`; no acceptance criterion is contradicted by the code. |
| C-036 | Regression LOW, non-blocking, effectively unreachable (R-7). | Design :739 promises every `unknown` entry with an id; `record.py:182-184` and `record.py:548` make `launch_cwd` always present today, so no reachable entry is dropped. |
| C-026 | Regression LOW, non-blocking (R-6). | Design :634 "anywhere in stdout or stderr"; the 500-byte cap (`runner.py:15`, `:126`) hides a later marker from `launch.py:322`. |
| C-024 | Advisory MEDIUM, unverified; does not gate. | The real Orca reply shape is UNVERIFIED (`launch.py:39-45`, design :636, FU-1); no criterion can be quoted against it until FU-1 lands. |
| C-017 | Advisory LOW, verified; V2's Round 1 Regression withdrawn. | `record.py:421-431` `lexists` versus `os.stat` contradicts only the runbook (setup :298, :302), not an acceptance criterion. |

## Advisory Gaps

None of these gates the verdict. "Verified" means the judge re-read the cited lines.

| Gap | Finding | Location | Judge severity | Verified |
|---|---|---|---|---|
| C-016 | Future-dated `consumed_at` falls outside the day-cap window; accepted residual R16 (spec-final.md:456) | `record.py:689-703` | LOW (accepted residual) | yes |
| C-017 | Dangling DISABLED symlink disables cycles but `status` cannot show "disabled since" | `record.py:421-431` | LOW | yes |
| C-018 | Exception after launch loses the record and retry hint; safety holds (INV-012) | `cycle.py:685-690` | LOW | yes |
| C-019 | Large child output is fully buffered before the cap | `runner.py:91-101` | MEDIUM | no (inferred) |
| C-022 | Same-second approval rule | `predicates.py:205-209` | LOW | yes |
| C-023 | Post-spawn `OSError` classed `spawn_error` | `launch.py:318-319` | LOW | yes |
| C-024 | Operation-id search also walks error paths; reply shape UNVERIFIED (FU-1) | `launch.py:326-334`, `launch.py:39-45`, design :636 | MEDIUM | no |
| X-008 / C-025 | Operation-id pattern allows a leading `-` | `predicates.py:57`, `launch.py:127-130` | LOW | yes |
| C-035 | "not both" message also printed when neither reset form is given | `cli.py:309-311` | LOW | yes |
| C-037 | Fallback line checks the reason but not the exit code | `audit.py:393-402` | LOW | yes |
| Parity tests | No test pins the local copies in N-1 to their sources | `audit.py:203`, `launch.py:30`, `launch.py:36` | LOW | yes |
| INV-001 | At-most-once holds per single store per login only; scope warning, already stated in design :17 (R12) | design :17 | MEDIUM (scope) | yes |
| INV-005 | Late-launch fix does not shorten the 240 s worst case; accepted at design :649 | `cycle.py:1062` | LOW | yes |
| INV-006 | DISABLED not re-checked after the origin call or the save | `cycle.py:1033`, `:1041-1045`, `:1061` | LOW | yes |
| INV-007 | Reserved call budget may be exhausted by paged re-reads; liveness only | `github.py:448-454` (per invariant-probe) | LOW | no |
| INV-008 | Day cap and clock steps (same root as C-016) | `record.py:689-690`, `:696` | LOW | yes |
| INV-009 | Local `pending_at` against server marker time; liveness only | `cycle.py:1060` | LOW | no |

Grounding Gaps (evidence too thin to classify; carried as open questions, not findings): C-020 (dead code), C-021 (`mark_pending` state check), C-027 (approvers-file `fstat`), C-028 (`re-approved` branch near `cycle.py:641`), C-029 (seven anchored departures), C-039 (wiring and subprocess coverage). X-009 / C-015 is not a defect (`cycle.py:693-694`, `:1033-1034`); C-038 is folded into R-4.

## Changes NOT Being Made (with rationale)

| Proposed by | Change not made | Rationale |
|---|---|---|
| V2 | HIGH (and calibrator MEDIUM) severity for the late launch | The window is one local fsync'd save; LOW, still blocking because it contradicts AC-19. |
| V2 | "Blocking" label on its Drift row 2 | Only a Regression can block. |
| Calibrator | Reading the fix as "skip after the save and leave the entry pending" | Leaves a stranded pending entry on every hit; INV-003 and INV-004 require a restore. V2:53 itself is compatible with the restore. |
| V1 | "Regression 0" | X-001, X-002, X-003 (part), X-006, X-007, C-026 and C-036 each contradict a quoted criterion. |
| V1 | Line ranges `cycle.py:335-337` and `cycle.py:308` | Wrong; corrected to `cycle.py:1060-1062` and `cycle.py:693-694` / `:1033-1034`. |
| V1 | MEDIUM for X-002 | Behaviour-neutral (exit 0); LOW. |
| V3 | Path `src/superclaude/main.py:563-565` | Does not exist; corrected to `src/superclaude/cli/main.py:563-565`. |
| any | Consolidating `_fsync_dir` (`record.py:310-315`, `audit.py:204-206`) | Design :237 forbids `audit` importing from the package; the copy is Necessary. |
| invariant-probe | Treating INV-005 as a defect | Design :649 accepts the 240 s worst case. |

## Risk Summary

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| R-1 fix restores fields instead of the whole document and writes an invalid store | Medium if done field by field | Store unreadable, exit 6 | Restore the captured document (INV-004); the new test asserts the restored document equals the captured one |
| R-1 re-check placed before the save instead of after it | Low | The save window stays open | The test advances the clock inside `store.save`, so a pre-save check fails it |
| Crash between the save and the restore | Very low | Entry stranded as `pending_orphan` until `reset --forfeit-guarantee`; no double launch | Accepted (INV-003) |
| R-5 root-independent rewrites change what the five tests prove | Low | Lost coverage of permission paths | Keep each test's assertion; change only how the unreadable state is produced |
| Document amendments (R-2, R-3, R-4, D-1, D-2) drift from tests again | Low | Repeat findings | Each amendment names the pinning test as its verifier |
| Judge not independent of the variants (`judge_class_collision: true`) | n/a | Scores may share the variants' blind spots | Disclosed; Step 5 merge review should be run by a fresh context |

## Final Verdict

**FAIL.**

One blocking Regression survives: R-1 (X-007 / C-014), a launch can start after the 120 s cutoff when the pending-state save crosses it, contradicting design :647 and AC-19 (design :892). The other six Regressions are non-blocking (four are document amendments, one is test hygiene, one is effectively unreachable). The verdict becomes PASS-with-deviations once R-1 is fixed and its verifier test passes.

Surviving counts: Regression 7 (1 blocking), Drift 4, Necessary 3, Authorized 5, advisory 17, Grounding Gaps 6.

## Review Status

| Item | Status |
|---|---|
| Step 3 (scoring) | Complete: `scoring-matrix.md`, `base-selection.md` |
| Step 4 (refactor plan) | Complete: this file |
| Step 5 (merge execution) | Not started; the merge executor applies this register to the V2 base |
| Independent review of this plan | Not done; the judge reviewed its own work only, and the reverse scoring pass was not an independent instance |
| Tests | None run by the judge; every verifier above is a test to add or run |
