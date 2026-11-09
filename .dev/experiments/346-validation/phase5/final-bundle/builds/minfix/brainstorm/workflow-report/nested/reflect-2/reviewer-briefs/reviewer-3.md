# Reviewer 3 brief (persona: refactorer; UC-1 pre-execution audit of a plan against its spec)

Audit target: plan .dev/tasks/to-do/TASK-WF-spec-20261108-181543/TASK-WF-spec-20261108-181543.md against spec .dev/tasks/to-do/TASK-WF-spec-20261108-181543/source.md. Read both in full. You are read-only: return findings, do not write files.
Persona instruction: Check task order, dependencies, task size and independence, file paths (repo-relative, no .claude/ outputs), and whether any acceptance criterion cannot pass as written (for example contradictions between tasks or with repo tests such as tests/skills/test_worker_contract.py).

## T1 card excerpt

## Structural / tech debt (refactorer slice)

- Task granularity: Tasks 1-3 all edit one script and one test file in sequence; each has its own acceptance tests, so each stays independently reviewable.
- Absolute source paths appear in Task 8 (plan line 160) because the owner ruling names files outside the repo, two of them under /tmp. Risk: /tmp files may be gone before implementation; Task 8 stops as blocked rather than reconstructing.
- Task 7 test depends on commit 95f2c6e4 being in the clone (verified present now: `git cat-file -t 95f2c6e4` = commit; 472 lines).


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T18:21:40Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bs346-minfix projectPath=/home/coder/workspaces/worktrees/IronClaude/bs346-minfix

### .dev/tasks/to-do/TASK-WF-spec-20261108-181543/TASK-WF-spec-20261108-181543.md:1-175

(the plan; Read it from disk with line numbers)

### .dev/brainstorms/346-minfix/workflow-report/nested/reflect-2/artifacts/coverage-matrix.json

(deterministic containment matrix: 142 inferred rows, 104 matched, 38 unmapped)

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| source.md section 3 (3.1-3.4) | Tasks 1-7 | covered except INF-032 | coverage-matrix.json |
| source.md section 4 | Tasks 7-8 | covered | coverage-matrix.json |
| source.md sections 1, 2, 5, 6, 7 | n/a | out of declared scope (plan line 19) unless a requirement constrains sections 3-4 | coverage-matrix.json |
