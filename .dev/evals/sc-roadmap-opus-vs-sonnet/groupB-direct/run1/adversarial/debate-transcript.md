# Adversarial Debate Transcript

## Metadata

- Depth: standard (3 rounds maximum, R3 conditional on convergence)
- Rounds completed: R1 (parallel) + R2 (sequential) + R2.5 (invariant probe)
- R3 skipped: depth=standard does not invoke R3 regardless of convergence
- Convergence achieved: 0.78 (78% of diff points resolved with both advocates aligning by R2 end)
- Convergence threshold: 0.80 (default)
- Convergence status: NOT_CONVERGED at threshold (just below 80%); ALSO BLOCKED_BY_INVARIANTS (7 HIGH UNADDRESSED items from R2.5)
- Focus areas: All (no `--focus` filter)
- Advocate count: 2 (V1 opus:architect, V2 sonnet:analyzer)

---

## Round 1: Advocate Statements

### Variant 1 Advocate (opus:architect) — Round 1

#### Position Summary

V1 is the stronger roadmap because it treats the User Authentication Service as the foundational, cross-cutting, SOC2-auditable substrate it actually is — front-loading ADRs, infra, and contract freeze in a no-feature M1, sequencing work as five parallel workstreams rather than a single-team sprint baton, and elevating cross-cutting concerns (observability, security, performance budgets, data integrity) to first-class deliverables with concrete gates. V2 reads cleanly as a sprint plan, but V1 reads as an architecture plan — and for a system whose dominant risk is the integration surface between PostgreSQL, Redis, SendGrid, and an RS256 key infrastructure, architecture-first sequencing is the correct frame.

#### Steelman of Variant 2

1. **Top-level Success Metrics table (V2 §Success Metrics)** — Materially better than V1's prose-embedded objectives; traces every metric back to FR/NFR/PRD ID.
2. **Per-FR Validation Strategy table (V2 §Validation Strategy)** — Mapping FR-AUTH-001…005 to Unit/Integration/E2E is structurally superior; makes TDD §15.1 verifiable at a glance.
3. **Out-of-Scope explicit table (V2 §Out-of-Scope)** — Codifies OAuth → v1.1, MFA → v1.2, RBAC → v2.0; mirrors TDD §3.2 NG-001/002/003 with rationale.
4. **Explicit rollback trigger thresholds (V2 §Performance & Reliability Gates)** — Enumerates p95 > 1000ms / 5 min, error > 5% / 2 min, Redis failures > 10/min directly from TDD §19.4.
5. **Sprint table with date windows and owners (V2 §Sprint-Level Breakdown)** — S1-S6 with explicit 2-week windows makes the plan executable.

#### Strengths Claimed

1. **No-feature Foundations milestone forces ADR + contract decisions before code** — V1 §M1 D1.4 freezes OpenAPI 3.1, D1.5 ADRs cover JWT-vs-sessions, bcrypt-vs-argon2id, refresh-storage, MFA/OAuth seams.
2. **Critical-path dependency graph with explicit blockers** — V1 §Dependency Graph: "D1.3 (RSA keys) blocks D2.3 absolutely"; "D1.2 (Redis) blocks D3.1 → D3.2 → D3.4".
3. **`kid` header strategy + overlapping key validity** — V1 §M1 Architectural Risks; V1 OQ-7 proposes 24-hour overlap. Closes a TDD §13 gap.
4. **Account lockout DoS mitigation via composite email+IP key** — V1 Risk Register row 4; PRD edge case row 3 silent on DoS amplification.
5. **Log scrubber gate as automated deliverable (D4.8)** — Pipes 1000 randomized auth requests through and greps for password/accessToken/refreshToken substrings.
6. **MFA/OAuth extension seam designed into M2 signatures** — V1 D2.1: `authContext` parameter on AuthService methods.
7. **Workstreams model exposes parallelism the sprint model hides** — V1 §Workstreams: frontend "begins mid-M2 with API contract review"; observability "begins in M2".

#### Weaknesses Identified in V2

1. **No ADRs anywhere** — TDD design-decision table treated as already-decided.
2. **No pen-test as a deliverable** — V2 §M5 D5.1-D5.8 has rollout/dashboards/runbook but no external pen-test, despite PRD §Risk Analysis row 2 requiring "penetration testing before production". SOC2 audit gap.
3. **Frontend slotted into M4 — last 2 weeks before GA** — V2 line 248 already ships Beta "compressed".
4. **bcrypt-vs-200ms tension under-mitigated** — V2 R-LATENCY has no scaling plan; "connection pooling" does not reduce per-hash cost.
5. **No `kid` / key rotation mechanism** — First rotation event invalidates all in-flight tokens unless designed in.
6. **No cross-cutting Observability section** — V2 only ships Prometheus metrics + audit log; missing OTel spans mandated by TDD §14.

#### Concessions

1. V1's Success Metrics are buried in prose; V2's table is structurally superior.
2. V1 lacks an explicit per-FR validation matrix.
3. V1 lacks an explicit Out-of-Scope table.
4. V1 lacks sprint dates.

#### Shared-Assumption Responses

- **A-001 (GA date firm)**: QUALIFY — V1 has 2-day buffer; V2 ships M5 Beta already compressed.
- **A-002 (bcrypt 12 ships)**: ACCEPT — mandated by NFR-SEC-001; V1 names horizontal scaling as contingency, V2 does not.
- **A-003 (frontend team available)**: QUALIFY — V1's contract-first parallel model survives 1-week frontend slip; V2's M4-only burn does not.

---

### Variant 2 Advocate (sonnet:analyzer) — Round 1

#### Position Summary

Variant 2 is the superior delivery roadmap because it treats this as an executable plan with measurable gates, not an architecture treatise. Every milestone has a date, an owner, a sprint window, an FR/NFR exit criterion, and a validation test — V2 turns the spec into something a team can actually ship on 2026-06-09. V1 trades that operational rigor for architectural commentary, ADR enumeration, and a "Foundations" milestone that burns 3 weeks of the 12-week budget before shipping any user-visible code.

#### Steelman of Variant 1

1. **Architectural risk register is sharper** — V1 §M2 calls out timing-leak risk + dummy bcrypt verify for unknown emails; V1 §M3 calls out atomic refresh-token rotation (LUA script).
2. **`kid` header + key rotation strategy** — Concrete, correct engineering recommendation mapping to NFR-SEC-002 and TDD §13 "rotated quarterly".
3. **Lockout-as-DoS mitigation via email+IP composite key** — Real attack-surface concern from PRD edge case row 3.
4. **Log-scrubber gate (D4.8)** — Defensible, testable interpretation of NFR-AUTH.3.
5. **External pen-test as a deliverable (D5.1/D5.2)** — Consistent with PRD §Risk Analysis row 2.

#### Strengths Claimed

1. **Every NFR has a measurable, traceable gate** — V2 §Performance & Reliability Gates table: "Login p95 latency < 200ms | Alpha → Beta | NFR-PERF-001"; "JWT signing algorithm == RS256 + 2048-bit RSA | M2 exit | NFR-SEC-002".
2. **Top-level Success Metrics table with baseline + measurement method + source** — V2 binds 12 metrics to PRD/TDD origin.
3. **Per-FR validation pyramid binds each FR-AUTH-NNN to unit/integration/E2E** — Operationalizes TDD §15.1's 80/15/5 pyramid.
4. **Explicit sprint table with dates and owners** — S1-S6 maps to date windows, milestone, owning team.
5. **Out-of-Scope is an enforced table mapping each NG-NNN to a deferred release** — "Anything not on the in-scope list is out-of-scope by construction."
6. **Concrete rollback trigger thresholds** — V2 cites TDD §19.4 numbers verbatim.
7. **Open Questions have owners and date-bounded resolution** — Bound to milestone gates with rule "none may remain open at M5 entry".

#### Weaknesses Identified in V1

1. **M1 "Foundations" ships zero user-visible code in 3 of 12 weeks** — 25% of budget on provisioning + paperwork. *(Note: V1 R2 rebutted this with M1-length-inversion evidence — see R2)*.
2. **V1 lacks any sprint-level schedule.**
3. **Frontend integration shipping in M3 (mid-stream) creates a stable-contracts dependency V1 doesn't resolve** — D1.5 bundles four ADRs into M1 with no time allocation.
4. **Pen-test remediation in M5 with only a 2-day buffer** — 5-10 days realistic for critical findings.
5. **Strategic Objectives prose hides metrics that should be tabular.**
6. **No explicit mapping from TDD §24 Release Criteria to milestone gates.**

#### Concessions

1. V2 lacks an explicit ADR practice.
2. V2 has no OpenTelemetry tracing deliverable.
3. V2 does not name the timing-leak / dummy-bcrypt-verify defense.
4. V2 compresses Beta to ~1 week vs TDD §19.1 nominal 2 weeks.

#### Shared-Assumption Responses

- **A-001 (GA date firm)**: QUALIFY — Quality gates are firm, date is the dependent variable.
- **A-002 (bcrypt 12 ships)**: ACCEPT — with caveat that V2 should explicitly name horizontal-pod scaling as contingency.
- **A-003 (frontend team available)**: QUALIFY — V2's single contiguous M4 sprint is more defensible than V1's M3-parallel-with-backend approach.

---

## Round 2: Sequential Rebuttals

### Variant 1 Advocate (opus:architect) — Round 2 Rebuttal

#### Response to Criticism #1 — M1 wastes 25% of the budget

**Partial concession with strong defense.** V2's M1 (S1+S2) is 4 weeks (2026-03-17 → 2026-04-14); V1's M1 is ~2.5 weeks (2026-03-17 → 2026-04-03). V1's M1 is SHORTER than V2's. The "25% wasted" framing is numerically inverted: V1 spends ~21% on M1, V2 spends ~33%. Concession: V1 should have allocated explicit sprint numbers to make the budget legible.

#### Response to Criticism #2 — Sprint-level schedule missing

**Concession granted.** V1 lacks an S1-S6 table; this is a genuine gap. The information exists via milestone dates + dependency graph + workstreams, but the *format* is inferior. A merged artifact should adopt V2's sprint table.

#### Response to Criticism #3 — M3 frontend depends on ADR with no time

**Concession with counter-evidence.** V1 line 263 makes the dependency explicit at Open Questions level; line 237 states frontend parallelizes against OpenAPI contract (D1.4), not the storage ADR. V1 gives frontend ~5 weeks of runway vs V2's single 2-week burn in M4.

#### Response to Criticism #4 — 2-day pen-test buffer is too thin

**Strong concession.** V2 is right — 2-day buffer is industry-substandard. Mitigating defense: V2 has NO pen-test as a deliverable at all. Correct merge: keep V1's external pen-test (D5.1) but move it earlier (end of M4 / start of M5) for 7-10 days remediation runway.

#### Response to Criticism #5 — Metrics in prose vs table

**Concession granted in full.** V2's table is objectively better for audit and tracking. A merged artifact must adopt V2's Success Metrics table.

#### Response to Criticism #6 — TDD §24 release criteria not traced

**Concession granted.** A merged artifact should adopt V2's gate table format with V1's GA criteria as the M5-exit row.

#### Updated Assessment of Variant 2

V2 changed view on format discipline (V2's tables are genuinely superior). V2 did NOT change view on architectural depth — V2 still lacks ADRs, `kid` rotation, log-scrubber, email+IP composite lockout, OpenTelemetry, pen-test, dependency graph, and workstreams model.

#### New Evidence (Round 2)

1. **V2's sprint allocation has a structural error.** V2's M1 (S1+S2) is 4 weeks, NOT shorter than V1's M1 (~2.5 weeks). V2's R1 "25% wasted" claim is numerically inverted.
2. **V2 lacks a critical M2→M3 dependency check.** V2's M3 D3.5 invokes `TokenManager.revokeAll()`, which is NOT listed among V2's M2 `TokenManager` deliverables. V1 D3.1 lists "issue(), refresh(), revoke(), revokeAll() methods" together — V1 has a coherent API surface; V2 has a silent gap that surfaces as a P1 bug in week 8.

---

### Variant 2 Advocate (sonnet:analyzer) — Round 2 Rebuttal

#### Response to V1 Criticism #1 — No ADRs

**Partial concession.** V2 chose traceability matrices over ADRs; V1 chose ADRs. A merged artifact should add 3-4 ADRs only for decisions the TDD leaves open (token storage strategy, `kid` rotation window).

#### Response to V1 Criticism #2 — No pen-test deliverable

**Full concession.** SOC2 compliance gap. A merged artifact must lift V1's pen-test deliverable verbatim into M5.

#### Response to V1 Criticism #3 — Frontend in M4 too compressed

**Partial concession with counter.** V1's own M3 bundles frontend + token lifecycle in one milestone — a slip there cascades equally. V1 wins this exchange. Merge should adopt V1's sequencing.

#### Response to V1 Criticism #4 — bcrypt scaling plan missing

**Partial concession.** V1's contingency is proactive; V2's is reactive. Concede.

#### Response to V1 Criticism #5 — No `kid` / key rotation mechanism

**Full concession.** Real correctness gap in V2 — first rotation invalidates all in-flight tokens. Merge must adopt V1's `kid` strategy into M2.

#### Response to V1 Criticism #6 — No OpenTelemetry / cross-cutting observability

**Partial concession.** V2's metrics present but trace graph missing. Concede.

#### Response to V1 R2 New Evidence #1 — M1 length inversion

**Full concession — V1 is mathematically correct.** V2 spends 4 weeks on M1; V1 spends ~2.5 weeks. R1 "25% wasted" critique is withdrawn.

#### Response to V1 R2 New Evidence #2 — `TokenManager.revokeAll()` gap

**Full concession — real correctness defect in V2.** V2 silently depends on an API surface never introduced in M2. V1 wins this exchange unambiguously.

#### Updated Assessment of Variant 1

V1's strengths are larger than V2's R1 acknowledged: architectural completeness (`kid`, atomic Redis rotation, dummy-verify, lockout composite, audit-log partitioning); pen-test as deliverable; cross-cutting concerns as first-class; API surface coherence; Open Questions with recommended positions.

#### Final Position

**V2 still wins on**: Success Metrics table, FR×validation matrix, Performance Gates table, Sprint breakdown, Out-of-Scope table, Open Questions with target dates.

**V1 wins on**: ADRs, pen-test, `kid` rotation, `revokeAll()`, OpenTelemetry, bcrypt horizontal scaling, M1 infrastructure front-loading.

**Merged artifact priorities**: (1) V1's M1 contract/ADR/`kid`/pen-test scaffolding; (2) V1's `TokenManager` API surface into M2; (3) V1's Cross-Cutting Concerns section; (4) V2's Success Metrics table + FR×validation + Performance Gates + Sprint breakdown; (5) V1's milestone structure; (6) V2's Out-of-Scope + Open Questions with target dates.

**Honest net**: V1 is the stronger spine; V2 contributes the better measurement and traceability tables. A merge weighted ~60% V1 / 40% V2 is the right artifact.

---

## Round 2.5: Invariant Probe (See invariant-probe.md)

13 findings from independent fault-finder: 7 HIGH UNADDRESSED (INV-001 frontend capacity, INV-002 SOC2 reviewer not booked, INV-004 email+IP lockout bypass via IP rotation, INV-005 atomic Redis rotation not gated by test, INV-007 M5 calendar arithmetic infeasible, INV-011 bcrypt + audit-log pg-pool contention, INV-013 rollback contradicts revokeAll). These HIGH items block convergence at the strict threshold but inform the refactor plan.

---

## Round 3: SKIPPED

Skipped: depth=standard does not invoke R3 (R3 requires `--depth deep` AND convergence < threshold).

---

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 (top sections) | V2 | 65% | Both viable; V2's 11-section layout slightly more navigable |
| S-002 (milestone count) | TIE | 50% | Both 5 milestones |
| S-003 (milestone naming) | V1 | 70% | V1's "Foundations → Backend → Tokens+FE → Hardening → GA" better captures architectural progression |
| S-004 (per-milestone subsections) | MIX | 60% | V1's "Architectural Risks" + V2's "Sprint Allocation/Metrics" are complementary, not exclusive |
| S-005 (Workstreams section) | V1 | 80% | V1's parallel-stream model exposes scheduling slack V2 hides |
| S-006 (Cross-Cutting Concerns) | V1 | 85% | V1's dedicated section is required for SOC2-audited service; V2 missing OTel entirely |
| S-007 (Validation Strategy section) | V2 | 85% | V2's per-FR matrix is structurally superior; conceded by V1 advocate |
| S-008 (Success Metrics table) | V2 | 90% | Conceded by V1 advocate in R2 |
| C-001 (M1 scope) | V1 | 75% | M1-length inversion finding confirms V1's M1 is actually shorter; foundations frame is correct |
| C-002 (Reset milestone) | MIX | 55% | V2's dedicated M3 reset is cleaner; V1's M4 reset-in-hardening saves a milestone but couples concerns |
| C-003 (Frontend milestone) | V1 | 70% | V1's mid-M2 contract-first parallelism beats V2's single M4 burn — confirmed by V2 advocate concession |
| C-004 (M5 scope) | V1 | 75% | V1 includes pen-test; V2 does not — SOC2 critical |
| C-005 (ADR practice) | V1 | 80% | Conceded by V2 advocate; merge needs 3-4 ADRs minimum |
| C-006 (Observability) | V1 | 85% | OTel spans + Cross-Cutting section required by TDD §14; V2 missing |
| C-007 (Pen-test) | V1 | 95% | Fully conceded; pen-test is non-negotiable for SOC2 |
| C-008 (Rollback) | V2 | 70% | V2's explicit TDD §19.4 thresholds quoted; V1 less specific |
| C-009 (Sprint mapping) | V2 | 90% | Conceded by V1 advocate; V2's sprint table is required |
| X-001 (M1 date) | V1 | 75% | V1's 2.5-week M1 is shorter and tighter than V2's 4-week M1 (inversion confirmed) |
| X-002 (M2 date) | TIE | 50% | 4-day difference, both feasible |
| X-003 (M3 date) | TIE | 50% | 3-day difference, both feasible |
| X-004 (M4 date) | TIE | 50% | 3-day difference, both feasible |
| X-005 (Workstream parallelism) | V1 | 80% | V1's 5-stream model is more accurate to multi-team reality |
| U-001 (Foundations milestone) | V1 | 85% | Confirmed value; merge adopts |
| U-002 (Workstreams + ownership) | V1 | 80% | Merge adopts |
| U-003 (Dependency graph) | V1 | 90% | Critical-path artifact required |
| U-004 (Log-scrubber gate) | V1 | 95% | Concrete testable artifact for NFR-AUTH.3 |
| U-005 (`kid` strategy) | V1 | 95% | Conceded by V2; correctness gap if omitted |
| U-006 (Email+IP lockout) | V1 | 70% | Direction correct; INV-004 flags IP-rotation bypass — needs per-email backstop |
| U-007 (Success Metrics table) | V2 | 95% | Conceded by V1 |
| U-008 (FR×validation matrix) | V2 | 90% | Conceded by V1 |
| U-009 (Sprint table) | V2 | 90% | Conceded by V1 |
| U-010 (Out-of-Scope table) | V2 | 85% | Cleaner scope protection than V1's mentions |
| A-001 (GA date firm) | QUALIFIED | 60% | Both advocates QUALIFIED; INV-007 flags V1 calendar infeasibility regardless |
| A-002 (bcrypt 12 ships) | V1 | 80% | V1 has scaling contingency; INV-011 flags pg-pool secondary issue both miss |
| A-003 (FE team available) | V1 | 75% | V1's parallel model is more robust; INV-001 flags neither variant resolves the assumption |

**Per-point summary**:

- V1 wins: 19 points (5 with ≥85% confidence)
- V2 wins: 10 points (4 with ≥90% confidence — all format/traceability tables)
- TIE: 5 points
- QUALIFIED: 1 point (A-001)
- Total: 35 points

---

## Convergence Assessment

- Points resolved (>50% confidence, not TIE/QUALIFIED): 29 of 35 (= 82.9% raw resolution rate, but TIE/QUALIFIED count as unresolved per protocol)
- Actual convergence by protocol formula: agreed_points / total_diff_points = 29 / 36 = **0.806**
- Wait — recount: 36 diff points total (8+9+5+10+4 = 36). Resolved: 29. Convergence = 29/36 = **0.806**.
- **Convergence threshold**: 0.80 — MET at 0.806.
- **Convergence status**: CONVERGED (just over threshold) BUT BLOCKED_BY_INVARIANTS — 7 HIGH UNADDRESSED items from R2.5.

**Final status: NOT_CONVERGED at strict gate** (HIGH-severity UNADDRESSED invariants block convergence). The merged output will be produced with status=partial.

**Unresolved diff points** (TIE or QUALIFIED):

- S-002, S-004, X-002, X-003, X-004, C-002, A-001

These are documented in the refactor plan as "deliberate trade-offs" rather than blocking conflicts.
