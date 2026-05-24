# Refactoring Plan

## 1. Overview

- Base variant: Variant 1 (opus, default persona)
- Non-base variants: Variant 2 (sonnet, default persona)
- Total planned changes: 16
- Total rejected changes: 6
- Overall risk: Medium

The base is Variant 1 (opus-default), winner by 13.7% combined-score margin (base-selection.md §4). The plan incorporates 6 strengths from V2 (per base-selection.md §"Strengths to Incorporate"), surfaces 10 HIGH UNADDRESSED invariants from invariant-probe.md as exit criteria / risks / explicit open-question decisions, and reconciles two divergent recommendations (refresh-token cap, roles cap) by elevating them to named-owner falsifiable decisions. Overall risk is Medium because several changes (CH-007, CH-009, CH-016) restructure existing exit-criteria tables and the M0 effort estimate, rather than appending net-new content.

---

## 2. Planned Changes

### CH-001: Add R-009 conversion-rate risk

- **Title:** Adopt R-006 conversion-rate risk (renumbered R-009 in base register)
- **Source:** Variant 2 §6.R-006 "Registration conversion below 60% target" (diff-analysis U-008)
- **Target Location:** §6 Risk Register — append after R-008
- **Integration Approach:** append
- **Content to Add:** New risk row `R-009 | Registration conversion < 60% PRD target | Likelihood: Medium | Impact: High (PRD success metric #1) | Mitigation: instrument funnel events Registration_Start / Registration_Submit / Registration_Success at M1 exit; weekly conversion review post-GA | Contingency: A/B test simplification (remove displayName, add social proof messaging) | Owner: PM + auth-team lead | Trigger: 7-day rolling conversion < 60% at M5+1w review`
- **Rationale:** V2 Advocate Round 1 §3.1 (R-006 is the only risk tying roadmap to PRD success metric); V1 Advocate Round 2 §2 "More compelling than I thought" — concedes unmodified adoption; debate-transcript Round 2 §4.3 final-concession from V1 confirms strict-superset improvement. Combined-score qual rubric Risk Coverage #5 both MET, but V1 lacks product-metric coverage. Confidence: high (both advocates agreed).
- **Risk Level:** Low (additive)

### CH-002: Sub-component performance budgets (micro-benchmarks)

- **Title:** Add §8.5 Sub-Component Performance Budgets
- **Source:** Variant 2 §8.3 micro-benchmark gates (diff-analysis U-010)
- **Target Location:** §8 Quality & Testing Gates — new subsection 8.5
- **Integration Approach:** insert
- **Content to Add:** New §8.5 table with three rows: `JwtService.sign p95 < 5ms (k6 microbench, 10k iterations)`, `JwtService.verify p95 < 5ms (Jest microbench)`, `TokenManager Redis read/write/revoke p95 < 10ms (testcontainers redis 7.x)`, `PasswordHasher bcrypt-12 hash time p95 < 500ms (existing §8.4 gate, cross-referenced)`. Measurement protocol adopts V1's k6 + Jest rigor (Round 2 §2 walk-back: "adopt Sonnet's target numbers but use Opus's measurement rigor").
- **Rationale:** V2 Advocate Round 1 §3.3 (decomposes 200ms p95 NFR into auditable sub-budgets); V1 Round 2 §2 (partial walk-back — adopt targets, retain Opus measurement rigor). Confidence: high.
- **Risk Level:** Low (additive)

### CH-003: Lockout state durability on Redis flush

- **Title:** Lockout counter durability exit criterion + R-002 mitigation expansion
- **Source:** Invariant Probe INV-001 + INV-017 (HIGH UNADDRESSED, state_variables + interaction_effects)
- **Target Location:** §2.M1 exit criteria (append new criterion) + §6 R-002 Mitigation column (expand)
- **Integration Approach:** append + insert
- **Content to Add:** New §2.M1 exit criterion: `Lockout counter (failed_count + window_start_ts) persisted with Redis TTL = 16 min (1 min beyond window); on Redis-down → fail-closed reject login with 503 (NOT reset attacker budget); chaos test 'flush Redis mid-lockout' asserts surviving counter or fail-closed denial.` R-002 mitigation appended: `Lockout state recovery: Redis-down during active lockout → API returns 503 for affected users (fail-closed); no attempt-budget reset on flush.`
- **Rationale:** Invariant Probe INV-001 (HIGH) + INV-017 (HIGH, canonical "two correct individual invariants combine into a security regression"). Both variants accepted A-005 (Redis-down → universal re-login) without modeling lockout-counter side. Debate consensus blocked per invariant-probe summary line 64.
- **Risk Level:** Medium (modifies M1 exit gate and R-002)

### CH-004: Audit-log durability across deploys + crash

- **Title:** Audit-log durability as M3 exit criterion + §8 observability gate
- **Source:** Invariant Probe INV-002 (HIGH UNADDRESSED, state_variables)
- **Target Location:** §2.M3 exit criteria (append) + §8 Quality Gates §8.6 (new)
- **Integration Approach:** append + insert
- **Content to Add:** New §2.M3 exit criterion: `Audit log writes are durable BEFORE the auth response returns: synchronous write to PG audit_log table with explicit COMMIT before 2xx/4xx response; chaos test 'kill app-pod mid-auth-response' asserts audit row present.` New §8.6 row: `Audit durability — SOC2 100-event spot-check across 1 deploy + 1 rolling-restart window confirms zero missing audit events.`
- **Rationale:** Invariant Probe INV-002 (HIGH); SOC2/GDPR auditability assumed by both variants but never proven against crash window. V1 §2.M1 ex 7 "audit log emission" leaves write semantics unspecified.
- **Risk Level:** Medium (modifies M3 exit + adds §8.6)

### CH-005: Refresh-token malformed-input guard

- **Title:** FR-AUTH-003 refresh-token guard exit criterion
- **Source:** Invariant Probe INV-004 (HIGH UNADDRESSED, guard_conditions)
- **Target Location:** §2.M2 exit criteria (append)
- **Integration Approach:** append
- **Content to Add:** New §2.M2 exit criterion: `Refresh-token endpoint validates payload as non-null, well-formed JWT (header.payload.signature shape + base64url decodes) BEFORE SHA-256 hash + Redis lookup; null/empty/malformed token → 401 immediately, no Redis call. Unit test asserts SHA256(null), SHA256(""), SHA256("not-a-jwt") never reach Redis lookup path (mock asserts zero hgets).`
- **Rationale:** Invariant Probe INV-004 (HIGH): null/empty token hashed becomes deterministic key → cross-user collision risk. V1 R2 §3.3 specifies SHA-256 hash but does not gate malformed-input.
- **Risk Level:** Low (additive exit criterion)

### CH-006: Per-account DoS via lockout — new R-010 risk

- **Title:** Add R-010 per-account lockout DoS with rate-limit-per-IP mitigation
- **Source:** Invariant Probe INV-019 (HIGH) + diff-analysis A-006 (both variants REJECTED in Round 1, no mitigation landed)
- **Target Location:** §6 Risk Register — append after R-009 (from CH-001)
- **Integration Approach:** append
- **Content to Add:** New risk row `R-010 | Per-account lockout DoS — attacker scripts 5 wrong-password attempts per known email at sustained rate, locking victim ~hours/day | Likelihood: Medium | Impact: Medium (UX degradation, support load) | Mitigation: (a) IP-based rate limit on /auth/login at 30 req/min/IP (Redis token bucket), (b) CAPTCHA challenge inserted on 4th attempt instead of hard-lock-at-5, (c) email notification on lockout with self-service unlock link via verified-email reset path | Contingency: emergency IP-block runbook if coordinated attack observed in audit log | Owner: WS-4 Security | Trigger: SOC2 100-event audit shows ≥3 unique-IP-per-victim lockouts in any 7-day window`
- **Rationale:** Invariant Probe INV-019 (HIGH); A-006 diff-analysis both REJECTED; V1 R1 §6 + V2 R1 §6 both recommended CAPTCHA but neither integrated mitigation into Round 2. "Both variants agree it's broken; consensus output still ships broken" (INV-019 evidence).
- **Risk Level:** Low (additive)

### CH-007: Legacy auth rollback operational viability

- **Title:** Phase 1 pre-flight gate — legacy auth on-call ownership
- **Source:** Invariant Probe INV-020 (HIGH UNADDRESSED, sufficiency_challenge) + diff-analysis A-008
- **Target Location:** §7 Rollout & Release Gates — insert as Gate A pre-flight criterion (before Gate A entry)
- **Integration Approach:** insert
- **Content to Add:** New Gate A pre-flight row: `Legacy auth path operational ownership confirmed in writing — on-call rotation named, runbook v-current, schema-compatibility verified (legacy login can read new audit_log without errors), session-cookie format honored by new gateway during partial flip; owner: platform-team + auth-team lead; deadline: 2026-05-25 (3 days before Phase 1 entry).`
- **Rationale:** Invariant Probe INV-020 (HIGH): "rollback target without owner is non-rollback." V1 R1 §6 A-008 QUALIFY: "neither asserts legacy is operationally maintained"; V2 R1 §6 A-008 ACCEPT without operational evidence. Both Round 2s ship without owner.
- **Risk Level:** Medium (modifies §7 gate structure)

### CH-008: Feature-flag flip half-state runbook step

- **Title:** AUTH_NEW_LOGIN / AUTH_TOKEN_REFRESH half-flip runbook step
- **Source:** Invariant Probe INV-016 (HIGH UNADDRESSED, interaction_effects)
- **Target Location:** §7 Rollback Procedure — insert as step 2.5 (between current step 2 and step 3)
- **Integration Approach:** insert
- **Content to Add:** New rollback step: `2.5. Feature-flag half-state handling: in-flight requests carrying legacy session cookies during AUTH_NEW_LOGIN flip → gateway accepts both cookie formats for a 60-second drain window before flipping; AUTH_TOKEN_REFRESH flip → existing refresh tokens issued under old flag remain valid until TTL expiry (7d), no forced revocation; chaos drill 2026-06-01 (1 day before Alpha) exercises mid-request flip in staging.`
- **Rationale:** Invariant Probe INV-016 (HIGH): "half-flipped requests during rollback can produce 500s or silent authz failures." A-008 both variants REJECT/QUALIFY but Opus H-table covers handoffs, not cookie/token format transitions.
- **Risk Level:** Medium (modifies rollback runbook)

### CH-009: Reconcile divergent OQ recommendations — refresh-token cap

- **Title:** Elevate PRD-OQ-2 refresh-token cap to falsifiable decision with named owner
- **Source:** Diff-analysis C-004 / X-003 + Invariant Probe INV-010 (HIGH UNADDRESSED, collection_boundaries)
- **Target Location:** §9 Open Questions — modify PRD-OQ-2 row
- **Integration Approach:** restructure
- **Content to Add:** Reformulated row: `PRD-OQ-2 (refresh-token cap) | Decision: cap = 5 active refresh tokens per user (smaller blast radius default per V2; relaxable post-GA via config) | Eviction policy: oldest evicted on issuance of 6th (NOT block — blocking creates DoS for multi-device users per INV-010) | Owner: auth-team lead | Decision Date: 2026-04-15 | Exit criterion gate: M2 deliverable adds integration test 'issue 6 tokens → assert oldest evicted + new token valid'.`
- **Rationale:** Base-selection §"Strengths to Incorporate" #6 (V2's cap of 5 = smaller blast radius); INV-010 (HIGH): V2's "limit 5 concurrent" never specified eviction-vs-block; V1's "oldest evicted" closes the gap. Combined adoption per debate consensus.
- **Risk Level:** Medium (replaces recommendation with decision)

### CH-010: Reconcile divergent OQ recommendations — roles cap

- **Title:** Elevate TDD-OQ-002 roles cap to falsifiable decision
- **Source:** Diff-analysis C-005 / X-004 + Invariant Probe INV-005 + INV-011 (MEDIUM)
- **Target Location:** §9 Open Questions — modify TDD-OQ-002 row
- **Integration Approach:** restructure
- **Content to Add:** Reformulated row: `TDD-OQ-002 (UserProfile.roles cap) | Decision: cap = 10 roles (V2 default; generous for foreseeable RBAC v1.1; relaxable in v1.2 if RBAC PRD justifies) | Lower-bound: roles=[] explicitly rejected at registration (default ['user'] assigned); on admin role-removal that would empty array → 400 "role array cannot be empty" | Upper-bound: 11th role-add → 400 "role limit reached" (no silent eviction) | DB check constraint enforces both bounds | Owner: auth-team + future-RBAC-PM | Decision Date: 2026-04-22.`
- **Rationale:** Base-selection §"Strengths to Incorporate" #6 (V2's cap 10 = smaller blast radius); INV-005 (empty array case) + INV-011 (cap-action) both UNADDRESSED. Hybrid resolution adopts V2 cap with V1 explicit-rejection semantics.
- **Risk Level:** Medium (replaces recommendation with decision)

### CH-011: Lockout 5-fail off-by-one + window semantics

- **Title:** Lockout state-machine precision (off-by-one + sliding-vs-fixed window)
- **Source:** Invariant Probe INV-007 (HIGH) + INV-008 (MEDIUM)
- **Target Location:** §2.M1 exit criteria (modify lockout criterion) + Appendix A invariant table
- **Integration Approach:** replace
- **Content to Add:** Replace existing lockout criterion with: `Lockout state machine: failed_count incremented on each wrong-password response (NOT on lockout response); 5th wrong password → 423 Locked (the 5th attempt itself is the lockout-trigger response, not allowed); failed_count reset on successful auth OR on 15-min window expiry from FIRST failure (fixed window, not sliding — per INV-008 disambiguation); unit test 'pin index: attempt 1-4 → 401, attempt 5 → 423' + 'time-travel test: 14:59 from t0 → 401, 15:01 from t0 → counter reset.' Cooldown: per CH-012, 30-min from lockout timestamp before retry permitted.`
- **Rationale:** Invariant Probe INV-007 (HIGH): off-by-one ambiguity = security regression risk; INV-008 (MEDIUM): sliding vs fixed window unspecified affects DoS calculus.
- **Risk Level:** Medium (modifies exit criterion + Appendix A row)

### CH-012: 30-minute lockout cooldown

- **Title:** Adopt V2's 30-min cooldown (replacing V1's 15-min auto-unlock)
- **Source:** Base-selection §"Strengths to Incorporate" #3 + diff-analysis C-006 / X-005
- **Target Location:** §2.M1 exit criterion 6 + §9 PRD-OQ-3 row
- **Integration Approach:** replace
- **Content to Add:** Replace "cooldown after 15 min unlocks" → "30-min cooldown from lockout timestamp before next login attempt permitted; alternative unlock = successful password-reset flow (revoke-all + new password sets failed_count=0)." Update §9 PRD-OQ-3 from open to "Decision: 30-min cooldown OR password-reset path; Owner: WS-4 Security; Decision Date: 2026-04-07."
- **Rationale:** Base-selection §"Strengths to Incorporate" #3 (Opus R2 conceded default — doubles attacker re-attempt cost). V1 Round 2 §2 explicit concession.
- **Risk Level:** Low (numeric replacement)

### CH-013: M5 separate uptime vs latency exit criteria

- **Title:** Separate NFR-REL-001 and NFR-PERF-001 M5 exit gates
- **Source:** Base-selection §"Strengths to Incorporate" #4 + V2 R2 §3.1 evidence
- **Target Location:** §2.M5 exit criteria — restructure rows 3-4
- **Integration Approach:** restructure
- **Content to Add:** Replace bundled gate with two independently-measured rows: `(a) NFR-REL-001: 99.9% uptime over first 7 days post-GA, measured as 1 - (downtime_minutes / 10080), independently passing.` `(b) NFR-PERF-001: p95 < 200ms login + p95 < 100ms refresh over first 7 days post-GA, measured as rolling 1-hr p95 over the window, independently passing.` Add note: "neither metric can mask a regression in the other; both required for GA-100% gate."
- **Rationale:** V2 R2 §3.1 evidence: "Opus bundles them, which could allow a latency regression to hide behind a passing uptime metric"; base-selection §"Strengths to Incorporate" #4.
- **Risk Level:** Low (replaces single criterion with two)

### CH-014: Appendix B Gantt visualization adoption

- **Title:** Add Gantt timeline as Appendix B.2 (alongside existing Component matrix)
- **Source:** Base-selection §"Strengths to Incorporate" #5 + V2 §Appendix B (diff-analysis U-009)
- **Target Location:** Appendix B — append as B.2
- **Integration Approach:** append
- **Content to Add:** ASCII Gantt timeline rendering 5 workstreams × 11 weeks (W0..W10) with milestone markers M0..M5 and the WS-D week-6 gap explicitly filled by adopting SEC-4 timing checkpoint at M3 close (per V2 R2 §3.3 "demonstrates the two variants are genuinely complementary"). Existing Component → Milestone matrix retained as Appendix B.1.
- **Rationale:** Base-selection §"Strengths to Incorporate" #5 (reveals WS-D week-6 gap); V2 R2 §3.3 demonstrates the complementarity check.
- **Risk Level:** Low (additive appendix subsection)

### CH-015: Beta-duration debate documented as rejected alternative (with rationale)

- **Title:** Document V2's 1-week Beta argument as rejected alternative in §7
- **Source:** Diff-analysis C-009 + V1 R2 §3.1 + V2 R2 §4.2 concession
- **Target Location:** §7 Rollout & Release Gates — add footnote/sidebar to Phase 2 Beta row
- **Integration Approach:** append
- **Content to Add:** Sidebar note: `Alternative considered: 1-week Beta (V2-sonnet variant §7.2). Rejected because: (a) TDD §19.1 Phase 2 explicitly specifies "Beta — 2 weeks at 10%" — fidelity defect (V2 R2 §4.2 conceded); (b) NFR-REL-001 99.9% target requires ≥1000 events at 95% statistical confidence — 1 week of 10% production may not reach sample size depending on baseline traffic (V1 R2 §2 evidence). 2-week Beta retained.`
- **Rationale:** V1 R2 §3.1 (TDD evidence); V2 R2 §4.2 ("a fidelity defect I cannot refute"). Preserves debate evidence for downstream readers.
- **Risk Level:** Low (additive footnote)

### CH-016: M0 effort reduction with deliverable accountability preserved

- **Title:** Reduce M0 effort 8 EW → 6 EW; relabel platform-team deliverables
- **Source:** V1 R2 §4.2 ("M0 effort can drop from 8 EW to 6 EW") + V2 R2 §2 ("M0 over-counts platform-team work")
- **Target Location:** §1 capacity (48 EW → 46 EW) + §2.M0 effort field
- **Integration Approach:** restructure
- **Content to Add:** §2.M0 effort: 6 EW (was 8 EW). PG provisioning (D1) and Redis provisioning (D2) relabeled as "platform-team standard work, auth-team observer only — 0 EW charge"; remaining 6 deliverables (RSA, SendGrid, OpenAPI, flags, decisions, threat model) at 6 EW. §1 total: 46 EW (was 48 EW). Preserve M0 as a formal gate per V2 R2 §3 ("the gate is valuable; the 6-8 EW estimate for achieving it is not" — gate retained, estimate reduced).
- **Rationale:** V1 R2 final concession #2 (R2 §4.2). Both variants converged on a partial reduction; preserves V1's gate value while honoring V2's double-counting critique.
- **Risk Level:** Medium (modifies headline effort total + M0 row)

---

## 3. Changes NOT Being Made (Rejected Alternatives)

### REJECT-A: V2's 16 EW total

- **Concerns:** Diff-analysis C-001, X-002, X-008
- **Rationale:** V1 Advocate Round 2 §1 demonstrated 16 EW does not consume the team V2's own §3 staffs (5.5 FTE × 9 weeks = ~49 EW). V2 Round 2 §2 acknowledged "the capacity-plan reading is equally valid and more intuitive for most readers." X-008 confirms 2.5× understatement at M1 with same scope. V2's marginal-cost framing has merit but produces an effort total that conflicts with the staffing plan in the same document — a self-contradiction that fails IC scoring (V2 IC = 0.78 vs V1 = 0.96, base-selection §1). Base 46 EW (post-CH-016) retained.

### REJECT-B: V2's 4-workstream taxonomy (merged Security+Release)

- **Concerns:** Diff-analysis S-004
- **Rationale:** V1 Advocate Round 1 §3.3 — the 5-workstream split (WS-1..WS-5) provides explicit cross-cut accountability via H1-H10 handoff matrix; merging Security with Release in V2's WS-D loses the SEC-4 timing checkpoint visibility at M3 close (revealed by V2's own Gantt, per V2 R2 §3.3). V2 Round 2 §1 conceded "handoff matrix value scales with team size; at Sonnet's staffing level, useful but not critical" — but the merged output targets the full 5.5+ FTE team where the matrix IS critical. Base 5-workstream taxonomy retained.

### REJECT-C: V2's lower coverage targets (80% across all milestones)

- **Concerns:** Diff-analysis C-003
- **Rationale:** V1 Round 2 §1 — "for authentication code specifically, where untested branches map directly to security-incident likelihood, 5pp of headroom on three critical-path components is cheap insurance." V2 Round 2 §2 walk-back ("85% headroom rationale is hypothetical for this roadmap's structure") is plausible but does not outweigh the security-criticality argument. Base 85% (M1/M2/M3) + 80% (M4/M5 + project-wide) retained.

### REJECT-D: V2's component build-order omission

- **Concerns:** Diff-analysis U-003 + V1 R2 §4.1 concession
- **Rationale:** V1 conceded the table should be "advisory not prescriptive" (R2 §4.1) — but advisory ≠ omitted. V2's complete omission removes a Medium-value coordination artifact. Compromise: retain the table with V1's R2 framing "recommended sequence to minimize integration churn; parallel via interfaces acceptable once M0 contracts lock." Full omission rejected.

### REJECT-E: V2's omission of inter-workstream handoff matrix

- **Concerns:** Diff-analysis U-002 + V2 R2 §1 concession
- **Rationale:** H1-H10 in base provides coordination contract; V2 conceded "the handoff matrix should be adopted in a merged output" (R2 final concession #3). Removing it creates the exact coordination ambiguity V2's prose-only handoffs produce. Base H1-H10 table retained without modification.

### REJECT-F: V2's project-start-date 2026-04-07

- **Concerns:** Diff-analysis X-001 + S-002
- **Rationale:** V1's 2026-03-30 start accommodates the M0 foundation phase that V2 lacks. Per CH-016, M0 is preserved (with reduced effort). Without an M0 phase, V2's 04-07 start has M1 backend devs working against not-yet-provisioned infrastructure — V2 R2 §3 conceded "real risk that day-1 backend devs have no database." Base start date 2026-03-30 retained.

---

## 4. Risk Summary

| Change ID | Risk Level | Impact | Rollback |
|-----------|------------|--------|----------|
| CH-001 | Low | Additive — new R-009 row in §6 | Delete row |
| CH-002 | Low | Additive — new §8.5 subsection | Delete subsection |
| CH-003 | Medium | Modifies M1 exit gate + R-002 mitigation | Revert exit criterion + R-002 text |
| CH-004 | Medium | Modifies M3 exit + adds §8.6 | Revert exit + delete §8.6 |
| CH-005 | Low | Additive M2 exit criterion | Delete criterion |
| CH-006 | Low | Additive — new R-010 row | Delete row |
| CH-007 | Medium | Modifies §7 Gate A structure | Revert Gate A pre-flight row |
| CH-008 | Medium | Modifies rollback runbook | Remove step 2.5 |
| CH-009 | Medium | Replaces PRD-OQ-2 recommendation with decision | Revert to recommendation form |
| CH-010 | Medium | Replaces TDD-OQ-002 recommendation with decision | Revert to recommendation form |
| CH-011 | Medium | Modifies M1 lockout exit + Appendix A | Revert criterion + Appendix row |
| CH-012 | Low | Numeric replacement (15 → 30 min) | Revert numeric |
| CH-013 | Low | Splits bundled M5 criterion into two | Re-bundle |
| CH-014 | Low | Additive Appendix B.2 | Delete subsection |
| CH-015 | Low | Additive §7 footnote | Delete footnote |
| CH-016 | Medium | Modifies §1 total (48→46 EW) + §2.M0 effort | Revert effort + total |

Aggregate: 7 Medium + 9 Low. Overall risk: Medium (driven by exit-criteria modifications and headline-effort change; no High-risk restructuring).

---

## 5. Review Status

- Approval: auto-approved (non-interactive mode)
- Timestamp: 2026-05-22T00:00Z
- Reviewer: debate-orchestrator (per protocol default)
