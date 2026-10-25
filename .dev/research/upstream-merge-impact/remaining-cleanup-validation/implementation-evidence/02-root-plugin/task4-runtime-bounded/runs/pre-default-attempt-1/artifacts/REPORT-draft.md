# sc:sc-reflect — UC-1 pre-execution audit (DRAFT, pre-evidence-gate)

Audited plan: `proposed.md` against spec `spec.md`.
audit_repo_root: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project`. All `file:line` citations below are relative to that root.

```yaml
contract_version: 1.8.0
status: TBD-after-evidence-gate
mode: pre
tier_reached: 1
confidence_calibrated: 0.89
citation_budget_policy: full_reread
coverage_degraded: null
```

## Verdict

Ready with amendments. Every spec requirement maps to exactly one task, but the task bodies paraphrase the acceptance criteria, and the plan has no verification step.

## Coverage matrix

| Requirement | Spec citation | Task | Task citation | Match |
|---|---|---|---|---|
| R-001 Greeting | spec.md:5 | T-101 | proposed.md:3 | exact |
| R-002 Empty input | spec.md:8 | T-102 | proposed.md:6 | exact |
| R-003 Evidence | spec.md:11 | T-103 | proposed.md:9 | exact |

- coverage_pct 1.0, coverage_pct_union 1.0, unmapped: none.
- Pass 2 inference produced zero rows: each MUST statement (spec.md:6, spec.md:9, spec.md:12) sits inside a parsed heading span.
- best_practice_grade: 3/5.

## Findings

- **F-1 (low):** T-101 says "the required greeting" and does not restate the exact string "Hello, Ada!" (proposed.md:4 vs spec.md:6).
- **F-2 (medium):** T-103 does not state what the tests assert: exact equality to "Hello, Ada!", and ValueError specifically (proposed.md:10; spec.md:6, spec.md:9, spec.md:12). ValueError appears only in the implementation task (proposed.md:7).
- **F-3 (medium):** [INFERRED] "Empty name" is undefined in both the spec and the plan (spec.md:9, proposed.md:7).
- **F-4 (low):** [INFERRED] The spec defines output only for Ada. Generalising to other names is an assumption (spec.md:6, proposed.md:4).
- **F-5 (low):** [INFERRED] No task runs the tests or defines done. There are no file targets and no dependency ordering (proposed.md:3, proposed.md:6, proposed.md:9).
- **F-6 (low):** R-003 names no framework, location or assertion style (spec.md:12).

## Risks

- **(medium)** A test that catches bare Exception, or never asserts, would satisfy T-103 and R-003's "exercise" wording but not the R-002 ValueError contract (proposed.md:10, spec.md:9, spec.md:12).
- **(medium)** A loose ordinary-case assertion would not prove the exact string (proposed.md:10, spec.md:6).
- **(low)** [INFERRED] None and whitespace names may be handled inconsistently (spec.md:9).
- **(low)** [INFERRED] With no run-tests step, the plan could be marked complete while tests fail (proposed.md:9).

## Recommendations

- **R-1 (P1):** At proposed.md:4, state that greet("Ada") must return exactly "Hello, Ada!". Verifier: a test asserts `greet('Ada') == 'Hello, Ada!'`.
- **R-2 (P1):** At proposed.md:10, require two assertions: exact equality, and `pytest.raises(ValueError)`. Verifier: Read the tests; the empty case names ValueError and fails if nothing is raised.
- **R-3 (P2):** At proposed.md:7, define "empty" as `""` and mark None and whitespace out of scope, or amend spec.md:9. Verifier: the plan text contains the scope statement.
- **R-4 (P2):** After proposed.md:11 (end of file), add "T-104 Verify: run the test suite; T-103 depends on T-101 and T-102". Verifier: the run shows 2 passed.

## Inferred-claim audit

- citations_inferred: 6 ([INFERRED]-tagged claims: F-3, F-4, F-5, two risks; plus the generalisation in F-4 counted once) — final count is set after the gate.
