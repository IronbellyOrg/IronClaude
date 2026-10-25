# sc:sc-reflect — UC-1 pre-execution reflection (DRAFT, pre evidence-validator)

```yaml
contract_version: 1.8.0
status: <pending evidence-validator>
mode: pre
tier_reached: 1
confidence_calibrated: 0.91
citations_total: 15
citations_revalidated: <pending>
citations_dropped: <pending>
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: null
```

All paths below are relative to `audit_repo_root` =
`/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-bounded/fixtures/project`.

**Degraded run (loud):** `--no-mcp` → Serena/auggie grounding chain, Serena checkpoints and memory were not used (native Read only).
The optional `tech-research` best-practice lookup is UNAVAILABLE in this plugin-only distribution and was not performed;
`best_practice_grade` is an internal judgement only. Tier pinned to 1 by `--tier 1`; no Tier-2 reviewers, no adversarial merge.

## Coverage matrix

| Req | Spec citation | Task | Task citation | Match | Semantic adequacy |
|---|---|---|---|---|---|
| R-001 | spec.md:5 (heading), spec.md:6 (MUST) | T-101 | proposed.md:3, proposed.md:4 | exact | partial — exact literal not stated in task |
| R-002 | spec.md:8 (heading), spec.md:9 (MUST) | T-102 | proposed.md:6, proposed.md:7 | exact | full |
| R-003 | spec.md:11 (heading), spec.md:12 (MUST) | T-103 | proposed.md:9, proposed.md:10 | exact | partial — assertion content unspecified |

- `coverage_pct: 1.0` (3/3 parsed), `coverage_pct_union: 1.0`, `unmapped_requirements: []`, no orphan tasks.
- Pass-2 inference produced 0 surviving rows; the `## Inferred requirements (Pass 2)` section is therefore omitted.
- Spec line 3 ("This fixture is synthetic audit input, not shipped product code." — spec.md:3) is descriptive context, not a requirement.

## Findings

- **F-1 (grounded):** One-to-one traceability: each task heading names its requirement ID (proposed.md:3, proposed.md:6, proposed.md:9 ↔ spec.md:5, spec.md:8, spec.md:11).
- **F-2 (grounded):** T-102 "Reject an empty name using ValueError." (proposed.md:7) faithfully restates R-002 "MUST reject an empty name with ValueError." (spec.md:9).
- **F-3 (grounded, medium):** R-001 requires "the exact string Hello, Ada! for Ada" (spec.md:6) but T-101 says only "returning the required greeting" (proposed.md:4); the acceptance literal is absent from the plan.
- **F-4 (grounded, low):** spec.md:6 pins only the Ada case; the general greeting template for other names is unspecified, and proposed.md:4 does not resolve it.
- **F-5 (grounded, medium):** T-103 "Add ordinary and empty-name test cases." (proposed.md:10) does not require asserting the exact string or the ValueError type, although R-003 (spec.md:12) is the evidence requirement for both behaviours.
- **F-6 (grounded, medium):** The plan (proposed.md:1-10) names no module/file/test path, no verification command and no ordering; the spec (spec.md:1-12) names only "the greet function". The signature `greet(name)` is present (proposed.md:4).
- **F-7 (grounded, low):** "empty name" (spec.md:9, proposed.md:7) is undefined for whitespace-only or None input.
- **F-8 [INFERRED]:** No requirement carries a `durable_sink:`/`@sink` annotation; the FR-RH1 reachability gate is UC-2-only and not applicable here.

## Plan-vs-spec deviations

None. No task contradicts or expands its requirement; F-3 and F-5 are under-specification of acceptance detail, not divergence.
(Calibrator note, recorded: F-3 is a judgement call that a reviewer could frame as a Drift candidate; under UC-1 no work has executed, so it is reported as a precision gap with a P1 recommendation.)

## Risks

- **K-1 (grounded):** Without the exact literal in T-101 (proposed.md:4 vs spec.md:6), an implementation could satisfy a loose reading of the task and miss R-001.
- **K-2 (grounded):** Weak test oracles (proposed.md:10) give false assurance for R-001/R-002 (spec.md:6, spec.md:9, spec.md:12).
- **K-3 [INFERRED]:** Unspecified empty-input semantics may cause a post-hoc dispute in the later UC-2 audit.
- **K-4 [INFERRED]:** Without file targets or a run command, a later post-execution audit may struggle to reproduce evidence.
- **K-5 (grounded):** Blast radius is minimal; the fixture is synthetic (spec.md:3) and the plan has three small tasks (proposed.md:1-10).

## Best-practice grade

`best_practice_grade: 3` — complete traceability and no scope creep; weak on acceptance literals, assertion-level tests, file targets and a verifier command. Internal judgement only (no external lookup performed).

## Inferred-claim audit

- `citations_inferred: 3` (F-8, K-3, K-4)
- Inferred-fraction: 3 / 15 = 0.20

## Recommendations

### Recommendation R-1: Pin the acceptance literal in T-101
- **File:** proposed.md (T-101, line 4)
- **Change:** State that `greet("Ada")` must return exactly `Hello, Ada!` and name the target module/file. The signature `greet(name)` is already present, so only the module/file target is missing. Optionally state the general template, or record that it is out of scope.
- **Verifier:** Re-Read proposed.md T-101 and confirm the literal and module path are present; after execution, a test asserting `greet("Ada") == "Hello, Ada!"` passes.
- **Linked:** F-3, F-4, F-6 — **Priority:** P1

### Recommendation R-2: Require assertion-level tests in T-103
- **File:** proposed.md (T-103, line 10)
- **Change:** Require (a) an equality assertion on `Hello, Ada!` and (b) `pytest.raises(ValueError)` on `greet("")`, and name the test file path.
- **Verifier:** Re-Read proposed.md T-103 for both assertions; after execution, `uv run pytest <named test file> -q` exits 0, and mutating the literal or the exception type makes a test fail.
- **Linked:** F-5, F-6 — **Priority:** P1

### Recommendation R-3: Decide empty-input edge cases
- **File:** proposed.md (T-102, line 7)
- **Change:** Explicitly state whether whitespace-only and None inputs are in scope; if in scope, add a matching spec clause to spec.md R-002 and a T-103 test case.
- **Verifier:** Re-Read proposed.md T-102 for the explicit scope statement.
- **Linked:** F-7 — **Priority:** P2

### Recommendation R-4: Add ordering and a verification command
- **File:** proposed.md (new trailing section)
- **Change:** Declare T-101 and T-102 before T-103 and add one verification command (for example `uv run pytest <named test file> -q`) with expected result "exit 0".
- **Verifier:** The command named in proposed.md runs as written and exits 0 after execution.
- **Linked:** F-6 — **Priority:** P2
