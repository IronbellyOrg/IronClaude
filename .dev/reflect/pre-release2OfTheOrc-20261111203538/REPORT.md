# Reflect report (UC-1, pre-execution): Release 2 plan vs its source

Plan: `.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/TASK-WF-release2OfTheOrc-20261111-203306.md`
Source: `.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/source.md`
Mode: pre. Tier reached: 1 (single agent). Status: partial (reduced pass, see Process note).

## Process note (declared reduction)

This was a Tier-1 pass done inline by the planning session. The `confidence-calibrator` and `evidence-validator` agents, the reuse-auditor and the codegraph chain were NOT run; calibration is `inline-fallback` and citation re-validation was done by the author re-reading the cited files. So `evidence_validator_ran: false`, `status: partial`, `degraded_components: [evidence-validator, confidence-calibrator]`. The source has no requirement IDs, so Pass 1 found 0 labelled rows and Pass 2 (inference) produced the rows below, each quote-pinned to the source lines.

## Coverage matrix (Pass 2, all rows `source: inferred`)

| Row | Quote (source.md) | Task(s) | Result |
|---|---|---|---|
| INF-001 | "gate-text rewrite tasks (release-gates.md ...)" | Task 1 | covered |
| INF-002 | "... unverified-register.md ..." | Task 2 | covered |
| INF-003 | "... prd.md:106 per report 8.1" | Task 3 | covered |
| INF-004 | "fake-runner tests for the new argv" | Task 6 | covered |
| INF-005 | "`consumer_fenced` and `no_active_terminal` responses" | Task 6, Task 9, Task 10 | covered |
| INF-006 | "the 100-row cap fixture" | Task 14 | covered |
| INF-007 | "the T51 quiet-scope test" | Task 15 | covered |
| INF-008 | "recorded redacted samples of success, missing, stale, contradictory" | Task 13 | covered |
| INF-009 | "acceptance criteria per task" | all 18 tasks | covered |
| INF-010 | "One named Run only ... Never call `run-use`" | Task 4, 6, 12 | covered |
| INF-011 | "Every read passes `--types question`" | Task 6, 14 | covered |
| INF-012 | "observer-side retention" (handled question looks fresh) | Task 8 | covered |
| INF-013 | "100-row cap is disclosed in the UI" with the label | Task 10, 14 | covered |
| INF-014 | "Question identity is `message.id` ... keep it labelled UNVERIFIED for other Runs" | Task 7, 1, 2 | covered in docs; not shown in the panel (see finding F-1) |
| INF-015 | "gated risks with a named verification task" (Q-1, Q-2, rate) | Task 2, 16, 17 | covered |
| INF-016 | decision 8 label "coordinator questions", not "human" | Task 3, 10 | covered |
| INF-017 | decision 6 "never `run-use`", read permission for one named Run | Task 12, 17 | covered |

coverage_pct (parsed) = null (no labelled IDs); coverage_pct_union = 17/17 = 1.00; unmapped_requirements_union = []. `coverage_undefined: true` for the parsed pass, `coverage_degraded: parsed-sparse` (inferred_count 17 > parsed_count 0), which forbids a Tier-1 stop under the rubric; the run was kept at Tier 1 only because this is an advisory pass on a planning artifact, recorded as an override (`--tier 1` equivalent) with this WARN.

## Findings (advisory; the plan is not edited from them)

- F-1 (minor, INF-014): "UNVERIFIED for other Runs" is recorded in the gate docs (Tasks 1, 2) but no task makes the panel show it. If the owner wants it visible, Task 10 needs one more line in the panel.
- F-2 (minor, Task 3): the plan lists prd.md lines 106, 243 to 253, 425 and 471 (each re-read: 425 is OQ-7, 471 is owner item 8). It misses the row at prd.md:492 (`U4 | Whether a --types value identifies a human question | Open owner decision 8`). The task says "verify the line before editing", so the executor should also update line 492.
- F-3 (risk, Task 16): needs a plain Orca terminal that holds no Run; an executor agent may not be able to get one. The task has an honest BLOCKED verdict, so Task 18 then stays blocked. Expected, not a defect.
- F-4 (risk, Task 17 and 18): both are gated on owner input (the Run name; the owner-written pass record). The plan ends with the live read off, which is the intended safe state.
- F-5 (minor, Task 9): the `FixtureSource.read_questions` wording ("`not-found`-style `no-question-fixture`") is loose; the executor should pick one new code and add it to `CODES`.
- F-6 (judgement call, Task 10): the plan lists questions without per-question selection and keeps `m` on worker rows. That narrows the spec's `marked looked / not marked` sub-line; the plan states this in Constraints.

## Claims checked against disk (re-Read by the author)

- adapter.py: `FORBIDDEN_PREFIXES`, `WORKER_LIST_TEMPLATE`, `MAX_CALLS_PER_CYCLE = 5`, `LiveSource.read_pages` exist as the plan describes.
- collector.py: `Collector(..., run_id=...)`, `CycleSource.read_pages(clock, budget_deadline, run_id)`, `CycleResult` frozen dataclass exist.
- view.py: `GAP_NOTICE`, `LEDGER_TITLE`, `MESSAGES_CELL` exist; commands.py has `Options.run_id` and `--run`.
- tests/observe/conftest.py: `argv_allowed`, `FakeRunner`, `make_rows` exist; test_golden_contract.py uses `GOLDEN` and `SENSITIVE`.
- Probe shapes: `result.messages`, `count`, `acknowledged`, `runId`; error codes `consumer_fenced` (exit 1) and `no_active_terminal` confirmed from the recorded evidence files 01, 03, 14, 17, 24.

## Verdict

No blocking defect. Plan covers every inferred source requirement (union coverage 1.00). Status `partial` only because validators were not run.
