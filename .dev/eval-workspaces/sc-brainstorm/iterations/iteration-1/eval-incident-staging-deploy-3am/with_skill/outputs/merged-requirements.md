---
spec_type: requirements
domain: incident
strategy: systematic
adversarial_status: pass
convergence_score: 0.72
proposal_count: 2
source_seed: ../seed-brief.md
agents: [opus:analyzer, sonnet:security]
created: 2026-05-25T00:00:00Z
---

# Merged Requirements — Staging 3am Deploy Post-Mortem

## Problem Statement

A staging deployment at ~03:00 broke the staging environment, with
manual revert by the on-caller as the only effective mitigation. The
post-mortem must (a) reconstruct an evidence-based timeline, (b) name
a single counterfactual root cause plus contributing factors, (c)
inventory blast radius across data / credential / network / identity
planes, and (d) produce leverage-rated prevention items that close
both the bug-class gap and the response-control gap. Two control
loops failed — the deploy-gate loop (broken build shipped) and the
mitigation loop (no automated rollback). The post-mortem must treat
both as first-class outputs.

## Post-Mortem Framework

1. **Blameless framing.** Names omitted; roles named. No "should
   have" language; only "the system as-built did X; the system as
   desired would do Y."
2. **Evidence-cited timeline.** Every event has ≥2 independent
   sources (deploy audit log, application logs, infra metrics). Single-
   witness events flagged as evidence gaps and assigned a follow-up.
3. **Root cause + contributing factors, separately documented.**
   Root cause = smallest counterfactual change. Contributing factors
   = conditions that turned the root cause into an outage (missing
   control, off-hours deploy, slow detection, etc.).
4. **Parallel investigation tracks.** Causal track (analyzer-led) and
   hardening track (security-led) run concurrently, not sequentially.
   Hardening does not wait on root cause; root cause does not wait on
   exposure-window closure.

## Required Investigation Steps

1. **Reconstruct timeline.** Pull deploy audit log, app logs, infra
   metrics. Build minute-level event sequence with ≥2 sources per
   event. Output: timestamped event table.
2. **Diff the deploy artifact.** Enumerate change surface across
   code commits, config changes, dependency bumps, IaC changes, and
   secret/credential rotations between known-good and broken builds.
   This is the candidate-cause pool — exclude anything outside it.
3. **Inventory blast radius across four planes.** For data,
   credential, network, and identity planes: confirm "clean with
   evidence" or "dirty with remediation plan." Includes checking for
   half-written transactions, leaked debug endpoints, drifted
   network rules, and rotated/exposed access grants.
4. **Hypothesis testing.** Form 2-3 competing causal hypotheses;
   list supporting and refuting evidence for each; run cheap
   refutations first; document rejected hypotheses to avoid re-
   debating later.
5. **Quantify exposure window.** First-failure to revert-verified, in
   minutes. If >30m, escalate as separate finding against the
   staging-availability expectation.

## Prevention Acceptance Criteria

1. **One counterfactual root cause named.** Phrased as "had X not
   changed, the incident would not have occurred."
2. **Contributing factors enumerated separately**, each with
   prevention leverage rated as class-level (catches the category)
   or case-level (catches this specific bug). Class-level items get
   priority funding.
3. **Four control-gap prevention items named, each with owner and
   due date:** automated rollback on health-check failure; deploy
   gating with smoke tests; off-hours deploy guardrail; paging on
   staging-only failure.
4. **Detection improvements documented separately from prevention
   improvements** — these are different control loops and must not
   be collapsed.
5. **Pattern check completed:** has any post-mortem in the last 90
   days named a similar root-cause category or a similar control-gap
   category? If yes, escalate as a recurring systemic issue.

## Open Questions

1. What is the actual blast-radius depth for a staging-only event —
   how thorough must the data-plane corruption check be when no
   end-user traffic was involved? (Residual tension from debate;
   convergence not reached on this scope question.)
2. Why did the deploy happen at 03:00 — scheduled automation,
   accidental trigger, or chasing a previous failed deploy? This
   determines whether the off-hours-guardrail prevention item is
   targeting a recurring pattern or a one-off.

## Communication Plan

- **Internal eng audience:** post-mortem document published within 5
  business days; reviewed in next eng-wide post-mortem forum.
- **Affected teams (QA, integration test consumers):** direct ping
  on the staging-availability channel with revert ETA during the
  incident and link to the post-mortem doc when published.
- **Engineering leadership:** summary surfaces (a) the root cause
  category, (b) the four control gaps with owners and due dates, and
  (c) the pattern-check result. No customer comms required — staging
  scope.
- **Follow-up cadence:** prevention items tracked in a single epic
  with weekly status until all four control-gap items are closed.
