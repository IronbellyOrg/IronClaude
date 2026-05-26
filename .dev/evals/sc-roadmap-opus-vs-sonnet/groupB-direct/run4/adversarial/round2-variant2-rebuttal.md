# Round 2 — Variant 2 (Sonnet) Rebuttal

## 1. Response to Criticisms

**"16 EW is implausibly low — Sonnet's own staffing implies ~49 EW" (X-002, Opus R2 §1).**

*Re-framing.* Opus's arithmetic (5.5 FTE x 9 weeks = 49.5 EW) conflates capacity with effort. The 16 EW figure is not "total team capacity consumed" — it is the estimated **effort directly chargeable to auth-roadmap deliverables**. WS-C's platform engineer provisions PostgreSQL and Redis, but that is part of their existing platform backlog, not incremental auth work. Similarly, WS-D's security reviewer conducts checkpoints as part of their security-review rotation. Opus counts every hour from every named role as roadmap effort; Sonnet counts only hours that would not exist without this roadmap. The 16 EW figure is the marginal cost, not the gross cost. Both framings are valid; Opus's 48 EW is a capacity plan, Sonnet's 16 EW is a marginal-cost estimate. A merged output should present both.

**"M1 at 4 EW is a 2.5x understatement" (X-008, Opus R1 §4.2, R2 §1).**

*Counter-evidence.* Opus counts 10 M1 deliverables and 8 exit criteria as evidence that 4 EW is insufficient. But several deliverables are trivially small: `PasswordHasher` wrapping bcryptjs (established library) is a 2-hour task, not a multi-day one. The lockout state machine is a counter + timestamp check — standard patterns. The enumeration parity test is a response-shape assertion, not the statistical timing framework Opus builds. The p95 load test at 100 RPS is a single k6 script. The **remaining** scope — AuthService orchestrator, UserRepo, two endpoints, password policy, audit emission — is approximately 4 deliverables of genuine complexity. At 4 EW (160 engineer-hours), that is 40 hours per complex deliverable, which is a reasonable sprint velocity. Opus's 10 EW allocates 100 hours per complex deliverable, which is conservative but not 2.5x more precise.

**"Missing M0 creates dependency risk" (S-001, Opus R1 §3.1).**

*Partial concession + re-framing.* Concede: a formal gate for infrastructure readiness before M1 coding is valuable. Sonnet's WS-C W1-W2 sequencing runs infrastructure provisioning in parallel with M1, creating a real risk that day-1 backend devs have no database. However, re-frame: Sonnet's approach is how most 2-pizza teams actually operate — infra and feature work start together, with a "soft gate" (WS-C handoff at W2: "PostgreSQL and Redis available in staging and CI"). The formal M0 gate Opus proposes adds 2 calendar weeks and 8 EW (or 6 EW per Opus's R2 concession). For a 9-week build, those 2 weeks represent 22% of the total schedule. The right merge is a **lightweight readiness check** at W1 end — not a full milestone — confirming PG + Redis + RSA keys are available, without burning 6-8 EW on a formal M0 deliverable set.

**"80% coverage is the floor; Opus's 85% leaves headroom" (C-003, Opus R2 §1).**

*Counter-evidence.* Opus's own §8.1 M5 row states the project-wide gate is ">= 80% project-wide." If M1/M2/M3 ship at 85%, and subsequent milestones add code that is tested to 80%, the project-wide average will be above 80% without the headroom argument. More importantly, the "headroom" rationale only works if coverage drifts downward — but Sonnet's milestones each test their own code to 80%, so there is no drift mechanism. The headroom argument is valid only if later milestones write code against M1/M2/M3 APIs without adding tests, which neither roadmap plans. Opus's 85% is prudent but not necessary at the TDD's stated 80% gate.

**"No quantitative timing-variance enforcement" (C-008, Opus R1 §3.4).**

*Concession.* This is the strongest critique in the debate. Sonnet states "no enumeration via timing differences" (Appendix A) without a measurable threshold, making the criterion subjective and un-enforceable in CI. Opus's +/-15ms (login) and +/-10ms (reset) parity-test budgets are genuinely superior. Concede fully: a merged output should adopt Opus's quantitative timing-variance ATs verbatim.

**"Less rigorous open-Q escalation protocol" (Opus R1 §3.6).**

*Concession.* Sonnet has decision deadlines but no escalation trigger. Opus's "any open question still Open within 4 calendar days of its Decision Date -> escalated to engineering lead" is a simple, effective mechanism. Concede and adopt.

**"No inter-workstream handoff matrix" (Opus R1 §3.3).**

*Concession with nuance.* Opus's H1-H10 table is genuinely valuable for multi-team coordination. Sonnet's prose handoffs are adequate for a 4-person team but insufficient at 6+ FTE. Concede: the handoff matrix should be adopted in a merged output. However, note that Opus's table includes H8 ("Frontend bundle from WS-3 to WS-5 at M4 end") — a handoff between the frontend team and the SRE team. In Sonnet's 4-workstream model, this coordination happens organically because WS-C (platform/SRE) is already involved in WS-B (frontend) integration. The handoff matrix's value scales with team size; at Sonnet's staffing level, it is useful but not critical.

## 2. Updated Assessment of Variant 1

**More compelling than I thought:**

- **Opus's defense of 48 EW (R2 §1)** using Sonnet's own staffing numbers is a stronger argument than I credited. The arithmetic is sound: 5.5 FTE x 9 weeks does imply ~49 EW of capacity. My Round 1 defense ("2 engineers for 2 weeks is natural sprint cadence") only addressed backend and ignored the other named roles. This is a genuine gap in my Round 1 argument. The marginal-cost framing (above) is my revised position, but I acknowledge the capacity-plan reading is equally valid and more intuitive for most readers.

- **Beta duration contradicting TDD §19.1 (Opus R2 §3.1)** is a fidelity defect I cannot refute. If the TDD specifies "Beta — 2 weeks at 10%," Sonnet's 1-week Beta (§7.2) is non-compliant. Opus's 2-week Beta is correct. This is the single strongest new point in Opus's Round 2.

- **Refresh token hash algorithm specificity (Opus R2 §3.3).** Sonnet says "hashed refresh token in Redis" without naming SHA-256. Opus names the algorithm explicitly (§2.M2 deliverable 3). This is a genuine precision gap — an implementer could choose a weaker hash. Concede.

**Less compelling than initially conceded:**

- **M0 as a full milestone.** Opus's R2 partial concession (dropping from 8 EW to 6 EW) validates my core argument: M0 over-counts platform-team work. But Opus still insists on 6 EW for the remaining 6 deliverables (RSA keys, SendGrid, OpenAPI, flags, decisions, threat model). Of these, "feature-flag scaffolding" is typically a 2-hour configuration task (two boolean flags), and "decision records for 6 open questions" is a PM/lead activity that happens in meetings, not engineering sprints. A realistic M0 is closer to 3-4 EW, not 6.

- **85% coverage "headroom" (Opus R2 §1).** Opus's defense that "coverage is a lagging indicator that drifts downward" is true in general but assumes later milestones add untested code to existing modules. Both roadmaps scope later milestones (M3 reset, M4 frontend, M5 rollout) as additive new code with its own 80% tests, not modifications to M1/M2 core. The drift scenario is hypothetical for this roadmap's structure.

- **Opus's component build-order concession (R2 §4.1).** Opus conceded that the 7-step ordering should be advisory, not prescriptive. This validates my Round 1 criticism and weakens Opus's claim that §5 is a "strength." The build-order table is useful reference material but not a roadmap differentiator.

**M0 vs TDD §18 duplication:**

Opus's R2 argument — "TDD §18 is a dependency list, not an execution plan" — is partially valid. Listing PostgreSQL as a dependency does not provision it. But the counter is also true: provisioning PostgreSQL is a platform-team task ticket, not an auth-team milestone. M0's value is not the deliverables themselves but the **gate** that confirms they exist before M1 starts. The gate is valuable; the 6-8 EW estimate for achieving it is not. A merged output should have a readiness gate at W1/W2 boundary without a dedicated milestone.

## 3. New Evidence Not Presented in Round 1

1. **TDD §23.2 Phase 3 exit criteria** specifies "99.9% uptime over first 7 days" as a post-GA gate. Both variants adopt this. However, Opus's M5 exit criterion 3 states "99.9% uptime over first 7 days post-GA" (§2.M5 exit 3) while also requiring "p95 < 200ms" in the same window. Sonnet's M5 exit criteria (§2.M5) separate the uptime gate from the latency gate, making it clearer that these are independently measured. Opus bundles them, which could allow a latency regression to hide behind a passing uptime metric if the gate is evaluated as a single boolean. Sonnet's separation is the more auditable structure.

2. **Industry sizing benchmark.** A comparable authentication service (email/password login, JWT tokens, password reset, Redis session store, PostgreSQL user store, bcrypt cost 12) at a mid-stage SaaS company typically estimates 3-5 engineer-months for v1.0. Sonnet's 16 EW = 4 engineer-months sits at the median of this range. Opus's 48 EW = 12 engineer-months is at the high end, more typical of a team building from scratch with no prior auth experience and significant compliance overhead (SOC2 Type II audit from day one). For a team with prior bcrypt/JWT experience — which the TDD's detailed component specifications imply — 4 engineer-months is a defensible estimate.

3. **Sonnet's Appendix B Gantt visualization (U-009) enables a critical-path integrity check.** By rendering all four workstreams against a weekly timeline, it is immediately visible that WS-D (Security) has a gap in W6 (no security activity between Checkpoint 2 at W5 and pen test at W7). This gap means no security review of the password-reset implementation before the pen test. In a merged output, this gap would be filled by adopting Opus's SEC-4 timing checkpoint at M3 close — demonstrating that the two variants are genuinely complementary rather than contradictory.

## 4. Final Concessions

1. **Timing-variance ATs should be adopted from Opus verbatim.** The +/-15ms (login) and +/-10ms (reset) parity-test budgets with statistical method are the right CI gate. Sonnet's qualitative "no enumeration" language is insufficient. This is the single most important adoption from Opus.

2. **Beta duration must be 2 weeks per TDD §19.1.** My Round 1 defense of a 1-week Beta was incorrect given the TDD's explicit Phase 2 duration. A merged output must match the TDD spec.

3. **The handoff matrix H1-H10 adds real coordination value** even at Sonnet's smaller team size, particularly H6 (TokenManager.revokeAllForUser from WS-2 to WS-1) which Sonnet's prose handoffs do not surface.

4. **Refresh token hash should specify SHA-256 explicitly** to match TDD §13 and eliminate implementer ambiguity.

5. **Open-Q escalation protocol (4-day trigger)** is a lightweight, effective mechanism that Sonnet should adopt.

6. **Sonnet's R-006 conversion-risk remains the strongest product-oriented risk** in either variant and should be included in any merged output. Opus has adopted this in their R2 concession, confirming cross-variant agreement.

---
