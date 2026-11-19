# Reviewer 3 brief (persona: refactorer; UC-1 pre-execution review of a workflow plan)

You are a read-only reviewer. Audit ONLY the plan and the hunks below; do not run commands, do not edit anything. Return one card as YAML text (the orchestrator saves it).

Inputs (repo root: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline):
- Spec (driving request): .dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/source.md
- Plan under review: .dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/TASK-WF-refactorScIssueC-20261118-041634.md

Lens: scope discipline and consistency. Does the plan do exactly what the spec asks, no more and no less? Look for edits that go beyond the request, for places that state the default level or the simple feature chain that no task updates (search src/, docs/, plugins/, README.md), and for task ordering or dependency mistakes.

## T1 card slice
Candidate findings: C-1 (bare --submit now runs at full, a derived relaxation of a STOP rule), C-2 (ship-gate sentence kept while full becomes default), C-3 (claim.md final output text wrong for full), C-4 (test_launch.py not edited).

## Codegraph run state
index_state: fresh, checked_at: 2026-11-18T04:16:47Z, worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline. Use Grep and Read unless your tool list shows a codegraph tool.

## Grounding hunks
- Places that state the default today: src/superclaude/commands/issue.md:16 and :43; src/superclaude/skills/sc-issue-protocol/SKILL.md:17; docs/user-guide/commands.md:368 and :377; src/superclaude/core/HOW-WE-WORK.md:328 (mirrored byte for byte in plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md); docs/designs/sc-issue-claim-pipeline-flag.md:21 and :43; docs/designs/sc-issue-command.md:64 and :494; docs/designs/issue-watcher.md:41 (dated record, no task edits it); src/superclaude/skills/sc-issue-protocol/templates/next-steps.md:7.
- The simple feature row is src/superclaude/skills/sc-issue-protocol/refs/chains.md:11; the only other place that lists chain rows by name is docs/designs/sc-issue-command.md (Grep "Feature, simple").
- The worktree claim-handoff-planb edits issue.md lines 16 and 43-44, SKILL.md, refs/claim.md and HOW-WE-WORK.md.

## Card format
```yaml
reviewer: 3
persona: refactorer
verdict: pass | pass-with-findings | fail
confidence: <0-1>
coverage_assessment: <text>
findings:
  - id: F1
    severity: blocking | medium | note
    claim: <one sentence>
    evidence: <file:line, quoted>
    class: scope-creep | missed-site | bad-dependency | other
    tag: grounded | INFERRED
```
Tag every claim grounded or [INFERRED]. A zero-finding review must say what you checked.
