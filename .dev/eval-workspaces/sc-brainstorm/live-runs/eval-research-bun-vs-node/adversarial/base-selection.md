# Base Selection

**Run**: eval-research-bun-vs-node
**Mode**: B (parallel generate → debate → merge)
**Date**: 2026-05-27

## Variants generated

| Variant | Model | Persona | Stance summary |
|---------|-------|---------|----------------|
| V1 | opus | analyzer | Evidence-driven systematic comparison — six-axis matrix with workload-scoped recommendation, pilot framing as default outcome. |
| V2 | sonnet | architect | Runtime-architecture trade-off framing — emphasizes ecosystem maturity, native-module / APM compatibility, and workload-fit gating. |
| V3 | haiku | scribe | Decision-framework synthesis — heavier on risk register, structured open questions, and traceable recommendation criteria. |

## Base selection rationale

V1 (analyzer/opus) is selected as the base merge candidate because:

- It provides the most complete six-axis comparison structure that maps directly to the seed brief's success criteria.
- Its workload-scoped recommendation framing matches the operator's explicit `acceptance_target` (actionable adopt / pilot / defer / reject decision).
- It cleanly preserves every seed-brief `must_preserve` anchor.

V2 and V3 contribute targeted additions:

- V2 → architecture / compatibility section depth and the explicit "native modules + APM + FaaS hosting" risk surface inventory.
- V3 → the structured decision framework (decision rule + exit criteria for pilot) and the formal risk register layout.

Base = V1, augmented by V2 (compatibility + architecture detail) and V3 (decision framework + risk register format).

## Blind mode

Disabled (operator did not pass `--blind`). Model identities visible during debate.
