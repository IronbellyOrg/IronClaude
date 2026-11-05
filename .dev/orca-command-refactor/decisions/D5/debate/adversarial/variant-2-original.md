# D5 option (b): raise Orca's nesting depth so workers can start workers

Position: raise "Nested worker depth" in Orca's settings (`CAPS:99`) so a command running as a worker could start its own Orca workers for its fan-out, the design section 1.3 rejects (`SPEC:31-42`, `SPEC:353`).

Citation key: `SPEC:N` = spec line; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`.

## Strongest case for it
- **Per-unit records for heavy fan-out.** Today a command's Agent-tool fan-out (for example troubleshoot Tier 2 at "+4-15 min", `SPEC:74`) is invisible to Orca: no Task, no liveness, no independent retry, and a heartbeat gap the spec has to accept (WC-10, `SPEC:74`). Orca keeps those records only for workers it starts (`CAPS:158`; `SPEC:42`). Depth 2 would give each sub-unit its own Task and Dispatch.
- **Orca's provenance rule prefers it.** "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested" (`CAPS:158`).
- **The change itself is one setting** in the desktop app (`CAPS:99`).

## Safety
- Removes Orca's fence against runaway fan-out (`CAPS:97`, `CAPS:100`). The setting is per profile (`CAPS:98`), so it applies to every run on this machine, not only IronClaude workers.

## Reliability
- Depth alone does not make the rejected design work: commands would still need Orca calls, which fail in other projects without Orca (R2, `SPEC:37`), cannot own the parent's `worker_done` (R3, `SPEC:38`), and must handle the platform-specific executable name (R4, `SPEC:39`). Which call sites enforce the depth check is UNVERIFIED (`CAPS:103`).

## How a person works day to day
- More workers and Tasks per run; more terminals to release (`CAPS:113`).

## Implementation cost
- The setting is trivial; using it means rewriting commands to call Orca, against SA-2 and non-goal 1 (`SPEC:170`, `SPEC:314`). No phase of the spec uses it.
