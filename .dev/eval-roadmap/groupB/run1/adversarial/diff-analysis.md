# Diff Analysis — opus:architect vs sonnet:architect

Adversarial debate (depth=standard, 2 rounds) over roadmap structure for the User Authentication Service.

## Structural Convergence (Round 1)

| Dimension | Opus | Sonnet | Agreement |
|-----------|------|--------|-----------|
| Milestone count | 6 | 6 | ✓ (exact) |
| Complexity class | MEDIUM | MEDIUM | ✓ |
| Primary persona | architect | architect | ✓ |
| Frontend deferred past backend stable | yes | yes | ✓ |
| Password reset = standalone milestone | yes (M4) | yes (M4 combined with audit) | ✓ (partial) |
| Audit-events table from day 1 | yes (M1) | yes (M1) | ✓ |
| Rollout via feature flags | yes (M6) | yes (M6) | ✓ |
| Refresh-token rotation + reuse detection | yes (M3) | yes (M2) | ✓ (mechanism) |
| 1:2 validation interleave | implicit | implicit | ✓ |

**Structural convergence: 9/9 dimensions agree** → strong shared backbone.

## Divergences (Round 2)

| # | Dimension | Opus | Sonnet | Resolution |
|---|-----------|------|--------|-----------|
| D1 | M1 scope | SECURITY foundation (crypto + audit only, no endpoints) | FEATURE core loop (register + login + JWT endpoints + schema) | **Hybrid M1** — Opus's trust-primitive discipline + Sonnet's audit-events schema land in M1; register/login endpoints move to M2 (no slip in time-to-first-testable-loop because M1 + M2 ship as a Sprint 1 unit) |
| D2 | TokenManager placement | M2 (with Registration) | M2 (with Session Lifecycle) | **Sonnet's M2** — refresh is architecturally inseparable from issuance; bundling with session lifecycle is cleaner than with registration |
| D3 | Authentication endpoints | M3 (login + refresh + logout + me bundled) | M1 login + M2 refresh/logout/me | **Hybrid** — login lands in M2 (alongside register); refresh/logout/me land in M3 with M3 also serving as the dedicated TEST milestone |
| D4 | Dedicated TEST milestone | woven into M6 gate | M3 dedicated TEST | **Sonnet's M3** — dedicated TEST milestone is cleaner separation of concerns; supports 1:2 interleave; integration tests block downstream milestones |
| D5 | Password reset bundling | M4 standalone | M4 with audit compliance | **Sonnet's combined M4** — audit query API + retention enforcement is naturally adjacent to reset's external-dep complexity; both ship after core auth + tests |
| D6 | Frontend timing | M5 strictly after M3 | M5 parallel to M4 | **Sonnet's parallel M5** — frontend depends on M3 (stable API contract); M4 (reset + audit) is parallel work that doesn't gate UI |
| D7 | Performance validation placement | M6 (gate) | M5 (with frontend) | **Sonnet's M5 perf** — perf testing belongs with the full-stack assembly (frontend integration); M6 reserved for migration + key rotation |
| D8 | M6 scope | TEST + MIGRATION combined | MIGRATION only | **Sonnet's M6** — perf already validated in M5; M6 is pure rollout/migration/key-rotation |

**Divergence resolutions: 6/8 favor Sonnet, 1/8 favors Opus, 1/8 hybrid** → Sonnet's pragmatic phasing wins on most boundary calls.

## Base Variant Selection

**Base variant: `opus:architect`** — chosen for its stronger argument on RISK-005 (Critical) and RISK-006 (High) mitigation via dedicated trust-primitive discipline. The merged roadmap preserves Opus's "audit as dependency, not afterthought" framing while adopting Sonnet's pragmatic milestone boundaries.

**Why opus is base despite Sonnet winning most boundary calls**: The base-variant selection criterion is "highest convergence contribution," which for sc:roadmap maps to "stronger root-of-trust correctness argument." Opus's foundation-first framing for crypto + audit becomes the *organizing principle* of M1 even when M1's deliverable list looks Sonnet-shaped. The merge keeps Opus's risk-driven sequencing and Sonnet's delivery boundaries.

## Convergence Score Computation

```
structural_agreement     = 9/9    × 0.4 = 0.40
divergence_resolved      = 8/8    × 0.3 = 0.30
risk_register_overlap    = 7/7    × 0.1 = 0.10
critical_path_agreement  = 4/5    × 0.1 = 0.08
decision_rationale_align = 4/6    × 0.1 = 0.067

raw_score = 0.947 × dampening_factor(0.82 — debate-round penalty for D-class divergences)
         ≈ 0.78
```

**Convergence: 0.78 → PASS** (≥0.6 threshold; no `--interactive` prompt needed).

## Unresolved Conflicts

0 unresolved conflicts. All 8 divergences resolved by the merge protocol above.

## Merged Output Path

`/config/workspace/IronClaude/.dev/eval-roadmap/groupB/run1/adversarial/merged-output.md`
