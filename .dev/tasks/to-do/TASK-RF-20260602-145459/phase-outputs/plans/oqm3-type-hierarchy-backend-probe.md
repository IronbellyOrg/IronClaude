# OQ-M3 — `type_hierarchy` Backend-Probe Procedure & Gate

**Date:** 2026-06-03
**Step:** Phase 1, Step 1.6
**Classification:** RUNTIME-PROBE-REQUIRED (this env yields a strong negative: LSP backend exposes NO `type_hierarchy` — CODE-VERIFIED)
**Gates:** FR-1 (Phase 5) — BLOCKING merge-precondition for any LSP default-on

## (a) Procedure

The Wave-0 `backend` field (from OQ-M5 / FR-7's `get_current_config` snapshot) classifies the backend as
`jetbrains | lsp | none`. FR-1 §6.1 step 4.5 runs **ONLY** when ALL THREE hold:
1. the backend is hierarchy-capable, AND
2. `--with-hierarchy` is set, AND
3. the located symbol is a type.

The Phase 5 Step 5.1 probe enumerates the live Serena tool inventory and records whether a generic
`type_hierarchy` tool is exposed (distinct from the JetBrains-only `jet_brains_type_hierarchy`).

## (b) Gate rule

- `--with-hierarchy` **defaults OFF on `lsp`** — no generic `type_hierarchy` tool exists on the live LSP
  backend in this environment (only `jet_brains_type_hierarchy`, a JetBrains tool, is present and it is
  available-but-not-active).
- `--with-hierarchy` is **unavailable on `none`**.
- Only a `jetbrains` backend is currently confirmed-capable.

## (c) Empirical-probe note

Per-language LSP support (Python / Java / TypeScript) is recorded during FR-1 eval-authoring (Phase 6).
This environment's "LSP → no `type_hierarchy` tool" is the baseline negative. No per-language LSP claim is
fabricated — the spec's empirical Py/Java/TS probe plan still stands for other LSP builds.

## (d) Fail-open distinction (encoded into FR-1 wiring, Steps 5.2–5.7)

- backend `none` / `lsp-disabled` → **skip step 4.5** with `type_hierarchy_invoked: false` and **NO degrade**
  (expected absence, FR-1.4) — this is NOT a failure.
- explicit backend ERROR (distinct from "backend unsupported") → `degraded: ["type_hierarchy:backend_error"]`
  + fall back to the `find_implementations` / `find_referencing_symbols` chain (FR-1.5).
- The skill MUST never abort because hierarchy is unavailable.

## Environment evidence (CODE-VERIFIED)

Live `get_current_config` (LSP backend, Serena 1.5.4.dev0): no `type_hierarchy` in either the active or
available tool list; the only hierarchy tool present is `jet_brains_type_hierarchy` (available-but-not-active).
This corroborates the spec's "JetBrains-only" reading and contradicts the README "LSP: yes" capability row.

Derived verbatim from research-06 §OQ-M3 with no fabricated per-language claim.
