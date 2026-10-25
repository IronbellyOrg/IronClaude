# sc:reflect UC-1 (pre-execution) report

```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 1
confidence_calibrated: 0.78
citations_total: 22
citations_revalidated: 22
citations_dropped: 0
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: null
```

- **Audit repo root:** fixtures/project. Resolved with `git rev-parse --show-toplevel`; the repo has no commits.
- **Inputs:** `spec.md` (driving spec) and `proposed.md` (proposed tasklist). `input_tree_sha256` is `1811526544b9…5fc09`, and it was unchanged at Wave 5 (no drift).
- **Tier:** 1, pinned by `--tier 1`.
  - **WARN:** calibrated confidence 0.78 is below the 0.85 floor. Under `--tier auto`, rubric rule 6 would have escalated to Tier 2.
- **Calibration:**
  - Independent and blind: `sc:confidence-calibrator` on the opus slot, scoring a card written on the sonnet slot.
  - Scores: citation 0.88, coverage 1.00, classification 0.30, risk 0.80, actionability 0.90. Mean 0.78.
- **Evidence gate:** `sc:evidence-validator` re-read all 22 citations and dropped none.
  - The audit log carries `zero-drop-flag: true` (a zero-drop pass is suspect by protocol).
- **Degraded:**
  - `--no-mcp`: Serena and auggie symbolic grounding, memory, diagnostics and `think_about_*` checkpoints were skipped. Grounding used native Read and Grep only.
  - No external best-practice lookup was done (`tech-research` is unavailable in this plugin).

## Coverage matrix

| Spec requirement | Spec citation | Task | Task citation | Match |
|---|---|---|---|---|
| R-001 Greeting | spec.md:5 | T-101 | proposed.md:3 | exact |
| R-002 Empty input | spec.md:8 | T-102 | proposed.md:6 | exact |
| R-003 Evidence | spec.md:11 | T-103 | proposed.md:9 | exact |

- `coverage_pct` = 1.0 (3 of 3 parsed). `coverage_pct_union` = 1.0. Nothing is unmapped, on either the parsed-only or the union count.
- Pass 2 inference added 0 rows. The MUST statements at spec.md:6, spec.md:9 and spec.md:12 fall inside parsed requirement spans, and parsed rows win.
- No scope expansion: the tasklist contains only T-101, T-102 and T-103 (proposed.md:3, proposed.md:6, proposed.md:9).
- `S_dev_density` = 0.0.
- Erratum: the run's coverage matrix gave R-003's span as 11-13. spec.md has 12 lines, so the span is 11-12. See `artifacts/coverage-matrix-errata.yaml`.

## Gap registry (plan-vs-spec fidelity)

UC-1 audits a proposed plan, so there is no completed work to classify under the UC-2 deviation taxonomy. Gaps are listed instead.

### G-1 (P1): T-101 omits the exact acceptance value
- **Spec:** "The greet function MUST return the exact string Hello, Ada! for Ada." (spec.md:6)
- **Task:** "Implement greet(name) returning the required greeting." (proposed.md:4)
- The task names neither the literal `Hello, Ada!` nor the `Ada` input.

### G-2 (P2): T-103 does not state its assertions
- **Spec:** "Tests MUST exercise the ordinary greeting and empty-input rejection." (spec.md:12)
- **Task:** "Add ordinary and empty-name test cases." (proposed.md:10)
- Both cases are named, but the task gives no expected value and no expected exception.
- [INFERRED] A test that only checks for "no crash" would satisfy the task text.

### G-3 (P2): No verification or ordering step
- The plan has three tasks and no run-tests step (proposed.md:3–10).
- [INFERRED] This is a plan-quality gap, not a spec violation: the spec requires the tests to exercise the behaviour (spec.md:12), not to pass.

### G-4 (P2): T-102 is faithful to the spec
- **Task:** "Reject an empty name using ValueError." (proposed.md:7)
- **Spec:** "The greet function MUST reject an empty name with ValueError." (spec.md:9)
- The trigger and the exception type both match.

**Best-practice grade: 3/5.** Traceability is clean. Acceptance criteria are underspecified (G-1, G-2), and there is no verification step (G-3).

## Risks
- If T-101 is executed without the literal, the output format could drift (for example, a missing `!`). Only a T-103 test that pins the value would catch it (spec.md:6, proposed.md:4).
- [INFERRED] The spec does not mention whitespace-only or `None` names. An implementer might add unrequested handling or silently leave it out.

## Inferred-claim audit
- `citations_inferred: 3`
- Inferred fraction: 3 / 22 = 0.14

## Recommendations

> **Gated: `sc:confidence-check` scored 0.15, below 0.70.** The recommendations below are advisory only and need more context before anyone acts on them.
> - The confidence check found pre-existing project state outside this audit's selected inputs; see `artifacts/confidence-check.yaml`. That state may make T-101's "Implement" wording a duplicate.
> - Confirm the intended baseline before amending the plan. If the work already exists, a `--mode post` audit (diff or task log) is the appropriate check.
> - This run edits nothing.

### R-1 (P1): Pin the greeting literal in T-101
- **File:** proposed.md
- **Change:** Reword T-101 to state that `greet("Ada")` returns exactly `"Hello, Ada!"`.
- **Verifier:** Re-read proposed.md T-101 and confirm the literal `Hello, Ada!` and the input `Ada` appear.
- **Linked gap:** G-1

### R-2 (P2): State the T-103 assertions
- **File:** proposed.md
- **Change:** T-103 asserts that `greet("Ada")` equals `"Hello, Ada!"` and that `greet("")` raises `ValueError`. Use the project's existing test idiom.
- **Verifier:** Both assertions appear in the T-103 text.
- **Linked gap:** G-2

### R-3 (P2): Add ordering and a final test run
- **File:** proposed.md
- **Change:** Add a dependency (T-103 runs after T-101 and T-102) and a final step that runs the test suite and expects it to pass.
- **Verifier:** The plan names the test command and the expected pass outcome.
- **Linked gap:** G-3

## Disposition
- **Promotion:** suppressed (`--no-promote`; also not applicable in UC-1). No moves, archive writes or mutations.
- **Remediation:** not requested (no `--remediate`). Wave 6 did not run.
