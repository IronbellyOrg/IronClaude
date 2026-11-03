# Reflection report: pre-execution review of the P0 plan

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.86
citations_total: 180
citations_revalidated: 81
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 81`: size of the re-Read sample (81 of 180). It holds all 15 citations on blocking findings, 30% of the rest and a 10% spot-check (`artifacts/citation-sample.yaml`).
> - `citations_dropped: 0`: drops seen in the sample (`artifacts/evidence-validation.yaml`).
> - `citations_dropped_extrapolated: 0`: estimate for all 180, `round(0 x 180/81)`. Recorded only; it does not gate promotion.
>
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.

## Summary

**Verdict: FAIL.** The plan should not be run as written. One defect is blocking, and a second blocking candidate is open.

- **Blocking (D-001, Task 7):** no order of Task 7's steps meets all its instructions. The task must commit and then install, yet "make the commit the last action". It must also record the commit ID. `/sc:implement`'s check fails a task that breaks its own instruction. After Task 7's own commit, a failed check cannot be retried, so the run halts.
- **Open, possibly blocking (INV-002, Task 8 and the spec):** acceptance check AC-0.4 needs live-check step 3, which compares the worker's outcome with a contract file that no P0 command writes (that arrives in P1). Every smoke run would fail step 3, or pass it only by reporting `failed`. This looks like a gap in the spec itself, so the owner must decide it.
- **Should-fix (D-002 to D-004):** no checked run longer than the heartbeat cadence (Task 8). The no-copy rule is widened to the whole contract file (TL:21). Tasks 1 and 5 ask for "four" refusal texts where the spec gives three plus a prefix.
- **Minor (D-005 to D-015):** eleven smaller defects. The Task 3 dependency gap is harmless because `/sc:implement` runs tasks in file order. Others are a missing closing task and phase report, and the missing `--source terminal` fallback.
- **Method:** a Tier 2 review by three reviewers on different model classes, each blind-calibrated (0.83, 0.87, 0.87). The cards were merged by an adversarial debate: 2 rounds plus an invariant probe, convergence 0.96 but blocked by 2 open high-severity invariants. 81 of 180 citations were re-Read; 0 dropped.
- **Coverage:** 25 of 101 inferred spec requirements match a plan task (0.25). The plan covers only phase P0 on purpose (TL:19), so most unmatched rows belong to P1-P4.

## Deviations

### Deviation D-001: Task 7's instructions cannot all be followed in any order, on the task that commits and runs `--force` (blocking; merged id M-01)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:110
- **Mapped tasklist item:** Task 7
- **Spec section:** source.md:282
- **Evidence:** cited lines TL:25, TL:110, TL:113, SRC:282, retry.md:41, retry.md:44, qa.md:52, qa.md:61, qa.md:288. Re-Read 9 of its citations, 0 dropped. Example: "...ask the owner to approve committing... then ask to approve `uv run superclaude install --force`... Make the commit the last action of the task." (TL:110, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line; the commit itself is a necessary deviation (SRC:282). Severity set by the adversarial debate (debate confidence 0.85); raised by reviewer 3 R3-F1 (calibrated 0.87, was blocking); reviewer 3 R3-F4 (calibrated 0.87, was minor); reviewer 1 F3 (calibrated 0.83, was minor).
- **Default remediation:** rewrite TL:110 as one order with each approval asked just before its own action (INV-001): install approval, install, write `t7-approvals.md` without the ID, commit approval, stage the listed P0 paths (C:77-81) plus `.dev/tasks` and commit with `git commit --only -- <paths> .dev/tasks` as the last product action, then append the commit ID and stage it; a refusal or any QA failure after the commit ends in a halt for the person's Ruling and is never retried; add a Constraint line that the run is attended and never headless.

### Deviation D-002: Task 8 never requires a checked run longer than the heartbeat cadence (should-fix; merged id M-02)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:122
- **Mapped tasklist item:** Task 8
- **Spec section:** source.md:291, source.md:78
- **Evidence:** cited lines SRC:291, SRC:78, TL:15, TL:122, TL:124-128. Re-Read 2 of its citations, 0 dropped. Example: "From the person-opened session acting as coordinator, create one Orca Run and run the ./source.md section 7.2 live check, steps 1-3 and 5-7 ..." (TL:122, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity set by the adversarial debate (debate confidence 0.9); raised by reviewer 1 F4 (part a) (calibrated 0.83, was minor); reviewer 2 R2-1 (calibrated 0.87, was blocking); reviewer 3 R3-F2 (calibrated 0.87, was blocking).
- **Default remediation:** Task 8's AC requires `ac-0.4-smoke.md` to name one checked run whose top-level session, outside Agent-tool calls, lasted longer than the preamble cadence, with start and end times; if none qualifies, add or extend a run, and if none is achieved the report records the duty as unmet and P0 does not pass (R2-C:69).

### Deviation D-003: TL:21 widens the spec's no-copy rule to the whole file, against the guard line TL:52 requires verbatim (should-fix; merged id M-03)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:21
- **Mapped tasklist item:** Constraints (TL:21) and Task 2 (TL:52)
- **Spec section:** source.md:59, source.md:86
- **Evidence:** cited lines TL:21, TL:42, TL:52, TL:87, SRC:59, SRC:86. Re-Read 3 of its citations, 0 dropped. Example: "The file contains no `orca orchestration` verb syntax copied from Orca's guides and no fixed heartbeat cadence; it points to the dispatch preamble for both." (TL:42, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity set by the adversarial debate (debate confidence 0.8); raised by reviewer 3 R3-F3 (calibrated 0.87, was minor).
- **Default remediation:** scope TL:21 to the worker-session duties as SRC:59 does, and add to TL:52 "copied verbatim from `./source.md` section 2.3 'Brief layout', including its `worker_done` text" (R2-C:43).

### Deviation D-004: Tasks 1 and 5 demand "four" exact `guard refused:` texts; the spec gives three plus a case-3 prefix (should-fix; merged id M-04)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:41
- **Mapped tasklist item:** Task 1 and Task 5
- **Spec section:** source.md:60, source.md:306, source.md:312
- **Evidence:** cited lines SRC:60, SRC:306, SRC:312, TL:21, TL:36, TL:41, TL:87. Re-Read 2 of its citations, 0 dropped. Example: "...(WC-2 to WC-13 as listed, the four `guard refused:` reason texts, and the never-as-worker list naming `/sc:agent`, ...)" (TL:41, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line; inherits spec looseness; log SRC:306 as a spec erratum. Severity set by the adversarial debate (debate confidence 0.95); raised by reviewer 1 F2 (calibrated 0.83, was minor).
- **Default remediation:** in TL:41 and TL:87 require "the three exact `guard refused:` texts of section 2.1 plus, for case 3, the `guard refused:` prefix and the never-as-worker condition", and log SRC:306's "four ... reason texts" as a spec erratum.

### Deviation D-005: `tests/cli` is red between Task 1 and Task 3; Depends-on lines omit Task 3 (minor; merged id M-05)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:58
- **Mapped tasklist item:** Tasks 1, 3, 4 and 7
- **Spec section:** n/a
- **Evidence:** cited lines tests/cli/test_how_we_work_install.py:44, TL:58, TL:72, TL:77, TL:108, SKILL.md:79, SKILL.md:97. Re-Read 3 of its citations, 0 dropped. Example: "Depends on: Task 1" (TL:58, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity set by the adversarial debate (debate confidence 0.95); raised by reviewer 3 R3-F5 (calibrated 0.87, was minor); reviewer 1 F1 (calibrated 0.83, was blocking); reviewer 2 R2-4 (dependency half) (calibrated 0.87, was minor); reviewer 3 R3-F4 (dependency sentence) (calibrated 0.87, was minor).
- **Default remediation:** move the KNOWN_CORE_FILES edit into Task 1 (or state that `tests/cli` stays red until Task 3), and add Task 3 to the Depends-on lines of Tasks 4 and 7 as documentation.

### Deviation D-006: Task 8 does not carry the AC-0.6 `--source terminal` fallback into step 5 (minor; merged id M-06)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:122
- **Mapped tasklist item:** Task 8
- **Spec section:** source.md:291, source.md:303
- **Evidence:** cited lines SRC:291, SRC:303, TL:122, TL:127. Re-Read 1 of its citations, 0 dropped. Example: "AC-0.6 | Read one AC-0.4 transcript with `worker-read --source transcript --json` and record whether tool calls appear by name ... 7.2 step 5 follows that answer" (SRC:303, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity set by the adversarial debate (debate confidence 0.7); raised by reviewer 1 F4 (part b) (calibrated 0.83, was minor); reviewer 2 R2-2 (calibrated 0.87, was minor); reviewer 3 R3-F14 (calibrated 0.87, was minor).
- **Default remediation:** Task 8 reads `ac-0.6-transcript.md` first; if it says no, step 5 for all three runs uses `--source terminal` output and the gap is recorded in `ac-0.4-smoke.md`.

### Deviation D-007: No closing task: AC-C5 never recorded, common checks not re-run at phase end, no P0 report, no closing staging (minor; merged id M-07)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:15
- **Mapped tasklist item:** unmapped (no closing task exists)
- **Spec section:** source.md:216, source.md:241, source.md:271, source.md:396
- **Evidence:** cited lines SRC:216, SRC:241, SRC:271, SRC:396, TL:15, TL:22, TL:79. Re-Read 3 of its citations, 0 dropped. Example: "Each phase is independently useful... Later phases do not start until the earlier phase's checks in section 7 pass." (SRC:216, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity set by the adversarial debate (debate confidence 0.8); raised by reviewer 3 R3-F11 (calibrated 0.87, was minor); reviewer 1 F7 (calibrated 0.83, was minor); reviewer 2 R2-3 (calibrated 0.87, was minor); reviewer 2 R2-4 (phase-end half) (calibrated 0.87, was minor).
- **Default remediation:** add a final task that re-runs AC-C1, AC-C2, the AC-C3 comparison and AC-C4, records AC-C5 as run with an empty edit set, writes `artifacts/p0-phase-report.md` with one PASS or FAIL line per P0 check, and ends with a recorded `git add .dev/tasks`.

### Deviation D-008: Negative checks in Tasks 5 and 6 have no safe target (minor; merged id M-08)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:87
- **Mapped tasklist item:** Task 5 and Task 6
- **Spec section:** n/a
- **Evidence:** cited lines TL:87, TL:91, TL:97, TL:100, Makefile:171, Makefile:174. Re-Read 3 of its citations, 0 dropped. Example: "Create `tests/skills/test_worker_contract.py`. It reads `src/superclaude/core/WORKER-CONTRACT.md` and asserts that the file states each rule ..." (TL:87, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity set by the adversarial debate (debate confidence 0.7); raised by reviewer 3 R3-F8 (calibrated 0.87, was minor); reviewer 1 F5 (calibrated 0.83, was minor).
- **Default remediation:** the test takes the contract path and scan roots from fixtures that the negative checks monkeypatch to `tmp_path` copies, so no scratch file lands under `src/superclaude/`.

### Deviation D-009: AC-0.9's "refused under `--unattended`" class is empty at P0; `gh api` posts undefined (minor; merged id M-09)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:97
- **Mapped tasklist item:** Task 6
- **Spec section:** source.md:305
- **Evidence:** cited lines TL:97, SRC:305. Re-Read 1 of its citations, 0 dropped. Example: "AC-0.9 | Write-verb audit ... passes only when each hit is allowed by WC-9, refused under `--unattended`, or on an explicit allowlist with a reason" (SRC:305, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity set by the adversarial debate (debate confidence 0.9); raised by reviewer 3 R3-F13 (calibrated 0.87, was minor); reviewer 1 F6 (calibrated 0.83, was minor).
- **Default remediation:** at P0 every hit must be allowed by WC-9 or allowlisted with the phase that converts it; define `gh api` posts as `-X POST`, `--method POST`, `-f`, `-F`, `--input`; state that WC-9's no-git-state claim covers only classified hits.

### Deviation D-010: Task 5's test may assert rule labels, not rule substance (minor; merged id M-10)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:38
- **Mapped tasklist item:** Task 5
- **Spec section:** source.md:59, source.md:77
- **Evidence:** cited lines SRC:59, SRC:77, TL:38, TL:87, TL:91. Re-Read 1 of its citations, 0 dropped. Example: "Worker-session duties from section 2.2: WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats, stating only the IronClaude-specific rule and pointing to the dispatch preamble" (TL:38, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity set by the adversarial debate (debate confidence 0.85); raised by reviewer 2 R2-5 (calibrated 0.87, was minor); reviewer 3 R3-F9 (calibrated 0.87, was minor).
- **Default remediation:** Task 5 lists one load-bearing phrase per rule (WC-5 outcome mapping, WC-7 top level only, WC-3 ask only when the brief allows and the one-ask bound, WC-9's three grant conditions, the WC-4 error text, "at most 10", "at least 2", the guard line).

### Deviation D-011: Stale cite "lines 13-25" for KNOWN_CORE_FILES (minor; merged id M-11)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:60
- **Mapped tasklist item:** Task 3
- **Spec section:** source.md:59
- **Evidence:** cited lines TL:60, SRC:59, src/superclaude/cli/install_core.py:13, src/superclaude/cli/install_core.py:27. Re-Read 2 of its citations, 0 dropped. Example: "Add 'WORKER-CONTRACT.md' to `KNOWN_CORE_FILES` in `src/superclaude/cli/install_core.py` (lines 13-25 today)." (TL:60, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality defect (no taxonomy class applies); spec has the same stale range (SRC:59). Severity set by the adversarial debate (debate confidence 0.9); raised by reviewer 2 R2-6 (calibrated 0.87, was minor); reviewer 3 R3-F12 (calibrated 0.87, was minor); reviewer 1 F1 (recommendation) (calibrated 0.83, was blocking).
- **Default remediation:** cite `KNOWN_CORE_FILES` by symbol name, or as lines 13-27.

### Deviation D-012: Task 4 edits HOW-WE-WORK.md but runs only three test files (minor; merged id M-12)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:77
- **Mapped tasklist item:** Task 4
- **Spec section:** source.md:263
- **Evidence:** cited lines TL:77, SRC:263. Re-Read 1 of its citations, 0 dropped. Example: "...`uv run pytest tests/core/test_how_we_work_routing_table.py tests/core/test_claude_md_routing_block.py tests/cli/test_how_we_work_install.py -q` passes (AC-0.2)." (TL:77, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line; was regression, reclassed per R1-C:53; calibrator: count and test_help_command cite overstated (C:285). Severity set by the adversarial debate (debate confidence None); raised by reviewer 3 R3-F6 (calibrated 0.87, was minor).
- **Default remediation:** extend Task 4's AC to `uv run pytest tests/core tests/commands tests/recommend tests/cli -q`, compared with a baseline taken in Task 1.

### Deviation D-013: "after P0, none" in HOW-WE-WORK.md goes stale every phase (minor; merged id M-13)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:74
- **Mapped tasklist item:** Task 4
- **Spec section:** source.md:212
- **Evidence:** cited lines TL:74, SRC:212. Re-Read 1 of its citations, 0 dropped. Example: "SA-5 | `src/superclaude/` stays the source of truth ... The routing guide gains an Orca section without changing any existing routing row" (SRC:212, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity set by the adversarial debate (debate confidence None); raised by reviewer 3 R3-F7 (calibrated 0.87, was minor).
- **Default remediation:** say a command accepts `--unattended` only when its file has an `## Unattended mode` section, and point to `~/.claude/WORKER-CONTRACT.md` for the never-as-worker list.

### Deviation D-014: Brief template passes `--report-dir`, which no command accepts until P1 (minor; merged id M-14)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:49
- **Mapped tasklist item:** Task 2
- **Spec section:** source.md:143, source.md:152, source.md:221
- **Evidence:** cited lines TL:49, SRC:143, SRC:152, SRC:221. Re-Read 2 of its citations, 0 dropped. Example: "workflow | `--handoff none`; `--report-dir <dir>` (its `--output` is retired, `cmd/workflow.md:42`) | ..." (SRC:152, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity set by the adversarial debate (debate confidence None); raised by reviewer 3 R3-F10 (calibrated 0.87, was minor).
- **Default remediation:** the template marks `--report-dir` as "from P1".

### Deviation D-015: Task 7's `ls-remote` check and Task 8's coordinator check name no evidence (minor; merged id M-15)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:116
- **Mapped tasklist item:** Task 7 and Task 8
- **Spec section:** n/a
- **Evidence:** cited lines TL:116, TL:122, TL:26. Re-Read 1 of its citations, 0 dropped. Example: "...The coordinator for live checks is a session the person opened, never one started by `worker-start` (`./source.md` D5, non-goal 2). Worktrees are created by Orca..." (TL:26, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality defect (no taxonomy class applies). Severity set by the adversarial debate (debate confidence None); raised by reviewer 1 F8 (parts b and c) (calibrated 0.83, was minor).
- **Default remediation:** Task 7 saves the `git ls-remote origin` output to an artifact and checks that the Task 7 commit ID is absent from it; Task 8 states that the coordinator is the person-opened implement session and records that check.

## Unaddressed invariants from the adversarial merge

The merge's invariant probe (adversarial/adversarial/invariant-probe.md) left these items open. The advocates did not debate them, so they are not classified deviations. They stop the merge from counting as converged (`convergence_status: BLOCKED_BY_INVARIANTS`).

| ID | Severity | Category | Open assumption |
|---|---|---|---|
| INV-001 | HIGH | sufficiency_challenge | The merged Task 7 order ("ask both approvals up front, then install, write the record, commit") removes every instruction conflict in Task 7. |
| INV-002 | HIGH | sufficiency_challenge | Once Task 7 and the should-fixes are fixed, Task 8 can reach a passing AC-0.4, so P0 can pass (TL:15). |
| INV-003 | MEDIUM | sufficiency_challenge | The plan text added by the fix ("a QA failure after the commit is never retried") removes the `head-moved` exposure. |
| INV-004 | MEDIUM | guard_conditions | An "attended, never headless" Constraint line makes Task 7's two approval questions legal under the executor. |
| INV-005 | MEDIUM | state_variables | The `--force` effect statement the fix keeps (TL:25: "core files, rules, output styles and agents ... including `~/.claude/CLAUDE.md`") gives the owner an informed approval, and the install has a single outcome. |
| INV-006 | MEDIUM | interaction_effects | The merged cadence fix ("Task 8's AC requires at least one such run; if none is achieved, the report records the duty as unmet and P0 does not pass") has one meaning under the executor. |
| INV-007 | MEDIUM | guard_conditions | Every Task 7 and Task 8 AC can be shown true to a FINAL subagent that sees only files and logs. |
| INV-009 | LOW | guard_conditions | Tasks 8 and 9 use the right Orca executable and command timeouts for the session that runs them. |
| INV-013 | LOW | collection_boundaries | The AC-C3 baseline log has no failures, so the FINAL rule "a log cited on a task's latest complete line shows a failure at its outcome line" (qa:310) cannot fire on Task 1's evidence. |
| INV-015 | LOW | interaction_effects | The commit step in the fixed Task 7 cannot be changed or aborted by repository hooks. |

INV-002 detail: Task 8 cannot reach a passing AC-0.4 at P0 (step 3 needs a WC-4 contract). Cited lines: SRC:73, SRC:241, SRC:285, SRC:301, TL:122, TL:125. Re-Read 6 of its citations, 0 dropped. Example: "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `worker_status` under WC-5; its report path is the WC-4 contract path." (SRC:285, re-Read 2026-11-03). This is a candidate second blocking finding. It may be a spec defect rather than a plan defect, because no P0 command writes the WC-4 contract that step 3 checks.

INV-001 is folded into D-001's remediation: ask each approval just before its own action, as the plan's Constraint requires.

## Inferred requirements (Pass 2)

Pass 2 inferred 101 requirement rows from the spec (Pass 1 found no labelled requirement IDs). 25 match a plan task by word containment; most of the rest belong to phases P1-P4, which the plan defers on purpose (TL:19).

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | **Worker run**: a session that received an Orca preamble carrying a Task ID and a Dispatch ID. Only such a session may send lifecycle messages; a session the user started, inside or outside Orca, is an ordinary session | `source.md:54` | unmatched (best T1 0.3889) |
| INF-002 | The mode is selected only by the flag (decision D1, section 9: option (c) as amended). No command detects Orca, its preamble or its environment. | `source.md:55` | matched T1 (0.6667) |
| INF-003 | **Flag parse rule**: `--unattended` counts only as a standalone argument token outside any quoted argument. | `source.md:56` | unmatched (best T1 0.5455) |
| INF-004 | **Person-mode flags are refused**: under `--unattended`, every command refuses the flags that exist to involve a person: `--interactive`, `--format interactive` (explain), `--mode socratic` (business-panel), `--watch` (test), `--monitor 1` (pr-submit). | `source.md:57` | unmatched (best T1 0.381) |
| INF-005 | **Report directory**: the directory that holds the worker contract (WC-4). Under `--unattended` the brief passes exactly one: either the command's own existing directory-valued output flag (`--output <dir>` or `--output-dir <dir>`), or the new flag `--report-dir <dir>` (for a command without such a flag, or a brief that does not pass it). | `source.md:58` | matched T1 (0.6154) |
| INF-006 | **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. | `source.md:59` | unmatched (best T1 0.5833) |
| INF-007 | For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats) it states only the IronClaude-specific rule (outcome mapping from `worker_status`, top-level only, ask only when the brief allows it) and points to the dispatch preamble as the authority for Orca verb syntax and heartbeat cadence; it never copies them, because the preamble is issued per dispatch by the running Orca version (`CAPS:130`). | `source.md:59` | matched T1 (0.6216) |
| INF-008 | Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once. | `source.md:59` | matched T1 (0.625); deferred by tasklist |
| INF-009 | **Brief guard** (worker session, from P1): it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (see "Worker run"). Before invoking anything, the worker checks every `Command:` line of its brief (section 2.3, "Brief layout"), and only those lines. | `source.md:60` | unmatched (best T2 0.5312) |
| INF-010 | **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard` (section 4), plus `/sc:pr-submit` while the answer to D3 keeps it off workers. | `source.md:61` | matched T1 (0.7222) |
| INF-011 | **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). | `source.md:62` | unmatched (best T1 0.5714) |
| INF-012 | WC-1 \| **No prompt before the agent is ready.** Nothing in the launch path (wrapper, hook, startup command) may wait on a person before Claude's input box is ready. | `source.md:69` | unmatched (best T9 0.3529) |
| INF-013 | WC-2 \| **No person-blocking step in unattended mode.** Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer, and never says STOP AND WAIT. | `source.md:70` | unmatched (best T1 0.3) |
| INF-014 | WC-3 \| **Questions go to the coordinator, not to a local prompt.** The brief fixes the policy for a blocked gate; under `ask the coordinator` the worker applies the eligibility test below and makes no other choice. | `source.md:71` | unmatched (best T1 0.2381) |
| INF-015 | WC-4 \| **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<report-dir>/return-contract.yaml`, where `<report-dir>` is the one report directory the brief passes (section 2.1): either the command's own directory-valued `--output` / `--output-dir`, or `--report-dir`. | `source.md:72` | matched T1 (0.6538) |
| INF-016 | WC-5 \| **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. | `source.md:73` | unmatched (best T1 0.5) |
| INF-017 | WC-6 \| **Every retry is a new Task.** A Task's brief cannot change after creation (`task-update` changes only `--status` and `--result`, `task-update --help` line 3), and a re-run into the first attempt's directories could mix its files with the retry's. | `source.md:74` | unmatched (best T2 0.4231) |
| INF-018 | WC-7 \| **Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. | `source.md:75` | matched T8 (0.6875) |
| INF-019 | WC-8 \| **No Orca fan-out from inside a command.** A command never calls `worker-start`, `dispatch` or `task-create`. | `source.md:76` | matched T8 (0.6) |
| INF-020 | WC-9 \| **No outward action from a worker; local commits only by grant.** Under `--unattended` every outward default (push, merge into a shared branch, PR, GitHub post, install on a shared or real target, VM, paid external run) is off, and no brief can turn it on (D4); the coordinator performs those actions (section 2.3). | `source.md:77` | unmatched (best T2 0.3611) |
| INF-021 | WC-10 \| **Liveness during long waits.** The worker sends heartbeats at the cadence its preamble sets (5 minutes in current preambles). | `source.md:78` | unmatched (best T1 0.4) |
| INF-022 | WC-11 \| **Parallel-safe writes.** Two workers in one worktree must never write the same file. | `source.md:79` | unmatched (best T8 0.4545) |
| INF-023 | WC-12 \| **Coordinator follow-ups are pulled, not pushed.** The worker runs `check` at natural checkpoints and once before `worker_done`; if `check` returns `consumer_fenced` it stops without sending `worker_done`. | `source.md:80` | unmatched (best T8 0.3889) |
| INF-024 | WC-13 \| **No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. | `source.md:81` | matched T9 (0.7391) |
| INF-025 | For each Task the coordinator's brief states: the exact command line, including `--unattended` where the command accepts it at this phase, and every flag section 3 lists as required, written as a `Command:` line in the layout below; the report directory, unique to this Task, so the contract path is known before dispatch (WC-4, WC-11); the blocked-gate policy line, `On a blocked gate: report blocked` or `On a blocked gate: ask the coordinator` (WC-3) | `source.md:84` | unmatched (best T1 0.4615) |
| INF-026 | **Brief layout.** The brief puts the preamble-facing instructions and the guard line before the commands, and gives each command its own labelled `Command:` line in run order (for example `Command: /sc:load ...`, then the converted command), so the Task text never starts with `/sc:`. | `source.md:86` | unmatched (best T2 0.5) |
| INF-027 | Guard line: `Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".` | `source.md:86` | unmatched (best T2 0.45) |
| INF-028 | **Feature worktree and child worktrees.** Every worktree is created by Orca at Orca's default location, never with raw `git worktree add` and never under `.dev/worktrees/`. | `source.md:88` | matched T2 (0.7333) |
| INF-029 | **Git and GitHub ownership.** The coordinator performs every git and GitHub outward action, and every install, VM or paid run, in its own conversation, only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation (`sk/sc-post-release-protocol/SKILL.md:351`). | `source.md:90` | unmatched (best T2 0.2857) |
| INF-030 | Every such action targets `IronbellyOrg/IronClaude`: never the SuperClaude upstream, and never through Orca's issue or PR linking while Orca records the project as the upstream. | `source.md:90` | unmatched (best T4 0.3125) |
| INF-031 | Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this. | `source.md:90` | unmatched (best T7 0.3) |
| INF-032 | **Reading a result before anything depends on it.** Orca settles a Task on any valid `worker_done` (`CAPS:77`) and does not start ready Tasks itself (`CAPS:92`), so the coordinator decides what runs next: | `source.md:92` | unmatched (best T2 0.4583) |
| INF-033 | `partial`: dependents do not start until the coordinator has read the contract's `report_path` and recorded, in its own run notes, whether the partial deliverable is usable; an unusable one is handled like `failed`. | `source.md:94` | unmatched (best T8 0.4) |
| INF-034 | `failed` or `blocked`: dependents do not start; the coordinator retries per WC-6, answers per the example below, or reports the failure to the person. | `source.md:95` | unmatched (best T8 0.3077) |
| INF-035 | No contract, and a `worker_done --outcome failed` body that starts `guard refused:`: a brief-guard refusal; nothing ran. The coordinator fixes the brief in a new Task (WC-6), never re-creates it unchanged, and allows at most 2 brief fixes for the same work (3 attempts); a third refusal escalates to the person. | `source.md:96` | unmatched (best T2 0.3333) |
| INF-036 | Every dependent Task is created only after all its inputs have settled and been admitted under the bullets above, with `--deps` naming the Tasks that actually succeeded (an original Task or its replacement). | `source.md:97` | unmatched (best T2 0.3889) |
| INF-037 | The coordinator starts only Tasks it created itself. A ready Task it did not create is not started; it is reported to the person with its spec text. | `source.md:98` | unmatched (best T2 0.4706) |
| INF-038 | *Freeze.* A plan is frozen when its latest implement contract is `blocked`, or `failed` with any STOP code other than `E-RESUME-NEEDED`. | `source.md:101` | unmatched (best T1 0.2857) |
| INF-039 | *Lifting the freeze.* The freeze lifts only when the person's explicit hand-back is recorded in the coordinator's run notes **and** the ledger shows the matching state: | `source.md:107` | unmatched (best T2 0.3333) |
| INF-040 | *Check before a resume Task under (c).* The coordinator reads the ledger and the worktree, never edits either, and dispatches only if all of the following hold. | `source.md:112` | unmatched (best T2 0.4) |
| INF-041 | *Placement.* The resume Task starts in the halted worktree by selector (`worker-start --worktree path:<absolute worktree path>`), never in a new or child worktree. | `source.md:120` | unmatched (best T2 0.4615) |
| INF-042 | The coordinator plans N no larger than the merge command's maximum of 10 inputs (`cmd/adversarial.md:15`); a re-run replaces its input rather than adding one, so the admitted count never exceeds 10. Create the merge Task only when at least 2 inputs are admitted, and list every dropped input and its reason in its brief. | `source.md:122` | unmatched (best T2 0.3529) |
| INF-043 | These run as workers now only if the brief uses the stated flags and avoids the inputs that trigger a gate; the worker reports the named file until Phase 1 adds the contract. | `source.md:137` | unmatched (best T2 0.4286) |
| INF-044 | Fix its own contract filename to `<output>/adversarial/return-contract.yaml` (P1); the worker contract is `<output>/return-contract.yaml` and lists that file in `artifacts` (WC-4) | `source.md:141` | matched T8 (0.6429); deferred by tasklist |
| INF-045 | Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt (P2) | `source.md:148` | unmatched (best T4 0.3846); deferred by tasklist |
| INF-046 | on `E-HALT-QA` or `E-NO-RULING`, stop with the halt recorded in the ledger and the contract as blocked, carrying the Ruling question, the STOP code in `reason` | `source.md:169` | unmatched (best T1 0.1538); deferred by tasklist |
| INF-047 | the "Resume? [Y/n]" prompt is replaced by the explicit resume flag (resume only when passed); `--interactive` refused | `source.md:178` | unmatched (best T1 0.2727); deferred by tasklist |
| INF-048 | Without `--unattended`, every prompt, approval gate, default flag value, output path and outward default stays as it is today, including the auggie-review PR posting default and every `AskUserQuestion`. | `source.md:208` | unmatched (best T8 0.2632) |
| INF-049 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. | `source.md:209` | unmatched (best T8 0.5833) |
| INF-050 | The new contract file and report files are written only in unattended mode or when the caller passes the new output flag. | `source.md:210` | matched T1 (0.6923); deferred by tasklist |
| INF-051 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. | `source.md:211` | unmatched (best T5 0.4); deferred by tasklist |
| INF-052 | `src/superclaude/` stays the source of truth; `.claude/` copies come from `make sync-dev` and are never staged. The routing guide gains an Orca section without changing any existing routing row, and its two mirrored copies are updated as the repo requires. | `source.md:212` | unmatched (best T4 0.5556) |
| INF-053 | The existing headless rule of `/sc:reflect` under `claude --print` keeps working exactly as today; `--unattended` reuses it and does not replace it. | `source.md:213` | unmatched (best T1 0.3125); deferred by tasklist |
| INF-054 | Each phase is independently useful and leaves standalone behaviour unchanged (section 5). Later phases do not start until the earlier phase's checks in section 7 pass. | `source.md:216` | unmatched (best T6 0.3158) |
| INF-055 | Write `src/superclaude/core/WORKER-CONTRACT.md` (the contents section 2.1 assigns to it, plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1), and confirm the two Orca behaviours later checks rely on (AC-0.5, AC-0.6). | `source.md:220` | unmatched (best T1 0.3774) |
| INF-056 | The WC-4 contract, the report-directory rule, the flag parse rule and the person-mode refusal (section 2.1) for the P1 commands only; `--unattended` is added to a command only in the phase that converts its gates, so no command accepts the flag while it can still prompt; output flags for commands that lack one; the small fixes to ready commands. | `source.md:221` | unmatched (best T1 0.5312); deferred by tasklist |
| INF-057 | Each default-on gate resolves per its section 3 row; WC-10 wait splitting for cli-eval. | `source.md:222` | unmatched (best T1 0.3333); deferred by tasklist |
| INF-058 | Reconcile command and skill where they disagree; make memory writes parallel-safe. | `source.md:223` | unmatched (best T4 0.2); deferred by tasklist |
| INF-059 | Apply the approved D2-D4 outcomes: the implement halt path, post-release with every outward step off (D4), pr-submit as a worker only if D3 (b) is chosen. | `source.md:224` | unmatched (best T2 0.2778); deferred by tasklist |
| INF-060 | none (smoke runs use each command's existing flags) | `source.md:230` | matched T8 (0.875) |
| INF-061 | Each phase is one written plan executed under the repo's level-3 route (`/sc:workflow`, then `/sc:implement` when execution is requested), because each touches more than one source file (hard limit at `src/superclaude/core/CLAUDE.md:66` and `src/superclaude/core/HOW-WE-WORK.md:22`). | `source.md:238` | unmatched (best T1 0.3704) |
| INF-062 | **AC-C1** (SA-2, WC-8). Pass: prints nothing. | `source.md:244` | unmatched (best T4 0.5) |
| INF-063 | **AC-C2** (SA-5). Pass: exits 0. | `source.md:256` | matched T4 (0.8) |
| INF-064 | **AC-C3**. Before the phase starts, save the output below as the baseline; after the phase, run it again. | `source.md:261` | matched T1 (0.6667) |
| INF-065 | **AC-C4** (`CLAUDE.md:16`). Pass: prints nothing. | `source.md:266` | unmatched (best T4 0.5) |
| INF-066 | **AC-C5** (SA-4: edits are additive). Run for every command file the phase edits without a named defect fix. | `source.md:271` | unmatched (best T2 0.4167) |
| INF-067 | **AC-C6** (D5, non-goal 2). Pass: prints exactly one line per Orca profile and every line is `"nestedWorkerMaxDepth":1`. | `source.md:276` | unmatched (best T9 0.5714) |
| INF-068 | For each command under test, the coordinator runs the steps below with one worker in a fresh disposable worktree that holds the phase's edits, so step 6 can attribute every change to the worker under test (WC-11 allows sharing a worktree in normal use; the check does not). | `source.md:282` | matched T8 (0.6154) |
| INF-069 | AC-0.1 \| `uv run python -c "from superclaude.cli.install_core import KNOWN_CORE_FILES; assert 'WORKER-CONTRACT.md' in KNOWN_CORE_FILES"`, then the install check in the block below the table, then `uv run pytest tests/skills/test_worker_contract.py -q`, which asserts the file states each rule section 2.1 assigns to it and the section 2.3 dependent-creation and fan-in rules | `source.md:298` | matched T5 (0.697) |
| INF-070 | AC-0.2 \| `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and the level-table test the repo already runs (`CLAUDE.md:334`) \| identical; tests pass | `source.md:299` | matched T4 (0.65) |
| INF-071 | AC-0.3 \| The deletions check in the block below the table, on `src/superclaude/core/HOW-WE-WORK.md` \| prints nothing: no existing routing line removed (SA-5) | `source.md:300` | matched T4 (0.7647) |
| INF-072 | AC-0.4 \| 7.2 live check on `/sc:troubleshoot "<real symptom>"` (no `--fix`, no `--depth deep`), `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | `source.md:301` | matched T8 (0.9091) |
| INF-073 | AC-0.5 \| WC-1: `worker-start` with the user's normal launch setup (the same shell wrapper, hooks and startup command a person's sessions use), timed \| exit 0, `state: ready`, and the start returns in under 45 s. | `source.md:302` | unmatched (best T8 0.56) |
| INF-074 | AC-0.6 \| Read one AC-0.4 transcript with `worker-read --source transcript --json` and record whether tool calls appear by name (for example `Bash`, `Agent`, `AskUserQuestion`) | `source.md:303` | matched T8 (0.7647) |
| INF-075 | AC-0.7 \| Read-only trace in Orca's installed code, starting from the AC-0.7 block below the table, of (1) which calls check nesting depth: `worker-start`, `dispatch`, `task-create`, low-level dispatch, `worktree create --agent`, `agent launch`; and (2) what depth Orca gives a session the person opens (expected 0, `CAPS:97`). | `source.md:304` | matched T9 (0.7941) |
| INF-076 | AC-0.9 \| Write-verb audit: `test_worker_contract.py` scans the skills, commands and agents under `src/superclaude/` (the installed primitives' source) for git and gh write verbs (`add`, `commit`, `push`, `merge`, `worktree add/remove`, `stash`, `update-ref`, `gh pr`, `gh api` posts) | `source.md:305` | matched T6 (0.8571) |
| INF-077 | AC-1.1 \| `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command listed for P1 in the section 6 table of commands accepting `--unattended` has a `## Unattended mode` section naming `return-contract.yaml`, `~/.claude/WORKER-CONTRACT.md` and its report directory flag, and that no other command has one yet (load, pr-submit under D3 (a), the section 4 commands, and the P2-P4 commands until their phase). | `source.md:306` | unmatched (best T1 0.5641); deferred by tasklist |
| INF-078 | AC-1.2 \| 7.2 live check on each P1 command with `--unattended` and its report directory (`--output <dir>` or `--report-dir <dir>`) | `source.md:307` | matched T8 (0.7143); deferred by tasklist |
| INF-079 | AC-1.3 \| For two P1 commands, run once with no `--unattended` and no new output flag, then `git status --short`. | `source.md:308` | unmatched (best T1 0.5); deferred by tasklist |
| INF-080 | AC-1.4 \| `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | `source.md:309` | unmatched (best T1 0.25); deferred by tasklist |
| INF-081 | AC-1.5 \| WC-4 missing report directory: `/sc:analyze src/ --unattended` with neither `--output` nor `--report-dir`, as a 7.2 live check whose steps 3-4 are replaced by this row's conditions | `source.md:310` | unmatched (best T1 0.4286); deferred by tasklist |
| INF-082 | AC-1.6 \| Person-mode refusal (section 2.1): `/sc:test --watch --unattended --report-dir <dir>` as a 7.2 live check | `source.md:311` | unmatched (best T1 0.5714); deferred by tasklist |
| INF-083 | AC-1.7 \| Brief-guard refusals (section 2.1), one 7.2 live check per case, with steps 3-4 replaced by this row's conditions. | `source.md:312` | unmatched (best T8 0.375); deferred by tasklist |
| INF-084 | AC-1.8 \| WC-9 commit grant: a commit-authorized worker started with `--worktree new-child --base-branch <feature branch>`, with the four records of AC-4.2 taken before dispatch and after the run | `source.md:313` | unmatched (best T7 0.3333); deferred by tasklist |
| INF-085 | AC-2.1 \| `test_worker_contract.py` gains one assertion per gate listed in the section 3 row, for example the auggie-review section names both `--no-post-pr` and `--no-remediation-offer`; for cli-eval, the eval wait step names a single-wait limit of at most 240 s (WC-10) | `source.md:314` | unmatched (best T5 0.2308); deferred by tasklist |
| INF-086 | AC-2.2 \| Gate-trigger run per P2 command: a 7.2 live check whose brief carries `On a blocked gate: report blocked` and input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file> --report-dir <dir>` with a bare topic; `/sc:cli-eval run --unattended --report-dir <dir>` with no `--suite`). | `source.md:315` | unmatched (best T8 0.4); deferred by tasklist |
| INF-087 | AC-2.3 \| Happy-path run per P2 command with every required flag in the brief \| 7.2 passes with `--outcome succeeded` | `source.md:316` | unmatched (best T8 0.4615); deferred by tasklist |
| INF-088 | AC-2.4 \| `/sc:auggie-review <PR> --unattended --output-dir <dir>` on a fork PR; before and after, `gh api repos/IronbellyOrg/IronClaude/pulls/<PR>/reviews --jq length` and `.../pulls/<PR>/comments --jq length` | `source.md:317` | unmatched (best T6 0.2778); deferred by tasklist |
| INF-089 | AC-2.5 \| A person runs `/sc:cli-eval run` and `/sc:cleanup <dir> --interactive` in a plain session (manual check) | `source.md:318` | unmatched (best T8 0.4615); deferred by tasklist |
| INF-090 | AC-2.6 \| WC-3 and WC-6, the section 2.3 worked example run live: T1 hits the tdd gate and reports blocked; the coordinator creates T2 with the answer and new directories; then a third Task T3 with the same bare-topic input and `On a blocked gate: ask the coordinator`, where the coordinator answers the `ask`. | `source.md:319` | unmatched (best T2 0.2667); deferred by tasklist |
| INF-091 | AC-2.9 \| Brief guard, discriminating run: `/sc:tdd "auth" --output <file> --report-dir <dir>` (bare topic, no `--unattended`) as a 7.2 live check, with steps 3-4 replaced by this row's conditions | `source.md:320` | unmatched (best T8 0.44); deferred by tasklist |
| INF-092 | AC-2.8 \| `--unattended` parse rule (section 2.1): `/sc:troubleshoot "the worker ignores --unattended"` run by a person in a plain session (manual check) | `source.md:321` | unmatched (best T1 0.5); deferred by tasklist |
| INF-093 | AC-3.1 \| `test_worker_contract.py` asserts that `cmd/validate-roadmap.md` and `sk/sc-validate-roadmap-protocol/SKILL.md` name the same report filename | `source.md:322` | unmatched (best T5 0.1667); deferred by tasklist |
| INF-094 | AC-3.2 \| `/sc:roadmap <spec> --unattended --output <dir>` with an existing `<dir>/.session-memory.md` and no resume flag \| starts fresh, no `[Y/n]` in the transcript, contract written | `source.md:323` | unmatched (best T1 0.3684); deferred by tasklist |
| INF-095 | AC-3.3 \| `test -d` on the default target in `cmd/validate-tests.md`; `/sc:validate-tests --report <path> --unattended --report-dir <dir>` | `source.md:324` | unmatched (best T1 0.3571); deferred by tasklist |
| INF-096 | AC-3.4 \| Two workers in one worktree each run `/sc:save --unattended --report-dir <own dir>` | `source.md:325` | matched T1 (0.6154); deferred by tasklist |
| INF-097 | AC-4.1 \| `/sc:implement <plan> --unattended --report-dir <dir>` with the brief line `On a blocked gate: ask the coordinator` (the policy most likely to relay a Ruling), on a plan with one acceptance criterion that cannot be met | `source.md:326` | unmatched (best T1 0.3043); deferred by tasklist |
| INF-098 | AC-4.2 \| `/sc:post-release <version> --unattended --output <dir>` with no authorization flags | `source.md:327` | unmatched (best T1 0.4); deferred by tasklist |
| INF-099 | AC-4.3 \| If D3 allows pr-submit as a worker: one 7.2 run on a scratch fork PR; `worker-read` transcript inspected for Bash waits | `source.md:328` | unmatched (best T8 0.375); deferred by tasklist |
| INF-100 | AC-4.4 \| (1) Before the coordinator ever launches a pr-submit session: on each Chat UI setting the user uses (chat, terminal) | `source.md:329` | unmatched (best T8 0.3571); deferred by tasklist |
| INF-101 | AC-4.5 \| Two workers in one feature: one `/sc:implement` task whose rollback is forced, in a child worktree, and one report-only worker in the parent | `source.md:330` | unmatched (best T8 0.4375); deferred by tasklist |

Postscript: 40 of the 101 rows were in the re-Read sample; all 40 quotes matched their cited lines, and 0 rows were dropped. `coverage_pct_union` (0.2475), `unmapped_requirements_union` and `S_dev_density` (0.7525) need no recompute.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 180` = 0.00

## Recommendations

### Recommendation R-001: Fix M-01 in Task 7

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** rewrite TL:110 as one order with each approval asked just before its own action (INV-001): install approval, install, write `t7-approvals.md` without the ID, commit approval, stage the listed P0 paths (C:77-81) plus `.dev/tasks` and commit with `git commit --only -- <paths> .dev/tasks` as the last product action, then append the commit ID and stage it; a refusal or any QA failure after the commit ends in a halt for the person's Ruling and is never retried; add a Constraint line that the run is attended and never headless.
- **Verifier:** re-Read the edited plan lines against TL:25, TL:110, TL:113, SRC:282, retry.md:41, retry.md:44, qa.md:52, qa.md:61, qa.md:288, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-01 is not raised again.
- **Linked deviation(s):** D-001
- **Priority:** P0

### Recommendation R-016: Decide how AC-0.4 step 3 can pass at P0 (spec and plan)

- **File:** n/a (spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` and its copy `source.md`, plus Task 8 of the plan)
- **Change:** (probe's repair, not adjudicated) Task 8 states a P0 version of step 3, with the outcome taken from the command's own status through the WC-4 mapping (SRC:72) and the report path equal to the existing report file, and puts it in each brief so the worker does not apply WC-5's no-contract rule; log SRC:301 as a spec gap.
- **Verifier:** re-Read source.md:285 and source.md:301 against the revised spec, and confirm Task 8's acceptance criteria name a step-3 pass condition that a P0 command can meet.
- **Linked deviation(s):** none (unaddressed invariant INV-002, not adjudicated by the debate)
- **Priority:** P0

### Recommendation R-002: Fix M-02 in Task 8

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** Task 8's AC requires `ac-0.4-smoke.md` to name one checked run whose top-level session, outside Agent-tool calls, lasted longer than the preamble cadence, with start and end times; if none qualifies, add or extend a run, and if none is achieved the report records the duty as unmet and P0 does not pass (R2-C:69).
- **Verifier:** re-Read the edited plan lines against SRC:291, SRC:78, TL:15, TL:122, TL:124-128, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-02 is not raised again.
- **Linked deviation(s):** D-002
- **Priority:** P1

### Recommendation R-003: Fix M-03 in Constraints (TL:21) and Task 2 (TL:52)

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** scope TL:21 to the worker-session duties as SRC:59 does, and add to TL:52 "copied verbatim from `./source.md` section 2.3 'Brief layout', including its `worker_done` text" (R2-C:43).
- **Verifier:** re-Read the edited plan lines against TL:21, TL:42, TL:52, TL:87, SRC:59, SRC:86, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-03 is not raised again.
- **Linked deviation(s):** D-003
- **Priority:** P1

### Recommendation R-004: Fix M-04 in Task 1 and Task 5

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** in TL:41 and TL:87 require "the three exact `guard refused:` texts of section 2.1 plus, for case 3, the `guard refused:` prefix and the never-as-worker condition", and log SRC:306's "four ... reason texts" as a spec erratum.
- **Verifier:** re-Read the edited plan lines against SRC:60, SRC:306, SRC:312, TL:21, TL:36, TL:41, TL:87, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-04 is not raised again.
- **Linked deviation(s):** D-004
- **Priority:** P1

### Recommendation R-005: Fix M-05 in Tasks 1, 3, 4 and 7

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** move the KNOWN_CORE_FILES edit into Task 1 (or state that `tests/cli` stays red until Task 3), and add Task 3 to the Depends-on lines of Tasks 4 and 7 as documentation.
- **Verifier:** re-Read the edited plan lines against tests/cli/test_how_we_work_install.py:44, TL:58, TL:72, TL:77, TL:108, SKILL.md:79, SKILL.md:97, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-05 is not raised again.
- **Linked deviation(s):** D-005
- **Priority:** P2

### Recommendation R-006: Fix M-06 in Task 8

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** Task 8 reads `ac-0.6-transcript.md` first; if it says no, step 5 for all three runs uses `--source terminal` output and the gap is recorded in `ac-0.4-smoke.md`.
- **Verifier:** re-Read the edited plan lines against SRC:291, SRC:303, TL:122, TL:127, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-06 is not raised again.
- **Linked deviation(s):** D-006
- **Priority:** P2

### Recommendation R-007: Fix M-07 in unmapped (no closing task exists)

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** add a final task that re-runs AC-C1, AC-C2, the AC-C3 comparison and AC-C4, records AC-C5 as run with an empty edit set, writes `artifacts/p0-phase-report.md` with one PASS or FAIL line per P0 check, and ends with a recorded `git add .dev/tasks`.
- **Verifier:** re-Read the edited plan lines against SRC:216, SRC:241, SRC:271, SRC:396, TL:15, TL:22, TL:79, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-07 is not raised again.
- **Linked deviation(s):** D-007
- **Priority:** P2

### Recommendation R-008: Fix M-08 in Task 5 and Task 6

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** the test takes the contract path and scan roots from fixtures that the negative checks monkeypatch to `tmp_path` copies, so no scratch file lands under `src/superclaude/`.
- **Verifier:** re-Read the edited plan lines against TL:87, TL:91, TL:97, TL:100, Makefile:171, Makefile:174, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-08 is not raised again.
- **Linked deviation(s):** D-008
- **Priority:** P2

### Recommendation R-009: Fix M-09 in Task 6

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** at P0 every hit must be allowed by WC-9 or allowlisted with the phase that converts it; define `gh api` posts as `-X POST`, `--method POST`, `-f`, `-F`, `--input`; state that WC-9's no-git-state claim covers only classified hits.
- **Verifier:** re-Read the edited plan lines against TL:97, SRC:305, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-09 is not raised again.
- **Linked deviation(s):** D-009
- **Priority:** P2

### Recommendation R-010: Fix M-10 in Task 5

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** Task 5 lists one load-bearing phrase per rule (WC-5 outcome mapping, WC-7 top level only, WC-3 ask only when the brief allows and the one-ask bound, WC-9's three grant conditions, the WC-4 error text, "at most 10", "at least 2", the guard line).
- **Verifier:** re-Read the edited plan lines against SRC:59, SRC:77, TL:38, TL:87, TL:91, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-10 is not raised again.
- **Linked deviation(s):** D-010
- **Priority:** P2

### Recommendation R-011: Fix M-11 in Task 3

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** cite `KNOWN_CORE_FILES` by symbol name, or as lines 13-27.
- **Verifier:** re-Read the edited plan lines against TL:60, SRC:59, src/superclaude/cli/install_core.py:13, src/superclaude/cli/install_core.py:27, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-11 is not raised again.
- **Linked deviation(s):** D-011
- **Priority:** P2

### Recommendation R-012: Fix M-12 in Task 4

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** extend Task 4's AC to `uv run pytest tests/core tests/commands tests/recommend tests/cli -q`, compared with a baseline taken in Task 1.
- **Verifier:** re-Read the edited plan lines against TL:77, SRC:263, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-12 is not raised again.
- **Linked deviation(s):** D-012
- **Priority:** P2

### Recommendation R-013: Fix M-13 in Task 4

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** say a command accepts `--unattended` only when its file has an `## Unattended mode` section, and point to `~/.claude/WORKER-CONTRACT.md` for the never-as-worker list.
- **Verifier:** re-Read the edited plan lines against TL:74, SRC:212, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-13 is not raised again.
- **Linked deviation(s):** D-013
- **Priority:** P2

### Recommendation R-014: Fix M-14 in Task 2

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** the template marks `--report-dir` as "from P1".
- **Verifier:** re-Read the edited plan lines against TL:49, SRC:143, SRC:152, SRC:221, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-14 is not raised again.
- **Linked deviation(s):** D-014
- **Priority:** P2

### Recommendation R-015: Fix M-15 in Task 7 and Task 8

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md
- **Change:** Task 7 saves the `git ls-remote origin` output to an artifact and checks that the Task 7 commit ID is absent from it; Task 8 states that the coordinator is the person-opened implement session and records that check.
- **Verifier:** re-Read the edited plan lines against TL:116, TL:122, TL:26, then re-run `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` on the revised plan and confirm M-15 is not raised again.
- **Linked deviation(s):** D-015
- **Priority:** P2
