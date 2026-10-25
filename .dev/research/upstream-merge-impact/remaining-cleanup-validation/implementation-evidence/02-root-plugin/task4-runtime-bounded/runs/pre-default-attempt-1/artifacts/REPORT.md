# sc:sc-reflect — UC-1 pre-execution audit

Audited plan: `proposed.md` against spec `spec.md`.
audit_repo_root: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project` (Git root; the repo has no commits). All `file:line` citations are relative to that root. Each one was re-Read by `sc:evidence-validator` (see `artifacts/evidence-validation.yaml`).

```yaml
contract_version: 1.8.0
status: partial                 # forced: evidence-validator dropped 1 citation (§11.2)
mode: pre
tier_reached: 1
confidence_calibrated: 0.89     # blind sc:confidence-calibrator (opus slot); self-reported 0.72 ignored
citations_total: 13
citations_revalidated: 13
citations_dropped: 1
citations_inferred: 5
citation_budget_policy: full_reread
coverage_degraded: null
```

## Verdict

**Ready with amendments.** Every spec requirement maps to exactly one task (coverage 1.0). However, the task bodies paraphrase the acceptance criteria instead of stating them, and the plan has no verification step.

## Coverage matrix

| Requirement | Spec citation | Task | Task citation | Match |
|---|---|---|---|---|
| R-001 Greeting | spec.md:5 | T-101 | proposed.md:3 | exact |
| R-002 Empty input | spec.md:8 | T-102 | proposed.md:6 | exact |
| R-003 Evidence | spec.md:11 | T-103 | proposed.md:9 | exact |

- `coverage_pct` 1.0, `coverage_pct_union` 1.0. Nothing is unmapped. `coverage_undefined: false`.
- Pass 2 inference produced zero rows. Each MUST statement (spec.md:6, spec.md:9, spec.md:12) sits inside a parsed heading span, so the Inferred-requirements section is omitted.
- `best_practice_grade`: 3/5. Traceability is complete, but the tasks lack acceptance detail, a verify step and ordering.
- Deviation classes do not apply in pre mode (UC-1).

## Findings

- **F-1 (low):** T-101 says "the required greeting" and does not restate the exact string "Hello, Ada!" (proposed.md:4 vs spec.md:6).
- **F-2 (medium):** T-103 names the two test cases but not their assertions: exact equality to "Hello, Ada!", and ValueError specifically (proposed.md:10; spec.md:6, spec.md:9, spec.md:12). ValueError appears only in the implementation task (proposed.md:7).
- **F-3 (medium):** [INFERRED] "Empty name" is undefined in both the spec and the plan. It could mean `""` only, or also None, whitespace or non-str input (spec.md:9, proposed.md:7).
- **F-4 (low):** [INFERRED] The spec defines output only for Ada. Generalising to other names is an assumption (spec.md:6, proposed.md:4).
- **F-5 (low):** [INFERRED] No task runs the tests or defines done. There are no file targets and no dependency of T-103 on T-101/T-102 (proposed.md:3, proposed.md:6, proposed.md:9).
- **F-6 (low):** R-003 names no framework, location or assertion style, and "ordinary greeting" is undefined (spec.md:12).

## Risks

- **(medium)** A test that catches bare Exception, or never asserts, would satisfy T-103 and R-003's "exercise" wording while breaking the R-002 ValueError contract (proposed.md:10, spec.md:9, spec.md:12).
- **(medium)** A loose ordinary-case assertion, or a different name, would not prove the exact string (proposed.md:10, spec.md:6).
- **(low)** [INFERRED] None and whitespace names may be handled inconsistently (spec.md:9).
- **(low)** [INFERRED] With no run-tests step, the plan could be marked complete while tests fail (proposed.md:9).

## Grounding Gaps — dropped citations

| Dropped citation | Original claim | Reason |
|---|---|---|
| `proposed.md:11` | R-4: "After proposed.md:11 (end of file), add T-104…" | Line 11 does not exist; proposed.md has 10 lines. Dropped, and R-4 below no longer has a line anchor. |

The dropped citation was a recommendation anchor, not a coverage-matrix or Pass-2 row. Coverage fields are therefore unchanged and need no recompute. `grounding-gaps.yaml` (§10.6, unclassifiable findings) was not created because there are no evidence-insufficient findings, so `needs_human_decision` is false.

## Inferred-claim audit

- `citations_inferred: 5` (F-3, F-4, F-5, Risk 3, Risk 4)
- Inferred fraction: 5 / 13 = 0.38. The WARN threshold (>20 citations) is not reached.

## Recommendations

Advisory only. Nothing was edited. `sc:confidence-check` used the lightweight form: anchors were verified by the evidence gate, and one token is marked [UNVERIFIED].

### R-1: Make T-102/T-103 assert ValueError specifically (P1)
- **File:** proposed.md:10
- **Change:** Require two assertions: `greet("Ada") == "Hello, Ada!"`, and that `greet("")` raises ValueError specifically, not bare Exception. Use `pytest.raises(ValueError)` if pytest is the runner. [UNVERIFIED]: the audited repo declares no test runner or config.
- **Verifier:** Read the test file. The empty-name test names ValueError and fails if no exception is raised.
- **Linked:** F-2, Risks 1–2

### R-2: Restate the exact acceptance string in T-101 (P1)
- **File:** proposed.md:4
- **Change:** Replace with "Implement greet(name) so greet("Ada") returns exactly "Hello, Ada!" (spec.md:6)."
- **Verifier:** A test asserts `greet('Ada') == 'Hello, Ada!'`.
- **Linked:** F-1

### R-3: Define "empty" (P2)
- **File:** proposed.md:7 (or amend spec.md:9)
- **Change:** State that empty means `""` and that None and whitespace are out of scope, or specify them explicitly.
- **Verifier:** The plan or spec text contains the scope statement, and a test covers each in-scope empty form.
- **Linked:** F-3

### R-4: Add a verification/ordering task (P2)
- **File:** proposed.md (append at end of file; the line anchor was dropped by the evidence gate)
- **Change:** Add "T-104 Verify: run the test suite; done when both tests pass. T-103 depends on T-101 and T-102."
- **Verifier:** The test run shows 2 passed, and the dependency is stated in the plan.
- **Linked:** F-5, Risk 4

## Run notes / degradation

- Tier 1 only. Rule 2 fired: C=0.89 ≥ 0.85, S_scope=3, S_domains=2, S_dev_density=0.0. Waves 3–4 (reviewers, adversarial merge) did not run. No merged verdict exists, and none is claimed.
- Serena, auggie, context7 and tavily MCP tools were not exposed. Native Read/Grep/Glob were used instead. No symbolic, diagnostic or external best-practice verification was performed, and the `think_about_*` checkpoints were skipped.
- `--no-promote` was set, and Wave 7 does not apply to UC-1. Nothing was moved or mutated.
- `changes.patch`, `completed.md` and `execution.log` exist in the repo but were not selected inputs for this pre audit. `src/greeting.py` and `tests/test_greeting.py` were read as context only.
