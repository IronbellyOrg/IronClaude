# Reviewer 2 brief: qa lens (model class: haiku slot)

Mode: UC-1 pre-execution. You audit a PROPOSED plan (tasklist) against its driving spec, read-only. Do not run commands. Return findings only; the orchestrator persists them.

Spec: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/source.md
Tasklist under review (read it in full): /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md
Coverage matrix: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/reflect/pre-refactorIronClau-20261102175540/artifacts/coverage-matrix.json

Your lens: coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also check that each task's acceptance criteria actually prove the requirement it covers (observable, checkable, not vacuous). Classify each divergence under the 4-category taxonomy (authorized expansion, necessary deviation, drift, regression) with a one-line rationale and a file:line citation.

## T1 card excerpt

Verbatim from /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/reflect/pre-refactorIronClau-20261102175540/t1-card.md, section "Coverage section (qa lens)":

- Pass 1 parsed IDs: 0 (source.md has no R-/REQ-/SPEC-/T- labels). Pass 2 inferred rows: 11 (artifacts/pass2-inferred.yaml). coverage_degraded: parsed-sparse (Step 1B.2b), so a Tier 1 stop is forbidden.
- Containment match (artifacts/coverage-matrix.json): 10 of 11 matched, coverage_pct_union 0.9091, coverage_pct null (no parsed rows), S_dev_density 0.0909.
- INF-011 "never stage .claude mirrors" is lexically unmatched (best Task 3, ratio 0.5). Content-level disposition: COVERED. The plan Constraints (line 20) forbid staging any `.claude/` path except `.claude/settings.json`, and Task 6 and Task 7 acceptance criteria require `git diff --cached --name-only` to list no other `.claude/` path (plan lines 116-122, 134-137). The word "mirrors" is missing, not the obligation.
- Content-level check of the matched rows: INF-005 is matched lexically, but the plan answers it with THREE classes, not the two the source names (see F1). INF-007 is covered by "unchanged" assertions, not by a test run (see S2).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-02T17:55Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths projectPath=/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths

### .dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/source.md:1-1 (full spec body)

```text
Refactor IronClaude to Orca's default worktree paths: replace the .dev/worktrees rule in CLAUDE.md and every tracked file that encodes .dev/worktrees or git worktree add (git grep -E '\.dev/worktrees|git worktree add' -- ':!.dev'). Classify each hit as project worktree (move to Orca-created worktrees at Orca's default location) or internal temporary checkout used by a CLI or test (keep working without Orca). Also tighten the CLAUDE.md rule: SuperClaude upstream is never pushed to or interacted with. Source of truth is src/superclaude; run make sync-dev; never stage .claude mirrors.
```

### .dev/reflect/pre-refactorIronClau-20261102175540/artifacts/pass2-inferred.yaml

The 11 quote-pinned inferred requirement rows (INF-001 to INF-011), each with a verbatim quote and the citation source.md:1.

## Coverage slice

| Requirement | Matched task | Status | Grounding |
|---|---|---|---|
| INF-001 overall goal | Task 1 | containment 0.857 | source.md:1 |
| INF-002 replace CLAUDE.md rule | Task 2 | containment 1.0 | source.md:1 |
| INF-003 every tracked file | Task 1 | containment 0.75 | source.md:1 |
| INF-004 the git grep hit set | Task 1 | containment 1.0 | source.md:1 |
| INF-005 classify each hit (two classes) | Task 1 | containment 0.842 | source.md:1 |
| INF-006 project worktree to Orca | Task 2 | containment 0.889 | source.md:1 |
| INF-007 internal checkout keeps working | Task 1 | containment 0.889 | source.md:1 |
| INF-008 tighten upstream rule | Task 3 | containment 0.9 | source.md:1 |
| INF-009 source of truth src/superclaude | Task 5 | containment 1.0 | source.md:1 |
| INF-010 run make sync-dev | Task 6 | containment 1.0 | source.md:1 |
| INF-011 never stage .claude mirrors | none (lexical) | content-level covered per T1 card | source.md:1 |
