# Diagnosability Context Card

**Issue**: Issue 501: invalid swarm refactor-find recommendation
**failing_component**: src/superclaude/cli/swarm/lenses/refactor_find.py
**Verdict**: partial
**Complexity**: trivial (score 0: no explicit scope, no stack trace, deterministic, not performance/security)
**Hard-stop fired**: false
**Round**: 0 counted discriminator emissions of 3; no counter update
**Captured bytes (failing run)**: 1559 execution-log.jsonl; 4221 return-contract.yaml

## 3-W's coverage
| W | Answerable | Evidence |
|---|---|---|
| When | partial | Event log has dispatch timestamps, not a timestamped recommendation event. |
| Where | yes | Live lens source :53 and captured return-contract.yaml:64 identify the disputed string. |
| Why | yes | Captured complete command plus local source path through commands.py:2141 and reduce.py:672 explains stale name and literal input prefix. |

## Branch A — Log-call inventory
Five signal sites: one stdout print in commands.py:2173; four structured event calls upstream in dispatch.py. No diagnostic calls inside the 60-line lens constant module. No handler or error reporter there. No recommendation fields in the captured 1559-byte event log. degraded=false. Full inventory in wave1_6-branch-A.md.

## Branch B — Log-config reachability
Generated job declares runtime.log_level=info. Recommendation is a direct YAML result artifact, not a severity-filtered logger message: emit_contract writes its actual value. The 4221-byte captured artifact confirms reaches_sink for this run. Effective logger level was not measured and is not needed to explain this value. degraded=false. Full inventory in wave1_6-branch-B.md.

## Sufficiency rubric application
S14 does not apply: disputed datum is present unchanged in the captured failing artifact. S1/S2 absent; S3/S4 unmet (no three symptom-local logger calls and When partial); S5 cannot fire from unmeasured per-stream diagnostic bytes; no S6 filter or S7 reporter; S8 absent local INFO logs. S9 applies to deterministic plain stdout at the immediate caller: partial. No multiple-producer or missing-datum discriminator trigger. Complexity trivial means no hard-stop.

## Implication for diagnosis confidence
Existing result artifact exposes the full recommendation and actual successful report paths.
Event logs do not diagnose recommendation validity, so log-only inspection is incomplete.
The captured artifact and source are enough for a bounded deterministic diagnosis; no hidden value or competing cause remains to instrument.
Proceed to hypothesis/calibration; do not claim a replacement has executed or a fix has passed.

## Tasklist reference
diagnosability-tasklist.md (retained audit record; no additional instrumentation is required for the already captured datum).
