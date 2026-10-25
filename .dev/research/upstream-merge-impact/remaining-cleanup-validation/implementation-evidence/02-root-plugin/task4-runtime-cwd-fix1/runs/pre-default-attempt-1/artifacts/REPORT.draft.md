# sc:sc-reflect — UC-1 pre-execution audit (DRAFT, pending evidence-validator)

```yaml
contract_version: 1.8.0
status: <pending evidence-validator>
mode: pre
tier_reached: 1
confidence_calibrated: 0.90
citations_total: 13
citations_revalidated: <pending>
citations_dropped: <pending>
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: null
```

Citation base: all `spec.md:N` / `proposed.md:N` citations are relative to
`audit_repo_root=/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/fixtures/project`.

## Summary

The proposed tasklist covers every labeled spec requirement 1:1 (ID coverage 3/3,
`coverage_pct: 1.0`). No inferred (Pass 2) requirements survived dedup. The plan is
traceable but thin: two tasks paraphrase rather than restate the testable contract.
Best-practice grade: **3/5**. Tier 1 stop (rule 2). No blocking gaps.

## Coverage matrix

| Requirement | Spec | Task | Task ref | Match | Semantic |
|---|---|---|---|---|---|
| R-001 Greeting | spec.md:5-6 | T-101 | proposed.md:3-4 | exact | partial — literal "Hello, Ada!" not restated |
| R-002 Empty input | spec.md:8-9 | T-102 | proposed.md:6-7 | exact | full — whitespace-only policy unspecified in both docs |
| R-003 Evidence | spec.md:11-12 | T-103 | proposed.md:9-10 | exact | partial — assertions / exception type not named |

- `coverage_pct: 1.0`, `coverage_pct_union: 1.0`, `unmapped_requirements: []`, `unmapped_requirements_union: []`, `S_dev_density: 0.0`.
- Pass 2: zero `INF-NNN` rows. The MUST statements at spec.md:6, spec.md:9, spec.md:12 sit inside their parsed spans; spec.md:3 ("This fixture is synthetic audit input, not shipped product code.") is a non-normative scope note. (Inferred-requirements section omitted: zero rows.)

## Findings

- **F-003 (medium)** — T-101 says "Implement greet(name) returning the required greeting." (proposed.md:4) while the spec requires "the exact string Hello, Ada! for Ada." (spec.md:6). The literal lives only in the spec.
- **F-004 (low)** — T-102 restates "Reject an empty name using ValueError." (proposed.md:7), matching spec.md:9; neither document defines whether whitespace-only names count as empty.
- **F-005 (medium)** — T-103 "Add ordinary and empty-name test cases." (proposed.md:10) covers both cases required by spec.md:12 but names no equality assertion or ValueError expectation.
- [INFERRED] **F-007 (low)** — The plan declares no dependency of T-103 on T-101/T-102 and names no target module for greet (headings proposed.md:3, proposed.md:6, proposed.md:9 carry only IDs).

## Risk register

- K-001 (medium): T-101 satisfiable with a wrong greeting string (proposed.md:4 vs spec.md:6).
- K-002 (medium): T-103 tests could pass without asserting the exact string or ValueError type (proposed.md:10 vs spec.md:12).
- K-003 (low): whitespace-only input behavior undefined (spec.md:9, proposed.md:7).

## Inferred-claim audit

- `citations_inferred: 1`
- Inferred-fraction: 1 / 13 = 0.08

## Recommendations

### Recommendation R-001: Restate the exact greeting literal in T-101
- **File:** proposed.md
- **Change:** Reword T-101 (proposed.md:4) to "Implement greet(name) so that greet('Ada') returns exactly 'Hello, Ada!'".
- **Verifier:** Grep the T-101 section of proposed.md for the literal `Hello, Ada!`.
- **Linked deviation(s):** none (proactive; UC-1)
- **Priority:** P1

### Recommendation R-002: Name the assertions in T-103
- **File:** proposed.md
- **Change:** Reword T-103 (proposed.md:10) to require `greet('Ada') == 'Hello, Ada!'` and that `greet('')` raises `ValueError`.
- **Verifier:** Grep the T-103 section for `ValueError` and `Hello, Ada!`.
- **Linked deviation(s):** none
- **Priority:** P1

### Recommendation R-003: Decide the whitespace-only policy
- **File:** spec.md
- **Change:** Add one sentence under R-002 (spec.md:9) stating whether whitespace-only names are rejected or out of scope.
- **Verifier:** Re-read the spec.md R-002 section for an explicit whitespace statement.
- **Linked deviation(s):** none
- **Priority:** P2

### Recommendation R-004: Declare dependency and target module
- **File:** proposed.md
- **Change:** Add "Depends on T-101, T-102" and the target module path to T-103 / T-101.
- **Verifier:** Re-read the T-101 and T-103 sections for the module path and dependency line.
- **Linked deviation(s):** none
- **Priority:** P2
