# Diagnosability Context Card

**Issue**: PR #359 round 2: escaped [[, process substitution before python3, backticks in $(( ))
**failing_component**: src/superclaude/hooks/scripts/block-bare-python.sh (awk scanner: endword, cmdchar, arithchar)
**Verdict**: partial
**Complexity**: trivial (score 0: single file, deterministic, type bug)
**Hard-stop fired**: false
**Round**: 0 of 3 (discriminator-required: no; counter not incremented)
**Captured bytes (failing run)**: n/a (audit-time only)

## 3-W's coverage
| W | Answerable | Evidence |
|---|---|---|
| When | yes | deterministic (tier1-observation.md) |
| Where | yes | trace-probe.out: no word / printf / echo chosen |
| Why | yes | chosen word plus the scanner lines read |

## Branch A — Log-call inventory
Total 15 hits; the scanner's only output is the matched word at :125. `degraded`: true.

## Branch B — Log-config reachability
LC_ALL=C only; block message reaches_sink, matched-word print filtered_out. `degraded`: true.

## Sufficiency rubric application
Row fired: S1-equivalent (deterministic, directly traced); S14 not applicable. Capped at partial by the degradation rule (Grep/Read discovery).

## Implication for diagnosis confidence
Existing instrumentation: the hook reports only a matched word.
Gap: closed by the read-only scanner-copy trace (trace-probe.sh).
Consequence: all three mechanisms observed directly; partial is a discovery-tool cap.
Next step: proceed to hypothesis formation; no instrumentation needed.

## Tasklist reference
/home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/troubleshoot/bug-pr359-round2-hook-findings-20261104153447/diagnosability-tasklist.md
