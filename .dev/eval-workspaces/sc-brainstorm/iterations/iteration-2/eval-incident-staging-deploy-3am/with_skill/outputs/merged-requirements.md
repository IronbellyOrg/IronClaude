---
topic: "post-mortem: staging deployment broke at 3am, manual revert was the only mitigation"
domain: incident
strategy: systematic
depth: standard
proposals_target: 3
adversarial_status: pass
convergence_score: 0.78
source_proposals:
  - adversarial/proposal-1-analyzer.md
  - adversarial/proposal-2-security.md
  - adversarial/proposal-3-devops.md
debate_transcript: adversarial/debate-transcript.md
created: 2026-05-25T00:00:00Z
---

# Merged Requirements: Post-Mortem — Staging Deployment Broke at 3am

## Problem Statement

A cron-driven staging deployment at 02:47 UTC broke the API service within ~90 seconds, paged the on-call engineer at 03:02, and was mitigated at 03:41 via a manual `kubectl rollout undo` plus a hand-written `ALTER TABLE` against the `orders` schema using a shared admin credential. The pipeline has no automated rollback, no canary, and no progressive rollout; the manual revert was the only mitigation available. This was the third 3am staging page in six weeks. The post-mortem must (a) establish the proximate technical root cause with evidence, (b) close prevention and detection gaps at both code-path and pipeline-path layers, (c) address the on-call ergonomics pattern, and (d) close the audit-trail gap that left the mitigation actions reconstructible only from shell history and Slack timestamps.

## Post-Mortem Framework

Five principles govern the post-mortem; each has a concrete operationalization, not a slogan.

1. **Blameless but not actionless.** The on-caller who improvised the manual revert saved the environment and should be thanked by name in the document. The systemic fix is to ensure no future on-caller is put in that position. Operationalize: every finding has an owner who is *not* the on-caller, and a due date.

2. **Two-control-loop discipline: prevention AND detection, tracked separately.** A finding that says "the migration was unsafe → we'll review migrations more carefully" is *neither* prevention nor detection. A prevention finding makes the bug class impossible to ship; a detection finding makes the bug class caught faster. Operationalize: every finding is tagged `prevention` OR `detection` OR `recovery`; the document enumerates each track separately.

3. **Evidence-backed root cause.** Every claim about root cause cites a log line, metric, trace, or commit reference. Hypotheses without evidence are surfaced as hypotheses, not stated as fact. Operationalize: minimum three independent evidence sources before a hypothesis is promoted to "root cause"; counterfactual probe applied to the leading hypothesis.

4. **Architectural fitness functions over runbook discipline.** Where a finding can be expressed as a CI check, a pipeline gate, or an automated alert, it must be — not as a human-discipline reminder. Operationalize: each prevention action specifies its enforcement mechanism (CI, pipeline, alert, runbook); runbook-only enforcement is the last resort and must be justified.

5. **On-call ergonomics is a first-class finding.** A page that requires ad-hoc DB surgery is itself a finding, not a footnote. Page-quality is a release-engineering metric. Operationalize: dedicated section in the post-mortem with metrics, owners, and target SLOs for page-quality.

6. **Audit completeness is non-negotiable for production parity.** Staging mitigations are rehearsals for prod mitigations. If the staging revert isn't audit-complete, the prod revert won't be either. Operationalize: every mitigation action — automated or manual — flows through a logged, attributable channel.

7. **Recovery speed must not trade against audit completeness.** Async audit logging on the recovery path; the recovery proceeds, audit events queue locally and forward asynchronously, and the *next deploy* is gated on audit-backlog reconciliation. This separates the recovery-blocker from the release-gate.

## Required Investigation Steps

Investigation runs in parallel with prevention work; investigation completion is not a blocker for closing pipeline gaps that are unsafe regardless of tonight's specific root cause.

1. **Build the wall-clock timeline** with every observable event and two independent timestamp sources per claim. Sources: ArgoCD pipeline logs, `kubectl get events`, Prometheus AlertManager, Slack timestamps, on-caller's shell history (`~/.bash_history`, `~/.psql_history`). Mark `[single-source]` where corroboration is missing. Evidence standard: timeline is reviewable by a third party who was not present.

2. **Construct the causal graph.** For each observable event in the timeline, ask "what caused this?" Walk backward until you reach a code change, config change, vendor change, or state change that should have been caught earlier. Each "why" cites a file, commit, log, or metric — no prose-only causation. Apply a 5-Whys probe with the hard rule that each "why" has a primary-source citation.

3. **Catalog parallel hypotheses.** At minimum: H1 (schema migration without backfill), H2 (code path writes without feature flag check), H3 (deploy ordering creating split-brain), H4 (vendor/library regression masquerading as schema bug), H5 (deployment policy itself as root cause, schema bug as incidental). For each hypothesis, document predicted evidence if true *and* if false.

4. **Apply the counterfactual probe** to the leading hypothesis: "if X had not happened, would the breakage have occurred?" If yes → X is a contributing factor, not the root cause. Iterate until you find the cause whose absence would have prevented the breakage.

5. **Score and rank hypotheses** on confidence (0-1) after evidence collection. Publishable root cause requires ≥0.8 confidence across ≥3 independent evidence sources. Hypotheses in 0.5-0.8 are documented as "leading, unconfirmed, requires follow-up." Below 0.5 → "ruled out, with evidence."

6. **Reconstruct the mitigation actions** end-to-end: every command the on-caller executed, every Slack message, every credential checkout. Cross-reference against authoritative logs (not just human memory). Gap analysis: which mitigation actions cannot be reconstructed from logs alone? Each gap is an audit finding.

7. **Quantify the exposure window** across data, credential, network, and identity planes. Even on staging, document the *act of quantifying* — this is the discipline that catches the case where "no impact" was hand-waved.

8. **Diff the dependency tree** from last-good release to broken release. Migration framework bumps, ORM bumps, driver bumps are silent contributors to schema-shape bugs. Document any dep changes; flag for follow-up if any touch migration semantics.

## Prevention Acceptance Criteria

Each prevention action has an owner (placeholder names for the eval; the team lead assigns real owners) and a due date relative to post-mortem publish (`+Nd` = N days after publication).

1. **Migration-safety CI fitness function.** Static analysis of every migration PR rejects: (a) non-nullable column addition without paired backfill migration; (b) DROP COLUMN on a column referenced by code in HEAD; (c) any migration not accompanied by a paired down-migration *or* an explicit `@unsafe-no-rollback` annotation reviewed by two engineers. Owner: platform-eng-lead. Due: +14d. Enforcement: CI required-check.

2. **Feature-flag-gated schema writes.** Any code path that writes to a column added in the *current* release must be gated by an explicitly named feature flag, statically verifiable. Owner: backend-tech-lead. Due: +21d. Enforcement: CI fitness function + code-review checklist.

3. **Signed-revert capability.** Every deploy registers a "known good" SHA. Rollback is a one-command operation that re-deploys that SHA, logged and attributable. Schema-affecting migrations register a paired down-migration; the rollback path runs the down-migration as part of the revert. Owner: devops-lead. Due: +30d. Enforcement: pipeline-gated; deploys without registered known-good are blocked.

4. **Two-person rule for emergency DB mutations.** Manual `ALTER`, `UPDATE`, `DELETE` against any environment (including staging) requires a second engineer's approval, captured in a break-glass system. Owner: security-lead. Due: +30d. Enforcement: break-glass CLI wrapper that refuses to exec without a second approver token.

5. **Shared admin credentials eliminated or vaulted.** All shared DB admin credentials are either removed (replaced by per-user attributable credentials) or vaulted with checkout/return cycle. Every checkout writes to audit. Owner: security-lead. Due: +45d. Enforcement: Vault policy + post-incident credential rotation.

6. **Deploy-window policy.** Default: no unattended deploys 22:00-08:00 local time. Opt-in for after-hours deploys requires explicit operator presence + canary gating. Cron-driven deploys removed from staging unless they meet the opt-in criteria. Owner: devops-lead. Due: +14d. Enforcement: pipeline rejects cron-scheduled deploys outside business hours unless flagged.

7. **Dependency diff in deploy notes.** Every deploy auto-generates a dependency diff from the last successful release; if migration-framework or DB-driver versions changed, the deploy is flagged for human review. Owner: platform-eng-lead. Due: +21d. Enforcement: pipeline annotation + reviewer assignment.

## Detection Improvements

Tracked separately from prevention. Each has a target detection latency.

1. **Synthetic transaction probes.** End-to-end transactions (create order → read order → cancel order) run every 60s; page on 3 consecutive failures. Target detection latency: <3 minutes from breakage. Owner: sre-lead. Due: +21d.

2. **Deploy-correlated alerts.** Every alert annotates "deploy X happened Y minutes ago" so the on-caller has the causal hint pre-loaded. Owner: sre-lead. Due: +14d.

3. **Schema-shape canary.** Before a migration is applied to the main DB, it runs against a shadow DB; alert if the shadow DB shape diverges from production expectations. Target detection: before any user-visible impact. Owner: platform-eng-lead. Due: +30d.

4. **Page-quality SLO.** "Pages requiring ad-hoc DB surgery": target 0 per quarter; current 3 per 6 weeks. Tracked in the on-call dashboard; reviewed monthly. Owner: eng-manager. Due: +7d (instrumentation), then ongoing.

5. **Auto-revert SLO breach trigger.** If error-rate or p99-latency exceeds threshold within 10 minutes of deploy, auto-revert fires; page goes out *after* the revert with "we auto-reverted X, here's why." Owner: devops-lead. Due: +45d.

## On-Call Ergonomics

This section addresses the human-cost dimension the technical post-mortem would otherwise bury.

- **Three 3am pages in 6 weeks is a pattern, not bad luck.** The current pipeline maturity is inflating the on-call burden. The fix is upstream (canary + auto-revert), not downstream (more sleep aids).
- **Capability bounds for unilateral mitigation.** Define what an on-caller can do alone vs. what requires a second engineer. Schema mutations: two-person rule. Pod restarts, config reloads, traffic shifts: unilateral. Document explicitly in the runbook; do not leave to judgment-under-stress.
- **Runbook ergonomics.** The runbook for "deploy broke staging" reads in order: (1) check auto-revert status; (2) if not reverted, run signed-revert command; (3) if signed-revert fails, escalate to second-on-call *before* any manual DB action; (4) manual DB action requires break-glass approval.
- **No-blame ergonomics.** The post-mortem explicitly thanks the on-caller who improvised the mitigation. The text makes clear that the systemic fix is to never put another on-caller in that position. This is not boilerplate — it shapes whether the next on-caller takes the necessary risk or freezes.
- **Sleep-debt and recovery time.** The on-caller who took a 3am page gets the next morning off, no questions. Tracked in the on-call dashboard so the pattern is visible to management.
- **Burnout signal.** "Number of after-hours pages per on-caller per quarter" is a tracked metric. Threshold breached → trigger pipeline-maturity review, not "talk to the engineer about resilience."

## Communication Plan

- **Internal post-mortem** published within 5 business days. Distributed to: directly affected team (eng-eng, sre, security), eng-leadership, on-call rotation members.
- **Cross-team summary** (1-page) within 10 business days for any team whose roadmap is affected by the prevention work (e.g., the migration-safety CI gate affects every team that ships migrations).
- **Customer comms**: none required (staging-only impact). Document the *decision* to skip customer comms in the post-mortem so the reasoning is preserved.
- **Follow-up review** scheduled at +45d to confirm all due dates met; any slipped action gets an explicit re-owner and new due date, captured in a follow-up doc (not silently dropped).
- **Cross-org sharing**: anonymized version (no engineer names, no credential specifics) shared to internal eng-all channel as a learning artifact.

## Open Questions

These are honest residuals from the adversarial debate that the team-lead must resolve:

1. **Deploy-window policy aggressiveness.** Three positions surfaced: (a) no deploys 22:00-08:00 ever; (b) business-hours default with opt-in for after-hours; (c) attended-deploy-only with no time restriction. The post-mortem proposes (b); team-lead confirms or overrides.
2. **Sequencing of pipeline hardening vs. investigation depth.** Investigation runs in parallel with pipeline hardening, but if the investigation reveals a root cause that re-prioritizes hardening (e.g., a vendor regression that suggests dependency-pinning is the higher-value gap), how do we reconcile? Proposed: weekly checkpoint during the first 30 days.
3. **Two-person rule scope.** Should it apply to all environments uniformly, or graduated (staging = single-person + post-hoc audit, prod = two-person live)? Security-lens pushes for uniform; devops-lens pushes for graduated to reduce friction.
4. **Architectural fitness function maintenance cost.** CI checks have ongoing maintenance burden; who owns keeping them green as the codebase evolves? Proposed: the team that owns the affected subsystem; team-lead confirms.

## Provenance

Trace from requirement back to the proposal that originated it.

| Requirement | Source |
|-------------|--------|
| Causal graph + counterfactual probe (Investigation §1-5) | analyzer |
| Architectural fitness functions / migration-safety CI (Prevention §1-2, §7) | analyzer |
| Blast-radius across four planes, exposure-window quantification (Investigation §7) | security |
| Audit-trail completeness, shared-credential elimination (Prevention §4-5; Framework §6-7) | security |
| Credential-review-under-stress, supply-chain dep diff (Investigation §8) | security |
| Release-engineering maturity scoring, canary + signed-revert + auto-revert (Prevention §3, §6; Detection §5) | devops |
| Deploy-window policy (Prevention §6) | devops |
| On-call ergonomics, page-quality SLO, capability bounds (On-Call Ergonomics §all; Detection §4) | devops |
| Two-control-loop discipline (Framework §2) | analyzer + devops (joint) |
| Async audit logging on recovery path (Framework §7) | security + analyzer (resolution from debate Tension 3) |
| Two-person rule (Prevention §4) | security + devops (joint) |
| Synthetic transaction probes, deploy-correlated alerts (Detection §1-2) | devops |
| Schema-shape canary (Detection §3) | analyzer + devops (joint) |
| Communication plan, follow-up review (Communication §all) | merged from all three (procedural floor) |
| Open question 1 (deploy-window aggressiveness) | unresolved tension from debate |
| Open question 2 (sequencing) | unresolved tension between analyzer and devops |
| Open question 3 (two-person scope) | unresolved tension between security and devops |
| Open question 4 (fitness function maintenance) | analyzer surfaced; not resolved in debate |
