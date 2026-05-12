# Dimension 3: Anti-Instinct Audit

**Compared artifact:** `anti-instinct-audit.md` across 3 runs
**Sources:** Research files 01, 02, 03 (QA-verified); spot-checks against actual YAML frontmatter

---

## Comparison Table

| Metric | Run A (Baseline) | Run B (Spec+PRD) | Run C (TDD+PRD) |
|--------|:----------------:|:----------------:|:----------------:|
| **Lines** | 37 | 46 | 53 |
| **fingerprint_coverage** | 0.72 (13/18) | 0.72 (13/18) | 0.73 (33/45) |
| **undischarged_obligations** | 0 | 2 | 1 |
| **uncovered_contracts** | 0 | 3 | 4 |
| **total_obligations** | 1 | 2 | 1 |
| **total_contracts** | 6 | 6 | 8 |
| **fingerprint_total** | 18 | 18 | 45 |
| **fingerprint_found** | 13 | 13 | 33 |
| **Missing fingerprints** | 5 (JIRA, OIDC, PASETO, CSRF, OWASP) | 5 (JIRA, PASETO, CSRF, UUID, REST) | 12 (complexity_class, feature_id, spec_type, target_release, quality_scores, WHAT, SMTP, UUID, NULL, NULLABLE, AUTH_INVALID_CREDENTIALS, OWASP) |
| **Pipeline status** | PASS (implied) | FAIL | FAIL (implied) |

---

## Spot-Check Results

| Check | Research Value | Spot-Check Value | Method | Match |
|-------|:-------------:|:----------------:|--------|:-----:|
| Run A fingerprint_coverage | 0.72 | 0.72 | `grep 'fingerprint_coverage' anti-instinct-audit.md` | YES |
| Run B undischarged | 2 | 2 | `grep 'undischarged' anti-instinct-audit.md` | YES |
| Run C fingerprint_coverage | 0.73 | 0.73 | `grep 'fingerprint_coverage' anti-instinct-audit.md` | YES |
| Run C uncovered_contracts | 4 | 4 | `grep 'uncovered' anti-instinct-audit.md` | YES |

---

## Assessment

All three runs achieve nearly identical fingerprint coverage (~0.72-0.73), but the underlying metrics differ substantially. Run C (TDD+PRD) has 2.5x more fingerprints to track (45 vs 18) because the TDD input introduces many more technical terms, yet maintains comparable coverage. However, Run A has the cleanest audit: 0 undischarged obligations and 0 uncovered contracts, while Runs B and C both have obligations and contract gaps. The paradox is that richer inputs create more surface area for the audit to find gaps, so higher undischarged/uncovered counts in B and C reflect more thorough auditing rather than worse quality. Run B's 3 uncovered contracts all relate to middleware_chain integration; Run C's 4 uncovered contracts are strategy_pattern references -- both are architecture-level patterns that the roadmap narrative tends not to discharge explicitly.
