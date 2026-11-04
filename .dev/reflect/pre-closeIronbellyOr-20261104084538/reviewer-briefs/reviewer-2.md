# Reviewer 2 brief: persona qa, model haiku (UC-1 pre-execution plan review)

Audit target: the plan `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/TASK-WF-closeIronbellyOr-20261104-084334.md` (121 lines; Read it in full) against its spec `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/source.md`. Lens: coverage, acceptance criteria, test surface. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also judge whether each task's acceptance criteria actually prove the change (a check that cannot fail is a weak verifier). Classify each divergence as authorized | necessary | drift | regression (plan-vs-spec), or route it to a grounding gap.

## T1 card excerpt

From `reflection-card.yaml` (verbatim):

```yaml
  - id: F-1
    kind: coverage-gap
    claim: "`make verify-sync` (required by the source checks) appears in no task's acceptance criteria."
  - id: F-2
    kind: weak-verifier
    claim: "Tasks 3 and 4 use `make lint` as an acceptance check for Markdown edits, but `make lint` runs only lint-architecture and `ruff check .` (Makefile:48-50), so it does not check the docs or CHANGELOG."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T08:47:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin

### .dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/source.md:1

The whole spec is this one line (Read it verbatim; it is the full requirement source). It names: the design file, the ledger decision and its alternative, five delivery files with their scope notes, the no-change list, the checks list (pytest on three test paths, `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync`, `grep -rn 'six plugins' docs/` empty), and the non-blocking manual AC-M1 in a throwaway HOME.

### Makefile:48-50

```make
lint: lint-architecture
	@echo "Running linter..."
	uv run ruff check .
```

### tests/cli/test_install_user_setup.py:73-98, 175-242

Existing tests the plan extends (`test_settings_defaults_fill_only_missing_values`, `_plugin_home`, `test_plugins_install_missing_enabled_defaults`, `test_plugins_skip_already_installed`, `test_plugin_failures_and_time_limit_never_fail_install`). Read them and check that each planned test leg (T1, T2, T3/T4, T5, T5c) can be written against them and would fail on the current code where the plan says it should.

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-004 defaults three entries | Task 1 | covered (ratio 1.0) | source.md:1 |
| INF-006 tests T1, T2, T3/T4, T5, T5c | Task 1 | covered (ratio 0.86); T5/T5c actually in Task 2 | source.md:1 |
| INF-007 installation.md | Task 3 | covered | source.md:1 |
| INF-008 CHANGELOG | Task 4 | covered | source.md:1 |
| INF-010 checks list | Task 2 | covered (ratio 0.72) | source.md:1 |
| INF-011 manual AC-M1 | Task 5 | covered | source.md:1 |

Return a reviewer card (YAML) with: reviewer, persona, model, findings (id, claim, evidence as file:line, deviation_class or grounding_gap, severity blocking|minor, recommendation), self_reported_confidence. Do not write files.
