# sc:reflect UC-1 (pre-execution) report — DRAFT (pre evidence-validator)

```yaml
contract_version: 1.8.0
status: PENDING_EVIDENCE_GATE
mode: pre
tier_reached: 1
confidence_calibrated: 0.78
citations_total: PENDING
citations_revalidated: PENDING
citations_dropped: PENDING
citations_inferred: PENDING
citation_budget_policy: full_reread
coverage_degraded: null
```

- **Audit repo root:** fixtures/project (git root; repo has no commits)
- **Inputs:** `spec.md` (driving spec), `proposed.md` (proposed tasklist)
- **Tier:** 1 (pinned by `--tier 1`). **WARN:** calibrated confidence 0.78 is below the 0.85 floor. Under `--tier auto`, rubric rule 6 would have escalated to Tier 2.
- **Degraded:** `--no-mcp` (Serena/auggie symbolic grounding, memory, diagnostics and checkpoints skipped; native Read only). External best-practice lookup was not performed (`tech-research` unavailable in this plugin).

## Coverage matrix

| Spec requirement | Spec citation | Task | Task citation | Match |
|---|---|---|---|---|
| R-001 Greeting | spec.md:5 | T-101 | proposed.md:3 | exact |
| R-002 Empty input | spec.md:8 | T-102 | proposed.md:6 | exact |
| R-003 Evidence | spec.md:11 | T-103 | proposed.md:9 | exact |

- `coverage_pct` = 1.0 (3/3 parsed); `coverage_pct_union` = 1.0; unmapped = [] (both parsed-only and union).
- Pass 2 inference: 0 rows. The MUST statements at spec.md:6, spec.md:9 and spec.md:12 sit inside parsed requirement spans, so the parsed rows win.
- No scope expansion: the tasklist contains only T-101, T-102 and T-103 (proposed.md:3, proposed.md:6, proposed.md:9).
- `S_dev_density` = 0.0.

## Gap registry (plan-vs-spec fidelity)

UC-1 audits a proposed plan, so there is no completed work to classify under the UC-2 deviation taxonomy. Gaps are listed here instead.

### G-1 (P1): T-101 omits the exact acceptance value
- **Spec:** "The greet function MUST return the exact string Hello, Ada! for Ada." (spec.md:6)
- **Task:** "Implement greet(name) returning the required greeting." (proposed.md:4)
- The task names neither the literal `Hello, Ada!` nor the `Ada` input.

### G-2 (P2): T-103 does not state its assertions
- **Spec:** "Tests MUST exercise the ordinary greeting and empty-input rejection." (spec.md:12)
- **Task:** "Add ordinary and empty-name test cases." (proposed.md:10)
- Both cases are named, but the expected value and expected exception are not.
- [INFERRED] A test that only checks for "no crash" would satisfy the task text.

### G-3 (P2): No verification or ordering step
- The plan has three tasks and no run-tests step (proposed.md:3–10).
- [INFERRED] This is a plan-quality gap, not a spec violation: the spec requires the tests to exercise the behaviour (spec.md:12), not to pass.

### G-4 (P2, faithful): T-102
- **Task:** "Reject an empty name using ValueError." (proposed.md:7)
- **Spec:** "The greet function MUST reject an empty name with ValueError." (spec.md:9)
- Trigger and exception type both match.

**Best-practice grade:** 3/5. Traceability is clean, but acceptance criteria are underspecified (G-1, G-2) and there is no verification step (G-3).

## Risks
- If T-101 is executed without the literal, the implementation could drift in format (for example, a missing `!`). Only a T-103 test that pins the value would catch it (spec.md:6, proposed.md:4).
- [INFERRED] The spec does not address whitespace-only or `None` names. An implementer may add handling nobody asked for, or silently leave it out.

## Inferred-claim audit
- `citations_inferred: PENDING`

## Recommendations
(Pending `sc:confidence-check`. The audited inputs are not edited by this run.)

### R-1 (P1): Pin the greeting literal in T-101
- **File:** proposed.md
- **Change:** Reword T-101 to: `greet("Ada")` returns exactly `"Hello, Ada!"`.
- **Verifier:** Re-read proposed.md T-101 and confirm the literal `Hello, Ada!` and the input `Ada` appear.
- **Linked gap:** G-1

### R-2 (P2): State the T-103 assertions
- **File:** proposed.md
- **Change:** T-103 asserts `greet("Ada") == "Hello, Ada!"` and `pytest.raises(ValueError)` for `greet("")`.
- **Verifier:** Both assertions appear in the T-103 text.
- **Linked gap:** G-2

### R-3 (P2): Add ordering and a final test run
- **File:** proposed.md
- **Change:** Add a dependency (T-103 after T-101 and T-102) and a final step that runs the test suite and expects it to pass.
- **Verifier:** The plan names the test command and the expected pass outcome.
- **Linked gap:** G-3
