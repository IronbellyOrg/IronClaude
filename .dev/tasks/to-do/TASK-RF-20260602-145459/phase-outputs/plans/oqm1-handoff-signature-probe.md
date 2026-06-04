# OQ-M1 — `prepare_for_new_conversation` Signature Runtime-Probe Procedure

**Date:** 2026-06-03
**Step:** Phase 1, Step 1.5
**Classification:** RUNTIME-PROBE-REQUIRED (confirmed ABSENT in this environment; signature genuinely unknown — CODE-VERIFIED)
**Gates:** FR-3 (Phase 4) — BLOCKING merge-precondition for any parameter-dependent wiring

## (a) Procedure — probe at Wave 0 of the implementing reflect run

1. Enumerate the live Serena tool inventory: read the loaded-tools list from a `get_current_config`
   call (the FR-7 §4.0 Step 0.5c snapshot already does this) and/or inspect `serena_info`, and/or the
   agent's own `mcp__serena__*` MCP tool surface.
2. Check whether `prepare_for_new_conversation` is exposed (ACTIVE-tools list OR available-but-not-active list).
3. If exposed, determine its exact parameter shape from the live surface BEFORE wiring any parameter.

## (b) Branch rule

- **ABSENT** (the realistic default in a `claude-code` context — and the CODE-VERIFIED state of THIS
  environment): wire the `mcp__serena__write_memory` fallback with an inline-built summary blob and emit
  `handoff_persist_method: write_memory_fallback`. Gate any `prepare_for_new_conversation` call behind a
  runtime-presence check.
- **PRESENT**: confirm the signature by live probe BEFORE wiring any parameter (FR-3.6). NEVER hard-code an
  assumed parameter shape. The `write_memory` fallback is STILL authored for the context-excluded case.

## (c) Hard-blocker note

FR-3 parameter-dependent wiring **MUST NOT merge** (Phase 4) until this probe resolves. The `write_memory`
fallback is the default path either way — so FR-3 can be wired safely (fallback-first) even while the tool
is absent, provided NO assumed `prepare_for_new_conversation` parameter is hard-coded.

## Environment evidence (this workspace, CODE-VERIFIED)

- `prepare_for_new_conversation` is **NOT exposed** here — absent from both the ACTIVE tools list and the
  "available but not active" list of the live `get_current_config` output, and there is no
  `mcp__serena__prepare_for_new_conversation` in this agent's MCP tool surface.
- Therefore its signature cannot be determined in this environment; the spec's "largest research gap"
  characterization (spec lines 197–215) is upheld.
- This live-absence is direct evidence that the `write_memory` fallback is the realistic default path for
  FR-3 under a `claude-code`-context Serena.

Derived verbatim from research-06 §OQ-M1 with no fabricated procedure.
