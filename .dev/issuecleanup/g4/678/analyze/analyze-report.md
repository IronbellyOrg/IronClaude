# Architecture analysis: launch-level guard

## Scope and method
Command: `/sc:analyze src/superclaude/hooks/scripts/launch-level-guard.sh --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/678/analyze`.
Read-only static architecture analysis of the single Bash guard, with its design, tests and historical observation as supporting evidence. No source changes, dynamic runs, installation or GitHub writes.
Codegraph: index_state=fresh, checked_at=2026-11-24T13:46:23Z; degraded: graph:empty.
The scoped graph layout found only JavaScript; the Bash target had no indexed entry, so Grep and Read supplied the source evidence. No missing graph row was treated as proof of absence.

## Severity-rated findings
1. Medium, confirmed classification gap: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:456-468 sets separate executable and launch-flag indicators; :510 requires both before adding ESCAPE. A plain executable plus prompt does not meet that condition. ESCAPE is denied at all four levels at :818; the missing classification, not the denial table, is the problem.
2. Medium, conditional identity gap: the same source at :367-368 accepts a new prompt with no binding and no launch marker; :391-395 permits unbound tool calls. This supports the issue's concern about a child session, but an unrestricted child in a real governed launch remains UNVERIFIED. The historical isolated setup at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/442/scripts/setup.sh:125-139 installs only a logging probe for PreToolUse, not the enforcing guard.
3. Note, compatibility constraint: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_launch_level_guard.py:3129-3157 covers flagged launches; :3159-3167 explicitly expects discovery and version checks to be allowed. A future executable-wide block must deliberately settle that version-check expectation.

## Metrics and limitations
One production Bash file is the analysis target. Supporting inspection covered its design, guard test table, observation test gate, runbook, archived raw log and result block. No complexity score, coverage percentage or performance measurement was collected. Unit tests and live child-session checks were not run: the task forbids uv and writes outside its report directory. Historical observation data is not a fresh runtime test.

## Recommendations
Keep issue 678 parked and still relevant: its live body records the owner's 2026-11-19 decision not to act now. If separately authorized, first verify child binding and tool enforcement in a disposable governed launch, then fix the shared classifier, update the design and regression table, and repeat observation item 8. Do not describe unrestricted access in the current environment as observed. This analysis authorizes none of those actions.
