# Diff Analysis — Per-Task QA Architectures

## Metadata
- Generated: 2026-06-01
- Variants compared: 3
- Total differences found: 24 (S: 4, C: 6, X: 4, U: 8, A: 2)
- Categories: structural (4), content (6), contradictions (4), unique contributions (8), shared assumptions (2)

## Structural Differences

| # | Area | V1 /task | V2 /task-builder | V3 /sc:task | Severity |
|---|---|---|---|---|---|
| S-001 | Verification phase placement | Execution-time (phase boundary) | Plan-time (research / structural / qualitative stages) | Task-time (per individual task) | High — three orthogonal placements |
| S-002 | Number of verification layers | 2 (phase-gate + post-completion) | 3 (research-gate + structural + qualitative) | 1 (tier-routed) + 1 conditional (TFEP) | Medium |
| S-003 | Gate-blocking model | Blocks next phase until PASS | Blocks next stage until PASS | Does NOT block; verification skip allowed | High — different floor on strictness |
| S-004 | Failure ladder topology | Fix-cycle (max 3) → HALT-ask-user | Gap-fill (max 3) → Open Questions | Forensic-ladder (light → standard → FULL-STOP) | Medium |

## Content Differences

| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity |
|---|---|---|---|---|---|
| C-001 | Fix authority | rf-qa fix_authorization: true (auto-fix) | A.8 read-only; A.10/A.10.5 fix_authorization: true | NO ad-hoc fixes (VIOLATION-level prohibition) | High — philosophical opposites |
| C-002 | Test-modification handling | Allowed via fix_authorization (prompt constrains) | n/a (plan-time; doesn't run tests) | Architecturally PROHIBITED; tests_are_wrong → user adjudication | High |
| C-003 | Regression detection | Cross-phase post-completion structural pass | n/a (plan-time) | Baseline-snapshot at task start; pre-existing failure → MUST escalate | Medium |
| C-004 | Cross-phase consistency | Post-completion 2-step explicitly covers it | Single artifact; cross-phase not applicable | Per-task isolation; no cross-task interaction-effect detection | Medium |
| C-005 | Partition-agent failure handling | Single-instance failure → defer to user | DNSP synthetic-finding protocol (HIGH-severity emission with byte-exact contract) | Not addressed (forensic-ladder triggers on test failures, not QA-agent crashes) | High |
| C-006 | Token cost shape | ~5-15K per phase + ~10-20K post | ~30-50K total (parallelizable within layer) | ~3-5K STRICT / ~300-500 STANDARD / ~0 LIGHT (distribution-weighted lowest) | Medium |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | fix_authorization | true (auto-fix is correct response to defects) | true at A.10/A.10.5 (auto-fix is correct for structural drift) | PROHIBITED (auto-fix is the path to test-gaming) | High — operationally contradictory philosophies |
| X-002 | Mandatory verification floor | Mandatory phase-gate on Phase ≥2 | Mandatory at every gate | LIGHT/EXEMPT tiers SKIP verification | High — different floor |
| X-003 | Tests-are-wrong response | rf-qa can modify (advisory prompt restraint) | n/a | NEVER auto-edit; user adjudicates | High |
| X-004 | Hallucination protection | None explicit | AX-5 invented-content axis + anti-inflation rule | None explicit | Medium — V2 is the only variant with explicit defense |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | Cross-phase orphaned-output / missing-output detection in post-completion | HIGH — catches integration bugs no single-phase gate sees |
| U-002 | V1 | 15-item operational checklist (gate dry-run, runtime failure path trace, completion scope honesty, ambient dep completeness) | HIGH — most granular behavioral validation across variants |
| U-003 | V2 | DNSP synthetic-finding protocol (HIGH-severity emission with byte-exact contract, dedup_key 2-tuple, INV-021 N-1 cohort concurrency invariant) | HIGH — only formal partition-failure handling across variants |
| U-004 | V2 | DM-005 Phase Contract (frozen wire ABI, schema_version 1.0.0) + INV-002 freshness re-extract + INV-010 dynamic catalogue enumeration | HIGH — eliminates redundant re-checking while preventing stale-verdict gaming |
| U-005 | V2 | 5 Adversarial Axes (drift / contradictions / omissions / weakened-criteria / invented-content); FORBIDDEN to use N/A in Axis column | MEDIUM — structurally forces sycophantic-agreement defenses |
| U-006 | V3 | Test baseline snapshot distinguishing pre-existing vs new failures (regression auto-detection) | HIGH — solves real test-failure-classification problem |
| U-007 | V3 | VIOLATION-level prohibitions architecturally enforced (no ad-hoc fixes, no test modification) | HIGH — empirically informed (Goodhart's-law / test-gaming literature) |
| U-008 | V3 | Tier classification routing (STRICT 3-5K / STANDARD 300-500 / LIGHT 0 / EXEMPT 0) | MEDIUM — token efficiency win, but keyword-based heuristic blind to semantic criticality |

## Shared Assumptions (UNSTATED preconditions promoted to [SHARED-ASSUMPTION] diff points)

| # | Assumption | Source Agreement | Impact | Classification |
|---|---|---|---|---|
| A-001 | Sub-agent verifications converge to truth (the verifier doesn't share representational bias with the executor at the level of the specific defect) | All 3 variants delegate verification to a sub-agent (rf-qa / rf-qa-qualitative / quality-engineer) without explicit calibrator-disjoint-set enforcement | HIGH — empirically falsified by memory `feedback_sc_reflect_vs_inline_rfqa.md` (R0 PR #112 inline rf-qa missed 2 blindspots `/sc:reflect --mode post` caught). Self-confirmation bias is real and unaddressed | UNSTATED |
| A-002 | Citations / file:line refs in QA reports are accurate (the verifier's claim that X exists at file:N actually corresponds to the on-disk state) | All 3 variants treat QA reports as ground truth without re-Read of cited line ranges | MEDIUM — none have an evidence-validator final gate (which `sc-reflect-protocol` has at §11.2 as a mandatory non-negotiable). Citations could be hallucinated and propagate through to fix decisions | UNSTATED |

## Summary

- Total structural differences: 4 (1 High, 3 Medium)
- Total content differences: 6 (3 High, 3 Medium)
- Total contradictions: 4 (3 High, 1 Medium)
- Total unique contributions: 8 (6 High, 2 Medium)
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: S-001, S-003, C-001, C-002, C-005, X-001, X-002, X-003, U-001, U-002, U-003, U-004, U-006, U-007, A-001
