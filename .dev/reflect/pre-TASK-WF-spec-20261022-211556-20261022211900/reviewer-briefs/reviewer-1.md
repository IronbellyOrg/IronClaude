# Reviewer 1 brief (persona: analyzer, model class: sonnet)

You are a read-only reviewer in a pre-execution (UC-1) reflection. You audit a proposed tasklist against the spec that drives it. You do not run commands, edit files, or fix anything. Cite only file:line ranges you Read yourself. A claim you cannot cite is dropped. Assume the plan has defects; a zero-finding review must include a self-audit of what you checked.

Inputs: spec /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-spec-20261022-211556/source.md ; tasklist /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/tasks/to-do/TASK-WF-spec-20261022-211556/TASK-WF-spec-20261022-211556.md ; Tier-1 card /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-spec-20261022-211556-20261022211900/t1-card.md ; coverage matrix /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-spec-20261022-211556-20261022211900/artifacts/coverage-matrix.yaml ; target files under /config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/ (pull-sync-framework.yml, boundary-guard.yml, test.yml, README.md), /config/workspace/IronClaude/.dev/worktrees/ci-followup/scripts/README.md, /config/workspace/IronClaude/.dev/worktrees/ci-followup/src/superclaude/pr_submit/ci.py, /config/workspace/IronClaude/.dev/worktrees/ci-followup/tests/swarm/test_merge_boundary_guards.py.

Your lens: plan logic, task ordering, and whether each acceptance bullet would FAIL on a wrong edit (not just pass on a right one). Judge Tier-1 claims C1-C6 independently: confirm, correct, or reject each with your own citations. Check each task's commands for anything that cannot work as written (paths, placeholders, PyYAML 'on' key, git/gh behaviour, stub design).

## T1 card excerpt

- C1 (Task 9, tasklist lines 19 and 146-156): the plan defines the scripts/README.md "one paragraph" as lines 7-12 (sentence plus its bullet list) and leaves lines 3, 14, 16-28, 39 and the Upload Failures section unchanged as listed leftovers. The spec says "Change nothing else in that file" (source.md:35). After the edit, line 3 ("handled by the GitHub Actions workflow described below") and the Required Secrets / Release steps sections will contradict the new paragraph. Interpretation is defensible but the result is an internally inconsistent README; it needs a user decision. Severity medium.
- C2 (Task 5, tasklist line 94): the backslash-before-backtick check is written as inline code containing a backtick (`grep -c '\\`'`), which breaks the Markdown code span and is ambiguous to an executor. Severity medium.
- C3 (Task 6, tasklist line 114): the stub run says "`git` push and `gh` replaced by PATH stubs". The step body also runs `git config`, `git add`, `git diff --cached`, `git commit`; a PATH stub named git must delegate every non-push subcommand to the real git or the run fails for the wrong reason. Not specified. Severity medium.
- C4 (Task 5, tasklist lines 88 and 91): header comment check uses fixed `sed -n '19,20p'`; if the reworded comment changes the line count, the check reads the wrong lines and can pass or fail spuriously. Same for "the two lines starting at 3. **PR-review discipline**". Severity low.
- C5 (Tasks 5-9, tasklist lines 87, 112, 125, 144, 156): `<t1-head>` is a placeholder the executor must replace with the content of ./artifacts/t1-head.txt; not stated explicitly. Severity low.
- C6 (tasklist lines 43, 53, 65, 75, 101, 119, 132, 148): a single linear chain makes Task 3 depend on Task 2, Task 4 on Task 3, Task 6 on Task 5 although they are independent. Spec asks for "real chains where order matters" (source.md:40). Real orders: Task 7 needs Task 2; Task 8 needs Tasks 5, 6, 7; Task 9 needs all. One-name-per-line forces some linearisation, but Task 3 to Task 2 and Task 4 to Task 3 are spurious. Severity low.
- C7 (Task 7, tasklist line 117 onward): the spec offers an alternative "delete the step and its README mentions" if the fork does not use Codecov (source.md:30); "Decisions taken as defaults" (source.md:44) fixes the token path, so no alternative branch is needed. Confirmed covered.
- C8 (Fix 1 consequences, source.md:14): stated verbatim in Constraint bullet 9 and repeated into ./artifacts/t6-fix1-notes.md by Task 6. Covered.
- C9 (Task 3): `can_approve_pull_request_reviews` is the field the workflow-permissions API returns for the "Allow GitHub Actions to create and approve pull requests" setting [INFERRED from API knowledge; Task 3 itself records the raw JSON].

## Grounding hunks

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/boundary-guard.yml:1-98 (read it yourself; lines 19-20 header, 37 job name, 50 ::warning, 66-67 summary item 3, 76 git diff)

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/pull-sync-framework.yml:1-112 (11-12 permissions, 85-112 Commit and Push Changes)

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/.github/workflows/test.yml:42-48 (Upload coverage to Codecov)

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/scripts/README.md:1-39 (publish-pypi text at 3, 5-14, 16-28, 39)

### /config/workspace/IronClaude/.dev/worktrees/ci-followup/src/superclaude/pr_submit/ci.py:19,70-77 (_HUMAN_NAME = "boundary")

## Coverage slice

Rows in /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-spec-20261022-211556-20261022211900/artifacts/coverage-matrix.yaml. Unmapped (containment < 0.6): INF-001, INF-003, INF-037, INF-040, INF-041, INF-042, INF-045. You own rows tied to plan logic: INF-037, INF-041, INF-042 and every Fix 2 row (INF-015..INF-026).

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
