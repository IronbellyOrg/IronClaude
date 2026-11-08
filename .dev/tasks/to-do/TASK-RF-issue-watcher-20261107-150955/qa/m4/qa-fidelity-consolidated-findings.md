# Consolidated fidelity findings (M4 gate, fix cycle 1)

**Step:** 9.M4. **Date:** 2026-11-08.
**Inputs (exact names, all in `qa/m4/`):**
- `qa-source-fidelity-report-1.md` (design-fidelity lens, "report 1"; its finding ids are `M1` to `M8`, cited below as `D-M1` to `D-M8`)
- `qa-source-fidelity-report-2.md` (spec-fidelity lens; its ids `M2-1` to `M2-9` are kept as written)
- `qa-cross-source-contradictions-report.md` (cross-source lens; its ids `C-01` to `C-41` and `N-01` to `N-13` are kept as written)

Ids `M-1`, `M-2`, ... below are the unique consolidated ids. They stay unchanged in cycle 2.

## blocking: 1, minor: 65

Source counts before deduplication: design-fidelity 0 blocking + 8 minor; spec-fidelity 1 blocking + 8 minor; cross-source 0 blocking + 54 findings (41 covered by a decision + 13 NEW, all minor). Total raw: 1 blocking + 70 minor = 71. After deduplication: 1 blocking + 65 minor = 66 ids (M-1 to M-66). The five merges are: D-M4 into M-1; D-M3 and N-01 into M-4; M2-3 and N-02 into M-10; M2-2 and C-41 into M-9; D-M2 and C-38 into M-3.

## Regrade of the blocking finding (checked against the cited spec line and the cited code)

**M-1 is genuinely blocking.** I read the three sources myself.
- Spec Section 3 "Claimed" (`spec-final.md` line 100): "The cycle line records the offset between the local clock and the `Date` header of the `gh api user --include` reply, **and** an offset above 60 s [PROPOSAL] writes a `clock_skew` warning line." Two separate duties. The first has no threshold.
- Design table (`issue-watcher.md` line 715): `clock_skew_s` is "yes" in the cycle-line column, while `discovery_count` on the same table is "optional" in that column. The design therefore also says the field is always on the cycle line.
- Code (`cycle.py` lines 751-756): `self.clock_skew_s` is assigned only inside `if skew > SKEW_WARN_S:`. `_conclude` (line 1154) passes the attribute, which stays `None` otherwise, and `audit.py` leaves a `None` value out of the line. At 60 s or less the cycle line carries no offset.
- Test (`test_cycle.py` line 1710): `assert "clock_skew_s" not in _the_cycle_line(lines)` for skews 0, 59, 60 and -60. The test pins the omission; no test asserts the field is present at or below the threshold (lines 1724 and 1726 assert it only above).
- No decision covers it: DF-22 authorizes the 60/61 s boundary tests and the `clock_skew` warning reason, not dropping the cycle-line field; OQ-36 to OQ-51 do not mention it.

Grade: the code does not do what the spec sentence says (behaviour against a stated requirement, data the operator is meant to see before the warning threshold). It is small in impact and cheap to fix, but it matches the blocking definition "wrong behaviour" against the spec, so it stays blocking. Design-fidelity (D-M4) graded the same fact minor because the runbook section 10.3 also calls it optional; that runbook wording repeats the departure and does not authorize it. Fix scope: set the offset on every cycle where the `Date` header parses, keep the warning guarded by `> 60`, change the assertion at `test_cycle.py:1710` to require the value (and the runbook sentence if it calls the field optional).

**Other regrades, honestly checked.**
- M-6 (a 401 on a per-issue read is a skip, not exit 3): stays minor. Spec line 337 ties `gh_auth_failed` to Section 3 Own login, FR-002, NFR-008, NFR-007, FR-007, not to per-issue reads, so the code follows the spec; design line 584 is flat and ambiguous (line 588 says per-issue failures skip). Fail-closed, nothing launches.
- M-7 (the `re-approved` note is never written): stays minor. Spec line 272 says a newer approval event "is reported as `re-approved`", and the code never emits it, so this is a real gap against that sentence. It is owner-accepted as OQ-49 (`TASK-RF...md` line 960: "This task adds no code for it"), and the prompt of the gate lists OQ-49 as not drift. The runbook sentence that the note "is written when the approval event differs" is vacuously true, not false.
- M-12 (clock reads outside the `Clock` Protocol, NFR-014 / spec lines 231 and 269): stays minor. The reads are `audit.stderr_fallback` stamps and `time.monotonic` for `duration_s`; none feeds a decision, and the module documents this. A literal reading of "every time read" is not met, which is why it is recorded.
- M-10 (marker read before the approval test): stays minor. The design (lines 354 and 384) prescribes this order and the spec order cannot be implemented for T-11/T-12 (cross-source N-02); only the reason label and one extra call on unapproved candidates differ, inside the 35-call cap.
- M-9 (non-empty operation id outside the pattern becomes `unknown`): stays minor. Fail-closed, owner-listed OQ-47.

## Findings table

Columns: unique id, severity, originating agent(s) and their local ids, source lines (D = `docs/designs/issue-watcher.md`, S = `spec-final.md`), implementation location, short statement.

### Blocking

| id | severity | agents (local ids) | source lines | implementation location | finding |
|---|---|---|---|---|---|
| M-1 | BLOCKING | spec-fidelity (M2-1, blocking); design-fidelity (D-M4, graded minor there) | S 100; D 715 | `cycle.py:751-756` (`_login_step`), `cycle.py:1154` (`_conclude`), `audit.py:164-165`, `tests/issue_watch/test_cycle.py:1710` | The cycle line records `clock_skew_s` only when the offset exceeds 60 s; the spec says the cycle line records the offset every cycle and the design marks it "yes". The test at line 1710 asserts the omission. Not covered by any decision. |

### Minor, from the design-fidelity and spec-fidelity lenses

| id | severity | agents (local ids) | source lines | implementation location | finding |
|---|---|---|---|---|---|
| M-2 | minor | design-fidelity (D-M1) | D 344 | `cycle.validate_setup` 352-358; `test_validate_setup_checks_the_worktree_before_the_approvers__fr027` | Worktree is validated before the approvers file; the design order is approvers first. Both exit 2; only the reason name differs when both are invalid. Not in the register. |
| M-3 | minor | design-fidelity (D-M2); cross-source (C-38, covered by OQ-41a) | D 614, 647, 277-279 | `cycle._launch` 1017-1022; `launch.find_orca` 163-188 (line 184) | Probe cache moved from the `OrcaLauncher` instance to the cycle (OQ-41a, covered). Undeclared addition: `find_orca` skips a non-absolute `which` result, so a relative PATH entry ends as `orca_not_found`. Spec-fidelity also noted the absolute-path guard and stricter `topics` shape under FR-013 (coverage note, behaviour-neutral for a real Orca). |
| M-4 | minor | design-fidelity (D-M3); cross-source (N-01, NEW residual of X-1) | D 166, 386; S 163-164, 197 | `cycle._candidates` 814-815, `_fail` 999-1005; `test_cycle.py:844-849` | After any launch-step outcome the cycle halts (S1, Q1), so "7 with 5" and "7 with 3" and the FR-028 GWT "a `failed` entry written earlier stands" are unreachable as worded; they exist only as `resolve_exit` tests. Owner to confirm a pre-pending `failed` entry ends the cycle. |
| M-5 | minor | design-fidelity (D-M5) | D 239 | `record.py:23-29`; `test_module_boundaries.py:57-61` and docstring 20-22 | `record` imports four helper functions and one type from `predicates`, not "types only"; the boundary test no longer enforces the qualifier. Forced (no design type exists, D 220); not in the register. Recorded earlier as Gate B B-24 and partly OQ-46. |
| M-6 | minor | design-fidelity (D-M6) | D 584, 588; S 337, 379 | `cycle._val` 817-827, `cycle._rv` 946-958, `github._failed` 580-581 | A 401 on a per-issue events read or the re-read is a skip (`events_unreadable` / `revalidation_failed`), not exit 3 `gh_auth_failed`. Follows the spec; design row ambiguous. Fail-closed. A token revoked after G1 yields an exit-0 `cycle_complete`. No cycle-level test for a per-issue 401. |
| M-7 | minor | design-fidelity (D-M7) | D 716; S 272, 357 | `cycle._issue_line` 627-642; runbook section 10.2 | The `note: re-approved` branch is unreachable: stored approval fields are null for every entry that gets a newly computed approval. Owner-accepted as OQ-49 (no emission); OQ-49 text is now stale because the branch exists. |
| M-8 | minor | design-fidelity (D-M8) | D 906-933 | `phase-outputs/reports/ac-trace.md` lines 5 and 7; `final-change-set.md` section 2 | Reports say 2628 passed and 844 tests; the post-fix `p9-g1-summary.md` says 2635 passed. Wording only. |
| M-9 | minor | spec-fidelity (M2-2); cross-source (C-41, covered by OQ-47) | S 157, 289; D 633, 689 | `launch.py:36` and `:332` (`outcome_of`); `predicates.py:57` | An exit-0 reply with a non-empty id outside `^[A-Za-z0-9._:-]{1,128}$` is stored null and recorded `unknown` (exit 7) instead of `launched`. Fail-closed, at-most-once holds. To be confirmed against a captured id in FU-1. |
| M-10 | minor | spec-fidelity (M2-3); cross-source (N-02, NEW) | S 102-105; D 322, 354, 384, 545-548 | `cycle.py:922-928` (`_examine`) | Comments (G4) are read before events (G3) and before the approval test, so a candidate that is both unapproved and unreadable is skipped `marker_unreadable` rather than `not_approved`, and one extra call is spent per unapproved issue. The design contradicts itself on read order; the spec order is the contract if reads are reordered later. |
| M-11 | minor | spec-fidelity (M2-4) | S 82, 102-105 | `predicates.py` (no `is_tagged` / `is_open`); `cycle.py:896-942` | "Tagged" and "open" rely on server-side filters; a case-variant label reaches `_examine` and fails closed as `events_incomplete`. `_revalidate` does test the exact trigger name. |
| M-12 | minor | spec-fidelity (M2-5) | S 231, 269 | `audit.py:396` (`stderr_fallback`); `runner.py:89,110,120,129` | Wall-clock and monotonic reads outside the `Clock` Protocol; stamps only, none feeds a decision. |
| M-13 | minor | spec-fidelity (M2-6) | S 227 (NFR-012) | `ac-trace.md` NFR-012 row | Proved only by the one-off gate G-10 (`git diff --exit-code pyproject.toml Makefile`); no durable test. Stated openly in the register. |
| M-14 | minor | spec-fidelity (M2-7) | S 361 | `tests/issue_watch/test_marker_contract.py:22-39` | The contract test also reads `~/.claude/skills/sc-issue-protocol/...` when present, so the result depends on the host's installed copy. The two `src/` copies are checked unconditionally. |
| M-15 | minor | spec-fidelity (M2-8) | S 330-358, 336 | `audit.py:261-285` (`line()`) | The schema checks reason membership only; a cycle-kind reason is accepted on a decision line and a skip reason on a cycle line. |
| M-16 | minor | spec-fidelity (M2-9) | S 185 (FR-020 GWT) | `cycle.py:758-773` (`_sweep`) plus `_candidates`; `test_cycle.py:2567-2570` | A swept issue that is also discovered gets two decision lines in one cycle. Read as consistent with the spec; flagged because the GWT wording is literal. |

### Minor, NEW contradictions between the design and the spec (no decision of their own; cross-source lens, no implementation read)

| id | severity | agents (local ids) | source lines | implementation location | finding |
|---|---|---|---|---|---|
| M-17 | minor | cross-source (N-03) | D 462, 502, T-10; S 100, 143, 294 | n/a (not read by the lens) | GWT and transition row say a marker "older/newer than T"; Section 3 allows a 300 s tolerance. A test for "older than T" must use more than 300 s. |
| M-18 | minor | cross-source (N-04) | D 546-548; S 122, 207 | n/a | FR-003 GWT read literally forbids argv that NFR-002 requires (marker and edit-time reads); a scan must target requested text fields, not the word `comments`. |
| M-19 | minor | cross-source (N-05) | D 22, 369; S 98, 121, 139 | n/a | `unassigned` / `assigned_other` "arise only in unit tests and the re-read" versus discovery dropping non-owned issues; the design follows FR-003 / FR-008. |
| M-20 | minor | cross-source (N-06) | D 369-372, 354; S 103 | n/a | The design flow table drops `already_dispatched` before the marker read, while D 354 and S 103 read the marker for such entries. |
| M-21 | minor | cross-source (N-07) | D 640, 647; S 199 | n/a | D 640 says every runner call is shortened to the remaining time; D 647 and FR-029 say a started launch is never cut short. Wording. |
| M-22 | minor | cross-source (N-08) | D 823; S 184 | n/a | Two retention figures (about 60 days of cycle lines per file versus about 40 days for 25 MiB). Rationale text only. |
| M-23 | minor | cross-source (N-09) | D 855, 862, 58, 133; S 402, 409 | n/a | Follow-up items FU-3 and FU-10 differ in content and timing between design and spec. Follow-ups are not built. |
| M-24 | minor | cross-source (N-10) | D 129, 139; S 193 | n/a (runbook `docs/designs/issue-watcher-setup.md` should show `schema_version: 1`) | The design adds required config validation (`schema_version`, unknown keys, distinct labels, 50-character limit) not in the FR-027 field list. |
| M-25 | minor | cross-source (N-11) | D 110, 117; S 190, 312, 324 | n/a | The design adds `--config` to every verb and uses exit 6 for "store already exists"; the spec is silent. |
| M-26 | minor | cross-source (N-12) | D 350; S 293, 294, 514 | n/a | The sweep moves `launched` past its lease to `abandoned` without a read; the later marker read moves it to `claimed` (A-009). Wording. |
| M-27 | minor | cross-source (N-13) | D 84, 564; S 92, 470 | n/a | Citation ranges for `poll-augment-review.sh` differ by two lines. |

### Minor notes: contradictions already covered by a decision (never blocking)

| id | severity | agents (local ids) | source lines | covered by | contradiction |
|---|---|---|---|---|---|
| M-28 | minor | cross-source (C-01) | D 177, 759; S 190 | DF-06 | "6 verbs" versus five command names. |
| M-29 | minor | cross-source (C-02) | D 218, 264-265; S 309 | DF-01 | Free function `run_command` versus `Runner` Protocol; no `cwd` in the design. |
| M-30 | minor | cross-source (C-03) | D 222, 604; S 154, 309 | DF-54 | `find_orca(runner)` versus `find_orca(runner, which)`. |
| M-31 | minor | cross-source (C-04) | D 100, 613; S 154 | DF-36 | Non-dict topic rejected where the original `_find_orca` raises. |
| M-32 | minor | cross-source (C-05) | D 101, 741; S 160-161 | Q2 / X2 (DF-50) | Retry text: short form versus full original argv plus flag. |
| M-33 | minor | cross-source (C-06) | D 104, 388; S 163-164 | Q1 / X1 (DF-50) | S1 stop rule versus "examines k and launches 1". |
| M-34 | minor | cross-source (C-07) | D 103, 602; S 196-197 | Q3 / X3 (DF-50), DF-51 | `Retry-After` honoured versus the 3600 s clamp on per-issue limits. |
| M-35 | minor | cross-source (C-08) | D 410, 360; S 267 | X4 (DF-50) | Design adds store key `last_completed_cycle_at`. |
| M-36 | minor | cross-source (C-09) | D 115, 121; S 187, 315-326 | X5 (DF-50) | `status` exit 1 exists only in the design. |
| M-37 | minor | cross-source (C-10) | D 30, 766; S 32, 384 | DF-60 | Runbook inside the design doc versus a separate setup file. |
| M-38 | minor | cross-source (C-11) | D 570-572, 118-119, 449, 718; S 136, 330-358 | DF-02, DF-03, DF-22, DF-57 | Reasons the closed table lacks (marker/edits unreadable, reset lines, dry-run shadow reset). |
| M-39 | minor | cross-source (C-12) | D 118; S 190, 297 | DF-04 | `reset N` with no entry. |
| M-40 | minor | cross-source (C-13) | D 399; S 330-358 | DF-57 | "Every exit of `once` and `reset`" audited. |
| M-41 | minor | cross-source (C-14) | D 892; S 219 | DF-55 | AC-19 sleeping stub versus the 20 s timeout. |
| M-42 | minor | cross-source (C-15) | D 896, 798; S 366 | DF-05 | Gate `make test` versus the affected subset locally. |
| M-43 | minor | cross-source (C-16) | D 800 | DF-09 | `uv run ruff format --check` versus pinned `uvx --offline ruff@0.15.20`. |
| M-44 | minor | cross-source (C-17) | D 765, 780; S 361 | DF-10 | Committed stubs versus stubs written at test time. |
| M-45 | minor | cross-source (C-18) | D 93, 693; S 213 | DF-12 | `property_based` marker on a seeded-loop test. |
| M-46 | minor | cross-source (C-19) | D 441, 362; S 181 | DF-17 | Migrated store saved first versus dry-run never writing `dispatch.json`. |
| M-47 | minor | cross-source (C-20) | D 572 | DF-18 | "Item missing a field" versus `--jq` always emitting every key. |
| M-48 | minor | cross-source (C-21) | D 131-132; S 82 | DF-20 | Label comma rule versus `gh issue list --label` splitting on comma. |
| M-49 | minor | cross-source (C-22) | D 110, 137; S 193 | DF-13 | Default config path contains `~`. |
| M-50 | minor | cross-source (C-23) | D 296, 779; S 213 | DF-15 | "k-th write" versus `crash_at="C1".."C5"`; five reruns. |
| M-51 | minor | cross-source (C-24) | D 297-298, 777-778 | DF-24 | `RecordingLauncher` / `FakeClock(start, step)` versus `FakeLauncher` / `FakeClock(now, mono)`. |
| M-52 | minor | cross-source (C-25) | D 224, 745 | DF-25 | `slo_numbers(lines, store, now)` versus a `StoreDoc` argument. |
| M-53 | minor | cross-source (C-26) | D 221, 350, 492, 737 | DF-44 | `sweep` / `day_cap_count` take a `StoreDoc`. |
| M-54 | minor | cross-source (C-27) | D 95, 761 | DF-27 | False premise of a test-name collision with `tests/cli_portify/test_cli.py`. |
| M-55 | minor | cross-source (C-28) | D 102, 554 | DF-28 | "Every G2 to G7 argv has `--method GET`" versus the precise rule. |
| M-56 | minor | cross-source (C-29) | D 244, 173, 760; S 309 | DF-29 | Lazy versus eager registration. |
| M-57 | minor | cross-source (C-30) | D 437, 237-239 | DF-42 | `record` validating `last_reason` membership without importing `audit`. |
| M-58 | minor | cross-source (C-31) | D 476-492; S 285-288 | DF-43 | No T-row for `failed` to `failed`. |
| M-59 | minor | cross-source (C-32) | D 295, 776 | DF-48 | `FakeRunner` script value type. |
| M-60 | minor | cross-source (C-33) | D 774-790; S 213 | DF-47 | The design test list has no account-rename test (NFR-005). |
| M-61 | minor | cross-source (C-34) | D 220, 545; S 142 | DF-21 | Marker literal appears twice (`CLAIM_MARKER`, `MARKER_JQ`). |
| M-62 | minor | cross-source (C-35) | D 791; S 142 | DF-46 | Dual-surface read of `claim.md` not available in CI. |
| M-63 | minor | cross-source (C-36) | D 709; S 184, 330-358 | Deviation register Table 2 item 1 | No spec reason for a normal exit-0 cycle or a crash line (`cycle_complete`, `cycle_crashed`; table now 59 names). |
| M-64 | minor | cross-source (C-37) | D 354; S 103, 296 | OQ-36 | A `failed` entry in backoff gets only the marker read versus T-12 needing the approval time. |
| M-65 | minor | cross-source (C-39) | D 362, 701-716; S 181-182 | OQ-39 | Dry-run would-launch line has no reason and no key in the closed schema. |
| M-66 | minor | cross-source (C-40) | D 633, 634; S 157-158 | OQ-40 | Overlapping outcome rows: exit 0 plus an operation id versus `agent_session_operation_unknown`. |

## Coverage check of the deduplication

- Every raw finding is present exactly once: D-M1 to D-M8 in M-2, M-3, M-4, M-5, M-6, M-7, M-8 and M-1 (D-M4); M2-1 to M2-9 in M-1, M-9 to M-16; N-01 to N-13 in M-4, M-10, M-17 to M-27; C-01 to C-41 in M-28 to M-66 except C-38 (in M-3) and C-41 (in M-9).
- No contradiction classified as covered by a decision is listed as blocking.
- No finding asks to undo one of the 29 authorized departures.

## Minor notes carried forward (never rechecked)

All of M-2 to M-66 are minor notes carried forward unchanged into cycle 2 and are not rechecked by the verification agents. The ones worth an owner decision after the task (optional, none blocks the gate):
- M-6: decide whether a per-issue 401 should end the cycle as `gh_auth_failed` (a small rule in `cycle._val` and `_rv` plus one test).
- M-7: either make the `re-approved` note reachable or delete the dead branch and the runbook sentence; refresh OQ-49.
- M-4: confirm that a pre-pending `failed` entry ends the cycle (else Q1 must be amended).
- M-9: confirm the operation-id pattern against a captured id in FU-1, or suppress the retry line for such an id instead of using `unknown`.
- M-24: show `schema_version: 1` in the config example of `docs/designs/issue-watcher-setup.md`.
- M-5: amend the design cell to "pure helpers and types".
- M-8: update the stale counts when the change-set record is next touched.
- M-10: if the per-issue reads are ever reordered, the spec order (approval events, marker, edit timestamps, Project items) is the contract.
