# Round 2 Rebuttal — Advocate for Variant 1 (Opus Default)

**Author:** V1 Advocate
**Round:** 2 (Rebuttal)
**Date:** 2026-05-22

---

## Response to Criticisms

V2's Round 1 raised six specific weaknesses against V1. I take each in turn, restate them faithfully with citations, and respond with counter-evidence or concession.

### Criticism 1 — "Token-first sequencing delays user-visible value by two sprints"

**V2's claim** (round-1-advocate-v2.md §Weaknesses-in-V1 #1): "V1 M2 (Token Lifecycle) delivers only library code... No user can register or log in until M3 (Sprints 5-7). V2 ships registration and login in M2 (Sprints 3-4)... For a service that 'unblocks Q2-Q3 2026 personalization features (projected $2.4M ARR contribution)' (V1 Executive Summary, line 16), two extra sprints of invisible library work is a significant delay to time-to-value."

**Response: Mostly wrong, but with a sliver of truth.**

The "two sprints earlier value" framing equivocates on what "value" means. Three problems:

1. **V2's M2 endpoints are not GA-able value.** V2's own M2 Scope-Out (variant-2-sonnet-default.md line 156): login returns "session identifier placeholder; M3 adds JWT". A login endpoint that returns a placeholder token nobody can verify, refresh, or revoke is not value to any of the PRD personas — not Maya (returning user), not Sam (API consumer), not Jordan (admin). It is an unfinished endpoint behind a feature flag.

2. **The GA cut date is identical.** Both variants target the end of Sprint 12 for GA. V2 has not moved the date the personalization team can rely on — it has moved the date of a demo of an unfinished surface. V1's Executive Summary (variant-1-opus-default.md line 16) commits to the same Q2 2026 GA. The $2.4M ARR unblock happens on the same calendar week in both plans.

3. **V2's "earlier value" assumes the retrofit cost is bounded.** V2 concedes this in its own Round 1 Concessions #1 ("M2 exit criteria validate endpoints that will be modified in M3, requiring re-testing"). The retrofit isn't just a 2-day code change — it invalidates the integration tests, contract tests, audit-event shapes, and frontend assumptions written in M2. V2's defense ("D3.5/D3.6... 2 days of work, V2 M3 Effort") accounts only for code, not for the test-suite churn.

**Sliver of truth I concede:** For stakeholder *demos* (PM, exec sponsor, design reviewer), V2's M2 produces a clickable end-to-end flow earlier. That has real political value in a 6-month project where stakeholders get nervous around Sprint 4. V1 should explicitly produce a Sprint-4 demo artifact (e.g., a Postman collection driving the token library through staged scenarios) to neutralize this gap.

### Criticism 2 — "V1's 6.5 FTE fixed team size is unrealistic for most organizations"

**V2's claim** (round-1-advocate-v2.md §Weaknesses-in-V1 #2): "V1 Section 2 requires '4 backend engineers, 2 frontend engineers, 0.5 SRE, 0.5 security reviewer' for the full 12 sprints. This assumes zero attrition... Most growth-stage teams cannot afford."

**Response: Partial concession, but V2's "3-5 engineers" is a planning anti-pattern.**

I concede that V1's team specification reads as a hard requirement. V2 reads as more flexible. But "3-5 engineers" is a range that hides the most important question: *which 3-5*? A team of 3 backends and 2 frontends is wildly different from a team of 5 backends and 0 frontends. V2 cannot land its own M5 (Frontend Integration) deliverable without frontend headcount it never names, and its Roadmap Overview (variant-2-sonnet-default.md line 28) admits this with "plus frontend-team for M4" — but that frontend-team is uncounted in the 3-5.

V1's number is more honest precisely because it is specific. The mitigation V1 should add: rephrase the team line as "capacity equivalent to 4 BE × 12 sprints, 2 FE × 4 sprints, 0.5 SRE + 0.5 sec for the duration, with the FE allocation falling primarily in M3 and M6". That preserves the FTE budget honesty while acknowledging the team can be smaller if scope is correspondingly cut.

**Concession recorded:** V1's team section should be reworded to "capacity-equivalent" rather than "engineers-allocated".

### Criticism 3 — "V1 omits GDPR right-to-erasure"

**V2's claim** (round-1-advocate-v2.md §Weaknesses-in-V1 #3): "V1's GDPR mapping (Section 9.1, line 503) covers consent capture and data minimization but has no deletion endpoint. GDPR Article 17 is not optional."

**Response: V2 is correct. Full concession.**

This was already conceded in my Round 1 Concessions #1, and V2 correctly amplifies it. `DELETE /auth/me` (or an equivalent admin-side erasure flow) is a GDPR Article 17 obligation, not optional. V1 must absorb V2 D6.3 (or move erasure earlier into M4 alongside the reset flow, where most of the same revoke-all-sessions plumbing is already present). Any merged variant must include this.

I will further upgrade the concession: erasure should probably ship in M4 (not M6 as V2 has it), because (a) the technical work (nullify PII, revoke sessions) is the exact same primitive as password reset, and (b) deferring erasure until M6 means V2 itself is non-compliant during the M5 beta-10% production exposure period. V1 should adopt erasure but at M4, which is *stronger than V2's own placement*.

### Criticism 4 — "V1's dedicated M5 creates a compliance bolt-on risk despite claiming to avoid it"

**V2's claim** (round-1-advocate-v2.md §Weaknesses-in-V1 #4): "V1 defers all audit-log persistence to M5 — M3 and M4 emit events 'to a stub sink'. This means M3 and M4 run in production (behind feature flags) with no durable audit trail until M5 completes. If M5 slips, the system operates for an extended period without compliant audit logging."

**Response: Misreads V1's timeline. M5 finishes before any production exposure.**

This is V2's sharpest-feeling critique, and it is structurally wrong. Read V1's milestone schedule carefully (variant-1-opus-default.md §M5 line 316, §M6 line 378):

- M5 = Sprint 10 + half of Sprint 11
- M6 = second half of Sprint 11 + Sprint 12
- Staged rollout (1% → 10% → 50% → 100%) begins inside M6, after M5 exits

So M5 completes *before* any user traffic hits the system. V2's "M3 and M4 run in production with no durable audit trail" never happens in V1 — M3 and M4 run only in *staging* until M5 lights up the audit table, dashboards, and alerts. The first production packet is in M6, after M5 exit criteria have been verified.

Now, V2 might counter: "what if M5 slips?" Two answers:

1. V1's M5 exit is a *hard gate* on M6 entry (§4 Cross-Milestone Dependency Table line 400: "M5 → M6 Hard"). If M5 slips, GA slips. The bolt-on risk is *contained inside the schedule*.

2. V1's M3 emits events to a stub sink *with the same envelope schema* the durable table accepts (§11 Sequencing Rationale line 543: "Audit-event emission is wired into M3 endpoints from day one... M5 lights up the durable audit table"). When M5 wires the durable store, no producer code changes. Compare to V2's approach where M2 writes directly to `audit_log` synchronously (variant-2-sonnet-default.md M2 D2.4) — this looks like "compliance from sprint 3" but the outbox pattern V1 commits to in D5.2 is what auditors actually want, because synchronous writes can lose events under partial failure (the audit-completeness scenario CC7.2 targets).

**V2's critique would land if V1 cut M5 entirely or moved it after M6.** V1 does neither.

### Criticism 5 — "V1's KMS dependency on M2 creates a blocking external dependency"

**V2's claim** (round-1-advocate-v2.md §Weaknesses-in-V1 #5): "If the KMS provisioning slips — which is common in organizations where KMS requires security-team approval — M2 is entirely blocked with no fallback. V2 uses Kubernetes secret mounts (V2 M3 D3.7), which require no external approval."

**Response: True risk, but V2's framing inverts the audit reality.**

I accept that KMS provisioning is a Hard external dependency with a non-zero probability of slipping. V1's R-DEP-1 already documents this as Low probability / Critical impact, and V1 §8 Assumption 3 escalates KMS access to a P1 dependency block if not confirmed by end of M1. That is the correct posture, not a hidden risk.

However, V2's claimed alternative — "Kubernetes secret mounts require no external approval" — is wrong in any organization with a working access-control posture. K8s secrets at the namespace level are readable by anyone with `kubectl get secret -n auth` permission, which in practice includes platform-team, SREs, and often the on-call rotation. SOC2 CC6.1 (logical access controls) auditors will ask "who can read the JWT signing key?" and "K8s secret in the auth namespace" is a list of 10–50 humans. KMS is a list of two service principals with a CloudTrail audit log.

V2's "no external approval" benefit is a developer-velocity benefit, not a security benefit. For a SOC2 Type II audit, the velocity benefit and the audit cost run in opposite directions. V1 is correct to pay the velocity cost.

**What I concede:** V1 should add a fallback path — "if KMS provisioning slips past M1 sprint 2, fall back to a Vault-namespace-backed signing key with the same overlapping-`kid` rotation discipline, and migrate to KMS post-GA". This preserves the audit posture (Vault is also HSM-backed) while removing the single-vendor blocking dependency.

### Criticism 6 — "V1's edge-case catalog is descriptive but not testable at the invariant level"

**V2's claim** (round-1-advocate-v2.md §Weaknesses-in-V1 #6): "V1 Section 13 catalogs 30+ edge cases... However, the catalog does not declare severity — is a violated edge case a P1, P2, or P3? V2's Appendix B invariants are all declared P1 by construction."

**Response: Correct critique, partial concession. The two formats are complementary, not substitutes.**

V2's invariant table is genuinely a stronger artifact for QA hand-off than V1's prose catalog. INV-01..INV-10 give the QA-lead an unambiguous P1-classified checklist. V1 should adopt the invariant-table format on top of its scenario catalog.

But V2 also overstates the substitution. The invariant table tells you *what* must hold; the scenario catalog tells you *how it can fail*. Example: V2's INV-02 ("Each refresh token is used exactly once") tells the QA engineer to write a test that asserts second-use returns 401. V1's §13.1 row 1 tells them *the specific concurrent-tabs failure path* that produced this requirement, *the N=8 parallel-request test design*, and *the owner milestone*. The catalog is a richer authoring guide; the invariant table is a tighter pass/fail gate. The merged variant should have both.

**Concession recorded:** V1 should add an invariant table indexed to the §13 catalog rows, with each catalog row mapped to a numbered INV-* and declared P1.

---

## Updated Assessment of V2

After V2's Round 1, my confidence in the relative positions has shifted on three axes.

### V2's strongest arguments (where I have moved closer)

1. **GDPR erasure (U-010) is a non-negotiable gap in V1.** V2's positioning is decisive on this. I am moving from "V1 should add a deletion endpoint" (Round 1 concession) to "V1's omission is a *correctness failure*, not a feature-omission". Any merged variant must include erasure, and arguably should do so earlier than V2 places it (M4, not M6, for the reasons in my Criticism-3 response).

2. **State-mechanics invariants (U-009) are a superior format for the P1-gate layer.** V2's INV-01..10 binds severity to the property, which V1's prose does not. I am moving from "complementary formats" (Round 1) to "V2's format is structurally better for the QA-handoff slice, and V1's catalog should be re-presented to feed into an invariant table". V2 wins this format debate.

3. **Open-questions resolution log (U-011) is a better artifact than V1's scattered §8 assumptions.** V2 Appendix A tracks PRD OQ1-OQ4 and TDD OQ1-OQ2 with status, owner, resolution. V1 mentions some in §13 and §8 but never closes them. This is a documentation-quality gap V1 should close by adopting V2's table format.

### V2's weakest arguments

1. **"Compliance bolt-on risk in V1's M5" (Criticism 4 above) is a misread of V1's schedule.** M5 finishes before production exposure begins. V2's critique would land against a strawman V1 that ships M3/M4 to production with stub-sink audit logging — which V1 explicitly does not do.

2. **"Two sprints earlier value" framing (Criticism 1 above) confuses demo cadence with delivery cadence.** V2's M2 ships placeholder endpoints that get rewritten in M3. The GA date is identical. The argument should be reframed as "earlier stakeholder demos" (which V1 can match with a Sprint-4 demo artifact) not "earlier value to users".

3. **"Auth-first validates the use case before building tokens" (V2 Round 1 §Focused Defense #1) is the weakest defense of the build order.** V2 says "tokens have no meaning without a use case", but the PRD AUTH-PRD-001 and TDD AUTH-001 *are* the use case — they precisely specify access-token lifetime (15 min), refresh-token lifetime (7 days), rotation semantics, revocation surface, and clock-skew tolerance. The use case is fully specified in the inputs. V1's token library is informed by that spec, not invented in a vacuum. The "premature abstraction" risk V2 invokes assumes the spec is vague, but the spec here is unusually concrete.

4. **`allkeys-lru` defense ignores cross-keyspace contamination** (my Round 1 §Weaknesses-in-V2 #2). V2's Round 1 defense addresses refresh-token eviction but never addresses lockout-counter eviction. A locked-out attacker whose counter is evicted gets 5 fresh attempts. V2's Sequencing Rationale and risk register do not address this. The `allkeys-lru` policy needs to be narrowed to a token-only sub-keyspace or rejected for the lockout/rate-limit keyspaces.

5. **"Filesystem path key management is upgradeable post-GA" (V2 Round 1 §Focused Defense #3) misjudges audit timing.** SOC2 Type II is *Q3 2026*, immediately after GA. Saying "we'll upgrade to KMS post-GA" means the *first audit window* runs against the filesystem-secret posture. Auditors will write a finding. Either V2 ships KMS by GA (matching V1) or V2 accepts a SOC2 finding it could have avoided. Post-GA upgrade does not help.

### Points where I have moved closer to V2's position

- **GDPR erasure must be in scope.** Full move.
- **Invariant table format is superior to prose catalog for QA gates.** Full move.
- **Open-questions resolution log should be a first-class section.** Full move.
- **Infrastructure cost estimate should appear in the roadmap.** Full move (already conceded Round 1).
- **Team-sizing language should be "capacity-equivalent" not "engineers-allocated"** to honor V2's headcount-flexibility critique.
- **V1 should add a Sprint-4 demo artifact** to neutralize V2's "earlier stakeholder validation" advantage.

### Points where I have *not* moved

- **Build order:** token-library-first remains correct for a SOC2-bound service with a fully-specified token spec.
- **Redis eviction policy:** `noeviction` on the auth keyspace remains correct because the keyspace mixes refresh tokens with lockout counters and revocation lists, and V2 never addresses the contamination problem.
- **Reset-token persistence:** Postgres remains correct because reset-email-in-flight loss is a worse user experience than V2 frames (the user clicks a "Reset password" link from email and sees "Invalid token" with no actionable recovery path).
- **Key management:** KMS/HSM remains correct given the Q3 2026 SOC2 timeline. V2's "upgrade post-GA" path concedes a finding.
- **GA before pen-test:** V1's order remains correct. Pen-testing after GA is a category error for an authentication service.
- **OpenAPI spec + contracts package:** still correct for a service with a frontend consumer and an SDK consumer (Sam-the-API-consumer per PRD); V2's defense ("integration tests catch drift") catches it post-merge, not pre-merge.

---

## New Evidence

Five points not surfaced in Round 1.

### NE-1 — V2's INV-08 is inconsistent with V2's M2 D2.4 audit-write semantics

V2 Appendix B INV-08 (variant-2-sonnet-default.md line 852): "All auth events produce an audit log row with required fields... Audit writer called in every auth flow path (success and failure)... Integration test for each event type." But V2 M2 D2.4 writes audit events synchronously in the request flow with no transactional guarantee. If the auth-row INSERT commits and the audit INSERT subsequently fails (constraint violation, connection drop after the first INSERT), INV-08 is silently violated — the auth event occurred, the audit row did not. V2 has no detection mechanism. The integration test ("Integration test for each event type") only proves the *happy path*; it does not prove the invariant under partial failure.

V1's outbox pattern (D5.2) makes INV-08 *structurally* impossible to violate: the audit-event row is INSERTed in the *same* DB transaction as the state change, and an async publisher drains to the durable store. State change without audit row is impossible because they share the transaction boundary.

This is a case where V2's invariant table is *better than V2's implementation can support*. V2 should adopt V1's outbox pattern; otherwise INV-08 is a wish, not a guarantee.

### NE-2 — V2's INV-05 contradicts V2's `allkeys-lru` policy

V2 INV-05 (line 849): "Account lockout is atomic: 5th failed attempt triggers lock even under concurrent requests... Integration test: 5 concurrent failed logins result in exactly 1 lock." V2 enforces this via a Postgres atomic UPDATE — good. But the *lockout state itself* (the locked-until window, the failed-attempt counter window) lives in Redis in V2's M2 (variant-2-sonnet-default.md M2 D2.3: "5 failed attempts within 15 minutes locks for 30 minutes"). Under `allkeys-lru` (V2 M3 D3.2 Risks), this state can evict. INV-05 then holds only for *non-evicted* counters. Under any memory pressure, an attacker can hold open enough connections to push the lockout counter out of LRU and resume brute-forcing.

V2 has not connected its invariant to its eviction policy. V1's `noeviction` makes the invariant uniformly hold; V2's policy makes it conditional.

### NE-3 — V1's `@auth/contracts` package directly de-risks V2's biggest unstated risk

V2 Round 1 §Focused Defense #4 argues code-first is fine because "the PRD already specifies request/response shapes for every endpoint". But the PRD specifies shapes in *prose tables*, not in machine-validated JSON schemas. V2 has no automated mechanism to detect a frontend (M5) that reads `userProfile.display_name` while the backend (M2-M4) returns `userProfile.displayName`. Integration tests catch this *if and only if* the integration test asserts the specific field name — which is exactly the kind of bug that slips through tests that "look like they pass".

V1's `@auth/contracts` package (D1.3) makes this a *compile-time* type error in both backend and frontend. V2 catches it as a runtime test failure in M5 (Sprint 10) at the earliest, and possibly as a production bug if the integration tests assert behavior loosely. The cost of `@auth/contracts` (V2 estimates 2-3 days) is exactly the cost V1 pays to make this whole class of integration bugs uncompilable.

### NE-4 — V2's "earlier GA in M5" framing breaks under its own pen-test schedule

V2 M5 D5.7 ships "GA 100%" at the end of M5 (Sprint 11). V2 M6 D6.1 (pen test) runs in Sprint 12. So under V2's plan, 100% of users hit the auth service in the *week before* the pen test starts. If the pen test finds a Critical (V2 M6 Risks acknowledges this is Low/Critical), V2's "extend sprint by 1 week" mitigation runs against a *production* footprint, not a staging one. V2 cannot withdraw production exposure once it has been granted.

V1's order (pen test inside M6, then staged rollout 1% → 100% over 7 days) keeps users *staged behind the pen-test finding window*. If V1's pen test finds a Critical at the 1% stage, the blast radius is 1% of users. V2's blast radius at the same finding is 100% of users.

V2's M5/M6 ordering converts a Low-probability/Critical-impact risk into Low-probability/Catastrophic-impact. V1's ordering keeps it at Low/Critical. This is the single largest structural argument against V2 and it deserves more weight in the final judgment than my Round 1 gave it.

### NE-5 — The "single GA cut" framing reveals V1's posture is more aggressive on rollout safety than V2

It is worth surfacing what looks like a paradox: V1's plan *feels* heavier (KMS, OpenAPI, outbox, threat model) and yet V1's *rollout* is more conservative (1% → 10% → 50% → 100% over 7 days, with auto-rollback on SLO violation per D6.5). V2's rollout (alpha 0% → beta 10% → GA 100%, total ~4 weeks) sounds slower in wall-clock, but the gating is coarser (only three steps, no 50% intermediate, no auto-rollback infrastructure called out in V2's deliverable list).

The pattern: V1 spends earlier-sprint effort on isolation, contracts, and threat modeling so that the *rollout* can be gated mechanically with auto-rollback. V2 saves earlier-sprint effort but must *make a human decision* at each rollout gate. For an authentication service where the failure modes are silent and security-relevant, mechanical gating is the safer posture.

---

## Updated Concessions

Beyond my Round 1 concessions (GDPR erasure, infrastructure cost, premature-abstraction risk, invariant-table format, open-questions log), Round 2 surfaces three more I owe.

### UC-1 — V1's M2 needs a Sprint-4 demo artifact to neutralize the "no user-visible value" critique

V2 Criticism 1 has a real political point even if its delivery framing is wrong. V1's Sprint 4 ends with a library-only deliverable. The mitigation is to add to V1 M2's exit criteria a "Sprint-4 stakeholder demo: scripted Postman/Insomnia collection driving `JwtService.sign`, `TokenManager.refreshPair`, `revokeAllForUser`, and a key-rotation drill through the library's API, with a recorded walkthrough delivered to PM, exec sponsor, and design reviewer." This costs ~1 day, neutralizes V2's "invisible work" framing, and turns the crypto-isolation choice into a demonstrable engineering milestone.

### UC-2 — V1's M2 KMS dependency needs a documented fallback

V2 Criticism 5 is partly right that "M2 entirely blocked" is a real concern. V1's R-DEP-1 lists Low probability / Critical impact but does not document a Plan B. I owe: V1 should add to ADR-002 ("KMS vs Vault") a documented fallback chain: "If AWS KMS provisioning slips past M1 end, fall back to HashiCorp Vault transit-engine signing. If both slip, fall back to a Vault-namespace-stored RSA key with overlapping-`kid` rotation discipline, and migrate to KMS-managed signing post-GA." This preserves the audit posture (Vault is HSM-backed) and removes the single-vendor blocking dependency. V2's critique was correct that V1 had no Plan B for this scenario.

### UC-3 — V1's team-allocation should be reframed as capacity-equivalent

V2 Criticism 2 has a genuine point. V1's "4 BE, 2 FE, 0.5 SRE, 0.5 sec" reads as a rigid allocation in a way that V2's "3-5 engineers" does not. V1 should rephrase as: "capacity equivalent to ~80 BE-engineer-sprints, ~12 FE-engineer-sprints (concentrated in M3 and M6), and ~12 SRE+security-reviewer-sprints across the program, with FE allocation falling primarily during the frontend-coupled milestones." That is honest about the *amount* of work without lying about the *shape* of headcount.

---

## Closing Posture

V1 and V2 are both coherent plans for the same problem. The debate is not "good plan vs bad plan" — it is "which set of trade-offs better fits a SOC2-Type-II-bound authentication service shipping to Q2 2026 GA with a Q3 audit window."

After Round 1 and these rebuttals, I believe:

- **V1's structural decisions** (token-library isolation, `noeviction` auth keyspace, Postgres reset tokens, KMS-backed signing, OpenAPI + contracts package, outbox audit, frontend coupling, hardening-before-rollout) are the correct posture for a SOC2-bound auth service.
- **V2's content additions** (GDPR erasure, invariant table, open-questions log, infrastructure cost, admin REST API) are content V1 should adopt — they are not architectural reversals, they are missing rows.
- **V2's structural decisions** (auth-first build order, separated frontend, `allkeys-lru`, Redis reset tokens, K8s-secret signing keys, code-first, GA-before-pen-test) optimize for a problem profile V2 is implicitly assuming — a startup-velocity green-field service without a hard compliance deadline. That problem profile is not this problem.

A merged variant should be V1's spine with V2's missing rows grafted on, plus V1's three new Round 2 concessions (Sprint-4 demo artifact, documented KMS fallback, capacity-equivalent team language). V2's structural reversals (build order, eviction policy, reset-token medium, key management, GA-before-pen) should not survive the merge.

Wrote round-2-rebuttal-v1.md.
