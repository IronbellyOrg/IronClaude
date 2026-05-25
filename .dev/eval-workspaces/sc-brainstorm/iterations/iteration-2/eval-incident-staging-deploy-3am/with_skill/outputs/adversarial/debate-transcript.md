# Adversarial Debate Transcript

**Topic**: post-mortem: staging deployment broke at 3am, manual revert was the only mitigation
**Participants**: analyzer (opus), security (sonnet), devops (haiku)
**Convergence score**: 0.78
**Status**: PASS

---

## Tension 1 — Investigate first vs. harden first

**analyzer**: We don't yet have an evidence-backed root cause. Writing prevention actions before causal-chain reconstruction is theater. We could end up hardening the deploy pipeline when the actual root is a code-path bug that ignores feature flags, and we'd be back at 3am next month with a different symptom.

**devops**: Disagree on the framing. The pipeline gaps — no canary, no automated rollback, no deploy-window policy — are real *regardless* of tonight's specific root cause. Those should run in parallel with the investigation, not after it. We don't need to know whether H1, H2, or H3 was right to know that auto-deploying at 02:47 UTC with no canary is unsafe.

**security**: I'd insert a third path: audit the *recovery* in parallel with both. The mitigation used a shared admin credential with no logging. Investigation might take days; pipeline hardening will take weeks; the credential gap is closeable this week.

**Resolution**: All three workstreams run in parallel, with explicit ownership. Investigation is the *spine* of the post-mortem narrative; pipeline hardening and audit fixes are independent prevention tracks that don't block on investigation completion.

---

## Tension 2 — Signed-revert vs. single-command revert (v1 baseline reconciliation)

**devops**: Adopt a signed-revert: every deploy registers a "known good" SHA, rollback re-deploys that SHA, the command is logged and attributable. This is what the v1 baseline post-mortem converged on.

**security**: I like signed-revert *because* it's logged. But add: an automated rollback path must also have audit logging — an auto-revert that silently mutates schema is the same risk in a more dangerous package. The "automated" doesn't excuse the "unlogged."

**analyzer**: Fine, but signed-revert is *recovery*, not *prevention*. We should do both, but I want the prevention plan to be explicit that signed-revert improves MTTR — it doesn't reduce the rate at which we ship broken migrations. The architectural fitness function (CI rejects unsafe migrations) is what reduces the rate.

**Resolution**: Both. Signed-revert + auto-revert on SLO breach is the recovery layer (devops + security audit overlay). Migration-safety fitness function in CI is the prevention layer (analyzer). The post-mortem explicitly separates these two control loops.

---

## Tension 3 — Audit completeness vs. MTTR speed

**security**: A 60-second automated revert with no logs is worse than a 5-minute revert with full attribution, in the long run. Audit trail is non-negotiable, especially because staging mitigations are rehearsals for prod.

**devops**: I don't want to slow down the recovery path. If the auto-revert pauses to write to a SIEM and the SIEM is unhealthy, we've now coupled our recovery to our observability stack. That's the wrong coupling.

**analyzer**: There's a middle path: log asynchronously. The revert proceeds; an audit event is queued (locally first, then forwarded). If the audit queue fails, the revert still happens, but the next deploy is blocked until the audit backlog is reconciled. That gives you the recovery speed AND the audit completeness, with a clear failure mode.

**Resolution**: Async audit logging on the recovery path; the next-deploy gate ensures backlogs are reconciled. Audit completeness is a release-gate, not a recovery-blocker.

---

## Tension 4 — Capability bounds and the "two-person rule"

**devops**: Define what an on-caller can do unilaterally. Schema mutations should require a second engineer's approval, even in staging.

**security**: Strong agree. The shared admin credential without a two-person rule is the same threat model as a malicious insider — we shouldn't distinguish between "tired engineer making a mistake" and "compromised engineer making a deliberate change." Both are mitigated by the same control.

**analyzer**: I'm sympathetic but want to flag a confounder: the *reason* the on-caller had to do manual SQL was that the rollback wasn't automated. Fix that first, and the two-person rule applies to a much smaller surface area. Don't add a process gate without first removing the *need* for the gate.

**Resolution**: Two-person rule is the long-term policy; signed-revert + auto-revert reduces how often the policy actually triggers. Both are in the prevention plan; the runbook orders them: try signed-revert first, escalate before any manual DB action.

---

## Tension 5 — On-call ergonomics: a finding or a footnote?

**devops**: Three 3am staging pages in 6 weeks is a pattern, not bad luck. The post-mortem must treat on-call ergonomics as a first-class finding with its own section, owners, and metrics.

**analyzer**: I'd treat it as a *secondary* finding — important, but downstream of the technical root cause. If we fix the deploy pipeline, the pages drop, and the ergonomics issue resolves.

**security**: Splitting the difference: on-call ergonomics is also a security finding. Tired engineers at 3am take shortcuts that expand the credential / audit gaps. Treating it as a footnote is how those gaps persist.

**Resolution**: First-class section in the merged spec, with explicit metrics (page-quality SLO, target: 0 ad-hoc-SQL pages per quarter). Not buried in "future work."

---

## Convergence Assessment

- **Convergence on prevention strategy**: 0.85 — strong agreement on two-control-loop separation (prevent + detect), on signed-revert, on architectural fitness functions, on capability bounds.
- **Convergence on investigation discipline**: 0.80 — agreement that causal-chain reconstruction is required before "publishable root cause" but disagreement remains on whether prevention work blocks on investigation completion.
- **Convergence on audit/security overlay**: 0.75 — agreement that audit trail is required; residual tension on the speed/audit tradeoff for the recovery path (resolved with async logging).
- **Convergence on on-call ergonomics**: 0.70 — agreement that it's a first-class finding; residual disagreement on whether it's primary or secondary.

**Overall convergence**: 0.78 (PASS). The merge can proceed; unresolved tensions are captured in the spec's Open Questions.

**Unresolved**: How aggressive should the deploy-window policy be? (no deploys 22:00-08:00? no unattended deploys ever? business-hours-only?) The three personas have different answers; the post-mortem should propose one and explicitly defer the choice to the team-lead.
