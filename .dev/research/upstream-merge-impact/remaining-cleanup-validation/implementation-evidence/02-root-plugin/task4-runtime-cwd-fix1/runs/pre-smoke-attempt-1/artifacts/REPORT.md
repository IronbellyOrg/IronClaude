# sc:reflect — UC-1 pre-execution audit — Tier 1, validated

Citation base: all `spec.md:N` / `proposed.md:N` citations are relative to
`audit_repo_root=/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/task4-runtime-cwd-fix1/fixtures/project`.

```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 1
confidence_calibrated: 0.94
citations_total: 25
citations_revalidated: 25
citations_dropped: 0
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: null
```

## Summary

The proposed tasklist maps every spec requirement to exactly one task: R-001→T-101,
R-002→T-102, R-003→T-103. Coverage is 3/3 = 1.00 (parsed and union), with 0 inferred
requirements. That is ID-level coverage. Two tasks paraphrase their requirement and lose
acceptance detail: T-101 drops the exact greeting literal, and T-103 states no assertions.
Executing the plan as written could therefore pass while violating R-001.

## Coverage matrix

| Requirement | Spec | Task | Tasklist | Method | Content fidelity |
|---|---|---|---|---|---|
| R-001 Greeting | spec.md:5-6 | T-101 | proposed.md:3-4 | exact | partial (C-1) |
| R-002 Empty input | spec.md:8-9 | T-102 | proposed.md:6-7 | exact | full |
| R-003 Evidence | spec.md:11-12 | T-103 | proposed.md:9-10 | exact | partial (C-2) |

- coverage_pct = 1.0; coverage_pct_union = 1.0; unmapped_requirements = []; S_dev_density = 0.0
- Pass 2 inference: 0 valid rows. Every MUST statement (spec.md:6, spec.md:9, spec.md:12) lies inside a parsed heading span, and spec.md:1-3 is a title/disclaimer with no requirement.

## Findings (UC-1 gap registry)

### C-1 (medium): R-001 exact literal not carried into T-101
- Spec: "The greet function MUST return the exact string Hello, Ada! for Ada." (spec.md:6)
- Task: "Implement greet(name) returning the required greeting." (proposed.md:4)
- The literal `Hello, Ada!` and the example input are absent from the task, so an implementer working from the task alone could ship a different format.

### C-2 (medium): R-003 tests do not state their assertions
- Spec: "Tests MUST exercise the ordinary greeting and empty-input rejection." (spec.md:12)
- Task: "Add ordinary and empty-name test cases." (proposed.md:10)
- Neither the exact-output assertion nor the ValueError assertion appears anywhere in the tasklist. The spec's own verb is "exercise", not "assert" (spec.md:12).

### C-3 (low/info): R-002 carried faithfully
- "MUST reject an empty name with ValueError" (spec.md:9) vs "Reject an empty name using ValueError." (proposed.md:7). Neither document defines whitespace-only names. This ambiguity is shared by both documents, not a plan gap.

### C-4 (info): plan adds signature greet(name)
- proposed.md:4 fixes `greet(name)`; the spec says only "the greet function" (spec.md:6). Harmless plan-level detail.

[INFERRED] The likely root cause of C-1/C-2 is that the tasks were authored by requirement-ID reference (proposed.md:3, proposed.md:9 headings) rather than by restating acceptance criteria. The documents do not record their authoring method.

## Risks
- A wrong greeting format accepted silently (C-1 + C-2): primary load-bearing risk.
- A false-green test suite: tests that call `greet` without asserting can pass (C-2).
- Divergent edge-case behaviour for whitespace-only names (C-3). Small blast radius.

## Tier decision
`--tier 1` hard override (§5.1). Rubric recording: C=0.94, S_scope=3, S_domains=2, S_dev_density=0.0 → rule 2 (STOP at T1) would also have fired. No Tier-2 reviewers and no adversarial merge, so `merge_method` is not applicable.

## Degradation / grounding gaps (non-gating, no grounding-gaps.yaml rows)
- `--no-mcp`: Serena/auggie chain, memory hydrate, `get_current_config`, `think_about_*` checkpoints and FR-1 implementor checks were not run, so `missing_implementations_count: 0` is a degenerate no-op. Native Read only.
- `tech-research` is unavailable in this plugin distribution, so no external best-practice lookup was done. `best_practice_grade: 3` is a judgement made from the plan text only.
- Fixture `src/` and `tests/` were intentionally not read. A UC-1 audit reviews the plan, not completed work.

## Inferred-claim audit
- citations_inferred: 1
- Inferred fraction: 1 / 25 = 0.04

## Evidence gate
- `sc:evidence-validator` (opus slot) re-read all 25 citation occurrences in the draft: 25 verified, 0 dropped (`artifacts/evidence-validation.yaml`). Under §11.2 a zero-drop pass is audit-logged with `zero-drop-flag: true`, so it counts as a suspect pass, not a clean one. UC-1 with no drops may report `status: success`.
- The validator flagged several uncited absence claims. They are true, and are supported by citations elsewhere in this report: "Neither document defines whitespace-only names" (C-3) and "neither assertion appears anywhere in the tasklist" (C-2). The report text was left unchanged after validation so the validated citation set stays exact.
- `sc:confidence-check` (lightweight form) re-verified each recommendation's tokens by Grep before they were surfaced (`artifacts/confidence-check.yaml`).

## Recommendations

### Recommendation R-1: Restate the greeting literal in T-101 (P1)
- **File:** proposed.md
- **Change:** At proposed.md:4, state that greet("Ada") returns exactly "Hello, Ada!".
- **Verifier:** Grep the T-101 block of proposed.md for `Hello, Ada!` (≥1 match).
- **Linked:** C-1

### Recommendation R-2: State the assertions in T-103 (P1)
- **File:** proposed.md
- **Change:** At proposed.md:10, require that the ordinary test assert the return value equals "Hello, Ada!" and that the empty-name test assert ValueError is raised.
- **Verifier:** Grep the T-103 block for both `Hello, Ada!` and `ValueError`.
- **Linked:** C-2

### Recommendation R-3: Decide whitespace-only names (P2, optional)
- **File:** spec.md
- **Change:** At spec.md:9, state whether whitespace-only names count as empty, or record them as out of scope.
- **Verifier:** The R-002 text carries the statement and T-102 (proposed.md:7) matches it.
- **Linked:** C-3
