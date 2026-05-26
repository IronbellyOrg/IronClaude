# Adversarial Debate Transcript: User Authentication Roadmap

## Metadata

- Depth: standard
- Rounds completed: Round 1 + Round 2 + Round 2.5 (invariant probe)
- Round 3: Skipped (depth=standard does not include Round 3)
- Advocate count: 2 (opus, sonnet — both model-only specs, default persona)
- Convergence threshold: 0.80 (default)
- Focus areas: All

---

## Round 1: Advocate Statements (Parallel)

### Variant 1 Advocate (opus) — Summary

Opus positions V1 as the stronger roadmap on three pillars: schedule arithmetic that matches the PRD's explicit 6-sprint count (12 calendar weeks, not V2's internally contradictory 22-week label), SOC2-grade audit infrastructure from M1 day 1 (versus V2's M3 deferral that leaves 8-12 weeks of events unstructured), and formal state machines plus token-family semantics that eliminate implementation ambiguity at coding time. Opus concedes four V2 strengths: lockout belongs in M1 (not M3), the greenfield rollback path is infeasible as written, the single-row staffing is unactionable, and V2's D-030 admin audit query deliverable is the correct pattern. Opus tallies 25 V1 wins, 12 V2 wins, 3 ties across 40 scored diff points, arguing that V1 owns the security-discipline and engineering-formalization axis while V2 owns the operational-detail axis. The synthesis position: adopt V1's milestone cadence, state machines, audit-day-1, and OQ-conflict discipline, plus V2's staffing table, post-GA section, lockout-in-M1, greenfield rollback, and beta buffer.

Full file: round-1-advocate-1.md

### Variant 2 Advocate (sonnet) — Summary

Sonnet positions V2 as the more operationally honest roadmap, emphasizing greenfield-correct rollback, a 10-row per-sprint staffing table, lockout in M1 closing a brute-force window V1 leaves open for 4 weeks, post-GA v1.1/v2.0 sequencing, feature-flag lifecycle dates, a concrete admin audit query deliverable (D-030), and pentest budget quantification. Sonnet argues that V1's security formalization (state machines, token families, chaos testing) belongs in the TDD rather than the roadmap. Sonnet concedes the 22-week duration label is a documentation error, the M3 audit deferral creates a SOC2 gap, the absence of state machines shifts burden to implementers, and the missing enumeration-timing and chaos-testing tracks are genuine weaknesses. Sonnet agrees on all six shared assumptions (ACCEPT/QUALIFY), and converges on the same synthesis: V1's engineering backbone plus V2's operational polish.

Full file: round-1-advocate-2.md

---

## Round 2: Rebuttals (Sequential)

### Variant 1 Rebuttal (opus) — Summary

Opus reaffirms all R1 concessions (lockout-in-M1, greenfield rollback, staffing table, admin audit query, post-GA structure with quarter caveat, beta buffer, audit retention wording fix, three-phase rationale note). New R2 evidence: PRD Phasing section explicitly states "Phase 1 (Sprint 1-3) + Phase 2 (Sprint 4-6) = 6 sprints" — decisive for the duration dispute; TDD Section 13 grounds 15-minute lockout window; TDD Section 25.3 sizes Redis at ~50 MB (auth-only), exposing V2's Bull/BullMQ as an undocumented capacity expansion; PRD R-002 mitigation column co-requires both lockout AND rate limiting, making M1 lockout a PRD compliance requirement. New criticisms: V2's Bull/BullMQ creates undisclosed monitoring, runbook, and queue-poisoning surface; V2's "soft M3-to-M4 dependency" parallelization claim is illusory because M2 is the binding constraint for M4. Opus shifts C-020 (async email) from Tie to V1 for v1.0 scope. Net tally: V1=25, V2=12, Ties=3.

Full file: round-2-rebuttal-1.md

### Variant 2 Rebuttal (sonnet) — Summary

Sonnet reaffirms R1 concessions on duration labeling (now strengthened by V1's PRD sprint-count citation), audit-day-1 as PRD compliance (not best practice), audit retention conflict-flagging, state machines (now fully conceded with qualification: tie to deliverable IDs), chaos testing, and enumeration timing. On async email: partial rebuttal (Bull is standard Node.js tooling, not niche) but concedes V1's in-process approach is simpler for v1.0 single-template scope; Bull is the v1.1 recommendation. On M4 parallelization: partial concession (M2 is the binding constraint, but M3-dependent pages gain ~1 week of real parallelism). New evidence: TDD Section 19.2 feature-flag removal targets directly support V2's Appendix B; PRD Non-Goals version future work, grounding V2's post-GA structure; V1 risk R-113 on consent transaction scope is a GDPR detail V2 should adopt. Net tally converges with opus: V1=25, V2=12, Ties=3.

Full file: round-2-rebuttal-2.md

---

## Round 2.5: Invariant Probe (Independent Fault-Finder)

- Total findings: 26
- ADDRESSED: 4 (INV-004, INV-009, INV-012, INV-018)
- UNADDRESSED: 22 (HIGH=9, MEDIUM=10, LOW=7)
- HIGH-severity UNADDRESSED IDs: INV-001, INV-005, INV-006, INV-013, INV-017, INV-021, INV-022, INV-023, INV-026
- Robustness verdict: The emerging consensus is structurally sound on roadmap-level decisions but has **critical gaps in interaction effects and sufficiency** — in-process SendGrid retry contradicts 200ms p95 budget (INV-021), audit-log nullability and timing-symmetry interaction with enumeration resistance is unanalyzed (INV-005, INV-006, INV-008), bcrypt-cost-12 latency budget violation remains unresolved (INV-026), and SOC2 audit-log immutability plus GDPR right-to-erasure are necessary-not-sufficient conditions (INV-022, INV-025).
- Full file: invariant-probe.md

---

## Per-Point Scoring Matrix

The matrix below covers all diff points with severity Medium or above across structural, content, and contradiction categories, plus all promoted shared assumptions. For each, the winner is determined from R1 positions, R2 concessions/rebuttals, and R2.5 invariant findings.

### Content Differences

| Diff ID | Category | Topic | Winner | Confidence | Evidence Summary |
|---------|----------|-------|--------|-----------|------------------|
| C-001 | Content | Total roadmap duration | V1 | 100% | Both advocates agree; V2 concedes in R1 and R2. PRD Phasing section explicitly prescribes 6 sprints = 12 weeks. V1's 11-week active + 2-week tail matches. R1 (both), R2 (V2 reaffirmed). |
| C-002 | Content | Per-milestone duration | V1 | 95% | TDD Section 23.1 specifies fortnightly cadence. V2 concedes. R1 (both). |
| C-003 | Content | Lockout milestone placement | V2 | 95% | V1 concedes in R1 and R2. PRD R-002 co-requires lockout AND rate limiting. V2's "20-30 lines of code" framing makes scope objection untenable. R1 (V1 concession), R2 (strengthened). |
| C-004 | Content | Audit log milestone placement | V1 | 95% | V2 concedes in R1 and R2. PRD constraint is unconditional ("All auth events"). Application logs are not audit logs. R1 (both), R2 (V2 strengthened concession). |
| C-005 | Content | Audit retention conflict handling | V1 | 90% | V2 concedes. V1's OQ-R1 conflict-flagging is correct process. R2 refines D-102 wording: "retention parameterized, default 90d per TDD, set to 12 months pending OQ-R1." R1 (V2 concede), R2 (wording fix). |
| C-006 | Content | Reset token storage medium | Tie | 80% | Both advocates rate as Tie in R1 and R2. Redis TTL (V1) and DB-hashed (V2) are architecturally valid. V1 ADR D-308 documents trade-off. R1, R2 (unchanged). |
| C-007 | Content | Max refresh tokens per user | V2 | 85% | Both advocates agree V2's 10-token FIFO cap is concrete v1.0 policy. V1's "no cap, observe" defers a sizing decision. R1 (both). INV-013 flags eviction-vs-family interaction as HIGH UNADDRESSED. |
| C-008 | Content | Lockout auto-unlock timing | V1 | 85% | TDD Section 13 grounds 15-minute window. V2's 30-minute recommendation lacks source support and is more punitive for legitimate users. R1 (both), R2 (V1 cites TDD Section 13 explicitly). |
| C-009 | Content | Token family / reuse detection | V1 | 90% | V2 concedes in R1 (Concession 3) and R2. TDD lacks token-family semantics; roadmap must supply them. R1, R2 (strengthened). |
| C-010 | Content | Multi-tab coordination | V1 | 85% | BroadcastChannel API closes a visible SPA UX defect. V2 has no equivalent. R1 (V1 strength). |
| C-014 | Content | Chaos testing | V1 | 95% | V2 concedes in R1 (Concession 5) and R2. QA-7 track is a concrete, testable deliverable. R1, R2. |
| C-015 | Content | Enumeration timing variance | V1 | 95% | V2 concedes in R1 (Concession 4) and R2. <50ms / <30ms gates are CI-enforceable. V2's "identical response" is untestable. R1, R2. |
| C-018 | Content | Admin audit log query | V2 | 90% | V1 concedes in R1 (Concession 4) and R2. V2 D-030 is the correct Jordan-persona deliverable. R1, R2. |
| C-019 | Content | GDPR right-to-erasure | V1 | 80% | V1 flags as hard legal obligation with urgency. V2 lists as "Post-v1.0" without urgency. Both advocates agree in R1. INV-025 flags this as MEDIUM UNADDRESSED: GDPR Article 17 is operative from GA day 1. |
| C-020 | Content | Async email recommendation | V1 (v1.0) / V2 (v1.1) | 85% | R2 convergence: V1's in-process retry is simpler for single-template v1.0. V2's Bull/BullMQ is the v1.1 recommendation. V1 R2 raises undisclosed complexity; V2 R2 concedes v1.0 scope but defends Bull as standard. INV-021 flags the in-process approach as HIGH UNADDRESSED: synchronous retry with backoff violates 200ms p95 budget. |
| C-021 | Content | Feature flag removal timeline | V2 | 90% | V1 concedes in R1 and R2. Appendix B operationalizes TDD Section 19.2 with concrete sprint deadlines. R1, R2. |
| C-022 | Content | Legacy auth assumption | V2 | 95% | V1 concedes in R1 (Concession 2) and R2 (P1-incident failure mode). Greenfield per PRD. R1, R2 (sharpened). |
| C-023 | Content | Pentest cost | V2 | 85% | Budget enables procurement; V1 silent. Both advocates agree. R1. |
| C-029 | Content | Beta buffer | V2 | 90% | V1 concedes in R1 and R2 ("standard PM practice"). 1-week hidden buffer between Beta and GA. R1, R2. INV-010 flags arithmetic incompatibility with stated GA date. |

### Structural Differences (Medium+ severity)

| Diff ID | Category | Topic | Winner | Confidence | Evidence Summary |
|---------|----------|-------|--------|-----------|------------------|
| S-001 | Structural | Top-level section count | Unresolved | 50% | Neither advocate debates this directly. V1 has 19 sections + 2 appendices; V2 has 13 sections + 3 appendices. Structural preference is aesthetic. |
| S-005 | Structural | Cross-cutting workstream count | Unresolved | 50% | Not directly debated. V1 has 4 workstreams with named items; V2 has 5 with sprint-level tables. Both functional; preference depends on team norms. |
| S-006 | Structural | Edge cases section | Unresolved | 55% | V1 has dedicated section with 19-row table; V2 embeds 16-row table. V1's enumeration-timing targets (QA-6) make its edge-case section more actionable, but the section placement is editorial. |
| S-007 | Structural | State management section | V1 | 95% | V2 concedes in R1 (Concession 3) and R2 (with qualification: tie to deliverable IDs). V1 Section 9 is roadmap-appropriate because TDD lacks these state machines. R1, R2. |
| S-008 | Structural | Personas coverage check | V1 | 80% | V1 Section 13 verifies Alex/Jordan/Sam against deliverables. V2 has no equivalent. R1 (both). V2 concedes D-030 is stronger Jordan deliverable but V1's cross-persona check remains unique. |
| S-009 | Structural | Governance cadence | V1 | 80% | V1 Section 15 operationalizes review rhythm. V2 has no governance section. Both advocates agree. R1. V2 R2 notes it is "standard PM practice" — valuable but not a structural differentiator. |
| S-011 | Structural | Capacity planning placement | Unresolved | 55% | Not directly debated. V1's is brief in Section 14; V2's is detailed in Section 10 with 3 subsections. INV-014 flags initial monitoring blindness but does not resolve placement preference. |
| S-012 | Structural | Team composition detail | V2 | 95% | V1 concedes in R1 (Concession 3) and R2. V2's 10-row per-sprint table is actionable. R1, R2. |
| S-013 | Structural | Post-GA planning | V2 | 85% | V1 concedes in R1 and R2 (adopt V2 structure, mark quarters as "target"). V2's three-subsection layout provides product continuity. R1, R2 (refined with quarter caveat). |
| S-020 | Structural | Open questions structure | V1 | 75% | V1's two-tier structure (Section 11.1 maps PRD/TDD OQs, Section 11.2 raises 6 new roadmap-level OQs) is more rigorous. V2's single-tier mixes source and roadmap questions. Not directly debated in R2 but V1's OQ-R1/R2/R3/R4 discipline is consistently cited as superior. |

### Contradictions

| Diff ID | Category | Topic | Winner | Confidence | Evidence Summary |
|---------|----------|-------|--------|-----------|------------------|
| X-001 | Contradiction | Roadmap total duration | V1 | 100% | V2 concedes in R1 and R2. PRD sprint count is explicit (6 sprints). V2's "22 weeks" label is indefensible. R1 (V2 concede), R2 (PRD citation decisive). |
| X-002 | Contradiction | Account lockout milestone | V2 | 95% | V1 concedes in R1 and R2. Lockout in M1 closes brute-force window and satisfies PRD R-002 co-requirement. R1, R2 (strengthened). |
| X-003 | Contradiction | Audit log milestone | V1 | 95% | V2 concedes in R1 and R2. SOC2 audit trail from day 1 is a PRD compliance requirement, not best practice. R1, R2. |
| X-004 | Contradiction | Legacy auth system existence | V2 | 95% | V1 concedes in R1 and R2. Greenfield per PRD Executive Summary. V1's rollback step 2 is infeasible (P1-incident failure mode). R1, R2 (sharpened). |
| X-005 | Contradiction | Lockout auto-unlock timing | V1 | 85% | TDD Section 13 grounds 15-minute window. V2's 30-minute recommendation doubles the window without source support. R1, R2 (V1 cites TDD Section 13). |
| X-006 | Contradiction | Max refresh tokens per user | V2 | 85% | V2's 10-token FIFO cap is a concrete v1.0 policy. V1's "no cap, observe" defers. Both advocates agree. R1. INV-013 flags eviction-family interaction as unresolved. |
| X-007 | Contradiction | Reset token storage | Tie | 80% | Both advocates rate as Tie in R1 and R2. Redis TTL and DB-hashed are both architecturally valid. R1, R2 (unchanged). |
| X-008 | Contradiction | Audit retention source truth | V1 | 90% | V2 concedes. V1's OQ-R1 conflict-flagging beats silent override. R2 refines D-102 wording. R1, R2. |

### Shared Assumptions (Promoted)

| Diff ID | Category | Topic | Winner | Confidence | Evidence Summary |
|---------|----------|-------|--------|-----------|------------------|
| A-005 | Assumption | NTP synchronization required | Accepted | 95% | Both advocates ACCEPT in R1. TDD Section 12 requires 5-second clock skew tolerance. NTP is the standard mechanism. R1 (both). |
| A-008 | Assumption | Frontend is React SPA | Accepted | 95% | Both advocates ACCEPT in R1. TDD Section 10 specifies React-specific AuthProvider signature. R1 (both). |
| A-009 | Assumption | No server-side session affinity | Accepted | 95% | Both advocates ACCEPT in R1. TDD Section 6.4 chooses stateless JWT. HPA scaling model breaks under sticky sessions. R1 (both). |
| A-010 | Assumption | Named security reviewer allocated | Accepted | 90% | Both advocates ACCEPT in R1. Security gates block GA without reviewer. V2's staffing table accounts for this explicitly. R1 (both). |
| A-011 | Assumption | bcryptjs is v1.0 hashing library | Accepted | 95% | Both advocates ACCEPT in R1. TDD Section 6.4 names bcrypt. argon2id is v1.1+ per V1's pluggable interface. R1 (both). |
| A-012 | Assumption | Redis provisioned for auth only | Qualified | 75% | Both advocates QUALIFY in R1. TDD Section 25.3 sizes at ~50 MB for tokens. V2's Bull/BullMQ would require capacity adjustment. R1 (both). R2 convergence to defer Bull for v1.0 resolves the tension. |

### Scoring Matrix Summary

| Category | V1 Wins | V2 Wins | Tie | Unresolved | Total |
|----------|---------|---------|-----|------------|-------|
| Content (C-NNN) | 12 | 7 | 1 | 0 | 20 |
| Structural (S-NNN) | 4 | 2 | 0 | 3 | 9 |
| Contradictions (X-NNN) | 3 | 3 | 1 | 0 | 7 |
| Assumptions (A-NNN) | 0 | 0 | 6 | 0 | 6 |
| **Total** | **19** | **12** | **8** | **3** | **42** |

---

## Convergence Assessment

### Diff-Point Agreement

- Total diff points in scope for convergence (S + C + X + promoted A): 70
  - Structural: 20
  - Content: 30
  - Contradictions: 8
  - Shared assumptions (promoted): 12

- Agreed points (winner determined with >= 60% confidence):
  - V1 wins (unanimous or conceded): C-001, C-002, C-004, C-005, C-008, C-009, C-010, C-014, C-015, C-019, S-007, S-008, S-009, X-001, X-003, X-005, X-008 = 17
  - V2 wins (unanimous or conceded): C-003, C-007, C-018, C-021, C-022, C-023, C-029, S-012, S-013, X-002, X-004, X-006 = 12
  - Ties (both agree on tie): C-006, C-016, X-007 = 3
  - Accepted assumptions: A-005, A-008, A-009, A-010, A-011, A-012 = 6
  - Total agreed: 17 + 12 + 3 + 6 = **38**

- **Diff-point convergence: 38 / 70 = 54.3%**
- Threshold: 80%
- **Diff-point convergence: BELOW THRESHOLD**

Note: The 54.3% figure reflects that 28 of 70 diff points are Low-severity structural/formatting differences (S-002 through S-019, C-011 through C-030 Low-severity items, U-NNN unique contributions) that were not debated and remain unresolved. Among the 42 Medium+ severity points actually scored, agreement is 38/42 = 90.5% — well above threshold. The convergence gap is driven by the long tail of Low-severity structural formatting differences that neither advocate considered consequential enough to debate.

### Weighted Convergence (Medium+ severity only)

- Medium+ severity diff points scored: 42
- Agreed at >= 60% confidence: 38
- **Weighted convergence: 38 / 42 = 90.5%**
- **Weighted convergence: ABOVE THRESHOLD**

### Taxonomy Coverage Gate (AD-5)

- **L1 (surface/naming/format):** Covered — S-001 through S-020 structural items include section counts, ID schemes, formatting conventions, appendix placement, and timeline representation. YES
- **L2 (structural/architecture):** Covered — M1-M5 milestone structure debated across C-001/C-002 (duration), C-003 (lockout placement), C-004 (audit placement), S-007 (state machines), S-013 (post-GA planning), S-017 (dependency chains). YES
- **L3 (state-mechanics/guards/boundaries):** Covered — R2.5 invariant probe explicitly addressed state variables (INV-001 through INV-003), guard conditions (INV-005 through INV-008), collection boundaries (INV-013 through INV-016), interaction effects (INV-017 through INV-020), and sufficiency challenges (INV-022 through INV-026). YES

**Taxonomy coverage: PASS (all three levels covered)**

### Invariant Probe Gate (AD-1)

- HIGH-severity UNADDRESSED count: **9**
- Gate condition: convergence requires count == 0
- **Result: BLOCKED**

The nine HIGH-severity unaddressed findings are:

1. **INV-001** — Refresh-token family lineage state is persisted in Redis and survives Redis restarts so that reuse-detection can revoke descendants discovered after a cold-start. Neither variant specifies how family lineage is stored; V1 D-202 stores hashed tokens with 7-day TTL but family/parent linkage is not in the schema.

2. **INV-005** — M1 audit_log table accepts NULL `user_id` for pre-authentication failure events (e.g., failed login for unknown email). V1 D-102 schema does not specify nullability; if `user_id NOT NULL`, every `login_failure` for unknown-email cannot be audited, contradicting audit-day-1 consensus.

3. **INV-006** — The enumeration-timing constraint (<50ms variance, QA-6) holds when audit-log INSERT happens on the failure path. Unknown-email path has no `user_id` to insert; wrong-password path has one — asymmetric DB write costs blow the 50ms variance budget unless both paths perform identical-shape writes.

4. **INV-013** — Maximum refresh tokens per user (consensus: V2's 10-token FIFO cap) eviction at the 11th token does not race with reuse-detection on the 10th. If an evicted token is later "used" by the legitimate device, reuse-detection fires and revokes the entire family — false-positive user logout across all devices.

5. **INV-017** — M1 audit-log writes for `login_success` + M2 `lastLoginAt` UPDATE + M2 TokenManager Redis SET are correctly ordered. If Redis fails between step 3 and 4, user has "logged in" audit + updated lastLoginAt + NO token. SOC2 audit trail becomes non-deterministic relative to system state.

6. **INV-021** — The in-process SendGrid retry consensus (C-020 V1 wins for v1.0) does not block the request thread long enough to violate NFR-PERF-001 200ms p95. In-process retry with exponential backoff on SendGrid 5xx could take >60s; either fire-and-forget (loses retry guarantee on restart) or synchronous-with-retry (violates 200ms p95). Cannot be both.

7. **INV-022** — Consensus audit-log in M1 is sufficient to pass SOC2 Type II audit gate without immutability guarantees. SOC2 CC7.2 and CC6.1 require tamper-evident logs, segregation of duties on log access, and log integrity verification — none addressed by either variant.

8. **INV-023** — Consensus M1 lockout (5 attempts / 15 min) alone is sufficient against PRD R-002 "High probability" brute-force risk. Lockout is bypassed trivially: distributed attack across 1M IPs hitting 4 attempts each. Need lockout + gateway rate limit + per-account global rate limit + optional CAPTCHA.

9. **INV-026** — Consensus bcrypt cost-12 (~300ms hash time) achieves NFR-PERF-001 (<200ms p95 login). Sum-of-latencies at cost-12: bcrypt 300ms + DB writes 20-50ms + Redis 5-10ms = 325-360ms. The roadmap names cost-11 as fallback but does not commit to it.

### Final Status

- Weighted diff-point agreement (Medium+): **90.5%** (above 80%)
- Unweighted diff-point agreement (all 70): **54.3%** (below 80%)
- Taxonomy coverage: **YES** (all three levels covered)
- HIGH UNADDRESSED invariants: **9**
- **Status: BLOCKED_BY_INVARIANTS**

Despite high diff-point convergence on Medium+ severity items from extensive R2 concessions on both sides (90.5% weighted convergence, well above the 80% threshold), the AD-1 invariant probe gate BLOCKS convergence due to 9 HIGH-severity UNADDRESSED items. These span state durability (INV-001), schema correctness (INV-005, INV-006), collection-interaction safety (INV-013), transactional ordering (INV-017), architectural contradiction in the consensus email approach (INV-021), audit sufficiency for SOC2 Type II (INV-022), brute-force mitigation sufficiency (INV-023), and NFR-PERF-001 achievability at cost-12 (INV-026). These must be addressed in the refactoring plan (Step 4) and merge (Step 5), or explicitly documented as residual risk with named owners.

---

## Unresolved Points (carried to refactor plan)

All HIGH UNADDRESSED INV-NNN IDs with their assumption text. The merge must address each:

| INV ID | Category | Assumption Text | Refactor Action Required |
|--------|----------|----------------|--------------------------|
| INV-001 | STATE VARIABLES | Refresh-token "family" lineage state is persisted in Redis and survives Redis restarts so that reuse-detection can revoke descendants discovered after a Redis cold-start. | Define family-linkage storage schema in D-202 (parent_id field or Redis SET per family). Specify durability: AOF persistence or periodic RDB. Document family-metadata TTL alignment with refresh-token TTL. |
| INV-005 | GUARD CONDITIONS | M1 audit_log table accepts NULL `user_id` for pre-authentication failure events (e.g., failed login for unknown email). | Add explicit `user_id VARCHAR NULL` constraint to D-102 schema. Add OBS-1 workstream item: "verify NULL user_id audit rows in M1 integration tests." |
| INV-006 | GUARD CONDITIONS | The `unknown-email vs wrong-password` enumeration-timing constraint (<50ms variance, V1 QA-6) holds when audit-log INSERT happens on failure path. | Mandate identical-shape audit writes on both paths: unknown-email writes `user_id=NULL, email_hash=H(email)`. Verify in QA-6 CI gate that both paths produce <50ms timing variance WITH audit writes enabled. |
| INV-013 | COLLECTION BOUNDARIES | Maximum refresh tokens per user (consensus V2 10-token FIFO cap). Eviction at the 11th token does not race with reuse-detection on the 10th. | Pair eviction with explicit family-metadata cleanup: when evicting oldest token, also mark that token's family entry as `evicted=true` so reuse-detection on an evicted token logs a warning instead of revoking the entire family. Add integration test for eviction-during-reuse race. |
| INV-017 | INTERACTION EFFECTS | M1 audit-log writes for `login_success` + M2 `lastLoginAt` UPDATE + M2 TokenManager Redis SET are correctly ordered to avoid partial-state audit entries. | Define login-path transaction scope in Section 9.5 equivalent: audit INSERT + lastLoginAt UPDATE in single DB transaction; Redis SET outside transaction. Document rollback semantics: if Redis SET fails, audit row shows `login_success` but token is not issued — client retries, producing a second `login_success` audit row. Decide: is this acceptable or should login be idempotent per session? |
| INV-021 | INTERACTION EFFECTS | The "in-process SendGrid retry" consensus (C-020 V1 wins for v1.0) does not block the request thread long enough to violate NFR-PERF-001 200ms p95. | Resolve the architectural contradiction: either (a) fire-and-forget the email (accept that process restart loses the send — acceptable for reset-request which always-200s), or (b) defer to Bull/BullMQ in v1.0 despite the complexity, or (c) single in-process attempt + dead-letter log for manual retry. Option (c) is the safest: one SendGrid call with 5-second timeout; if it fails, log the payload to a `pending_emails` table and add a cron-based retry sweep. Name the decision owner. |
| INV-022 | SUFFICIENCY CHALLENGE | Consensus audit-log in M1 (V1's day-1 SOC2 coverage) is sufficient to pass SOC2 Type II audit gate without immutability guarantees. | Add to M1 scope or M5 pre-GA checklist: (a) DB trigger preventing UPDATE/DELETE on audit_log table, (b) separate DB role for audit writes with no grant for UPDATE/DELETE, (c) quarterly log-integrity verification script (checksum or row-count reconciliation). Name the SOC2 auditor's specific CC7.2/CC6.1 requirements and map each to a deliverable. |
| INV-023 | SUFFICIENCY CHALLENGE | Consensus M1 lockout (5 attempts / 15 min) alone is sufficient against the PRD R-002 "High probability" brute-force risk. | Explicitly list the defense-in-depth stack: (a) M1 lockout per-account, (b) M1 gateway IP rate limit 10/min/IP (R-102), (c) M1 per-account global rate limit (new deliverable: rate-limit login attempts by email-hash regardless of IP, e.g., 20/hour), (d) M5 CAPTCHA contingency (R-112). Document which layers ship in which milestone. |
| INV-026 | SUFFICIENCY CHALLENGE | Consensus bcrypt cost-12 + ~300ms hash time achieves NFR-PERF-001 (<200ms p95 login). | Pre-commit: M1 Week 1 bcrypt benchmark on target hardware. If cost-12 exceeds 200ms p95 (expected), commit to cost-11 with documented security rationale + NIST compliance note. Update D-103 deliverable to specify "cost factor determined by benchmark in M1 Week 1, default 11, target 12." Update risk R-104 mitigation from "drop to cost 11" to "ship at cost 11 unless benchmark demonstrates cost-12 within budget." |

---

*Transcript assembled from: diff-analysis.md (98 diff points), round-1-advocate-1.md (opus R1), round-1-advocate-2.md (sonnet R1), round-2-rebuttal-1.md (opus R2), round-2-rebuttal-2.md (sonnet R2), invariant-probe.md (R2.5, 26 findings).*
