Implement docs/designs/surgical-remediation.md as corrected by .dev/issues/624/accuracy-check.md and .dev/issues/624/analysis/analyze-sc-workflow-protocol.md (the reflect contract bump 1.8.0 to 1.9.0 has consumers: src/superclaude/cli/reflect/panel_lint.py and two tests under tests/cli/reflect/; the workflow contract stays at 1.1; at least seven superseded packages, not four, sit in .dev/tasks/to-do/). Code: src/superclaude/skills/sc-workflow-protocol/, src/superclaude/skills/sc-reflect-protocol/, src/superclaude/cli/reflect/, src/superclaude/skills/sc-implement-protocol/, src/superclaude/commands/workflow.md, src/superclaude/core/HOW-WE-WORK.md, .dev/README.md

## Revision 1

Supersedes TASK-WF-implementDocsDes-20261120-005507. Review chain: /home/coder/workspaces/worktrees/IronClaude/issue-624/.dev/reflect/pre-implementDocsDes-20261120005835/REPORT.md (verdict not-ready, 12 blocking findings in the union of three reviewer cards). Fix map: one Edit per finding group, listed in ./artifacts/revision-log.md. Only blocking findings were repaired.

## Revision 2

Supersedes TASK-WF-implementDocsDes-20261120-020554 (archived). Review chain: the pre-execution review report and the re-review of TASK-WF-implementDocsDes-20261120-020554 (one new blocking finding, N2: Wave 5 could overwrite review_verdict). Fix map in ./artifacts/revision-log.md. Only the blocking finding was repaired.

## Revision 3

Supersedes TASK-WF-implementDocsDes-20261120-021216 (archived). Review chain: re-review 3 of that package (ready, 0 blocking; 2 Medium and several Medium or Note findings kept as follow-ups). This cycle repaired the Medium findings by owner order. Fix map in ./artifacts/revision-log.md.
