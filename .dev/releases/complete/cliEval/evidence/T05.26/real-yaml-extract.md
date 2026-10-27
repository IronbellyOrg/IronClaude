# T05.26 — real.yaml extract (optional_capabilities ↔ requires coupling)

Captures the manifest lines establishing the `--no-mcp` exclusion-set.
Source: `src/superclaude/cli/eval/suites/real.yaml` as of 2026-05-20.

## optional_capabilities (lines 36-40)

```yaml
optional_capabilities:
  - { name: mcp_server.auggie,            gate_flag: "--no-mcp", failure_mode: skip }
  - { name: mcp_server.auggie-mcp,        gate_flag: "--no-mcp", failure_mode: skip }
  - { name: mcp_server.airis-mcp-gateway, gate_flag: "--no-mcp", failure_mode: skip }
  - { name: mcp_server.serena,            gate_flag: "--no-mcp", failure_mode: skip }
```

Every `mcp_server.*` row declares `gate_flag: "--no-mcp"` with
`failure_mode: skip`. The harness `CapabilityGates` picks these up
through `_DEFAULT_CAPABILITY_SPECS` and routes them through the
soft-skip override path when `--no-mcp` is active.

## MCP-tagged evals

```yaml
- id: E1
  ...
  requires: [mcp_server.auggie]
  no_pty: skip

- id: E2.1
  ...
  requires: [mcp_server.auggie]
  no_pty: skip

- id: E2.2
  ...
  requires: [mcp_server.auggie-mcp]
  no_pty: skip

- id: E2.3
  ...
  requires: [mcp_server.airis-mcp-gateway]
  no_pty: skip
```

Each MCP-tagged eval names exactly one MCP server in its `requires:`
tuple — the matcher-coverage trio E2.1-3 deliberately splits the
`mcp__auggie__.*` / `mcp__auggie-mcp__.*` / `mcp__airis-mcp-gateway__auggie_.*`
hook branches into three independent gating surfaces (OQ-2 / D-0082 §3).

## Coupling logic

```
optional_capabilities[name=mcp_server.X].gate_flag == "--no-mcp"
                                ↓
EvalSpec.requires.contains("mcp_server.X")
                                ↓
CapabilityGates(skip_flags={"--no-mcp"}).check_all()
        soft_skips ⊇ {"mcp_server.X"}
                                ↓
run_one(spec) emits EvalOutcome(
    status="SKIPPED",
    skip_reason="capability_gate:mcp_server.X",
    skip_flag_triggered="--no-mcp",
)
```

The third stage is the M2 → M3 wiring TEST-014's end-to-end test gates
on (`_no_mcp_runtime_wired()` source probe). The first two stages are
already wired and pinned by the eleven passing tests.
