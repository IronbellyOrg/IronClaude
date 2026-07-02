# Diagnosability Context Card

**Issue**: `superclaude sprint run ... --start 3` stalled >300s, then phases 3-5 showed ERROR / 0 B
**failing_component**: `.dev/releases/current/v0.1/results` and installed `superclaude` sprint runner
**Verdict**: sufficient
**Complexity**: non-trivial (score breakdown: multi-phase build/recovery + external provider rate-limit/timeout + long-running orchestration)
**Hard-stop fired**: false
**Round**: 1 of 3
**Captured bytes (failing run)**: phase 3 T03.05 transcript 1104129 bytes; T03.13 transcript 487123 bytes; many 429-only transcripts ~13 KB; phase-level TUI output is not reliable

## 3-W's coverage

| W | Answerable | Evidence |
|---|------------|----------|
| When  | yes | `execution-log.md` and phase result JSON record exact phase/task timestamps; per-task transcripts include terminal result envelopes. |
| Where | yes | Phase 3 localizes the first non-recoverable failure to T03.05 and the cooldown cascade to T03.13 onward. |
| Why   | yes | Per-task outputs contain terminal `API Error: The operation timed out` and 429 `rate_limit_error`/provider cooldown messages. |

## Branch A — Log-call inventory

Existing persisted artifacts are sufficient diagnostic signal. Total: 3 representative high-value hits. Breakdown by call_type: result_artifact: 1; transcript_result: 2. Exception-handler richness: n/a. `degraded`: true because native artifact inspection was used instead of Auggie branch search.

## Branch B — Log-config reachability

Effective log level for sprint artifacts: n/a; task transcripts and result JSON are persisted files, not filtered logger calls. Per-Branch-A-hit reachability_verdict summary: reaches_sink: 2; filtered_out: 0; unknown: 0. `degraded`: true.

## Sufficiency rubric application

Row fired: S1/S2-equivalent runtime artifacts. Reason: the symptom is a build/orchestration failure with persisted, line-addressable result JSON plus per-task terminal envelopes; the artifacts directly answer when/where/why.

## Implication for diagnosis confidence

The run has enough artifacts to diagnose without adding instrumentation: phase result JSON localizes failed task IDs and task transcripts contain terminal provider errors. The main caveat is the TUI's phase-level `0 B`, which is misleading because per-task output files contain nonzero captured output. Diagnosis confidence should be based on per-task transcript/result JSON evidence, not phase-level output bytes. Proceed with recovery planning rather than an instrumentation hard-stop.

## Tasklist reference

n/a (verdict=sufficient)
