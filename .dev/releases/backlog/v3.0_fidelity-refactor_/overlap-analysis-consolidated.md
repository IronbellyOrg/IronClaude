# Consolidated Overlap Analysis: Three-Spec Cross-Comparison

**Date**: 2026-03-17
**Methodology**: Three independent analysts each took one spec as their primary perspective and scored overlap against the other two. Results are merged below with score ranges showing inter-analyst agreement.

**Files analyzed**:
- **Wiring Verification**: `v3.0_fidelity-refactor_/wiring-verification-gate-v1.0-release-spec.md`
- **Anti-Instincts**: `v3.05_Anti-instincts_/anti-instincts-gate-unified.md`
- **Unified Audit Gating**: `v3.1_unified-audit-gating-v1.2.1/spec-refactor-plan-merged.md`

---

## Consolidated 3x3 Overlap Matrix

Scores shown as **median [range]** across 3 independent analysts:

| | Wiring Verification | Anti-Instincts | Unified Audit Gating |
|---|---|---|---|
| **Wiring Verification** | N/A (self) | **5/10 — 50% [4-6]** | **4/10 — 40% [3-5]** |
| **Anti-Instincts** | **5/10 — 50% [4-6]** | N/A (self) | **3/10 — 30% [3-4]** |
| **Unified Audit Gating** | **4/10 — 40% [3-5]** | **3/10 — 30% [3-4]** | N/A (self) |

### Score Breakdown by Analyst

| Pair | Analyst 1 (Wiring primary) | Analyst 2 (Anti-Instincts primary) | Analyst 3 (Unified Audit primary) | Median |
|---|---|---|---|---|
| Wiring <-> Anti-Instincts | 6/10 (60%) | 5/10 (50%) | 4/10 (40%) | **5/10 (50%)** |
| Wiring <-> Unified Audit | 3/10 (30%) | 4/10 (40%) | 5/10 (50%) | **4/10 (40%)** |
| Anti-Instincts <-> Unified Audit | 4/10 (40%) | 3/10 (30%) | 3/10 (30%) | **3/10 (30%)** |

---

## Consensus Findings

All three analysts independently identified the same overlap instances. Below is the deduplicated, consolidated list.

---

### Pair 1: Wiring Verification <-> Anti-Instincts — 5/10 (50%)

**Highest overlap pair.** Both specs respond to the same cli-portify no-op bug and target overlapping failure modes, but operate at fundamentally different pipeline stages.

#### OL-1.1: Unwired Registry / Dispatch Table Detection

| Aspect | Wiring Verification | Anti-Instincts |
|---|---|---|
| **Section** | 4.2.3 (Unwired Registry Analysis) | Section 5 (Integration Contract Extractor) |
| **Mechanism** | AST analysis of Python source code | Regex on spec/roadmap text |
| **Pipeline stage** | Post-implementation (code exists) | Pre-implementation (roadmap generation) |
| **Patterns matched** | `REGISTRY`, `DISPATCH`, `RUNNERS`, `HANDLERS`, `ROUTER` | `RUNNERS`, `HANDLERS`, `DISPATCH`, `routing_table`, `command_map`, `step_map`, `plugin_registry` |

**Verdict**: Both detect the same artifact class (dispatch tables/registries). If both ship, a registry like `PROGRAMMATIC_RUNNERS` would be flagged twice. This is defense-in-depth (different pipeline stages), not pure waste, but the detection target is identical.

**Differentiation**: Anti-Instincts covers 7 integration mechanism categories; Wiring Verification covers 3 analyzers but with AST-level precision (actual import resolution). For dispatch registries specifically, Anti-Instincts is broader; for verifying actual code wiring, Wiring Verification is authoritative.

#### OL-1.2: Unwired Callable / Constructor Injection Detection

| Aspect | Wiring Verification | Anti-Instincts |
|---|---|---|
| **Section** | 4.2.1 (Unwired Callable Analysis) | Section 5, DISPATCH_PATTERNS Category 3 |
| **Target** | `Optional[Callable]` params with `None` default never provided at call sites | Spec text matching `accepts/takes/requires Callable/Protocol/Interface` |
| **Pipeline stage** | Code AST analysis | Document regex |

**Verdict**: Both would catch the `step_runner: Optional[Callable] = None` bug — the exact motivating defect. Wiring Verification catches it more precisely (zero call-site verification); Anti-Instincts catches it earlier (before code is written).

#### OL-1.3: Orphan Module Detection vs. Fingerprint Coverage

Wiring Verification (Section 4.2.2) detects exported functions in Python files within `steps/`, `handlers/`, `validators/`, and `checks/` directories with zero importers. Anti-Instincts' fingerprint extraction (Section 6) checks spec identifier coverage in roadmap. Both would catch `steps/validate_config.py::run_validate_config` being defined but never connected, but through entirely different mechanisms on different artifacts. **Partial overlap only.**

#### OL-1.4: Shared Forensic Origin

Both cite the cli-portify no-op bug and orphaned-step evidence. Wiring Verification additionally references the `step_runner=None` default, `STEP_REGISTRY` as metadata-only, and "Link 3 does not exist." If both ship, the same root defect class is prevented by multiple redundant mechanisms.

#### OL-1.5: Gate Infrastructure Pattern (Non-contradictory)

Both define `GateCriteria` constants (`WIRING_GATE`, `ANTI_INSTINCT_GATE`) consumed by `gate_passed()`. These are additive and coexist without conflict. **No contradiction.**

#### OL-1.6: Shadow Mode Rollout Pattern (Non-redundant)

Both define shadow -> soft -> full rollout tracks, but for different gates with independent timelines. The pattern is shared but the enforcement is independent.

---

### Pair 2: Wiring Verification <-> Unified Audit Gating — 4/10 (40%)

**Moderate overlap.** Concentrated in shared defect references, `gates.py` modifications, and rollout patterns.

#### OL-2.1: D-03/D-04 Dispatch Table Checks vs. Wiring Verification's Registry Detection

| Aspect | Wiring Verification | Unified Audit Gating |
|---|---|---|
| **Section** | 4.2.3 (Unwired Registry Analysis) | SS13.4, D-03/D-04 |
| **Target** | Registries with unresolvable function values | Dispatch table names from spec appearing in roadmap |
| **Depth** | AST analysis (import resolution) | Text presence check |

**Verdict**: Both detect `PROGRAMMATIC_RUNNERS` failures. D-03 is a shallow presence check; Wiring Verification is a deep code analysis. D-03/D-04 operate at spec-to-roadmap level; Wiring Verification operates at code level. Different depth, different stage, overlapping target.

#### OL-2.2: Shared `step_runner` Defect Reference (P0-A)

Unified Audit Gating schedules the direct fix (P0-A blocker). Wiring Verification builds systematic prevention. **Complementary, not redundant** — immediate fix + long-term gate.

#### OL-2.3: Concurrent Modification of `roadmap/gates.py`

Both modify `SPEC_FIDELITY_GATE.semantic_checks`. Wiring Verification adds deviation count reconciliation; Unified Audit Gating adds D-03/D-04 dispatch checks. The checks themselves are different, but concurrent modification creates **merge conflict risk**.

#### OL-2.4: Shadow/Soft/Full Rollout Pattern Duplication

**This is the most actionable overlap in this pair.** Wiring Verification (Section 8) defines its own rollout plan with independent thresholds. Unified Audit Gating (SS7.1/SS7.2) defines a general rollout framework with configurable profiles and override governance.

**Risk**: Contradictory enforcement behavior if both define independent rollout thresholds.
**Recommendation**: Wiring Verification should use the Unified Audit Gating rollout framework rather than defining its own.

#### OL-2.5: Smoke Test Gate (G-012) vs. Wiring Verification

Unified Audit Gating defines two behavioral protections: G-012 (Smoke Test Gate — a release-tier blocking gate validating real artifact production) and SilentSuccessDetector (a post-execution hook detecting no-op pipeline runs). Wiring Verification catches the same defect class statically. These complement each other — G-012 + SilentSuccessDetector are symptom detection; Wiring Verification is root-cause detection. **Low redundancy.**

---

### Pair 3: Anti-Instincts <-> Unified Audit Gating — 3/10 (30%)

**Lowest overlap.** These specs operate at different pipeline layers (roadmap generation vs. sprint execution).

#### OL-3.1: D-03/D-04 as a Strict Subset of Anti-Instincts

**All three analysts agreed this is the most significant overlap in this pair.**

| Aspect | Anti-Instincts | Unified Audit Gating |
|---|---|---|
| **Dispatch table detection** | `fingerprint.py` extracts ALL_CAPS constants + code identifiers | D-03 checks `UPPER_CASE_NAME = {` patterns |
| **Function name detection** | `fingerprint.py` extracts function defs from code blocks | D-04 checks `_run_*()` patterns |
| **Coverage threshold** | 70% fingerprint coverage ratio | Binary pass/fail per pattern |
| **Wiring verification** | `integration_contracts.py` checks for explicit wiring tasks (verb-anchored) | D-03 checks name presence only |

**Verdict**: D-03/D-04 materially overlap with a narrower subset of Anti-Instincts' fingerprint and integration-contract coverage. If Anti-Instincts ships, D-03/D-04 are redundant for dispatch table detection. D-03/D-04's stated advantage is rapid independent deployment (~6 hours).

#### OL-3.2: Shared Forensic Motivation

Both cite the cli-portify no-op bug. Both use this evidence to justify integration-wiring checks. No functional conflict.

#### OL-3.3: Concurrent Modification of `roadmap/gates.py`

Anti-Instincts adds `ANTI_INSTINCT_GATE` with 3 checks. Unified Audit Gating adds D-03/D-04 to `SPEC_FIDELITY_GATE`. Both modify the same file. **Merge conflict risk.**

#### OL-3.4: Prompt-Level vs. Deterministic Checks (Complementary, Not Redundant)

Anti-Instincts adds `INTEGRATION_WIRING_DIMENSION` to prompt templates. Unified Audit Gating adds deterministic regex checks. These are complementary strategies (LLM-influencing vs. LLM-bypassing). **No redundancy.**

---

## Cross-Cutting Findings

### No Contradictions Found

No direct contradictions were identified among the three base specs at the gate-definition level; the main concerns are overlap, merge-conflict risk, and duplicated governance patterns. They define separate gates, target different pipeline positions, and use the same `GateCriteria`/`SemanticCheck` infrastructure. All three can coexist with coordination.

### Defense-in-Depth Pattern

The overlap between Wiring Verification and Anti-Instincts is intentional layered defense:
- **Anti-Instincts** prevents the bug at roadmap generation (spec -> roadmap fidelity)
- **Wiring Verification** catches the bug at code implementation (code -> runtime fidelity)
- **Unified Audit Gating** provides the framework for gate enforcement during sprint execution

### Key Unique Value per Spec

| Spec | Unique, non-overlapping value |
|---|---|
| **Wiring Verification** | AST-level static analysis of Python code (unwired callable detection, orphan module detection, import resolution). No equivalent exists in the other two specs. |
| **Anti-Instincts** | Obligation scanner (scaffold/discharge detection), spec structural audit (extraction quality), prompt-level modifications, 7-category integration mechanism taxonomy. Broadest prevention layer. |
| **Unified Audit Gating** | Audit workflow state machine, transition validator, audit lease/heartbeat, profile system, TUI display, sprint-level orchestration, Silent Success Detection (G-012). The execution framework all gates run within. |

---

## Actionable Recommendations

| # | Overlap | Risk | Recommendation |
|---|---|---|---|
| 1 | D-03/D-04 (Unified Audit) duplicates fingerprint/contract coverage (Anti-Instincts) | **Medium** | If Anti-Instincts ships first, make D-03/D-04 conditional on Anti-Instincts gate not being present. If Anti-Instincts ships second, D-03/D-04 serve as interim protection. |
| 2 | Wiring Verification rollout plan duplicates Unified Audit Gating framework | **Medium** | Wiring Verification should adopt the Unified Audit Gating rollout infrastructure (profiles, override governance, rollback triggers) rather than defining independent thresholds. |
| 3 | Three specs all modify `roadmap/gates.py` | **Medium** | Coordinate implementation order. Establish a single PR that adds all gate extensions, or sequence PRs to avoid merge conflicts. |
| 4 | Registry/dispatch detection overlap between Wiring Verification and Anti-Instincts | **Low** | Defense-in-depth is warranted (different pipeline stages). No action unless budget-constrained; if so, Anti-Instincts provides broader coverage while Wiring Verification provides deeper precision. |
| 5 | Shared `step_runner` defect reference across all three specs | **Low** | Not redundant — immediate fix (Unified Audit P0-A) + upstream prevention (Anti-Instincts) + downstream detection (Wiring Verification). All warranted. |

---

## Appendix: Individual Analyst Reports

The three per-perspective analyses are preserved at:
- `overlap-analysis-wiring.md` (Wiring Verification perspective)
- `overlap-analysis-anti-instincts.md` (Anti-Instincts perspective)
- `overlap-analysis-unified-audit.md` (Unified Audit Gating perspective)
