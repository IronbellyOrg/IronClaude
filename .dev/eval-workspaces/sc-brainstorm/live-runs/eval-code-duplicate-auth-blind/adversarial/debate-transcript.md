---
mode: B
blind_mode: true
depth: deep
advocates: [Agent A, Agent B, Agent C, Agent D, Agent E]
convergence_score: 0.82
rounds: 3
---

# Adversarial Debate Transcript — BLIND MODE

All advocate identities are anonymized. Only Agent A through Agent E labels are
used. No advocate role, no model identity, and no project-specific name appears.

## Round 1 — Opening Positions

### Agent A (Variant A)

Proposes a strangler-fig consolidation: introduce a thin canonical facade in
front of all three modules, route call-sites through the facade behind a
per-call-site flag, then collapse implementations one surface at a time. Argues
this minimises blast radius and gives a per-site rollback. Identifies the
canonical baseline by behavioural-equivalence matrix, not by codebase tenure.

### Agent B (Variant B)

Proposes a specification-first approach: write the canonical auth contract as
an executable specification (typed interface plus property-based tests) before
any code consolidation, then implement once and migrate. Argues that without a
fixed spec the merger will inherit accidental divergence as legitimate behaviour.
Estimates higher upfront cost, lower long-term drift.

### Agent C (Variant C)

Proposes a highest-coverage-wins approach: pick the module with the strongest
existing test suite and hardening posture as the baseline, port missing
behaviours into it, retire the other two. Argues this is the fastest path and
inherits proven hardening. Acknowledges the risk of importing baseline-specific
quirks as canonical.

### Agent D (Variant D)

Proposes a shadow-and-diff consolidation: run the canonical implementation in
shadow mode behind every call-site for a soak period, diff the auth events
against the legacy module's output, and only cut over when divergence drops to
zero on a per-call-site basis. Argues this is the only approach that empirically
verifies behavioural equivalence rather than asserting it.

### Agent E (Variant E)

Proposes a minimal-canonical-plus-adapters approach: extract only the truly
shared core (token issuance, session lookup, password verification primitives)
into a canonical library, and keep three thin adapter layers that translate each
surface's quirks into the core. Argues full consolidation is over-reach when the
quirks are sometimes legitimately divergent.

## Round 2 — Critiques

### Agent A on Agent B

Spec-first is correct in principle but stalls. Three teams will not agree on a
canonical contract without a forcing function, and the forcing function is the
facade-and-flag scaffolding from Variant A. Suggests merging: facade first,
contract second, written against the facade's observed traffic.

### Agent B on Agent C

Highest-coverage-wins makes test coverage a proxy for correctness. Coverage is
necessary but not sufficient — the highest-coverage module might be the one
that institutionalised an incident-derived bug as a passing test. Demands the
baseline-selection criteria include a written behavioural-equivalence audit,
not coverage alone.

### Agent C on Agent D

Shadow-and-diff is rigorous but ruinously expensive at the proposed soak length.
The cost compounds because every auth call is doubled for the duration. Suggests
shadow-and-diff only on a per-call-site basis during cutover, not as the entire
migration strategy.

### Agent D on Agent E

Minimal-canonical-plus-adapters preserves the duplication problem in a new
shape: three adapters with three subtly different translation rules become the
new drift surface. Concedes that legitimate divergence exists, but argues it
should be modelled as explicit policy on the canonical module, not as adapter
logic.

### Agent E on Agent A

Strangler-fig with a facade is the right scaffolding, but the proposal under-
specifies how legitimate per-surface divergence is preserved. Without an
explicit policy hook on the canonical module, the facade either flattens
legitimate differences or silently keeps them in the legacy modules forever.

## Round 3 — Convergence

All advocates converge on a synthesis with the following load-bearing elements:

1. A canonical facade is introduced first (from Variant A), routing all
   call-sites behind a per-call-site flag — this is the forcing function.
2. A canonical contract is written against the facade's observed traffic
   (from Variant B), with property-based tests that codify required behaviours.
3. A baseline-selection audit combines coverage, hardening posture, and
   behavioural-equivalence-matrix score (from Variant C, hardened by Variant
   B's critique). Coverage alone does not pick the baseline.
4. A shadow-and-diff window is run per-call-site at cutover time (from
   Variant D, scoped down by Variant C's cost critique), not as a global soak.
5. Legitimate divergence is modelled as explicit policy on the canonical
   module (from Variant E, hardened by Variant D's critique), not as adapter
   layers and not as silent flattening.
6. Rollback is per-call-site via the facade flag, with a documented MTTR
   target and a global kill-switch.

### Remaining Unresolved Tensions

- The exact soak length for the per-call-site shadow window — Agent C argues
  for 24 hours, Agent D argues for 7 days. Recorded as an open decision for the
  implementation phase, parameterised in the canonical-policy module.
- Whether the canonical contract should be written as a typed interface plus
  property tests (Agent B preference) or as an OpenAPI-style document plus
  contract tests (Agent C preference for tooling parity). Both are compatible
  with the canonical-facade scaffolding; recorded as a tooling-tier decision,
  not a strategy-tier decision.

### Convergence Score

0.82 — strong agreement on the five load-bearing elements; the two remaining
tensions are scoped to implementation parameters rather than strategic direction.
