# Base Selection

## Qualitative scoring (30-criterion additive rubric, 6 dimensions)

| Dimension (max 5) | V1 architect | V2 security | V3 devops |
|-------------------|:---:|:---:|:---:|
| Completeness | 4 | 4 | 4 |
| Correctness | 4 | **5** | 3 |
| Structure | **5** | 4 | 4 |
| Clarity | 4 | 4 | **5** |
| Risk Coverage | 4 | **5** | 4 |
| Invariant & Edge-Case Coverage | 3 | **5** | 3 |
| **qual subtotal /30** | 24 (0.80) | **27 (0.90)** | 23 (0.77) |

Edge-case floor (≥1/5 on Invariant dimension): all three pass.

## Quantitative scoring (proxy)

| Metric (weight) | V1 | V2 | V3 |
|-----------------|:--:|:--:|:--:|
| Requirement coverage (C1–C6, SC1–7, OQ-A–E) (0.30) | 0.90 | 0.92 | 0.80 |
| Internal consistency (0.25) | 0.85 | 0.80 | 0.80 |
| Specificity (0.15) | 0.90 | 0.85 | **0.95** |
| Dependency completeness (0.15) | **0.95** | 0.80 | 0.85 |
| Section coverage (0.15) | 0.90 | 0.85 | **1.00** |
| **quant score** | 0.89 | 0.85 | 0.86 |

## Combined (0.5 quant + 0.5 qual)

| Variant | quant | qual | **combined** |
|---------|:-----:|:----:|:-----:|
| V1 architect | 0.89 | 0.80 | 0.845 |
| **V2 security** | 0.85 | 0.90 | **0.875** |
| V3 devops | 0.86 | 0.77 | 0.815 |

## Selected base: **Variant 2 (sonnet:security)**

**Rationale.** For a system whose defining risk is *running a write-capable LLM against
untrusted comment text*, Correctness + Risk Coverage + Invariant/Edge-Case are the
load-bearing dimensions, and V2 leads all three. V2 also contributes the single most
decision-relevant architectural move — the **split dispatcher/runner host** (U-001 partner)
that reconciles the V1↔V3 host dispute (X-001) — and the **injection-as-data** correction
(U-001) that fixes the literal topic phrasing. Margin over V1 is 0.030 (>0.05? no → within
tiebreaker band vs V1). Tiebreaker L2 (correctness criteria count): V2 (5) > V1 (4) → V2.

**Strengths to preserve from base (V2):** threat model, authz bypass enumeration,
injection-as-data envelope, effective-level-minimum, parent re-check, sandbox boundary,
scoped credentials, secret allowlist-env wrapper.

**Strengths to incorporate:**
- From **V1 architect**: 15-component inventory with SoT paths (A1–A15); explicit control-flow;
  parent resolution via `in_reply_to_id` + parentless-reject; build sequencing; ledger-as-SoT
  principle; commit-point discipline (upgraded to two-phase per INV-002).
- From **V3 devops**: systemd unit + hardening; ETag/304 rate-limit + 403 backoff; audit-ledger
  JSONL schema; observability/alerting; atomic-write + flock; SHA-correlation (upgraded to
  exact-match per INV-005); deploy/rollback runbook.

**Base weaknesses to fix via merge:** V2's `MIN()` formula underspecified (INV-006);
V2 lighter on component inventory + ops mechanics (filled by V1/V3); all-variant HIGH gaps
INV-001/002/003/007 resolved in §Invariant Resolutions of the merged spec.
