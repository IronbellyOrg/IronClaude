---
high_severity_count: 3
medium_severity_count: 5
low_severity_count: 3
total_deviations: 11
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap introduces a `files_skipped` frontmatter field not present in the specification's WIRING_GATE required_frontmatter_fields or Section 6.3 frontmatter contract
- **Spec Quote**: `required_frontmatter_fields=["gate", "target_dir", "files_analyzed", "unwired_count", "orphan_count", "registry_count", "total_findings", "analysis_complete", "enforcement_scope", "resolved_gate_mode", "whitelist_entries_applied"]` (Section 4.4)
- **Roadmap Quote**: `a separate files_skipped: N frontmatter field provides visibility into degraded runs` (Phase 1, Milestone 1.2)
- **Impact**: The roadmap mandates a frontmatter field that is not in the gate's `required_frontmatter_fields` list. If the implementer adds it to the gate definition, it contradicts the spec's exact 11-field contract. If they don't add it to the gate definition but do emit it, the field exists but is unvalidated — inconsistent with the roadmap's framing as an observability mechanism. The spec explicitly states `analysis_complete` reflects degraded state but does not introduce a separate `files_skipped` field.
- **Recommended Correction**: Either (a) add `files_skipped` to the spec's `WIRING_GATE.required_frontmatter_fields` and Section 6.3 contract table, or (b) remove the `files_skipped` field from the roadmap and rely solely on `analysis_complete` as the spec intends. Option (b) is more conservative for v1.0.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: Roadmap extends whitelist scope to all three finding types; spec restricts whitelist to `unwired_callables` only
- **Spec Quote**: `unwired_callables: - symbol: "module.path.ClassName.param_name" ...` (Section 4.2.1, whitelist schema); `Whitelist mechanism: A wiring_whitelist.yaml file can list intentionally-optional callables` (Section 4.2.1)
- **Roadmap Quote**: `Extend to all three finding types in v1.0. Cost is ~10 LOC; prevents FPR mitigation gap.` (OQ-9)
- **Impact**: The spec's whitelist schema only defines `unwired_callables` as a key. Extending to orphan modules and unwired registries requires new schema keys, validation rules, and matching logic not specified. Implementers following the spec will build a single-type whitelist; implementers following the roadmap will build a three-type whitelist. This is a fundamental scope difference.
- **Recommended Correction**: If the three-type whitelist is desired, update the spec's Section 4.2.1 whitelist schema to include `orphan_modules` and `unwired_registries` keys with their own entry schemas. Also update Section 4.3.2 to clarify that `whitelist_entries_applied` counts across all three types.

### DEV-003
- **ID**: DEV-003
- **Severity**: HIGH
- **Deviation**: Roadmap excludes provider directory heuristic ("3+ files with common prefix") from v1.0; spec includes it as part of the orphan module algorithm
- **Spec Quote**: `1. Identify "provider directories" by convention: - directories named steps/, handlers/, validators/, checks/ - directories containing 3+ Python files with a common function prefix` (Section 4.2.2, Algorithm step 1)
- **Roadmap Quote**: `Exclude from v1.0. Named directory matching is sufficient and testable. Heuristic algorithm unspecified and untested.` (OQ-8)
- **Impact**: The spec's algorithm explicitly includes two provider directory identification methods. The roadmap unilaterally removes one. An implementer following the spec would implement the heuristic; an implementer following the roadmap would not. This is a functional requirement reduction that could cause missed orphan modules in non-conventionally-named directories.
- **Recommended Correction**: Update the spec's Section 4.2.2 Algorithm step 1 to remove the second bullet (`directories containing 3+ Python files with a common function prefix`) and note it as deferred to v1.1, or restore it in the roadmap.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap LOC estimate for `wiring_config.py` (80-120) significantly exceeds spec estimate (40-60)
- **Spec Quote**: `src/superclaude/cli/audit/wiring_config.py | CREATE | 40-60 | Configuration dataclass, patterns, whitelist loader` (Section 5)
- **Roadmap Quote**: `audit/wiring_config.py | 1 | +80-120 (new) | None` (Resource Requirements)
- **Impact**: The doubled estimate suggests the roadmap anticipates additional scope (likely the three-type whitelist from OQ-9) beyond what the spec defined. This is consistent with DEV-002 but represents an implicit scope expansion without explicit spec amendment.
- **Recommended Correction**: If the three-type whitelist is adopted, update the spec's LOC estimate for `wiring_config.py` to 80-120. If not, the roadmap estimate should revert to 40-60.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Roadmap LOC estimate for `wiring_gate.py` (200-280) is lower than spec estimate (250-300)
- **Spec Quote**: `src/superclaude/cli/audit/wiring_gate.py | CREATE | 250-300 | Core analysis engine, report emitter, gate definition` (Section 5)
- **Roadmap Quote**: `audit/wiring_gate.py | 1 | +200-280 (new) | None` (Resource Requirements)
- **Impact**: Minor misalignment in scope estimation. The lower bound dropped by 50 lines. Could lead to under-scoping if the spec's estimate reflects required complexity more accurately. However, this is an estimate, not a hard constraint.
- **Recommended Correction**: Align estimates. The spec's 250-300 range should be authoritative since it accounts for the full analysis engine, report emitter, and gate definition.

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: Roadmap references `sprint/config.py` as MODIFY in dependency map but spec also references it; however the roadmap's OQ-4 says it's "handled implicitly via sprint/models.py" while the spec's dependency map explicitly lists `sprint/config.py (MODIFY)`
- **Spec Quote**: `sprint/config.py (MODIFY)` (Section 11, Dependency Map)
- **Roadmap Quote**: `Handled implicitly via sprint/models.py where SprintConfig lives. Verify during Phase 2; not a blocker.` (OQ-4)
- **Impact**: The spec's dependency map shows `sprint/config.py` as a modified file, but the roadmap's Files Modified table does not list it. If SprintConfig actually lives in `sprint/models.py`, the spec's dependency map is wrong. If it lives in `sprint/config.py`, the roadmap's file manifest is incomplete. Either way, there's ambiguity about which file to modify.
- **Recommended Correction**: Determine where SprintConfig actually lives. Update the spec's dependency map or the roadmap's file manifest accordingly to eliminate ambiguity.

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: Roadmap defers `--skip-wiring-gate` CLI flag; spec explicitly includes it in Phase 2 rollout
- **Spec Quote**: `Override available via --skip-wiring-gate flag` (Section 8, Phase 2: Soft)
- **Roadmap Quote**: `Defer. Shadow mode provides non-interference. Flag adds complexity without v1.0 value.` (OQ-5)
- **Impact**: The spec's Phase 2 rollout plan explicitly offers this flag as an override mechanism. Deferring it means Phase 2 (soft mode) will lack the specified escape hatch. While Phase 2 is itself deferred beyond v1.0, the roadmap should acknowledge this as a deviation from the spec's rollout plan rather than silently dropping it.
- **Recommended Correction**: Note in the spec that `--skip-wiring-gate` is deferred to Phase 2 activation (not v1.0), or add it to the roadmap's Phase 5 soft-mode readiness milestone.

### DEV-008
- **ID**: DEV-008
- **Severity**: MEDIUM
- **Deviation**: Roadmap states `analysis_complete: true` even when files are skipped; spec says `analysis_complete field reflects degraded state`
- **Spec Quote**: `logs a warning; analysis_complete field reflects degraded state` (Section 9.1, parse error test case)
- **Roadmap Quote**: `analysis_complete: true with separate files_skipped: N frontmatter field. Degraded analysis is an observability event.` (OQ-3)
- **Impact**: The spec implies `analysis_complete` should be `false` (or otherwise reflect degradation) when parse errors occur. The roadmap explicitly overrides this to keep `analysis_complete: true` and use a separate field. This changes the semantic check behavior — `_analysis_complete_true` would pass even on degraded runs, which the spec's test case seems to preclude.
- **Recommended Correction**: Align the spec's Section 9.1 parse error test case with the roadmap's decision. If `analysis_complete` stays `true` on degraded runs, update the spec's test case description to reflect that the gate does NOT fail on parse errors and that `files_skipped` provides the observability signal instead.

### DEV-009
- **ID**: DEV-009
- **Severity**: LOW
- **Deviation**: Roadmap uses "FR: Goal-1a, Goal-1b" etc. requirement references that don't exist in the spec; spec uses numbered Goals (1-5) without sub-letter granularity
- **Spec Quote**: `1. Detect unwired injectable dependencies ... 2. Detect orphan modules ... 3. Detect unwired dispatch registries ... 4. Emit a structured YAML report ... 5. Deploy in shadow mode initially` (Section 2, Goals)
- **Roadmap Quote**: `FR: Goal-1a, Goal-1b` ... `FR: Goal-2a, Goal-2b, Goal-2c, Goal-2d` (Milestone 1.2)
- **Impact**: The roadmap's requirement traceability references are internally fabricated — the spec never defines Goal-1a, Goal-1b, etc. While the intent is clear, the traceability chain is broken since the cited requirements don't exist in the source document.
- **Recommended Correction**: Either add sub-goal decomposition to the spec (Section 2) or use the spec's actual identifiers (Goal 1, Goal 2, etc.) in the roadmap's requirement columns.

### DEV-010
- **ID**: DEV-010
- **Severity**: LOW
- **Deviation**: Roadmap references NFR-001 through NFR-008 but the spec never defines numbered NFR identifiers
- **Spec Quote**: Performance targets, coverage requirements, backward compatibility constraints are described in prose across Sections 7, 9, and scattered throughout (no NFR-NNN numbering)
- **Roadmap Quote**: `NFR-001, SC-009` (Milestone 4.3), `NFR-002` (Milestone 1.2), `NFR-003` (Phase 1 Acceptance), `NFR-004` (Milestone 2.1), `NFR-005` (Milestone 1.3), `NFR-006` (Milestone 2.2), `NFR-007` (Milestone 2.1), `NFR-008` (Milestone 1.1)
- **Impact**: Same traceability issue as DEV-009. The NFR identifiers are roadmap-internal constructs with no spec counterpart. Implementers cannot look up "NFR-006" in the spec.
- **Recommended Correction**: Either add explicit NFR identifiers to the spec or replace roadmap NFR references with spec section numbers.

### DEV-011
- **ID**: DEV-011
- **Severity**: LOW
- **Deviation**: Spec's `roadmap/gates.py` LOC estimate is `+40`; roadmap estimates `+35-50`
- **Spec Quote**: `src/superclaude/cli/roadmap/gates.py | MODIFY | +40 | _deviation_counts_reconciled semantic check` (Section 5)
- **Roadmap Quote**: `roadmap/gates.py | 3 | +35-50` (Resource Requirements)
- **Impact**: Trivial estimate variance. The spec uses a point estimate; the roadmap uses a range that encompasses it. No functional impact.
- **Recommended Correction**: None required — the range is compatible.

---

## Summary

**Severity distribution**: 3 HIGH, 5 MEDIUM, 3 LOW (11 total deviations)

The three HIGH-severity deviations cluster around scope decisions the roadmap made unilaterally:

1. **DEV-001**: Introduction of an unspecified `files_skipped` frontmatter field that conflicts with the spec's 11-field gate contract
2. **DEV-002**: Expanding whitelist scope from unwired-callables-only to all three finding types without updating the spec's schema
3. **DEV-003**: Removing the provider directory heuristic algorithm from v1.0 scope

These are all resolvable by updating the spec to match the roadmap's decisions (which appear well-reasoned), but the spec must be amended before the roadmap can be considered faithful. The roadmap cannot be used as a tasklist source until these three HIGH deviations are reconciled.

The MEDIUM deviations (DEV-004 through DEV-008) are primarily consequences of the HIGH deviations (LOC estimate drift from scope changes, `analysis_complete` semantics mismatch) plus one file-location ambiguity (`sprint/config.py` vs `sprint/models.py`).

The LOW deviations (DEV-009 through DEV-011) are traceability formatting issues — the roadmap fabricates requirement IDs (Goal-1a, NFR-001) that don't exist in the spec, breaking the traceability chain but not affecting correctness.
