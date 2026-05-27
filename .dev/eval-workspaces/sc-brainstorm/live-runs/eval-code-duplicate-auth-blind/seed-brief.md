---
schema_version: "1.0"
topic: "Brainstorm consolidating three duplicate auth modules"
domain: code
strategy: systematic
depth: deep
proposals_target: 5
handoff_target: none
blind_mode: true
intent_summary: "Consolidate three duplicate authentication modules into a single canonical module, preserving every legitimate behaviour, with a per-call-site migration path, rollback, and zero security regressions."
context_anchors:
  - "Three independent auth modules currently in use, each owned by a different team and reached from production code paths."
  - "Overlap is partial: shared concepts (login, token issuance, session lookup) coexist with module-specific quirks (lockout policy, password-hash algorithm, claim shape)."
  - "Cross-module drift has produced at least one historical correctness incident; the codebase is under active development during the consolidation."
must_preserve:
  - "Zero auth-related security regressions across the cutover window."
  - "No user-visible session invalidation outside an explicit, comms-coordinated event."
  - "Every legacy behaviour preserved, explicitly deprecated with migration, or explicitly removed with documented rationale."
  - "Migration is reversible per-call-site (feature flag or shim) until full cutover; global kill-switch available."
  - "Audit trail and observability at least as strong as the strongest of the three legacy modules."
  - "Compliance posture (password storage, MFA enforcement, session timeout) does not weaken; ideally strengthens to the strictest of the three."
out_of_scope:
  - "Per-call-site shadow-soak length (24h vs. 7d) — implementation-tier parameter, not strategy."
  - "Canonical-contract format (typed interface + property tests vs. OpenAPI-style + contract tests) — tooling-tier decision."
  - "Identity-provider (SSO/IdP) re-architecture and external-claim-shape redesign — out of scope; consolidation preserves existing external integrations."
  - "Greenfield auth-protocol changes (e.g., switching from sessions to bearer-only, or introducing new MFA factors) — explicitly deferred."
source_confidence: medium
created: 2026-05-27T00:00:00Z
---

# Seed Brief: consolidate-duplicate-auth-modules

## Intent Summary

Consolidate three duplicate authentication modules into a single canonical
module. The consolidation must preserve every behaviour the three current
modules legitimately provide, eliminate drift-derived correctness incidents,
reduce the auth attack surface to one implementation, and provide a clear
per-call-site migration path with a documented end-state, rollback procedure,
and global kill-switch. Systematic strategy at deep depth: five orthogonal
proposals, adversarial debate, merged spec ready for downstream implementation
planning. No handoff (none) — the merged spec is the end artifact of this
brainstorm.

## Context Anchors

- Three independent auth modules currently in use, each owned by a different
  team. None is dead code: each is reached from production code paths.
- Behaviour overlap is partial. Shared concepts include login, token issuance,
  and session lookup. Module-specific quirks include divergent lockout
  policies, different password-hash algorithms (and parameters), and divergent
  claim shapes on issued tokens.
- Cross-module drift has produced at least one historical correctness incident.
  Assumed worst-case for systematic-strategy planning: drift is ongoing.
- The codebase is under active development. The consolidation must not block
  feature delivery on the affected services.
- Codebase enrichment is auto-skipped at seed time: the topic does not name
  concrete module paths, so a repo-wide grep would have low signal. Concrete
  paths will be resolved during implementation planning downstream of this
  brainstorm.
- Research-light enrichment is auto-skipped: the topic is an internal-refactor
  problem and does not reference external frameworks or libraries that would
  benefit from official-docs lookup.

## Must Preserve

- **Zero auth-related security regressions** across the entire cutover window.
  Any candidate plan that risks a security regression is disqualified.
- **No user-visible session invalidation** outside an explicit,
  comms-coordinated event. Silent forced re-auth is out of bounds.
- **Behavioural fidelity**: every behaviour the three legacy modules currently
  provide is preserved, explicitly deprecated with a migration path, or
  explicitly removed with documented rationale. Silent flattening of
  legitimate per-surface divergence is forbidden.
- **Reversibility**: migration is reversible per-call-site (feature flag or
  shim) until full cutover. A global kill-switch reverts every call-site to
  its legacy module within a documented MTTR target.
- **Observability and audit**: the canonical module's auth-event telemetry,
  per-call-site divergence metrics during shadow mode, and audit-log
  completeness all meet or exceed the strongest of the three legacy modules.
- **Compliance posture**: password storage, MFA enforcement, and session
  timeout must not weaken; the canonical module adopts the strictest setting
  in use across the three legacy modules, or a documented justified exception.
- **Drift-derived incident coverage**: every historical drift-derived incident
  yields a regression test on the canonical module before cutover begins.

## Out of Scope

- Per-call-site shadow-soak length (24 hours vs. 7 days). This is an
  implementation-tier parameter, exposed as configurable policy on the
  canonical module. The brainstorm does not pick the value.
- Canonical-contract format (typed interface plus property tests vs.
  OpenAPI-style document plus contract tests). Tooling-tier decision; both
  are compatible with the canonical-facade scaffolding.
- Identity-provider (SSO/IdP) re-architecture and external-claim-shape
  redesign. The consolidation preserves existing external integrations as-is;
  any external-claim changes are a separate workstream.
- Greenfield auth-protocol changes — switching from sessions to bearer-only,
  introducing new MFA factors, or migrating to a passkey-only flow — are
  explicitly deferred. This brainstorm only consolidates the three existing
  module surfaces.
- Per-service organisational changes (team ownership, on-call rotation
  reassignment, code-ownership routing) downstream of consolidation.
- Cost-modelling and capacity-planning details for the shadow-execution
  budget. Budget exists as a constraint (must be bounded, must throttle on
  exceed) but the absolute number is set during implementation planning.
