# Diagnosability Context Card

**Issue**: PR #359 round 3: python3() function definition blocked; {fd}> redirection hides python3
**failing_component**: src/superclaude/hooks/scripts/block-bare-python.sh (awk scanner: endword, cmdchar redirection branch)
**Verdict**: partial
**Complexity**: trivial (score 0)
**Hard-stop fired**: false
**Round**: 1 of 3 (discriminator-required: yes — two surviving producers, one per finding)
**Captured bytes (failing run)**: n/a (audit-time only)

## 3-W's coverage
| W | Answerable | Evidence |
|---|---|---|
| When | yes | deterministic |
| Where | yes | trace-probe.out: cmdword=python3 (definition) / cmdword={fd} |
| Why | yes | chosen word plus scanner lines 206, 216-219 |

## Branch A — Log-call inventory
12 hits; only the matched word is printed (:130). `degraded`: true.

## Branch B — Log-config reachability
Block message reaches_sink; allow path silent. `degraded`: true.

## Sufficiency rubric application
Row fired: S1-equivalent (deterministic, traced); S14 not applicable; capped at partial (Grep-only discovery).

## Implication for diagnosis confidence
Existing instrumentation: matched word only. Gap closed by the read-only scanner-copy trace. Both mechanisms observed directly. Proceed; no instrumentation needed.

## Tasklist reference
/home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/troubleshoot/bug-pr359-round3-hook-findings-20261104164446/diagnosability-tasklist.md
