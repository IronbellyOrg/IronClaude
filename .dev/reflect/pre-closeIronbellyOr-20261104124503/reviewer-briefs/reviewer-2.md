# Reviewer 2 brief: persona qa, model haiku-slot (UC-1 pre-execution plan review)

Audit target: the plan `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/TASK-WF-closeIronbellyOr-20261104-124207.md` (Read it in full) against its spec (below, in full) and the design `.dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md` (Tests and Acceptance Criteria at its lines 263-289). Lens: coverage, acceptance criteria and verification. Assume mistakes exist. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also check: does every acceptance criterion describe an observable, checkable outcome; is every spec check (pytest set, make lint, ruff format --check, make verify-sync, six-plugins grep, AC-M1 non-blocking) owned by some task; would the named tests actually fail on the defect they pin? Grade each finding blocking or minor (blocking = wrong behaviour, false claim, missing required deliverable, or a security/data-loss risk).

## T1 card excerpt

From `reflection-card.yaml` (verbatim):

```yaml
  - id: F-1
    kind: coverage-by-paraphrase
    claim: "The eight containment-unmapped rows are stated in the plan outside a single task's literal wording ... The matcher scores single tasks only."
  - id: F-3
    kind: acceptance-ambiguity
    claim: "Task 2's 'at most 5 changed lines' is ambiguous: the design's shape adds one line and changes three (git counts 4 insertions plus 3 deletions)."
  - id: F-5
    kind: cohesion
    claim: "The manual install proof (AC-M1..M3) sits in Task 4, the CHANGELOG task; M1b/M1c need a Claude session in a throwaway HOME, which likely has no credentials, so they will probably be UNVERIFIED."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T12:45:03Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin

### .dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/source.md:1

The spec is one line (whole file). Read it in full; it is the authoritative requirement list.

### tests/cli/test_install_user_setup.py:73-98, 175-242

Existing tests the plan extends: fill-only-missing (:73-98), `_plugin_home` (:175-179), install-missing-enabled-defaults (:182-209), skip-already-installed (:212-226), failures-and-time-limit (:229-242). Read them.

### artifacts/coverage-matrix.json

`.dev/reflect/pre-closeIronbellyOr-20261104124503/artifacts/coverage-matrix.json`: 17 inferred rows with verbatim quotes, containment match results and ratios.

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-002 env lite filled only when unset | none (Task 1 + Constraints) | unmapped by containment | source.md:1 |
| INF-004 no pluginConfigs; ledger on documented | Task 3 | covered | source.md:1 |
| INF-006 map + subagent documented | Task 3 | covered | source.md:1 |
| INF-009 docs: change mode, opt out | Task 3 | covered | source.md:1 |
| INF-010 three defaults entries | Task 1 | covered | source.md:1 |
| INF-012 tests T1-T5c with lite | Task 1 | covered | source.md:1 |
| INF-013 docs + CHANGELOG files | Task 3 | covered | source.md:1 |
| INF-015 checks list | none (split Task 2/3/4) | unmapped by containment | source.md:1 |
| INF-016 manual AC-M1 throwaway HOME, non-blocking | Task 4 | covered | source.md:1 |

Return a reviewer card (YAML) with: reviewer, persona, model, verdict, findings (id, claim, evidence as file:line, deviation_class or grounding_gap, severity blocking|minor, recommendation), self_reported_confidence. Do not write files.
