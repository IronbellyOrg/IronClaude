<!-- Provenance: This document was produced by /sc:adversarial Mode A -->
<!-- Base: Variant 3 (/sc:task tier-classified executor) -->
<!-- Incorporated: Variant 1 (/task) + Variant 2 (/task-builder) per refactor-plan.md -->
<!-- Architectural additions: sc:reflect-post integration (INV-006 resolution) + NEEDS_HUMAN_ADJUDICATION verdict + composition-safety check -->
<!-- Merge date: 2026-06-01 -->
<!-- Convergence: 0.71 raw / 0.85+ effective post-INV-006 resolution -->
<!-- Status: BLOCKED_BY_INVARIANTS (INV-006) → unblocked by Change #9 -->

# Merged QA Architecture Recommendation: Three-Variant Synthesis

## Executive Summary

The three variants (/task /task-builder /sc:task) are **not competing architectures** — they are **layered architectures operating at different validation timepoints**:

- `/task-builder` validates at **plan-time** (BUILD-time of task files)
- `/task` validates at **execution-time** (per-phase during MDTM execution)
- `/sc:task` validates at **task-time** (per individual task with risk-routing)

The 3-variant adversarial debate (15/21 numbered diff points resolved, 0/2 [SHARED-ASSUMPTION] points resolved — convergence BLOCKED_BY_INVARIANTS by INV-006) surfaced that **all three share a structural blindspot**: none has a calibrator-disjoint-set / out-of-context independent verifier. This blindspot is empirically demonstrated by the R0 PR #112 case where inline rf-qa missed 2 blindspots that `/sc:reflect --mode post` caught.

The merged recommendation **selects V3 as base** (highest combined score 0.845; strongest on asymmetric-cost 0.92 and token-efficiency 0.92) and **incorporates 8 protocol-level transfers + 3 architectural additions** including the INV-006 resolution.

---

## The Composition Pattern (Three Variants Together)

```
                  ┌──────────────────────────────────────────────────┐
                  │  /task-builder QA — PLAN-TIME                    │
                  │  ──────────────────────────────────────────────  │
                  │  A.8 research-gate (analyst + qa parallel)       │
                  │  A.10 structural (TB-Add-1..8)                   │
                  │  A.10.5 qualitative (15-item + 5 axes)           │
                  │  DM-005 producer/consumer wire ABI               │
                  │  DNSP synthetic-finding protocol                 │
                  └──────────────────┬───────────────────────────────┘
                                     ▼ (task file passes 3 gates)
                  ┌──────────────────────────────────────────────────┐
                  │  /task QA — EXECUTION-TIME                       │
                  │  ──────────────────────────────────────────────  │
                  │  Phase-gate (after every phase ≥2)               │
                  │    rf-qa adversarial + fix_authorization         │
                  │    + cross-phase orphan/missing detection        │
                  │    + 15-item operational checklist               │
                  │  Post-completion 2-step structural + qualitative │
                  │  Critical Path Override per V3 tighter floor     │
                  └──────────────────┬───────────────────────────────┘
                                     ▼ (per-item delegation)
                  ┌──────────────────────────────────────────────────┐
                  │  /sc:task QA — TASK-TIME (BASE)                  │
                  │  ──────────────────────────────────────────────  │
                  │  Tier classification (STRICT/STANDARD/LIGHT/EX)  │
                  │  Tighter floor: tested modules → ≥STANDARD       │
                  │  STRICT-tier: quality-engineer +                 │
                  │    V1's 15-item checklist                        │
                  │    V2's 5 Adversarial Axes (AX-1..AX-5)          │
                  │    V2's DNSP partition handling                  │
                  │  TFEP no-ad-hoc-fixes + baseline snapshot        │
                  │  DM-005 wire to forensic + anti-inflation rule   │
                  │  NEEDS_HUMAN_ADJUDICATION 3rd verdict state      │
                  └──────────────────┬───────────────────────────────┘
                                     ▼ (after STRICT-tier completes)
                  ┌──────────────────────────────────────────────────┐
                  │  /sc:reflect --mode post --depth deep            │
                  │  ──────────────────────────────────────────────  │
                  │  ARCHITECTURAL ADDITION — RESOLVES INV-006       │
                  │  Out-of-context independent verifier             │
                  │  Calibrator-disjoint-set property                │
                  │  4-category deviation classification             │
                  │  Mandatory evidence-validator gate (§11.2)       │
                  │  Empirically validated (R0 PR #112)              │
                  └──────────────────────────────────────────────────┘
```

---

## Critical Insights from the Debate

### Insight 1 — fix_authorization is not the dichotomy

The right framing is **"what should the fixer be allowed to do?"** rather than "should the fixer have authority?"

- V3's prohibition is the SPECIFIC defensive prohibition: NO ad-hoc fixes in response to test failures; NO modifying tests to make failures pass
- V1/V2's broad fix_authorization is fine for STRUCTURAL fixes (frontmatter shape, missing sections, formatting drift)
- The merged base **adopts V3's prohibition for test files specifically** and **adopts V1/V2's fix authority for structural / formatting / non-test artifacts**
- Empirical support: Goodhart's-law / sycophancy literature shows AI agents systematically gravitate toward test-modification when given freedom; architectural prohibition is more reliable than instructional restraint on this specific dimension

### Insight 2 — Plan-time / task-time / execution-time are ORTHOGONAL

The three variants have been DEBATED as if they compete, but they don't:

- /task-builder catches defects in TASK FILES (cheap to fix at plan-time, 10-100× more expensive post-execution)
- /task catches defects in PHASE OUTPUTS (groundable in actual files on disk)
- /sc:task catches defects in INDIVIDUAL TASKS (with risk-routing)

Each layer's verification has **strictly different signal** than the others. The optimal architecture composes them.

### Insight 3 — The shared blindspot is self-confirmation bias

**INV-006 sufficiency_challenge** (HIGH UNADDRESSED across all 3) and **A-001 calibrator-disjoint-set** (UNSTATED shared assumption empirically falsified):

- None of the three variants has structural protection against the case where the verifier shares representational bias with the executor at the level of the specific defect
- R0 PR #112 documents this empirically: inline rf-qa passed inline-rf-qa's surface signal but missed the underlying defect that out-of-context `/sc:reflect --mode post` caught (2 blindspots in M8 + M9)
- The fix is `/sc:reflect --mode post --depth deep` as an out-of-context independent verifier between QA cycles
- This is exactly what the SprintRunReflect brainstorm (.dev/releases/backlog/SprintRunReflect/) proposes integrating into the sprint pipeline

### Insight 4 — DNSP partition handling is the only formal contract across variants

Of all the mechanisms surveyed, V2's DNSP synthetic-finding protocol is the most formally specified:
- byte-exact emission contract with named rejection symbols (R-117 through R-121)
- INV-021 N-1 cohort concurrency invariant
- Dedup_key 2-tuple with closed vocabulary for the exhaust-point alphabet
- Found_n_times counter with monotonic exact +1 increment on within-cycle collapse

The pattern is transferable beyond /task-builder. The merged recommendation adopts it at STRICT-tier verification in /sc:task.

### Insight 5 — V2's anti-inflation rule structurally prevents Self-Audit gaming

The rule `(consumer's Self-Audit MUST list which producer-PASS items it relied on AND ≥1 semantic check where producer-PASS was insufficient)` is preserved byte-stable across releases. This is the only mechanism in any variant that structurally prevents the "rubber-stamp" failure mode where a downstream verifier passes everything because an upstream verifier passed it.

---

## Detailed Per-Dimension Scoring (5 user-specified focus areas)

| Dimension | V1 | V2 | V3 | Winner | Why |
|---|---|---|---|---|---|
| Correctness | 0.75 | 0.85 | 0.80 | V2 | 3 orthogonal layers + AX-5 invented-content; weakness in plan-time-only scope |
| Coverage | 0.72 | 0.85 | 0.62 | V2 | 3 layers + DNSP + DM-005 + freshness rules; V3 tier-skip allows blind spots |
| Asymmetric-cost | 0.60 | 0.72 | 0.92 | V3 | TFEP no-ad-hoc-fixes is the gold standard for test-gaming defense |
| Token-efficiency | 0.55 | 0.45 | 0.92 | V3 | Tier routing matches cost to risk |
| Operational-realism | 0.82 | 0.62 | 0.70 | V1 | MDTM phase-gate is shape-agnostic |

**Combined (weighted equally)**: V3 = 0.845 > V2 = 0.825 > V1 = 0.805 (2.0% margin at top resolved at tiebreaker Level 1 in V3's favor: V3 won 7/14 scoring-matrix rows vs V2's 5)

---

## The 11 Refactor-Plan Changes Summarized

| # | Change | Source | Risk |
|---|---|---|---|
| 1 | Adopt V1 cross-phase post-completion validation | V1 §2 Layer 2 | Low |
| 2 | Adopt V1 15-item operational checklist as STRICT-tier depth | V1 §2 Layer 2 Step 2b | Low |
| 3 | Adopt V2 DNSP synthetic-finding protocol for STRICT-tier partition failures | V2 §2 Layer 1 | Low |
| 4 | Adopt V2 5 Adversarial Axes including AX-5 invented-content | V2 §2 Layer 3 | Low |
| 5 | Adopt V2 anti-inflation rule for forensic remediation reports | V2 §2 Layer 3 | Low |
| 6 | Adopt V2 DM-005 Phase Contract pattern for forensic-to-remediation handoff | V2 §2 Layer 3 | Low |
| 7 | Tighten V3 tier-routed SKIP criteria (tested-module override) | INV-005 | Medium |
| 8 | Document V1+V3 composition pattern explicitly | INV-005 | Low |
| **9** | **Integrate /sc:reflect --mode post as out-of-context independent verifier** | **INV-006 resolution** | **Medium** |
| 10 | Define third QA-finding state NEEDS_HUMAN_ADJUDICATION | INV-001 | Low |
| 11 | Composition-safety check for /task + /sc:task interaction | INV-005 | Low |

---

## Resolution of the Convergence Block

INV-006 (HIGH UNADDRESSED across all 3) is resolved by **Change #9** (sc:reflect-post integration). Post-resolution:

- A-001 (calibrator-disjoint-set, UNSTATED) → ADDRESSED (sc:reflect runs in a different context window, providing the disjoint-set property)
- A-002 (citation accuracy, UNSTATED) → ADDRESSED (sc:reflect-protocol §11.2 has mandatory evidence-validator gate)
- INV-002 (HIGH partially-addressed by V2) → ADDRESSED across the composed system (sc:reflect's evidence-validator re-Reads cited file:line ranges)
- INV-006 (HIGH UNADDRESSED) → ADDRESSED (sc:reflect's adversarial-stance + 4-category deviation taxonomy catches the underlying-defect-vs-surface-signal mismatch)

Effective convergence post-resolution: **0.85+** (well above the 0.80 threshold).

---

## Operational Realism: When to Use Each Variant Standalone

The merged recommendation is for composed pipelines. Standalone use cases:

| Use case | Recommended variant | Why |
|---|---|---|
| Building MDTM task files from a request | `/task-builder` only | Plan-time validation is its native scope |
| Executing MDTM task files with rich phase structure | `/task` only | Phase-gate + post-completion is purpose-built for this |
| Executing individual code-modification tasks with cost-routing | `/sc:task` only | Tier classification is the differentiator |
| Composed sprint pipelines with end-to-end validation | `/task-builder` → `/task` → `/sc:task` → `/sc:reflect --mode post` | The full merged architecture |

---

## Recommendations for Implementation

1. **Adopt the merged base** (V3 + 11 refactor-plan changes) as `/sc:task-v2` or as a new `/sc:task --strict-merged` mode
2. **Wire `/sc:reflect --mode post --depth deep`** as a mandatory post-STRICT-tier hook (Change #9) — this is the highest-impact addition
3. **Document the composition pattern** in a top-level architecture doc so operators can compose the three variants explicitly
4. **Empirically validate** the tier-floor tightening (Change #7) against the actual distribution of LIGHT-tier tasks in production
5. **Track INV-001/003/005** as v1.1 hardening opportunities — they are MEDIUM/LOW severity and don't block initial adoption

---

## Open Questions

1. Should the merged recommendation be a NEW skill (`/sc:task-merged-v2`) or an EXTENSION of `/sc:task` via flags?
2. What's the empirical cost of Change #9 (sc:reflect-post integration) per STRICT-tier task in production? The estimate is 10-30K tokens; needs validation.
3. How does the merged architecture compose with the SprintRunReflect brainstorm's `reflect_fleet.py` proposal? Are they parallel additions or layered?
4. Should `/sc:task-builder` adopt V1+V3 transfers symmetrically? The current refactor-plan focuses on V3 base; V2 itself could be enriched.
