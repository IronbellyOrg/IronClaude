# D5 option (a): keep Orca's nesting depth at 1

Position: workers may not start workers. Fan-out stays inside a command (Agent-tool subagents) or is split into separate Tasks by the coordinator (`SPEC:352`; `SPEC:42`). This is the spec's current recommendation.

Citation key: `SPEC:N` = spec line; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`.

## Safety
- Depth 1 is Orca's own default and its fence against runaway fan-out: "1 means a coordinator dispatches workers and those workers may not dispatch further"; a malformed setting "falls back to the default rather than disabling the fence"; a new Run does not reset depth (`CAPS:97`, `CAPS:100-101`). Orca's advice at the limit is "Do the work in this terminal" (`CAPS:99`).
- The setting is machine-wide, not per run: it lives in the Orca profile file (`/home/coder/.config/orca/profiles/local-default/orca-data.json:1`, `"nestedWorkerMaxDepth":1`, `CAPS:98`). Raising it for this spec would raise it for every Orca run on the machine.

## Reliability
- Nothing in the spec needs depth 2: commands never call Orca (WC-8, SA-2 at `SPEC:72`, `SPEC:170`), and the coordinator gets per-unit Task records by splitting work into Tasks (`SPEC:42`). Agent-tool subagents are not counted by the fence (`CAPS:155`).
- The rejected design that depth 2 would enable fails for reasons depth does not fix: standalone use breaks without Orca (R2), a command cannot own `worker_done` (R3), the executable name differs by platform (R4), and a second orchestrator competes with the coordinator (R5) (`SPEC:37-40`).

## How a person works day to day
- No change. The coordinator plans fan-out as Tasks (for example N troubleshoot workers then one adversarial merge, `SPEC:87`).

## Implementation cost
- Zero. Raising depth later is one desktop setting (`CAPS:99`); the spec can revisit it if P0 smoke runs (`SPEC:181`) show coordinator-side splitting is inadequate.
