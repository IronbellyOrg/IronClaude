# OQ-3 Pilot Record — `summarize_changes` signature (FR-5)

**Date:** 2026-06-02
**Source:** research 06 §OQ-3 (matrix:294-298, matrix:306, matrix:559, spec:521, spec:231) + review R5.
**Gates:** FR-5 promotion from pilot/deferred status. **SHOULD-probe (not a hard merge block)** — distinct from OQ-1's MUST.

## Why FR-5 is pilot-only / ships-last

- `summarize_changes` signature is "**not surfaced**" in primary sources — no documented parameters. Treat as **zero-arg** until probed: `{"tool": "mcp__serena__summarize_changes", "arguments": {}}` (matrix:319).
- It is a **prompt-provider**, NOT a computed diff (matrix:296/306) — it returns instructions to the LLM to summarize session changes; the "independent check" is weaker than implied (still model-mediated).
- It is **session-aware** (v1.2.0): the prompt provision is tied to the active MCP session; cross-session invocation returns empty/generic (matrix:298).
- Per review R5, the eval harness has **no stated session-identity mechanism**, so FR-5 is **pilot-only / manual** until the same-MCP-session requirement (FR-5.1) is confirmed satisfiable.
- FR-5 **ships last** (lowest cost/benefit, spec:231).

## The pilot (this eval case is the OQ-3 pilot)

This case directory `cases/serena-summarize-changes/` IS the OQ-3 pilot. Before FR-5 is promoted from pilot status, the pilot must:

1. Invoke `summarize_changes` **zero-arg** and **observe the actual return shape** (signature probe).
2. Confirm the **same-MCP-session requirement** (FR-5.1) is satisfiable in the eval harness (R5 — currently unconfirmed → manual).
3. Set `serena_summary_corroboration` ∈ `{agree, partial, disagree, unavailable}` (matrix:325, spec:223) by comparing the summary vs the supplied diff.
4. Exercise the **cross-session** path (fresh session → `serena_summary_corroboration: unavailable`, main verdict unchanged, FR-5.4).

## Disposition

FR-5 is wired in this task (allowed-tools token, §6.1 step 7', §9.1 field, §10.3 mirror, eval scaffold) in its **corrected, fail-open, ships-last form**, but is flagged **pilot/manual** pending the OQ-3 signature probe + R5 session-identity confirmation. No hard merge block (SHOULD, not MUST). Recorded in this task's Open Questions.
