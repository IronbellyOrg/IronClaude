---
title: "Round 3 — Final Arguments and Invariant Resolutions"
timestamp: 2026-03-18T00:00:00Z
round: 3
depth: deep
invariant_findings_resolved: 7
convergence_status: CONVERGED
---

# Adversarial Debate — Round 3: Final Arguments

## Invariant Resolutions

### INV-001: No shared utility for semantic checks to extract typed frontmatter values from raw string content

**Status**: RESOLVED
**Severity**: HIGH

**Problem**: Each `check_fn(content: str) -> bool` must independently parse YAML frontmatter from raw markdown. The existing `_check_frontmatter()` in `pipeline/gates.py:83` only validates field presence -- it does not return parsed values. Every semantic check function that needs to read a value (e.g., `rollout_mode`, `blocking_findings`, `total_findings`) must re-implement frontmatter extraction.

**Which variants address it**: None explicitly. All three variants define semantic check functions that implicitly must parse frontmatter, but none specify a shared extraction utility.

**Resolution**: Create a private helper `_extract_frontmatter_values(content: str) -> dict[str, str]` co-located with the semantic checks in `audit/wiring_gate.py`. This helper:

1. Uses the same `_FRONTMATTER_RE` regex pattern from `pipeline/gates.py:77` (imported or duplicated as a private constant -- duplication is acceptable because it is a 3-line regex and avoids creating a public API surface in pipeline/).
2. Returns a `dict[str, str]` mapping each key to its raw string value.
3. Each semantic check calls this helper once and casts values as needed (`int()`, string comparison).
4. This helper lives in `audit/wiring_gate.py`, not in `pipeline/*`, preserving the layering constraint (NFR-007).

**Why not modify `_check_frontmatter()`**: That function is in `pipeline/gates.py` which must remain domain-agnostic. Adding a value-extraction return type would change its contract, violating the "zero changes to pipeline/*" constraint.

**Impact on consensus**: Adds one private function (~15 LOC) to `audit/wiring_gate.py`. No spec changes required -- this is an implementation-level detail that all three specs implicitly require.

---

### INV-003: `_build_steps()` and `_get_all_step_ids()` are already desynchronized

**Status**: RESOLVED
**Severity**: HIGH

**Problem**: `_build_steps()` (line 344) returns a list ending at `spec-fidelity` (8 steps). `_get_all_step_ids()` (line 538) returns 11 IDs including `remediate` and `certify`. The new `wiring-verification` step must be inserted, but its position relative to the existing desynchronization is ambiguous.

**Evidence from code**:
- `_build_steps()` ends at line 473 with `spec-fidelity` -- returns 8 steps.
- `_get_all_step_ids()` at line 542 returns `["extract", ..., "spec-fidelity", "remediate", "certify"]` -- 11 IDs.
- `remediate` and `certify` exist as IDs in `_get_all_step_ids()` but are not constructed by `_build_steps()`. They are defined elsewhere (see lines 315-341) as standalone `Step` objects used conditionally by the remediation loop.

**Which variants address it**: Variant A (Section 9.3) explicitly notes that `_get_all_step_ids()` must be updated. Variant B (Section 5.6, Step 5) also mentions updating `_get_all_step_ids()`. Variant C does not mention it.

**Resolution**: Insert `"wiring-verification"` into both functions:

1. In `_build_steps()`: append the new `Step` after `spec-fidelity` (after line 473, before `return steps`).
2. In `_get_all_step_ids()`: insert `"wiring-verification"` after `"spec-fidelity"` and before `"remediate"` in the returned list.

The desynchronization between `_build_steps()` and `_get_all_step_ids()` is intentional -- `remediate` and `certify` are conditionally executed steps not part of the initial pipeline build. `wiring-verification` belongs in the unconditional pipeline, so it goes in both.

**Impact on consensus**: Confirms Variant A and B's approach. Adds explicit requirement to update both functions.

---

### INV-005: Semantic checks need typed value extraction but no shared parser exists

**Status**: RESOLVED (merged with INV-001)
**Severity**: HIGH

**Problem**: Identical root cause as INV-001. The `check_fn(content: str) -> bool` contract forces each check to re-parse frontmatter.

**Resolution**: Same as INV-001. The `_extract_frontmatter_values()` helper resolves both INV-001 and INV-005.

**Impact on consensus**: No additional changes beyond INV-001.

---

### INV-006: `resolve_gate_mode()` forces BLOCKING at release scope, defeating shadow mode

**Status**: RESOLVED
**Severity**: HIGH

**Problem**: `resolve_gate_mode()` at `trailing_gate.py:613` returns `GateMode.BLOCKING` unconditionally when `scope == GateScope.RELEASE`. If the roadmap pipeline operates at release scope, then `GateMode.TRAILING` set on the `Step` definition would be overridden, making shadow mode impossible. This could require changes to `pipeline/*` -- violating the "zero changes" constraint.

**Evidence from code**:
```python
# trailing_gate.py:613-615
if scope == GateScope.RELEASE:
    # Release gates are ALWAYS blocking -- enforced invariant
    return GateMode.BLOCKING
```

**Which variants address it**:
- Variant A (Section 4.3): Notes the constraint but does not show how to resolve it.
- Variant B (Section 5.6, R8): Explicitly calls this out: "resolve_gate_mode() forces BLOCKING" and sets `gate_mode=GateMode.TRAILING` on the Step, acknowledging that this relies on the executor honoring the Step-level mode rather than calling `resolve_gate_mode()`.
- Variant C: Sets `GateMode.TRAILING` on the Step without discussing the interaction.

**Resolution**: The executor at `pipeline/executor.py:160-163` resolves effective mode based on `config.grace_period`, not by calling `resolve_gate_mode()`:

```python
effective_mode = step.gate_mode
if config.grace_period == 0:
    effective_mode = GateMode.BLOCKING
```

This means `resolve_gate_mode()` is NOT called by the pipeline executor for individual steps. It exists as a policy-level function for callers who need scope-aware resolution. The actual gate mode is determined by:

1. `step.gate_mode` (set at Step construction) -- primary
2. `config.grace_period` override -- secondary

Therefore: setting `gate_mode=GateMode.TRAILING` on the Step definition works for shadow mode IF `config.grace_period > 0` (or is not explicitly zeroed). The risk is that a roadmap config with `grace_period=0` forces BLOCKING regardless.

**Design fix**: The wiring-verification step should be constructed with `gate_mode=GateMode.TRAILING`. The roadmap config should set a non-zero `grace_period` during shadow rollout. This requires no changes to `pipeline/*`.

However, the real safeguard comes from Variant A/B's mode-aware semantic check design: even if the gate runs in BLOCKING mode, the `_zero_blocking_findings_for_mode` check reads `rollout_mode=shadow` from frontmatter and returns `True` unconditionally. The report emitter sets `blocking_findings=0` in shadow mode. So the gate passes regardless of whether TRAILING or BLOCKING mode is effective.

This is the decisive argument for the A/B semantic check design over Variant C's per-category-zero approach. Under C's design, if `grace_period=0` forces BLOCKING, shadow mode breaks entirely because the zero-count checks would fail on any findings.

**Impact on consensus**: Adopts A/B's mode-aware semantic check design as mandatory. No `pipeline/*` changes needed. Documents the `grace_period` interaction as an operational requirement for shadow rollout.

---

### INV-008: Three-way count invariant (`category_sum == severity_sum == total_findings`)

**Status**: RESOLVED
**Severity**: HIGH

**Problem**: The report frontmatter encodes findings in two projections:
- By category: `unwired_callable_count + orphan_module_count + unwired_registry_count`
- By severity: `critical_count + major_count + info_count`

Both must equal `total_findings`. This dual-projection from the same finding list requires single-source computation to guarantee consistency.

**Which variants address it**:
- Variant A: Specifies both `finding_counts_consistent` and `severity_summary_consistent` checks but does not specify the computation mechanism.
- Variant B: Specifies both checks and provides the `WiringReport` dataclass with `total_findings` as a computed property (`len(unwired_callables) + len(orphan_modules) + len(unwired_registries)`).
- Variant C: Only checks category sum via `_total_findings_consistent`. Does not have severity-level counts, so the three-way invariant does not arise.

**Resolution**: Enforce single-source computation in `emit_report()`:

1. `WiringReport` stores findings in three typed lists (by category). This is the single source.
2. `total_findings` is a computed property: sum of list lengths. This guarantees category projection consistency.
3. Severity counts are computed by iterating the same lists: `critical_count = sum(1 for f in all_findings if f.severity == "critical")`, etc.
4. Both projections derive from the same `list[WiringFinding]` data, making the three-way invariant a tautology.
5. The semantic checks `_finding_counts_consistent` and `_severity_summary_consistent` validate the serialized form as a defense against report corruption or manual editing.

**Impact on consensus**: Requires `WiringReport` to compute severity counts as derived properties (not stored fields). The report emitter serializes these computed values. Both semantic checks remain as corruption detectors.

---

### INV-012: `retry_limit=0` semantics are ambiguous

**Status**: RESOLVED
**Severity**: HIGH

**Problem**: Does `retry_limit=0` mean "zero retries after initial attempt" (runs once) or "zero total attempts" (never executes)?

**Evidence from code** (`pipeline/executor.py:158`):
```python
max_attempts = step.retry_limit + 1  # retry_limit=1 means 2 attempts total
```

This is unambiguous. `retry_limit=0` means `max_attempts = 1` -- the step runs exactly once with no retries. The comment in the code explicitly documents this.

**Which variants address it**:
- Variants A and B: Use `retry_limit=0` with rationale "Deterministic; retry won't help."
- Variant C: Uses `retry_limit=1` without rationale.

**Resolution**: `retry_limit=0` is correct and unambiguous per the existing executor implementation. The step executes once. If the gate fails, no retry occurs. This is appropriate for a deterministic step where re-execution produces identical results.

Variant C's `retry_limit=1` would cause the same deterministic analysis to run twice on failure, wasting time. The only scenario where retry helps is transient filesystem errors, which are better handled by the analysis function itself (retry file reads, not the entire step).

**Winner**: Variants A and B. Use `retry_limit=0`.

**Impact on consensus**: Settles the `retry_limit` value at 0. No design change needed.

---

### INV-014: Nested `severity_summary` YAML block collides with flat key extraction in `_check_frontmatter()`

**Status**: RESOLVED
**Severity**: HIGH

**Problem**: Variant A's frontmatter includes a nested YAML block:

```yaml
severity_summary:
  critical: 3
  major: 0
  info: 0
```

The existing `_check_frontmatter()` at `pipeline/gates.py:100-107` extracts keys by splitting on `:`:

```python
for line in frontmatter_text.splitlines():
    line = line.strip()
    if ":" in line:
        key = line.split(":", 1)[0].strip()
        if key:
            found_keys.add(key)
```

This would extract `severity_summary`, `critical`, `major`, and `info` as top-level keys. If the report also has top-level `critical_count`, `major_count` fields, there is no collision because the nested keys have different names. However, the `_FRONTMATTER_RE` regex pattern `r"^---[ \t]*\n((?:[ \t]*\w[\w\s]*:.*\n)+)---[ \t]*$"` expects each line to match `\w[\w\s]*:.*`. Indented nested keys (`  critical: 3`) would match because the pattern starts with `[ \t]*\w` -- the leading whitespace is consumed by `[ \t]*` and `critical` matches `\w`.

The real problem is that `_check_frontmatter()` treats nested keys as top-level. So `required_frontmatter_fields=["critical"]` would pass due to the nested `critical: 3` line, even if there is no top-level `critical` field. This creates false-positive field presence validation.

**Which variants address it**:
- Variant A: Uses nested `severity_summary` block AND separate top-level `critical_count`, `major_count`, `info_count` fields. The nested keys (`critical`, `major`, `info`) have different names from the top-level keys (`critical_count`, etc.), so there is no collision for required field validation. However, semantic checks that extract values by key name would get incorrect values if they search for `critical` and find the nested one.
- Variant B: Flattens severity into top-level fields only (`critical_count`, `major_count`). No nested block. Avoids the problem entirely.
- Variant C: No severity fields at all. Avoids the problem entirely.

**Resolution**: Adopt Variant B's flat frontmatter approach. Do not use nested YAML blocks in gate-validated frontmatter.

Rationale:
1. The existing `_check_frontmatter()` was designed for flat key-value frontmatter. Nested blocks interact unpredictably with the regex-based extraction.
2. The `_extract_frontmatter_values()` helper (from INV-001) would also need nested-key awareness if nested blocks are used, adding complexity.
3. Flat fields (`critical_count: 3`, `major_count: 0`, `info_count: 0`) convey the same information without interaction risks.
4. The `severity_summary` nested block is redundant when flat severity fields exist.

**Impact on consensus**: Removes `severity_summary` nested block from frontmatter schema. Uses flat `critical_count`, `major_count`, `info_count` fields (per Variant B). The `_severity_summary_consistent` semantic check validates `critical_count + major_count + info_count == total_findings` using flat field extraction.

---

## Final Per-Point Scoring Matrix

### Contradictions (X-NNN)

| Diff Point | Winner | Confidence | Evidence |
|-----------|--------|------------|----------|
| X-001: Gate constant location | **B/C** (`audit/wiring_gate.py`) | 85% | Co-locating gate with analysis engine improves cohesion. The gate's semantic checks reference analysis-specific concepts (rollout mode, wiring categories). Placing the gate in `roadmap/gates.py` would create a dependency from `roadmap/gates.py` on `audit/wiring_gate.py` for the check functions, which is worse than `roadmap/executor.py` importing `WIRING_GATE` from `audit/`. Existing precedent: `SPEC_FIDELITY_GATE` lives in `roadmap/gates.py` because its checks are roadmap-specific. `WIRING_GATE` checks are audit-specific. Import into `roadmap/gates.py:ALL_GATES` for registry purposes (per B). |
| X-002: Semantic check philosophy | **A/B** (mode-aware) | 95% | Per INV-006 analysis, the mode-aware approach is the only design that survives `grace_period=0` forcing BLOCKING. C's per-category-zero checks break shadow mode under this condition. The `blocking_findings` field computed per mode is the essential bridge between rollout policy and gate enforcement within the `check_fn(content) -> bool` constraint. |
| X-003: `audit_artifacts_used` type | **A/B** (integer) | 90% | Integer count is strictly more informative than boolean. Tells you HOW MANY audit artifacts contributed, not just whether any did. |
| X-004: Output file name | **A/B** (`wiring-verification.md`) | 80% | Consistent with step ID `wiring-verification`. C's `wiring-report.md` diverges from the ID convention. |
| X-005: Step retry policy | **A/B** (`retry_limit=0`) | 95% | Per INV-012, the executor treats `retry_limit=0` as exactly 1 attempt. Deterministic analysis produces identical results on retry. |
| X-006: `WiringReport.passed` semantics | **B** (acknowledged mismatch) | 75% | B acknowledges that `report.passed` (zero findings) differs from "gate passed" (mode-dependent). This semantic gap is acceptable because the report object represents analysis truth while the gate represents enforcement policy. Document it, do not try to unify them. |
| X-007: Modification of `roadmap/gates.py` | **B** (import only) | 85% | Gate definition lives in `audit/wiring_gate.py` (per X-001). `roadmap/gates.py` adds only an import and `ALL_GATES` entry. C's deviation reconciliation is a separate feature and should not be bundled. |
| X-008: Audit-analyzer field design | **B** (single "Wiring path" field) | 70% | B's chain-oriented field ("Declaration -> Registration -> Invocation") is more actionable than A/C's 4-5 separate fields. A single structured field forces the analyzer to trace the full chain, making broken links immediately visible. However, A/C's approach is more machine-parseable. Slight edge to B for audit-analyzer ergonomics. |
| X-009: Sprint output path | **B** (`work_dir / task_id`) | 75% | Co-locating sprint wiring reports with task output is simpler than creating a separate `.sprint-state/wiring/` directory structure. |
| X-010: Minimum unit test count | **B** (20 minimum) | 70% | The higher count reflects the need to test mode-aware semantic checks (shadow/soft/full) which add test cases not present in C's simpler design. |
| X-011: Deviation count reconciliation | **Defer** (out of scope) | 90% | C's companion feature is valuable but should not be bundled with the wiring gate release. Separate release prevents scope creep and merge conflicts. Track as independent task. |

### Content Differences (C-NNN) -- High Severity Only

| Diff Point | Winner | Confidence | Evidence |
|-----------|--------|------------|----------|
| C-002: Sprint integration scope | **B/C** (include sprint) | 80% | Sprint integration enables shadow-mode data collection at the task level, which is essential for calibrating FPR before soft/full rollout. The incremental cost is ~28 LOC (post-task hook) + 3 LOC (config field). However, sprint integration should be Phase 1 shadow-only to limit risk. |
| C-004: ToolOrchestrator AST plugin | **B** (include in v1, full impl) | 65% | B provides the only implementation-level design. The AST plugin improves cleanup-audit accuracy by populating the empty `references` field. However, this is the highest-risk addition (new module, new integration surface). Recommendation: include in scope but schedule as a parallel track that can be cut without blocking the core wiring gate. |
| C-006: Semantic check design | **A/B** (mode-aware) | 95% | Decisive per INV-006 analysis. Mode-aware enforcement via `blocking_findings` is the only approach that works within the `check_fn(content) -> bool` contract while supporting shadow mode under all executor configurations. |
| C-021: Dual/triple mode taxonomy | **B** (named modes A/B/C) | 75% | Explicit named modes improve specification clarity. Mode A (roadmap), Mode B (sprint), Mode C (cleanup-audit) can each be scoped and tested independently. |

### Unique Contributions

| Diff Point | Winner | Confidence | Evidence |
|-----------|--------|------------|----------|
| U-001: A's insertion point rationale | **Adopt** from A | 85% | Valuable architectural reasoning that should be preserved in the merged spec's design rationale section. |
| U-002: A's report body sections | **Adopt** from A | 80% | Prescribing body sections ensures human-readable reports have consistent structure. |
| U-003: A's rejected option doc | **Adopt** from A | 60% | Good practice but lower priority. Include in decision table. |
| U-004: A's suppression expiry | **Defer** to v1.1 | 70% | Useful for suppression hygiene but adds complexity to whitelist schema. |
| U-006: B's "What changed" section | **Adopt** from B | 85% | Lineage traceability is valuable for spec evolution tracking. |
| U-007: B's ToolOrchestrator impl | **Adopt** from B | 65% | See C-004 scoring. Include as parallel track. |
| U-008: B's YAML injection prevention | **Adopt** from B | 90% | Security hardening with minimal cost. Elevate to MUST requirement. |
| U-009: B's pre-activation checklist | **Adopt** from B/C | 85% | Both B and C include this. Essential for preventing silent misconfiguration. |
| U-010: B's `blocking_findings` computation | **Adopt** from B | 95% | This is the keystone of mode-aware enforcement. Without this explicit mapping, the rollout model is underspecified. |
| U-012: C's deviation reconciliation | **Defer** (separate release) | 90% | Valuable but orthogonal. Prevents scope creep. |
| U-013: C's coordination notes | **Adopt** from C | 85% | Operational awareness of merge-conflict risks with Anti-Instincts and Unified Audit Gating. |
| U-014: C's FPR calibration formula | **Adopt** from C | 80% | `measured_FPR + 2 sigma` is more rigorous than B's simple percentage threshold. |

---

## Consensus Spec Definition

Based on the above resolutions, the merged specification adopts:

### From Variant A
- Insertion point rationale ("Why `_build_steps()` is the correct insertion point")
- Report body section requirements (7 sections)
- Suppression expiry concept (deferred to v1.1 backlog)
- Rejected option documentation in decision table
- Resume behavior discussion

### From Variant B (Primary)
- Gate constant location: `audit/wiring_gate.py`
- Mode-aware semantic check design with `blocking_findings` computation
- Flat frontmatter (no nested `severity_summary`)
- `ToolOrchestrator` AST analyzer plugin (parallel track)
- YAML injection prevention as MUST requirement
- Pre-activation checklist
- Named operation modes (A/B/C)
- `retry_limit=0`, `timeout_seconds=60`
- Output filename: `wiring-verification.md`
- `audit_artifacts_used: int`
- `whitelist_entries_applied` in frontmatter
- Forensic cross-reference appendix
- "What changed" lineage section
- 20 minimum unit tests

### From Variant C
- Deviation count reconciliation (deferred to separate release)
- Coordination notes section (merge-conflict risk awareness)
- FPR calibration formula (`measured_FPR + 2 sigma`)
- `WiringConfig` dataclass (concrete config model)
- Explicit task decomposition with parallel tracks

### Rejected
- Variant A's `WIRING_VERIFICATION_GATE` naming (use `WIRING_GATE`)
- Variant A's placement of gate constant in `roadmap/gates.py`
- Variant A's nested `severity_summary` frontmatter block
- Variant A's exclusion of sprint integration
- Variant C's per-category-zero semantic checks
- Variant C's `enforcement_mode` naming (use `rollout_mode`)
- Variant C's `retry_limit=1`
- Variant C's `wiring-report.md` filename
- Variant C's `audit_artifacts_used: bool`
- Variant C's bundling of deviation count reconciliation

---

## Convergence Assessment

| Metric | Value |
|--------|-------|
| Invariant findings addressed | 7/7 |
| Invariant findings resolved | 6/7 (INV-005 merged with INV-001) |
| Contradiction points resolved | 11/11 |
| High-severity content diffs resolved | 4/4 |
| Unique contributions dispositioned | 14/14 |
| Points with clear winner | 29/30 |
| Points requiring investigation | 0 |
| Alignment | 97% |
| **Status** | **CONVERGED** |

### Remaining Operational Risks (Accepted)

1. **INV-006 operational dependency**: Shadow mode requires `config.grace_period > 0` OR relies on mode-aware semantic checks to pass even under BLOCKING. The semantic check safeguard is sufficient, but operators should be aware of the interaction. Severity: LOW (accepted risk).

2. **ToolOrchestrator integration cut risk**: The AST analyzer plugin (from Variant B) is the highest-risk addition. If it threatens the critical path, it can be deferred to v1.1 without affecting core wiring gate functionality. Severity: LOW (mitigated by parallel track scheduling).

3. **Frontmatter regex robustness**: The `_FRONTMATTER_RE` regex and flat key extraction approach works for the specified frontmatter schema. Future additions of nested YAML blocks would require parser upgrades. Severity: LOW (documented constraint).

### Convergence Blockers Cleared

All 7 HIGH-severity invariant findings are resolved:

| INV | Resolution | Mechanism |
|-----|-----------|-----------|
| INV-001 | Private `_extract_frontmatter_values()` helper | New ~15 LOC function in `audit/wiring_gate.py` |
| INV-003 | Insert `wiring-verification` in both `_build_steps()` and `_get_all_step_ids()` | Desync is intentional; new step belongs in both |
| INV-005 | Merged with INV-001 | Same helper resolves both |
| INV-006 | Mode-aware semantic checks + `blocking_findings` computation | Survives `grace_period=0` forcing BLOCKING |
| INV-008 | Single-source computation from typed finding lists | Category and severity counts derived from same data |
| INV-012 | `retry_limit=0` means exactly 1 attempt | Confirmed by `executor.py:158`: `max_attempts = retry_limit + 1` |
| INV-014 | Flat frontmatter, no nested YAML blocks | Avoids regex/extraction interaction entirely |
