# Merge Log — DD-1

## Metadata
- Base: Variant A (derive-only)
- Status: success (merged recommendation = REFACTOR DD-1)
- Date: 2026-06-02

## Changes Applied
1. Corrected "phase_start before execution" claim (single-process path spawns first). [from B / X-001]
2. Corrected "phase number always survives" → result.json is the atomic anchor; ledger is non-durable. [from B / C-001, U-001, X-002]
3. Hardened §3 COMPLETED to key off atomic result.json, fixing the torn-`phase_complete` needless-rerun bug. [INV-004 + fault-finder]
4. Documented concurrency caveat (deterministic release_dir, no lock). [INV-003]
- Rejected: adopting the breadcrumb file — redundant with result.json's existing atomic guarantee (NG1).

## Post-Merge Validation
- Structural: pass. References: all file:line citations independently verified against source.
- New contradictions introduced: 0.
- Return contract: status=partial (convergence 78% < 0.80, blocked by INV-001 against rationale; resolved via REFACTOR).
