---
persona: devops
model: haiku
stance: "the deploy practice is the root cause; the migration bug is just what fell out tonight"
---

# Proposal 3 — DevOps Lens

## Core Stance

The proximate cause is a schema migration bug. The **root cause** — in the release-engineering sense — is a deployment practice that ships unattended at 3am with no canary, no progressive rollout, no automated rollback, and no SLO-based gating. The migration bug is what fell out *tonight*; if not this, then something else next month. My priority push: **harden the delivery pipeline so the next bug-class doesn't become a 3am page, and address on-call ergonomics so the team doesn't burn out from a backlog of 3am incidents we keep treating as one-off bad luck.**

## Release Engineering Maturity (the gap analysis)

Rate the current pipeline on a 0-4 maturity scale across six dimensions:

| Dimension | Current | Target | Gap |
|-----------|---------|--------|-----|
| Progressive rollout (canary → 10% → 50% → 100%) | 0 (instant 100%) | 3 (auto-promote with SLO gate) | Big |
| Automated rollback on SLO breach | 0 (manual `kubectl undo`) | 3 (auto-revert on alert) | Big |
| Pre-deploy migration dry-run | 0 (migration runs at deploy) | 2 (shadow run + diff) | Medium |
| Deploy-window policy (e.g., no deploys 22:00-08:00 unless attended) | 0 (cron at 02:47) | 2 (business-hours default, after-hours opt-in) | Medium |
| Health-check coverage (readiness probes match real-world failure modes) | 1 (basic probe, didn't catch the schema bug for 90s) | 3 (synthetic transaction probes) | Medium |
| Audit trail of pipeline actions | 1 (ArgoCD logs) | 3 (pipeline + DB actions in unified audit) | Medium |

This table *is* the prevention plan. We don't need to fill every cell to 4 to win; closing the 0→2 gaps would have either prevented this incident or made it a non-event.

## Canary & Progressive Rollout Practices

Concrete recommendation: adopt **Argo Rollouts** (already deployed in the cluster for one other service) as the standard deployment controller. Default rollout:

1. Deploy to 1 pod (canary). Run synthetic transaction probe for 5 minutes.
2. If probe passes AND error-rate-delta < 1% vs. baseline AND p99-latency-delta < 20% → promote to 25%.
3. Same gate → 50% → 100%.
4. At any gate, if probe fails or SLOs breach → auto-revert to previous ReplicaSet (this is the rollback).

For migrations specifically: the migration runs **separately from the code rollout**, with its own dry-run-then-execute step, and the code rollout is gated on the migration completing successfully *and* a feature flag being explicitly enabled. This decouples the two failure modes that conflated in this incident.

## Automated Rollback

A pipeline that requires a human to type `kubectl rollout undo` at 3am is not a rollback strategy; it's a recovery improvisation. Concretely:

- **Signed-revert** (per the v1 baseline reconciliation): every deploy registers a "known good" SHA. Rollback is a one-command operation that re-deploys that SHA. The command is logged, attributable, and idempotent.
- **Auto-revert on SLO breach**: if error rate, p99 latency, or readiness-probe failure crosses threshold within 10 minutes of deploy, the pipeline auto-reverts without human intervention. Page fires *after* the rollback completes ("we auto-reverted X, here's why") rather than *before* ("X is broken, you decide what to do").
- **Schema rollback**: schema-affecting migrations register a paired down-migration as part of the deploy. The rollback path runs the down-migration as well as the code revert. If a down-migration is unsafe (e.g., DROP COLUMN on a populated column), the deploy is *rejected at PR time*, not at 3am.

## On-Call Ergonomics & Burnout

This is the finding that often gets buried in a release-engineering post-mortem. Surface it explicitly:

- **Three 3am staging pages in 6 weeks is a pattern, not bad luck.** The team's effective on-call burden is being inflated by a delivery pipeline that treats staging as a chaos environment. The cost shows up as sleep debt, attention degradation during business hours, and eventual attrition.
- **Capability bounds for unilateral mitigation**: define what an on-caller can do alone vs. what requires a second engineer ("two-person rule for schema mutations even in staging"). This protects the on-caller from being the sole point of failure on a high-stakes decision at 3am.
- **Page-quality SLO**: track "pages that required ad-hoc DB surgery" as a leading indicator of pipeline maturity. Target: 0 per quarter. Currently: 3 in 6 weeks.
- **Runbook ergonomics**: the runbook for "deploy broke staging" should not be "improvise with psql." It should be: (1) check auto-rollback status; (2) if not reverted, run signed-revert command; (3) if signed-revert fails, escalate to second-on-call before any manual DB action; (4) any manual DB action requires break-glass approval logged to audit.
- **No-blame ergonomics**: the on-caller who did the manual `ALTER TABLE` saved the environment. The post-mortem must explicitly thank them, *and* must make clear that the systemic fix is to never put another on-caller in that position again.

## SLO Impact & Observability

- Define an SLO for the staging environment itself ("staging is available 95% of business hours") so we have a measurable signal of whether changes are improving or degrading the pattern.
- Synthetic transaction probes: run end-to-end transactions every 60s, page if 3 consecutive fail. This would have caught this incident in ~3 minutes instead of waiting for readiness probes to flap.
- Deploy-correlated alerts: every alert should annotate "deploy X happened Y minutes ago" so the on-caller has the causal hint pre-loaded.

## What I'd Disagree With

- I'd push back on "investigate to the root before changing anything" (the analyzer's stance). The pipeline gaps are real *regardless* of tonight's root cause. We should be doing the investigation AND closing the canary/rollback gaps in parallel — they're not on the same critical path.
- I'd push back on framing audit trail as the *primary* gap (the security lens). It's real, but it's downstream of "we shouldn't need humans executing manual SQL at 3am in the first place." Fix the need, then audit the residual.
- I'd push back on any prevention plan that doesn't have an on-call ergonomics section. A post-mortem that focuses only on the technical bug and ignores the human cost is incomplete.

## What's Out of Scope For Me

- The detailed causal-chain reconstruction methodology → analyzer lens.
- The credential review and exposure-window quantification → security lens.
- The depth of architectural fitness functions in CI → analyzer lens (though I'd happily consume them as pipeline gates).
