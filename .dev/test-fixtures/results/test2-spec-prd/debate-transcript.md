---
convergence_score: 0.72
rounds_completed: 2
---

# Adversarial Debate: Opus (Variant A) vs Haiku (Variant B)

## Divergence Points Under Debate

Five key divergences from the diff analysis warrant structured debate:

1. **D1/D2**: Phase structure and timeline (4 phases/14 weeks vs 2 phases/6 weeks)
2. **D3**: Audit log provisioning timing
3. **D4**: Security review checkpoint placement
4. **D7**: Password policy enforcement location
5. **D11**: Account lockout handling

---

## Round 1: Initial Positions

### D1/D2 — Phase Structure & Timeline

**Variant A (Opus):**
Four phases across 14 weeks provides essential go/no-go gates between Foundation, Core Auth, Session/Recovery, and Compliance. Each gate is a stakeholder checkpoint where scope can be adjusted, risks reassessed, and quality validated before committing to the next phase. The 14-week timeline reflects realistic single-threaded delivery with sprint overlap — not padding. Security-critical systems should not be rushed. The compliance phase (Phase 4) being isolated ensures audit logging, performance validation, and security review receive dedicated focus rather than being squeezed into the tail of a feature sprint.

**Variant B (Haiku):**
Two phases across 6 weeks reflects parallel FTE allocation (~2.8 FTE) and eliminates unnecessary coordination overhead. Four go/no-go gates for a medium-complexity service is bureaucratic — the mid-stream security review at Week 3 provides sufficient validation before expanding scope. The 6-week timeline is achievable because: (1) Backend Lead and Support work in parallel after core services are ready, (2) QA begins test planning in Week 1, (3) DevOps provisions infrastructure concurrently. The 14-week estimate either assumes serial execution or inflates buffer. For a Q2 2026 compliance deadline, 14 weeks may not even be available.

---

### D3 — Audit Log Provisioning Timing

**Variant A (Opus):**
Deferring audit logging to Phase 4 keeps early phases focused on functional correctness. Audit logging is an instrumentation concern that should wrap completed, stable handlers — not incomplete ones. Wiring audit events into Phase 1-2 handlers that are still being actively modified creates churn. The Phase 4 "retrofit" is straightforward: each handler emits a structured event through a dispatcher. The schema and dispatcher can be defined early; the wiring happens once handlers are stable.

**Variant B (Haiku):**
Pre-provisioning the `audit_logs` table in Phase 1 Week 1 and wiring event dispatch incrementally is architecturally superior. The "retrofit problem" Opus acknowledges in its own Phase 4 integration points table ("retroactive wiring into Phase 2–3 handlers") is a real risk: handlers written without audit awareness may not capture the right context (IP address, outcome, user_id at the correct scope). Incremental wiring means each handler is tested with audit logging from the start. If SOC2 compliance is a hard deadline, discovering audit gaps in Week 12 of a 14-week plan is unacceptable.

---

### D4 — Security Review Checkpoint Placement

**Variant A (Opus):**
A single, comprehensive security review in Phase 4.3 allows the security engineer to evaluate the complete system holistically — token lifecycle, password handling, rate limiting, and input validation all in context. Fragmenting security review across multiple checkpoints risks incomplete coverage where interactions between components are missed. The Phase 4 review also includes penetration testing, which requires a complete system. Security engineers are scarce; concentrating their time is more efficient.

**Variant B (Haiku):**
A mid-stream security review at Phase 1 Week 3 (Milestone 1.5.2) catches fundamental flaws in password hashing, JWT signing, and secrets management before those primitives are consumed by every subsequent feature. Discovering that bcrypt cost factor configuration is wrong, or that the JWT implementation is vulnerable to algorithm confusion, in Week 12 forces rework of everything built on those foundations. The pre-production pen test still happens — the mid-stream review is additive, not a replacement. At 0.3 FTE, the security engineer's time is already budgeted for Phase 1 involvement.

---

### D7 — Password Policy Enforcement Location

**Variant A (Opus):**
Enforcing password policy at the registration endpoint keeps concerns separated. PasswordHasher's responsibility is hashing — it should not know about business rules like "1 uppercase required." Policy may differ across contexts (registration vs password reset vs admin-set password). Endpoint-level enforcement allows context-specific rules and clearer error messages (the endpoint knows the user-facing context). This follows the Single Responsibility Principle.

**Variant B (Haiku):**
Enforcing password policy inside PasswordHasher at hash time is defense-in-depth. If any caller bypasses the endpoint layer (direct service call, test harness, future API), the policy is still enforced. The question "will password policy ever be checked without hashing?" has the answer "no" — every password validation leads to a hash. Coupling validation to hashing means it is impossible to store a weak password. The slight coupling is worth the guarantee.

---

### D11 — Account Lockout Handling

**Variant A (Opus):**
Progressive lockout (5 failures → 15min, 10 → 1hr, 20 → admin unlock) provides account-level protection against credential stuffing that IP-level rate limiting cannot catch. Attackers using distributed IPs bypass per-IP limits trivially. Without account lockout, an attacker with a botnet can attempt unlimited passwords against a specific account. The implementation is straightforward: a failure counter on the user record with a lockout timestamp. This should be in v1.0 given the security profile of the service.

**Variant B (Haiku):**
Deferring account-level lockout to v1.1 is pragmatic scope management for v1.0. IP-level rate limiting (5/min/IP) provides baseline protection. Account lockout introduces UX complexity (legitimate users locked out, customer support burden, DoS vector where attackers intentionally lock out target accounts). For v1.0 with limited user base, IP-level limiting is sufficient. The lockout mechanism can be designed properly in v1.1 with user feedback from v1.0 informing the policy.

---

## Round 2: Rebuttals

### D1/D2 — Phase Structure & Timeline

**Variant A rebutting B:**
The 2.8 FTE assumption is optimistic for a greenfield security service. Haiku's parallel execution assumes no blocking dependencies between Backend Lead and Support, but the critical path (TokenManager → AuthService → Endpoints) is inherently serial. The Support engineer cannot write endpoints until AuthService interfaces are stable. The 6-week estimate also compresses security review, compliance validation, load testing, and penetration testing into a single week (Week 6) — any slip cascades into a missed deadline. Four phases provide slack absorption points that two phases lack.

**Variant B rebutting A:**
Opus's 14-week timeline does account for sprint overlap (Sprints 1-2 overlap, 3-5 overlap), which already implies parallel execution — yet still arrives at 14 weeks. This suggests either inflated task estimates or insufficient parallelization. The critical path concern is valid but overstated: DI interfaces can be defined in Week 1 (Milestone 1.1.3), allowing Support to write endpoint stubs against interfaces while Lead implements services. The real question is team capacity — if only 1 FTE is available, 14 weeks may be right; if 2.8 FTE is available, 6 weeks is achievable. This is a staffing input, not an architectural disagreement.

**Convergence:** Both sides agree the timeline depends on team capacity. The true estimate is likely 8-10 weeks with ~2 FTE, acknowledging serial critical path constraints but allowing parallel endpoint and test work.

---

### D3 — Audit Log Provisioning Timing

**Variant A rebutting B:**
Pre-provisioning the table is fine — the disagreement is about when to wire event dispatch. Wiring audit events into handlers during active development creates noise: every handler change requires updating the corresponding audit test. If the audit event schema changes (which it will, given Open Question #5 is unresolved), all wired handlers must be updated. Better to define the schema, provision the table, and wire once handlers are stable.

**Variant B rebutting A:**
The "noise" argument assumes audit logging is an afterthought rather than a first-class concern. If handlers are designed with audit-awareness from the start (emitting events through a dispatcher interface), the wiring is trivial and stable even as handlers evolve. Opus's own roadmap acknowledges this creates "retroactive wiring" — a term that implicitly concedes the approach is suboptimal. The Open Question #5 risk is mitigated by provisioning the table with the PRD's specified fields (user_id, event_type, timestamp, IP, outcome), which both variants agree on.

**Convergence:** Both agree the table should be provisioned early. The remaining dispute is narrow: wire incrementally (Haiku) vs wire once at the end (Opus). Given that both variants specify the same audit fields and SOC2 is a hard deadline, incremental wiring is the lower-risk approach. **Haiku wins this point.**

---

### D4 — Security Review Checkpoint Placement

**Variant A rebutting B:**
The mid-stream review adds a Phase 2 blocker — if the security engineer finds issues, Phase 2 is delayed while fixes are applied. A holistic end-stage review avoids this pipeline stall. The specific risks Haiku cites (algorithm confusion, cost factor misconfiguration) are caught by unit tests, not security reviews. The security review's value is in system-level analysis: can the complete authentication flow be exploited? That requires the complete system.

**Variant B rebutting A:**
Unit tests catch what you test for — they don't catch what you don't know to test. Algorithm confusion attacks are a known JWT vulnerability class that a security engineer would specifically probe for, but a developer might not think to test. A mid-stream review is cheaper than end-stage rework: fixing a flawed PasswordHasher in Week 3 affects 1 service; fixing it in Week 12 affects every handler built on it. The Phase 2 delay risk is real but manageable — at 0.3 FTE, the review is 1-2 days, not weeks.

**Convergence:** Both agree a pre-production security review is essential. The dispute is whether an additional earlier checkpoint is worth the coordination cost. Given the security-critical nature of the service, an early review of foundational primitives (hashing, signing, key management) is high-value and low-cost. **Haiku's approach is stronger, but both agree on the pre-production review.**

---

### D7 — Password Policy Enforcement Location

**Variant A rebutting B:**
"Every password validation leads to a hash" is not strictly true — password policy can be validated for user feedback (inline form validation) without hashing. The frontend needs to check policy before submission. If PasswordHasher owns policy, the frontend must duplicate it or call the backend for validation. Endpoint-level policy keeps the validation near the user interaction layer. Defense-in-depth is valuable, but not at the cost of responsibility confusion.

**Variant B rebutting A:**
Frontend validation is always duplicated regardless — it's a UX optimization, not a security boundary. The backend must enforce policy independently of the frontend. Whether it enforces at the endpoint layer or the hash layer, the frontend still has its own copy. The question is: on the backend, where is the last line of defense? Inside PasswordHasher, the policy cannot be bypassed by any code path. At the endpoint, a future internal service call could bypass it. Defense-in-depth is the correct principle for a security-critical component.

**Convergence:** This is a genuine design trade-off with no clear winner. Both approaches are defensible. A pragmatic resolution: validate at the endpoint for user-facing error messages, and add a guard assertion inside PasswordHasher as a backstop. This gives both contextual error handling and defense-in-depth. **Draw — merge both approaches.**

---

### D11 — Account Lockout Handling

**Variant A rebutting B:**
The "DoS via intentional lockout" concern is mitigated by progressive lockout with timed auto-unlock (15min, 1hr) rather than permanent lock. Only the 20-failure threshold requires admin intervention, which is appropriate for what would clearly be an attack. IP-level rate limiting alone is ineffective against distributed attacks — this is well-documented in OWASP guidelines. Deferring account protection to v1.1 leaves a known security gap in a v1.0 that has compliance requirements.

**Variant B rebutting A:**
Progressive lockout with auto-unlock is reasonable but adds implementation scope: failure counter storage, lockout state checks on every login, timer-based unlock logic, admin unlock interface (or at minimum, a database query). For v1.0 with a limited user base and a compliance deadline, the attack surface is low. The security gap is real but bounded — IP-rate limiting catches naive attacks, and monitoring (which both variants include) catches sophisticated ones. Implementing lockout properly in v1.1 with real usage data is better than rushing it into v1.0.

**Convergence:** Both acknowledge the security gap. The resolution depends on timeline pressure: if 6 weeks, defer; if 14 weeks, include. A middle ground: implement the failure counter and lockout state in v1.0 schema (zero additional endpoint scope), but defer the unlock flow and admin interface to v1.1. This captures the data needed for v1.1 without adding v1.0 scope.

---

## Convergence Assessment

### Areas of Agreement (Strong Convergence)

1. **Core architecture**: Both variants agree on the technology stack, component decomposition, token strategy, and DI pattern. No debate needed.
2. **Risk inventory**: Identical risks with matching assessments. Complete alignment.
3. **Success criteria**: Same 8 metrics with same targets. Complete alignment.
4. **Audit log table should be provisioned early**: Even Opus agrees the schema is foundational — the dispute is only about wiring timing.
5. **Logout should be in v1.0 scope**: Both recommend it; Haiku is more decisive by assigning it a milestone.
6. **GDPR consent is a v1.0 hard requirement**: Both flag this as needing immediate resolution and recommend inclusion.
7. **Pre-production security review + pen test**: Both include this as a launch gate.

### Areas of Partial Convergence

| Divergence | Resolution Direction | Confidence |
|---|---|---|
| Timeline (D2) | 8-10 weeks with ~2 FTE; depends on staffing input | Medium |
| Phase structure (D1) | 3 phases (compromise): Foundation → Core+Session → Compliance+Launch | Medium |
| Audit wiring (D3) | Incremental wiring (Haiku's approach) with early schema lock | High |
| Security review (D4) | Two checkpoints: mid-stream for primitives + pre-production for system | High |
| Password policy (D7) | Both layers: endpoint for UX errors, PasswordHasher guard for safety | High |
| Account lockout (D11) | Schema-only in v1.0; full implementation in v1.1 | Medium |

### Remaining Disputes (Low Convergence)

1. **Exact timeline**: Cannot be resolved without knowing team capacity. Opus assumes ~1 FTE throughput; Haiku assumes ~2.8 FTE. The debate correctly identifies this as a staffing input, not an architectural disagreement.

2. **FTE estimation granularity (D9)**: Opus argues role categories are sufficient; Haiku argues specific FTE numbers are needed for planning. Both are right for different audiences — Haiku's granularity is better for project managers, Opus's flexibility is better for variable team sizes. Not reconcilable without knowing the audience.

3. **Email dispatch sync/async (D12)**: Minor. Opus's pragmatic fallback (sync acceptable for v1.0) vs Haiku's architectural purity (async only). Both are reasonable; resolve based on whether a message queue is already available in the infrastructure.

### Synthesis Recommendation

A merged roadmap should adopt:
- **Haiku's** audit provisioning, security review cadence, DI container milestone, dedicated password reset table, logout milestone, FTE allocations, and post-launch timeline
- **Opus's** open questions analysis table, scope guardrails section, feature flag strategy, and risk commentary on replay detection atomicity
- **Compromise** on 3-phase structure (~8-10 weeks), password policy enforcement at both layers, and schema-only account lockout in v1.0
