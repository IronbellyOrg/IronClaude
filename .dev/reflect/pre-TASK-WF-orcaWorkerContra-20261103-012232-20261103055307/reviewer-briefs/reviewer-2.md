# Reviewer 2 brief (persona: qa)

## T1 card excerpt

## Coverage and acceptance (qa slice)
- Scope decision. The plan is the static half of P0 (`TL:19`). The spec now says each phase's plan has a static part and a live part, with the owner's commit and install in between (`SRC:238`). Classification: authorized scope limit. AC-0.4, AC-0.5, AC-0.6 and the 7.2 live check are deferred to the P0 live plan by that rule.
- Low union coverage is mostly deferral plus identifier-style citation. Tasks 1 and 2 name rules by WC identifier and section ("Section 2.3 in full", `TL:56`), so containment under-scores rows such as INF-013 (WC-2) and INF-029 (git ownership). By meaning these rows are assigned to `WORKER-CONTRACT.md`.
- Unverified: whether the eleven-check static report (`TL:154`) is enough for the live plan to cite. The spec's phase report is written by the live plan (`SRC:238`), but no line says how the static report's results carry into it.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-03T05:53:07Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:1-159
The full tasklist under review (Read it whole).

### .dev/reflect/pre-TASK-WF-orcaWorkerContra-20261103-012232-20261103055307/artifacts/grounding-hunks.md
Wave 1A grounding hunks H1-H12: install_core.py KNOWN_CORE_FILES (H1-H2), the set-equality test (H3), build_superclaude_plugin.py core grep (H4), plugins/superclaude/core listing (H5), Makefile verify-sync (H6), the CLAUDE.md level-table test (H7), no `## Unattended mode` sections today (H8), git/gh write-verb hit counts (H9), executor rules (H10), test dirs (H11), Orca install path (H12).

### /home/coder/.claude/skills/sc-implement-protocol/SKILL.md:79-97
Executor rules that decide severity: Depends-on is ignored and tasks run in source order (79, 97). Grade blocking findings against these rules, not against an imagined dependency-driven executor.

### /home/coder/.claude/skills/sc-implement-protocol/refs/qa.md:40-70
Executor QA: which finding types are blocking (for example a breach of a quoted constraint or task instruction). A finding is blocking only if this QA or the FINAL review would fail the task or block archiving.

### /home/coder/.claude/skills/sc-implement-protocol/refs/qa.md:276-312
Halt paths, the no-prompt rule (288) and the FINAL derived test.

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:1-10
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:11-16
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:17-50
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:51-130
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:131-186
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:187-202
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:203-214
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:215-239
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:240-372
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:373-384
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:385-397
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:398-423
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:424-451
Spec body section (Read these lines).

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

### .dev/reflect/pre-TASK-WF-orcaWorkerContra-20261103-012232-20261103055307/artifacts/coverage-matrix.yaml
Wave 1B coverage matrix: 105 inferred rows, deferral targets, in-scope unmatched rows.

## Coverage slice

| Requirement / Task | Status | Grounding |
|---|---|---|
| Static P0 scope: section 2.1-2.3 contract content, AC-0.1, AC-0.2, AC-0.3, AC-0.7, AC-0.9, AC-C1 to AC-C6 | in scope; see coverage-matrix.yaml transparency.in_scope_unmatched | .dev/reflect/pre-TASK-WF-orcaWorkerContra-20261103-012232-20261103055307/artifacts/coverage-matrix.yaml |
| AC-0.4, AC-0.5, AC-0.6, 7.2 live check, WC-1 timing | deferred to the P0 live plan (spec section 6 last paragraph) | .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:238 |
| P1-P4 rows | deferred to later phase plans | .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:19 |
