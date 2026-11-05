# Reviewer 2 brief — persona: qa (model class: haiku alias = glm-5.3)

Mode: UC-1 pre-execution. Audit the proposed tasklist `.dev/tasks/to-do/TASK-WF-renameTheScIssue-20261104-174359/TASK-WF-renameTheScIssue-20261104-174359.md` against its spec `.dev/tasks/to-do/TASK-WF-renameTheScIssue-20261104-174359/source.md`. Lens: coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also check that every acceptance criterion is observable and would actually prove its requirement. Classify each finding (authorized | necessary | drift | regression, or grounding gap), grade it blocking or minor, and cite file:line for every claim. Read-only: return findings as text; do not write files.

## T1 card excerpt

Pass 1 parsed 0 requirement IDs (the spec has no R-/REQ-/SPEC-/T- tokens). Pass 2 inferred 9 quote-pinned rows (artifacts/inferred-requirements.json), all citing source.md:1. The deterministic containment matcher (artifacts/coverage-matrix.json) matched all 9: INF-001 and INF-002 -> Task 1; INF-003 and INF-006 -> Task 2; INF-005, INF-007, INF-008 -> Task 3; INF-004 and INF-009 -> Task 4. coverage_pct (parsed) = null; coverage_pct_union = 1.0; coverage_degraded = parsed-sparse (9 inferred > 0 parsed).

INF-004 ("the developer and user guide rows"): the plan edits neither guide. Evidence: `grep -n -i issue` on docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md finds no /sc:issue row (its `summary.md` hits at lines 1178 and 1239 are unrelated `/sc:summary` examples); docs/user-guide/commands.md line 115 and lines 347-380 name no summary file. Task 4 records this check as ./artifacts/t4-guides.log. Classified as a documented necessary deviation, not a coverage gap.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T17:46:40Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command projectPath=/home/coder/workspaces/worktrees/IronClaude/feat-sc-issue-command

### .dev/tasks/to-do/TASK-WF-renameTheScIssue-20261104-174359/source.md:1
(whole spec body; one paragraph, 1 line — Read the file in full.)

### .dev/reflect/pre-renameTheScIssue-20261104174640/artifacts/coverage-matrix.json:1-
(deterministic containment matcher output — Read the file.)

### .dev/reflect/pre-renameTheScIssue-20261104174640/artifacts/inferred-requirements.json:1-11
(the 9 inferred rows with verbatim quotes.)

### tests/skills/test_issue_protocol.py:134
```python
        for pattern in ("refs/*.md", "templates/*.md", "scripts/*.py")
```

### docs/user-guide/commands.md:115
```markdown
| [`/sc:issue`](#scissue---github-issue-claim-and-create) | Claim a GitHub issue (assign, accuracy check, summary, next-step prompt) or create a templated issue | `issue.md` | Yes (posts to GitHub; writes `.dev/issues/`) |
```

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-001 .. INF-009 (all rows) | Tasks 1-4 | covered (containment >= 0.6) | artifacts/coverage-matrix.json |
| INF-004 developer and user guide rows | Task 4 | covered by a recorded no-change check | docs/user-guide/commands.md:115 |
