# Overlap Analysis: Unified Audit Gating (Primary) vs. Wiring Verification vs. Anti-Instincts

**Date**: 2026-03-17
**Analyst context**: Evidence-based comparison of three specification files
**Primary file**: Unified Audit Gating v1.2.1 (spec-refactor-plan-merged.md)

---

## 3x3 Overlap Matrix

| | Wiring Verification | Anti-Instincts | Unified Audit Gating |
|---|---|---|---|
| **Wiring Verification** | N/A (self) | 4/10 (40%) | 5/10 (50%) |
| **Anti-Instincts** | 4/10 (40%) | N/A (self) | 3/10 (30%) |
| **Unified Audit Gating** | 5/10 (50%) | 3/10 (30%) | N/A (self) |

---

## Detailed Overlap Justification

---

### Wiring Verification <-> Anti-Instincts: 4/10 (40%)

These two specs address the same root cause (the cli-portify no-op bug) but operate at different pipeline stages and detect different things. The overlap is real but partial.

#### Overlap Instance 1: Unwired Registry Detection vs. Integration Contract Extraction

**Wiring Verification** (Section 4.2.3):
> "Detect dictionary constants with naming patterns indicating dispatch registries (`REGISTRY`, `DISPATCH`, `RUNNERS`, `HANDLERS`, `ROUTER`) whose values reference functions that cannot be resolved via import."

**Anti-Instincts** (Section 5, `integration_contracts.py`):
> "An integration contract is any place where a data structure maps identifiers to callables, a constructor accepts injectable dependencies, an explicit wiring step is described, or a lookup/dispatch mechanism is defined."

Both detect missing dispatch table/registry wiring. However:
- **Wiring Verification** operates on **production Python code** (AST analysis of actual source files) and detects registries whose values are unresolvable at import time.
- **Anti-Instincts** operates on **spec and roadmap text** (regex on natural language documents) and detects whether the roadmap contains an explicit wiring task for each integration mechanism found in the spec.

**Why partially redundant**: If both are deployed, a missing dispatch table would be caught twice -- once at roadmap generation time (Anti-Instincts) and again at code implementation time (Wiring Verification). This is defense-in-depth, not pure waste, but there is genuine overlap in the detection target.

**Which is more complete**: Neither subsumes the other. Anti-Instincts catches the problem earlier (before code is written). Wiring Verification catches the problem more precisely (actual code analysis vs. natural language regex). Both are warranted if the goal is layered defense.

#### Overlap Instance 2: Unwired Callable Detection vs. Callback Injection Detection

**Wiring Verification** (Section 4.2.1):
> "Detect constructor parameters typed `Optional[Callable]` (or `Callable | None`) with default `None` that are never explicitly provided at any call site in the codebase."

**Anti-Instincts** (Section 5, DISPATCH_PATTERNS Category 3):
> `re.compile(r'\b(?:accepts?|takes?|requires?|expects?)\s+(?:a\s+)?(?:Callable|Protocol|ABC|Interface|Factory|Provider|Registry)\b')`

Both target the pattern where a constructor accepts an injectable callable that is never provided. Again:
- **Wiring Verification** does this on real Python AST (precise, code-level).
- **Anti-Instincts** does this on spec/roadmap text (early, but heuristic).

**Why partially redundant**: Same detection target, different pipeline stages. If Anti-Instincts catches the missing wiring task in the roadmap, the code should never be written without the injection -- making Wiring Verification's detection of the same pattern theoretically unnecessary. In practice, the code-level check remains valuable as a last-resort backstop.

**Which is more complete**: Wiring Verification is more precise (zero false positives on true unwired callables). Anti-Instincts is more preventive (catches before code exists).

#### Overlap Instance 3: Shared Forensic Root Cause

**Wiring Verification** (Section 1):
> "The cli-portify executor no-op bug (forensic report, 2026-03-17) demonstrated that Link 3 of the fidelity chain (Tasklist -> Code) has zero programmatic coverage."

**Anti-Instincts** (Section 2):
> "Three release specs (v2.24, v2.24.1, v2.25) specified [...] Three-way dispatch [...] PROGRAMMATIC_RUNNERS dictionary [...] Zero mentions of PROGRAMMATIC_RUNNERS"

Both specs were motivated by the same incident and cite the same forensic evidence. This is not functional overlap but increases the risk of contradictory design decisions if the specs evolve independently.

#### Why the score is 4/10 (not higher)

The remaining 60% is genuinely distinct:
- Wiring Verification's orphan module analysis (Section 4.2.2) has no counterpart in Anti-Instincts.
- Anti-Instincts' obligation scanner (Section 4, scaffold/discharge detection) has no counterpart in Wiring Verification.
- Anti-Instincts' fingerprint coverage (Section 6) has no counterpart in Wiring Verification.
- Anti-Instincts' spec structural audit (Section 7) has no counterpart in Wiring Verification.
- Anti-Instincts' prompt modifications (Section 10) have no counterpart in Wiring Verification.
- Wiring Verification operates on code; Anti-Instincts operates on documents. They are fundamentally at different pipeline stages.

---

### Wiring Verification <-> Unified Audit Gating: 5/10 (50%)

The Unified Audit Gating spec-refactor-plan incorporates behavioral gate extensions (Plan A) that directly reference and partially duplicate Wiring Verification's scope.

#### Overlap Instance 1: Smoke Test Gate G-012 vs. Wiring Verification Gate

**Unified Audit Gating** (SS13.3 / New Section 13):
> "Smoke Test Gate (G-012) -- A release-tier blocking gate that invokes the CLI against a minimal test fixture and validates that real artifacts with substantive content are produced."
> Checks: "Timing: elapsed < SMOKE_NOOP_CEILING_S (5s)" / "Intermediate artifact absence" / "Content evidence (fixture proper nouns)"

**Wiring Verification** (Section 2, Goals):
> "Detect unwired injectable dependencies [...] Detect orphan modules [...] Detect unwired dispatch registries [...] Emit a structured YAML report compatible with the GateCriteria/SemanticCheck pattern"

**Why partially redundant**: Both aim to prevent the no-op pipeline from passing. G-012 detects no-ops at runtime (actual execution produces no artifacts). Wiring Verification detects no-ops statically (code analysis reveals unwired dependencies). If Wiring Verification catches the unwired callable, the smoke test gate would never encounter the no-op. Conversely, if the smoke test fails, it indicates a wiring problem that Wiring Verification should have caught.

**Which is more complete**: They complement each other. Wiring Verification is a root-cause detector (identifies the specific unwired symbol). G-012 is a symptom detector (catches the behavioral consequence). Neither fully replaces the other, but deploying both for the same failure class is partially redundant.

#### Overlap Instance 2: Defect Fix Prerequisites (P0-A) vs. Wiring Verification Scope

**Unified Audit Gating** (SS12.3, Blocker 9 / Top 5 Immediate Action 0c):
> "P0-A defect fix scheduling -- Defect 1 (`step_runner` wiring) and Defect 2 (`validate_portify_config()` call) must be scheduled as separate work items"

**Wiring Verification** (Section 4.2.1, Pattern matched):
> "Constructor parameter `step_runner: Optional[Callable] = None` is never provided at any of 1 call sites."

The Unified Audit Gating spec identifies `step_runner` wiring as a prerequisite defect fix (blocker 9). Wiring Verification builds an entire static analysis gate around detecting exactly this class of bug. If Wiring Verification is deployed, the specific `step_runner` defect is one of its test cases (SC-010). The Unified Audit Gating spec treats it as a manual fix item, not as a gate-detected issue.

**Why partially redundant**: Both address the exact same `step_runner` unwiring, but with different remediation strategies. Unified Audit Gating says "schedule the fix manually." Wiring Verification says "build a gate to detect this class of bug automatically."

**Which is more complete**: Wiring Verification is more complete for this specific concern -- it generalizes the fix into a reusable gate rather than treating it as a one-off defect.

#### Overlap Instance 3: Spec Fidelity D-03/D-04 vs. Deviation Count Reconciliation

**Unified Audit Gating** (SS13.4 / New Section 13):
> "Check D-03 -- Named dispatch table preservation: `_DISPATCH_TABLE_PATTERN` regex finds `UPPER_CASE_NAME = {` or `dict(` in spec; verifies each found name appears anywhere in roadmap text."
> "Check D-04 -- Pseudocode dispatch function name preservation"

**Wiring Verification** (Section 4.6):
> "Deviation Count Reconciliation Gate [...] Parse frontmatter for `high_severity_count`, `medium_severity_count`, `low_severity_count`. Regex-scan body for `DEV-\d{3}` entries [...] Compare body counts to frontmatter counts."

These are distinct checks (D-03/D-04 check spec-to-roadmap dispatch table preservation; deviation reconciliation checks report-internal consistency). However, both modify `roadmap/gates.py` and add semantic checks to the fidelity gate infrastructure, creating implementation-level overlap in the same file.

**Why partially redundant**: The implementation overlap is shallow (both add to `SPEC_FIDELITY_GATE.semantic_checks` in `roadmap/gates.py`), but the detection targets are different. The redundancy is in the modification site, not in the functional purpose.

#### Overlap Instance 4: Shadow/Soft/Full Rollout Pattern

**Unified Audit Gating** (SS7.1, SS7.2):
> Defines a shadow -> soft -> full rollout with configurable profiles, override governance, and rollback triggers for the audit gate system.

**Wiring Verification** (Section 8):
> "Phase 1: Shadow [...] Phase 2: Soft [...] Phase 3: Full"
> "Decision Criteria: Shadow -> Soft Threshold [...] Soft -> Full Threshold"

Both use the identical shadow->soft->full rollout pattern. The Unified Audit Gating spec defines this as a general framework; Wiring Verification defines it independently for its specific gate. If Wiring Verification is deployed within the Unified Audit Gating framework, its rollout should use the framework's infrastructure rather than defining its own thresholds and override mechanisms.

**Why partially redundant**: Wiring Verification's rollout plan (Section 8) duplicates rollout mechanics that the Unified Audit Gating framework already provides. The thresholds differ (Wiring Verification uses FPR/TPR metrics; Unified Audit Gating uses profile-based thresholds), which could lead to contradictory enforcement behavior.

**Which is more complete**: Unified Audit Gating's rollout framework is more complete (configurable profiles, override governance, rollback triggers, KPI calibration). Wiring Verification's rollout plan should be adapted to use the framework rather than standing alone.

#### Why the score is 5/10 (not higher)

The remaining 50% is genuinely distinct:
- Wiring Verification's core value (AST-based static analysis of Python code) is not addressed anywhere in the Unified Audit Gating spec.
- Wiring Verification's orphan module detection and unwired registry analysis are unique.
- Unified Audit Gating's state machine (AuditWorkflowState, AuditLease, transition validator) has no counterpart in Wiring Verification.
- Unified Audit Gating's TUI display, sprint integration model, and per-scope gate evaluation are distinct concerns.

---

### Anti-Instincts <-> Unified Audit Gating: 3/10 (30%)

The overlap here is lower because the two specs operate at different layers. Anti-Instincts is a roadmap-generation quality gate; Unified Audit Gating is a sprint-execution audit framework.

#### Overlap Instance 1: D-03/D-04 Deterministic Checks in Both Specs

**Unified Audit Gating** (SS13.4 / New Section 13):
> "Check D-03 -- Named dispatch table preservation"
> "Check D-04 -- Pseudocode dispatch function name preservation"
> "Gate: Extension to existing `SPEC_FIDELITY_GATE` in `roadmap/gates.py`"

**Anti-Instincts** (Section 6, `fingerprint.py`):
> "Goes beyond formal requirement IDs to extract 'structural fingerprints' -- function names, class names, data structure names [...] Verifies each fingerprint appears in the roadmap."

D-03 and D-04 in the Unified Audit Gating spec overlap with Anti-Instincts' fingerprint coverage module. Specifically:
- D-03 checks that `UPPER_CASE_NAME = {` patterns from the spec appear in the roadmap. Anti-Instincts' `fingerprint.py` extracts `ALL_CAPS` constants (Section 6: `r'\b([A-Z][A-Z_]{3,})\b'`) and checks their presence in the roadmap.
- D-04 checks that `_run_*()` function names from spec code fences appear in the roadmap. Anti-Instincts' `fingerprint.py` extracts backtick-delimited identifiers and code-block function definitions, checking roadmap presence.

**Why partially redundant**: D-03/D-04 are a strict subset of the fingerprint coverage check. Anti-Instincts' fingerprint module checks ALL code-level identifiers with a 70% coverage threshold. D-03/D-04 check two specific patterns (dispatch tables and dispatch functions) with a presence/absence binary. If Anti-Instincts is deployed, D-03 and D-04 are redundant -- they would never catch something that the fingerprint module misses, because the fingerprint module casts a wider net.

**Which is more complete**: Anti-Instincts' fingerprint module is strictly more general. D-03/D-04 are narrower, purpose-built checks that could exist as special cases within the fingerprint module. However, D-03/D-04 provide more specific failure messages ("dispatch_tables_preserved: false" vs. generic "fingerprint coverage below 0.7"), which has diagnostic value.

#### Overlap Instance 2: Integration Contract Coverage vs. Integration Wiring Dimension

**Anti-Instincts** (Section 5, `integration_contracts.py`):
> Extracts integration contracts from spec text and verifies each has a corresponding explicit task in the roadmap.

**Unified Audit Gating** (SS13.4 referencing P02):
> D-03 and D-04 are described as extensions to `SPEC_FIDELITY_GATE`. The Unified Audit Gating spec does NOT include Anti-Instincts' full integration contract extraction. However, the general concern (verifying spec integration points are preserved in the roadmap) is shared.

**Why partially redundant**: The intent overlaps -- both want to ensure spec-defined integration mechanisms survive into downstream artifacts. But the implementations differ: Anti-Instincts uses a comprehensive 7-category pattern library with explicit wiring-task verification; Unified Audit Gating uses two narrow regex checks (D-03/D-04) focused specifically on dispatch tables and function names.

**Which is more complete**: Anti-Instincts is significantly more complete for integration contract verification. D-03/D-04 are a minimal viable subset.

#### Overlap Instance 3: Shared Reference to `SPEC_FIDELITY_GATE` in `roadmap/gates.py`

Both specs plan to modify `roadmap/gates.py`:
- Anti-Instincts adds `ANTI_INSTINCT_GATE` with 3 semantic checks and updates `ALL_GATES`.
- Unified Audit Gating adds D-03/D-04 as semantic checks on `SPEC_FIDELITY_GATE`.

This is implementation-site overlap. Both specs modify the same file with checks that partially overlap in purpose (dispatch table/function name preservation). This creates a merge conflict risk if both are implemented independently.

#### Why the score is 3/10 (not higher)

The remaining 70% is genuinely distinct:
- Anti-Instincts' obligation scanner (scaffold/discharge detection) has no counterpart in Unified Audit Gating.
- Anti-Instincts' spec structural audit (extraction quality guard) has no counterpart in Unified Audit Gating.
- Anti-Instincts' prompt modifications have no counterpart in Unified Audit Gating.
- Unified Audit Gating's state machine, transition validator, audit lease, profile system, TUI display, and sprint-level orchestration are entirely absent from Anti-Instincts.
- Unified Audit Gating's Silent Success Detection (P05) and Smoke Test Gate (G-012) are behavioral checks that have no counterpart in Anti-Instincts (which is purely a document-quality gate).
- The two specs target different pipeline stages: Anti-Instincts runs during roadmap generation; Unified Audit Gating runs during sprint execution.

---

## Summary of Actionable Overlap

| Overlap | Risk Level | Recommendation |
|---------|-----------|----------------|
| D-03/D-04 (Unified Audit) duplicates fingerprint coverage (Anti-Instincts) | **Medium** | If Anti-Instincts ships first, D-03/D-04 become redundant. Consider making D-03/D-04 conditional on Anti-Instincts gate not being present. |
| Unwired registry detection (Wiring Verification) overlaps integration contract extraction (Anti-Instincts) | **Low** | Different pipeline stages (code vs. documents). Defense-in-depth is warranted. No action needed unless budget is constrained. |
| Shadow/soft/full rollout (Wiring Verification) duplicates Unified Audit Gating framework | **Medium** | Wiring Verification should use Unified Audit Gating's rollout infrastructure rather than defining independent thresholds. |
| `step_runner` defect fix (Unified Audit) is a special case of Wiring Verification's detection | **Low** | Not contradictory -- the manual fix is immediate; the gate is long-term prevention. Both are warranted. |
| Both Anti-Instincts and Unified Audit Gating modify `roadmap/gates.py` | **Medium** | Coordinate implementation order to avoid merge conflicts. |
