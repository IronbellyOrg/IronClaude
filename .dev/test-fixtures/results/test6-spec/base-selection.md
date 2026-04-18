---
base_variant: "roadmap-haiku-architect"
variant_scores: "A:71 B:76"
---

## 1. Scoring Criteria

Derived from the six debate divergences plus convergence assessment:

| # | Criterion | Weight | Source |
|---|---|---|---|
| C1 | Phase boundary justification | 12 | Divergence 1: phase count |
| C2 | Component granularity fit | 15 | Divergence 2: 7 vs 15 components |
| C3 | Testing timing correctness | 15 | Divergence 3: dedicated vs distributed |
| C4 | Priority classification accuracy | 10 | Divergence 4: password reset P0/P1 |
| C5 | Security completeness | 15 | Divergences 5+6, Haiku rebuttal on cookie/CORS/config |
| C6 | Deployment actionability | 10 | Divergence 6: 5 tasks vs 2+runbook |
| C7 | Timeline realism | 10 | Round 2: 14-19d vs 17-21d |
| C8 | Task referenceability | 8 | Opus global numbering vs Haiku per-phase reset |
| C9 | Spec fidelity | 5 | Both claim 22 SC, 6 risks, 6 OQs |

## 2. Per-Criterion Scores

| Criterion | Variant A (Opus) | Variant B (Haiku) | Justification |
|---|---|---|---|
| C1 Phase boundaries (12) | 7 | 9 | Haiku's rebuttal landed: Phase 0 contains trivial tasks (DEP-1: "install npm package", effort S). A 2-3 day phase with 11 tasks including package installs is padding, not a meaningful gate. JwtService constructor failure surfaces key issues without a phase boundary. However, Opus's explicit infrastructure checkpoint has value for teams >3 people. |
| C2 Component granularity (15) | 8 | 10 | Haiku wins on security-sensitive components. Opus has zero explicit tasks for cookie configuration, CORS, or boot-time config validation — these are OWASP-relevant failure modes. SecretsProvider, AuthCookiePolicy, AuthConfig are not over-engineering; they're explicit attention to common production failures. Opus's rebuttal that AuthCookiePolicy is "10-15 lines" doesn't negate that those lines deserve explicit AC and testing. Deducting from Haiku: AuthFeatureGate as a standalone component is marginal. |
| C3 Testing timing (15) | 9 | 11 | Haiku's rebuttal was decisive: Opus implements AuthService in Phase 2 but defers AuthService unit tests (TEST-004) to Phase 3 — a 4-5 day gap. Haiku places TEST-002 (auth service unit tests) in Phase 3 immediately after Phase 2 implementation, with route integration tests in the same phase. Opus does test crypto primitives earlier (Phase 1), which is correct. Neither variant is perfect; the ideal is Opus's early crypto tests + Haiku's co-located service tests. |
| C4 Priority accuracy (10) | 6 | 8 | Password reset as P0 (Haiku) is the stronger default for a production auth system. Opus's P1 argument ("ship faster, manual reset covers the gap") is valid for internal tools but weak for user-facing products. The debate correctly flags this as a product-owner decision, but Haiku's default is safer. Opus's admin-endpoint fallback is unspecified in the roadmap itself — it's an argument, not a deliverable. |
| C5 Security completeness (15) | 9 | 13 | Haiku explicitly covers: cookie security config (COMP-015), CORS policy, config validation at boot (COMP-013), migration recovery drills (TEST-005). Opus has none of these as explicit tasks. Opus's lockout policy (OPS-007, P2) is a reasonable interim measure, but Haiku's argument that building unapproved security policy is worse than deferring has merit. Rate limiting at 5/min/IP (both variants) covers v1 brute-force. Net: Haiku's explicit security surface coverage is materially better. |
| C6 Deployment actionability (10) | 9 | 6 | Opus wins clearly. Five granular deployment tasks (runbook, 10% canary, SC validation, full rollout, key rotation) vs Haiku's two tasks + a P2 doc. Haiku's DOC-001 is P2 while OPS-005 (execute rollout) is P0 — a dependency inversion Opus correctly identified. "Execute feature-flag rollout plan" is hand-waving without specifying canary percentage, success criteria, or monitoring duration. |
| C7 Timeline realism (10) | 6 | 9 | Opus's 14-day lower bound requires infrastructure + schema + three crypto modules + nine test suites in 5-7 days (Phase 0+1). Haiku's 17-day lower bound allocates 4-5 days for the merged foundation phase alone, better reflecting secrets manager integration delays and native addon compilation. The debate's synthesis recommended Haiku's timeline as the planning baseline. |
| C8 Task referenceability (8) | 7 | 5 | Opus uses global sequential numbering (1-52), making cross-phase references unambiguous. Haiku resets numbering per phase, so "task 1" is ambiguous without phase context. Both use ID-based references (COMP-001, TEST-002), but Opus's global # column aids sprint planning and standup communication. |
| C9 Spec fidelity (5) | 4 | 5 | Both achieve 22 SC, 6 risks, 6 OQs. Haiku maps SC validation to specific test IDs more consistently. Opus's SC table is cleaner but validation phases are less precise ("Phase 2" vs Haiku's "Phase 2-3" ranges). Minor edge to Haiku for traceability. |

## 3. Overall Scores

| Variant | Raw Score | /100 | Justification |
|---|---|---|---|
| A (Opus) | 65/100 | **71** (normalized) | Stronger deployment specificity, better task numbering, clean executive summary. Weakened by absent cookie/CORS/config tasks, AuthService unit test gap, and optimistic timeline. |
| B (Haiku) | 76/100 | **76** (normalized) | Stronger security coverage, better testing co-location, more realistic timeline. Weakened by vague deployment tasks, per-phase numbering reset, and DOC-001 dependency inversion. |

## 4. Base Variant Selection Rationale

**Selected base: Variant B (Haiku)**

Haiku is the stronger base because:

1. **Security surface coverage is the hardest to retrofit.** Adding COMP-013 (AuthConfig), COMP-015 (AuthCookiePolicy), and TEST-005 (migration drills) to Opus would require restructuring phases. In Haiku, these already exist with explicit AC.
2. **Testing co-location is architecturally correct.** The 4-5 day gap between AuthService implementation and its unit tests in Opus is a real risk for security code. Haiku's structure avoids this.
3. **Timeline is the planning baseline.** Per the debate's own synthesis, Haiku's 17-21d estimate is more realistic.
4. **Component boundaries are production-informed.** SecretsProvider, UserRepository, and RefreshTokenRepository as explicit components with file paths create a testable, injectable architecture that Opus leaves implicit.

Opus's strengths (deployment granularity, global numbering) are additive improvements that can be merged into Haiku's structure without restructuring.

## 5. Improvements to Incorporate from Variant A (Opus)

| # | Improvement | Source (Opus) | Target (Haiku location) | Rationale |
|---|---|---|---|---|
| 1 | Replace OPS-005 with 5 granular deployment tasks | Opus Phase 4: OPS-008 through OPS-012 | Haiku Phase 4: replace OPS-005 + elevate DOC-001 | Eliminates dependency inversion; specifies canary %, success criteria, monitoring window |
| 2 | Add global sequential task numbering | Opus # column (1-52) | All Haiku phases: add cumulative # column | Unambiguous cross-phase references for sprint planning |
| 3 | Add crypto primitive tests to Phase 1 | Opus Phase 1: TEST-001, TEST-002, TEST-003 | Haiku Phase 1: add after COMP-003/COMP-004 | Validates PasswordHasher and JwtService before TokenManager depends on them; Opus was correct that earlier crypto testing is better |
| 4 | Promote DOC-001 from P2 to P1 | Opus OPS-008 (runbook) is P0 | Haiku Phase 4: DOC-001 → P1 minimum | Deployment runbook must exist before rollout execution |
| 5 | Add RSA key rotation schedule task | Opus OPS-012 | Haiku Phase 4: after OPS-004 | Opus's explicit 90-day rotation task with dual-key overlap and zero-downtime testing is more actionable than Haiku's OPS-004 which only "defines" the procedure |
| 6 | Adopt Opus's integration points table format | Opus per-phase tables | Haiku per-phase tables | Opus includes "Consumed By" cross-references more consistently; adopt for traceability |
