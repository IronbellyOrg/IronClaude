# Base Selection: Hybrid Scoring

## Metadata

- Variants: V1 (opus-architect, 484 lines), V2 (sonnet-architect, 450 lines)
- Source requirements basis: AUTH-MERGED-PRD-TDD (FR-AUTH-001..005, NFR-PERF-001/002, NFR-SEC-001/002, NFR-AUTH.3, NFR-REL-001 + PRD/TDD section references)

---

## Quantitative Scoring (50% weight)

### Per-metric scores

| Metric (weight) | V1 (Opus) | V2 (Sonnet) | Computation Note |
|---|---|---|---|
| Requirement Coverage RC (0.30) | 0.90 | 0.94 | Both cover all FR-AUTH-001..005, NFR-*. V2 edges via explicit admin endpoint (PRD FR-AUTH.5 admin AC), explicit auto-login (PRD Signup Flow), GDPR consent UI. V1 defers admin AC to v1.1. |
| Internal Consistency IC (0.25) | 0.95 | 0.93 | V1: minor friction on Redis-in-M1 acknowledged + justified. V2: in-row lockout counter race not addressed in original (per INV-009/INV-013); admin endpoint × RBAC-out-of-scope contradiction (INV-004). |
| Specificity Ratio SR (0.15) | 0.90 | 0.88 | Both highly concrete with bcrypt cost 12, RS256 2048-bit, 5-attempt/15-min, p95<200ms. V1 edges via explicit implementation mechanisms (dummy-hash, always-enqueue) vs V2's outcome-only ACs. |
| Dependency Completeness DC (0.15) | 0.95 | 0.95 | All internal M*/D*.X/R-NNN refs resolve in both. |
| Section Coverage SC (0.15) | 1.00 | 0.857 | V1: 7 H2 sections (incl. Sequencing Rationale). V2: 6 H2 sections. Normalized by max=7. |

### Quant subtotal

```
V1 quant = (0.90×0.30) + (0.95×0.25) + (0.90×0.15) + (0.95×0.15) + (1.00×0.15)
        = 0.270 + 0.2375 + 0.135 + 0.1425 + 0.150 = 0.935

V2 quant = (0.94×0.30) + (0.93×0.25) + (0.88×0.15) + (0.95×0.15) + (0.857×0.15)
        = 0.282 + 0.2325 + 0.132 + 0.1425 + 0.1286 = 0.918
```

---

## Qualitative Scoring (50% weight) — 30-criterion CEV Rubric

Dual-pass position-bias mitigation: pass-1 (V1→V2), pass-2 (V2→V1) yielded identical verdicts on all 30 criteria (binary objective rubric).

### Completeness (5/5 both)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| C1 | Covers all explicit requirements | MET (FR-AUTH-001..005 + NFR-* traced) | MET (same + admin AC) |
| C2 | Addresses edge cases / failure scenarios | MET (timing oracle, lockout race, refresh-token replay) | MET (concurrent registration, Redis failover, tab refresh race) |
| C3 | Dependencies / prerequisites | MET (PG/Redis/SendGrid/Vault) | MET (same set) |
| C4 | Success/completion criteria | MET (per-M ACs + overall DoD) | MET (same structure) |
| C5 | Out-of-scope specified | MET (Scope (out) per M) | MET (Out per M) |

### Correctness (V1: 3/5, V2: 3/5)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| Cor1 | No factual errors | MET | MET |
| Cor2 | Technical approaches feasible | MET (Redis INCR atomic by default) | NOT MET (PG-column lockout requires atomic-UPDATE or FOR UPDATE; D1.1/D2.1 don't specify — race-prone as written; surfaced by INV-009/INV-013) |
| Cor3 | Terminology consistent | MET | MET |
| Cor4 | No internal contradictions | NOT MET (INV-014: dummy-hash defense creates new oracle vs locked-account fast-reject — V1 line 66) | NOT MET (INV-004: admin endpoint requires admin role, but RBAC enforcement out-of-scope V2 L308) |
| Cor5 | Claims supported by evidence/rationale | MET (Sequencing Rationale section + risk reasoning) | MET (traceability column) |

### Structure (5/5 both)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| S1 | Logical section ordering | MET | MET |
| S2 | Consistent hierarchy depth | MET | MET |
| S3 | Clear separation of concerns | MET | MET (cleaner via 6-milestone separation) |
| S4 | Navigation aids | MET (inline TDD §/PRD § cross-refs) | MET (traceability column per deliverable) |
| S5 | Follows artifact conventions | MET | MET |

### Clarity (5/5 both)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| Cl1 | Unambiguous language | MET (no "as appropriate") | MET |
| Cl2 | Concrete vs abstract | MET (explicit dummy-hash mechanism) | MET (concrete deliverable tables) |
| Cl3 | Section purpose clear | MET | MET |
| Cl4 | Acronyms defined | MET | MET |
| Cl5 | Actionable next steps | MET | MET |

### Risk Coverage (5/5 both)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| R1 | ≥3 risks with prob/impact | MET (10 risks R-001..R-010) | MET (8 risks RR-1..RR-8) |
| R2 | Mitigation strategy per risk | MET | MET |
| R3 | Failure modes and recovery | MET (TDD §25.1 scenarios) | MET (RR-5 Redis runbook) |
| R4 | External dependencies failure | MET (R-005 SendGrid) | MET (RR-4 SendGrid) |
| R5 | Monitoring/validation mechanism | MET (alerts at >20% failure, p95>500ms) | MET |

### Invariant & Edge Case Coverage (V1: 4/5, V2: 2/5)

| # | Criterion | V1 | V2 |
|---|-----------|----|----|
| I1 | Boundary conditions for collections | MET (R-006 audit-log unbounded growth) | MET (RR-3 partition at 10M rows) |
| I2 | State variable interactions across boundaries | MET (D1.4 lockout state machine; Sequencing Rationale on contract-freeze interaction) | NOT MET (column-based state with race; INV-009 unaddressed) |
| I3 | Guard condition gaps | NOT MET (INV-014: V1 L66 introduces new timing oracle) | NOT MET (no explicit mechanism for constant-time; "<50ms variance" AC only) |
| I4 | Count divergence scenarios | MET (R-008 lockout counter race explicit) | NOT MET (in-row counter race unaddressed) |
| I5 | Interaction effects | MET (Sequencing Rationale: M2 contract freeze × M4 parallel; lockout-Redis × M2 boundary) | NOT MET (admin-endpoint × RBAC interaction unaddressed; reset audit-log × admin query interaction unaddressed) |

### Edge Case Floor Check

- V1 Invariant score: 4/5 ✓ (above 1/5 floor)
- V2 Invariant score: 2/5 ✓ (above 1/5 floor)
- **Both variants eligible as base.**

### Qualitative Subtotals

```
V1 qual = (5 + 3 + 5 + 5 + 5 + 4) / 30 = 27/30 = 0.900
V2 qual = (5 + 3 + 5 + 5 + 5 + 2) / 30 = 25/30 = 0.833
```

---

## Position-Bias Mitigation

Dual-pass evaluation: pass-1 (input order V1→V2) and pass-2 (reverse V2→V1) executed in parallel. All 30 criteria yielded identical verdicts on both passes (binary objective rubric on textual artifacts is insensitive to evaluation order). No criterion required re-evaluation; no verdicts changed.

---

## Combined Scoring

```
V1 = (0.50 × 0.935) + (0.50 × 0.900) = 0.4675 + 0.4500 = 0.9175
V2 = (0.50 × 0.918) + (0.50 × 0.833) = 0.4590 + 0.4165 = 0.8755

Margin: 0.9175 − 0.8755 = 0.0420 = 4.20%
```

**Within 5% tiebreaker threshold → tiebreaker fires.**

---

## Tiebreaker Protocol

### Level 1: Debate Performance (points won in Step 2 scoring matrix)

Counting from `debate-transcript.md` per-point scoring:

- V1 outright wins (5 points): S-003, C-004, C-005, C-006, X-004
- V1 contested wins (2 points): A-003, A-007
- V2 outright wins (8 points): S-001, S-002, S-004, C-002, C-007, C-008, X-001, X-005
- Hybrid (split 0.5/0.5, 4 points): C-001, C-003, X-002, X-003 → V1 gets 2, V2 gets 2
- Resolved-mutual (5 points): A-001, A-002, A-004, A-005, A-006 → V1 gets 2.5, V2 gets 2.5

```
V1 debate score: 5 + 2 + 2.0 + 2.5 = 11.5
V2 debate score: 8 + 0 + 2.0 + 2.5 = 12.5
```

**V2 wins on debate performance (12.5 vs 11.5).**

Tiebreaker resolved at Level 1; Levels 2 and 3 not invoked.

---

## Selected Base: Variant 2 (Sonnet — sonnet-architect)

### Selection Rationale

V2's combined score (0.876) is within the 4.2% tiebreaker margin of V1's (0.918). The tiebreaker resolves in V2's favor on debate performance — V2 won 12.5 of the 24 diff-point contests vs V1's 11.5. V2's strengths are *structural and scope-completeness*: the 6-milestone scaffold separates infrastructure from auth logic cleanly, the traceability tables are SOC2-auditor-friendly, and V2 ships three deliverables V1 defers (admin audit endpoint, concurrent-registration AC, auto-login at registration) that directly satisfy PRD requirements.

However, V1 won the qualitative dimension overall (0.900 vs 0.833), particularly on Invariant & Edge Case Coverage (4/5 vs 2/5). The merged roadmap MUST adopt V1's security-depth contributions — constant-time mechanisms, Sequencing Rationale, OQ-7 retention conflict surfacing, Redis-counter atomicity reasoning — even though V2 is the structural base.

### Strengths to Preserve from Base (V2)

1. **6-milestone scaffold** (M1 infrastructure / M2 auth core / M3 token lifecycle / M4 password reset+admin / M5 frontend / M6 rollout) — keeps M1 lean and gates infra readiness before service logic.
2. **Traceability column format** per deliverable table — auditable source-tracking that V1's inline `(TDD §x.y)` citations don't match.
3. **Admin audit-log endpoint D4.7** — `GET /admin/audit-logs?user_id=&event_type=&from=&to=` satisfies PRD FR-AUTH.5 admin AC.
4. **Concurrent-registration AC #9** — explicit testable AC for DB-unique-constraint race.
5. **Explicit auto-login on registration D2.2** — captures PRD Signup Flow's "submit → logged in" precisely.
6. **SendGrid deliverability hardening** — SPF/DKIM/DMARC pre-warming + Gmail/Outlook spam-folder testing.
7. **Reset tokens in Redis with 1-hour TTL** — self-cleaning ephemeral storage, no cron purge needed.
8. **API Gateway rate limits as IaC** (Terraform/Pulumi) — environment parity.

### Strengths to Incorporate from V1

1. **Sequencing Rationale section** (V1 L476–484) — adopt verbatim as final section of merged roadmap.
2. **Constant-time login defense** (V1 L66, L87) — explicit "run `PasswordHasher.verify` against constant dummy hash on miss" pattern as M2 deliverable + AC.
3. **Constant-time reset defense** (V1 L218) — explicit "always enqueue email job (drop in worker if unregistered)" pattern as M4 deliverable + AC.
4. **OQ-7 PRD-vs-TDD retention conflict** (V1 L462) — surface as OQ with proposed split-tables resolution; commit M1 schema to support it without destructive migration (INV-002 fix).
5. **Lockout atomicity** (V1 L86) — require atomic counter semantics regardless of storage backend; in V2's PG-columns approach, mandate `UPDATE users SET failed_login_count = failed_login_count + 1, locked_until = CASE WHEN failed_login_count + 1 >= 5 THEN NOW() + INTERVAL '15 minutes' ELSE locked_until END WHERE email = $1 RETURNING ...` (single-statement atomic).
6. **Quarterly RS256 key-rotation runbook + drill** (V1 D2.7, D5.7) — schedule + first drill in M5.
7. **Pen-test split** (V1 + V2 R2 compromise) — backend pen-test late M4, frontend pen-test M5 Week 1.
8. **Per-email rate limit + per-IP** (A-004 resolution) — per-email is the authoritative anti-brute-force control; per-IP is secondary guardrail.
9. **15-minute residual access-token exposure window documented** (V1 L156) — denylist deferred to v1.1 with explicit SOC2 risk acceptance.
10. **Performance Budgets table including `/auth/me`** (V1 L388–399).

### Must-Address Invariant Items (from Round 2.5)

Promoted from `invariant-probe.md` as REFACTOR-MUST items:

- INV-014: Lockout-rejected response timing must match dummy-hash verify path (no fast-reject).
- INV-004: Either drop admin endpoint to v1.1, OR add minimal `isAdmin` JWT claim + admin-emails seed in M1 (recommend the latter to keep V2's PRD-completeness win).
- INV-009: Resolve C-001 atomicity (PG atomic-UPDATE adopted; specify in M2 D2.1).
- INV-007: Worker must emit audit row for dropped (unregistered) reset requests so audit-log absence ≠ unregistered.
- INV-012: Isolate BullMQ queue on separate Redis instance (or explicit memory-budget per key namespace).
- INV-001: Dummy hash seeded at build/deploy time as config constant (not per-pod boot-time hash).
- INV-002: M1 audit-log schema includes optional `soc2_relevant BOOLEAN` flag to enable M5 split-tables-view without destructive migration.
- INV-005: Sliding-window lockout via Redis sorted-set of failure timestamps OR explicit AC that lockout-rejected response time matches dummy-verify regardless of window state.

---

## Final Disposition

- **Base variant**: V2 (sonnet-architect)
- **Tiebreaker applied**: Yes — Level 1 (debate performance, V2: 12.5 vs V1: 11.5)
- **Convergence status**: BLOCKED_BY_INVARIANTS (gate failure — 8 HIGH UNADDRESSED)
- **Return contract status**: `partial` (force-selected base, unaddressed invariants flagged)
- **Merged output**: scaffold from V2 + security-depth from V1 + invariant fixes from probe
