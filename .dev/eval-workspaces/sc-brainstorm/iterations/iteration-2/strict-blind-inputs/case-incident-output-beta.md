# Brainstorm Requirements — Post-Mortem: Staging Deployment Broke at 3am (Manual Revert)

**Command**: `/sc:brainstorm "post-mortem: staging deployment broke at 3am, manual revert was the only mitigation" --depth deep`
**Protocol**: v1 (brainstorm.md)
**Output type**: REQUIREMENTS SPECIFICATION ONLY (no architecture, no code)

---

## Intro

The triggering event is an **incident-style brainstorm**: a staging environment deployment failed at 03:00 local time, and the only mitigation available to the on-call engineer was a **manual revert** (presumably hand-edited rollback or `git revert` + redeploy executed under load). The user is asking for a structured post-mortem requirements discovery — i.e., *what would a "good post-mortem and prevention program" need to contain* — not the post-mortem itself.

Per v1 protocol the goal is to transform this ambiguous incident into a concrete **requirements specification** for the post-mortem deliverable and the preventive program around it. Implementation, architecture diagrams, and runbook code are explicitly out of scope and will be handed off to `/sc:design` and `/sc:workflow`.

### Phase 0 — Codebase Context Decision

Topic mentions "deployment" — borderline code-related under v1's Signal A (could imply pipeline / deploy code). However:
- No file paths, no language extensions, no framework names.
- No development action verbs (implement / build / refactor) — only incident verbs (broke, revert, mitigation).
- No project-specific terms identified in the topic string.

v1 edge-case rule: *"If uncertain whether topic is code-related, do NOT trigger. False negatives are preferred over wasting tokens on business/strategy brainstorms."*

**Decision: SKIP Phase 0 codebase context loading.** This is a process / post-mortem brainstorm, not a codebase change request. If the user later wants to inspect the actual deploy pipeline code, they can re-run with `--codebase`.

---

## Phase 1 — Explore (Socratic Dialogue)

Generated 10 questions, answered with the most plausible incident-specific framings.

### Q1. What does "broke" mean — hard failure, soft regression, or partial outage?
**A.** Most likely a **service-level break observable to staging consumers**: failed health checks, 5xx surge, or crash-looping pods. The fact that on-call escalated to revert (rather than wait it out or roll forward) implies signals exceeded a tolerance threshold — not a cosmetic regression.

### Q2. Why was 3am the discovery time — was the deploy scheduled, drifted, or triggered by an upstream event?
**A.** Three plausible framings: (a) **off-hours release window** (intentional, low-traffic), (b) **delayed pipeline** that started business-hours but only reached staging at 3am, or (c) **automated nightly redeploy** (CI cron, dependency bump bot, infra refresh). Each has different prevention implications; the post-mortem must distinguish them.

### Q3. Why was *manual* revert the *only* mitigation? What failed in the automated rollback path?
**A.** This is the load-bearing question. Candidates: (a) no automated rollback exists, (b) rollback exists but requires healthy CI and CI was also red, (c) rollback exists but on-call wasn't trained/authorized to invoke it, (d) rollback exists but the failure mode (e.g., DB migration) made it non-trivially reversible. Each is a separate preventive workstream.

### Q4. Who was on-call, and did they have the tools / access / runbook needed?
**A.** Assume **single on-call engineer**, possibly junior or rotation-fresh. Likely gaps: no rollback runbook, no break-glass credentials cached locally, no documented "who to wake up" escalation tree past the primary. Post-mortem must audit the on-call experience, not just the system failure.

### Q5. Was this a *staging-only* problem, or does staging behavior predict a future production incident?
**A.** **Staging is the canary by design.** A 3am staging break that needed manual mitigation is a high-value warning: the same deploy path would fail in prod with worse blast radius. The post-mortem's prevention requirements must treat this as a near-miss for production.

### Q6. What signals fired (or failed to fire) and how was the engineer notified?
**A.** Assume some monitor paged. Open question: was the page *actionable* (specific failing service / clear runbook link) or *vague* (synthetic check failed, no context)? Post-mortem must capture alert quality, MTTD (time to detect), MTTA (time to acknowledge), MTTR (time to revert).

### Q7. Was there a recent change in the deploy pipeline, dependencies, or infra config?
**A.** Failures of this class typically correlate with one of: dependency version bump, base-image refresh, IaC change, secret rotation, or a feature flag flip. Post-mortem must reconstruct the **change timeline for the prior 24-72h**, not just the deploy artifact under investigation.

### Q8. Is "manual revert" a recurring pattern or a first-time event?
**A.** If recurring, this is a **systemic gap**, not an incident — the requirements must include trend analysis from past incidents and on-call handoff notes. If first-time, requirements scope narrows to this specific failure plus generic resilience hardening.

### Q9. What blameless culture norms should the post-mortem honor?
**A.** Post-mortem must be **blameless by construction**: focus on system/process failures, not on the on-call engineer's keystroke choices at 3am. Action items framed as "the system should not have required X" rather than "the engineer should have done Y".

### Q10. What is the success criterion for the *prevention program* spawned by this post-mortem?
**A.** Concrete, measurable: "Next time a staging deploy fails outside business hours, the on-call engineer can mitigate using a documented one-command rollback within MTTR ≤ 15 minutes, without writing custom commands or escalating." This becomes the north-star acceptance criterion.

### Socratic Q&A Summary

The exploration converged on five workstreams: **(1)** reconstruct the incident timeline and surface the true root cause(s); **(2)** audit the automated rollback gap that forced the manual revert; **(3)** evaluate alert quality and on-call ergonomics; **(4)** identify the upstream change that introduced risk; **(5)** treat staging-at-3am as a near-miss signal for production. The post-mortem deliverable must be **blameless**, **evidence-based**, and produce **action items with owners and target dates**.

---

## Phase 2 — Multi-Persona Analysis

Five domain perspectives, ~250 words each.

### Persona 1: Analyzer (Root Cause)

The analyzer's lens treats "deployment broke" and "manual revert was the only mitigation" as **two distinct failures** requiring independent root-cause analysis. The first is a *deploy-time* failure: something in the artifact, config, or environment was incompatible with staging. The second is a *resilience* failure: the recovery path did not auto-engage. Conflating them produces shallow fixes.

For RCA, the post-mortem must use a structured method — **5-Whys** for linear causality, plus **causal-chain diagramming** (Cynefin "complicated" domain) when multiple contributing causes interleave. The analyzer rejects the first plausible cause; for example, if logs show "OOMKilled" the analyzer asks *why now*, *why this pod*, *why no headroom*, *why no canary catch*, *why no auto-rollback*, until reaching a class-of-failure conclusion (e.g., "no resource regression testing in CI") rather than a point-fix ("bump memory limit").

Evidence requirements: timestamped log excerpts, alert payloads, deploy manifest diff vs. previous successful deploy, change-log of dependencies & infra in the 72h window, and the actual revert command(s) executed. The analyzer flags **missing evidence** as an action item — e.g., if pod logs were already rotated by morning, that's a *retention requirement gap*.

Output from this lens: a contributing-factor tree distinguishing **trigger** (the specific change that detonated), **latent conditions** (the gaps that allowed the trigger to detonate), and **amplifiers** (what made manual revert the only option). Each becomes a candidate action item, prioritized by likelihood of recurrence × blast radius.

### Persona 2: Security (Exposure)

The security lens reframes the question: *what did this incident expose, and what would have been worse if it had been production?* A 3am manual revert under stress is a **security-relevant event** even when no breach occurred.

Concerns: (1) **break-glass credentials** — did the on-call engineer use elevated production credentials to remediate staging, blurring privilege boundaries? (2) **audit trail integrity** — manual `kubectl` / `terraform` / `git` commands executed at 3am from a personal laptop are often **outside the audited deploy pipeline**, leaving gaps in the change ledger. (3) **secret exposure** — if logs containing secrets surfaced in the failure mode (common with verbose error handling), those logs may now sit in Slack channels, screenshots, or terminal history without rotation.

Additionally: a stressed on-call engineer is the **prime target profile for social engineering**. If a "helpful" outsider had paged in at 3am offering to "help debug," the fatigue + pressure environment lowers verification rigor. Security requirements must include incident-mode identity controls.

The security lens also asks: was the deploy artifact **signed/verified**, and was the revert artifact equally signed? Manual reverts often skip signing in favor of speed, creating a precedent where un-signed code can reach a deploy target under "emergency" framing — a documented attacker pivot.

Requirements implication: post-mortem must include a **security review subsection** even for ostensibly non-security incidents, covering credential handling, audit completeness, log sanitization, and any policy exceptions granted during mitigation.

### Persona 3: DevOps (Release Engineering)

The devops lens treats this as a **release engineering maturity** problem. Three properties of a healthy release system failed: **safety** (the bad change reached staging), **reversibility** (manual revert was needed), and **observability** (failure was detected only by an automated probe, not by progressive rollout signals).

Concrete deficiencies likely present: (a) **no progressive rollout** — the deploy was all-or-nothing rather than canary or blue/green, so the bad version replaced the good version before any health gate could intervene; (b) **no automated rollback hook** tied to post-deploy health checks; (c) **no deploy freeze window** for off-hours, or one that was bypassed; (d) **rollback artifact not pre-staged** — to revert, the engineer had to rebuild or re-tag, costing minutes under stress.

Release engineering best practice the post-mortem should evaluate: **forward-only vs. backward-compatible migrations** (was the failed deploy migration-bound, making revert dangerous?), **deploy idempotency** (can the same deploy command be re-run safely?), **deploy artifact immutability** (is the artifact reproducible from source 6 months later for forensic replay?).

Action items in this lens cluster around: introducing canary deploys (even 10%-90% split for staging), automating rollback on health-check failure with a defined hysteresis window, pre-staging the prior known-good artifact at deploy time so revert is a single command, and instituting an off-hours deploy policy (either freeze, or require explicit approval + on-call confirmation).

### Persona 4: Backend (System Behavior)

The backend lens focuses on **what the failing service was actually doing** when it broke. The same surface symptom (5xx, crash, hang) can have radically different backend root causes: schema migration race, connection-pool exhaustion, dependency timeout, serialization break, feature-flag misconfiguration, or environment-variable drift between staging-prior and staging-current.

The backend persona insists the post-mortem capture the **failure topology**: which service failed first, what downstream services were affected (cascade), what upstream services were unaffected (containment). Without this, the team will fix the symptom rather than the propagation pattern.

Specific backend hypotheses worth listing as investigation requirements:
1. **DB migration ordering** — did a code change ship before its schema migration, or vice versa, creating a window where neither old nor new code worked?
2. **Configuration drift** — did staging environment variables silently diverge from prod (e.g., DB host, feature flag), causing the change to behave differently than tested in dev/CI?
3. **Connection / resource leak** — did the new code introduce a leak that crossed a threshold only at scale?
4. **Backwards-incompatible API change** — did an internal client get out of sync with a server contract?
5. **Background job poison** — did a queued job from before the deploy hit the new code in an unhandled shape?

Backend requirements: post-mortem must produce a **failure-mode classification** that maps to existing test coverage gaps — i.e., "the failure class was X, and we have/don't have automated tests in CI that would catch X." This converts incident learning into concrete test-suite action items.

### Persona 5: Architect (Preventive Design)

The architect's lens steps back from the immediate incident and asks: *what architectural properties, if present, would have made this incident either impossible or trivially recoverable?* The answer is rarely "more careful engineers"; it's almost always **design properties** that bound the failure.

Properties to evaluate: **deploy reversibility-by-construction** (immutable infra, versioned artifacts, schema-migration patterns that are forward+backward compatible for one version), **environment parity** (staging is structurally identical to prod, not just functionally similar), **isolation boundaries** (a bad deploy in service A cannot cascade to service B without an explicit dependency), **observability-as-a-contract** (every service exposes the signals required for automated rollback decisions, not optional).

The architect also evaluates **organizational design**: a single on-call engineer with no co-pilot at 3am is an *architecture decision* (single-person on-call rotation), not just a staffing decision. Two-person on-call for high-impact systems, or "follow-the-sun" rotations, changes the failure surface.

Long-horizon recommendation: the post-mortem should produce not only action items but also **architectural fitness functions** — automated checks that fail the build if a regression to a healthier property occurs. Example: a fitness function that fails CI if any service ships a schema migration that is not backward-compatible for one release.

Architect-level requirements: post-mortem must include an "architectural debt" subsection that maps each action item to a long-term architectural property, so single incidents accumulate into directional change rather than spot fixes.

---

## Phase 3 — Validate (Cross-Domain Feasibility)

Cross-checking the five lenses against each other:

| Workstream | Analyzer | Security | DevOps | Backend | Architect | Verdict |
|---|---|---|---|---|---|---|
| Reconstruct incident timeline | Required | Required (audit) | Required | Required | Required | **Feasible, blocking** |
| Audit automated rollback gap | Required | Required (privilege) | Owner | Supports | Owner | **Feasible** |
| Improve alert + on-call ergonomics | Supports | Required | Required | Supports | Required | **Feasible** |
| Identify upstream change | Required (RCA) | Supports (audit) | Required | Required | Supports | **Feasible, blocking** |
| Treat as production near-miss | Supports | Required | Required | Supports | Required | **Feasible, mandatory framing** |
| Architectural fitness functions | Supports | Supports | Required | Supports | Owner | **Feasible but longer horizon** |

No cross-domain conflicts identified. Two tensions to flag:
- **Speed vs. signing** (security vs. devops): security wants signed revert artifacts; devops wants single-command revert. Resolution: pre-sign known-good artifacts at deploy time, so revert remains one command but uses pre-signed bits.
- **Blameless culture vs. accountability** (analyzer vs. architect): analyzer insists on no individual blame; architect wants clear action-item owners. Resolution: action items have *team* owners with named *drivers*, not blame for past behavior.

All requirements are feasible with existing tooling (CI/CD, monitoring, IaC). No exotic tech required.

---

## Phase 4 — Specify (Requirements Document)

### Functional Requirements (Post-Mortem Framework)

**FR-1. Incident Timeline Reconstruction**
- Document every event from 24h before the deploy through 1h after the manual revert.
- Include: deploy trigger, build/CI events, monitor firings, page deliveries, on-call actions (commands run), restoration confirmation.
- Source-of-truth for each event must be cited (log line, alert ID, chat timestamp).

**FR-2. Root-Cause Analysis Section**
- Use structured method (5-Whys + contributing-factor tree).
- Distinguish **trigger**, **latent conditions**, **amplifiers**.
- Reject single-cause narratives; require minimum 3 contributing factors with evidence.

**FR-3. Rollback-Gap Analysis**
- Document why manual revert was the *only* mitigation.
- Enumerate the automated rollback paths that *should have* engaged and why each did not.
- Cite the specific gap (missing tooling, missing config, missing training, technically-infeasible-given-this-failure-mode).

**FR-4. Change-Window Reconstruction**
- Enumerate every change merged to the deploy pipeline, dependencies, IaC, secrets, and feature flags in the prior 72h.
- For each, assess correlation with the failure.

**FR-5. On-Call Experience Audit**
- Capture: alert-to-page latency, page actionability score, runbook availability, escalation path used, tools/access available, total engineer-hours expended.
- Include the on-call engineer's qualitative narrative (blameless framing).

**FR-6. Security Review Subsection**
- Credential usage during mitigation (any production credentials touched).
- Audit-trail completeness (commands executed outside the audited pipeline).
- Log sanitization (any secrets surfaced in failure output).
- Policy exceptions granted during mitigation.

**FR-7. Failure-Mode Classification**
- Map the failure to a named class (e.g., "migration ordering", "config drift", "resource exhaustion", "API contract drift").
- Assess whether existing test suites cover the class; if not, log a test-coverage gap.

**FR-8. Production-Impact Assessment**
- Treat staging incident as production near-miss.
- Estimate: blast radius if same deploy had reached production, MTTR if same failure occurred in production, customer-facing impact.

**FR-9. Action Items with Owners and Dates**
- Every action item has: description, owning team, named driver, target date, success criterion.
- Categorize by horizon: hotfix (≤1 week), short-term (≤1 month), architectural (≤1 quarter).

**FR-10. Blameless Framing Throughout**
- Action items framed as system/process changes, never as "engineer should have…".
- Post-mortem reviewed by an uninvolved party for blameless tone before publication.

### Non-Functional Requirements (Prevention Program)

**NFR-1. Time-to-Mitigate (off-hours)**
- Target: ≤15 minutes from page to mitigation for a failed staging deploy, using documented one-command tooling.

**NFR-2. Rollback Automation Coverage**
- Target: ≥90% of deploys have an automated rollback path that engages on health-check failure within 5 minutes.

**NFR-3. Deploy Reversibility-by-Construction**
- All schema migrations backward-compatible for one release.
- All deploy artifacts immutable and reproducible for ≥6 months.

**NFR-4. Alert Actionability**
- Every page links to a runbook within ≤2 clicks.
- Alert payload includes failing service, failing check, last-known-good version, and one-command mitigation hint.

**NFR-5. Audit Completeness**
- 100% of mitigation commands captured in an immutable audit log, including off-pipeline manual interventions.

**NFR-6. On-Call Ergonomics**
- Off-hours pages for any team capped per-engineer-per-quarter; breach triggers a structural review.
- Two-person on-call (primary + secondary) for systems with production blast radius.

**NFR-7. Log Retention**
- Minimum 30-day retention for pod/service logs, sufficient to forensically reconstruct any incident discovered ≤30 days later.

**NFR-8. Staging-Production Parity**
- Staging environment variables, infrastructure topology, and resource limits structurally derived from prod (not hand-maintained).

### Acceptance Criteria

**AC-1.** The post-mortem document exists, follows FR-1 through FR-10, and is reviewed by an uninvolved party for blameless tone before publication.

**AC-2.** A named driver is identified for each action item, with a target date and a success criterion.

**AC-3.** The rollback-gap action items (FR-3) include at least one item that, when complete, would have allowed the original 3am incident to mitigate without manual intervention.

**AC-4.** The change-window reconstruction (FR-4) identifies the specific change(s) correlated with the failure, OR documents a process gap that prevented identification.

**AC-5.** A fire-drill exercise is scheduled within 30 days to validate the rollback path identified in FR-3 actually works end-to-end.

**AC-6.** The next deploy after the post-mortem is published runs through the new gating (whatever is added) and either deploys successfully or rolls back automatically without manual intervention.

**AC-7.** A trend-tracking metric is added to the team's monthly review: count of incidents-requiring-manual-mitigation per month, target trending downward.

### Open Questions

1. **Was this the first manual revert, or one of many?** Determines whether scope is "this incident" or "systemic gap."
2. **Was the deploy intentional at 3am, or did the pipeline drift?** Determines whether the prevention program needs deploy-window controls or pipeline-latency controls.
3. **Who owns the deploy pipeline itself** — platform team, the application team, or shared? Owner gap is a common contributing factor.
4. **Are there compliance / regulatory implications?** (E.g., SOC2 change-management requirements may be triggered by un-audited manual interventions, even on staging.)
5. **What is the team's appetite for canary / progressive rollout** vs. the simplicity of all-or-nothing deploys? This is a values question, not just a technical one.
6. **Does the on-call engineer have psychological-safety support** after a stressful 3am incident? Post-mortems often surface burnout signals that need HR-aware handling.
7. **Is there a customer-facing trust dimension?** Staging is internal, but if customers were notified of a "scheduled maintenance" that was actually this incident, the communications policy is in scope.

### Next-Step Suggestions

- **`/sc:design`** — Architect the rollback automation (FR-3) and deploy-gating system (NFR-2) once requirements are signed off.
- **`/sc:workflow`** — Generate the implementation workflow for the top 3 action items (rollback automation, canary deploys, alert-payload improvement).
- **`/sc:research`** — Investigate industry post-mortem templates (Google SRE book, Etsy "morgue", PagerDuty post-mortem guide) for additional structural requirements not covered here.
- **`/sc:brainstorm "on-call rotation health and burnout indicators" --depth normal`** — Spin off the on-call ergonomics workstream (NFR-6) as its own discovery.

---

**Protocol compliance**: This document is a REQUIREMENTS SPECIFICATION ONLY (per v1 CRITICAL BOUNDARIES). No architecture diagrams, no implementation code, no schema designs were produced. Hand off to `/sc:design` for architecture and `/sc:workflow` for implementation planning.
