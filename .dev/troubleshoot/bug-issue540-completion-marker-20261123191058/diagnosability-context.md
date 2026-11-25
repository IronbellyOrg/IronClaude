# Diagnosability Context Card

**Issue**: issue 540, missing completion marker after foreground success
**failing_component**: src/superclaude/cli/swarm/commands.py::run_cmd completion
**Verdict**: partial
**Complexity**: trivial (score 1: investigation spans more than two source files; no other signal)
**Hard-stop fired**: false
**Round**: 0 of 3 (no counted discriminator emission)
**Captured bytes (failing run)**: JSONL 1559, Markdown 999; contract 4825 and state 104 are artifacts, not log-stream bytes.

## 3-W's coverage

| W | Answerable | Evidence |
|---|---|---|
| When | partial | Timestamped dispatch events and terminal-state timestamp, but no marker-publication event. |
| Where | partial | Direct CLI and artifact paths identify completion, but stdout summary does not locate a marker-write site. |
| Why | partial | Counts/status and inspected completion code are available; logger does not record marker publication. Direct filesystem capture independently establishes absence. |

## Branch A — Log-call inventory

Four directly relevant signals: one print (commands.py:2173), one structured event (dispatch.py:497), two writer sinks (logging_.py:156,158). The sinks are not three independent events and do not earn S3. No exception handler or error reporter in the completion continuation. No invented stdout byte count. degraded=false.

## Branch B — Log-config reachability

Custom logger is unfiltered when present, with output-root paths selected by the manifest directory. Declared log_level fields are not evidence of an effective threshold. All four Branch A signals reach their sinks if executed; none is filtered out. Runtime log files and stdout were captured. degraded=false.

## Sufficiency rubric application

S14 does not apply: no intermediate layer loses or substitutes the disputed datum; the parent directly measured done_exists=false for real foreground and resume runs. S1/S2/S3/S4/S5/S6/S7 do not match. S8 matches the one relevant structured dispatch event plus minimal stdout, deterministic behavior, and no exception-handler logging/error reporter: partial. No inferred missing stream is assigned zero bytes. Complexity is trivial, so no hard-stop. No discriminator required: the missing-artifact state is captured, not an ambiguous emitted token; no competing producer menu.

## Implication for diagnosis confidence

Dispatch events and persisted state/contract reach disk, but do not prove marker publication.
The parent directly captured marker absence after real successful foreground and resume commands.
Proceed with grounded hypothesis formation; do not mistake a missing marker call for log filtering.
No production instrumentation or extra log-level override is needed for this deterministic omission.
Detached, failed/partial, and disabled-policy acceptance still require repair-stage validation.

## Tasklist reference

`diagnosability-tasklist.md`: preserves audit limits and completed observational checks, with no required pending diagnostic measurement and no production-source instrumentation.
