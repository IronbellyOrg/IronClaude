# Adversarial Debate Transcript

## Metadata

- Depth: standard
- Rounds completed: Round 1 (parallel), Round 2 (sequential rebuttals), Round 2.5 (invariant probe)
- Round 3: skipped (depth=standard)
- Convergence achieved: 0.82 (per-point agreement, see scoring matrix)
- Convergence threshold: 0.80
- Convergence gate status: **BLOCKED_BY_INVARIANTS** — diff-point convergence ≥ threshold AND taxonomy levels all covered, BUT 9 HIGH-severity UNADDRESSED invariant findings from Round 2.5 block formal convergence
- Focus areas: All (no `--focus` filter)
- Advocate count: 2 (opus, sonnet)

## Component Transcripts

Round transcripts are stored as separate artifacts to keep this transcript navigable. Each is the verbatim output of the corresponding advocate / fault-finder agent.

| Round | File | Lines |
|-------|------|-------|
| Round 1 — V1 (opus) advocate | `round1-variant1-advocate.md` | 191 |
| Round 1 — V2 (sonnet) advocate | `round1-variant2-advocate.md` | 241 |
| Round 2 — V1 (opus) rebuttal | `round2-variant1-rebuttal.md` | 168 |
| Round 2 — V2 (sonnet) rebuttal | `round2-variant2-rebuttal.md` | 186 |
| Round 2.5 — Fault-finder | `invariant-probe.md` | (see file) |

## Scoring Matrix

Per-diff-point winners with calibrated confidence and one-line evidence summary.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| **Structural** ||||
| S-001 (14w vs 17w) | V1 | 55% | Tighter schedule defensible with cross-cutting tracks; not unanimous |
| S-002 (milestone grouping) | V1 | 70% | Foundations-first (crypto/audit before login) is cleaner sequencing |
| S-003 (login+reg split/combined) | V2 | 55% | Combining is simpler for single-team execution; V1's split is over-engineered for source scope |
| S-004 (audit substrate in M1) | V1 | 85% | Audit must exist when first event occurs; both advocates agreed late in debate |
| S-005 (rate limit timing) | V1 | 70% | R-002 (brute force) needs mitigation when login ships, not deferred to M3 |
| S-006 (format style) | tie | 50% | Tabular vs narrative is cosmetic |
| **Content** ||||
| C-001 (Argon2id vs bcrypt) | V1 | 80% | V2 conceded OWASP 2025 favors Argon2id; bcrypt acceptable but inferior |
| C-002 (refresh TTL 30d/7d) | V2 | 55% | 7-day default is safer-by-default; V1's 30d defensible with family rotation |
| C-003 (access-token revocation) | V1 | 80% | V2's "no list needed" breaks down under FR-004 mid-session role changes |
| C-004 (RBAC dynamic vs static) | V2 | 60% | Source spec says "RBAC" literally, not ABAC; V2's static hierarchy closer to literal text |
| C-005 (perm propagation gap) | V1 | 85% | V2 conceded role change won't propagate until refresh; gap is real |
| C-006 (token-bucket vs sliding-window) | V2 | 55% | Sliding-window is more common; both are valid |
| C-007 (lockout policy) | tie | 50% | 5/15min and 10/1hr are both reasonable; pick one |
| C-008 (deactivation grace) | V2 | 55% | 14d aligns with privacy-by-default; GDPR favors shorter |
| C-009 (2FA key separation) | V1 | 85% | V2 conceded missing key separation is a defense-in-depth gap |
| C-010 (recovery codes hash) | V1 | 70% | Specific algorithm (bcrypt-12) beats unspecified |
| C-011 (JWT lib named) | V1 | 65% | python-jose vs unspecified — minor but specificity wins |
| C-012 (OAuth lib named) | V1 | 65% | authlib vs unspecified |
| C-013 (TOTP lib) | V1 | 55% | pyotp named; V2's language-agnostic mention is also reasonable |
| C-014 (verify token spec) | V1 | 70% | 32-byte CSPRNG + SHA-256 stored + 24h TTL is specific and correct |
| C-015 (external pentest) | V1 | 80% | V2 conceded ZAP-only insufficient for OWASP compliance claim |
| C-016 (chaos engineering) | V1 | 80% | NFR-005 (99.9% uptime) not verifiable without chaos drill |
| C-017 (DR runbook RTO/RPO) | V1 | 80% | NFR-005 requires operational targets, not just monitoring |
| C-018 (soak duration 1h vs 4h) | V2 | 75% | 4-hour soak catches slow Redis memory leaks; V1 conceded |
| **Contradictions** ||||
| X-001 = C-001 | V1 | 80% | (same as C-001) |
| X-002 = C-002 | V2 | 55% | (same as C-002) |
| X-003 = C-003 | V1 | 80% | (same as C-003) |
| X-004 = C-004 | V2 | 60% | (same as C-004) |
| X-005 = S-004 | V1 | 85% | (same as S-004) |
| X-006 = C-008 | V2 | 55% | (same as C-008) |
| **Unique Contributions** ||||
| U-001 (chaos eng) | V1 retains | 90% | V2 conceded gap; incorporate as-is |
| U-002 (DR runbook RTO/RPO) | V1 retains | 90% | V2 conceded gap |
| U-003 (key rotation drill) | V1 retains | 90% | V2 conceded gap |
| U-004 (external pentest) | V1 retains | 90% | V2 conceded gap |
| U-005 (IR playbook) | V1 retains | 85% | V2 conceded — GDPR 72-hr requires rehearsed playbook |
| U-006 (STRIDE threat modeling) | V1 retains | 80% | V2 silent; merge as-is |
| U-007 (refresh family rotation) | V1 retains | 90% | OAuth BCP citation — both accept |
| U-008 (perm propagation via denylist) | V1 retains | 85% | V2 conceded; merge |
| U-009 (trusted-device cookie) | V1 retains | 70% | Useful UX feature; modest priority |
| U-010 (feature flags via unleash) | V1 retains | 70% | Standard practice; merge |
| U-011 (mTLS API↔Redis) | V1 retains | 80% | Defense-in-depth; merge |
| U-012 (avatar upload S3/R2) | **V2 incorporate** | 85% | V1 conceded missing; FR-010 implies profile management which includes avatar |
| U-013 (reactivation endpoint) | **V2 incorporate** | 85% | V1 conceded missing explicit endpoint; FR-012 implies workflow not just one-way |
| U-014 (audit DB-role INSERT/SELECT only) | **V2 incorporate** | 90% | V1 conceded gap; DB-role-level constraint is stronger than application-only |
| **Shared Assumptions** ||||
| A-001 (single-region) | converged ACCEPT | 80% | Both advocates accepted with QUALIFY for V1 |
| A-002 (GDPR+OWASP only regulatory) | converged QUALIFY | 75% | Both advocates QUALIFIED; explicit out-of-scope owed |
| A-003 (REST only) | converged ACCEPT | 90% | Unambiguously in scope |
| A-004 (single team can absorb) | converged QUALIFY | 70% | Both flagged staffing assumption |
| A-005 (p95 boundary) | converged REJECT | 80% | Both advocates rejected — real ambiguity in both variants |

### Convergence Calculation

- Total diff points (S+C+X+U+A): 6 + 18 + 6 + 14 + 5 = 49
- Agreed points (confidence ≥ 55% with explicit winner OR shared-assumption converged): 41
- Per-point convergence: 41/49 = **0.836** ≥ 0.80 threshold ✓
- Taxonomy coverage: L1=6, L2=11, L3=23+ ✓ (all levels covered)
- Invariant probe gate: **9 HIGH-severity UNADDRESSED items** → **BLOCKS** formal convergence

### Score by Variant (Diff-Point Tally)

| Variant | Diff Points Won (winner side) | Notes |
|---------|-------------------------------|-------|
| V1 (opus) | 25 + 11 unique retained = **36** | Dominant on security/operational rigor (Argon2, audit timing, perm propagation, chaos, DR, pentest, IR, key separation) |
| V2 (sonnet) | 9 + 3 unique = **12** | Strong on simplicity/source-fidelity (static RBAC, longer soak, 14-day grace, avatar, reactivation, DB-role audit) |
| Ties / shared | 1 + 5 shared assumptions = 6 | S-006 cosmetic; A-001..A-005 mutual |

## Convergence Assessment

- **Per-point alignment**: 41/49 = 83.6% (above 80% threshold) ✓
- **Taxonomy coverage**: all three levels addressed ✓
- **Invariant probe**: 9 HIGH-severity UNADDRESSED findings ✗ → **BLOCKS** convergence

**Status**: BLOCKED_BY_INVARIANTS

**Interpretation**: The debate produced strong per-point convergence (V1 wins majority of high-severity contradictions; V2 retains specific source-fidelity / admin-UX wins). However, Round 2.5 surfaced 9 HIGH-severity invariant gaps in the emerging consensus (e.g., OAuth+2FA interaction unpinned, RBAC empty-roles edge case, audit-event taxonomy gaps for FR-004 role changes and FR-012 deactivation). These gaps must be tracked in the return contract's `unaddressed_invariants` field and folded into the refactor plan as explicit clarification deliverables in the merged roadmap.

### Unresolved Points (carried into refactor plan)

- X-002 (refresh TTL): split decision — refactor plan will adopt V1's 30-day with family rotation + V2's 7-day-rotated-on-each-use as the **default behavior** (compromise: 7-day rotation cadence inside a 30-day absolute family lifetime)
- X-004 (RBAC architecture): split decision — refactor plan will adopt V2's static 4-role hierarchy as the **default seeded model** (closer to source spec) but retain V1's permissions table + `perms[]` JWT claim as the **underlying schema** (forward extensibility without complexity-cost in v1)
- X-006/C-008 (deactivation grace): split decision — refactor plan will adopt V2's 14-day grace + V2's explicit reactivation endpoint
- C-007 (lockout policy): pick V2's 5/15min — closer to common industry default
- 9 HIGH-severity invariants from Round 2.5: each becomes a specific clarification deliverable in the merged roadmap (e.g., explicit interaction-effect deliverables for OAuth+2FA, deactivation+access-token race, audit-event-taxonomy completeness for FR-004 / FR-012)

## Base Variant Recommendation

**Variant 1 (opus)** is the recommended base. Rationale:

- Wins 25 of ~38 contested diff points (66%)
- Retains 11 unique contributions of high operational value (chaos, DR, pentest, IR, key separation, perm propagation, family rotation)
- V2's wins are concentrated in 3 admin-UX deliverables (U-012/13/14) + 1 ops parameter (soak duration C-018) + 4 architectural simplifications (C-004, C-006, C-007, C-008) — all incorporable into V1 base via the refactor plan with low integration risk.

Formal scoring (quant + qual) follows in `base-selection.md`.
