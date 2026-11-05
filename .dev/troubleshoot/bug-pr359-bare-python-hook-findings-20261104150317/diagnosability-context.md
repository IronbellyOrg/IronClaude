# Diagnosability Context Card

**Issue**: PR #359 round 1: hook misclassifies ANSI-C words, wrapper long options and [[ =~ ]] alternation
**failing_component**: src/superclaude/hooks/scripts/block-bare-python.sh (awk scanner, endword/qchar/cmdchar)
**Verdict**: partial
**Complexity**: trivial (score 0: single file, deterministic, no intermittent/performance keywords, type bug)
**Hard-stop fired**: false
**Round**: 0 of 3 (discriminator-required: no; counter not incremented)
**Captured bytes (failing run)**: n/a (audit-time only; the hook writes no log file)

## 3-W's coverage

| W | Answerable | Evidence |
|---|------------|----------|
| When  | yes | deterministic: every run of the probe gives the same result (tier1-observation.md) |
| Where | yes | trace probe prints the chosen command word per input: 160ython3, 30, [[ then python (trace-probe.out) |
| Why   | yes | the chosen word plus the source lines 101, 190-191 and 206 explain each decision |

## Branch A — Log-call inventory

Total: 21. logger_call: 0 | print: 6 | exception_handler: 11 | error_reporter_init: 4 (test captures). Richness: rich 3 | minimal 3 | silent 9. The scanner's only output is the matched word at line 111. `degraded`: true.

## Branch B — Log-config reachability

No log level; LC_ALL=C is the only env var. reaches_sink: 1 (block message) | filtered_out: 3 | unknown: 0. `degraded`: true.

## Sufficiency rubric application

Row fired: S1-equivalent (deterministic, self-describing reproduction) with the trace probe resolving the Where/Why gap; S14 does not apply (no disputed datum is lost: the trace shows it). Verdict capped at `partial` by the degradation rule (auggie unavailable, Grep/Glob found signal).

## Implication for diagnosis confidence

Existing instrumentation: the hook emits only the matched word, so wrong allows leave no trace in the hook itself.
Gap: closed for this run by a read-only copy of the scanner that prints every chosen command word (trace-probe.sh).
Consequence: the three mechanisms are directly observed, not inferred; the cap to partial is a discovery-tool limit, not an evidence gap.
Next step: proceed to hypothesis formation; no instrumentation of the hook is needed.

## Tasklist reference

/home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/troubleshoot/bug-pr359-bare-python-hook-findings-20261104150317/diagnosability-tasklist.md
