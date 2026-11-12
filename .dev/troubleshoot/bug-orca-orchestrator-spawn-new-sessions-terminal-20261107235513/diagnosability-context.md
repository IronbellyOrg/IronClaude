# Diagnosability Context Card

**Issue**: Orca orchestrator continues to spawn new sessions via a new terminal session shortcut instead of a new claude session shortcut. Resulting in empty terminals and a waiting orchestrator
**failing_component**: not localizable to code (S1.6.0). The deciding actor is an LLM orchestrator choosing an `orca` command; no source file emits that choice. Its tool calls are recorded only in Claude transcripts (~/.claude/projects/**/*.jsonl) and Orca's daemon log has no caller field.
**Verdict**: unknown at S12, raised to partial by the discriminator trigger (`discriminator-required: yes`: 4 `surviving=yes` producers in producers.md, and the observed datum, an orchestrator `terminal create` call, is absent from every captured output)
**Complexity**: non-trivial (score 2: Wave 1 cause class "Stale state/cache" does not apply; signals: "continues to" implies recurrence/intermittent +1, multi-module/instruction-plus-Orca-app spread +1). No hard-stop: the verdict is not `insufficient`.
**Hard-stop fired**: false
**Round**: 1 of 3 (key `ironbelly/fix-flaky-parallel-thread-test` / `orca-orchestrator-spawn-session-surface`)
**Captured bytes (failing run)**: n/a (audit-time only; no failing-run log was supplied)

## 3-W's coverage

| W | Answerable | Evidence |
|---|------------|----------|
| When  | partial | daemon.log timestamps every tab start (hasCommand true/false) to the millisecond; transcripts timestamp every tool call. No caller field joins them. |
| Where | no | No captured record names which orchestrator command created an empty tab. |
| Why   | no | The choice is a model decision; no log carries its reasoning or the instructions it loaded. |

## Branch A — Log-call inventory

Not run: no `failing_component` to inspect (S12). Branch workers were not spawned. `degraded`: not applicable.

## Branch B — Log-config reachability

Not run (same reason). Orca's own logs were read directly in Wave 1 (tier1-observation.md O2).

## Sufficiency rubric application

Row fired: S12 (`failing_component` not localizable) giving `unknown`; then S1.6.4 step (i) set `partial` because `discriminator-required: yes`. S14 does not apply: no layer is known to drop a datum that exists at a known code site.

## Implication for diagnosis confidence

Existing instrumentation: Orca daemon log (tab start with or without a startup command) and Claude transcripts (every Bash call).
Gap: nothing joins "tab created" to "who asked", and no transcript of a failing orchestrator run was supplied.
Consequence: any hypothesis about what the orchestrator chose is inference; the live evidence (O4) shows the supervised spawns used `worker-start --agent claude`, the correct route.
Next step: proceed to hypothesis formation, but a definite cause needs the failing orchestrator's session id or tab (see tasklist rows).

## Tasklist reference

.dev/troubleshoot/bug-orca-orchestrator-spawn-new-sessions-terminal-20261107235513/diagnosability-tasklist.md
