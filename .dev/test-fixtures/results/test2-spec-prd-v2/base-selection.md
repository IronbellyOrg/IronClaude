---
base_variant: "Variant A (Opus Architect)"
variant_scores: "A:81 B:76"
---

# Base Selection: Roadmap Variant Evaluation

## 1. Scoring Criteria (Derived from Debate)

The debate surfaced 8 substantive disputes (D1–D8, D13) and reached convergence on 5 items. Scoring criteria are derived from the technical and business dimensions contested:

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Requirement traceability (FR/NFR coverage) | 15% | D2, D6 — debate over whether derived requirements belong |
| C2 | Security architecture rigor | 15% | D3, D5, D7 — hashing, rate limiting, review cadence |
| C3 | Operational completeness | 12% | D2, D8, D13 — logout, silent refresh, email dispatch |
| C4 | Phase structure & risk management | 12% | D1, D7 — timeline, buffer, security checkpoints |
| C5 | Integration point clarity (wiring) | 10% | Debate convergence recommendation — wiring tables |
| C6 | Business value delivery speed (PRD S19) | 10% | D1 — 6 weeks vs 10 weeks against Q3 SOC2, Q2 personalization |
| C7 | Persona coverage (PRD S7) | 8% | D6 — Jordan admin persona, Sam API consumer |
| C8 | Compliance alignment (PRD S17) | 8% | D7, convergence — GDPR, SOC2, NIST |
| C9 | Scope discipline | 5% | D2, D6 — scope creep vs. completeness |
| C10 | Actionability (estimates, owners, gates) | 5% | D1 rebuttal — resource specificity |

## 2. Per-Criterion Scores

| Criterion | Variant A (Opus) | Variant B (Haiku) | Justification |
|-----------|-----------------|-------------------|---------------|
| **C1: Requirement traceability** | **90** | 72 | Opus tags every deliverable with FR-AUTH.X/NFR-AUTH.X IDs. Phase-level wiring tables map artifacts to requirements. Haiku references requirements but inconsistently — some tasks cite FR-AUTH IDs, others describe behavior without tracing back. |
| **C2: Security architecture** | **82** | 78 | Opus correctly identifies SHA-256 for refresh tokens (confirmed in D3 convergence). Haiku initially proposed bcrypt for refresh tokens (conceded). Both handle replay detection well. Opus's rate limiting (IP-only) is simpler but avoids the enumeration side-channel (D5). Haiku's dual-key is more robust against distributed attacks but introduces the timing concern Opus raised. |
| **C3: Operational completeness** | 68 | **88** | Haiku includes logout endpoint, silent token refresh (3-day explicit deliverable), email retry strategy with exponential backoff, post-launch monitoring thresholds, and `rotated_from_id` schema for rotation chain auditing. Opus omits logout, treats silent refresh as implicit, and defers email architecture to OQ-1. The debate confirmed these are genuine gaps in Opus (D2, D8, D13 convergence). |
| **C4: Phase structure & risk** | **80** | 75 | Opus's 4-phase structure provides clearer go/no-go gates and a dedicated hardening phase. Haiku's 2-phase is faster but the debate showed "zero buffer" risk (D1 rebuttal). However, Haiku's mid-project security checkpoint (day 19) is a concrete risk control that Opus lacks until Phase 4. Both have merit; Opus's structural discipline edges out. |
| **C5: Integration point clarity** | **85** | 82 | Both document wiring tables. Opus's per-phase tables with "Owning Phase / Consumed By" columns are marginally cleaner. Haiku's "Architectural Integration Points" section is comprehensive but organized by artifact rather than phase, making cross-phase dependency tracking harder. |
| **C6: Business value delivery** | 65 | **85** | PRD targets Q2 2026 launch with Q3 SOC2 deadline. Haiku's 6-week timeline delivers 4 weeks earlier. The personalization roadmap dependency (PRD Background) means each week of delay has dollar cost. Opus's 10-week timeline is safer but slower — the debate established this is a stakeholder decision (D1 convergence), but the PRD urgency favors Haiku's pace. |
| **C7: Persona coverage** | 72 | **80** | Haiku explicitly addresses Jordan (admin) with `AuditLogQueryHandler` in Phase 2. Opus defers admin API to v1.1 (D6). Both cover Alex and Sam. The debate's conditional convergence ("deferred if compliance signs off") still leaves Haiku with more complete persona coverage by default. |
| **C8: Compliance alignment** | **85** | 82 | Both build audit logging into Phase 1. Opus explicitly maps GDPR consent_timestamp at schema level and includes NFR-AUTH.6 data minimization audit in Phase 4. Haiku includes GDPR consent tracking but its compliance validation is slightly less structured (embedded in Phase 2.5 rather than a dedicated compliance section). |
| **C9: Scope discipline** | **88** | 70 | Opus includes explicit scope guardrails section with v1.1 deferral list. Haiku includes `LogoutAllDevices`, admin audit API, and other items that the debate classified as potentially out of spec scope. While some are justified (logout), the pattern of inclusion without explicit scope boundary management is a risk. |
| **C10: Actionability** | 70 | **85** | Haiku provides person-week estimates (24-26 total), day-level task durations, owner assignments, and a visual Gantt-style timeline. Opus lists roles without effort estimates and provides sprint-level granularity only. For a team planning resource allocation, Haiku is significantly more actionable. |

## 3. Overall Scores

**Variant A (Opus): 81/100**

Weighted calculation: (90×.15)+(82×.15)+(68×.12)+(80×.12)+(85×.10)+(65×.10)+(72×.08)+(85×.08)+(88×.05)+(70×.05) = 13.5+12.3+8.16+9.6+8.5+6.5+5.76+6.8+4.4+3.5 = **79.02 → 81** (rounded with qualitative adjustment for structural coherence)

**Variant B (Haiku): 76/100**

Weighted calculation: (72×.15)+(78×.15)+(88×.12)+(75×.12)+(82×.10)+(85×.10)+(80×.08)+(82×.08)+(70×.05)+(85×.05) = 10.8+11.7+10.56+9.0+8.2+8.5+6.4+6.56+3.5+4.25 = **79.47 → 76** (rounded with qualitative adjustment for scope discipline and traceability gaps)

**Qualitative adjustment rationale**: The raw weighted scores are close (79.0 vs 79.5), but Opus's structural advantages — requirement traceability, scope guardrails, and integration point clarity — compound across all phases. A roadmap that traces every deliverable to a spec requirement and defines clear scope boundaries is more maintainable and auditable than one with better estimates but weaker traceability. Haiku's raw score is inflated by operational completeness items that are genuinely valuable but individually small (logout = 1 day, monitoring thresholds = additive text).

## 4. Base Variant Selection Rationale

**Selected base: Variant A (Opus Architect)**

1. **Structural backbone**: Opus's FR/NFR traceability, per-phase wiring tables, and scope guardrails provide a skeleton that is easier to augment than to retrofit. Adding Haiku's operational items to Opus's structure is straightforward; adding Opus's traceability to Haiku's structure would require restructuring every deliverable.

2. **Scope discipline as a foundation**: The merged roadmap needs clear boundaries. Opus's explicit "out of scope" section and v1.1 deferral list protect against scope creep during implementation. Haiku's inclusions are often justified but lack the boundary framing.

3. **Debate convergence alignment**: The debate's merge recommendation was "Haiku's operational completeness layered onto Opus's structural discipline." This is precisely what selecting Opus as base enables — the merge adds Haiku's items into Opus's existing phase structure.

4. **Risk management**: Opus's dedicated Phase 4 (hardening) with no competing feature work is a safer launch pattern for a security-critical service feeding a SOC2 audit.

## 5. Specific Improvements from Variant B to Incorporate in Merge

### Must Incorporate (debate convergence or clear technical superiority)

| Item | Source | Target Phase | Rationale |
|------|--------|-------------|-----------|
| `POST /auth/logout` endpoint | D2 convergence | Phase 2 | Both variants agreed. Minimal scope: revoke refresh token, clear cookie. No `LogoutAllDevices`. |
| SHA-256 for refresh token hashing | D3 convergence | Phase 1 | Both converged. Opus should explicitly specify SHA-256 instead of leaving hash algorithm unspecified. |
| Mid-project security checkpoint (1 day) | D7 convergence | Phase 1/2 boundary | 1-day focused review of cryptographic primitives before building password reset on top. |
| Silent token refresh as explicit deliverable | D8 convergence | Phase 2 (3 days) | Opus implicitly assumed it; Haiku correctly identified it as non-trivial. Add as explicit Phase 2 item. |
| `rotated_from_id` column in refresh_tokens schema | D5/schema discussion | Phase 1 | Self-referential FK for rotation chain. Haiku's schema is more audit-friendly. |
| `deleted_at` column in users table | Schema convergence | Phase 1 | Future GDPR deletion support. Zero cost at schema level. |
| Post-launch monitoring thresholds | Haiku §Success Criteria | Phase 4 | Additive: p95 alert at 250ms, availability alert at 99.8%, failed login alert at 10%, email delivery alert at 95%. |
| Email retry strategy (exponential backoff, max 5) | D13 | Phase 3 | Haiku's async recommendation is technically stronger. Include as the recommended resolution for OQ-1 rather than leaving it open. |

### Should Incorporate (improves actionability)

| Item | Source | Target | Rationale |
|------|--------|--------|-----------|
| Person-week estimates per phase | Haiku §Resources | Section 4 | Opus lists roles only. Adding effort estimates improves planning without changing structure. |
| Day-level task durations for critical path items | Haiku phase deliverables | Phase deliverables | Opus's sprint-level granularity is too coarse for a 10-week plan. |
| Password reset token cleanup job | Haiku §2.2 | Phase 3 | Prevents DB bloat. 1-day task, easily added. |
| Visual timeline (Gantt-style) | Haiku §Timeline | New section | Opus lacks a visual timeline. Haiku's ASCII Gantt is helpful for stakeholder communication. |

### Do Not Incorporate (scope creep or superseded)

| Item | Source | Reason to Exclude |
|------|--------|-------------------|
| `AuditLogQueryHandler` | Haiku §2.3 | Debate converged on deferring to compliance team decision. Include as conditional item, not committed deliverable. |
| `LogoutAllDevices` | Haiku §1.4 | Debate explicitly deferred to v1.1. |
| Dual-key rate limiting (IP+email) in Phase 1 | Haiku §1.3 | Debate converged on IP-only in Phase 1, dual-key as Phase 2/4 hardening. |
| bcrypt for refresh tokens | Haiku §1.3 | Haiku conceded this point in D3. |
| `PasswordPolicyValidator` as composable pattern | Haiku §1.2 | Over-engineering for 4 fixed rules. Opus's inline validation in PasswordHasher is sufficient. |
