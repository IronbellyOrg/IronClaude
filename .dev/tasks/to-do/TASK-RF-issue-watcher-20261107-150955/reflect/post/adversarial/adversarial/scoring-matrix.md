# Scoring Matrix: issue-watch deviation audit (Steps 3 and 4 judge)

## Scoring Matrix

Judge: debate-orchestrator (Steps 3 and 4), Mode A, depth standard, focus correctness / coverage / deviation classification. Variants: V1 (analyzer, sonnet), V2 (qa, haiku), V3 (refactorer, opus). "Winner" names the variant(s) whose Round 2 final position the judge adopts after re-reading the code; "merge" means the ruling combines positions. An advocate's label was never taken as evidence: every evidence cell is what the judge re-read. Code paths are under `src/superclaude/cli/issue_watch/`; "design" is `docs/designs/issue-watcher.md`, "setup" is `docs/designs/issue-watcher-setup.md`, "task" is `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md`.

The 22 debated points are X-001 to X-010 plus C-013, C-014, C-016, C-017, C-018, C-019, C-022, C-024, C-026, C-034, C-036 and C-037 (C-013 and C-014 are the C ids of X-006 and X-007).

| id | winner or 'merge' | confidence | evidence |
|---|---|---|---|
| X-001 | V2 + V3: Regression LOW, non-blocking | 0.85 | `cli.py:35` `_EXIT_CRASH = 1`, crash path `cli.py:123-129`; design :114 lists `once` exits "0, 2, 3, 4, 5, 6, 7, 75"; AC-17 at design :890 "Each verb's exit codes match section 4". V1's Necessary rests on the `[PROPOSAL]` comment, which is not authority (A-002 rejected); task deviation register :43 lists no authorizing decision. |
| X-002 | V2 + V3: Regression LOW, non-blocking | 0.80 | `cycle.py:1134-1137` returns `cycle_complete`; `audit.py:62-64`; design :718 "`audit.REASONS` is a `frozenset` equal to the spec's reason table"; disclosed at task :905. Behaviour-neutral (exit 0), so V1's MEDIUM is rejected. |
| X-003 | merge: Authorized for three functions plus the type; Regression LOW for `valid_operation_id` | 0.85 | `record.py:23-29` imports `ApprovalResult`, `format_utc`, `parse_utc`, `valid_issue_number`, `valid_operation_id`. Task :332 allows "`predicates` of the package (`parse_utc`, `format_utc`, `valid_issue_number`)"; design :239 says "types only", which covers `ApprovalResult`. `valid_operation_id` is named in neither and contradicts design :239 (V2 and V3 in Round 2). V1's Necessary is rejected: `launch.py:36` shows the conformant alternative (a local copy). |
| X-004 | all three: Necessary LOW | 0.90 | `audit.py:203` `_MAX_ISSUE = 999_999_999`, `launch.py:30` `MAX_ISSUE_NUMBER`; design :237 gives `audit` no package import and :240 lets `launch` import only `runner`. A parity test for the copies is advisory. |
| X-005 | all three: Authorized | 0.85 | `runner.py:89` `start = time.monotonic()`; task :193 orders `duration_s` "with `time.monotonic()` ... (the one clock read outside the cycle; it is never used for a decision)". |
| X-006 | merge: V2's class, V1/V3's non-blocking: Regression MEDIUM, non-blocking | 0.80 | Task :188 "No test may use `pytest.skip`, `skipif` or `xfail`, because gates G-1 and G-3 require zero skipped tests."; five sites: `tests/issue_watch/test_cli.py:967`, `:1070`, `test_record.py:739`, `test_cycle.py:735`, `:4694`. Task :908 records them as minor ("nothing was skipped in any recorded run"). No production behaviour changes, so it does not gate. |
| C-013 | same ruling as X-006 | 0.80 | Same evidence as X-006. |
| X-007 | merge: V2's finding, V1/V3's LOW severity, V2/V3's blocking flag: Regression LOW, BLOCKING | 0.85 | `cycle.py:1048` is the last `launch_allowed()` check; `cycle.py:1060` `mark_pending`, `:1061` `self._save()  # FR-010: durable before the launch call`, `:1062` the `launcher.launch` call, no check between; `cycle.py:410` `launch_allowed`. Design :647: Orca launch "not started when `elapsed() > 120`; the step ends with no entry and no reason other than a `budget_exhausted` decision line"; AC-19 at design :892 "no launch starts after 120 s". LOW because the window is one local fsync'd save. |
| C-014 | same ruling as X-007 | 0.85 | Same evidence as X-007. |
| X-008 | all three: advisory LOW | 0.85 | `predicates.py:57` `^[A-Za-z0-9._:-]{1,128}$` allows a leading `-`; `launch.py:127-130` `retry_argv` validates before `status` prints it. No spec anchor, so advisory. |
| X-009 | all three: not a defect | 0.95 | `cycle.py:693-694` (first DISABLED check under the lock) and `cycle.py:1033-1034` (`disabled_mid_cycle`); V1's `cycle.py:308` is wrong. The 1033-1060 window is INV-006 (advisory LOW). |
| X-010 | V2 + V3: Regression LOW, non-blocking (same root as X-002) | 0.80 | Task :199 "exactly 57 entries (52 from spec lines 332-358 plus the five proposals above)"; DF-41 (`research/06-gap-fill-decisions.md:175`) names 57; setup :344 and `test_audit.py:215-219` pin 59. |
| C-016 | all three: advisory, accepted residual | 0.80 | `record.py:689-703` excludes future-dated `consumed_at`; spec-final.md:456 (R16) records it as an accepted residual. |
| C-017 | all three: advisory LOW (V2 withdrew Regression in Round 2) | 0.85 | `record.py:421-431`: `disabled()` uses `lexists`, `disabled_since()` uses `os.stat`, so a dangling symlink disables cycles (setup :298) but `status` cannot show "disabled since" (setup :302). Contradicts the runbook, not an acceptance criterion. |
| C-018 | all three: advisory LOW | 0.85 | `cycle.py:685-690` catches only `_Stop`; safety holds (INV-012); the record and retry hint are lost. |
| C-019 | all three: advisory MEDIUM, unverified | 0.60 | `runner.py:91-101` `subprocess.run(..., capture_output=True, timeout=...)`; inferred, PATH stubs cannot show it. |
| C-022 | all three: advisory LOW, verified | 0.80 | `predicates.py:205-209` same-second rule; the spec words it the same way (V1 gap 8). |
| C-024 | all three: advisory MEDIUM, unverified | 0.65 | `launch.py:326-334` `_first_hit` also searches error paths; `launch.py:39-45` `OPERATION_ID_PATHS` marked `[PROPOSAL, UNVERIFIED]`; design :636 defers the real reply shape to FU-1. |
| C-026 | V2 + V3: Regression LOW, non-blocking | 0.70 | Design :634: "`agent_session_operation_unknown` anywhere in stdout or stderr" maps to `unknown`; `runner.py:15` `STDERR_CAP_BYTES = 500`, cap at `runner.py:57-64`, applied before return at `:126`; `launch.py:322` searches the capped text, so a marker past byte 500 is missed. |
| C-034 | all three: Drift LOW (documentation) | 0.85 | Setup :53 platform list omits `reset` although `cli.py:314` runs the platform check; setup :432 and design :726 list `status` exits 0, 1, 6 while design :115 lists 0, 1, 2, 6 and `cli.py:169` exits 2. |
| C-036 | V2 + V3: Regression LOW, non-blocking, effectively unreachable | 0.70 | Design :739 `retry` lists "`unknown` entries with an `operation_id`"; `cycle.py:1271`, `:1279-1280` also require `launch_cwd` and drop ids `retry_argv` refuses; `record.py:182-184` and `mark_pending` (`record.py:548`) always set an absolute `launch_cwd`, so no reachable entry is dropped today. |
| C-037 | all three: advisory LOW, verified | 0.85 | `audit.py:393-402`: reason membership is checked, the exit code is not; `"kind": "cycle"` is always written at `:402`. |

## Shared Assumptions

Tally for A-001 to A-010: **accept 5, reject 3, qualify 2**.

| id | ruling | reason |
|---|---|---|
| A-001 | accept | The R-003 decision register (`research/06-gap-fill-decisions.md`) and the task file are the authorizing artifacts where they amend the design. |
| A-002 | reject | A `[PROPOSAL]` comment (`cli.py:35`, `audit.py:55-57`) is the executor's own label, not authority. |
| A-003 | accept | Design and spec text are the baseline; the tasklist amends them only where it says so. |
| A-004 | reject | Not every citation is correct: V1 `cycle.py:335-337` (real 1060-1062) and `cycle.py:308` (real 693 and 1033); V3 `src/superclaude/main.py` (real `src/superclaude/cli/main.py:563-565`); V2 `p9-g2-summary.md:8` (real :9). |
| A-005 | accept | No variant ran tests (V2:55 says so); inferred findings carry no runtime check. |
| A-006 | accept | The audited change is `e8db2fe6..26f551f4`. |
| A-007 | qualify | The Orca reply shape is UNVERIFIED (`launch.py:39-45`, design :636); findings that depend on it (C-024) stay unverified advisory. |
| A-008 | qualify | Where design rows disagree on `status` exits, design :115 (0, 1, 2, 6) and the code (`cli.py:169`) win; design :726 is the omission. |
| A-009 | reject | The persona slices (38, 13 and 18 units) barely overlap; silence is not agreement. |
| A-010 | accept | Calibrated confidence 0.70 / 0.82 / 0.76 is context, not truth. |

## Uncontested and Single-Source Points

"Uncontested" means two or more variants raise the point and none disputes it; "single-source" names the one variant that raises it. "Verified" means the judge re-read the cited lines. Unverified single-source points are Grounding Gaps and are not counted as agreed.

| id | status | judge ruling | verified |
|---|---|---|---|
| S-001 | uncontested (structural) | Slices of 38 / 13 / 18 units | yes |
| S-002 | uncontested (structural) | Only V2 gives a verdict (V2:8, FAIL) | yes |
| S-003 | uncontested (structural) | Row counts 12 / 5 / 11 | yes |
| S-004 | uncontested (structural) | Gap tables: V1 13, V2 none, V3 5 | yes |
| S-005 | uncontested (structural) | Provenance limits stated at V1:51-57 and V3:62-66 | yes |
| S-006 | uncontested (structural) | V1 header "1 MEDIUM, 11 LOW" (V1:7) contradicts its rows 1 and 2, both MEDIUM | yes |
| S-007 | uncontested (structural) | V2:53 is the only recommendation; V3 gives "do not consolidate `_fsync_dir`" guidance | yes |
| S-008 | uncontested (structural) | Adherent-area notes in all three; V3:34-61 itemizes them | yes |
| C-001 | uncontested (V1, V3); scored with X-001 | Regression LOW, non-blocking | yes |
| C-002 | uncontested (V1, V3); scored with X-002 | Regression LOW, non-blocking | yes |
| C-003 | uncontested (V1, V3); scored with X-002 / X-010 | Part of the reason-count Regression; remedy is a document amendment | yes |
| C-004 | single-source V1 | Authorized (the five proposed reasons that task :199 lists) | yes |
| C-005 | uncontested (all); scored with X-003 | Same merge as X-003 | yes |
| C-006 | uncontested (V1, V3) | Drift LOW: `cli.py:319` reaches `predicates.format_utc` through `cycle` | yes |
| C-007 | uncontested (V1, V3); scored with X-004 | Necessary LOW | yes |
| C-008 | uncontested (V1, V3) | Drift LOW: `cycle.py:468` `_LOGIN` copies `github.py:134` `_LOGIN_RE`; design :241 lets `cycle` import `github` | yes |
| C-009 | single-source V3 | Drift LOW for `cycle.py:76` (cycle may import `predicates`, design :241); Necessary LOW for the `audit` copy (design :237) | yes |
| C-010 | single-source V1 | Necessary LOW: `predicates.py:57` and `launch.py:36` (design :240) | yes |
| C-011 | single-source V3 | Necessary LOW: `record.py:310-315`, `audit.py:204-206`; do not consolidate `_fsync_dir` | yes |
| C-012 | uncontested (V1, V3) | `stderr_fallback` wall clock (`audit.py:395-397`): Drift LOW; runner monotonic clock: Authorized (X-005) | yes |
| C-015 | uncontested (V1, V3); scored with X-009 | Not a defect; the window is INV-006, advisory | yes |
| C-020 | single-source V1 | Grounding Gap (dead-code list not re-read) | no |
| C-021 | single-source V1 | Grounding Gap (`mark_pending` state-versus-launches check not re-read line by line) | no |
| C-023 | single-source V1 | Advisory LOW: `launch.py:318-319` classes a post-spawn `OSError` as `spawn_error` | yes |
| C-025 | uncontested (V1, V3); scored with X-008 | Advisory LOW | yes |
| C-027 | single-source V1 | Grounding Gap (V1 did not confirm the approvers-file `fstat` gap; judge did not either) | no |
| C-028 | single-source V1 | Grounding Gap (the `re-approved` branch at `cycle.py:641` was located but its reachability not traced) | no |
| C-029 | single-source V1 (V3 partial adherent note) | Grounding Gap (seven DF anchors not all re-read) | no |
| C-030 | single-source V2 | Necessary LOW: `test_cycle.py:4150-4154` keeps the six-per-24h cap | yes |
| C-031 | single-source V2 | Authorized (DF-05, `research/06-gap-fill-decisions.md:28`) | yes |
| C-032 | single-source V3 | Authorized (DF-29, `research/06-gap-fill-decisions.md:208`); corrected path `src/superclaude/cli/main.py:563-565` | yes |
| C-033 | single-source V3 | Necessary LOW: `cycle.py:1225-1230` reads `launch._ORCA_CLIS` | yes |
| C-035 | single-source V3 | Advisory LOW: `cli.py:309-313` "not both" message is also printed when neither reset flag is given | yes |
| C-038 | single-source V3 | Advisory LOW (docstring miscount `test_module_boundaries.py:20-21`), fixed with X-003 | yes |
| C-039 | V2 and V3 notes | Grounding Gap (wiring and subprocess-coverage claim not verified by the judge) | no |

## Convergence Assessment

- **Total points:** 67 = 22 debated + 8 structural (S-001 to S-008) + 27 other C points + 10 shared assumptions (A-001 to A-010).
- **Agreed: 56.**
  - All 22 debated points: at least 2 of 3 advocates hold the same final category after Round 2.
  - All 8 structural points, verified.
  - 21 of the 27 other C points (uncontested or single-source, verified by the judge): C-001 to C-012, C-015, C-023, C-025, C-030 to C-033, C-035, C-038.
  - 5 accepted assumptions: A-001, A-003, A-005, A-006, A-010.
- **Not agreed: 11** = 6 Grounding Gaps (C-020, C-021, C-027, C-028, C-029, C-039) + 3 rejected and 2 qualified assumptions.
- **Convergence:** 56 / 67 = **0.836**, above the 0.80 threshold: **CONVERGED**.

## Taxonomy Coverage

| Level | Meaning | Points addressed | Count > 0 |
|---|---|---|---|
| L1 | Surface: wording, documentation, counts in text | C-038, C-034, X-010 / C-003, C-035 | yes |
| L2 | Structural: module boundaries, duplication, imports | X-003, X-004, C-006, C-008, C-009, C-011, C-033 | yes |
| L3 | State mechanics: ordering, persistence, guards, timing | X-007 / C-014, C-036, C-018, C-017, C-016, C-026 | yes |

Every level has at least one addressed point: **taxonomy gate PASS**.

## Invariant-Probe Gate

Source: `invariant-probe.md` in this directory (12 findings, INV-001 to INV-012).

- HIGH UNADDRESSED: 0.
- MEDIUM UNADDRESSED: 1, INV-001 (at-most-once holds only per single store per login). Logged as a scope warning: design :17 (invariant-probe cites :21) already limits the guarantee to "per intact, single dispatch store per login" and names R12 as a documented residual risk. Not a code defect.
- LOW: INV-004 to INV-009 and INV-012. INV-003 and INV-004 constrain the X-007 fix (see the late-launch ruling in `refactor-plan.md`).

**Invariant-probe gate: PASS** (no HIGH-severity UNADDRESSED invariant).
