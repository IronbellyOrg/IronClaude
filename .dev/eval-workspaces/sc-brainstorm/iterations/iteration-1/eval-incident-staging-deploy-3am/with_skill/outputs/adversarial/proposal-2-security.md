---
proposal_id: 2
agent: sonnet:security
focus: blast radius, exposure window, control gaps
---

# Proposal 2 — Security Lens

## Frame

Staging is not "just staging." Staging frequently runs against
production-shaped data (anonymized but realistic), production-shaped
credentials (separate but parallel scope), and production-shaped
integrations (real third-party sandboxes, real SSO IdPs in test
realms). A break in staging at 3am with manual-only mitigation is a
control-plane incident first, a code incident second. The first job is
to harden — investigate causally *after* the exposure window is
closed.

## Blast-Radius Inventory (mandatory before causal analysis)

1. **Data plane.** Did the broken deploy write to any persistent store
   (RDS, S3, Redis, message queues)? If yes, is the data corrupt,
   half-written, or merely paused? Half-written transactions are a
   silent corruption risk that outlives the revert. Audit by
   comparing row counts / checksums against pre-deploy snapshots
   where possible.

2. **Credential plane.** Did the deploy mint, rotate, or expose any
   secrets (env vars logged, debug endpoints enabled, IAM role
   bindings changed)? A buggy deploy that left a debug route exposed
   for 60 minutes is a separate incident from the original bug.
   Inventory every credential the deployed artifact touches.

3. **Network plane.** Did the deploy modify ingress/egress rules,
   security groups, VPC configs, or service-mesh policies? Network
   plane drift survives application-layer reverts.

4. **Identity/access plane.** Were any access grants, tokens, or
   service-account bindings rotated as part of the deploy? Were any
   exposed in logs during the failure window?

## Control-Gap Audit

The fact that manual revert was the *only* mitigation reveals at least
four control gaps:

- **No automated rollback** — the deploy system lacked (or did not
  trigger) auto-revert on health-check failure.
- **No deploy gating** — health-check / smoke-test passed (or wasn't
  run) for a build that immediately broke the environment.
- **No off-hours guardrail** — 3am deploys to staging should require
  either explicit override or extra approval, and probably alert
  someone other than the deployer.
- **No paging on staging-only failure** — detection was apparently
  slow enough that someone "found" the break rather than being paged
  to it.

Each gap is a separate prevention item with a separate owner. Do not
collapse them into one "improve CI" line.

## Exposure Window

The window from "deploy completed broken" to "revert completed +
verified" is the exposure window. Even in staging, this window:

- Halts contract-test runs from other teams → false-negative signal
  about their own changes.
- Risks staging-test data inconsistency if writes were in flight.
- May leak to monitoring/alerting noise that desensitizes the on-call
  rotation ("staging is always broken").

Quantify the window. If it exceeded 30 minutes, the SLO-equivalent for
staging is also broken and that's a separate finding.

## Investigate-After-Harden Sequence

1. Close exposure window: confirm revert is fully effective across all
   four planes (data, credential, network, identity).
2. Inventory blast radius across those planes; document.
3. Then — and only then — investigate root cause with the analyzer's
   methodology. Hardening cannot wait on root cause.

## Acceptance Criteria

- Blast radius documented for all four planes (each plane either
  "clean" with evidence or "dirty" with remediation plan).
- Each of the four named control gaps has an owner and a due date.
- Exposure window quantified to the minute; if >30m, escalated.
- Detection improvements named separately from prevention
  improvements — they are different control loops.
