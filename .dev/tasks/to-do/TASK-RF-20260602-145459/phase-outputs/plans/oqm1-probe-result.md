# OQ-M1 Probe Result — `prepare_for_new_conversation`

**Date:** 2026-06-03
**Step:** Phase 4, Step 4.1 (merge-precondition runtime probe)

## (a) ABSENT or PRESENT — **ABSENT** (with evidence)

The live Serena MCP tool surface in this environment does **NOT** expose
`mcp__serena__prepare_for_new_conversation`. The serena tools available this session are:
`activate_project`, `find_symbol`, `find_referencing_symbols`, `find_implementations`,
`find_declaration`, `get_symbols_overview`, `get_diagnostics_for_file`, `read_memory`,
`write_memory`, `list_memories`, `delete_memory`, `rename_memory`, `edit_memory`, `onboarding`,
`get_current_config`, `replace_content`, `replace_symbol_body`, `insert_after_symbol`,
`insert_before_symbol`, `safe_delete_symbol`, `search_for_pattern`, `initial_instructions`.
There is no `prepare_for_new_conversation` in either the active or available list — consistent with
the OQ-M1 finding (research-06) that it is excluded by default in `claude-code`/`ide-assistant` contexts.

## (b) Confirmed parameter shape — N/A (tool absent)

The signature cannot be determined here; it remains genuinely unknown. NO assumed parameter shape may be hard-coded.

## (c) Resulting wiring decision — write_memory fallback is the DEFAULT path

Because the tool is ABSENT (the expected default):
- Wire `mcp__serena__write_memory` with an inline-built summary blob as the **default** handoff path,
  emitting `handoff_persist_method: write_memory_fallback`.
- Gate ANY `prepare_for_new_conversation` call behind a **runtime-presence check** — invoke it only if a
  future Serena context exposes it AND its signature is confirmed by live probe at that time (FR-3.6).
- NEVER hard-code an assumed `prepare_for_new_conversation` parameter shape.
- The subsequent FR-3 edits (Steps 4.2–4.8) honor this: `prepare_for_new_conversation` is declared in
  `allowed-tools` (so the skill CAN use it where a context exposes it), but the §4.6 Wave-6 detail writes
  the handoff via the fallback-first chain and directs the implementer to OQ-M1 resolution rather than
  wiring assumed parameters.

**Merge-precondition status:** SATISFIED for a fallback-first implementation. FR-3 parameter-dependent
wiring (a real `prepare_for_new_conversation(...)` call with parameters) must NOT merge until a future
live probe confirms presence + signature; the `write_memory` fallback is the default either way.
