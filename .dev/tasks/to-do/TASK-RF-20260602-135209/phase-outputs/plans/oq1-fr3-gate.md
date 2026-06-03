# OQ-1 → FR-3 Gate Decision (Phase 6)

**Date:** 2026-06-02
**Source:** the Phase-1 OQ-1 precondition record (`oq1-find-referencing-probe.md`) + research 06 §OQ-1.
**Precedes:** Step 6.2 (the §6.1 step-4 `include_info` edit).

## Gate decision

FR-3 is implemented as the **corrected `include_info: true` parameter on the EXISTING §6.1 step-4 `find_referencing_symbols` call** — the ABSENT/expected branch of the OQ-1 probe. This is the form FR-3.4 mandates **regardless of probe outcome** ("prefer the extended-info path regardless", matrix:189), so the wiring is deterministic and does not block on the runtime result.

Concretely, the FR-3 wiring at merge MUST:

1. Add `include_info: true` to the existing step-4 call — **NOT** a new step, and **NEVER** a standalone `find_referencing_code_snippets` tool (it was absorbed into the extended-info return shape at Serena v1.0+/v1.5.0).
2. Emit `references_extended_info_used: true` to `audit.log` (FR-3.1).
3. Record the **Wave-0 tool-inventory probe result** re `find_referencing_code_snippets` presence/absence in `audit.log` (FR-3.2) — the probe itself runs at Wave 0 of the actual implementing reflect run (via `serena_info` or `get_current_config`'s loaded-tools list), as documented in the Phase-1 record; this task wires the corrected form that the probe's expected (ABSENT) branch selects.
4. Add **no new §9.1 contract field** for FR-3 (FR-3.3).

## Runtime-probe disposition

The OQ-1 runtime tool-inventory probe is a **Wave-0 step of the live reflect run**, not a task-build-time action; this task encodes the probe procedure (Phase-1 record) and wires the corrected `include_info` path that satisfies the expected (ABSENT) branch. The PRESENT branch (older pinned Serena <v1.0) also routes to the extended-info path per FR-3.4 — so no branch wires the defunct standalone tool. Gate is therefore RESOLVED for the purpose of the Step 6.2 merge: proceed with the `include_info` param add.
