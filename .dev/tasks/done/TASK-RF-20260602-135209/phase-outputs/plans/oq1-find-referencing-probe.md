# OQ-1 Precondition Record — `find_referencing_code_snippets` absorption probe

**Date:** 2026-06-02
**Source:** research 06 §OQ-1 (matrix:181, matrix:558, spec:180–195, spec:519)
**Gates:** **FR-3 merge** — HARD BLOCKER (spec:195: "Runtime probe (OQ-1) MUST resolve before merge").

## (a) The runtime-probe procedure

At **Wave 0** of the implementing reflect run:

1. Enumerate the live Serena MCP tool inventory. Two evidenced mechanisms:
   - **(a)** Invoke the `serena_info` probe (introduced v1.2.0; matrix:216) to enumerate the current Serena tool inventory; **OR**
   - **(b)** Invoke `get_current_config` (FR-7) — its return includes the loaded-tools list (matrix:399).
2. Check whether the string `find_referencing_code_snippets` appears in the returned tool list.
3. Record the probe result in `audit.log` (FR-3.2, spec:188 — "the audit notes whether `find_referencing_code_snippets` is present").

## (b) The branch rule

- **ABSENT (expected)** → confirm the absorption story. Wire the corrected path: `find_referencing_symbols(..., include_info=true)`. Emit `references_extended_info_used: true` to audit (FR-3.1, spec:185).
- **PRESENT (older pinned Serena <v1.0)** → do **NOT** silently wire the named standalone tool. Route to the OQ-1 resolution decision per FR-3.4 (spec:189). Even if present, its signature is undocumented in current docs — **prefer the extended-info path regardless** (matrix:189).

## (c) Hard-blocker note

- FR-3 **MUST NOT merge** (Phase 6) until this probe resolves (spec:195).
- The FR-3 wiring is the corrected `include_info` parameter on the **existing §6.1 step-4 `find_referencing_symbols` call** — **NEVER a new standalone `find_referencing_code_snippets` tool** (it was absorbed into the extended-info return shape at v1.0+/v1.5.0).
- No new return-contract (§9.1) field is added for FR-3 (FR-3.3, spec:188).
- Phase 6 Step 6.1 re-confirms this gate decision before the Step 6.2 edit.
