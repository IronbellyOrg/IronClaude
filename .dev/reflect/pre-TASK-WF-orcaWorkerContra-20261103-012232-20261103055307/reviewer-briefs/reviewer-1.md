# Reviewer 1 brief (persona: analyzer)

## T1 card excerpt

## Root cause and deviation (analyzer slice)
- Task 3 asks the executor to decide the plugin copy by reading `scripts/build_superclaude_plugin.py` (`TL:69`). A grep of that script for "core" returns nothing (H4), yet `plugins/superclaude/core/` holds six core files (H5). The evidence that decides the convention may live elsewhere (for example a Makefile plugin target), so the task can reach a conclusion from the wrong file. Candidate class: drift (an incomplete instruction).
- Task 6 requires each allowlisted write-verb hit to carry "the phase that converts its command" (`TL:125`). H9 shows about 121 hits, many in commands that no phase converts: `/sc:pr-submit` and `/sc:git` are never workers (`SRC:61`). The reason format has no slot for "never a worker", so an executor may invent a phase. Candidate class: drift.
- Task 1 adds the `KNOWN_CORE_FILES` entry in the same task that creates the file (`TL:42`). `test_known_core_set_matches_shipped` compares the frozenset with the shipped files (H3, `tests/cli/test_how_we_work_install.py:44`), so the tree stays green. No defect.

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

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:51-130
Spec sections 2.1-2.3 (contract contents).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:215-239
Spec section 6 (phases and the two-part plan rule at 238).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:240-345
Spec section 7 (common checks, 7.2, 7.3 P0 rows, command blocks).

## Coverage slice

| Requirement / Task | Status | Grounding |
|---|---|---|
| Static P0 scope: section 2.1-2.3 contract content, AC-0.1, AC-0.2, AC-0.3, AC-0.7, AC-0.9, AC-C1 to AC-C6 | in scope; see coverage-matrix.yaml transparency.in_scope_unmatched | .dev/reflect/pre-TASK-WF-orcaWorkerContra-20261103-012232-20261103055307/artifacts/coverage-matrix.yaml |
| AC-0.4, AC-0.5, AC-0.6, 7.2 live check, WC-1 timing | deferred to the P0 live plan (spec section 6 last paragraph) | .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/source.md:238 |
| P1-P4 rows | deferred to later phase plans | .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:19 |
