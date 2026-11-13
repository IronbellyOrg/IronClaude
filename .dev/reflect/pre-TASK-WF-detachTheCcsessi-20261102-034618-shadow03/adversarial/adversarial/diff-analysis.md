# Diff Analysis: reflect reviewer-card comparison (Mode A)

## Metadata
- Generated: 2026-11-12T23:26Z (approx)
- Variants compared: 3 (reviewer cards: analyzer / qa / refactorer)
- Total differences found: 10 (structural 1, content 7, contradictions 1, unique 5, shared assumptions 2 promoted)

## Content Differences

| # | Topic | Card 1 (analyzer) | Card 2 (qa) | Card 3 (refactorer) | Severity |
|---|---|---|---|---|---|
| C-001 | verify-sync AC gap | present, MAJOR severity, non-blocking (F1) | present, MINOR severity (F2) | absent | Medium |
| C-002 | T4.AC4 pid baseline never recorded | present (F2) | absent | absent | Medium |
| C-003 | Pipeline Hardening HC1/HC5 absent from matrix + plan | absent | present (F1) | absent | Medium |
| C-004 | T5 narrows AC2 test-discovery grep | absent | present (F3) | absent | Low |
| C-005 | setsid isatty guard: plan-literal output != HEAD | absent | absent | present (F1) | Medium |
| C-006 | T1.AC3 pgrep cleanup over-claim (sleep child) | present (F4) | absent | absent | Low |
| S-007 | stale line anchors, symbols named | present (F3) | present (F4) | present (F2) | Low |

## Contradictions

| # | Point of Conflict | Card 1 | Card 2 | Impact |
|---|---|---|---|---|
| X-001 | severity of C-001 (verify-sync gap) | MAJOR | MINOR | Low: both non-blocking; affects report prominence only |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | Card 1 | pid baseline gap (C-002) | Medium |
| U-002 | Card 2 | HC1/HC5 Pipeline Hardening omission (C-003) | Medium |
| U-003 | Card 2 | grep discovery narrowing (C-004) | Low |
| U-004 | Card 3 | isatty guard divergence (C-005) | Medium |
| U-005 | Card 1 | pgrep cleanup over-claim (C-006) | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | S-007 rated minor by all three | Line-number anchors remain findable because symbol names sit alongside; executor will search by symbol rather than trust the number | UNSTATED | yes |
| A-002 | All cards cite prior-run artifacts (t5-checks.log etc.) as evidence | Prior-run improvisations are admissible evidence when judging the plan as a plan (they show the plan's gaps, not the plan's content) | UNSTATED | yes |

## Taxonomy tagging (AD-5)
C-001 L2, X-001 L2, C-002 L3, C-003 L2, C-004 L3, C-005 L3, C-006 L3, S-007 L1, A-001 L2, A-002 L2. All three levels covered (L1:1, L2:5, L3:4).

## Summary
- structural 1 (S-007), content 6, contradictions 1, unique 5, shared assumptions promoted 2; total diff points (denominator) = 10
- Highest severity: C-001 (Medium; the only point with cross-card severity disagreement X-001)
