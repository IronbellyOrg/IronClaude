# Diagnosability Context Card

**Issue**: install_core_files skips files
**failing_component**: src/superclaude/cli/install_core.py
**Verdict**: partial
**Complexity**: trivial (score 0)
**Hard-stop fired**: true (counter update unavailable, not insufficient/non-trivial branch)
**Round**: uncommitted; prior value 1 of 3
**Captured bytes (failing run)**: n/a (audit-time only)

## 3-W's coverage
| W | Answerable | Evidence |
|---|---|---|
| When | no | No incident output or timestamped signal captured. |
| Where | partial | Static skip branch and caller output sites localized; incident site unknown. |
| Why | partial | Source exposes the preservation guard, but actual destination state and force value unobserved. |

## Branch A - Log-call inventory
Seven returned-message / console-output signal groups, including two caller emissions and diagnostic construction. Zero structured logger calls or reporter initializations identified. One exception handler captures exception text in the returned failure message; minimal richness. All captured_bytes null. degraded: true.

## Branch B - Log-config reachability
No controlling log-level configuration identified in bounded fallback searches. Returned text and caller console output are not structured logger calls. All nine inventoried source coordinates have reachability unknown. degraded: true.

## Sufficiency rubric application
S14 not evidenced: no demonstrated intermediary lost or substituted the disputed datum. Console-only diagnostics fit the deterministic S9 analogue; degraded discovery independently caps verdict at partial. Complexity score 0: no intermittent, performance, security or multi-domain signals in the request. discriminator-required: yes because the failing-run observation corpus is empty. No categorical producer rows and no numeric limit, so no producer pairs or brackets apply.

## Implication for diagnosis confidence
Source and documentation explain a preservation policy, not this incident.
The command, output, destination state and force argument are missing.
The required locked counter update was denied by session permissions; it was not retried or bypassed.
Stop before hypothesis formation; preserve pending evidence and publish a blocked diagnostic report.
No installation, test, or instrumentation was executed.

## Tasklist reference
.dev/troubleshoot/untyped-install-core-files-skips-files-20261031153823/diagnosability-tasklist.md
