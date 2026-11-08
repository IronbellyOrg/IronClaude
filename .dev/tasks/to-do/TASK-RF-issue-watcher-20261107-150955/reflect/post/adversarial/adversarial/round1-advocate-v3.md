| Status | Result |
|---|---|
| DONE | Read the three variant reports, the diff analysis, the code (`cycle.py`, `launch.py`, `runner.py`, `record.py`, `audit.py`, `cli.py`, `predicates.py`), the design, the spec, the runbook and the task file, all read-only. |
| DONE | Decided the late-launch point and the two launch-outcome points (C-024, C-026), answered A-001 to A-010, and filled the point table. |
| NEXT | Round 2 rebuttal, if the orchestrator runs one. I wrote no files and ran no tests. |

## Position summary

Variant 3 is the most accurately calibrated variant on classification. It records negative evidence for every area it checked, its line numbers hold up, and it gets the shell-safety question and the forced-copy question right.

It has one real hole. It said nothing about the launch that can start after the 120-second cut-off. I concede that point and rate it Regression LOW, not V2's HIGH. I also accept V1's two launch-outcome gaps (C-024 and C-026) as real.

## Steelman of Variant 1

- V1 covers the widest correctness slice and finds the most advisory gaps.
- Several of those gaps are real and I verified them:
  - C-024: `launch.py:277-288` and `:311-334` accept `error.operation_id` on exit 0.
  - C-026: the stderr cap at `runner.py:15` and `:126` runs before the marker search at `launch.py:322`.
  - C-018: `cycle.py:685-690` catches only `_Stop`.
  - C-022: `predicates.py:199-209` turns a same-second approval/trigger tie into a permanent events_incomplete.
- V1 is also right that the at-most-once ordering holds. `cycle.py:1060-1062` saves before it launches.

## Steelman of Variant 2

- V2 is the only variant that read the tests and the task file directly.
- It found the only real breach of the 120-second rule (FR-029, spec `:199`; design `:647`): the last check is at `cycle.py:1048`, before the save at `:1061` and the launch at `:1062`.
- It found the plain breach of the no-skip rule (task file `:188` against `test_cli.py:967` and `:1070`, `test_record.py:739`, `test_cycle.py:735` and `:4694`).
- It gave a clear verdict, and its calibrator confirmed 21 of 22 citations exact.

## Strengths claimed (Variant 3)

1. **Correct DISABLED line numbers.** The kill-switch file is checked at `cycle.py:693` and again at `:1033` (`_Stop("disabled_mid_cycle")`). The only remaining window is between `:1033` and `:1061`, and the design accepts it (X-009, not a defect). V1 misplaces these checks at `:335-337` and `:308`.
2. **Shell safety right (X-008).**
   - `retry_argv` (`launch.py:119-132`) checks the id against `^[A-Za-z0-9._:-]{1,128}$` (`launch.py:36`) and prints it with `shlex.join` (design `:741`), so the printed retry command is shell-safe.
   - What remains is a possible option confusion, for example an id starting with `-`. It is unverified and LOW.
3. **Forced copy correctly called Necessary (X-004).**
   - Design `:237` and `:240` keep `audit` and `launch` apart from the modules they would otherwise import. That forces the duplicated constants.
   - Example: `audit.py:200-206`, `_MAX_ISSUE = 999_999_999` copies `launch.py:30`.
   - V3's advice not to consolidate `_fsync_dir` is right.
4. **C-017 is real.**
   - `disabled()` uses lexists, while `disabled_since()` uses `os.stat` and catches only FileNotFoundError (`record.py:421-431`).
   - So a dangling or looping symlink (ELOOP) counts as present for the cycle, but `status` (`cli.py:164-177`, which catches only StoreError) crashes or misreports.
   - This contradicts the runbook's "a dangling symlink ... counts as present" and "status shows ... disabled since" (around `issue-watcher-setup.md:296-300`).
5. **C-034 parts (a) and (b).**
   - (a) The runbook says `check-config` and `init-state` exit 2 on any other platform (`issue-watcher-setup.md:53`). The code also puts `reset` behind the platform check (`cli.py:84-91`, `:314`).
   - (b) Design `:121` asks for a usage error when `reset` is given both flags or neither. The code gives one "not both" message for both cases (`cli.py:309-320`).
6. **C-037.** `stderr_fallback` (`audit.py:381-404`) reads the wall clock when no timestamp is given, checks only that the reason exists, and always writes `"kind": "cycle"`. That is a real, small gap.
7. **The parity-test gap.** No test checks the copied constants against their originals. That is the right follow-up for X-004.

## Weaknesses identified in the others

1. **V1 header miscount.** It says "1 MEDIUM, 11 LOW", but rows 1 and 2 are both MEDIUM.
2. **V1 wrong lines.** `cycle.py:335-337` and `:308` are not the DISABLED checks; those are `:693` and `:1033`.
3. **V1 reviewed without the authorities.** It did not read the deviation register, the spec or the tests. So it could not tell disclosed changes from silent ones.
4. **V1 missed the late launch.** It called the launch ordering "adherent" after checking only FR-010 (save before launch). It never checked FR-029 (no launch after 120 s).
5. **V2's HIGH severity has no likelihood reasoning.**
   - Network filesystems are rejected for the state folder (`cycle.py:50-52`, used at `:271`), so the save is a local fsync.
   - The worst case of about 241 s still fits inside the 300 s cadence (design `:649`).
   - The lock prevents overlapping cycles.
   - At-most-once is not affected.
6. **V2's implied fix breaks the design.**
   - V2's recommended action (variant-2-original.md:53) asks only that the fix keep durable-before-launch ordering and the budget-exhausted outcome. Its calibrator read that as a re-check after the save.
   - A plain re-check after the save leaves a pending entry with no launch.
   - Design `:647` requires "no entry" in that case, so the fix also needs a rollback (see C-014 below).
7. **V2's slice is narrow.** It audited 13 units and had nothing on the launch-outcome mapping, the stderr fallback or the kill-switch file.

## Concessions

1. **The late launch.** V3 said nothing about C-014/X-007. V2 found a real FR-029 breach that V3 missed.
2. **X-005 is Authorized, not Necessary.** Task Step 2.1 explicitly authorizes `duration_s` through `time.monotonic()`, "never used for a decision".
3. **C-034(c) needs revising.** V3 missed that design `:115` (status exits 0, 1, 2, 6) and design `:726` (status exits 0, 1, 6) disagree. The runbook (`issue-watcher-setup.md:432`) follows `:726`. That is a conflict inside the design, not plain drift.
4. **Row 11 path is wrong.** The registration is in `src/superclaude/cli/main.py:563-565`.
5. **C-036 is only LOW.** `mark_pending` requires an absolute `launch_cwd` (`record.py:548-549`, validated at `:184`), and the store validates the id, so the gap is close to unreachable.
6. **Rows 8 and 10 are near-aligned.**
7. **Some citations predate a context reset.** My `runner.py` and `main.py` line citations come from reads made before my context was compacted.

## Late-launch decision (C-014 / X-007)

**Verdict: Regression LOW, non-blocking.**
- **Why it is a Regression.** FR-029 (spec `:199`) and design `:647` say no launch starts after 120 s. `cycle.py` checks the cut-off at `:1039` and again at `:1048`, after the git call. Then come `mark_pending` (`:1060`), the fsync'd save (`:1061`) and the launch (`:1062`), with no check in between.
- **The authors saw the pattern.** Gate C cycle 2 added the re-check at `:1046-1048` for the git call, but not for the save.
- **Why the severity is LOW.** The save is local, there is a 60 s margin in the cadence, the lock prevents overlap, and at-most-once holds.

**Fix compatible with "durable record before the spawn":**
1. Keep `prev = self.doc` before `mark_pending`.
2. After `_save()`, test `if not self.deadline.launch_allowed():`.
3. On that branch, call `self._set(prev)` and `self._save()`, then `raise _Skip("budget_exhausted")`.

What this gives:
- No spawn ever happens without a durable pending entry.
- Restoring `prev` also restores the launch count, `consumed_at` and `consumed_log`, so the step ends with no entry, as design `:647` requires.
- If the process crashes, or the rollback save fails (`_save` maps OSError to `_Stop("state_dir_unwritable")`, `cycle.py:582-587`), a pending entry remains. The next sweep turns it into `pending_orphan` with no launch, which is the case design `:529` already documents.

Add a test with a clock that moves past 120 s inside `store.save`. It should assert no launcher call, an unchanged entry, and a budget_exhausted decision line.

Rejected alternatives:
- A re-check with no rollback leaves an orphan entry, which contradicts "no entry".
- A fixed safety margin before the save cannot bound how long an fsync takes.

## C-024 and C-026

- **C-024 is real: advisory gap, LOW-MEDIUM.**
  - Take an exit-0 reply whose stdout JSON holds only `error.operation_id`, with no unknown-outcome text. It passes the marker search (`launch.py:322`), the exit-code check and the JSON parse.
  - `_first_hit` checks both paths in `OPERATION_ID_PATHS` (`launch.py:39-45`, marked [PROPOSAL, UNVERIFIED]) and finds the error one. The function then returns `launched`.
  - Effect: an uncertain launch is reported as launched, so exit 7 and the retry hint are lost. At-most-once still holds.
  - No test covers this. The unknown fixture (`orca_launch_unknown.json`) is exit 1, used at `test_launch.py:554` and `:697`.
  - Fix: accept only `receipt.operation_id` for launched, and read `error.operation_id` only on the unknown branch. Add a test.
- **C-026 is real but narrow: advisory gap, LOW.**
  - Runner caps stderr at 500 bytes (`runner.py:15`, applied at `:126`) before `launch.py:322` searches it for the unknown-outcome text.
  - It misreports only when the exit is 0, a valid receipt id exists, and the text sits past byte 500.
  - The cap itself is required by the design (`:218`, `:822`), so the fix belongs in the order of operations: search for the text before capping, or have runner keep a found/not-found flag.

## Shared-assumption responses

| Id | Answer | Reason |
|---|---|---|
| A-001 | QUALIFY | The registers are authoritative only where a reviewer actually read their text. V1 never read them. |
| A-002 | REJECT | A [PROPOSAL] comment discloses a change; it does not authorize it. Example: `cli.py:35`. |
| A-003 | ACCEPT | The tasklist acts as an amending layer. Task `:332` authorizes three predicate functions for `record`. |
| A-004 | REJECT | The citation errors are confirmed: V1's DISABLED lines and V3's `main.py` path. |
| A-005 | ACCEPT | No reviewer ran tests; every finding comes from reading control flow. |
| A-006 | ACCEPT | No disagreement. |
| A-007 | QUALIFY | The Orca reply shape is unverified (design `:629-636`, `launch.py:39-45`). C-024 and C-026 depend on that shape. |
| A-008 | QUALIFY | Design `:115` and `:726` disagree on the status exit codes. |
| A-009 | REJECT | V3's silence on C-014 is not agreement. |
| A-010 | ACCEPT | Context only. |

## POINT TABLE

"Necessary" means a necessary deviation, and "Authorized" means an authorized expansion.

| Point id | Final classification | Backs | Conf. | Evidence |
|---|---|---|---|---|
| X-001 | Drift MEDIUM | V3 | 70% | `cli.py:35`: crash exit 1 is not in the `once` exit list at design `:114`. The design's crash fallback at `:722` softens it. Disclosed at task `:905`. |
| X-002 | Necessary LOW | V3 | 70% | Design `:709` requires a reason on every cycle line, but the exit-0 row at `:157` names none. `audit.py:55-64`. |
| X-003 | Split. Authorized LOW for the three functions; Drift LOW for `valid_operation_id` | V3 | 65% | `record.py:23-29` against design `:239` ("types only"). Task `:332` lists only three functions; PRE-11 (task `:998`). |
| X-004 | Necessary LOW | V3 | 85% | Design `:237` and `:240`; `audit.py:200-206` copies `launch.py:30`. |
| X-005 | Authorized LOW | none (V3 conceded) | 75% | Task Step 2.1 authorizes `time.monotonic()` for `duration_s`; `runner.py:89`. |
| X-006 | Drift MEDIUM, non-blocking | V2 | 75% | Task `:188` bans skips; five skip sites; task `:908` admits it. |
| X-007 | Regression LOW | V2 (category only) | 65% | No cut-off check between `cycle.py:1048` and `:1062`; spec `:199`. |
| X-008 | Advisory gap LOW | V3 | 60% | `launch.py:119-132` and `:36` validate the id and print it with `shlex.join` (design `:741`). |
| X-009 | Not a defect | V3 | 85% | `cycle.py:693` and `:1033`; the remaining window up to `:1061` is accepted by the design. |
| X-010 | Documentation Drift LOW | V1 and V3 | 80% | The task says 57 reason names (`:199`); the runbook says 59 (`issue-watcher-setup.md:344`). |
| C-014 | Regression LOW, fix with snapshot and rollback | V2 (category only) | 65% | `cycle.py:1060-1062`; design `:647` and `:529`. |
| C-013 | Drift MEDIUM, non-blocking (same as X-006) | V2 | 75% | Task `:188`; skips at `test_cycle.py:4694` and `test_cli.py:1070`. |
| C-016 | Advisory gap LOW, conforms to the design | V1 | 70% | `record.py:689-703`: day-cap window `now-24h < t <= now`. |
| C-017 | Advisory gap LOW | V3 | 85% | `record.py:421-431`; `cli.py:164-177`; runbook around `:296-300`. |
| C-018 | Advisory gap LOW, reachable only through a bug | V1 | 70% | `cycle.py:685-690` catches only `_Stop`. |
| C-019 | Advisory gap, unverified | V1 | 55% | `runner.py:91-101`: `capture_output` waits for pipe end-of-file. |
| C-024 | Advisory gap LOW-MEDIUM | V1 | 75% | `launch.py:277-288` and `:311-334`; no exit-0 error-path test. |
| C-026 | Advisory gap LOW | V1 | 70% | `runner.py:126` caps stderr before `launch.py:322` searches it. |
| C-036 | Advisory gap LOW, near-unreachable | V3 (severity reduced) | 70% | `record.py:548-549` and `:184`; `cycle.py:1271-1280`. |
| C-037 | Advisory gap LOW | V3 | 80% | `audit.py:381-404`. |
| C-034 | Drift LOW, part (c) revised | V3 | 75% | (a) runbook `:53` against `cli.py:84-91` and `:314`; (b) design `:121` against `cli.py:309-320`; (c) design `:115` against `:726`, runbook `:432` follows `:726`. |
| C-022 | Advisory gap LOW-MEDIUM, conforms to the spec but has no recovery | V1 | 70% | `predicates.py:199-209`; spec `:92`. |

Not checked: I ran no tests, and I did not reproduce C-019's pipe behaviour. The C-024 and C-026 verdicts depend on the Orca reply shape, which the design itself marks unverified.
