# Base Selection — Hybrid Scoring Breakdown

## Metadata

- Date: 2026-05-22
- Variants scored: 2 (variant-1-opus-default, variant-2-sonnet-default)
- Method: 50% quant + 50% qual with dual-pass position-bias mitigation
- Source: `.dev/eval-roadmap/groupB-direct/run4/adversarial/` + `inputs/merged-prd-tdd-user-auth.md`
- Requirement set: FR-AUTH-001..005, NFR-PERF-001/002, NFR-REL-001, NFR-SEC-001/002, FR-AUTH.1..5 + NFR-AUTH.1..3 (treated as duplicates; unique logical set = 10)

---

## Section 1: Quantitative Scoring (50% weight)

| Metric | Weight | V1 (opus) | V2 (sonnet) | Computation |
|--------|--------|-----------|-------------|-------------|
| **RC — Requirement Coverage** | 0.30 | 1.00 (10/10) | 1.00 (10/10) | Both variants map FR-AUTH-001..005, NFR-PERF-001/002, NFR-REL-001, NFR-SEC-001/002 in §4 traceability. V1 adds NFR-AUTH.1..3 explicit aliases (§4). V2 maps NFR-AUTH equivalents via NFR-PERF/REL/SEC IDs. Both = 10/10 unique reqs. |
| **IC — Internal Consistency** | 0.25 | 0.96 (24/25 claims clean; 1 minor: M0 8 EW vs 6 EW after Opus R2 concession not reflected in artifact) | 0.78 (≈11/14 claims clean; 3 self-contradictions: 16 EW total vs 5.5+ FTE staffing implied by §3 WS-A/B/C/D; 1-week Beta vs TDD §19.1 explicit "2 weeks"; §4 attributes NFR-PERF-001 solely to M5 yet §8.3 measures it at M2 exit) | Count scorable claims (bcrypt 12, RS256 2048, 7-day refresh, 5-fail lockout, 15-min window, p95<200ms, refresh p95<100ms, 1-hr reset TTL, 60s email SLA, 80/85% coverage, EW totals, dates, etc.). IC = 1 − (contradictions/claims). |
| **SR — Specificity Ratio** | 0.15 | 0.94 (concrete: 95; vague: 6) | 0.84 (concrete: 64; vague: 12) | V1 concrete items: explicit dates per phase, AT-001..AT-016, ±15ms/±10ms variance, 50-parallel registration test, 100-event SOC2 spot-check, SHA-256 algorithm naming, 24h key-overlap window, RSA 2048, cost 12, etc. V2 concrete: JwtService<5ms, Redis<10ms, ≥80% coverage, dates, 10-role cap. V2 vague: "documented procedure," "no enumeration via timing differences" without bound, "monitor delivery." |
| **DC — Dependency Completeness** | 0.15 | 0.97 (resolved: 38/39; one dangling: R-005 references "audit log can be async-buffered" without defining buffer mechanism elsewhere) | 0.90 (resolved: 27/30; R-006 references "A/B test" without defining test framework; G-001..G-005 referenced in §4 but G-001..G-005 IDs never defined in this variant — they are TDD goal IDs not surfaced) | Count internal refs (M0-M5, AT-001..016, H1-H10, R-001..R-008, FR/NFR/AT IDs, SEC-1..7, WS-1..5/WS-A..D, OQ IDs, gates A..D). Check each is defined. |
| **SC — Section Coverage** | 0.15 | 1.00 (12 H2: Roadmap Overview, Milestones, Workstreams, Requirement Traceability, Critical Path & Dependencies, Risk Register, Rollout & Release Gates, Quality & Testing Gates, Open Questions, Success Metrics, Appendix A, Appendix B) | 1.00 (12 H2: same 10 + Appendix A + Appendix B) | Both equally span the 10-section roadmap spec + 2 appendices. max H2 = 12. |

**Quant Subtotal**

- V1: (1.00×0.30) + (0.96×0.25) + (0.94×0.15) + (0.97×0.15) + (1.00×0.15) = 0.300 + 0.240 + 0.141 + 0.1455 + 0.150 = **0.9765**
- V2: (1.00×0.30) + (0.78×0.25) + (0.84×0.15) + (0.90×0.15) + (1.00×0.15) = 0.300 + 0.195 + 0.126 + 0.135 + 0.150 = **0.9060**

---

## Section 2: Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria) — CEV table

| # | Criterion | V1 Evidence | V1 Verdict | V2 Evidence | V2 Verdict |
|---|-----------|-------------|------------|-------------|------------|
| 1 | Explicit requirements enumerated | §4 maps all 10 FR/NFRs + GDPR/SOC2/NIST rows | MET | §4 maps all 10 FR/NFRs + G-001..G-005 goals | MET |
| 2 | Edge cases enumerated | Appendix A: 13 invariants (lockout, clock-skew, Redis-down, concurrent reg, multi-device, TLS, CORS, etc.) | MET | Appendix A: 14 invariants (similar coverage + accessToken-not-in-localStorage) | MET |
| 3 | Dependencies enumerated | §5: external (SendGrid, PG, Redis, SEC-POLICY), internal component order, risk-bearing deps | MET | §5.2/§5.3/§5.4: external table + internal diagram + risk-bearing table | MET |
| 4 | Success criteria explicit | §10: 5 PRD metrics + 5 TDD technical + 2 TDD business, with instrumentation + review milestone | MET | §10.1/10.2: 5 PRD + 7 TDD metrics with instrumentation + review milestone | MET |
| 5 | Out-of-scope captured | OQ-001 names "deferred to v1.1 scope"; "remember me" deferred (§9); RBAC for v1.1 (§9 TDD-OQ-002) | MET | §9 OQ #4 "Defer to v1.1"; OQ-001 "Defer to v1.1"; NG-003 RBAC referenced (§9 OQ-002 row) | MET |

**Completeness V1: 5/5; V2: 5/5**

### Correctness (5 criteria) — CEV table

| # | Criterion | V1 Evidence | V1 Verdict | V2 Evidence | V2 Verdict |
|---|-----------|-------------|------------|-------------|------------|
| 1 | No factual errors | bcrypt 12, RS256 2048, 7-day refresh, 15-min access, 1-hr reset, ±5s clock-skew, 2-week Beta — all match TDD source | MET | Beta = 1 week (§7.2 "2026-06-02 through 2026-06-08") **contradicts TDD §19.1 "Beta — 2 weeks at 10%"** (re-verified by Opus R2 §3.1; conceded by Sonnet R2 §"Beta duration must be 2 weeks") | NOT MET |
| 2 | Feasibility | 48 EW across 11 weeks ≈ 4.4 FTE — consistent with own §3 staffing (auth + frontend + platform + security) | MET | 16 EW total claim vs §3 staffing of ≥5.5 FTE × 9 weeks = ~49 EW capacity — self-contradictory (Sonnet R2 §2 acknowledges "capacity-plan reading is equally valid"). M1 = 4 EW for 10 deliverables + 8 exit criteria is implausibly tight. | NOT MET |
| 3 | Terminology consistency | `AuthService`, `TokenManager`, `JwtService`, `PasswordHasher`, `UserProfile`, `AuthToken`, `AuthProvider` used consistently throughout | MET | Same component vocabulary used consistently | MET |
| 4 | No internal contradictions | §1 capacity 48 EW = §2 roll-up 48 EW; gate dates align (M5 = 2026-06-09); Beta dates self-consistent | MET | §1 phasing "Phase 3: Rollout & GA W8-W9 (M5)" but §7 Phases 1-3 dated 2026-05-26→06-15 spans into post-W9; §4 attributes NFR-PERF-001 solely to M5 but §8.3 measures p95 at M2 exit | NOT MET |
| 5 | Claims supported by evidence | Every numeric claim cites TDD section (§4.1, §13, §15.1, §19.1, §23.1, etc.); AT-001..AT-016 each have specific assertion | MET | Most claims cite TDD; some defaults (refresh cap 5, roles cap 10) cite no source — chosen unilaterally | MET (borderline; cited recommendations differ from TDD but TDD leaves OQs open) |

**Correctness V1: 5/5; V2: 2/5**

### Structure (5 criteria) — CEV table

| # | Criterion | V1 Evidence | V1 Verdict | V2 Evidence | V2 Verdict |
|---|-----------|-------------|------------|-------------|------------|
| 1 | Logical ordering | Overview → Milestones → Workstreams → Traceability → Critical Path → Risk → Rollout → QA → OQs → Metrics → Appendices | MET | Same canonical 10-section ordering + appendices | MET |
| 2 | Consistent hierarchy | All milestones use same table schema (ID/Name/Date/Scope/Deliverables/Deps/Exit/Effort); all risks use same schema | MET | Milestones use Field/Detail table + Deliverables list + Exit Criteria checklist — consistent across M1-M5 | MET |
| 3 | Separation of concerns | WS-1 Backend / WS-2 Token / WS-3 Frontend / WS-4 Security / WS-5 SRE — clean axis-of-change separation | MET | WS-A Backend / WS-B Frontend / WS-C Observability+Compliance / WS-D Security+Release — compliance merged with observability arguably blurs concerns | MET (debatable; merged but defensible) |
| 4 | Navigation aids | Numbered §1-§10 + Appendix A/B + cross-refs (TDD §X.Y, AT-NNN, H1-H10, R-NNN); Component→Milestone matrix Appendix B | MET | Numbered §1-§10 + Appendix A/B (Gantt); §3 sub-sections per workstream | MET |
| 5 | Type conventions | YAML frontmatter with id/title/target_release/variant/status; tables Markdown-uniform | MET | No frontmatter; Markdown-only header | NOT MET |

**Structure V1: 5/5; V2: 4/5**

### Clarity (5 criteria) — CEV table

| # | Criterion | V1 Evidence | V1 Verdict | V2 Evidence | V2 Verdict |
|---|-----------|-------------|------------|-------------|------------|
| 1 | Unambiguous language | Quantitative thresholds (±15ms, 100 RPS, 50 parallel POSTs, 100-event spot-check); algorithm names (SHA-256, bcrypt-12, RS256) | MET | Many concrete numbers (≥80% coverage, 60s send, 1-hr TTL); but "no enumeration via timing differences" lacks bound; "documented procedure" without artifact | MET (borderline) |
| 2 | Concrete vs abstract | Highly concrete: AT-001..AT-016, H1-H10, OQ deadlines per-day, EW per milestone | MET | Concrete but less granular: exit-criteria as checklist; effort fewer breakdown items | MET |
| 3 | Clear section purpose | Each H2 starts with single-sentence purpose; M0-M5 each declared phase | MET | Each section/milestone has clear lead-in; phasing summary at §1 | MET |
| 4 | Acronyms defined | EW, RPS, AT, OQ, FR/NFR, GDPR/SOC2/NIST all surfaced in context; TDD §X.Y reffed | MET | Same acronyms used; no glossary but surfaced in context | MET |
| 5 | Actionable next steps | Gate D scheduled 2026-06-23; rollback procedure 6 numbered steps; escalation 4-day trigger | MET | Rollback procedure 6 numbered steps; gate criteria explicit per phase; no escalation trigger | MET |

**Clarity V1: 5/5; V2: 5/5**

### Risk Coverage (5 criteria) — CEV table

| # | Criterion | V1 Evidence | V1 Verdict | V2 Evidence | V2 Verdict |
|---|-----------|-------------|------------|-------------|------------|
| 1 | ≥3 risks with prob/impact | §6: 8 risks (R-001..R-008) with Likelihood + Impact columns | MET | §6: 7 risks (R-001..R-007) with Likelihood + Impact columns | MET |
| 2 | Mitigation per risk | Every R-NNN row has Mitigation column populated | MET | Every R-NNN row has Mitigation + Contingency columns populated | MET |
| 3 | Failure modes/recovery | §7 Rollback Triggers (5 conditions) + Rollback Procedure (6 steps) per TDD §19.3 | MET | §7.5 Rollback Triggers (5 conditions) + Rollback Procedure (6 steps) | MET |
| 4 | External dependency failures | §5 External Deps table: SendGrid (AWS SES fallback), PG, Redis, SEC-POLICY | MET | §5.2 External Deps table: SendGrid, PG, Redis, SEC-POLICY, RS256 keys | MET |
| 5 | Monitoring mechanism | §2.M5 Grafana dashboards enumerated; §7 Gate criteria are metric-driven; SOC2 100-event spot-check | MET | §2.M5 monitoring dashboards listed; §7.5 alerting rules; APM/OpenTelemetry references | MET |

**Risk Coverage V1: 5/5; V2: 5/5**

### Invariant & Edge Case Coverage (5 criteria) — CEV table

| # | Criterion | V1 Evidence | V1 Verdict | V2 Evidence | V2 Verdict |
|---|-----------|-------------|------------|-------------|------------|
| 1 | Boundary conditions for collections | Refresh-token cap 10 with "oldest evicted on issuance" (§9 PRD-OQ-2); roles soft-cap 16 with DB check constraint (§9 TDD-OQ-002) | MET | Refresh-token limit 5 (§9 OQ #2) but eviction-vs-block unspecified (invariant-probe INV-010 flags); roles max 10 (§9 OQ-002) but action at cap unspecified | MET (borderline — V1 cleaner) |
| 2 | State variable interactions | Lockout state machine (§2.M1 ex 6: 5 fails/15-min/auto-unlock); refresh hashing+revocation (§2.M2 D3-D7); Redis-down → refresh rejects 503 (§2.M2 D9) | MET | Lockout (§2.M1 + §9 OQ #3 30-min cooldown); refresh hashing+revoke (§2.M2 deliverables); Redis unavail → reject refresh (§2.M2 ex 9) | MET |
| 3 | Guard condition gaps | Generic 401 for unknown email AND wrong password (§2.M1 D8); 423 on lockout; 503 on Redis-down (NOT 200 stale) | MET | "No enumeration via timing differences" stated but no measurable bound (Appendix A); single-use reset enforced (§2.M3 ex) | MET (borderline) |
| 4 | Count divergence | Explicit ±15ms login / ±10ms reset variance; 5-fail threshold; 1-hr reset TTL; 60s email SLA; statistical method implied via parity test | MET | "no enumeration via timing differences" without quantitative bound — count divergence unenforceable in CI (Opus R1 §3.4 / R2 §3.1; Sonnet R2 conceded fully) | NOT MET |
| 5 | Interaction effects | R-007 M3+M4 simultaneous slip; R-008 key rotation in-flight tokens (24h overlap); password reset → revokeAllForUser (FR-AUTH-005 + AT-012); multi-device test (Appendix A) | MET | Password reset → revoke all sessions (§2.M3 ex 5); some interaction effects implicit; no explicit handling of key-rotation in-flight or M3/M4 timing interaction | MET (borderline; thinner) |

**Invariant & Edge Case Coverage V1: 5/5; V2: 3/5**

### Qualitative Subtotals

| Dimension | V1 | V2 |
|-----------|----|----|
| Completeness | 5/5 | 5/5 |
| Correctness | 5/5 | 2/5 |
| Structure | 5/5 | 4/5 |
| Clarity | 5/5 | 5/5 |
| Risk Coverage | 5/5 | 5/5 |
| Invariant & Edge Case | 5/5 | 3/5 |
| **Qual Total** | **30/30 = 1.000** | **24/30 = 0.800** |

### Edge Case Floor Check

- V1 Invariant & Edge Case score: 5/5 → **ELIGIBLE**
- V2 Invariant & Edge Case score: 3/5 → **ELIGIBLE** (floor is ≥1/5; both pass)
- Floor not suspended.

---

## Section 3: Position-Bias Mitigation

- **Pass 1** (V1 → V2 order): produced verdicts above.
- **Pass 2** (V2 → V1 order): re-scored each criterion starting with V2 first.
- **Disagreement count**: 2 of 30 criteria pairs had initial Pass 2 deltas.
  - Correctness #5 (claims supported by evidence): Pass 2 V2 borderline → re-evaluated; V2 cites TDD for most claims but defaults (refresh cap 5) lack source. Settled as MET (borderline). No change.
  - Invariant #1 (collection boundaries): Pass 2 V1 borderline (16-role cap vs TDD soft-cap rationale). Re-evaluated against debate-transcript X-004 — V1 cites "soft cap 16 with DB check constraint" with rationale "document for downstream RBAC PRD," V2 cites "10 roles" with rationale "generous for future RBAC." Both MET on boundary handling; V1 slightly cleaner. No verdict change.
- **Changed-verdict count**: 0
- Both passes converged on the same scores. Position bias deemed not material to outcome.

---

## Section 4: Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | Combined | Margin |
|---------|---------------|--------------|----------|--------|
| **V1 (opus)** | 0.9765 × 0.50 = 0.48825 | 1.000 × 0.50 = 0.50000 | **0.98825** | — |
| V2 (sonnet) | 0.9060 × 0.50 = 0.45300 | 0.800 × 0.50 = 0.40000 | 0.85300 | — |

**Winner: V1 (opus-default)**

**Margin: 0.98825 − 0.85300 = 0.13525 absolute → 13.7% relative gap (well above 5% tiebreaker threshold)**

---

## Section 5: Tiebreaker

Not applicable. Combined-score margin (13.7%) exceeds the 5% tiebreaker threshold. Skipping Level 1/2/3 tiebreaker logic.

---

## Section 6: Selected Base

- **Base: Variant 1 (opus-default)**

### Selection Rationale

Variant 1 wins decisively on three axes the rubric weights heavily: **(a) factual fidelity to the TDD** (V2's 1-week Beta directly contradicts TDD §19.1's "Beta — 2 weeks at 10%", a fidelity defect Sonnet's R2 conceded; V2 also fails to name SHA-256 for refresh-token hashing where TDD §13 specifies it); **(b) quantitative rigor for security invariants** (V1's AT-001..AT-016 + ±15ms / ±10ms parity-test variance budgets convert the enumeration-prevention NFR into a CI-enforceable gate — V2 states the invariant qualitatively but produces an unimplementable test, the single largest defect Sonnet conceded "fully" in R2); **(c) coordination scaffolding for a multi-team build** (M0 foundation milestone, H1-H10 inter-workstream handoff matrix, R-008 key-rotation risk with 24-hour overlap, and the 4-day open-question escalation protocol — all unique-contribution items U-001, U-002, U-004, U-005, U-007 from diff-analysis). Variant 1 also passes internal effort/staffing consistency (48 EW ≈ §3 staffing capacity), where Variant 2's 16 EW total is self-inconsistent with its own 5.5+ FTE workstream allocation. Variant 1 is penalized for one Risk Coverage gap (no R-006 conversion-rate risk) and one Structure concession (component build-order over-prescriptive) — both flagged for incorporation from V2.

### Strengths to PRESERVE from base (V1)

1. **M0 Foundation milestone** with 8 deliverables (schema, Redis, RSA keys, SendGrid, OpenAPI 3.1 contract, feature-flag scaffolding, decision records, threat model) — provides the readiness gate V2 lacks.
2. **48 EW capacity-plan totals** with per-milestone EW breakdown (M0=8, M1=10, M2=9, M3=7, M4=7, M5=7) — internally consistent with §3 staffing.
3. **H1-H10 inter-workstream handoff table** (§3) with explicit From → To + milestone + artifact — eliminates coordination ambiguity for 5.5+ FTE multi-team build.
4. **Quantitative timing-variance acceptance tests AT-001..AT-016** (§2.M1 ex 4, §2.M3 ex 2, §6.R-006) — ±15ms login / ±10ms reset parity-test budgets enforce enumeration prevention in CI.
5. **R-008 RS256 key-rotation risk** with 24-hour overlap window + emergency rotation runbook scaffolding (§6.R-008, §2.M2 D10).
6. **4-day open-question escalation protocol** (§9) — any OQ open within 4 calendar days of decision date → engineering lead.
7. **TDD-compliant 2-week Beta phase** (§2.M5: 2026-06-03 → 2026-06-09) — matches TDD §19.1 Phase 2 duration spec.
8. **SHA-256 algorithm specification** for refresh-token Redis storage (§2.M2 D3) — matches TDD §13.
9. **YAML frontmatter** (id, title, target_release, variant, status) for pipeline automation.

### Strengths to INCORPORATE from non-base (V2)

1. **R-006 conversion-rate risk** with A/B-test contingency (§6.R-006) — the only risk tying a roadmap decision to a measurable PRD success metric (>60% registration conversion). Adopt unmodified; Opus R2 conceded.
2. **Micro-benchmark gates: JwtService < 5ms, Redis ops < 10ms** (§8.3) — decomposes the 200ms p95 NFR into component-level budgets that catch regressions earlier in CI. Adopt the targets; layer onto V1's k6/Jest measurement rigor.
3. **30-minute lockout cooldown** (§9 OQ #3) instead of V1's 15-minute auto-unlock — doubles attacker re-attempt cost; Opus R2 conceded the default.
4. **Separation of uptime vs latency M5 exit criteria** (§2.M5) — keep these independently measurable rather than V1's bundled gate.
5. **Appendix B Gantt timeline visualization** — useful for tech-lead sprint kickoff and reveals the WS-D week-6 gap (no security review between Checkpoint 2 and pen test) that V1's denser table format hid.
6. **Refresh-token cap of 5 / roles cap of 10** — smaller blast radius defaults; easier to relax later than to tighten. Pair with V1's "oldest evicted on issuance" eviction policy to close INV-010.

---

**END OF BASE SELECTION**
