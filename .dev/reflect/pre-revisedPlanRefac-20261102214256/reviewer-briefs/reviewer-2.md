# Reviewer 2 brief: qa lens (model class: haiku slot)

Mode: UC-1 pre-execution. You audit a PROPOSED plan (tasklist) against its driving spec, read-only. Do not run commands. Return findings only.

Spec: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/source.md
Tasklist under review (read in full): /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md
Coverage matrix: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/reflect/pre-revisedPlanRefac-20261102214256/artifacts/coverage-matrix.json
Inferred requirement rows: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/reflect/pre-revisedPlanRefac-20261102214256/artifacts/pass2-inferred.yaml

Your lens: coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Check that each task's acceptance criteria actually prove the requirement they cover (observable, checkable, not vacuous, not able to pass while the requirement fails), especially the regression test for scripts/eval_runner.py and the zero-skip rule. Classify each divergence under the 4-category taxonomy with a one-line rationale and a file:line citation.

## T1 card excerpt

Verbatim from /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/reflect/pre-revisedPlanRefac-20261102214256/t1-card.md, section "Coverage section (qa lens)":

- Pass 1 parsed IDs: 0. Pass 2 inferred rows: 41 (artifacts/pass2-inferred.yaml), including one or more rows per D-001..D-014. coverage_degraded: parsed-sparse, so a Tier 1 stop is forbidden.
- Containment match (artifacts/coverage-matrix.json): 36 of 41 matched; coverage_pct_union 0.878; coverage_pct null; S_dev_density 0.122.
- The 5 lexically unmatched rows, content-level disposition (all COVERED): INF-010 (Constraints staging bullet plus Task 7/8 staging criteria); INF-011 (first Constraints bullet names the superseded plan); INF-012 (every task names the D-ids it resolves); INF-016 (Search B in Constraints, Task 1, Task 8); INF-039 (Constraints "recorded only. No task moves, removes or edits them").
- Content level: 41 of 41 covered; the open items are findings, not coverage gaps.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-02T21:43Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths projectPath=/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths

### .dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/source.md:1-1 (full spec body)

The spec is a single line; read the file in full (it is under 400 lines). It names the original obligations, two owner decisions, and deviations D-001..D-014.

### tests/troubleshoot/backtest/test_git_replay_integration.py:56-68

```python
pytestmark = pytest.mark.skipif(
    _GIT_UNAVAILABLE or bool(_MISSING),
```

### tests/skills/test_implement_retry_revert.py:357

```python
@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
```

## Coverage slice

All 41 rows of artifacts/coverage-matrix.json are yours (match_method, best_task and best_ratio per row). The 5 rows with match_method "none" are INF-010, INF-011, INF-012, INF-016, INF-039.
