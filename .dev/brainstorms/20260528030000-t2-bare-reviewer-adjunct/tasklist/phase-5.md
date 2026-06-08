---
phase_id: 5
title: MCP transport adapter (OPTIONAL / DEFERRED)
depends_on: [1]
blocks: []
estimated_loc: 250 new
compliance_tier: STANDARD
acceptance_gates: [AC-5.1, AC-5.2]
status: DEFERRED
---

# Phase 5 — MCP transport adapter (optional)

## Status: DEFERRED

This phase is nice-to-have, not blocking. The reference Bash+curl transport (Phase 1) is sufficient for v1.0 ship. Phase 5 is appropriate when:

- Bash+curl prompt-escaping proves problematic for large/complex targets
- Vendor-side streaming output is desired (Bash+curl doesn't stream)
- A specific MCP adapter (e.g., LiteLLM MCP server) becomes available and supported

## Scope (if activated)

Build a `t2-proxy` MCP server that wraps the same OpenAI-compatible proxy contract but exposes structured tool calls instead of raw curl.

## Tasks

### T-5.1 — MCP server skeleton
- `mcp__t2-proxy__chat` tool exposing the same parameters as Bash+curl
- Streaming support (optional)
- Structured error responses
- LOC: ~200

### T-5.2 — sc-bare-review auto-detection
- Detect `mcp__t2-proxy__*` availability at Wave A
- If available, use MCP path; else fall back to Bash+curl
- Document the detection logic in skill
- LOC: ~50

## Acceptance Gate

- **AC-5.1** MCP server skeleton ships
- **AC-5.2** sc-bare-review auto-detects + falls back cleanly

## Activation Criteria

Promote from DEFERRED to ACTIVE when:
- 3+ workflow failures attributable to Bash+curl escaping over a rolling month
- A user explicitly requests streaming bare-review output for long targets
- A maintained MCP transport adapter becomes available externally
