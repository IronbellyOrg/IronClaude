# Lens contribution policy (swarm operator pointer)

**Canonical policy:** [`docs/dev/lens-contribution-policy.md`](../dev/lens-contribution-policy.md).

This page is a thin pointer for swarm operators who land here from the
OPS-005 handoff. The full, authoritative lens-contribution policy lives
at [`docs/dev/lens-contribution-policy.md`](../dev/lens-contribution-policy.md)
and is the single source of truth — do **not** duplicate its rules here.

**What you'll find at the canonical doc:**

- The **five-criterion reviewer checklist (C1–C5)**: C1 real caller,
  C2 §11.5 injection-guard substring, C3 `normalizer_strategy` matches
  recipe output shape, C4 real downstream command, C5 `suspect: true`
  by-construction justification — the single sign-off surface for any PR
  touching `cli/swarm/lenses/`.
- The **COMP-023 lens validator** (`cli/swarm/lenses/_validate.py`) and
  its CLI surface `superclaude swarm validate-lenses`.
- The **embedded PR-review checklist** plus the pre-commit/CI wiring
  (warning-mode local, blocking in CI).
- The extra **`suspect: true` scrutiny** path (architect sign-off +
  written by-construction justification) and the owners/sign-off log.

**Requirements satisfied (OPS-005 / D-0135 / R-154):** lens-registry
PR-review discipline per **NFR-008** and **NFR-012**. See the canonical
doc for the FR-040 / roadmap-row provenance.
