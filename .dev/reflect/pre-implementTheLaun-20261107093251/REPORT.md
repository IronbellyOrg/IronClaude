```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.66
citations_total: 170
citations_revalidated: 160
citations_dropped: 3
citations_inferred: 5
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

# sc:reflect pre-execution audit: launch-level hook plan (issue #394)

- Plan under audit: `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md` (22 tasks, 9 phases).
- Spec: `.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md` (a one-sentence prompt).
- Full findings table (25 rows, severity ordered): `.dev/reflect/pre-implementTheLaun-20261107093251/adversarial/merged-review.md`.
- Advisory only. Reflect does not edit the plan.

**Verdict: not ready to execute as written; no Regression (nothing ran).** One HIGH item and the gate items should be handled in the plan first. Status is `partial` because 3 citations were dropped and because one HIGH invariant (INV-001) remains unaddressed.

> **Citation budget: sampled mode**
> - `citations_revalidated: 160` of about 170 (the validator re-read nearly all; 100% of the HIGH row and the carried-forward invariant).
> - `citations_dropped: 3` is the count in the sample and is the field that gates promotion (promotion does not apply to a pre-execution audit).
> - `citations_dropped_extrapolated: 3`.
> The extrapolated value is telemetry, not a verdict.

## Why Tier 2

The spec has no labeled requirement ids, so Pass 1 found 0 ids and Pass 2 inferred 3 requirements; the parse-density guard forbids a Tier-1 stop. The Tier-1 card was also calibrated at C = 0.61 (rule 6, below 0.85). Three heterogeneous reviewers (analyzer/sonnet, qa/haiku, refactorer/opus) audited the plan; each card was blind-calibrated (0.66, 0.71, 0.78; calibrator opus, diversity degraded because no class disjoint from the reviewers was available); the cards were merged by the adversarial pipeline (convergence 17 of 17 diff points; base: the refactorer card, combined score 0.879).

## Top findings (all category Drift; severities as in the findings table)

### Deviation D-001 (HIGH): the shared launch fixture and the tests that must be re-baselined
- **Location:** Tasks 18 and 20 (PLAN:287-299, PLAN:314-325)
- **Evidence:** the launch fixture writes only `#!/bin/sh` (tests/skills/test_issue_orca_worktree.py:1011); 12 tests assert `launched` (lines 1051, 1124, 1196, 1210, 1234, 1265, 1276, 1301, 1481, 1534, 1571, 1594); la3 changes outcome because the new check runs before `publish_pending` (orca_worktree.py:937 then 941). Predicted from reading, not observed. Becomes a Regression if executed unchanged.
- **Classification rationale:** a plan step that would break currently passing tests, with no task that migrates the fixture.

### Deviation D-002 (MEDIUM): the Task 1 gate has no consumer
- **Location:** Task 1 (PLAN:36). A STOP verdict stops nothing in Tasks 2 to 22; synthetic fixtures replace the OB-H1 ordering (DESIGN:359-360); the existing `live_probe.py` is ignored.

### Deviation D-003 (MEDIUM): the owned-L2 hook predicate is undefined, and cannot be built yet (INV-001, HIGH invariant)
- **Location:** Task 20 (PLAN:318-320). DESIGN:512 rejects a header as ownership proof; the install place is open (DESIGN:377, 457); L2 is built only after B-CTX (DESIGN:366). No fixture can stand in for an owned L2.

### Other MEDIUM rows (see the findings table)
Task 19 pins L2 "absent" while Task 20 has an owned branch; the registration check ignores matchers; the identity-adapter runtime prerequisites are missing from the preflight; the check order inside `cmd_launch` is unstated; `--pipeline none` cannot be tested at script level; the circular observation gate (OB-H2 needs a governed launch that Task 20 refuses); the install remedy does not repair a stale guard; the `enforcement_hook` field meaning; Task 3 asks for all 18 message ids while classifiers are stubs; the coverage matrix omits three source clauses; T-MSG-4 to T-MSG-6 are unassigned; the F1-F8 definitions cannot be resolved (their file is absent).

### Notes
- Necessary deviation (not a finding): Task 12 inserts the guard before the identity hook; compatible while the identity hook stays last (tests/cli/test_install_hooks.py:844).
- Authorized expansion (not a finding): refusing a governed launch when the guard or L2 is absent exceeds the PR 425 warning, and the design requires it (DESIGN:355, 514). Record the consequence before implementing Task 20.

## Grounding Gaps

None written to `grounding-gaps.yaml`. Three items were dropped by the evidence-validator instead (listed in the merged review under "Dropped by the evidence-validator"): former rows 26 and 27 and one advisory item; their citations did not support the claims. Three line numbers were corrected.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | Implement the launch-level enforcement hook for issue #394 from the design docs/designs/sc-issue-launch-level-hook.md | .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1 | Task 22 (containment 0.9167); reviewers: the build is carried by Tasks 3 to 13, so this is a weak automatic match |
| INF-002 | The B-CTX feasibility gate must be the first plan step. | .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1 | Task 1 (0.8571); first position confirmed, gate not functional (D-002) |
| INF-003 | Code: src/superclaude/hooks/, src/superclaude/cli/install_hooks.py, src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, tests/hooks/. | .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1 | Task 18 (0.9333); the other areas are covered by other tasks |

The reviewer (qa) found that the spec sentence also names three input documents that the matrix does not list as separate clauses (merged requirements, addendum, cheatsheet).

## Inferred-claim audit

- `citations_inferred: 5`
- Inferred-fraction: 5 / 170 = 0.03

## Recommendations

### Recommendation R-001: migrate the shared launch fixture and list the re-baselined tests
- **File:** tests/skills/test_issue_orca_worktree.py (plan Tasks 18 and 20)
- **Change:** have Task 18 update `launch_scene` (a guard with the version line, a `settings.json` with both registrations, a known `jq`, `CLAUDE_CONFIG_DIR` unset) and name every re-baselined test including la3, la6, la2, TOW:1246, 1291, 1313 and the pr425 tests; have Task 20 add an owned-L2 fixture.
- **Verifier:** `uv run pytest tests/skills/test_issue_orca_worktree.py -v` passes after Task 18 and again after Task 20.
- **Linked deviation(s):** D-001
- **Priority:** P0

### Recommendation R-002: give the Task 1 gate a consumer
- **File:** the plan, Tasks 2 to 22
- **Change:** make enforcement tasks depend on an `L1: PROCEED` verdict and state what a STOP triggers; cite and reuse `tests/hooks/fixtures/launch_level/live_probe.py` in Tasks 1 and 2.
- **Verifier:** re-read Tasks 2 to 22 for the dependency line; the plan gate (`workflow-plan/1.2`) still passes.
- **Linked deviation(s):** D-002
- **Priority:** P1

### Recommendation R-003: decide the L2 question before Task 20, then define or drop the owned-hook predicate
- **File:** the plan, Task 20 and Task 21; `docs/designs/sc-issue-launch-level-hook.md` section 19
- **Change:** ask the owner whether governed claims should refuse to launch while L2 is absent (IR-7 as written), and either define the owned-hook proof (not a header) with negative cases or detect absence only; reconcile with Task 19's printed status and with the circular OB-H2 gate (INV-009).
- **Verifier:** the owner's reply recorded in the PR body; Task 20's tests contain no case that needs an undefined marker.
- **Linked deviation(s):** D-003
- **Priority:** P1

### Recommendation R-004: name the worker-contract test in the plan
- **File:** tests/skills/test_worker_contract.py
- **Change:** [INFERRED] memory from the previous review of the claim-pipeline plan says this test classifies every line naming `git add|commit|push|merge` or `gh pr|api` in `src/superclaude/{skills,commands,agents}` files; Tasks 19, 22 and the doc updates add such text, so the plan should name the test and its classification entries. Not verified in this run beyond the test file existing (line 1155 `_check_all_classified`).
- **Verifier:** `uv run pytest tests/skills/test_worker_contract.py -v`.
- **Linked deviation(s):** none (proactive)
- **Priority:** P2

## Unaddressed invariants carried forward

INV-001 (HIGH): Task 20's "L2 present and owned, launch proceeds" test cannot be built while the install place and marker are open (see D-003).
