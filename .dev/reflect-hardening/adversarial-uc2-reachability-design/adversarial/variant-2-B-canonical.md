# Variant 2 — Position: B is the canonical UC-2 reachability capability (owns contract 1.6.0)

<!-- Source: design position extracted from EXISTING_MATRIX rows M-028..M-031; Tasklist B TASK-RF-uc2-reachability-20260620-025931 -->

## Thesis

The canonical UC-2 reachability capability is **Tasklist B (FR-RSR runtime-surface reachability)** — it is the prior art, it carries the original "uc2-reachability" name, and it provides broad detection of unwired/dead production surfaces. It owns `contract_version: "1.6.0"`; C is deferred or folded in.

## Design summary (B)

- **Detection question:** "Is this production code surface (a symbol/function) actually reached/wired by production callers, or is it dead/unwired?"
- **Posture (high recall, fail-open):** `surface_unreached` pre-filter; `UNREACHED` as a *finding modifier* (no fifth deviation class, 4-category invariant preserved); fail-open on backend/tool unavailability (no STOP, no clean PASS on an unevaluable surface); degrade-only — **does not force Tier 2**.
- **Contract:** six §9.1 fields + `1.5.0 → 1.6.0` advisory bump; `runtime-surface-ledger.yaml`; `refs/runtime-surface.md` new source-of-truth ref; `refs/reviewer-spec.md` grounding hunk.
- **Evals:** `uc2-unwired-surface-passes` (headline fail-pre/pass-post), positive-control, dynamic-dispatch (DEGRADE-not-Regression), degraded-backend, test-only-ref; ids 37-41.

## Why this should be canonical

1. **Broader recall** — catches *any* unwired surface, not only explicitly `@sink`-annotated contracts. C's gate is blind to un-annotated durable effects by design.
2. **Prior art / naming** — "uc2-reachability" originates here; the runtime-surface model is the established FR-RSR design.
3. **Fail-loud-on-uncertainty discipline** — its degrade/fail-open apparatus is purpose-built so uncertainty never becomes a silent PASS.
