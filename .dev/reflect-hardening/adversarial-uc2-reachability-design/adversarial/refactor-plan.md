# Refactor Plan: Make C Canonical, Refactor (not discard) B

## Overview
- **Base:** Variant 1 (C-canonical, owns contract 1.6.0).
- **Incorporated:** B preserved as complementary advisory detector, sequenced after C.
- **Change count:** 6 planned + 2 binding preconditions (from invariant probe).
- **Overall risk:** Medium (cross-task coordination; no destructive deletion).
- **Review status:** auto-approved (non-interactive). Two items flagged `needs_human_decision`.

## Planned Changes

| # | Change | Source→Target | Rationale (evidence) | Risk |
|---|---|---|---|---|
| 1 | **C keeps `contract_version: "1.6.0"`** with reachability_* R7 fields, unchanged. | C as-is | base-selection combined 0.880; C is gate-grade + complete | Low |
| 2 | **Re-point B's contract bump OFF 1.6.0.** Choose ONE: (a) additive `1.7.0` stable minor rebased onto post-C SKILL.md, OR (b) reclassify `runtime_surface_*` as **advisory telemetry** (no stable bump). | B-008 §9.1 → 1.7.0 or telemetry | Resolves X-001/M-028; A-002 surfaced telemetry option | Medium — `needs_human_decision` (B-task owner) |
| 3 | **Re-allocate eval ids.** C registers its `uc2-reachability-*` cases first at 1.6.0; B rebases `uc2-surface-*` off the hardcoded `37-41`. | B-024 → new ids | INV-003; resolves M-031 | Low |
| 4 | **B rebases its SKILL.md / deviation-taxonomy edits onto C's post-1.6.0 baseline** (additive, preserving C's real-boot-only Regression semantics). | B-006/B-012/B-013 | INV-004; resolves M-029/X-002/X-003 | Medium |
| 5 | **Re-express C-040's intent as a B-side guard:** "runtime_surface_* additions never alter reachability_* gate verdicts; reachability gate remains real-boot-only." | C-040 → B QA lens | Resolves M-030/X-004 without discarding B | Medium |
| 6 | **Update the M-008 `/sc:adversarial` debate** to adopt: C owns skill 1.6.0; A's CLI return-contract is a separate surface; B is 1.7.0-additive or advisory-telemetry. | matrix M-008/M-042 | Resolves M-042; prevents M-008 resolving a 2-body framing of a 3-body collision | Low |

## Binding Preconditions (from invariant probe — MANDATORY before any B+C coexistence)

| # | Precondition | Origin |
|---|---|---|
| P-1 | **Precedence invariant:** C's reachability `unreachable`/Regression is authoritative and MUST NOT be softened to a B `degrade`/fail-open for the same root cause. B (later) must add a guard + an eval proving "unwired surface whose annotated contracted sink is unobserved → Regression (C wins), never degrade-only." | INV-001 (HIGH) |
| P-2 | **Sufficiency closure:** treat changes #2–#6 as a *set*; "C canonical" is not complete until all are applied. Verify each of M-028/M-029/M-030/M-031/M-042 is independently closed. | INV-002 (HIGH) |

## Changes NOT Being Made (considered & rejected)

| Rejected change | Why rejected |
|---|---|
| Discard B entirely | Loses unique unwired-surface recall (U-002); B passed its own PRE reflect; no obsolescence/unsafety — discard criteria unmet. |
| Discard C | C is the higher-precision, more-complete gate; discarding loses the highest-value capability. |
| Coexist now under one 1.6.0 union (Variant 3) | Combined 0.485; violates C-040 as written, forces 3-way single-fix-agent merge (M-016/M-047), unsafe without P-1. Mechanically valid but strictly dominated by sequencing. |

## Answer to "can one 1.6.0 contract host both field families?"
**Technically yes** (names don't collide; both additive/optional) — **but not recommended.** Sequence as additive minors (1.6.0 = reachability_*, 1.7.0 = runtime_surface_*), or make B telemetry (no bump). Immediate union is unsafe until P-1 ships.
