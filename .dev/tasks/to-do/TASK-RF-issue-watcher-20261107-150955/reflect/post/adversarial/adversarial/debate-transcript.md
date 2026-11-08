# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 invariant probe
- Convergence achieved: 83.6% (56 of 67 points, computed by the judge in scoring-matrix.md)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (variant 1 sonnet/analyzer, variant 2 haiku/qa, variant 3 opus/refactorer)
- Judge: opus (judge_class_collision: true, disclosed in base-selection.md)
- Mode: A (compare); variants are the three blind-calibrated reviewer cards (C = 0.70, 0.82, 0.76)

## Round 1: Advocate Statements

### Variant 1 Advocate

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

### Variant 2 Advocate

| Status | Result |
|---|---|
| DONE | Independently reviewed the disputed source paths and task authority. Variant 2’s late-launch finding stands, with severity reduced to MEDIUM. |
| NEXT | Correct the deadline path without removing durable-before-launch protection, then verify the slow-save case and the prohibited test skips. |

## Position summary

**Verdict: FAIL.** Variant 2 identifies a real violation of the acceptance requirement that no launch starts after 120 seconds, but HIGH severity is unsupported by the available evidence. Its no-skip finding also stands; its blanket authorization of predicate-helper imports does not.

The classifications below apply the supplied precedence: **Regression > Drift > Necessary deviation > Authorized expansion**. A useful implementation choice does not override an explicit, unamended requirement.

## Steelman of Variant 1

Variant 1 correctly separates at-most-once protection from recovery quality and identifies valuable concerns involving clock rollback, lost launch receipts, event-history ties, and truncated stderr. Its strongest structural observation is that validating operation ids is necessary, although that does not establish that importing a fourth predicate helper was the only permitted solution.

Its confirmation that persistence precedes launch is correct. That ordering proves one safety property, not compliance with the separate launch deadline.

## Steelman of Variant 3

Variant 3 gives the strongest explanation of why some duplication follows the required module boundaries. In particular, consolidating helpers across isolated modules would itself require changing those boundaries.

It also identifies concrete operator-facing gaps: inconsistent kill-switch status and silent omission of some schema-valid unknown entries from the retry list. Its distinction between documented proposals and authorized changes is useful, although it overlooks explicit task instructions for runner timing and reset/status exit codes.

## Strengths claimed

1. **The late-launch counterexample is direct control flow, not speculation about Orca.** The last check permits launch at 119 seconds; persistence can finish at 121 seconds; the next statement invokes the launcher with its full timeout. The deadline helper permits launch only through 120 seconds, while the acceptance criterion expressly forbids later starts. See [cycle.py:410][deadline-helper], [cycle.py:1048][launch-path], and [issue-watcher.md:892][acceptance].

2. **The no-skip finding rests on an explicit instruction and an actual prohibited construct.** The task prohibits skip expressions unconditionally, while the test suite contains a root-dependent `skipif`. A successful non-root run does not remove that contradiction. See [task:188][task-tests] and [test_cli.py:1070][skip].

3. **Variant 2 correctly distinguishes authorized verification scope from a full-suite pass.** The decision register expressly replaces the local full-suite gate with named affected subsets and leaves the full suite to CI. That is authorization for the narrower local gate, not evidence that every repository test passed. See [06-gap-fill-decisions.md:28][local-gate].

### Deadline correction that preserves durable-before-spawn ordering

Keep the pending-state save **before** every launcher invocation. Preserve the immediately preceding document, recheck the deadline after that save, and invoke the launcher only if the cutoff still permits it.

If persistence crosses the cutoff before any spawn, durably restore the pre-pending document under the existing lock. This must remove the new reservation or restore the previous failed entry, avoid consuming the daily allowance, and retain the existing unstamped `budget_exhausted` outcome. If restoration fails, stop without launching and report persistence failure; do not claim that rollback succeeded.

A bare post-save check is insufficient: it leaves a pending reservation that the next sweep abandons as an orphan. Moving the save after the spawn would instead break the at-most-once protection. See [record.py:538][pending] and [record.py:627][sweep].

Add an injected-clock case where pending persistence crosses 120 seconds. It must assert no launcher invocation, restored prior state, no new consumed reservation, and the required budget-exhausted decision. This is a proposed correction, not an implemented or executed test.

## Weaknesses identified in the others

1. **Variant 1’s deadline conclusion checks the wrong property.** Save-before-spawn ordering and no-late-launch behavior must both hold. Its “checked once” account of the kill switch is also incorrect: the source contains a second check immediately before the origin/deadline portion of the launch step. See [cycle.py:1033][launch-path].

2. **Neither alternative classification of runner timing survives the task text.** The task expressly orders `time.monotonic()` around the child and says that duration is never used for a decision. This is Authorized expansion, not Drift or merely Necessary deviation. See [task:193][task-tests].

3. **Variant 3 overstates the reset/status production deviations.** The task expressly requires configuration-invalid status exit 2 and platform/configuration reset exit 2. The remaining problem is incomplete documentation, not unauthorized command behavior. See [task:498][task-cli] and [task:501][task-cli].

4. **Both broader cards require qualifications on external-process claims.** The code explicitly marks Orca reply paths UNVERIFIED. Captured-pipe inheritance and leading-dash argument handling are risks to investigate, not demonstrated failures of the actual Orca executable. See [launch.py:39][orca-shapes] and [runner.py:91][runner].

## Concessions

- **Reduce late-launch severity from HIGH to MEDIUM, retaining blocking status.** The acceptance violation is established, but neither its frequency nor a HIGH-impact consequence was demonstrated. Approval checks and durable at-most-once protection remain intact.
- **Correct Variant 2’s import finding.** Three predicate functions are expressly permitted; `valid_operation_id` is a fourth function. Blanket authorization of every predicate name is broader than the task permits. See [task:332][task-record] and [record.py:23][record-imports].
- **Correct the no-skip category under the supplied precedence.** Variant 2 called it Drift. Because the implementation directly contradicts an explicit verification requirement, my final classification is Regression, MEDIUM.
- **Do not present reviewed assertions or recorded gate results as fresh test execution.** No tests or shell commands were run in this review, and no files were changed.

## Shared-assumption responses

| Assumption | Response |
|---|---|
| A-001, decision-register authority | **Qualified acceptance.** Explicit task instructions and registered owner decisions authorize their stated departures. Mere disclosure of an executor choice does not authorize it. |
| A-002, proposal comments as authority | **Reject.** A proposal comment alone proves neither authorization nor necessity. |
| A-003, task as an amending layer | **Accept.** Apply explicit amendments narrowly, then assess remaining contradictions against the unchanged requirements. |
| A-004, reliable card citations | **Reject.** The supplied cards contain stale lines, a wrong source path, and a line-offset error. Conclusions require independent source reads. |
| A-005, source-only findings | **Qualified acceptance.** This review ran no tests or shell commands. Recorded historical results and source-derived counterexamples remain distinct evidence. |
| A-006, complete audited change span | **Qualified acceptance.** I accept the supplied target span as scope, but did not independently reproduce the Git comparison. |
| A-007, verified Orca reply shapes | **Reject.** The implementation itself labels those paths UNVERIFIED. |
| A-008, unstated precedence among requirements | **Reject.** Resolve specific conflicts through explicit amendments. The status-exit task instruction resolves that particular inconsistency; it is not blanket precedence for every conflict. |
| A-009, complete combined coverage | **Reject.** Different reviewer slices and their union do not establish exhaustive coverage. Silence is not agreement. |
| A-010, calibration scores | **Accept as metadata only.** Scores do not decide whether a cited counterexample is correct. |

## POINT TABLE

“Backed variant” identifies the closest supported substantive account, not endorsement of every original label. Confidence concerns the recommendation shown, not the probability of an unobserved production failure.

| Point id | Recommended final classification | Backed variant | Confidence | One-line evidence with file:line |
|---|---|---|---:|---|
| X-001 | **Regression, MEDIUM** | V3 | 96% | Crash exit 1 contradicts the specified `once` exit set and exit-code acceptance criterion; [issue-watcher.md:114][commands], [issue-watcher.md:890][acceptance]. |
| X-002 | **Regression, LOW** | V3, severity only | 94% | A completion reason fills a real gap, but the added name still contradicts the unamended closed-table contract; [audit.py:62][reasons], [issue-watcher.md:718][audit-contract]. |
| X-003 | **Authorized expansion, LOW for three helpers; Regression, LOW for the fourth and overbroad boundary allowance** | V1, partial | 96% | The task names three functions, while the source imports four; [task:332][task-record], [record.py:23][record-imports]. |
| X-004 | **Not a defect** | V3, rationale | 95% | Independent bounds in isolated modules comply with the prescribed import boundaries; [issue-watcher.md:235][boundaries], [launch.py:30][orca-shapes]. |
| X-005 | **Authorized expansion, LOW** | none | 99% | The task explicitly requires runner `time.monotonic()` outside the cycle’s decision clock; [task:193][task-tests]. |
| X-006 | **Regression, MEDIUM; blocking** | V2 | 99% | An explicit unconditional no-skip instruction conflicts with a root-dependent `skipif`; [task:188][task-tests], [test_cli.py:1070][skip]. |
| X-007 | **Regression, MEDIUM; blocking** | V2 | 99% | Persistence separates the final deadline check from an unconditional launcher call; [cycle.py:1048][launch-path], [cycle.py:1061][launch-path]. |
| X-008 | **Advisory gap; actual parser failure UNVERIFIED** | V1, qualified | 94% | The accepted pattern permits a leading dash; validation and shell quoting do not establish Orca option-parser compatibility; [launch.py:36][orca-shapes], [launch.py:127][retry]. |
| X-009 | **Not a defect as alleged; residual timing window is advisory** | V3, partial | 99% | A second kill-switch check exists before the origin call; the “checked once” account is false; [cycle.py:1033][launch-path]. |
| X-010 | **Regression, LOW for the extra two names; correct the accounting** | V1 | 98% | The task requires 57 names, including five authorized additions; the implementation additionally defines completion and crash names; [task:199][task-tests], [audit.py:55][reasons]. |
| C-014 | **Regression, MEDIUM; blocking** | V2 | 99% | The acceptance criterion explicitly says no launch starts after 120 seconds; the save-to-launch interval is unchecked; [issue-watcher.md:892][acceptance], [cycle.py:1061][launch-path]. |
| C-013 | **Regression, MEDIUM; blocking** | V2 | 99% | Root-dependent skipping remains prohibited regardless of whether a recorded non-root run skipped nothing; [task:188][task-tests], [test_cli.py:1070][skip]. |
| C-016 | **Advisory design gap, not implementation drift** | V1 | 97% | Future consumed timestamps are excluded after clock rollback by the expressly required half-open window; [record.py:689][day-cap], [task:338][task-record]. |
| C-017 | **Regression, LOW: incorrect status/error reporting** | V3 | 98% | Presence uses `lexists`, timestamp reporting follows symlinks, and status catches only `StoreError`; [record.py:421][disabled], [cli.py:175][status-cli]. |
| C-018 | **Advisory recovery gap** | V1, qualified | 96% | An ordinary exception bypasses final commit; pending recovery preserves at-most-once behavior, but receipt information can be lost; [cycle.py:685][commit], [record.py:627][sweep]. |
| C-019 | **Advisory external-process risk, UNVERIFIED** | V1, qualified | 92% | Captured pipes and a timeout establish the mechanism, not that real Orca descendants retain those pipes; [runner.py:91][runner]. |
| C-024 | **Advisory integration uncertainty; no demonstrated implementation defect** | none | 96% | Exit-zero JSON with a valid id follows the specified mapping; candidate error-id semantics remain unverified; [issue-watcher.md:633][launch-design], [launch.py:39][orca-shapes]. |
| C-026 | **Regression, MEDIUM at the runner/launcher boundary** | V1 | 97% | Truncation can discard an unknown-outcome marker before classification, contradicting the “anywhere” rule; [runner.py:63][runner], [launch.py:322][outcome], [issue-watcher.md:634][launch-design]. |
| C-036 | **Regression, LOW: schema-valid status edge case** | V3 | 96% | Validation permits a missing working directory, while status silently excludes that unknown entry despite its operation id; normal pending creation supplies the directory; [record.py:184][validation], [cycle.py:1271][status]. |
| C-037 | **Advisory contract inconsistency; no demonstrated requirement for exit-pair validation** | V3, qualified | 94% | Fallback always emits kind `cycle`, while reset instructions both prohibit cycle lines and require this fallback; [audit.py:402][fallback], [task:501][task-cli]. |
| C-034 | **Drift, LOW, limited to documentation omissions** | V3, narrowed | 98% | Task-authorized exit 2 behavior is missing from the runbook’s status list; [task:498][task-cli], [issue-watcher-setup.md:432][runbook-status]. |
| C-022 | **Advisory specification gap** | V1 | 97% | Tie detection scans the complete event history, so later reapproval does not remove an old opposing tie; the task explicitly prescribes that behavior; [predicates.py:205][ties], [task:196][task-tests]. |

**Recommended action:** retain the FAIL verdict and correct the late-launch path first, including durable restoration when persistence crosses the cutoff. Then replace the prohibited skips and reverify the affected requirements.

Skipped: runtime reproduction, live GitHub/Orca checks, and an independent Git comparison. Actual Orca reply semantics and the production frequency of slow persistence remain unverified.

[deadline-helper]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:410
[launch-path]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:1033
[acceptance]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:880
[task-tests]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:188
[skip]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_cli.py:1070
[local-gate]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md:28
[pending]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:538
[sweep]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:627
[task-cli]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:498
[orca-shapes]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:30
[runner]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/runner.py:57
[task-record]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:332
[record-imports]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:23
[commands]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:114
[reasons]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/audit.py:55
[audit-contract]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:718
[boundaries]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:235
[retry]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:127
[day-cap]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:689
[disabled]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:421
[status-cli]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cli.py:175
[commit]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:685
[launch-design]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:633
[outcome]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:322
[validation]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:184
[status]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:1271
[fallback]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/audit.py:402
[runbook-status]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher-setup.md:432
[ties]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/predicates.py:205

### Variant 3 Advocate

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

## Round 2: Rebuttals

### Variant 1 Advocate (rebuttal)

| Status | Result |
|---|---|
| DONE | Verified disputed facts (a) to (d) against the live files. Final rebuttal and 22-row table are below. |
| NEXT | None. |

## Round 2 rebuttal, Variant 1

**Concessions.** My Round 1 had wrong line cites: `cycle.py:335-337` should be 1060-1062, and `:308` should be 693 and 1033. My header said "1 MEDIUM" when two rows were MEDIUM. I rated the skip sites Necessary LOW, which was wrong. I missed the late launch. I also did not read the register, tests or `spec-final.md` before arguing.

**(a) Crash exit 1 and the two added reasons.**
- Design line 722 requires a stderr fallback "used for a crash". Line 718 makes `line()` reject any name outside the table. So the design forced a name for the crash line, and it never gave one.
- `_EXIT_CRASH = 1` (`cli.py:35`) is Python's default for an uncaught exception. The task discloses the change (task 900, 905).
- AC-17 (design 890) is tested on normal outcomes. The crash path is not in it.
- Verdict: Necessary deviation LOW, plus Drift LOW because the design was never amended. It is not Regression. I withdraw my Round 1 MEDIUM, which was too high.

**(b) Root-guarded skips.**
- This does violate task line 188. The five sites (`test_record.py:739`, `test_cycle.py:735` and `:4694`, `test_cli.py:967` and `:1070`) are real, and the task graded them "minor" itself (task 908).
- The recorded runs (p8-g1, p8-g3, p9-g3) had 0 skipped, so the gate criterion was met. The skips only bite when the suite runs as root.
- Verdict: Drift MEDIUM, non-blocking. V2's "blocking" overstates it. V3's Regression is not warranted either, because no previously working behaviour broke.

**(c) V2's "Regression" labels.** Under the strict definition, none of X-001, X-002, X-010, C-013, C-017, C-026 or C-036 qualifies.
- X-010 is stale documentation, and the tests pin 59 names (`test_audit.py:215-219`).
- C-017 is only an implied conflict with the runbook, in a dangling-symlink corner case (setup 298, `record.py:421-431`).
- C-026 is a conflict inside the design itself: the 500-byte cap (design 218, 822) against the "anywhere" rule (634). It needs exit 0, a valid id, and the marker past byte 500.
- C-036 is reachable only through a hand-edited store.

I steelman V2 on C-013. The task did say "no skips", the skips are a clear drift, and V2 is right that they are more than cosmetic. I now agree with V2 on the category and disagree only on "blocking".

**(d) Late launch (X-007, C-014). My position changed.**
- `launch_allowed()` is checked at `cycle.py:1039`. Between 1048 and 1062 there is a git call, `mark_pending` and an fsync'd `_save()` (1060-1061), and no further cutoff check before `launcher.launch` at 1062.
- If the clock crosses 120 s during that window, a launch starts after the cutoff. That contradicts design 647 and the letter of AC-19.
- It is narrow. The save is a local fsync, the worst case is about 241 s of the 300 s budget, and at-most-once still holds.
- Verdict: Regression LOW, non-blocking. I now side with V3 on the label. V2's HIGH and blocking is too high. My Round 1 "advisory gap" was too low.
- Fix: snapshot `prev`, re-check the cutoff after `_save()`, then `_set(prev)`, `_save()`, and `raise _Skip("budget_exhausted")`. If the rollback save fails, the sweep turns the entry into `pending_orphan` with no launch. Add a slow-save test with a clock that passes 120 s inside `store.save`. Existing tests only cover 121 s and exactly 120 s (`test_cycle.py:1964`, `:1982`).

**New evidence on X-003.** `test_module_boundaries.py:20-22` records that `record` imports three functions and one type from `predicates`, where design 5.3 says "types only". The deviation is disclosed in the test. `valid_operation_id` stays the weakly disclosed piece.

**Other variants.** V3 is right that X-001 and X-002 also leave the design un-amended, and I now carry that as Drift LOW. V2 is right that the skips are Drift. I still disagree that either one is Regression.

## UPDATED POINT TABLE

"Changed" means changed since my Round 1. Evidence marked "not re-read" comes from the diff analysis only, and its confidence is capped.

| Point | Final classification | Backs | Conf | Evidence | Changed |
|---|---|---|---|---|---|
| X-001 | Necessary deviation LOW + Drift LOW (design not amended) | V1 category, V3 doc gap | 65% | `cli.py:35`, `122-129`; design 718, 722; task 905 | Yes (MEDIUM to LOW) |
| X-002 | Necessary deviation LOW | V3 | 70% | `audit.py:62-64`; `cycle.py:1134-1137`; `test_audit.py:215-219` | No |
| X-003 | Authorized LOW; `valid_operation_id` Necessary/Drift LOW | none | 60% | `test_module_boundaries.py:20-22`; `record.py:168-210`; design 239 | No |
| X-004 | Necessary deviation LOW + parity-test advisory gap | V3 | 60% | diff-analysis X-004 row (not re-read) | No |
| X-005 | Authorized expansion LOW | none | 75% | task 193 | No |
| X-006 | Drift MEDIUM, non-blocking | V2 category | 72% | skip sites above; task 188, 908 | Yes (Necessary LOW to Drift MEDIUM) |
| X-007 | Regression LOW, non-blocking | V3 | 62% | `cycle.py:1039`, `1048`, `1060-1062`; design 634, 647 | Yes (advisory gap to Regression LOW) |
| X-008 | Advisory correctness gap LOW | none | 50% | diff-analysis X-008 row (not re-read) | No |
| X-009 | Not a defect (second check exists) | none | 80% | `cycle.py:693`, `1033` | No |
| X-010 | Not a defect (stale doc, disclosed) | none | 75% | task 905; `test_audit.py:215-219` | No |
| C-014 | Regression LOW, non-blocking | V3 | 62% | same as X-007 | Yes |
| C-013 | Drift MEDIUM, non-blocking | V2 category | 72% | same as X-006 | Yes |
| C-016 | Advisory gap LOW (design-conformant) | none | 55% | not re-read | No |
| C-017 | Advisory gap LOW | V1, V3 | 65% | setup 298, 302; `record.py:421-431` | No |
| C-018 | Advisory gap LOW | none | 55% | not re-read | No |
| C-019 | Advisory gap, unverified | none | 50% | not re-read | No |
| C-024 | Advisory gap LOW-MEDIUM (reply shape unverified) | none | 60% | `launch.py:296-334` | No |
| C-026 | Advisory gap LOW | none | 65% | `launch.py:322`, `326-334`; design 218, 634, 822 | No |
| C-036 | Advisory gap LOW (near-unreachable) | none | 65% | `record.py:168-210` | No |
| C-037 | Advisory gap LOW | none | 60% | `cycle.py:1255-1290` | No |
| C-034 | Drift LOW (docs only); part (c) not a defect | none | 55% | `cli.py:164-182`; design 115, 726 | No |
| C-022 | Advisory gap LOW (fail-closed, spec-conformant) | none | 70% | `record.py:421-431`; setup 298 | No |

**Recommended action:** Treat X-007/C-014 as the only Regression, at LOW and non-blocking, and fix it with the re-check after `_save()` plus the slow-save test.

### Variant 2 Advocate (rebuttal)

| Status | Result |
|---|---|
| DONE | Re-read the disputed implementation and requirements; revised classifications and confidence below. |
| NEXT | Retain the acceptance failures; correct the late-launch path with restoration and a slow-save test. |

## Rebuttal

**Variant 2’s acceptance-based argument survives, but its confidence was overstated.** My Round-1 values of 94-99% conflated confidence in a source observation with confidence in a contested classification. Every updated value below is at most 90%.

**Late launch remains a Regression, MEDIUM and blocking.** Acceptance criterion 19 says: “A sleeping stub ends with `gh_timeout`; **no launch starts after 120 s**” ([design:892][acceptance]). The source checks the cutoff, changes the document, persists it, then invokes the launcher without another check ([cycle.py:1048-1062][launch-path]). Persistence crossing the cutoff supplies a direct counterexample. The cadence margin and preserved at-most-once protection reduce impact; neither exempts the acceptance criterion. “Blocking” follows the unmet requirement, not a demonstrated HIGH operational risk.

**Restoration is compatible with the design, with a failure qualification.** Design 647 requires “no entry” when the deadline prevents launch ([design:638-649][deadline]). Snapshot the pre-pending document, keep durable-before-spawn ordering, and restore that document durably if persistence crosses the cutoff. For a previously failed entry, restoration means returning to that prior state, not deleting it; the design expressly recognizes “no entry (or `failed`)” ([design:527-533][crash]). A bare post-save skip is wrong. If restoration fails or the process crashes, do not claim successful restoration: leave the conservative pending state and report failure. That exceptional state is already documented at crash point C3.

**The strict taxonomy preserves several disputed Regression labels.** Regression does not require previously working behavior to break when an acceptance criterion or documented invariant is contradicted.

- **Crash exit, completion reason, and reason count:** acceptance criterion 17 requires each verb’s exits to match section 4; the task also mandates exactly 57 reasons ([design:890][acceptance], [task:199][task-tests]). A required crash fallback does not itself authorize exit 1 or amend the closed table. The register explicitly calls these executor decisions without authorizing research rows ([register:43-47][register]). These remain LOW contract regressions, not three independent defects.
- **Prohibited skips:** the unconditional construction rule is violated by `skipif`; zero skips during recorded runs does not satisfy “No test may use” it ([task:188][task-tests], [test_cli.py:1070][skip]). This remains a verification Regression.
- **Kill-switch status:** I withdraw Regression for this point. The task explicitly prescribes `os.stat`; its interaction with dangling symlinks exposes an advisory contract gap, rather than an unambiguous implementation departure ([task:335][task-record], [record.py:421-431][disabled]).
- **Truncated stderr:** retain Regression, reduced to LOW. The counterexample requires exit 0, a valid id, and the unknown-outcome marker beyond byte 500. The design’s “anywhere” rule is explicit; limiting retained stderr does not exempt classification ([design:634][deadline], [runner.py:126][runner], [launch.py:322-334][outcome]).
- **Missing retry directory:** retain Regression LOW against acceptance criterion 9 and the unqualified retry-list source rule. Normal creation supplies the directory, but validation accepts null and status silently drops that schema-valid entry ([record.py:183-184][validation], [design:739][retry-contract], [cycle.py:1271-1280][status]).

**Updated view of the alternatives:** Variant 1 contributes the strongest breadth of behavioral investigation and correctly challenges severity inflation. Variant 3 contributes the strongest module-boundary explanation and operator-facing checks. Their advisory cautions improve Variant 2, but neither makes explicit requirement contradictions disappear. Conversely, my original blanket authorization of imports and Regression label for kill-switch status were too broad.

## UPDATED POINT TABLE

“Changed” marks a substantive classification or severity change since my Round 1. Confidence is recalibrated throughout. “Backs” identifies the closest substantive account, not endorsement of its original label.

| Point | Final classification | Backs | Confidence | Evidence file:line | Changed |
|---|---|---|---:|---|---|
| X-001 | Regression LOW: crash exit violates exit-set contract | V3 | 80% | [design:114][verbs], [design:890][acceptance], [cli.py:123-129][crash-cli] | Yes |
| X-002 | Regression LOW: added name violates closed-table contract | none | 78% | [task:199][task-tests], [audit.py:62-64][reasons] | No |
| X-003 | Authorized for three helpers and permitted type; Regression LOW for fourth helper | none | 82% | [task:332][task-record], [record.py:23-29][imports], [design:231-239][boundaries] | No |
| X-004 | Necessary LOW: isolated-module duplication; parity checking advisory | V3 | 83% | [design:237-240][boundaries], [launch.py:30][constants] | Yes |
| X-005 | Authorized LOW: runner timing expressly instructed | none | 90% | [task:193][task-tests] | No |
| X-006 | Regression MEDIUM, blocking: prohibited test constructs | V2 | 87% | [task:188][task-tests], [test_cli.py:1070][skip] | No |
| X-007 | Regression MEDIUM, blocking: deadline acceptance failure | V2 | 88% | [design:892][acceptance], [cycle.py:1048-1062][launch-path] | No |
| X-008 | Advisory LOW: option parsing unverified, not shell injection | V3 | 82% | [launch.py:36][constants], [launch.py:127-132][retry] | No |
| X-009 | Alleged single check disproved; residual window advisory | V3 | 88% | [cycle.py:693][commit], [cycle.py:1033][launch-path] | No |
| X-010 | Regression LOW: same unamended count contract as X-002 | none | 80% | [task:199][task-tests], [register:43-47][register] | No |
| C-014 | Regression MEDIUM, blocking; restore prior document before skipping | V2 | 88% | [cycle.py:1060-1062][launch-path], [design:647][deadline] | No |
| C-013 | Regression MEDIUM, blocking: same as X-006 | V2 | 87% | [task:188][task-tests], [test_cli.py:1070][skip] | No |
| C-016 | Advisory design gap: prescribed rolling window | V1 | 86% | [record.py:689-703][day-cap], [task:338][task-record] | No |
| C-017 | Advisory LOW: prescribed timestamp lookup conflicts with presence semantics | V1/V3 | 80% | [task:335][task-record], [record.py:421-431][disabled] | **Yes** |
| C-018 | Advisory recovery gap: ordinary exceptions bypass final commit | V1 | 82% | [cycle.py:685-690][commit], [design:529-530][crash] | No |
| C-019 | Advisory external-process risk, UNVERIFIED | V1 | 65% | [runner.py:91-101][runner] | No |
| C-024 | Advisory integration uncertainty; error-id semantics UNVERIFIED | none | 77% | [launch.py:39-45][constants], [launch.py:326-334][outcome] | No |
| C-026 | Regression LOW: narrow violation of “anywhere” classification | V1 | 79% | [runner.py:126][runner], [launch.py:322-334][outcome], [design:634][deadline] | **Yes** |
| C-036 | Regression LOW: schema-valid input omitted from required retry list | V3 | 79% | [record.py:183-184][validation], [cycle.py:1271-1280][status], [design:739][retry-contract] | No |
| C-037 | Advisory contract inconsistency, not demonstrated exit-pair requirement | V3 | 78% | [audit.py:393-402][fallback], [task:501][task-cli] | No |
| C-034 | Drift LOW: documentation omissions; command exits authorized | V3 | 83% | [task:498-501][task-cli], [setup:432][runbook] | No |
| C-022 | Advisory specification gap: historical ties expressly prescribed | V1 | 86% | [predicates.py:199-209][ties], [task:196][task-tests] | No |

**Recommended action:** correct the late-launch acceptance failure first, preserving durable-before-spawn ordering and testing successful restoration plus restoration failure.

Not checked: runtime reproduction, live Orca behavior, or production frequency. No files changed and no tests ran.

[acceptance]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:878
[deadline]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:625
[verbs]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:114
[boundaries]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:229
[crash]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:523
[retry-contract]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher.md:739
[task-tests]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:188
[task-record]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:332
[task-cli]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:498
[register]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/deviation-register.md:43
[launch-path]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:1007
[commit]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:685
[status]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cycle.py:1271
[disabled]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:421
[validation]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:183
[imports]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:23
[day-cap]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/record.py:689
[runner]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/runner.py:57
[outcome]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:311
[constants]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:30
[retry]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/launch.py:119
[reasons]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/audit.py:55
[fallback]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/audit.py:381
[crash-cli]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/cli.py:123
[skip]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/tests/issue_watch/test_cli.py:1070
[ties]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/issue_watch/predicates.py:199
[runbook]: /home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/docs/designs/issue-watcher-setup.md:432

### Variant 3 Advocate (rebuttal)

| Status | Result |
|---|---|
| DONE | Read the diff analysis, all three Round-1 statements and both Round-2 rebuttals, then re-read the disputed source lines. |
| NEXT | Final merge by the orchestrator. I wrote no files and ran no tests. |

## Round 2 rebuttal, Variant 3

**Answers to the criticisms of Variant 3**

1. **X-001, the crash exit.** I concede on category. Under the strict rule, Drift ("contradicts nothing") is the wrong label.
   - `_EXIT_CRASH = 1` (`cli.py:35`, used at `:124-129`) is not in the `once` exit list: "0, 2, 3, 4, 5, 6, 7, 75" (design `:114`).
   - AC-17 says "Each verb's exit codes match section 4" (design `:890`).
   - The register says outright that "no R-003 row authorizes" it (deviation-register.md:43).
   - The design does require a crash fallback (`:722`) but gives it no exit code. That lowers the severity. It does not change the category.
   - Final: Regression LOW, non-blocking. The fix is to amend design `:114`.
2. **Wrong path in row 11.** Conceded again. The registration is at `src/superclaude/cli/main.py:563-565`. It is planned in research/06:208 (DF-29), so the row stays Authorized.
3. **Hedged categories.** I have collapsed them into a single label per row. X-002 and X-010 are one root issue. The table has 59 names (`test_audit.py:215-219`), but task `:199` says "exactly 57 entries" and design `:718` says `REASONS` is "equal to the spec's reason table". Both are Regression LOW. X-010 is not a separate defect.
4. **Rows 8 and 10 "closer to aligned".** Accepted. I hold row 10 (X-004) as Necessary, citing design `:237` and `:240` via the diff analysis. I did not re-read them.
5. **Row 6(c) against design `:726`.** The task settles this. The status command must exit "0 healthy, 1 unhealthy, 2 config invalid, 6 store unreadable" (task `:498`, which matches design `:115`).
   - Design `:726` and runbook `issue-watcher-setup.md:432` both leave out exit 2.
   - So C-034 is a documentation omission, not a code defect.

**Updated view of the other variants**

- **V2's strongest point holds.** AC-19 is a real acceptance criterion, and the code contradicts it. I was wrong to weigh impact as if it decided whether the work can be approved.
- **V1 is right that severity is low.** My reasons stand: a local fsync, about 241 s of the 300 s cadence, the lock, and at-most-once still holding.
- **V2 is also right on C-026 and C-036 under the strict rule.**
  - C-026: the design's "anywhere in stdout or stderr" rule (`:634`) can be met together with the 500-byte cap: search before truncating. So the cap does not force the gap.
  - C-036: design `:739` defines `retry` as "`unknown` entries with an `operation_id`". Validation accepts a null `launch_cwd` (`record.py:184`), so a valid store can still lose a retry line.
- **V2 has dropped Regression for C-017, and I agree.** The task prescribes `os.stat`.

## Late launch (C-014 / X-007): final position

- **Category and severity:** Regression, LOW severity, **blocking**. I still back Regression, now with every variant agreeing on the category.
- **What it contradicts:**
  - AC-19, design `:892`: "A sleeping stub ends with `gh_timeout`; no launch starts after 120 s".
  - FR-029, `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md:199`: "No launch starts after 120 s."
  - Design `:647`: "not started when `elapsed() > 120`; the step ends with no entry".
- **The code path:** the last cut-off check is at `cycle.py:1048`. Then come `mark_pending` (`:1060`), the fsync'd save (`:1061`) and an unconditional `launcher.launch` (`:1062`). `launch_allowed()` is `elapsed() <= 120` (`cycle.py:410-412`).
- **Why I changed to blocking:** an acceptance criterion with a direct counterexample should not be approved as met. A Gate C fix already tried to close this exact property (task `:901`). Low impact sets the severity, not whether it blocks.
- **A compatible fix exists:**
  1. Keep `prev = self.doc`. `mark_pending` returns a new document built with `replace` and `_with_entry` (`record.py:554-568`), so `prev` is not changed by it.
  2. After `_save()`, re-check the cut-off.
  3. On failure, restore `prev`, save again, then `raise _Skip("budget_exhausted")`.
- **What the fix gives:**
  - The step ends with "no entry (or `failed`)", which is crash point C1 (design `:527`).
  - If the restore save fails, the entry is left in crash state C3, which becomes `pending_orphan` with no launch (`:529`).
  - The save stays durable before any spawn.
- **Test to add:** a clock that passes 120 s inside `store.save`. It should assert no launcher call, the restored entry, and a `budget_exhausted` decision line.

## What blocks approval

- **Blocks approval:** only C-014 / X-007.
- **Must be fixed before the task is closed, but does not block:** X-006 / C-013, the skips. They break task `:188` ("No test may use `pytest.skip`, `skipif` or `xfail`"), so they are Regression MEDIUM. They are MEDIUM because `NOT_ROOT` (`test_cli.py:1070`) silently skips the file-mode security tests when the suite runs as root. They do not block because every recorded gate run had zero skips (task `:908`).
- **Everything else:** non-blocking documentation or test-hygiene findings.

## UPDATED POINT TABLE

| Point | Final classification | Backs | Conf. | Evidence | Changed |
|---|---|---|---|---|---|
| X-001 | Regression LOW, non-blocking (design gives a crash no code) | V2 | 65% | `cli.py:35`, `:124-129`; design `:114`, `:890`, `:722`; register `:43` | Yes |
| X-002 | Regression LOW, non-blocking (same root issue as X-010) | V2 | 65% | task `:199`; design `:718`; `test_audit.py:215-219` | Yes |
| X-003 | Authorized for 3 functions and the type; Regression LOW for `valid_operation_id` | V2 | 60% | task `:332`; `record.py:23-29`, `:183`; design `:239` | Yes |
| X-004 | Necessary LOW; parity test advised | V3 | 80% | design `:237-240` (from the diff analysis); `launch.py:30` | No |
| X-005 | Authorized LOW | none | 88% | task `:193`; `runner.py:89` | No |
| X-006 | Regression MEDIUM, fix before closing the task, not blocking | V2 (category) | 72% | task `:188`, `:908`; `test_cli.py:1070` | Yes |
| X-007 | Regression LOW, **blocking** | V2 | 75% | `cycle.py:1048-1062`, `:410-412`; design `:892`, `:647` | Yes (now blocking) |
| X-008 | Advisory LOW (option parsing unverified) | V3 | 65% | `launch.py:36`, `:119-132` | No |
| X-009 | Not a defect | V3 | 88% | `cycle.py:693`, `:1033-1034` | No |
| X-010 | Same finding as X-002 (Regression LOW) | V2 | 65% | task `:199`; setup `:344` | Yes |
| C-014 | Regression LOW, **blocking**; fix with snapshot and restore | V2 | 75% | `cycle.py:1060-1062`; `record.py:554-568`; design `:527-529`, `:647` | Yes |
| C-013 | Same as X-006 | V2 (category) | 72% | task `:188`; `test_cli.py:1070` | Yes |
| C-016 | Advisory LOW; matches the design | V1 | 70% | `record.py:689-703` | No |
| C-017 | Advisory LOW (runbook claims more than the code does) | V1/V3 | 75% | `record.py:421-431`; setup `:296`, `:301` | No |
| C-018 | Advisory LOW | V1 | 70% | `cycle.py:685-690` | No |
| C-019 | Advisory, unverified | V1 | 50% | `runner.py:91-101` | No |
| C-024 | Advisory LOW-MEDIUM; matches the design; reply shape unverified | V1 | 65% | design `:633`, `:636`; `launch.py:39-45` | No |
| C-026 | Regression LOW, non-blocking (a compatible fix exists) | V2 | 55% | design `:634`; `runner.py:126`; `launch.py:322` | Yes |
| C-036 | Regression LOW, nearly unreachable, non-blocking | V2/V3 | 60% | design `:739`; `record.py:184`; `record.py:548-549`; `cycle.py:1271-1280` | Yes |
| C-037 | Advisory LOW | V3 | 75% | `audit.py:381-404`; design `:722` | No |
| C-034 | Documentation Drift LOW; code exits are authorized | V3 (narrowed) | 80% | setup `:53`, `:432`; task `:498`; design `:115`, `:121`, `:726` | Yes (part c) |
| C-022 | Advisory LOW-MEDIUM; the tie rule is prescribed by the task | V1 | 75% | `predicates.py:199-209`; task `:196` | No |

**Recommended action:** before approval, fix C-014 with the snapshot-and-restore re-check after `_save()` and add the slow-save test. Replace the five skip sites in the same pass.

Not checked: I ran no tests and reproduced nothing. Design `:237-240` and the full text of task `:332` were not re-read this round.

## Round 2.5: Invariant Probe

See invariant-probe.md (12 findings, 0 HIGH unaddressed). Raw output:

No HIGH finding blocks convergence. Within one store, launching at most once per issue holds. One way to break it exists outside that scope: two watchers running on the same login and repo with different state directories. The proposed restore fix is safe and better than leaving the entry pending, as long as it restores the snapshot taken just before line 1060.

**ID: INV-001** | sufficiency_challenge | ASSUMPTION: "at-most-once holds" with no further condition | STATUS: UNADDRESSED | SEVERITY: MEDIUM | EVIDENCE: The lock and the store both live under `state_dir` (record.py:380-419). The only guard across stores is the claim marker (cycle.py:922-928), and the marker exists only after the launched agent posts it. Two watchers with different `state_dir` values on the same login and repo can each pass every check at cycle.py:917-942 and both launch, before either marker appears. Nothing in the code enforces "one store per login and repo" (I did not verify whether the design states this assumption). This needs operator misconfiguration, so MEDIUM, not HIGH.

**ID: INV-002** | sufficiency_challenge | ASSUMPTION: no relaunch path within a single store | STATUS: ADDRESSED | SEVERITY: LOW | EVIDENCE: `_launch` is reachable only from no entry, or from `failed` after its backoff (cycle.py:913-942). `mark_pending` accepts only those two states (record.py:544-546). Every entry that has been pending goes through the marker-only branch, which can claim but never launch (cycle.py:903-912): that covers pending, which the sweep turns into abandoned (record.py:638-648), launched, unknown, and abandoned with `pending_at` (spawn_error keeps it). Entries are deleted only by `reset_entry` (record.py:706-720). Re-init cannot pass an old approval (predicates.py:230-231). The pending record is durable before the launch (cycle.py:1060-1062), using fsync, then replace, then directory fsync (record.py:370-378, swarm/atomic.py:14-39).

**ID: INV-003** | interaction_effects | ASSUMPTION: the restore fix adds no double-launch | STATUS: ADDRESSED (only if the fix is ordered correctly) | SEVERITY: LOW | EVIDENCE: The re-check and the restore must both happen after `_save` (1061) and before `launcher.launch` (1062). If the process crashes between the pending save and the restore, the pending entry stays on disk. The sweep then makes it `pending_orphan` (record.py:638-639), which only a marker can resolve (cycle.py:903-912). That is safe, but the issue is stranded until `reset --forfeit-guarantee`. A failed restore save becomes `state_dir_unwritable` (cycle.py:582-587), and the commit is skipped for that reason, so the result is the same safe orphan. Leaving the entry pending or abandoned on purpose is worse: no agent will ever post a marker, so every cut-off crossing strands an issue. Restoring is better.

**ID: INV-004** | state_variables | ASSUMPTION: the restore puts back exactly the state from before the launch attempt | STATUS: UNADDRESSED (a fix-design constraint) | SEVERITY: LOW | EVIDENCE: `mark_pending` sets launches to 1 and sets `consumed_at` and `pending_at`, while keeping `attempts` (record.py:554-567). The load-time validator rejects `failed` with launches 1 (record.py:168-210). So a field-by-field undo that only sets the state back to `failed` produces a store that will not load. The restore must reinstate the whole document captured just before 1060. The load-time document is wrong because the pending save also persisted that cycle's sweep and claims. With the right snapshot, launches goes back to 0, `consumed_at` is cleared (so the day cap is uncharged, which is correct because nothing launched), `consumed_log` is unchanged, and a `failed` entry keeps its attempts. Raising `_Skip("budget_exhausted")` leaves the candidate unstamped (cycle.py:793-815), so it is retried first next cycle (predicates.py:299-312).

**ID: INV-005** | sufficiency_challenge | ASSUMPTION: the late-launch fix alone keeps the cycle within 240 s | STATUS: UNADDRESSED | SEVERITY: LOW | EVIDENCE: The launch timeout is a fixed `LAUNCH_TIMEOUT_S` (120 s) and is not limited by the time left on the deadline (cycle.py:1062, Deadline at 395-412). A launch that starts at exactly 120 s can run to 240 s, and the commit and audit line then run past 240 s. The `_save` fsync has no time limit either. The overshoot is small (save plus commit time), but the fix as proposed does not bound it.

**ID: INV-006** | guard_conditions | ASSUMPTION: the DISABLED file stops a launch that was already being prepared | STATUS: UNADDRESSED | SEVERITY: LOW | EVIDENCE: DISABLED is checked at cycle.py:1033. It is not checked again after the origin git call, which can take up to 10 s (1041-1045), or after the save (1061). An operator who creates DISABLED in that window still gets one launch.

**ID: INV-007** | count_divergence | ASSUMPTION: 3 reserved calls cover revalidation | STATUS: UNADDRESSED | SEVERITY: LOW | EVIDENCE: The reserved cap is 35 against 32 for other calls (github.py:448-454). The events and project re-reads page up to 5 times, one call per page. If the reserve runs out, or the deadline floor is hit, `_call` returns `budget_exhausted` (github.py:557-577), and the cycle halts at revalidation (cycle.py:960-997). Only liveness is affected: the candidate is unstamped and retried first next cycle. The reason name also hides whether the cause was the deadline or the budget.

**ID: INV-008** | collection_boundaries | ASSUMPTION: the day cap survives clock steps | STATUS: UNADDRESSED (already a known advisory) | SEVERITY: LOW | EVIDENCE: `_in_window` excludes any future-dated `t` (record.py:689-690), so after a backward clock step recent launches stop counting and the cap fails open. `prune_consumed_log` keeps future times (`t > cutoff`, record.py:696), so they start counting again once the clock catches up. The window is inconsistent but never under-counts after that point.

**ID: INV-009** | interaction_effects | ASSUMPTION: the claim window lines up local and server time | STATUS: UNADDRESSED | SEVERITY: LOW | EVIDENCE: `pending_at` comes from the local clock (cycle.py:1060), while the marker time comes from the GitHub server (predicates.py:274-276, 294-295). If the local clock runs more than 300 s ahead of the server, a real claim marker never counts. The entry then stays abandoned for good. Only liveness is affected, never a relaunch.

**ID: INV-010** | state_variables | ASSUMPTION: reset cannot cause an unauthorized second launch | STATUS: ADDRESSED | SEVERITY: LOW | EVIDENCE: `reset_entry` accepts only abandoned or unknown entries, and it moves `consumed_at` into `consumed_log` so the day-cap count is kept (record.py:706-720). The CLI takes the lock and requires `--forfeit-guarantee` (cli.py:282-348). Resetting an `unknown` entry whose launch really happened gives a second launch, but the operator has explicitly authorized it.

**ID: INV-011** | guard_conditions | ASSUMPTION: the unconditional sweep cannot orphan a live pending entry | STATUS: ADDRESSED | SEVERITY: LOW | EVIDENCE: The sweep turns every pending entry into abandoned with no age check (record.py:627-651). This is safe only because every cycle, dry-run and reset takes the exclusive flock (record.py:380-419, cycle.py:663-683). The cost is that a dry-run holding the lock makes a real cycle exit with `lock_held`.

**ID: INV-012** | interaction_effects | ASSUMPTION: an exception after the launch keeps the record correct | STATUS: ADDRESSED for safety, UNADDRESSED for the record | SEVERITY: LOW | EVIDENCE: `_locked_body` catches only `_Stop` (cycle.py:685-690). Any other exception after line 1062 skips `_commit`, and cli.py:123-129 reports `cycle_crashed`. The disk still holds pending, which the sweep orphans and only a marker can resolve, so at-most-once holds. But the outcome of the launch and its operation id are lost, so the retry list cannot offer that issue (cycle.py:1271).

Summary:
1. At-most-once holds within one store (INV-002). It breaks with two stores on one login and repo (INV-001, MEDIUM, a scope assumption the code does not enforce).
2. The restore fix is safe and better than leaving the entry pending, provided it restores the snapshot taken before line 1060 and runs before line 1062 (INV-003, INV-004).
3. The fix alone does not keep the cycle within 240 s (INV-005), and DISABLED is not re-checked after the git call (INV-006). Both are LOW.

| Status | Result |
|---|---|
| DONE | Traced every state that can reach a launch, and re-read the cited lines in cycle.py, record.py and predicates.py this turn. |
| DONE | Checked the restore fix against a crash, a previously failed entry, launches going back to 0, and day-cap accounting. |
| NEXT | Team-lead decides whether INV-001 is in scope; if so, the design must state "one store per login and repo" or add a cross-store guard. |

I skipped the debate files, audit.py, and the rest of github.py and launch.py. The INV-001 scope statement is UNVERIFIED against the design document, and the github.py, cli.py and atomic.py line numbers come from reads made before the context reset; I did not re-read them this turn.

## Scoring Matrix

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

## Convergence Assessment

- Points resolved: 56 of 67 (see scoring-matrix.md for the definition of total and agreed points)
- Alignment: 83.6%
- Threshold: 80%
- Status: CONVERGED (taxonomy levels L1, L2, L3 all covered; invariant-probe gate passed: no HIGH-severity UNADDRESSED invariant)
- Unresolved points: listed in scoring-matrix.md (11 points not agreed)
