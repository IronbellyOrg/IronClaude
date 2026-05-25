---
topic: "post-mortem: staging deployment broke at 3am, manual revert was the only mitigation"
domain: incident
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-05-25T00:00:00Z
---

# Seed Brief: post-mortem-staging-deploy-3am

## Problem Statement

A scheduled staging deployment kicked off at approximately 02:47 UTC and immediately broke the environment — service health endpoints flipped red within ~90 seconds and synthetic monitors failed shortly after. The on-call engineer was paged at 03:02, and after ~25 minutes of unsuccessful forward-fix attempts, executed a manual `kubectl rollout undo` followed by a hand-written DB schema patch to bring the environment back online at 03:41. The deployment pipeline had no automated rollback path; the manual revert was effectively the *only* mitigation available. We need a post-mortem that establishes root cause with evidence, prevents recurrence at both detection and prevention layers, and addresses the on-call ergonomics of a 3am page that demanded ad-hoc database surgery.

## Known Context

- **Timeline**: deploy started 02:47 UTC, breakage detected 02:48-02:50 UTC, page fired 03:02 UTC, manual revert completed 03:41 UTC. MTTR ≈ 54 minutes from breakage; ≈ 39 minutes from page.
- **Trigger**: scheduled nightly auto-deploy of `staging` branch to staging cluster (cron-driven, not gated by canary or progressive rollout).
- **Failure surface**: API service returned 500s on all endpoints touching the `orders` table; readiness probes failed after ~90s warmup; downstream worker pool back-pressured.
- **Mitigation actually applied**: `kubectl rollout undo deployment/api -n staging` + manual `ALTER TABLE orders DROP COLUMN tax_jurisdiction_code` to back out a partial schema migration that the new code had begun writing to.
- **No automated rollback exists**: pipeline has no signed-revert, no canary gate, no progressive rollout. The manual revert was the on-caller improvising under pressure.
- **Suspected proximate cause (unconfirmed)**: a schema migration in the new release added a non-nullable column without a backfill; legacy reads in a sibling service threw on the new constraint. Hypothesis is not yet evidence-backed.
- **No customer impact** (staging only) — but the on-caller lost ~1.5 hours of sleep, and this is the third 3am staging page in the past 6 weeks.
- **Audit trail during mitigation**: the manual `ALTER TABLE` was executed via a personal psql session with a shared admin credential; no command was logged to a central audit system. Recovery actions are reconstructible only from shell history and Slack timestamps.

## Constraints

- Post-mortem must be blameless and follow the existing template (`docs/post-mortems/TEMPLATE.md`).
- Findings must be evidence-backed: every claim about root cause needs a log line, metric, trace, or commit reference.
- Prevention actions must have a named owner and a due date — no "we should consider..." entries.
- Detection improvements must be tracked separately from prevention (two-control-loop discipline: prevent the bug from shipping AND catch it faster if it ships anyway).
- Recommendations must not assume new headcount or budget. Existing tools (Argo Rollouts, Prometheus, OpenTelemetry, Vault) are in-house but underused.
- On-call ergonomics matter: a 3am page that requires hand-written SQL is itself a finding, not just a footnote.
- Audit trail completeness is non-negotiable for production parity — staging mitigations must be reconstructible.

## Success Criteria

- Root cause identified with ≥3 independent evidence sources (logs + metrics + commit/PR).
- Concrete prevention actions enumerated with owner + due date, covering both code-path and pipeline-path causes.
- Concrete detection improvements enumerated separately, with target detection latency (e.g., "<5 min from deploy start").
- Rollback capability is automated and signed-off — manual `kubectl undo` is no longer the primary mitigation strategy.
- On-call ergonomics are addressed: a 3am page should not require ad-hoc DB surgery. Runbook + safe revert button + capability bounds for unilateral mitigation.
- Audit trail: all mitigation actions (including emergency DB writes) flow through a logged, attributable channel.
- Post-mortem document is sharable with the broader engineering org within 5 business days.

## Open Questions

- Was the schema migration actually the root cause, or a symptom of a code path that should never have written the new column without feature-flagging?
- Why is staging on auto-deploy at 02:47 UTC with no canary? Is this a deliberate choice (treat staging as a chaos environment) or a process gap?
- Should the team adopt automated rollback (e.g., Argo Rollouts with auto-promote) before, after, or alongside fixing the proximate migration bug?
- What's the right "capability bound" for on-call: which mitigations can a single engineer execute unilaterally vs. which require a second pair of eyes?

## Enrichment Context

_No enrichment performed for this evaluation pass — seed brief built from Socratic dialogue alone per --depth standard defaults. Codebase/research enrichment skipped to keep the eval-controlled comparison clean against the v1 baseline._
