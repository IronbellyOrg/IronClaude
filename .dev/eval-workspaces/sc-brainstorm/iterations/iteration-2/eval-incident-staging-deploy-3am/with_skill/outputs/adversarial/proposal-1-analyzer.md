---
persona: analyzer
model: opus
stance: "investigate first, harden second — without a confirmed causal chain, prevention is theater"
---

# Proposal 1 — Analyzer Lens

## Core Stance

The proposed "schema migration with missing backfill" hypothesis is plausible but **not yet evidence-backed**. Before we write a single prevention action, we owe ourselves a disciplined causal reconstruction. Half the value of a post-mortem is in the investigation rigor — sloppy investigation produces prevention actions that target the wrong layer, and we'll be back at 3am within the quarter. My priority push: **investigate to the root, then harden the layer where the root actually lives.**

## Causal Chain Reconstruction (the spine of the post-mortem)

Build the timeline in three passes, each with explicit evidence standards:

1. **Wall-clock timeline** — every observable event, with timestamp source. Deploy pipeline events (ArgoCD/Flux logs), pod lifecycle events (`kubectl get events`), service signal flips (Prometheus alert manager), human actions (Slack timestamps, command history). Evidence standard: **two independent timestamp sources** for every claim. If only one source exists, mark `[single-source]`.

2. **Causal graph** — for each observable, ask "what caused this?" walking backward until you hit either (a) a code change, (b) a config change, (c) a vendor/infra change, or (d) a state change that *should* have been caught earlier. Don't stop at "the deploy" — that's a trigger, not a cause. Use a 5-Whys probe per terminal node, but with a hard rule: each "why" must cite a file, commit, log, or metric. No prose-only causation.

3. **Counterfactual probe** — for the top candidate root cause, ask: "if X had not happened, would the breakage have occurred?" If yes → X is not the root cause. Iterate. Most teams stop at the first plausible cause; this step catches the case where the schema migration is a *contributing factor* but the *real* root is "code path executes write before the feature flag check is even evaluated."

## Hypothesis Testing

Catalog **all** parallel hypotheses, not just the leading one. From the seed brief, at minimum:

- H1: schema migration added non-nullable column without backfill, sibling service threw on read
- H2: code path wrote new column unconditionally (no feature flag check), independent of migration order
- H3: deploy ordering — migration shipped to one pod before the rest, creating a split-brain window during rollout
- H4: dependency / vendor regression (e.g., Postgres driver update, library bump) hiding behind the schema change as a red herring
- H5: cron-driven deploy hit at a time when no one was watching, so the *real* root cause is the deployment policy, and the schema bug is incidental

For each hypothesis, list: **predicted evidence if true** (specific log lines, metric shapes, commit hunks) and **predicted evidence if false**. This is the discipline that prevents "we found the first plausible thing and stopped."

## Evidence Weighting

Score each hypothesis on a 0-1 confidence after evidence collection. Anything above 0.8 across **≥3 independent evidence sources** (logs, metrics, commit, trace) is the publishable root cause. Anything in 0.5-0.8 → "leading hypothesis, unconfirmed, requires follow-up." Below 0.5 → "ruled out."

## Architectural Fitness Functions (the prevention layer I push for)

Once the root cause is confirmed, the prevention I want to push for is **architectural fitness functions** — automated tests that fail the build when the architecture drifts toward the failure mode. Concretely, for this incident class:

- **Migration safety fitness function**: a CI check that parses every migration and rejects any non-nullable column addition without a paired backfill migration OR a feature-flag gate proven by static analysis.
- **Deploy-order fitness function**: assert that migrations always run before code that reads/writes the affected columns (parseable from migration metadata + code grep).
- **Capability fitness function**: assert that no production-path code writes to a column added in the *current* release without a feature flag.

These are higher-value than runbook updates because they're enforced by CI, not by human discipline. A runbook says "remember to backfill"; a fitness function says "the build is red if you don't."

## What I'd Disagree With

- I would push back on any prevention action that's "we'll be more careful." That's not a prevention action; it's a hope. If a finding can be expressed as a fitness function, an alert, or a pipeline gate, do that. If it can't, write it as a runbook step with a verification test.
- I'd push back on "ship the rollback automation first." That solves *recovery*, not *prevention*. We should do both, but starting with rollback means we keep producing the same class of bug — we just notice faster.
- I'd push back on framing this as a "deploy at 3am is bad" story. The deploy time is a confounder, not a root cause. Move the deploy to 10am and we'd still have shipped the broken migration; we'd just have noticed faster.

## What's Out of Scope For Me (Other Personas Should Own)

- Security/audit-trail questions during the mitigation (the manual psql session, the shared admin credential) → security lens.
- The "should staging auto-deploy at 3am with no canary" question → devops lens (release engineering maturity).
- On-call ergonomics and the burnout angle of three 3am pages in 6 weeks → devops lens.
