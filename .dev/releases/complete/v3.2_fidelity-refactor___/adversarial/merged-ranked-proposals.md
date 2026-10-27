# Spec-Fidelity Resolution: Validated Proposal

## Winner: Amend Spec (Variant A)

**Score**: 0.935 / 1.000 — decisive margin over alternatives.

## Required Spec Amendments

Apply these 3 edits to `wiring-verification-gate-v1.0-release-spec.md`, then `--resume` the pipeline.

### Amendment 1: Add `files_skipped` to gate contract (resolves DEV-001)

**Target**: Section 4.4 (`required_frontmatter_fields`) and Section 6.3 (frontmatter contract table)

**Change to §4.4**: Add `"files_skipped"` to `WIRING_GATE.required_frontmatter_fields` list (12th field).

**Change to §6.3**: Add row to frontmatter contract table:
```
| files_skipped | int | >= 0; count of Python files that failed AST parsing |
```

**Rationale** (OQ-3): Failing the gate on unrelated parse errors makes shadow mode unreliable. `analysis_complete: true` with `files_skipped: N` provides observability without false gate failures.

### Amendment 2: Extend whitelist schema to all 3 finding types (resolves DEV-002)

**Target**: Section 4.2.1 (whitelist schema)

**Change**: Add `orphan_modules` and `unwired_registries` keys to the whitelist YAML schema:
```yaml
# wiring_whitelist.yaml
unwired_callables:
  - symbol: "module.path.ClassName.param_name"
    reason: "string"
orphan_modules:
  - symbol: "module.path.function_name"
    reason: "string"
unwired_registries:
  - symbol: "registry.key.name"
    reason: "string"
```

**Also update §4.3.2**: Clarify that `whitelist_entries_applied` counts across all three finding types.

**Rationale** (OQ-9): The spec defines 3 analysis functions. Having whitelist support for only 1 creates an FPR mitigation gap for orphan modules and registries. Cost is ~10 LOC.

### Amendment 3: Remove heuristic from orphan module algorithm (resolves DEV-003)

**Target**: Section 4.2.2, Algorithm step 1

**Change**: Remove the second bullet from provider directory identification:
```
Before:
1. Identify "provider directories" by convention:
   - directories named steps/, handlers/, validators/, checks/
   - directories containing 3+ Python files with a common function prefix

After:
1. Identify "provider directories" by convention:
   - directories named steps/, handlers/, validators/, checks/

   Note: Heuristic detection (3+ files with common prefix) deferred to v1.1
   pending algorithm specification and test case definition.
```

**Rationale** (OQ-8): The heuristic has no algorithm specification, no edge case definitions, and no test cases. Named directory matching is sufficient and fully testable for v1.0.

## Expected Cascade Effects

The 3 amendments should auto-resolve these MEDIUM deviations:
- **DEV-004** (LOC estimate mismatch for `wiring_config.py`): 3-type whitelist justifies 80-120 LOC estimate
- **DEV-008** (`analysis_complete` semantics): Spec now explicitly defines degraded-run behavior matching roadmap

## Execution Steps

1. Apply 3 amendments to the spec
2. Run: `superclaude roadmap run <spec.md> --resume`
3. Verify `high_severity_count: 0` in regenerated spec-fidelity output
