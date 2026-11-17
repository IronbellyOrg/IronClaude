# Reflect pre-execution report (UC-1)

```yaml
contract_version: 1.8.0
status: partial            # Tier 2 required by the rubric but not run (see Tier note)
mode: pre
tier_reached: 1
confidence_calibrated: 0.80   # inline-fallback calibration, not blind (see Tier note)
citations_total: 3
citations_revalidated: 3
citations_dropped: 0
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Plan: `.dev/tasks/to-do/TASK-WF-removeThePrdComm-20261117-200005/TASK-WF-removeThePrdComm-20261117-200005.md` against `./source.md` (advisory; the plan was not edited).

## Tier note (read this first)

The source is one paragraph with no labeled requirement IDs, so Pass 1 found 0 requirements and Pass 2 inferred 5. Rule 1B.2b (inferred greater than parsed) forbids stopping at Tier 1, so the rubric routes to Tier 2. Tier 2 needs several reviewer sub-agents on different model classes plus a blind calibrator and the adversarial merge. This session runs under a standing instruction not to start sub-agents, so only Tier 1 ran, with the calibration done inline (marker `calibration: inline-fallback`) and the evidence re-read done by the orchestrator (marker `evidence_validator_ran: false`). Nothing here is an independent second opinion; read it as one author checking their own plan.

## Coverage

Coverage by the deterministic rule is 2 of 5 (`coverage_pct_union` 0.40; parsed-only `coverage_pct` is null). Detail: `artifacts/coverage-matrix.md`.

- Mapped: INF-001 (`superclaude prd` gone) by Task 1; INF-004 (pass count drops only by removed tests) by Task 2 and the baseline figures in Constraints.
- Not mapped to any one task: INF-002 (interactive skill still installs), INF-003 (no live file names the pipeline), INF-005 (lint, format, verify-sync, `git diff --check`).
- [INFERRED] These three are whole-change checks, which the workflow rules leave to the executor ("Final verification belongs to the executor"), so the low number reflects how the source is phrased and not a missing change. They still need an explicit home when the work runs: the install check, the all-files name search and the four green checks must be run as the final regression gate.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | "`superclaude prd` is gone and `superclaude --help` does not list it" | source.md:1 | Task 1 (0.80) |
| INF-002 | "the interactive prd skill still installs" | source.md:1 | unmapped (best 0.50) |
| INF-003 | "no file outside the historical records names the removed pipeline" | source.md:1 | unmapped (best 0.57) |
| INF-004 | "0 new test failures and the pass count drops only by the removed tests" | source.md:1 | Task 9 (0.62; Task 2 is the real owner) |
| INF-005 | "lint, format, verify-sync and git diff --check stay green" | source.md:1 | unmapped (best 0.29) |

No inferred row was dropped (quotes match the cited line).

## Findings

### Finding F-1 (Medium): a row-count line in the cap fixture is not in Task 5

- **Location:** `tests/skills/fixtures/review_severity_cap_edits.yaml:1386` (`rows: 161`), and the same line in `.dev/review-severity-rule/cap-edits.yaml:1386`.
- **Mapped tasklist item:** Task 5 (removes row C-152 and edits the header comment) and Task 6 (updates the test's `161`).
- **Evidence:** `rows: 161` sits in the trailer of both copies; `tests/skills/test_review_severity_rule.py:281` pins 161 separately and does not read this line, so no test fails if it is left.
- **Classification:** none of the four deviation classes applies (plan-quality note, not a deviation). It would leave a stale number in two tracked files after Task 5.
- **Default remediation:** when running Task 5, also change `rows: 161` to `rows: 160` in both cap copies (the sweep copy has no such trailer line; checked with `git grep -E '\b139\b'`).

### Finding F-2 (Note): Tasks 11-14 depend on Task 1 only for ordering

The doc and index tasks do not need the code removal to be applied first; the dependency lines are harmless. No change needed.

## What was checked and found fine

- All 19 files and every quoted line number in the tasks exist and match (Pre-check in `artifacts/codegraph-grounding.md`).
- The three rows to remove (C-152, S-107, S-108) are the only fixture rows naming `cli/prd/` files (`git grep`), and the four files that must stay byte-equal are listed in Task 5.
- No task puts an output under the distributable skill, agent or command mirror folders, and the plan has no checkbox or numbered lines.

## Open items for the person running the plan

- Run Tier 2 reflect on this plan only if an independent review is wanted; it needs permission to start sub-agents.
- Carry F-1 into Task 5; run the install, name-search, lint, format, verify-sync and `git diff --check` checks as the final gate.

Footer: citations_inferred is 1 of 3, below the inference warning threshold. Tier 1 only; degraded_components: `t2-not-run-no-subagents`, `calibration-inline`, `evidence-validator-inline`, `graph:absent`.
