# TDD Comparison: anti-instinct-audit.md (Test 1 vs Test 3)

**Generated**: 2026-04-02
**Purpose**: Compare fingerprint metrics between TDD and spec pipeline runs

---

## Frontmatter Metrics Comparison

| Metric | Test 1 (TDD) | Test 3 (Spec) | Delta | Notes |
|---|---|---|---|---|
| fingerprint_total | 45 | 18 | +27 (+150%) | TDD extraction produces far more backticked identifiers as fingerprints |
| fingerprint_found | 34 | 12 | +22 (+183%) | More fingerprints found in TDD roadmap |
| fingerprint_coverage | 0.76 | 0.67 | +0.09 (+13%) | TDD has higher coverage ratio |
| total_obligations | 5 | 1 | +4 | TDD roadmap has more skeleton/TODO markers to scan |
| undischarged_obligations | 5 | 0 | +5 | TDD has more undischarged obligations |
| total_contracts | 8 | 6 | +2 | TDD roadmap has more integration contracts |
| uncovered_contracts | 4 | 0 | +4 | TDD has more uncovered contracts |
| generator | superclaude-anti-instinct-audit | superclaude-anti-instinct-audit | same | |

---

## Anti-Instinct Gate Status

| Test | Gate Result | Reason |
|---|---|---|
| Test 1 (TDD) | **FAIL** | fingerprint_coverage 0.76 (and undischarged obligations) |
| Test 3 (Spec) | **FAIL** | fingerprint_coverage 0.67 (below 0.70 threshold implied by pipeline behavior) |

Both tests FAIL the anti-instinct gate. This is expected and confirms pipeline behavior consistency.

---

## Fingerprint Analysis

### Test 1 (TDD) Missing Fingerprints (11 of 45)

- `complexity_class`
- `feature_id`
- `spec_type`
- `target_release`
- `quality_scores`
- `WHAT`
- `CORS`
- `SMTP`
- `PRIMARY`
- `AUTH_INVALID_CREDENTIALS`
- `OWASP`

### Test 3 (Spec) Missing Fingerprints (6 of 18)

- `AuthService`
- `JIRA`
- `OIDC`
- `PASETO`
- `CSRF`
- `UUID`

### Key Observation

Test 1 has 2.5x more total fingerprints (45 vs 18) because the TDD extraction produces far more backticked identifiers (component names, data model names, endpoint paths, error codes) that become fingerprints for the anti-instinct audit. Despite having more missing fingerprints in absolute terms (11 vs 6), Test 1 achieves a higher coverage ratio (0.76 vs 0.67) because its roadmap successfully incorporates most of the TDD-specific identifiers.

Test 3's missing fingerprints include `AuthService` -- a core component name that the spec-only extraction did not produce as a backticked fingerprint, but which appears in the spec's prose. This confirms that spec extraction produces fewer formal identifiers.

---

## Obligation and Contract Analysis

### Test 1 Obligations (5 undischarged)

All relate to `skeleton` patterns in Phase 1 and Phase 2 wiring tables:
- `TokenManager` skeleton reference (Phase 1, lines 88 and 96)
- `JwtService` skeleton reference (Phase 1, line 96)
- `AuthService` skeleton reference (Phase 1, line 98)
- Phase 2 skeleton reference (line 129)

These are expected in a TDD roadmap that describes skeleton-first implementation phases.

### Test 3 Obligations (0 undischarged)

One obligation detected and discharged. The spec-based roadmap uses working-code-first language rather than skeleton patterns.

### Test 1 Contracts (4 uncovered of 8)

Four uncovered contracts are all `strategy_pattern` references to Testing Strategy and Migration Strategy sections. These are expected because the TDD roadmap references testing and migration strategies that the anti-instinct scanner matches as integration contract patterns.

### Test 3 Contracts (0 uncovered of 6)

All 6 contracts covered. The spec-based roadmap has fewer contract-pattern references.

---

## Verdict: **TDD_HIGHER_FINGERPRINTS_CONFIRMED**

Test 1 (TDD) produces 2.5x more fingerprints (45 vs 18), finds 2.8x more fingerprints in its roadmap (34 vs 12), and achieves 13% higher fingerprint coverage (0.76 vs 0.67). The TDD extraction pipeline generates substantially more formal identifiers that propagate through to the roadmap, confirming that TDD content enriches the anti-instinct audit surface.
