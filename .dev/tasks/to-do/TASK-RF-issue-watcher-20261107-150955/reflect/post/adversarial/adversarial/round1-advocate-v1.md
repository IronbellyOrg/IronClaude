# Round-1 advocate statement, VARIANT 1 (reviewer 1, sonnet, analyzer)

All paths below are under `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher`. I wrote no files. This is a static read only: I ran nothing, so the late-launch window and the pipe-hang point are reasoned from the code, not reproduced.

## 1. Position summary

Variant 1 is the only card that covers behaviour in `cycle.py`, `record.py` and `launch.py` at requirement level. Its main classification (exit 1 and `cycle_crashed` are Necessary) holds against the design text. It was wrong to skip the tests and the decision register, and wrong to say nothing about the late launch and the test skips. The late launch is a real but small gap, not a blocking Regression. The test skips are real Drift against an explicit task ban.

## 2. Steelman of Variant 2

Variant 2 read the tests and the task file itself, with absolute paths and a stated "no commands run" limit. It caught two things Variant 1 missed:

- **Late launch.** There is no deadline check between the pending save (`src/superclaude/cli/issue_watch/cycle.py:1061`) and the spawn (`cycle.py:1062`). The design says an Orca launch is "not started when `elapsed() > 120`" (`docs/designs/issue-watcher.md:647`). That is a correct control-flow reading.
- **Skips.** The task bans `skip`, `skipif` and `xfail` outright (task file line 188). The tests use them at `tests/issue_watch/test_record.py:739`, `test_cli.py:967`, `test_cli.py:1070`, `test_cycle.py:735` and `test_cycle.py:4694`. Its Drift call is correct, and recorded non-root zero-skip runs do not cure an unconditional ban.

Its verdict is explicit and its fix is concrete: add a slow-save test. Its DF-05 and multi-day-test readings are accurate.

## 3. Steelman of Variant 3

Variant 3 read the design and runbook directly and keeps per-area negative evidence, including 13 runbook claims. It found things the others did not:

- **Boundary leak.** `record.py` imports four predicate functions, not the three the task allows. I read `record.py:23-29` and task file line 332: the allowed set is `parse_utc`, `format_utc`, `valid_issue_number`, and `valid_operation_id` is not on it.
- **Private import.** `cycle` reads the private `launch._ORCA_CLIS` (`cycle.py:1227,1230`).
- **Silent retry drop.** The retry list in `status_report` silently drops some `unknown` entries (`cycle.py:1271-1280`).
- **Fallback weaknesses.** `stderr_fallback` does not check the exit and always writes kind `cycle` (`audit.py:381-404`).
- **ELOOP.** The ELOOP traceback on the disabled flag (`record.py:421-431`) is correct.
- **Copy risk.** It correctly notes that copied constants have no parity tests.

Its Drift call on exit 1 is the strongest competing reading, because `docs/designs/issue-watcher.md:114` lists `once` exits as "0, 2, 3, 4, 5, 6, 7, 75" with no 1.

## 4. Strengths claimed for Variant 1

1. **Widest correct coverage.** It alone found four behaviours, all verified:
   - `_locked_body` catches only `_Stop` (`cycle.py:663-690`), so an exception after the spawn skips `_commit`.
   - A same-second approval and unlabel/trigger event stays `events_incomplete` (`predicates.py:205-209`).
   - An exit-0 reply carrying only `error.operation_id` is accepted as launched (`launch.py:326-334`).
   - The day cap ignores times later than `now` (`record.py:689-703`).
2. **FR-010 ordering is right.** Its substance is correct: `mark_pending` (`cycle.py:1060`), then `_save()` marked "FR-010: durable before the launch call" (`cycle.py:1061`), then the spawn (`cycle.py:1062`). Only its line numbers were wrong.
3. **Exit 1 is Necessary, not invented.** Design 10.1 line 722 says the stderr fallback is "used for a crash". But `stderr_fallback` raises on a name not in `REASONS` (`audit.py:381-404`), and the closed table had no crash name. A name was forced by the design's own text. Exit 1 is Python's default for an uncaught exception.
4. **Only card to flag the unamended design.** The spec has 52 reasons, the task file says 57, the code has 59 (`audit.py:26-102`, `final-change-set.md:208`), and the design and spec were not amended. The deviation register lists the 57-versus-59 stale text (`phase-outputs/reports/deviation-register.md:47,61`), so the stale-count point is disclosed. The un-amended design is not.
5. **Dangling DISABLED symlink gap is real.** `disabled()` uses `lexists` (`record.py:421-423`), but `disabled_since()` uses `os.stat` and catches only `FileNotFoundError` (`record.py:425-431`). `status` can then say "disabled since: no" while cycles are disabled.
6. **Honest labels.** It marks inferred items as inferred (pipe hang, stderr cap).

## 5. Weaknesses identified in the other variants

**Variant 2:**
1. **Severity without likelihood.** The late launch is called HIGH and blocking with no likelihood reasoning. The window covers an in-memory `mark_pending` plus a local atomic write, chmod and directory fsync (`record.py:370-378`). Network filesystems are rejected for `state_dir`. The worst case is about 241 s of a 300 s cadence, which design 649 says is acceptable.
2. **Its fix breaks the design.** A bare check after the save leaves a pending entry with no spawn. Design 647 says the step "ends with no entry". Such an entry still counts toward the day cap, because `day_cap_count` counts every state.
3. **Thin coverage.** It has 5 rows, no advisory gaps, and silence on the exit-1 and reason-table topics (C-001 to C-012). The FAIL verdict rests on two items.
4. **Overstated "authorized".** Its boundary row says the tasklist authorizes the imports, but `record.py:23-29` imports more than task line 332 allows.
5. **Unchecked count.** I did not verify its "6 functions, 7 cases" count of skipped tests. A Grep shows five skip lines, and the `NOT_ROOT` marker at `test_cli.py:1070` is applied to more than one test.

**Variant 3:**
1. **Drift on exit 1 ignores design 722.** That line itself calls for a crash fallback.
2. **Wrong path.** It cites `src/superclaude/main.py` where the real file is `src/superclaude/cli/main.py`.
3. **Row 6(c) ignores design line 726.** That line lists `status` exits as 0/1/6, while line 115 lists 2. The design disagrees with itself, so the runbook cannot be Drift against both.
4. **Silent on the late launch and the skips.** Six of its 11 rows are Drift, mostly LOW hygiene items.
5. **Hedged `stderr_fallback` call.** Calling the wall-clock read in `stderr_fallback` Drift is arguable, since the fallback runs where the cycle failed. I could not confirm whether a clock was available at the call site, so I count it LOW either way.

## 6. Concessions

- Variant 1's citations were wrong in places: it cites `cycle.py:335-337` for lines 1060-1062 and `cycle.py:308` for lines 693 and 1033. The header says "1 MEDIUM, 11 LOW" while rows 1 and 2 are both MEDIUM.
- Variant 1 did not read the decision register, the tests or `spec-final.md`. Its Authorized and skip rows were therefore unsupported.
- Its Necessary LOW call on the skips is wrong. The ban is explicit and the tests violate it. This is Drift, MEDIUM.
- Its silence on the late launch is a miss, not an "adherent" finding.
- Variant 3 is right that `record` imports a function the task did not allow (`valid_operation_id`). My own earlier "Authorized" reading did not cover it.
- Variant 1's MEDIUM severity on the exit-1 and reason-table row was too high. LOW is more accurate.

## 7. Shared-assumption responses

| ID | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | The registers are authoritative only if read. Variant 1 did not read them, so its Authorized rows stand only where the register backs them (for example `deviation-register.md` Table 1). |
| A-002 | REJECT | A `[PROPOSAL]` comment is a disclosure, not an authorization. But a disclosed departure with a forcing constraint is Necessary, not Drift. The exit-1 and `cycle_crashed` names are also in the register (Table 2 row 1), the runbook (`docs/designs/issue-watcher-setup.md:344`) and the QA reports. |
| A-003 | ACCEPT | Design and spec text are the baseline, with the task file as the amending layer. |
| A-004 | ACCEPT | The citations are wrong in places (Variant 1 `335-337`, `308`; Variant 3 `main.py` path; Variant 2 one line off). Wrong citations do not change the ordering facts at `cycle.py:1048-1062`. |
| A-005 | ACCEPT | All cards are static reads, mine included. The late-launch window and the pipe hang are unreproduced. |
| A-006 | QUALIFY | The code diff is the scope. The design file is outside the change set (`qa/gate-c/qa-verification-structural-report.md:34,50-51`), so the "never amended" finding is about absence, not a diff line. |
| A-007 | ACCEPT | `OPERATION_ID_PATHS` is `[PROPOSAL, UNVERIFIED]` (`launch.py:39-45`). Any gap that depends on the Orca reply shape (C-024, C-026) stays at most LOW. |
| A-008 | QUALIFY | Precedence is unstated. Where the design contradicts itself (lines 114/722, 115/726), the more specific mechanism text wins. Record a documentation defect, not code Drift. |
| A-009 | ACCEPT | The slices barely overlap, so silence is not agreement. Only Variant 1 covered `cycle.py` at requirement level. |
| A-010 | ACCEPT | Context only. The calibrator's note on Variant 2's HIGH also applies. |

## 7a. Late-launch decision (C-014 / X-007)

**Verdict: a real, small gap. Record it as an advisory gap and documented residual limit, LOW.**

- **Where it sits.** The cutoff is checked at `cycle.py:1048` (N-1, after the origin call). `mark_pending` runs at 1060, `_save()` at 1061, and the spawn at 1062. Nothing re-checks between 1048 and 1062. It is a check-then-act window, and the only slow step in it is the local fsync'd save.
- **Not a Regression/HIGH.** The worst case is about 241 s of a 300 s cadence, and every check has the same window. No test pins it, which is the real defect.
- **Not Drift.** The N-1 re-check was added on purpose and disclosed (`deviation-register.md:50`).
- **If the panel forces a four-category label,** use Regression LOW (it contradicts design 647 in the edge case). Never HIGH.
- **Fix compatible with "durable record before the spawn":**
  1. Document the limit in design 8.5, and add a slow-save test (a fake store whose save advances `FakeClock` past 120 s) that pins the chosen behaviour. This needs no code change.
  2. Optional, needs an owner decision: after the save, re-check, and if past the cutoff restore the pre-pending document, save again, and raise `_Skip("budget_exhausted")`. This keeps "no entry". If the second save crashes, the leftover pending entry is swept and never launched (`deviation-register.md` row DF-15, crash point C3), so at-most-once holds.
  3. A bare post-save skip is not acceptable. It leaves a pending entry with no spawn that counts against the day cap and contradicts design 647.

## 8. POINT TABLE

| Point | Final classification | Backs | Conf. | Evidence |
|---|---|---|---|---|
| X-001 | Necessary deviation, LOW (behaviour); the un-amended design is a separate Drift, LOW (documentation) | V1 on category, V3 on the doc gap | 65% | `cli.py:35` `_EXIT_CRASH = 1 # [PROPOSAL]`; `docs/designs/issue-watcher.md:114` (no exit 1) vs `:722` (fallback "used for a crash"); `audit.py:381-404` raises on a name not in the table |
| X-002 | Necessary deviation, LOW | V3 | 70% | `cycle.py:1137` returns `cycle_complete`; design 10.1 wants a reason on every cycle line |
| X-003 | Split: `format_utc`, `parse_utc`, `valid_issue_number` Authorized LOW; `ApprovalResult` (a type) allowed by design 239; `valid_operation_id` Necessary LOW with weak disclosure | none (split) | 60% | `record.py:23-29` vs task file line 332 allowed list |
| X-004 | Necessary deviation, LOW; add a parity test as an advisory gap | V3 | 65% | `audit.py:203` same-bound comment; `launch.py:30` |
| X-005 | Necessary deviation, LOW | V3 | 70% | `runner.py:89` `time.monotonic()` times a real child process |
| X-006 | Drift, MEDIUM (explicit ban violated; fix is easy) | V2 | 75% | task file line 188; `test_cli.py:1070`, `test_cycle.py:4694`, and 3 other skip lines |
| X-007 | Advisory gap / documented residual limit, LOW (Regression LOW if a category is forced) | none (V1 missed it, V2 overrated it) | 70% | `cycle.py:1048,1061,1062`; design `:647,649` |
| X-008 | Advisory gap, LOW (pattern allows a leading `-`; the id is validated first) | none (both partly right) | 55% | `predicates.py:57`; `launch.py:127-130` |
| X-009 | Advisory gap, LOW (the kill switch is re-checked before the origin call, not before `mark_pending`) | none (V1's line is wrong, its substance is partly right) | 60% | `cycle.py:693,1033,1060` |
| X-010 | Not a defect: both counts are consistent (52 spec + 5 DF = 57, + 2 proposals = 59); stale text is disclosed | none | 80% | `deviation-register.md:47,61`; `audit.py:26-102` |
| C-014 | Advisory gap / documented residual limit, LOW | none | 70% | as X-007 |
| C-013 | Drift, MEDIUM | V2 | 75% | as X-006 |
| C-016 | Advisory gap, LOW | V1 | 55% | `record.py:689-703` (later times not counted; a `clock_skew` warning exists past 60 s) |
| C-017 | Advisory gap, LOW | V1 and V3 | 85% | `record.py:421-431` (`lexists` vs `os.stat` catching only `FileNotFoundError`) |
| C-018 | Advisory gap, LOW (id and retry hint lost; at-most-once preserved by the sweep) | V1 | 55% | `cycle.py:663-690` |
| C-019 | Advisory gap, LOW (inferred; `subprocess.run` can wait on a grandchild holding the pipe) | V1 | 50% | `runner.py:91-101` |
| C-022 | Advisory gap, LOW (fail-closed: never launches until re-labelled) | V1 | 70% | `predicates.py:205-209` |
| C-024 | Advisory gap, LOW (reply shape unverified) | V1 | 60% | `launch.py:326-334` |
| C-026 | Advisory gap, LOW (narrow: only an exit-0 reply with the marker beyond 500 bytes of stderr; any non-zero exit is `unknown` anyway) | V1, narrower than claimed | 65% | `runner.py:63` keeps the first 500 bytes; `launch.py:322,324-325` |
| C-036 | Advisory gap, LOW (defensive; stored ids are already validated) | V3 | 60% | `cycle.py:1271-1280`; `record.py` validates with `valid_operation_id` |
| C-037 | Advisory gap, LOW | V3 | 60% | `audit.py:393-402` |
| C-034 | Not a defect for (c); (a) and (b) unverified | none | 50% | design `:115` vs `:726` disagree |
| C-022 | (see the C-022 row above) | V1 | 70% | `predicates.py:205-209` |

## DONE / NEXT

| Status | Result |
|---|---|
| DONE | Read `cycle.py`, `record.py`, `launch.py`, `runner.py`, `audit.py`, `predicates.py`, the design and the register; checked skips, imports and the stderr cap again. |
| NEXT | Lead scores the point table. If late launch stays open, ask the owner whether to take fix 1 (document and test) or fix 2 (roll back after the save). |
