# Reviewer 1 brief (persona: analyzer, model class: sonnet)

You are a read-only reviewer in a pre-execution (UC-1) reflection. You audit a proposed tasklist against the spec that drives it. You do not run commands, edit files, or fix anything. Cite only file:line ranges you Read yourself. A claim you cannot cite is dropped. Assume the plan has defects; a zero-finding review must include a self-audit of what you checked.

Inputs: spec /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/source.md ; tasklist /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-specR1-20261023-031725/TASK-WF-specR1-20261023-031725.md ; Tier-1 card /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/t1-card.md ; coverage matrix /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/artifacts/coverage-matrix.yaml ; prior cycle merged verdict /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-spec-20261022-211556-20261022211900/adversarial/merged-verdict.yaml ; target files under /config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/ (pull-sync-framework.yml, boundary-guard.yml, test.yml, README.md), /config/workspace/IronClaude/.dev/worktrees/ci-followup/scripts/README.md, /config/workspace/IronClaude/.dev/worktrees/ci-followup/src/superclaude/pr_submit/ci.py, /config/workspace/IronClaude/.dev/worktrees/ci-followup/tests/swarm/test_merge_boundary_guards.py.

Your lens: plan logic and whether every acceptance bullet FAILS on a wrong edit and PASSES a correct one (check each bullet both ways). Confirm or reject Tier-1 claims C1-C7 with your own citations. Verify each of the 18 prior findings (M-01..M-18 in the prior merged verdict) is actually fixed in this tasklist; list any that are not.

## T1 card excerpt

- C1 (Task 9, Constraints "Necessary deviation"): the tooling-output exclusion (`.dev/reflect/`, `.dev/troubleshoot/`, `.dev/workflow/`) departs from source:39 ("only .github/workflows/, scripts/README.md and the plan package folder may differ"). It is disclosed with a reason, as source:70 asked. Check that it cannot hide a real product edit (those roots hold no product files). Severity low.
- C2 (Task 1, Task 9): converting `git status --porcelain -uall -z` to "one path per line" is underspecified for renames, where -z emits two NUL-separated paths. Severity low.
- C3 (Task 5 Warning bullet): the acceptance check requires the literal word `advisory` on the `::warning` line, but the instruction only says "advisory wording". A correct reword without that word fails. Severity low.
- C4 (Task 6, "the file contains no `<` placeholder"): wording is ambiguous; the intended check is that the edited workflow contains no `<` character (base has 0). Severity low.
- C5 (Task 6 stub run (d)): the push runs before `gh pr list`, so a failing `gh` leaves the branch pushed with no pull request but the step red. The spec's intent (fail closed, visible) is met; check the reviewers agree. Severity low.
- C6 (Depends on lines): Task 6 -> Task 3, Task 7 -> Task 2, Task 8 -> Task 7, Task 9 -> Task 8; Task 9 also needs Task 3's artifact and Task 8 needs Tasks 5 and 6, stated in the bodies with the "number order" rule in Constraints. Check this satisfies source:40 and source:82.
- C7 (Prior findings): spot-check that M-01..M-18 of the prior merged verdict are each addressed (M-07 durable record, M-08 fail-closed, M-09 run (b), M-10 whole document, M-06 Decision line, M-05 scope parsing).

## Grounding hunks

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/boundary-guard.yml:1-98 (read it yourself)

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/pull-sync-framework.yml:1-112

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/test.yml (Upload coverage to Codecov step)

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/scripts/README.md:1-67

## Coverage slice

Rows in /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/artifacts/coverage-matrix.yaml. Unmapped (containment < 0.6): INF-001, INF-003, INF-023, INF-037, INF-040, INF-042, INF-045, INF-050, INF-057, INF-062. You own plan-logic rows: INF-037, INF-041, INF-046..INF-069 (Review Feedback).

## Output (your final message is ONLY this YAML)

```yaml
reviewer_id: <n>
persona: <persona>
model_class: <class>
findings:
  - id: R<n>-<k>
    kind: coverage_gap | lexical_miss_confirmed | scope_creep | ordering | ambiguity | unworkable_check | card_claim_rejected | other
    severity: high | medium | low
    tasks: [<Task numbers or CON-n>]
    claim: <one or two sentences>
    evidence: [<file:line you Read>, ...]
    card_ref: <C1..C9 or null>
    recommendation: <concrete change to the tasklist>
    confidence: <0.00-1.00>
unmapped_row_verdicts:
  - {row: INF-001, verdict: covered | partial | gap, where: <Task/CON or null>}
overall_verdict: ready | ready_with_notes | not_ready
self_confidence: <0.00-1.00>
self_audit: <what you checked, required if findings is empty>
```
