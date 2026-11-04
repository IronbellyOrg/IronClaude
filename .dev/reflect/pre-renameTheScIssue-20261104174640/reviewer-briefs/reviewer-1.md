# Reviewer 1 brief — persona: analyzer (model class: sonnet)

Mode: UC-1 pre-execution. Audit the proposed tasklist `.dev/tasks/to-do/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md` against its spec `.dev/tasks/to-do/TASK-WF-renameTheScIssue-20261104-174359/source.md`. Lens: root cause and deviations. Find gaps, wrong instructions, or steps that would make an acceptance criterion fail. Classify each finding (authorized | necessary | drift | regression, or grounding gap), grade it blocking or minor, and cite file:line for every claim. Read-only: return findings as text; do not write files.

## T1 card excerpt

- D-1 (candidate, blocking for the executor's own acceptance): renaming `templates/summary.md` to `templates/issue-summary.md` leaves a stale `.claude/skills/sc-issue-protocol/templates/summary.md`. `make sync-dev` only copies (Makefile:117-123, `cp "$$src" "$$target_dir/"`), never deletes, and `make verify-sync` runs `diff -rq` over each skill dir (Makefile:178), so it reports the orphan and exits non-zero. The coordinator requires verify-sync exit 0. No task removes the stale mirror (deleting a gitignored `.claude/` copy is not staging, so it is allowed).
- D-2 (minor): Task 2 defines `<scope>` as "the main path's last segment", while refs/chains.md:7 already defines `<scope>` as "the main path from the summary". Two meanings of one placeholder in one skill.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T17:46:40Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command projectPath=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command

### Makefile:112-125
```make
	@for skill_dir in src/superclaude/skills/*/; do \
		... find "$$skill_dir" -type f ... -exec sh -c ' ... cp "$$src" "$$target_dir/" ' ...
```

### Makefile:178
```make
			changes=$$(diff -rq --exclude='__init__.py' --exclude='__pycache__' "$$skill_dir" ".claude/skills/$$name" 2>/dev/null); \
```

### src/superclaude/skills/sc-issue-protocol/refs/chains.md:7
```markdown
... `<S>` = `.dev/issues/<N>/summary.md`; `<symptom>` is the bug's one-line symptom from the summary (at least 10 words); `<scope>` is the main path from the summary. ...
```

### src/superclaude/skills/sc-issue-protocol/SKILL.md:86
```markdown
5. **Wave 4, accuracy check and summary.** Spawn `issue-worker-t2`, or `issue-worker-t1` when `scout.md` says `complex`; it writes `<D>/accuracy-check.md`, `<D>/summary.md` (effort in hours) and, when out of date, `<D>/analysis/`.
```

### src/superclaude/agents/issue-worker-t2.md:15
```markdown
The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, `summary.md`, the reports under `analysis/`, ...) are input files ... so a general instruction against writing report or summary `.md` files does not apply to them. ...
```

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-001 rename summary.md to issue-summary.md (template may be renamed) | Task 1 | covered | source.md:1 |
| INF-002 references in SKILL.md, refs/claim.md, refs/chains.md, claim-comment.md, next-steps.md | Task 1 | covered | source.md:1 |
| INF-003 three worker agent files incl. fix-2 paragraph, commands/issue.md Outputs table | Task 2 | covered | source.md:1 |
| INF-006 fix-2 paragraph states the real mechanism | Task 2 | covered | source.md:1 |
