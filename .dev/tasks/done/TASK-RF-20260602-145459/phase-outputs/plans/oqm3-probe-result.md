# OQ-M3 Probe Result — `type_hierarchy` backend capability

**Date:** 2026-06-03
**Step:** Phase 5, Step 5.1 (merge-precondition backend probe)

## (a) Detected backend + tool exposure (with evidence)

- **Backend: `lsp`** (this environment's live Serena backend; corroborated by research-06 §OQ-M3 / OQ-M5: "Language backend: LSP", Serena 1.5.4.dev0).
- **Generic `type_hierarchy` tool: NOT exposed.** The live Serena surface this session exposes no generic
  `type_hierarchy`; the only hierarchy-related tool is `jet_brains_type_hierarchy` (a JetBrains-backend tool,
  available-but-not-active). This corroborates the spec's "JetBrains-only" reading and contradicts the README
  "LSP: yes" capability row.

## (b) Gating decision

- `--with-hierarchy` **defaults OFF on `lsp`** (no generic `type_hierarchy` tool present here) and is **unavailable on `none`**.
- Only a `jetbrains` backend is currently confirmed-capable.
- FR-1 step 4.5 runs ONLY when: backend is hierarchy-capable AND `--with-hierarchy` is set AND the located symbol is a type.

## (c) Fail-open distinction encoded into FR-1 wiring (Steps 5.2–5.7)

- backend `none` / `lsp-disabled` → **skip step 4.5** with `type_hierarchy_invoked: false` and **NO degrade**
  (expected absence, FR-1.4) — not a failure.
- explicit backend ERROR (distinct from unsupported) → `degraded: ["type_hierarchy:backend_error"]` + fall back
  to `find_implementations` / `find_referencing_symbols` (FR-1.5).
- the skill never aborts because hierarchy is unavailable.

## (d) Empirical per-language note

Per-language LSP support (Python / Java / TypeScript) is recorded during Phase 6 eval-authoring. This env's
"LSP → no `type_hierarchy` tool" is the baseline negative. No per-language LSP claim is fabricated.

**Merge-precondition status:** SATISFIED — `--with-hierarchy` default-off-on-LSP gate is the safe default;
FR-1 wiring honors the skip-no-degrade vs error-degrade distinction.
