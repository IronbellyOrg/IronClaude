---
convergence_score: 0.62
rounds_completed: 2
---

# Adversarial Debate: Opus Roadmap vs Haiku Roadmap

## Round 1: Initial Positions

### Divergence Point D-01: Timeline (10 weeks vs 20 weeks)

**Variant A (Opus):**
10–11 weeks is achievable with disciplined parallelism and experienced engineers. The authentication service is MEDIUM complexity (0.55) — not a greenfield distributed system. The core components (PasswordHasher, UserRepo, AuthService, JwtService, TokenManager) are well-understood patterns with mature libraries. Doubling the timeline to 20 weeks invites scope creep, stakeholder fatigue, and delays the $2.4M revenue unlock from personalization features. The SOC2 Type II audit deadline is Q3 2026 — a 20-week timeline starting now lands GA in mid-August, leaving zero buffer. A 10-week timeline lands GA in early June with months of margin.

**Variant B (Haiku):**
10 weeks is unrealistic without specifying team size. Our roadmap explicitly plans for ~11 FTE and still requires 20 weeks. The 10-week estimate doesn't account for: Phase 0 infrastructure lead time (provisioning delays are real), security policy finalization (SEC-POLICY-001 requires cross-team sign-off), penetration testing turnaround (2+ weeks from external firms), and the reality that integration bugs always surface during hardening. An aggressive timeline that slips is worse than a conservative one that delivers — missed deadlines erode stakeholder trust and create pressure to skip security review. The SOC2 deadline argument actually favors us: better to plan 20 weeks honestly than promise 10 and deliver in 16 with compliance shortcuts.

---

### Divergence Point D-03: Compliance Timing (Early vs Late)

**Variant A (Opus):**
Building GDPR consent and audit logging into Phase 2 alongside registration is architecturally cleaner and cheaper. Adding `consent_timestamp` to the `UserProfile` schema at creation time costs nothing extra. Retrofitting it later requires a schema migration, backfill of existing test data, and regression testing of the registration flow — all avoidable rework. The same applies to audit logging: if you instrument `AuthService` from the start, every subsequent endpoint automatically benefits. Deferring compliance to Phase 3 means Phase 1-2 code ships without audit trails, creating a blind spot during development and making it harder to debug issues retroactively.

**Variant B (Haiku):**
Deferring compliance to a dedicated Phase 3 is a deliberate architectural choice, not negligence. Grouping GDPR consent, audit logging, and admin query APIs into one focused phase enables: (1) a single compliance review gate rather than piecemeal checks, (2) dedicated engineering focus without context-switching between feature development and compliance plumbing, (3) explicit Phase 3→4 gate that proves compliance readiness to auditors. The "retrofit cost" argument is overstated — adding a nullable `consent_timestamp` column is a trivial migration. What matters is that Phase 3 has an explicit exit criterion: compliance is validated before hardening begins. Opus's approach risks half-baked compliance that passes unit tests but fails audit scrutiny.

---

### Divergence Point D-04: Frontend Timing (Parallel vs Sequential)

**Variant A (Opus):**
Frontend work should wait until Phase 4, after the backend API contract is stable. Starting frontend in Phase 1 against an incomplete backend means: (1) frontend builds against stub APIs that will change, (2) token management isn't implemented yet so `AuthProvider` is a placeholder, (3) any backend API change cascades into frontend rework. The frontend team can work on other projects during Phases 1-3. When they start in Phase 4, they build against a stable, tested API — no rework, no coordination overhead, no wasted effort.

**Variant B (Haiku):**
Building `LoginPage` and `RegisterPage` in Phase 1 enables E2E validation from the start. Real users (QA, product) can test actual flows, not Postman collections. The frontend team would otherwise be idle for 8+ weeks — that's a massive resource waste for a team of 2 FTE. The "API might change" risk is manageable: login and registration are the most stable endpoints (email + password in, token out). Token management changes in Phase 2 only affect `AuthProvider`, not the page components themselves. Early frontend work also surfaces UX issues (form validation, error handling, loading states) that pure backend testing misses.

---

### Divergence Point D-05: Admin Audit Log Query API

**Variant A (Opus):**
The admin audit log query API is not in the TDD v1.0 scope. Including it adds ~18h of implementation plus admin authorization middleware. The Jordan (admin) persona is acknowledged, but v1.0 should focus on the core authentication flows that unblock personalization revenue. Admins can query PostgreSQL directly or use existing log aggregation tools (ELK/Datadog) in the interim. Adding admin APIs increases the attack surface and testing burden. Defer to post-GA when the actual admin usage patterns are known.

**Variant B (Haiku):**
The PRD defines Jordan as a key persona. If SOC2 Type II audit requires demonstrable admin access to auth logs by Q3 2026, building it post-GA creates a compliance gap. The admin query API is straightforward (paginated SELECT with authorization middleware) and leverages the `auth_events` table we're already building. The ~18h cost is minimal compared to the risk of failing an audit because admins can't query logs through the application. Direct PostgreSQL access is not an acceptable compliance control — auditors want to see application-level access with proper authorization.

---

### Divergence Point D-07/D-08: Team Sizing and Task Granularity

**Variant A (Opus):**
Omitting headcount is intentional — team sizing is an organizational decision, not a roadmap artifact. The roadmap defines *what* and *when*; resourcing defines *who* and *how many*. Coupling these creates brittleness: if the team changes size, the entire roadmap timeline needs rewriting. Similarly, hour-level task estimates create a false sense of precision — they'll be wrong within the first sprint and become maintenance overhead. The roadmap should be a strategic guide, not a project plan. Sprint planning happens in Jira/Linear with the actual team, not in a roadmap document.

**Variant B (Haiku):**
A roadmap without resourcing is a wish list, not a plan. Our explicit headcount (~11 FTE) directly justifies the 20-week timeline and makes capacity constraints visible. Without this, Opus's 10-week timeline is unverifiable — is it 10 weeks with 20 engineers or 10 weeks with 5? Hour estimates per task enable: (1) sprint planning without a separate decomposition pass, (2) identification of bottlenecks before they hit (e.g., the security engineer is only 0.5 FTE), (3) realistic capacity allocation across teams. Yes, estimates will drift, but having them and adjusting is better than not having them and discovering in Week 4 that you're 3x over capacity.

---

### Divergence Point D-12: Approval Gates

**Variant A (Opus):**
Lightweight exit criteria per phase are sufficient. Formal approval gates with named approvers add governance overhead that slows delivery. For a MEDIUM-complexity project, the overhead of scheduling gate reviews, getting sign-offs, and documenting approvals is disproportionate. The team should be empowered to move between phases based on objective criteria (tests passing, coverage met, NFRs validated), not waiting for a meeting. SOC2 audit evidence can come from CI/CD logs, test reports, and commit history — not from approval meeting minutes.

**Variant B (Haiku):**
For a SOC2-bound project, formal approval gates are not optional overhead — they're audit evidence. SOC2 Type II requires demonstrable change management controls. Named approvers at each phase boundary create: (1) accountability — someone specific signs off that security review passed, (2) audit trail — auditors can verify who approved what and when, (3) risk checkpoints — prevents "we'll fix it later" from propagating past phase boundaries. The Phase 3→4 gate explicitly requires compliance readiness sign-off — without this, hardening could begin with incomplete audit logging. The cost of a 30-minute gate review is trivial compared to a failed SOC2 audit.

---

### Divergence Point D-13: Rollback Trigger Specificity

**Variant A (Opus):**
Our rollback triggers are operationally precise: p95 > 1000ms for 5 minutes, error rate > 5% for 2 minutes, Redis failures > 10/min, any data corruption. An on-call engineer at 3 AM can make an instant rollback decision without judgment calls or escalation. "Metrics within normal ranges" (Haiku's language) requires the engineer to know what "normal" means — which varies by time of day, day of week, and deployment stage. Specific thresholds are automatable: you can wire Prometheus alerts directly to rollback triggers.

**Variant B (Haiku):**
We concede this point partially — Opus's rollback thresholds are more operationally precise. However, our approach describes rollback *capability* and *procedure* more thoroughly, including step-by-step runbook testing and team drills. Precise thresholds without tested procedures are still dangerous. Our Phase 4 includes explicit runbook drills where the team executes each rollback scenario. The thresholds themselves should be tuned during beta based on observed baselines, not set a priori in the roadmap.

---

## Round 2: Rebuttals

### Variant A (Opus) Rebuts Variant B:

**On timeline (D-01):** Haiku claims 20 weeks is "honest" but includes significant padding. Phase 0 (2 weeks for infrastructure) is over-engineered — PostgreSQL and Redis provisioning takes days, not weeks, on any modern cloud platform. Phase 4 (4 weeks for hardening) is also inflated — penetration testing can run in parallel with other hardening tasks. The 20-week timeline assumes serial execution of tasks that can be parallelized. If Haiku's ~11 FTE team worked with Opus's parallelism strategy, 14-15 weeks would be realistic — splitting the difference.

**On compliance timing (D-03):** Haiku's "dedicated compliance phase" argument falls apart under scrutiny. You can't retrofit `consent_timestamp` as a "trivial migration" AND argue it needs a dedicated phase. If it's trivial, do it in Phase 2. If it needs dedicated focus, it's not trivial. The real risk is that Phases 1-2 generate test user data *without* consent timestamps, creating a data quality problem that complicates compliance validation. Building it in from the start eliminates this entirely.

**On frontend timing (D-04):** "The frontend team would be idle" is a resourcing argument, not an architectural one. If the frontend team is idle, they should work on other projects or help with backend testing. Building frontend against incomplete APIs creates coupling that slows both teams. The `AuthProvider` in Phase 1 is necessarily a stub — real token management doesn't exist yet. This is the definition of throwaway work.

**On admin API (D-05):** "Auditors want application-level access" is speculative. SOC2 Type II audits evaluate controls, not specific UI/API implementations. Log aggregation tools with proper access controls (Datadog with RBAC, for example) satisfy audit requirements. Building a custom admin API before understanding actual admin workflows is premature optimization.

**On approval gates (D-12):** SOC2 does NOT require approval gates at every phase boundary. It requires change management controls. A well-configured CI/CD pipeline with branch protection, code review requirements, and deployment approvals satisfies this — GitHub's audit log IS the approval trail. Adding manual approval meetings is governance theater that satisfies auditors at the cost of engineering velocity.

---

### Variant B (Haiku) Rebuts Variant A:

**On timeline (D-01):** Opus's "parallelism" argument has a hidden assumption: experienced engineers who can context-switch between security-sensitive components without introducing bugs. In practice, parallelizing PasswordHasher, UserRepo, AuthService, and JwtService across different engineers creates integration risk at the seams. Our serial-within-phase, parallel-across-teams approach is more realistic. Furthermore, Opus provides no team sizing — "10 weeks" could mean 10 weeks with 3 engineers (impossible) or 10 weeks with 20 engineers (wasteful). Without resourcing, the timeline claim is unfalsifiable.

**On compliance timing (D-03):** The "data quality problem" argument is a red herring. Test environments are reset between phases. No production user data exists during Phases 1-2. The consent timestamp migration is trivial *technically* but significant *organizationally* — it requires product sign-off on consent wording, legal review of the checkbox text, and UX review of the registration flow changes. Grouping these decisions into Phase 3 ensures they get dedicated attention rather than being rushed as Phase 2 afterthoughts.

**On frontend timing (D-04):** "Work on other projects" is not realistic team management — context-switching between projects is expensive and most organizations don't have idle frontend work conveniently queued. The `AuthProvider` stub argument is overstated: `LoginPage` and `RegisterPage` call POST endpoints with JSON bodies and display responses. This is stable API surface. The `AuthProvider` token management (Phase 2) is a separate concern from the page components. Building pages early validates UX, accessibility, and form validation — none of which require token management.

**On admin API (D-05):** "Speculative" is incorrect — the PRD explicitly defines the Jordan persona with admin audit needs. "Use Datadog" is a non-answer for a roadmap: it creates an external dependency not in the infrastructure requirements, requires separate access provisioning and RBAC configuration, and means the auth service doesn't self-serve its own compliance needs. The 18h cost is a rounding error on a 20-week project. Building it ensures the auth service is compliance-complete at GA, not compliance-complete-except-for-the-admin-part.

**On approval gates (D-12):** "Governance theater" is dismissive of real compliance needs. Yes, CI/CD provides change management evidence. But SOC2 also evaluates *risk assessment* and *management review* — which require human judgment, not automated pipelines. A security lead signing off that penetration testing passed is not theater; it's accountability. Our gates are lightweight (30-minute reviews with defined criteria), not bureaucratic. Opus's "exit criteria without gates" means criteria can be silently unmet — who checks? Gates create the forcing function.

---

## Convergence Assessment

### Areas of Agreement (Strong Convergence)

1. **Core architecture is settled.** Both variants agree completely on JWT/RS256, bcrypt cost 12, Redis refresh tokens, feature flags, three-phase rollout, and scope guardrails. No debate needed on technical fundamentals.

2. **Rollback precision favors Opus.** Haiku partially conceded D-13 — specific numeric rollback thresholds are operationally superior. The merged recommendation should adopt Opus's thresholds and Haiku's runbook drill process.

3. **Compliance must be in v1.0.** Both agree GDPR and SOC2 requirements are non-negotiable for GA. The debate is *when* in the timeline, not *whether*.

4. **Decision-forward defaults are preferable.** Both acknowledge that unresolved open questions create risk. Opus's approach of implementing conservative defaults (12-month retention, async email) while tracking resolution is less risky than leaving decisions open.

### Areas of Partial Convergence

5. **Timeline should be 14-16 weeks**, not 10 or 20. Opus's 10 weeks lacks resourcing justification; Haiku's 20 weeks includes excessive padding. A merged roadmap should: adopt Haiku's Phase 0 (but compress to 1 week), keep Opus's compressed Phase 2-3, and use Haiku's dedicated Phase 4 hardening (but 2 weeks, not 4). Target: ~15 weeks with ~8-10 FTE.

6. **Frontend timing is context-dependent.** If the frontend team exists and would be idle, Haiku's approach is pragmatic. If frontend engineers are shared resources, Opus's sequential approach avoids wasted effort. The merged roadmap should start `LoginPage`/`RegisterPage` in Phase 2 (not Phase 1 or Phase 4) — after the API contract is defined but before token management is complete.

7. **Approval gates should be lightweight but present.** Not at every phase boundary (Haiku's overhead), but at 3 critical junctures: (1) Pre-development (infrastructure + policy ready), (2) Pre-hardening (features complete + compliance validated), (3) Pre-GA (security review passed). This satisfies SOC2 without blocking velocity.

### Remaining Disputes (Low Convergence)

8. **Admin audit API scope (D-05):** Genuinely unresolvable without product input. If SOC2 audit requires application-level admin log access, it's v1.0. If log aggregation tools suffice, it's v1.1. This is a product/compliance decision, not an engineering one. **Recommendation: escalate to product owner with a deadline of Week 0.**

9. **Task-level granularity (D-08):** Philosophical disagreement. Opus favors strategic roadmaps with separate sprint planning; Haiku favors immediately-actionable plans. Both are valid depending on team maturity and PM tooling. **Recommendation: the merged roadmap should include Haiku's team sizing and phase-level effort estimates, but defer hour-level task breakdown to sprint planning.**

10. **Compliance timing (D-03):** Both sides made strong arguments. Early integration avoids retrofit; dedicated phases ensure focus. **Recommendation: add the `consent_timestamp` field to the schema in Phase 1 (zero-cost schema decision per Opus), but defer the full compliance validation (audit logging infrastructure, consent UX, admin APIs) to a focused phase per Haiku's grouping approach.** This hybrid captures the best of both.
