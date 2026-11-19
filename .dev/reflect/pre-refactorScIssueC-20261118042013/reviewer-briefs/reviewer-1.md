# Reviewer 1 brief (persona: analyzer; UC-1 pre-execution review of a workflow plan)

You are a read-only reviewer. Audit ONLY the plan and the hunks below; do not run commands, do not edit anything. Return one card as YAML text (the orchestrator saves it).

Inputs (repo root: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline):
- Spec (driving request): .dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/source.md
- Plan under review: .dev/tasks/to-do/TASK-WF-refactorScIssueC-20261118-041634/TASK-WF-refactorScIssueC-20261118-041634.md

Lens: does the plan cover every requirement of the spec, with no silent drops, and are the task bodies and acceptance criteria correct against the real code? Check each plan claim against the files; cite file:line for anything you assert.

## T1 card slice
Five inferred requirements INF-001..INF-005 all map to tasks (union coverage 5/5). Candidate findings: C-1 (bare --submit now runs at full: derived, not authorized by the spec), C-2 (ship-gate sentence kept while full becomes default), C-3 (claim.md final output text wrong for full), C-4 (test_launch.py named in spec but not edited).

## Codegraph run state
index_state: fresh, checked_at: 2026-11-18T04:16:47Z, worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/RefactorIssueClaimPipeline. You have no codegraph tool unless your tool list shows one; use Grep and Read otherwise.

## Grounding hunks
- src/superclaude/skills/sc-issue-protocol/refs/chains.md:11 row `| Feature, simple | /model claude-gw-tier2 | 1. /sc:brainstorm "<topic> @<S>" --depth quick (no --handoff) <br>2. /sc:workflow <brainstorm dir>/merged-requirements.md --depth quick --handoff none <br>3. /sc:implement <plan path printed by step 2> |`
- src/superclaude/commands/issue.md:16 ends the level list with "`worktree` (the default) stops at a plan a human approves, `full` also implements without a commit or a push"; line 43 Options row `--pipeline` default `worktree`; line 57 STOP rule: "`--submit` with a value, or without `--pipeline full`: STOP `E-SUBMIT-NEEDS-FULL`".
- src/superclaude/skills/sc-issue-protocol/SKILL.md:17 "`worktree` (default) plans and waits for approval"; line 154 error-table row naming `E-SUBMIT-NEEDS-FULL`.
- src/superclaude/skills/sc-issue-protocol/refs/claim.md:79-82 (Wave 5 steps 1-4; step 4 says "where `<L>` is the `--pipeline` value"), and line 142: for `launched` the printed text begins "It stops at the plan boundary and waits; run the printed implement command ..." followed by a separate sentence for `full`.
- tests/commands/test_issue_command.py:113 `assert rows["--pipeline"][2] == "`worktree`"`; tests/skills/test_issue_protocol.py:653-667 asserts 3 brainstorm steps across 6 rows.
- src/superclaude/cli/issue_watch/launch.py:33 PROMPT_PATTERN `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`; tests/issue_watch/test_launch.py:929-939 pin `build_claim_prompt(9) == "/sc:issue --claim 9 --pipeline none"`.

## Card format
```yaml
reviewer: 1
persona: analyzer
verdict: pass | pass-with-findings | fail
confidence: <0-1>
coverage_assessment: <text>
findings:
  - id: F1
    severity: blocking | medium | note
    claim: <one sentence>
    evidence: <file:line, quoted>
    class: coverage-gap | wrong-claim | scope-drift | missing-dependency | other
    tag: grounded | INFERRED
```
Tag every claim grounded or [INFERRED]. A zero-finding review must say what you checked.
