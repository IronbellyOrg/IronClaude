# Gate 2 fix report (cycle 2)

**Date:** 2026-11-20
**Status:** Complete
**Work list:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/qa/qa-synthesis-consolidated-findings-c2.md (BLOCKING only: N-1)

## Fix summary

Blocking findings: 1. FIXED: 1. UNFIXABLE-FROM-EVIDENCE: 0.

## Log

| Finding ID | Synth file and location | Action | Exact change or missing evidence | Evidence used (path:line) |
|---|---|---|---|---|
| N-1 | /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/synthesis/synth-06-conventions-extension-debt-appendix.md, Section 14.3 table, row at line 283 (now lines 283-284) | FIXED | One row split into two. D-18 row: Deferred Because now "No decision found in the files this reference cites (D-18); the guard design says it does not govern such a worker (design :23)"; Revisit When "No revisit trigger found in the files read (Q-11)"; OD-1, OD-3 and the OW:822 trigger removed from it. D-21 row: Deferred Because now "No decision found that leaves the gate prose-only (D-21); the one related owner decision (OD-3) keeps the IR-7 refusal off (`IR7_REFUSE = False`, OW:818-822) until the #442 observations pass"; Revisit When "After the #442 observations pass, for the IR-7 refusal (OW:822); none recorded for the OB-H gate as code". OD-1 dropped (it is the declared L2 limits, design :534). No other synth file repeats the claim: grep of D-18, D-21, OD-1, OD-3, OW:818/822 and "coordinator-started" across synthesis/ found the wrong claim only at this row; synth-06 lines 186, 261, 305, synth-01 line 169, synth-04 line 315 and synth-05 line 88 already say no decision / not governed. | synth-06 D-18 row line 261 and 14.1.1 row line 186 (agree with new text); `/home/coder/.cache/ic-snap-20261120/master/docs/designs/sc-issue-launch-level-hook.md:23` (guard does not govern a coordinator-started worker), `:534` (OD-1 = "Limits", L2 same-user guard); `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:818-822` (IR-7 refusal off, OD-3, `IR7_REFUSE = False`, turn on after #442 observations) |

Status: Complete
